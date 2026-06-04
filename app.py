import streamlit as st
import plotly.graph_objects as go
from agent.core import run_research
from agent.tools.stock import get_price_history

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
    with st.spinner(f"Researching {ticker}... this may take 30-60 seconds"):
        try:
            result = run_research(ticker)
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("⚠️ This tool is for informational purposes only and does not constitute financial advice.")