# financial-agent — OCI migration (CLAUDE.md)

## What this is
Production financial research agent. Six services: FastAPI, Celery worker, Redis,
Postgres, Streamlit, MCP server (stdio + streamable-HTTP). Eval harness runs as a
gated Argo Workflows DAG with a nightly CronWorkflow. Pluggable OpenAI-compatible
LOCAL_MODEL_BACKEND (code default ollama for local dev; the k3s nodes set
openai -> in-cluster vLLM; vLLM v0.10.2 validated serving the merged
fine-tune pinned to one A10 on the Phase 1.75 VM — plain Docker 2026-09-02,
in-cluster on k3s 2026-09-03. Eval A/Bs against it FAILED the gate: 10-ticker
2026-09-03 (12.31% vs 3.03%, judge v1, p=0.054) and the deciding 40-ticker
2026-09-05/06 (8.15% vs 3.06%, judge v2, p=0.0023), so hosted models stay the
production path. OKE serving still pending; the dev CPU cannot run vLLM, no
AVX-512).

Current demo target (first week of November 2026, follow-up to the first
demo; plan in docs/demo.md): the provided OKE cluster as harness and app
plane, plus node 2's (vm-a10-inst-2) keyed GPU llama.cpp endpoint;
vm-a10-inst-1 is the frozen first-demo box (k3s + fine-tuned vLLM),
standby/fallback only. Single topology statement: docs/architecture.md,
"Deployed topology (October 2026)". kind stays the local equivalence
baseline, with probes and resource bounds.

## Goal
Migrate to OCI, with a live demo of the result (first week of November 2026):
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
- Single VM (the first demo's target; since 2026-10-05 vm-a10-inst-1 is
  frozen standby and vm-a10-inst-2, node 2, serves the GPU llama.cpp
  endpoint of the demo; on node 2 vLLM STAYS SCALED TO 0 until after the
  demo — it answers 30880 unkeyed, k3s NodePorts bypass ufw, and the
  30880 security-list rule stays open to the OKE egress IP until then;
  runbook "Demo live run"): vm-a10-inst-1 and vm-a10-inst-2 — two
  VM.GPU.A10.1 nodes (1x A10 24 GB, Ubuntu 22.04, NVIDIA driver 570
  preinstalled), rebuilt from the runbook 2026-09-23 (bootstrap, vm-images,
  vm-up green on both; runbook "Rebuild on fresh nodes, 2026-09-23").
  Constraints: ssh access only (VCN seclist admits 22, plus node 2's
  30880 from the OKE egress IP 129.80.187.92/32 only; everything else
  reached via ssh -L tunnels, nothing else bound publicly); no OKE compartment,
  OCIR, or Object Storage bucket exists yet. Runs single-node k3s with the
  k3s overlays. The Sep 2 VM.GPU.A10.2 (Phase 1.75 validation box, where
  vLLM pinned to one GPU validated the A10.1-shaped oke-gpu serving config
  on 2026-09-03) is gone.
- OKE, provided cluster — the demo's harness and app plane (authored 2026-10-02; app plane, Argo,
  metrics-server chart 3.14.0 and the hosted smoke x2cx8 EXECUTED
  2026-10-03 — per-step status in the runbook): a cluster
  provisioned for us, NOT by terraform/oci — never run Terraform against
  it, with ONE exception (explicit owner override, 2026-10-07): terraform
  import and plan only, read-only in the cloud, only in
  terraform/oci-provided/, local gitignored state, apply/destroy NEVER;
  every Terraform command there goes through scripts/tf_provided.sh, which
  refuses anything but init, fmt, validate, plan, show, providers,
  import (local state only) and state list/show. Zero-diff plan REACHED
  2026-10-07: 94 resources (VCN networking, the cluster, 2 node pools)
  imported into local state, plan "No changes"; config and state stay on
  the operator (OCIDs); terraform/oci-provided/README.md. OKE v1.34.1,
  4x VM.Standard.E5.Flex amd64 at 16 vCPU (two ~28 GiB,
  two ~58 GiB allocatable), no GPUs, cri-o (no image import), default
  StorageClass oci-bv. CPU-only harness: no vLLM or GPU resources,
  USE_LOCAL_MODEL=false; hosted models unless SLM_FULL. Its optional CPU
  SLM endpoint (k8s/llamacpp/overlays/oke-cpu) served one traffic-proven
  smoke 2026-10-03 (see the Self-served bullet below); no doc may claim
  vLLM on it, or SLM serving beyond the runbook's EXECUTED steps. Overlays
  k8s/overlays/oke-provided +
  argo/overlays/oke-provided (oke stays the Terraform path); app image
  from GHCR pinned by git sha (make oke-images on node 2, oci2 — the
  laptop's WSL disk filled during a build 2026-10-03; the pin edit goes
  to the laptop as a patch — git diff on node 2, git apply + commit +
  push on the laptop); a new image re-runs every arm on it.
  make oke-up on the private operator host (ssh oke-operator, ProxyJump
  oke-bastion). Operator gotchas: kubectl's oci credential plugin
  consumes ssh stdin and a non-login ssh lacks its PATH, so secrets go
  over as a 0600 temp file (umask 077; cat > file), are created on the
  operator, then shred -u — never streamed into kubectl (streaming works
  on node 2's k3s); remote one-liners need bash -ic, bash -lc fails.
  Every Service ClusterIP; the public Streamlit UI (one OCI flexible LB,
  allowlist + basic auth, k8s/overlays/oke-provided-public-ui; runbook
  "Public Streamlit UI"), security-list management mode since 2026-10-08
  (the controller may not create NSGs); LIVE and verified 2026-10-08
  03:12Z, allowlist 99.164.75.62/32 only, status in the runbook.
  Every change in the financial-agent namespace goes through the repo's
  overlays and scripts only (an outside change exposed Streamlit without
  auth on 2026-10-08, about 02:05–02:19 and 02:22–02:31Z). Access by
  port-forward behind
  ssh -L; nightly CronWorkflow suspended. Runbook "OKE (provided
  cluster)". Yahoo has returned 429 from its egress IP: check the
  aggregate's "stock block empty" count on every run there.
- OKE (Phase 2, once the compartment lands): the Terraform-created cluster
  per the Goal section above.

## Hard constraints
1. kind must remain a working local target throughout. Use kustomize overlays or
   Helm values (kind vs oke), never fork the manifests.
2. The Argo eval DAG and nightly CronWorkflow must keep passing. The eval harness
   is the centerpiece of the demo, not the Streamlit UI.
3. The pytest suite (7502 lines, 610 tests collected: 609 passed + 1 skipped,
   the credit-gated judge test, as of 2026-10-06) must pass on every commit. Canonical
   command: `python -m pytest tests/` (pytest.ini scopes bare `pytest` to
   tests/ as well).
4. Celery stays request-time async; Argo owns eval orchestration. Do not merge them.
5. SETTLED, now on a clearly separated 40-ticker A/B (2026-09-05/06, judge
   v2, same image and index both arms): the fine-tune serves in-cluster but
   FAILS the grounding gate — 8.15% unsupported (30/368, CI 5.8–11.4%) vs
   baseline 3.06% (12/392, CI 1.8–5.3%), Fisher p = 0.0023; the failure
   concentrates in the two sections the fine-tune owns (attributed FH+RF
   claims 19.82% vs 0.50%, p = 4.6e-10, eval/section_attribution.py). The
   earlier 10-ticker judge-v1 A/B (12.31% vs 3.03%, p = 0.054) agrees in
   direction but could not separate the arms alone. USE_LOCAL_MODEL
   therefore ships off and hosted models remain the production path; Ollama
   stays the fallback for local serving demos. State it as
   measured-and-declined, not unfinished.
6. Work on branch `oci-migration`. Small commits, imperative messages.
7. Judge-calling tests spend Anthropic credits: they run ONLY under an
   explicit env flag (CRITIC_INJECTION=1 today; the same pattern for any
   future one), never in the default pytest suite, and never on push, PR or
   scheduled CI triggers — manual dispatch only (the Sunday schedule was
   removed 2026-09-28).

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

Phase 1.75 — EXECUTED END TO END on the VM, 2026-09-03 (vm-images → vm-up →
vm-eval all green; steps flipped only on confirmed terminal output):
- 2026-09-02: vLLM v0.10.2 served the fine-tune pinned to one A10 with the
  oke-gpu args, in plain Docker (runbook "Validated so far").
- 2026-09-03: vm-up green on k3s — six app deployments, local-path PVC, Argo,
  eval CRDs. vLLM base fixes from the box, in order: "vllm serve" moved to
  command: (entrypoint collision), enableServiceLinks: false (VLLM_PORT
  injection), 2Gi Memory emptyDir at /dev/shm. Then: vLLM rollout green with
  /v1/models on the NodePort, and vm-eval Succeeded — 10/10 tickers, 66
  claims, 3.03% unsupported (judge v1), gate passed (hosted models; not a
  numbers-of-record re-run).
- 2026-09-03 later: local-model arm ran against in-cluster vLLM (20 confirmed
  /v1 requests) and FAILED the gate — 12.31% vs baseline 3.03% same day (judge v1).
  Dated A/B recorded in docs/eval-methodology.md; constraint 5 settled.
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
  stop Terraform work and rehearse. RESOLVED: no compartment landed by Sep
  10; the k3s VM path is the demo target (now two A10.1 nodes, see Targets).

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
- Numbers of record (since 2026-10-07), image f3043751, 40 tickers.
  LEAD WITH THE DETERMINISTIC MEASURES: numeric check (adjudicated) wrong
  stock figures 1/565 hosted `4hsn2` vs 1/432 GPU SLM `nstp9` (both the
  current price written as the 52-week low); currency-label findings 0
  and 0 (22 and 11 on 9jzmj/p9jr2 before the fix); figures bound to a
  stock-data field 4.47 vs 3.05 per brief, +1.43 (CI +0.93 to +1.93,
  p = 0.0001; eval/density_check.py). Judge-flagged grounding is
  SECONDARY, judge v2, three judgings, mean (range): 4hsn2 2.55%
  (1.47–3.76%), nstp9 3.57% (3.27–3.75%), numeric 0.86% vs 2.42%; paired
  bootstrap -1.22 points (CI -4.39 to +1.78), no difference detected —
  always with the judge's noise (up to ~2x between judgings) and its
  calibration (precision ~29%, recall ~11%, calibration of record below)
  stated right beside it. CPU SLM arm: `8vpq6` on the PREVIOUS image
  1f51dad (2.89%, 2.13–3.63%), because both f3043751 CPU runs failed their
  traffic proofs (5bdz5 +1, 4kkgm -4: every request matched the server
  log, the /metrics counter drifted; not citable); compared ONLY with
  1f51dad runs (9jzmj, p9jr2). SAME-IMAGE COMPARISONS ONLY. The one-judging
  three-way on 1f51dad (9jzmj 1.70%, 8vpq6 3.63%, p9jr2 2.45%) is the
  FORMER numbers of record (2026-10-05 to 2026-10-07), a dated record,
  9jzmj with its aggregate-rebuilt status. Hosted is the production path.
  Never a before/after with j4cnp ("fell from 3.06% to
  1.70%"): different pipeline (512 vs 2048 RAG cap), and the 10-ticker
  hosted smokes span 1.11–7.92% on judge listing alone. Table and
  framing rules: docs/numbers-of-record.md. `j4cnp` (2026-09-05/06),
  12/392 = 3.06% (CI 1.8–5.3%), judge v2, reweighted 5.7%, is the FORMER
  number of record (2026-09-06 to 2026-10-05): a dated record with its
  512-cap caveat, and still the hosted arm of the lsnnc fine-tune A/B
  (constraint 5). "49% pre-fix -> 0/84" is RETIRED as current: it was
  measured 2026-08-24 under judge v1 on the pre-Sep-4 retrieval pipeline,
  so it is a dated record only, quoted with both tags (judge v1,
  pre-retrieval-fix). Never a bare 0%.
- Every cited unsupported rate must name the judge prompt version that
  produced it (agent/grounding.py JUDGE_PROMPT_VERSION; logged in every eval
  summary). All judge-v1 rates carry the recall caveat: v1 recall on
  UNSUPPORTED measured 1/9 against human labels (2026-09-04), so v1 rates are
  lower bounds. Judge v2 is VALIDATED held-out (2026-09-06, 50 blind labels,
  zero dev-set overlap): kappa 0.580, UNSUPPORTED precision 60% (9/15, CI
  35.7–80.2%). CALIBRATION OF RECORD (2026-10-07, applies to the current
  numbers of record, measured on those runs): 180 blind labels on 4hsn2 +
  nstp9, claims listed by any of three judgings, strata U/I/W/S reweighted
  (eval/build_threejudge_calibration.py, eval/threejudge_report.py;
  eval-methodology "The judge's calibration on these runs"). Precision on
  UNSUPPORTED 25.0–36.8% per judging, majority 29.4% (CI 8.3–52.9%);
  population-weighted recall 9.2–16.0% per judging, majority 11.4% (CI
  3.1–27.9%), a claim a judging did not list counting as missed; recall
  over each judging's own listed claims (the September definition)
  13.3–28.8%. True-rate estimates, always labelled WIDE: 4hsn2 3.8% (CI
  1.9–9.7%), nstp9 8.7% (CI 5.4–18.5%), denominator every claim any
  judging listed; no test between them. Precision is driven by hedged
  Outlook watch-items (limitation 1): 14 of the 16 judge-flagged claims
  labelled INFERENCE. The SEPTEMBER CALIBRATION (2026-09-24) is a dated
  record since 2026-10-07 and still describes the runs of its time:
  judge-SUPPORTED stratum
  4/123 from a blind relabel of 123 claims, judge-UNSUPPORTED 9/15 and
  judge-INFERENCE 2/15 from the held-out sample; population-weighted
  recall 32.5% on the baseline run (CI 16.0–52.4%), lsnnc 59.2% (CI
  36.0–77.9%), pooled 47.9% (CI 26.5–68.3%) (eval/reweight_calibration.py
  with --use; command in eval-methodology). The 2026-09-06 "75% recall"
  (unweighted) and the 2026-09-24 held-out-only reweight (25.4%, 1/20
  judge-SUPPORTED) are superseded. The calibration batch's first-pass
  labels are DISCARDED (over-strict: blind relabel test-retest kappa
  0.242, 39 of 42 judge-SUPPORTED UNSUPPORTED labels withdrawn); they are
  on record as a dated finding only and never feed a figure. Every v2 rate
  is the judge-flagged rate; where a reweighted true-rate estimate exists
  it goes beside it (j4cnp 5.7%, CI 3.5–9.9%; lsnnc 8.3%, CI 5.5–12.5%;
  pooled 6.9%, CI 4.5–11.1%; 2nh8v 3.9%, CI 1.8–8.3%). A/B
  directions and the per-section attribution are unaffected when both arms
  share the judge. The 50-claim dev set remains a development set and
  validates nothing.
- Judge recall is only ever quoted population-weighted (reweighted to the
  run's judge-label counts), with its CI. Never quote recall computed on a
  judge-label-stratified sample as drawn.
- Cost of record: $0.0366/brief (2026-09-06, post-retrieval-fix) from the
  committed harness. Cost per brief on image f3043751 (2026-10-07, dated,
  model cost only): hosted $0.0357 (n = 3, cost_report.py run locally on
  the unchanged pipeline code), GPU SLM nstp9 $0.0303 (a CEILING, A10 at
  35.7%); CPU from 8vpq6 below. Same-pipeline cost per brief on image 1f51dad (2026-10-05,
  dated, model cost only — harness pods, storage and judge excluded on
  every arm): hosted $0.0370 (n = 3, run locally on the 1f51dad pipeline
  code; the demo cost table uses it with that label), GPU SLM p9jr2
  $0.0293 (a CEILING: whole A10 VM at $2.00/h, A10 at 38% utilization),
  CPU SLM 8vpq6 $0.0107 (pod request 4 OCPU + 30 GiB billed as 30 GB —
  OCI's memory GB taken as binary; $0.0110 converted to decimal GB; whole
  node 8 OCPU + 64 GiB $0.0219, approximate). CPU is cheapest at 13.7x hosted's latency: batch, not
  interactive. Prices from the OCI price API (cost.md); never project a
  GPU floor without a run. $0.0316 is a dated pre-retrieval-fix record — never quote
  it as current. $0.0269 is retired. "54% cost reduction" is retired.
- The Redis cache is exact-key per ticker. Never "semantic cache."
- Never claim Celery/Redis ran in production on ECS. ECS reality was a single
  FastAPI container + RDS. K8s is the first full-topology deployment.
- Never claim vLLM served or deployed the model beyond what has actually run.
  Legitimate as of 2026-09-03: vLLM v0.10.2 served the merged fine-tune pinned
  to one A10 with the committed serving args — in plain Docker (2026-09-02)
  and in-cluster on single-node k3s via the k3s-gpu overlay (2026-09-03,
  green rollout + /v1/models on the NodePort), both confirmed from the box.
  Also legitimate: the eval DAG ran against the in-cluster vLLM on
  2026-09-03 (10 tickers, judge v1: 12.31% vs 3.03%, p = 0.054) and on
  2026-09-05/06 at 40 tickers (judge v2, same image/index: 8.15% vs 3.06%,
  p = 0.0023 — the citable A/B) — always with both numbers and the judge
  version tag. Also legitimate as of 2026-09-23: vLLM v0.10.2 re-served
  `financial-lora` on both VM.GPU.A10.1 nodes (single-node k3s, no manifest
  changes), and on vm-a10-inst-2 also served untuned Qwen2.5-1.5B-Instruct
  and Qwen2.5-7B-Instruct (swapped with `make vm-vllm`) for the four-arm
  comparison — a dated comparison set, not numbers of record, 40 tickers,
  judge v2: hosted `kcf7s` 4/383 = 1.04% (CI 0.4–2.7%) and its 2026-09-24
  same-image rerun `dvvxk` 7/389 = 1.80% (CI 0.9–3.7%, p = 0.55), fine-tune `v924f`
  25/385 = 6.49% (CI 4.4–9.4%), 1.5B base `4nfsm` 31/400 = 7.75% (CI
  5.5–10.8%), 7B base `cnkp2` 18/393 = 4.58% (CI 2.9–7.1%); quote it as a
  dated set with run IDs and CIs. Also legitimate as of 2026-09-29: vLLM
  v0.10.2 served the fine-tune quantized to GPTQ W4A16 (`financial-lora-w4a16`,
  llm-compressor compressed-tensors, Marlin kernels) on vm-a10-inst-2
  (single-node k3s via `make vm-vllm`, no manifest change), and the eval DAG
  ran against it: `r5nzh`, 40 tickers, judge v2, 23/344 = 6.69% (CI
  4.5–9.8%) vs the BF16 fine-tune `v924f` 6.49%, p = 1.00 — no detectable
  difference at this sample size, on the judge's audited sections (Exec
  Summary + Outlook) only; section-level numeric accuracy is the numeric
  check's to report. A dated comparison, not a number of record. Still gated: serving on OKE — update this line when that
  actually runs.
- Self-served Qwen3.6-35B-A3B (authored 2026-10-02): llama.cpp
  b11347 serving ggml-org Q4_K_M @baec3eb on a CPU endpoint on the provided
  OKE cluster and a GPU endpoint on vm-a10-inst-2 (same GGUF, same engine).
  Legitimate as of 2026-10-03, dated smokes on image 2dd1aa3 only: the CPU
  endpoint served the 10-ticker smoke `nb6r6` (judge v2, traffic proof
  EXACT): 3/73 = 4.11% (CI 1.4–11.4%), beside the same-image hosted smoke
  `x2cx8` 2/84 = 2.38% (CI 0.7–8.3%) — never numbers of record, never an
  arm comparison, always with the caveat that 13 of 20 SLM RAG answers
  were cut at the then-512 RAG cap, and both to be re-run on the next
  image. On image 30c832b (lock fix + 2048 RAG cap), same 10 tickers,
  judge v2, no truncation: hosted smoke `hm527` 1/90 = 1.11% (CI
  0.2–6.0%) and CPU smoke `9jddz` 1/53 = 1.89% (CI 0.3–9.9%). 9jddz's
  TRAFFIC PROOF is FAIL, explained: one Argo retry (NVDA) after Anthropic
  credits ran out; the failed attempt's SLM calls were not recorded on
  that image. 9jddz is NOT CITABLE: quote it only with that status, never
  as a pass, never as the CPU baseline — the CPU baseline on the new image
  is the next CPU smoke (`wnrjr` on 1f51dad: 1/58 = 1.72%, CI 0.3–9.1%,
  numeric 0/33, proof EXACT). Which proof outcomes make an SLM run citable:
  EXACT, or LOWER-BOUND with every excess token attributed to calls the
  harness itself logged as failed. Nothing else: any FAIL, explained or
  not, and any run with a failed attempt lacking a complete call record,
  is not citable. From the next image failed attempts log their own
  calls, eval/attempts.py reports retries with cause and counts labelled
  as from failed attempts (printed under the aggregate by make eval-run
  and written to ~/<workflow>-attempts.json; no RBAC for the aggregate
  pod, by decision), and the proof counts every attempt. PROOF METHOD
  CHANGED 2026-10-07, declared before any run it judges: an SLM run is
  citable only if scripts/traffic_proof_tasks.py gives TASK-EXACT — every
  task in the endpoint's own llama-server log, from the workflow's
  creation to the capture right after the run, matches a harness call on
  (prompt, completion) tokens and vice versa, none incomplete. The
  /metrics counter proof still runs and is reported, never deciding (it
  drifted 1, 2, 2 tokens in the controlled replay with per-request counts
  exact). Runs judged under the counter method keep their verdicts:
  5bdz5, 4kkgm, 6z5xz stay NOT CITABLE, never re-scored; the CPU arm stays
  8vpq6 on 1f51dad. Numeric claims
  are co-primary with the rate: every SLM-vs-hosted all-claims rate goes
  with numeric claims per ticker and the numeric-claim unsupported rate
  (hm527 6.1/ticker, 0/61; 9jddz 3.1/ticker, 0/31), plus claims per
  ticker. The SLM synthesis states about half the figures of hosted (3.1
  vs 6.1 numeric claims/ticker) because it follows the synthesis prompt
  literally; judge v2's listing of qualitative claims varies run to run
  (GOOGL 11 vs 2, V 6 vs 16) — recorded, not fixed: a scope change would
  be a new judge version needing calibration. The numeric rate is a
  judge-flagged subset rate, not separately calibrated
  (eval/claim_density.py, run by eval/multi_arm_stats.py;
  eval-methodology). A lower SLM rate alone is never "better grounding".
  Hosted smokes on the 10-ticker set, judge v2, dated: `x2cx8` 2/84 =
  2.38% (CI 0.7–8.3%, 512 RAG cap, no hosted answer cut), `hm527` 1/90 =
  1.11% (CI 0.2–6.0%), `7c66k` 8/101 = 7.92% (CI 4.1–14.9%, GATE FAILED:
  all 8 on MSFT, where the judge listed 14 qualitative claims vs 1 and
  0). Numeric unsupported is 0 in all three. This is smoke-level
  run-to-run variance from judge listing, not a pipeline change: the same
  ungrounded MSFT content is in all three syntheses, and the lower runs
  are judge misses consistent with the population-weighted v2 recall, not
  cleaner briefs. Never quote one smoke's rate as "the hosted rate", never
  call 7c66k a regression or the low runs clean, never rank arms on
  smokes: compare arms on the extended runs, numeric co-primary first. Do
  not change the judge or the gate for it.
  The GPU endpoint loaded with all layers on the A10 (nvidia-smi:
  llama-server 20,488 of 23,028 MiB, --n-cpu-moe 0; llama.cpp logs no
  offload line, nvidia-smi process memory is the evidence) and enforces
  its key; it answered the 20 requests of the RAG natural-length
  pre-check (not an eval, no grounding claim), then the GPU smoke k6zxd and
  the GPU extended p9jr2 (2026-10-05, proof EXACT; bullet below). No doc may say more of either
  endpoint, or quote any other slm-full number, until its runbook step is
  EXECUTED and the run's traffic proof passed (EXACT or LOWER-BOUND).
  x2cx8's printed LLM-call table double-counts the hosted RAG sites (a
  handler registered twice, fixed by a lock): the real figures are 10
  calls per RAG site and 7.0 agent calls/ticker in both arms — quote the
  corrected table (eval-methodology, scripts/rag_ledger_from_workflow.py);
  the $0.0366 cost of record predates that handler and is unaffected.
  Both arms' RAG answers share one cap (RAG_MAX_TOKENS, 2048 since
  2026-10-03; 512 through image 2dd1aa3; sized from the dated GPU
  pre-check — the smoke's 20 SLM answers uncut: median 577, p95 802, max
  854; truncations still counted): a hosted run on that image is NOT the j4cnp
  pipeline exactly — answers cut at 512 (SFIX risks in j4cnp, kcf7s,
  dvvxk) now complete; say so wherever such a run sits beside j4cnp. A GPU run with --n-cpu-moe > 0 (served alias
  -hybrid-ncmoe<n>) is HYBRID in every table, never "GPU". Under SLM_FULL
  the judge and the multi-agent critic stay Sonnet (the critic is the one
  hosted dependency of the SLM app path). vLLM for this model on one A10:
  computed infeasible from the published 4-bit builds and driver 570, not
  booted — state it that way (eval-methodology). The RAG-faithfulness
  metric (rf-v1) is unvalidated: judge-flagged, its own column, never part
  of the grounding rate.
- Hosted extended baseline on the comparison image: `9jzmj` (2026-10-04,
  40 tickers, judge v2, image 1f51dad): 7/411 = 1.70% (CI 0.8–3.5%),
  numeric 2/277 = 0.72% (CI 0.2–2.6%). ALWAYS with its status: workflow
  Error at aggregate (controller lacked configmaps create for template
  offload); rebuilt offline from all 40 pod findings dumps; gate evaluated
  offline; est. run cost not reconstructable. Citable as the same-image
  hosted extended baseline because the rebuild
  (scripts/results_from_pod_log.py + the unchanged eval_aggregate.py)
  reproduces 7c66k's in-cluster aggregate exactly apart from the
  estimated-cost line, and because the aggregate run on the rows stored in
  9jzmj's own workflow object (eval/runs/9jzmj-workflow.json,
  scripts/workflow_nodes.py results) prints the same report, plus est. run
  cost $4.0998 — "not reconstructable" applies to the pod logs only. A
  dated run and, since 2026-10-05, the hosted arm of the grounding
  numbers of record (the three-way); 9jzmj is not the j4cnp pipeline
  exactly (2048 RAG cap).
- CPU SLM extended run on the comparison image: `8vpq6` (2026-10-04, 40
  tickers, slm-full-cpu, judge v2, image 1f51dad) — a dated, CITABLE run:
  traffic proof EXACT (270 calls, 342,244 + 96,811 tokens), 40/40 on the
  first attempt, no Trunc/Loop/Parse/Fmt/Err. 9/248 = 3.63% (CI 1.9–6.8%)
  vs hosted `9jzmj` 7/411 = 1.70% (CI 0.8–3.5%). HEADLINE, in these words:
  no grounding difference detected at this sample size (Fisher p = 0.126
  all claims; 0.362 numeric, 3/161 vs 2/277); numeric density is the
  separated result (paired +2.90 numeric claims/ticker for hosted, CI
  +2.15 to +3.70, sign test p = 1e-8, hosted higher on 35 of 40). Never
  "equivalent", never "the SLM grounds as well": not detected is not
  absent. Always with: the SLM states about 4.0 figures per ticker vs 6.9;
  pipeline 355 s vs 26 s per ticker (13.7x) with the endpoint saturating
  its 8-CPU limit; RAG faithfulness side by side with denominators and the
  UNVALIDATED label (6/1415 vs 14/1017 over 70 answers each — the SLM's
  answers are longer, so the lower rate is not a validated quality claim).
  Of the SLM's three numeric unsupported claims only CHGG is a wrong
  number (-52.997M written as -52.9M, truncation, from its Financial
  Health section; hosted wrote $53M); BEAM is a context source conflict
  (yfinance -86.52M vs the filing's -80.0M) judged against the filing;
  META is judge error (price at 80% of range, same claim SUPPORTED in
  9jzmj). "Numeric" = the claim text contains a digit, so "52-week"
  phrases count (6/277 hosted, 3/161 SLM): quote the sensitivity row with
  it (2/271 vs 2/158, p = 0.628; paired +2.83). Fixing that definition is
  a post-comparison change (it is image code); do not change it now.
  Part of the grounding numbers of record since 2026-10-05 (the
  three-way). GPU endpoint: next bullet.
- GPU SLM extended run on the comparison image: `p9jr2` (2026-10-05, 40
  tickers, slm-full-gpu, all layers on node 2's A10 — alias without
  -hybrid, judge v2, image 1f51dad) — a dated, CITABLE run, part of the
  grounding numbers of record since 2026-10-05 (the three-way): traffic
  proof EXACT (270 calls, 350,290 + 98,232 tokens), 40/40 on the first
  attempt, no Trunc/Loop/Parse/Fmt/Retry/Err. 6/245 = 2.45% (CI
  1.1–5.2%), numeric 3/155 = 1.94% (CI 0.7–5.5%). HEADLINE: no grounding
  difference detected on any pair at this sample size (GPU vs hosted 9jzmj
  p = 0.567 all, 0.355 numeric; GPU vs CPU 8vpq6 0.602, 1.000; p-values
  unadjusted across the three pairs); numeric density separates GPU from
  hosted (paired +3.05 for hosted, CI +2.33 to +3.83, sign p = 2e-9) and
  NOT from CPU (+0.15, CI -0.35 to +0.68, 17/6/17, p = 1.0) — the
  same-model consistency check holds. Same quoting rules as 8vpq6: never
  "equivalent"; always with density (3.9 figures/ticker vs 6.9) and the
  52-week sensitivity row (3/148 vs 2/271, p = 0.351). Numeric unsupported
  claims are reported BY TYPE, never as one count (eval/error_types.py on
  eval/runs/numeric-error-types-2026-10-05.json): wrong value hosted 0 /
  CPU 1 (CHGG) / GPU 0; wrong label 0 / 0 / 2 (SFIX current price called
  the recent low; CRBU per-share low attached to "market
  capitalization"); source conflict 0 / 1 (BEAM) / 1 (OMER); judge error
  0 / 1 (META) / 0, plus CRBU's stated judge reason is incorrect (it
  rejected a correct rounding) while the verdict stands; not in context
  2 (AFRM, NVO) / 0 / 0. Model errors (value + label + not in context —
  everything but source conflicts and judge errors) 2/277, 1/161, 2/155,
  no pair separates (Fisher unadjusted, p >= 0.617). Latency: CPU
  is 10–15x slower than GPU at every call site, 11.4x per ticker; GPU is
  2.0–3.4x slower than hosted per call except synthesis (hosted 1.6x
  slower, longer brief), 1.2x per ticker (31.1 s vs 25.9 s). GPU use
  during p9jr2 (nvidia-smi every 5 s, scripts/nvsmi_summary.py): mean
  38%, median 0% at parallelism 2 — headroom on the A10; never project
  throughput from it without a run. Smoke k6zxd (3/63, all AAPL
  qualitative watch-items, numeric 0/32) is smoke variance from judge
  listing, never an arm comparison. Tool-use check 2026-10-05: every route
  parse 1.0, correct tool 10/10, completed 10/10, errors 0; expected tool
  first hosted 8/10 (WMT, V fetched the filing list first), CPU and GPU
  10/10 — n=10, never "Qwen picks tools better"; not under a traffic
  proof, cite only its JSONs and the saved pane.
- Argo template offload (found 2026-10-04): a step whose resolved template
  exceeds 131,072 bytes (Argo v3.7.18 MaxEnvVarLen) is offloaded by the
  CONTROLLER to a ConfigMap; the aggregate crosses that from 27 hosted /
  18 SLM tickers since the 2026-10-02 LLM ledger grew the per-ticker rows
  (about 4.9 KB hosted, 7.5 KB SLM; 0.6 KB before). argo/base/rbac.yaml
  grants the controller SA (argo in namespace argo) configmaps [create]
  in financial-agent — nothing wider; proven on kind, first live OKE use
  in 8vpq6 (aggregate template 301,083 bytes, 2.30x the limit;
  scripts/aggregate_template_size.py). KNOWN POST-COMPARISON CHANGE, deferred because it
  changes the image: shrink the eval pod's output parameter to what the
  aggregate reads, with a worst-case size test and a pre-submit warning.
  Do not make that change while the comparison on 1f51dad is running.
  eval/attempts.py and scripts/slm_traffic_proof.py run inside pods
  (harness import; api-pod snapshots): do not edit them without saying so
  — host-side fixes go in host-only files (scripts/workflow_nodes.py
  expands status.compressedNodes for them).
- Known limitations, recorded 2026-10-03, NOT fixed during the SLM
  comparison (either fix changes the pipeline and needs new baselines on
  every arm; post-demo): (1) the synthesis prompt asks for watch-items
  naming metrics, and judge v2 labels a hedged watch-item unsupported when
  the context lacks the metric — a prompt/judge interaction in every arm;
  (2) the highlights RAG query reaches only risk-factor text for AMZN,
  JPM, MSFT, NVDA and WMT, so their RAG highlights answer is a refusal and
  the "SEC Filing Highlights" section is a refusal for 4–5 of 10 briefs
  per run. State both when describing brief quality; do not present the
  briefs as having a working filing-highlights section for those tickers.
  (3) the context can hold conflicting figures from different sources
  (BEAM net income: yfinance -86.52M vs the filing's RAG answer -80.0M)
  and nothing in the pipeline reconciles or flags them; (4) the SLM
  truncates where it should round on at least one derived figure (CHGG,
  -52.997M written as -52.9M). Same rule: recorded, post-demo, unchanged
  during the comparison. Added 2026-10-05: (3) is RECURRING, not a
  one-off — OMER in p9jr2 (yfinance net income 116.53M vs the filing's
  3.4M net loss) is the second net-income conflict; (5) the foreign
  filers BABA, NVO, SAP, TM, TSM (20-F) make no RAG call and get no SEC
  context on any arm; (6) the LLM ledger does not record the hosted ReAct
  agent's calls (llm_calls 0 on 8 of 10 tool-use questions), so the
  hosted tool-use route is attributed by its setting; (7) on the CPU
  tool-use route WMT and V retrieval took 35.8 s and 40.9 s vs 2–4 s
  elsewhere — cause not determined, contention between the api pod and
  the CPU llama.cpp pod is a hypothesis only. (8) added 2026-10-06: the
  synthesis prompt's Outlook example ("watch services-margin trend") leaks
  into briefs as ungrounded "services margins" watch-items (NVDA and MSFT
  in m7qvv, AFRM in p9jr2); not changed in the stock-data-fix image, the
  fix is post-demo. (9) added 2026-10-08: the current price stated as the
  52-week low ("near its 52-week low of $X", X the current price) — UPST
  4hsn2, EVGO nstp9, BLNK vks4c, hosted and SLM alike; adjudicated
  TRUE_ERRORs, all judge-flagged; post-demo prompt fix beside (8). GPU smoke m7qvv (4/60, gate failed, all watch-items,
  numeric 0/30, proof EXACT) is smoke-level judge variance on qualitative
  watch-items (limitation 1), precedent 7c66k -> 9jzmj; the extended chain
  went ahead on the adjudicator's go. Numeric check on the
  three-way (adjudicated 2026-10-05 by one human, not blind; dated, not a
  number of record): 12 flags, TRUE_ERROR 8/569 hosted, 1/389 CPU, 2/423
  GPU, every one attributed to the upstream data findings (currency,
  margin fraction), 0 otherwise in every arm, no paired difference
  excludes zero; the judge SUPPORTED the hosted TM figures (51.96 trillion
  in the filer's reporting currency — yen by magnitude, inferred, not
  checked live — labelled USD, written as "$52.0 billion"; two judge
  misses). The check cannot see truncation under its 2%
  tolerance (CHGG) or wrong labels (SFIX, CRBU): never cite it as covering
  either.
- Cross-encoder reranking and the multi-agent supervisor shipped default-off
  because evals showed no grounding gain at higher cost/latency. State it that way.
  Reranking was re-tested 2026-10-08 on pre-registered criteria (vks4c vs
  2mzdd, 40 tickers, f3043751): DON'T SHIP — refusals 5 vs 7 of 35 (no
  drop), +11.0 s per ticker warm (41.5%, limit 20%); bound figures and
  judge-flagged grounding unchanged. The critic A/B was dropped before the
  demo (README decisions).
- Judge noise (2026-10-06, eval-methodology "the judge's run-to-run noise
  on identical inputs"): the same briefs re-judged with the same inputs,
  prompt and temperature-0 judge moved by up to ~2x (4hsn2 15/399 ->
  6/408; 5bdz5 19/265 -> 9/258), in the qualitative claims. New numbers of
  record use THREE JUDGINGS per run (original + two re-judges,
  eval/rejudge_runs.py): per-run mean and range; between arms a paired
  ticker-level bootstrap on per-ticker rates averaged over the judgings;
  per-judging Fisher only for continuity, labelled. Never pool the three
  judgings' claims into one Fisher test.
- The specificity result (hosted states more figures than the self-served
  model) is stated from the JUDGE-INDEPENDENT count first
  (eval/density_check.py): figures bound to a stock-data field as the
  conservative figure, all numbers stated beside it; judge-based numeric
  claims per ticker only as corroboration.
- Any new number in docs must come from a committed, re-runnable harness.