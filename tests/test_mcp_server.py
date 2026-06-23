"""Tests for the MCP server (mcp_server.py).

These drive a REAL in-memory MCP client/server session through the official SDK
(create_connected_server_and_client_session), so the protocol path is what's
exercised: tools are listed with their JSON schemas and calls go over the
session and come back as MCP content, not the wrapper functions called directly.
Network is mocked at the tool boundary, so the tests are offline and fast.
"""
import sys
import os
import json
import time
import types
from unittest.mock import patch, MagicMock, call

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import anyio
from mcp.shared.memory import create_connected_server_and_client_session as connect

import mcp_server

EXPECTED_TOOLS = {
    "get_stock_data": ["ticker"],
    "get_price_history": ["ticker"],
    "get_company_news": ["company_name"],
    "get_sec_filings": ["ticker"],
    "query_sec_filings": ["ticker", "question"],
}


def _run(async_fn):
    """Run an async test body on a fresh event loop (no pytest-asyncio needed)."""
    anyio.run(async_fn)


# ── Tool registration + schemas ──────────────────────────────────────────────────

def test_lists_all_tools_with_schemas():
    async def body():
        async with connect(mcp_server.mcp) as session:
            result = await session.list_tools()
            tools = {t.name: t for t in result.tools}

            assert set(tools) == set(EXPECTED_TOOLS), "unexpected tool set"
            for name, required in EXPECTED_TOOLS.items():
                t = tools[name]
                assert t.description, f"{name} has no description"
                props = t.inputSchema.get("properties", {})
                assert set(required) <= set(props), f"{name} missing params {required}"
                assert set(t.inputSchema.get("required", [])) == set(required)
    _run(body)


# ── Live protocol round-trips (network mocked) ───────────────────────────────────

def test_get_stock_data_roundtrip():
    """A dict-returning tool round-trips as JSON content over the protocol."""
    payload = {"ticker": "AAPL", "current_price": 123.45, "pe_ratio": 30.1}

    async def body():
        async with connect(mcp_server.mcp) as session:
            # StructuredTool is a frozen pydantic model, so replace the module
            # reference rather than patching the instance method.
            with patch.object(mcp_server, "_get_stock_data",
                              MagicMock(invoke=MagicMock(return_value=payload))) as m:
                result = await session.call_tool("get_stock_data", {"ticker": "AAPL"})

            assert result.isError is False
            assert json.loads(result.content[0].text) == payload
            m.invoke.assert_called_once_with({"ticker": "AAPL"})
    _run(body)


def test_get_company_news_roundtrip():
    """A list-returning tool round-trips; each item is its own content block."""
    articles = [{"title": "A"}, {"title": "B"}]

    async def body():
        async with connect(mcp_server.mcp) as session:
            with patch.object(mcp_server, "_get_company_news",
                              MagicMock(invoke=MagicMock(return_value=articles))):
                result = await session.call_tool("get_company_news", {"company_name": "Apple"})

            assert result.isError is False
            items = [json.loads(c.text) for c in result.content]
            assert items == articles
    _run(body)


def test_query_sec_filings_lazy_import_and_arg_assembly():
    """The RAG tool is imported lazily inside the wrapper; the (ticker, question)
    args are assembled into the 'TICKER: question' string the underlying tool
    expects, and the result round-trips as text."""
    stub_tool = MagicMock()
    stub_tool.invoke = MagicMock(return_value="[From Pinecone cache] risk factors ...")
    fake_rag = types.ModuleType("agent.tools.rag")
    fake_rag.query_sec_filing = stub_tool

    async def body():
        async with connect(mcp_server.mcp) as session:
            # Inject the stub so the wrapper's `from agent.tools.rag import ...`
            # resolves to it (proves the lazy-import path without loading the
            # real RAG stack / HF model).
            with patch.dict(sys.modules, {"agent.tools.rag": fake_rag}):
                result = await session.call_tool(
                    "query_sec_filings", {"ticker": "AAPL", "question": "What are the risks?"})

            assert result.isError is False
            assert "risk factors" in result.content[0].text
            stub_tool.invoke.assert_called_once_with({"input": "AAPL: What are the risks?"})
    _run(body)


def test_tool_timeout_returns_error_not_hang():
    """A slow/throttled upstream call is bounded by MCP_TOOL_TIMEOUT at the
    wrapper layer and returns the {'error': ...} shape instead of hanging the
    server. (The reused tools have no request timeout of their own.)"""
    slow = MagicMock(invoke=MagicMock(side_effect=lambda *a, **k: time.sleep(1.5) or {"x": 1}))

    async def body():
        async with connect(mcp_server.mcp) as session:
            with patch.object(mcp_server, "_TOOL_TIMEOUT", 0.3), \
                 patch.object(mcp_server, "_get_stock_data", slow):
                result = await session.call_tool("get_stock_data", {"ticker": "AAPL"})

            assert result.isError is False
            data = json.loads(result.content[0].text)
            assert "error" in data and "timed out" in data["error"].lower()
    _run(body)


def test_tool_error_payload_roundtrips_without_protocol_error():
    """A tool returning an {'error': ...} dict is a normal result, not a
    protocol-level error (matches the existing tools' graceful failure mode)."""
    err = {"error": "Failed to fetch stock data for ZZZZ"}

    async def body():
        async with connect(mcp_server.mcp) as session:
            with patch.object(mcp_server, "_get_stock_data",
                              MagicMock(invoke=MagicMock(return_value=err))):
                result = await session.call_tool("get_stock_data", {"ticker": "ZZZZ"})

            assert result.isError is False
            assert json.loads(result.content[0].text) == err
    _run(body)
