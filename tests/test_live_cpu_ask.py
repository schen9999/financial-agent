"""scripts/live_cpu_ask.py: the route check, the hosted-call guard, and one
whole ask through the real ReAct graph and SLMChatModel against a stubbed
CPU endpoint (no network, no Anthropic credit)."""
import json

import anthropic
import pytest
from anthropic._base_client import AsyncAPIClient, SyncAPIClient
from langchain_core.tools import tool

from agent import llm_ledger
from agent.tools import news, rag, sec, slm, stock
from scripts import live_cpu_ask as lca

CFG = {"SLM_FULL": "true", "SLM_ENDPOINT": "cpu", "SLM_CPU_URL": "http://slm-cpu:8080",
       "SLM_CPU_API_KEY": "k-cpu", "SLM_MODEL_NAME": "qwen3.6-35b-a3b-q4km"}


@pytest.fixture
def cpu_env(monkeypatch):
    for k, v in CFG.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("SLM_GPU_URL", raising=False)
    monkeypatch.delenv("SLM_GPU_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_MODEL_THINKING", raising=False)
    # block_hosted() patches these class attributes; monkeypatch restores them
    monkeypatch.setattr(SyncAPIClient, "request", SyncAPIClient.request)
    monkeypatch.setattr(AsyncAPIClient, "request", AsyncAPIClient.request)
    llm_ledger.drain()
    yield
    llm_ledger.enable(False)
    llm_ledger.drain()


@pytest.mark.parametrize("env,needle", [
    ({"SLM_FULL": "false"}, "SLM_FULL is not true"),
    ({"SLM_ENDPOINT": "gpu"}, "not 'cpu'"),
    ({"SLM_GPU_URL": "http://node2:30880"}, "SLM_GPU_URL is set"),
    ({"SLM_GPU_API_KEY": "k"}, "SLM_GPU_API_KEY is set"),
])
def test_check_route_refuses_anything_but_cpu_only(cpu_env, monkeypatch, env, needle):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    with pytest.raises(SystemExit, match=needle):
        lca.check_route()


def test_check_route_passes_on_cpu_only(cpu_env):
    lca.check_route()


def test_block_hosted_raises_and_counts(cpu_env):
    attempts = lca.block_hosted()
    client = anthropic.Anthropic(api_key="not-a-key")
    with pytest.raises(lca.HostedCallBlocked):
        client.messages.create(model="claude-sonnet-4-6", max_tokens=5,
                               messages=[{"role": "user", "content": "hi"}])
    assert attempts["n"] == 1


class _Resp:
    status_code = 200

    def __init__(self, body):
        self._body, self.text = body, json.dumps(body)

    def json(self):
        return self._body


def _tool_call(name, args, cid):
    return {"id": cid, "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}


def _completion(content="", tool_calls=None):
    msg = {"role": "assistant", "content": content}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return {"model": CFG["SLM_MODEL_NAME"],
            "choices": [{"message": msg, "finish_reason": "tool_calls" if tool_calls else "stop"}],
            "usage": {"prompt_tokens": 2000, "completion_tokens": 40, "total_tokens": 2040}}


@pytest.fixture
def stub_endpoint(cpu_env, monkeypatch):
    queue = [
        _completion(tool_calls=[_tool_call("get_sec_filings", {"ticker": "V"}, "a")]),
        _completion(tool_calls=[_tool_call("query_sec_filing", {"input": "V: competition"}, "b")]),
        _completion(content="Visa filed its 10-K on 2025-11-13; it names Mastercard and others."),
    ]
    urls = []

    def post(url, json=None, headers=None, timeout=None):
        urls.append(url)
        return _Resp(queue.pop(0))

    monkeypatch.setattr(slm.requests, "post", post)

    @tool
    def get_sec_filings(ticker: str) -> str:
        """Latest 10-K and 10-Q filing summaries from EDGAR."""
        return "10-K filed 2025-11-13"

    @tool
    def query_sec_filing(input: str) -> str:
        """RAG search over SEC filings. Input 'TICKER: question'."""
        return "Competitors include Mastercard, American Express."

    @tool
    def get_stock_data(ticker: str) -> str:
        """Stock data."""
        raise AssertionError("not expected")

    @tool
    def get_company_news(company_name: str) -> str:
        """News."""
        raise AssertionError("not expected")

    monkeypatch.setattr(sec, "get_sec_filings", get_sec_filings)
    monkeypatch.setattr(rag, "query_sec_filing", query_sec_filing)
    monkeypatch.setattr(stock, "get_stock_data", get_stock_data)
    monkeypatch.setattr(news, "get_company_news", get_company_news)
    monkeypatch.setattr(slm, "server_facts", lambda: {
        "slm_endpoint": "slm-cpu", "slm_served_name": CFG["SLM_MODEL_NAME"], "slm_build": "b11347"})
    return urls


def test_whole_ask_on_the_stubbed_cpu_endpoint(stub_endpoint):
    lines = []
    attempts = lca.block_hosted()
    res = lca.run("V", lca.QUESTIONS[0][1], out=lines.append)
    assert res["tools"] == ["get_sec_filings", "query_sec_filing"]
    assert res["answer"].startswith("Visa filed")
    assert res["endpoints"] == ["slm-cpu"] and res["aliases"] == [CFG["SLM_MODEL_NAME"]]
    assert len(res["calls"]) == 3
    assert all(u == "http://slm-cpu:8080/v1/chat/completions" for u in stub_endpoint)
    text = "\n".join(lines)
    assert "tool call   get_sec_filings" in text and "tool result query_sec_filing" in text
    assert "served alias qwen3.6-35b-a3b-q4km" in text
    ok, line = lca.verdict(res, attempts["n"])
    assert ok and line.startswith("LIVE CPU ASK: OK") and "not a citable run" in line


def test_verdict_fails_on_one_tool_or_a_hosted_attempt():
    res = {"answer": "x", "tools": ["get_sec_filings"], "endpoints": ["slm-cpu"], "calls": [],
           "wall_s": 1.0, "aliases": []}
    assert not lca.verdict(res, 0)[0]
    res["tools"] = ["get_sec_filings", "query_sec_filing"]
    assert lca.verdict(res, 0)[0]
    assert not lca.verdict(res, 1)[0]
    res["endpoints"] = ["slm-cpu", "slm-gpu"]
    assert not lca.verdict(res, 0)[0]


def test_questions_each_need_two_tools():
    assert len(lca.QUESTIONS) == 3
    assert all(len(set(q[2])) == 2 for q in lca.QUESTIONS)
    assert "get_stock_data" not in lca.QUESTIONS[0][2]  # the default stays off Yahoo
