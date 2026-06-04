import yfinance as yf
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional


class StockData(BaseModel):
    ticker: str
    company_name: str
    current_price: Optional[float] = None
    currency: str = "USD"
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    profit_margin: Optional[float] = None
    dividend_yield: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None


class PriceHistory(BaseModel):
    ticker: str
    dates: list[str]
    prices: list[float]
    start_price: float
    end_price: float
    change_pct: float


@tool
def get_stock_data(ticker: str) -> dict:
    """
    Fetches current stock price, key financials, and company info
    for a given ticker symbol. Use this to get quantitative financial
    data about a company.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        data = StockData(
            ticker=ticker.upper(),
            company_name=info.get("longName", "N/A"),
            current_price=info.get("currentPrice"),
            currency=info.get("currency", "USD"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE"),
            forward_pe=info.get("forwardPE"),
            week_52_high=info.get("fiftyTwoWeekHigh"),
            week_52_low=info.get("fiftyTwoWeekLow"),
            revenue=info.get("totalRevenue"),
            net_income=info.get("netIncomeToCommon"),
            profit_margin=info.get("profitMargins"),
            dividend_yield=info.get("dividendYield"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            summary=info.get("longBusinessSummary"),
        )

        return data.model_dump()

    except Exception as e:
        return {"error": f"Failed to fetch stock data for {ticker}: {str(e)}"}


@tool
def get_price_history(ticker: str) -> dict:
    """
    Fetches 12 months of historical closing prices for a given ticker.
    Use this to provide price trend context in the investment brief.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        if hist.empty:
            return {"error": f"No price history found for {ticker}"}

        dates = hist.index.strftime("%Y-%m-%d").tolist()
        prices = [round(float(p), 2) for p in hist["Close"].tolist()]

        data = PriceHistory(
            ticker=ticker.upper(),
            dates=dates,
            prices=prices,
            start_price=prices[0],
            end_price=prices[-1],
            change_pct=round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)
        )

        return data.model_dump()

    except Exception as e:
        return {"error": f"Failed to fetch price history for {ticker}: {str(e)}"}