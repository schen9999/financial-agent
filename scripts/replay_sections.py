#!/usr/bin/env python3
"""Frozen-input replay of the two locally served sections (Financial Health,
Risk Factors) against a vLLM OpenAI-compatible endpoint.

Isolates the served weights from live-input drift: every arm sees the
byte-identical context the committed v924f run saw, rebuilt from its
findings files, and the byte-identical prompt the pipeline builds.

- Context: the "Retrieved source context" block of
  <findings-dir>/<T>_local-model.md is parsed back into the trimmed stock /
  news / SEC dicts and the two RAG strings, re-rendered the way
  grounding_check.py renders it, and required to match the file byte for
  byte (and its context_sha256) before anything is sent.
- Prompt: built by the pipeline's own agent.core._haiku_section, with
  _section_llm swapped for a capture object for the duration of the call;
  no prompt text lives in this script. Section contexts follow
  grounding_check.run_arm: Financial Health gets _data_context(stock, news,
  sec); Risk Factors gets the RAG risk text, or that same context when RAG
  returned nothing.
- Request: agent.tools.local_model.LocalChat's own sampling_params()
  (temperature 0.1, max_tokens, the pinned top_p/top_k/repetition_penalty/
  min_p), plus a per-request `seed`, identical across arms for the same
  (ticker, section, sample), so arms are paired draw for draw.

No Anthropic calls, no judge. Writes one file per (ticker, sample):
  <out>/<arm>/<T>-s<k>.md  with context sha256, prompt sha256s, seeds,
  sampling, the endpoint's model id and finish reasons, the stock dict, and
  each section's raw output between replay-section markers.

Run inside the app image so agent/ is exactly the code the eval pods ran,
e.g. on the node:
  docker run --rm --network host -v ~/financial-agent:/repo -w /app \\
    financial-agent-app:local python /repo/scripts/replay_sections.py \\
    --findings-dir /repo/eval/runs/raw/v924f-findings --arm bf16 \\
    --served-name financial-lora --url http://localhost:30880 \\
    --out /repo/eval/runs/replay-2026-09-30

--dry-run builds and verifies every context and prompt without sending.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SECTIONS = ("### Financial Health", "### Risk Factors")
_HEADERS = ("STOCK DATA", "NEWS ARTICLES", "SEC FILING SUMMARIES",
            "RAG — SEC HIGHLIGHTS", "RAG — RISK FACTORS")
_NOT_AVAILABLE = "(not available)"
_CTX_START = "## Retrieved source context\n\n"
_CTX_END = "\n\n## Pre-written sections (judge input)"
MARK = "<!-- replay-section: {} -->"
_MARK_RE = re.compile(r"^<!-- replay-section: (.+?) -->$", re.M)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- context ------------------------------------------------------------------

def render_context(stock, news, sec, rag_highlights, rag_risks) -> str:
    """grounding_check.run_arm's source_context layout (verified against the
    committed files by load_context, which requires a byte-exact match)."""
    return "\n\n".join([
        f"STOCK DATA:\n{json.dumps(stock, indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps(news, indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps(sec, indent=2)}",
        f"RAG — SEC HIGHLIGHTS:\n{rag_highlights or _NOT_AVAILABLE}",
        f"RAG — RISK FACTORS:\n{rag_risks or _NOT_AVAILABLE}",
    ])


def load_context(path: Path) -> dict:
    """Parse one findings file's source context back into its parts and
    verify the round trip is byte-exact and matches context_sha256."""
    text = path.read_text(encoding="utf-8")
    start = text.index(_CTX_START) + len(_CTX_START)
    context = text[start:text.index(_CTX_END, start)]
    meta = dict(re.findall(r"^(ticker|arm|context_sha256): (\S+)$", text, re.M))
    if sha256(context) != meta.get("context_sha256"):
        raise ValueError(f"{path}: context does not hash to context_sha256")
    bounds = []
    pos = 0
    for h in _HEADERS:
        marker = f"{h}:\n" if not bounds else f"\n\n{h}:\n"
        i = context.index(marker, pos)
        bounds.append((i, i + len(marker)))
        pos = i + len(marker)
    parts = []
    for n, (_, body_start) in enumerate(bounds):
        end = bounds[n + 1][0] if n + 1 < len(bounds) else len(context)
        parts.append(context[body_start:end])
    stock, news, sec = (json.loads(p) for p in parts[:3])
    rag_h, rag_r = (None if p == _NOT_AVAILABLE else p for p in parts[3:])
    if render_context(stock, news, sec, rag_h, rag_r) != context:
        raise ValueError(f"{path}: re-rendered context differs from the file")
    return {"ticker": meta["ticker"], "context": context,
            "context_sha256": meta["context_sha256"], "stock": stock,
            "news": news, "sec": sec, "rag_highlights": rag_h, "rag_risks": rag_r}


# --- prompts, from the pipeline's own code ------------------------------------

def _pipeline_env(url: str, served_name: str):
    """Environment the pipeline's local arm runs with; set before importing
    agent.core. REDIS_URL / ANTHROPIC_API_KEY only satisfy import-time
    checks: this script never touches Redis or Anthropic. Tracing off."""
    os.environ.update({
        "USE_LOCAL_MODEL": "true", "LOCAL_MODEL_BACKEND": "openai",
        "LOCAL_MODEL_URL": url, "LOCAL_MODEL_NAME": served_name,
        "LANGCHAIN_TRACING_V2": "false", "LANGSMITH_TRACING": "false",
    })
    os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:1/0")
    os.environ.setdefault("ANTHROPIC_API_KEY", "unused-by-replay")


class _Capture:
    def __init__(self):
        self.messages = None

    def invoke(self, messages):
        self.messages = messages

        class _R:
            content = ""
        return _R()


def build_requests(ctx: dict) -> list[dict]:
    """[{heading, messages, client}] for the two local sections, via
    agent.core._haiku_section with _section_llm captured."""
    import agent.core as core
    contexts = {"### Financial Health": core._data_context(ctx["stock"], ctx["news"], ctx["sec"])}
    contexts["### Risk Factors"] = ctx["rag_risks"] or contexts["### Financial Health"]
    company = ctx["stock"].get("company_name", ctx["ticker"])
    instructions = dict(core._SECTIONS)
    out = []
    for heading in SECTIONS:
        client = core._section_llm(heading)
        if type(client).__name__ != "LocalChat":
            raise RuntimeError(f"{heading} is not routed to the local model")
        cap = _Capture()
        original = core._section_llm
        core._section_llm = lambda h, _cap=cap: _cap
        try:
            core._haiku_section(heading, instructions[heading], company,
                                ctx["ticker"], contexts[heading])
        finally:
            core._section_llm = original
        out.append({"heading": heading, "messages": cap.messages, "client": client})
    return out


def payload(req: dict, served_name: str, seed: int) -> dict:
    client = req["client"]
    return {
        "model": served_name,
        **client.sampling_params(),
        "messages": [{"role": client._role(m), "content": m.content}
                     for m in req["messages"]],
        "seed": seed,
    }


def prompt_sha(req: dict) -> str:
    return sha256(json.dumps([m.content for m in req["messages"]]))


def seed_for(seed_base: int, ticker_index: int, section_index: int, sample: int) -> int:
    return seed_base + 10_000 * sample + 10 * ticker_index + section_index


# --- replay files ---------------------------------------------------------------

def write_replay_file(path: Path, meta: dict, stock: dict, outputs: dict):
    lines = [f"# {meta['ticker']} — replay s{meta['sample']} — {meta['arm']}", "",
             "## Metadata", ""]
    lines += [f"{k}: {v if isinstance(v, str) else json.dumps(v)}" for k, v in meta.items()]
    lines += ["", "## Stock data", "", json.dumps(stock, indent=2), ""]
    for heading, text in outputs.items():
        lines += [MARK.format(heading.removeprefix("### ")), text, ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def read_replay_file(path: Path) -> dict:
    """-> {meta, stock, sections: [(name, text)]} (inverse of write_replay_file)."""
    text = path.read_text(encoding="utf-8")
    head, _, rest = text.partition("\n## Stock data\n\n")
    meta = {}
    for line in head.split("## Metadata", 1)[1].strip().splitlines():
        k, _, v = line.partition(": ")
        try:
            meta[k] = json.loads(v)
        except ValueError:
            meta[k] = v
    stock, end = json.JSONDecoder().raw_decode(rest)
    body = rest[end:]
    marks = list(_MARK_RE.finditer(body))
    sections = [(m.group(1), body[m.end():marks[i + 1].start() if i + 1 < len(marks)
                                  else len(body)].strip("\n"))
                for i, m in enumerate(marks)]
    return {"meta": meta, "stock": stock, "sections": sections}


# --- run ------------------------------------------------------------------------

def _repo_relative(path: Path) -> str:
    """eval/runs/raw/... wherever the findings are mounted."""
    p = str(path).replace("\\", "/")
    i = p.find("eval/runs/raw/")
    return p[i:] if i >= 0 else p


def _post(url: str, body: dict, timeout: float) -> dict:
    import requests
    r = requests.post(f"{url}/v1/chat/completions", json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser(description="Frozen-input section replay.")
    ap.add_argument("--findings-dir", required=True)
    ap.add_argument("--arm", required=True, help="output subdirectory, e.g. bf16")
    ap.add_argument("--served-name", required=True)
    ap.add_argument("--url", default="http://localhost:30880")
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--seed-base", type=int, default=42)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=300)
    ap.add_argument("--out", default=f"eval/runs/replay-{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d}")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    _pipeline_env(args.url, args.served_name)
    import agent.core as core  # noqa: F401  (after the env is set)
    core_sha = hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()

    # Sorted by plain name (Windows Path ordering is case-insensitive), so
    # ticker indices, and therefore seeds, are the same on every platform.
    files = sorted(Path(args.findings_dir).glob("*_local-model.md"), key=lambda p: p.name)
    if not files:
        sys.exit(f"no *_local-model.md files in {args.findings_dir}")
    ctxs = [load_context(f) for f in files]
    reqs = [build_requests(c) for c in ctxs]
    print(f"{len(ctxs)} contexts verified byte-exact; agent/core.py sha256 {core_sha[:12]}")
    if args.dry_run:
        for c, r in zip(ctxs, reqs):
            print(c["ticker"], c["context_sha256"][:12], [prompt_sha(x)[:12] for x in r])
        return

    import requests
    ids = [m["id"] for m in requests.get(f"{args.url}/v1/models", timeout=30).json()["data"]]
    if args.served_name not in ids:
        sys.exit(f"{args.served_name} is not served at {args.url} (serving {ids})")

    jobs = []
    for ti, (c, r) in enumerate(zip(ctxs, reqs)):
        for k in range(1, args.samples + 1):
            for si, req in enumerate(r):
                jobs.append((ti, k, si, seed_for(args.seed_base, ti, si, k)))

    def run(job):
        ti, k, si, seed = job
        resp = _post(args.url, payload(reqs[ti][si], args.served_name, seed), args.timeout)
        return job, resp

    results = {}
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for (ti, k, si, seed), resp in ex.map(run, jobs):
            results[(ti, k, si)] = (seed, resp)

    out = Path(args.out) / args.arm
    now = f"{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}"
    for ti, (c, r) in enumerate(zip(ctxs, reqs)):
        for k in range(1, args.samples + 1):
            outputs, meta = {}, {
                "ticker": c["ticker"], "arm": args.arm, "sample": k,
                "served_name": args.served_name,
                "source_findings": _repo_relative(files[ti]),
                "context_sha256": c["context_sha256"],
                "agent_core_sha256": core_sha,
                "sampling": r[0]["client"].sampling_params(),
                "endpoint": args.url, "generated_utc": now,
            }
            for si, req in enumerate(r):
                seed, resp = results[(ti, k, si)]
                key = req["heading"].removeprefix("### ").lower().replace(" ", "_")
                choice = resp["choices"][0]
                outputs[req["heading"]] = choice["message"]["content"]
                meta[f"{key}_prompt_sha256"] = prompt_sha(req)
                meta[f"{key}_seed"] = seed
                meta[f"{key}_response_model"] = resp.get("model")
                meta[f"{key}_finish_reason"] = choice.get("finish_reason")
                meta[f"{key}_completion_tokens"] = (resp.get("usage") or {}).get("completion_tokens")
            write_replay_file(out / f"{c['ticker']}-s{k}.md", meta, c["stock"], outputs)
    print(f"wrote {len(ctxs) * args.samples} files to {out}")


if __name__ == "__main__":
    main()
