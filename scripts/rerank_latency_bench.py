#!/usr/bin/env python3
"""Warm retrieval latency, reranking off vs on — the latency leg of the
reranking A/B (pre-registered 2026-10-08, eval-methodology).

Why separate: each eval pod is fresh, so a reranked eval pod downloads and
loads the cross-encoder inside its first timed retrieval; that one-time
cost would be charged to every ticker. Here the model is loaded once,
before any timing, as a long-lived app process would hold it.

For each ticker with an indexed 10-K namespace and each of the pipeline's
two RAG questions (agent/core.py DEFAULT_HIGHLIGHTS_QUERY and
DEFAULT_RISKS_QUERY), retrieval only — no answer synthesis, no LLM call:
  off  similarity_top_k = BASELINE_TOP_K (3), the TOC-listing filter
  on   similarity_top_k = RERANK_CANDIDATES (20), the TOC-listing filter,
       then the cross-encoder down to RERANK_TOP_N (3)
in alternating order per query (off, on, on, off ...), REPEATS times each.
Reported: median and p95 per arm over all queries, and the paired
per-query median difference.

Runs where the app's code and Pinecone access are (the app image, as a
Job: k8s/jobs/rerank-latency-bench.yaml), prints a JSON summary line
`RERANK_LATENCY {...}`.
  python scripts/rerank_latency_bench.py --tickers AAPL MSFT ... --repeats 3
"""
import argparse
import json
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tickers", nargs="+", required=True)
    ap.add_argument("--repeats", type=int, default=3)
    args = ap.parse_args(argv)

    from llama_index.core import VectorStoreIndex
    from llama_index.core.schema import QueryBundle
    from llama_index.vector_stores.pinecone import PineconeVectorStore

    from agent.core import DEFAULT_HIGHLIGHTS_QUERY, DEFAULT_RISKS_QUERY
    from agent.tools import rag
    from agent.tools.reranker import (baseline_top_k, get_reranker, rerank_candidates,
                                      rerank_model, rerank_top_n)

    rag._ensure_settings()
    t0 = time.perf_counter()
    reranker = get_reranker()
    load_s = time.perf_counter() - t0
    pine = rag._get_pinecone_index("sec-filings")
    toc = rag._DropTocListings()
    questions = [DEFAULT_HIGHLIGHTS_QUERY, DEFAULT_RISKS_QUERY]

    def retrieve(index, q, on):
        t = time.perf_counter()
        k = rerank_candidates() if on else baseline_top_k()
        nodes = index.as_retriever(similarity_top_k=k).retrieve(q)
        bundle = QueryBundle(q)
        nodes = toc.postprocess_nodes(nodes, query_bundle=bundle)
        if on:
            nodes = reranker.postprocess_nodes(nodes, query_bundle=bundle)
        return time.perf_counter() - t, len(nodes)

    rows, skipped = [], []
    for ticker in args.tickers:
        index = VectorStoreIndex.from_vector_store(
            vector_store=PineconeVectorStore(pinecone_index=pine, namespace=ticker.lower()))
        for q in questions:
            off_t, on_t = [], []
            try:
                for r in range(args.repeats):
                    order = (False, True) if r % 2 == 0 else (True, False)
                    for on in order:
                        dt, n = retrieve(index, q, on)
                        if n == 0:
                            raise RuntimeError("no nodes")
                        (on_t if on else off_t).append(dt)
            except Exception as e:  # noqa: BLE001 - a ticker without an index is skipped, recorded
                skipped.append(f"{ticker}: {type(e).__name__}: {e}"[:160])
                break
            rows.append({"ticker": ticker, "question": q[:20], "off_s": statistics.median(off_t),
                         "on_s": statistics.median(on_t)})
            print(f"{ticker:6} {q[:24]:24} off {rows[-1]['off_s']:.3f}s  on {rows[-1]['on_s']:.3f}s", flush=True)

    off = [r["off_s"] for r in rows]
    on = [r["on_s"] for r in rows]
    diff = sorted(r["on_s"] - r["off_s"] for r in rows)

    def pct(v, q):
        v = sorted(v)
        return v[min(len(v) - 1, int(q * len(v)))] if v else None

    summary = {
        "queries": len(rows), "repeats": args.repeats, "reranker": rerank_model(),
        "reranker_load_s": round(load_s, 2), "candidates": rerank_candidates(), "top_n": rerank_top_n(),
        "baseline_top_k": baseline_top_k(),
        "off_median_s": statistics.median(off) if off else None, "off_p95_s": pct(off, 0.95),
        "on_median_s": statistics.median(on) if on else None, "on_p95_s": pct(on, 0.95),
        "paired_median_diff_s": statistics.median(diff) if diff else None,
        "per_ticker_added_s_median": 2 * statistics.median(diff) if diff else None,
        "skipped": skipped, "rows": rows,
    }
    print("RERANK_LATENCY " + json.dumps(summary), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
