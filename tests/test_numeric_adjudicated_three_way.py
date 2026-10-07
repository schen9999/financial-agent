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


FX_ADJ = nb.REPO / "eval/numeric_check/adjudication-2026-10-06-9jzmj-8vpq6-p9jr2-fx.csv"
PREFLIGHT = nb.REPO / "eval/runs/financial-currency-2026-10-06.json"


def test_retroactive_currency_set_reproduces_with_the_preflight_file():
    """The 2026-10-06 retroactive check (before the fix): with the reporting
    currencies added, every flag matches its verdict and the currency_label
    TRUE_ERRORs are 22 / 10 / 11; without them the flags do not match."""
    import pytest
    res = na.run_three_way(FX_ADJ, ["9jzmj", "8vpq6", "p9jr2"], "2026-10-06", draws=200,
                           financial_currency=PREFLIGHT)
    assert res["financial_currency"]["injected"] == {
        "BABA": "CNY", "NVO": "DKK", "SAP": "EUR", "TM": "JPY", "TSM": "TWD"}
    cl = res["currency_label_true_errors"]["run"]
    assert [(cl[r]["k"], cl[r]["n"]) for r in ("9jzmj", "8vpq6", "p9jr2")] == \
        [(22, 569), (10, 389), (11, 423)]
    te = res["true_error_rates"]["true_error"]["run"]
    assert [te[r]["k"] for r in ("9jzmj", "8vpq6", "p9jr2")] == [2, 1, 2]
    assert "currency_label TRUE_ERRORs per checked number" in na.markdown_three_way(res)
    with pytest.raises(AssertionError):
        na.run_three_way(FX_ADJ, ["9jzmj", "8vpq6", "p9jr2"], "2026-10-06", draws=50)


def test_new_runs_show_true_errors_outside_the_upstream_causes():
    adj = ADJ.parent / "adjudication-2026-10-06-4hsn2-nstp9.csv"
    res = na.run_three_way(adj, ["4hsn2", "nstp9"], "2026-10-06", draws=200)
    md = na.markdown_three_way(res)
    assert "| baseline | 1 | 0 | 0 | 0 | 1 |" in md and "| slm-full-gpu | 1 | 0 | 0 | 0 | 1 |" in md
