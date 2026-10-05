#!/usr/bin/env python3
"""Summarise an nvidia-smi sampler CSV per run window.

The sampler on node 2 appends one row every 5 s from

  nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv -l 5

(timestamp in the node's clock, UTC on the OCI Ubuntu images). One capture
can span several runs, so it is sliced into windows: an Argo run's window is
its workflow object's status.startedAt..finishedAt (--workflow), anything
else is given by hand (--window, e.g. a tool-use route bounded by file
mtimes — put "approx" in its label). Per window: samples, GPU utilization
mean / median / p95 / max, the share of samples above 0%, and memory.used
min / max. memory.used is the whole GPU's, not one process's
(nvidia-smi --query-compute-apps gives that). The last row counts samples
outside every window, so GPU activity no window explains stays visible.

  python3 scripts/nvsmi_summary.py eval/runs/gpu-nvsmi-p9jr2.csv \\
      --window "tool-use gpu (approx)" 2026-10-05T02:59:15Z 2026-10-05T02:59:57Z \\
      --workflow k6zxd eval/runs/slm-proof-k6zxd/grounding-eval-slm-gpu-k6zxd-workflow.json

Host-side only, stdlib only.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone


def parse_csv(text: str) -> list[tuple[datetime, int, int]]:
    """[(UTC time, utilization %, memory.used MiB)], header skipped."""
    out = []
    for row in csv.reader(text.splitlines()):
        if not row or row[0].startswith("timestamp"):
            continue
        t = datetime.strptime(row[0].strip(), "%Y/%m/%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
        out.append((t, int(row[1].split()[0]), int(row[2].split()[0])))
    return out


def iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def workflow_window(path: str) -> tuple[datetime, datetime]:
    with open(path, encoding="utf-8") as f:
        st = json.load(f)["status"]
    return iso(st["startedAt"]), iso(st["finishedAt"])


def pct(vals: list[int], q: float) -> float:
    """Nearest-rank percentile."""
    s = sorted(vals)
    return s[max(0, -(-len(s) * q // 100) - 1)] if s else 0


def summarize(samples: list[tuple], start: datetime, end: datetime) -> dict | None:
    sel = [(u, m) for t, u, m in samples if start <= t <= end]
    if not sel:
        return None
    util = [u for u, _ in sel]
    mem = [m for _, m in sel]
    return {"samples": len(sel), "mean": sum(util) / len(util), "median": pct(util, 50),
            "p95": pct(util, 95), "max": max(util), "busy": sum(u > 0 for u in util),
            "mem_min": min(mem), "mem_max": max(mem)}


def outside(samples: list[tuple], windows: list[tuple]) -> dict:
    rest = [(t, u) for t, u, _ in samples
            if not any(s <= t <= e for _, s, e in windows)]
    busy = [t for t, u in rest if u > 0]
    return {"samples": len(rest), "busy": len(busy),
            "first_busy": busy[0] if busy else None, "last_busy": busy[-1] if busy else None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("csv")
    ap.add_argument("--workflow", nargs=2, action="append", default=[], metavar=("LABEL", "FILE"))
    ap.add_argument("--window", nargs=3, action="append", default=[],
                    metavar=("LABEL", "START", "END"))
    args = ap.parse_args(argv)
    with open(args.csv, encoding="utf-8") as f:
        samples = parse_csv(f.read())
    windows = [(label, iso(s), iso(e)) for label, s, e in args.window]
    windows += [(label, *workflow_window(p)) for label, p in args.workflow]
    windows.sort(key=lambda w: w[1])

    first, last = samples[0][0], samples[-1][0]
    print(f"{args.csv}: {len(samples)} samples, {first:%Y-%m-%d %H:%M:%S} to {last:%H:%M:%S} UTC")
    print(f"  {'window':<24} {'start':>8} {'end':>8} {'samples':>7} {'util mean':>9} "
          f"{'median':>6} {'p95':>4} {'max':>4} {'>0%':>9} {'mem.used MiB':>13}")
    for label, s, e in windows:
        r = summarize(samples, s, e)
        if r is None:
            print(f"  {label:<24} {s:%H:%M:%S} {e:%H:%M:%S}  no samples")
            continue
        print(f"  {label:<24} {s:%H:%M:%S} {e:%H:%M:%S} {r['samples']:>7} {r['mean']:>8.1f}% "
              f"{r['median']:>5}% {r['p95']:>3}% {r['max']:>3}% "
              f"{r['busy']:>3} ({100 * r['busy'] / r['samples']:>3.0f}%) "
              f"{r['mem_min']:>6}-{r['mem_max']}")
    o = outside(samples, windows)
    span = (f", first {o['first_busy']:%H:%M:%S}, last {o['last_busy']:%H:%M:%S}"
            if o["busy"] else "")
    print(f"  outside every window: {o['samples']} samples, {o['busy']} above 0%{span}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
