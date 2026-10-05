#!/usr/bin/env python3
"""Serving cost per brief of an slm-full eval run, from its measured wall time.

Every agent call of an slm-full run goes to the self-served endpoint, so
the brief's model cost is what the endpoint's resource costs while the run
holds it:

  cost per brief = hourly price x (finishedAt - startedAt) / 3600 / briefs

from the workflow object's status (the whole run, aggregate step and pod
scheduling included) and the number of per-ticker result rows. That is the
throughput the run achieved at its own parallelism, not the resource's
capacity: where the resource sat partly idle (the A10 in p9jr2 averaged 38%
utilization at parallelism 2), the figure is a ceiling on cost per brief,
not an estimate of the floor.

Scope: the model serving resource only, as the hosted cost of record is
API cost only. Excluded on every arm: the harness pods, storage (PVCs,
boot volumes) and the judge (eval-only). The multi-agent critic is off.

Price, one of:
  --hourly-usd H                     a whole resource at H per hour
                                     (VM.GPU.A10.1: the GPU price covers
                                     the VM)
  --e5 OCPU GIB --ocpu-usd P --gb-usd Q
                                     E5 Flex: OCPU x P + memory x Q per
                                     hour, memory converted from GiB (a
                                     Kubernetes request) to GB (the SKU)

Also printed, as context: the ledger's tokens and calls per brief, and the
endpoint seconds per brief (sum of call latencies; calls overlap, so this
can exceed the pipeline time).

  python scripts/cost_per_brief_slm.py \\
      eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-workflow.json \\
      --label gpu-p9jr2 --hourly-usd 2.00

Host-side only.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from eval.multi_arm_stats import load_rows  # noqa: E402

GB_PER_GIB = 2 ** 30 / 10 ** 9


def iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def e5_hourly(ocpu: float, gib: float, ocpu_usd: float, gb_usd: float) -> tuple[float, float]:
    """(USD per hour, memory in GB) for an E5 Flex share."""
    gb = gib * GB_PER_GIB
    return ocpu * ocpu_usd + gb * gb_usd, gb


def summarize(workflow: Path, hourly: float) -> dict:
    st = json.loads(workflow.read_text(encoding="utf-8"))["status"]
    wall = (iso(st["finishedAt"]) - iso(st["startedAt"])).total_seconds()
    rows = load_rows(workflow)
    n = len(rows)
    tot = [(r.get("llm") or {}).get("total") or {} for r in rows]

    def per_brief(key):
        return sum(t.get(key) or 0 for t in tot) / n

    return {"workflow": workflow.name, "started": st["startedAt"], "finished": st["finishedAt"],
            "phase": st.get("phase"), "wall_s": wall, "briefs": n, "s_per_brief": wall / n,
            "briefs_per_hour": 3600 * n / wall, "hourly_usd": hourly,
            "usd_per_brief": hourly * wall / 3600 / n,
            "calls": per_brief("calls"), "prompt_tokens": per_brief("prompt_tokens"),
            "completion_tokens": per_brief("completion_tokens"),
            "endpoint_s": per_brief("latency_s_total"),
            "pipeline_s": sum(r["pipeline_s"] for r in rows) / n}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workflow", type=Path)
    ap.add_argument("--label", required=True)
    price = ap.add_mutually_exclusive_group(required=True)
    price.add_argument("--hourly-usd", type=float)
    price.add_argument("--e5", nargs=2, type=float, metavar=("OCPU", "GIB"))
    ap.add_argument("--ocpu-usd", type=float)
    ap.add_argument("--gb-usd", type=float)
    args = ap.parse_args(argv)
    if args.e5:
        if args.ocpu_usd is None or args.gb_usd is None:
            ap.error("--e5 needs --ocpu-usd and --gb-usd")
        hourly, gb = e5_hourly(*args.e5, args.ocpu_usd, args.gb_usd)
        basis = (f"E5 Flex {args.e5[0]:g} OCPU x ${args.ocpu_usd} + {args.e5[1]:g} GiB = "
                 f"{gb:.2f} GB x ${args.gb_usd} = ${hourly:.4f}/h")
    else:
        hourly, basis = args.hourly_usd, f"${args.hourly_usd:.2f}/h, whole resource"
    s = summarize(args.workflow, hourly)
    print(f"{args.label}: {s['workflow']} ({s['phase']})")
    print(f"  window            : {s['started']} .. {s['finished']} = {s['wall_s']:.0f} s")
    print(f"  briefs            : {s['briefs']}  ->  {s['s_per_brief']:.1f} s per brief, "
          f"{s['briefs_per_hour']:.1f} briefs/hour at the run's parallelism")
    print(f"  price             : {basis}")
    print(f"  cost per brief    : ${s['usd_per_brief']:.4f}  (serving only; excludes harness "
          f"pods, storage, judge)")
    print(f"  per brief, ledger : {s['calls']:.2f} calls, {s['prompt_tokens']:.0f} prompt + "
          f"{s['completion_tokens']:.0f} completion tokens, {s['endpoint_s']:.1f} endpoint s; "
          f"pipeline {s['pipeline_s']:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
