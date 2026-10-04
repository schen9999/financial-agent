"""scripts/aggregate_template_size.py: the aggregate step's template against
Argo's 131,072-byte inline limit, from the committed workflow objects."""
import importlib.util
import json
import pathlib

_REPO = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aggregate_template_size",
                                              _REPO / "scripts/aggregate_template_size.py")
ats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ats)


def _measure(rel):
    return ats.measure(json.loads((_REPO / rel).read_text(encoding="utf-8")))


def test_go_json_len_counts_escapes_and_utf8():
    assert ats.go_json_len("abc") == 5
    assert ats.go_json_len('a"b') == 6 and ats.go_json_len("a\nb") == 6
    assert ats.go_json_len("<") == 8          # \u003c
    assert ats.go_json_len("\u2013") == 5     # en dash: three UTF-8 bytes
    assert ats.LIMIT == 131072


def test_smokes_stay_inline_and_forty_tickers_cross_the_limit():
    hosted = _measure("eval/runs/hm527-workflow.json")
    assert hosted["tickers"] == 10 and hosted["template_bytes"] < ats.LIMIT
    assert hosted["crosses_at"] == 27
    slm = _measure("eval/runs/9jddz-workflow.json")
    assert slm["template_bytes"] < ats.LIMIT and slm["crosses_at"] == 18


def test_the_two_extended_runs_were_over_the_limit():
    """9jzmj errored there before the controller could create ConfigMaps;
    8vpq6's aggregate succeeded once it could — with a template 2.3x the
    limit, which only the offload can deliver."""
    hosted = _measure("eval/runs/9jzmj-workflow.json")
    assert (hosted["tickers"], hosted["phase"]) == (40, "Error")
    assert hosted["template_bytes"] > ats.LIMIT and round(hosted["times_limit"], 2) == 1.51
    slm = _measure("eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json")
    assert (slm["tickers"], slm["phase"]) == (40, "Succeeded")
    assert round(slm["times_limit"], 2) == 2.30


def test_workflow_without_an_aggregate_node_is_reported_not_guessed():
    assert ats.measure({"metadata": {"name": "x"}, "status": {"nodes": {}}}) is None
