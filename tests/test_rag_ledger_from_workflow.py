"""scripts/rag_ledger_from_workflow.py: per-call RAG tokens from a workflow
object, halving only rows that are provably the same call recorded twice."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import rag_ledger_from_workflow as rl  # noqa: E402


def _site(calls, prompt, completion, total, mx, truncated=0):
    return {"calls": calls, "prompt_tokens": prompt, "completion_tokens": completion,
            "latency_s_total": total, "latency_s_max": mx, "truncated": truncated}


def _workflow(rows):
    nodes = {f"n{i}": {"outputs": {"parameters": [{"name": "result", "value": json.dumps(r)}]}}
             for i, r in enumerate(rows)}
    nodes["agg"] = {"outputs": {"parameters": [{"name": "x", "value": "not json"}]}}
    return {"metadata": {"name": "wf"}, "status": {"phase": "Succeeded", "nodes": nodes}}


def _row(ticker, highlights, risks):
    return {"ticker": ticker, "timing_s": {"retrieval": 7.09},
            "llm": {"by_site": {"rag:highlights": highlights, "rag:risks": risks,
                                "synthesis": _site(1, 10, 10, 1.0, 1.0)}}}


def test_identical_pair_is_halved():
    c = rl.per_call(_site(2, 4924, 912, 11.79, 5.90))
    assert c == {"records": 2, "duplicated": True, "unexplained": False, "prompt_tokens": 2462,
                 "completion_tokens": 456, "latency_s": 5.90, "truncated": 0}


def test_two_different_calls_are_not_halved():
    # refine-style second call: different latency, odd sums
    c = rl.per_call(_site(2, 4925, 913, 9.0, 6.0))
    assert c["unexplained"] and not c["duplicated"] and c["completion_tokens"] == 913


def test_single_record_passes_through():
    c = rl.per_call(_site(1, 2306, 512, 166.86, 166.86, truncated=1))
    assert (c["duplicated"], c["unexplained"], c["completion_tokens"], c["truncated"]) == (
        False, False, 512, 1)


def test_analyse_and_main(tmp_path, capsys):
    wf = _workflow([
        _row("TSLA", _site(2, 4948, 730, 9.86, 4.93), _site(2, 4924, 912, 11.79, 5.90)),
        _row("WMT", _site(2, 6608, 412, 5.35, 2.67), _site(2, 5568, 436, 6.25, 3.12)),
    ])
    res = rl.analyse(wf)
    assert res["duplicated_sites"] == 4 and res["unexplained_sites"] == 0
    assert res["sites"]["rag:risks"] == {"calls": 2, "records": 4, "prompt_tokens": 5246,
                                         "completion_tokens": 674, "min": 218, "median": 337.0,
                                         "p95": 444.1, "max": 456, "truncated": 0}
    assert res["sites"]["both"]["calls"] == 4
    p = tmp_path / "wf.json"
    p.write_text(json.dumps(wf), encoding="utf-8")
    assert rl.main([str(p)]) == 0
    assert "duplicated (ticker, site) rows: 4" in capsys.readouterr().out
