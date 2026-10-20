#!/usr/bin/env python3
"""Build the model stub's corpus from a committed self-served run.

The harness benchmark (docs/harness-benchmark-plan.md) replaces the model
with scripts/model_stub.py. The stub answers every call site with the text
the real model wrote for that ticker and site in a committed run, and waits
the delay a latency profile assigns to that call's recorded token counts.

Source, both committed:
  - the run's findings dir (eval/runs/raw/<run>-findings): the four
    pre-written sections, the Executive Summary and Outlook from each .md,
    and the two RAG answers from each .ragf.json
  - the run's traffic-proof log (eval/runs/slm-proof-<run>/*.log): one
    EVAL_LLM_CALL line per call with its site and prompt/completion tokens,
    mapped to a ticker by the pod's "Tickers: <T>" line. Judge sites
    (judge, rag_judge) are evaluation, not harness, and are dropped.

Output: one JSON object, {"source": ..., "tickers": {T: {site: {"text",
"prompt_tokens", "completion_tokens"}}}}. Synthesis keeps only the Executive
Summary and Outlook; the stub rebuilds the full brief from the sections in
the synthesis prompt, as the real model is told to.

Usage:
  python scripts/build_stub_corpus.py --run nstp9 --out k8s/model-stub/corpus.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_SITES = ("rag:highlights", "rag:risks", "section:financial_health",
                 "section:recent_developments", "section:sec_filing_highlights",
                 "section:risk_factors", "synthesis")
SECTION_HEADINGS = {"Financial Health": "section:financial_health",
                    "Recent Developments": "section:recent_developments",
                    "SEC Filing Highlights": "section:sec_filing_highlights",
                    "Risk Factors": "section:risk_factors"}

_POD = re.compile(r"^\[pod/([^/\]]+)/[^\]]*\] (.*)$")
_TICKERS = re.compile(r"Tickers: ([A-Z.\-]+)\s*$")


def calls_by_ticker(log_text: str) -> dict:
    """{ticker: {site: {"prompt_tokens", "completion_tokens"}}} from a proof
    log; the first non-retry, error-free call per (ticker, site)."""
    pod_ticker, calls = {}, []
    for line in log_text.splitlines():
        m = _POD.match(line)
        if not m:
            continue
        pod, rest = m.groups()
        t = _TICKERS.search(rest)
        if t:
            pod_ticker[pod] = t.group(1)
        if rest.startswith("EVAL_LLM_CALL "):
            calls.append((pod, json.loads(rest[len("EVAL_LLM_CALL "):])))
    out: dict = {}
    for pod, c in calls:
        if c.get("site") not in HARNESS_SITES or c.get("retry") or c.get("error"):
            continue
        ticker = pod_ticker.get(pod)
        if ticker is None:
            continue
        out.setdefault(ticker, {}).setdefault(c["site"], {
            "prompt_tokens": c.get("prompt_tokens"),
            "completion_tokens": c.get("completion_tokens")})
    return out


def _blocks(md: str, top: str) -> dict:
    """The '### X' blocks under the '## <top>' heading, as {X: body}."""
    part = md.split(f"\n## {top}", 1)
    if len(part) < 2:
        return {}
    body = part[1].split("\n## ", 1)[0]
    out = {}
    for chunk in body.split("\n### ")[1:]:
        head, _, text = chunk.partition("\n")
        out[head.strip()] = text.split("\n---\n", 1)[0].strip()
    return out


def texts_for(findings_md: str, ragf: dict) -> dict:
    out = {}
    for head, body in _blocks(findings_md, "Pre-written sections").items():
        if head in SECTION_HEADINGS:
            out[SECTION_HEADINGS[head]] = f"### {head}\n\n{body}"
    audited = _blocks(findings_md, "Audited")
    if audited.get("Executive Summary") and audited.get("Outlook"):
        out["synthesis"] = {"executive_summary": audited["Executive Summary"],
                            "outlook": audited["Outlook"]}
    for key in ("highlights", "risks"):
        ans = (ragf.get("answers") or {}).get(key) or {}
        if ans.get("answer"):
            out[f"rag:{key}"] = ans["answer"]
    return out


def build(run: str) -> dict:
    findings = ROOT / "eval" / "runs" / "raw" / f"{run}-findings"
    logs = sorted((ROOT / "eval" / "runs" / f"slm-proof-{run}").glob("*.log"))
    if not findings.is_dir() or not logs:
        raise SystemExit(f"missing {findings} or eval/runs/slm-proof-{run}/*.log")
    tokens = calls_by_ticker("\n".join(p.read_text(encoding="utf-8") for p in logs))
    tickers = {}
    for md in sorted(findings.glob("*.md")):
        ticker = md.name.split("_", 1)[0]
        ragf_path = md.with_suffix(".ragf.json")
        ragf = json.loads(ragf_path.read_text()) if ragf_path.exists() else {}
        texts = texts_for(md.read_text(encoding="utf-8"), ragf)
        sites = {}
        for site, text in texts.items():
            tok = (tokens.get(ticker) or {}).get(site) or {}
            sites[site] = {"text": text, "prompt_tokens": tok.get("prompt_tokens"),
                           "completion_tokens": tok.get("completion_tokens")}
        tickers[ticker] = sites
    return {"source": {"run": run, "findings": str(findings.relative_to(ROOT)),
                       "proof_logs": [str(p.relative_to(ROOT)) for p in logs]},
            "tickers": tickers}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", default="nstp9")
    ap.add_argument("--out", default=str(ROOT / "k8s" / "model-stub" / "corpus.json"))
    a = ap.parse_args(argv)
    corpus = build(a.run)
    missing = [(t, s) for t, sites in corpus["tickers"].items() for s in sites
               if sites[s]["completion_tokens"] is None]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(corpus, indent=1, sort_keys=True) + "\n")
    n_sites = sum(len(s) for s in corpus["tickers"].values())
    print(f"{a.out}: {len(corpus['tickers'])} tickers, {n_sites} site texts, "
          f"{len(missing)} without recorded tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
