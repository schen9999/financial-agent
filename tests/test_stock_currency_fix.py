"""The stock-data fix plus the currency-labelling prompt rule (2026-10):
financial_currency and profit_margin_pct in the stock dict, the rule in the
section context, the numeric check's currency_label finding, and the
backward compatibility that keeps every committed run reproducible."""
import importlib.util
import json
import pathlib

import pytest

from agent import core
from agent import numeric_check as nc
from agent.tools import stock as stock_tool

_REPO = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "financial_currency_preflight", _REPO / "scripts/financial_currency_preflight.py")
pre = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pre)

TM_INFO = {"longName": "Toyota Motor Corporation", "currentPrice": 181.49, "currency": "USD",
           "financialCurrency": "JPY", "marketCap": 214917464064.0,
           "totalRevenue": 51957024686080.0, "netIncomeToCommon": 4483796959232.0,
           "profitMargins": 0.0863}


class _FakeTicker:
    def __init__(self, info):
        self.info = info


def _fetch(monkeypatch, info, ticker="TM"):
    monkeypatch.setattr(stock_tool.yf, "Ticker", lambda t: _FakeTicker(info))
    return stock_tool.get_stock_data.invoke({"ticker": ticker})


# --- stock dict ------------------------------------------------------------------

def test_stock_dict_carries_reporting_currency_and_margin_as_percent(monkeypatch):
    d = _fetch(monkeypatch, TM_INFO)
    assert d["currency"] == "USD" and d["financial_currency"] == "JPY"
    assert d["revenue"] == 51957024686080.0 and d["profit_margin_pct"] == 8.63
    assert "profit_margin" not in d


def test_margin_above_one_hundred_percent_and_missing_fields(monkeypatch):
    d = _fetch(monkeypatch, {"longName": "Lucid", "profitMargins": -2.49214}, "LCID")
    assert d["profit_margin_pct"] == -249.21
    assert d["financial_currency"] is None
    d = _fetch(monkeypatch, {"longName": "X"}, "X")
    assert d["profit_margin_pct"] is None


# --- prompt rule -------------------------------------------------------------------

def test_currency_rule_only_for_a_foreign_reporter():
    trimmed = core._trim_stock(dict(_fetch_static(TM_INFO), summary="long"))
    assert trimmed["financial_currency"] == "JPY" and "summary" not in trimmed
    ctx = core._data_context(trimmed, [], {})
    assert "Currency rule: revenue and net_income are in JPY" in ctx
    assert "never with a $ sign" in ctx
    us = {"ticker": "AAPL", "currency": "USD", "financial_currency": "USD", "revenue": 1.0}
    assert core._currency_rule(us) == ""
    assert core._currency_rule({"ticker": "OLD", "currency": "USD", "revenue": 1.0}) == ""
    assert core._data_context(us, [], {}) == (
        f"Stock: {json.dumps(us)}\nNews: []\nSEC: {{}}")


def _fetch_static(info):
    return {"ticker": "TM", "company_name": info["longName"], "currency": info["currency"],
            "financial_currency": info["financialCurrency"], "revenue": info["totalRevenue"],
            "net_income": info["netIncomeToCommon"], "profit_margin_pct": 8.63}


# --- numeric check -------------------------------------------------------------------

OLD_TM = {"ticker": "TM", "company_name": "Toyota Motor Corporation", "currency": "USD",
          "revenue": 51957024686080.0, "net_income": 4483796959232.0, "profit_margin": 0.0863}
NEW_TM = {k: v for k, v in OLD_TM.items() if k != "profit_margin"}
NEW_TM.update(financial_currency="JPY", profit_margin_pct=8.63)


def _kinds(text, stock):
    r = nc.check_sections([("Financial Health", text)], stock)
    return r["checked"], [(f["kind"], f["stated"]) for f in r["findings"]]


@pytest.mark.parametrize("text,expected", [
    # the hosted 9jzmj figure and the CPU 8vpq6 faithful copy: both in dollars
    ("Toyota generates $52.0 billion in annual revenue.", [("currency_label", "$52.0 billion")]),
    ("Toyota generates $51.96 trillion in revenue.", [("currency_label", "$51.96 trillion")]),
    ("It generated 51.96 trillion USD in revenue.", [("currency_label", "51.96 trillion USD")]),
    # stated in the reporting currency: compared as usual
    ("Revenue of ¥51.96 trillion supports the business.", []),
    ("It reported revenue of JPY 51.96 trillion.", []),
    ("It generated 51.96 trillion yen in revenue.", []),
    ("Toyota posted ¥4.48 trillion in net income.", []),
    ("It generated 9.9 trillion yen in revenue.", [("mismatch", "9.9 trillion")]),
    # unmarked: compared as usual
    ("It generated revenue of 51.96 trillion.", []),
])
def test_currency_label_for_a_foreign_reporter(text, expected):
    checked, found = _kinds(text, NEW_TM)
    assert checked == 1 and found == expected


def test_old_dicts_are_checked_exactly_as_before():
    """No financial_currency: the faithful "$51.96 trillion" matches the
    field and passes, "$52.0 billion" is a plain mismatch, and a yen prefix
    is not bound — the behaviour every committed run was measured with."""
    assert _kinds("Toyota generates $51.96 trillion in revenue.", OLD_TM) == (1, [])
    assert _kinds("Toyota generates $52.0 billion in annual revenue.", OLD_TM) == (
        1, [("mismatch", "$52.0 billion")])
    assert _kinds("Revenue of ¥51.96 trillion supports the business.", OLD_TM) == (0, [])
    r = nc.check_sections([("S", "Revenue of $52.0 billion.")], OLD_TM)
    assert "currency_labels" not in r


def test_margin_from_the_percent_field():
    lcid_new = {"ticker": "LCID", "company_name": "Lucid", "profit_margin_pct": -249.21}
    lcid_old = {"ticker": "LCID", "company_name": "Lucid", "profit_margin": -2.49214}
    for stock in (lcid_new, lcid_old):
        assert _kinds("A net profit margin of -249.2% weighs.", stock) == (1, [])
        checked, found = _kinds("A net profit margin of -2.49% weighs.", stock)
        assert found == [("mismatch", "-2.49%")]
    r = nc.check_sections([("S", "A net profit margin of -2.49% weighs.")], lcid_new)
    assert r["findings"][0]["source_is_pct"] is True
    assert "stock data -249.2%" in nc.render_note(r["findings"])


def test_currency_label_note_and_block():
    r = nc.check_sections([("Financial Health", "Toyota generates $52.0 billion in annual revenue.")],
                          NEW_TM)
    assert r["currency_labels"] == 1 and r["mismatches"] == 0
    assert "revenue stated $52.0 billion in USD; the stock data reports it in JPY" in \
        nc.render_note(r["findings"])
    brief = "### Financial Health\nToyota generates $52.0 billion in annual revenue.\n"
    out, report = nc.apply_numeric_check(brief, NEW_TM, "block")
    assert report["blocked_sections"] == ["Financial Health"] and nc.BLOCK_NOTICE in out


# --- retroactive check and preflight ----------------------------------------------------

def test_retroactive_injection_flags_the_faithful_copy_in_8vpq6():
    from scripts import numeric_backtest as nb
    path = nb.RAW / "8vpq6-findings" / "TM_slm-full-cpu.md"
    brief = nb.load_brief(path, nb.RAW)
    before = nc.check_sections(brief["sections"], brief["stock"])
    assert not [f for f in before["findings"] if f["field"] == "revenue"]
    injected = nb.inject_financial_currency([brief], {"TM": "JPY", "AAPL": "USD"})
    assert injected == {"TM": "JPY"} and brief["stock"]["financial_currency"] == "JPY"
    after = nc.check_sections(brief["sections"], brief["stock"])
    labels = [f for f in after["findings"] if f["kind"] == "currency_label"]
    assert labels and all(f["stated_currency"] == "USD" for f in labels)
    assert any(f["stated"] == "$51.96 trillion" for f in labels)


def test_load_financial_currency_accepts_preflight_output_and_plain_maps(tmp_path):
    from scripts import numeric_backtest as nb
    p = tmp_path / "fx.json"
    p.write_text(json.dumps({"tickers": {"TM": {"currency": "USD", "financialCurrency": "JPY"},
                                         "X": {"error": "HTTPError: 429"}}}))
    assert nb.load_financial_currency(p) == {"TM": "JPY"}
    p.write_text(json.dumps({"TM": "JPY", "AAPL": "USD"}))
    assert nb.load_financial_currency(p) == {"TM": "JPY", "AAPL": "USD"}


def test_preflight_collects_per_ticker_and_records_failures():
    def fetch(t):
        if t == "BAD":
            raise RuntimeError("429 Too Many Requests")
        return {"currency": "USD", "financialCurrency": "JPY" if t == "TM" else "USD"}
    out = pre.collect(["TM", "AAPL", "BAD"], fetch)
    assert out["TM"] == {"currency": "USD", "financialCurrency": "JPY"}
    assert out["BAD"]["error"].startswith("RuntimeError")
    assert len(pre.read_tickers(pre.DEFAULT_TICKERS)) == 40
