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

A directory argument stands for every *.json in it, labeled by file name.

--matrix prints one row per engine x precision x device instead: output
tok/s at concurrency 8, mean E2E, TTFT p50 at concurrency 1, and the
weights' size on disk. Each group needs exactly one concurrency-8 and one
concurrency-1 file. Precision is the run's quantization (W4A16 on vLLM, the
GGUF type on llama.cpp), else its dtype. Size comes from the run's
weights_bytes metadata (recorded since quant-bench, 2026-09-28);
--weights-bytes PATH=BYTES supplies it for older files under PATH.

--sweep prints the sweep files (scripts/vm_bench_cpu.sh and
vm_bench_cpu_gguf.sh `sweep`) as one concurrency x threads table per
engine x precision x device: output tok/s / TTFT p50 ms / TPOT p50 ms.

Usage:
  python scripts/bench_table.py \\
      eval/runs/bench/financial-lora.json=A10 \\
      eval/runs/bench/cpu-2026-09-28/financial-lora-c8.json=CPU \\
      --section-tokens 530 --section-tokens 1024
  python scripts/bench_table.py --matrix eval/runs/bench/a10-quant-2026-09-28 ...
  python scripts/bench_table.py --sweep eval/runs/bench/cpu-sweep-2026-09-28
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


def is_result(path):
    """A `vllm bench serve` result, not a sidecar such as quant_meta.json."""
    return "num_prompts" in json.loads(path.read_text(encoding="utf-8"))


def expand(specs):
    """A directory spec becomes one spec per result *.json in it, in name order."""
    out = []
    for spec in specs:
        path, _, _ = spec.partition("=")
        p = Path(path)
        out += [str(f) for f in sorted(p.glob("*.json")) if is_result(f)] if p.is_dir() else [spec]
    return out


def load(spec):
    path, _, label = spec.partition("=")
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    data["_path"] = path
    return (label or Path(path).stem), data


def precision(d):
    """The quantization the run served (w4a16-g128, Q4_K_M, ...), else its dtype."""
    q = d.get("quantization", "none")
    return d.get("dtype", "?") if q in ("none", d.get("dtype")) else q


def hardware(d):
    """Device, backend, dtype, cores from the run's metadata."""
    if "device" not in d:
        return "A10 (pre-metadata)", "vllm 0.10.2", "bfloat16", "n/a"
    backend = f"{d.get('backend', '?')} {d.get('backend_version', '?')}"
    dtype = d.get("dtype", "?")
    if precision(d) != dtype:
        dtype = f"{precision(d)} ({dtype})"
    if d["device"] == "cpu":
        return d.get("cpu_model", "cpu"), backend, dtype, str(d.get("pinned_cores", "?"))
    return d.get("gpu_model", d["device"]), backend, dtype, "n/a"


def prompts(label, d):
    """Prompt count, refusing an incomplete run unless its only losses are the
    transport losses scripts/bench_fix_llamacpp.py recorded (never served)."""
    done, n = d.get("completed"), d.get("num_prompts")
    lost = len(d.get("lost_requests", []))
    if done + lost != n:
        raise ValueError(f"{label}: completed {done} of {n} prompts")
    return f"{done} of {n}" if lost else str(n)


def row(label, d):
    device, backend, dtype, cores = hardware(d)
    cells = [label, device, backend, dtype, cores,
             str(d["max_concurrency"]), prompts(label, d)]
    for _, key, fmt in COLUMNS:
        keys = key if isinstance(key, tuple) else (key,)
        cells.append(" / ".join(fmt.format(d[k]) for k in keys))
    cells.append(prefix_cache(d))
    return "| " + " | ".join(cells) + " |"


def prefix_cache(d):
    """Share of the timed run's prompt tokens served from the prefix cache."""
    if "llamacpp_prompt_tokens_processed" in d:
        return "n/a (llama.cpp)"
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


def group_key(d):
    """(engine, precision, device) of a run."""
    device, backend, _, _ = hardware(d)
    return backend, precision(d), device


def grouped(specs):
    groups = {}
    for label, d in map(load, expand(specs)):
        prompts(label, d)
        groups.setdefault(group_key(d), []).append((label, d))
    return groups


def weights_bytes(d, overrides):
    if "weights_bytes" in d:
        return int(d["weights_bytes"])
    path = Path(d["_path"]).resolve()
    for prefix, n in overrides.items():
        if path.is_relative_to(Path(prefix).resolve()):
            return n
    return None


def matrix(specs, overrides=None):
    """Engine x precision x device: c=8 throughput, c=1 latency, weights size."""
    overrides = overrides or {}
    head = ["Engine", "Precision", "Device", "Output tok/s (c=8)", "Mean E2E s (c=1)",
            "TTFT p50 ms (c=1)", "Weights on disk (GB)"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for (engine, prec, device), runs in grouped(specs).items():
        by_conc = {}
        for label, d in runs:
            if d["max_concurrency"] in by_conc:
                raise ValueError(f"{engine} {prec} {device}: two concurrency-"
                                 f"{d['max_concurrency']} files")
            by_conc[d["max_concurrency"]] = d
        if set(by_conc) != {1, 8}:
            raise ValueError(f"{engine} {prec} {device}: needs one concurrency-8 and one "
                             f"concurrency-1 file, got {sorted(by_conc)}")
        sizes = {weights_bytes(d, overrides) for d in by_conc.values()} - {None}
        if len(sizes) > 1:
            raise ValueError(f"{engine} {prec} {device}: weights sizes differ {sorted(sizes)}")
        size = f"{sizes.pop() / 1e9:.2f}" if sizes else "not recorded"
        c8, c1 = by_conc[8], by_conc[1]
        lines.append("| " + " | ".join([
            engine, prec, device, f"{c8['output_throughput']:.1f}",
            f"{c1['mean_e2el_ms'] / 1000:.1f}", f"{c1['median_ttft_ms']:.0f}", size]) + " |")
    return "\n".join(lines)


def sweep(specs):
    """One concurrency x threads table per engine x precision x device."""
    blocks = []
    for (engine, prec, device), runs in grouped(specs).items():
        cells = {}
        for label, d in runs:
            key = (d["max_concurrency"], int(d["pinned_cores"]))
            if key in cells:
                raise ValueError(f"{label}: second file for concurrency {key[0]}, "
                                 f"{key[1]} threads")
            cells[key] = d
        concs = sorted({c for c, _ in cells})
        threads = sorted({t for _, t in cells})
        head = ["Concurrency"] + [f"{t} threads" for t in threads]
        lines = [f"{engine}, {prec}, {device}: output tok/s / TTFT p50 ms / TPOT p50 ms",
                 "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        for c in concs:
            row = [str(c)]
            for t in threads:
                d = cells.get((c, t))
                row.append(f"{d['output_throughput']:.1f} / {d['median_ttft_ms']:.0f} / "
                           f"{d['median_tpot_ms']:.1f}" if d else "not run")
            lines.append("| " + " | ".join(row) + " |")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def parse_weights(values):
    out = {}
    for v in values:
        path, sep, n = v.rpartition("=")
        if not sep or not n.isdigit():
            raise SystemExit(f"--weights-bytes {v!r}: expected PATH=BYTES")
        out[path] = int(n)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", help="result JSON (optionally path=Label) or a directory")
    ap.add_argument("--section-tokens", type=int, action="append", default=[],
                    help="FH + RF output tokens per brief; repeatable")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--matrix", action="store_true",
                      help="engine x precision x device table (c=8 and c=1 files per group)")
    mode.add_argument("--sweep", action="store_true",
                      help="concurrency x threads tables from sweep files")
    ap.add_argument("--weights-bytes", action="append", default=[], metavar="PATH=BYTES",
                    help="weights size for files under PATH that predate weights_bytes")
    args = ap.parse_args(argv)
    if args.matrix:
        print(matrix(args.files, parse_weights(args.weights_bytes)))
        return 0
    if args.sweep:
        print(sweep(args.files))
        return 0
    args.files = expand(args.files)
    print(table(args.files))
    if args.section_tokens:
        print("\nTwo local sections, serial: 2 x mean TTFT + T x mean TPOT (concurrency-1 files)")
        print("\n".join(section_lines(args.files, args.section_tokens)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
