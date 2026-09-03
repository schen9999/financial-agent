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

Artifact archival (off by default): when EVAL_ARTIFACTS_PUT_URL is set — an
OCI Object Storage pre-authenticated request that permits writes — the run's
summary and per-ticker results are PUT under eval-runs/<run-id>/ in the
versioned eval-artifacts bucket. Best-effort BY DESIGN: the gate measures
grounding, archival is auxiliary, so an upload failure prints a WARNING and
never changes the exit code. Failed runs are archived too — they are the most
valuable ones to keep.
"""
import sys
import json
import os
import argparse
import urllib.request
from datetime import datetime, timezone


def maybe_upload_artifacts(summary, results, skipped):
    """PUT the run's artifacts to the archive; returns None when disabled,
    else True/False for upload success. Never raises."""
    base = os.getenv("EVAL_ARTIFACTS_PUT_URL", "").strip()
    if not base:
        return None
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    objects = {
        "aggregate.json": summary,
        "results.json": {"results": results, "skipped": skipped},
    }
    ok = True
    for name, doc in objects.items():
        url = f"{base.rstrip('/')}/eval-runs/{run_id}/{name}"
        req = urllib.request.Request(
            url,
            data=json.dumps(doc, indent=2).encode("utf-8"),
            method="PUT",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30):
                pass
        except Exception as e:  # noqa: BLE001 — archival must never fail the gate
            print(f"  WARNING: artifact upload failed for {name}: {e}")
            ok = False
    if ok:
        print(f"  artifacts uploaded: eval-runs/{run_id}/ ({len(objects)} objects)")
    return ok


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

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "supported": sup, "unsupported": uns, "inference": inf, "claims": tot,
            "unsupported_pct": round(unsupported_pct, 2),
            "mean_retrieval_s": round(mean_retr, 2), "mean_pipeline_s": round(mean_pipe, 2),
            "tickers_completed": n, "tickers_skipped": len(skipped),
        },
        "gate": {
            "max_unsupported_pct": args.max_unsupported_pct,
            "min_claims": args.min_claims,
            "passed": not failures,
            "failures": failures,
        },
    }
    maybe_upload_artifacts(summary, results, skipped)

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
