# 📈 Financial Research Agent

An AI agent that researches stocks and answers follow-up questions using live financial data, news, and SEC filings.

**Live Demo:** [financial-research-agent.streamlit.app](https://financial-research-agent.streamlit.app)

---

## What It Does

**Generate Brief** — enter a ticker and the app produces a structured investment brief:
1. Fetches stock data (yfinance), news (NewsAPI), and SEC filing summaries (EDGAR) — stock first, then news + SEC in parallel
2. Runs two concurrent Pinecone RAG queries to ground the SEC Filing Highlights and Risk Factors sections in actual filing text
3. Generates the four middle sections (Financial Health, Recent Developments, SEC Highlights, Risk Factors) in parallel using Claude Haiku
4. Streams the Executive Summary and Outlook from Claude Sonnet, which receives the pre-written sections as context
5. Caches the completed brief in Redis (semantic similarity) and PostgreSQL

**Ask a follow-up** — type a free-form question below the brief and a LangGraph ReAct agent answers it, selecting whichever tools it needs (stock data, news, SEC filings, or RAG search).

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM — section generation | Claude Haiku 4.5 (4 sections in parallel) |
| LLM — synthesis + ReAct agent | Claude Sonnet 4.6 (exec summary, outlook, /ask) |
| Agent framework | LangGraph `create_react_agent` |
| Financial data | yfinance |
| News | NewsAPI |
| SEC filings | SEC EDGAR REST API |
| SEC RAG | LlamaIndex + Pinecone + HuggingFace `bge-small-en-v1.5` |
| Semantic cache | Redis (cosine similarity on brief embeddings) |
| Persistence | PostgreSQL via SQLAlchemy |
| Async tasks | Celery + Redis |
| REST API | FastAPI |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## Architecture

### Brief pipeline

```
"Generate Brief"
       │
       ▼
Redis semantic cache ──hit──► cached brief
       │ miss
       ▼
get_stock_data  (yfinance — sequential, company name needed for news)
       │
       ▼
┌──────────────────┐  ┌─────────────────┐
│ get_company_news │  │ get_sec_filings  │  parallel
└──────────────────┘  └─────────────────┘
       │                       │
       └───────────┬───────────┘
                   │
       ┌───────────▼───────────┐
       │   Pinecone RAG (×2)   │  concurrent
       │  · SEC highlights     │
       │  · Risk factors       │
       └───────────┬───────────┘
                   │
   ┌───────────────┼───────────────────────┐
   ▼               ▼               ▼       ▼
Haiku           Haiku           Haiku   Haiku      4 parallel calls
Financial       Recent          SEC     Risk
Health          Developments    Highl.† Factors†   † RAG-grounded
   │               │               │       │
   └───────────────┴───────────────┴───────┘
                   │
       ┌───────────▼───────────┐
       │  Sonnet: Exec Summary │  streams to browser
       │  + Outlook            │
       └───────────┬───────────┘
                   │
       Redis cache + PostgreSQL
```

### Follow-up questions

```
"Ask" (free-form question)
       │
       ▼
LangGraph ReAct agent  (claude-sonnet-4-6)
  ├─ get_stock_data
  ├─ get_company_news
  ├─ get_sec_filings
  └─ query_sec_filing  (Pinecone RAG)
       │
       ▼
     answer
```

---

## Project Structure

```
financial-agent/
├── agent/
│   ├── core.py            # Brief pipeline: parallel fetch + Haiku sections + Sonnet stream
│   ├── react_agent.py     # LangGraph ReAct agent for follow-up questions
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
| `POST` | `/ask` | Answer a free-form question via ReAct agent |
| `GET` | `/history/{ticker}` | Past briefs for a ticker |
| `GET` | `/history` | 10 most recent briefs |

---

## Disclaimer

This tool is for informational purposes only and does not constitute financial advice.
