"""eval/density_check.py: judge-independent and re-judged density reproduce
the 2026-10-06 figures, and numbers are not double-counted."""
from pathlib import Path

from eval import density_check as dc
from eval import multi_arm_stats as mas


def test_counts_each_number_once():
    text = "### Executive Summary\nRevenue of $10.0 billion and a P/E of 20.5x; 52-week high $30.\n"
    c = dc.text_counts(text)
    assert c["bound"] == 3
    assert c["numbers"] == 3          # not 3 + 3: bound numbers are among the counted tokens


def test_committed_runs_reproduce():
    text = {r: dc.text_density(r) for r in ("9jzmj", "p9jr2")}
    mean = lambda d, f: sum(x[f] for x in d.values()) / len(d)  # noqa: E731
    assert round(mean(text["9jzmj"], "numbers"), 2) == 6.80
    assert round(mean(text["p9jr2"], "numbers"), 2) == 3.42
    pr = mas.paired(text["9jzmj"], text["p9jr2"], "bound")
    assert round(pr["mean_diff"], 2) == 1.80 and (pr["a_more"], pr["equal"], pr["b_more"]) == (30, 9, 1)
    rj = dc.rejudge_density("9jzmj", dc.ROOT / "eval/runs/rejudge-2026-10-06")
    assert round(mean(rj, "numeric"), 2) == 6.97
