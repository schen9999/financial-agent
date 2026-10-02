#!/usr/bin/env python3
"""Detect briefs that were written with an empty STOCK DATA block.

agent.tools.stock.get_stock_data catches every exception (a yfinance 429
included) and returns {"error": ...}; agent.core._trim_stock keeps none of
that, so the brief AND the judge see `STOCK DATA: {}` — no retry, no skip,
just a brief written from news + SEC alone. Detection only: nothing here
changes harness behaviour or the gate.

One definition, used three ways:
  - grounding_check.run_arm records `stock_block_empty` on every result row
  - scripts/eval_aggregate.py counts those rows into the aggregate output
  - this script's CLI applies it retroactively to committed findings dirs

`stock_block_empty` returns True (block present, parses, empty), False
(present and non-empty), or None (no STOCK DATA block found, or it does not
parse) — None is reported as unknown, never as clean.

Usage:
  python eval/stock_block.py eval/runs/raw/j4cnp-findings eval/runs/raw/dvvxk-findings
"""
import json
import re
import sys
from pathlib import Path

# The source-context layout grounding_check.run_arm builds: the stock dict
# (json.dumps indent=2) between these two block labels.
_STOCK_RE = re.compile(r"^STOCK DATA:\n(.*?)\n\nNEWS ARTICLES:", re.S | re.M)


def stock_block_empty(source_context: str) -> bool | None:
    m = _STOCK_RE.search(source_context.replace("\r\n", "\n"))
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return None
    return not data


def scan_findings_dir(findings_dir: Path) -> dict:
    """Apply stock_block_empty to every findings .md in one run's dir —
    recursively, since some runs keep one subdirectory per ticker (9j2dj)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from eval.label import parse_findings_file

    empty, unknown, files = [], [], sorted(Path(findings_dir).rglob("*.md"))
    for f in files:
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        verdict = stock_block_empty(parsed["context"]) if parsed else None
        if verdict is None:
            unknown.append(f.stem)
        elif verdict:
            empty.append(f.stem)
    return {"dir": str(findings_dir), "files": len(files),
            "empty": empty, "unknown": unknown}


def main(argv=None) -> int:
    dirs = (argv if argv is not None else sys.argv[1:])
    if not dirs:
        print(__doc__)
        return 2
    print(f"  {'Findings dir':<40} {'Files':>5} {'Empty':>5} {'Unknown':>7}  Empty-block files")
    for d in dirs:
        r = scan_findings_dir(Path(d))
        print(f"  {r['dir']:<40} {r['files']:>5} {len(r['empty']):>5} "
              f"{len(r['unknown']):>7}  {', '.join(r['empty']) or '-'}")
        if r["unknown"]:
            print(f"    unknown (no parseable STOCK DATA block): {', '.join(r['unknown'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
