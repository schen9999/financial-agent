"""scripts/rerank_ab_decide.py: the pre-registered criteria, computed as
stated. Synthetic inputs except the baseline pipeline time, read from a
committed workflow object."""
from scripts import rerank_ab_decide as d


def test_mcnemar_exact():
    assert d.mcnemar_exact(0, 0) == 1.0
    assert round(d.mcnemar_exact(6, 0), 4) == 0.0312      # 6 discordant, all one way
    assert round(d.mcnemar_exact(5, 0), 4) == 0.0625      # not enough


def test_refusal_criterion_needs_a_drop_of_three_and_p_below_005():
    base = {f"T{i}": i < 9 for i in range(35)}            # 9 refusals
    better = dict(base, T0=False, T1=False, T2=False, T3=False, T4=False, T5=False)
    assert d.refusals(base, better)["pass"] and d.refusals(base, better)["b"] == 6
    small = dict(base, T0=False, T1=False, T2=False)
    assert not d.refusals(base, small)["pass"]              # b - c = 3 but p = 0.25


def test_latency_and_decision():
    lat = d.latency({"per_ticker_added_s_median": 4.0}, baseline_pipeline_s=26.7)
    assert lat["pass"] and round(lat["share"], 3) == 0.150
    assert not d.latency({"per_ticker_added_s_median": 6.0}, 26.7)["pass"]
    ok = {"pass": True}
    assert d.decide({"refusals": ok, "numeric": ok, "density": ok, "latency": ok}) == "SHIP"
    assert d.decide({"refusals": {"pass": False}, "numeric": ok, "density": ok, "latency": ok}) == "DON'T SHIP"
    assert d.decide({"refusals": ok, "numeric": {"pass": None}, "density": ok, "latency": ok}) == "PENDING"
    assert d.decide({"refusals": ok, "numeric": ok, "density": ok, "latency": ok,
                     "grounding": {"blocks": True}}).startswith("DON'T SHIP")


def test_baseline_pipeline_time_from_a_committed_workflow():
    assert 20 < d.baseline_pipeline_s("4hsn2") < 40
