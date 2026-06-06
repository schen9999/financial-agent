# 📈 Financial Research Agent

An AI agent that researches stocks and generates structured investment briefs using live financial data, news, and SEC filings.

**Live Demo:** [financial-research-agent.streamlit.app](https://financial-research-agent.streamlit.app)

---

## What It Does

Enter a stock ticker and the agent:
1. Fetches live price data and key financials (yfinance)
2. Retrieves recent news articles about the company (NewsAPI)
3. Downloads and parses the latest SEC 10-K and 10-Q filings (SEC EDGAR)
4. Synthesizes everything into a structured investment brief using Claude AI

Data sources are fetched in parallel and fed into a single LLM synthesis call, keeping response time around 30–45 seconds.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude Sonnet (Anthropic API via LangChain) |
| Financial data | yfinance |
| News | NewsAPI |
| SEC filings | SEC EDGAR REST API |
| RAG | LlamaIndex + Pinecone + HuggingFace embeddings |
| Semantic cache | Redis (cosine similarity on brief embeddings) |
| Persistence | PostgreSQL via SQLAlchemy |
| Async tasks | Celery + Redis |
| REST API | FastAPI |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Architecture

```
User enters ticker
       │
       ▼
 Redis semantic cache ──hit──► return cached brief
       │ miss
       ▼
┌─────────────────────────────┐
│  get_stock_data             │  (sequential — company name needed for news)
└─────────────────────────────┘
       │
       ▼
┌──────────────────┐  ┌──────────────────┐
│  get_company_news│  │  get_sec_filings  │  (parallel)
└──────────────────┘  └──────────────────┘
       │                      │
       └──────────┬───────────┘
                  ▼
         Claude LLM synthesis
                  │
                  ▼
         Investment brief ──► Redis cache + PostgreSQL
```

The FastAPI layer also exposes async research jobs via Celery, allowing non-blocking research requests with status polling.

---

## Project Structure

```
financial-agent/
├── agent/
│   ├── core.py            # Parallel fetch + LLM synthesis
│   └── tools/
│       ├── stock.py       # yfinance wrapper
│       ├── news.py        # NewsAPI wrapper
│       ├── sec.py         # SEC EDGAR API client
│       └── rag.py         # LlamaIndex RAG with Pinecone vector store
├── app.py                 # Streamlit frontend
├── api.py                 # FastAPI REST API
├── cache.py               # Redis semantic cache
├── database.py            # PostgreSQL persistence (SQLAlchemy)
├── celery_worker.py       # Celery async task worker
├── tests/
├── requirements.txt
└── .env.example
```

---

## Running Locally

**1. Clone and install**
```bash
git clone https://github.com/schen9999/financial-agent.git
cd financial-agent
pip install -r requirements.txt
```

**2. Add API keys**

Copy `.env.example` to `.env` and fill in your keys:
```
ANTHROPIC_API_KEY=
NEWS_API_KEY=
REDIS_URL=
DATABASE_URL=
PINECONE_API_KEY=
```

| Key | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) |
| `REDIS_URL` | [upstash.com](https://upstash.com) (free tier) or local Redis |
| `DATABASE_URL` | PostgreSQL connection string |
| `PINECONE_API_KEY` | [pinecone.io](https://pinecone.io) (free tier) |

**3. Run the Streamlit app**
```bash
streamlit run app.py
```

**4. Run the FastAPI server (optional)**
```bash
uvicorn api:app --reload
```

**5. Run the Celery worker (optional, for async jobs)**
```bash
celery -A celery_worker worker --loglevel=info
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/stock/{ticker}` | Live stock data |
| `GET` | `/stock/{ticker}/history` | 12-month price history |
| `POST` | `/research` | Generate brief (synchronous) |
| `POST` | `/research/async` | Submit research job (returns job ID) |
| `GET` | `/research/status/{job_id}` | Poll async job status |
| `GET` | `/history/{ticker}` | Past briefs for a ticker |
| `GET` | `/history` | 10 most recent briefs |

---

## Example Output

```
## NVDA (NVDA) — Investment Brief

### Executive Summary
...

### Financial Health
...

### Recent Developments
...

### SEC Filing Highlights
...

### Risk Factors
...

### Outlook
...
```

---

## Disclaimer

This tool is for informational purposes only and does not constitute financial advice.
