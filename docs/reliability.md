# Reliability

How a brief request moves through the app, what each component does when
it fails, and how the eval plane keeps its runs trustworthy. Behaviour is
taken from the code and the Kubernetes manifests. Where it comes from a
library default rather than this repo's code it is marked **(library
default, inferred)**. Where no test or recorded run covers it, it says
**not tested**.

## Part 1: the app plane

### How a brief request flows

**Synchronous, `POST /research`** (`api.py`): the API pod runs the whole
pipeline in the request (`agent.core.run_research_checked`):

1. Cache lookup: Redis, exact key `research:{TICKER}`, 24 h TTL
   (`cache.py`).
2. Data: stock data (yfinance), then news (NewsAPI) and SEC filings
   (EDGAR) in parallel; the two SEC RAG answers (Pinecone retrieval plus an
   LLM answer).
3. Four sections in parallel (Claude Haiku), then the synthesis (Claude
   Sonnet).
4. The deterministic numeric check, in `warn` mode by default (appends a
   note).
5. Cache write (Redis), then `save_brief` writes the brief to Postgres and
   the API returns it.

**Asynchronous, `POST /research/async`**: the API enqueues a Celery task
on Redis (`celery_worker.py`) and returns a job ID at once. The worker
(one pod, `--concurrency=1`) runs the same pipeline, stores the result in
Redis (the Celery result backend, and the brief cache), and
`GET /research/status/{job_id}` reads it back. **The async path does not
write to Postgres:** `research_task` never calls `save_brief`; only the
synchronous route does.

Every app Deployment runs one replica (`k8s/base/`). Postgres sits on a
50Gi persistent volume (`oci-bv` on OKE); Redis has no volume, by design
— a rebuildable exact-key cache and short-lived Celery results.

### What happens when each piece fails

| Failure | Behaviour | Evidence |
|---|---|---|
| **Worker crash mid-task** | Kubernetes restarts the pod (startup, readiness and liveness probes run `celery inspect ping`). The task is not re-run: `task_acks_late` is not set, so the message was acknowledged when the worker took it **(library default, inferred)**, and with `task_track_started=True` its status keeps reading "processing" until the result record expires **(library default, inferred)**. Other queued tasks wait for the restarted worker. | `celery_worker.py`, `k8s/base/31-worker.yaml`; **not tested** |
| **Redis restart (no volume)** | The brief cache empties and refills from the next requests. Queued Celery tasks and stored results are lost; a status query for a lost job reads "queued", because Celery reports an unknown ID as PENDING **(library default, inferred)**. While Redis is down, cache reads and writes fail open — logged, the request falls through to the LLM — but enqueueing an async job fails, and the API returns 500 **(inferred: the call is not caught)**. | `cache.py` (fail-open in code), `api.py`; **not tested** |
| **Postgres pod restart** | The data survives on its volume. The Deployment uses `Recreate`, so two Postgres pods never share the ReadWriteOnce volume. While it is down, `save_brief` raises and `/research` returns 500 after the brief was generated; the brief was already cached in Redis, so a retry within 24 h is served from the cache. The SQLAlchemy engine has no `pool_pre_ping`, so a stale pooled connection can fail the first request after a restart **(inferred)**. `/history` endpoints return 500 while it is down. | `database.py`, `k8s/base/21-postgres.yaml`; **not tested** |
| **API pod restart** | One replica, one uvicorn process: requests in flight are lost, including a synchronous `/research` (about 26 s for a hosted brief). Startup, readiness and liveness probes on `/health` keep traffic off the pod until it answers; an init container waits for Postgres. Async jobs are unaffected (they live in Redis and the worker). | `k8s/base/30-api.yaml`; **not tested** |
| **Hosted LLM timeout or error** (Anthropic) | `langchain-anthropic` 1.4.4 retries twice and sets no request timeout **(library defaults: `max_retries=2`, `default_request_timeout=None`; not configured in this repo)**. After that the exception propagates: `/research` returns 500, an async job reads "error". No fallback model. | `agent/core.py`; **not tested** in the app plane (the eval plane's credit guard is, below) |
| **Self-served LLM timeout or error** (`SLM_FULL`) | One request timeout (`SLM_TIMEOUT`, default 900 s); a connection or HTTP error raises `SLMRequestError`, with no hosted fallback, by design. Structured output gets one retry, then fails; a synthesis missing its Executive Summary or Outlook gets one retry, then `BriefFormatError`. | `agent/tools/slm.py`, `agent/core.py`; the format guard and parse retry are unit-tested (`tests/test_slm.py`) |
| **Upstream 429: yfinance** | `get_stock_data` catches every error and returns `{"error": …}`, which the trimming step drops: the brief is written from news and filings with an empty STOCK DATA block. No retry. Every eval aggregate counts these (`stock block empty`), and yfinance has answered 429 from the OKE egress IP. | `agent/tools/stock.py`, `eval/stock_block.py` (tested, `tests/test_stock_block.py`); runbook, "OKE (provided cluster)" |
| **Upstream 429: NewsAPI, SEC EDGAR, Pinecone** | NewsAPI and EDGAR errors return an error item (EDGAR requests time out at 15 s); the brief is written without that data, no retry. A failed RAG retrieval returns nothing and the two filing sections fall back to the raw data context. | `agent/tools/news.py`, `agent/tools/sec.py`, `agent/core.py`; **not tested** |
| **Upstream 429: Anthropic** | Covered by the library's two retries (above). | **not tested** |

## Part 2: the eval plane

The eval runs as an Argo workflow: one pod per ticker (`BYPASS_CACHE`, so
it never reads or writes the live cache), then an aggregate step that
gates the run (at most 5% unsupported claims, at least 30 claims). Around
that, these mechanisms decide whether a run counts.

**Traffic proof (self-served runs).** Before and after a run,
`make slm-eval-run` reads the llama.cpp server's own token counters from
inside the api pod; afterwards `scripts/slm_traffic_proof.py verify`
compares the server's difference with every token the harness logged, over
every attempt. **EXACT** means they match to the token; **LOWER-BOUND**
means the server saw more, and the run is citable only if every excess
token belongs to calls the harness itself logged as failed; **FAIL** means
the server saw traffic the harness did not log, and the run is not citable
— explained or not. Every self-served run on record carries its verdict
(`eval/runs/slm-proof-*/`); `9jddz` (2026-10-03) is the recorded FAIL:
one Argo retry after the Anthropic balance ran out, whose failed attempt's
calls that image did not log
([eval-methodology.md](eval-methodology.md#smokes-on-image-30c832b-2026-10-03-dated-the-cpu-runs-traffic-proof-is-fail-explained)).

**Attempts record and retries.** `eval/attempts.py` rebuilds every eval
pod's attempts from the workflow object and the pod logs: Argo retries
with their cause, and the LLM calls of failed attempts, which each
attempt logs itself from image `1f51dad` on. `make eval-run` prints it
under the aggregate and writes `<workflow>-attempts.json`; the traffic
proof counts failed attempts' tokens.

**Run-time gate.** `make run-time-check` blocks a 40-ticker run unless the
smoke's worst-case projection (slowest smoke ticker × waves + the
aggregate) fits the run's deadline, the slowest smoke ticker is within 75%
of the per-ticker deadline, and the projection plus a day of capture fits
the 7-day TTL.

**Credit guard.** An exhausted Anthropic balance returns a "credit
balance" 400; `eval/runtime_guards.py` makes it fail the run loudly
instead of exhausting the per-ticker retries and surfacing as skipped
tickers, the failure mode seen on 2026-09-03. Tested
(`tests/test_runtime_guards.py`).

**Template-offload permission.** Argo v3.7.18 hands a step its template in
an environment variable capped at 131,072 bytes; a larger one is offloaded
by the controller to a ConfigMap. The aggregate crosses that from 27
hosted or 18 self-served tickers, and on 2026-10-04 hosted run `9jzmj`
ended in Error there because the controller could not create ConfigMaps.
`argo/base/rbac.yaml` now grants the controller `configmaps: [create]` in
the eval namespace and nothing wider; proven on kind, first used on OKE by
`8vpq6` (a 301,083-byte template). `9jzmj` was rebuilt offline with the
unchanged aggregate code
([eval-methodology.md](eval-methodology.md#dated-finding-the-aggregate-steps-template-outgrew-argos-inline-limit-2026-10-04)).

**Capture within the TTL.** Workflows and their pods are deleted 7 days
after they finish. Each run's pod log, workflow object, attempts record,
proof files and per-ticker findings are captured into `eval/runs/` before
then ([deploy-runbook.md](deploy-runbook.md#oke-provided-cluster), step 9).

**Smoke, then extended, with stop rules.** A new image re-runs every arm:
a 10-ticker smoke per arm first, checked before anything longer runs, then
the 40-ticker runs behind the run-time gate. A chain of extended runs stops
at the first run that fails, retries, or has a traffic proof other than
EXACT. A smoke that fails its gate on judge listing of qualitative claims
is recorded as smoke variance, not re-run for a pass, and the extended run
may go ahead on an explicit decision: hosted smoke `7c66k` then `9jzmj`,
GPU smoke `m7qvv` then the October chain
([deploy-runbook.md](deploy-runbook.md#rerun-on-the-stock-data-fix-image-october-2026)).
