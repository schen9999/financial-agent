"""eval/reweight_calibration.py: population-weighted recall and true rate."""
import pytest

from eval.reweight_calibration import (interval, posterior_draws, reweight,
                                       stratum_counts, summarize)


def test_stratum_counts_from_pairs():
    pairs = ([("SUPPORTED", "SUPPORTED")] * 9 + [("SUPPORTED", "UNSUPPORTED")]
             + [("UNSUPPORTED", "UNSUPPORTED")] * 3 + [("UNSUPPORTED", "INFERENCE")]
             + [("INFERENCE", "INFERENCE")] * 4)
    assert stratum_counts(pairs) == {"SUPPORTED": (1, 10),
                                     "UNSUPPORTED": (3, 4),
                                     "INFERENCE": (0, 4)}


def test_reweight_hand_computed():
    # p_S = 1/10, p_U = 3/4, p_I = 0/4; population 900 S / 40 U / 60 I.
    # T = 900*0.1 + 40*0.75 + 60*0 = 90 + 30 = 120
    # recall = 30 / 120 = 0.25; true rate = 120 / 1000 = 0.12
    strata = {"SUPPORTED": (1, 10), "UNSUPPORTED": (3, 4), "INFERENCE": (0, 4)}
    pop = {"SUPPORTED": 900, "UNSUPPORTED": 40, "INFERENCE": 60}
    recall, rate = reweight(strata, pop)
    assert recall == pytest.approx(0.25)
    assert rate == pytest.approx(0.12)


def test_unweighted_sample_would_overstate_recall():
    # Same strata, sample-as-drawn recall is 3/(1+3+0) = 75%; weighting by
    # the population drops it to 25%, the published-holdout failure mode.
    strata = {"SUPPORTED": (1, 10), "UNSUPPORTED": (3, 4), "INFERENCE": (0, 4)}
    sample_pop = {k: n for k, (_, n) in strata.items()}
    assert reweight(strata, sample_pop)[0] == pytest.approx(0.75)


def test_intervals_bracket_point_and_are_deterministic():
    strata = {"SUPPORTED": (1, 20), "UNSUPPORTED": (9, 15), "INFERENCE": (2, 15)}
    pop = {"SUPPORTED": 354, "UNSUPPORTED": 12, "INFERENCE": 26}
    a = summarize(strata, pop, posterior_draws(strata, draws=5000, seed=1))
    b = summarize(strata, pop, posterior_draws(strata, draws=5000, seed=1))
    assert a == b
    assert a["recall"] == pytest.approx(7.2 / (17.7 + 7.2 + 26 * 2 / 15))
    assert a["recall_ci"][0] < a["recall"] < a["recall_ci"][1]
    assert a["rate_ci"][0] < a["rate"] < a["rate_ci"][1]


def test_interval_percentiles():
    assert interval([i / 1000 for i in range(1001)]) == (0.025, 0.975)
