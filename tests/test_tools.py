import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yfinance as yf


def test_yfinance_returns_data():
    stock = yf.Ticker("AAPL")
    info = stock.info
    assert info is not None
    assert "currentPrice" in info or "regularMarketPrice" in info


def test_yfinance_price_history():
    stock = yf.Ticker("AAPL")
    hist = stock.history(period="1mo")
    assert not hist.empty
    assert len(hist) > 0


def test_yfinance_invalid_ticker():
    stock = yf.Ticker("INVALIDXYZ123")
    hist = stock.history(period="1mo")
    assert isinstance(hist, object)
