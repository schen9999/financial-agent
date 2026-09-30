"""agent/numeric_check.py: parsing, tolerance, scope, placeholders, the CRBU
motivating case, warn/block/off rendering, pipeline wiring (no network, no
LLM), and the numeric injections in eval/perturb.py."""
import importlib.util
import pathlib
import random
from unittest.mock import MagicMock

import pytest

from agent import numeric_check as nc
from eval.perturb import inject_numeric

REPO = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "numeric_backtest", REPO / "scripts" / "numeric_backtest.py")
nb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nb)

STOCK = {
    "ticker": "ACME", "company_name": "Acme Robotics, Inc.",
    "current_price": 1.57, "market_cap": 168315792.0, "pe_ratio": 31.04,
    "forward_pe": -1.2427474, "week_52_high": 3.535, "week_52_low": 1.38,
    "revenue": 10035000.0, "net_income": -103403000.0, "profit_margin": 0.453,
}


def _one(text, stock=STOCK, rel_tol=nc.DEFAULT_REL_TOL):
    return nc.check_section("Financial Health", text, stock, rel_tol)


def _checked(text, stock=STOCK):
    """(field, stated_value) of every checked binding in text."""
    return [(b["field"], b["stated_value"]) for b in _one(text, stock)["bindings"]
            if b["status"] == "checked"]


def _status(text, stock=STOCK):
    return [(b["field"], b["status"]) for b in _one(text, stock)["bindings"]]


# --- parsing -----------------------------------------------------------------

@pytest.mark.parametrize("text,field,value", [
    ("It has a market capitalization of $16.8 billion.", "market_cap", 16.8e9),
    ("It has a market cap of $168.3M today.", "market_cap", 168.3e6),
    ("It has a $2.22 trillion market capitalization.", "market_cap", 2.22e12),
    ("- **Revenue**: $96,550,000 USD", "revenue", 96_550_000.0),
    ("**Revenue:** $1,560.35 million", "revenue", 1560.35e6),
    ("It generated $4.3 billion in annual revenue.", "revenue", 4.3e9),
    ("- **Market Cap**: $4.13 Billion", "market_cap", 4.13e9),
])
def test_money_units(text, field, value):
    assert _checked(text) == [(field, pytest.approx(value))]


@pytest.mark.parametrize("text,field,value", [
    ("It trades at a P/E ratio of 31.0x today.", "pe_ratio", 31.0),
    ("It trades at a relatively modest 23.26x P/E.", "pe_ratio", 23.26),
    ("Valuation sits at 20.8x trailing earnings.", "pe_ratio", 20.8),
    ("The forward P/E of 14.4x implies growth.", "forward_pe", 14.4),
    ("The Price-to-Earnings (P/E) ratio stands at 10.82.", "pe_ratio", 10.82),
    ("It carries a forward P/E ratio of -1.2x.", "forward_pe", -1.2),
    ("Relative to forward earnings expectations of 12.49x P/E.", "forward_pe", 12.49),
])
def test_x_suffix_and_pe_labels(text, field, value):
    assert _checked(text) == [(field, pytest.approx(value))]


@pytest.mark.parametrize("text,value", [
    ("It posts a net profit margin of 45.3%.", 45.3),
    ("A 45.3% net profit margin stands out.", 45.3),
    ("It has a negative profit margin of -52.5%.", -52.5),
    ("It has a negative profit margin of 52.5%.", -52.5),
])
def test_percent_profit_margin(text, value):
    assert _checked(text) == [("profit_margin", pytest.approx(value))]


@pytest.mark.parametrize("text", [
    "It reports net income of -$103.4 million.",
    "It reports a net loss of $103.4 million.",
    "It reports net losses of $103.4 million.",
    "It reports a net loss of -$103.4 million.",
    "It reports negative net income of $103.4 million.",
    "It posted a $103.4 million net loss.",
])
def test_negative_and_loss_of(text):
    assert _checked(text) == [("net_income", pytest.approx(-103.4e6))]
    assert _one(text)["findings"] == []


def test_prices_and_52_week_fields():
    got = dict(_checked("CRBU trades at $1.57, near its 52-week low of $1.38 "
                        "and well off its 52-week high of $3.54."))
    assert got == {"current_price": 1.57, "week_52_low": 1.38,
                   "week_52_high": pytest.approx(3.54)}
    rng = dict(_checked("The 52-week range ($1.38-$3.54) is wide."))
    assert rng == {"week_52_low": 1.38, "week_52_high": pytest.approx(3.54)}


# --- scope: labeled only, never guessed ---------------------------------------

def test_unlabeled_numbers_are_unchecked_not_guessed():
    r = _one("The company holds $142.8 million in cash and 12 programs.")
    assert r["bindings"] == [] and r["findings"] == []
    assert r["checked"] == 0 and r["unchecked"] == 2


def test_non_metric_tokens_do_not_count_as_unchecked():
    r = _one("Its 10-K for 2025 and the Q2 10-Q cite the 52-week window.")
    assert r["unchecked"] == 0


@pytest.mark.parametrize("text,reason", [
    ("It reported net losses of $148.1 million in 2025.", "period"),
    ("Over the past five years, it reported net income of $25.8 billion.", "period"),
    ("It posted a net loss of $2.7 billion for the year ended December 31, 2025.", "period"),
    ("Its net loss of $5.4 billion compared to $4.1 billion in the prior year.", "period"),
    ("The S&P 500's P/E ratio of 22.9x is higher.", "other_entity"),
    ("Its services revenue of $96.6 billion grew.", "subline"),
    ("It has a market cap of over $1 billion.", "bound"),
    ("Its net profit margin stands at -0.14x.", "form"),
])
def test_out_of_scope_labeled_numbers(text, reason):
    r = _one(text)
    assert [b["status"] for b in r["bindings"]] == [reason]
    assert r["findings"] == [] and r["unchecked_reasons"] == {reason: 1}


def test_ttm_and_dated_as_of_are_not_periods():
    assert _status("As of June 30, 2026, it reported $10.0 million in annual "
                   "revenue over the trailing twelve months.") == [("revenue", "checked")]


def test_field_missing_from_stock_is_no_source():
    stock = {k: v for k, v in STOCK.items() if k != "pe_ratio"}
    assert _status("It trades at a P/E of 25.0x.", stock) == [("pe_ratio", "no_source")]


@pytest.mark.parametrize("text", [
    "The foldable phone is priced at $2,000.",           # product, not stock
    "It sits 79% below its 52-week high at $0.56.",       # $0.56 is the price
    "It targets early B2B revenue traction.",             # not $2B
    "The net income has decreased by $31.1 billion.",     # a change, not a level
    "Operating margin of 30% and gross margin of 45%.",   # other margins
])
def test_near_miss_phrases_bind_nothing(text):
    assert _one(text)["bindings"] == []


# --- tolerance ---------------------------------------------------------------

def test_stated_precision_rounding_edges():
    for src, ok in ((16.75e9, True), (16.85e9, True), (16.86e9, False),
                    (16.74e9, False)):
        r = _one("It has a market cap of $16.8 billion.",
                 dict(STOCK, market_cap=src), rel_tol=0.0)
        assert (r["findings"] == []) is ok, src


def test_relative_tolerance_edges():
    assert nc.compare(100.0, 102.0, 0.05)       # 2.0 <= 2.04 + 0.05
    assert not nc.compare(100.0, 97.9, 0.05)    # 2.1 >  1.958 + 0.05
    assert nc.compare(0.0, 0.0, 0.5)            # 0% margin vs 0.0


def test_hedge_makes_trailing_zeros_rounding():
    stock = dict(STOCK, net_income=-440e6)
    assert _one("It reports a net loss of approximately $400 million.", stock)["findings"] == []
    assert len(_one("It reports a net loss of $400 million.", stock)["findings"]) == 1


def test_profit_margin_fraction_vs_percent():
    assert _one("It posts a 45.3% profit margin.")["findings"] == []
    f = _one("It posts a 0.45% profit margin.")["findings"]
    assert f[0]["field"] == "profit_margin" and f[0]["ratio"] == pytest.approx(0.01, rel=0.01)


def test_mismatch_finding_shape():
    f = _one("It has a market capitalization of $16.8 billion.")["findings"]
    assert len(f) == 1
    f = f[0]
    assert f["kind"] == "mismatch" and f["field"] == "market_cap"
    assert f["stated"] == "$16.8 billion" and f["source"] == 168315792.0
    assert f["ratio"] == pytest.approx(99.81, abs=0.01)
    assert f["section"] == "Financial Health"


# --- placeholders ------------------------------------------------------------

@pytest.mark.parametrize("text,token", [
    ("It is headquartered in [City Name], United States.", "[City Name]"),
    ("[Company] trades on the Nasdaq.", "[Company]"),
    ("Revenue grew [X] percent.", "[X]"),
    ("Price is $5.29 as of [insert date].", "[insert date]"),
    ("It has a market capitalization of $X billion.", "$X"),
    ("Ticker {ticker} is listed.", "{ticker}"),
])
def test_placeholders_flagged(text, token):
    f = [x for x in _one(text)["findings"] if x["kind"] == "placeholder"]
    assert [x["stated"] for x in f] == [token]


@pytest.mark.parametrize("text", [
    "See the [annual report](https://example.com) for details.",
    "Revenue rose as reported [1].",
    "- [x] Reviewed the filing.",
])
def test_links_citations_checkboxes_not_placeholders(text):
    assert _one(text)["findings"] == []


def test_na_filler_only_where_the_field_exists():
    f = _one("**P/E Ratio:** N/A")["findings"]
    assert [(x["kind"], x["field"]) for x in f] == [("placeholder", "pe_ratio")]
    stock = {k: v for k, v in STOCK.items() if k != "pe_ratio"}
    assert _one("**P/E Ratio:** N/A", stock)["findings"] == []


# --- the motivating case, from the committed findings file ------------------

def test_crbu_lsnnc_fixture_from_committed_findings():
    path = REPO / "eval" / "runs" / "raw" / "lsnnc-findings" / "CRBU_local-model.md"
    b = nb.load_brief(path, REPO / "eval" / "runs" / "raw")
    assert b["stock"]["market_cap"] == 168315792.0
    r = nc.check_sections(b["sections"], b["stock"])
    mc = [f for f in r["findings"] if f["field"] == "market_cap"]
    assert len(mc) == 1 and mc[0]["section"] == "Financial Health"
    assert mc[0]["stated"] == "$16.8 billion"
    assert mc[0]["ratio"] == pytest.approx(99.8, abs=0.1)
    ph = [f for f in r["findings"] if f["kind"] == "placeholder"]
    assert [f["stated"] for f in ph] == ["[City Name]"]
    # Price, 52-week low and forward P/E in the same brief are right.
    assert {f["field"] for f in r["findings"]} == {"market_cap", None}
    b["report"] = r
    assert nb.assert_crbu([dict(b, run="lsnnc", ticker="CRBU")])["passed"]


# --- warn / block / off ------------------------------------------------------

BRIEF = """## Acme Robotics (ACME) — Investment Brief

### Executive Summary
Acme trades at $1.57 per share.

### Financial Health
The company carries a market capitalization of $16.8 billion.

### Recent Developments
It is headquartered in [City Name].

### Outlook
The lean is cautious.

---
*This brief is for informational purposes only and does not constitute financial advice.*
"""


def test_off_returns_brief_unchanged_and_no_report():
    out, report = nc.apply_numeric_check(BRIEF, STOCK, "off")
    assert out == BRIEF and report is None


def test_warn_appends_note_and_keeps_brief_as_prefix():
    out, report = nc.apply_numeric_check(BRIEF, STOCK, "warn")
    assert out.startswith(BRIEF)
    note = out[len(BRIEF):]
    assert "**Numeric check**" in note and "2 issue(s)" in note
    assert "market cap stated $16.8 billion, stock data $168.3M (99.8x)" in note
    assert 'unfilled placeholder "[City Name]"' in note
    assert report["mode"] == "warn" and report["mismatches"] == 1
    assert report["placeholders"] == 1 and "bindings" not in report


def test_block_replaces_only_mismatched_sections():
    out, report = nc.apply_numeric_check(BRIEF, STOCK, "block")
    assert "market capitalization of $16.8 billion" not in out.split("---")[0]
    assert "### Financial Health\n\n" + nc.BLOCK_NOTICE in out
    assert "Acme trades at $1.57 per share." in out          # untouched
    assert "headquartered in [City Name]" in out              # placeholder: noted, not blocked
    assert "**Numeric check**" in out
    assert report["blocked_sections"] == ["Financial Health"]


def test_clean_brief_unchanged_in_every_mode():
    clean = BRIEF.replace("$16.8 billion", "$168.3 million").replace(
        "[City Name]", "Berkeley")
    for mode in ("warn", "block"):
        out, report = nc.apply_numeric_check(clean, STOCK, mode)
        assert out == clean and report["findings"] == []


def test_mode_env(monkeypatch):
    monkeypatch.delenv("NUMERIC_CHECK", raising=False)
    assert nc.numeric_check_mode() == "warn"
    for m in ("off", "warn", "block"):
        monkeypatch.setenv("NUMERIC_CHECK", m.upper())
        assert nc.numeric_check_mode() == m
    monkeypatch.setenv("NUMERIC_CHECK", "loud")
    assert nc.numeric_check_mode() == "warn"


# --- pipeline wiring: no network, no LLM added --------------------------------

@pytest.fixture
def core(monkeypatch):
    """agent.core with every LLM, data fetch and cache call mocked, and
    LangSmith tracing off so the @traceable wrappers send nothing."""
    from langsmith import tracing_context

    import agent.core as core
    from agent import graph
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content=BRIEF)
    llm.stream.return_value = [MagicMock(content=BRIEF[:40]),
                               MagicMock(content=BRIEF[40:])]
    fetch = MagicMock(return_value=(STOCK, [], {}))
    cache_set = MagicMock()
    monkeypatch.setattr(core, "_synthesis_llm", llm)
    monkeypatch.setattr(core, "_parallel_sections", MagicMock(return_value=["s"]))
    monkeypatch.setattr(core, "fetch_research_data", fetch)
    monkeypatch.setattr(core, "get_cached_response", MagicMock(return_value=None))
    monkeypatch.setattr(core, "set_cached_response", cache_set)
    monkeypatch.setattr(graph, "multi_agent_enabled", lambda: False)
    core._mocks = {"llm": llm, "fetch": fetch, "cache_set": cache_set}
    with tracing_context(enabled=False):
        yield core


@pytest.mark.parametrize("mode", ["off", "warn", "block"])
def test_run_research_checked_modes(core, monkeypatch, mode):
    monkeypatch.setenv("NUMERIC_CHECK", mode)
    out = core.run_research_checked("ACME")
    m = core._mocks
    assert m["fetch"].call_count == 1 and m["llm"].invoke.call_count == 1
    if mode == "off":
        assert out == {"brief": BRIEF, "numeric_check": None}
    else:
        assert out["numeric_check"]["mismatches"] == 1
        assert "**Numeric check**" in out["brief"]
        assert (nc.BLOCK_NOTICE in out["brief"]) is (mode == "block")
    m["cache_set"].assert_called_once_with(
        "ACME", out["brief"], numeric_check=out["numeric_check"])
    assert core.run_research("ACME") == out["brief"]


def test_run_research_checked_cache_hit_returns_stored_report(core, monkeypatch):
    stored = {"findings": [], "mode": "warn"}
    monkeypatch.setattr(core, "get_cached_response", MagicMock(
        return_value={"result": "cached", "ticker": "ACME", "cache_hit": True,
                      "numeric_check": stored}))
    assert core.run_research_checked("ACME") == {"brief": "cached",
                                                 "numeric_check": stored}
    assert core._mocks["fetch"].call_count == 0


def test_stream_synthesis_warn_streams_then_appends_note(core, monkeypatch):
    monkeypatch.setenv("NUMERIC_CHECK", "warn")
    chunks = list(core.stream_synthesis("ACME", STOCK, [], {}))
    assert chunks[:2] == [BRIEF[:40], BRIEF[40:]]
    assert len(chunks) == 3 and chunks[2].lstrip().startswith("---")


def test_stream_synthesis_block_yields_once(core, monkeypatch):
    monkeypatch.setenv("NUMERIC_CHECK", "block")
    chunks = list(core.stream_synthesis("ACME", STOCK, [], {}))
    assert len(chunks) == 1 and nc.BLOCK_NOTICE in chunks[0]


def test_stream_synthesis_off_is_unchanged(core, monkeypatch):
    monkeypatch.setenv("NUMERIC_CHECK", "off")
    assert "".join(core.stream_synthesis("ACME", STOCK, [], {})) == BRIEF


# --- injections (eval/perturb.py) --------------------------------------------

INJ_STOCK = dict(STOCK, revenue=10.0e9)
CLEAN = [("Financial Health",
          "Acme trades at $1.57 with a market capitalization of $168.3 million "
          "and $10.0 billion in annual revenue, a 45.3% profit margin and a "
          "forward P/E of -1.2x.")]


@pytest.mark.parametrize("kind", ["x10", "x100", "x0.01", "sign_flip",
                                  "swap_fields", "unit_down", "placeholder"])
def test_every_injection_is_detected_on_a_clean_brief(kind):
    base = nc.check_sections(CLEAN, INJ_STOCK)
    assert base["findings"] == []
    for seed in range(5):
        inj = inject_numeric(CLEAN, base["bindings"], kind, random.Random(seed))
        assert inj is not None
        if kind == "placeholder" and inj["token"] in ("TBD", "XX", "[●]", "N/A"):
            continue  # tokens the detector is known not to cover in this slot
        r = nc.check_sections(inj["sections"], INJ_STOCK)
        assert nb._detected(inj, r), (kind, seed, inj["note"])


def test_swap_skips_the_two_ends_of_a_range():
    secs = [("Financial Health", "The 52-week range ($1.38-$3.54) is wide.")]
    base = nc.check_sections(secs, STOCK)
    assert inject_numeric(secs, base["bindings"], "swap_fields", random.Random(0)) is None


# --- backtest bookkeeping (scripts/numeric_backtest.py) ----------------------

def test_run_labels_lsnnc_is_the_fine_tune_and_separate_from_v924f(monkeypatch):
    monkeypatch.chdir(REPO)
    raw = pathlib.Path("eval/runs/raw")  # relative on purpose (was a crash)
    ls = nb.load_brief(raw / "lsnnc-findings" / "CRBU_local-model.md", raw)
    v9 = nb.load_brief(raw / "v924f-findings" / "CRBU_local-model.md", raw)
    assert (ls["run"], ls["model"]) == ("lsnnc", "financial-lora")
    assert (v9["run"], v9["model"]) == ("v924f", "financial-lora")
    assert "2026-09-05/06" in nb.RUN_INFO["lsnnc"]["label"]


def _brief(run, prewritten, text, ticker="ACME"):
    return {"run": run, "arm": "baseline", "model": "hosted", "ticker": ticker,
            "stock": STOCK, "sections": [("Financial Health", text)],
            "has_prewritten": prewritten}


def test_partial_runs_listed_separately_and_kept_out_of_arm_rates():
    bad = "It has a market capitalization of $16.8 billion."
    good = "It trades at $1.57 with a market cap of $168.3 million."
    briefs = [_brief("full1", True, bad), _brief("full1", True, good, "B"),
              _brief("part1", False, bad)]
    summary, rows = nb.backtest(briefs)
    assert summary["partial_runs"] == ["part1"]
    assert summary["run"]["part1"]["scope"].startswith("partial")
    assert summary["arm"]["baseline"]["runs"] == ["full1"]
    assert summary["arm"]["baseline"]["briefs"] == 2
    assert summary["all_full"]["briefs_flagged"] == 1
    rate = summary["arm"]["baseline"]["mismatches_per_checked"]
    assert (rate["k"], rate["n"]) == (1, 3)  # one wrong of three checked
    assert {r["run"]: r["scope"] for r in rows} == {"full1": "full", "part1": "partial"}


def _adj(run, scope, verdict, arm="baseline", model="hosted"):
    return {"id": "1", "run": run, "scope": scope, "arm": arm, "model": model,
            "verdict": verdict}


def test_precision_reported_two_ways_for_other_defect():
    rows = [_adj("r", "full", v) for v in
            ("TRUE_ERROR", "TRUE_ERROR", "FALSE_POSITIVE", "OTHER_DEFECT", "")]
    rows.append(_adj("p", "partial", "FALSE_POSITIVE"))
    res = nb.precision(rows)
    a = res["arm"]["baseline"]
    assert (a["TRUE_ERROR"], a["FALSE_POSITIVE"], a["OTHER_DEFECT"], a["unlabeled"]) == (2, 1, 1, 1)
    assert (a["precision_other_defect_as_tp"]["k"], a["precision_other_defect_as_tp"]["n"]) == (3, 4)
    assert (a["precision_other_defect_excluded"]["k"], a["precision_other_defect_excluded"]["n"]) == (2, 3)
    assert res["run"]["p"]["FALSE_POSITIVE"] == 1 and res["all_full"]["rows"] == 5


def test_precision_rejects_unknown_verdicts():
    with pytest.raises(ValueError):
        nb.precision([_adj("r", "full", "MAYBE")])
    assert set(nb.VERDICTS) == {"TRUE_ERROR", "FALSE_POSITIVE", "OTHER_DEFECT"}


# --- cluster bootstrap and fine-tune comparisons -----------------------------

def test_cluster_bootstrap_is_seeded_and_wider_than_wilson_when_clustered():
    from eval.stats import wilson_interval
    # 4 briefs with every number wrong, 36 with none: 40/400 = 10%.
    run = [(10, 10)] * 4 + [(0, 10)] * 36
    a = nb.cluster_bootstrap_ci([run], draws=2000, seed=42)
    b = nb.cluster_bootstrap_ci([run], draws=2000, seed=42)
    assert a == b
    lo, hi = a["ci95"]
    wlo, whi = wilson_interval(40, 400)
    assert lo <= 0.10 <= hi
    assert (hi - lo) > 2 * (whi - wlo)


def test_cluster_bootstrap_zero_events_is_degenerate():
    assert nb.cluster_bootstrap_ci([[(0, 5)] * 10], draws=500)["ci95"] == [0.0, 0.0]


def test_bootstrap_difference_paired_by_ticker():
    a = {f"T{i}": (1, 10) for i in range(30)}
    d = nb.bootstrap_difference(a, dict(a), draws=1000)
    assert d["paired_by_ticker"] and d["difference"] == 0
    assert not d["excludes_zero"] and d["ci95"] == [0.0, 0.0]
    hi = {t: (6, 10) for t in a}
    d = nb.bootstrap_difference(hi, a, draws=1000)
    assert d["excludes_zero"] and d["difference"] == pytest.approx(0.5)


def _runs(rates):
    out = []
    for run, k in rates.items():
        for i in range(30):
            out.append({"run": run, "ticker": f"T{i}", "counts": (k if i % 2 else 0, 10)})
    return out


def test_w4a16_separable_only_against_both_bf16_runs():
    sep = nb.fine_tune_comparisons(_runs({"lsnnc": 2, "v924f": 2, "r5nzh": 8}), draws=1000)
    assert sep["w4a16_vs_bf16_separable"] and "IS separable" in sep["statement"]
    # r5nzh sits with one BF16 run, not the other: not separable.
    mixed = nb.fine_tune_comparisons(_runs({"lsnnc": 8, "v924f": 2, "r5nzh": 8}), draws=1000)
    assert not mixed["w4a16_vs_bf16_separable"]
    assert "is not separable from run-to-run variation" in mixed["statement"]
    assert "two BF16 runs themselves differ" in mixed["statement"]
