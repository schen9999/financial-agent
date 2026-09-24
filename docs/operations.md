# Operations

How to bring up, use, and tear down the system as it runs today. This page
is the current procedure; [deploy-runbook.md](deploy-runbook.md) is the dated
history of how each step was first executed and what broke along the way.
Environment variables are in [configuration.md](configuration.md); costs in
[cost.md](cost.md).

## An OCI A10 node (single-node k3s)

The running target: a VM.GPU.A10.1 (1x A10 24 GB) with Ubuntu 22.04 and the
NVIDIA driver preinstalled, reachable by ssh only. Each node is its own
single-node k3s cluster. All commands run on the node, as `ubuntu`, from the
repository checkout, unless marked "laptop".

### 1. Network baseline (OCI console, before anything else)

The VCN security list on the node's subnet must admit only 22/tcp from your
allowlisted CIDR: no NodePort range (30000–32767), no 80/443. The security
list is the real gate; the node's ufw is defense in depth, because
kube-proxy programs NodePorts directly in iptables.

### 2. Bootstrap

```bash
git clone https://github.com/schen9999/financial-agent.git && cd financial-agent
git checkout oci-migration
bash scripts/vm_bootstrap.sh
```

The script is idempotent. It installs base packages, ufw (22/tcp only),
Docker CE with buildx, the NVIDIA container toolkit, k3s with the NVIDIA
runtime as default, the NVIDIA device plugin, the kubeconfig and
`KUBECONFIG` export, and the hostPath directories. It ends with a checklist
and exits non-zero on any FAIL row. On an A10.1, `nvidia.com/gpu`
allocatable reads 1. Log out and back in (or `newgrp docker`) before the
next step. If `nvidia-smi` is missing, install the driver first
(`sudo ubuntu-drivers install --gpgpu`, reboot) and rerun the script.

### 3. Model weights

```bash
# laptop: the merged fine-tune lives only on the dev machine
rsync -avP financial-lora-merged/ ubuntu@<node-ip>:/home/ubuntu/models/qwen-ft/
# node: rerun the bootstrap so step 9 strips the tokenizer key vLLM rejects
bash scripts/vm_bootstrap.sh
```

Rerun the bootstrap after **every** copy of weights: the checkpoint's
`tokenizer_config.json` carries an `extra_special_tokens` list that vLLM
v0.10.2 cannot parse (see Troubleshooting).

### 4. Build and deploy

```bash
make vm-images    # build the app image under BuildKit and import it into k3s
make vm-up        # app overlay + secrets, Argo install, Argo k3s overlay, then vLLM
```

`make vm-up` needs a filled-in `.env` in the checkout. It creates
`infra-secrets` (a random Postgres password) once, builds `app-secrets` from
`.env`, applies `k8s/overlays/k3s`, installs Argo, runs
`make argo-deploy ARGO_OVERLAY=k3s`, and finishes with `make vm-vllm`
(defaults: serve `financial-lora` from `/home/ubuntu/models/qwen-ft`). The
first run can sit in `ContainerCreating` for several minutes while the
multi-GB vLLM image downloads; `sudo k3s crictl pull docker.io/vllm/vllm-openai:v0.10.2`
beforehand front-loads that wait.

To re-apply only the eval workflow objects later:
`make argo-deploy ARGO_OVERLAY=k3s`.

### 5. Verify

```bash
kubectl -n financial-agent get pods,svc,pvc            # six services + vllm Running; postgres PVC Bound
kubectl -n argo get pods                                # workflow-controller, argo-server Running
kubectl -n financial-agent get cronworkflow grounding-eval-nightly \
    -o jsonpath='{.spec.suspend}'                       # must print: true
curl -s localhost:30880/v1/models                       # lists financial-lora
nvidia-smi                                              # vLLM's process on the A10
```

If the nightly does not read `true`, rerun `make argo-deploy ARGO_OVERLAY=k3s`.

### 6. Reach it from the laptop

```bash
# laptop — local ports 31xxx, because kind owns 30080/30501/30800 locally
ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<node-ip>
```

Then Streamlit is at http://localhost:31501, the API at
http://localhost:31080 (reference: [api.md](api.md)), and vLLM at
http://localhost:31880. MCP stays ClusterIP; to reach it, run
`kubectl -n financial-agent port-forward svc/mcp 30800:8000` on the node and
add `-L 31800:localhost:30800` to the tunnel.

For one-off commands without a login shell, pass the kubeconfig inline:
`ssh ubuntu@<node-ip> 'KUBECONFIG=$HOME/.kube/config kubectl -n financial-agent get pods'`.

### 7. Swap the served model

```bash
make vm-vllm MODEL_DIR=qwen2.5-7b-instruct SERVED_NAME=qwen2.5-7b-instruct MAX_LEN=4096
make vm-vllm                                   # back to the fine-tune (defaults)
```

Weights go under `/home/ubuntu/models/<MODEL_DIR>` first. The target
renders the k3s-gpu overlay with the three values swapped, applies it,
waits for the rollout, retries `/v1/models` for up to 120 s, and only then
sets `LOCAL_MODEL_NAME` and `LOCAL_MODEL_DIR` in `app-config`. `MAX_LEN` is
per model: a 7B bf16 leaves much less KV cache on the 24 GB A10 than the
1.5B. Swap only between runs, and only with `make vm-vllm`; applying the
k3s app or vLLM overlays by hand puts the served model and `app-config` out
of step. Compare only models that share a chat template (Qwen2.5 here).

### 8. Run an eval

```bash
make vm-eval                                                   # hosted models, 10 tickers
make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml           # local-model arm, 10 tickers
make eval-run EVAL_RUN_FILE=argo/eval-run-extended.yaml        # hosted, 40 tickers
make eval-run EVAL_RUN_FILE=argo/eval-run-extended-local.yaml  # local-model arm, 40 tickers
```

Every run spends Anthropic credits in every arm (Haiku sections, Sonnet
synthesis, the Sonnet judge); a low balance stops the run with a FATAL
message rather than skipping tickers. The aggregate prints the gate verdict,
the unsupported rate with its Wilson interval, and an estimated run cost.
Local-model runs first check that `/v1/models` lists `LOCAL_MODEL_NAME` and
record the served model and sampling in the findings. The gate fails the
workflow if unsupported claims exceed 5%, any ticker is skipped, or fewer
than 30 claims were audited.

### 9. Capture the findings

Workflows are deleted a day after they finish, so capture per-claim
evidence while the pods exist:

```bash
kubectl -n financial-agent logs -l workflows.argoproj.io/workflow=<wf> \
    --prefix --tail=-1 > eval/runs/raw/<wf>.log        # the log stays local (gitignored)
python3 scripts/extract_findings.py --log eval/runs/raw/<wf>.log --out eval/runs/raw/<wf>-findings/
python3 eval/parse_run_log.py --log eval/runs/raw/<wf>.log --run <workflow-name> \
    --findings-dir eval/runs/raw/<wf>-findings/ --contexts-dir eval/runs/<wf>-contexts \
    --out eval/runs/<wf>-claims.jsonl
```

On k3s the findings also stay on the node under
`/home/ubuntu/eval-findings/<workflow-name>/`. Commit the findings
directory, the claims file, and the contexts.

## Teardown

| Target | Stop the workload | Remove it entirely |
|---|---|---|
| kind (laptop) | `make vllm-down` (vLLM only) | `make cluster-down` deletes the cluster |
| k3s node | `kubectl delete -k k8s/vllm/overlays/k3s-gpu` frees the GPU; `kubectl delete -k k8s/overlays/k3s` removes the app | `sudo /usr/local/bin/k3s-uninstall.sh` removes k3s and everything in it (installed by the k3s installer the bootstrap runs) |
| The A10 VM itself | — | **Stopped or terminated by the tenancy owner in the OCI console.** Nothing in this repository stops or deletes the VMs. |
| AWS ECS | `infra/ecs-scale.sh 0` (the normal parked state; RDS keeps running) | `terraform destroy` in `infra/`; see [infra/README.md](../infra/README.md), "Teardown" |
| OKE (never applied) | — | `terraform destroy` in `terraform/oci/` if it is ever applied; see [deploy-runbook.md](deploy-runbook.md), "OKE (OCI)" |

## Troubleshooting

Each entry is an incident that actually happened; the dated account is in
[deploy-runbook.md](deploy-runbook.md) unless noted.

| Symptom | Cause | Fix |
|---|---|---|
| `vm_bootstrap.sh` dies at its sudo check on a fresh OCI image | `sudo -v` prompts for a password even with NOPASSWD | Fixed in the script (`sudo -n true`, 92f5b45); pull the latest checkout |
| `docker build` succeeds but the image lacks `app.py` | The legacy builder ignores `Dockerfile.k8s.dockerignore` and applies the ECS `.dockerignore` | Build under BuildKit: the Makefile sets `DOCKER_BUILDKIT=1`; the bootstrap installs buildx |
| vLLM crashloops with "unrecognized arguments: … serve" | `vllm/vllm-openai`'s entrypoint is already the API server | Fixed in the base manifest (`vllm serve` in `command:`) |
| vLLM crashes parsing `VLLM_PORT` | Kubernetes service links inject `VLLM_PORT=tcp://…` because the Service is named `vllm` | Fixed in the base (`enableServiceLinks: false`) |
| vLLM fails in its multi-process engine | The container's default 64 MiB `/dev/shm` | Fixed in the base (2 GiB memory-backed `/dev/shm`) |
| vLLM fails loading the tokenizer: `'list' object has no attribute 'keys'` | The checkpoint's `extra_special_tokens` list (newer transformers layout) | Rerun `bash scripts/vm_bootstrap.sh` after every weights copy |
| First `vm-up` sits in `ContainerCreating` for minutes | The multi-GB vLLM image is downloading | Wait, or pre-pull with `sudo k3s crictl pull docker.io/vllm/vllm-openai:v0.10.2` |
| `make vm-vllm` fails at `/v1/models` with connection refused right after the rollout | The NodePort can lag the rollout reporting ready | Fixed: the check retries for up to 120 s (b972f37) |
| `make vm-vllm` times out at the rollout after a model swap | `MAX_LEN` too large for the KV cache left beside the weights | `kubectl -n financial-agent logs deploy/vllm` states the largest length that fits; lower `MAX_LEN` |
| An eval pod exits FATAL: `LOCAL_MODEL_NAME` not listed on `/v1/models` | The served model and `app-config` are out of step | Swap only with `make vm-vllm`, and not during a run |
| An eval run stops with FATAL "credit balance too low" | The Anthropic account ran out of credits | Top up, then rerun; the guard exists so this is never mistaken for skipped tickers |
| The nightly CronWorkflow is scheduled on k3s | The k3s overlay's suspend was not the overlay applied | Verify `.spec.suspend` is `true`; rerun `make argo-deploy ARGO_OVERLAY=k3s` |
| `make argo-deploy` applied the kind overlay on the node | `ARGO_OVERLAY` defaults to `kind` | `make vm-up` passes `k3s`; by hand, pass `ARGO_OVERLAY=k3s` |
| "Address already in use" opening the tunnel | kind owns 30080/30501/30800 on the laptop | Use the 31xxx local ports shown above |
| `ssh <node> "kubectl …"` cannot find the cluster | One-shot ssh runs a non-login shell, so `~/.bashrc`'s `KUBECONFIG` is not loaded | Pass `KUBECONFIG=$HOME/.kube/config` inline |
| Per-claim findings missing after a run | Workflows and their pods are garbage-collected | Capture within a day (step 9); on k3s, copy from `/home/ubuntu/eval-findings/` |
| ECS `/research` returns 500 "invalid x-api-key" | A stale Anthropic key in Secrets Manager (observed 2026-09-24) | Update `financial-agent/ANTHROPIC_API_KEY`; a new task picks it up at start |
| ECS reports task health UNKNOWN | The task definition has no container health check (Fargate ignores the Dockerfile `HEALTHCHECK`) | Expected; check `GET /health` directly |
