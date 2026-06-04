import yfinance as yf
from langchain.tools import tool


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

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "net_income": info.get("netIncomeToCommon", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A"),
        }
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

        return {
            "ticker": ticker.upper(),
            "dates": dates,
            "prices": prices,
            "start_price": prices[0],
            "end_price": prices[-1],
            "change_pct": round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)
        }

    except Exception as e:
        return {"error": f"Failed to fetch price history for {ticker}: {str(e)}"}