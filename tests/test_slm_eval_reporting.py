"""SLM eval reporting: the aggregate's LLM/failure/RAG-faithfulness/SLM_TRAFFIC
output, scripts/slm_traffic_proof.py verdicts, and eval/rag_faithfulness."""
import importlib.util
import json
import pathlib

import pytest

from agent import llm_ledger

_REPO = pathlib.Path(__file__).resolve().parents[1]


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, _REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


eval_aggregate = _load("eval_aggregate", "scripts/eval_aggregate.py")
proof = _load("slm_traffic_proof", "scripts/slm_traffic_proof.py")


def _summary(endpoint, calls=7, prompt=1000, compl=300, **flags):
    llm_ledger.enable()
    llm_ledger.drain()
    for i in range(calls):
        llm_ledger.record("section:x" if i else "synthesis", endpoint, "m",
                          prompt_tokens=prompt // calls, completion_tokens=compl // calls,
                          latency_s=1.0, finish_reason="stop", **(flags if i == 0 else {}))
    s = llm_ledger.summarize(llm_ledger.drain())
    llm_ledger.enable(False)
    return s


def _row(ticker, **extra):
    return {"ticker": ticker, "supported": 9, "unsupported": 1, "inference": 0, "total": 10,
            "retrieval_s": 1.0, "pipeline_s": 2.0, **extra}


def _aggregate(monkeypatch, tmp_path, rows, failures=(), skipped=()):
    f = tmp_path / "all.json"
    f.write_text(json.dumps([json.dumps({"results": rows, "skipped": list(skipped),
                                         "failures": list(failures)})]), encoding="utf-8")
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    captured = {}
    monkeypatch.setattr(eval_aggregate, "maybe_upload_artifacts",
                        lambda summary, results, skipped: captured.update(summary))
    monkeypatch.setattr(eval_aggregate.sys, "argv",
                        ["eval_aggregate.py", "--input", str(f), "--min-claims", "1",
                         "--max-unsupported-pct", "50"])
    try:
        eval_aggregate.main()
    except SystemExit:
        pass
    return captured


def test_llm_table_and_traffic_line(monkeypatch, tmp_path, capsys):
    rows = [_row("AAPL", llm=_summary("slm-cpu")), _row("NVDA", llm=_summary("slm-cpu"))]
    fail = {"ticker": "JPM", "arm": "slm-full-cpu", "kind": "format", "error": "x",
            "llm": _summary("slm-cpu", calls=2, prompt=200, compl=100, format_failure=True)}
    summary = _aggregate(monkeypatch, tmp_path, rows, [fail], ["JPM"])
    out = capsys.readouterr().out
    assert "LLM calls (agent) : 16 over 2 completed ticker(s) + 1 failed" in out
    assert "failures by kind  : format 1 (JPM)" in out
    (line,) = [ln for ln in out.splitlines() if "SLM_TRAFFIC" in ln]
    t = json.loads(line.split("SLM_TRAFFIC ", 1)[1])
    # failed tickers' calls reached the endpoint, so they are in the totals
    assert (t["endpoint"], t["calls"]) == ("slm-cpu", 16)
    assert t["prompt_tokens"] == 2 * (1000 // 7) * 7 + 200
    assert summary["llm"]["by_site"]["synthesis"]["format_failure"] == 1


def test_no_traffic_line_for_hosted(monkeypatch, tmp_path, capsys):
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", llm=_summary("anthropic"))])
    out = capsys.readouterr().out
    assert "SLM_TRAFFIC" not in out and "endpoints anthropic" in out


def test_rag_faithfulness_reported_separately(monkeypatch, tmp_path, capsys):
    rows = [_row("AAPL", rag_faithfulness={"highlights": {"supported": 8, "unsupported": 2, "total": 10},
                                           "risks": None})]
    summary = _aggregate(monkeypatch, tmp_path, rows)
    out = capsys.readouterr().out
    assert "RAG faithfulness  : 2/10 RAG-answer claims" in out and "UNVALIDATED" in out
    assert summary["rag_faithfulness"] == {"answers": 1, "supported": 8, "unsupported": 2, "claims": 10}
    assert summary["totals"]["unsupported"] == 1  # grounding totals untouched by it


def test_slm_provenance_lines(monkeypatch, tmp_path, capsys):
    prov = {"slm_endpoint": "slm-gpu", "slm_url": "http://n2:30880", "slm_served_name": "q",
            "slm_artifact": "ggml-org/Qwen3.6-35B-A3B-GGUF@baec3eb:Qwen3.6-35B-A3B-Q4_K_M.gguf",
            "slm_build": "b11347-5fc4f3c8c", "slm_model_path": "/models/x.gguf",
            "slm_model_ftype": "Q4_K - Medium", "slm_n_ctx": 32768, "slm_total_slots": 4,
            "slm_thinking": "off", "slm_sampling": "{}"}
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", slm=prov), _row("NVDA", slm={**prov, "slm_n_ctx": 8})])
    out = capsys.readouterr().out
    assert "slm server        : build b11347-5fc4f3c8c" in out
    assert "more than one SLM endpoint/config" in out


# ── traffic proof ────────────────────────────────────────────────────────────

METRICS = """# HELP llamacpp:prompt_tokens_total x
llamacpp:prompt_tokens_total {p}
llamacpp:prompt_tokens_cached_total {c}
llamacpp:tokens_predicted_total {t}
llamacpp:n_decode_total 5
llamacpp:requests_processing 0
"""


def _snap(p, c, t, build="b11347-5fc4f3c8c", path="/models/q.gguf"):
    return {"endpoint": "slm-cpu", "url": "u", "build": build, "model_path": path,
            "counters": proof.parse_metrics(METRICS.format(p=p, c=c, t=t))}


def _traffic(prompt, compl, errored=0):
    return {"endpoint": "slm-cpu", "calls": 3, "prompt_tokens": prompt, "completion_tokens": compl,
            "errored_calls": errored, "calls_without_usage": errored}


def test_proof_exact():
    v, _ = proof.verify(_snap(440, 416, 787), _snap(540, 516, 887), _traffic(200, 100))
    assert v == "EXACT"


def test_proof_server_saw_less_is_fail():
    v, lines = proof.verify(_snap(0, 0, 0), _snap(10, 0, 5), _traffic(200, 100))
    assert v == "FAIL" and any("FEWER" in ln for ln in lines)


def test_proof_extra_traffic_without_errors_is_fail():
    v, lines = proof.verify(_snap(0, 0, 0), _snap(300, 0, 150), _traffic(200, 100))
    assert v == "FAIL" and any("other traffic" in ln for ln in lines)


def test_proof_extra_from_errored_calls_is_lower_bound():
    v, _ = proof.verify(_snap(0, 0, 0), _snap(300, 0, 150), _traffic(200, 100, errored=1))
    assert v == "LOWER-BOUND"


def test_proof_restart_and_model_change_fail():
    assert proof.verify(_snap(500, 0, 500), _snap(10, 0, 5), _traffic(10, 5))[0] == "FAIL"
    assert proof.verify(_snap(0, 0, 0), _snap(200, 0, 100, path="/models/other.gguf"),
                        _traffic(200, 100))[0] == "FAIL"


def test_proof_requires_metrics_flag():
    with pytest.raises(SystemExit, match="--metrics"):
        proof.parse_metrics("llamacpp:requests_processing 0\n")


def test_parse_traffic_picks_endpoint():
    log = ('x\n  SLM_TRAFFIC {"endpoint": "slm-gpu", "calls": 1}\n'
           '  SLM_TRAFFIC {"endpoint": "slm-cpu", "calls": 2}\n')
    assert proof.parse_traffic(log, "slm-cpu")["calls"] == 2
    with pytest.raises(SystemExit, match="no SLM_TRAFFIC"):
        proof.parse_traffic("nothing", "slm-cpu")


# ── RAG faithfulness ─────────────────────────────────────────────────────────

def test_rag_faithfulness_grade(monkeypatch):
    from eval import rag_faithfulness as rf
    seen = {}

    def invoke(messages):
        seen["user"] = messages[1].content
        return type("R", (), {"content": 'CLAIM: "Revenue $391B"\nLABEL: SUPPORTED\nREASON: [1]\n'
                                         'CLAIM: "Margin 50%"\nLABEL: UNSUPPORTED\nREASON: absent'})()

    res = rf.grade(["Revenue was $391B."], "[From Pinecone cache] Revenue $391B; margin 50%.", invoke)
    assert (res["supported"], res["unsupported"], res["total"]) == (1, 1, 2)
    assert "[1] Revenue was $391B." in seen["user"]
    assert "[From Pinecone cache]" not in seen["user"]
    assert res["prompt_version"] == "rf-v1"


def test_rag_faithfulness_off_by_default(monkeypatch):
    from eval import rag_faithfulness as rf
    monkeypatch.delenv("EVAL_RAG_FAITHFULNESS", raising=False)
    assert not rf.enabled()
