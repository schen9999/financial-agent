#!/usr/bin/env python3
"""cost_report.py — re-runnable cost-per-brief instrumentation.

Measures the real cost of a brief by running the production single-agent
pipeline (agent.core.run_research) with token accounting on every LLM call,
priced from scripts/model_prices.json. This replaces the historical
$0.0269/brief figure — which came from an uncommitted harness and cannot be
re-derived — as the source of any cost claim (see docs/PHASE0_AUDIT.md §4).

Two accounting layers, reported separately and honestly:

  exact      LangChain ChatAnthropic calls (4 Haiku sections + Sonnet
             synthesis): token counts come from the API's own usage metadata
             via langchain's UsageMetadataCallbackHandler — exact.
  estimated  The RAG answer-synthesis Haiku calls made inside LlamaIndex
             (2 per brief when RAG is active): LlamaIndex's
             TokenCountingHandler counts with a local tokenizer, not API
             usage — an estimate, labeled as such in the output.

BYPASS_CACHE is forced so every run measures full generation, never a cache
hit. Flags are NOT overridden — the report measures the pipeline as configured
(defaults: reranking off, multi-agent off, local model off).

Usage:
  python scripts/cost_report.py                        # default 3 tickers
  python scripts/cost_report.py --tickers AAPL NVDA JPM MSFT GOOGL
  python scripts/cost_report.py --json-out cost.json
"""
import sys
import os
import json
import time
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Force full generation BEFORE importing anything that touches the cache.
os.environ["BYPASS_CACHE"] = "true"

from dotenv import load_dotenv
load_dotenv()

from langchain_core.callbacks import UsageMetadataCallbackHandler

PRICES_PATH = Path(__file__).parent / "model_prices.json"


def load_prices() -> dict:
    return json.loads(PRICES_PATH.read_text(encoding="utf-8"))


def price_usage(model: str, usage: dict, prices: dict) -> float:
    """Price one model's usage dict from the config table. Unknown models are a
    hard error — silently pricing at $0 would fabricate a lower cost."""
    table = prices["models"]
    if model not in table:
        raise KeyError(
            f"model '{model}' not in {PRICES_PATH.name} — add its rates before pricing"
        )
    rates = table[model]
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    details = usage.get("input_token_details", {}) or {}
    cache_read = details.get("cache_read", 0)
    cache_creation = details.get("cache_creation", 0)
    # input_tokens from the API includes only uncached tokens; cache tokens are
    # reported separately in the details and priced at their multipliers.
    cost = input_tokens / 1e6 * rates["input_per_mtok"]
    cost += cache_read / 1e6 * rates["input_per_mtok"] * prices["cache_read_multiplier"]
    cost += cache_creation / 1e6 * rates["input_per_mtok"] * prices["cache_creation_multiplier"]
    cost += output_tokens / 1e6 * rates["output_per_mtok"]
    return cost


def run_one(ticker: str, prices: dict) -> dict:
    """Run the production pipeline once for a ticker with token accounting."""
    # LlamaIndex layer (estimated): tokenizer-based counting on the RAG
    # pipeline's internal LLM calls (answer synthesis over retrieved chunks).
    from llama_index.core import Settings
    from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
    token_counter = TokenCountingHandler()
    Settings.callback_manager = CallbackManager([token_counter])

    from agent.core import run_research, _haiku, _llm

    # LangChain layer (exact): attach the usage callback DIRECTLY to the two
    # chat models rather than via get_usage_metadata_callback(). The context-
    # manager version rides a ContextVar, and the 4 Haiku section calls run in
    # a ThreadPoolExecutor where that ContextVar doesn't propagate — it would
    # silently count only the main-thread Sonnet call. Direct attachment fires
    # from any thread. (Instruments the single-agent path; the flag-gated
    # multi-agent planner/judge construct their own LLMs and aren't counted.)
    usage_cb = UsageMetadataCallbackHandler()
    prev_haiku_cbs, prev_llm_cbs = _haiku.callbacks, _llm.callbacks
    _haiku.callbacks = [usage_cb]
    _llm.callbacks = [usage_cb]
    t0 = time.perf_counter()
    try:
        brief = run_research(ticker)
    finally:
        _haiku.callbacks = prev_haiku_cbs
        _llm.callbacks = prev_llm_cbs
    elapsed = time.perf_counter() - t0

    exact_by_model = {}
    exact_cost = 0.0
    for model, usage in usage_cb.usage_metadata.items():
        cost = price_usage(model, usage, prices)
        exact_by_model[model] = {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cost_usd": round(cost, 6),
        }
        exact_cost += cost

    # RAG-internal calls run on the llama_index Settings.llm (Haiku).
    rag_model = "claude-haiku-4-5-20251001"
    rag_in = token_counter.prompt_llm_token_count
    rag_out = token_counter.completion_llm_token_count
    rag_cost = price_usage(rag_model, {"input_tokens": rag_in, "output_tokens": rag_out}, prices)
    token_counter.reset_counts()

    return {
        "ticker": ticker,
        "elapsed_s": round(elapsed, 2),
        "brief_chars": len(brief),
        "exact_by_model": exact_by_model,
        "exact_cost_usd": round(exact_cost, 6),
        "rag_estimated": {
            "model": rag_model,
            "input_tokens": rag_in,
            "output_tokens": rag_out,
            "cost_usd": round(rag_cost, 6),
        },
        "total_cost_usd": round(exact_cost + rag_cost, 6),
    }


def main():
    parser = argparse.ArgumentParser(description="Re-runnable cost-per-brief report.")
    parser.add_argument("--tickers", nargs="+", default=["AAPL", "NVDA", "JPM"])
    parser.add_argument("--json-out", default=None, metavar="PATH")
    args = parser.parse_args()

    prices = load_prices()
    print(f"Cost report — pipeline as configured (BYPASS_CACHE forced).")
    print(f"Prices from {PRICES_PATH.name}: "
          + ", ".join(f"{m} ${r['input_per_mtok']}/{r['output_per_mtok']} per MTok"
                      for m, r in prices["models"].items() if not m.endswith("-20251001")))
    print()

    runs = []
    for ticker in args.tickers:
        print(f"[{ticker}] running pipeline...", flush=True)
        r = run_one(ticker, prices)
        runs.append(r)
        models = ", ".join(
            f"{m}: {u['input_tokens']}in/{u['output_tokens']}out=${u['cost_usd']:.4f}"
            for m, u in r["exact_by_model"].items()
        )
        rag = r["rag_estimated"]
        print(f"[{ticker}] {r['elapsed_s']}s  exact[{models}]  "
              f"rag-est[{rag['input_tokens']}in/{rag['output_tokens']}out=${rag['cost_usd']:.4f}]  "
              f"TOTAL ${r['total_cost_usd']:.4f}", flush=True)

    n = len(runs)
    mean_exact = sum(r["exact_cost_usd"] for r in runs) / n
    mean_rag = sum(r["rag_estimated"]["cost_usd"] for r in runs) / n
    mean_total = sum(r["total_cost_usd"] for r in runs) / n
    mean_s = sum(r["elapsed_s"] for r in runs) / n

    print(f"\n{'='*74}")
    print(f"  MEAN over {n} brief(s):")
    print(f"    exact (LangChain calls, API-reported tokens):   ${mean_exact:.4f}")
    print(f"    estimated (RAG-internal calls, tokenizer est.): ${mean_rag:.4f}")
    print(f"    TOTAL cost/brief:                               ${mean_total:.4f}")
    print(f"    mean total latency (incl. data fetch):          {mean_s:.1f}s")
    print(f"{'='*74}")

    if args.json_out:
        payload = {
            "tickers": args.tickers,
            "runs": runs,
            "mean": {
                "exact_cost_usd": round(mean_exact, 6),
                "rag_estimated_cost_usd": round(mean_rag, 6),
                "total_cost_usd": round(mean_total, 6),
                "elapsed_s": round(mean_s, 2),
            },
            "prices_file": str(PRICES_PATH.name),
        }
        Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"JSON written to {args.json_out}")


if __name__ == "__main__":
    main()
