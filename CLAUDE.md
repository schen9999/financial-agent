# financial-agent — OCI migration (CLAUDE.md)

## What this is
Production financial research agent. Six services: FastAPI, Celery worker, Redis,
Postgres, Streamlit, MCP server (stdio + streamable-HTTP). Eval harness runs as a
gated Argo Workflows DAG with a nightly CronWorkflow. Pluggable OpenAI-compatible
LOCAL_MODEL_BACKEND (currently Ollama; vLLM v0.10.2 validated serving the merged
fine-tune on one A10 via a plain-Docker smoke test on the Phase 1.75 VM,
2026-09-02 — in-cluster vLLM still pending; the dev CPU cannot run vLLM, no
AVX-512).

Current deploy target: single-node kind K8s with probes and resource bounds.

## Goal
Migrate to OCI for a hiring demo (deadline: demo Fri Sep 18, 2026):
- OKE basic cluster, created via Terraform (cluster creation is part of the deliverable)
- App node pool: 2x VM.Standard.E4.Flex, 4 OCPUs / 32 GB each (1 OCPU = 2 vCPUs;
  size K8s requests/limits in vCPU terms: 16 vCPU / 64 GB total across the pool)
- GPU node pool: 1x VM.GPU.A10.1 (1x A10 24 GB, 15 OCPUs, 240 GB) running vLLM
  serving fine-tuned Qwen2.5-1.5B via LOCAL_MODEL_BACKEND
- Storage: OCI Block Volume CSI storage class for the Postgres PVC (50 GB
  minimum per volume). Redis is deliberately PVC-less on every target — a
  rebuildable exact-key cache and short-lived Celery results earn no volume.
  Block total 350 GB: 2x50 app boot + 200 GPU boot + 50 Postgres PVC.
  Object Storage bucket for eval artifacts and the vLLM model weights.
- Images pushed to OCI Container Registry (OCIR)

## Targets
- kind (local, working): single-node dev cluster; the equivalence baseline
  every overlay change is proven against.
- Single VM (Phase 1.75 validation; demo fallback): one VM.GPU.A10.2 —
  2x A10 24 GB, 30-core Xeon, 472 GB RAM, 1 TB disk, Ubuntu 22.04, NVIDIA
  driver 570 preinstalled. Constraints: ssh access only (VCN seclist admits
  22 only; everything reached via ssh -L tunnels, nothing bound publicly);
  Docker/k3s not yet installed; no OKE compartment, OCIR, or Object Storage
  bucket exists yet. Runs single-node k3s with the k3s overlays; vLLM pins
  one GPU so a green run validates the A10.1-shaped oke-gpu serving config.
- OKE (Phase 2, once the compartment lands): the Terraform-created cluster
  per the Goal section above.

## Hard constraints
1. kind must remain a working local target throughout. Use kustomize overlays or
   Helm values (kind vs oke), never fork the manifests.
2. The Argo eval DAG and nightly CronWorkflow must keep passing. The eval harness
   is the centerpiece of the demo, not the Streamlit UI.
3. The 833-line pytest suite (47 tests) must pass on every commit. Canonical
   command: `python -m pytest tests/` (pytest.ini scopes bare `pytest` to
   tests/ as well).
4. Celery stays request-time async; Argo owns eval orchestration. Do not merge them.
5. Ollama remains the committed fallback backend until vLLM serves in-cluster
   and the eval DAG passes against it. (The hardware question is settled:
   vLLM demonstrably served the fine-tune on an A10 — Docker smoke test on
   the VM, 2026-09-02. The remaining gate is the in-cluster path.)
6. Work on branch `oci-migration`. Small commits, imperative messages.

## Phases
Phase 1 — COMPLETE (no OCI credentials):
- Terraform authored in terraform/oci (VCN, OKE basic cluster, both node
  pools, OCIR, bucket, BV storage class); fmt + validate pass, no plan/apply.
- Manifests parameterized as kustomize base + kind/oke overlays (app, vllm,
  argo trees); kind renders proven equivalent via scripts/render_diff.py.
- vLLM manifests sized against the A10 (24 GB budget, nvidia.com/gpu request,
  CUDA image). Docs skeleton in /docs.

Phase 1.5 — COMPLETE (pre-credential gaps closed so Phase 2 is apply, push,
deploy and nothing else):
- vLLM weights delivery: fetch-model init container + Object Storage read PAR
  (zero secrets); kind exercises the same path with a small public model.
- ocir-pull-secret referenced by every oke Deployment and the Argo workflow
  pods; secret created imperatively from an auth token (runbook step 6).
- Argo install pinned and committed (argo/install, apply -k); verified by
  full delete, reinstall, and a green eval DAG run.
- Eval artifact archival to the bucket: env-gated (EVAL_ARTIFACTS_PUT_URL,
  off by default), best-effort, unit-tested with a mocked client.
- LB ingress deny-all by default (lb_allowed_cidrs) with seclist management
  mode None so Terraform is the single authority.
- Storage story reconciled: Redis ephemeral everywhere, 350 GB itemized.
- enable_gpu_pool flag for free-trial tenancy dry runs (never the demo
  tenancy; no numbers or claims from trial runs).

Phase 1.75 — single-VM validation target (manifests/tooling committed; steps
flip to executed only on confirmed terminal output from the box):
- 2026-09-02 validated: vLLM v0.10.2 served the fine-tune on one A10 with the
  oke-gpu args, in plain Docker (runbook "Validated so far").
- 2026-09-03 validated: vm-up green on k3s — six app deployments, local-path
  PVC, Argo controller/server, eval WorkflowTemplate/CronWorkflow. vLLM
  crashlooped on a base args bug (entrypoint vs "vllm serve"), fixed by
  moving vllm serve to command:. vLLM-on-k3s and vm-eval remain not executed.
- k3s overlays for all three trees (k8s/overlays/k3s, argo/overlays/k3s,
  k8s/vllm/overlays/k3s-gpu): the oke shape with environmental deltas only —
  NodePorts behind ssh tunnels (mcp stays ClusterIP), imported local image
  with pullPolicy Never, Postgres on local-path at 50Gi, hostPath weights,
  vLLM pinned to one of the two A10s with the exact oke-gpu image and args.
  kind and oke renders proven unchanged by render_diff.py.
- Makefile vm-images / vm-up / vm-eval (run on the VM); runbook section
  "Single-VM path (k3s)" with every step marked NOT YET EXECUTED, network
  baseline (seclist + ufw allow-22) before any NodePort exists.
- CHECKPOINT: If no OKE compartment by Sep 10, the VM is the demo target;
  stop Terraform work and rehearse.

Phase 2 — once OCI access lands (detailed steps: docs/deploy-runbook.md):
1. Fill terraform.tfvars: OCIDs, region/AD with A10 capacity, re-confirm the
   pinned kubernetes_version, set api_allowed_cidr + lb_allowed_cidrs.
2. terraform init / plan / apply (two-stage -target fallback documented).
3. OCIR: docker login with an auth token, tag + push the app image, create
   ocir-pull-secret in-cluster.
4. Set the CHANGEME image refs in both oke overlays (local edit), create
   app-secrets/infra-secrets, kubectl apply -k k8s/overlays/oke; verify PVC
   binds on financial-agent-bv, probes green, LBs get IPs (allowlist first).
5. make argo-install; kubectl apply -k argo/overlays/oke; eval DAG green
   against hosted models. Optionally set EVAL_ARTIFACTS_PUT_URL (write PAR)
   to turn on archival.
6. Upload the merged weights to the bucket, create the read PAR, set
   MODEL_BASE_URL locally (never committed), apply k8s/vllm/overlays/oke-gpu.
   Only after vLLM serves on the A10 may docs (and this file) say it does.
7. Point LOCAL_MODEL_URL at vLLM with LOCAL_MODEL_BACKEND=openai, run the
   eval DAG against it, re-run scripts/cost_report.py on OCI and record the
   new number.

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
- Never claim vLLM served or deployed the model beyond what has actually run.
  Legitimate as of 2026-09-02: vLLM v0.10.2 served the merged fine-tune on one
  A10 with the committed serving args, in plain Docker on the validation VM
  (smoke test confirmed from the box). Still gated: any claim of in-cluster
  serving (k3s or OKE) or of the eval DAG running against vLLM — update this
  line when those actually run.
- Cross-encoder reranking and the multi-agent supervisor shipped default-off
  because evals showed no grounding gain at higher cost/latency. State it that way.
- Any new number in docs must come from a committed, re-runnable harness.