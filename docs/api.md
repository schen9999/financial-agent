# API reference

The FastAPI app in [`api.py`](../api.py). FastAPI also serves an interactive,
generated reference of the same routes at `/docs` (Swagger UI) and the schema
at `/openapi.json` on any running instance (e.g. `http://localhost:30080/docs`
on kind, or `http://localhost:31080/docs` through the k3s ssh tunnel).

Tickers are case-insensitive; every route upper-cases them. There is no
authentication: on ECS the security group restricts access to one IP, and on
the k3s nodes the API is reachable only through an ssh tunnel.

Examples use `http://localhost:30080` (kind); substitute the base URL for
your target. Response values are abbreviated (`…`).

## Summary

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `GET` | `/stock/{ticker}` | Current quote, key financials, and company info |
| `GET` | `/stock/{ticker}/history` | 12 months of daily closing prices |
| `POST` | `/research` | Generate a full brief synchronously (cached per ticker) |
| `POST` | `/research/async` | Queue a brief on Celery; returns a job ID |
| `GET` | `/research/status/{job_id}` | Poll an async job |
| `POST` | `/ask` | Answer a free-form question with the ReAct agent |
| `GET` | `/history/{ticker}` | Saved briefs for one ticker |
| `GET` | `/history` | The 10 most recent saved briefs |

## `GET /health`

Response `200`: `{"status": "ok", "version": "1.0.0"}`

```bash
curl -s http://localhost:30080/health
```

## `GET /stock/{ticker}`

Response `200`: an object with `ticker`, `company_name`, `current_price`,
`currency`, `market_cap`, `pe_ratio`, `forward_pe`, `week_52_high`,
`week_52_low`, `revenue`, `net_income`, `profit_margin`, `dividend_yield`,
`sector`, `industry`, `summary` (from yfinance; any field may be `null`).
`404` with `{"detail": "Failed to fetch stock data for …"}` if the lookup fails.

```bash
curl -s http://localhost:30080/stock/aapl
# {"ticker": "AAPL", "company_name": "Apple Inc.", "current_price": …,
#  "currency": "USD", "market_cap": …, "pe_ratio": …, …, "summary": "…"}
```

## `GET /stock/{ticker}/history`

Response `200`: `{"ticker": str, "dates": [str "YYYY-MM-DD"], "prices": [float],
"start_price": float, "end_price": float, "change_pct": float}`, covering the
last year of daily closes. `404` if no history is found.

```bash
curl -s http://localhost:30080/stock/aapl/history
# {"ticker": "AAPL", "dates": ["…", …], "prices": [ …, … ],
#  "start_price": …, "end_price": …, "change_pct": …}
```

## `POST /research`

Request: `{"ticker": str}`. Response `200`: `{"ticker": str, "brief": str}`,
the brief as Markdown (Executive Summary, Financial Health, Recent
Developments, SEC Filing Highlights, Risk Factors, Outlook). The brief is
saved to PostgreSQL. A repeat request for the same ticker within 24 hours is
served from the exact-key Redis cache (`research:{TICKER}`). `500` with
`{"detail": "…"}` on any pipeline error. A cold request takes about 26 s
(numbers-of-record, pipeline latency).

```bash
curl -s -X POST http://localhost:30080/research \
     -H 'Content-Type: application/json' -d '{"ticker": "AAPL"}'
# {"ticker": "AAPL", "brief": "## Apple Inc. (AAPL) — Investment Brief\n\n### Executive Summary\n…"}
```

## `POST /research/async`

Request: `{"ticker": str}`. Response `200`:
`{"job_id": str, "status": "queued", "ticker": str}`. Requires the Celery
worker and Redis, which run on Kubernetes but not on ECS.

```bash
curl -s -X POST http://localhost:30080/research/async \
     -H 'Content-Type: application/json' -d '{"ticker": "NVDA"}'
# {"job_id": "…", "status": "queued", "ticker": "NVDA"}
```

## `GET /research/status/{job_id}`

Response `200`, one of:

| `status` | Extra fields | Meaning |
|---|---|---|
| `queued` | none | Not started (Celery `PENDING`) |
| `processing` | `meta`: `{"status": "Researching {ticker}..."}` | Running |
| `complete` | `result`: `{"status": "complete", "ticker": str, "brief": str}` | Done |
| `error` | `error`: str | The task failed, or its state could not be read |

```bash
curl -s http://localhost:30080/research/status/<job_id>
# {"job_id": "…", "status": "complete", "result": {"status": "complete", "ticker": "NVDA", "brief": "…"}}
```

## `POST /ask`

Request: `{"ticker": str, "question": str}`. Response `200`:
`{"ticker": str, "question": str, "answer": str}`. The ReAct agent chooses
among stock data, news, SEC filings, and RAG search. `500` with
`{"detail": "…"}` on error.

```bash
curl -s -X POST http://localhost:30080/ask -H 'Content-Type: application/json' \
     -d '{"ticker": "AAPL", "question": "What are the main risk factors in the latest 10-K?"}'
# {"ticker": "AAPL", "question": "What are the main risk factors…", "answer": "…"}
```

## `GET /history/{ticker}`

Response `200`: a list of `{"id": int, "ticker": str, "created_at": str
(ISO 8601), "brief": str}`, with each `brief` truncated to 500 characters plus
`...`. `404` with `{"detail": "No history found for …"}` if none exist.

```bash
curl -s http://localhost:30080/history/aapl
# [{"id": …, "ticker": "AAPL", "created_at": "…", "brief": "## Apple Inc. …..."}]
```

## `GET /history`

Response `200`: a list of up to 10 `{"id": int, "ticker": str, "created_at":
str}`, most recent first (no brief text).

```bash
curl -s http://localhost:30080/history
# [{"id": …, "ticker": "AAPL", "created_at": "…"}, …]
```
