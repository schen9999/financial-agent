"""scripts/numeric_adjudicated.py: upstream attribution, verdict joining,
stratum-weighted precision and the adjudication-adjusted replication gap."""
import random

import pytest

from scripts import numeric_adjudicated as na
from scripts import numeric_backtest as nb


def _r(ticker="AAPL", field="revenue", ratio="0.1", source="1e12", verdict="TRUE_ERROR",
       kind="mismatch", note=""):
    return dict(id="1", run="j4cnp", scope="full", arm="baseline", model="hosted",
                ticker=ticker, section="Financial Health", kind=kind, field=field,
                stated="$1", sentence="s", source=source, ratio=ratio, verdict=verdict,
                note=note)


@pytest.mark.parametrize("ratio,e", [("0.001001", -3), ("0.09962", -1), ("10", 1),
                                     ("1", 0), ("0.00985", -2), ("3.388", None),
                                     ("", None), ("0", None), ("-0.01", -2)])
def test_pow10(ratio, e):
    assert na.pow10(ratio) == e


def test_upstream_currency_needs_a_power_of_ten_rescale_of_the_source():
    assert na.upstream_cause(_r("TM", "revenue", "0.001001")) == "currency"
    assert na.upstream_cause(_r("NVO", "net_income", "0.09996")) == "currency"
    assert na.upstream_cause(_r("TSM", "revenue", "3.4")) is None        # not a rescale
    assert na.upstream_cause(_r("TM", "market_cap", "0.001")) is None    # field unaffected
    assert na.upstream_cause(_r("TM", "revenue", "0.001", verdict="FALSE_POSITIVE")) is None


def test_sap_is_listed_not_attributed():
    r = _r("SAP", "net_income", "10")
    assert na.upstream_cause(r) is None
    assert na.upstream_adjacent(r) == "sap"


def test_upstream_margin_fraction_only_at_one_hundredth():
    m = dict(field="profit_margin")
    assert na.upstream_cause(_r("LCID", ratio="0.009991", source="-2.49214", **m)) == "margin_fraction"
    other = _r("EDIT", ratio="0.09999", source="-1.57322", **m)
    assert na.upstream_cause(other) is None
    assert na.upstream_adjacent(other) == "margin_other_scale"
    assert na.upstream_cause(_r("AFRM", ratio="0.01", source="0.453", **m)) is None


def test_attach_verdicts_rejects_unmatched_flags_and_rows():
    f = {"section": "Financial Health", "kind": "mismatch", "field": "revenue",
         "stated": "$1", "sentence": "s", "source": 1.0, "ratio": 0.1}
    brief = {"run": "j4cnp", "ticker": "AAPL", "report": {"findings": [f, dict(f)]}}
    row = _r()
    na.attach_verdicts([brief], [row])
    assert len(brief["adj"]) == 1 and brief["adj"][0][0]["occurrences"] == 2
    with pytest.raises(AssertionError, match="rows without a flag"):
        na.attach_verdicts([brief], [row, _r(ticker="MSFT")])
    with pytest.raises(AssertionError, match="flags without a verdict"):
        na.attach_verdicts([brief], [_r(verdict="")])


def test_strata_precision_two_ways_and_missing_strata():
    labels = {"a": ["TRUE_ERROR", "OTHER_DEFECT"], "b": ["FALSE_POSITIVE", "TRUE_ERROR"]}
    pop = {"a": 30, "b": 10, "c": 5}
    p, missing = na.strata_precision(labels, "other_defect_as_tp", pop)
    assert p == pytest.approx((30 * 1.0 + 10 * 0.5) / 40) and missing == ["c"]
    p, _ = na.strata_precision(labels, "other_defect_excluded", pop)
    assert p == pytest.approx((30 * 1.0 + 10 * 0.5) / 40)
    labels["a"] = ["OTHER_DEFECT"]
    p, missing = na.strata_precision(labels, "other_defect_excluded", pop)
    assert p == pytest.approx(0.5) and missing == ["a", "c"]


def _frame(rng):
    tickers = [f"T{i}" for i in range(12)]
    out = {}
    for arm in nb.REPLAY_ARMS:
        out[arm] = {"flags": {t: {"revenue": rng.randint(0, 6), "net_income": rng.randint(0, 6)}
                              for t in tickers},
                    "checked": {t: rng.randint(10, 20) for t in tickers}}
    return out


def _record(frame):
    rec = {"arms": {}}
    for arm, f in frame.items():
        pop = {}
        for c in f["flags"].values():
            for h, n in c.items():
                pop[h] = pop.get(h, 0) + n
        rec["arms"][arm] = {"population_by_field": pop}
    return rec


def test_adjusted_gap_at_full_precision_equals_the_registered_bootstrap():
    frame = _frame(random.Random(1))
    labels = {a: {"revenue": ["TRUE_ERROR"] * 5, "net_income": ["TRUE_ERROR"] * 5}
              for a in nb.REPLAY_ARMS}
    adj = na.adjusted_gap(frame, labels, _record(frame), draws=500)
    ticker_pairs = {a: {t: (sum(frame[a]["flags"][t].values()), frame[a]["checked"][t])
                        for t in frame[a]["checked"]} for a in nb.REPLAY_ARMS}
    reg = nb.bootstrap_difference(ticker_pairs["w4a16"], ticker_pairs["bf16"], draws=500)
    assert adj["difference"] == reg["difference"]
    assert adj["ci95"] == reg["ci95"]


def test_adjusted_gap_weights_flags_by_stratum_true_share():
    frame = _frame(random.Random(2))
    labels = {"w4a16": {"revenue": ["TRUE_ERROR", "OTHER_DEFECT"], "net_income": ["TRUE_ERROR"]},
              "bf16": {"revenue": ["TRUE_ERROR"], "net_income": ["FALSE_POSITIVE", "TRUE_ERROR"]}}
    adj = na.adjusted_gap(frame, labels, _record(frame), draws=50)

    def rate(a, s):
        k = sum(c[h] * s[h] for c in frame[a]["flags"].values() for h in c)
        return k / sum(frame[a]["checked"].values())
    want = rate("w4a16", {"revenue": 0.5, "net_income": 1.0}) - \
        rate("bf16", {"revenue": 1.0, "net_income": 0.5})
    assert adj["difference"] == pytest.approx(want, abs=1e-4)


def test_adjusted_gap_bounds_an_unlabelled_stratum():
    frame = _frame(random.Random(3))
    for t in frame["w4a16"]["flags"]:
        frame["w4a16"]["flags"][t]["current_price"] = 1
    labels = {a: {"revenue": ["TRUE_ERROR"], "net_income": ["TRUE_ERROR"]} for a in nb.REPLAY_ARMS}
    rec = _record(frame)
    zero, one = (na.adjusted_gap(frame, labels, rec, draws=20, unlabelled=u) for u in ("zero", "one"))
    n = sum(frame["w4a16"]["checked"].values())
    assert one["difference"] - zero["difference"] == pytest.approx(12 / n, abs=1e-4)


def test_notes_report_counts_doubt_on_labelled_rows():
    rows = [_r(note="doubt: period?"), _r(note="checked"), _r(verdict="", note="doubt: x")]
    rep = na.notes_report(rows)
    assert rep["labelled"] == 2 and rep["doubt_notes"] == 1 and len(rep["notes"]) == 3
