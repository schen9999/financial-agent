#!/usr/bin/env python3
"""MCP server exposing the Financial Research Agent's tools over the Model
Context Protocol (official `mcp` SDK / FastMCP).

Standalone and additive: it reuses the existing LangChain tools (no duplicated
logic) and touches nothing in the FastAPI app, the Streamlit UI, or the agent.
Run it on its own:

    python mcp_server.py                                 # stdio (Claude Desktop / Inspector)
    mcp dev mcp_server.py                                # launch the MCP Inspector over stdio
    MCP_TRANSPORT=streamable-http python mcp_server.py   # HTTP transport

stdout hygiene (spec compliance): on the stdio transport, stdout IS the JSON-RPC
channel, so any library print() to stdout would corrupt the protocol. Each tool
runs under redirect_stdout(sys.stderr); the transport captured the real stdout
once at startup, so tool/library prints (e.g. rag.py's "[rag] ..." lines, the
embedding-model load output) go to stderr while protocol frames are unaffected.

robustness: the reused tools have no request timeout of their own, so a
throttled / slow upstream API (yfinance, SEC, NewsAPI) would otherwise hang the
stdio server indefinitely. Each call is bounded at the wrapper layer by
MCP_TOOL_TIMEOUT and fails into the tools' existing {"error": ...} shape.
"""

# Windows event-loop fix -- must run BEFORE anything imports asyncio/anyio/mcp
# machinery, so the policy is in place before any loop is created. The default
# ProactorEventLoop makes native-extension HTTP backends hang when a tool runs in
# FastMCP's worker thread over the stdio transport -- notably yfinance's
# curl_cffi/libcurl and the torch/HuggingFace RAG stack. The SelectorEventLoop
# avoids it. Set at import time (not inside __main__) so `mcp dev` / `mcp run`,
# which import this module rather than executing __main__, get the fix too. No
# effect off Windows.
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import concurrent.futures
import os
from contextlib import redirect_stdout

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Existing tools, reused not reimplemented. These imports are light. The RAG
# tool is imported lazily inside its wrapper (see query_sec_filings): rag.py
# loads llama_index + Pinecone + a HuggingFace embedding model at import time,
# so deferring it keeps server startup fast and lets the server run without
# PINECONE_API_KEY until the RAG tool is actually called.
from agent.tools.stock import get_stock_data as _get_stock_data
from agent.tools.stock import get_price_history as _get_price_history
from agent.tools.news import get_company_news as _get_company_news
from agent.tools.sec import get_sec_filings as _get_sec_filings

load_dotenv()

# Bind address/port for the HTTP transports (streamable-http / sse). Defaults
# preserve the original behaviour (loopback:8000); the K8s deployment sets
# MCP_HOST=0.0.0.0 so the pod is reachable on its pod IP. Passed as constructor
# kwargs because this mcp SDK version does not read FASTMCP_* env vars.
mcp = FastMCP(
    "financial-research-agent",
    host=os.getenv("MCP_HOST", "127.0.0.1"),
    port=int(os.getenv("MCP_PORT", "8000")),
)

# Wrapper-layer call guard: wall-clock timeout + stdout->stderr redirect.
_TOOL_TIMEOUT = float(os.getenv("MCP_TOOL_TIMEOUT", "30"))
_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="mcp-tool")


def _guarded(fn, *args, **kwargs):
    """Run a blocking upstream tool call with the stdout redirect active and a
    wall-clock timeout. The reused tools have no request timeout of their own, so
    without this a throttled/slow upstream would hang the stdio server forever.
    On timeout we return the tools' existing {"error": ...} shape instead of
    hanging; the orphaned upstream thread is abandoned (it cannot be force-killed)
    but no longer blocks the MCP response. Additive: tool internals are untouched."""
    def _run():
        with redirect_stdout(sys.stderr):
            return fn(*args, **kwargs)

    future = _EXECUTOR.submit(_run)
    try:
        return future.result(timeout=_TOOL_TIMEOUT)
    except concurrent.futures.TimeoutError:
        return {"error": f"upstream tool call timed out after {int(_TOOL_TIMEOUT)}s"}


@mcp.tool()
def get_stock_data(ticker: str) -> dict:
    """Fetch current price, market cap, P/E ratio, revenue, margins, and company
    info for a stock ticker (e.g. "AAPL"). A quantitative financial snapshot."""
    return _guarded(_get_stock_data.invoke, {"ticker": ticker})


@mcp.tool()
def get_price_history(ticker: str) -> dict:
    """Fetch 12 months of daily closing prices for a ticker, with start/end price
    and percent change. Use this for price-trend context."""
    return _guarded(_get_price_history.invoke, {"ticker": ticker})


@mcp.tool()
def get_company_news(company_name: str) -> list:
    """Fetch the 5 most recent news articles about a company. Pass the full
    company name (e.g. "Apple"), not the ticker."""
    return _guarded(_get_company_news.invoke, {"company_name": company_name})


@mcp.tool()
def get_sec_filings(ticker: str) -> dict:
    """Fetch the most recent 10-K and 10-Q filing summaries from SEC EDGAR for a
    ticker symbol (e.g. "AAPL")."""
    return _guarded(_get_sec_filings.invoke, {"ticker": ticker})


@mcp.tool()
def query_sec_filings(ticker: str, question: str) -> str:
    """Answer a specific question about a company's SEC filings using RAG over
    the indexed 10-K / 10-Q text (Pinecone). Example: ticker="AAPL",
    question="What are the primary risk factors?"."""
    def _do():
        # Lazy import: rag.py loads llama_index + Pinecone + an embedding model
        # at import time. Importing here keeps server startup fast.
        from agent.tools.rag import query_sec_filing
        return query_sec_filing.invoke({"input": f"{ticker}: {question}"})

    return _guarded(_do)


if __name__ == "__main__":
    # Default stdio (Claude Desktop / Inspector); MCP_TRANSPORT can select
    # "streamable-http" or "sse" for HTTP deployment.
    mcp.run(transport=os.getenv("MCP_TRANSPORT", "stdio"))
