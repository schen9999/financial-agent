#!/usr/bin/env python3
"""
compare_synthesis.py: three-way synthesis quality + latency comparison.

For each of 3 tickers, fetches data and generates the 4 Haiku sections
once, then runs the synthesis step (Exec Summary + Outlook) three ways:

  A) Sonnet       — original prompt
  B) Haiku        — original prompt
  C) Haiku tuned  — explicit prompt: requires specific figures, names
                    catalysts + risks, states investment thesis directly

Prints all three outputs in full so quality can be compared side by side.
Does not write to cache. This is the experiment behind the Sep 8, 2026
decision to move synthesis to Haiku with the tuned prompt (option C);
see docs/numbers-of-record.md, cost section. Run from repo root:
    python3 scripts/compare_synthesis.py
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from agent.core import (
    fetch_research_data,
    _parallel_sections,
    _synthesis_prompt,
    _trim_stock, _trim_news, _trim_sec, _data_context,
    _llm,    # Sonnet
    _haiku,  # Haiku
)

TICKERS = ["AAPL", "NVDA", "JPM"]
SEP = "=" * 80
DIV = "-" * 80


def _synthesis_prompt_haiku_tuned(ticker: str, company: str, sections: list[str]) -> str:
    """Explicit synthesis prompt engineered to push Haiku toward Sonnet-level depth.

    Differences from the original:
    - Executive Summary: 3 sentences with hard requirements — specific figures
      inline, investment thesis stated directly, one concrete catalyst and one
      concrete risk named.
    - Outlook: 2 paragraphs — first names 2-3 specific forward-looking catalysts
      with at least one metric; second names 2 risks and states a clear
      directional view with the condition that would change it.
    """
    section_block = "\n\n".join(sections)
    return f"""You are writing an investment brief for {company} ({ticker.upper()}). \
The four body sections below are already written — copy them verbatim into the output. \
Your only task is to write the Executive Summary and Outlook.

Pre-written sections (copy verbatim):
{section_block}

REQUIREMENTS — read carefully before writing:

### Executive Summary  (exactly 3 sentences, no more)
1. What the company does and its market position; cite at least two specific \
financial figures from the data (e.g. market cap, revenue, margin, P/E).
2. The investment thesis stated directly: what makes this stock worth owning \
or avoiding right now and why.
3. Name one concrete near-term catalyst and one concrete near-term risk that \
will determine whether the thesis plays out.

### Outlook  (exactly 2 paragraphs)
Paragraph 1 — Catalysts: name 2-3 specific forward-looking catalysts \
(product launches, macro tailwinds, business inflections, regulatory changes). \
Be concrete — no generic statements. Cite at least one metric or threshold \
that defines success (e.g. margin target, revenue run-rate, P/E level).
Paragraph 2 — Risks and stance: name 2 specific risks that could derail the \
thesis with concrete detail. Close with a clear directional view (buy / \
accumulate / hold / avoid) and state explicitly what condition or valuation \
level would change that view.

Output the full brief in this exact format — no extra sections, no preamble:

## {company} ({ticker.upper()}) — Investment Brief

### Executive Summary
[your 3 sentences here]

{section_block}

### Outlook
[your 2 paragraphs here]

---
*This brief is for informational purposes only and does not constitute financial advice.*"""


def synthesise(
    llm,
    ticker: str,
    company: str,
    sections: list[str],
    prompt_fn=None,
) -> tuple[str, float]:
    """Invoke llm with the given prompt function. Returns (output, elapsed_s)."""
    if prompt_fn is None:
        prompt_fn = _synthesis_prompt
    prompt = prompt_fn(ticker, company, sections)
    t0 = time.perf_counter()
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content, time.perf_counter() - t0


sonnet_times:      list[float] = []
haiku_times:       list[float] = []
haiku_tuned_times: list[float] = []

for ticker in TICKERS:
    print(f"\n{SEP}", flush=True)
    print(f"  {ticker}", flush=True)
    print(SEP, flush=True)

    # 1. Fetch data
    print(f"\n[{ticker}] Fetching data...", flush=True)
    stock_data, news_data, sec_data = fetch_research_data(ticker)
    stock   = _trim_stock(stock_data)
    news    = _trim_news(news_data)
    sec     = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)

    # 2. Generate 4 shared Haiku sections
    print(f"\n[{ticker}] Generating 4 Haiku sections (shared)...", flush=True)
    sections = _parallel_sections(ticker, company, context)
    print(f"[{ticker}] Sections ready.", flush=True)

    # 3a. Sonnet — original prompt
    print(f"\n[{ticker}] A) Sonnet (original prompt)...", flush=True)
    sonnet_out, sonnet_t = synthesise(_llm, ticker, company, sections)
    sonnet_times.append(sonnet_t)
    print(f"[{ticker}] done {sonnet_t:.2f}s  ({len(sonnet_out)} chars)", flush=True)

    # 3b. Haiku — original prompt
    print(f"[{ticker}] B) Haiku (original prompt)...", flush=True)
    haiku_out, haiku_t = synthesise(_haiku, ticker, company, sections)
    haiku_times.append(haiku_t)
    print(f"[{ticker}] done {haiku_t:.2f}s  ({len(haiku_out)} chars)", flush=True)

    # 3c. Haiku — tuned prompt
    print(f"[{ticker}] C) Haiku (tuned prompt)...", flush=True)
    haiku_tuned_out, haiku_tuned_t = synthesise(
        _haiku, ticker, company, sections, _synthesis_prompt_haiku_tuned
    )
    haiku_tuned_times.append(haiku_tuned_t)
    print(f"[{ticker}] done {haiku_tuned_t:.2f}s  ({len(haiku_tuned_out)} chars)", flush=True)

    # 4. Print three outputs
    print(f"\n{DIV}", flush=True)
    print(f"  A) SONNET  original  ({sonnet_t:.2f}s  {len(sonnet_out)} chars)", flush=True)
    print(DIV, flush=True)
    print(sonnet_out, flush=True)

    print(f"\n{DIV}", flush=True)
    print(f"  B) HAIKU   original  ({haiku_t:.2f}s  {len(haiku_out)} chars)", flush=True)
    print(DIV, flush=True)
    print(haiku_out, flush=True)

    print(f"\n{DIV}", flush=True)
    print(f"  C) HAIKU   tuned     ({haiku_tuned_t:.2f}s  {len(haiku_tuned_out)} chars)", flush=True)
    print(DIV, flush=True)
    print(haiku_tuned_out, flush=True)


# Summary
print(f"\n\n{SEP}", flush=True)
print("  SYNTHESIS LATENCY SUMMARY", flush=True)
print(SEP, flush=True)
print(f"  {'Variant':<22}  {'Mean':>8}  {'Min':>8}  {'Max':>8}", flush=True)
print(f"  {'-'*22}  {'-'*8}  {'-'*8}  {'-'*8}", flush=True)

variants = [
    ("Sonnet (original)",   sonnet_times),
    ("Haiku  (original)",   haiku_times),
    ("Haiku  (tuned)",      haiku_tuned_times),
]
for label, times in variants:
    mean = sum(times) / len(times)
    print(f"  {label:<22}  {mean:>7.2f}s  {min(times):>7.2f}s  {max(times):>7.2f}s", flush=True)

print(f"\n  Per-ticker breakdown:", flush=True)
print(f"  {'Ticker':<6}  {'Sonnet':>8}  {'Haiku':>8}  {'Haiku+':>8}  {'Son-Hku+':>10}", flush=True)
print(f"  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*10}", flush=True)
for ticker, st, ht, htt in zip(TICKERS, sonnet_times, haiku_times, haiku_tuned_times):
    print(f"  {ticker:<6}  {st:>7.2f}s  {ht:>7.2f}s  {htt:>7.2f}s  {st-htt:>+9.2f}s", flush=True)
print(flush=True)
