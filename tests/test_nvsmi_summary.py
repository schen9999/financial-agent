"""scripts/nvsmi_summary.py: an nvidia-smi sampler CSV sliced per run window."""
import importlib.util
import json
import pathlib

_REPO = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("nvsmi_summary", _REPO / "scripts/nvsmi_summary.py")
nv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nv)

CSV = """timestamp, utilization.gpu [%], memory.used [MiB]
2026/10/05 03:00:00.100, 0 %, 20540 MiB
2026/10/05 03:00:05.100, 90 %, 20540 MiB
2026/10/05 03:00:10.100, 10 %, 20600 MiB
2026/10/05 03:00:15.100, 0 %, 20540 MiB
2026/10/05 03:00:20.100, 50 %, 20540 MiB
"""


def test_window_stats_and_activity_outside_every_window():
    samples = nv.parse_csv(CSV)
    assert len(samples) == 5 and samples[1][1:] == (90, 20540)
    r = nv.summarize(samples, nv.iso("2026-10-05T03:00:00Z"), nv.iso("2026-10-05T03:00:12Z"))
    assert (r["samples"], r["max"], r["busy"], r["mem_min"], r["mem_max"]) == (3, 90, 2, 20540, 20600)
    assert round(r["mean"], 2) == 33.33 and r["median"] == 10 and r["p95"] == 90
    assert nv.summarize(samples, nv.iso("2026-10-05T04:00:00Z"), nv.iso("2026-10-05T04:01:00Z")) is None
    o = nv.outside(samples, [("w", nv.iso("2026-10-05T03:00:00Z"), nv.iso("2026-10-05T03:00:12Z"))])
    assert (o["samples"], o["busy"]) == (2, 1)
    assert o["first_busy"] == o["last_busy"] == nv.iso("2026-10-05T03:00:20.100Z")


def test_workflow_window_from_status(tmp_path):
    wf = tmp_path / "wf.json"
    wf.write_text(json.dumps({"status": {"startedAt": "2026-10-05T03:13:00Z",
                                         "finishedAt": "2026-10-05T03:48:12Z"}}))
    s, e = nv.workflow_window(str(wf))
    assert (e - s).total_seconds() == 35 * 60 + 12


def test_committed_p9jr2_capture_has_no_gpu_activity_outside_the_runs():
    """The 2026-10-05 capture: every busy sample falls in a run window, which
    also checks that node 2's clock and the workflow times agree."""
    runs = _REPO / "eval" / "runs"
    samples = nv.parse_csv((runs / "gpu-nvsmi-p9jr2.csv").read_text(encoding="utf-8"))
    windows = [("tool-use gpu (approx)", nv.iso("2026-10-05T02:59:15Z"), nv.iso("2026-10-05T02:59:57Z"))]
    windows += [(w, *nv.workflow_window(str(runs / f"slm-proof-{w}" / name)))
                for w, name in (("k6zxd", "grounding-eval-slm-gpu-k6zxd-workflow.json"),
                                ("p9jr2", "grounding-eval-extended-slm-gpu-p9jr2-workflow.json"))]
    assert len(samples) == 709
    assert nv.outside(samples, windows)["busy"] == 0
    r = nv.summarize(samples, *windows[2][1:])
    assert (r["samples"], r["busy"], r["max"], r["mem_max"]) == (422, 182, 100, 20540)
