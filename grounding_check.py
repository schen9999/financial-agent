#!/usr/bin/env python3
"""
grounding_check.py — LLM-as-judge grounding eval with reranking A/B arms.

Runs the constrained Sonnet synthesis pipeline from core.py across a set of
tickers under up to three retrieval arms and audits grounding with a Sonnet
judge (temperature=0). The headline comparison holds the final chunk count
constant (baseline top_k=3  vs.  retrieve-20 -> rerank -> top-3); the optional
top-5 arm only measures the effect of added context.

  ARMS
    baseline   RERANKING_ENABLED=false, top_k=3            (today's behaviour)
    rerank3    retrieve 20 -> cross-encoder rerank -> 3    (headline vs baseline)
    rerank5    retrieve 20 -> cross-encoder rerank -> 5    (added-context arm)

For each (ticker, arm) it records:
  - grounding: SUPPORTED / UNSUPPORTED / INFERENCE counts over the Exec Summary
    and Outlook (every quantitative / forward-looking claim)
  - retrieval latency: wall time of the two SEC RAG queries
  - pipeline latency: retrieval + Haiku sections + Sonnet synthesis
    (shared data-fetch is excluded — it is network-bound and identical per arm)

The Redis exact-key cache is bypassed (BYPASS_CACHE=true) so no arm can return
another arm's cached brief; base stock/news/SEC data is fetched once per ticker
and reused across arms so only the retrieval stage varies.

This is a dev harness — it does not change core.py defaults. Reranking stays
off in production unless RERANKING_ENABLED=true.

Usage:
  python grounding_check.py                       # all 10 tickers, all 3 arms
  python grounding_check.py --arms baseline rerank3
  python grounding_check.py --tickers AAPL NVDA --verbose
"""
import sys
import os
import json
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from eval.stats import fisher_exact, format_rate_ci
from eval.runtime_guards import check_fatal_api_error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Bypass the Redis exact-key cache for the whole run BEFORE importing anything
# that touches it, so A/B arms never collide on a cached brief.
os.environ["BYPASS_CACHE"] = "true"

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage

from agent.core import (
    fetch_research_data,
    _rag_contexts,
    _SECTIONS,
    _haiku_section,
    _trim_stock, _trim_news, _trim_sec, _data_context,
    _llm as _sonnet,
    _synthesis_prompt,
)
from agent.grounding import (  # single source of truth for the judge
    JUDGE_PROMPT_VERSION,
    JUDGE_SYSTEM,
    extract_exec_and_outlook,
    get_judge_llm,
    grade_brief,
    judge_user_prompt,
)

ALL_TICKERS = ["AAPL", "NVDA", "JPM", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "V", "WMT"]

# Retrieval arms: env overrides applied per arm. Config in core/rag/reranker is
# read at call-time, so toggling these in-process re-routes the next query.
ARMS = {
    "baseline": {
        "label": "Baseline (top_k=3, no rerank)",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3"},
    },
    "context5": {
        "label": "Plain top-5 (no rerank)",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "5"},
    },
    "rerank3": {
        "label": "Rerank 20 -> 3",
        "env": {"RERANKING_ENABLED": "true", "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "3"},
    },
    "rerank5": {
        "label": "Rerank 20 -> 5",
        "env": {"RERANKING_ENABLED": "true", "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "5"},
    },
    "local-model": {
        # Fine-tuned Qwen2.5-1.5B (Ollama) serves the 2 trained sections
        # (Financial Health, Risk Factors); Haiku keeps Recent Developments and
        # SEC Filing Highlights. Requires `ollama serve` + the model loaded.
        "label": "Local model (2 sec) + Haiku",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3", "USE_LOCAL_MODEL": "true"},
    },
}

# Every arm explicitly sets the flags it depends on so values can't leak across
# arms within one process. Fill in the ones an arm leaves unset with inert
# defaults (e.g. a baseline arm still resets RERANKING_ENABLED / USE_LOCAL_MODEL).
_ARM_ENV_DEFAULTS = {
    "RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3",
    "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "false",
}

# Haiku 4.5 pricing (USD per million tokens) for the cost estimate. Update if
# rates change; cost is reported as an estimate from char/4 token approximation.
_HAIKU_IN_PER_MTOK = 1.00
_HAIKU_OUT_PER_MTOK = 5.00
from agent.tools.local_model import LOCAL_SECTIONS as _LOCAL_SECTIONS  # canonical routing set


def _est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


# Full-run cost estimate: chars/4 tokens priced from the same committed table
# the cost harness uses (scripts/model_prices.json). Labeled an estimate in
# all output — scripts/cost_report.py (exact API usage) stays the cost of
# record; this line exists so no eval run burns credits silently.
_PRICES = None


def _price_est(model: str, in_tok: int, out_tok: int) -> float:
    global _PRICES
    if _PRICES is None:
        _PRICES = json.loads(
            (Path(__file__).parent / "scripts" / "model_prices.json")
            .read_text(encoding="utf-8"))["models"]
    r = _PRICES[model]
    return in_tok / 1e6 * r["input_per_mtok"] + out_tok / 1e6 * r["output_per_mtok"]


def _brief_haiku_cost(arm: str, company: str, ticker: str,
                      section_contexts: dict, sections: list[str]) -> float:
    """Estimated Haiku $/brief: only sections actually served by Haiku cost
    money. In the local-model arm the 2 trained sections (Financial Health,
    Risk Factors) are local ($0.00) and Recent Developments + SEC Filing
    Highlights hit Haiku; other arms pay Haiku for all 4."""
    local = ARMS[arm]["env"].get("USE_LOCAL_MODEL") == "true"
    in_tok = out_tok = 0
    for (heading, instr), out in zip(_SECTIONS, sections):
        if local and heading in _LOCAL_SECTIONS:
            continue  # served by the local model — $0.00
        prompt = (f"Write ONLY the '{heading}' section for a {company} ({ticker}) investment brief.\n"
                  f"{instr}\nStart with the markdown heading. Be concise.\n\nData:\n"
                  f"{section_contexts[heading]}")
        in_tok += _est_tokens(prompt)
        out_tok += _est_tokens(out)
    return in_tok / 1e6 * _HAIKU_IN_PER_MTOK + out_tok / 1e6 * _HAIKU_OUT_PER_MTOK

# The judge LLM, prompt, and claim-parsing now live in agent/grounding.py so the
# offline harness and the inline grounding-critic share one definition.


# ── Resilience ──────────────────────────────────────────────────────────────────

def _retry(fn, *args, _attempts=4, _base=3.0, **kwargs):
    """Retry a call with exponential backoff. A long A/B run makes many LLM/API
    calls; a single transient connection error shouldn't waste the whole run."""
    for i in range(_attempts):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            # Non-retryable: a credit-balance 400 raises SystemExit here —
            # fail the run loudly instead of burning retries into a silent
            # per-ticker skip (measured failure mode, 2026-09-03).
            check_fatal_api_error(e)
            if i == _attempts - 1:
                raise
            wait = _base * (2 ** i)
            print(f"    transient error ({type(e).__name__}): retry {i+1}/{_attempts-1} in {wait:.0f}s...",
                  flush=True)
            time.sleep(wait)


# ── Judge helpers ──────────────────────────────────────────────────────────────
# The judge prompt, claim parsing, and scoring live in agent/grounding.py. Only
# the harness-specific findings persistence stays local.

FINDINGS_DIR = Path(__file__).parent / "eval_findings"


def _save_findings(ticker: str, arm: str, source_context: str, exec_and_outlook: str, findings: str):
    """Persist the retrieved source context + audited text + judge findings so a
    run's per-claim evidence survives (the printed counts alone can't be
    re-derived without the judge, and auditing a label needs the source it saw)."""
    try:
        FINDINGS_DIR.mkdir(exist_ok=True)
        (FINDINGS_DIR / f"{ticker}_{arm}.md").write_text(
            f"# {ticker} — {arm}\n\n## Retrieved source context\n\n{source_context}\n\n"
            f"## Audited (Exec Summary + Outlook)\n\n{exec_and_outlook}\n\n"
            f"## Judge findings\n\n{findings}\n",
            encoding="utf-8",
        )
    except Exception as e:
        print(f"    (could not save findings for {ticker}/{arm}: {e})", flush=True)


# ── Data fetch (shared across arms) ─────────────────────────────────────────────

def fetch_base(ticker: str) -> dict:
    """Fetch and trim stock/news/SEC data once. Reused across all arms so only
    the retrieval stage differs between them (and to save network round-trips)."""
    print(f"[{ticker}] Fetching stock / news / SEC (shared across arms)...", flush=True)
    stock_data, news_data, sec_data = _retry(fetch_research_data, ticker)
    stock   = _trim_stock(stock_data)
    news    = _trim_news(news_data)
    sec     = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)
    return {
        "company": company,
        "context": context,
        "stock": stock,
        "news": news,
        "sec": sec,
    }


# ── Per-arm pipeline ────────────────────────────────────────────────────────────

def _apply_arm_env(arm: str):
    # Reset every controlled flag to its inert default, then apply this arm's
    # overrides — so no flag leaks from the previously-run arm.
    env = {**_ARM_ENV_DEFAULTS, **ARMS[arm]["env"]}
    for k, v in env.items():
        os.environ[k] = v


def run_arm(ticker: str, base: dict, arm: str, verbose: bool) -> dict:
    _apply_arm_env(arm)
    company = base["company"]
    context = base["context"]

    print(f"  [{ticker} | {arm}] RAG retrieval...", flush=True)
    t_rag = time.perf_counter()
    rag_highlights, rag_risks = _retry(_rag_contexts, ticker)
    retrieval_s = time.perf_counter() - t_rag

    section_contexts = {
        "### Financial Health":      context,
        "### Recent Developments":   context,
        "### SEC Filing Highlights": rag_highlights or context,
        "### Risk Factors":          rag_risks or context,
    }

    t_sec = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                _retry, _haiku_section, heading, instr, company, ticker, section_contexts[heading]
            )
            for heading, instr in _SECTIONS
        ]
        sections = [f.result() for f in futures]
    sections_s = time.perf_counter() - t_sec

    t_syn = time.perf_counter()
    brief = _retry(
        _sonnet.invoke,
        [HumanMessage(content=_synthesis_prompt(ticker, company, sections))],
    ).content
    synth_s = time.perf_counter() - t_syn

    pipeline_s = retrieval_s + sections_s + synth_s
    haiku_cost = _brief_haiku_cost(arm, company, ticker, section_contexts, sections)

    source_context = "\n\n".join([
        f"STOCK DATA:\n{json.dumps(base['stock'], indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps(base['news'], indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps(base['sec'], indent=2)}",
        f"RAG — SEC HIGHLIGHTS:\n{rag_highlights or '(not available)'}",
        f"RAG — RISK FACTORS:\n{rag_risks or '(not available)'}",
    ])

    exec_and_outlook = extract_exec_and_outlook(brief)
    section_block    = "\n\n".join(sections)

    print(f"  [{ticker} | {arm}] judging...", flush=True)
    # Shared judge; retry-wrap the LLM call so one transient error can't waste a
    # long A/B run.
    grade = grade_brief(
        source_context, section_block, exec_and_outlook,
        invoker=lambda messages: _retry(get_judge_llm().invoke, messages),
    )

    _save_findings(ticker, arm, source_context, exec_and_outlook, grade.findings)

    # Estimated total spend for this (ticker, arm): Haiku sections (existing
    # estimate) + Sonnet synthesis + Sonnet judge, chars/4 tokens priced from
    # scripts/model_prices.json. Excludes retried calls.
    est_cost = haiku_cost
    est_cost += _price_est("claude-sonnet-4-6",
                           _est_tokens(_synthesis_prompt(ticker, company, sections)),
                           _est_tokens(brief))
    est_cost += _price_est("claude-sonnet-4-6",
                           _est_tokens(JUDGE_SYSTEM) + _est_tokens(
                               judge_user_prompt(source_context, section_block, exec_and_outlook)),
                           _est_tokens(grade.findings))

    counts = {
        "supported": grade.supported, "unsupported": grade.unsupported,
        "inference": grade.inference, "total": grade.total,
    }

    s, u, i, t = grade.supported, grade.unsupported, grade.inference, grade.total
    print(
        f"  [{ticker} | {arm}] {s} SUP  {u} UNSUP  {i} INF  ({t} claims)  "
        f"retrieval={retrieval_s:.2f}s  pipeline={pipeline_s:.2f}s  haiku_cost=${haiku_cost:.5f}",
        flush=True,
    )
    if verbose:
        print(grade.findings, flush=True)

    return {
        "ticker": ticker, "arm": arm,
        "judge_version": JUDGE_PROMPT_VERSION,
        "retrieval_s": retrieval_s, "pipeline_s": pipeline_s, "haiku_cost": haiku_cost,
        "est_cost": round(est_cost, 5),
        "inference_claims": grade.inference_claims,
        **counts,
    }


# ── Summary tables ──────────────────────────────────────────────────────────────

def _balanced_tickers(results: list[dict], arms: list[str]) -> set:
    """Tickers that completed *every* requested arm — so the comparison stays
    apples-to-apples even if a run was cut short (e.g. by an API outage or
    credit limit) and some tickers only finished a subset of arms."""
    by_arm = {arm: {r["ticker"] for r in results if r["arm"] == arm} for arm in arms}
    if not by_arm or any(not v for v in by_arm.values()):
        return set()
    return set.intersection(*by_arm.values())


def _aggregate(results: list[dict], arm: str, only: set | None = None) -> dict:
    rows = [r for r in results if r["arm"] == arm and (only is None or r["ticker"] in only)]
    n = len(rows)
    agg = {k: sum(r[k] for r in rows) for k in ("supported", "unsupported", "inference", "total")}
    agg["tickers"] = n
    agg["grounding_pct"] = (agg["supported"] / agg["total"] * 100) if agg["total"] else 0.0
    agg["unsupported_pct"] = (agg["unsupported"] / agg["total"] * 100) if agg["total"] else 0.0
    agg["retrieval_s"] = (sum(r["retrieval_s"] for r in rows) / n) if n else 0.0
    agg["pipeline_s"] = (sum(r["pipeline_s"] for r in rows) / n) if n else 0.0
    agg["haiku_cost"] = (sum(r["haiku_cost"] for r in rows) / n) if n else 0.0
    return agg


def print_comparison(results: list[dict], arms: list[str]):
    # Restrict the comparison to tickers that completed every arm, so a partial
    # run still yields an honest apples-to-apples table.
    balanced = _balanced_tickers(results, arms)
    all_tickers = {r["ticker"] for r in results}
    excluded = sorted(all_tickers - balanced)

    print(f"\n\n{'='*100}", flush=True)
    print("  BEFORE / AFTER — RERANKING A/B  (LLM-as-judge grounding)", flush=True)
    print(f"{'='*100}", flush=True)
    print(f"  Judge prompt: {JUDGE_PROMPT_VERSION}", flush=True)
    print(f"  Balanced over {len(balanced)} ticker(s) completing all arms: "
          f"{', '.join(sorted(balanced)) or '(none)'}", flush=True)
    if excluded:
        print(f"  Excluded (incomplete arms): {', '.join(excluded)}", flush=True)
    header = (
        f"  {'Arm':<30} {'Tk':>3} {'Sup':>5} {'Uns':>5} {'Inf':>5} {'Tot':>5} "
        f"{'Ground%':>8} {'Unsup%':>7} {'Retr(s)':>8} {'Pipe(s)':>8} {'Haiku$/brief':>13}"
    )
    print(header, flush=True)
    print(f"  {'-'*114}", flush=True)
    for arm in arms:
        a = _aggregate(results, arm, only=balanced)
        print(
            f"  {ARMS[arm]['label']:<30} {a['tickers']:>3} {a['supported']:>5} "
            f"{a['unsupported']:>5} {a['inference']:>5} {a['total']:>5} "
            f"{a['grounding_pct']:>7.1f}% {a['unsupported_pct']:>6.1f}% "
            f"{a['retrieval_s']:>8.2f} {a['pipeline_s']:>8.2f} {a['haiku_cost']:>12.5f}",
            flush=True,
        )

    # Statistics: interval on every rate, exact test on every comparison —
    # at ~65-85 claims per run, point estimates alone overstate what a
    # single pass can resolve.
    ref = "baseline" if "baseline" in arms else arms[0]
    ref_agg = _aggregate(results, ref, only=balanced)
    print(f"\n  Statistics (Wilson 95% CI; Fisher exact vs {ARMS[ref]['label']}):", flush=True)
    for arm in arms:
        a = _aggregate(results, arm, only=balanced)
        line = f"    {ARMS[arm]['label']:<30} unsupported {format_rate_ci(a['unsupported'], a['total'])}"
        if arm != ref and a["total"] and ref_agg["total"]:
            p = fisher_exact(
                ref_agg["unsupported"], ref_agg["total"] - ref_agg["unsupported"],
                a["unsupported"], a["total"] - a["unsupported"],
            )
            line += f"  p={p:.4f}"
        print(line, flush=True)

    # Headline delta: baseline vs rerank3 (final chunk count held constant).
    if "baseline" in arms and "rerank3" in arms:
        b = _aggregate(results, "baseline", only=balanced)
        r = _aggregate(results, "rerank3", only=balanced)
        print(f"\n  HEADLINE (chunk count held at 3): baseline -> rerank3", flush=True)
        print(
            f"    unsupported claims : {b['unsupported']} -> {r['unsupported']} "
            f"({b['unsupported_pct']:.1f}% -> {r['unsupported_pct']:.1f}%)", flush=True,
        )
        print(
            f"    grounding rate     : {b['grounding_pct']:.1f}% -> {r['grounding_pct']:.1f}%",
            flush=True,
        )
        print(
            f"    retrieval latency  : {b['retrieval_s']:.2f}s -> {r['retrieval_s']:.2f}s "
            f"(+{r['retrieval_s'] - b['retrieval_s']:.2f}s)", flush=True,
        )
        print(
            f"    pipeline latency   : {b['pipeline_s']:.2f}s -> {r['pipeline_s']:.2f}s "
            f"(+{r['pipeline_s'] - b['pipeline_s']:.2f}s)", flush=True,
        )
    print(flush=True)


# ── Main ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Grounding eval with reranking A/B arms.")
    parser.add_argument("--arms", nargs="+",
                        default=["baseline", "context5", "rerank3", "rerank5"],
                        choices=list(ARMS.keys()), help="Which retrieval arms to run.")
    parser.add_argument("--tickers", nargs="+", default=ALL_TICKERS,
                        help="Which tickers to evaluate.")
    parser.add_argument("--verbose", action="store_true",
                        help="Print full per-claim judge findings.")
    parser.add_argument("--json-out", default=None, metavar="PATH",
                        help="Write per-(ticker,arm) results + per-arm aggregates as JSON. "
                             "Used by the Argo eval workflow to fan out one ticker per pod "
                             "and aggregate in a final step.")
    args = parser.parse_args()

    print(f"BYPASS_CACHE={os.getenv('BYPASS_CACHE')} — Redis exact-key cache disabled for this run.",
          flush=True)
    print(f"Arms: {', '.join(args.arms)}   Tickers: {', '.join(args.tickers)}\n", flush=True)

    results = []
    skipped = []
    for ticker in args.tickers:
        print(f"\n{'='*72}\n  {ticker}\n{'='*72}", flush=True)
        try:
            base = fetch_base(ticker)
            for arm in args.arms:
                results.append(run_arm(ticker, base, arm, args.verbose))
        except Exception as e:
            # After retries, a ticker still failed — skip it so the rest of the
            # run (and the comparison table) still completes.
            print(f"  [{ticker}] SKIPPED after retries: {type(e).__name__}: {e}", flush=True)
            skipped.append(ticker)

    print_comparison(results, args.arms)
    if skipped:
        print(f"  NOTE: {len(skipped)} ticker(s) skipped after retries: {', '.join(skipped)}",
              flush=True)

    # Sample of INFERENCE-labeled claims from the rerank arms — lets you verify
    # the "denominator effect" (more inference claims, not more fabrication).
    rerank_arms = [a for a in args.arms if a.startswith("rerank")]
    samples = [
        (r["ticker"], r["arm"], c)
        for r in results if r["arm"] in rerank_arms
        for c in r.get("inference_claims", [])
    ]
    if samples:
        print(f"\n  INFERENCE claims in rerank arms (sample of up to 10 of {len(samples)}):",
              flush=True)
        for ticker, arm, claim in samples[:10]:
            print(f"    [{ticker}|{arm}] {claim}", flush=True)
    print(f"\n  Full per-claim judge findings saved to: {FINDINGS_DIR}", flush=True)

    if args.json_out:
        balanced = _balanced_tickers(results, args.arms)
        payload = {
            "arms": args.arms,
            "tickers": args.tickers,
            "skipped": skipped,
            "results": results,
            "aggregate": {arm: _aggregate(results, arm, only=balanced) for arm in args.arms},
        }
        Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"  JSON results written to: {args.json_out}", flush=True)


if __name__ == "__main__":
    main()
