#!/usr/bin/env python3
"""Summarise a `kubectl top pods` capture taken during an eval run.

The runbook's sampler appends, every 15 s, a `== <UTC time>` line and the
`kubectl top pods` rows. This groups the rows by workload — the llama.cpp
endpoint, the eval pods (all of a run's eval-one pods together), and each
app Deployment — and prints samples, median and peak CPU (millicores) and
peak memory, so "the endpoint is saturated and the harness is idle" is a
number read from the capture, not an impression.

Eval pods are also split into startup spikes and steady state: a pod's
first samples include imports and the embedding-model load. `--spike`
(default 100m) is the line between the two.

  python3 scripts/top_summary.py eval/runs/top-cpu-ext.txt

Host-side only, stdlib only.
"""
import argparse
import re
import sys

_ROW = re.compile(r"^(\S+)\s+(?:\S+\s+)?(\d+)m\s+(\d+)Mi\s*$")


def group_of(pod: str) -> str:
    if "-eval-one-" in pod:
        return "eval pods"
    if "-aggregate-" in pod:
        return "aggregate pod"
    return pod.split("-")[0]


def parse(text: str) -> tuple[int, dict]:
    """(number of samples, {group: [(millicores, MiB, pod)]})."""
    samples, rows = 0, {}
    for line in text.splitlines():
        if line.startswith("=="):
            samples += 1
            continue
        m = _ROW.match(line.rstrip())
        if m:
            rows.setdefault(group_of(m.group(1)), []).append(
                (int(m.group(2)), int(m.group(3)), m.group(1)))
    return samples, rows


def median(vals: list) -> float:
    s = sorted(vals)
    return (s[(len(s) - 1) // 2] + s[len(s) // 2]) / 2


def summarize(rows: dict, spike: int) -> dict:
    out = {}
    for group, r in sorted(rows.items()):
        cpu = [c for c, _m, _p in r]
        out[group] = {"readings": len(r), "pods": len({p for _c, _m, p in r}),
                      "cpu_median": median(cpu), "cpu_max": max(cpu),
                      "mem_median": median([m for _c, m, _p in r]),
                      "mem_max": max(m for _c, m, _p in r)}
        if group == "eval pods":
            steady = [c for c in cpu if c < spike]
            out[group].update(spikes=len(cpu) - len(steady),
                              steady_median=median(steady) if steady else None,
                              steady_max=max(steady) if steady else None)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("capture")
    ap.add_argument("--spike", type=int, default=100,
                    help="eval-pod readings at or above this many millicores count as startup")
    args = ap.parse_args(argv)
    with open(args.capture, encoding="utf-8", errors="replace") as f:
        samples, rows = parse(f.read())
    print(f"{args.capture}: {samples} samples")
    print(f"  {'workload':<14} {'pods':>4} {'readings':>8} {'CPU median':>11} {'CPU peak':>9} "
          f"{'mem median':>11} {'mem peak':>9}")
    summary = summarize(rows, args.spike)
    for group, s in summary.items():
        print(f"  {group:<14} {s['pods']:>4} {s['readings']:>8} {s['cpu_median']:>10.0f}m "
              f"{s['cpu_max']:>8}m {s['mem_median']:>9.0f}Mi {s['mem_max']:>7}Mi")
    ev = summary.get("eval pods")
    if ev:
        print(f"  eval pods: {ev['spikes']} of {ev['readings']} readings at or above {args.spike}m "
              f"(startup); the rest median {ev['steady_median']:.0f}m, max {ev['steady_max']}m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
