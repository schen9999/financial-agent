# Phase 0 Audit — Repo State Before the K8s / Argo / vLLM Work

Date: 2026-08-24. Audited from code and config as committed at `b8ec9ab`, not from
the README's description of itself. This document gates the later phases: the
Kubernetes migration, Argo workflows, and vLLM serving are built against **this**
topology, and the flags and cache semantics below are preserved exactly.

---

## 1. Actual service topology

**There is no docker-compose file in this repo.** The deployable topology exists in
three distinct forms, none of which is a compose stack:

| Environment | What actually runs |
|---|---|
| Local dev | `streamlit run app.py` — the Streamlit process imports the agent **in-process** (`agent.core.stream_synthesis`); FastAPI is not involved. `api.py` and a Celery worker can be run separately by hand. |
| AWS (Terraform, `infra/`) | **One** FastAPI container on ECS Fargate + RDS PostgreSQL + Secrets Manager. No Redis service and no Celery worker are deployed: the cache degrades to a no-op (every call fails into the `except` fallback) and `/research/async` accepts jobs that no worker will ever pick up (they poll as `queued` forever). |
| Streamlit Cloud (live demo) | `app.py` in-process pipeline again — independent of the AWS footprint. |

Components as wired in code:

- **FastAPI** ([api.py](../api.py)) — sync `/research` (runs the pipeline in the request thread, saves to Postgres), `/research/async` (Celery `research_task.delay`), `/research/status/{job_id}`, `/ask` (ReAct agent), `/history`, `/health`, `/stock/*`. `init_db()` runs at import, so Postgres must be reachable at startup.
- **Celery worker** ([celery_worker.py](../celery_worker.py)) — one task, `research_task`; Redis is both broker and result backend. JSON serialization, `task_track_started`.
- **Redis** — two roles: exact-key brief cache ([cache.py](../cache.py)) and Celery broker/backend. Failure-tolerant on the cache path (falls through to the LLM), hard-required at import time (`REDIS_URL` unset raises).
- **PostgreSQL** ([database.py](../database.py)) — single table `research_briefs`, created via `Base.metadata.create_all` at API startup.
- **Streamlit UI** ([app.py](../app.py)) — **does not call the FastAPI**; it imports the agent and Redis cache directly. Any in-cluster Streamlit deployment therefore runs the full pipeline (embedding model included) in its own pod, unless the app is rewritten — which we are not doing (the live Streamlit Cloud app must stay untouched).
- **MCP server** ([mcp_server.py](../mcp_server.py)) — standalone FastMCP process reusing the LangChain tools; stdio transport by default, `MCP_TRANSPORT=streamable-http` for HTTP. Per-call wall-clock timeout `MCP_TOOL_TIMEOUT` (default 30s). Note: `mcp[cli]` is in `requirements.txt` but **not** in `requirements-api.txt`, so the ECS image cannot run it — a K8s MCP Service needs the full requirements set.
- **External dependencies** — Anthropic API (Haiku 4.5 sections + Sonnet 4.6 synthesis/judge/ReAct), NewsAPI, SEC EDGAR, yfinance, Pinecone (index `sec-filings`, namespace per ticker, 384-dim bge-small-en-v1.5), LangSmith (optional tracing), Ollama at `LOCAL_MODEL_URL` (optional local model).
- **Docker image** ([Dockerfile](../Dockerfile)) — `python:3.13-slim`, installs `requirements-api.txt`, bakes the bge-small embedding model into `/opt/hf-cache`, single uvicorn worker, healthcheck on `/health` with a 180s start period. Built for ECS; reused as the base pattern for the K8s images.

### 1a. Deployed vs. designed

Stated plainly: **the full FastAPI + Celery + Redis + Postgres topology has never run
as a complete deployment.** ECS runs a reduced single-container FastAPI deployment —
no Redis service, no Celery worker; the cache no-ops (every Redis call fails into the
best-effort fallback) and async jobs are accepted but never executed. Local dev runs
Streamlit in-process, also without a worker. The Phase 1 Kubernetes cluster is the
**first environment where the designed topology actually runs end-to-end**, which is
why the smoke test asserts a completed Celery task loudly rather than treating it as
routine.

**Live ECS routes that enqueue or poll Celery today (known-broken there):**

| Route | Behaviour on ECS today |
|---|---|
| `POST /research/async` ([api.py:115](../api.py#L115)) | Calls `research_task.delay()`. With no broker reachable, the publish either errors (500) or, if a stale `REDIS_URL` accepts connections, enqueues a job no worker will ever run. |
| `GET /research/status/{job_id}` ([api.py:125](../api.py#L125)) | Reports any unknown/never-run job as `queued` — indistinguishable from a real pending job, forever. |

These are **flagged as known-broken on ECS rather than disabled**: the README already
documents the reduction, removing them would change the public API surface for a
deployment being superseded by Phase 1, and both routes become genuinely functional in
the K8s cluster (which deploys the worker and Redis they require).

## 2. Feature flags (verified in code; all preserved as-is)

| Flag | Default | Read in | Meaning |
|---|---|---|---|
| `RERANKING_ENABLED` | `false` | `agent/tools/reranker.py` | Cross-encoder rerank stage. Default-off **by evidence**: the 4-arm eval showed 4–5x retrieval latency for no grounding gain. |
| `RERANK_CANDIDATES` / `RERANK_TOP_N` / `RERANK_MODEL` | `20` / `3` / `BAAI/bge-reranker-base` | reranker.py | Rerank stage config; read per-call so eval arms can toggle in-process. |
| `BASELINE_TOP_K` | `3` | reranker.py | Single-stage top-k (eval knob). |
| `USE_LOCAL_MODEL` | `false` | `agent/tools/local_model.py` | Routes the 2 trained sections (Financial Health, Risk Factors) to the local fine-tuned Qwen2.5-1.5B. Default-off: sections-only cost saving (the Phase 3 full-brief re-measure found no measurable total reduction — see benchmarks.md) at 85.4% vs 88.6% grounding as recorded at the time. |
| `LOCAL_MODEL_NAME` / `LOCAL_MODEL_URL` | `financial-lora` / `http://localhost:11434` | local_model.py | Which model/endpoint `LocalChat` hits (Ollama chat API). Phase 3's vLLM backend swaps in here. |
| `MULTI_AGENT_ENABLED` | `false` | `agent/graph.py` | Supervisor graph (planner→research→critic→supervisor). Default-off **by evidence**: +92% cost, +68% latency, null grounding benefit on this corpus. |
| `CRITIC_MAX_UNSUPPORTED_PCT` / `MAX_REVISIONS` | `5` / `2` | graph.py | Critic threshold and revision budget. |
| `BYPASS_CACHE` | unset (`false`) | `cache.py` | Eval-only: forces cache miss on read **and** skips writes so A/B arms can't cross-pollute. |
| `MCP_TRANSPORT` / `MCP_TOOL_TIMEOUT` | `stdio` / `30` | mcp_server.py | MCP transport and per-tool-call timeout. |
| `LANGSMITH_TRACING` (+`LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`; legacy `LANGCHAIN_*` accepted) | off unless set | `agent/tracing.py` | Observability. |
| (derived) `_RAG_ENABLED` | presence of `PINECONE_API_KEY` | `agent/core.py` | RAG sections silently fall back to raw data context without Pinecone. |

## 3. Redis cache semantics (confirmed, and deliberately preserved)

Exact-key lookup: `research:{TICKER}` (uppercased), `SETEX` with 24h TTL, JSON value
`{ticker, result}`. **Not semantic, on purpose** — the previous embedding-similarity scan
returned wrong-company briefs (the ticker was the only varying token in the embedded
text) and was replaced with the exact-key lookup at `ce04724`. Best-effort on both
paths: any Redis exception logs and falls through. The Phase 1 smoke test asserts an
exact-key hit and asserts a *different* ticker still misses.

## 4. Claimed-metric verification

| Claim | Verdict | Evidence |
|---|---|---|
| ~700 pytest lines | ✅ reproduces | 704 lines (`tests/*.py` 701 + root `conftest.py` 3); 41 tests, all pass locally in ~50s on Python 3.13.2. |
| 49% → 3% unsupported claims | ⚠️ half-verifiable *(fresh number below)* | The 49% is historical pre-fix behaviour and is **not re-runnable by design** — the fix (grounding rules in `_synthesis_prompt`) is now the only committed prompt. The current unsupported rate was re-measured today; see below. |
| $0.0269/brief (single-agent) | ⚠️ recorded, not re-runnable from committed code | The figure comes from the multi-agent A/B run (README table); the harness that computed full $/brief (Haiku sections + Sonnet synthesis + tokens) was never committed. The committed `grounding_check.py` reports **Haiku-only** cost/brief. Treat $0.0269 as a recorded historical measurement. |
| ~26s latency/brief | ✅ re-measured today | `grounding_check.py` `pipeline_s` (retrieval + sections + synthesis, excluding shared data fetch) — fresh number below. |
| Reranking 4-arm table, QLoRA 85.4%/88.6%, multi-agent +92%/+68% | ✅ recorded with per-claim artifacts | `eval_findings/` holds the per-ticker judge evidence for the reranking arms and local-model arm; README documents method + numbers. Not re-run today (they are A/B conclusions, not current-state claims). |

### Fresh baseline eval (2026-08-24, `grounding_check.py --arms baseline`, 10 tickers)

Command: `python grounding_check.py --arms baseline` (BYPASS_CACHE=true, retrieval top-3,
all flags at production defaults, temperature-0 Sonnet judge — per-claim evidence in
`eval_findings/*_baseline.md`, which is gitignored eval evidence kept locally).

| Tickers | Claims | Supported | Unsupported | Inference | Unsup % | Mean retrieval | Mean pipeline latency | Haiku-only $/brief |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10/10 | 84 | 65 | **0** | 19 | **0.0%** | 5.38s | **26.29s** | $0.00592 |

**The number of record going forward: 49% unsupported pre-fix → 0/84 unsupported (0.0%) measured today**
(the previously recorded 3% has improved; run-to-run generation variance means small
non-zero rates can recur — the earlier single WMT flag was already shown to be
temperature variance). Note the judge splits non-supported claims into UNSUPPORTED
(contradicts/absent from source) vs INFERENCE (reasonable derivation); today's run
labeled 22.6% of claims INFERENCE, none UNSUPPORTED.

**Latency claim reproduces:** 26.29s mean pipeline latency vs the recorded ~26s.

**Cost:** $0.0269/brief is **historical only** — recorded from the uncommitted
multi-agent A/B harness and not re-runnable from committed code. Do not reuse it in
new claims. The committed harness measures Haiku-only cost ($0.00592/brief today);
a re-runnable full-cost instrumentation harness (per-brief token counts by model,
priced from a config table) ships in Phase 2 and replaces $0.0269 as the source of
any future cost claim.

## 5. Discrepancies found (stale comments, untracked files)

1. **“3 trained sections” is stale in two places.** `.env.example` says the local model
   serves “Financial Health / SEC Highlights / Risk Factors”, and `grounding_check.py`'s
   local-model arm comments say “3 trained sections”. The code (`LOCAL_SECTIONS` in
   `agent/tools/local_model.py`, mirrored in `scripts/build_dataset.py`) and the README
   agree on **2 sections** (Financial Health, Risk Factors). Code is correct; comments lag.
2. **Untracked files:** `compare_synthesis.py` (its own docstring says “Do NOT commit”)
   and `.streamlit/config.toml` (`fileWatcherType = "none"`, a local dev convenience).
   Left untracked deliberately.
3. **README “Redis/Celery are stubbed” on ECS** is accurate but implicit in code: nothing
   disables `/research/async`; it just has no worker, so jobs poll as `queued` forever.

## 6. Environment constraints discovered (gates Phases 1–3)

- **No container runtime on this machine**: no Docker Desktop/CE, kind, minikube,
  kubectl, or helm anywhere on PATH or in standard install locations.
- **WSL2 is enabled but has no distro installed.** Plan: import an Ubuntu rootfs into
  WSL2 (no admin required), install Docker CE + kind + kubectl inside it, and run the
  single-node kind cluster there. This is the closest honest realization of
  “kind/minikube, single node” available on this machine.
- **Ollama 0.32.15 is installed on the Windows host** (serves the current GGUF build).
- **vLLM does not run natively on Windows** — Phase 3 will run vLLM **CPU mode** inside
  WSL2/the cluster and document the limitation (no GPU on this machine; tokens/sec
  numbers are CPU numbers and say nothing about GPU throughput).
- The merged HF-format checkpoint (`financial-lora-merged/`, safetensors) exists locally
  and is what vLLM will serve; it is gitignored (~3 GB) and stays that way.
