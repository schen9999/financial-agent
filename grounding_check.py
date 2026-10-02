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
from eval.runtime_guards import check_fatal_api_error, check_local_model_served
from eval.label import count_labels_deduped
from eval.stock_block import stock_block_empty

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Bypass the Redis exact-key cache for the whole run BEFORE importing anything
# that touches it, so A/B arms never collide on a cached brief.
os.environ["BYPASS_CACHE"] = "true"

from dotenv import load_dotenv
load_dotenv()

from agent.core import (
    fetch_research_data,
    _rag_contexts,
    _SECTIONS,
    _haiku_section,
    _section_llm,
    _trim_stock, _trim_news, _trim_sec, _data_context,
    synthesize,
    BriefFormatError,
    _synthesis_prompt,
    DEFAULT_HIGHLIGHTS_QUERY,
    DEFAULT_RISKS_QUERY,
)
from agent import llm_ledger
from agent.tools import slm as _slm
from agent.tools.rag import pop_sources
from eval import rag_faithfulness
from agent.grounding import (  # single source of truth for the judge
    JUDGE_PROMPT_VERSION,
    JUDGE_SYSTEM,
    extract_exec_and_outlook,
    get_judge_llm,
    grade_brief,
    judge_user_prompt,
)

ALL_TICKERS = ["AAPL", "NVDA", "JPM", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "V", "WMT"]

# Arms (env overrides per arm) live in eval/arms.py, importable by tests.
from eval.arms import ARMS  # noqa: E402
from eval.arms import apply_arm_env as _apply_arm_env  # noqa: E402
from eval.arms import uses_local_model as _uses_local_model  # noqa: E402
from eval.arms import slm_endpoint_name, uses_slm  # noqa: E402

# Ledger sites that are evaluation, not harness: never subject to an SLM
# arm's endpoint check, and summarized separately.
_EVAL_SITES = ("judge", "rag_judge")


class EndpointMismatchError(RuntimeError):
    """An SLM arm's agent call was served by something other than its endpoint."""


# Failures no retry can fix: retrying would only re-spend or re-mask them.
_NON_RETRYABLE = (BriefFormatError, _slm.SLMParseError, _slm.SLMConfigError,
                  EndpointMismatchError)

# Server-reported endpoint facts per SLM arm, checked once before any ticker.
_SLM_PROVENANCE: dict[str, dict] = {}

# Haiku 4.5 pricing (USD per million tokens) for the cost estimate. Update if
# rates change; cost is reported as an estimate from char/4 token approximation.
_HAIKU_IN_PER_MTOK = 1.00
_HAIKU_OUT_PER_MTOK = 5.00
from agent.tools.local_model import LOCAL_SECTIONS as _LOCAL_SECTIONS  # canonical routing set
from agent.tools.local_model import LocalChat, local_model_backend


def _local_model_provenance(arm: str) -> dict | None:
    """Which model served this arm's local sections, recorded in the findings
    metadata and the result row so runs against different models can be told
    apart later. Name, URL, and sampling come from the exact client the
    pipeline builds for a local section (agent.core._section_llm, under this
    arm's env); LOCAL_MODEL_DIR is set alongside the served name by
    `make vm-vllm`. None for arms that never route to the local model."""
    if not _uses_local_model(arm):
        return None
    _apply_arm_env(arm)
    client = _section_llm(next(iter(_LOCAL_SECTIONS)))
    if not isinstance(client, LocalChat):
        raise SystemExit(f"FATAL: arm {arm!r} sets USE_LOCAL_MODEL but local "
                         f"sections route to {type(client).__name__}")
    return {
        "local_model_served_name": client.model,
        "local_model_dir": os.getenv("LOCAL_MODEL_DIR") or "unrecorded",
        "local_model_backend": local_model_backend(),
        "local_model_url": client.url,
        "local_model_sampling": json.dumps(client.sampling_params(), sort_keys=True),
    }


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
        except _NON_RETRYABLE:
            raise
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


def _save_findings(ticker: str, arm: str, source_context: str, section_block: str,
                   exec_and_outlook: str, findings: str,
                   provenance: dict | None = None):
    """Persist EVERYTHING the judge saw plus its findings, so a run's
    per-claim evidence survives and is self-describing: metadata (ticker,
    arm, judge prompt version, context hash), the retrieved source context,
    the pre-written sections (judge input — previously unpersisted, the
    documented validation caveat), the audited text, and the findings.
    Format rendered by eval.label.render_findings_md, which lives beside
    the parser that reads it back."""
    from eval.label import render_findings_md
    try:
        FINDINGS_DIR.mkdir(exist_ok=True)
        (FINDINGS_DIR / f"{ticker}_{arm}.md").write_text(
            render_findings_md(ticker, arm, JUDGE_PROMPT_VERSION,
                               source_context, section_block,
                               exec_and_outlook, findings,
                               extra_metadata=provenance),
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

def _judge_invoke(site: str, messages):
    """The shared Sonnet judge, retry-wrapped, recorded under an eval site."""
    t0 = time.perf_counter()
    resp = _retry(get_judge_llm().invoke, messages)
    llm_ledger.record_response(site, "anthropic", "claude-sonnet-4-6", resp, t0)
    return resp


def _check_slm_endpoint(arm: str, agent_records: list[dict]):
    """An SLM arm proves its traffic: at least one agent call, and every agent
    call served by the arm's endpoint — never a run quietly served by Anthropic."""
    want = slm_endpoint_name(arm)
    if not agent_records:
        raise EndpointMismatchError(f"{arm}: no agent LLM calls recorded")
    wrong = sorted({f"{r['site']}@{r['endpoint']}" for r in agent_records if r["endpoint"] != want})
    if wrong:
        raise EndpointMismatchError(f"{arm}: agent calls not served by {want}: {wrong}")


def _rag_faithfulness(ticker: str, arm: str, answers: dict, sources: dict) -> dict:
    """Judge each RAG answer against its own retrieved chunks (separate
    metric, eval/rag_faithfulness.py); persists a .ragf.json per (ticker, arm)."""
    out, record = {}, {"ticker": ticker, "arm": arm,
                       "prompt_version": rag_faithfulness.RAG_JUDGE_PROMPT_VERSION, "answers": {}}
    for which, answer in answers.items():
        chunks = sources.get(which)
        if not answer or not chunks:
            out[which] = None  # RAG unavailable for this question: nothing to judge
            continue
        res = rag_faithfulness.grade(chunks, answer,
                                     invoke=lambda m: _judge_invoke("rag_judge", m))
        out[which] = {k: res[k] for k in ("supported", "unsupported", "total")}
        record["answers"][which] = {"chunks": chunks, "answer": answer, **res}
    try:
        FINDINGS_DIR.mkdir(exist_ok=True)
        (FINDINGS_DIR / f"{ticker}_{arm}.ragf.json").write_text(
            json.dumps(record, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"    (could not save RAG faithfulness for {ticker}/{arm}: {e})", flush=True)
    return out


def run_arm(ticker: str, base: dict, arm: str, verbose: bool) -> dict:
    _apply_arm_env(arm)
    llm_ledger.drain()  # this (ticker, arm)'s calls only
    company = base["company"]
    context = base["context"]
    slm_arm = uses_slm(arm)

    print(f"  [{ticker} | {arm}] RAG retrieval...", flush=True)
    t_rag = time.perf_counter()
    rag_highlights, rag_risks = _retry(_rag_contexts, ticker)
    retrieval_s = time.perf_counter() - t_rag
    rag_sources = {"highlights": pop_sources(DEFAULT_HIGHLIGHTS_QUERY),
                   "risks": pop_sources(DEFAULT_RISKS_QUERY)}

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

    # Same prompt and model as before (Sonnet; the SLM on SLM arms). guard:
    # a brief without a non-empty Executive Summary + Outlook is retried once,
    # then fails this ticker loudly (BriefFormatError) — never judged as 0
    # claims. 0 of 370 committed findings files would have tripped it.
    t_syn = time.perf_counter()
    brief = _retry(synthesize, ticker, company, sections, guard=True)
    synth_s = time.perf_counter() - t_syn

    pipeline_s = retrieval_s + sections_s + synth_s
    haiku_cost = 0.0 if slm_arm else _brief_haiku_cost(arm, company, ticker,
                                                       section_contexts, sections)

    source_context = "\n\n".join([
        f"STOCK DATA:\n{json.dumps(base['stock'], indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps(base['news'], indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps(base['sec'], indent=2)}",
        f"RAG — SEC HIGHLIGHTS:\n{rag_highlights or '(not available)'}",
        f"RAG — RISK FACTORS:\n{rag_risks or '(not available)'}",
    ])

    exec_and_outlook = extract_exec_and_outlook(brief)
    section_block    = "\n\n".join(sections)
    # Detection only (eval/stock_block.py): a failed stock fetch is not
    # retried or skipped — the brief is written without stock data. Record
    # it so the aggregate can count it; behaviour is unchanged.
    stock_empty = stock_block_empty(source_context)
    if stock_empty:
        print(f"  [{ticker} | {arm}] NOTE: STOCK DATA block is empty — brief "
              f"written without stock data (yfinance failure?)", flush=True)

    print(f"  [{ticker} | {arm}] judging...", flush=True)
    # Shared judge, unchanged inputs; retry-wrapped so one transient error
    # can't waste a long A/B run.
    t_judge = time.perf_counter()
    grade = grade_brief(
        source_context, section_block, exec_and_outlook,
        invoker=lambda messages: _judge_invoke("judge", messages),
    )
    judge_s = time.perf_counter() - t_judge

    ragf = None
    if rag_faithfulness.enabled():
        ragf = _rag_faithfulness(ticker, arm, {"highlights": rag_highlights, "risks": rag_risks},
                                 rag_sources)

    records = llm_ledger.drain()
    agent_records = [r for r in records if r["site"] not in _EVAL_SITES]
    eval_records = [r for r in records if r["site"] in _EVAL_SITES]
    if slm_arm:
        _check_slm_endpoint(arm, agent_records)
    llm = llm_ledger.summarize(agent_records)

    provenance = _local_model_provenance(arm) or _SLM_PROVENANCE.get(arm)
    findings_meta = {**(provenance or {}),
                     "llm_calls": llm["total"]["calls"],
                     "llm_endpoints": ",".join(llm["endpoints"]),
                     "llm_by_site": json.dumps(llm["by_site"], sort_keys=True)}
    _save_findings(ticker, arm, source_context, section_block, exec_and_outlook,
                   grade.findings, findings_meta)

    # Estimated total spend for this (ticker, arm): Haiku sections (existing
    # estimate) + Sonnet synthesis + Sonnet judge, chars/4 tokens priced from
    # scripts/model_prices.json. Excludes retried calls. SLM arms pay only the
    # judge. The RAG-faithfulness judge is priced from its recorded usage.
    est_cost = haiku_cost
    if not slm_arm:
        est_cost += _price_est("claude-sonnet-4-6",
                               _est_tokens(_synthesis_prompt(ticker, company, sections)),
                               _est_tokens(brief))
    est_cost += _price_est("claude-sonnet-4-6",
                           _est_tokens(JUDGE_SYSTEM) + _est_tokens(
                               judge_user_prompt(source_context, section_block, exec_and_outlook)),
                           _est_tokens(grade.findings))
    for r in eval_records:
        if r["site"] == "rag_judge":
            est_cost += _price_est("claude-sonnet-4-6", r["prompt_tokens"] or 0,
                                   r["completion_tokens"] or 0)

    # Deduped recount from the findings text (eval.label): one label per
    # CLAIM block; a repeated identical label is suppressed, a different
    # label in the same block still counts (free-form verdict). grade's own
    # counts tally every LABEL: line and ran one high on 9j2dj (JPM).
    counts = count_labels_deduped(grade.findings)
    dups = counts.pop("duplicates_suppressed")
    if dups:
        print(f"  [{ticker} | {arm}] NOTE: {dups} duplicate LABEL line(s) "
              f"suppressed within a claim block", flush=True)

    s, u, i, t = (counts["supported"], counts["unsupported"],
                  counts["inference"], counts["total"])
    tot = llm["total"]
    print(
        f"  [{ticker} | {arm}] {s} SUP  {u} UNSUP  {i} INF  ({t} claims)  "
        f"retrieval={retrieval_s:.2f}s  pipeline={pipeline_s:.2f}s  haiku_cost=${haiku_cost:.5f}  "
        f"llm_calls={tot['calls']} ({','.join(llm['endpoints'])}) truncated={tot['truncated']} "
        f"loops={tot['repeat_run']} parse_fail={tot['parse_failure']} "
        f"format_fail={tot['format_failure']} retries={tot['retry']}",
        flush=True,
    )
    if verbose:
        print(grade.findings, flush=True)

    return {
        "ticker": ticker, "arm": arm,
        "judge_version": JUDGE_PROMPT_VERSION,
        "retrieval_s": retrieval_s, "pipeline_s": pipeline_s, "haiku_cost": haiku_cost,
        "est_cost": round(est_cost, 5),
        "stock_block_empty": stock_empty,
        "inference_claims": grade.inference_claims,
        **counts,
        "timing_s": {"retrieval": round(retrieval_s, 3), "sections": round(sections_s, 3),
                     "synthesis": round(synth_s, 3), "judge": round(judge_s, 3)},
        "llm": llm,
        "llm_eval": llm_ledger.summarize(eval_records),
        **({"rag_faithfulness": ragf} if ragf is not None else {}),
        **({"local_model": provenance} if _uses_local_model(arm) and provenance else {}),
        **({"slm": provenance} if slm_arm and provenance else {}),
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

    # A local-model arm must measure the model it claims to: confirm the
    # server lists LOCAL_MODEL_NAME before any ticker runs (exits otherwise).
    local_arm = next((a for a in args.arms if _uses_local_model(a)), None)
    if local_arm:
        prov = _local_model_provenance(local_arm)
        if prov["local_model_backend"] == "openai":
            ids = check_local_model_served(prov["local_model_url"],
                                           prov["local_model_served_name"])
            print(f"Local model: {prov['local_model_served_name']} (dir "
                  f"{prov['local_model_dir']}) listed on "
                  f"{prov['local_model_url']}/v1/models {ids}\n", flush=True)
        else:
            print(f"Local model: {prov['local_model_served_name']} via "
                  f"{prov['local_model_backend']} — /v1/models check applies to "
                  f"the openai backend only; not checked\n", flush=True)

    # An SLM arm must measure the endpoint it names: the server must list
    # SLM_MODEL_NAME and answer with the key; its own facts (build, model
    # file, quant, context, slots) become provenance. Exits otherwise.
    for arm in args.arms:
        if uses_slm(arm):
            _apply_arm_env(arm)
            try:
                _SLM_PROVENANCE[arm] = _slm.server_facts()
            except _slm.SLMConfigError as e:
                raise SystemExit(f"FATAL: {e}")
            f = _SLM_PROVENANCE[arm]
            print(f"SLM endpoint for {arm}: {f['slm_endpoint']} {f['slm_url']} serves "
                  f"{f['slm_served_name']} ({f['slm_model_path']}, {f['slm_model_ftype']}, "
                  f"n_ctx {f['slm_n_ctx']}, {f['slm_total_slots']} slots, build "
                  f"{f['slm_build']}); thinking {f['slm_thinking']}\n", flush=True)

    llm_ledger.enable()
    results = []
    skipped = []
    failures = []
    for ticker in args.tickers:
        print(f"\n{'='*72}\n  {ticker}\n{'='*72}", flush=True)
        arm = None
        try:
            base = fetch_base(ticker)
            for arm in args.arms:
                results.append(run_arm(ticker, base, arm, args.verbose))
        except Exception as e:
            # After retries, a ticker still failed — skip it so the rest of the
            # run (and the comparison table) still completes. The kind is
            # recorded: a format/parse/endpoint failure is a measured outcome
            # the aggregate counts, not just a missing row.
            kind = ("format" if isinstance(e, BriefFormatError) else
                    "parse" if isinstance(e, _slm.SLMParseError) else
                    "endpoint_mismatch" if isinstance(e, EndpointMismatchError) else
                    "endpoint_error" if isinstance(e, _slm.SLMRequestError) else "other")
            print(f"  [{ticker}] SKIPPED after retries ({kind}): {type(e).__name__}: {e}", flush=True)
            skipped.append(ticker)
            failures.append({"ticker": ticker, "arm": arm, "kind": kind,
                             "error": f"{type(e).__name__}: {str(e)[:300]}",
                             "llm": llm_ledger.summarize(llm_ledger.drain())})

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
            "failures": failures,
            "results": results,
            "aggregate": {arm: _aggregate(results, arm, only=balanced) for arm in args.arms},
        }
        Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"  JSON results written to: {args.json_out}", flush=True)


if __name__ == "__main__":
    main()
