#!/usr/bin/env python3
"""Tally adjudicated error types of the judge-UNSUPPORTED numeric claims.

The adjudication (one type per claim, with its evidence note) is a
committed JSON file written by hand from the findings — see
eval/runs/numeric-error-types-2026-10-05.json. This script makes the counts
re-runnable and keeps the file honest: every UNSUPPORTED numeric claim
(claim text contains a digit, as eval.label.numeric_claim_counts) in each
run's claims file must be classified exactly once, and nothing else may be.

Prints counts by type per run, then model errors (wrong value + wrong
label + not in context: everything except source conflicts and judge
errors) over each run's numeric claims with Wilson CIs and an exact
two-sided Fisher test for every pair — unadjusted for multiple
comparisons — and the claims whose judge reason is recorded as incorrect.

  python eval/error_types.py eval/runs/numeric-error-types-2026-10-05.json

Host-side only.
"""
import argparse
import json
import re
import sys
from itertools import combinations
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from eval.stats import fisher_exact, format_rate_ci  # noqa: E402

MODEL_ERRORS = ("wrong value", "wrong label", "not in context")


def numeric(claim) -> bool:
    return bool(re.search(r"\d", claim or ""))


def load(spec: dict, root: Path = _REPO) -> dict:
    """{run: {"numeric": n, "unsupported": [(ticker, claim)]}} from the claims files."""
    out = {}
    for run, path in spec["runs"].items():
        rows = [json.loads(line) for line in (root / path).read_text(encoding="utf-8").splitlines()
                if line.strip()]
        num = [r for r in rows if numeric(r["claim"])]
        out[run] = {"numeric": len(num),
                    "unsupported": sorted((r["ticker"], r["claim"]) for r in num
                                          if r["judge_label"] == "UNSUPPORTED")}
    return out


def check(spec: dict, runs: dict) -> list[str]:
    """Problems: unknown types, and any mismatch between the classified
    claims and the UNSUPPORTED numeric claims of each run."""
    problems = [f"unknown type {c['type']!r} ({c['run']} {c['ticker']})"
                for c in spec["classified"] if c["type"] not in spec["types"]]
    for run, r in runs.items():
        listed = sorted((c["ticker"], c["claim"]) for c in spec["classified"] if c["run"] == run)
        for t, c in sorted(set(r["unsupported"]) - set(listed)):
            problems.append(f"{run}: unclassified {t} {c!r}")
        for t, c in sorted(set(listed) - set(r["unsupported"])):
            problems.append(f"{run}: classified but not an UNSUPPORTED numeric claim: {t} {c!r}")
        if len(listed) != len(set(listed)):
            problems.append(f"{run}: a claim is classified more than once")
    return problems


def tally(spec: dict) -> dict:
    out = {run: {t: [] for t in spec["types"]} for run in spec["runs"]}
    for c in spec["classified"]:
        out[c["run"]][c["type"]].append(c["ticker"])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("adjudication")
    args = ap.parse_args(argv)
    spec = json.loads(Path(args.adjudication).read_text(encoding="utf-8"))
    runs = load(spec)
    problems = check(spec, runs)
    if problems:
        print("\n".join(problems))
        return 1
    t = tally(spec)
    print("Judge-UNSUPPORTED numeric claims by adjudicated type (tickers):")
    w = max(map(len, spec["runs"]))
    for run in spec["runs"]:
        cells = "; ".join(f"{k} {len(v)}" + (f" ({', '.join(v)})" if v else "")
                          for k, v in t[run].items())
        print(f"  {run:<{w}}  {len(runs[run]['unsupported'])}/{runs[run]['numeric']}: {cells}")
    print("\nModel errors (" + " + ".join(MODEL_ERRORS) + ") over numeric claims:")
    me = {run: sum(len(t[run][k]) for k in MODEL_ERRORS) for run in spec["runs"]}
    for run in spec["runs"]:
        print(f"  {run:<{w}}  {me[run]}/{runs[run]['numeric']} = "
              f"{format_rate_ci(me[run], runs[run]['numeric'])}")
    print("Pairwise, exact two-sided Fisher, unadjusted:")
    for a, b in combinations(spec["runs"], 2):
        na, nb = runs[a]["numeric"], runs[b]["numeric"]
        p = fisher_exact(me[a], na - me[a], me[b], nb - me[b])
        print(f"  {a:<{w}} vs {b:<{w}}  {me[a]}/{na} vs {me[b]}/{nb}   p = {p:.4f}")
    wrong_reason = [c for c in spec["classified"] if c.get("judge_reason_incorrect")]
    if wrong_reason:
        print("\nVerdict stands, judge's stated reason incorrect:")
        for c in wrong_reason:
            print(f"  {c['run']} {c['ticker']}: {c['judge_reason_incorrect']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
