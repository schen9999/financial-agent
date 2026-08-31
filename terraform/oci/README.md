# terraform/oci — OKE migration target

Terraform for the OCI deployment (Phase 1 of the OKE migration; see
[CLAUDE.md](../../CLAUDE.md)). The AWS config in [infra/](../../infra/) is the
retired ECS deployment and stays untouched.

## What this creates

| Resource | Detail |
|---|---|
| VCN | 10.0.0.0/16; public api (10.0.0.0/28) + lb (10.0.2.0/24) subnets, private workers (10.0.1.0/24); IGW, NAT, service gateway |
| OKE cluster | `BASIC_CLUSTER`, flannel overlay CNI, public API endpoint |
| App node pool | 2x VM.Standard.E4.Flex, 4 OCPUs / 32 GB each (= 16 vCPU / 64 GB schedulable) |
| GPU node pool | 1x VM.GPU.A10.1 (A10 24 GB) for vLLM; OKE GPU image auto-taints `nvidia.com/gpu:NoSchedule` |
| OCIR | `financial-agent/app` private repo (one image serves api/worker/streamlit/mcp + Argo eval templates) |
| Object Storage | `financial-agent-eval-artifacts` bucket, versioned, private |
| StorageClass | `financial-agent-bv` (Block Volume CSI, WaitForFirstConsumer, expandable) — PVCs must request >= 50Gi (OCI block volume minimum) |

## Phase 1 status — validate only

No OCI credentials exist yet. Only these are run (and must pass):

```sh
terraform -chdir=terraform/oci init -backend=false
terraform -chdir=terraform/oci fmt -check
terraform -chdir=terraform/oci validate
```

**No `plan` or `apply` until Phase 2.**

## Phase 2 checklist (when credentials land)

1. `cp terraform.tfvars.example terraform.tfvars` and fill in OCIDs (gitignored).
2. Confirm the pinned `kubernetes_version` is still offered:
   `oci ce cluster-options get --cluster-option-id all`.
3. Confirm A10 capacity in the target region/AD; set `gpu_availability_domain`
   if the default AD is out of capacity.
4. `terraform init` (real backend decision), `plan`, `apply`. The StorageClass
   rides the kubernetes provider whose config comes from the new cluster — if
   the first full apply fails on it, apply in two stages:
   `terraform apply -target=oci_containerengine_node_pool.app`, then `terraform apply`.
   The OCI CLI (`oci`) must be on PATH — the kubeconfig authenticates via exec.
5. Push the image: see `ocir_app_repo_url` / `ocir_login_hint` outputs
   (password is an auth token, not the console password).

## Known deltas from CLAUDE.md

- CLAUDE.md budgets "~400 GB block total" and PVCs for "Postgres/Redis".
  Redis is deliberately ephemeral (no PVC — see k8s/manifests/20-redis.yaml),
  so today only Postgres claims a volume. Boot volumes (2x100 + 250 GB) plus a
  50 GB Postgres PVC land at ~400 GB total.
