# financial-agent — OCI migration (CLAUDE.md)

## What this is
Production financial research agent. Six services: FastAPI, Celery worker, Redis,
Postgres, Streamlit, MCP server (stdio + streamable-HTTP). Eval harness runs as a
gated Argo Workflows DAG with a nightly CronWorkflow. Pluggable OpenAI-compatible
LOCAL_MODEL_BACKEND (currently Ollama; vLLM manifests committed but never executed —
CPU lacks AVX-512).

Current deploy target: single-node kind K8s with probes and resource bounds.

## Goal
Migrate to OCI for a hiring demo (deadline: demo Fri Sep 18, 2026):
- OKE basic cluster, created via Terraform (cluster creation is part of the deliverable)
- App node pool: 2x VM.Standard.E4.Flex, 4 OCPUs / 32 GB each (1 OCPU = 2 vCPUs;
  size K8s requests/limits in vCPU terms: 16 vCPU / 64 GB total across the pool)
- GPU node pool: 1x VM.GPU.A10.1 (1x A10 24 GB, 15 OCPUs, 240 GB) running vLLM
  serving fine-tuned Qwen2.5-1.5B via LOCAL_MODEL_BACKEND
- Storage: OCI Block Volume CSI storage class for Postgres/Redis PVCs (50 GB min
  per volume), 350 GB block total, Object Storage bucket for eval artifacts
- Images pushed to OCI Container Registry (OCIR)

## Hard constraints
1. kind must remain a working local target throughout. Use kustomize overlays or
   Helm values (kind vs oke), never fork the manifests.
2. The Argo eval DAG and nightly CronWorkflow must keep passing. The eval harness
   is the centerpiece of the demo, not the Streamlit UI.
3. The 833-line pytest suite (47 tests) must pass on every commit. Canonical
   command: `python -m pytest tests/` (pytest.ini scopes bare `pytest` to
   tests/ as well).
4. Celery stays request-time async; Argo owns eval orchestration. Do not merge them.
5. Ollama remains the committed fallback backend until vLLM demonstrably serves
   on the A10.
6. Work on branch `oci-migration`. Small commits, imperative messages.

## Phases
Phase 1 — no OCI credentials yet (NOW):
- Author Terraform: VCN, OKE basic cluster, both node pools, OCIR, Object Storage
  bucket, block volume storage class. Must pass `terraform fmt` and
  `terraform validate`. No plan/apply until credentials exist.
- Parameterize manifests for OKE: storage class name, image registry prefix,
  service exposure (LoadBalancer vs NodePort), GPU node selector + toleration
  for the vLLM deployment.
- Verify vLLM manifests against A10 specs: 24 GB VRAM budget, nvidia.com/gpu
  resource request, correct image for CUDA on A10.
- Docs skeleton in /docs: architecture diagram, deploy runbook, eval methodology,
  numbers-of-record table.

Phase 2 — once OCI access lands:
- terraform plan/apply, push images to OCIR, deploy overlay, PVCs bind,
  all probes green.
- Bring up vLLM on the A10, point LOCAL_MODEL_BACKEND at it, run the eval DAG
  against it. Only after this runs end-to-end may docs say vLLM served the model.
- Re-run the committed cost harness on OCI and record the new number.

Phase 3 — demo polish:
- Full documentation pass, demo script centered on the Argo eval DAG and
  benchmarking, fresh eval run for current numbers.

## Documentation honesty rules (apply to ALL written output: docs, READMEs, comments)
- Grounding number of record: "49% pre-fix -> 0/84 unsupported in current eval."
  Never a bare 0%.
- Cost of record: $0.0316/brief from the committed harness. $0.0269 is retired.
  "54% cost reduction" is retired.
- The Redis cache is exact-key per ticker. Never "semantic cache."
- Never claim Celery/Redis ran in production on ECS. ECS reality was a single
  FastAPI container + RDS. K8s is the first full-topology deployment.
- Never claim vLLM served or deployed the model until it actually runs on the A10.
  After it does, update this file and the claim becomes legitimate.
- Cross-encoder reranking and the multi-agent supervisor shipped default-off
  because evals showed no grounding gain at higher cost/latency. State it that way.
- Any new number in docs must come from a committed, re-runnable harness.