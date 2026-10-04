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
