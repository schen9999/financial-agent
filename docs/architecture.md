# Architecture

Six services plus an eval plane, deployed as one topology on Kubernetes
(kind locally; OKE is the Phase 2 target of the OCI migration). Per the
Phase 0 audit, K8s is the **first environment where the full designed
topology runs** — the retired ECS deployment (infra/) was a single FastAPI
container + RDS, with no Celery, Redis, Streamlit, or MCP in production.

```mermaid
flowchart LR
    subgraph clients [Clients]
        browser([Browser])
        rest([REST client])
        mcpc([MCP client])
    end

    subgraph cluster ["Kubernetes — namespace financial-agent"]
        streamlit["Streamlit UI<br/>(pipeline runs in-process,<br/>unchanged app.py)"]
        api["FastAPI<br/>sync /research +<br/>async /research/async"]
        worker["Celery worker<br/>(request-time async only)"]
        redis[("Redis<br/>exact-key cache per ticker<br/>+ Celery broker/results")]
        pg[("Postgres<br/>research_briefs")]
        mcp["MCP server<br/>streamable-HTTP /mcp"]

        subgraph argo ["Argo Workflows — eval orchestration only"]
            cron["CronWorkflow<br/>nightly 03:30 ET"] --> wft["WorkflowTemplate<br/>grounding-eval"]
            evalrun["eval-run.yaml<br/>(manual submit)"] --> wft
            wft --> pods["eval pods (fan-out per ticker,<br/>BYPASS_CACHE=true)"]
            pods --> gate["aggregate + gate:<br/>fail on unsupported-claim breach"]
        end
    end

    subgraph llm ["LLM seam (agent/tools/local_model.py)"]
        hosted["Anthropic API<br/>(hosted Claude — default for<br/>every section)"]
        local["LOCAL_MODEL_BACKEND<br/>ollama (committed fallback) |<br/>openai → vLLM (served on an A10<br/>2026-09-03; A/B failed the gate<br/>— ships default-off)"]
    end

    browser --> streamlit
    rest --> api
    mcpc --> mcp
    api -->|enqueue| redis
    redis -->|research_task| worker
    api <--> pg
    worker --> pg
    api <-->|cache get/set| redis
    streamlit -.->|agent pipeline in-process| llm
    api -.-> llm
    worker -.-> llm
    mcp -.-> llm
    pods -.-> llm
```

## Reading the diagram

- **Four pods embed the same agent pipeline** (one image, four commands —
  see Dockerfile.k8s). Streamlit deliberately runs the pipeline in-process
  (no Streamlit→FastAPI hop); the MCP server calls the agent tools directly.
- **Celery vs Argo is a hard boundary.** Celery handles request-time async
  (`POST /research/async` → Redis broker → worker); Argo owns batch/eval
  orchestration. They are never merged (CLAUDE.md constraint 4).
- **The Redis cache is an exact-key cache** — key `research:{TICKER}`,
  24h TTL. It is not a semantic cache. Redis is PVC-less on purpose, on
  every deploy target (kind and OKE alike): the cache is rebuildable and
  Celery results are short-lived, so a restart costs only a cold cache.
- **The LLM seam**: hosted Claude serves everything by default. With
  `USE_LOCAL_MODEL=true`, only the two sections the fine-tuned
  Qwen2.5-1.5B was trained on (Financial Health, Risk Factors) route to
  `LOCAL_MODEL_URL`; `LOCAL_MODEL_BACKEND` selects the protocol —
  `ollama` (the committed fallback) or `openai` (what vLLM serves). vLLM
  served the fine-tune on an A10 (plain Docker 2026-09-02, in-cluster
  k3s 2026-09-03), and the eval DAG then measured it: **12.31%
  unsupported vs a same-day 3.03% hosted baseline (judge v1) — the fine-tune fails
  the 5% gate on the two sections it owns** (same harness, same day;
  dated A/B in eval-methodology.md). `USE_LOCAL_MODEL` ships off as a
  measured negative result. OKE serving remains Phase 2.
- **Default-off features**: cross-encoder reranking and the multi-agent
  supervisor ship default-off because evals showed no grounding gain at
  higher cost/latency (docs/PHASE0_AUDIT.md).
- **Eval pods bypass the cache** (`BYPASS_CACHE=true`) and gate the
  workflow on the unsupported-claim rate — see
  [eval-methodology.md](eval-methodology.md).

## Deploy targets

Manifests are kustomize base + overlays (k8s/, k8s/vllm/, argo/): the kind
overlays reproduce the single-node local cluster exactly (proof:
[verification.md](verification.md)); the oke overlays add OCIR images,
OCI LoadBalancers, Block Volume PVCs, and the A10 GPU scheduling for vLLM.
See [deploy-runbook.md](deploy-runbook.md).
