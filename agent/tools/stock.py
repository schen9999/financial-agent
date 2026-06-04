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