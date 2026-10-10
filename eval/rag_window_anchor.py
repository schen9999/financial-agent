#!/usr/bin/env python3
"""Where the filing window starts, per ticker, from committed findings
(offline; a proxy).

agent/tools/rag.py:191 indexes ONE window of one filing per ticker (the latest 10-K,
else the 10-Q):
skip_front_matter(clean, 15000) (agent/tools/sec_common.py:164-194), which
anchors on Item 1A Risk Factors and falls back to Item 7 MD&A only when no
Item 1A anchor is found. Both RAG queries (highlights and risks) retrieve
from that window. The window itself is not recorded in the findings, but
the SEC FILING SUMMARIES block is: agent/tools/sec.py:136 cuts the same
filing's summary with the same skip_front_matter anchor (a 2,000-char
window), so the summary's first words show which anchor the RAG window
used. A proxy: the namespace was indexed at its own time (never refreshed),
from the filing current then.

  python eval/rag_window_anchor.py 4hsn2
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.context_blocks import run_blocks  # noqa: E402


def anchor(sec) -> str:
    """The 10-K summary's anchor, else the 10-Q's — rag.py indexes the 10-K
    and falls back to the 10-Q the same way (rag.py:298-300)."""
    if not isinstance(sec, dict):
        return "no SEC block"
    for form in ("10-K", "10-Q"):
        k = sec.get(form)
        s = (k.get("summary") or "") if isinstance(k, dict) else ""
        if s:
            break
    else:
        return "no 10-K or 10-Q summary"
    if re.match(r"item\s*1a", s, re.I):
        return f"Item 1A ({form})"
    if re.match(r"item\s*7", s, re.I):
        return f"Item 7 ({form})"
    return f"other ({form})"


def main(argv=None) -> int:
    runs = argv if argv is not None else sys.argv[1:]
    if not runs:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for run in runs:
        per = run_blocks(ROOT / "eval" / "runs" / "raw" / f"{run}-findings")
        by = {}
        for t, b in sorted(per.items()):
            by.setdefault(anchor(b["sec"]), []).append(t)
        print(f"{run}: filing summary starts at, per ticker ({len(per)} tickers):")
        for k, ts in sorted(by.items(), key=lambda kv: -len(kv[1])):
            print(f"  {k:<24} {len(ts):>2}  {', '.join(ts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
