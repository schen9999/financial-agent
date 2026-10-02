"""Self-served small language model (SLM) for the slm-full arm and the live app.

Under SLM_FULL=true EVERY agent LLM call — sections, synthesis, SEC RAG
answering, the multi-agent planner and synthesis, the ReAct /ask agent — goes
to one OpenAI-compatible endpoint (llama.cpp's llama-server), chosen by
SLM_ENDPOINT=cpu|gpu. The grounding judge and the multi-agent critic stay on
Sonnet: they are evaluation, not harness. There is no hosted fallback: a
missing endpoint setting, an HTTP error or an unparseable structured output
raises; it never quietly reroutes to Anthropic.

Configuration (env; keys from a Secret, never a ConfigMap):
  SLM_FULL                 "true" routes everything here (default "false")
  SLM_ENDPOINT             "cpu" | "gpu"
  SLM_CPU_URL, SLM_GPU_URL base URLs (no /v1)
  SLM_CPU_API_KEY, SLM_GPU_API_KEY
  SLM_MODEL_NAME           served alias the endpoint must list on /v1/models
  SLM_ARTIFACT             weights identity recorded in provenance
  LOCAL_MODEL_THINKING     "off" (default) | "on" — sent per request as
                           chat_template_kwargs.enable_thinking
  SLM_TIMEOUT              per-request seconds (default 900; CPU decoding of
                           a 1.5k-token synthesis behind queued requests)

Sampling is sent in full on every request — llama-server applies its own
defaults to anything omitted (min_p 0.05 among them). Temperature mirrors the
hosted call each site replaces; top_p/top_k follow the Qwen3.6 model card;
every penalty and auxiliary sampler is sent at its neutral value.
"""
import json
import os
import time
from typing import Any

import requests
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, convert_to_openai_messages
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool

from agent import llm_ledger


class SLMConfigError(RuntimeError):
    """SLM routing is on but the endpoint is not fully configured."""


class SLMRequestError(RuntimeError):
    """The endpoint answered with an error, or not at all."""


class SLMParseError(RuntimeError):
    """A structured output failed to parse after its one retry."""


def slm_full_enabled() -> bool:
    return os.getenv("SLM_FULL", "false").strip().lower() == "true"


def thinking_enabled() -> bool:
    v = os.getenv("LOCAL_MODEL_THINKING", "off").strip().lower()
    if v not in ("on", "off"):
        raise SLMConfigError(f"LOCAL_MODEL_THINKING must be 'on' or 'off', got {v!r}")
    return v == "on"


ENDPOINTS = ("cpu", "gpu")


def endpoint() -> dict:
    """The configured endpoint, or SLMConfigError naming what is missing."""
    name = os.getenv("SLM_ENDPOINT", "").strip().lower()
    if name not in ENDPOINTS:
        raise SLMConfigError(f"SLM_FULL is on but SLM_ENDPOINT is {name!r}; "
                             f"expected one of {ENDPOINTS}")
    up = name.upper()
    cfg = {"name": f"slm-{name}",
           "url": os.getenv(f"SLM_{up}_URL", "").strip().rstrip("/"),
           "api_key": os.getenv(f"SLM_{up}_API_KEY", "").strip(),
           "model": os.getenv("SLM_MODEL_NAME", "").strip()}
    missing = [var for var, val in ((f"SLM_{up}_URL", cfg["url"]),
                                    (f"SLM_{up}_API_KEY", cfg["api_key"]),
                                    ("SLM_MODEL_NAME", cfg["model"])) if not val]
    if missing:
        raise SLMConfigError(f"SLM endpoint {name!r} is missing {', '.join(missing)} "
                             f"— refusing to run (no hosted fallback)")
    return cfg


# Per-call-site profile. temperature = the hosted call it replaces (Haiku
# sections 0.1, Sonnet synthesis 0.2, llama_index's Anthropic default 0.1
# for RAG, the Haiku planner and Sonnet ReAct agent at 0). max_tokens sized
# from the measured maxima of every committed hosted run (chars/4): sections
# <= ~331, synthesis <= ~1.9k, RAG answers <= ~646 tokens — about 2x headroom.
SITE_PROFILES = {
    "section":   {"temperature": 0.1, "max_tokens": 768},
    "synthesis": {"temperature": 0.2, "max_tokens": 4096},
    "rag":       {"temperature": 0.1, "max_tokens": 1024},
    "planner":   {"temperature": 0.0, "max_tokens": 1024},
    "react":     {"temperature": 0.0, "max_tokens": 1024},
}

# Shared by every site. Neutral values disable the sampler explicitly.
SAMPLING = {
    "top_p": 0.8, "top_k": 20, "min_p": 0.0,
    "presence_penalty": 0.0, "frequency_penalty": 0.0,
    "repeat_penalty": 1.0, "dry_multiplier": 0.0, "xtc_probability": 0.0,
    "typical_p": 1.0, "top_n_sigma": -1.0,
}


def _profile_root(site: str) -> str:
    return site.split(":", 1)[0]


def request_params(site: str) -> dict:
    """Every sampling/generation parameter a request from `site` sends —
    also exactly what provenance records."""
    prof = SITE_PROFILES[_profile_root(site)]
    return {**prof, **SAMPLING,
            "chat_template_kwargs": {"enable_thinking": thinking_enabled()}}


def provenance_sampling() -> str:
    return json.dumps({s: request_params(s) for s in SITE_PROFILES}, sort_keys=True)


def _timeout() -> float:
    try:
        return float(os.getenv("SLM_TIMEOUT", "900"))
    except ValueError:
        return 900.0


def chat_completion(site: str, messages: list[dict], *, tools: list | None = None,
                    response_format: dict | None = None, retry: bool = False) -> dict:
    """POST one non-streaming /v1/chat/completions request; return the JSON.
    Non-streaming and unpooled on purpose: llama-server closes streamed
    keep-alive sockets after [DONE], which loses requests on reuse."""
    cfg = endpoint()
    body = {"model": cfg["model"], "messages": messages, **request_params(site)}
    if tools:
        body["tools"] = tools
    if response_format:
        body["response_format"] = response_format
    t0 = time.perf_counter()
    try:
        r = requests.post(f"{cfg['url']}/v1/chat/completions", json=body,
                          headers={"Authorization": f"Bearer {cfg['api_key']}"},
                          timeout=_timeout())
    except requests.RequestException as e:
        llm_ledger.record(site, cfg["name"], cfg["model"], latency_s=time.perf_counter() - t0,
                          max_tokens=body["max_tokens"], retry=retry,
                          error=type(e).__name__)
        raise SLMRequestError(f"{cfg['name']} request failed: {type(e).__name__}: {e}") from e
    if r.status_code != 200:
        llm_ledger.record(site, cfg["name"], cfg["model"], latency_s=time.perf_counter() - t0,
                          max_tokens=body["max_tokens"], retry=retry,
                          error=f"HTTP {r.status_code}")
        raise SLMRequestError(f"{cfg['name']} HTTP {r.status_code}: {r.text[:300]}")
    data = r.json()
    choice = data["choices"][0]
    usage = data.get("usage") or {}
    llm_ledger.record(site, cfg["name"], data.get("model") or cfg["model"],
                      prompt_tokens=usage.get("prompt_tokens"),
                      completion_tokens=usage.get("completion_tokens"),
                      latency_s=time.perf_counter() - t0,
                      finish_reason=choice.get("finish_reason"),
                      text=choice["message"].get("content") or "",
                      max_tokens=body["max_tokens"], retry=retry)
    return data


# ── LangChain chat model (sections, synthesis, ReAct with tools) ────────────

class SLMChatModel(BaseChatModel):
    """BaseChatModel over chat_completion, so it drops in wherever the agent
    uses ChatAnthropic: `.invoke(messages).content`, `.stream`, and
    `bind_tools` for LangGraph's create_react_agent."""

    site: str

    @property
    def _llm_type(self) -> str:
        return "slm-openai-compatible"

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        return self.bind(tools=[convert_to_openai_tool(t) for t in tools], **kwargs)

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None,
                  tools: list | None = None, ledger_retry: bool = False,
                  **kwargs: Any) -> ChatResult:
        data = chat_completion(self.site, convert_to_openai_messages(messages),
                               tools=tools, retry=ledger_retry)
        choice = data["choices"][0]
        msg = choice["message"]
        tool_calls, invalid = [], []
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
                if not isinstance(args, dict):
                    raise ValueError("arguments is not a JSON object")
                tool_calls.append({"name": fn.get("name", ""), "args": args,
                                   "id": tc.get("id"), "type": "tool_call"})
            except ValueError as e:
                invalid.append({"name": fn.get("name"), "args": fn.get("arguments"),
                                "id": tc.get("id"), "error": str(e),
                                "type": "invalid_tool_call"})
        if invalid:
            llm_ledger.flag_last(self.site, parse_failure=True)
        usage = data.get("usage") or {}
        ai = AIMessage(
            content=msg.get("content") or "",
            tool_calls=tool_calls, invalid_tool_calls=invalid,
            usage_metadata={"input_tokens": usage.get("prompt_tokens") or 0,
                            "output_tokens": usage.get("completion_tokens") or 0,
                            "total_tokens": usage.get("total_tokens") or 0},
            response_metadata={"finish_reason": choice.get("finish_reason"),
                               "model_name": data.get("model")},
        )
        return ChatResult(generations=[ChatGeneration(message=ai)])


def structured(site: str, messages: list[dict], model_cls):
    """JSON-schema-constrained call parsed into pydantic `model_cls`. One
    retry on a parse failure, then SLMParseError — never a silent default."""
    schema = model_cls.model_json_schema()
    fmt = {"type": "json_schema",
           "json_schema": {"name": model_cls.__name__, "schema": schema}}
    last = None
    for attempt in range(2):
        data = chat_completion(site, messages, response_format=fmt, retry=attempt > 0)
        text = data["choices"][0]["message"].get("content") or ""
        try:
            return model_cls.model_validate_json(text)
        except ValueError as e:  # pydantic ValidationError subclasses ValueError
            llm_ledger.flag_last(site, parse_failure=True)
            last = e
    raise SLMParseError(f"{site}: structured output failed to parse twice: {last}")


def invoke_recorded(llm, site: str, messages, *, retry: bool = False):
    """`llm.invoke(messages)` with exactly one ledger record per call: the SLM
    client records itself; hosted (ChatAnthropic) and LocalChat calls are
    recorded here from the response. Observation only."""
    if isinstance(llm, SLMChatModel):
        return llm.invoke(messages, ledger_retry=retry)
    t0 = time.perf_counter()
    resp = llm.invoke(messages)
    ep = "local-model" if type(llm).__name__ == "LocalChat" else "anthropic"
    llm_ledger.record_response(site, ep, getattr(llm, "model", None), resp, t0, retry=retry)
    return resp


# ── llama_index LLM (the SEC RAG query engine's answer synthesis) ───────────

def llama_index_llm(site: str):
    """A llama_index LLM over chat_completion, passed per query to
    as_query_engine(llm=...) — the process-global Settings.llm (hosted Haiku)
    is never touched. Built lazily: llama_index imports are heavy."""
    from llama_index.core.base.llms.types import (ChatMessage, ChatResponse,
                                                  CompletionResponse, LLMMetadata,
                                                  MessageRole)
    from llama_index.core.llms.callbacks import llm_chat_callback, llm_completion_callback
    from llama_index.core.llms.custom import CustomLLM

    max_tokens = SITE_PROFILES["rag"]["max_tokens"]

    class _SLMLlamaIndex(CustomLLM):
        site_name: str = site

        @property
        def metadata(self) -> LLMMetadata:
            # context_window: the per-request budget the endpoints are
            # deployed with (k8s/llamacpp, --ctx-size shared by the slots).
            return LLMMetadata(context_window=int(os.getenv("SLM_CONTEXT_WINDOW", "32768")),
                               num_output=max_tokens, is_chat_model=True,
                               model_name=os.getenv("SLM_MODEL_NAME", "slm"))

        @llm_chat_callback()
        def chat(self, messages, **kwargs) -> ChatResponse:
            data = chat_completion(self.site_name, [
                {"role": m.role.value, "content": m.content or ""} for m in messages])
            text = data["choices"][0]["message"].get("content") or ""
            return ChatResponse(message=ChatMessage(role=MessageRole.ASSISTANT, content=text),
                                raw={"slm": True})

        @llm_completion_callback()
        def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
            data = chat_completion(self.site_name, [{"role": "user", "content": prompt}])
            return CompletionResponse(text=data["choices"][0]["message"].get("content") or "",
                                      raw={"slm": True})

        @llm_completion_callback()
        def stream_complete(self, prompt: str, formatted: bool = False, **kwargs):
            yield self.complete(prompt, formatted=formatted, **kwargs)

    return _SLMLlamaIndex()


# ── Endpoint facts for provenance (server-reported, not config claims) ──────

def server_facts(timeout: float = 30.0) -> dict:
    """/v1/models + /props as the server reports them; raises SystemExit if
    the endpoint does not serve SLM_MODEL_NAME (wrong model, or not ours)."""
    cfg = endpoint()
    h = {"Authorization": f"Bearer {cfg['api_key']}"}
    try:
        models = requests.get(f"{cfg['url']}/v1/models", headers=h, timeout=timeout)
        models.raise_for_status()
        props = requests.get(f"{cfg['url']}/props", headers=h, timeout=timeout)
        props.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"FATAL: {cfg['name']} at {cfg['url']} unreachable or "
                         f"rejected the key: {type(e).__name__}: {e}")
    data = models.json().get("data", [])
    ids = [m.get("id") for m in data]
    if cfg["model"] not in ids:
        raise SystemExit(f"FATAL: {cfg['name']} serves {ids}, expected "
                         f"SLM_MODEL_NAME={cfg['model']!r}")
    meta = next(m for m in data if m.get("id") == cfg["model"]).get("meta") or {}
    p = props.json()
    return {
        "slm_endpoint": cfg["name"], "slm_url": cfg["url"], "slm_served_name": cfg["model"],
        "slm_artifact": os.getenv("SLM_ARTIFACT", "unrecorded"),
        "slm_build": p.get("build_info"), "slm_model_path": p.get("model_path"),
        "slm_model_ftype": p.get("model_ftype"), "slm_total_slots": p.get("total_slots"),
        "slm_n_ctx": (p.get("default_generation_settings") or {}).get("n_ctx"),
        "slm_n_params": meta.get("n_params"), "slm_model_size_bytes": meta.get("size"),
        "slm_thinking": "on" if thinking_enabled() else "off",
        "slm_sampling": provenance_sampling(),
    }
