"""eval/stock_block.py + its aggregate count — briefs written with an empty
STOCK DATA block (a swallowed stock-fetch failure) are counted, never
silently passed as clean. Detection only: the gate is unchanged."""
import importlib.util
import json
import pathlib

import pytest

from eval.label import render_findings_md
from eval.stock_block import main, scan_findings_dir, stock_block_empty, stock_block_no_figures

_REPO = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "eval_aggregate", _REPO / "scripts" / "eval_aggregate.py")
eval_aggregate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eval_aggregate)


def _context(stock: dict) -> str:
    """The layout grounding_check.run_arm builds."""
    return "\n\n".join([
        f"STOCK DATA:\n{json.dumps(stock, indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps([{'title': 't'}], indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps({}, indent=2)}",
        "RAG — SEC HIGHLIGHTS:\n(not available)",
        "RAG — RISK FACTORS:\n(not available)",
    ])


def test_populated_block_is_not_empty():
    assert stock_block_empty(_context({"ticker": "AAPL", "current_price": 1.0})) is False


def test_empty_block_detected():
    assert stock_block_empty(_context({})) is True


def test_crlf_context():
    assert stock_block_empty(_context({}).replace("\n", "\r\n")) is True


@pytest.mark.parametrize("text", ["no stock block here",
                                  "STOCK DATA:\n{not json\n\nNEWS ARTICLES:\n[]"])
def test_missing_or_unparseable_is_unknown(text):
    assert stock_block_empty(text) is None


def test_no_figures_rule():
    # RDFN's block since 9j2dj: identifiers only, no quote from yfinance.
    ids_only = {"ticker": "RDFN", "company_name": "N/A", "currency": "USD",
                "financial_currency": "USD"}
    assert stock_block_empty(_context(ids_only)) is False
    assert stock_block_no_figures(_context(ids_only)) is True
    assert stock_block_no_figures(_context({})) is True
    assert stock_block_no_figures(_context({"ticker": "AAPL", "week_52_low": 1.0})) is False
    assert stock_block_no_figures("no stock block here") is None


def test_harness_layout_still_matches():
    # Drift guard without importing the harness (it mutates env at import):
    # run_arm must still emit the two labels this module keys on, in order.
    src = (_REPO / "grounding_check.py").read_text(encoding="utf-8")
    i = src.index('f"STOCK DATA:\\n{json.dumps(base[\'stock\'], indent=2)}"')
    assert src.index('f"NEWS ARTICLES:\\n', i) > i
    assert '"stock_block_empty": stock_empty' in src


def _write(d, ticker, stock):
    (d / f"{ticker}_baseline.md").write_text(
        render_findings_md(ticker, "baseline", "v2", _context(stock), "sec", "audit",
                           "CLAIM: \"x\"\nLABEL: SUPPORTED\nREASON: y"),
        encoding="utf-8")


def test_scan_findings_dir(tmp_path, capsys):
    _write(tmp_path, "AAPL", {"ticker": "AAPL"})
    _write(tmp_path, "TSLA", {})
    (tmp_path / "JUNK_baseline.md").write_text("not a findings file", encoding="utf-8")
    r = scan_findings_dir(tmp_path)
    assert r["files"] == 3
    assert r["empty"] == ["TSLA_baseline"]
    assert r["unknown"] == ["JUNK_baseline"]
    assert main([str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "TSLA_baseline" in out and "unknown (no parseable STOCK DATA block): JUNK_baseline" in out
    r = scan_findings_dir(tmp_path, stock_block_no_figures)
    assert r["empty"] == ["AAPL_baseline", "TSLA_baseline"]
    assert main(["--no-figures", str(tmp_path)]) == 0
    assert "Rule: no figures" in capsys.readouterr().out


def test_scan_per_ticker_subdirs(tmp_path):
    for t, stock in (("AAPL", {"ticker": "AAPL"}), ("TSLA", {})):
        (tmp_path / t).mkdir()
        _write(tmp_path / t, t, stock)
    r = scan_findings_dir(tmp_path)
    assert (r["files"], r["empty"], r["unknown"]) == (2, ["TSLA_baseline"], [])


def _row(ticker, **extra):
    return {"ticker": ticker, "supported": 5, "unsupported": 0, "inference": 0,
            "total": 5, "retrieval_s": 1.0, "pipeline_s": 2.0, **extra}


def _aggregate(monkeypatch, tmp_path, rows):
    f = tmp_path / "all.json"
    f.write_text(json.dumps([json.dumps({"results": rows, "skipped": []})]), encoding="utf-8")
    monkeypatch.delenv("EVAL_ARTIFACTS_PUT_URL", raising=False)
    captured = {}
    monkeypatch.setattr(eval_aggregate, "maybe_upload_artifacts",
                        lambda summary, results, skipped: captured.update(summary))
    monkeypatch.setattr(eval_aggregate.sys, "argv",
                        ["eval_aggregate.py", "--input", str(f), "--min-claims", "1"])
    eval_aggregate.main()  # gate still passes: detection never fails it
    return captured


def test_aggregate_counts_and_warns(monkeypatch, tmp_path, capsys):
    summary = _aggregate(monkeypatch, tmp_path, [
        _row("AAPL", stock_block_empty=False), _row("TSLA", stock_block_empty=True),
        _row("JPM", stock_block_empty=True)])
    out = capsys.readouterr().out
    assert "stock block empty : 2/3 (JPM, TSLA)" in out
    assert "WARNING: briefs above were written WITHOUT stock data" in out
    assert "GATE PASSED" in out
    assert summary["totals"]["stock_block_empty"] == 2
    assert summary["totals"]["stock_block_empty_tickers"] == ["JPM", "TSLA"]
    assert summary["totals"]["stock_block_unrecorded"] == 0


def test_aggregate_clean_run(monkeypatch, tmp_path, capsys):
    _aggregate(monkeypatch, tmp_path, [_row("AAPL", stock_block_empty=False)])
    out = capsys.readouterr().out
    assert "stock block empty : 0/1\n" in out
    assert "WITHOUT stock data" not in out


def test_aggregate_old_rows_are_unrecorded_not_clean(monkeypatch, tmp_path, capsys):
    summary = _aggregate(monkeypatch, tmp_path, [_row("AAPL"), _row("NVDA")])
    out = capsys.readouterr().out
    assert "stock block empty : 0/2   (2 row(s) unrecorded)" in out
    assert summary["totals"]["stock_block_unrecorded"] == 2
