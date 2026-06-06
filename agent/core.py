import os
import json
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


def run_research(ticker: str) -> str:
    """
    Fetches stock, news, and SEC data in parallel, then makes a single
    LLM call to synthesize the investment brief. Much faster than a
    ReAct agent loop which makes 5-8 sequential LLM round-trips.
    """
    cached = get_cached_response(ticker)
    if cached:
        return cached["result"]

    print(f"\nResearching {ticker.upper()}...\n")

    # Step 1: stock data first — needed to get the proper company name for news search
    stock_data = get_stock_data.invoke({"ticker": ticker})
    company_name = stock_data.get("company_name", ticker)

    # Step 2: news and SEC fetched in parallel — they're independent of each other
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_news = executor.submit(get_company_news.invoke, {"company_name": company_name})
        f_sec = executor.submit(get_sec_filings.invoke, {"ticker": ticker})
        news_data = f_news.result()
        sec_data = f_sec.result()

    # Step 3: single LLM synthesis call with all gathered data
    prompt = (
        f"Research {ticker.upper()} and write a full investment brief using this data:\n\n"
        f"## Stock Data\n{json.dumps(stock_data, indent=2)}\n\n"
        f"## Recent News\n{json.dumps(news_data, indent=2)}\n\n"
        f"## SEC Filings\n{json.dumps(sec_data, indent=2)}"
    )

    response = _llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    brief = response.content

    set_cached_response(ticker, brief)
    return brief
