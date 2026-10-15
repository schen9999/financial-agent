"""scripts/anthropic_cost_estimate.py: reads committed run files and the
aggregates of committed f3043751 runs; no API call."""
import pytest

from scripts import anthropic_cost_estimate as ace


def test_run_shape_reads_file_and_template_defaults():
    assert ace.run_shape("argo/eval-run-extended-slm-cpu.yaml") == (["slm-full-cpu"], 40)
    assert ace.run_shape("argo/eval-run-slm-gpu-smoke.yaml") == (["slm-full-gpu"], 10)
    assert ace.run_shape("argo/eval-run.yaml") == (["baseline"], 10)


def test_one_judging_priced_from_the_price_file():
    # 3,690 in + 725 out at Sonnet $3 / $15 per Mtok; x40 is the documented ~$0.88
    assert ace.judging_per_brief() == pytest.approx(0.021945)
    assert 40 * ace.judging_per_brief() == pytest.approx(0.878, abs=0.001)


def test_cpu_extended_three_judgings_uses_the_dearest_same_size_reference():
    (r,) = ace.estimate("argo/eval-run-extended-slm-cpu.yaml", 3)
    assert r["ref"]["log"].endswith("cpu-rerun-f304375.log") and r["ref"]["cost"] == 3.3109
    assert r["in_cluster"] == pytest.approx(3.3109)
    assert r["rejudges"] == pytest.approx(2 * 40 * 0.021945)


def test_smoke_uses_smoke_references_and_unknown_arm_stops():
    (r,) = ace.estimate("argo/eval-run-slm-gpu-smoke.yaml", 1)
    assert r["tickers"] == 10 and r["ref"]["tickers"] == 10 and r["rejudges"] == 0
    refs = [x for x in ace.references() if x["arm"] != "slm-full-gpu"]
    with pytest.raises(SystemExit):
        ace.estimate("argo/eval-run-slm-gpu-smoke.yaml", 1, refs)
