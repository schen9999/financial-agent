"""eval/three_judging_stats.py: each judging's totals reproduce the
recorded figures (original runs, re-judge 1 and 2), and the paired test
runs on ticker rates averaged over the three judgings."""
from eval import three_judging_stats as tj

SOURCES = ["raw", "eval/runs/rejudge-2026-10-06", "eval/runs/rejudge-2026-10-06-r2"]


def test_judging_totals_reproduce_the_records():
    js = [tj.judging_counts("4hsn2", s) for s in SOURCES]
    assert [(t["unsupported"], t["total"]) for t in map(tj.totals, js)] == [(15, 399), (6, 408), (10, 415)]
    assert tj.totals(js[0])["unsupported_numeric"] == 3


def test_ticker_rates_average_the_judgings_with_a_denominator():
    a = {"X": {"unsupported": 1, "total": 4, "unsupported_numeric": 0, "numeric": 0}}
    b = {"X": {"unsupported": 0, "total": 2, "unsupported_numeric": 1, "numeric": 2}}
    r = tj.ticker_rates([a, b])
    assert r["X"]["rate"] == 0.125 and r["X"]["numeric_rate"] == 0.5


def test_pair_lines_label_fisher_per_judging():
    js = {r: [tj.judging_counts(r, s) for s in SOURCES] for r in ("4hsn2", "nstp9")}
    L = tj.pair_lines("4hsn2", "nstp9", js["4hsn2"], js["nstp9"])
    assert "over 40 tickers" in L[1] and "continuity only" in L[3]
