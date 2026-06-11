import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent

from agent.tracing import traceable

load_dotenv()

_SYSTEM_PROMPT = """You are a financial research assistant with access to real-time data and SEC filings.
You are given a stock ticker and a free-form question. Use the available tools to answer accurately.

Tool usage guide:
- get_stock_data(ticker): current price, market cap, P/E ratio, revenue, margins
- get_company_news(company_name): recent news — pass the full company name, not the ticker
- get_sec_filings(ticker): latest 10-K and 10-Q filing summaries from EDGAR
- query_sec_filing("TICKER: question"): RAG search over SEC filings for specific questions

Call only the tools needed. Be concise and cite the data source where relevant."""

# Built lazily on first call so importing this module stays cheap.
_graph = None


def _build_graph():
    from agent.tools.stock import get_stock_data
    from agent.tools.news import get_company_news
    from agent.tools.sec import get_sec_filings
    from agent.tools.rag import query_sec_filing

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0,
    )
    return create_react_agent(
        llm,
        tools=[get_stock_data, get_company_news, get_sec_filings, query_sec_filing],
        prompt=_SYSTEM_PROMPT,
    )


@traceable(run_type="chain", name="answer_question", tags=["follow_up"],
           metadata={"request_type": "follow_up", "model": "claude-sonnet-4-6"})
def answer_question(ticker: str, question: str) -> str:
    """Run the ReAct agent to answer a free-form question about a stock.
    The agent selects and calls whichever tools it needs, then returns a
    synthesised answer."""
    global _graph
    if _graph is None:
        _graph = _build_graph()

    result = _graph.invoke({
        "messages": [HumanMessage(content=f"Ticker: {ticker.upper()}. {question}")]
    })

    messages = result.get("messages", [])
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not getattr(msg, "tool_calls", None):
            if isinstance(msg.content, str) and msg.content.strip():
                return msg.content
    return "Could not generate an answer."
