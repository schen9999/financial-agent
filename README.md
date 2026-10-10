# 📈 Financial Research Agent

An AI agent that researches stocks and answers follow-up questions using live financial data, news, and SEC filings, with an evaluation harness that measures how far its briefs can be trusted.

**Live Demo:** [financial-research-agent.streamlit.app](https://financial-research-agent.streamlit.app) | **Built with Claude Code**

**Documentation:** start at [docs/README.md](docs/README.md), which maps each question a reviewer might ask to the document that answers it. Every number below comes from a committed, re-runnable harness; run IDs, intervals and the rules for quoting them are in [docs/numbers-of-record.md](docs/numbers-of-record.md).

---

## What it does

- **Generate Brief:** enter a ticker. The app fetches stock data (yfinance), news (NewsAPI) and SEC filing summaries (EDGAR), and grounds the SEC Filing Highlights and Risk Factors sections in filing text with Pinecone RAG. Claude Haiku writes the four middle sections in parallel, then Claude Sonnet streams the Executive Summary and Outlook. The brief is cached in Redis (exact key `research:{TICKER}`) and PostgreSQL.
- **Ask a follow-up:** a LangGraph ReAct agent answers free-form questions, picking the tools it needs (stock data, news, SEC filings, or RAG search).
- **Two execution paths:** the Streamlit UI runs the `agent/` pipeline in-process, and the FastAPI app runs the same code behind REST endpoints (the app Kubernetes deploys).

## Conclusions

Measured on OCI in October 2026, 40 tickers per run, image `f3043751`. Deterministic measures first; the LLM judge second, with its limits beside it.

- **Hosted Claude stays the production path; a self-served open-weight model is a measured alternative.** Qwen3.6-35B-A3B on llama.cpp on an A10 gets stock figures wrong about as rarely as hosted — **1/432 vs 1/565** per checked number, adjudicated, not separated — and both now label foreign filers' figures in the right currency (**22 and 11 currency errors before the stock-data fix, 0 and 0 after**). It states fewer figures: **3.05 vs 4.47** bound to stock data per brief (CI on the difference +0.93 to +1.93), counted without the judge.
- **The judge finds no grounding difference — and the judge is a weak instrument.** Judge-flagged unsupported claims, mean of three judgings: hosted **2.55%**, A10 **3.57%** (paired CI −4.39 to +1.78 points). The same briefs re-judged moved by **up to 2×**, and against blind human labels on these runs the judge's precision is **~29%** and its recall **~11%**. "Not detected" is the strongest grounding claim made.
- **Cost per brief, model only:** hosted **$0.0357**; the A10 at most **$0.0303** (a ceiling: the GPU averaged 36% busy, waiting on the harness); CPU **$0.0107**, but **13.7×** hosted's time per ticker — batch work, not interactive.
- **CPU serving is sized right at 8 vCPU.** On the OKE node, prompt processing speeds up **1.8×** from 4 to 8 vCPU, then not at all; generation runs at about **13 tok/s** at every level. More throughput would come from more replicas on separate nodes — an inference, not measured.
- **Turned off, each for a measured reason:** the fine-tuned Qwen2.5-1.5B (**8.15% vs 3.06%** unsupported — it fails the 5% gate, the excess in the two sections it writes; claim-level Fisher p = 0.0023, and at the ticker level the paired interval excludes zero, **+2.08 to +10.95** points on ticker-averaged rates of 8.68% vs 2.32%, while the sign test does not reach 0.05, p = 0.078), cross-encoder reranking (no drop in refused filing answers, **+11.0 s per ticker**, 41.5% against a 20% limit, on criteria fixed before the runs), and the multi-agent critic (no headroom to show).
- **Two eval layers, because each misses what the other catches.** The judge accepted Toyota's revenue written in dollars from a figure in the filer's reporting currency (yen, inferred from its magnitude) labelled USD; the deterministic numeric check flagged it. The check cannot see a correct figure under the wrong label; the judge flagged those. ([The limits of each layer](docs/debugging-story.md#the-limits-of-each-layer))

- **Some briefs run on thin context:** of the 40 tickers, the 5 ADRs (20-F filers) run without SEC context, 2 (RDFN, VERV) without stock data, and 32 without news in `4hsn2` ([known limitations](docs/eval-methodology.md#known-limitations-from-the-cold-read-review-2026-10-09)).

Self-served models' runs count only when a traffic proof shows the model, and nothing else, produced them: since 2026-10-07, every request in the server's own log must match a harness call ([method](docs/eval-methodology.md#traffic-proof-by-per-request-match-declared-2026-10-07)).

## Next steps

- **After the demo, pipeline fixes** (each changes the pipeline, so each means new baselines on every arm): the recorded limitations — watch-items the judge cannot ground, refused filing-highlights answers, unreconciled yfinance-vs-filing figures, truncated derived figures, the synthesis prompt's example leaking into watch-items, and the current price stated as the 52-week low; shrink the eval pod's output parameter; count "52-week" phrases as labels, not figures. ([Known limitations](docs/eval-methodology.md))
- **CPU endpoint startup probe:** a cold load of the 20.4 GB model from the block volume takes about 15 minutes, longer than the startup probe allows, so a cold restart can be killed once before it comes up. Lengthen the probe (post-demo manifest change; nothing changed now).
- **Traffic proof:** record each response's own token counts in the LLM ledger, so the per-request proof needs no server log.
- **App plane** ([docs/reliability.md](docs/reliability.md)): late acknowledgement for Celery tasks with an idempotent `research_task`; persist async briefs; a deadline for lost jobs; a timeout on the Anthropic client.
- **Infrastructure:** apply the OKE Terraform when a compartment exists; switch the numeric check from warn to block.

---

## Deployed on OCI

- **Where:** a provided OKE cluster (v1.34.1, four VM.Standard.E5.Flex nodes, no GPUs) runs the app plane, the Argo eval harness and the CPU model endpoint; `vm-a10-inst-2`, a VM.GPU.A10.1 on single-node k3s, serves the GPU model endpoint; `vm-a10-inst-1`, the first demo's box, is standby. [docs/architecture.md, "Deployed topology"](docs/architecture.md#deployed-topology-october-2026).
- **What runs there:** the six services and Argo Workflows running the gated grounding-eval DAG, from one image pinned by git sha; two llama.cpp endpoints serving the same Qwen3.6-35B-A3B Q4_K_M file, one on CPU in OKE, one on the A10 (keyed, reachable only from the cluster's egress IP).
- **Access:** the Streamlit UI is public to an IP allowlist only — one OCI load balancer with TLS, the allowlist enforced in the load balancer's security list and again in an nginx sidecar, then basic auth. Everything else is ClusterIP, reached by port-forward through a bastion.
- **One manifest set:** a kustomize base with `kind`, `k3s`, `oke` and `oke-provided` overlays; `scripts/render_diff.py` proves overlay changes never alter the kind render ([docs/verification.md](docs/verification.md)).
- **OKE Terraform:** a cluster with an A10 pool, OCIR, a bucket and a Block Volume storage class, validated and **never applied** (no compartment). The provided cluster is codified separately by import, with a zero-diff plan and no apply ([terraform/oci-provided](terraform/oci-provided/README.md)).
- **More:** [GPU and CPU inference](docs/gpu-inference.md) · [reliability](docs/reliability.md) · [deploy runbook](docs/deploy-runbook.md) · [operations](docs/operations.md) · [configuration](docs/configuration.md) · [cost](docs/cost.md) · [AWS deployment (secondary)](docs/aws.md)

## Key results

Judge-v2 rates are judge-flagged rates; the judge's calibration is the row below them. Full records, run IDs and quoting rules: [docs/numbers-of-record.md](docs/numbers-of-record.md).

| Result | Value | Record |
|---|---|---|
| Wrong stock figures, currency labels, figures stated (no judge) | 1/565 hosted vs 1/432 A10; currency errors 0 and 0 (22 and 11 before the fix); 4.47 vs 3.05 figures bound to stock data per brief | [current](docs/numbers-of-record.md#current) |
| Grounding, judge-flagged, three judgings | hosted 2.55% vs A10 3.57%, no difference detected; CPU 2.89% on the previous image | [current](docs/numbers-of-record.md#current) |
| Judge v2 calibration (blind labels) | precision 29.4% (CI 8.3–52.9%), recall 11.4% (CI 3.1–27.9%), majority of three judgings | [current](docs/numbers-of-record.md#current) |
| Model cost per brief | hosted $0.0357; A10 at most $0.0303; CPU $0.0107 (previous image) | [dated](docs/numbers-of-record.md#dated-run-records) |
| Cost of record (hosted pipeline) | $0.0366 per brief (2026-09-06) | [current](docs/numbers-of-record.md#current) |
| Fine-tune vs hosted | 8.15% vs 3.06% unsupported, claim-level Fisher p = 0.0023; ticker-level paired CI +2.08 to +10.95 points (ticker-averaged rates), sign test p = 0.078; fails the gate | [dated](docs/numbers-of-record.md#dated-run-records) |
| Reranking A/B | refusals 5 vs 7 of 35; +11.0 s per ticker; don't ship | [dated](docs/numbers-of-record.md#dated-run-records) |
| CPU core scaling | prompt 1.8× from 4 to 8 vCPU, then flat; generation about 13 tok/s at every level | [dated](docs/numbers-of-record.md#dated-run-records) |
| W4A16 vs BF16 fine-tune on the A10 | 1075.7 vs 708.3 output tok/s; no detected grounding difference | [dated](docs/numbers-of-record.md#dated-run-records) |

The experiment records — the grounding eval, the self-served comparison, reranking, the QLoRA fine-tune and the multi-agent supervisor — are in [docs/experiments.md](docs/experiments.md).

## Engineering decisions

| Decision | Evidence | Result |
|---|---|---|
| Keep hosted models as the production path | Same wrong-figure rate as the self-served model (1/565 vs 1/432), more figures stated (4.47 vs 3.05), no judge-flagged difference; the CPU route is 13.7× slower | `SLM_FULL` ships off; the self-served model is a measured option |
| Do not adopt the fine-tuned Qwen2.5-1.5B | Fails the 5% gate: 8.15% vs 3.06% unsupported, the excess in the two sections it writes. Claim-level Fisher p = 0.0023; ticker-level paired CI +2.08 to +10.95 points on ticker-averaged rates, sign test p = 0.078 — the decision rests on the gate, not one p-value | `USE_LOCAL_MODEL` ships off ([record](docs/experiments.md#qlora-fine-tuning-experiment)) |
| Keep cross-encoder reranking off | Re-tested on criteria fixed before the runs: no drop in refusals (5 vs 7 of 35), +11.0 s per ticker (41.5%, limit 20%); figures stated and judge-flagged grounding unchanged | Default-off ([pre-registered A/B](docs/eval-methodology.md#reranking-ab-pre-registered-2026-10-08-before-any-run)) |
| Keep the multi-agent critic off | June A/B (judge v1): no grounding headroom, +68% latency; a re-test was dropped before the demo — its value would be on qualitative claims, which the judge cannot measure at ~11% recall | Default-off; harness kept ([record](docs/experiments.md#multi-agent-orchestration-experiment)) |
| Serve Qwen3.6-35B-A3B with llama.cpp, not vLLM | Computed, not booted: no 4-bit build leaves usable context on one A10, and no vLLM image for its CUDA 12.8 driver supports the architecture | llama.cpp on CPU (OKE) and the A10 ([finding](docs/eval-methodology.md#dated-finding-computed-not-booted-no-4-bit-qwen36-35b-a3b-fits-one-a10-under-vllm-2026-10-02)) |
| Match CPU or GPU serving to the workload | CPU $0.0107 per brief at 13.7× hosted's time; the A10 at most $0.0303; CPU stops scaling at 8 vCPU | CPU for batch, the A10 for interactive latency; neither in production |
| Keep two eval layers | Each caught what the other missed (Toyota's currency; wrong labels) | Judge in the eval DAG; numeric check in the pipeline (`NUMERIC_CHECK=warn`) and offline |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM -- section generation | Claude Haiku 4.5 (4 sections in parallel) |
| LLM -- synthesis + ReAct agent | Claude Sonnet 4.6 |
| Agent framework | LangGraph -- `create_react_agent` (follow-ups) + a supervisor `StateGraph` (optional multi-agent brief pipeline) |
| Financial data | yfinance |
| News | NewsAPI |
| SEC filings | SEC EDGAR REST API |
| SEC RAG | LlamaIndex + Pinecone + HuggingFace `bge-small-en-v1.5` |
| Reranking (optional) | Cross-encoder `BAAI/bge-reranker-base` |
| Observability | LangSmith (tool calls, tokens, latency, cost) |
| Brief cache | Redis (exact key per ticker, `research:{TICKER}`) |
| Persistence | PostgreSQL via SQLAlchemy |
| Async tasks | Celery + Redis |
| REST API | FastAPI |
| Frontend | Streamlit |
| Orchestration | Kubernetes — kind (local), single-node k3s on OCI A10 VMs, and a provided OKE cluster |
| Batch / eval orchestration | Argo Workflows v3.7 (fan-out eval DAG, nightly CronWorkflow, quality gate) |
| Self-served models (default-off) | llama.cpp (Qwen3.6-35B-A3B Q4_K_M, CPU and A10); vLLM v0.10.2 (the fine-tune, A10) |
| Cloud | OCI (OKE, A10 VMs); AWS ECS Fargate + RDS ([secondary](docs/aws.md)) |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Development | Claude Code |

Diagrams of the brief pipeline, the follow-up agent, the multi-agent graph and the Kubernetes layout, and why Celery and Argo both exist: [docs/architecture.md](docs/architecture.md#pipeline-and-kubernetes-diagrams-moved-from-the-readme-2026-10-08).

---

## Running Locally

**1. Clone and install**
```bash
git clone https://github.com/schen9999/financial-agent.git
cd financial-agent
pip install -r requirements.txt
```

**2. Add API keys** -- copy `.env.example` to `.env`:

| Key | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) |
| `REDIS_URL` | [upstash.com](https://upstash.com) (free tier) |
| `DATABASE_URL` | PostgreSQL connection string |
| `PINECONE_API_KEY` | [pinecone.io](https://pinecone.io) (free tier) |

**3. Run**
```bash
streamlit run app.py
```

**Or run the full topology on Kubernetes** (Linux/WSL2 with docker + kind +
kubectl; see [k8s/README.md](k8s/README.md) for setup):

```bash
make cluster-up      # single-node kind cluster
make deploy          # build image, secrets from .env, deploy all six services
make smoke-test      # end-to-end: brief, Celery async, cache hit/miss, MCP, UI
make argo-install    # Argo Workflows (pinned v3.7.18)
make argo-deploy     # eval WorkflowTemplate + nightly CronWorkflow
make eval-run        # run the gated grounding eval now
make cluster-down    # tear down
```

The MCP server (the agent's tools over the Model Context Protocol, for Claude Desktop and other clients): [docs/mcp.md](docs/mcp.md).

---

## Testing

| What | Command | Notes |
|---|---|---|
| Unit and integration tests | `python -m pytest tests/` | 610 collected: 609 passed + 1 skipped (as of 2026-10-08). Runs in CI on every pull request and push to `main`. A fresh clone needs `REDIS_URL` and `ANTHROPIC_API_KEY` set for the suite to collect; dummy values are fine. Three tests in `tests/test_tools.py` call yfinance live. |
| Credit-gated judge test | `CRITIC_INJECTION=1 python -m pytest tests/test_critic_injection.py -q -s` | Calls the paid Sonnet judge, so it is skipped by default and runs only on manual dispatch (`critic-injection.yml`). |
| Kubernetes smoke test | `make smoke-test` | On kind: a sync brief, a Celery async task, a cache hit and miss, and the MCP server. |
| Manifest equivalence | `python3 scripts/render_diff.py LEFT RIGHT` | Semantic diff of two rendered manifest sets ([docs/verification.md](docs/verification.md)). |
| Grounding eval gate | `make eval-run` | The Argo DAG fails the workflow if unsupported claims exceed 5%, any ticker is skipped, or fewer than 30 claims were audited. |

---

## API Endpoints

Full reference: [docs/api.md](docs/api.md). A running instance also serves the generated reference at `/docs`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/stock/{ticker}` | Current quote and key financials |
| `GET` | `/stock/{ticker}/history` | 12 months of daily closes |
| `POST` | `/research` | Generate brief (synchronous) |
| `POST` | `/research/async` | Submit research job |
| `GET` | `/research/status/{job_id}` | Poll async job status |
| `POST` | `/ask` | ReAct agent answer |
| `GET` | `/history/{ticker}` | Past briefs for a ticker |
| `GET` | `/history` | The 10 most recent briefs |

---

## Disclaimer

For informational purposes only. Does not constitute financial advice.
