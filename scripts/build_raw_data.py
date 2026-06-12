#!/usr/bin/env python3
"""Stage A of the LoRA dataset pipeline: harvest RAW, Claude-free research data.

Writes data/raw_research.jsonl — one JSON row per ticker:
    {
      "ticker", "company_name",
      "stock":  {trimmed stock dict from yfinance},
      "news":   [trimmed news list from NewsAPI],
      "sec_raw": {"10-K": <raw filing narrative or null>,
                  "10-Q": <raw filing narrative or null>}
    }

The SEC text comes from agent.tools.rag._fetch_filing_text — the raw 10-K/10-Q
narrative window straight off EDGAR — NOT from RAG-retrieved / Claude-summarized
chunks. Every field here is either a number, an API string, or raw filing text,
so the training inputs derived from it are genuinely Claude-free.

This runs locally (it needs the project's API keys + network). The Colab
notebook consumes the committed JSONL, so training never needs live keys.

Usage:
  python scripts/build_raw_data.py                       # default ticker list
  python scripts/build_raw_data.py --tickers AAPL MSFT   # subset
  python scripts/build_raw_data.py --limit 12            # first N of the list
"""
import os
import re
import sys
import json
import html
import time
import argparse
import requests
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from agent.tools.stock import get_stock_data
from agent.tools.news import get_company_news
from agent.core import _trim_stock, _trim_news

_HEADERS = {"User-Agent": "FinancialAgent agent@financial.com"}
_SECTION_CAP = 12000  # chars kept per extracted Item region

# Anchors for the two narrative sections we want as training targets. We take the
# LONGEST match-to-next-Item span, which selects the real section body over its
# short table-of-contents mention.
# End anchors require the *standard SEC item title* (not just the item number) so
# in-text references like "...see Part II, Item 8" don't prematurely truncate the
# section. These titles are fixed by SEC form rules, so they're reliable.
_RISK_START = r"item\s*1a[\.\)\s:]+\s*risk factors"
_RISK_END = [r"item\s*1b[\.\)\s:]+\s*unresolved", r"item\s*2[\.\)\s:]+\s*propert"]
_MDA_START = r"item\s*7[\.\)\s:]+\s*management.s discussion"
_MDA_END = [r"item\s*7a[\.\)\s:]+\s*quantitative", r"item\s*8[\.\)\s:]+\s*financial statement"]


def _cik(ticker: str) -> str | None:
    r = requests.get(
        f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&ticker={ticker}"
        f"&type=10-K&dateb=&owner=include&count=1&output=atom",
        headers=_HEADERS, timeout=15)
    t = r.text
    i = t.find("CIK=") + 4
    j = t.find("&", i)
    return t[i:j].zfill(10) if i > 4 and j > i else None


def _primary_doc_url(cik: str, form: str) -> str | None:
    r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=_HEADERS, timeout=15)
    recent = r.json().get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accs = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])
    for k, f in enumerate(forms):
        if f == form:
            return (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                    f"{accs[k].replace('-', '')}/{docs[k]}")
    return None


def _full_filing_text(ticker: str, form: str) -> str | None:
    """Fetch the FULL primary filing document and return HTML-stripped text."""
    cik = _cik(ticker)
    if not cik:
        return None
    url = _primary_doc_url(cik, form)
    if not url:
        return None
    r = requests.get(url, headers=_HEADERS, timeout=30)
    clean = re.sub(r"<[^>]+>", " ", r.text)
    clean = html.unescape(clean)  # decode &#8217; (apostrophe), &#160; etc. so anchors match
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean or None


def _extract_item(full: str, start_re: str, end_res: list[str]) -> str | None:
    """Pull the Item region: longest span from a start anchor to the next section
    header. Defaults to a full _SECTION_CAP window so a missed end-header still
    yields the body; the +1000 offset skips the intro so inline 'see Item 8'
    references in the first sentence can't truncate the span."""
    low = full.lower()
    best = ""
    for m in re.finditer(start_re, low):
        s = m.start()
        e = s + _SECTION_CAP  # full-window fallback
        for er in end_res:
            em = re.search(er, low[s + 1000:])
            if em:
                e = min(e, s + 1000 + em.start())
        seg = full[s:e]
        if len(seg) > len(best):
            best = seg
    return best[:_SECTION_CAP] if len(best) > 200 else None


def _fetch_sec_sections(ticker: str) -> dict:
    """Return {form, mda, risk_factors} extracted from the 10-K (10-Q fallback)."""
    for form in ("10-K", "10-Q"):
        try:
            full = _full_filing_text(ticker, form)
        except Exception:
            full = None
        time.sleep(0.3)
        if not full:
            continue
        mda = _extract_item(full, _MDA_START, _MDA_END)
        risk = _extract_item(full, _RISK_START, _RISK_END)
        if mda or risk:
            return {"form": form, "mda": mda, "risk_factors": risk}
    return {"form": None, "mda": None, "risk_factors": None}

DATA_DIR = Path(__file__).parent.parent / "data"
OUT_PATH = DATA_DIR / "raw_research.jsonl"

# Sector-diverse large/mid caps with reliably clean EDGAR filings.
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AMD", "INTC", "CRM",
    "JPM", "BAC", "WFC", "GS", "MS", "V", "MA", "AXP", "C", "SCHW",
    "JNJ", "PFE", "MRK", "ABBV", "LLY", "UNH", "CVS", "TMO", "ABT", "BMY",
    "WMT", "COST", "TGT", "HD", "LOW", "NKE", "MCD", "SBUX", "KO", "PEP",
    "XOM", "CVX", "COP", "SLB", "BA", "CAT", "GE", "HON", "UPS", "FDX",
    "DIS", "NFLX", "CMCSA", "T", "VZ", "ORCL", "IBM", "CSCO", "QCOM", "TXN",
    "PG", "CL", "KMB", "MO", "PM", "GILD", "AMGN", "DHR", "LIN", "NEE",
    "F", "GM", "DAL", "UAL", "MMM", "DE", "LMT", "RTX", "NOC", "GD",
]


def harvest(ticker: str) -> dict | None:
    """Fetch raw stock + news + filing text for one ticker. None if unusable."""
    stock_data = get_stock_data.invoke({"ticker": ticker})
    if not isinstance(stock_data, dict) or stock_data.get("error"):
        return None

    company = stock_data.get("company_name", ticker)
    news_data = get_company_news.invoke({"company_name": company})

    sec = _fetch_sec_sections(ticker)
    # Require at least one extracted Item region — the SEC sections need it.
    if not (sec.get("mda") or sec.get("risk_factors")):
        return None

    return {
        "ticker": ticker,
        "company_name": company,
        "stock": _trim_stock(stock_data),
        "news": _trim_news(news_data),
        "sec_raw": sec,  # {form, mda, risk_factors}
    }


def main():
    parser = argparse.ArgumentParser(description="Harvest raw research data for LoRA training.")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    parser.add_argument("--limit", type=int, default=None, help="Only the first N tickers.")
    parser.add_argument("--out", default=str(OUT_PATH))
    args = parser.parse_args()

    tickers = args.tickers[: args.limit] if args.limit else args.tickers
    DATA_DIR.mkdir(exist_ok=True)

    rows, failed = [], []
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] {ticker} ...", end=" ", flush=True)
        try:
            row = harvest(ticker)
        except Exception as e:
            row = None
            print(f"error: {type(e).__name__}", end=" ")
        if row:
            rows.append(row)
            s = row["sec_raw"]
            has = "+".join([k for k in ("mda", "risk_factors") if s.get(k)]) or "none"
            print(f"ok (news={len(row['news'])}, {s['form']} {has})", flush=True)
        else:
            failed.append(ticker)
            print("skipped (no usable data)", flush=True)
        time.sleep(0.2)

    with open(args.out, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\nWrote {len(rows)} rows to {args.out}")
    if failed:
        print(f"Skipped {len(failed)}: {', '.join(failed)}")


if __name__ == "__main__":
    main()
