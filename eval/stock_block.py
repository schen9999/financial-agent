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

A second, stricter rule, offline only (`--no-figures`, added 2026-10-09):
`stock_block_no_figures` counts a block as empty when it holds none of the
nine numeric fields the numeric check binds (agent.numeric_check.FIELDS).
yfinance returns no quote for RDFN and VERV, so their block carries only
ticker, company_name "N/A" and currency: not an empty dict, so
`stock_block_empty` passes it, but the brief has no stock figures. The
in-pod path (grounding_check.run_arm, eval_aggregate) keeps
`stock_block_empty` unchanged until the next image.

Usage:
  python eval/stock_block.py eval/runs/raw/j4cnp-findings eval/runs/raw/dvvxk-findings
  python eval/stock_block.py --no-figures eval/runs/raw/4hsn2-findings ...
"""
import json
import re
import sys
from pathlib import Path

# The source-context layout grounding_check.run_arm builds: the stock dict
# (json.dumps indent=2) between these two block labels.
_STOCK_RE = re.compile(r"^STOCK DATA:\n(.*?)\n\nNEWS ARTICLES:", re.S | re.M)


def _stock_block(source_context: str) -> dict | None:
    m = _STOCK_RE.search(source_context.replace("\r\n", "\n"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def stock_block_empty(source_context: str) -> bool | None:
    data = _stock_block(source_context)
    return None if data is None else not data


def stock_block_no_figures(source_context: str) -> bool | None:
    """Offline rule: True when the block holds none of the numeric fields
    (an empty dict included). Same True/False/None contract as
    stock_block_empty. Not used by the harness."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from agent.numeric_check import FIELDS

    data = _stock_block(source_context)
    if data is None:
        return None
    return not any(data.get(k) is not None for k in FIELDS)


def scan_findings_dir(findings_dir: Path, rule=stock_block_empty) -> dict:
    """Apply `rule` (stock_block_empty by default) to every findings .md in
    one run's dir — recursively, since some runs keep one subdirectory per
    ticker (9j2dj)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from eval.label import parse_findings_file

    empty, unknown, files = [], [], sorted(Path(findings_dir).rglob("*.md"))
    for f in files:
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        verdict = rule(parsed["context"]) if parsed else None
        if verdict is None:
            unknown.append(f.stem)
        elif verdict:
            empty.append(f.stem)
    return {"dir": str(findings_dir), "files": len(files),
            "empty": empty, "unknown": unknown}


def main(argv=None) -> int:
    dirs = list(argv if argv is not None else sys.argv[1:])
    rule = stock_block_empty
    if "--no-figures" in dirs:
        dirs.remove("--no-figures")
        rule = stock_block_no_figures
        print("Rule: no figures — a STOCK DATA block holding none of the nine numeric "
              "fields (agent.numeric_check.FIELDS) counts as empty")
    if not dirs:
        print(__doc__)
        return 2
    print(f"  {'Findings dir':<40} {'Files':>5} {'Empty':>5} {'Unknown':>7}  Empty-block files")
    for d in dirs:
        r = scan_findings_dir(Path(d), rule)
        print(f"  {r['dir']:<40} {r['files']:>5} {len(r['empty']):>5} "
              f"{len(r['unknown']):>7}  {', '.join(r['empty']) or '-'}")
        if r["unknown"]:
            print(f"    unknown (no parseable STOCK DATA block): {', '.join(r['unknown'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
