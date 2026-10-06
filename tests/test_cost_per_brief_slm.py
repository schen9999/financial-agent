"""scripts/cost_per_brief_slm.py: serving cost per brief from a run's wall time."""
import importlib.util
import pathlib

_REPO = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cost_per_brief_slm",
                                              _REPO / "scripts/cost_per_brief_slm.py")
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)


def test_e5_hourly_bills_each_gib_as_one_gb_unless_asked_to_convert():
    hourly, gb = cps.e5_hourly(4, 30, 0.03, 0.002)
    assert gb == 30 and round(hourly, 6) == 0.18
    hourly, gb = cps.e5_hourly(4, 30, 0.03, 0.002, decimal_gb=True)
    assert round(gb, 3) == 32.212
    assert round(hourly, 6) == round(4 * 0.03 + 32.21225472 * 0.002, 6)


def test_committed_gpu_run_cost_from_its_workflow_object():
    """p9jr2: 03:13:00 .. 03:48:12 UTC = 2,112 s for 40 briefs."""
    s = cps.summarize(_REPO / "eval/runs/slm-proof-p9jr2/"
                      "grounding-eval-extended-slm-gpu-p9jr2-workflow.json", 2.00)
    assert (s["wall_s"], s["briefs"]) == (2112.0, 40)
    assert round(s["s_per_brief"], 1) == 52.8
    assert round(s["usd_per_brief"], 4) == round(2.00 * 2112 / 3600 / 40, 4) == 0.0293
    assert s["calls"] == 270 / 40
    assert round(s["prompt_tokens"] * 40) == 350290 and round(s["completion_tokens"] * 40) == 98232
