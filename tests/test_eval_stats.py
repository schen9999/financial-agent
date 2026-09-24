"""eval/stats.py against known published values.

Wilson: the textbook k=1, n=10 example (Wilson 1927 / standard references)
gives (0.0179, 0.4041) at 95%. Fisher: scipy's documented example
fisher_exact([[1, 9], [11, 3]]) = 0.0027594..., and the classic
lady-tasting-tea table [[3, 1], [1, 3]] = 0.4857...
"""
import pytest

from eval.stats import fisher_exact, format_rate_ci, wilson_interval


def test_wilson_textbook_value():
    lo, hi = wilson_interval(1, 10)
    assert lo == pytest.approx(0.0179, abs=5e-4)
    assert hi == pytest.approx(0.4041, abs=5e-4)


def test_wilson_zero_successes_has_width():
    lo, hi = wilson_interval(0, 84)
    assert lo == 0.0
    assert hi == pytest.approx(0.0437, abs=5e-4)  # 0/84 still admits ~4.4%


def test_wilson_run_of_record_contains_the_gate():
    # 2/66 (the 2026-09-03 baseline): the 95% interval spans the 5% gate,
    # which is exactly why a 3.03% point estimate cannot resolve the gate.
    lo, hi = wilson_interval(2, 66)
    assert lo < 0.05 < hi
    assert lo == pytest.approx(0.0083, abs=5e-4)
    assert hi == pytest.approx(0.1039, abs=5e-4)


def test_wilson_degenerate_n():
    assert wilson_interval(0, 0) == (0.0, 1.0)
    with pytest.raises(ValueError):
        wilson_interval(5, 3)


def test_fisher_scipy_documented_example():
    assert fisher_exact(1, 9, 11, 3) == pytest.approx(0.0027594, rel=1e-4)


def test_fisher_lady_tasting_tea():
    assert fisher_exact(3, 1, 1, 3) == pytest.approx(0.485714, rel=1e-4)


def test_fisher_symmetric_table_is_one():
    assert fisher_exact(5, 5, 5, 5) == pytest.approx(1.0, rel=1e-9)


def test_fisher_rejects_negative():
    with pytest.raises(ValueError):
        fisher_exact(-1, 2, 3, 4)


def test_format_rate_ci_shape():
    s = format_rate_ci(2, 66)
    assert s.startswith("3.03%") and "95% CI" in s
