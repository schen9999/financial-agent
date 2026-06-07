import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from agent.tools.stock import get_stock_data
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings
from agent.tools.rag import query_sec_filing
from cache import get_cached_response, set_cached_response

load_dotenv()

# Sonnet: executive summary + outlook — quality matters here
_llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.2,
    streaming=False,
)

# Haiku: parallel section generation — fast and cheap for data-heavy sections
_haiku = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.1,
    streaming=False,
)

_synthesis_llm = _llm
_synthesis_label = "sonnet"

_RAG_ENABLED = bool(os.getenv("PINECONE_API_KEY"))
_RAG_FAILURE_PREFIXES = ("RAG query failed", "Could not retrieve")


# --- #6: Input trimming — strip fields the LLM ignores ---

def _trim_stock(data: dict) -> dict:
    keep = {"ticker", "company_name", "current_price", "currency", "market_cap",
            "pe_ratio", "forward_pe", "week_52_high", "week_52_low",
            "revenue", "net_income", "profit_margin", "dividend_yield",
            "sector", "industry"}
    return {k: v for k, v in data.items() if k in keep and v is not None}


def _trim_news(data: list) -> list:
    if not isinstance(data, list):
        return data
    return [
        {"title": a.get("title"), "source": a.get("source"),
         "published_at": a.get("published_at"), "description": a.get("description")}
        for a in data if isinstance(a, dict) and "error" not in a
    ][:5]


def _trim_sec(data: dict) -> dict:
    trimmed = {}
    for form_type, filing in data.items():
        if isinstance(filing, dict) and "summary" in filing:
            trimmed[form_type] = {
                "form_type": filing.get("form_type"),
                "filing_date": filing.get("filing_date"),
                "summary": (filing.get("summary") or "")[:800],
            }
        else:
            trimmed[form_type] = filing
    return trimmed


def _data_context(stock: dict, news: list, sec: dict) -> str:
    return f"Stock: {json.dumps(stock)}\nNews: {json.dumps(news)}\nSEC: {json.dumps(sec)}"


def _rag_contexts(ticker: str) -> tuple[str | None, str | None]:
    """Run SEC highlights and risk-factor RAG queries concurrently.
    Returns (highlights_text, risks_text); either is None on failure or when RAG is disabled."""
    if not _RAG_ENABLED:
        return None, None
    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            f_highlights = executor.submit(
                query_sec_filing.invoke,
                f"{ticker}: Summarize the key takeaways from the latest 10-K and 10-Q"
            )
            f_risks = executor.submit(
                query_sec_filing.invoke,
                f"{ticker}: What are the primary risk factors disclosed?"
            )
            highlights = f_highlights.result()
            risks = f_risks.result()

        def _ok(result: str) -> str | None:
            if not result or any(result.startswith(p) for p in _RAG_FAILURE_PREFIXES):
                return None
            return result

        return _ok(highlights), _ok(risks)
    except Exception:
        return None, None


# --- #4: Parallel section generation with Haiku ---

_SECTIONS = [
    ("### Financial Health",
     "Key metrics: price, market cap, P/E ratio, revenue, profit margin. Brief financial assessment. 3-5 sentences."),
    ("### Recent Developments",
     "Summarize the most relevant news and what it means for investors. 3-5 sentences."),
    ("### SEC Filing Highlights",
     "Key takeaways from the most recent 10-K or 10-Q. 3-5 sentences."),
    ("### Risk Factors",
     "2-3 primary risks an investor should be aware of, as a bullet list."),
]


def _haiku_section(heading: str, instruction: str, company: str, ticker: str, context: str) -> str:
    prompt = (
        f"Write ONLY the '{heading}' section for a {company} ({ticker}) investment brief.\n"
        f"{instruction}\nStart with the markdown heading. Be concise.\n\nData:\n{context}"
    )
    return _haiku.invoke([HumanMessage(content=prompt)]).content


def _parallel_sections(ticker: str, company: str, context: str) -> list[str]:
    """Generate the 4 data-heavy sections concurrently using Haiku.
    SEC Filing Highlights and Risk Factors use RAG-grounded context when available,
    falling back to the raw data context if RAG is disabled or fails."""
    t_rag = time.perf_counter()
    rag_highlights, rag_risks = _rag_contexts(ticker)
    print(f"[timing:{ticker}] rag_sections={time.perf_counter() - t_rag:.2f}s")

    section_contexts = {
        "### Financial Health": context,
        "### Recent Developments": context,
        "### SEC Filing Highlights": rag_highlights or context,
        "### Risk Factors": rag_risks or context,
    }

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                _haiku_section, heading, instruction, company, ticker,
                section_contexts[heading]
            )
            for heading, instruction in _SECTIONS
        ]
        return [f.result() for f in futures]


def _synthesis_prompt(ticker: str, company: str, sections: list[str]) -> str:
    section_block = "\n\n".join(sections)
    return f"""Complete this investment brief for {company} ({ticker.upper()}) by writing the Executive Summary and Outlook. The four middle sections are already written below — include them verbatim.

Pre-written sections:
{section_block}

GROUNDING RULES — follow strictly:
- Cite a specific number ONLY if it appears explicitly in the pre-written sections above. Do NOT invent, estimate, or extrapolate any numeric figure.
- Never fabricate price targets, future revenue or run-rate projections, P/E targets, or numeric valuation thresholds of any kind.
- Write the Outlook as qualitative direction: name the key variables an investor should watch (e.g. "watch services-margin trend and China exposure") and describe what conditions would strengthen or weaken the thesis — without attaching invented numeric targets to any of them.

### Executive Summary  (2-3 sentences)
Sentence 1: What the company does and its market position; you may reference financial figures that appear explicitly in the pre-written sections.
Sentence 2: The current investment situation and why the stock is notable now.
Sentence 3: The single most important near-term variable that will shape the outcome.

### Outlook  (1 paragraph)
Describe the directional outlook — tailwinds, headwinds, and the key variables an investor should monitor. State a directional lean (e.g. cautiously constructive, neutral, cautious) and what would change that view. No price targets, revenue forecasts, or numeric valuation thresholds.

Write the full brief in this exact format:

## {company} ({ticker.upper()}) — Investment Brief

### Executive Summary
[your 2-3 sentences here]

{section_block}

### Outlook
[your 1 paragraph here]

---
*This brief is for informational purposes only and does not constitute financial advice.*"""


# --- Public API ---

def fetch_research_data(ticker: str) -> tuple[dict, list, dict]:
    """Fetch stock, news, and SEC data with per-stage timing."""
    t0 = time.perf_counter()
    stock_data = get_stock_data.invoke({"ticker": ticker})
    print(f"[timing:{ticker}] stock_data={time.perf_counter() - t0:.2f}s")

    company_name = stock_data.get("company_name", ticker)

    t1 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_news = executor.submit(get_company_news.invoke, {"company_name": company_name})
        f_sec = executor.submit(get_sec_filings.invoke, {"ticker": ticker})
        news_data = f_news.result()
        sec_data = f_sec.result()
    print(f"[timing:{ticker}] news+SEC(parallel)={time.perf_counter() - t1:.2f}s")

    return stock_data, news_data, sec_data


def stream_synthesis(ticker: str, stock_data: dict, news_data, sec_data: dict):
    """Generator: Haiku generates 4 sections in parallel; Sonnet writes exec summary +
    outlook with the pre-written sections in context. Caches the full brief on completion."""
    stock = _trim_stock(stock_data)
    news = _trim_news(news_data)
    sec = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)

    t0 = time.perf_counter()
    sections = _parallel_sections(ticker, company, context)
    print(f"[timing:{ticker}] haiku_sections(parallel)={time.perf_counter() - t0:.2f}s")

    t1 = time.perf_counter()
    full_response = []
    for chunk in _synthesis_llm.stream([HumanMessage(content=_synthesis_prompt(ticker, company, sections))]):
        if chunk.content:
            full_response.append(chunk.content)
            yield chunk.content

    brief = "".join(full_response)
    print(f"[timing:{ticker}] {_synthesis_label}_stream={time.perf_counter() - t1:.2f}s  chars={len(brief)}")
    print(f"[timing:{ticker}] total_llm={time.perf_counter() - t0:.2f}s")
    set_cached_response(ticker, brief)


def run_research(ticker: str) -> str:
    """Non-streaming path used by FastAPI and Celery workers."""
    t_total = time.perf_counter()

    t0 = time.perf_counter()
    cached = get_cached_response(ticker)
    print(f"[timing:{ticker}] cache_check={time.perf_counter() - t0:.2f}s")
    if cached:
        return cached["result"]

    print(f"\nResearching {ticker.upper()}...\n")
    stock_data, news_data, sec_data = fetch_research_data(ticker)

    stock = _trim_stock(stock_data)
    news = _trim_news(news_data)
    sec = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)

    t_sections = time.perf_counter()
    sections = _parallel_sections(ticker, company, context)
    print(f"[timing:{ticker}] haiku_sections(parallel)={time.perf_counter() - t_sections:.2f}s")

    t_llm = time.perf_counter()
    response = _synthesis_llm.invoke([HumanMessage(content=_synthesis_prompt(ticker, company, sections))])
    print(f"[timing:{ticker}] {_synthesis_label}_invoke={time.perf_counter() - t_llm:.2f}s")

    brief = response.content
    set_cached_response(ticker, brief)
    print(f"[timing:{ticker}] total={time.perf_counter() - t_total:.2f}s")
    return brief
