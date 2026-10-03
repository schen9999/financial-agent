#!/usr/bin/env python3
"""How long does the SLM's RAG answer want to be? Replays a smoke run's RAG
answer calls against an SLM endpoint with a generous max_tokens and reports
the natural completion-token lengths per site — the measurement the shared
RAG cap (agent/tools/slm.py RAG_MAX_TOKENS) is sized from. A truncated answer
only says "more than the cap"; this says how much more.

Two steps, on two machines:

  build  (laptop, repo venv) Rebuild the smoke's RAG requests from its
         captured pod log: each (ticker, site)'s retrieved chunks are in the
         run's RAG-faithfulness findings, and the request is produced by the
         real path — llama_index's query engine in its default response mode,
         the SLM adapter, the "rag" site profile (temperature, every sampler,
         thinking off) — with only max_tokens replaced. No retrieval, no
         network. Each request carries the prompt-token count the smoke's
         ledger recorded for it.

  run    (node 2 host, stdlib only) Send them to the endpoint and report
         median / p95 / max completion tokens per site. The rebuilt prompts
         are checked, not trusted: the server's prompt_tokens must equal the
         smoke's recorded count for every request (same GGUF, same template),
         otherwise the run says which differ and exits non-zero.

  python scripts/rag_natural_length.py build \\
      --log eval/runs/slm-proof-nb6r6/grounding-eval-slm-cpu-nb6r6.log \\
      --out eval/runs/rag-natural-length-requests-nb6r6.json
  LLAMA_API_KEY=... python3 scripts/rag_natural_length.py run \\
      --requests eval/runs/rag-natural-length-requests-nb6r6.json \\
      --url http://localhost:30880 --api-key-env LLAMA_API_KEY \\
      --out ~/rag-natural-length-gpu.json

One sample per prompt at temperature 0.1: a dated measurement of 20 answers,
not a number of record.
"""
import argparse
import base64
import io
import json
import math
import os
import re
import sys
import tarfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SITES = {"highlights": "rag:highlights", "risks": "rag:risks"}
_TGZ = re.compile(r"===EVAL_FINDINGS_TGZ_BEGIN pod=(\S+?)===\n(.*?)\n[^\n]*===EVAL_FINDINGS_TGZ_END===",
                  re.S)
_POD_PREFIX = re.compile(r"^\[pod/[^\]]+\] ")


# ── build (laptop) ──────────────────────────────────────────────────────────

def read_smoke(log_text: str) -> dict:
    """{ticker: {"chunks": {which: [...]}, "by_site": {...}}} from the
    per-pod findings archives embedded in a captured run log."""
    out = {}
    for _pod, body in _TGZ.findall(log_text):
        b64 = "".join(_POD_PREFIX.sub("", line) for line in body.splitlines())
        try:
            tf = tarfile.open(fileobj=io.BytesIO(base64.b64decode(b64)), mode="r:gz")
        except (ValueError, tarfile.TarError):
            continue
        for mem in tf.getmembers():
            if mem.name.endswith(".ragf.json"):
                rec = json.load(tf.extractfile(mem))
                out.setdefault(rec["ticker"], {})["chunks"] = {
                    which: a["chunks"] for which, a in rec["answers"].items()}
            elif mem.name.endswith(".md"):
                text = tf.extractfile(mem).read().decode("utf-8")
                ticker = re.search(r"(?m)^ticker: (\S+)", text)
                by_site = re.search(r"(?m)^llm_by_site: (\{.*\})\s*$", text)
                if ticker and by_site:
                    out.setdefault(ticker.group(1), {})["by_site"] = json.loads(by_site.group(1))
    return out


def rebuild_messages(ticker: str, question: str, chunks: list[str], site: str) -> list[dict]:
    """The exact chat messages the SLM arm sends for one RAG answer: the real
    query engine and SLM adapter over the recorded chunks, in retrieval order,
    with the metadata rag.py indexes every filing under."""
    from unittest import mock

    from llama_index.core.query_engine import RetrieverQueryEngine
    from llama_index.core.retrievers import BaseRetriever
    from llama_index.core.schema import NodeWithScore, TextNode

    from agent.tools import slm

    class _Recorded(BaseRetriever):
        def _retrieve(self, query_bundle):
            return [NodeWithScore(node=TextNode(text=c, metadata={"ticker": ticker,
                                                                  "source": "SEC EDGAR"}),
                                  score=1.0) for c in chunks]

    sent = []

    def capture(site_name, messages, **kwargs):
        sent.append(messages)
        return {"choices": [{"message": {"content": "(captured)"}}]}

    with mock.patch.object(slm, "chat_completion", capture):
        RetrieverQueryEngine.from_args(_Recorded(), llm=slm.llama_index_llm(site)).query(question)
    if len(sent) != 1:
        raise SystemExit(f"{ticker} {site}: the query engine made {len(sent)} LLM calls, expected 1")
    return sent[0]


def build(args) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    os.environ.setdefault("LOCAL_MODEL_THINKING", "off")
    from agent.core import DEFAULT_HIGHLIGHTS_QUERY, DEFAULT_RISKS_QUERY
    from agent.tools import slm

    questions = {"highlights": DEFAULT_HIGHLIGHTS_QUERY, "risks": DEFAULT_RISKS_QUERY}
    smoke = read_smoke(Path(args.log).read_text(encoding="utf-8", errors="replace"))
    reqs = []
    for ticker in sorted(smoke):
        row = smoke[ticker]
        for which, site in SITES.items():
            chunks = (row.get("chunks") or {}).get(which)
            led = (row.get("by_site") or {}).get(site)
            if not chunks or not led or led["calls"] != 1:
                raise SystemExit(f"{ticker} {site}: no recorded chunks, or not exactly one "
                                 f"ledger call, in {args.log}")
            body = {"messages": rebuild_messages(ticker, questions[which], chunks, site),
                    **slm.request_params(site), "max_tokens": args.max_tokens}
            reqs.append({"ticker": ticker, "site": site,
                         "smoke_prompt_tokens": led["prompt_tokens"],
                         "smoke_completion_tokens": led["completion_tokens"],
                         "smoke_truncated": bool(led["truncated"]),
                         "body": body})
    doc = {"source_log": Path(args.log).as_posix(),
           "max_tokens": args.max_tokens,
           "sampling": {**slm.request_params("rag"), "max_tokens": args.max_tokens},
           "requests": reqs}
    Path(args.out).write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(reqs)} requests ({len(smoke)} tickers) -> {args.out}")
    print(f"  sampling: {json.dumps(doc['sampling'], sort_keys=True)}")
    return 0


# ── run (endpoint host; stdlib only) ────────────────────────────────────────

def percentile(values: list[float], q: float) -> float:
    """Linear-interpolated percentile (numpy's default)."""
    xs = sorted(values)
    k = (len(xs) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def summarize(rows: list[dict]) -> dict:
    """Per-site and pooled natural-length stats over completed rows."""
    def stats(sel):
        vals = [r["completion_tokens"] for r in sel]
        if not vals:
            return None
        return {"n": len(vals), "min": min(vals), "median": percentile(vals, 0.5),
                "p95": percentile(vals, 0.95), "max": max(vals),
                "hit_max_tokens": sum(1 for r in sel if r["finish_reason"] == "length"),
                "over_512": sum(v > 512 for v in vals), "over_800": sum(v > 800 for v in vals),
                "over_1024": sum(v > 1024 for v in vals)}
    ok = [r for r in rows if not r.get("error")]
    out = {site: stats([r for r in ok if r["site"] == site]) for site in SITES.values()}
    out["both"] = stats(ok)
    return out


def prompt_mismatches(rows: list[dict]) -> list[dict]:
    return [r for r in rows if not r.get("error") and r["prompt_tokens"] != r["smoke_prompt_tokens"]]


def _http_json(url: str, key: str | None, body: dict | None, timeout: float) -> dict:
    # One connection per request, non-streaming: llama-server closes
    # keep-alive sockets after a response, which loses reused requests.
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", "Connection": "close",
                                          **({"Authorization": f"Bearer {key}"} if key else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def send_one(url: str, key: str | None, model: str, req: dict, timeout: float,
             http=_http_json) -> dict:
    row = {k: req[k] for k in ("ticker", "site", "smoke_prompt_tokens",
                               "smoke_completion_tokens", "smoke_truncated")}
    t0 = time.perf_counter()
    try:
        data = http(f"{url}/v1/chat/completions", key, {"model": model, **req["body"]}, timeout)
    except (urllib.error.URLError, OSError, ValueError) as e:
        return {**row, "error": f"{type(e).__name__}: {e}"}
    choice, usage = data["choices"][0], data.get("usage") or {}
    text = choice["message"].get("content") or ""
    return {**row, "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "finish_reason": choice.get("finish_reason"),
            "latency_s": round(time.perf_counter() - t0, 2), "chars": len(text), "answer": text}


def run(args, http=_http_json) -> int:
    doc = json.loads(Path(args.requests).read_text(encoding="utf-8"))
    url = args.url.rstrip("/")
    key = None
    if args.api_key_env:
        key = os.environ.get(args.api_key_env)
        if not key:
            raise SystemExit(f"--api-key-env {args.api_key_env}: variable is empty or unset")
    try:
        served = [m.get("id") for m in http(f"{url}/v1/models", key, None, 30.0).get("data", [])]
        props = http(f"{url}/props", key, None, 30.0)
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise SystemExit(f"{url} unreachable or rejected the key: {type(e).__name__}: {e}")
    model = args.model or (served[0] if len(served) == 1 else None)
    if model not in served:
        raise SystemExit(f"{url} serves {served}; pass --model with one of them")
    build_info = props.get("build_info")
    print(f"endpoint {url}: model {model}, build {build_info}; max_tokens {doc['max_tokens']}, "
          f"{len(doc['requests'])} requests, concurrency {args.concurrency}", flush=True)

    def one(req):
        row = send_one(url, key, model, req, args.timeout, http)
        if row.get("error"):
            print(f"  {row['ticker']:<6} {row['site']:<15} ERROR {row['error']}", flush=True)
        else:
            print(f"  {row['ticker']:<6} {row['site']:<15} prompt {row['prompt_tokens']:>5} "
                  f"(smoke {row['smoke_prompt_tokens']:>5}) completion {row['completion_tokens']:>5} "
                  f"finish={row['finish_reason']:<6} {row['latency_s']:>7.1f}s "
                  f"[smoke: {row['smoke_completion_tokens']}"
                  f"{' truncated' if row['smoke_truncated'] else ''}]", flush=True)
        return row

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        rows = list(pool.map(one, doc["requests"]))

    summary = summarize(rows)
    print(f"\nnatural completion tokens (max_tokens {doc['max_tokens']}, p95 interpolated):")
    print(f"  {'site':<15} {'n':>3} {'min':>5} {'median':>7} {'p95':>6} {'max':>5} "
          f"{'>512':>5} {'>800':>5} {'>1024':>6} {'hit cap':>8}")
    for name, s in summary.items():
        if s:
            print(f"  {name:<15} {s['n']:>3} {s['min']:>5} {s['median']:>7.0f} {s['p95']:>6.0f} "
                  f"{s['max']:>5} {s['over_512']:>5} {s['over_800']:>5} {s['over_1024']:>6} "
                  f"{s['hit_max_tokens']:>8}")
    errors = [r for r in rows if r.get("error")]
    bad = prompt_mismatches(rows)
    if bad:
        print(f"\nPROMPT CHECK: MISMATCH on {len(bad)} request(s) - the rebuilt prompt is not "
              f"token-identical to the smoke's; report the deltas with any length quoted:")
        for r in bad:
            print(f"  {r['ticker']} {r['site']}: server {r['prompt_tokens']} vs smoke "
                  f"{r['smoke_prompt_tokens']} ({r['prompt_tokens'] - r['smoke_prompt_tokens']:+d})")
    else:
        print(f"\nPROMPT CHECK: EXACT - {len(rows) - len(errors)} of {len(rows)} requests "
              f"tokenized to the smoke's recorded prompt_tokens")
    if errors:
        print(f"ERRORS: {len(errors)} request(s) failed")
    if args.out:
        out = Path(os.path.expanduser(args.out))
        out.write_text(json.dumps({
            "endpoint": url, "model": model, "build_info": build_info,
            "max_tokens": doc["max_tokens"], "sampling": doc["sampling"],
            "source_log": doc["source_log"], "concurrency": args.concurrency,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "prompt_check": "EXACT" if not bad else "MISMATCH",
            "summary": summary, "rows": rows}, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"written: {out}")
    return 1 if (bad or errors) else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="rebuild a smoke run's RAG requests (laptop)")
    b.add_argument("--log", required=True, help="captured pod log of an SLM smoke run")
    b.add_argument("--out", required=True)
    b.add_argument("--max-tokens", type=int, default=4096)
    r = sub.add_parser("run", help="send the requests to an endpoint (stdlib only)")
    r.add_argument("--requests", required=True)
    r.add_argument("--url", default="http://localhost:30880")
    r.add_argument("--api-key-env", default=None, metavar="VAR",
                   help="env var holding the endpoint's API key; never on the command line")
    r.add_argument("--model", default=None, help="served alias (default: the only one listed)")
    r.add_argument("--concurrency", type=int, default=2,
                   help="the harness sends a brief's two RAG calls together")
    r.add_argument("--timeout", type=float, default=900.0)
    r.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    return build(args) if args.cmd == "build" else run(args)


if __name__ == "__main__":
    sys.exit(main())
