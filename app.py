import streamlit as st
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
from agent.tools.stock import get_price_history, get_stock_data
from agent.tools.news import get_company_news
from agent.tools.sec import get_sec_filings
from agent.core import stream_synthesis
from cache import get_cached_response

st.set_page_config(
    page_title="Financial Research Agent",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Financial Research Agent")
st.caption("Powered by Claude AI — Enter a stock ticker to generate an investment brief")

ticker = st.text_input(
    "Stock Ticker",
    placeholder="e.g. AAPL, TSLA, NVDA",
    max_chars=10
).upper().strip()

if st.button("Generate Brief", type="primary", disabled=not ticker):

    # Price chart
    with st.spinner("Fetching price data..."):
        try:
            history = get_price_history.invoke({"ticker": ticker})
            if "error" not in history:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history["dates"],
                    y=history["prices"],
                    mode="lines",
                    line=dict(color="#1f77b4", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(31, 119, 180, 0.1)"
                ))
                change = history["change_pct"]
                color = "green" if change >= 0 else "red"
                fig.update_layout(
                    title=f"{ticker} — 12 Month Price History  "
                          f"<span style='color:{color}'>({'+' if change >= 0 else ''}{change}%)</span>",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    height=350,
                    margin=dict(l=0, r=0, t=40, b=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)")
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load price chart: {str(e)}")

    # Investment brief
    cached = get_cached_response(ticker)
    if cached:
        st.markdown(cached["result"])
    else:
        try:
            # Data fetch phase — show live status so the user isn't staring at a blank screen
            with st.status("Gathering data...", expanded=True) as status:
                status.write("📊 Fetching stock data...")
                stock_data = get_stock_data.invoke({"ticker": ticker})
                company_name = stock_data.get("company_name", ticker)

                status.write("📰 Fetching news and SEC filings...")
                with ThreadPoolExecutor(max_workers=2) as executor:
                    f_news = executor.submit(get_company_news.invoke, {"company_name": company_name})
                    f_sec = executor.submit(get_sec_filings.invoke, {"ticker": ticker})
                    news_data = f_news.result()
                    sec_data = f_sec.result()

                status.update(label="Data ready — generating brief...", state="complete", expanded=False)

            # LLM phase — stream tokens directly to the page as they arrive
            st.write_stream(stream_synthesis(ticker, stock_data, news_data, sec_data))

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("⚠️ This tool is for informational purposes only and does not constitute financial advice.")
