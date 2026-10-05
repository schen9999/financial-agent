"""scripts/numeric_adjudicated.py --adjudication --runs: the 2026-10-05
same-image three-way reproduces from the committed verdicts."""
from scripts import numeric_adjudicated as na
from scripts import numeric_backtest as nb

ADJ = nb.REPO / "eval/numeric_check/adjudication-2026-10-05-9jzmj-8vpq6-p9jr2.csv"


def test_three_way_reproduces_counts_upstream_and_judge_overlap():
    res = na.run_three_way(ADJ, ["9jzmj", "8vpq6", "p9jr2"], "2026-10-05", draws=200)
    p = res["precision"]
    assert [(p[r][na.TE], p[r][na.FP]) for r in ("9jzmj", "8vpq6", "p9jr2")] == [(8, 0), (1, 0), (2, 1)]
    te = res["true_error_rates"]["true_error"]["run"]
    assert [(te[r]["k"], te[r]["n"]) for r in ("9jzmj", "8vpq6", "p9jr2")] == \
        [(8, 569), (1, 389), (2, 423)]
    ex = res["true_error_rates"]["true_error_ex_upstream"]["run"]
    assert all(ex[r]["k"] == 0 for r in ex)
    assert set(res["true_error_rates"]["true_error"]["differences"]) == \
        {"8vpq6 - 9jzmj", "p9jr2 - 9jzmj", "p9jr2 - 8vpq6"}
    tm = [j for j in res["judge_on_same_figure"] if j["ticker"] == "TM" and j["section"] == "Executive Summary"]
    assert {(j["stated"], j["judge"][0]["judge_label"]) for j in tm} == \
        {("$4.5 billion", "SUPPORTED"), ("$52.0 billion", "SUPPORTED")}
