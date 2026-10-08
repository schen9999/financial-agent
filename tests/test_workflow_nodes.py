"""scripts/workflow_nodes.py: node status read from status.nodes or
status.compressedNodes, and a plain stop when it is offloaded to Argo's
database; the host-side readers go through it."""
import base64
import gzip
import importlib.util
import io
import json
import pathlib
import sys

import pytest

_REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
import workflow_nodes as wn  # noqa: E402

from eval import attempts  # noqa: E402


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, _REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _compress(nodes):
    # Argo: gzip, then standard base64 (util/file CompressEncodeString)
    return base64.b64encode(gzip.compress(json.dumps(nodes).encode("utf-8"))).decode("ascii")


def _compressed(workflow):
    out = json.loads(json.dumps(workflow))
    out["status"]["compressedNodes"] = _compress(out["status"].pop("nodes"))
    return out


PLAIN = json.loads((_REPO / "eval/runs/hm527-workflow.json").read_text(encoding="utf-8"))


def test_nodes_from_plain_and_compressed_status_are_the_same_map():
    packed = _compressed(PLAIN)
    assert "nodes" not in packed["status"]
    assert wn.nodes(packed) == wn.nodes(PLAIN) == PLAIN["status"]["nodes"]
    expanded = wn.expand(packed)
    assert expanded["status"]["nodes"] == PLAIN["status"]["nodes"]
    assert "compressedNodes" not in expanded["status"]
    assert "nodes" not in packed["status"]  # the input object is not modified


def test_offloaded_nodes_stop_instead_of_reading_as_an_empty_workflow():
    wf = {"metadata": {"name": "wf-x"}, "status": {"offloadNodeStatusVersion": "fnv:123"}}
    with pytest.raises(SystemExit, match="OFFLOADED to Argo's persistence database"):
        wn.nodes(wf)
    assert wn.nodes({"metadata": {"name": "new"}, "status": {}}) == {}


def test_attempts_report_sees_every_pod_once_the_object_is_expanded():
    packed = _compressed(PLAIN)
    # what eval/attempts.py sees unexpanded: the bug this guards against
    assert attempts.build_report(packed, {})["eval_pods"] == 0
    rep = attempts.build_report(wn.expand(packed), {})
    assert (rep["eval_pods"], rep["tickers"], rep["retries"]) == (10, 10, 0)


def test_expand_cli_reads_stdin_and_reports_the_source(monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_compressed(PLAIN))))
    assert wn.main(["expand"]) == 0
    cap = capsys.readouterr()
    assert len(json.loads(cap.out)["status"]["nodes"]) == len(PLAIN["status"]["nodes"])
    assert "read from status.compressedNodes" in cap.err
    assert wn.main([]) == 2


REAL = _REPO / "eval/runs/9jzmj-workflow.json"  # a real 40-ticker object, as kubectl returned it


def test_real_compressed_workflow_has_every_pod_and_no_retries():
    wf = json.loads(REAL.read_text(encoding="utf-8"))
    assert "nodes" not in wf["status"] and wf["status"]["compressedNodes"]
    ns = wn.nodes(wf)
    pods = [n for n in ns.values() if n["type"] == "Pod"]
    assert (len(ns), len(pods)) == (83, 41)
    assert sum(n["templateName"] == "eval-one" and n["phase"] == "Succeeded" for n in pods) == 40
    (agg,) = [n for n in pods if n["templateName"] == "aggregate"]
    assert agg["phase"] == "Error" and "configmaps is forbidden" in agg["message"]
    rep = attempts.build_report(wn.expand(wf), {})
    assert (rep["eval_pods"], rep["tickers"], rep["retries"], rep["failed_attempts"]) == (40, 40, 0, [])


def test_stored_rows_of_9jzmj_give_the_same_aggregate_as_the_pod_log_rebuild(monkeypatch):
    """The rows Argo stored for the aggregate step that never ran, against
    the rows rebuilt from the pod logs: the aggregate prints the same
    report, plus the estimated cost only the stored rows carry."""
    agg = _load("eval_aggregate_nodes", "scripts/eval_aggregate.py")
    rows = wn.eval_results(json.loads(REAL.read_text(encoding="utf-8")))
    assert len(rows) == 40

    def report(payloads, tmp):
        tmp.write_text(json.dumps(payloads), encoding="utf-8")
        lines = []
        monkeypatch.setattr(agg, "print", lambda *a, **k: lines.append(" ".join(map(str, a))),
                            raising=False)
        monkeypatch.setattr(agg.sys, "argv", ["eval_aggregate.py", "--input", str(tmp)])
        monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
        agg.main()
        return [ln.rstrip() for ln in lines if ln.strip()]

    import tempfile
    with tempfile.TemporaryDirectory() as d:
        stored = report(rows, pathlib.Path(d) / "stored.json")
        rebuilt = report(json.loads((_REPO / "eval/runs/9jzmj-results-rebuilt.json")
                                    .read_text(encoding="utf-8")), pathlib.Path(d) / "rebuilt.json")
    extra = [ln for ln in stored if ln not in rebuilt]
    assert [ln for ln in rebuilt if ln not in stored] == []
    assert len(extra) == 1 and extra[0].startswith("  est. run cost     : $4.0998")
    assert "  TOTAL     381    7   23  411     5.41    25.86" in stored


def test_run_time_projection_and_rag_ledger_read_compressed_workflows(tmp_path, capsys):
    rtp = _load("run_time_projection_nodes", "scripts/run_time_projection.py")
    ledger = _load("rag_ledger_nodes", "scripts/rag_ledger_from_workflow.py")
    packed = _compressed(PLAIN)
    times, _phases = rtp.ticker_times(wn.expand(packed))
    assert len(times) == 10 and rtp.ticker_times(packed)[0] == {}
    f = tmp_path / "wf.json"
    f.write_text(json.dumps(packed), encoding="utf-8")
    assert ledger.main([str(f)]) == 0
    assert "grounding-eval-hm527 (Succeeded): 10 tickers" in capsys.readouterr().out
    assert rtp.main(["--workflow", str(f), "--next",
                     str(_REPO / "argo/eval-run-extended.yaml")]) in (0, 1)
    assert "10 tickers" in capsys.readouterr().out
