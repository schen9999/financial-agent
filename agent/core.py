import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from agent.tools.stock import get_stock_data
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings
from agent.tools.rag import query_sec_filing
from cache import get_cached_response, set_cached_response

load_dotenv()

tools = [get_stock_data, get_company_news, get_sec_filings, query_sec_filing]

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


def _build_graph():
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.2,
        streaming=False,
    )
    return create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)


# Build once at import time — reused across all run_research calls
_graph = _build_graph()


def run_research(ticker: str) -> str:
    """
    Main entry point. Takes a ticker symbol and returns
    a formatted investment brief using a LangGraph ReAct agent.
    Checks semantic cache first before calling the LLM.
    """
    # Check semantic cache first
    cached = get_cached_response(ticker)
    if cached:
        return cached["result"]

    # Cache miss — run the full agent
    print(f"\nResearching {ticker.upper()} with LangGraph...\n")

    result = _graph.invoke({
        "messages": [
            HumanMessage(content=f"Research the stock {ticker.upper()} and produce a full investment brief.")
        ]
    })

    # Extract final message
    messages = result.get("messages", [])
    for message in reversed(messages):
        if hasattr(message, "content") and isinstance(message.content, str) and len(message.content) > 100:
            # Store in semantic cache
            set_cached_response(ticker, message.content)
            return message.content

    return "Research could not be completed."