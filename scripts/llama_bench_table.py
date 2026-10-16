#!/usr/bin/env python3
"""Markdown table from committed llama-bench JSON files (`llama-bench -o json`),
so the cross-shape table in docs is produced from files, not copied by hand.

Each argument is a result file, optionally `path=Label`. One row per file:
device (cpu_info, or gpu_info when layers are on a GPU), backends, threads,
GPU layers, then mean tok/s (± stddev over the repetitions) for each test in
the file: prompt processing at each n_prompt, generation at each n_gen.
A test whose repetitions spread by more than --cold-pct of the mean (a cold
first repetition) prints with a dagger and is not to be quoted.

  python scripts/llama_bench_table.py \\
    eval/runs/llama-bench-cpu-2026-10-08/P4.json="AMD EPYC 9J14, OKE E5" ...
"""
import argparse
import json
import sys


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def test_name(r: dict) -> str:
    return f"pp{r['n_prompt']}" if r["n_gen"] == 0 else f"tg{r['n_gen']}"


def cell(r: dict, cold_pct: float) -> str:
    mean, sd = r["avg_ts"], r["stddev_ts"]
    spread = (max(r["samples_ts"]) - min(r["samples_ts"])) / mean * 100 if mean else 0.0
    return f"{mean:.1f} (±{sd:.2f}){' †' if spread > cold_pct else ''}"


def device(r: dict) -> str:
    on_gpu = r.get("gpu_info") and r.get("n_gpu_layers", 0) != 0 and "CUDA" in r.get("backends", "")
    return r["gpu_info"] if on_gpu else r["cpu_info"]


def rows(specs: list[tuple[str, str]], cold_pct: float):
    tests: list[str] = []
    out = []
    for path, label in specs:
        recs = load(path)
        by = {test_name(r): r for r in recs}
        for t in by:
            if t not in tests:
                tests.append(t)
        r0 = recs[0]
        out.append((label or path, device(r0), r0["backends"], r0["n_threads"], r0["n_gpu_layers"],
                    r0["build_number"], {t: cell(r, cold_pct) for t, r in by.items()}))
    return tests, out


def markdown(tests, out) -> str:
    head = ["Where", "Device", "Backend", "Threads", "GPU layers"] + [f"{t} tok/s" for t in tests]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    builds = set()
    for label, dev, be, thr, ngl, build, cells in out:
        builds.add(build)
        lines.append("| " + " | ".join([label, dev, be, str(thr), str(ngl)] + [cells.get(t, "—") for t in tests]) + " |")
    lines.append("")
    lines.append(f"llama.cpp build(s): {', '.join('b%s' % b for b in sorted(builds))}. "
                 "† repetitions spread wider than the cold threshold: not quoted.")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+", help="path[=Label]")
    ap.add_argument("--cold-pct", type=float, default=10.0,
                    help="flag a test whose samples spread more than this %% of the mean")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    specs = [tuple(s.split("=", 1)) if "=" in s else (s, "") for s in args.files]
    print(markdown(*rows(specs, args.cold_pct)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
