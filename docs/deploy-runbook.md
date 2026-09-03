# Deploy runbook

Two targets, one manifest tree: `kind` (local, fully working today) and
`oke` (OCI, Phase 2). Anything not yet executed is marked
**[Phase 2 — NOT YET EXECUTED]**; everything else has been run end-to-end
on this repo.

## kind (local) — end to end

Prerequisites: Linux environment with `docker`, `kind`, `kubectl`, `make`,
`jq`, `openssl`, and a filled-in `.env` in the repo root. On the dev
machine this is the WSL2 distro `financial-agent` (see k8s/README.md for
environment specifics).

```bash
make cluster-up      # create the single-node kind cluster (idempotent;
                     # also restarts a stopped node after WSL idle-termination)
make deploy          # build image, kind load, secrets from .env,
                     # kubectl apply -k k8s/overlays/kind, wait for rollouts
make smoke-test      # sync brief, async Celery brief, cache hit+miss, MCP
make argo-install    # Argo controller + server (kubectl apply -k argo/install,
                     # version pinned in that kustomization)
make argo-deploy     # kubectl apply -k argo/overlays/kind
                     # (RBAC, grounding-eval WorkflowTemplate, nightly cron)
make eval-run        # submit the eval DAG now and follow it to completion
make cost-report     # re-runnable cost/brief harness (local, needs .env)
make status          # pods, services, recent events
make cluster-down    # delete the cluster
```

After `make deploy`: FastAPI http://localhost:30080, Streamlit
http://localhost:30501, MCP http://localhost:30800/mcp.

Notes:

- **Redis runs without a PVC on every target, deliberately**: the
  exact-key cache (`research:{TICKER}`) is rebuildable and Celery results
  are short-lived, so a restart costs only a cold cache — persistence
  would buy nothing and cost a block volume.
- Secrets never touch git: `app-secrets` is materialized from `.env`,
  `infra-secrets` (Postgres password + DATABASE_URL) is generated once,
  in-cluster only.
- **vLLM local (CPU mode)**: `make vllm-deploy` applies
  `k8s/vllm/overlays/kind-cpu`. Model delivery is a `fetch-model` init
  container that downloads env-listed files into an emptyDir at pod
  start; the kind overlay points it at a small public HF model
  (Qwen2.5-0.5B-Instruct, no token) so the delivery path is exercisable
  locally. On the current dev CPU the vLLM container itself is not
  runnable (no AVX-512 — see benchmarks.md), so the committed way to
  exercise `USE_LOCAL_MODEL` locally is Ollama via
  `LOCAL_MODEL_BACKEND`'s default. This is exactly why Ollama remains the
  committed fallback until vLLM demonstrably serves on the A10.

## OKE (OCI) — Phase 2

All OCI infrastructure is authored in `terraform/oci/` (fmt + validate
pass). **No step below has been executed — there are no OCI credentials
yet.** Execute in order once access lands.

1. **[Phase 2 — NOT YET EXECUTED]** Auth + variables:
   `cp terraform/oci/terraform.tfvars.example terraform/oci/terraform.tfvars`,
   fill in tenancy/compartment OCIDs; confirm the pinned
   `kubernetes_version` is still offered and the target AD has
   VM.GPU.A10.1 capacity (see terraform/oci/README.md).
2. **[Phase 2 — NOT YET EXECUTED]** `terraform init` / `plan` / `apply` —
   creates VCN, OKE basic cluster, app pool (2x E4.Flex 4 OCPU/32 GB),
   GPU pool (1x VM.GPU.A10.1), OCIR repo, eval-artifacts bucket, and the
   `financial-agent-bv` StorageClass. First full apply may need the
   documented two-stage `-target` sequence.
3. **[Phase 2 — NOT YET EXECUTED]** Merge kubeconfig
   (`kubeconfig_command` output) and confirm both node pools are Ready.
4. **[Phase 2 — NOT YET EXECUTED]** Push the image: `docker login` to
   OCIR (`ocir_login_hint` output; password is an auth token), tag
   `financial-agent-app:local` as `ocir_app_repo_url` + tag, push.
5. **[Phase 2 — NOT YET EXECUTED]** Replace the `CHANGEME` OCIR values in
   `k8s/overlays/oke/kustomization.yaml` and
   `argo/overlays/oke/kustomization.yaml` with the pushed image ref.
6. **[Phase 2 — NOT YET EXECUTED]** Create secrets in the cluster: the
   same two-secret scheme as kind (`app-secrets`, `infra-secrets`), plus
   the OCIR pull secret every oke Deployment and the Argo workflow pods
   reference. Generate an **auth token** for your user (Console → User
   Settings → Auth tokens — it is not your console password; never
   commit it), then:

   ```bash
   kubectl -n financial-agent create secret docker-registry ocir-pull-secret \
     --docker-server=<region-key>.ocir.io \
     --docker-username='<tenancy-namespace>/<username>' \
     --docker-password='<auth-token>'
   ```

   (Federated/IDCS users: the username is
   `<tenancy-namespace>/oracleidentitycloudservice/<email>`.) Then
   `kubectl apply -k k8s/overlays/oke`. Verify: Postgres PVC binds on
   `financial-agent-bv` at 50Gi, all probes green, streamlit/api
   LoadBalancers get external IPs.

   **LoadBalancer ingress is deny-all by default.** Streamlit and the
   API carry no authentication, so the Terraform security list on the LB
   subnet is the only gate: `lb_allowed_cidrs` defaults to `[]` and the
   LBs serve nothing until you allowlist CIDRs in terraform.tfvars. The
   LB services pin `security-list-management-mode: "None"` so the OKE
   cloud controller cannot re-open `0.0.0.0/0` on its own. Trade-off:
   for a demo to an audience off your network you must either add their
   egress CIDR, or temporarily allowlist `0.0.0.0/0` — accepting that
   an unauthenticated research UI (and its API-key spend) is then
   world-reachable — and revert immediately after. The mcp service is
   never exposed; use `kubectl port-forward`.
7. **[Phase 2 — NOT YET EXECUTED]** `make argo-install`, then
   `kubectl apply -k argo/overlays/oke`; run the eval DAG end-to-end
   against hosted models first. To turn on eval artifact archival
   (off by default): create a write-capable PAR on the eval-artifacts
   bucket permitting objects under `eval-runs/`, and add
   `EVAL_ARTIFACTS_PUT_URL=<PAR URL>` to the `.env` that app-secrets is
   created from (a PAR is a bearer URL — never commit it). The aggregate
   step then archives `aggregate.json` + `results.json` per run,
   best-effort.
8. **[Phase 2 — NOT YET EXECUTED]** vLLM on the A10: upload the six
   files of `financial-lora-merged/` to the eval-artifacts bucket under
   a `financial-lora/` prefix (`oci os object put`), create a read-only
   pre-authenticated request (PAR) scoped to that prefix, set
   `MODEL_BASE_URL` in `k8s/vllm/overlays/oke-gpu/kustomization.yaml` to
   the PAR URL **locally, uncommitted** (a PAR is a bearer URL — treat
   it like terraform.tfvars), then
   `kubectl apply -k k8s/vllm/overlays/oke-gpu`. The `fetch-model` init
   container downloads the weights into an emptyDir at pod start — no
   cluster secrets, no IAM policies. Only after vLLM serves the model on
   the A10 may any doc claim it does; update CLAUDE.md at that point.
9. **[Phase 2 — NOT YET EXECUTED]** Point `LOCAL_MODEL_URL` at the vLLM
   Service with `LOCAL_MODEL_BACKEND=openai`, re-run the eval DAG against
   it, and re-run `scripts/cost_report.py` on OCI. Both numbers are **to
   be measured in Phase 2** — no OKE number exists yet.

## Invariants (both targets)

- kind stays a working target throughout the migration — overlays, never
  forked manifests. Equivalence proof: [verification.md](verification.md).
- The Argo eval DAG and nightly cron must keep passing; Celery stays
  request-time async (they are never merged).
- `python -m pytest tests/` (43 tests) must pass on every commit.
