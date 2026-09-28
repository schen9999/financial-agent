#!/usr/bin/env python3
"""Unsupported-claim rates across N eval runs: Wilson 95% CI per run, exact
two-sided Fisher for every pair, and a per-section breakdown.

Written for the 2026-09-23 four-arm comparison (hosted baseline vs three
local models), where three runs share the harness arm name `local-model`,
so runs are keyed by a caller-supplied label instead of the arm.
eval/section_attribution.py (keyed by arm, two runs) is left unchanged so its
recorded j4cnp/lsnnc output keeps reproducing; this script reuses its
attribution heuristic exactly — claims are attributed to the pre-written
section they restate (normalized containment, else word-overlap >= 0.6,
else unattributed). Section buckets are diagnostic; the per-run totals are
the measured result. Free-form verdicts without a CLAIM line (claim=null)
count in the totals and land in "unattributed".

Usage:
  python eval/multi_arm_stats.py \\
      --run hosted  eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings \\
      --run lora    eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings ... \\
      [--pool hosted-pooled hosted rerun]

--pool NAME LABEL LABEL... concatenates the claims of runs from the same arm
(e.g. two hosted runs on one image) and tests each run outside the pool
against it.
"""
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval.section_attribution import attribute, section_texts  # noqa: E402
from eval.stats import fisher_exact, format_rate_ci  # noqa: E402

SECTIONS = ("financial-health", "risk-factors", "recent-developments",
            "sec-filing-highlights", "other", "unattributed")
OWNED = ("financial-health", "risk-factors")


def load_run(claims_path: Path, findings_dir: Path) -> list[dict]:
    """Claim rows, each with its attributed section added."""
    secs = section_texts(findings_dir)
    rows = []
    for line in claims_path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        r["attributed"] = attribute(r["claim"], secs.get((r["ticker"], r["arm"]), {})) \
            or "unattributed"
        rows.append(r)
    return rows


def tally(rows, pred=lambda r: True) -> tuple[int, int]:
    sel = [r for r in rows if pred(r)]
    return sum(r["judge_label"] == "UNSUPPORTED" for r in sel), len(sel)


def pairwise(runs: dict, pred=lambda r: True) -> list[tuple]:
    out = []
    for a, b in combinations(runs, 2):
        (ua, na), (ub, nb) = tally(runs[a], pred), tally(runs[b], pred)
        out.append((a, b, ua, na, ub, nb, fisher_exact(ua, na - ua, ub, nb - ub)))
    return out


def pooled(runs: dict, name: str, members: list[str], pred=lambda r: True) -> list[tuple]:
    """Fisher of the pooled member runs against each run outside the pool."""
    pool = [r for m in members for r in runs[m]]
    up, np_ = tally(pool, pred)
    out = []
    for label, rows in runs.items():
        if label in members:
            continue
        u, n = tally(rows, pred)
        out.append((label, name, u, n, up, np_, fisher_exact(u, n - u, up, np_ - up)))
    return out


def fmt_p(p: float) -> str:
    return f"{p:.4f}" if p >= 1e-4 else f"{p:.1e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", nargs=3, action="append", required=True,
                    metavar=("LABEL", "CLAIMS_JSONL", "FINDINGS_DIR"))
    ap.add_argument("--pool", nargs="+", action="append", default=[],
                    metavar="NAME LABEL",
                    help="pool the labeled runs under NAME and test every other "
                         "run against the pool (e.g. --pool hosted-pooled kcf7s dvvxk)")
    args = ap.parse_args()
    runs = {label: load_run(Path(c), Path(f)) for label, c, f in args.run}
    for name, *members in args.pool:
        if len(members) < 2 or any(m not in runs for m in members):
            ap.error(f"--pool {name}: needs two or more labels given by --run")

    print("Per run (all judged claims):")
    for label, rows in runs.items():
        u, n = tally(rows)
        print(f"  {label:<14} {u}/{n} = {format_rate_ci(u, n)}")

    print("\nPairwise, exact two-sided Fisher (all claims):")
    for a, b, ua, na, ub, nb, p in pairwise(runs):
        print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")

    for name, *members in args.pool:
        print(f"\nPooled {name} ({' + '.join(members)}), exact two-sided Fisher "
              f"(all claims):")
        for a, b, ua, na, ub, nb, p in pooled(runs, name, members):
            print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")

    print("\nPer section (attributed; unsupported/claims = rate, 95% CI):")
    for sec in SECTIONS:
        print(f"  {sec}")
        for label, rows in runs.items():
            u, n = tally(rows, lambda r, s=sec: r["attributed"] == s)
            print(f"    {label:<14} {u}/{n} = {format_rate_ci(u, n)}")

    owned = lambda r: r["attributed"] in OWNED  # noqa: E731
    rest = lambda r: r["attributed"] not in OWNED  # noqa: E731
    for title, pred in (("Financial Health + Risk Factors (fine-tune-owned in the "
                         "local arms)", owned), ("All other claims", rest)):
        print(f"\n{title}, per run:")
        for label, rows in runs.items():
            u, n = tally(rows, pred)
            print(f"  {label:<14} {u}/{n} = {format_rate_ci(u, n)}")
        print(f"{title}, pairwise Fisher:")
        for a, b, ua, na, ub, nb, p in pairwise(runs, pred):
            print(f"  {a:<14} vs {b:<14} {ua}/{na} vs {ub}/{nb}   p = {fmt_p(p)}")


if __name__ == "__main__":
    main()
