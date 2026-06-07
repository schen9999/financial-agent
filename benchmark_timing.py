#!/usr/bin/env python3
"""
benchmark_timing.py

Measures end-to-end brief generation latency after RAG wiring.

Two passes per ticker:
  cold — first run; Pinecone namespace may be built on this pass
  warm — second run; Pinecone namespace exists, Redis cache cleared again

All research:* Redis keys are wiped before every timed run so
run_research never measures a cache hit as a real run.
"""
import sys
import os
import io
import re
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("Loading modules (HuggingFace weights load on first import)...", flush=True)
t0 = time.perf_counter()
from cache import redis_client          # noqa: E402
from agent.core import run_research     # noqa: E402
print(f"Modules ready in {time.perf_counter() - t0:.1f}s\n", flush=True)


TICKERS = ["AAPL", "MSFT", "NVDA", "JPM", "XOM"]

# Timing keys emitted by run_research / helpers, in display order
STAGES = [
    "cache_check",
    "stock_data",
    "news+SEC(parallel)",
    "rag_sections",
    "haiku_sections(parallel)",
    "sonnet_invoke",
    "total",
]


# -- Cache helpers -------------------------------------------------------------

def clear_all_research_cache() -> int:
    """Delete every research:* key. Returns count deleted."""
    deleted = 0
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="research:*", count=100)
        if keys:
            redis_client.delete(*keys)
            deleted += len(keys)
        if cursor == 0:
            break
    return deleted


# -- Output capture ------------------------------------------------------------

class _Tee:
    """Write to both a StringIO buffer and the real stdout simultaneously."""
    def __init__(self, buf: io.StringIO, real):
        self._buf = buf
        self._real = real

    def write(self, s: str):
        self._buf.write(s)
        self._real.write(s)

    def flush(self):
        self._buf.flush()
        self._real.flush()


def _parse_timings(text: str) -> dict[str, float]:
    """Extract [timing:TICKER] key=Xs lines into {key: seconds}."""
    return {
        m.group(1): float(m.group(2))
        for m in re.finditer(r'\[timing:\w+\] ([^=\n]+)=(\d+\.\d+)s', text)
    }


# -- Single timed run ----------------------------------------------------------

def run_timed(ticker: str, label: str) -> dict[str, float]:
    """Clear all research cache, run run_research, return parsed timings + wall time."""
    SEP = "-" * 64
    print(f"\n{SEP}", flush=True)
    print(f"  {ticker}  [{label}]", flush=True)
    print(SEP, flush=True)

    n = clear_all_research_cache()
    print(f"  [cache] Cleared {n} research:* key(s)", flush=True)

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = _Tee(buf, old_stdout)

    try:
        wall_start = time.perf_counter()
        run_research(ticker)
        wall_elapsed = time.perf_counter() - wall_start
    finally:
        sys.stdout = old_stdout

    timings = _parse_timings(buf.getvalue())
    timings["_wall"] = round(wall_elapsed, 2)
    return timings


# -- Benchmark loop ------------------------------------------------------------

results: dict[str, dict[str, dict]] = {"cold": {}, "warm": {}}

for ticker in TICKERS:
    results["cold"][ticker] = run_timed(ticker, "cold")
    results["warm"][ticker] = run_timed(ticker, "warm")

# -- Cache hit latency ---------------------------------------------------------
print(f"\n{'=' * 64}", flush=True)
print("  CACHE HIT LATENCY  (AAPL)", flush=True)
print(f"{'=' * 64}", flush=True)

# Populate cache with a fresh AAPL brief, then immediately hit it.
clear_all_research_cache()
print("  [1/2] Populating cache (run_research, no cache)...", flush=True)
run_research("AAPL")          # fills Redis; output already printed above

print("  [2/2] Timing cache hit...", flush=True)
buf = io.StringIO()
old_stdout = sys.stdout
sys.stdout = _Tee(buf, old_stdout)
try:
    t_hit = time.perf_counter()
    run_research("AAPL")
    cache_hit_latency = time.perf_counter() - t_hit
finally:
    sys.stdout = old_stdout

print(f"\n  Cache hit latency: {cache_hit_latency:.3f}s", flush=True)

# Cleanup — don't leave benchmark artifacts in the live cache
n = clear_all_research_cache()
print(f"\n  [cache] Final cleanup: cleared {n} key(s)", flush=True)


# -- Summary table -------------------------------------------------------------

W = 34  # column width for stage name

def _stats(vals: list[float]) -> tuple[float, float, float]:
    return sum(vals) / len(vals), min(vals), max(vals)

print("\n\n" + "=" * 74)
print("  BENCHMARK SUMMARY")
print("=" * 74)

for pass_name in ("cold", "warm"):
    d = results[pass_name]
    print(f"\n  -- {pass_name.upper()} PASS  (n={len(TICKERS)} tickers) --------------------------")
    print(f"  {'Stage':{W}}  {'Mean':>8}  {'Min':>8}  {'Max':>8}")
    print(f"  {'-'*W}  {'-'*8}  {'-'*8}  {'-'*8}")

    for key in STAGES:
        vals = [d[t][key] for t in TICKERS if d[t].get(key) is not None]
        if not vals:
            continue
        mean, lo, hi = _stats(vals)
        print(f"  {key:{W}}  {mean:>7.2f}s  {lo:>7.2f}s  {hi:>7.2f}s")

    # Derived: haiku-only = haiku_sections(parallel) − rag_sections
    haiku_only = [
        d[t]["haiku_sections(parallel)"] - d[t]["rag_sections"]
        for t in TICKERS
        if d[t].get("haiku_sections(parallel)") is not None
        and d[t].get("rag_sections") is not None
    ]
    if haiku_only:
        mean, lo, hi = _stats(haiku_only)
        label = "  > haiku-only (haiku - rag)"
        print(f"  {label:{W}}  {mean:>7.2f}s  {lo:>7.2f}s  {hi:>7.2f}s")

    # Wall clock
    walls = [d[t]["_wall"] for t in TICKERS]
    mean, lo, hi = _stats(walls)
    print(f"  {'wall_total':{W}}  {mean:>7.2f}s  {lo:>7.2f}s  {hi:>7.2f}s")

print(f"\n  -- PER-TICKER TOTALS ----------------------------------------------")
hdr = f"  {'Ticker':<8}  {'Cold total':>12}  {'Cold wall':>10}  {'Warm total':>12}  {'Warm wall':>10}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for ticker in TICKERS:
    c, w = results["cold"][ticker], results["warm"][ticker]
    ct = c.get("total", c["_wall"])
    wt = w.get("total", w["_wall"])
    print(f"  {ticker:<8}  {ct:>11.2f}s  {c['_wall']:>9.2f}s  {wt:>11.2f}s  {w['_wall']:>9.2f}s")

print()
