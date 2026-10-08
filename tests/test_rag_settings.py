"""agent/tools/rag.py one-time llama_index setup: the two RAG queries of a
brief run in two threads and both reach _ensure_settings() before either
finishes (the embedding model takes seconds to load). Found on hosted smoke
x2cx8 (2026-10-03): each thread registered its own usage handler, so every
hosted RAG answer call was recorded twice in the ledger. Also: the hosted and
SLM arms share one RAG answer budget."""
import threading
import time

import pytest
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.instrumentation import get_dispatcher

from agent import llm_ledger
from agent.tools import rag, slm


class _SlowEmbedding(MockEmbedding):
    """Stands in for HuggingFaceEmbedding: slow to construct, no download."""

    def __init__(self, model_name=None, **kwargs):
        time.sleep(0.3)
        super().__init__(embed_dim=384)


def _usage_handlers():
    return [h for h in get_dispatcher().event_handlers if h.class_name() == "HostedRagUsage"]


@pytest.fixture
def fresh_settings(monkeypatch):
    disp = get_dispatcher()
    saved_handlers, saved = list(disp.event_handlers), (Settings._llm, Settings._embed_model)
    disp.event_handlers = [h for h in saved_handlers if h.class_name() != "HostedRagUsage"]
    monkeypatch.setattr(rag, "_settings_configured", False)
    monkeypatch.setattr(rag, "HuggingFaceEmbedding", _SlowEmbedding)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("SLM_FULL", "false")
    llm_ledger.drain()
    llm_ledger.enable()
    yield
    llm_ledger.enable(False)
    llm_ledger.drain()
    disp.event_handlers = saved_handlers
    Settings._llm, Settings._embed_model = saved


def _stub_anthropic(monkeypatch):
    """Stub only the SDK request; the llama_index Anthropic LLM is real."""
    from anthropic.types import Message, TextBlock, Usage
    requests = []

    def create(self, **kw):
        requests.append(kw)
        return Message(id="msg_x", type="message", role="assistant", model=kw["model"],
                       content=[TextBlock(type="text", text="The filing reports growth.")],
                       stop_reason="end_turn", stop_sequence=None,
                       usage=Usage(input_tokens=2650, output_tokens=300))

    monkeypatch.setattr(type(Settings.llm._client.messages), "create", create)
    return requests


def test_concurrent_callers_register_one_handler_one_record_per_api_call(fresh_settings, monkeypatch):
    start = threading.Barrier(2)

    def caller():
        start.wait()
        rag._ensure_settings()

    threads = [threading.Thread(target=caller) for _ in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(_usage_handlers()) == 1

    requests = _stub_anthropic(monkeypatch)
    index = VectorStoreIndex.from_documents([Document(text="Revenue grew. Margins held.")])
    with llm_ledger.site("rag:highlights"):
        rag._run_rag_query(index, "Summarize the key takeaways")
    records = llm_ledger.drain()
    assert len(requests) == 1
    assert [(r["site"], r["prompt_tokens"], r["completion_tokens"]) for r in records] == [
        ("rag:highlights", 2650, 300)]


def test_hosted_and_slm_rag_share_one_answer_budget(fresh_settings, monkeypatch):
    rag._ensure_settings()
    assert Settings.llm.max_tokens == slm.RAG_MAX_TOKENS == slm.SITE_PROFILES["rag"]["max_tokens"]
    assert Settings.llm.metadata.num_output == slm.llama_index_llm("rag").metadata.num_output

    requests = _stub_anthropic(monkeypatch)
    index = VectorStoreIndex.from_documents([Document(text="Revenue grew. Margins held.")])
    rag._run_rag_query(index, "Summarize the key takeaways")
    assert [r["max_tokens"] for r in requests] == [slm.RAG_MAX_TOKENS]
