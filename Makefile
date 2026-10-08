# Local Kubernetes workflow (single-node kind). Run inside a Linux environment
# with docker + kind + kubectl (on this repo's dev machine: the `financial-agent`
# WSL2 distro). See k8s/README.md for setup and layout.
SHELL := /bin/bash

CLUSTER   ?= financial-agent
NAMESPACE ?= financial-agent
IMAGE     ?= financial-agent-app:local
ENV_FILE  ?= .env

# docker build runs under BuildKit (DOCKER_BUILDKIT=1 inline on both build
# lines): Dockerfile.k8s relies on its per-Dockerfile ignore file
# (Dockerfile.k8s.dockerignore), a BuildKit-only feature — the legacy builder
# applies the ECS .dockerignore and drops app.py. Needs the buildx plugin
# (Docker CE ships it; scripts/vm_bootstrap.sh installs it on the VM).

.PHONY: cluster-up deploy smoke-test cluster-down status logs \
        argo-install argo-deploy eval-run cost-report \
        vm-images vm-up vm-eval vm-vllm oke-images oke-up \
        vm-llamacpp vm-llamacpp-down oke-llamacpp oke-llamacpp-down oke-slm-app slm-eval-run \
        run-time-check

cluster-up: ## Create the single-node kind cluster (or restart its stopped node)
	@if kind get clusters 2>/dev/null | grep -qx $(CLUSTER); then \
		echo "cluster exists — ensuring node container is running"; \
		docker start $(CLUSTER)-control-plane >/dev/null 2>&1 || true; \
	else \
		kind create cluster --config k8s/kind-config.yaml; \
	fi
	@# Right after a node restart the apiserver answers before RBAC is ready — retry.
	@for i in $$(seq 1 30); do \
		kubectl wait --for=condition=Ready node/$(CLUSTER)-control-plane --timeout=10s >/dev/null 2>&1 && break; \
		echo "waiting for node to be Ready ($$i/30)..."; sleep 5; \
	done
	kubectl wait --for=condition=Ready node/$(CLUSTER)-control-plane --timeout=60s
	kubectl cluster-info --context kind-$(CLUSTER)

deploy: ## Build the app image, load it into kind, apply manifests, wait for rollout
	@test -f $(ENV_FILE) || { echo "ERROR: $(ENV_FILE) not found — copy .env.example and fill in keys"; exit 1; }
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.k8s -t $(IMAGE) .
	kind load docker-image $(IMAGE) --name $(CLUSTER)
	kubectl apply -f k8s/base/00-namespace.yaml
	@# infra-secrets: random Postgres password, generated once, lives only in-cluster
	@kubectl -n $(NAMESPACE) get secret infra-secrets >/dev/null 2>&1 || { \
		PGPASS=$$(openssl rand -hex 16); \
		kubectl -n $(NAMESPACE) create secret generic infra-secrets \
			--from-literal=POSTGRES_PASSWORD=$$PGPASS \
			--from-literal=DATABASE_URL=postgresql://agent:$$PGPASS@postgres:5432/financial_agent; \
		echo "created infra-secrets (random Postgres password)"; }
	@# app-secrets: developer API keys from the local .env (never committed)
	kubectl -n $(NAMESPACE) create secret generic app-secrets \
		--from-env-file=$(ENV_FILE) --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -k k8s/overlays/kind
	@# restart app deployments so an updated image/secrets take effect on redeploy
	kubectl -n $(NAMESPACE) rollout restart deployment/api deployment/worker deployment/streamlit deployment/mcp 2>/dev/null || true
	kubectl -n $(NAMESPACE) rollout status deployment/redis    --timeout=180s
	kubectl -n $(NAMESPACE) rollout status deployment/postgres --timeout=300s
	kubectl -n $(NAMESPACE) rollout status deployment/api      --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/worker   --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/streamlit --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/mcp      --timeout=600s
	@echo "Deployed. API: http://localhost:30080  Streamlit: http://localhost:30501  MCP: http://localhost:30800/mcp"

smoke-test: ## End-to-end: sync brief, async Celery brief, exact-key cache hit + miss, MCP
	bash scripts/k8s_smoke_test.sh

cluster-down: ## Delete the kind cluster
	kind delete cluster --name $(CLUSTER)

status: ## Pods, services, and recent events
	kubectl -n $(NAMESPACE) get pods,svc
	kubectl -n $(NAMESPACE) get events --sort-by=.lastTimestamp | tail -15

logs: ## Tail logs: make logs C=api|worker|streamlit|mcp|redis|postgres
	kubectl -n $(NAMESPACE) logs deployment/$(C) --tail=100 -f

# ── Argo Workflows (batch/eval — request-time async stays on Celery) ─────────

# Argo version is pinned in argo/install/kustomization.yaml (single source of truth).
argo-install: ## Install Argo Workflows (controller + server), pinned via argo/install
	kubectl apply -k argo/install
	kubectl -n argo rollout status deploy/workflow-controller --timeout=300s
	kubectl -n argo rollout status deploy/argo-server --timeout=300s

# Which argo overlay to apply (kind locally; vm-* targets pass k3s).
ARGO_OVERLAY ?= kind

argo-deploy: ## Apply eval workflow RBAC, WorkflowTemplate, and nightly CronWorkflow
	@# the OKE overlay pins a GHCR build: refuse the UNPINNED placeholder
	@if [ "$(ARGO_OVERLAY)" = "$(OKE_OVERLAY)" ]; then python3 scripts/pin_oke_image.py --overlay $(OKE_OVERLAY) --check; fi
	kubectl apply -k argo/overlays/$(ARGO_OVERLAY)
	@SUSPEND=$$(kubectl -n $(NAMESPACE) get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.suspend}'); \
	echo "Nightly eval: $$(kubectl -n $(NAMESPACE) get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.schedule} {.spec.timezone}') suspend=$${SUSPEND:-<unset>}"

# Override to submit a different one-shot Workflow, e.g. the local-model arm:
#   make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml
EVAL_RUN_FILE ?= argo/eval-run.yaml
# Poll pacing: ceiling = activeDeadlineSeconds + margin. Overridable so the
# guard paths can be exercised in seconds with a fake kubectl.
EVAL_POLL_MARGIN ?= 600
# Where eval-run leaves <workflow>-attempts.json (retries and failed attempts,
# eval/attempts.py) for the capture steps to pick up.
ATTEMPTS_DIR ?= $(HOME)
EVAL_POLL_INTERVAL ?= 20

eval-run: ## Submit the grounding eval workflow now and follow it to completion
	@WF=$$(kubectl -n $(NAMESPACE) create -f $(EVAL_RUN_FILE) -o name | sed 's|.*/||'); \
	if [ -z "$$WF" ]; then \
		echo "ERROR: submit returned no workflow name — kubectl create failed (auth, context, or file?). Aborting."; \
		exit 1; \
	fi; \
	echo "submitted workflow: $$WF"; \
	DEADLINE=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.spec.activeDeadlineSeconds}' 2>/dev/null); \
	test -n "$$DEADLINE" || DEADLINE=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.storedWorkflowTemplateSpec.activeDeadlineSeconds}' 2>/dev/null); \
	test -n "$$DEADLINE" || DEADLINE=3600; \
	MAX=$$((DEADLINE + $(EVAL_POLL_MARGIN))); ELAPSED=0; \
	echo "polling up to $$MAX s (activeDeadlineSeconds=$$DEADLINE + $(EVAL_POLL_MARGIN)s margin)"; \
	while :; do \
		phase=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.phase}' 2>/dev/null); \
		prog=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.progress}' 2>/dev/null); \
		echo "  [$$(date +%H:%M:%S)] phase=$$phase progress=$$prog"; \
		case "$$phase" in Succeeded|Failed|Error) break;; esac; \
		if [ $$ELAPSED -ge $$MAX ]; then \
			echo "ERROR: exceeded max poll duration ($$MAX s) with phase='$$phase' — aborting the follow; the workflow (if any) keeps running in-cluster."; \
			exit 1; \
		fi; \
		sleep $(EVAL_POLL_INTERVAL); ELAPSED=$$((ELAPSED + $(EVAL_POLL_INTERVAL))); \
	done; \
	echo; echo "=== aggregate step output ==="; \
	AGG=$$(kubectl -n $(NAMESPACE) get pods -l workflows.argoproj.io/workflow=$$WF -o name | grep aggregate | head -1); \
	test -n "$$AGG" && kubectl -n $(NAMESPACE) logs $$AGG -c main --tail=80 || echo "(aggregate pod not found)"; \
	echo; echo "=== attempts: retries and failed attempts, from the workflow object and every pod's log (NOT in the aggregate above) ==="; \
	T=$$(mktemp -d); kubectl -n $(NAMESPACE) get workflow $$WF -o json | python3 scripts/workflow_nodes.py expand > $$T/wf.json; \
	kubectl -n $(NAMESPACE) logs -l workflows.argoproj.io/workflow=$$WF --prefix --tail=-1 > $$T/pods.log 2>/dev/null; \
	python3 eval/attempts.py --workflow $$T/wf.json --log $$T/pods.log --json-out "$(ATTEMPTS_DIR)/$$WF-attempts.json" || echo "(attempts report failed — run eval/attempts.py on the captured workflow json and pod log)"; \
	rm -rf $$T; \
	test "$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.phase}')" = Succeeded

cost-report: ## Re-runnable cost/brief measurement (runs locally; needs .env)
	python scripts/cost_report.py

# ── Single-VM path (k3s on the OCI A10 box — docs/deploy-runbook.md) ─────────
# These targets run ON the VM over ssh, not on the dev machine. The app image
# and the Argo workflow pods share ONE image (financial-agent-app: one image,
# four commands, plus both eval containers) — vm-images imports that single
# artifact into k3s containerd and lists what both roles will run.
# Fresh-VM prerequisite: bash scripts/vm_bootstrap.sh (ufw 22-only, Docker +
# buildx, container toolkit, k3s with default-runtime nvidia, device plugin,
# kubeconfig, hostPath dirs, tokenizer strip) — NOT YET EXECUTED; see the
# runbook's single-VM section.

VM_IMAGE_TAR ?= /tmp/financial-agent-app.tar

vm-images: ## Build the app+workflow image and import it into k3s containerd
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.k8s -t $(IMAGE) .
	docker save $(IMAGE) -o $(VM_IMAGE_TAR)
	sudo k3s ctr images import $(VM_IMAGE_TAR)
	rm -f $(VM_IMAGE_TAR)
	@echo "── images now in k3s containerd (this one serves the app Deployments AND the Argo workflow pods):"
	@sudo k3s ctr images ls | grep financial-agent || { echo "ERROR: financial-agent image not found after import"; exit 1; }

vm-up: ## Apply the k3s overlays in order: app (+secrets), Argo, vLLM
	@test -f $(ENV_FILE) || { echo "ERROR: $(ENV_FILE) not found — copy .env.example and fill in keys"; exit 1; }
	kubectl apply -f k8s/base/00-namespace.yaml
	@kubectl -n $(NAMESPACE) get secret infra-secrets >/dev/null 2>&1 || { \
		PGPASS=$$(openssl rand -hex 16); \
		kubectl -n $(NAMESPACE) create secret generic infra-secrets \
			--from-literal=POSTGRES_PASSWORD=$$PGPASS \
			--from-literal=DATABASE_URL=postgresql://agent:$$PGPASS@postgres:5432/financial_agent; \
		echo "created infra-secrets (random Postgres password)"; }
	kubectl -n $(NAMESPACE) create secret generic app-secrets \
		--from-env-file=$(ENV_FILE) --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -k k8s/overlays/k3s
	kubectl -n $(NAMESPACE) rollout status deployment/redis     --timeout=180s
	kubectl -n $(NAMESPACE) rollout status deployment/postgres  --timeout=300s
	kubectl -n $(NAMESPACE) rollout status deployment/api       --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/worker    --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/streamlit --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/mcp       --timeout=600s
	kubectl apply -k argo/install
	kubectl -n argo rollout status deploy/workflow-controller --timeout=300s
	kubectl -n argo rollout status deploy/argo-server --timeout=300s
	$(MAKE) argo-deploy ARGO_OVERLAY=k3s
	@# vLLM last: weights must already be at /home/ubuntu/models/qwen-ft (runbook).
	@# Defaults reproduce the committed k3s-gpu deployment and record the model
	@# in app-config for the eval's local-model arm.
	$(MAKE) vm-vllm
	@# local ports 31xxx on purpose: kind maps 30080/30501/30800 on the dev laptop
	@echo "Up. Tunnel from the laptop: ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<vm-ip>"

vm-eval: eval-run ## Run the grounding eval DAG on the VM (same submit/follow as eval-run)

# Model swap for the local-model eval arm (runbook "Model comparison").
# Weights live in /home/ubuntu/models/$(MODEL_DIR); MAX_LEN is per model — a
# 7B bf16 leaves far less KV cache on the 24 GB A10 than the 1.5B fine-tune.
# Defaults reproduce the committed k3s-gpu deployment exactly.
MODEL_DIR ?= qwen-ft
SERVED_NAME ?= financial-lora
MAX_LEN ?= 4096
VLLM_RENDER ?= /tmp/vllm-k3s-gpu

vm-vllm: ## Serve MODEL_DIR as SERVED_NAME (MAX_LEN) on the VM's A10 and point LOCAL_MODEL_NAME at it
	@test -d /home/ubuntu/models/$(MODEL_DIR) || { echo "ERROR: /home/ubuntu/models/$(MODEL_DIR) not found — copy the weights there first"; exit 1; }
	kubectl kustomize k8s/vllm/overlays/k3s-gpu > $(VLLM_RENDER).yaml
	python3 scripts/vllm_model_swap.py --model-dir '$(MODEL_DIR)' --served-name '$(SERVED_NAME)' --max-len '$(MAX_LEN)' \
		< $(VLLM_RENDER).yaml > $(VLLM_RENDER)-swapped.yaml
	kubectl apply -f $(VLLM_RENDER)-swapped.yaml
	kubectl -n $(NAMESPACE) rollout status deployment/vllm --timeout=900s
	@# rollout-ready can precede the NodePort answering: poll up to 120s
	python3 scripts/wait_for_model.py --url http://localhost:30880 --name '$(SERVED_NAME)' --timeout 120
	kubectl -n $(NAMESPACE) patch configmap app-config --type merge -p '{"data":{"LOCAL_MODEL_NAME":"$(SERVED_NAME)","LOCAL_MODEL_DIR":"$(MODEL_DIR)"}}'
	@echo "vLLM serves $(SERVED_NAME) from /home/ubuntu/models/$(MODEL_DIR) (max-model-len $(MAX_LEN)); eval pods read LOCAL_MODEL_NAME/DIR at start."

# GPU SLM endpoint (k8s/llamacpp/overlays/k3s-gpu) on node 2: takes NodePort
# 30880 from the financial-lora vLLM (scaled to 0, its Service deleted —
# `make vm-llamacpp-down && make vm-vllm` restores it). NCMOE>0 = hybrid
# (experts of the first NCMOE layers in host RAM; alias ...-hybrid-ncmoeN).
NCMOE ?= 0
LLAMACPP_RENDER ?= /tmp/llamacpp-k3s-gpu

vm-llamacpp: ## (node 2) Serve the Qwen3.6 GGUF via llama.cpp on the A10, keyed, on NodePort 30880 (NCMOE=0 all-GPU)
	@kubectl -n $(NAMESPACE) get secret llamacpp-api-key -o jsonpath='{.data.LLAMA_API_KEY}' 2>/dev/null | grep -q . || { \
		echo "ERROR: llamacpp-api-key Secret (key LLAMA_API_KEY) missing — create it first (runbook, SLM step 3)"; exit 1; }
	@if kubectl -n $(NAMESPACE) get deployment vllm >/dev/null 2>&1; then kubectl -n $(NAMESPACE) scale deployment/vllm --replicas=0; fi
	kubectl -n $(NAMESPACE) delete service vllm --ignore-not-found
	kubectl kustomize k8s/llamacpp/overlays/k3s-gpu | python3 scripts/llamacpp_layout.py --ncmoe $(NCMOE) > $(LLAMACPP_RENDER).yaml
	kubectl apply -f $(LLAMACPP_RENDER).yaml
	@# first rollout downloads 20.4 GB into /home/ubuntu/models/qwen3.6-35b-a3b-gguf, then loads it to VRAM
	kubectl -n $(NAMESPACE) rollout status deployment/llamacpp --timeout=3600s
	@kubectl -n $(NAMESPACE) logs deploy/llamacpp -c fetch-gguf | tail -2
	@# b11347 prints no layer-offload line at default verbosity, so the layout
	@# evidence is the deployed args plus llama-server's own memory on the A10
	@# (2026-10-03, all layers on the GPU: 20,488 MiB of 23,028 MiB).
	@echo "── GPU layout (record it): deployed args, then llama-server's memory on the GPU per nvidia-smi:"
	@kubectl -n $(NAMESPACE) get deploy llamacpp -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}'
	@nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv
	@nvidia-smi --query-gpu=name,memory.used,memory.total,driver_version --format=csv
	@nvidia-smi --query-compute-apps=process_name --format=csv,noheader | grep -q llama-server || { \
		echo "ERROR: no llama-server process holds GPU memory — the model is not on the A10"; exit 1; }
	@kubectl -n $(NAMESPACE) logs deploy/llamacpp -c llama-server | grep -E "n_threads|n_slots" || true
	LLAMA_API_KEY=$$(kubectl -n $(NAMESPACE) get secret llamacpp-api-key -o jsonpath='{.data.LLAMA_API_KEY}' | base64 -d) \
		python3 scripts/wait_for_model.py --url http://localhost:30880 --timeout 300 --api-key-env LLAMA_API_KEY \
		--name $$(python3 -c "import sys; sys.path.insert(0, 'scripts'); import llamacpp_layout as l; print(l.served_alias($(NCMOE)))")

vm-llamacpp-down: ## (node 2) Remove the llama.cpp endpoint (weights stay on the host); then make vm-vllm restores financial-lora
	kubectl -n $(NAMESPACE) delete deployment/llamacpp service/llamacpp --ignore-not-found

vm-local-model: ## Toggle app-plane local-model routing (ON=true|false); eval arms are unaffected
	@test -n "$(ON)" || { echo "usage: make vm-local-model ON=true|false"; exit 1; }
	kubectl -n $(NAMESPACE) patch configmap app-config --type merge -p '{"data":{"USE_LOCAL_MODEL":"$(ON)"}}'
	kubectl -n $(NAMESPACE) rollout restart deployment/api deployment/worker deployment/streamlit
	@echo "USE_LOCAL_MODEL=$(ON) (live patch — kubectl apply -k k8s/overlays/k3s restores the committed false)"

# ── OKE, provided cluster (docs/deploy-runbook.md "OKE (provided cluster)") ──
# Hosted models only: no vLLM, no GPU. cri-o cannot import images, so every
# image comes from a registry: the app image from GHCR, tagged with the git
# sha it was built from and pinned in both OKE_OVERLAY overlays (never
# :latest). oke-images runs on the LAPTOP (WSL: docker + buildx, logged in to
# ghcr.io with write:packages); oke-up runs on the OPERATOR host (kubectl).

OKE_OVERLAY     ?= oke-provided
GHCR_IMAGE      ?= ghcr.io/schen9999/financial-agent-app
OKE_PULL_SECRET ?= ghcr-pull-secret

oke-images: ## (laptop) Build the app image with BuildKit, push GHCR :<git-sha>, pin it in both OKE_OVERLAY overlays
	@test -z "$$(git status --porcelain)" || { echo "ERROR: working tree is dirty — the image tag must be the commit it was built from. Commit or stash first:"; git status --short; exit 1; }
	@git branch -r --contains HEAD | grep -q . || echo "WARNING: HEAD is not on any remote branch yet — push it so the image's commit is reachable"
	@SHA=$$(git rev-parse HEAD); \
	echo "building $(GHCR_IMAGE):$$SHA"; \
	DOCKER_BUILDKIT=1 docker buildx build --platform linux/amd64 -f Dockerfile.k8s \
		--label org.opencontainers.image.revision=$$SHA \
		--label org.opencontainers.image.source=https://github.com/schen9999/financial-agent \
		-t $(GHCR_IMAGE):$$SHA --push . && \
	python3 scripts/pin_oke_image.py --overlay $(OKE_OVERLAY) --tag $$SHA && \
	echo "Pushed and pinned. Commit the pin, push, then pull on the operator:" && \
	echo "  git commit -am 'Pin $(OKE_OVERLAY) images to $$(echo $$SHA | cut -c1-12)' && git push"

oke-up: ## (operator) Check pin + secrets, apply OKE_OVERLAY, wait for every rollout
	@python3 scripts/pin_oke_image.py --overlay $(OKE_OVERLAY) --check
	@kubectl get storageclass oci-bv >/dev/null || { echo "ERROR: StorageClass oci-bv not found — is KUBECONFIG pointing at the OKE cluster?"; exit 1; }
	kubectl apply -f k8s/base/00-namespace.yaml
	@kubectl -n $(NAMESPACE) get secret app-secrets -o jsonpath='{.data.ANTHROPIC_API_KEY}' 2>/dev/null | grep -q . || { \
		echo "ERROR: app-secrets missing or without ANTHROPIC_API_KEY — stream it from the laptop (runbook, OKE step 3)"; exit 1; }
	@test "$$(kubectl -n $(NAMESPACE) get secret $(OKE_PULL_SECRET) -o jsonpath='{.type}' 2>/dev/null)" = kubernetes.io/dockerconfigjson || { \
		echo "ERROR: $(OKE_PULL_SECRET) (kubernetes.io/dockerconfigjson) missing in $(NAMESPACE) — create it (runbook, OKE step 3)"; exit 1; }
	@kubectl -n $(NAMESPACE) get secret infra-secrets >/dev/null 2>&1 || { \
		PGPASS=$$(openssl rand -hex 16); \
		kubectl -n $(NAMESPACE) create secret generic infra-secrets \
			--from-literal=POSTGRES_PASSWORD=$$PGPASS \
			--from-literal=DATABASE_URL=postgresql://agent:$$PGPASS@postgres:5432/financial_agent; \
		echo "created infra-secrets (random Postgres password)"; }
	kubectl apply -k k8s/overlays/$(OKE_OVERLAY)
	kubectl -n $(NAMESPACE) rollout status deployment/redis     --timeout=300s
	@# first rollout: oci-bv provisions + attaches the 50Gi block volume (WaitForFirstConsumer)
	kubectl -n $(NAMESPACE) rollout status deployment/postgres  --timeout=600s
	kubectl -n $(NAMESPACE) rollout status deployment/api       --timeout=900s
	kubectl -n $(NAMESPACE) rollout status deployment/worker    --timeout=900s
	kubectl -n $(NAMESPACE) rollout status deployment/streamlit --timeout=900s
	kubectl -n $(NAMESPACE) rollout status deployment/mcp       --timeout=900s
	@kubectl -n $(NAMESPACE) get pvc postgres-data
	@echo "Up. Nothing is exposed; on this host:"
	@echo "  kubectl -n $(NAMESPACE) port-forward svc/streamlit 8501:8501 &  kubectl -n $(NAMESPACE) port-forward svc/api 8000:8000 &"
	@echo "then on the laptop: ssh -N -L 32501:localhost:8501 -L 32080:localhost:8000 oke-operator"

# ── Self-served SLM: llama.cpp endpoints (k8s/llamacpp; runbook "SLM endpoints") ──
# Same GGUF and engine build on both: CPU on OKE (oke-llamacpp, operator) and
# GPU on node 2 (vm-llamacpp, on the VM). Every eval against one goes through
# slm-eval-run, which proves the endpoint received the run's traffic.

oke-llamacpp: ## (operator) Deploy the CPU llama.cpp endpoint (downloads + verifies the GGUF once), check it from a harness pod
	@kubectl -n $(NAMESPACE) get secret slm-endpoints -o jsonpath='{.data.SLM_CPU_API_KEY}' 2>/dev/null | grep -q . || { \
		echo "ERROR: slm-endpoints Secret with SLM_CPU_API_KEY missing — create it first (runbook, SLM step 1)"; exit 1; }
	kubectl apply -k k8s/llamacpp/overlays/oke-cpu
	@# first rollout downloads 20.4 GB into the oci-bv PVC, then loads it
	kubectl -n $(NAMESPACE) rollout status deployment/llamacpp --timeout=3600s
	@kubectl -n $(NAMESPACE) logs deploy/llamacpp -c fetch-gguf | tail -2
	@kubectl -n $(NAMESPACE) logs deploy/llamacpp -c llama-server | grep -E "build:|n_threads|system_info|n_slots|offloaded" || true
	@# the harness's own path: app-config + Secret env, key, /v1/models + /props
	kubectl -n $(NAMESPACE) exec deploy/api -- env SLM_FULL=true SLM_ENDPOINT=cpu python -c \
		"import json; from agent.tools.slm import server_facts; print(json.dumps(server_facts(), indent=1))"

oke-llamacpp-down: ## (operator) Remove the CPU endpoint; keeps the PVC so the GGUF is not downloaded again
	kubectl -n $(NAMESPACE) delete deployment/llamacpp service/llamacpp --ignore-not-found

oke-slm-app: ## (operator) Route the live app through the SLM (ON=true|false, ENDPOINT=cpu|gpu); eval arms are unaffected
	@test -n "$(ON)" || { echo "usage: make oke-slm-app ON=true|false [ENDPOINT=cpu|gpu]"; exit 1; }
	kubectl -n $(NAMESPACE) patch configmap app-config --type merge -p '{"data":{"SLM_FULL":"$(ON)","SLM_ENDPOINT":"$(or $(ENDPOINT),cpu)"}}'
	kubectl -n $(NAMESPACE) rollout restart deployment/api deployment/worker deployment/streamlit deployment/mcp
	@echo "SLM_FULL=$(ON) (live patch — kubectl apply -k k8s/overlays/$(OKE_OVERLAY) restores the committed false)"

PROOF_DIR ?= $(HOME)/slm-proof

slm-eval-run: ## (operator) Snapshot the endpoint, run EVAL_RUN_FILE, capture logs, snapshot again, prove the traffic (ENDPOINT=cpu|gpu)
	@test -n "$(ENDPOINT)" || { echo "usage: make slm-eval-run ENDPOINT=cpu|gpu EVAL_RUN_FILE=argo/<slm run file>"; exit 1; }
	@grep -q "value: slm-full-$(ENDPOINT)$$" $(EVAL_RUN_FILE) || { echo "ERROR: $(EVAL_RUN_FILE) is not a slm-full-$(ENDPOINT) run"; exit 1; }
	@P="$(PROOF_DIR)"; mkdir -p "$$P"; STAMP=$$(date -u +%Y%m%dT%H%M%SZ); \
	kubectl -n $(NAMESPACE) exec deploy/api -- python scripts/slm_traffic_proof.py snapshot --endpoint $(ENDPOINT) \
		> "$$P/$$STAMP-before.json" || { echo "ERROR: before-snapshot failed — endpoint unreachable?"; exit 1; }; \
	$(MAKE) --no-print-directory eval-run EVAL_RUN_FILE=$(EVAL_RUN_FILE); rc=$$?; \
	WF=$$(kubectl -n $(NAMESPACE) get workflows --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1:].metadata.name}'); \
	kubectl -n $(NAMESPACE) logs -l workflows.argoproj.io/workflow=$$WF --prefix --tail=-1 > "$$P/$$WF.log"; \
	kubectl -n $(NAMESPACE) get workflow $$WF -o json | python3 scripts/workflow_nodes.py expand > "$$P/$$WF-workflow.json"; \
	kubectl -n $(NAMESPACE) exec deploy/api -- python scripts/slm_traffic_proof.py snapshot --endpoint $(ENDPOINT) \
		> "$$P/$$STAMP-after.json"; \
	mv "$$P/$$STAMP-before.json" "$$P/$$WF-before.json"; \
	mv "$$P/$$STAMP-after.json" "$$P/$$WF-after.json"; \
	echo "=== traffic proof for $$WF (files in $$P) ==="; \
	python3 scripts/slm_traffic_proof.py verify --before "$$P/$$WF-before.json" \
		--after "$$P/$$WF-after.json" --log "$$P/$$WF.log" --workflow "$$P/$$WF-workflow.json"; prc=$$?; \
	if [ -n "$(PROJECT_FOR)" ]; then \
		echo "=== measured run time of $$WF, projected to $(PROJECT_FOR) ==="; \
		kubectl -n $(NAMESPACE) get workflow $$WF -o json | python3 scripts/run_time_projection.py --next $(PROJECT_FOR); \
	fi; \
	echo "eval-run exit $$rc, traffic proof exit $$prc"; test $$rc -eq 0 -a $$prc -eq 0

run-time-check: ## (operator) Gate a long run on a finished smoke's measured per-ticker time: WF=<smoke workflow> NEXT=<run file>
	@test -n "$(WF)" -a -n "$(NEXT)" || { echo "usage: make run-time-check WF=<finished smoke workflow> NEXT=argo/<run file>"; exit 1; }
	kubectl -n $(NAMESPACE) get workflow $(WF) -o json | python3 scripts/run_time_projection.py --next $(NEXT)

# ── vLLM (CPU mode — backs the default-off USE_LOCAL_MODEL flag) ─────────────

VLLM_IMAGE ?= public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2

vllm-deploy: ## Deploy vLLM (CPU mode); the fetch-model init container downloads the model at pod start
	docker pull -q $(VLLM_IMAGE)
	kind load docker-image $(VLLM_IMAGE) --name $(CLUSTER)
	kubectl apply -k k8s/vllm/overlays/kind-cpu
	kubectl -n $(NAMESPACE) rollout status deployment/vllm --timeout=900s
	@echo "vLLM up. In-cluster URL: http://vllm:8000  (port-forward: kubectl -n $(NAMESPACE) port-forward svc/vllm 18000:8000)"

vllm-down: ## Remove the vLLM deployment (frees ~4.5GB on the node)
	kubectl delete -k k8s/vllm/overlays/kind-cpu --ignore-not-found

vllm-bench: ## Benchmark the vLLM endpoint (expects port-forward on :18000)
	python scripts/vllm_benchmark.py --url http://localhost:18000 --json-out /tmp/vllm_bench.json
