#!/usr/bin/env python3
"""How many figures each arm's briefs state: judged and judge-independent.

Three counts per brief, each compared between runs with the paired
per-ticker test of eval/multi_arm_stats.py (mean difference with a seeded
bootstrap interval, exact two-sided sign test):

  numbers   judge-independent: every stated number in the audited Executive
            Summary + Outlook, counted by the numeric check's own tokenizer
            (agent/numeric_check.py, `unchecked` with an empty stock dict:
            years, "52" in "52-week", filing names and list numbers excluded)
  bound     judge-independent, conservative: numbers the check binds to a
            stock-data field label ("revenue of $X", "P/E of Y")
  numeric   judge-based: claims with a digit, from a re-judge pass
            (eval/rejudge_runs.py output) — the density co-primary

Counting note (2026-10-06): with an empty stock dict no binding is checked,
so `unchecked` already counts every number; adding the per-reason counts on
top double-counts the bound ones (a first pass did, giving ~11 numbers per
hosted brief instead of 6.8).

  python eval/density_check.py --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 5bdz5 \\
      --pairs 9jzmj:8vpq6 9jzmj:p9jr2 8vpq6:p9jr2 4hsn2:5bdz5 4hsn2:nstp9 5bdz5:nstp9 \\
      --rejudge eval/runs/rejudge-2026-10-06
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from agent import numeric_check as nc  # noqa: E402
from eval import multi_arm_stats as mas  # noqa: E402
from eval.label import parse_claims, parse_findings_file  # noqa: E402

RAW = ROOT / "eval" / "runs" / "raw"


def text_counts(audited: str) -> dict:
    """Judge-independent counts for one brief's audited text."""
    rep = nc.check_sections(nc.split_sections(audited.split("\n---\n")[0]), {})
    return {"numbers": rep["unchecked"], "bound": len(rep["bindings"])}


def text_density(run: str) -> dict:
    out = {}
    for f in sorted((RAW / f"{run}-findings").rglob("*_*.md")):
        p = parse_findings_file(f.read_text(encoding="utf-8"))
        out[f.stem.rsplit("_", 1)[0]] = text_counts(p["audited"])
    return out


def rejudge_density(run: str, rejudge_dir: Path) -> dict:
    out = {}
    for f in sorted((rejudge_dir / run).glob("*.findings.txt")):
        claims = parse_claims(f.read_text(encoding="utf-8"))
        out[f.name.split("_")[0]] = {"numeric": sum(1 for c in claims if re.search(r"\d", c["claim"] or ""))}
    return out


def report(dens: dict, field: str, pairs: list[tuple[str, str]], title: str) -> list[str]:
    L = [title]
    for run, v in dens.items():
        vals = [x[field] for x in v.values()]
        L.append(f"  {run:8} mean {sum(vals) / len(vals):5.2f} per brief ({len(vals)} briefs)")
    for a, b in pairs:
        pr = mas.paired(dens[a], dens[b], field)
        L.append(f"  {a} - {b}: {pr['mean_diff']:+.2f} (95% bootstrap CI {pr['ci'][0]:+.2f} to "
                 f"{pr['ci'][1]:+.2f}); {a} more on {pr['a_more']}, equal {pr['equal']}, "
                 f"{b} more {pr['b_more']}; sign p = {mas.fmt_p(pr['sign_p'])}")
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--pairs", nargs="+", required=True, metavar="A:B")
    ap.add_argument("--rejudge", type=Path, help="a rejudge_runs.py output folder")
    args = ap.parse_args(argv)
    pairs = [tuple(p.split(":")) for p in args.pairs]
    text = {r: text_density(r) for r in args.runs}
    lines = report(text, "numbers", pairs, "Judge-independent: numbers stated in the audited text")
    lines += report(text, "bound", pairs, "Judge-independent, conservative: figures bound to a stock-data field")
    if args.rejudge:
        rj = {r: rejudge_density(r, args.rejudge) for r in args.runs}
        lines += report(rj, "numeric", pairs, f"Judge-based: numeric claims per brief ({args.rejudge.name})")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
