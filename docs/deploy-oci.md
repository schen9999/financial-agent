# Deploying on Oracle Cloud Infrastructure

How to stand up the Financial Research Agent on OCI as it runs in October
2026: the app plane, the Argo eval harness and a CPU model endpoint on an
OKE cluster, plus a GPU model endpoint on an A10 VM. This page is the
current procedure only. The dated record of how each step was first run,
and what broke, is [deploy-runbook.md](deploy-runbook.md); the topology is
[architecture.md](architecture.md#deployed-topology-october-2026).

Every step below maps to a runbook step marked EXECUTED, except where this
page says otherwise.

## What gets deployed

| Component | Where | Notes |
|---|---|---|
| App plane: FastAPI, Celery worker, Streamlit, MCP server, Redis, PostgreSQL | OKE, overlay `k8s/overlays/oke-provided` | Every Service ClusterIP; Postgres on a 50Gi `oci-bv` volume |
| Argo Workflows eval harness | OKE, `argo/install` + `argo/overlays/oke-provided` | One pod per ticker, an aggregate step, a 5% gate; nightly CronWorkflow suspended |
| CPU model endpoint: llama.cpp serving Qwen3.6-35B-A3B Q4_K_M | OKE, `k8s/llamacpp/overlays/oke-cpu` | Optional; keyed; off unless an `slm-full` arm or `SLM_FULL=true` |
| GPU model endpoint: the same GGUF on llama.cpp | A10 VM, single-node k3s, `k8s/llamacpp/overlays/k3s-gpu` | Optional; keyed; one NodePort open to the cluster's egress IP only |
| Worker autoscaling (KEDA) | OKE, `k8s/keda/` | Optional; scales the worker 1 to 4 on Redis queue depth |

The models in production are hosted (Anthropic). The self-served endpoints
exist for the evaluation; see [report.md](report.md).

## Resources

| Resource | Size used | Why |
|---|---|---|
| OKE cluster | v1.34.1, 4× VM.Standard.E5.Flex at 16 vCPU (two ~28 GiB and two ~58 GiB allocatable), amd64, no GPU | App plane, Argo, CPU endpoint |
| Block storage | StorageClass `oci-bv` (default): 50Gi for Postgres, 50Gi for the CPU endpoint's model file | 50Gi is the OCI volume minimum |
| CPU endpoint placement | 8 vCPU, 30Gi requested equal to limit | Fits only a ~58 GiB node; 8 vCPU is where prompt processing stops scaling ([gpu-inference.md](gpu-inference.md)) |
| GPU VM | VM.GPU.A10.1 (1× A10 24 GB), Ubuntu 22.04, NVIDIA driver 570 | The 20.4 GB GGUF loads fully on the A10 (20,488 of 23,028 MiB) |
| Registry | GHCR, private package, image pinned by git sha | cri-o pulls every image from a registry |
| Access hosts | A bastion and a private operator host with kubectl, helm, make, openssl, python3 3.6+ | Nothing is exposed publicly; access is by port-forward |

## Prerequisites

- An `.env` with `ANTHROPIC_API_KEY`, `NEWS_API_KEY` and `PINECONE_API_KEY`
  (unquoted values). Optional keys and every default:
  [configuration.md](configuration.md).
- Two GitHub tokens: one with `write:packages` on the build host, one with
  `read:packages` for the cluster's pull secret.
- A build host with Docker and buildx, logged in to `ghcr.io`.
- Anthropic credit for any eval: every arm calls the hosted judge. A
  10-ticker hosted run was estimated at about $0.90 (runbook, "OKE
  (provided cluster)" step 8).

Two facts about the operator host that every command depends on:

- kubectl there authenticates through the `oci` credential plugin, which
  reads stdin. Never pipe a secret into `ssh oke-operator 'kubectl …'`; land
  it in a 0600 file first, as below.
- Remote one-liners need an interactive shell:
  `ssh oke-operator 'bash -ic "kubectl …"' < /dev/null`.

## Part A: app plane and eval harness on OKE

**1. Build, push and pin the image** (build host, clean tree on `main`):

```bash
make oke-images      # refuses a dirty tree; pushes ghcr.io/schen9999/financial-agent-app:<sha>, pins both overlays
git commit -am "Pin oke-provided images to <sha12>" && git push
```

**2. Check out the pinned commit** (operator):

```bash
git clone https://github.com/schen9999/financial-agent.git && cd financial-agent   # or git pull
python3 scripts/pin_oke_image.py --check                  # prints the sha just pinned
kubectl get nodes -o wide && kubectl get storageclass     # 4 nodes; oci-bv (default)
```

**3. Create the secrets.** None are committed.

```bash
# operator: namespace and the pull secret from the read-only token
kubectl apply -f k8s/base/00-namespace.yaml
read -rs GHCR_PAT
kubectl -n financial-agent create secret docker-registry ghcr-pull-secret \
  --docker-server=ghcr.io --docker-username=schen9999 --docker-password="$GHCR_PAT"
unset GHCR_PAT
```

```bash
# laptop: copy .env to an owner-only file on the operator
ssh oke-operator 'umask 077; cat > ~/app-secrets.env' < .env
```

```bash
# operator: create app-secrets, then destroy the file
kubectl -n financial-agent create secret generic app-secrets \
  --from-env-file=$HOME/app-secrets.env --dry-run=client -o yaml | kubectl apply -f -
shred -u ~/app-secrets.env
```

`infra-secrets` (a random Postgres password) is created by the next step on
first run.

**4. Deploy the app plane** (operator):

```bash
make oke-up
kubectl -n financial-agent get pods -o wide     # all Running and Ready
kubectl -n financial-agent get pvc,svc          # PVC Bound on oci-bv; every Service ClusterIP
```

`oke-up` refuses to apply on a missing or mismatched pin, a missing `oci-bv`
StorageClass (wrong kubeconfig) or a missing secret, then waits on every
rollout.

**5. Install Argo and the eval workflows** (operator):

```bash
make argo-install
make argo-deploy ARGO_OVERLAY=oke-provided      # must print suspend=true
kubectl auth can-i create configmaps -n financial-agent --as system:serviceaccount:argo:argo   # yes
```

The last check matters for 40-ticker runs: the aggregate step's template
exceeds Argo's inline limit and is offloaded to a ConfigMap by the
controller.

**6. metrics-server, if absent** (operator). This is a cluster-level change:

```bash
kubectl get apiservice v1beta1.metrics.k8s.io && kubectl top nodes   # present: skip this step
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ && helm repo update
helm upgrade --install metrics-server metrics-server/metrics-server --version 3.14.0 --namespace kube-system
```

**7. Reach it** (port-forward only; this access path is written but not
marked executed in the runbook):

```bash
# operator
nohup kubectl -n financial-agent port-forward svc/streamlit 8501:8501 >/tmp/pf-streamlit.log 2>&1 &
nohup kubectl -n financial-agent port-forward svc/api 8000:8000 >/tmp/pf-api.log 2>&1 &
```

```bash
# laptop
ssh -N -L 32501:localhost:8501 -L 32080:localhost:8000 oke-operator
curl -s localhost:32080/health        # API; Streamlit at http://localhost:32501
```

A public Streamlit UI behind an allowlist, nginx and basic auth exists as a
separate, optional overlay: runbook, "Public Streamlit UI".

## Part B: CPU model endpoint on OKE (optional)

```bash
# operator: the endpoint's key and the GPU endpoint's settings, in one Secret
kubectl -n financial-agent create secret generic slm-endpoints \
  --from-literal=SLM_CPU_API_KEY=$(openssl rand -hex 32) \
  --from-file=SLM_GPU_API_KEY=$HOME/slm-gpu.key \
  --from-literal=SLM_GPU_URL=http://<node2-public-ip>:30880
shred -u ~/slm-gpu.key
kubectl -n financial-agent rollout restart deployment/api deployment/worker deployment/streamlit deployment/mcp
make oke-llamacpp
```

`~/slm-gpu.key` is the GPU endpoint's key from Part C, step 2; without a
GPU endpoint, drop those two lines. `make oke-llamacpp` downloads and
verifies the GGUF once into its own `oci-bv` volume, starts llama-server,
and checks the endpoint from inside the api pod, the harness's own path.

## Part C: GPU model endpoint on an A10 VM (optional)

This is the minimal path for a VM that serves only the llama.cpp endpoint.
It uses the same targets that ran on node 2, without the vLLM steps node 2
also ran; this exact order has not been run end to end on a fresh VM.

**1. Network baseline, then bootstrap** (OCI console, then the VM):
the subnet's security list admits 22/tcp from your CIDR only. Then:

```bash
git clone https://github.com/schen9999/financial-agent.git && cd financial-agent
bash scripts/vm_bootstrap.sh       # ufw, Docker, NVIDIA toolkit, k3s with the NVIDIA runtime, device plugin
export KUBECONFIG=$HOME/.kube/config
kubectl apply -f k8s/base/00-namespace.yaml
```

**2. The endpoint key** (laptop), one copy for each cluster:

```bash
GPU_KEY=$(openssl rand -hex 32)
printf %s "$GPU_KEY" | ssh <gpu-vm> 'KUBECONFIG=$HOME/.kube/config kubectl -n financial-agent \
  create secret generic llamacpp-api-key --from-file=LLAMA_API_KEY=/dev/stdin'
printf %s "$GPU_KEY" | ssh oke-operator 'umask 077; cat > ~/slm-gpu.key'      # used in Part B
unset GPU_KEY
```

**3. Serve the model** (VM):

```bash
make vm-llamacpp
curl -s -o /dev/null -w '%{http_code}\n' localhost:30880/v1/models   # 401: the key is enforced
```

The first run downloads 20.4 GB. The target prints the deployed arguments
and llama-server's own memory on the A10, and fails if no llama-server
process holds GPU memory. If the model does not fit, `make vm-llamacpp
NCMOE=<n>` keeps some experts in host memory; label every result from that
layout **hybrid**.

**4. Open exactly one port, to the cluster only.** Only after step 3 shows
401 without the key. The security list is the boundary, because k3s
NodePorts route around ufw; ufw is defense in depth:

```bash
set -a; . ~/financial-agent/.addresses.env; set +a       # OKE_EGRESS_IP, gitignored
sudo ufw allow from "$OKE_EGRESS_IP" to any port 30880 proto tcp
```

Then add one security-list rule: TCP 30880 from the cluster's egress IP
`/32`, never a range.

## Part D: worker autoscaling with KEDA (optional)

A cluster-level install; clear it with the cluster owner first.

```bash
make keda-install                                 # pinned chart, digest-checked, then a discovery check
make keda-worker KEDA_OVERLAY=oke-provided        # ScaledObject; HPA min 1, max 4
make keda-scale-test                              # no model calls: a builtin task backlog, 1 -> 4 -> 1
make keda-check                                   # API discovery healthy with KEDA installed
```

The builtin-task scale test ran 2026-10-16. Under brief load, with the
model replaced by a stub at A10-speed latency, KEDA delivered 704 briefs an
hour, 86% of a fixed four replicas
([harness-benchmark-plan.md](harness-benchmark-plan.md)).

## Verify

| Check | Command | Expect |
|---|---|---|
| App plane | `kubectl -n financial-agent get pods` | api, worker, streamlit, mcp, redis, postgres Running |
| Storage | `kubectl -n financial-agent get pvc` | Bound on `oci-bv` |
| Nightly eval off | `kubectl -n financial-agent get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.suspend}'` | `true` |
| API | `curl -s localhost:32080/health` (through the tunnel) | healthy |
| CPU endpoint | the last output of `make oke-llamacpp` | server facts from the api pod |
| GPU endpoint, from OKE | `kubectl -n financial-agent exec deploy/api -- env SLM_FULL=true SLM_ENDPOINT=gpu python -c "import json; from agent.tools.slm import server_facts; print(json.dumps(server_facts(), indent=1))"` | the served alias, n_ctx 32768 |

## Run an evaluation

```bash
make eval-run                                                    # hosted, 10 tickers: the platform check
make eval-run EVAL_RUN_FILE=argo/eval-run-extended.yaml          # hosted, 40 tickers
make slm-eval-run ENDPOINT=cpu EVAL_RUN_FILE=argo/eval-run-slm-cpu-smoke.yaml   # self-served, with the traffic proof
```

Nothing else may call a self-served endpoint during its run: the traffic
proof fails on foreign traffic, by design. Workflows and their pod logs are
deleted after 7 days, so capture the findings first: runbook, "OKE
(provided cluster)" step 9, and "Findings capture". Which results may be
quoted, and how: [numbers-of-record.md](numbers-of-record.md).

## Teardown

```bash
# operator, in this order
pkill -f 'kubectl -n financial-agent port-forward'
make keda-uninstall KEDA_OVERLAY=oke-provided    # if Part D ran
make oke-llamacpp-down                           # keeps the GGUF volume
kubectl delete -k argo/overlays/oke-provided
kubectl delete -k k8s/overlays/oke-provided      # deletes the Postgres PVC
kubectl -n financial-agent delete secret app-secrets infra-secrets ghcr-pull-secret slm-endpoints
kubectl delete namespace financial-agent
kubectl delete -k argo/install                   # only if nothing else uses Argo
helm uninstall metrics-server -n kube-system     # only if step 6 installed it
```

With `oci-bv`'s Delete reclaim policy, deleting the namespace removes the
block volumes and the stored briefs. On the A10 VM: `make vm-llamacpp-down`,
remove the ufw rule and the security-list rule, and
`sudo /usr/local/bin/k3s-uninstall.sh` to remove k3s. The VMs themselves are
stopped or terminated by the tenancy owner in the OCI console. GHCR image
versions stay until deleted from the package settings on GitHub.

## Constraints

- The provided cluster was not created by this repository's Terraform.
  Never run `terraform/oci` against it; `terraform/oci-provided/` is import
  and plan only ([its README](../terraform/oci-provided/README.md)).
- No IP address, OCID or resolvable hostname is committed. Real values
  live in the gitignored `.addresses.env` (template:
  `addresses.env.example`).
- vLLM serving on OKE has not run; the CPU endpoint is llama.cpp.
- A new image means every eval arm re-runs on it before arms are compared.
