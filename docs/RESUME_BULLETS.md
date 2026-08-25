# Resume bullets — financial-agent infra work (Aug 2026)

Rules these follow: only what was built and measured in this repo, real numbers
only, each defensible under a deep-dive. Supporting evidence noted under each.

---

**1.** Migrated a multi-service LLM research agent (FastAPI, Celery, Redis,
PostgreSQL, Streamlit, MCP server) from a reduced single-container AWS ECS
deployment to Kubernetes (single-node kind), with liveness/readiness probes,
resource bounds, and .env-templated secrets on every component; the smoke test
asserts an end-to-end research brief, the stack's first-ever completed async
Celery task in a full deployment, and exact-key cache hit/miss isolation
(13/13 assertions passing).

> Deep-dive backup: docs/PHASE0_AUDIT.md ("Deployed vs. designed"),
> k8s/manifests/, scripts/k8s_smoke_test.sh, Phase 1 commit. Debugging story:
> celery's `import_from_cwd` puts cwd on sys.path only temporarily → task-body
> imports failed only in the prefork child; fixed with image-level PYTHONPATH.

**2.** Converted an LLM-as-judge grounding evaluation into an Argo Workflows
DAG — per-ticker fan-out at bounded parallelism, aggregate step, and a hard
quality gate that fails the workflow above 5% unsupported claims — scheduled
nightly via CronWorkflow; the gate fired on its first full run (5.62%, one
outlier draft), and re-measurement attributed it to generation variance: the
threshold was kept and the red-night playbook documented instead of widening
the gate.

> Deep-dive backup: argo/eval-workflow.yaml, scripts/eval_aggregate.py, README
> "the gate fired on its first real run". Design choice: results travel as
> output parameters, so no artifact repository is needed on a local cluster;
> request-time async stays on Celery (split documented in README).

**3.** Built a re-runnable cost-instrumentation harness that prices exact
API-reported token usage per model from a config table, replacing a
non-reproducible historical figure; measured $0.0316/brief and showed that a
previously claimed "54% cost reduction" from a fine-tuned local model was
sections-only spend — at full-brief level the saving is within run-to-run
variance because synthesis-model tokens dominate.

> Deep-dive backup: scripts/cost_report.py, scripts/model_prices.json,
> benchmarks.md cost table. Instrumentation subtlety: ContextVar-based usage
> callbacks don't propagate into the ThreadPoolExecutor running the parallel
> section calls — the callback attaches directly to the chat-model objects.

**4.** Built a pluggable OpenAI-compatible serving backend
(`LOCAL_MODEL_BACKEND`) for a QLoRA-fine-tuned Qwen2.5-1.5B — vLLM Kubernetes
manifests committed for AVX-512-capable hardware after root-causing the
prebuilt vLLM CPU image's SIGILL to its AVX-512 requirement on AVX2-only
hardware, with the code path validated end-to-end via Ollama's /v1 endpoint —
and benchmarked it honestly: ~7.7 tok/s aggregate CPU saturation across
concurrency 1→8 (environment-limited, labeled not comparable to GPU/hosted),
and 86.2% vs 77.8% grounding against the hosted API on a balanced 9-ticker
suite — an expected, reported regression that keeps the feature default-off.

> Deep-dive backup: benchmarks.md (CPU-mode caveat up front; latency marked
> environment-limited), k8s/vllm/vllm.yaml, agent/tools/local_model.py
> (LOCAL_MODEL_BACKEND), exit-code-132 diagnosis in the Phase 3 commit.

---

**Numbers inventory** (source of truth for each figure):

| Number | Where it comes from |
|---|---|
| 49% pre-fix → 0/84 unsupported in current eval (10 tickers) | Phase 0 re-measure, docs/PHASE0_AUDIT.md §4 |
| $0.0316/brief hosted; $0.0321 hybrid | scripts/cost_report.py runs, benchmarks.md |
| 86.2% vs 77.8% grounding (9-ticker balanced) | grounding A/B run, benchmarks.md |
| 5.62% gate failure → variance | Argo run + NVDA re-measure (0/10), README |
| ~7.7 tok/s aggregate; p50 13.3s→74.1s (c=1→8) | scripts/vllm_benchmark.py, benchmarks.md |
| 13/13 smoke assertions; 43 pytest tests | scripts/k8s_smoke_test.sh output; pytest |
| ~26s pipeline latency (26.29s mean) | Phase 0 re-measure |
