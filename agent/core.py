import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from agent.tools.stock import get_stock_data
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings
from cache import get_cached_response, set_cached_response

load_dotenv()

SYSTEM_PROMPT = """You are a professional financial research analyst.
When given a stock ticker, you will use your tools to:
1. Fetch current stock data and key financials
2. Search for recent news about the company
3. Retrieve the latest SEC filings
4. Synthesize everything into a structured investment brief

Format your final response exactly like this:

## [Company Name] ([TICKER]) — Investment Brief

### Executive Summary
2-3 sentence overview of the company and current situation.

### Financial Health
Key metrics: price, market cap, P/E ratio, revenue, profit margin.
Brief assessment of financial strength.

### Recent Developments
Summarize the most relevant recent news and what it means for investors.

### SEC Filing Highlights
Key takeaways from the most recent annual or quarterly report.

### Risk Factors
2-3 primary risks an investor should be aware of.

### Outlook
1 paragraph forward-looking assessment based on all gathered data.

---
*This brief is for informational purposes only and does not constitute financial advice.*
"""

_llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.2,
    streaming=False,
)


def _build_prompt(ticker: str, stock_data: dict, news_data, sec_data: dict) -> str:
    return (
        f"Research {ticker.upper()} and write a full investment brief using this data:\n\n"
        f"## Stock Data\n{json.dumps(stock_data, indent=2)}\n\n"
        f"## Recent News\n{json.dumps(news_data, indent=2)}\n\n"
        f"## SEC Filings\n{json.dumps(sec_data, indent=2)}"
    )


def fetch_research_data(ticker: str) -> tuple[dict, list, dict]:
    """Fetch stock, news, and SEC data with per-stage timing logged to stdout."""
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
    """Generator: streams LLM response chunks and caches the full brief on completion."""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=_build_prompt(ticker, stock_data, news_data, sec_data)),
    ]

    t0 = time.perf_counter()
    full_response = []
    for chunk in _llm.stream(messages):
        if chunk.content:
            full_response.append(chunk.content)
            yield chunk.content

    brief = "".join(full_response)
    print(f"[timing:{ticker}] llm_stream={time.perf_counter() - t0:.2f}s  chars={len(brief)}")
    set_cached_response(ticker, brief)


def run_research(ticker: str) -> str:
    """Non-streaming path — used by FastAPI and Celery workers."""
    t_total = time.perf_counter()

    t0 = time.perf_counter()
    cached = get_cached_response(ticker)
    print(f"[timing:{ticker}] cache_check={time.perf_counter() - t0:.2f}s")
    if cached:
        return cached["result"]

    print(f"\nResearching {ticker.upper()}...\n")
    stock_data, news_data, sec_data = fetch_research_data(ticker)

    t_llm = time.perf_counter()
    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=_build_prompt(ticker, stock_data, news_data, sec_data)),
    ])
    print(f"[timing:{ticker}] llm_invoke={time.perf_counter() - t_llm:.2f}s")

    brief = response.content
    set_cached_response(ticker, brief)

    print(f"[timing:{ticker}] total={time.perf_counter() - t_total:.2f}s")
    return brief
