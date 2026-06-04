from agent.tools.stock import get_stock_data, get_price_history
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings


def test_stock_data_returns_expected_keys():
    result = get_stock_data.invoke({"ticker": "AAPL"})
    assert "error" not in result
    assert "current_price" in result
    assert "market_cap" in result
    assert "ticker" in result


def test_stock_data_invalid_ticker():
    result = get_stock_data.invoke({"ticker": "INVALIDXYZ"})
    assert isinstance(result, dict)


def test_price_history_returns_data():
    result = get_price_history.invoke({"ticker": "AAPL"})
    assert "error" not in result
    assert "dates" in result
    assert "prices" in result
    assert len(result["dates"]) > 0


def test_price_history_change_pct():
    result = get_price_history.invoke({"ticker": "AAPL"})
    assert "change_pct" in result
    assert isinstance(result["change_pct"], float)


def test_sec_filings_returns_dict():
    result = get_sec_filings.invoke({"ticker": "AAPL"})
    assert isinstance(result, dict)