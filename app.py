import streamlit as st
from agent.core import run_research

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
    with st.spinner(f"Researching {ticker}... this may take 30-60 seconds"):
        try:
            result = run_research(ticker)
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("⚠️ This tool is for informational purposes only and does not constitute financial advice.")