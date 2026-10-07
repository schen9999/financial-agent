# Deploy runbook

> **Status:** The Terraform OKE path is authored and reviewed, never applied: no compartment for it was provisioned. A provided OKE cluster now exists: its app plane, Argo and a hosted smoke ran there on 2026-10-03, and its CPU SLM endpoint served one traffic-proven smoke (dated runs; per-step status in those sections). The demo runs on single-node k3s on OCI A10 VMs.

Four targets, one manifest tree: `kind` (local, fully working today),
`k3s` (single-VM validation, Phase 1.75), `oke-provided` (a provided OKE
cluster, hosted models only) and `oke` (the Terraform cluster, Phase 2).
Anything not yet executed is marked **NOT YET EXECUTED** with its phase;
everything else has been run end-to-end on this repo.

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

## Single-VM path (k3s) — Phase 1.75

Validation target: one OCI VM.GPU.A10.2 (2x A10 24 GB, 30-core Xeon,
472 GB RAM, 1 TB disk, Ubuntu 22.04, NVIDIA driver 570 preinstalled),
reachable by ssh only. Purpose: rehearse the full topology and validate
the committed A10 vLLM serving args before OKE exists — and serve as the
demo target if it doesn't (see the CLAUDE.md checkpoint). Steps are
marked EXECUTED only after the run is confirmed from the box with
terminal output; everything else stays NOT YET EXECUTED.

**Validated so far (2026-09-02, confirmed from the box):** vLLM v0.10.2
served the merged fine-tune on one A10 in **plain Docker — not yet via
k3s** — with exactly the committed oke-gpu args (`--dtype bfloat16
--max-model-len 4096 --max-num-seqs 8 --gpu-memory-utilization 0.90`,
`--served-model-name financial-lora`): model load 2.89 GiB, 16.72 GiB
KV cache available, 200 OK on `/v1/models` and `/v1/chat/completions`,
port bound to 127.0.0.1 only. This validates the serving image, tag,
and args that the k3s-gpu and oke-gpu overlays commit to.

**Validated 2026-09-03 (confirmed from the box):** `make vm-up` brought
the app topology up green on k3s — all six app deployments rolled out,
Postgres PVC bound on `local-path`, Argo controller/server rolled out,
eval WorkflowTemplate + CronWorkflow applied. vLLM crashlooped on a
base-manifest bug (args `vllm serve ...` fed to `vllm/vllm-openai`,
whose entrypoint is already the api server → "unrecognized arguments");
fixed in the base by moving `vllm serve` to `command:`. The re-run then
hit the two further k8s gotchas below (also fixed in the base).

**Validated 2026-09-03, later (confirmed from the box) — end to end:**
after commit 4032e73 the vLLM deployment rolled out green on k3s;
`/v1/models` on NodePort 30880 lists `financial-lora`; `nvidia-smi`
confirms serving pinned to one A10 (~21 GiB used on the single granted
device, the other idle). `make vm-eval` then ran the full grounding DAG
on the VM to `Succeeded`: 10/10 tickers, 66 claims, 3.03% unsupported (judge v1) —
GATE PASSED (≤ 5%, ≥ 30 claims). That run used hosted models via the
existing harness — it is not a numbers-of-record re-run, and no eval
has yet run against vLLM itself.

**Known k8s gotchas (vLLM — fixed in the base, apply to every overlay):**
- **Entrypoint collision.** `vllm/vllm-openai`'s entrypoint is already
  the API server, so `args: [vllm, serve, ...]` produced "unrecognized
  arguments" — the 2026-09-03 crashloop. The base puts `vllm serve` in
  `command:` (commit 4032e73).
- **Service links inject `VLLM_PORT`.** Because the Service is named
  `vllm`, Kubernetes' legacy service links put
  `VLLM_PORT=tcp://<ip>:8000` into the pod env, and vLLM's
  `get_vllm_port` crashes parsing it. The base sets
  `enableServiceLinks: false` on the pod spec.
- **`/dev/shm` too small.** The container default is 64Mi shm; vLLM's
  multi-process engine needs real shared memory. The base mounts an
  emptyDir (`medium: Memory`, `sizeLimit: 2Gi`) at `/dev/shm`.

**Hand-fix ledger (2026-09-02/03).** Everything applied by hand on the
box during the first bring-up now lives in exactly one place — the
bootstrap script, a committed manifest or Makefile line, or a numbered
step below — so a fresh VM needs no tribal knowledge:

| Applied by hand on the box | Now lives in |
|---|---|
| `ufw default deny incoming`, `allow 22/tcp`, `enable` | `scripts/vm_bootstrap.sh` step 2 (step 1 below) |
| Docker install, plus buildx so `docker build` runs under BuildKit — `Dockerfile.k8s` uses a per-Dockerfile ignore file (`Dockerfile.k8s.dockerignore`), a BuildKit-only feature; the legacy builder applies the ECS `.dockerignore` and drops `app.py` | bootstrap step 3; `DOCKER_BUILDKIT=1` inline on both Makefile `docker build` lines (`deploy`, `vm-images`) |
| `nvidia-container-toolkit`, `nvidia-ctk runtime configure --runtime=docker`, docker restart | bootstrap step 4 |
| k3s install; `default-runtime: nvidia` in `/etc/rancher/k3s/config.yaml` + k3s restart, so the device plugin's static manifest (no `runtimeClassName`) and the vLLM pod run under the nvidia runtime | bootstrap step 5 |
| `/etc/rancher/k3s/k3s.yaml` → `~/.kube/config`; `export KUBECONFIG=$HOME/.kube/config` in `~/.bashrc` | bootstrap step 6 |
| NVIDIA device plugin v0.17.0 static manifest | bootstrap step 7 |
| `mkdir /home/ubuntu/models /home/ubuntu/eval-findings` — the hostPath parents of the k3s-gpu and argo k3s overlays | bootstrap step 8 |
| `extra_special_tokens` deleted from `tokenizer_config.json` (2026-09-02) | bootstrap step 9, after every rsync (step 2 below) |
| vLLM `vllm serve` → `command:`, `enableServiceLinks: false`, 2Gi `/dev/shm` | `k8s/vllm/base` (gotchas above; commit 4032e73) |
| `make argo-deploy` applied the kind argo overlay (target was hardcoded) | Makefile `ARGO_OVERLAY` (`vm-up` passes `k3s`) |
| ssh tunnel local ports colliding with kind's 30xxx | step 5 below (31xxx) |
| Pre-pull of the multi-GB vLLM image before the first `vm-up` | step 3 below |

Steps (the hand-executed history is kept per step; the script itself has
not run yet):

**Step 0 (only if `nvidia-smi` is missing) — NOT YET EXECUTED.** The
script treats the driver as a precondition (the VM image used so far
ships driver 570) and dies at its step 0 when `nvidia-smi` is absent.
On a plain Ubuntu image install the driver first, then re-run the
script:

```bash
sudo apt-get update && sudo apt-get install -y ubuntu-drivers-common && sudo ubuntu-drivers install --gpgpu && sudo reboot
```

1. **[NOT YET EXECUTED — Phase 1.75: `scripts/vm_bootstrap.sh` supersedes
   the hand steps of 2026-09-02/03 in the ledger; each action it wraps
   ran by hand then, the script has not]** **Network baseline, then one
   run of the bootstrap script.** First, outside the VM: verify the VCN
   security list on the VM's subnet admits only 22/tcp from your
   allowlisted CIDR (no 30000–32767, no 80/443). The seclist is the
   authoritative gate: kube-proxy programs NodePorts directly in iptables
   and can route around host firewalls, so ufw is defense-in-depth, not
   the guarantee (EXECUTED 2026-09-03: an external probe of NodePort
   30880 from outside the VCN times out). NodePorts will bind on the VM,
   but nothing is publicly reachable while the seclist admits only 22.
   Then, on the VM, from the repo checkout, as `ubuntu` (not root):

   ```bash
   bash scripts/vm_bootstrap.sh
   ```

   One run takes a fresh Ubuntu 22.04 box with the driver preinstalled
   to vm-up-ready: base packages, ufw (22/tcp only), Docker CE + buildx,
   the container toolkit (+ Docker runtime), k3s with
   `default-runtime: nvidia`, kubeconfig + `KUBECONFIG`, the device plugin
   (v0.17.0), both hostPath parents, and the tokenizer strip whenever
   weights are present. It is idempotent (`set -euo pipefail`; every step
   no-ops when already done) and ends with a checklist — `nvidia-smi`,
   `kubectl get nodes` with `nvidia.com/gpu` allocatable (expect 2 on the
   A10.2), `docker buildx version`, ufw, Docker's nvidia runtime, k3s,
   kubeconfig, `local-path`, dirs, tokenizer — exiting non-zero on any
   FAIL row. Log out and back in afterwards (docker group, `KUBECONFIG`),
   or `newgrp docker`, before `make vm-images`.
2. **[EXECUTED 2026-09-02 by hand — weights on the VM and loading: 2.89 GiB
   into VRAM per the Docker smoke test above. The scripted strip is NOT
   YET EXECUTED]** Weights to `/home/ubuntu/models/qwen-ft` — the
   k3s-gpu overlay's hostPath (`type: Directory`, so the directory must
   exist before `vm-up`; step 1 created the parent). Primary path — rsync
   straight from the dev machine (the merged checkpoint
   `financial-lora-merged/`, six files, exists only there; nothing leaves
   your machines):
   `rsync -avP financial-lora-merged/ ubuntu@<vm-ip>:/home/ubuntu/models/qwen-ft/`.
   Fallback if rsync from this network is impractical: push the
   checkpoint to a **private** HF repo (`huggingface-cli upload`), then
   on the VM `huggingface-cli login` (token, never committed) and
   `huggingface-cli download <org>/<repo> --local-dir /home/ubuntu/models/qwen-ft`.
   Then re-run `bash scripts/vm_bootstrap.sh`: steps 1–8 no-op and step
   9 strips the key below; the checklist's "weights + tokenizer" row must
   read PASS.

   **Known fix (hit on the VM, 2026-09-02):** the checkpoint's
   `tokenizer_config.json` ships `extra_special_tokens` as a JSON
   **list** (newer transformers layout); the transformers bundled in
   vllm v0.10.2 crashes on it with `'list' object has no attribute
   'keys'`. Fix: delete the `extra_special_tokens` key — the special
   tokens remain fully defined in `tokenizer.json`. The VM's copy was
   fixed by hand; the repo's `financial-lora-merged/` is **untracked
   and still carries the list-form key**, so every rsync/upload
   re-breaks the VM until the strip runs again — which is why it is a
   bootstrap step and not a one-time edit.
3. **[EXECUTED 2026-09-03 — vm-images + vm-up fully green: app
   topology, Argo, eval CRDs, and (after the base fixes) the vLLM
   rollout with `/v1/models` answering on NodePort 30880]**
   `make vm-images && make vm-up`
   (on the VM, from the repo checkout). `vm-images` builds under
   BuildKit (`DOCKER_BUILDKIT=1` is inline on the build line; buildx
   from step 1). Expect the first `vm-up` to sit
   in ContainerCreating for several minutes: `vllm/vllm-openai:v0.10.2`
   is a multi-GB CUDA image. Optional pre-pull to front-load that wait:
   `sudo k3s crictl pull docker.io/vllm/vllm-openai:v0.10.2`.
4. **[EXECUTED 2026-09-03 — workflow Succeeded on the VM: 10/10
   tickers, 66 claims, 3.03% unsupported (judge v1), GATE PASSED (hosted models;
   not a numbers-of-record re-run)]** `make vm-eval` — the grounding
   gate must pass on the VM.
5. **[EXECUTED 2026-09-03 — /v1/models answered through the tunnel and
   Streamlit rendered in the browser]** Access via ssh tunnels ONLY
   (nothing else is admitted by the seclist). Use **non-30xxx local
   ports** — the kind cluster maps 30080/30501/30800 on the dev laptop,
   so binding the same numbers locally collides ("Address already in
   use", hit on first attempt):
   `ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<vm-ip>`
   then browse http://localhost:31501 (Streamlit) / :31080 (API) /
   :31880 (vLLM). mcp stays ClusterIP exactly as on oke — on the VM run
   `kubectl -n financial-agent port-forward svc/mcp 30800:8000` and add
   `-L 31800:localhost:30800` to the tunnel.

**Stale-image warning (eval-rigor changes).** The `eval-rigor` branch
changed code the eval pods run — `agent/grounding.py` (judge v2),
`agent/tools/{rag,sec,sec_common}.py` (Item 1A anchoring, CIK lookup),
`grounding_check.py`, `scripts/eval_aggregate.py`, and the `eval/`
package. After pulling it on the VM, the full new-image sequence is
`make vm-images`, `make vm-up`, `make argo-deploy ARGO_OVERLAY=k3s` —
all three **before any `make eval-run`**, or the pods run the old code
(and, without the argo-deploy, the old WorkflowTemplate).

**Eval against the in-cluster vLLM — EXECUTED 2026-09-03, GATE FAILED.**
`grounding-eval-local-dkghz` ran the `local-model` arm on the VM with
vLLM confirmed serving (20 POST `/v1/chat/completions`, 2 sections × 10
tickers, no retries): 10/10 tickers, 65 claims, 48 sup / 8 uns / 9 inf,
**12.31% unsupported (judge v1) vs the 5% gate — FAILED**. The same-day baseline
(`grounding-eval-6zwqf`, ~40 min earlier, same VM) passed at 3.03% (judge v1).
See the dated A/B in eval-methodology.md; the fine-tune serves but does
not clear the gate on its two sections, so `USE_LOCAL_MODEL` stays off.
(Process note: that run's `make argo-deploy` applied the **kind** argo
overlay — the target was hardcoded. The actual diff from the k3s render
is **none**: the two overlays render semantically identical resources,
verified with `render_diff.py` (5/5). `argo-deploy` is now
overlay-aware: `ARGO_OVERLAY`, default `kind`; `vm-up` passes `k3s`.)

Mechanics: the eval pods read `app-config` (envFrom), which on k3s
carries the pointer values (`LOCAL_MODEL_BACKEND=openai`,
`LOCAL_MODEL_URL` at the vllm Service, `LOCAL_MODEL_NAME=financial-lora`).
The harness pins `USE_LOCAL_MODEL` **per A/B arm by design** (no flag
leakage between arms), so the ConfigMap flag never routes an eval — it
governs the app services only. The switches are therefore:

- Eval vs vLLM: `make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml`
  — submits the `local-model` arm (fine-tune serves Financial Health +
  Risk Factors; Haiku keeps the other two sections).
- App plane: `make vm-local-model ON=true` (revert with `ON=false`;
  `kubectl apply -k k8s/overlays/k3s` also restores the committed
  `false`).

**Credits warning — every eval run burns Anthropic credits**, in every
arm: the LLM-as-judge is Sonnet, and Haiku generates sections (all four
in `baseline`, two even in `local-model`). Two mitigations are wired
in: the aggregate prints an **estimated per-run cost** (chars/4 tokens
priced from `scripts/model_prices.json`, labeled an estimate — the cost
of record stays `scripts/cost_report.py`), and a low balance now
**fails the run loudly** — `eval/runtime_guards.py` raises on the
Anthropic "credit balance" 400 instead of letting it exhaust the
per-ticker retry and surface as skipped tickers (the measured failure
mode of 2026-09-03, where mass skips were indistinguishable at a
glance from a data problem).

**Extended benchmark — EXECUTED 2026-09-05/06** (baseline `j4cnp` gate
PASSED at 3.06%, local-model `lsnnc` gate FAILED at 8.15%, judge v2;
recorded in eval-methodology.md — actual per-run cost estimates from the
aggregates: $2.36 + $2.44 ≈ $4.80 for the two arms).
`argo/eval-run-extended.yaml` runs 40 tickers
(`eval/tickers_extended.txt`: large-cap, volatile-earnings, small-cap,
clinical-stage biotech, non-US ADRs — deliberately stressing data
coverage; a test keeps the two files in sync). Cost estimate for the
**two-arm 40-ticker A/B**, derived from the committed price table
(`scripts/model_prices.json`) and chars/4 token estimates over the
committed judge artifacts — the same labeled-estimate method the cost
harness uses for its non-exact layer; it slightly **under**estimates
because findings artifacts omit the pre-written sections the judge also
reads: **~$1.41 judge** (80 Sonnet calls, ~2,190 in / ~740 out tokens
each) **+ ~$2.53 generation** (80 briefs × the then-current $0.0316)
**≈ $4 total**; the 2026-09-04 post-retrieval-fix re-estimate raised it
to **≈ $4.30**. Actuals came in at ≈ $4.80 (aggregate estimates above).

**Cost-of-record re-measure — EXECUTED 2026-09-06:** the pre-fix
$0.0316 record was measured on the harness default, a 3-ticker mean
over AAPL, NVDA, JPM (benchmarks.md pins the run via its per-ticker
token evidence). The like-for-like re-measure on the fixed pipeline,
same N and tickers, set the cost of record to **$0.0366/brief**
($0.0282 exact + $0.0084 RAG-internal estimate; run evidence
`cost_record_post_fix.json`):

```bash
python scripts/cost_report.py --tickers AAPL NVDA JPM --json-out cost_record_post_fix.json
```
Submit only after topping up credits:
`make eval-run EVAL_RUN_FILE=argo/eval-run-extended.yaml` (baseline
pass; the local-model pass is a second submission overriding `arms`).
The workflow raises `activeDeadlineSeconds` to 3h — 40 tickers at
parallelism 2 will not fit the template's 1h default.

### Rebuild on fresh nodes, 2026-09-23

Two fresh VM.GPU.A10.1 nodes (1x A10 24 GB; Ubuntu 22.04, NVIDIA driver
570 preinstalled), `vm-a10-inst-1` and `vm-a10-inst-2`, rebuilt from
this runbook; the 2026-09-02 VM.GPU.A10.2 is gone. On an A10.1 the
bootstrap checklist's `nvidia.com/gpu` allocatable reads 1, not 2.

- **First contact:** `scripts/vm_bootstrap.sh` died at its sudo check.
  `sudo -v` prompts for a password on these OCI images despite
  NOPASSWD; the check is now `sudo -n true` (commit 92f5b45).
- **Otherwise green on the first try, on both nodes:** bootstrap,
  `make vm-images`, `make vm-up`. vLLM served `financial-lora` with no
  manifest changes (the k3s-gpu overlay's one-GPU pin is the whole
  node on an A10.1).
- **Reproduction eval:** `grounding-eval-2nh8v` on `vm-a10-inst-1`,
  hosted-models arm, judge v2 — 0/87 unsupported (95% CI 0.0–4.2%),
  gate PASSED; a reproduction run, not a number of record
  (numbers-of-record.md, dated run records).

**Post-`vm-up` check — the nightly must be suspended.** On 2026-09-23
no committed manifest set `spec.suspend` on `grounding-eval-nightly`:
node 2 came up unsuspended, as the base renders it. Node 1 read `true`,
and nothing committed or recorded explains it (a hand suspend is
possible, not confirmed). That day `make argo-deploy` printed
"Nightly eval scheduled: ..." whether or not it was suspended, because it
read only the schedule; it now prints `suspend=<value>` (`<unset>` when
the field is absent) at the end of its "Nightly eval:" line. The k3s argo
overlay now sets `suspend: true` (kind and oke unchanged, proven with
`render_diff.py`), so `vm-up` applies it and should print `suspend=true`.
Verify directly as well:

```bash
kubectl -n financial-agent get cronworkflow grounding-eval-nightly \
    -o jsonpath='{.spec.suspend}'   # must print: true
```

Anything else means the k3s overlay was not the one applied: re-run
`make argo-deploy ARGO_OVERLAY=k3s`, then check again.

**One-shot ssh needs `KUBECONFIG` inline.** `ssh <host> "kubectl ..."`
runs a non-interactive shell that never loads `~/.bashrc`, so the
bootstrap's `KUBECONFIG` export is absent and kubectl can't find the
cluster. Pass it on the command line:

```bash
ssh ubuntu@<vm-ip> 'KUBECONFIG=$HOME/.kube/config kubectl -n financial-agent get pods'
```

### Model comparison — NOT YET EXECUTED

Runs the eval's local-model arm against a different open-weight model with
no hand-edited manifests. `make vm-vllm` renders the k3s-gpu overlay, swaps
three values (`scripts/vllm_model_swap.py`), applies, waits for the rollout,
confirms `/v1/models` on NodePort 30880 lists the served name, and only then
sets `LOCAL_MODEL_NAME` + `LOCAL_MODEL_DIR` in app-config. Defaults
(`qwen-ft`, `financial-lora`, 4096) reproduce the committed deployment byte
for byte; `vm-up` calls it with them. On the VM, from the repo checkout:

```bash
# 1. weights under /home/ubuntu/models/<dir> (gated models: huggingface-cli login first)
huggingface-cli download Qwen/Qwen2.5-7B-Instruct --local-dir /home/ubuntu/models/qwen2.5-7b-instruct
# 2. swap, 3. run the local-model arm, 4. restore the fine-tune
make vm-vllm MODEL_DIR=qwen2.5-7b-instruct SERVED_NAME=qwen7b MAX_LEN=8192
make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml
make vm-vllm
```

- **Sizing is per model.** bf16 is 2 bytes per parameter, so a 7B model's
  weights take roughly 15 GB of the A10's 24 GB; what remains under
  `--gpu-memory-utilization=0.90` is KV cache, which bounds `MAX_LEN`. If it
  doesn't fit, vLLM refuses to start and its log states the largest length
  that would; `vm-vllm` then fails at the rollout wait — read
  `kubectl -n financial-agent logs deploy/vllm` and lower `MAX_LEN`.
- **Same request for every model.** `LocalChat` sends every sampling
  parameter explicitly: temperature 0.1, max_tokens 512, top_p 0.8,
  top_k 20, repetition_penalty 1.1, min_p 0.0 (`PINNED_SAMPLING` in
  `agent/tools/local_model.py`). Unpinned, vLLM v0.10.2 fills omitted
  parameters from each model's own `generation_config.json`
  (Qwen2.5-7B-Instruct: repetition_penalty 1.05). The pinned values are
  the fine-tune's effective ones, so its behaviour is unchanged. The
  prompt text is identical too; only the `model` field differs.
- **Provenance.** Every local-model row records the served name, model dir,
  backend, URL, and the sampling parameters sent — in the findings
  `## Metadata` block and on `local model :` / `local sampling :` lines in
  the aggregate (which warns if one run mixed models). Each eval pod first
  checks `/v1/models` and exits FATAL if `LOCAL_MODEL_NAME` isn't listed.
- **In scope: same-family comparisons only.** vLLM still applies each
  model's own chat template. Qwen2.5 models, the fine-tune included,
  inject the same default system prompt, so they compare cleanly.
  Cross-family comparisons need template handling and are out of scope:
  Llama 3.x adds a date/knowledge-cutoff system header, and Qwen3-style
  thinking models emit reasoning text that would land in the section the
  judge reads.
- **Swap only with `vm-vllm`, and not mid-run.** Pods read app-config at
  start. `kubectl apply -k k8s/overlays/k3s` resets `LOCAL_MODEL_NAME`, and
  `kubectl apply -k k8s/vllm/overlays/k3s-gpu` reverts vLLM to the
  fine-tune; either alone leaves the pair out of step. The preflight
  catches a name mismatch, but `LOCAL_MODEL_DIR` is only as current as the
  last `vm-vllm`.
- **App plane.** api/worker/streamlit keep their old env until restarted;
  if they route locally, re-run `make vm-local-model ON=true` after a swap.

### CPU inference benchmark (executed 2026-09-28 on `vm-a10-inst-2`)

Serves the same weights on the node's Xeon with the vLLM CPU backend and
runs the A10 benchmark client and shape against it. Plain Docker on the
host, outside k3s; no manifest changes. Results and method:
eval-methodology, "CPU inference benchmark". On a node rebuilt from this
runbook (weights under `/home/ubuntu/models`, the `extra_special_tokens`
fix applied to `qwen-ft`), from the repo checkout:

```bash
# 0. The vLLM CPU backend needs AVX-512: this must print avx512f
grep -ow avx512f /proc/cpuinfo | head -1
docker pull public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2
# 1. Quiet the node: scale the app plane to 0 (postgres, redis, argo and the
#    idle GPU vLLM stay up; check `kubectl top pods -A` shows them idle)
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=0
# 2. A10, CPU container stopped, against the running pod; seeds the pod
#    has not served (it keeps its prefix cache until restarted)
A=eval/runs/bench/a10-$(date +%F); mkdir -p $A
SEED=1 bash scripts/vm_bench_serve.sh financial-lora > $A/financial-lora-c8.json
CONCURRENCY=1 NUM_PROMPTS=50 SEED=2 bash scripts/vm_bench_serve.sh financial-lora \
  > $A/financial-lora-c1.json
# 3. CPU, a fresh server per model (about 36 min at c=8, 12 min at c=1)
D=eval/runs/bench/cpu-$(date +%F); mkdir -p $D
bash scripts/vm_bench_cpu.sh serve qwen-ft financial-lora
SEED=1 bash scripts/vm_bench_cpu.sh bench financial-lora 8 200 > $D/financial-lora-c8.json
SEED=2 bash scripts/vm_bench_cpu.sh bench financial-lora 1 50  > $D/financial-lora-c1.json
bash scripts/vm_bench_cpu.sh stop
#    (repeat serve/bench/stop with qwen2.5-1.5b-instruct for the base row)
# 4. Restore the app plane and confirm every pod is Running
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=1
kubectl -n financial-agent get pods
# 5. Table and the per-brief section time, from the committed files
python scripts/bench_table.py $A/financial-lora-c8.json=A10 $A/financial-lora-c1.json=A10 \
  $D/financial-lora-c8.json=CPU $D/financial-lora-c1.json=CPU \
  --section-tokens 530 --section-tokens 1024
```

- **Prefix caching.** Both servers run with vLLM's default prefix
  caching, so a prompt the server has already seen skips most of its
  prefill. Both scripts warm up on `WARMUP_SEED` (default 1000), never the
  timed `SEED`, and write the prefix-cache hit share of the timed run into
  the result JSON; `bench_table.py` prints it. Expect about 1-2% (the
  client's initial test request re-sends the first prompt). A seed's first
  N prompts are the same at any `--num-prompts` of N or more, so each timed
  run on one server needs its own seed. The 2026-09-23 A10 files were run
  before this and have their first 16 timed prompts cached.

- **Pinning.** The server container gets `--cpuset-cpus 2-29` (14 physical
  cores, 28 vCPUs; on this shape SMT siblings are pairs 2k, 2k+1) and one
  OMP thread per physical core (`VLLM_CPU_OMP_THREADS_BIND=2,4,...,28`);
  the client container runs on core 0 (vCPUs 0-1), which it shares with
  k3s. Other shapes: set `SERVER_CPUS`, `OMP_BIND` and `CLIENT_CPUS` from
  `lscpu -e` before running. Each result JSON records the pinning.
- **Same client and prompts as the A10.** `vllm bench serve` v0.10.2 from
  the CPU image, the tokenizer mounted at `/models/financial-lora` as in
  the pod, and the same seeds; each CPU file's total input tokens match
  the A10 file with the same seed and prompt count.
- **Nothing is exposed.** The server binds 127.0.0.1:8100 on the host.

### Quantization benchmark (executed 2026-09-29 on `vm-a10-inst-2`)

W4A16 on the A10 (speed and a grounding arm), GGUF builds on the Xeon.
Results and method: eval-methodology, "Quantization benchmark". From a
checkout of the branch on the node, with the node as left by the CPU
benchmark above. Long CPU steps belong in tmux so a dropped ssh session
does not end them.

```bash
# 1. W4A16 weights (throwaway venv; llm-compressor stays out of the image)
python3 -m venv ~/venvs/llmc && ~/venvs/llmc/bin/pip install llmcompressor==0.7.1
kubectl -n financial-agent scale deployment/vllm --replicas=0   # free the A10
~/venvs/llmc/bin/python scripts/quantize_w4a16.py --num-samples 104
# 2. Serve it (vLLM reads the scheme from config.json) and bench, quiet node
make vm-vllm MODEL_DIR=qwen-ft-w4a16 SERVED_NAME=financial-lora-w4a16 MAX_LEN=4096
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=0
A=eval/runs/bench/a10-quant-$(date -u +%F); mkdir -p $A
cp /home/ubuntu/models/qwen-ft-w4a16/quant_meta.json $A/
SEED=1 bash scripts/vm_bench_serve.sh financial-lora-w4a16 > $A/financial-lora-w4a16-c8.json
CONCURRENCY=1 NUM_PROMPTS=50 SEED=2 bash scripts/vm_bench_serve.sh financial-lora-w4a16 \
  > $A/financial-lora-w4a16-c1.json
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=1
# 3. Grounding arm on the same image (no vm-images), then findings capture below
make eval-run EVAL_RUN_FILE=argo/eval-run-extended-local-w4a16.yaml
make vm-vllm                                   # back to the BF16 fine-tune
# 4. GGUF: convert, then per file serve / c8 x 200 seed 1 / c1 x 50 seed 2 / stop
bash scripts/vm_bench_cpu_gguf.sh convert qwen-ft
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=0
G=eval/runs/bench/cpu-gguf-$(date -u +%F); mkdir -p $G
cp /home/ubuntu/models/qwen-ft-gguf/gguf_meta.json $G/
for q in f16 q8_0 q4_k_m; do
  bash scripts/vm_load_sampler.sh llama-cpu $G/load-financial-lora-$q.log & S=$!
  bash scripts/vm_bench_cpu_gguf.sh serve qwen-ft-gguf/financial-lora-$q.gguf financial-lora-$q
  SEED=1 bash scripts/vm_bench_cpu_gguf.sh bench financial-lora-$q 8 200 > $G/financial-lora-$q-c8.json
  SEED=2 bash scripts/vm_bench_cpu_gguf.sh bench financial-lora-$q 1 50 > $G/financial-lora-$q-c1.json
  bash scripts/vm_bench_cpu_gguf.sh stop; kill $S
done
# 5. Sweeps (vLLM BF16 at 7 and 14 threads; llama.cpp Q4_K_M at 14). On
#    2026-09-29 the llama.cpp sweep stopped at concurrency 2 (lost requests,
#    see below); the vLLM sweep completed
W=eval/runs/bench/cpu-sweep-$(date -u +%F); mkdir -p $W
bash scripts/vm_bench_cpu.sh sweep qwen-ft financial-lora $W
bash scripts/vm_bench_cpu_gguf.sh sweep qwen-ft-gguf/financial-lora-q4_k_m.gguf financial-lora-q4_k_m $W
kubectl -n financial-agent scale deploy api worker streamlit mcp --replicas=1
```

- **Token counts on llama.cpp** come from the server, not the client's
  re-tokenization, and a run is refused unless they are exactly 256 per
  completed request (`scripts/bench_fix_llamacpp.py`).
- **A lost request** (aiohttp `Server disconnected` before any response
  header, never reaching the server: llama-server closes every streamed
  response's connection while advertising keep-alive) is recorded, not
  retried; more than 1% of prompts lost (at least one allowed), or any
  other error, refuses the run. Low-concurrency llama.cpp cells are the most exposed (the Q4_K_M
  sweep's concurrency-2 cell lost 4 of 32). Do not rerun a refused run
  until one passes; record it as refused.
- **Calibration count.** `data/sections_dataset.jsonl` has 104 rows;
  `--num-samples` above 104 is refused rather than padded with repeats.

## Findings capture — after any eval run

Every eval pod and the aggregate print a base64 tar of
`/app/eval_findings` to stdout under `===EVAL_FINDINGS_TGZ_BEGIN/END===`
markers — the per-claim judge evidence (metadata, retrieved context,
judge-input sections, audited text, findings). Capture it while the
pods still exist, extract, and commit:

```bash
kubectl -n financial-agent logs -l workflows.argoproj.io/workflow=<wf> \
    --prefix --tail=-1 > eval/runs/raw/<wf>.log
python scripts/extract_findings.py --log eval/runs/raw/<wf>.log \
    --out eval/runs/raw/<wf>-findings/
git add eval/runs/raw/<wf>-findings/   # the log stays local (gitignored:
                                       # its payload duplicates the dir)
```

The label-selector capture takes every pod's dump — required on kind,
where the findings volume is a per-pod emptyDir; on k3s the volume is a
shared hostPath (`/home/ubuntu/eval-findings/<wf>` on the VM), so the
aggregate pod's dump alone is already complete and the hostPath is a
second copy. Per-claim rows (commit these too) then come from
`eval/parse_run_log.py --findings-dir eval/runs/raw/<wf>-findings/`
with `--contexts-dir eval/runs/<wf>-contexts --out
eval/runs/<wf>-claims.jsonl`.

If a run's aggregate step did not run (workflow Error after every eval pod
completed), the aggregate can be rebuilt from the same log with the
unchanged aggregate code — and must be recorded as rebuilt:

```bash
python scripts/results_from_pod_log.py --log eval/runs/raw/<wf>.log \
    --out eval/runs/<wf>-results-rebuilt.json --aggregate-out eval/runs/<wf>-aggregate.txt
```

It stops if a pod's printed counts, LLM call lines or attempt record do
not agree with its findings; the estimated run cost cannot be rebuilt.
Used for `9jzmj` (2026-10-04) after validating it line for line against
`7c66k`'s in-cluster aggregate.

A workflow object for a 40-ticker run carries its nodes in
`status.compressedNodes`: read it through `python3 scripts/workflow_nodes.py
expand` (the make targets do) before `eval/attempts.py`.

Emergency fallback if the logs are gone too (used 2026-09-05 to recover
9j2dj): deleted pods' written files survive in containerd snapshot upper
layers — on the node, `find` the containerd root (k3s:
`/var/lib/rancher/k3s/agent/containerd`) under
`io.containerd.snapshotter.v1.overlayfs/snapshots` for `eval_findings`.

## OKE (provided cluster)

An OKE cluster provisioned for us — **not** created by `terraform/oci`
(never run it against this cluster): OKE v1.34.1, four
VM.Standard.E5.Flex amd64 nodes at 16 vCPU (two ~28 GiB, two ~58 GiB
allocatable), no GPUs, cri-o (no image import: everything pulls from a
registry), default StorageClass `oci-bv`. **CPU-only harness: no vLLM, no
GPU resources, `USE_LOCAL_MODEL=false`; hosted models unless an `slm-full`
arm is run.** Nothing here may be cited as vLLM serving on OKE; SLM serving
on it is the llama.cpp CPU endpoint of the next section, citable only as
far as that section's EXECUTED steps state.

Overlays: `k8s/overlays/oke-provided` + `argo/overlays/oke-provided`
(the Terraform path keeps `oke`). App image from GHCR, pinned by git sha
in both overlays (`scripts/pin_oke_image.py`); postgres/redis fully
qualified for cri-o; Postgres PVC on `oci-bv` at 50Gi (the block volume
floor); every Service ClusterIP — no LoadBalancer, no NodePort; nightly
CronWorkflow suspended; workflow ttlStrategy 7 days.

Where commands run: **laptop = WSL** (the `oke-bastion` / `oke-operator`
ssh aliases live in WSL's `~/.ssh/config`); **node 2** (`ssh oci2`) builds
and pushes the image (step 1); **operator** = the private host with
kubectl/helm, reached as `ssh oke-operator` (ProxyJump through
`oke-bastion`).

Two operator facts, found 2026-10-03, that every remote command below
depends on:

- **kubectl on the operator authenticates through the `oci` credential
  plugin, and that plugin reads stdin.** Anything piped into
  `ssh oke-operator 'kubectl ...'` is consumed by the plugin, not by
  kubectl, so `--from-file=/dev/stdin` and `--from-env-file=/dev/stdin`
  do not work there. (Streaming into node 2's k3s works as written: k3s
  has no credential plugin.)
- **A non-interactive ssh command does not get the operator's interactive
  environment.** `ssh oke-operator 'bash -lc "kubectl ..."'` fails
  (`getting credentials: exec: executable oci failed with exit code 1`);
  `ssh oke-operator 'bash -ic "kubectl ..."' < /dev/null` works — the
  interactive shell reads `~/.bashrc`. It prints two job-control warnings
  on stderr (`cannot set terminal process group`, `no job control in this
  shell`); they are harmless. Read-only example, the one that fetched
  `eval/runs/x2cx8-workflow.json`:
  ```bash
  ssh oke-operator 'bash -ic "kubectl -n financial-agent get workflow <wf> -o json"' < /dev/null > eval/runs/<wf>-workflow.json
  ```

1. **[EXECUTED 2026-10-03 — image `2dd1aa38bb3e` built and pushed from
   node 2, pinned in commit `0ad7d42`; the hosted smoke's pods ran
   `ghcr.io/schen9999/financial-agent-app:2dd1aa38…`
   (`eval/runs/x2cx8-workflow.json`)]** Build, push, pin — **node 2
   (`ssh oci2`), not the laptop**: on 2026-10-03 the laptop's WSL disk
   filled during a build and WSL then failed to start. Clean tree on the
   pushed commit to deploy: `slm-harness`, which carries everything on
   `oke-deploy` plus the SLM work, so one image serves the hosted smoke,
   every SLM run and the hosted baseline. GHCR login needs a PAT with
   `write:packages` (a separate one from the cluster's read-only PAT):
   ```bash
   # node 2
   cd ~/financial-agent && git fetch && git checkout slm-harness && git pull
   docker login ghcr.io -u schen9999 --password-stdin   # paste the write PAT, then Ctrl-D
   make oke-images      # refuses a dirty tree; pushes ghcr.io/schen9999/financial-agent-app:<sha>
   # the target edited the pin into both oke-provided overlays: carry that
   # edit off as a patch and leave node 2's tree clean (nothing is committed here)
   git diff > /tmp/pin.patch && git checkout -- .
   ```
   ```bash
   # laptop, from the repo, on the same commit: apply, commit and push the pin
   scp oci2:/tmp/pin.patch /tmp/pin.patch
   git apply /tmp/pin.patch
   git commit -am "Pin oke-provided images to <sha12>" && git push
   ```
   The tag is the commit the image was built from; the pin commit comes
   after it. New GHCR packages are private, hence the pull secret below.
   A new image re-runs every arm on it: hosted smoke, CPU smoke, then the
   extended runs.
2. **[EXECUTED 2026-10-03 — no separate capture; evidenced by step 8's
   run on the pinned image]** Repo on the operator. The repo is public —
   no PAT to clone:
   ```bash
   ssh oke-operator
   git clone https://github.com/schen9999/financial-agent.git && cd financial-agent
   git checkout slm-harness         # the branch carrying the pin; or git pull, if already cloned
   python3 scripts/pin_oke_image.py --check     # must print the sha just pinned
   kubectl get nodes -o wide && kubectl get storageclass   # 4 nodes; oci-bv (default)
   ```
   The operator needs `make`, `openssl`, `python3` (stdlib only, 3.6+
   syntax) and github.com egress (`make argo-install` fetches the pinned
   Argo release manifest).
3. **[EXECUTED 2026-10-03 with the temp-file method below — the stdin
   form first written here does not work on the operator]** Secrets — none
   committed; on the operator a secret exists on disk only as a 0600 temp
   file, shredded as soon as the Secret is created:
   ```bash
   # operator: namespace, then the GHCR pull secret from a read:packages PAT
   kubectl apply -f k8s/base/00-namespace.yaml
   read -rs GHCR_PAT    # paste the read-only PAT (not echoed, not in history)
   kubectl -n financial-agent create secret docker-registry ghcr-pull-secret \
     --docker-server=ghcr.io --docker-username=schen9999 --docker-password="$GHCR_PAT"
   unset GHCR_PAT
   ```
   ```bash
   # laptop (WSL), from the repo: .env to a 0600 file on the operator.
   # cat reads the stream here, not kubectl, so the credential plugin
   # cannot swallow it; umask 077 makes the file owner-only from creation
   # (plain scp would keep the source file's mode).
   ssh oke-operator 'umask 077; cat > ~/app-secrets.env' < .env
   ```
   ```bash
   # operator (interactive shell): create the Secret, then destroy the file
   kubectl -n financial-agent create secret generic app-secrets \
     --from-env-file=$HOME/app-secrets.env --dry-run=client -o yaml | kubectl apply -f -
   shred -u ~/app-secrets.env
   ```
   Do **not** stream it into kubectl over ssh
   (`ssh oke-operator 'kubectl ... --from-env-file=/dev/stdin' < .env`):
   the OKE `oci` credential plugin consumes stdin, and a non-login ssh
   command lacks the plugin's PATH (see "Where commands run"). The same
   applies to `slm-endpoints` (SLM step 1).
   Same keys as `make deploy` / `vm-up` (`--from-env-file` of the whole
   `.env`; `REDIS_URL` / `DATABASE_URL` in it are overridden by app-config
   and infra-secrets, later in `envFrom`). `--from-env-file` skips comments
   and blank lines and keeps `=` and spaces inside values (verified on
   kind 2026-10-02). kubectl does **not** strip quotes,
   so `.env` values must be unquoted. The pull secret lives in
   `financial-agent` only: the workflow pods run there, and nothing in
   `argo` pulls from GHCR. `infra-secrets` (random Postgres password) is
   generated by `oke-up` on first run, as on k3s.
4. **[EXECUTED 2026-10-03 — api, mcp, postgres, redis, streamlit and
   worker pods Running throughout `eval/runs/top-hosted-smoke.txt`]** App
   plane — operator:
   ```bash
   make oke-up
   kubectl -n financial-agent get pods -o wide   # all Running/Ready, spread over nodes
   kubectl -n financial-agent get pvc,svc        # PVC Bound on oci-bv; every svc ClusterIP
   ```
   `oke-up` refuses to apply on an UNPINNED or mismatched pin, a missing
   `oci-bv` StorageClass (wrong kubeconfig), or missing `app-secrets` /
   `ghcr-pull-secret`, then waits on every rollout (the first Postgres
   rollout includes provisioning and attaching the block volume). The
   bound PV is 50Gi (`kubectl get pv`); a smaller request would only be
   rounded up to the OCI floor.
5. **[EXECUTED 2026-10-03 — evidenced by workflow `grounding-eval-x2cx8`
   Succeeded, step 8]** Argo — operator:
   ```bash
   make argo-install
   make argo-deploy ARGO_OVERLAY=oke-provided    # must print suspend=true
   ```
   `argo-deploy` also applies the eval RBAC from `argo/base/rbac.yaml`,
   including — since 2026-10-04 — the Role that lets the Argo
   **controller** (ServiceAccount `argo` in namespace `argo`) create
   ConfigMaps in `financial-agent`. A 40-ticker run needs it: the
   aggregate's template exceeds Argo's 131,072-byte inline limit and is
   offloaded to a ConfigMap (eval-methodology, "the aggregate step's
   template outgrew Argo's inline limit"). Check it before any extended
   run:
   ```bash
   kubectl -n financial-agent get role,rolebinding argo-controller-template-offload
   kubectl auth can-i create configmaps -n financial-agent --as system:serviceaccount:argo:argo   # yes
   ```
   `argo-deploy` runs the same pin check for this overlay. The nightly
   CronWorkflow ships suspended (every fire spends Anthropic credits);
   evals here are submitted by hand with `make eval-run`.
6. **[EXECUTED 2026-10-03 — installed via helm chart 3.14.0 (app
   v0.9.0), not the 3.12.2 first written here; `kubectl top` output is the
   two `eval/runs/top-*-smoke.txt` captures]** metrics-server — check
   first; installing it is a **cluster-level change** (kube-system,
   cluster-wide API service):
   ```bash
   kubectl get apiservice v1beta1.metrics.k8s.io && kubectl top nodes   # present? stop here
   # absent: install the pinned chart via helm
   helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
   helm repo update
   helm search repo metrics-server/metrics-server --versions | head -5   # 3.14.0 must be listed
   helm upgrade --install metrics-server metrics-server/metrics-server \
     --version 3.14.0 --namespace kube-system
   kubectl -n kube-system rollout status deploy/metrics-server --timeout=180s
   kubectl top nodes
   ```
   Chart 3.14.0 = metrics-server v0.9.0. If `kubectl top` reports
   kubelet x509 errors, stop: `--kubelet-insecure-tls` weakens kubelet
   TLS verification cluster-wide and is a decision, not a workaround.
7. **[NOT YET EXECUTED]** Access — port-forward only:
   ```bash
   # operator (binds the operator's localhost only)
   nohup kubectl -n financial-agent port-forward svc/streamlit 8501:8501 >/tmp/pf-streamlit.log 2>&1 &
   nohup kubectl -n financial-agent port-forward svc/api 8000:8000 >/tmp/pf-api.log 2>&1 &
   ```
   ```bash
   # laptop (WSL); local 32xxx so kind (30xxx) and the k3s tunnel (31xxx) stay free
   ssh -N -L 32501:localhost:8501 -L 32080:localhost:8000 oke-operator
   curl -s localhost:32080/health
   curl -s -X POST localhost:32080/research -H 'Content-Type: application/json' \
     -d '{"ticker":"AAPL"}' | python3 -m json.tool | head -40
   # Streamlit: http://localhost:32501
   ```
   Optional Argo UI: `kubectl -n argo port-forward svc/argo-server
   2746:2746` on the operator plus `-L 32746:localhost:2746`.
8. **[EXECUTED 2026-10-03 — `grounding-eval-x2cx8` Succeeded 11/11 on
   image `2dd1aa3`: 10/10 tickers, 84 claims, 2/84 = 2.38% unsupported
   (Wilson 95% CI 0.7–8.3%), judge v2, stock block empty 0/10, gate passed
   (`eval/runs/hosted-smoke.log`). Its printed LLM-call table
   double-counts the two RAG sites — see the note after this step]**
   Hosted smoke = platform validation (10 tickers,
   hosted baseline arm, judge v2, RAG faithfulness on; the first eval on
   the cluster, on the same pinned image as every later run). An
   estimated ~$0.90 of Anthropic credit: dvvxk's harness estimate of
   $2.34 per 40 tickers scaled to 10, plus ~$0.03/ticker for the two
   RAG-faithfulness judge calls. On the operator, in two shells:
   ```bash
   make eval-run          # argo/eval-run.yaml; prints "submitted workflow: <wf>"
   ```
   ```bash
   WF=<wf>; OUT=~/$WF-top.txt; : > $OUT
   while :; do
     P=$(kubectl -n financial-agent get workflow $WF -o jsonpath='{.status.phase}')
     case "$P" in Succeeded|Failed|Error) echo "=== $(date -u +%FT%TZ) phase=$P" >> $OUT; break;; esac
     { echo "=== $(date -u +%FT%TZ) phase=$P"; kubectl top pods -n financial-agent --containers; kubectl top nodes; } >> $OUT
     sleep 15
   done
   ```
   Then capture (step 9) and check the aggregate output: `stock block
   empty : N/10` (briefs written without stock data — a swallowed
   yfinance failure; Yahoo has returned 429 from this egress IP) and
   `tickers skipped`. Grep the log for `429` / `Too Many Requests` too.
   This is a dated **platform-validation run, not a number of record**;
   report it with its Wilson CI and the judge v2 calibration note.

   **x2cx8, as measured (2026-10-03).** The aggregate printed `90 calls =
   9.0/ticker` with 20 calls on each RAG site. The real figure is 70
   calls, 7.0/ticker, 10 per RAG site: on image `2dd1aa3` the two RAG
   threads each registered the hosted usage handler, so every hosted RAG
   call was written to the ledger twice (fixed by a lock in
   `agent/tools/rag.py`; finding and corrected token figures in
   [eval-methodology.md](eval-methodology.md), "Smokes on image
   `2dd1aa3`"). Grounding counts, the gate and the estimated run cost are
   unaffected. Resource use from the step's `kubectl top` loop
   (`eval/runs/top-hosted-smoke.txt`): eval pods 3–6 millicores at steady
   state and ~600 MiB each; the one 560m reading is startup (imports and
   the embedding-model load) — the same pod reads 6m in the next sample.
   The image this ran on is superseded: re-run this step on the next image
   before any SLM run is compared with it.

   **Re-run on image `30c832b` (2026-10-03): `grounding-eval-hm527`**
   Succeeded 11/11 — 10/10 tickers, 90 claims, 1/90 = 1.11% unsupported
   (Wilson 95% CI 0.2–6.0%), judge v2, 70 agent calls = 7.0/ticker (the
   ledger double count is gone), no truncation (`eval/runs/hm527-smoke.log`,
   `eval/runs/hm527-top.txt`, findings in `eval/runs/raw/hm527-findings`).
   Superseded in turn by the next image (attempt logging).

   **Re-run on image `1f51dad` (2026-10-03): `grounding-eval-7c66k` —
   GATE FAILED.** 10/10 tickers, 101 claims, 8/101 = 7.92% unsupported
   (Wilson 95% CI 4.1–14.9%), judge v2, 0 Argo retries, 70 agent calls, no
   truncation; numeric unsupported 0/59. All 8 unsupported claims are
   qualitative phrases in MSFT's brief, which the judge listed in this
   pass (14 qualitative MSFT claims, against 1 and 0 in the two earlier
   smokes on the same retrieved context and near-identical text). It is
   recorded as a failed gate; the gate and the judge are not changed
   (`eval/runs/hosted-smoke-3.log`, `eval/runs/raw/7c66k-findings`,
   `eval/runs/grounding-eval-7c66k-attempts.json`; eval-methodology,
   "Hosted smokes on the 10-ticker set"). The new aggregate lines and the
   attempts block ran on OKE for the first time in this run. A smoke
   validates the platform; arms are compared on the extended runs, numeric
   co-primary first.
9. **[EXECUTED 2026-10-03 for `x2cx8`: in the repo are the `make
   eval-run` output (`eval/runs/hosted-smoke.log`), the top capture
   (`eval/runs/top-hosted-smoke.txt`), the workflow object
   (`eval/runs/x2cx8-workflow.json`), and — commit `8147b67` — the
   findings extraction (`eval/runs/raw/x2cx8-findings/`), the per-claim
   rows (`eval/runs/x2cx8-claims.jsonl`) and their contexts
   (`eval/runs/x2cx8-contexts/`); the full pod log was captured to
   `eval/runs/raw/x2cx8.log`, kept local like every pod log (gitignored:
   its payload duplicates the findings)]** Findings + top capture — within 7 days (the
   ttlStrategy deletes the workflow and its pods, and their logs, after
   that):
   ```bash
   # operator
   kubectl -n financial-agent logs -l workflows.argoproj.io/workflow=$WF --prefix --tail=-1 > ~/$WF.log
   ```
   ```bash
   # laptop (WSL), from the repo
   scp oke-operator:'~/<wf>.log' eval/runs/raw/<wf>.log
   scp oke-operator:'~/<wf>-top.txt' eval/runs/<wf>-top.txt
   scp oke-operator:'~/<wf>-attempts.json' eval/runs/<wf>-attempts.json   # retries + failed attempts, written by make eval-run
   python3 scripts/extract_findings.py --log eval/runs/raw/<wf>.log --out eval/runs/raw/<wf>-findings/
   python3 eval/stock_block.py eval/runs/raw/<wf>-findings
   ```
   then the per-claim rows as in "Findings capture" above. The capture
   list for every run: the pod log, the top capture, the workflow object
   (`kubectl get workflow <wf> -o json` → `eval/runs/<wf>-workflow.json`),
   **`<wf>-attempts.json`**, and for SLM runs the `~/slm-proof/<wf>*`
   files. `<wf>-attempts.json` can be rebuilt from the workflow object and
   the pod log (`python3 eval/attempts.py --workflow … --log … --json-out
   …`) while both exist.
10. **[NOT YET EXECUTED]** Teardown — operator. If the public Streamlit UI
    is up, take it down first ("Public Streamlit UI", Teardown) so the load
    balancer is released before the namespace goes:
    ```bash
    pkill -f 'kubectl -n financial-agent port-forward'
    kubectl delete -k argo/overlays/oke-provided
    kubectl delete -k k8s/overlays/oke-provided    # deletes the PVC
    kubectl get storageclass oci-bv -o jsonpath='{.reclaimPolicy}'   # Delete => the block volume and stored briefs go too
    kubectl -n financial-agent delete secret app-secrets infra-secrets ghcr-pull-secret
    kubectl delete namespace financial-agent
    kubectl delete -k argo/install                 # only if nothing else here uses Argo
    helm uninstall metrics-server -n kube-system   # only if step 6 installed it
    ```
    GHCR image versions stay until deleted from the package's settings on
    github.com.

## Public Streamlit UI (OKE provided cluster)

Requested by the tenancy owner. **Streamlit only** is public — not the
API, Argo, MCP or either llama.cpp endpoint, which stay ClusterIP (or, for
node 2's GPU endpoint, keyed behind the egress-IP rule). Overlay
`k8s/overlays/oke-provided-public-ui` (oke-provided plus the load balancer
and an nginx sidecar); scripts `scripts/public_ui_secrets.sh`,
`scripts/public_ui_up.sh`, `scripts/public_ui_render.py`.

**What is public, to whom, and how it is protected**

- One OCI flexible load balancer, 10 Mbps (inside the Always Free
  allowance of one 10 Mbps LB per tenancy; about $9 a month at list price
  if that allowance is used elsewhere), on subnet `pub_lb-tbhcuw`,
  listening on **443 only**, TLS with a self-signed certificate (Secret
  `streamlit-tls`; viewers check the SHA-256 fingerprint the operator gives
  them, then accept the browser warning).
- **Source restriction, twice, from one gitignored list**
  (`k8s/overlays/oke-provided-public-ui/allowlist.txt`):
  `loadBalancerSourceRanges` becomes ingress rules in a front-end NSG that
  the cloud controller creates (`security-rule-management-mode: NSG`; with
  `workers-tbhcuw` as the backend NSG it also adds, and on deletion
  removes, the matching worker rules); nginx repeats the allowlist on the
  `X-Forwarded-For` client address. The LB is deliberately **not** in the
  `pub_lb-tbhcuw` NSG, which admits 443 and 80 from anywhere.
- **Basic auth** in nginx: user `reviewer`, a random password, hash in the
  Secret `streamlit-basic-auth`. The password lives only in
  `~/public-ui/credentials` (0600) on the operator; read it in your own
  terminal (`ssh oke-operator cat public-ui/credentials`), never in a shared
  one, never in chat or git.
- **Spend:** every uncached brief spends Anthropic credit (hosted $0.0357
  per brief, same-image measurement); a ticker already generated in the
  last 24 hours is served from the exact-key cache for free; follow-up
  questions also spend credit, unmeasured (the ledger does not record the
  hosted ReAct agent's calls). Someone generating new tickers back to back
  would spend about $4 an hour. The app has no brief cap and none is added
  before the demo (the image stays `f3043751`). **The hard cap is the
  monthly spend limit on the Anthropic workspace**, set by the project owner
  in the Anthropic console; the allowlist and basic auth limit who can
  spend at all.

**Bring up (operator, repo root, no eval running):**

1. Allowlist: copy the gitignored file to the operator
   (`scp k8s/overlays/oke-provided-public-ui/allowlist.txt
   oke-operator:financial-agent/k8s/overlays/oke-provided-public-ui/`).
   One IPv4 CIDR per line; the renderer refuses an empty list and anything
   wider than /24.
2. `bash scripts/public_ui_secrets.sh` — creates both Secrets; prints the
   certificate fingerprint only.
3. `bash scripts/public_ui_up.sh --diff`, then `bash scripts/public_ui_up.sh`:
   refuses while an eval runs, looks up the subnet and NSG OCIDs by name,
   renders, applies, waits for the external IP. Expected diff: the
   streamlit Deployment (nginx sidecar) and Service, two new ConfigMaps.
4. Verify: `kubectl get svc -A` shows the external IP; from an allowlisted
   address `curl -sk -o /dev/null -w '%{http_code}' https://<ip>/` gives 401
   and with the credentials 200; from the operator (egress IP not on the
   list) the request times out. Load the page and generate one ticker that
   is already cached (no spend).

While the public UI is up, re-apply with `scripts/public_ui_up.sh`, not
`make oke-up` (that applies `oke-provided` and would turn the Service back
into ClusterIP, releasing the LB). Operator port-forwards to Streamlit go
to the pod's own port: `kubectl -n financial-agent port-forward
deploy/streamlit 8501`.

**Add an IP** (a reviewer's, or yours when the residential IP changes):
add one line to the allowlist on the laptop, copy it to the operator as in
step 1, run `bash scripts/public_ui_up.sh`. The OCI rule and nginx's list
are rendered from the same file, so they change together. Remove an entry
the same way.

**Status (2026-10-07): NSG mode refused; NOT LIVE, awaiting the tenancy
owner.** The first apply (NSG mode) put the nginx sidecar in place, but the
cloud controller's `CreateNetworkSecurityGroup` calls failed with 404
NotAuthorizedOrNotFound: it may not create NSGs in this VCN, so no load
balancer was created. Streamlit was put back to ClusterIP (`kubectl apply
-k k8s/overlays/oke-provided`; mcp and postgres reported "configured" for
their last-applied annotation only, no restart); OCI holds no load balancer
and the VCN still has its 7 NSGs. The two Secrets stay for the next attempt.

**Fallback: join the owner's LB NSG** (security-rule management `None`,
which makes the controller ignore `loadBalancerSourceRanges`; the LB is
attached to the existing NSG `pub_lb-tbhcuw` with
`oci.oraclecloud.com/oci-network-security-groups`). That NSG's egress to
`workers-tbhcuw` (TCP 30000–32767, 10256) and the workers' matching
ingress already exist, and the Service's node port is pinned to 30443 inside
that range. What the tenancy owner changes, on the NSG `pub_lb-tbhcuw`:

1. Delete the ingress rule: source 0.0.0.0/0, TCP, destination port 443.
2. Delete the ingress rule: source 0.0.0.0/0, TCP, destination port 80.
3. Add an ingress rule: stateful, source each allowlist CIDR (today one), TCP,
   destination port 443.

Any other public LB later placed in that NSG inherits the same allowlist.
Then, on the operator: `ATTACH_NSG_NAME=pub_lb-tbhcuw bash
scripts/public_ui_up.sh --diff`, then without `--diff`. The script refuses
while the NSG still has any non-ICMP ingress rule from 0.0.0.0/0, so the LB
never comes up open to the internet. In this mode adding an IP needs the
owner too: a new rule 3 for the new CIDR, as well as the allowlist line
(nginx's list). If the controller may not attach an NSG either, the
Service's events say so and the alternative is an IAM grant from the owner
letting the cluster manage NSGs in the VCN compartment, which restores the
NSG-mode path as designed.

**Teardown** (before the rest of the OKE teardown):

```bash
kubectl -n financial-agent delete svc streamlit      # releases the LB and the controller's NSG rules
kubectl apply -k k8s/overlays/oke-provided           # streamlit back to ClusterIP, no sidecar
kubectl -n financial-agent get configmap -o name | grep streamlit-nginx | xargs -r kubectl -n financial-agent delete   # the two nginx ConfigMaps
kubectl -n financial-agent delete secret streamlit-basic-auth streamlit-tls
shred -u ~/public-ui/credentials; rm -f ~/public-ui/tls.crt
```

Then confirm no load balancer is left:
`oci lb load-balancer list --compartment-id <the VCN's compartment> --all` is empty.

## SLM endpoints: Qwen3.6-35B-A3B on llama.cpp (CPU on OKE, GPU on node 2)

The self-served SLM behind the `slm-full-*` arms and `SLM_FULL`
(`agent/tools/slm.py`; method: [eval-methodology.md](eval-methodology.md),
"Self-served SLM arm"). One GGUF (ggml-org Q4_K_M @`baec3eb`, 20.4 GB,
sha256-verified by the init container) and one engine build (llama.cpp
b11347) on both endpoints, `k8s/llamacpp/`. **Status 2026-10-03: steps
1–3 and the CPU smoke of step 6 are executed; the GPU endpoint is loaded
but has served no eval. No doc may claim more of either endpoint than an
EXECUTED step states.**
Node 1 (`oci1`) is frozen: nothing below touches it.

Prerequisite: "OKE (provided cluster)" steps 1–8 done with the image built
and pinned from `slm-harness` — one image for the hosted smoke (its step 8),
every SLM run and the hosted baseline. A new image means every arm
re-runs on it, in this order: hosted smoke (OKE step 8), CPU smoke, GPU
smoke, then the extended runs with their same-image hosted baseline
(step 6).

1. **[EXECUTED 2026-10-03 with the temp-file method below for the
   operator — streaming into kubectl over ssh works on node 2's k3s and
   does not work on the operator]** Keys — laptop (WSL). One key per
   endpoint, never in a ConfigMap; the GPU key goes to both clusters:
   ```bash
   # laptop (WSL)
   GPU_KEY=$(openssl rand -hex 32)
   # node 2: k3s has no credential plugin, so the stream reaches kubectl
   printf %s "$GPU_KEY" | ssh oci2 'KUBECONFIG=$HOME/.kube/config kubectl -n financial-agent \
     create secret generic llamacpp-api-key --from-file=LLAMA_API_KEY=/dev/stdin'
   # operator: the oci credential plugin would consume the stream, so land
   # it in a 0600 file instead (cat reads it, not kubectl)
   printf %s "$GPU_KEY" | ssh oke-operator 'umask 077; cat > ~/slm-gpu.key'
   unset GPU_KEY
   ```
   ```bash
   # operator (interactive shell)
   kubectl -n financial-agent create secret generic slm-endpoints \
     --from-literal=SLM_CPU_API_KEY=$(openssl rand -hex 32) \
     --from-file=SLM_GPU_API_KEY=$HOME/slm-gpu.key \
     --from-literal=SLM_GPU_URL=http://<node-2-public-ip>:30880
   shred -u ~/slm-gpu.key
   kubectl -n financial-agent rollout restart deployment/api deployment/worker deployment/streamlit deployment/mcp
   ```
   (`--from-file=KEY=<path>` stores the file's bytes exactly; `printf %s`
   writes no trailing newline.) The CPU key is generated on the
   operator and lives only in `slm-endpoints`, which both the CPU server and
   the harness read. The restart lets the app pods pick up the new Secret.
2. **[EXECUTED 2026-10-03 — the endpoint reported build
   `b11347-5fc4f3c8c`, `/models/Qwen3.6-35B-A3B-Q4_K_M.gguf`, n_ctx 32768,
   4 slots through the harness's own path (provenance lines of
   `eval/runs/cpu-smoke.log`)]** CPU endpoint — operator:
   ```bash
   make oke-llamacpp
   ```
   Applies `k8s/llamacpp/overlays/oke-cpu`; the init container downloads
   and verifies the GGUF into a 50Gi `oci-bv` PVC (first rollout only),
   then llama-server loads it. 30Gi requested == limit, so it can only land
   on a ~58 GiB node (`kubectl -n financial-agent get pod -l
   app.kubernetes.io/name=llamacpp -o wide`). The target prints the
   fetch-gguf result, the server's build / `n_threads` lines (record them
   with the run), and `server_facts()` from inside the api pod — the
   harness's own path (app-config + Secret, key, `/v1/models`, `/props`).
3. **[EXECUTED 2026-10-03 — llama-server loaded the GGUF with all
   layers on the A10: nvidia-smi shows `/app/llama-server` holding 20,488
   MiB of 23,028 MiB (driver 570.124.06), args `--n-gpu-layers all
   --n-cpu-moe 0`, alias `qwen3.6-35b-a3b-q4km`; the server rejects a bad
   key (`unauthorized: Invalid API Key` in its log). It answered the 20
   requests of step 6's RAG natural-length pre-check, then the GPU smoke
   `k6zxd` and GPU extended `p9jr2` of step 6 (2026-10-05, traffic proof
   EXACT on both)]** GPU endpoint — node 2 only (`ssh oci2`):
   ```bash
   cd ~/financial-agent && git fetch && git checkout <branch> && git pull
   export KUBECONFIG=$HOME/.kube/config
   make vm-llamacpp           # scales the financial-lora vLLM to 0, deletes its Service, takes 30880
   ```
   First run downloads 20.4 GB into `/home/ubuntu/models/qwen3.6-35b-a3b-gguf`.
   The target prints the GPU layout — record it: the deployed args
   (`--n-gpu-layers`, `--n-cpu-moe`) and **llama-server's own memory on
   the GPU from `nvidia-smi --query-compute-apps`**, and it fails if no
   llama-server process holds GPU memory. llama.cpp b11347 does not log
   layer offload at default verbosity (there is no `offloaded N/N layers`
   line to grep), so process memory is the evidence: 20,488 MiB of 23,028
   MiB on 2026-10-03 is this GGUF fully on the A10.

   The first line of the server log reads `ERROR: driverInitFileInfo 531
   result=1ERROR: init 608 result=1ERROR: init 250 result=1`. It is not a
   llama.cpp message: the string `driverInitFileInfo` is in the NVIDIA
   driver's `libnvidia-sandboxutils.so.570.124.06` (on node 2:
   `grep -l driverInitFileInfo /usr/lib/x86_64-linux-gnu/libnvidia*.so*`),
   a driver library the NVIDIA container runtime mounts into the pod, and
   it prints before llama-server's first timestamped line. Why that
   library's init returns 1 here is not determined; it did not prevent
   the load (memory figure above; the server answers and enforces its key).

   If the model does not load
   (CUDA out of memory in the log), do not lower anything else: rerun with
   `make vm-llamacpp NCMOE=<n>` (smallest n that loads) — the served alias
   becomes `qwen3.6-35b-a3b-q4km-hybrid-ncmoe<n>`; patch the OKE side to
   match (`kubectl -n financial-agent patch secret slm-endpoints --type merge
   -p '{"stringData":{"SLM_GPU_MODEL_NAME":"<that alias>"}}'`), and every
   result from it is labelled **hybrid**. Then, on node 2:
   ```bash
   curl -s -o /dev/null -w '%{http_code}\n' localhost:30880/v1/models   # 401: the key is enforced
   curl -s localhost:30880/health                                          # {"status":"ok"} (public by design)
   ```
4. **[EXECUTED — ufw and security-list rules in place; evidence captured
   2026-10-05 22:32 UTC from the operator, whose egress is 129.80.187.92:
   `GET http://<node 2>:30880/v1/models` without a key → HTTP 401
   `Invalid API Key`, with `SLM_GPU_API_KEY` → HTTP 200 serving the plain
   alias `qwen3.6-35b-a3b-q4km` (no `-hybrid` suffix), n_ctx 32768
   (`eval/runs/gpu-exposure-check-2026-10-05.txt`; the key went into a
   0600 header file, never printed, then shredded). The OKE harness
   reached the endpoint for both GPU runs of step 6, traffic proof EXACT
   on `k6zxd` and `p9jr2`]** Exposure — only after step 3 shows 401 without
   the key, and only port 30880. The VCN security list is the boundary
   (k3s NodePorts route around ufw — see the single-VM network baseline);
   ufw is defense in depth:
   ```bash
   sudo ufw allow from 129.80.187.92 to any port 30880 proto tcp   # node 2
   ```
   Then the security-list rule: TCP 30880 from 129.80.187.92/32 only — never
   a range (node 2's app NodePorts 30080/30501 have no auth). The financial-
   lora vLLM (unkeyed) is at 0 replicas with no Service, so nothing unkeyed
   answers on 30880. From the OKE side:
   ```bash
   kubectl -n financial-agent exec deploy/api -- env SLM_FULL=true SLM_ENDPOINT=gpu python -c \
     "import json; from agent.tools.slm import server_facts; print(json.dumps(server_facts(), indent=1))"
   ```
5. **[EXECUTED 2026-10-05 on image `1f51dad`, all three routes (JSONs
   written 02:54:17, 02:59:15, 02:59:57 UTC):
   parse rate 1.0, correct tool 10/10, completed 10/10, errors 0 on each
   (`eval/runs/tool-use-2026-10-05/`: the three JSONs and the saved tmux
   pane `tool_use_pane.txt`; eval-methodology, "Tool-use check"). Not
   under a traffic proof]** Tool-use check, one route at a time (no LLM
   judge; ~10 hosted Sonnet calls for the hosted route). As run — the
   copy-out is `cat` through `kubectl exec`, not the `kubectl cp` this
   step listed before:
   ```bash
   cd ~/financial-agent
   for r in hosted cpu gpu; do
     kubectl -n financial-agent exec deploy/api -- python eval/tool_use_check.py --route $r --json-out /tmp/tool_use_$r.json
     kubectl -n financial-agent exec deploy/api -- cat /tmp/tool_use_$r.json > ~/tool_use_$r.json
   done
   ```
   Keep the terminal output too: the `[rag] retrieval … <s>` lines are
   only on stdout (save the pane, e.g. `tmux capture-pane -pS - >
   ~/tool_use_pane.txt`). Nothing else may use the GPU endpoint while
   its route runs, and run it before the GPU smoke, not during one.
6. **[CPU smoke EXECUTED 2026-10-03 on image `2dd1aa3` —
   `grounding-eval-slm-cpu-nb6r6` Succeeded 11/11, TRAFFIC PROOF: EXACT
   (70 calls, 92,282 prompt + 22,466 completion tokens on both sides),
   RUN-TIME CHECK: PASS (`eval/runs/cpu-smoke.log`,
   `eval/runs/slm-proof-nb6r6/`). On image `1f51dad`, EXECUTED
   2026-10-03/04: CPU smoke `wnrjr` (traffic proof EXACT), hosted extended
   `9jzmj` (workflow Error at aggregate; rebuilt offline — below) and CPU
   extended `8vpq6` (Succeeded, traffic proof EXACT, 40/40 on the first
   attempt). On the same image, EXECUTED 2026-10-05: GPU smoke `k6zxd` and
   GPU extended `p9jr2` (both Succeeded, traffic proof EXACT, 0 retries —
   below)]**
   Runs, in order, each through the traffic proof
   (operator; nothing else may use that endpoint during a run — the proof
   FAILs on foreign traffic):
   ```bash
   make slm-eval-run ENDPOINT=cpu EVAL_RUN_FILE=argo/eval-run-slm-cpu-smoke.yaml \
     PROJECT_FOR=argo/eval-run-extended-slm-cpu.yaml       # prints measured + projected run time
   make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml \
     PROJECT_FOR=argo/eval-run-extended-slm-gpu.yaml       # after the seclist rule
   make eval-run EVAL_RUN_FILE=argo/eval-run-extended.yaml                         # same-image hosted baseline (9jzmj, 2026-10-04: see below)
   make run-time-check WF=<cpu smoke wf> NEXT=argo/eval-run-extended-slm-cpu.yaml && \
     make slm-eval-run ENDPOINT=cpu EVAL_RUN_FILE=argo/eval-run-extended-slm-cpu.yaml
   make run-time-check WF=<gpu smoke wf> NEXT=argo/eval-run-extended-slm-gpu.yaml && \
     make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-extended-slm-gpu.yaml
   ```
   `slm-eval-run` snapshots `/metrics` (from the api pod, the harness's
   network path), runs `eval-run`, captures every pod's log into
   `~/slm-proof/<wf>.log`, snapshots again and prints `TRAFFIC PROOF:
   EXACT | LOWER-BOUND | FAIL`; it exits non-zero on FAIL even if the gate
   passed. With `PROJECT_FOR` it also prints the smoke's measured wall time
   per ticker (`scripts/run_time_projection.py`: each task's Argo node,
   retries included, under the run's own parallelism) and the projection
   for the extended run. `run-time-check` is the gate: it exits non-zero —
   and `&&` keeps the extended run from launching — unless the worst-case
   projection (slowest smoke ticker × ⌈40 / parallelism⌉ waves + the
   aggregate) fits the run file's `activeDeadlineSeconds`, the slowest smoke
   ticker is within 75% of `ticker-deadline-seconds`, and the projection
   plus a day of capture fits the 7-day TTL. Do not raise a deadline to make
   it pass without saying so in the run's write-up.
   Stop after each smoke and check the aggregate's `Loop`, `Trunc`,
   `Parse`, `Fmt` columns and failure kinds before going on; loops in the
   smoke mean stop and review before any penalty change. Findings: as
   "Findings capture" above, from `~/slm-proof/<wf>.log`.

   **nb6r6, as measured (2026-10-03; dated smoke, not a number of
   record).** 10/10 tickers, 73 claims, 3/73 = 4.11% unsupported (Wilson
   95% CI 1.4–11.4%), judge v2, gate passed; 70 agent calls = 7.0/ticker,
   all on `slm-cpu`. **Trunc: 13 of the 20 RAG answers hit the 512-token
   cap (highlights 9/10, risks 4/10)** against 0/20 on the hosted smoke —
   the reason the RAG cap is now one shared 2048 (`RAG_MAX_TOKENS`) and
   this smoke must be re-run. Mean pipeline time 355.9 s per ticker (26.4
   s hosted). Resource use, from the same `kubectl top` loop as OKE step 8
   (`eval/runs/top-cpu-smoke.txt`): the llamacpp pod peaked at 7,998m —
   saturating its 8-CPU limit, which is 8 vCPU = 4 physical cores with SMT
   — and 27,424 MiB of its 30Gi; the harness is near idle beside it
   (worker ≤ 43m, api ≤ 5m, eval pods single-digit millicores at steady
   state with 490–780m startup spikes). For the later concurrency sweep:
   `--threads 8` on 4 physical cores is the only setting run; thread count
   against physical cores is untested.

   **Before the next image — RAG natural-length pre-check [EXECUTED
   2026-10-03 — PROMPT CHECK: EXACT 20/20; natural completion tokens
   median 577, p95 802, max 854 (MSFT `rag:risks`); 12 of 20 above 512,
   1 above 800, 0 above 1024; `RAG_MAX_TOKENS` set to 2048
   (`eval/runs/rag-natural-length-gpu-nb6r6.{txt,json}`;
   eval-methodology, "RAG natural-length pre-check")].** A truncated
   answer only shows the SLM wanted more than 512 tokens. `scripts/rag_natural_length.py` replays nb6r6's 20 RAG
   prompts (rebuilt from its captured log by the real query-engine path;
   `eval/runs/rag-natural-length-requests-nb6r6.json`) with the `rag`
   site's sampling, thinking off, and `max_tokens` 4096, on the GPU
   endpoint — same GGUF and engine, minutes instead of the CPU's hour. On
   node 2, with nothing else using the endpoint:
   ```bash
   cd ~/financial-agent && git pull
   export KUBECONFIG=$HOME/.kube/config
   LLAMA_API_KEY=$(kubectl -n financial-agent get secret llamacpp-api-key -o jsonpath='{.data.LLAMA_API_KEY}' | base64 -d) \
     python3 scripts/rag_natural_length.py run \
       --requests eval/runs/rag-natural-length-requests-nb6r6.json \
       --url http://localhost:30880 --api-key-env LLAMA_API_KEY \
       --out ~/rag-natural-length-gpu-nb6r6.json | tee ~/rag-natural-length-gpu-nb6r6.txt
   ```
   It prints median / p95 / max completion tokens per site and `PROMPT
   CHECK: EXACT` only if every request tokenized to the prompt-token count
   nb6r6's ledger recorded for it (otherwise it lists the deltas and exits
   non-zero). The cap must clear the max with room for the 40-ticker
   tail (4× the prompts): the 2026-10-03 max of 854 is why it is 2048 and
   not 1024. Copy both files into `eval/runs/`. Re-run this before
   changing the model, the quant, the sampling or the RAG prompt.

   **CPU smoke re-run on image `30c832b` (2026-10-03):
   `grounding-eval-slm-cpu-9jddz` — gate passed, TRAFFIC PROOF: FAIL,
   explained.** 10/10 tickers, 53 claims, 1/53 = 1.89% unsupported (Wilson
   95% CI 0.3–9.9%), judge v2, Trunc 0 on every site, 70 calls in the
   final attempts. The Anthropic balance ran out mid-run: the first NVDA
   attempt finished its SLM generation, failed at the judge on the
   credit-balance 400 (the harness's FATAL guard, exit 1), and Argo retried
   it after the balance was reloaded. The server counted 10,123 prompt +
   2,943 completion tokens more than the final attempts sent — one NVDA
   brief's worth — and that image did not record a failed attempt's calls,
   so the proof cannot balance. It is recorded as **FAIL, explained: one
   retry (NVDA) after credit exhaustion**, never as a pass
   (`eval/runs/9jddz-smoke.log`, `eval/runs/slm-proof-9jddz/`,
   `eval/runs/9jddz-workflow.json`; eval-methodology, "Smokes on image
   `30c832b`"). **This run is not citable; the CPU baseline on the new
   image is the next CPU smoke (`wnrjr`, below).** Check the Anthropic balance before every
   run: an exhausted balance costs a retry on the CPU endpoint and, on
   images up to `30c832b`, the proof.

   **Hosted extended on image `1f51dad` (2026-10-04):
   `grounding-eval-extended-9jzmj` — workflow Error at aggregate
   (controller lacked configmaps create for template offload); rebuilt
   offline from all 40 pod findings dumps; gate evaluated offline; est.
   run cost not reconstructable.** All 40 eval pods completed on their
   first attempt. Rebuilt aggregate: 7/411 = 1.70% unsupported (Wilson 95%
   CI 0.8–3.5%), numeric 2/277 = 0.72%, judge v2, no truncation, gate
   passed (`eval/runs/9jzmj-aggregate.txt`,
   `eval/runs/9jzmj-results-rebuilt.json`, findings in
   `eval/runs/raw/9jzmj-findings`). The rebuild was validated first on
   `7c66k`, where it reproduces the in-cluster aggregate exactly apart
   from the estimated-cost line, so `9jzmj` is the same-image hosted
   extended baseline. The workflow object
   (`eval/runs/9jzmj-workflow.json`) confirms it independently: the
   aggregate run on the rows Argo stored prints the same report, plus est.
   run cost $4.0998. Before the next extended run, apply the controller
   Role (OKE step 5) — every 40-ticker run depends on it until the eval
   pod's output parameter is shrunk, which is deferred to after the
   comparison because it changes the image.

   **CPU smoke and CPU extended on image `1f51dad` (2026-10-03/04).**
   `grounding-eval-slm-cpu-wnrjr`: 10/10 tickers, 1/58 = 1.72%
   unsupported (Wilson 95% CI 0.3–9.1%), numeric 0/33, TRAFFIC PROOF:
   EXACT (94,520 + 24,756 tokens), 0 retries, run-time check passed.
   `grounding-eval-extended-slm-cpu-8vpq6`: Succeeded, 40/40 tickers on
   the first attempt, 0 retries, TRAFFIC PROOF: EXACT (270 calls, 342,244
   + 96,811 tokens), 9/248 = 3.63% unsupported (CI 1.9–6.8%), numeric
   3/161 = 1.86% (CI 0.6–5.3%), no Trunc/Loop/Parse/Fmt/Err, gate passed —
   a dated, citable run. Its aggregate step was the first live use of the
   controller's ConfigMap template offload on OKE (the Role of OKE step 5).
   Files: `eval/runs/cpu-extended.log`, `eval/runs/top-cpu-ext.txt`,
   `eval/runs/slm-proof-8vpq6/`, `eval/runs/slm-proof-wnrjr/`, findings in
   `eval/runs/raw/`. Comparison with hosted `9jzmj`:
   eval-methodology, "CPU SLM extended run `8vpq6`"
   (`eval/runs/9jzmj-vs-8vpq6-comparison.txt`).

   **GPU smoke and GPU extended on image `1f51dad` (2026-10-05).**
   `grounding-eval-slm-gpu-k6zxd`: 10/10 tickers, 3/63 = 4.76% unsupported
   (Wilson 95% CI 1.6–13.1%, all three on AAPL, qualitative), numeric
   0/32, gate passed, TRAFFIC PROOF: EXACT (70 calls, 95,185 + 25,317
   tokens), 0 retries, mean pipeline 30.82 s per ticker; RUN-TIME CHECK:
   PASS (projected 40 tickers in 20 waves of 2: mean 37 min, worst 48 min).
   `grounding-eval-extended-slm-gpu-p9jr2`: Succeeded 03:13:00–03:48:12
   UTC, 40/40 tickers on the first attempt, 0 retries, TRAFFIC PROOF: EXACT
   (270 calls, 350,290 + 98,232 tokens), 6/245 = 2.45% unsupported (CI
   1.1–5.2%), numeric 3/155 = 1.94% (CI 0.7–5.5%), no
   Trunc/Loop/Parse/Fmt/Retry/Err on any call, stock block empty 0/40,
   gate passed — a dated, citable run, served all-GPU (alias without
   `-hybrid`). An nvidia-smi sampler ran on node 2 every 5 s from 02:51:49
   to 03:50:49 UTC across the tool-use check and both runs
   (`eval/runs/gpu-nvsmi-p9jr2.csv`, sliced per run by
   `scripts/nvsmi_summary.py`); there is no `kubectl top` capture for the
   GPU runs (the endpoint is not on OKE). Files: `eval/runs/gpu-smoke.log`,
   `eval/runs/gpu-extended.log`, `eval/runs/slm-proof-k6zxd/`,
   `eval/runs/slm-proof-p9jr2/`, the two `*-attempts.json`, findings in
   `eval/runs/raw/`. Three-way comparison with hosted `9jzmj` and CPU
   `8vpq6`: eval-methodology, "GPU SLM extended run `p9jr2`"
   (`eval/runs/9jzmj-8vpq6-p9jr2-comparison.txt`).

   **From the next image: retries are part of the report.** `make
   eval-run` prints, under the aggregate's output, an attempts block from
   the workflow object and every pod's log (`eval/attempts.py`): Argo
   retries, the tickers, and each failed attempt's cause, LLM calls and
   Trunc/Parse/Fmt/Err counts, labelled as from failed attempts. The
   same report is written to `~/<workflow>-attempts.json` (`ATTEMPTS_DIR`)
   — capture it with the run (OKE step 9). The aggregate pod itself only
   names the retried tickers: it has no RBAC to read other pods' logs, by
   decision. `slm-eval-run` saves the workflow object beside the pod log
   and the proof counts the failed attempts' tokens (`--workflow`). A run
   is citable only on **EXACT**, or on **LOWER-BOUND with every excess
   token attributed to calls the harness itself logged as failed**; a
   failed attempt without a complete call record is FAIL. The aggregate
   also prints claims per ticker, numeric claims per ticker and the
   numeric-claim unsupported rate next to the all-claims rate — read them
   together (eval-methodology, "Dated finding: claim density"); for a
   two-run comparison, `python3 eval/multi_arm_stats.py --run … --run …`
   prints the numeric comparison and the density table.
7. **[NOT YET EXECUTED]** Live app on the SLM (optional, for the demo):
   `make oke-slm-app ON=true ENDPOINT=cpu` (cache keys become
   `research:slm-cpu:<T>`, so no hosted brief is served as an SLM one);
   `make oke-slm-app ON=false` to return.
8. **[NOT YET EXECUTED]** Restore node 2's financial-lora vLLM (node 2):
   `make vm-llamacpp-down && make vm-vllm` — but first remove the ufw rule
   and the security-list rule: the vLLM endpoint has no key.

## Demo live run (November 2026): GPU smoke from the OKE harness

**[NOT YET EXECUTED]** The live part of the demo (docs/demo.md, "The live
run"): one GPU smoke, `argo/eval-run-slm-gpu-smoke.yaml`, from the OKE
harness against node 2's llama.cpp endpoint, with the traffic proof. It is
a new dated run on image `1f51dad`; capture it like `k6zxd`. Nothing here
changes a manifest.

**Network facts this section depends on.** The VCN security list is the
boundary for node 2's NodePorts: k3s NodePorts route around ufw, which is
defense in depth only (SLM step 4). The security-list rule admitting TCP
30880 from 129.80.187.92/32 stays in place until after the demo. The
financial-lora vLLM, when `make vm-vllm` restores it, also answers on
30880 **without a key**.

**vLLM stays scaled to 0 on node 2 until after the demo; llama.cpp keeps
running there.** Because k3s NodePorts bypass ufw, the security-list
rule stays open to the OKE egress IP until the demo, and vLLM on 30880
is unkeyed, serving vLLM on node 2 while the rule stands would expose an
unkeyed model to that IP. The default path never swaps; the one way vLLM
comes back before the demo is the contingency below, which closes the
rule first.

### Preflight — the day before, and again 30 minutes before

Run every check from the shell named; stop at the first failure and take
its branch below. Nothing in the preflight sends tokens to the GPU
endpoint, and all of it finishes before the run's first traffic-proof
snapshot.

1. **Anthropic balance** (console, billing page): the judge is Sonnet on
   every arm; the smoke's harness estimate was $0.9463 (`k6zxd`). Keep
   enough for the rehearsal, the demo run and a re-run. A low balance
   fails the run loudly (`eval/runtime_guards.py`), mid-run.
2. **OKE nodes and pods Ready** (operator):
   ```bash
   kubectl get nodes                                   # 4 Ready
   kubectl -n financial-agent get pods                 # api, worker, streamlit, mcp, redis, postgres, llamacpp Running
   kubectl -n argo get pods                            # workflow-controller, argo-server Running
   ```
3. **CronWorkflow still suspended** (operator):
   ```bash
   kubectl -n financial-agent get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.suspend}{"\n"}'   # true
   ```
4. **Image pin** (operator, repo at the pushed `slm-harness`):
   ```bash
   python3 scripts/pin_oke_image.py --overlay oke-provided --check     # pinned app image tag: f3043751…
   kubectl -n financial-agent get deploy api -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'   # same tag
   ```
5. **Node 2 endpoint and GPU** (node 2, `ssh oci2`):
   ```bash
   curl -s localhost:30880/health                                     # {"status":"ok"}
   curl -s -o /dev/null -w '%{http_code}\n' localhost:30880/v1/models # 401: key enforced
   nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv   # llama-server ~20,488 MiB
   ```
   And vLLM is at 0 (`kubectl -n financial-agent get deploy vllm` shows
   `0/0`). If vLLM is serving on 30880, that is the unkeyed exposure this
   section rules out: run `make vm-llamacpp` at once (it scales vLLM to 0
   and takes the port back), then tell the tenancy owner.
6. **30880 from OKE** (operator, whose egress is the cluster's,
   129.80.187.92): `scripts/gpu_exposure_check.sh` (how to run it is in
   its header) prints HTTP 401 without the key and HTTP 200 with it,
   serving the plain alias `qwen3.6-35b-a3b-q4km`, as in
   `eval/runs/gpu-exposure-check-2026-10-05.txt`. Then the harness's own
   path:
   ```bash
   kubectl -n financial-agent exec deploy/api -- env SLM_FULL=true SLM_ENDPOINT=gpu python -c \
     "import json; from agent.tools.slm import server_facts; print(json.dumps(server_facts(), indent=1))"
   ```
7. **Yahoo from the cluster** (operator; one request — yfinance has
   answered 429 from this egress IP):
   ```bash
   kubectl -n financial-agent exec deploy/api -- python -c \
     "import yfinance as yf; print(yf.Ticker('AAPL').fast_info['lastPrice'])"   # a price, not an error
   ```
8. **Screen sharing: nothing shown prints a key.** What the demo shows is
   safe: `scripts/gpu_exposure_check.sh` reads the key into a 0600 header
   file and prints only the endpoint's responses; `server_facts()` returns
   no key; `make slm-eval-run` writes its snapshots to files and its
   recipe is silent; llama-server takes its key from an environment
   variable, not an argument, so `ps` does not show it. On a shared screen
   never run `kubectl get secret … -o yaml|json`, `kubectl exec … env`,
   `printenv`/`env` in a pod or on node 2, `cat /proc/<pid>/environ`, or
   `cat .env` on the laptop; `kubectl describe secret` shows sizes only.
   The run's output shows node 2's public IP and the operator's private
   addresses — not credentials (30880 admits only the OKE egress IP).
   Pre-open the terminals to be shared (operator, node 2, laptop), clear
   their scrollback (`clear && printf '\e[3J'`, or tmux `clear-history`),
   and run the preflight in other terminals.
9. **Port-forwards and tunnels up** (operator, then laptop):
   ```bash
   # operator
   nohup kubectl -n argo port-forward svc/argo-server 2746:2746 >/tmp/pf-argo.log 2>&1 &
   nohup kubectl -n financial-agent port-forward svc/streamlit 8501:8501 >/tmp/pf-streamlit.log 2>&1 &
   # laptop (WSL)
   ssh -N -L 32746:localhost:2746 -L 32501:localhost:8501 oke-operator
   # Argo UI: https://localhost:32746 (check that it loads and lists the
   # workflows; argo-server's auth mode decides whether it asks for a token)
   # Streamlit: http://localhost:32501
   ```

**The day before only: a full rehearsal.** Run the launch below once,
end to end, and capture it. It measures the timings this section leaves
open (the swap's model load, the smoke's wall time on the day) and
proves the path. A rehearsal is a dated smoke like any other; it is not
an arm comparison.

### Launch (operator)

```bash
cd ~/financial-agent
make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml
```

The target snapshots the endpoint's counters from the api pod, submits
and follows the workflow (`[hh:mm:ss] phase=Running progress=n/11`),
captures every pod's log into `~/slm-proof/<wf>.log`, snapshots again and
prints the aggregate, the attempts block and `TRAFFIC PROOF: EXACT |
LOWER-BOUND | FAIL`. `k6zxd` took 9 min 40 s. Nothing else may call the
GPU endpoint until it finishes: other traffic fails the proof.

On screen while it runs: the operator pane with the target's progress;
the Argo UI graph (ten eval pods, two at a time, then the aggregate); a
node 2 pane with `watch -n 2 nvidia-smi` (the A10's utilization moving
with the calls, ~20.5 GB held). At the end: the aggregate table, the gate
line, `stock block empty`, the LLM-call table (Trunc, Loop, Parse, Fmt,
Err all 0), the attempts block (0 retries) and `TRAFFIC PROOF: EXACT`.

### Failure branches

Every branch ends at the recorded runs: `eval/runs/gpu-smoke.log`
(`k6zxd`, the smoke) and `eval/runs/gpu-extended.log` (`p9jr2`, the A10
run of record), open on the laptop before the demo starts. Say what
failed; do not debug live beyond the first check named.

- **Node 2 down** (`ssh oci2` fails, or `/health` does not answer on the
  node): a stopped VM is restarted by the tenancy owner in the console,
  and the model's load time is not one to wait out live. Fallback.
- **The endpoint answers 401 to the harness** (`server_facts` or the run's
  first calls): the key in OKE's `slm-endpoints` Secret no longer matches
  node 2's `llamacpp-api-key`. Re-keying is SLM step 1, not a live step.
  Fallback.
- **000 — no HTTP answer from the operator.** One check, on node 2:
  `curl -s localhost:30880/health`. If it answers there, the path from OKE
  is blocked (security-list rule) — the tenancy owner's console. If it
  does not, the pod is down or restarting: `kubectl -n financial-agent get
  pods -l app.kubernetes.io/name=llamacpp`; if it is not Running within a
  minute or two, fallback.
- **Yahoo 429** (preflight 7 errors, or the aggregate's `stock block
  empty` is above 0/10): the run still completes, but those briefs had no
  stock data, so their figures say nothing about the model. Show the
  count, do not quote the run's rate, do not retry (the 429 is on the
  egress IP). Fallback for the numbers.
- **The smoke fails its gate** (above 5% unsupported, or under 30 claims):
  a smoke's rate moves with how many qualitative claims the judge lists for
  one ticker — `7c66k` failed at 7.92% on MSFT alone, `k6zxd` passed at
  4.76% with all three on AAPL. Show which ticker holds the unsupported
  claims and that the numeric column is 0; arms are compared on the
  40-ticker runs, so go to `p9jr2`. Do not re-run to get a pass.
- **The balance runs out mid-run** (the run fails on the credit-balance
  error; retries appear in the attempts block): fallback; the proof may
  not be citable.
- **TRAFFIC PROOF: FAIL or LOWER-BOUND**: say what the proof caught
  (traffic the harness did not log, or a failed attempt) — that is the
  proof working. The run is not citable. Fallback.

### Contingency only: vLLM needed on node 2 before the demo

Not part of the default path. If vLLM must serve on node 2 before the
demo, in this order, all of it finished before the rehearsal:

1. **Close 30880 first.** Ask the tenancy owner to remove the
   security-list rule (TCP 30880 from 129.80.187.92/32); on node 2,
   `sudo ufw delete allow from 129.80.187.92 to any port 30880 proto tcp`;
   from the operator, `curl -s -m 10 -o /dev/null -w '%{http_code}\n'
   http://<node 2>:30880/health` prints `000`.
2. **Then vLLM** (node 2): `make vm-llamacpp-down && make vm-vllm`
   (rollout waits up to 15 minutes, then polls the model for up to 2).
3. **Swap back to llama.cpp** (node 2):
   ```bash
   cd ~/financial-agent && git pull
   export KUBECONFIG=$HOME/.kube/config
   make vm-llamacpp            # scales vLLM to 0, deletes its Service, takes 30880; the GGUF is already on disk
   curl -s localhost:30880/health && curl -s -o /dev/null -w '%{http_code}\n' localhost:30880/v1/models   # ok, 401
   ```
4. **Re-open 30880 for the OKE egress IP only:** `sudo ufw allow from
   129.80.187.92 to any port 30880 proto tcp` on node 2, and ask the
   tenancy owner to re-add the security-list rule (129.80.187.92/32,
   never a range). Then preflight 5 and 6.

Time: the Kubernetes steps take a minute or two each. Loading the 20.4 GB
GGUF into the A10 is not recorded — `make vm-llamacpp` waits up to an
hour (`rollout status --timeout=3600s`), then polls the model for up to
5 minutes; measure it if this path is used and write it here. The two
security-list changes depend on the tenancy owner. If `make vm-llamacpp`
fails on GPU memory, something else holds the A10: check `nvidia-smi`
first; do not lower layers or switch to a hybrid layout for the demo (a
hybrid run is labelled hybrid, not GPU).

### Teardown, after the demo

In this order — vLLM answers on 30880 without a key, and ufw does not
guard k3s NodePorts:

1. **Capture the live run** (and the rehearsal) within the 7-day TTL:
   OKE step 9's capture list, from `~/slm-proof/`.
2. **Public Streamlit UI down**, if it is up ("Public Streamlit UI",
   Teardown): the load balancer, its NSG rules, the Secrets and the
   operator's credentials file.
3. **Port-forwards and tunnels down** (operator):
   `pkill -f 'kubectl -n argo port-forward'; pkill -f 'kubectl -n
   financial-agent port-forward'`; close the laptop's `ssh -N`.
4. **Close ufw 30880** (node 2):
   `sudo ufw delete allow from 129.80.187.92 to any port 30880 proto tcp`.
5. **Ask the tenancy owner to remove the security-list rule** TCP 30880
   from 129.80.187.92/32. Then confirm from the operator:
   `curl -s -m 10 -o /dev/null -w '%{http_code}\n' http://<node 2>:30880/health`
   prints `000`.
6. **Only then, if wanted, restore vLLM** (node 2):
   `make vm-llamacpp-down && make vm-vllm`.

The CronWorkflow stays suspended throughout. The CPU endpoint on OKE is
not part of the live run and is left as it is.

## Rerun on the stock-data-fix image (October 2026)

The image carries only the stock-data fix plus currency-labelling prompt
rule (commits `19582b9`, `f304375`): `financial_currency` and
`profit_margin_pct` in the stock dict, the currency rule in the section
context and the synthesis prompt for a filer reporting in another
currency, and the numeric check's `currency_label` finding. Every arm
re-runs on it at 40 tickers, same protocol as the `1f51dad` three-way.
Hard cutoff 2026-10-25: if the reruns and the labelling are not done by
then, stop and keep the current numbers of record.

1. **[EXECUTED 2026-10-06]** Build, pin, deploy. Node 2 built and pushed
   `ghcr.io/schen9999/financial-agent-app:f3043751eb51083b8c674d23ad4ff1da91cbdeac`
   (digest `sha256:34896c1b…`; the code layer rebuilt, dependency layers
   from cache) from a clean tree at `f304375`; the pin is commit
   `88c1811`. On the operator, `make oke-up` rolled api, worker,
   streamlit and mcp onto it, then `kubectl apply -k
   argo/overlays/oke-provided` moved the grounding-eval WorkflowTemplate
   to it — `make oke-up` applies the app overlay only, so the template
   needs its own apply after every pin (a `kubectl diff` first showed the
   two image lines as the only change). The nightly CronWorkflow stayed
   suspended.
2. **[EXECUTED 2026-10-06T01:33:44Z]** Reporting-currency preflight, from
   the api pod (`scripts/financial_currency_preflight.py`, 40 tickers, no
   request errors): `eval/runs/financial-currency-2026-10-06.json`. TM
   JPY, TSM TWD, NVO DKK, BABA CNY, SAP EUR; the other 35 report in USD,
   except VERV — **yfinance returned no quote for VERV as of 2026-10-06**
   (`quoteType` NONE, no name, price, market cap or revenue). RDFN's
   listing currency is missing (the stock tool defaults it to USD); it
   reports in USD.

**Declared before any run (2026-10-06), for the before/after against the
`1f51dad` three-way:**

- The comparison uses the tickers both sides have: VERV is excluded (no
  quote as of 2026-10-06; it stays in the runs, all 40 tickers, and the new
  runs' own rates are over 40).
- Any ticker whose stock block is empty in a new run (`stock block empty`
  in the aggregate, `eval/stock_block.py`) is excluded from the
  before/after the same way, and listed.
- The currency before/after uses the same check on both sides: the old
  runs with `numeric_backtest.py --financial-currency` and this preflight
  file, the new runs as they are.
- Success criterion: currency and profit-margin TRUE_ERRORs at 0 in every
  arm, and `currency_label` flags only where a brief writes a non-USD
  amount in dollars. Grounding rates are compared as a dated before/after
  attributable to the fix and the prompt rule; run-to-run variance means
  no rate difference is claimed beyond "not detected".

   **Hosted smoke `grounding-eval-5jvhh` (2026-10-06, EXECUTED):**
   Succeeded 11/11, 0 retries, 0 failed attempts; 0/76 unsupported
   (Wilson 95% CI 0.0–4.8%), numeric 0/60, gate passed; stock block empty
   0/10; 70 agent calls, no Trunc/Loop/Parse/Fmt/Err; 26.8 s per ticker;
   est. $1.0441. The stock dicts carry `financial_currency` and
   `profit_margin_pct`. The 10-ticker set has no foreign filer and no
   margin above 100%, so this smoke checks the platform, not the fix.
   RAG faithfulness (rf-v1, unvalidated, never part of the grounding rate)
   20/250 = 8.00% against 1.56–2.17% in the earlier hosted smokes: 13 of
   the 20 are AMZN highlights (7/9) and MSFT highlights (6/8), both the
   limitation-(2) refusal ("the context only contains excerpts from the
   Risk Factors section"), near-identical to `hm527`'s and served from the
   RAG answer cache; rf-v1 listed the refusal's "sections I would need"
   bullets as claims this time (in `hm527` the AMZN refusal gave none).
   Judge listing variance, not a pipeline change. Files:
   `eval/runs/hosted-smoke-f304375.log`, `eval/runs/5jvhh-workflow.json`,
   `eval/runs/grounding-eval-5jvhh-attempts.json`,
   `eval/runs/raw/5jvhh-findings/`, `eval/runs/5jvhh-claims.jsonl`.

   **CPU smoke `grounding-eval-slm-cpu-xnwjm` (2026-10-06, EXECUTED):**
   Succeeded 11/11, 0 retries, 0 failed attempts, TRAFFIC PROOF: EXACT (70
   calls, 94,597 + 24,567 tokens); 3/60 = 5.00% unsupported (CI 1.7–13.7%),
   gate passed at its threshold, all three META hedged Outlook watch-items
   (limitation 1; META listed 10 claims here and in `wnrjr`, which had 0
   unsupported); numeric 0/36; stock block empty 0/10; 368.2 s per ticker;
   RUN-TIME CHECK: PASS (extended projected 2 h 28 min mean, 2 h 51 min
   worst); llama.cpp median 7,864m, peak 7,997m of 8,000m
   (`eval/runs/top-cpu-smoke-f304375.txt`); RAG faithfulness 4/428
   (unvalidated); est. $0.9175. Files: `eval/runs/cpu-smoke-f304375.log`,
   `eval/runs/slm-proof-xnwjm/`, findings and claims.

   **GPU smoke `grounding-eval-slm-gpu-m7qvv` (2026-10-06, EXECUTED, GATE
   FAILED):** 10/10 tickers, 0 retries, 0 failed attempts, TRAFFIC PROOF:
   EXACT (70 calls, 94,775 + 24,830 tokens); 4/60 = 6.67% unsupported (CI
   2.6–15.9%) against the 5% gate; numeric 0/30; stock block empty 0/10;
   36.4 s per ticker; RUN-TIME CHECK: PASS (extended projected 38 min mean,
   47 min worst); RAG faithfulness 3/402 (unvalidated); est. $0.9023. All
   four unsupported claims are hedged Outlook watch-items (limitation 1):
   NVDA "trend of services margins", "sustained demand elasticity",
   "market saturation"; MSFT "trajectory of services margins …". The judge
   listed 5 qualitative claims for NVDA here against 0 in `k6zxd`. "services
   margins" echoes the synthesis prompt's own example ("watch
   services-margin trend"), as did `p9jr2`'s AFRM claim (known limitation
   8, eval-methodology). Recorded as smoke-level judge variance on
   qualitative watch-items (limitation 1), not a platform failure — the
   precedent is hosted smoke `7c66k` (gate failed on MSFT watch-items),
   after which the extended run `9jzmj` went ahead. The run plan stopped
   the chain at the gate; the adjudicator then started it (2026-10-06
   04:49:54Z, tmux `rerun` on the operator,
   `~/rerun-chain.sh grounding-eval-slm-gpu-m7qvv
   grounding-eval-slm-cpu-xnwjm`), with the same stop rules. nvidia-smi on node 2 every 5 s,
   04:34:46 onward: `eval/runs/gpu-nvsmi-m7qvv.csv`. Files:
   `eval/runs/gpu-smoke-f304375.log`, `eval/runs/slm-proof-m7qvv/`,
   findings and claims.

   **Extended chain (2026-10-06, EXECUTED; stopped at the CPU run):**
   - Hosted `grounding-eval-extended-4hsn2`: Succeeded, 0 retries;
     15/399 = 3.76% unsupported (CI 2.3–6.1%), numeric 3/270; stock
     block empty 0/40; gate passed; 26.7 s per ticker; est. $4.1162.
   - GPU `grounding-eval-extended-slm-gpu-nstp9`: Succeeded, 0 retries,
     TRAFFIC PROOF: EXACT; 10/267 = 3.75% (CI 2.0–6.8%), numeric 4/166;
     stock block empty 0/40; gate passed; 34.6 s per ticker; est.
     $3.3433. nvidia-smi on node 2 every 5 s, 04:49:42–08:24:
     `eval/runs/gpu-nvsmi-ext-f304375.csv`.
   - CPU `grounding-eval-extended-slm-cpu-5bdz5`: every eval pod on its
     first attempt, 0 retries, but **GATE FAILED** (19/265 = 7.17%, CI
     4.6–10.9%; numeric 2/162) and **TRAFFIC PROOF: FAIL** — the server
     counted 1 prompt token more than the harness logged (346,636 against
     346,635; 0 completion tokens apart), with no failed calls. Cause not
     determined. Under the proof rule the run is **not citable**.
     Investigated offline (`eval/runs/slm-proof-5bdz5/INVESTIGATION.md`,
     with the endpoint's own log): 270 server tasks match the 270 harness
     calls pair for pair and sum to the harness's tokens exactly; no
     outside traffic; the +1 is a counter movement outside any logged
     request. Settling it needs per-request `timings` in the ledger, a
     post-demo change. The chain
     stopped there (`~/rerun-chain.log`). `kubectl top` during it:
     `eval/runs/top-cpu-ext-f304375.txt`.

   **LangSmith tracing (2026-10-06).** The LangSmith monthly unique-trace
   quota was exhausted on 2026-10-06: trace uploads from the local re-judge
   (`eval/rejudge_runs.py`) were rejected with HTTP 429 ("Monthly unique
   traces usage limit exceeded"). Uploads are best-effort and the judge
   calls themselves were unaffected. Tracing is now off for local eval
   scripts (`LANGCHAIN_TRACING_V2=false` in the laptop's `.env`, which is
   not committed). On the OKE cluster it is still on: `app-secrets`, made
   from that `.env` before the change, carries `LANGCHAIN_TRACING_V2=true`
   and a `LANGCHAIN_API_KEY`; the app pods and the eval pods (`envFrom:
   app-secrets`) read it, and the api pod's `tracing_enabled()` returns
   True. Left unchanged while the CPU re-run `4kkgm` runs; to turn it off
   there, re-create `app-secrets` from the updated `.env` (OKE step 3) and
   restart the app Deployments.

   **CPU extended re-run — rules recorded 2026-10-06, before it starts:**
   - It replaces `5bdz5` only because `5bdz5`'s traffic proof FAILed.
     Its grounding rate is the CPU arm's result whatever the gate says.
   - If its traffic proof is not EXACT, the CPU arm's after side is not
     citable, the before/after covers hosted and GPU only, and there is no
     third attempt.
   - Same protocol: `make run-time-check` against the CPU smoke
     (`grounding-eval-slm-cpu-xnwjm`), then `make slm-eval-run
     ENDPOINT=cpu`, `kubectl top` every 15 s throughout.

   **CPU extended re-run result (2026-10-06):**
   `grounding-eval-extended-slm-cpu-4kkgm`, 17:52–20:19Z. Run-time check
   PASS (projected worst 2h51m). Every eval pod on its first attempt, 0
   retries, no failed attempts; stock block empty 0/40. **GATE FAILED**
   (15/282 = 5.32%, CI 3.2–8.6%; numeric 2/166) and **TRAFFIC PROOF:
   FAIL** — the server counted 4 prompt tokens FEWER than the harness
   logged (353,897 against 353,901; completion 99,078 on both; 270 calls,
   0 errored). `5bdz5` was off by +1 in the other direction. Investigated
   offline (`eval/runs/slm-proof-4kkgm/INVESTIGATION.md`,
   `scripts/llamacpp_window_match.py`): all 270 server tasks match the 270
   ledger calls pair for pair and sum to the harness's tokens exactly; only
   the `/metrics` prompt counter is off (4 below the server's own per-task
   log). Cause not determined; both unexplained drifts are on the CPU
   endpoint, every GPU proof is EXACT. No rule change.
   Under the rules above: **not citable**; the CPU arm's after side is not
   citable, the before/after covers hosted and GPU only, and there is no
   third attempt. Captured: `eval/runs/slm-proof-4kkgm/` (counter
   snapshots, workflow object, pod log, `llamacpp-server-window.log`),
   `eval/runs/raw/4kkgm-findings/`, `eval/runs/4kkgm-claims.jsonl` and
   `-contexts/`, the attempts record, `eval/runs/cpu-rerun-f304375.log`
   (make output) and `eval/runs/top-cpu-rerun-f304375.txt`.

3. **[STOPPED — CPU extended failed its gate and its traffic proof]** Runs, in order: hosted smoke, CPU smoke, GPU
   smoke, hosted extended, CPU extended, GPU extended — each SLM run
   through `make slm-eval-run` (traffic proof), the extended SLM runs
   behind `make run-time-check`; `kubectl top` during the CPU runs, the
   nvidia-smi sampler on node 2 during the GPU runs; an Anthropic balance
   check first.

## OKE (OCI) — Phase 2

All OCI infrastructure is authored in `terraform/oci/` (fmt + validate
pass). **No step below has been executed — there are no OCI credentials
yet.** Execute in order once access lands.

**Optional free-trial dry run — NOT the demo tenancy.** Before the demo
tenancy's credentials arrive, steps 1–7 can be rehearsed against an OCI
free-trial tenancy with `enable_gpu_pool = false` in terraform.tfvars
(trials carry no GPU quota; everything except the A10 pool applies, so
vLLM steps 8–9 are excluded). If trial service limits bite on the app
pool, trim `app_pool_size` / `app_node_ocpus` in tfvars. Nothing from a
trial run counts as a demo-tenancy result: no numbers, no "deployed on
OKE" claims — tear it down (`terraform destroy`) when done and re-run
everything for real on the demo tenancy.

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
