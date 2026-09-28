#!/usr/bin/env python3
"""bench_table.py: markdown table from committed `vllm bench serve` result
JSONs (eval/runs/bench/), so serving figures in docs are produced from files,
not copied by hand.

Each argument is a result file, optionally `path=Label`. Device, backend,
dtype and pinned cores come from the run's --metadata (written by
scripts/vm_bench_cpu.sh and scripts/vm_bench_serve.sh). The 2026-09-23 A10
files predate --metadata; they were produced by scripts/vm_bench_serve.sh
against the k3s vLLM deployment (vllm/vllm-openai:v0.10.2, --dtype=bfloat16)
and print as "A10 (pre-metadata)".

The last column is the share of the timed run's prompt tokens served from
vLLM's prefix cache (recorded by both scripts since 2026-09-28; ~1% is the
client's initial test request re-sending the first prompt). Earlier files
print "not recorded".

--section-tokens T (repeatable) adds, for each concurrency-1 file, the
serial time to write the brief's two locally served sections (Financial
Health + Risk Factors) at T output tokens per brief:
2 x mean TTFT + T x mean TPOT. An estimate: TTFT was measured at 1024 input
tokens, and the pipeline sends the two sections in parallel, not serially.
T comes from scripts/cost_per_brief_selfhost.py (docs/model-recommendation.md).

Usage:
  python scripts/bench_table.py \\
      eval/runs/bench/financial-lora.json=A10 \\
      eval/runs/bench/cpu-2026-09-28/financial-lora-c8.json=CPU \\
      --section-tokens 530 --section-tokens 1024
"""
import argparse
import json
import sys
from pathlib import Path

COLUMNS = [
    ("Output tok/s", "output_throughput", "{:.1f}"),
    ("Total tok/s", "total_token_throughput", "{:.1f}"),
    ("Req/s", "request_throughput", "{:.3f}"),
    ("TTFT mean / median / p99 ms", ("mean_ttft_ms", "median_ttft_ms", "p99_ttft_ms"), "{:.0f}"),
    ("TPOT mean / median / p99 ms", ("mean_tpot_ms", "median_tpot_ms", "p99_tpot_ms"), "{:.1f}"),
    ("E2E mean / median / p99 ms", ("mean_e2el_ms", "median_e2el_ms", "p99_e2el_ms"), "{:.0f}"),
]


def load(spec):
    path, _, label = spec.partition("=")
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return (label or Path(path).stem), data


def hardware(d):
    """Device, backend, dtype, cores from the run's metadata."""
    if "device" not in d:
        return "A10 (pre-metadata)", "vllm 0.10.2", "bfloat16", "n/a"
    backend = f"{d.get('backend', '?')} {d.get('backend_version', '?')}"
    if d["device"] == "cpu":
        return (d.get("cpu_model", "cpu"), backend, d.get("dtype", "?"),
                str(d.get("pinned_cores", "?")))
    return d.get("gpu_model", d["device"]), backend, d.get("dtype", "?"), "n/a"


def row(label, d):
    device, backend, dtype, cores = hardware(d)
    if d.get("completed") != d.get("num_prompts"):
        raise ValueError(f"{label}: completed {d.get('completed')} of {d.get('num_prompts')} prompts")
    cells = [label, device, backend, dtype, cores,
             str(d["max_concurrency"]), str(d["num_prompts"])]
    for _, key, fmt in COLUMNS:
        keys = key if isinstance(key, tuple) else (key,)
        cells.append(" / ".join(fmt.format(d[k]) for k in keys))
    cells.append(prefix_cache(d))
    return "| " + " | ".join(cells) + " |"


def prefix_cache(d):
    """Share of the timed run's prompt tokens served from the prefix cache."""
    if "prefix_cache_query_tokens" not in d:
        return "not recorded"
    hits, queries = d["prefix_cache_hit_tokens"], d["prefix_cache_query_tokens"]
    return f"{100 * hits / queries:.1f}%" if queries else "0 queries"


def table(specs):
    head = ["Run", "Device", "Backend", "dtype", "Pinned cores", "Concurrency", "Prompts"]
    head += [name for name, _, _ in COLUMNS] + ["Prefix-cache hits"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += [row(*load(s)) for s in specs]
    return "\n".join(lines)


def section_seconds(d, tokens):
    """2 sections x mean TTFT + tokens x mean TPOT, in seconds."""
    return (2 * d["mean_ttft_ms"] + tokens * d["mean_tpot_ms"]) / 1000


def section_lines(specs, token_counts):
    lines = []
    for label, d in map(load, specs):
        if d["max_concurrency"] != 1:
            continue
        parts = [f"{section_seconds(d, t):.1f} s at T = {t}" for t in token_counts]
        lines.append(f"- {label}: " + "; ".join(parts))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", help="result JSON, optionally path=Label")
    ap.add_argument("--section-tokens", type=int, action="append", default=[],
                    help="FH + RF output tokens per brief; repeatable")
    args = ap.parse_args(argv)
    print(table(args.files))
    if args.section_tokens:
        print("\nTwo local sections, serial: 2 x mean TTFT + T x mean TPOT (concurrency-1 files)")
        print("\n".join(section_lines(args.files, args.section_tokens)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
