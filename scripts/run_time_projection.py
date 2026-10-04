#!/usr/bin/env python3
"""Measured per-ticker wall time of a finished eval workflow, projected to a
larger run, checked against that run's deadlines — the gate before the CPU
SLM extended run.

Input: `kubectl get workflow <wf> -o json` of the smoke (stdin or --workflow);
compressed node status is read through scripts/workflow_nodes.py.
Per-ticker time is each eval-ticker task's wall time as Argo recorded it
(the Retry node when the task has one, so a retried ticker counts its full
time), measured under the run's own parallelism — endpoint contention
between concurrent pods is already in it.

Projection for N tickers at parallelism P (the template's):
  mean   ceil(N/P) waves x mean ticker time      (throughput estimate)
  worst  ceil(N/P) waves x slowest ticker time   (the one gated on)
plus the aggregate step's measured time. Gate (exit 1 = do not launch):
  - worst projection        <= the next run file's activeDeadlineSeconds
  - slowest smoke ticker    <= 75% of its ticker-deadline-seconds (the
    extended set has tickers the smoke never ran; 25% headroom)
  - worst projection        <  the 7-day ttlStrategy, with a day to spare
    for capture (findings live in the pod logs until the TTL deletes them)

  kubectl -n financial-agent get workflow <wf> -o json | \\
    python3 scripts/run_time_projection.py --next argo/eval-run-extended-slm-cpu.yaml
Stdlib only, no newer-than-3.6 syntax.
"""
import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from workflow_nodes import expand  # noqa: E402  (status.compressedNodes -> status.nodes)
from datetime import datetime

TTL_SECONDS = 7 * 86400  # argo/overlays/oke-provided ttlStrategy
CAPTURE_SPARE = 86400
TICKER_MARGIN = 0.75
# The task node is "eval-ticker(<i>:<ticker>)"; a retried task's attempt pods
# append "(<n>)" and must not count as extra tickers.
_TASK_RE = re.compile(r"^eval-ticker\(\d+:[^()]*\)$")


def _t(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def ticker_times(wf):
    """{display name: seconds} for every finished eval-ticker task."""
    by_name = {}
    for n in (wf.get("status", {}).get("nodes") or {}).values():
        name = n.get("displayName", "")
        if not _TASK_RE.match(name) or n.get("type") not in ("Retry", "Pod"):
            continue
        if not (n.get("startedAt") and n.get("finishedAt")):
            continue
        # Prefer the Retry node: it spans every attempt of the task.
        if name in by_name and by_name[name][0] == "Retry":
            continue
        secs = (_t(n["finishedAt"]) - _t(n["startedAt"])).total_seconds()
        by_name[name] = (n["type"], secs, n.get("phase"))
    return {k: v[1] for k, v in by_name.items()}, {k: v[2] for k, v in by_name.items()}


def aggregate_time(wf):
    for n in (wf.get("status", {}).get("nodes") or {}).values():
        if n.get("displayName") == "aggregate" and n.get("startedAt") and n.get("finishedAt"):
            return (_t(n["finishedAt"]) - _t(n["startedAt"])).total_seconds()
    return 0.0


def parallelism(wf):
    spec = wf.get("status", {}).get("storedWorkflowTemplateSpec") or wf.get("spec") or {}
    return int(spec.get("parallelism") or 1)


def run_file_deadlines(text):
    """(workflow activeDeadlineSeconds, ticker-deadline-seconds) from a run file."""
    spec = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    wf = re.search(r"^\s{2}activeDeadlineSeconds:\s*(\d+)", spec, re.M)
    td = re.search(r"name: ticker-deadline-seconds\s+value:\s*\"?(\d+)", spec)
    tickers = re.search(r"name: tickers\s+value:\s*'(\[.*?\])'", spec, re.S)
    return (int(wf.group(1)) if wf else None, int(td.group(1)) if td else 1200,
            len(json.loads(tickers.group(1))) if tickers else 10)


def _hm(s):
    return "%dh%02dm" % (s // 3600, (s % 3600) // 60)


def project(wf, next_text):
    times, phases = ticker_times(wf)
    if not times:
        raise SystemExit("run_time_projection: no finished eval-ticker tasks in this workflow")
    p = parallelism(wf)
    wf_deadline, ticker_deadline, n_next = run_file_deadlines(next_text)
    agg = aggregate_time(wf)
    mean = sum(times.values()) / len(times)
    worst = max(times.values())
    waves = math.ceil(n_next / p)
    proj_mean = waves * mean + agg
    proj_worst = waves * worst + agg
    lines = [
        "smoke: %d tickers, parallelism %d, per ticker mean %s, min %s, max %s; aggregate %s"
        % (len(times), p, _hm(mean), _hm(min(times.values())), _hm(worst), _hm(agg)),
        "not Succeeded: %s" % (", ".join(sorted(k for k, v in phases.items() if v != "Succeeded")) or "none"),
        "projected %d tickers (%d waves of %d): mean %s, worst %s"
        % (n_next, waves, p, _hm(proj_mean), _hm(proj_worst)),
    ]
    checks = [
        ("worst projection <= workflow deadline %s" % (_hm(wf_deadline) if wf_deadline else "(none set)"),
         wf_deadline is not None and proj_worst <= wf_deadline),
        ("slowest smoke ticker %s <= %d%% of ticker deadline %s"
         % (_hm(worst), TICKER_MARGIN * 100, _hm(ticker_deadline)),
         worst <= TICKER_MARGIN * ticker_deadline),
        ("worst projection + 1 day capture < 7-day TTL", proj_worst + CAPTURE_SPARE < TTL_SECONDS),
    ]
    for label, ok in checks:
        lines.append(("PASS  " if ok else "FAIL  ") + label)
    return all(ok for _, ok in checks), lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--workflow", help="kubectl get workflow -o json output (default: stdin)")
    ap.add_argument("--next", required=True, help="the run file about to be launched")
    args = ap.parse_args(argv)
    wf = expand(json.load(open(args.workflow) if args.workflow else sys.stdin))
    with open(args.next) as f:
        ok, lines = project(wf, f.read())
    print("run-time check for %s against %s" % (wf.get("metadata", {}).get("name"), args.next))
    for ln in lines:
        print("  " + ln)
    print("RUN-TIME CHECK: %s" % ("PASS - ok to launch" if ok else "FAIL - do not launch"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
