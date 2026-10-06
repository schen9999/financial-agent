#!/usr/bin/env python3
"""Each ticker's listing and reporting currency, from yfinance.

The stock-data fix (2026-10) carries yfinance `financialCurrency` into the
stock dict as `financial_currency`. This reads it, with `currency` (the
listing's trading currency), for every ticker of a ticker file, so a run
can be preflighted and the runs before the fix can be checked with the
same currency rule (scripts/numeric_backtest.py --financial-currency).

One yfinance info request per ticker, from wherever it runs; run it from
the api pod so the request leaves from the cluster's egress IP, as the eval
pods' do (yfinance has answered 429 there; a failed ticker is recorded, not
retried):

  kubectl -n financial-agent exec deploy/api -- \\
      python scripts/financial_currency_preflight.py > eval/runs/financial-currency-<date>.json
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

DEFAULT_TICKERS = Path(__file__).resolve().parents[1] / "eval" / "tickers_extended.txt"


def read_tickers(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        t = line.split("#", 1)[0].strip()
        if t:
            out.append(t.upper())
    return out


def currencies(info: dict) -> dict:
    return {"currency": info.get("currency"), "financialCurrency": info.get("financialCurrency")}


def collect(tickers: list[str], fetch) -> dict:
    """{ticker: {currency, financialCurrency} | {error}} via fetch(ticker) -> info."""
    out = {}
    for t in tickers:
        try:
            out[t] = currencies(fetch(t))
        except Exception as e:  # noqa: BLE001 — recorded per ticker, never fatal
            out[t] = {"error": f"{type(e).__name__}: {str(e)[:200]}"}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tickers", type=Path, default=DEFAULT_TICKERS)
    args = ap.parse_args(argv)
    import yfinance as yf
    tickers = read_tickers(args.tickers)
    result = collect(tickers, lambda t: yf.Ticker(t).info)
    differ = sorted(t for t, v in result.items()
                    if v.get("financialCurrency") and v.get("currency")
                    and v["financialCurrency"] != v["currency"])
    print(json.dumps({
        "retrieved": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "yfinance Ticker.info: currency, financialCurrency",
        "tickers": result,
        "reporting_differs_from_listing": differ,
        "errors": sorted(t for t, v in result.items() if "error" in v),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
