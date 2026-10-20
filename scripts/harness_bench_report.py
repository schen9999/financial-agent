#!/usr/bin/env python3
"""Report for the harness benchmark (docs/harness-benchmark-plan.md).

Reads a captured sweep (one directory per cell repeat, written by
scripts/harness_bench_cell.sh: driver.log, cgroup-before/after.txt,
pods-before/after.json, events.json) and prints, in the plan's order:

  validity per cell repeat (a repeat that fails a check is reported, never used)
  per-cell table: throughput, latency p50/p95, CPU-s per brief, CPU/wall,
                  throttling, peak memory per process, Little's-law check
  the four reading rules exactly as pre-registered

Writes <dir>/results.json beside the captures.

  python scripts/harness_bench_report.py eval/runs/harness-bench-2026-10-20
"""
import json
import re
import statistics
import sys
from pathlib import Path

WAIT_MAX, CPU_BOUND_MIN = 0.25, 0.75     # Q2 thresholds (plan, "Reading rules")
SATURATION_GAIN = 0.10                   # Q3: doubling raises throughput < 10%
LITTLE_GAP = 0.10                        # Little's-law gap reported above 10%
ERROR_MAX = 0.01                         # validity: errors under 1% of briefs

_POD_HDR = re.compile(r"^=== pod (\S+) t=([\d.]+)")
_DIR = re.compile(r"^(L[012])-(?:r(\d+)|keda)-c(\d+)-r(\d+)$")


# ── parsing ─────────────────────────────────────────────────────────────────

def parse_driver(text: str) -> tuple[list, dict | None]:
    briefs, summary = [], None
    for line in text.splitlines():
        if line.startswith("BENCH_BRIEF "):
            briefs.append(json.loads(line[len("BENCH_BRIEF "):]))
        elif line.startswith("BENCH_SUMMARY "):
            summary = json.loads(line[len("BENCH_SUMMARY "):])
    return briefs, summary


def parse_cgroup(text: str) -> dict:
    """{pod: {"cpu_s", "nr_periods", "nr_throttled", "throttled_s",
    "mem_peak", "mem_current", "version"}} from a snapshot file. cgroup v2
    usage_usec / throttled_usec; v1 cpuacct.usage (ns) / throttled_time (ns)."""
    pods, cur = {}, None
    for line in text.splitlines():
        m = _POD_HDR.match(line)
        if m:
            cur = pods.setdefault(m.group(1), {"t": float(m.group(2))})
            continue
        if cur is None:
            continue
        parts = line.split()
        if len(parts) == 2 and parts[0] == "cgroup":
            cur["version"] = parts[1]
            continue
        if len(parts) != 2 or not parts[1].lstrip("-").isdigit():
            continue
        k, v = parts[0], int(parts[1])
        if k == "usage_usec":
            cur["cpu_s"] = v / 1e6
        elif k == "cpuacct.usage":
            cur["cpu_s"] = v / 1e9
        elif k in ("nr_periods", "nr_throttled"):
            cur[k] = v
        elif k == "throttled_usec":
            cur["throttled_s"] = v / 1e6
        elif k == "throttled_time":
            cur["throttled_s"] = v / 1e9
        elif k in ("memory.peak", "memory.max_usage_in_bytes"):
            cur["mem_peak"] = v
        elif k in ("memory.current", "memory.usage_in_bytes"):
            cur["mem_current"] = v
    return pods


def role(pod: str) -> str:
    for r in ("model-stub", "worker", "api", "redis"):
        if pod.startswith(r + "-"):
            return r
    return "other"


def restarts(pods_json: dict) -> dict:
    """{pod: (restarts summed over its containers, a last-termination reason)}."""
    out = {}
    for p in pods_json.get("items", []):
        name = p["metadata"]["name"]
        total, reason = 0, None
        for cs in (p.get("status") or {}).get("containerStatuses") or []:
            total += cs.get("restartCount", 0)
            reason = ((cs.get("lastState") or {}).get("terminated") or {}).get("reason") or reason
        out[name] = (total, reason)
    return out


def pct(xs: list, q: float) -> float | None:
    if not xs:
        return None
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def time_avg_in_flight(briefs: list, t0: float, t1: float) -> float | None:
    """Time-averaged number of briefs running in the workers over [t0, t1]."""
    if not t0 or not t1 or t1 <= t0:
        return None
    total = 0.0
    for b in briefs:
        s, f = b.get("start"), b.get("finish")
        if s is None or f is None:
            continue
        total += max(0.0, min(f, t1) - max(s, t0))
    return total / (t1 - t0)


# ── one cell repeat ─────────────────────────────────────────────────────────

def analyze_repeat(d: Path) -> dict:
    m = _DIR.match(d.name)
    out = {"dir": d.name, "valid": False, "reasons": []}
    if not m:
        out["reasons"].append("unrecognised directory name")
        return out
    out.update({"profile": m.group(1), "keda": m.group(2) is None,
                "replicas": int(m.group(2)) if m.group(2) else None,
                "concurrency": int(m.group(3)), "repeat": int(m.group(4))})
    out["cell"] = re.sub(r"-r\d+$", "", d.name)
    drv = d / "driver.log"
    briefs, s = parse_driver(drv.read_text()) if drv.exists() else ([], None)
    if s is None:
        out["reasons"].append("no BENCH_SUMMARY (driver did not finish)")
        return out
    if out["keda"]:
        out["replicas"] = s["replicas"]
    measured = [b for b in briefs if b.get("phase") == "measured" and b.get("state") == "SUCCESS"]
    lat = [b["finish"] - b["start"] for b in measured if b.get("start")]
    resp = [b["finish"] - b["submit"] for b in measured]
    window = (s["measure_end"] or 0) - (s["measure_start"] or 0)
    thr = s["measured"] / window * 3600 if window > 0 else None
    out.update({
        "capacity": s["capacity"], "completed": s["completed"], "measured": s["measured"],
        "errors": s["errors"], "bad_briefs": s["bad_briefs"],
        "throughput_per_h": thr, "latency_p50": pct(lat, 0.5), "latency_p95": pct(lat, 0.95),
        "latency_mean": statistics.mean(lat) if lat else None,
        "response_p50": pct(resp, 0.5),
        "queue_max": max((q["llen"] for q in s.get("queue_samples") or []), default=None),
    })
    l_obs = time_avg_in_flight(briefs, s["measure_start"], s["measure_end"])
    l_little = thr / 3600 * out["latency_mean"] if thr and out["latency_mean"] else None
    out["in_flight_obs"] = l_obs
    out["in_flight_little"] = l_little
    out["little_gap"] = (abs(l_little - s["capacity"]) / s["capacity"]
                         if l_little is not None else None)

    # CPU and memory from the cgroup snapshots
    before = parse_cgroup((d / "cgroup-before.txt").read_text()) if (d / "cgroup-before.txt").exists() else {}
    after = parse_cgroup((d / "cgroup-after.txt").read_text()) if (d / "cgroup-after.txt").exists() else {}
    cpu = {}
    thr_periods = thr_thr = 0
    peaks = []
    missing = []
    for pod, a in after.items():
        r = role(pod)
        b = before.get(pod)
        if b is None or "cpu_s" not in a or "cpu_s" not in b or a["cpu_s"] < b["cpu_s"]:
            missing.append(pod)
            continue
        cpu[r] = cpu.get(r, 0.0) + a["cpu_s"] - b["cpu_s"]
        if r == "worker":
            thr_periods += a.get("nr_periods", 0) - b.get("nr_periods", 0)
            thr_thr += a.get("nr_throttled", 0) - b.get("nr_throttled", 0)
            if a.get("mem_peak"):
                peaks.append(a["mem_peak"])
    if missing:
        out["reasons_cgroup"] = f"no before/after pair for {', '.join(sorted(missing))}"
    n_ok = s["completed"] - s["errors"]
    out["cpu_s_per_brief"] = {r: v / n_ok for r, v in cpu.items()} if n_ok else {}
    w = out["cpu_s_per_brief"].get("worker")
    out["worker_cpu_over_wall"] = (w / out["latency_p50"]) if w and out["latency_p50"] else None
    out["throttled_frac"] = thr_thr / thr_periods if thr_periods else None
    out["mem_peak_per_process_mib"] = (max(peaks) / out["concurrency"] / 2**20) if peaks else None

    # validity
    st = s["stub_after"]
    hosted_ok = st["requests"] == s["stub_requests_expected"] and st["errors"] == 0
    out["stub"] = {"requests": st["requests"], "expected": s["stub_requests_expected"],
                   "unmatched": st["unmatched"], "errors": st["errors"],
                   "max_in_flight": st["max_in_flight"],
                   "stock_block_empty": st["stock_block_empty"],
                   "stock_block_unknown": st["stock_block_unknown"]}
    if not hosted_ok:
        out["reasons"].append(f"stub requests {st['requests']} != expected "
                              f"{s['stub_requests_expected']} (or stub errors {st['errors']}): "
                              "a call went elsewhere or failed")
    if st["stock_block_empty"]:
        out["reasons"].append(f"stock block empty on {st['stock_block_empty']} brief(s)")
    if s["completed"] and (s["errors"] + s["bad_briefs"]) / s["completed"] >= ERROR_MAX:
        out["reasons"].append(f"errors {s['errors']} + bad briefs {s['bad_briefs']} "
                              f"of {s['completed']} (limit under 1%)")
    if s["measured"] != s["briefs"]:
        out["reasons"].append(f"measured {s['measured']} of {s['briefs']}")
    if missing and any(role(p) == "worker" for p in missing):
        out["reasons"].append("worker CPU not measurable: " + out["reasons_cgroup"])
    pb = restarts(json.loads((d / "pods-before.json").read_text())) if (d / "pods-before.json").exists() else {}
    pa = restarts(json.loads((d / "pods-after.json").read_text())) if (d / "pods-after.json").exists() else {}
    bumped = [f"{p} ({pa[p][1]})" for p in pa if p in pb and pa[p][0] > pb[p][0]]
    if bumped:
        out["reasons"].append("container restarts during the cell: " + ", ".join(bumped))
    ev = d / "events.json"
    if ev.exists():
        bad = []
        for e in json.loads(ev.read_text()).get("items", []):
            ts = e.get("lastTimestamp") or e.get("eventTime") or ""
            if e.get("reason") in ("Evicted", "OOMKilling", "EvictionThresholdMet",
                                   "SystemOOM", "NodeHasInsufficientMemory"):
                bad.append(f"{e['reason']} {e.get('involvedObject', {}).get('name')} {ts}")
        if bad:
            out["reasons"].append("node pressure events: " + "; ".join(bad[:5]))
    out["valid"] = not out["reasons"]
    return out


# ── cells and reading rules ─────────────────────────────────────────────────

def _mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def cells(repeats: list) -> dict:
    out = {}
    for r in repeats:
        out.setdefault(r.get("cell", r["dir"]), []).append(r)
    agg = {}
    for name, rs in out.items():
        ok = [r for r in rs if r["valid"]]
        first = rs[0]
        agg[name] = {
            "cell": name, "profile": first.get("profile"), "keda": first.get("keda"),
            "replicas": first.get("replicas"), "concurrency": first.get("concurrency"),
            "capacity": first.get("capacity"), "repeats": len(rs), "valid_repeats": len(ok),
            "throughput_per_h": _mean([r["throughput_per_h"] for r in ok]),
            "throughput_each": [r.get("throughput_per_h") for r in ok],
            "latency_p50": _mean([r["latency_p50"] for r in ok]),
            "latency_p95": _mean([r["latency_p95"] for r in ok]),
            "worker_cpu_s_per_brief": _mean([r["cpu_s_per_brief"].get("worker") for r in ok]),
            "api_cpu_s_per_brief": _mean([r["cpu_s_per_brief"].get("api") for r in ok]),
            "redis_cpu_s_per_brief": _mean([r["cpu_s_per_brief"].get("redis") for r in ok]),
            "worker_cpu_over_wall": _mean([r["worker_cpu_over_wall"] for r in ok]),
            "throttled_frac": _mean([r["throttled_frac"] for r in ok]),
            "mem_peak_per_process_mib": max((r["mem_peak_per_process_mib"] for r in ok
                                             if r.get("mem_peak_per_process_mib")), default=None),
            "little_gap": _mean([r["little_gap"] for r in ok]),
        }
    return agg


def reading_rules(agg: dict) -> dict:
    by = {(c["profile"], c["replicas"], c["concurrency"]): c
          for c in agg.values() if not c["keda"] and c["valid_repeats"]}
    rules = {}
    base = by.get(("L0", 1, 1))
    rules["Q1_overhead"] = ({"latency_p50_s": base["latency_p50"],
                             "worker_cpu_s_per_brief": base["worker_cpu_s_per_brief"]}
                            if base else "not measured: L0 (1,1) has no valid repeat")
    q2 = {}
    for (p, r, c), cell in sorted(by.items()):
        if p != "L1" or cell["worker_cpu_over_wall"] is None:
            continue
        x = cell["worker_cpu_over_wall"]
        q2[f"({r},{c})"] = {"cpu_over_wall": x, "reading": (
            "waiting (supports the post)" if x < WAIT_MAX else
            "CPU-bound" if x > CPU_BOUND_MIN else "mixed")}
    rules["Q2_wait_vs_work"] = q2 or "not measured: no valid L1 cell"
    q3 = {}
    for prof in ("L0", "L1"):
        rows = {}
        for (p, r, c), cell in by.items():
            if p != prof or not cell["throughput_per_h"]:
                continue
            gains = {}
            for label, nxt in (("2x replicas", (p, r * 2, c)), ("2x concurrency", (p, r, c * 2))):
                if nxt in by and by[nxt]["throughput_per_h"]:
                    gains[label] = by[nxt]["throughput_per_h"] / cell["throughput_per_h"] - 1
            rows[(r, c)] = gains
        sat = [rc for rc, g in rows.items() if g and all(v < SATURATION_GAIN for v in g.values())]
        sat.sort(key=lambda rc: (rc[0] * rc[1], rc))
        # every saturated cell at the smallest saturated capacity (R x c);
        # more than one means replicas and concurrency saturate alike there
        lowest = [rc for rc in sat if sat and rc[0] * rc[1] == sat[0][0] * sat[0][1]]
        q3[prof] = {"doubling_gains": {f"({r},{c})": g for (r, c), g in sorted(rows.items())},
                    "saturation_at": [f"({r},{c})" for r, c in lowest] if lowest else
                    "not reached within the sweep"}
    rules["Q3_saturation"] = q3
    q4 = {}
    for (p, r, c), cell in sorted(by.items()):
        if p != "L1" or not cell["worker_cpu_s_per_brief"] or not cell["throughput_per_h"]:
            continue
        q4[f"({r},{c})"] = {
            "briefs_per_h": cell["throughput_per_h"],
            "worker_vcpu": cell["worker_cpu_s_per_brief"] * cell["throughput_per_h"] / 3600,
            "worker_cpu_s_per_brief": cell["worker_cpu_s_per_brief"],
            "mem_peak_per_in_flight_brief_mib": cell["mem_peak_per_process_mib"]}
    rules["Q4_sizing"] = q4 or "not measured: no valid L1 cell"
    return rules


def fmt(x, nd=1):
    return "—" if x is None else f"{x:.{nd}f}"


def render(repeats: list, agg: dict, rules: dict) -> str:
    L = ["# Harness benchmark report", "",
         "Dated measurement on the provided OKE cluster (E5.Flex nodes); model replaced",
         "by scripts/model_stub.py. Every figure from the captures in this directory.", "",
         "## Validity per cell repeat", "",
         "| repeat | valid | stub req / expected | unmatched | stock empty | errors | reasons |",
         "|---|---|---|---|---|---|---|"]
    for r in sorted(repeats, key=lambda r: r["dir"]):
        st = r.get("stub") or {}
        L.append(f"| {r['dir']} | {'yes' if r['valid'] else 'NO'} | "
                 f"{st.get('requests', '—')} / {st.get('expected', '—')} | {st.get('unmatched', '—')} | "
                 f"{st.get('stock_block_empty', '—')} | {r.get('errors', '—')} | "
                 f"{'; '.join(r['reasons']) or ''} |")
    L += ["", "## Cells (mean of valid repeats)", "",
          "| cell | R | c | valid | briefs/h | p50 s | p95 s | worker CPU-s/brief | CPU/wall | "
          "throttled | peak MiB/process | api CPU-s/brief | Little gap |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in sorted(agg.values(), key=lambda c: (c["profile"] or "", c["keda"] or False,
                                                  c["replicas"] or 0, c["concurrency"] or 0)):
        L.append(f"| {c['cell']} | {c['replicas'] if not c['keda'] else '1–4 (KEDA)'} | "
                 f"{c['concurrency']} | {c['valid_repeats']}/{c['repeats']} | "
                 f"{fmt(c['throughput_per_h'])} | {fmt(c['latency_p50'])} | {fmt(c['latency_p95'])} | "
                 f"{fmt(c['worker_cpu_s_per_brief'], 2)} | {fmt(c['worker_cpu_over_wall'], 2)} | "
                 f"{fmt(c['throttled_frac'], 2)} | {fmt(c['mem_peak_per_process_mib'], 0)} | "
                 f"{fmt(c['api_cpu_s_per_brief'], 2)} | "
                 f"{fmt(c['little_gap'] * 100 if c['little_gap'] is not None else None, 0)}% |")
    L += ["", "## Reading rules (pre-registered)", "", "```",
          json.dumps(rules, indent=1, default=str), "```", ""]
    gaps = [c["cell"] for c in agg.values() if c["little_gap"] and c["little_gap"] > LITTLE_GAP]
    if gaps:
        L.append(f"Little's-law gap above 10% (queueing inside the harness): {', '.join(gaps)}")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        return 2
    root = Path(argv[0])
    repeats = [analyze_repeat(d) for d in sorted(root.iterdir())
               if d.is_dir() and (d / "cell.log").exists()]
    agg = cells(repeats)
    rules = reading_rules(agg)
    (root / "results.json").write_text(json.dumps(
        {"repeats": repeats, "cells": agg, "reading_rules": rules}, indent=1, default=str) + "\n")
    print(render(repeats, agg, rules))
    return 0


if __name__ == "__main__":
    sys.exit(main())
