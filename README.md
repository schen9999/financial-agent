# 📈 Financial Research Agent

An autonomous AI agent that researches stocks and generates structured investment briefs using live financial data, news, and SEC filings.

**Live Demo:** [financial-research-agent.streamlit.app](https://financial-research-agent.streamlit.app)

---

## What It Does

Enter a stock ticker and the agent autonomously:
1. Fetches live price data and key financials (yfinance)
2. Retrieves recent news articles about the company (NewsAPI)
3. Downloads and parses the latest SEC 10-K and 10-Q filings (SEC EDGAR)
4. Synthesizes everything into a structured investment brief using Claude AI

The agent decides on its own which tools to call and in what order — no hardcoded pipeline.

---

## Tech Stack

- **LLM:** Anthropic Claude API with native tool use
- **Financial Data:** yfinance
- **News:** NewsAPI
- **SEC Filings:** SEC EDGAR REST API
- **Frontend:** Streamlit
- **Deployment:** Streamlit Cloud
- **Infrastructure:** Docker, GitHub Actions CI

---

## Project Structure

```
financial-agent/
├── agent/
│   ├── core.py           # Main agent loop with tool orchestration
│   └── tools/
│       ├── stock.py      # yfinance wrapper
│       ├── news.py       # NewsAPI wrapper
│       └── sec.py        # SEC EDGAR API client
├── app.py                # Streamlit frontend
├── tests/
├── requirements.txt
└── .env.example
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/schen9999/financial-agent.git
cd financial-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add API keys**

Copy `.env.example` to `.env` and fill in your keys:
```
ANTHROPIC_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

Get your keys at:
- Anthropic: [console.anthropic.com](https://console.anthropic.com)
- NewsAPI: [newsapi.org](https://newsapi.org)

**4. Run the app**
```bash
streamlit run app.py
```

---

## Example Output

The agent generates a full investment brief with:
- Executive Summary
- Financial Health (price, market cap, P/E, revenue, margins)
- Recent Developments
- SEC Filing Highlights
- Risk Factors
- Outlook

---

## Disclaimer

This tool is for informational purposes only and does not constitute financial advice.