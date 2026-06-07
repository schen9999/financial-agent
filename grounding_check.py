#!/usr/bin/env python3
"""
grounding_check.py

For AAPL, NVDA, JPM — tests the constrained synthesis prompt from core.py
against BOTH Haiku and Sonnet as the synthesis model:
  1. Generates the brief using _synthesis_prompt from core.py.
  2. Assembles the exact source context the model had (trimmed stock,
     news, SEC summaries, RAG results, and the 4 pre-written sections).
  3. Runs a Claude Sonnet judge (temperature=0) that audits every
     specific quantitative claim, price target, and forward-looking
     figure in the Executive Summary and Outlook and labels each:
       SUPPORTED   — traceable to the source context
       UNSUPPORTED — not in the context (likely model-generated)
       INFERENCE   — reasonable extrapolation, not a verbatim figure
  4. Prints findings per ticker plus a supported/unsupported count.
  5. Prints a summary table for each synthesis model.

Do NOT change core.py defaults or commit this file.
"""
import sys
import os
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from agent.core import (
    fetch_research_data,
    _rag_contexts,
    _SECTIONS,
    _haiku_section,
    _trim_stock, _trim_news, _trim_sec, _data_context,
    _llm as _sonnet,
    _synthesis_prompt,
)

TICKERS = ["AAPL", "NVDA", "JPM", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "V", "WMT"]

# Dedicated judge LLM — temperature=0 for deterministic factual evaluation.
_judge_llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0,
    streaming=False,
)


# ── Judge helpers ──────────────────────────────────────────────────────────────

_JUDGE_SYSTEM = """\
You are a financial accuracy auditor. Your task is to verify whether specific \
claims in an AI-generated investment brief are grounded in the source data the \
model was given.

Evaluate ONLY the Executive Summary and Outlook sections. For every specific \
quantitative figure, price target, threshold, ratio, metric, percentage, named \
product milestone, or forward-looking number in those sections, output one entry \
in this exact format:

CLAIM: "<exact quoted text>"
LABEL: SUPPORTED | UNSUPPORTED | INFERENCE
REASON: <one sentence — if SUPPORTED, cite the source figure; if UNSUPPORTED, \
state it does not appear in the context; if INFERENCE, explain the derivation>

Definitions:
  SUPPORTED   — the exact number or fact is explicitly present in the source \
data or pre-written sections below.
  UNSUPPORTED — a specific number, price target, threshold, or named milestone \
that does NOT appear in the source data and cannot be derived from it.
  INFERENCE   — a directional conclusion, rounded/scaled figure, or reasonable \
extrapolation that follows logically from the data but is not verbatim in it.

Be exhaustive — do not skip any quantitative or forward-looking claim.\
"""


def _judge_user_prompt(source_context: str, brief: str, exec_and_outlook: str) -> str:
    return f"""BACKGROUND: An AI wrote the Executive Summary and Outlook using the \
four pre-written sections as its primary input. The raw source data below is what \
those sections were originally generated from.

=== RAW SOURCE DATA ===
{source_context}

=== PRE-WRITTEN SECTIONS (direct input to the synthesis model) ===
{brief}

=== EXECUTIVE SUMMARY AND OUTLOOK TO AUDIT ===
{exec_and_outlook}
"""


def _extract_exec_and_outlook(brief: str) -> str:
    """Pull only the Executive Summary and Outlook text from the full brief."""
    target_headings = {"Executive Summary", "Outlook"}
    result, current, buf = [], None, []

    for line in brief.split("\n"):
        if line.startswith("### "):
            if current in target_headings:
                result.append(f"### {current}\n" + "\n".join(buf).strip())
            current = line[4:].strip()
            buf = []
        else:
            if current in target_headings:
                buf.append(line)

    if current in target_headings:
        result.append(f"### {current}\n" + "\n".join(buf).strip())

    return "\n\n".join(result)


def _count_labels(text: str) -> dict[str, int]:
    # Matches both plain "LABEL: X" and bold "**LABEL:** X" judge formatting.
    return {
        "supported":   len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+SUPPORTED\b",   text, re.I)),
        "unsupported": len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+UNSUPPORTED\b", text, re.I)),
        "inference":   len(re.findall(r"\*{0,2}LABEL:\*{0,2}\s+INFERENCE\b",   text, re.I)),
    }


# ── Per-ticker pipeline ────────────────────────────────────────────────────────

def _fetch_ticker_data(ticker: str) -> tuple:
    """Fetch and trim all data for a ticker; returns (company, context, sections, source_context)."""
    print(f"[{ticker}] Fetching stock / news / SEC...", flush=True)
    stock_data, news_data, sec_data = fetch_research_data(ticker)
    stock   = _trim_stock(stock_data)
    news    = _trim_news(news_data)
    sec     = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)

    print(f"[{ticker}] Running RAG...", flush=True)
    t_rag = time.perf_counter()
    rag_highlights, rag_risks = _rag_contexts(ticker)
    print(f"[{ticker}] RAG done in {time.perf_counter()-t_rag:.2f}s", flush=True)

    section_contexts = {
        "### Financial Health":      context,
        "### Recent Developments":   context,
        "### SEC Filing Highlights": rag_highlights or context,
        "### Risk Factors":          rag_risks or context,
    }

    print(f"[{ticker}] Generating Haiku sections...", flush=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                _haiku_section, heading, instr, company, ticker, section_contexts[heading]
            )
            for heading, instr in _SECTIONS
        ]
        sections = [f.result() for f in futures]

    source_context = "\n\n".join([
        f"STOCK DATA:\n{json.dumps(stock, indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps(news, indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps(sec, indent=2)}",
        f"RAG — SEC HIGHLIGHTS:\n{rag_highlights or '(not available)'}",
        f"RAG — RISK FACTORS:\n{rag_risks or '(not available)'}",
    ])
    return company, context, sections, source_context


def run_ticker(ticker: str, company: str, sections: list[str], source_context: str) -> dict:
    SEP = "=" * 72
    print(f"\n{SEP}", flush=True)
    print(f"  {ticker}  [sonnet]", flush=True)
    print(SEP, flush=True)

    print(f"[{ticker}] Running constrained Sonnet synthesis...", flush=True)
    t_syn = time.perf_counter()
    brief = _sonnet.invoke(
        [HumanMessage(content=_synthesis_prompt(ticker, company, sections))]
    ).content
    print(f"[{ticker}] Synthesis done in {time.perf_counter()-t_syn:.2f}s ({len(brief)} chars)", flush=True)

    exec_and_outlook = _extract_exec_and_outlook(brief)
    section_block    = "\n\n".join(sections)

    print(f"[{ticker}] Running Sonnet judge (temperature=0)...", flush=True)
    t_judge = time.perf_counter()
    findings = _judge_llm.invoke([
        SystemMessage(content=_JUDGE_SYSTEM),
        HumanMessage(content=_judge_user_prompt(source_context, section_block, exec_and_outlook)),
    ]).content
    print(f"[{ticker}] Judge done in {time.perf_counter()-t_judge:.2f}s", flush=True)

    counts = _count_labels(findings)
    counts["total"] = sum(counts.values())

    return {"ticker": ticker, "brief": brief, "findings": findings, **counts}


# ── Main ───────────────────────────────────────────────────────────────────────

all_results = []

for ticker in TICKERS:
    company, context, sections, source_context = _fetch_ticker_data(ticker)
    result = run_ticker(ticker, company, sections, source_context)
    all_results.append(result)

    print(f"\n{'='*72}", flush=True)
    print(f"  JUDGE FINDINGS — {result['ticker']}", flush=True)
    print(f"{'='*72}", flush=True)
    print(result["findings"], flush=True)
    s, u, i, t = result["supported"], result["unsupported"], result["inference"], result["total"]
    print(f"\n  [ {s} SUPPORTED  {u} UNSUPPORTED  {i} INFERENCE  —  {t} total claims ]", flush=True)


# ── Summary table ─────────────────────────────────────────────────────────────

W = 12
print(f"\n\n{'='*72}", flush=True)
print("  GROUNDING SUMMARY — Sonnet + constrained prompt  (10 tickers)", flush=True)
print(f"{'='*72}", flush=True)
print(f"  {'Ticker':<8}  {'Supported':>{W}}  {'Unsupported':>{W}}  {'Inference':>{W}}  {'Total':>6}", flush=True)
print(f"  {'-'*8}  {'-'*W}  {'-'*W}  {'-'*W}  {'-'*6}", flush=True)

agg = {k: 0 for k in ("supported", "unsupported", "inference", "total")}
for r in all_results:
    print(f"  {r['ticker']:<8}  {r['supported']:>{W}}  {r['unsupported']:>{W}}  {r['inference']:>{W}}  {r['total']:>6}", flush=True)
    for k in agg:
        agg[k] += r[k]

print(f"  {'-'*8}  {'-'*W}  {'-'*W}  {'-'*W}  {'-'*6}", flush=True)
print(f"  {'TOTAL':<8}  {agg['supported']:>{W}}  {agg['unsupported']:>{W}}  {agg['inference']:>{W}}  {agg['total']:>6}", flush=True)

total = max(agg["total"], 1)
print(f"\n  Grounding rate    (Supported / Total):   {agg['supported']  / total * 100:.0f}%", flush=True)
print(f"  Unsupported rate  (Unsupported / Total): {agg['unsupported'] / total * 100:.0f}%", flush=True)
print(flush=True)
