"""agent/tools/slm.py and SLM_FULL routing: every agent call goes to the
configured endpoint with every parameter explicit; no hosted fallback; the
legacy arms route exactly as before."""
import json
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import HumanMessage

from agent import llm_ledger
from agent.tools import slm
from eval.arms import apply_arm_env

CFG = {"SLM_FULL": "true", "SLM_ENDPOINT": "cpu", "SLM_CPU_URL": "http://slm-cpu:8080",
       "SLM_CPU_API_KEY": "k-cpu", "SLM_MODEL_NAME": "qwen3.6-35b-a3b-q4km"}

GOOD_BRIEF = ("## Apple Inc. (AAPL) — Investment Brief\n\n### Executive Summary\nApple sells phones.\n\n"
              "### Financial Health\nok\n\n### Outlook\nWatch margins.\n")


@pytest.fixture
def slm_env(monkeypatch):
    for k, v in CFG.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("LOCAL_MODEL_THINKING", raising=False)
    llm_ledger.drain()
    llm_ledger.enable()
    yield
    llm_ledger.enable(False)
    llm_ledger.drain()


class _Resp:
    def __init__(self, body, status=200):
        self.status_code, self._body, self.text = status, body, json.dumps(body)

    def json(self):
        return self._body


def _completion(content="ok", finish="stop", tool_calls=None, prompt=11, completion=7):
    msg = {"role": "assistant", "content": content}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return {"model": CFG["SLM_MODEL_NAME"], "choices": [{"message": msg, "finish_reason": finish}],
            "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                      "total_tokens": prompt + completion}}


@pytest.fixture
def fake_post(monkeypatch):
    calls, queue = [], []

    def post(url, json=None, headers=None, timeout=None):
        calls.append({"url": url, "json": json, "headers": headers, "timeout": timeout})
        item = queue.pop(0) if queue else _completion()
        return item if isinstance(item, _Resp) else _Resp(item)

    monkeypatch.setattr(slm.requests, "post", post)
    return calls, queue


# ── endpoint config ──────────────────────────────────────────────────────────

def test_endpoint_requires_every_setting(slm_env, monkeypatch):
    monkeypatch.delenv("SLM_CPU_API_KEY")
    with pytest.raises(slm.SLMConfigError, match="SLM_CPU_API_KEY"):
        slm.endpoint()
    monkeypatch.setenv("SLM_ENDPOINT", "tpu")
    with pytest.raises(slm.SLMConfigError, match="SLM_ENDPOINT"):
        slm.endpoint()


def test_per_endpoint_model_name_overrides(slm_env, monkeypatch):
    assert slm.endpoint()["model"] == CFG["SLM_MODEL_NAME"]
    monkeypatch.setenv("SLM_CPU_MODEL_NAME", "qwen3.6-35b-a3b-q4km-hybrid-ncmoe4")
    assert slm.endpoint()["model"] == "qwen3.6-35b-a3b-q4km-hybrid-ncmoe4"


def test_thinking_value_validated(slm_env, monkeypatch):
    monkeypatch.setenv("LOCAL_MODEL_THINKING", "maybe")
    with pytest.raises(slm.SLMConfigError):
        slm.thinking_enabled()


# ── request payload ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("site,temp,max_tokens", [
    ("section:financial_health", 0.1, 768), ("synthesis", 0.2, 4096),
    ("rag:risks", 0.1, 1024), ("planner", 0.0, 1024), ("react", 0.0, 1024)])
def test_every_parameter_sent(slm_env, fake_post, site, temp, max_tokens):
    calls, _ = fake_post
    slm.chat_completion(site, [{"role": "user", "content": "hi"}])
    (c,) = calls
    body = c["json"]
    assert c["url"] == "http://slm-cpu:8080/v1/chat/completions"
    assert c["headers"] == {"Authorization": "Bearer k-cpu"}
    assert body["model"] == CFG["SLM_MODEL_NAME"]
    assert (body["temperature"], body["max_tokens"]) == (temp, max_tokens)
    for k, v in slm.SAMPLING.items():
        assert body[k] == v, k
    assert body["min_p"] == 0.0  # llama-server's own default is 0.05
    assert body["chat_template_kwargs"] == {"enable_thinking": False}


def test_thinking_on_is_sent_per_request(slm_env, fake_post, monkeypatch):
    monkeypatch.setenv("LOCAL_MODEL_THINKING", "on")
    slm.chat_completion("section:x", [{"role": "user", "content": "hi"}])
    assert fake_post[0][0]["json"]["chat_template_kwargs"] == {"enable_thinking": True}


def test_ledger_records_usage_and_truncation(slm_env, fake_post):
    fake_post[1].append(_completion(finish="length", completion=768))
    slm.chat_completion("section:risk_factors", [{"role": "user", "content": "hi"}])
    (r,) = llm_ledger.drain()
    assert (r["endpoint"], r["prompt_tokens"], r["completion_tokens"], r["truncated"]) == \
        ("slm-cpu", 11, 768, True)


def test_http_error_raises_and_is_recorded(slm_env, fake_post):
    fake_post[1].append(_Resp({"error": "boom"}, status=500))
    with pytest.raises(slm.SLMRequestError, match="HTTP 500"):
        slm.chat_completion("synthesis", [{"role": "user", "content": "hi"}])
    (r,) = llm_ledger.drain()
    assert r["error"] == "HTTP 500"


# ── chat model, tools, structured output ─────────────────────────────────────

def test_chat_model_parses_tool_calls(slm_env, fake_post):
    fake_post[1].append(_completion(content="", finish="tool_calls", tool_calls=[
        {"id": "a", "type": "function", "function": {"name": "get_stock_data", "arguments": '{"ticker":"AAPL"}'}},
        {"id": "b", "type": "function", "function": {"name": "get_company_news", "arguments": "{not json"}}]))
    ai = slm.SLMChatModel(site="react").invoke([HumanMessage("P/E?")])
    assert ai.tool_calls == [{"name": "get_stock_data", "args": {"ticker": "AAPL"}, "id": "a",
                              "type": "tool_call"}]
    assert ai.invalid_tool_calls[0]["name"] == "get_company_news"
    (r,) = llm_ledger.drain()
    assert r["parse_failure"] and r["finish_reason"] == "tool_calls"


def test_bind_tools_sends_openai_tool_schema(slm_env, fake_post):
    from langchain_core.tools import tool

    @tool
    def get_stock_data(ticker: str) -> dict:
        """Current price for a ticker."""
        return {}

    slm.SLMChatModel(site="react").bind_tools([get_stock_data]).invoke([HumanMessage("x")])
    (tool_spec,) = fake_post[0][0]["json"]["tools"]
    assert tool_spec["function"]["name"] == "get_stock_data"


def test_structured_retries_once_then_parses(slm_env, fake_post):
    from agent.graph import ResearchPlan
    fake_post[1].extend([_completion(content='{"highlights_query": "trunc'),
                         _completion(content=json.dumps({"highlights_query": "h", "risks_query": "r",
                                                         "coverage": [], "sub_questions": []}))])
    plan = slm.structured("planner", [{"role": "user", "content": "plan"}], ResearchPlan)
    assert plan.highlights_query == "h"
    first, second = llm_ledger.drain()
    assert first["parse_failure"] and not first["retry"]
    assert second["retry"] and not second["parse_failure"]
    assert fake_post[0][0]["json"]["response_format"]["type"] == "json_schema"


def test_structured_fails_visibly_after_retry(slm_env, fake_post):
    from agent.graph import ResearchPlan
    fake_post[1].extend([_completion(content="nope"), _completion(content="still nope")])
    with pytest.raises(slm.SLMParseError):
        slm.structured("planner", [{"role": "user", "content": "plan"}], ResearchPlan)
    assert [r["parse_failure"] for r in llm_ledger.drain()] == [True, True]


def test_slm_planner_schema_requires_every_field():
    from agent.graph import _RequiredResearchPlan
    schema = _RequiredResearchPlan.model_json_schema()
    assert schema["required"] == ["coverage", "highlights_query", "risks_query", "sub_questions"]


def test_slm_planner_failure_is_not_swallowed(slm_env, fake_post):
    from agent import graph
    fake_post[1].extend([_completion(content="x"), _completion(content="y")])
    hosted = MagicMock()
    with patch.object(graph, "_get_planner_llm", return_value=hosted):
        with pytest.raises(slm.SLMParseError):
            graph._make_plan("Apple Inc.", "AAPL", "ctx")
    hosted.invoke.assert_not_called()


# ── routing: SLM_FULL sends everything to the endpoint, nothing hosted ───────

def test_slm_full_routes_sections_and_synthesis(slm_env, fake_post):
    from agent import core
    for heading, _ in core._SECTIONS:
        llm = core._section_llm(heading)
        assert isinstance(llm, slm.SLMChatModel) and llm.site.startswith("section:")
    assert isinstance(core.synthesis_llm(), slm.SLMChatModel)


def test_slm_full_never_touches_hosted(slm_env, fake_post):
    from agent import core
    boom = MagicMock(side_effect=AssertionError("hosted model called"))
    fake_post[1].extend([_completion(content="### Financial Health\nfine"), _completion(content=GOOD_BRIEF)])
    with patch.object(core, "_haiku", MagicMock(invoke=boom)), \
         patch.object(core, "_synthesis_llm", MagicMock(invoke=boom)):
        out = core._haiku_section("### Financial Health", "x", "Apple", "AAPL", "ctx")
        brief = core.synthesize("AAPL", "Apple", [out])
    assert brief == GOOD_BRIEF
    assert {r["endpoint"] for r in llm_ledger.drain()} == {"slm-cpu"}


def test_synthesis_guard_retries_then_fails(slm_env, fake_post):
    from agent import core
    fake_post[1].extend([_completion(content="no headings"), _completion(content="still none")])
    with pytest.raises(core.BriefFormatError, match="Executive Summary"):
        core.synthesize("AAPL", "Apple", ["s"])
    a, b = llm_ledger.drain()
    assert a["format_failure"] and b["format_failure"] and b["retry"]


def test_synthesis_guard_recovers_on_retry(slm_env, fake_post):
    from agent import core
    fake_post[1].extend([_completion(content="### Outlook only"), _completion(content=GOOD_BRIEF)])
    assert core.synthesize("AAPL", "Apple", ["s"]) == GOOD_BRIEF


def test_rag_llm_passed_per_query_only_under_slm(slm_env, monkeypatch):
    from agent.tools import rag
    seen = []

    class _Index:
        def as_query_engine(self, **kw):
            seen.append(kw)
            return MagicMock(query=MagicMock(return_value=MagicMock(source_nodes=[])))

    with llm_ledger.site("rag:highlights"):
        rag._run_rag_query(_Index(), "q")
    assert seen[0]["llm"].site_name == "rag:highlights"
    monkeypatch.setenv("SLM_FULL", "false")
    rag._run_rag_query(_Index(), "q")
    assert "llm" not in seen[1]


def test_react_route_and_model(slm_env, monkeypatch):
    from agent import react_agent
    captured = {}
    monkeypatch.setattr(react_agent, "create_react_agent",
                        lambda llm, tools, prompt: captured.setdefault("llm", llm))
    assert react_agent._route() == "slm-cpu"
    react_agent._build_graph("slm-cpu")
    assert isinstance(captured["llm"], slm.SLMChatModel) and captured["llm"].site == "react"
    monkeypatch.setenv("SLM_FULL", "false")
    assert react_agent._route() == "hosted"


# ── legacy arms: routing exactly as before ───────────────────────────────────

@pytest.mark.parametrize("arm", ["baseline", "context5", "rerank3", "rerank5", "local-model"])
def test_legacy_arms_route_as_before(arm, monkeypatch):
    from agent import core
    from agent.tools.local_model import LocalChat
    for k in CFG:
        monkeypatch.delenv(k, raising=False)
    apply_arm_env(arm)
    for heading, _ in core._SECTIONS:
        llm = core._section_llm(heading)
        if arm == "local-model" and heading in ("### Financial Health", "### Risk Factors"):
            assert isinstance(llm, LocalChat)
        else:
            assert llm is core._haiku
    assert core.synthesis_llm() is core._llm
    for k in ("RERANKING_ENABLED", "BASELINE_TOP_K", "RERANK_CANDIDATES", "RERANK_TOP_N",
              "USE_LOCAL_MODEL", "SLM_FULL", "SLM_ENDPOINT"):
        monkeypatch.delenv(k, raising=False)


def test_hosted_synthesis_unguarded_single_call(monkeypatch):
    """Outside SLM_FULL the app's synthesis is one hosted call, as before —
    no retry even if headings are missing (the harness opts in to the guard)."""
    from agent import core
    monkeypatch.delenv("SLM_FULL", raising=False)
    sonnet = MagicMock()
    sonnet.invoke.return_value = MagicMock(content="no headings")
    with patch.object(core, "_synthesis_llm", sonnet):
        assert core.synthesize("AAPL", "Apple", ["s"]) == "no headings"
    assert sonnet.invoke.call_count == 1


def test_cache_key_hosted_unchanged_slm_separate(monkeypatch):
    import cache
    monkeypatch.delenv("SLM_FULL", raising=False)
    assert cache._cache_key("aapl") == "research:AAPL"  # the documented exact key
    monkeypatch.setenv("SLM_FULL", "true")
    monkeypatch.setenv("SLM_ENDPOINT", "gpu")
    assert cache._cache_key("aapl") == "research:slm-gpu:AAPL"


def test_slm_brief_cached_under_its_own_key(monkeypatch):
    import cache
    store = {}
    fake = MagicMock()
    fake.setex.side_effect = lambda k, ttl, v: store.__setitem__(k, v)
    fake.get.side_effect = lambda k: store.get(k)
    monkeypatch.setattr(cache, "redis_client", fake)
    monkeypatch.delenv("BYPASS_CACHE", raising=False)
    monkeypatch.setenv("SLM_FULL", "true")
    monkeypatch.setenv("SLM_ENDPOINT", "cpu")
    cache.set_cached_response("AAPL", "slm brief")
    monkeypatch.setenv("SLM_FULL", "false")
    assert cache.get_cached_response("AAPL") is None  # hosted path never sees it
    assert list(store) == ["research:slm-cpu:AAPL"]
