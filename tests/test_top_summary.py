"""scripts/top_summary.py: a kubectl-top capture grouped by workload."""
import importlib.util
import pathlib

_REPO = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("top_summary", _REPO / "scripts/top_summary.py")
top = importlib.util.module_from_spec(spec)
spec.loader.exec_module(top)

CAPTURE = """== 2026-10-04T01:15:33Z
api-7fcdfd9c46-8p4nb         1m    481Mi
llamacpp-548f6b8bc6-dgxrf    7806m 26886Mi
wf-x-eval-one-227411509      780m  300Mi
== 2026-10-04T01:15:49Z
api-7fcdfd9c46-8p4nb         5m    482Mi
llamacpp-548f6b8bc6-dgxrf    8000m 27449Mi
wf-x-eval-one-227411509      1m    582Mi
wf-x-eval-one-3189871064     3m    590Mi
wf-x-aggregate-1             2m    20Mi
NAME   CPU(cores)   MEMORY(bytes)
"""


def test_groups_pods_and_separates_eval_startup_from_steady_state():
    samples, rows = top.parse(CAPTURE)
    assert samples == 2 and sorted(rows) == ["aggregate pod", "api", "eval pods", "llamacpp"]
    s = top.summarize(rows, spike=100)
    assert (s["llamacpp"]["cpu_max"], s["llamacpp"]["mem_max"], s["llamacpp"]["pods"]) == (8000, 27449, 1)
    ev = s["eval pods"]
    assert (ev["pods"], ev["readings"], ev["cpu_max"], ev["spikes"]) == (2, 3, 780, 1)
    assert (ev["steady_median"], ev["steady_max"]) == (2.0, 3)
    assert s["api"]["cpu_median"] == 3.0


def test_container_column_form_is_read_too():
    _, rows = top.parse("== t\napi-1   api   4m   481Mi\n")
    assert rows["api"] == [(4, 481, "api-1")]


def test_committed_extended_capture(capsys):
    assert top.main([str(_REPO / "eval/runs/top-cpu-ext.txt")]) == 0
    out = capsys.readouterr().out
    assert "705 samples" in out
    assert "llamacpp          1      705       7806m     8000m" in out
