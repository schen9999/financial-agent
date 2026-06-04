import os
import json
import anthropic
from dotenv import load_dotenv
from agent.tools.stock import get_stock_data
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "get_stock_data",
        "description": "Fetches current stock price, key financials, and company info for a given ticker symbol.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol e.g. AAPL"}
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_company_news",
        "description": "Fetches the 5 most recent news articles about a company. Pass the full company name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "company_name": {"type": "string", "description": "Full company name e.g. Apple"}
            },
            "required": ["company_name"]
        }
    },
    {
        "name": "get_sec_filings",
        "description": "Downloads the most recent 10-K and 10-Q SEC filings for a given ticker.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol e.g. AAPL"}
            },
            "required": ["ticker"]
        }
    }
]

tool_functions = {
    "get_stock_data": lambda args: get_stock_data.invoke(args),
    "get_company_news": lambda args: get_company_news.invoke(args),
    "get_sec_filings": lambda args: get_sec_filings.invoke(args),
}

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


def run_research(ticker: str) -> str:
    """
    Main entry point. Takes a ticker symbol and returns
    a formatted investment brief.
    """
    messages = [
        {"role": "user", "content": f"Research the stock {ticker.upper()} and produce a full investment brief."}
    ]

    print(f"\nResearching {ticker.upper()}...\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )

        # Add assistant response to messages
        messages.append({"role": "assistant", "content": response.content})

        # If no tool calls, we have the final response
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Calling tool: {block.name} with {block.input}")
                func = tool_functions.get(block.name)
                if func:
                    result = func(block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return "Research could not be completed."