#!/usr/bin/env python3
"""eval_aggregate.py — final step of the Argo grounding-eval workflow.

Input: a JSON array of strings, each string being the --json-out payload of one
fanned-out grounding_check.py pod (one ticker each). Merges the per-ticker
results, prints the aggregate table, and enforces the quality gate:

  exit 1  if unsupported% > --max-unsupported-pct   (grounding regression)
  exit 1  if any ticker was skipped                 (incomplete eval is not a pass)
  exit 1  if total claims < --min-claims            (degenerate run can't pass 0/0)

A non-zero exit fails the Argo workflow, which is the point: the nightly eval
is a gate, not a report. Pure-stdlib on purpose — the aggregate pod starts fast.
"""
import sys
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Aggregate fanned-out grounding results.")
    parser.add_argument("--input", required=True,
                        help="Path to a JSON array of per-pod grounding_check --json-out strings.")
    parser.add_argument("--max-unsupported-pct", type=float, default=5.0)
    parser.add_argument("--min-claims", type=int, default=30,
                        help="Fail if fewer total claims were audited (guards against a "
                             "degenerate run passing on an empty denominator).")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        elements = json.load(f)

    results, skipped = [], []
    for el in elements:
        payload = json.loads(el) if isinstance(el, str) else el
        results.extend(payload.get("results", []))
        skipped.extend(payload.get("skipped", []))

    sup = sum(r["supported"] for r in results)
    uns = sum(r["unsupported"] for r in results)
    inf = sum(r["inference"] for r in results)
    tot = sum(r["total"] for r in results)
    n = len(results)
    unsupported_pct = (uns / tot * 100) if tot else 100.0
    mean_retr = sum(r["retrieval_s"] for r in results) / n if n else 0.0
    mean_pipe = sum(r["pipeline_s"] for r in results) / n if n else 0.0

    print("=" * 78)
    print("  NIGHTLY GROUNDING EVAL — AGGREGATE")
    print("=" * 78)
    print(f"  {'Ticker':<8} {'Sup':>4} {'Uns':>4} {'Inf':>4} {'Tot':>4} {'Retr(s)':>8} {'Pipe(s)':>8}")
    print(f"  {'-'*44}")
    for r in sorted(results, key=lambda r: r["ticker"]):
        print(f"  {r['ticker']:<8} {r['supported']:>4} {r['unsupported']:>4} "
              f"{r['inference']:>4} {r['total']:>4} {r['retrieval_s']:>8.2f} {r['pipeline_s']:>8.2f}")
    print(f"  {'-'*44}")
    print(f"  {'TOTAL':<8} {sup:>4} {uns:>4} {inf:>4} {tot:>4} {mean_retr:>8.2f} {mean_pipe:>8.2f}")
    print()
    print(f"  tickers completed : {n}")
    print(f"  tickers skipped   : {len(skipped)}{' (' + ', '.join(skipped) + ')' if skipped else ''}")
    print(f"  unsupported rate  : {unsupported_pct:.2f}%   (gate: <= {args.max_unsupported_pct}%)")
    print(f"  total claims      : {tot}   (gate: >= {args.min_claims})")

    failures = []
    if unsupported_pct > args.max_unsupported_pct:
        failures.append(f"unsupported rate {unsupported_pct:.2f}% exceeds {args.max_unsupported_pct}%")
    if skipped:
        failures.append(f"{len(skipped)} ticker(s) skipped: {', '.join(skipped)}")
    if tot < args.min_claims:
        failures.append(f"only {tot} claims audited (< {args.min_claims})")

    print()
    if failures:
        for f_ in failures:
            print(f"  GATE FAILED: {f_}")
        print("=" * 78)
        sys.exit(1)
    print("  GATE PASSED")
    print("=" * 78)


if __name__ == "__main__":
    main()
