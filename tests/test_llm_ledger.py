"""agent/llm_ledger.py — per-call records, per-site summaries, loop detection."""
import threading
import time

import pytest

from agent import llm_ledger
from agent.llm_ledger import repetition_run


@pytest.fixture(autouse=True)
def clean():
    llm_ledger.drain()
    llm_ledger.enable(False)
    yield
    llm_ledger.drain()
    llm_ledger.enable(False)


def test_disabled_records_nothing():
    llm_ledger.record("section", "anthropic", "m", prompt_tokens=1)
    assert llm_ledger.drain() == []


def test_record_drain_summarize():
    llm_ledger.enable()
    llm_ledger.record("section", "slm-cpu", "q", prompt_tokens=100, completion_tokens=20,
                      latency_s=1.5, finish_reason="stop", text="fine")
    llm_ledger.record("section", "slm-cpu", "q", prompt_tokens=90, completion_tokens=768,
                      latency_s=4.0, finish_reason="length")
    llm_ledger.record("synthesis", "slm-cpu", "q", latency_s=2.0, error="Timeout")
    recs = llm_ledger.drain()
    assert llm_ledger.drain() == []
    s = llm_ledger.summarize(recs)
    assert s["endpoints"] == ["slm-cpu"]
    assert s["total"]["calls"] == 3 and s["total"]["errors"] == 1
    sec = s["by_site"]["section"]
    assert (sec["prompt_tokens"], sec["completion_tokens"], sec["truncated"]) == (190, 788, 1)
    assert sec["latency_s_total"] == 5.5 and sec["latency_s_max"] == 4.0
    assert s["by_site"]["synthesis"]["prompt_tokens_unrecorded"] == 1


class _Resp:
    def __init__(self, content, usage, meta):
        self.content, self.usage_metadata, self.response_metadata = content, usage, meta


def test_record_response_maps_anthropic_max_tokens_to_length():
    llm_ledger.enable()
    llm_ledger.record_response("synthesis", "anthropic", "claude-sonnet-4-6",
                               _Resp("x", {"input_tokens": 10, "output_tokens": 5},
                                     {"stop_reason": "max_tokens"}), time.perf_counter())
    (r,) = llm_ledger.drain()
    assert (r["prompt_tokens"], r["completion_tokens"], r["truncated"]) == (10, 5, True)


def test_record_response_without_usage():
    llm_ledger.enable()
    llm_ledger.record_response("section", "local-model", "financial-lora",
                               type("R", (), {"content": "ok"})(), time.perf_counter())
    (r,) = llm_ledger.drain()
    assert r["prompt_tokens"] is None and r["finish_reason"] is None


def test_site_is_thread_local():
    seen = {}

    def worker(name):
        with llm_ledger.site(name):
            time.sleep(0.01)
            seen[name] = llm_ledger.current_site()

    ts = [threading.Thread(target=worker, args=(n,)) for n in ("rag:highlights", "rag:risks")]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert seen == {"rag:highlights": "rag:highlights", "rag:risks": "rag:risks"}
    assert llm_ledger.current_site() == "unknown"


def test_repetition_run_detects_loops():
    # Shape of a real loop (v924f-style): one sentence restated back to back.
    s = "Over the past year it reported a net loss of $5.4 billion compared to a prior loss. "
    assert repetition_run("Summary first. " + s * 3)
    assert not repetition_run("Summary first. " + s * 2)  # twice is not a loop


def test_repetition_run_ignores_normal_lists():
    text = ("### Risk Factors\n- **Competition:** rivals may cut prices.\n"
            "- **Regulation:** new rules may raise costs.\n"
            "- **Supply chain:** suppliers may fail to deliver parts.\n")
    assert not repetition_run(text)
    assert not repetition_run("short")


def test_repeat_run_flag_recorded():
    llm_ledger.enable()
    loop = "the margin trend should be watched closely by investors " * 4
    llm_ledger.record("synthesis", "slm-gpu", "q", text=loop, finish_reason="stop")
    (r,) = llm_ledger.drain()
    assert r["repeat_run"] and not r["truncated"]
