#!/usr/bin/env python3
"""Reconstruct per-claim rows for an Argo eval run from its captured
artifacts: the pod log (per-ticker count lines) and the workflow yaml
(per-pod result output parameters, which carry INFERENCE claim texts).

Honesty of the output, stated up front: the run's full per-claim findings
(claim texts for SUPPORTED/UNSUPPORTED, rationales, sections, contexts)
were written to /app/eval_findings INSIDE the eval pods and are not in
these artifacts — the known archival gap. Rows therefore carry:
  claim            text for INFERENCE claims (from inference_claims in the
                   pod result params); null otherwise
  judge_label      always present (reconstructed from the counts)
  judge_rationale  always null (not persisted anywhere)
  section          always null (not persisted anywhere)
  context_hash     always null (contexts not persisted anywhere)
  source           which artifact the row came from
The parser cross-checks log counts against workflow-parameter counts per
(ticker, arm) and reports mismatches.

Usage:
  python eval/parse_run_log.py --log eval/runs/9j2dj-full.log \
      --workflow-yaml eval/runs/9j2dj-workflow.yaml \
      --run grounding-eval-extended-9j2dj \
      --out eval/runs/9j2dj-claims.jsonl
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

_LOG_LINE = re.compile(
    r"\[(?P<ticker>[A-Z.-]{1,6}) \| (?P<arm>[\w-]+)\]\s+(?P<sup>\d+) SUP\s+"
    r"(?P<uns>\d+) UNSUP\s+(?P<inf>\d+) INF\s+\((?P<tot>\d+) claims\)")


def parse_log_counts(log_text: str) -> dict:
    counts = {}
    for m in _LOG_LINE.finditer(log_text):
        counts[(m["ticker"], m["arm"])] = {
            "supported": int(m["sup"]), "unsupported": int(m["uns"]),
            "inference": int(m["inf"]), "total": int(m["tot"]),
        }
    return counts


def parse_workflow_results(wf: dict) -> dict:
    """(ticker, arm) -> result row dicts from eval-one nodes' output params."""
    rows = {}
    for node in (wf.get("status", {}).get("nodes", {}) or {}).values():
        if node.get("templateName") != "eval-one":
            continue
        for p in (node.get("outputs", {}) or {}).get("parameters", []) or []:
            if p.get("name") != "result" or not p.get("value"):
                continue
            payload = json.loads(p["value"])
            for row in payload.get("results", []):
                rows[(row["ticker"], row["arm"])] = row
    return rows


def emit_rows(run: str, results: dict) -> list[dict]:
    out = []
    for (ticker, arm), row in sorted(results.items()):
        base = {
            "run": run, "ticker": ticker, "arm": arm,
            "judge_version": row.get("judge_version"),
            "section": None, "judge_rationale": None, "context_hash": None,
        }
        inf_texts = list(row.get("inference_claims") or [])
        if len(inf_texts) != row["inference"]:
            print(f"WARNING: {ticker}/{arm}: {len(inf_texts)} inference texts "
                  f"vs count {row['inference']}")
        for label, n in (("SUPPORTED", row["supported"]),
                         ("UNSUPPORTED", row["unsupported"])):
            for _ in range(n):
                out.append({**base, "claim": None, "judge_label": label,
                            "source": "reconstructed-from-counts"})
        for i in range(row["inference"]):
            out.append({**base,
                        "claim": inf_texts[i] if i < len(inf_texts) else None,
                        "judge_label": "INFERENCE",
                        "source": "workflow-output-params:inference_claims"})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    ap.add_argument("--workflow-yaml", required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    log_counts = parse_log_counts(Path(args.log).read_text(encoding="utf-8"))
    wf = yaml.safe_load(Path(args.workflow_yaml).read_text(encoding="utf-8"))
    results = parse_workflow_results(wf)

    mismatched = []
    for key, lc in sorted(log_counts.items()):
        wr = results.get(key)
        if not wr:
            mismatched.append((key, "in log, missing from workflow params"))
        elif any(lc[k] != wr[k] for k in ("supported", "unsupported", "inference", "total")):
            mismatched.append((key, f"log {lc} != params "
                                    f"{ {k: wr[k] for k in lc} }"))
    for key in results:
        if key not in log_counts:
            mismatched.append((key, "in workflow params, missing from log"))

    rows = emit_rows(args.run, results)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    with_text = sum(1 for r in rows if r["claim"])
    by_label = {}
    for r in rows:
        by_label[r["judge_label"]] = by_label.get(r["judge_label"], 0) + 1
    tots = [results[k]["total"] for k in results]
    print(f"rows: {len(rows)} ({by_label}) | claim text present: {with_text} "
          f"(INFERENCE only — findings were pod-local, see module docstring)")
    print(f"tickers: {len(results)} | per-ticker claims min={min(tots)} max={max(tots)}")
    print(f"log-vs-params mismatches: {mismatched if mismatched else 'none'}")


if __name__ == "__main__":
    main()
