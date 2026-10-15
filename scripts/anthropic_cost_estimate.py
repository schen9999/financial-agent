#!/usr/bin/env python3
"""Estimated Anthropic spend of planned eval runs, before topping up the
balance. No API call, no spend: it reads only committed files.

Per run file (argo/eval-run-*.yaml): its arm(s) and ticker count, from the
file or the WorkflowTemplate's defaults (argo/base/eval-workflow.yaml).

  in-cluster  the aggregate's own `est. run cost` (grounding judge,
              RAG-faithfulness judge, and on the hosted arm the Haiku
              sections and Sonnet synthesis; chars/4 tokens priced from
              scripts/model_prices.json, retries excluded) of the committed
              runs of the same arm on the pinned image f3043751, per ticker,
              the highest of the runs with the same ticker count
  re-judges   (judgings - 1) x tickers x one judging of a brief: 3,690 input
              + 725 output tokens (sizes from the 2026-10-06 re-judge,
              eval-methodology "three judgings per run"), Sonnet rates from
              scripts/model_prices.json

The margin (default 1.5x) is a judgement, not a measurement: the estimates
are chars/4 and exclude retries, and billed spend was never reconciled
against them.

  python scripts/anthropic_cost_estimate.py argo/eval-run-extended-slm-cpu.yaml:3 \\
      argo/eval-run-slm-gpu-smoke.yaml:1
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "argo/base/eval-workflow.yaml"
PRICES = ROOT / "scripts/model_prices.json"
JUDGE_MODEL = "claude-sonnet-4-6"
JUDGING_TOKENS_PER_BRIEF = (3690, 725)  # input, output (eval-methodology, 2026-10-06)
IMAGE = "f3043751"

# Committed runs on the pinned image: (arm, aggregate log, the run file it ran).
REFERENCES = [
    ("baseline", "eval/runs/hosted-extended-f304375.log", "argo/eval-run-extended.yaml"),          # 4hsn2
    ("baseline", "eval/runs/rr-ab-baseline-f304375.log", "argo/eval-run-extended.yaml"),           # vks4c
    ("baseline", "eval/runs/hosted-smoke-f304375.log", "argo/eval-run.yaml"),                      # 5jvhh
    ("slm-full-cpu", "eval/runs/cpu-extended-f304375.log", "argo/eval-run-extended-slm-cpu.yaml"),  # 5bdz5
    ("slm-full-cpu", "eval/runs/cpu-rerun-f304375.log", "argo/eval-run-extended-slm-cpu.yaml"),     # 4kkgm
    ("slm-full-cpu", "eval/runs/cpu-smoke-f304375.log", "argo/eval-run-slm-cpu-smoke.yaml"),        # xnwjm
    ("slm-full-gpu", "eval/runs/gpu-extended-f304375.log", "argo/eval-run-extended-slm-gpu.yaml"),  # nstp9
    ("slm-full-gpu", "eval/runs/gpu-p4b-f304375.log", "argo/eval-run-extended-slm-gpu-p4.yaml"),    # xgtxx
    ("slm-full-gpu", "eval/runs/gpu-smoke-f304375.log", "argo/eval-run-slm-gpu-smoke.yaml"),        # m7qvv
]
COST = re.compile(r"est\. run cost\s*:\s*\$([0-9.]+)")


def _params(path):
    params = {}
    for doc in (yaml.safe_load(Path(path).read_text()),):
        spec = (doc or {}).get("spec") or {}
        for p in (spec.get("arguments") or {}).get("parameters") or []:
            params[p["name"]] = p.get("value")
    return params


def run_shape(run_file):
    """(arms, ticker count) of a run file, template defaults filled in."""
    p = {**_params(TEMPLATE), **_params(ROOT / run_file if not Path(run_file).is_absolute() else run_file)}
    arms = [a.strip() for a in str(p["arms"]).split(",") if a.strip()]
    return arms, len(json.loads(p["tickers"]))


def judging_per_brief(prices=None):
    m = (prices or json.loads(PRICES.read_text()))["models"][JUDGE_MODEL]
    tin, tout = JUDGING_TOKENS_PER_BRIEF
    return (tin * m["input_per_mtok"] + tout * m["output_per_mtok"]) / 1e6


def references():
    out = []
    for arm, log, rf in REFERENCES:
        m = COST.search((ROOT / log).read_text(encoding="utf-8", errors="replace"))
        n = run_shape(rf)[1]
        out.append({"arm": arm, "log": log, "tickers": n, "cost": float(m.group(1)),
                    "per_ticker": float(m.group(1)) / n})
    return out


def estimate(run_file, judgings, refs=None):
    refs = refs if refs is not None else references()
    arms, n = run_shape(run_file)
    rows = []
    for arm in arms:
        same = [r for r in refs if r["arm"] == arm]
        if not same:
            raise SystemExit(f"no committed {IMAGE} reference run for arm {arm!r}")
        pool = [r for r in same if r["tickers"] == n] or same
        ref = max(pool, key=lambda r: r["per_ticker"])
        rows.append({"arm": arm, "tickers": n, "ref": ref, "in_cluster": ref["per_ticker"] * n,
                     "rejudges": (judgings - 1) * n * judging_per_brief()})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("runs", nargs="+", help="RUN_FILE[:JUDGINGS] (judgings default 1)")
    ap.add_argument("--margin", type=float, default=1.5)
    args = ap.parse_args(argv)
    refs = references()
    total = 0.0
    for spec in args.runs:
        rf, _, j = spec.partition(":")
        judgings = int(j or 1)
        for r in estimate(rf, judgings, refs):
            sub = r["in_cluster"] + r["rejudges"]
            total += sub
            print(f"{rf}  [{r['arm']}, {r['tickers']} tickers, {judgings} judging(s)]")
            print(f"  in-cluster : ${r['in_cluster']:.2f}  (${r['ref']['per_ticker']:.4f}/ticker from "
                  f"{Path(r['ref']['log']).name}, ${r['ref']['cost']:.4f} over {r['ref']['tickers']})")
            if judgings > 1:
                print(f"  re-judges  : ${r['rejudges']:.2f}  ({judgings - 1} x {r['tickers']} x "
                      f"${judging_per_brief():.4f}/brief)")
            print(f"  subtotal   : ${sub:.2f}")
    print(f"ESTIMATE   : ${total:.2f}   (image {IMAGE} references; retries excluded)")
    print(f"BUDGET     : ${total * args.margin:.2f}   (x{args.margin} margin, a judgement, not measured)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
