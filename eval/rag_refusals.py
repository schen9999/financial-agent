#!/usr/bin/env python3
"""Count the SEC-highlights RAG refusals of a run (known limitation 2),
deterministically, from the committed findings. No judge, no LLM.

The highlights answer is the "RAG — SEC HIGHLIGHTS:" block of each
findings file's retrieved context. It is a REFUSAL when its first sentence
(after the "[From Pinecone cache]" tag, which only means the ticker's
filing vectors were already indexed — retrieval and the answer still run)
says it cannot or is unable to provide the summary, and the answer gives no
takeaways anyway ("key takeaways", "key points", "highlights are/include").
A ticker with no RAG call ("(not available)": the 20-F filers, limitation
5) is outside the denominator.

Rule fixed 2026-10-07, before the reranking A/B, against the recorded
hosted runs: 4hsn2 and 9jzmj each 9 of 35, including all five tickers of
limitation 2 (AMZN, JPM, MSFT, NVDA, WMT).

  python eval/rag_refusals.py --runs 4hsn2 9jzmj
  python eval/rag_refusals.py --runs <run> --arm rerank3
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "eval" / "runs" / "raw"
BLOCK = re.compile(r"^RAG — SEC HIGHLIGHTS:\n(.*?)(?=^RAG — RISK FACTORS:|^## )", re.S | re.M)
CANNOT = re.compile(r"\b(cannot|can't|unable to) provide\b", re.I)
TAKEAWAYS = re.compile(r"key takeaways|key points|highlights (are|include)", re.I)


def highlights(findings_text: str) -> str | None:
    m = BLOCK.search(findings_text)
    if not m:
        return None
    a = m.group(1).strip()
    return None if a.startswith("(not available)") else a


def is_refusal(answer: str) -> bool:
    a = re.sub(r"^\[From Pinecone cache\]\s*", "", answer)
    first = re.split(r"(?<=[.!?])\s", a, maxsplit=1)[0]
    return bool(CANNOT.search(first)) and not TAKEAWAYS.search(a)


def run_refusals(run: str, arm: str | None = None) -> dict:
    """{ticker: True/False} over the tickers with a highlights answer."""
    out = {}
    for f in sorted((RAW / f"{run}-findings").rglob("*_*.md")):
        ticker, farm = f.stem.rsplit("_", 1)
        if arm and farm != arm:
            continue
        a = highlights(f.read_text(encoding="utf-8"))
        if a is not None:
            out[ticker] = is_refusal(a)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--arm")
    args = ap.parse_args(argv)
    for run in args.runs:
        r = run_refusals(run, args.arm)
        refused = sorted(t for t, v in r.items() if v)
        print(f"{run}: {len(refused)}/{len(r)} refusals: {' '.join(refused)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
