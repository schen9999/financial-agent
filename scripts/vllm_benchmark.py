#!/usr/bin/env python3
"""vllm_benchmark.py — throughput/latency benchmark for the vLLM endpoint.

Sends section-generation-shaped prompts (the workload the fine-tune serves) to
an OpenAI-compatible /v1/chat/completions endpoint at fixed concurrency levels
and reports per-request latency (p50/p95), completion tokens/sec per request,
and aggregate throughput. Token counts come from the server's reported usage.

CONTEXT: on this machine vLLM runs CPU-MODE inside WSL2 (no GPU). The numbers
measure that environment only — they are NOT comparable to GPU serving or to
the hosted Anthropic API (see benchmarks.md).

Usage:
  python scripts/vllm_benchmark.py --url http://localhost:18000 \
      --model financial-lora --concurrency 1 4 8 --requests-per-level 16
"""
import argparse
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# Two real section prompts (the trained sections) with representative data
# context, alternated across requests. Shape matches agent/core._haiku_section.
PROMPTS = [
    (
        "Write ONLY the '### Financial Health' section for a Example Corp (EXMP) "
        "investment brief.\nKey metrics: price, market cap, P/E ratio, revenue, "
        "profit margin. Brief financial assessment. 3-5 sentences.\nStart with the "
        "markdown heading. Be concise.\n\nData:\n"
        'Stock: {"ticker": "EXMP", "company_name": "Example Corp", "current_price": '
        '184.32, "market_cap": 2870000000000, "pe_ratio": 31.2, "forward_pe": 27.9, '
        '"revenue": 394328000000, "net_income": 96995000000, "profit_margin": 0.246, '
        '"week_52_high": 199.62, "week_52_low": 143.90, "sector": "Technology"}'
    ),
    (
        "Write ONLY the '### Risk Factors' section for a Example Corp (EXMP) "
        "investment brief.\n2-3 primary risks an investor should be aware of, as a "
        "bullet list.\nStart with the markdown heading. Be concise.\n\nData:\n"
        "The company faces intense competition in all markets. Supply chain "
        "concentration in Asia exposes operations to geopolitical disruption. "
        "Regulatory scrutiny of digital-platform businesses continues to increase "
        "across the US and EU, and litigation outcomes are uncertain."
    ),
]


def one_request(url: str, model: str, prompt: str, max_tokens: int) -> dict:
    t0 = time.perf_counter()
    resp = requests.post(
        f"{url}/v1/chat/completions",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": max_tokens,
        },
        timeout=600,
    )
    elapsed = time.perf_counter() - t0
    resp.raise_for_status()
    body = resp.json()
    usage = body.get("usage", {})
    completion_tokens = usage.get("completion_tokens", 0)
    return {
        "latency_s": elapsed,
        "completion_tokens": completion_tokens,
        "tokens_per_s": completion_tokens / elapsed if elapsed > 0 else 0.0,
    }


def run_level(url: str, model: str, concurrency: int, n_requests: int, max_tokens: int) -> dict:
    prompts = [PROMPTS[i % len(PROMPTS)] for i in range(n_requests)]
    t0 = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(one_request, url, model, p, max_tokens) for p in prompts]
        for f in as_completed(futures):
            results.append(f.result())
    wall = time.perf_counter() - t0

    latencies = sorted(r["latency_s"] for r in results)
    total_tokens = sum(r["completion_tokens"] for r in results)

    def pct(p):
        idx = min(len(latencies) - 1, max(0, round(p / 100 * (len(latencies) + 1)) - 1))
        return latencies[idx]

    return {
        "concurrency": concurrency,
        "requests": n_requests,
        "p50_s": round(statistics.median(latencies), 2),
        "p95_s": round(pct(95), 2),
        "mean_s": round(statistics.mean(latencies), 2),
        "mean_tokens_per_req": round(total_tokens / n_requests, 1),
        "per_request_tokens_per_s": round(
            statistics.mean(r["tokens_per_s"] for r in results), 2
        ),
        "aggregate_tokens_per_s": round(total_tokens / wall, 2),
        "wall_s": round(wall, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark an OpenAI-compatible endpoint.")
    parser.add_argument("--url", default="http://localhost:18000")
    parser.add_argument("--model", default="financial-lora")
    parser.add_argument("--concurrency", nargs="+", type=int, default=[1, 4, 8])
    parser.add_argument("--requests-per-level", type=int, default=16)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()

    # Warmup (excluded from measurements): first CPU inference includes graph/
    # cache warmup that would skew the level run.
    print(f"warmup request -> {args.url} ...", flush=True)
    one_request(args.url, args.model, PROMPTS[0], args.max_tokens)

    levels = []
    for c in args.concurrency:
        print(f"concurrency={c}: {args.requests_per_level} requests ...", flush=True)
        lv = run_level(args.url, args.model, c, args.requests_per_level, args.max_tokens)
        levels.append(lv)
        print(
            f"  p50={lv['p50_s']}s p95={lv['p95_s']}s "
            f"per-req={lv['per_request_tokens_per_s']} tok/s "
            f"aggregate={lv['aggregate_tokens_per_s']} tok/s",
            flush=True,
        )

    print("\n| Concurrency | Requests | p50 (s) | p95 (s) | tok/s per request | aggregate tok/s |")
    print("|---:|---:|---:|---:|---:|---:|")
    for lv in levels:
        print(
            f"| {lv['concurrency']} | {lv['requests']} | {lv['p50_s']} | {lv['p95_s']} "
            f"| {lv['per_request_tokens_per_s']} | {lv['aggregate_tokens_per_s']} |"
        )

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"url": args.url, "model": args.model, "levels": levels}, f, indent=2)
        print(f"\nJSON written to {args.json_out}")


if __name__ == "__main__":
    main()
