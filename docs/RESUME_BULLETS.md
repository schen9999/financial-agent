# Resume bullets — Financial Research Agent

The bullets below match the resume's Financial Research Agent section word
for word. Each is followed by its deep-dive backup: where the claim lives in
the repo, and any caveat a follow-up question would surface. Unsupported
rates are judge v2 unless stated: v2 carries the held-out calibration —
kappa 0.580, 75% recall / 60% precision on UNSUPPORTED against blind labels
(n=50, 2026-09-06) — so v2 rates are approximate point estimates
(docs/eval-methodology.md). Source of truth for every figure:
docs/numbers-of-record.md.

---

**1.** Built a tool-using LLM agent (Claude API + LangGraph ReAct)
synthesizing market data, news, and SEC filings into investment briefs over
a LlamaIndex + Pinecone RAG pipeline with exact-key Redis caching and
cost-aware routing ($0.0366/brief).

> Deep-dive backup: agent/react_agent.py (`create_react_agent`),
> agent/core.py (Haiku for the four sections, Sonnet for synthesis — the
> routing), agent/tools/rag.py (LlamaIndex over Pinecone), cache key
> `research:{TICKER}` (exact-key, never semantic). $0.0366/brief is the
> cost of record (2026-09-06, post-retrieval-fix, 3-ticker mean,
> `scripts/cost_report.py`).

**2.** Deployed to AWS ECS Fargate + RDS via Terraform and OIDC-authenticated
GitHub Actions CI/CD; exposed the agent's tools as a spec-compliant MCP
server (stdio and streamable-HTTP transports).

> Deep-dive backup: the AWS Terraform is still in the tree — `infra/`, 16
> files: ECR, RDS, Secrets, IAM, networking, ECS Fargate service, GitHub
> OIDC provider + scoped deploy role (added in commits 2f76e0d, e6fb147,
> fb831ad); .github/workflows/deploy.yml (OIDC
> `role-to-assume`, ECR push, ECS task-definition deploy). ECS ran a
> single FastAPI container + RDS; Celery/Redis never ran on ECS.
> MCP server: stdio and streamable-HTTP entrypoints, tests/test_mcp_*.py.

**3.** Migrated the six-service stack (FastAPI, Celery, Redis, PostgreSQL,
Streamlit, MCP) to Kubernetes with probes, resource bounds, and templated
secrets, then rebuilt it on two single-node k3s VMs (NVIDIA A10) with vLLM
serving the fine-tune.

> Deep-dive backup: k8s/ (kustomize base + kind/k3s/oke overlays),
> scripts/k8s_smoke_test.sh (13/13). Two VM.GPU.A10.1 nodes
> (vm-a10-inst-1, vm-a10-inst-2), each its own single-node k3s cluster,
> rebuilt from docs/deploy-runbook.md on 2026-09-23; vLLM v0.10.2 served
> `financial-lora` on both with no manifest changes (runbook "Rebuild on
> fresh nodes, 2026-09-23"). K8s is the stack's first full-topology
> deployment.

**4.** Converted the LLM-as-judge grounding eval into a gated Argo Workflows
DAG (40-ticker fan-out, 5% gate, Wilson CIs, Fisher tests); blind held-out
labels validated the judge (kappa 0.580); an earlier labeling pass exposed a
retrieval bug.

> Deep-dive backup: argo/base/eval-workflow.yaml, scripts/eval_aggregate.py
> (gate), eval/stats.py (Wilson, Fisher). Kappa 0.580 is judge v2 on the
> 50-claim held-out set, labeled blind 2026-09-06 (eval/agreement.py). The
> earlier pass was the 2026-09-04 labeling of the 50-claim dev set
> (author-adjudicated, not blind): reading retrieved contexts turned up
> exhibit boilerplate where Item 1A risk factors should be — the fetcher
> was indexing exhibits (AAPL's "10-K" was its Bylaws). Defect and fix:
> eval-methodology "Retrieval defect" (pre-fix 3/40 risk retrievals
> verified, post-fix 32/40).

**5.** Fine-tuned Qwen2.5-1.5B with QLoRA to write two report sections; a
40-ticker A/B measured 8.15% vs 3.06% unsupported claims (Fisher p =
0.0023), with the excess inside the fine-tune's own sections (19.8% vs
0.5%), so it ships disabled.

> Deep-dive backup: judge v2, same image and index both arms, 2026-09-05/06:
> local-model `lsnnc` 30/368 = 8.15% (CI 5.8–11.4%) vs hosted `j4cnp`
> 12/392 = 3.06% (CI 1.8–5.3%), p = 0.0023. Fine-tune-owned sections
> (Financial Health + Risk Factors, attributed): 22/111 = 19.82% vs
> 1/202 = 0.50%, p = 4.6e-10 (eval/section_attribution.py, heuristic
> attribution, ~78% coverage). USE_LOCAL_MODEL ships off: measured and
> declined.

**6.** Isolated the cause with a 4-arm comparison against untuned Qwen2.5
1.5B and 7B: the fine-tune matched its own base model, and the 7B still
trailed the hosted model while running 3.7x slower on the same GPU.

> Deep-dive backup: a dated comparison set, not numbers of record
> (2026-09-23, vm-a10-inst-2, 40 tickers, judge v2, identical pinned
> sampling). financial-lora `v924f` 25/385 = 6.49% (CI 4.4–9.4%) vs
> qwen2.5-1.5b-instruct `4nfsm` 31/400 = 7.75% (CI 5.5–10.8%), p = 0.58;
> qwen2.5-7b-instruct `cnkp2` 18/393 = 4.58% (CI 2.9–7.1%) vs hosted
> `kcf7s` 4/383 = 1.04% (CI 0.4–2.7%), p = 0.0039. 3.7x: output throughput
> 711.3 vs 194.6 tok/s and mean end-to-end latency 2878 vs 10517 ms on the
> same A10 and settings (`scripts/vm_bench_serve.sh`). Not a size curve —
> hosted is a different model family. 1.5B→7B within Qwen2.5: p = 0.076,
> borderline. Full tables: eval-methodology "Four-arm model comparison".

**7.** Shipped a supervisor multi-agent graph and cross-encoder reranking
default-off after evals showed no grounding gain.

> Deep-dive backup: README "Multi-agent" and "Reranking A/B Experiment" —
> both 10-ticker, judge v1, before the 2026-09-04 retrieval fix. Flags
> `MULTI_AGENT_ENABLED` (agent/graph.py) and `RERANKING_ENABLED`
> (agent/tools/reranker.py, `BAAI/bge-reranker-base`), both default false
> (docs/PHASE0_AUDIT.md flag table). If asked for magnitudes: both added
> cost or latency, but the multi-agent cost ratio came from an uncommitted
> harness (historical only), and the reranking penalty was measured on
> retrieval latency alone — so neither is quoted as a figure.

---

**Numbers inventory** (every figure in the bullets above):

| Number | Status | Where it comes from |
|---|---|---|
| $0.0366/brief | cost of record (2026-09-06) | scripts/cost_report.py, numbers-of-record |
| 13/13 smoke assertions | dated run record | scripts/k8s_smoke_test.sh, numbers-of-record |
| kappa 0.580 (judge v2 held-out, blind, n=50) | current | eval/agreement.py on holdout_sample.csv, numbers-of-record |
| 3/40 → 32/40 risk retrievals verified (retrieval defect) | dated run record | scripts/reindex_filings.py, numbers-of-record |
| 8.15% vs 3.06%, p = 0.0023 (judge v2, 40 tickers) | dated A/B, basis of the ship-off decision | grounding-eval DAG `lsnnc`/`j4cnp`, numbers-of-record |
| 19.82% vs 0.50% on fine-tune-owned sections, p = 4.6e-10 | dated A/B | eval/section_attribution.py, numbers-of-record |
| four-arm: p = 0.58 (fine-tune vs base), p = 0.0039 (7B vs hosted) | dated comparison set, not numbers of record | eval/multi_arm_stats.py, numbers-of-record |
| 3.7x (711.3 vs 194.6 output tok/s; 2878 vs 10517 ms mean E2E) | dated measurement, k3s A10 | scripts/vm_bench_serve.sh, eval/runs/bench/, numbers-of-record |
