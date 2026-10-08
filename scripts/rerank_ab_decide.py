#!/usr/bin/env python3
"""Ship or don't ship cross-encoder reranking: the decision of the reranking
A/B, on criteria stated before it ran (2026-10-08, eval-methodology
"Reranking A/B, pre-registered"). Two fresh 40-ticker hosted runs on one
image in one window: baseline (top-3 cosine) and rerank3 (20 candidates
reranked to 3).

Reranking SHIPS only if all four hold:
  1. refusals   the SEC-highlights RAG refusals (eval/rag_refusals.py)
                fall, paired by ticker over the tickers with a highlights
                answer: b = baseline refused and rerank3 did not, c = the
                reverse; b - c >= 3 and exact two-sided McNemar p < 0.05
  2. numeric    TRUE_ERROR per checked number (numeric check, adjudicated):
                the upper end of the 95% CI of rerank3 - baseline is at most
                +0.5 percentage points (scripts/numeric_adjudicated.py)
  3. density    figures bound to a stock-data field per brief
                (eval/density_check.py): the lower end of the 95% CI of
                rerank3 - baseline is at least -0.5
  4. latency    the per-ticker time reranking adds, warm
                (scripts/rerank_latency_bench.py: 2 x the paired median
                per-query difference), is at most 20% of the baseline run's
                mean pipeline time per ticker
Reported, not deciding: judge-flagged grounding over three judgings
(eval/three_judging_stats.py). It BLOCKS shipping only if rerank3 is worse
with the paired CI excluding zero.

  python scripts/rerank_ab_decide.py --baseline <run> --rerank <run> \\
      --adjudication eval/numeric_check/adjudication-<date>-<base>-<rr>.csv \\
      --latency eval/runs/rerank-latency-<date>.json \\
      --judgings-baseline raw <dir> <dir> --judgings-rerank raw <dir> <dir>
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from eval import density_check as dc  # noqa: E402
from eval import multi_arm_stats as mas  # noqa: E402
from eval import rag_refusals as rr  # noqa: E402

REFUSAL_MIN_DROP = 3
NUMERIC_MAX_UPPER = 0.005          # +0.5 percentage points, as a rate
DENSITY_MIN_LOWER = -0.5
LATENCY_MAX_SHARE = 0.20


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def refusals(base: dict, rer: dict) -> dict:
    common = sorted(set(base) & set(rer))
    b = sum(1 for t in common if base[t] and not rer[t])
    c = sum(1 for t in common if rer[t] and not base[t])
    p = mcnemar_exact(b, c)
    return {"tickers": len(common), "baseline_refusals": sum(base[t] for t in common),
            "rerank_refusals": sum(rer[t] for t in common), "b": b, "c": c, "p": p,
            "pass": b - c >= REFUSAL_MIN_DROP and p < 0.05}


def numeric(adj: Path | None, base: str, rer: str) -> dict:
    if adj is None or not adj.exists():
        return {"pass": None, "note": "no adjudication file yet"}
    import csv
    with open(adj, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if any(not r["verdict"].strip() for r in rows):
        return {"pass": None, "note": "adjudication pending"}
    import numeric_adjudicated as na
    res = na.run_three_way(adj, [base, rer], "decide")
    d = res["true_error_rates"]["true_error"]["differences"][f"{rer} - {base}"]
    ci = d.get("ci95") or [0.0, 0.0]
    return {"difference": d["difference"], "ci95": ci, "pass": ci[1] <= NUMERIC_MAX_UPPER}


def density(base: str, rer: str) -> dict:
    pr = mas.paired(dc.text_density(rer), dc.text_density(base), "bound")
    return {"rerank_minus_baseline": pr["mean_diff"], "ci": pr["ci"], "pass": pr["ci"][0] >= DENSITY_MIN_LOWER}


def latency(bench: dict, baseline_pipeline_s: float) -> dict:
    added = bench["per_ticker_added_s_median"]
    share = added / baseline_pipeline_s
    return {"added_s_per_ticker": added, "baseline_pipeline_s": baseline_pipeline_s,
            "share": share, "pass": share <= LATENCY_MAX_SHARE}


def baseline_pipeline_s(run: str) -> float:
    from workflow_nodes import eval_results
    wf = next((ROOT / "eval" / "runs").glob(f"**/*{run}-workflow.json"))
    pods = eval_results(json.loads(wf.read_text(encoding="utf-8")))
    vals = [r["pipeline_s"] for p in pods for r in p.get("results", []) if r.get("pipeline_s")]
    return sum(vals) / len(vals)


def grounding(base: str, rer: str, jb: list[str], jr: list[str]) -> dict:
    from eval import three_judging_stats as tj
    a = [tj.judging_counts(base, s) for s in jb]
    b = [tj.judging_counts(rer, s) for s in jr]
    pr = tj.paired_only(tj.ticker_rates(b), tj.ticker_rates(a), "rate")
    return {"rerank_minus_baseline_pts": pr["mean_diff"] * 100,
            "ci_pts": [x * 100 for x in pr["ci"]], "blocks": pr["ci"][0] > 0}


def decide(parts: dict) -> str:
    crit = [parts[k]["pass"] for k in ("refusals", "numeric", "density", "latency")]
    if parts.get("grounding", {}).get("blocks"):
        return "DON'T SHIP (judge-flagged grounding worse, CI excludes zero)"
    if any(c is False for c in crit):
        return "DON'T SHIP"
    if any(c is None for c in crit):
        return "PENDING"
    return "SHIP"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--rerank", required=True)
    ap.add_argument("--adjudication", type=Path)
    ap.add_argument("--latency", type=Path, required=True)
    ap.add_argument("--judgings-baseline", nargs=3)
    ap.add_argument("--judgings-rerank", nargs=3)
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args(argv)
    parts = {
        "refusals": refusals(rr.run_refusals(args.baseline), rr.run_refusals(args.rerank)),
        "numeric": numeric(args.adjudication, args.baseline, args.rerank),
        "density": density(args.baseline, args.rerank),
        "latency": latency(json.loads(args.latency.read_text(encoding="utf-8")), baseline_pipeline_s(args.baseline)),
    }
    if args.judgings_baseline and args.judgings_rerank:
        parts["grounding"] = grounding(args.baseline, args.rerank, args.judgings_baseline, args.judgings_rerank)
    parts["decision"] = decide(parts)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(parts, indent=2, default=str))
    if args.json_out:
        args.json_out.write_text(json.dumps(parts, indent=2, default=str) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
