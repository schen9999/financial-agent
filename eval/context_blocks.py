"""Shared reader for the source-context blocks of a committed findings file.

grounding_check.run_arm writes the context as labelled blocks separated by
blank lines (STOCK DATA, NEWS ARTICLES, SEC FILING SUMMARIES, RAG — ...);
this returns the JSON ones parsed, for the offline audit scripts
(eval/news_coverage.py, eval/rag_window_anchor.py). Offline only: nothing
in the harness imports it.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.label import parse_findings_file  # noqa: E402

_BLOCK = {
    "stock": r"^STOCK DATA:\n(.*?)\n\nNEWS ARTICLES:",
    "news": r"^NEWS ARTICLES:\n(.*?)\n\nSEC FILING SUMMARIES:",
    "sec": r"^SEC FILING SUMMARIES:\n(.*?)\n\nRAG",
}


def blocks(findings_text: str) -> dict | None:
    """{"stock", "news", "sec"} parsed from one findings .md (a block that is
    missing or does not parse is None); None if the file does not parse."""
    p = parse_findings_file(findings_text)
    if not p:
        return None
    ctx = p["context"].replace("\r\n", "\n")
    out = {}
    for name, pat in _BLOCK.items():
        m = re.search(pat, ctx, re.S | re.M)
        try:
            out[name] = json.loads(m.group(1)) if m else None
        except ValueError:
            out[name] = None
    return out


def run_blocks(findings_dir: Path) -> dict:
    """{ticker: blocks} for every findings .md of one run (recursive)."""
    out = {}
    for f in sorted(Path(findings_dir).rglob("*.md")):
        b = blocks(f.read_text(encoding="utf-8"))
        if b is not None:
            out[f.stem.split("_")[0]] = b
    return out
