# Configuration reference

Every environment variable the code reads, its default, what it does, and
where it is set on each target. Defaults are the values in the code when the
variable is unset. Secrets are never committed: they live in `.env` locally,
in the `app-secrets` Kubernetes Secret (built from `.env`), and in AWS Secrets
Manager on ECS.

## Where values come from

| Source | Applies to | How it is set |
|---|---|---|
| `.env` | local runs (Streamlit, `grounding_check.py`, scripts) | copy [`.env.example`](../.env.example) to `.env` |
| `app-secrets` Secret | every Kubernetes pod (kind, k3s) | `make deploy` / `make vm-up` build it from `.env` (`--from-env-file`) |
| `infra-secrets` Secret | Kubernetes pods | created once by `make deploy` / `make vm-up`: `POSTGRES_PASSWORD` and `DATABASE_URL` for the in-cluster Postgres |
| `app-config` ConfigMap | Kubernetes pods | [`k8s/base/10-configmap.yaml`](../k8s/base/10-configmap.yaml), patched by the k3s overlay and by `make vm-vllm` |
| Deployment `env` | the MCP pod; the Argo eval pods | [`k8s/base/33-mcp.yaml`](../k8s/base/33-mcp.yaml); [`argo/base/eval-workflow.yaml`](../argo/base/eval-workflow.yaml) |
| ECS task definition | the AWS API container | 4 plain variables in the task definition; 6 secrets from Secrets Manager (`financial-agent/<NAME>`) |
| The eval harness itself | eval runs | `grounding_check.py` sets `BYPASS_CACHE=true` and pins the routing flags per A/B arm |

**Precedence in Kubernetes pods:** `envFrom` lists `app-secrets`, then
`infra-secrets`, then `app-config`; a later source wins on a duplicate key. An
explicit `env` entry on a container wins over all three.

## Required

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | none | Claude API key: section generation, synthesis, the ReAct agent, the judge, RAG answer synthesis | `.env`; `app-secrets`; ECS secret |
| `REDIS_URL` | none; **import fails if unset** (`cache.py`, `celery_worker.py`) | Exact-key brief cache (`research:{TICKER}`, 24 h TTL) and the Celery broker/backend | `.env`; `app-config` (`redis://redis:6379/0`); ECS secret (no Redis runs on ECS: cache lookups fail and fall through to the pipeline) |
| `DATABASE_URL` | none; **import fails if unset** (`database.py`) | PostgreSQL for saved briefs | `.env`; `infra-secrets`; ECS secret (RDS) |
| `NEWS_API_KEY` | none | NewsAPI access for the news tool | `.env`; `app-secrets`; ECS secret |
| `PINECONE_API_KEY` | none; unset disables RAG (`agent/core.py`) | Pinecone vector index for SEC-filing retrieval | `.env`; `app-secrets`; ECS secret |

## Retrieval and reranking

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `BASELINE_TOP_K` | `3` | Chunks retrieved when reranking is off | eval harness (per arm); otherwise unset |
| `RERANKING_ENABLED` | `false` | Two-stage retrieval with a cross-encoder; ships off (no grounding gain in evals) | `app-config` (`false`); ECS task env (`false`) |
| `RERANK_CANDIDATES` | `20` | Stage-1 over-retrieval count when reranking | `app-config` |
| `RERANK_TOP_N` | `3` | Chunks kept after reranking | `app-config` |
| `RERANK_MODEL` | `BAAI/bge-reranker-base` | Cross-encoder model | `.env` only |

## Local model (vLLM or Ollama)

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `USE_LOCAL_MODEL` | `false` | Route the two trained sections (Financial Health, Risk Factors) to the local model; ships off | `app-config` (`false`); ECS task env (`false`); `make vm-local-model ON=…` patches it live on k3s. Eval arms set it themselves. |
| `LOCAL_MODEL_BACKEND` | `ollama` | Protocol: `ollama` (`/api/chat`) or `openai` (`/v1/chat/completions`, vLLM) | k3s overlay `app-config` (`openai`) |
| `LOCAL_MODEL_URL` | `http://localhost:11434` | Base URL of the local model server | k3s overlay `app-config` (`http://vllm.financial-agent.svc:8000`) |
| `LOCAL_MODEL_NAME` | `financial-lora` | Model name sent in each request; the eval checks `/v1/models` lists it | k3s overlay `app-config`; `make vm-vllm SERVED_NAME=…` |
| `LOCAL_MODEL_DIR` | unset (recorded as `unrecorded`) | Weights directory, recorded in eval provenance only | `make vm-vllm MODEL_DIR=…` patches `app-config` |
| `LOCAL_MODEL_TIMEOUT` | `180` (seconds) | Per-request timeout to the local model | `.env` only |
| `LOCAL_MODEL_MAX_TOKENS` | `512` | `max_tokens` on each OpenAI-backend request (sampling is otherwise pinned in `agent/tools/local_model.py`) | `.env` only |

## Multi-agent orchestration

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `MULTI_AGENT_ENABLED` | `false` | Planner → research → critic → supervisor graph instead of the single-agent pipeline; ships off (no grounding gain in evals) | `app-config` (`false`) |
| `CRITIC_MAX_UNSUPPORTED_PCT` | `5` | Unsupported-claim % the inline critic tolerates before a revision | `app-config` (`5`) |
| `MAX_REVISIONS` | `2` | Maximum critic → research revision passes | `app-config` (`2`) |

## Observability (LangSmith)

The LangSmith SDK accepts both naming schemes. [`agent/tracing.py`](../agent/tracing.py)
reads `LANGSMITH_*` first, falls back to the legacy `LANGCHAIN_*` name, and
mirrors whichever is set to the other. **Use `LANGSMITH_*`**: it is what
`.env.example`, the code's first lookup, and the ECS secret
(`financial-agent/LANGSMITH_API_KEY`) all use. The legacy names work, but
only through the fallback.

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `LANGSMITH_API_KEY` (legacy: `LANGCHAIN_API_KEY`) | none; tracing off without a key | LangSmith API key | `.env`; `app-secrets`; ECS secret |
| `LANGSMITH_TRACING` (legacy: `LANGCHAIN_TRACING_V2`) | unset (off) | `true` enables tracing | `.env`; ECS task env (`true`) |
| `LANGSMITH_PROJECT` (legacy: `LANGCHAIN_PROJECT`) | SDK default project | LangSmith project name | `.env`; ECS task env (`financial-agent`) |

## MCP server

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `MCP_TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` (`financial-agent-mcp --http` also selects HTTP) | MCP deployment `env` (`streamable-http`) |
| `MCP_HOST` | `127.0.0.1` | Bind address for the HTTP transports | MCP deployment `env` (`0.0.0.0`) |
| `MCP_PORT` | `8000` | Port for the HTTP transports | MCP deployment `env` (`8000`) |
| `MCP_TOOL_TIMEOUT` | `30` (seconds) | Per-tool-call timeout | `.env` only |

## Eval harness

| Variable | Default | Purpose | Set in |
|---|---|---|---|
| `BYPASS_CACHE` | `false` | `true` makes the pipeline skip the Redis cache so an eval measures the pipeline, not the cache. Leave unset in normal operation. | Argo eval pods (`true`); set by `grounding_check.py` and `scripts/cost_report.py` themselves |
| `EVAL_ARTIFACTS_PUT_URL` | unset (archival off) | OCI Object Storage write PAR; when set, the eval aggregate uploads its summary best-effort | `app-secrets` (Phase 2, never committed) |
| `CRITIC_INJECTION` | unset | `1` enables the credit-gated judge test (`tests/test_critic_injection.py`); tests only | the shell running pytest; the `critic-injection.yml` workflow |

## Make variables (not read by the code)

`make vm-vllm MODEL_DIR=… SERVED_NAME=… MAX_LEN=…` swaps the model vLLM serves
on a k3s node (defaults `qwen-ft`, `financial-lora`, `4096`) and then sets
`LOCAL_MODEL_NAME` and `LOCAL_MODEL_DIR` in `app-config`. `ARGO_OVERLAY`
selects the Argo overlay for `make argo-deploy` (`kind` by default; `vm-up`
passes `k3s`). `ENV_FILE` points the Makefile at a different `.env`.
