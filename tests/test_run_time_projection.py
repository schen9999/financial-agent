"""scripts/run_time_projection.py — the gate before the CPU extended run."""
import importlib.util
import pathlib

_REPO = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rtp", _REPO / "scripts" / "run_time_projection.py")
rtp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rtp)

EXT_CPU = (_REPO / "argo" / "eval-run-extended-slm-cpu.yaml").read_text(encoding="utf-8")


def _node(name, typ, start, end, phase="Succeeded"):
    return {"displayName": name, "type": typ, "startedAt": start, "finishedAt": end, "phase": phase}


def _wf(ticker_minutes, retried=None, agg_s=60, parallelism=2):
    nodes, t = {}, 0
    for i, m in enumerate(ticker_minutes):
        name = f"eval-ticker(0:{i})"
        s = f"2026-10-03T{10 + t // 60:02d}:{t % 60:02d}:00Z"
        e_min = t + m
        e = f"2026-10-03T{10 + e_min // 60:02d}:{e_min % 60:02d}:00Z"
        nodes[f"r{i}"] = _node(name, "Retry", s, e)
        # attempt pods are "<task>(<n>)" (Argo v3.7, checked on kind); a
        # retried task's attempts are each shorter than its Retry node
        nodes[f"p{i}"] = _node(name + "(0)", "Pod", s, e if i != retried else s.replace(":00Z", ":30Z"))
        if i == retried:
            nodes[f"q{i}"] = _node(name + "(1)", "Pod", s.replace(":00Z", ":30Z"), e)
    nodes["agg"] = _node("aggregate", "Pod", "2026-10-03T23:00:00Z", f"2026-10-03T23:0{agg_s // 60}:00Z")
    return {"metadata": {"name": "grounding-eval-slm-cpu-x"},
            "status": {"nodes": nodes, "storedWorkflowTemplateSpec": {"parallelism": parallelism}}}


def test_run_file_deadlines_read_from_the_committed_file():
    assert rtp.run_file_deadlines(EXT_CPU) == (57600, 5400, 40)


def test_fast_smoke_passes():
    ok, lines = rtp.project(_wf([20, 25, 30, 22, 18, 24, 26, 21, 19, 23]), EXT_CPU)
    assert ok, lines
    assert any("20 waves of 2" in ln for ln in lines)


def test_slow_smoke_fails_on_workflow_deadline():
    # 50 min worst ticker x 20 waves = 1000 min > 960 min (57600 s)
    ok, lines = rtp.project(_wf([30] * 9 + [50]), EXT_CPU)
    assert not ok
    assert any(ln.startswith("FAIL  worst projection <= workflow deadline") for ln in lines)


def test_ticker_near_its_deadline_fails():
    # 70 min > 75% of 90 min ticker deadline, even if the total would fit
    ok, lines = rtp.project(_wf([5] * 9 + [70]), EXT_CPU.replace("57600", "200000"))
    assert not ok
    assert any(ln.startswith("FAIL  slowest smoke ticker") for ln in lines)


def test_retry_node_spans_all_attempts():
    times, _ = rtp.ticker_times(_wf([10, 40], retried=1))
    assert sorted(times.values()) == [600.0, 2400.0]


def test_attempt_pods_are_not_extra_tickers():
    times, _ = rtp.ticker_times(_wf([10, 40, 12], retried=1))
    assert sorted(times) == ["eval-ticker(0:0)", "eval-ticker(0:1)", "eval-ticker(0:2)"]


def test_no_finished_tickers_exits():
    import pytest
    with pytest.raises(SystemExit):
        rtp.project({"status": {"nodes": {}}}, EXT_CPU)
