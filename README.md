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
| Reranking (optional) | Cross-encoder `BAAI/bge-reranker-base` (CPU, two-stage retrieval) |
| Observability | LangSmith tracing (tool calls, tokens, latency, cost) |
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
│   ├── tracing.py        # LangSmith setup + traceable decorator (env-aliased)
│   └── tools/
│       ├── stock.py       # yfinance wrapper
│       ├── news.py        # NewsAPI wrapper
│       ├── sec.py         # SEC EDGAR API client
│       ├── rag.py         # LlamaIndex RAG with Pinecone vector store
│       └── reranker.py    # Cross-encoder reranking (two-stage retrieval)
├── app.py                 # Streamlit frontend
├── api.py                 # FastAPI REST API
├── cache.py               # Redis semantic cache (BYPASS_CACHE for evals)
├── database.py            # PostgreSQL persistence (SQLAlchemy)
├── celery_worker.py       # Celery async task worker
├── grounding_check.py     # LLM-as-judge eval with reranking A/B arms
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

## Two-Stage Retrieval with Reranking

The SEC RAG pipeline supports an optional cross-encoder reranking stage. When
enabled, stage 1 over-retrieves a larger candidate pool from Pinecone (default
20), and a CPU-friendly cross-encoder (`BAAI/bge-reranker-base`) rescores the
candidates and passes only the top-N (default 3) to generation:

```
question ─► Pinecone vector search (top-20) ─► cross-encoder rerank ─► top-3 ─► LLM
```

Reranking is gated behind a flag so it can be A/B compared. With it **off**
(the default), retrieval is the original single-stage top-3 cosine search and
every existing path — Streamlit, Redis cache, Celery — behaves exactly as
before. Retrieval latency is logged on every query with the mode made explicit:

```
[rag] retrieval reranking=OFF 0.21s candidates=3 top_n=3
[rag] retrieval reranking=ON  0.68s candidates=20 top_n=3
```

| Env var | Default | Meaning |
|---|---|---|
| `RERANKING_ENABLED` | `false` | Turn the reranking stage on/off |
| `RERANK_CANDIDATES` | `20` | Stage-1 over-retrieval pool (top-k) |
| `RERANK_TOP_N` | `3` | Final chunks passed to generation |
| `RERANK_MODEL` | `BAAI/bge-reranker-base` | Cross-encoder model (CPU) |

The reranker model loads lazily and is cached — nothing is downloaded or held
in memory unless reranking is actually enabled.

## Observability (LangSmith)

Every agent run is traced with LangSmith: tool calls, retrieval results,
prompts, completions, token counts, latency, and cost per request. Traces are
tagged by request type (`full_brief` vs. `follow_up` vs. `rag_retrieval`) and by
model (Haiku vs. Sonnet), and async Celery runs carry an `async` tag.

The API key is read from the environment like every other secret — both
`LANGSMITH_API_KEY` and the legacy `LANGCHAIN_API_KEY` names are accepted. When
tracing is disabled or no key is present, the `traceable` instrumentation is a
near-zero-overhead pass-through, so nothing changes for local runs.

```
LANGSMITH_API_KEY=...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=financial-agent
```

## Evaluation: Reranking A/B

`grounding_check.py` runs the LLM-as-judge grounding suite across four retrieval
arms and prints a comparison table. The judge (Sonnet, temperature 0) audits
every quantitative and forward-looking claim in the Executive Summary and
Outlook and labels it `SUPPORTED` / `UNSUPPORTED` / `INFERENCE`. The headline
comparison holds the final chunk count constant (baseline top-3 vs.
retrieve-20→rerank→top-3); a **plain top-5 (no rerank)** arm isolates added
context from reranking, and a rerank→5 arm tests added context *with* reranking.
The Redis semantic cache is bypassed (`BYPASS_CACHE=true`) so no arm returns
another arm's cached brief, and per-claim judge findings (with retrieved source
context) are persisted to `eval_findings/` for auditing.

```bash
python grounding_check.py                                  # 10 tickers, all 4 arms
python grounding_check.py --arms baseline rerank3
```

### Results

All 10 tickers, every arm. `Unsupported%` is the hallucination-risk metric;
`Grounding%` is `SUPPORTED / total claims`. Latencies are per-ticker means.

| Arm | Claims | Grounding (SUP) | Unsupported | Inference | Retrieval | Pipeline |
|---|---:|---:|---:|---:|---:|---:|
| Baseline (top-3, no rerank) | 66 | 92.4% | 0.0% | 7.6% | 4.11 s | 25.25 s |
| Plain top-5 (no rerank) | 74 | 86.5% | **1.4%** | 12.2% | 4.46 s | 25.39 s |
| Rerank 20→3 (headline) | 84 | 78.6% | 0.0% | 21.4% | 20.65 s | 41.54 s |
| Rerank 20→5 | 69 | 85.5% | 0.0% | 14.5% | 20.44 s | 41.42 s |

**What the arms show:**

- **Hallucination (~0%) is controlled by the constrained synthesis prompt, not
  by retrieval depth or reranking.** It stays at zero across nearly every arm
  and is stable across repeated runs — retrieval changes don't move it.
- **The grounding ratio (78.6–92.4%) is run-to-run noisy** at synthesis
  temperature 0.2 and this eval scale. Across two full runs the same arm swung
  by ~10 points (e.g. rerank→5 was 95.2% in one run, 85.5% in the next), so the
  arm-to-arm differences sit *inside* the noise band and are not reliably
  interpretable as a ranking.
- **Reranking adds no grounding benefit over plain added context:** rerank→5
  (85.5%) ≈ plain top-5 (86.5%). Any top-5 effect is an added-context effect,
  not a reranking effect.
- **The single hallucination in the entire study came from the plain top-5 arm,
  not from any rerank arm** — added context, not reranking, introduced the only
  failure.
- **Reranking's only consistent effect is latency:** ~+16 s retrieval (4–5×
  baseline), worst on large filings (e.g. WMT ~50 s vs NVDA ~4 s). No grounding
  benefit justifies this cost.

**Conclusion:** reranking ships **default-off**. It does not reduce
hallucinations (already ~0%) and shows no reliable grounding gain over plain
top-k, while imposing a large latency penalty. The deliverable of value here is
the *measurement framework* — the A/B harness is what demonstrates the feature
isn't needed for this pipeline, rather than assuming it would help.

**Known limitations:**

- The grounding ratio is noisy at this claim count and synthesis temperature; a
  future run should lower the synthesis temperature and/or expand the claim set
  (more tickers, multiple briefs per ticker) before reading arm differences as
  signal.
- The judge rubric labels rounded numerics (e.g. "$840B" from a source
  market_cap of 839,999,946,752) as `INFERENCE` rather than `SUPPORTED`. This is
  conservative by design — it keeps `SUPPORTED` strictly verbatim — but it means
  `Grounding%` understates how much of each brief is trivially data-derived.

## LoRA Fine-Tuning Experiment

Can a small, locally-served open model match Haiku on section generation at lower
cost? This experiment fine-tunes **Qwen2.5-1.5B-Instruct** (Apache-2.0) with
QLoRA and benchmarks it as a drop-in for Haiku on the parallel section step.

**Scope.** The fine-tuned model serves **2 of the 4** sections — Financial
Health and Risk Factors — gated by `USE_LOCAL_MODEL` (default off). SEC Filing
Highlights and Recent Developments stay with Haiku: deterministic Claude-free
targets couldn't be built for them (MD&A figures are table-bound and flatten to
unusable number-soup; NewsAPI coverage is only ~18%). Sonnet synthesis is
untouched.

**Dataset (deterministic, Claude-free).** Training targets are built
*deterministically* from the project's own data — no LLM is called, so there's
no dependence on Claude outputs:

| Section | Builder | Coverage (78 tickers) |
|---|---|---|
| Financial Health | real figures into rotating templates | 100% |
| Risk Factors | risk-term + modal filtered sentences from Item 1A | 33% |

(SEC Filing Highlights was attempted via Item 7 MD&A extraction but dropped — for
large-caps the quantified results are entirely table-bound, leaving only
descriptive prose. That's a documented finding, not a gap to paper over.)

Two stages: `scripts/build_raw_data.py` harvests raw stock + raw 10-K Item 1A
text locally; the construction pipeline (`scripts/build_dataset.py`, mirrored
inline in the notebook) turns it into 104 instruction/target pairs.

**Training.** `fine_tune_financial.ipynb` (Colab T4): shows the construction
pipeline inline, halts for a 5-sample review, then QLoRA-trains (r=16, α=32,
all-linear targets, 4-bit NF4, gradient checkpointing, per-epoch checkpoints,
loss curve) and saves the adapter to `/adapters/financial-lora/`.

**Serving.** Merge adapter → GGUF (`q4_K_M`) → Ollama. `agent/tools/local_model.py`
wraps Ollama behind the same `.invoke(messages).content` interface as Haiku;
`USE_LOCAL_MODEL=true` routes the 2 trained sections to it.

**Benchmark.** A `local-model` arm in `grounding_check.py` reports grounding,
unsupported, and inference rates, latency, and an **honest hybrid cost**: the 2
local sections cost **$0.00**, while SEC Highlights and Recent Developments still
hit Haiku, versus all 4 sections on Haiku for the baseline.

```bash
# after training (Colab) + serving (ollama serve + model loaded):
python grounding_check.py --arms baseline rerank3 local-model \
    --tickers AAPL NVDA JPM MSFT XOM        # NVDA = extreme-figures outlier
```

> **Results pending the training run** — fill the `local-model` row from the
> benchmark output once the adapter is trained and served.

**Known limitations.** The experiment narrowed to 2 of 4 sections because
deterministic extraction can't produce grounded targets for the other two
(table-bound MD&A figures; sparse news) — an honest finding about the data, not
a shortcut. Risk Factors trained on **26/78 tickers (33%)**: the stricter
risk-term + modal filter trades coverage for quality (it excludes product/
service descriptions that merely mention a weak term like "loss"), the same
quality-over-quantity principle that dropped the other two sections. A 1.5B
model may reproduce the section *format* but
is more prone to figure errors than Haiku — which is exactly what the
grounding/unsupported metrics will measure; and CPU inference of the 2 local
sections is slower than the Haiku API, so the headline comparison is
**grounding-quality + cost**, not latency.

## Disclaimer

This tool is for informational purposes only and does not constitute financial advice.
