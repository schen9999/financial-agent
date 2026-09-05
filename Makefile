# Local Kubernetes workflow (single-node kind). Run inside a Linux environment
# with docker + kind + kubectl (on this repo's dev machine: the `financial-agent`
# WSL2 distro). See k8s/README.md for setup and layout.
SHELL := /bin/bash

CLUSTER   ?= financial-agent
NAMESPACE ?= financial-agent
IMAGE     ?= financial-agent-app:local
ENV_FILE  ?= .env

.PHONY: cluster-up deploy smoke-test cluster-down status logs \
        argo-install argo-deploy eval-run cost-report \
        vm-images vm-up vm-eval

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
	docker build -f Dockerfile.k8s -t $(IMAGE) .
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
	kubectl apply -k argo/overlays/$(ARGO_OVERLAY)
	@echo "Nightly eval scheduled: $$(kubectl -n $(NAMESPACE) get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.schedule} {.spec.timezone}')"

# Override to submit a different one-shot Workflow, e.g. the local-model arm:
#   make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml
EVAL_RUN_FILE ?= argo/eval-run.yaml

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
	MAX=$$((DEADLINE + 600)); ELAPSED=0; \
	echo "polling up to $$MAX s (activeDeadlineSeconds=$$DEADLINE + 600s margin)"; \
	while :; do \
		phase=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.phase}' 2>/dev/null); \
		prog=$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.progress}' 2>/dev/null); \
		echo "  [$$(date +%H:%M:%S)] phase=$$phase progress=$$prog"; \
		case "$$phase" in Succeeded|Failed|Error) break;; esac; \
		if [ $$ELAPSED -ge $$MAX ]; then \
			echo "ERROR: exceeded max poll duration ($$MAX s) with phase='$$phase' — aborting the follow; the workflow (if any) keeps running in-cluster."; \
			exit 1; \
		fi; \
		sleep 20; ELAPSED=$$((ELAPSED + 20)); \
	done; \
	echo; echo "=== aggregate step output ==="; \
	AGG=$$(kubectl -n $(NAMESPACE) get pods -l workflows.argoproj.io/workflow=$$WF -o name | grep aggregate | head -1); \
	test -n "$$AGG" && kubectl -n $(NAMESPACE) logs $$AGG -c main --tail=80 || echo "(aggregate pod not found)"; \
	test "$$(kubectl -n $(NAMESPACE) get workflow $$WF -o jsonpath='{.status.phase}')" = Succeeded

cost-report: ## Re-runnable cost/brief measurement (runs locally; needs .env)
	python scripts/cost_report.py

# ── Single-VM path (k3s on the OCI A10 box — docs/deploy-runbook.md) ─────────
# These targets run ON the VM over ssh, not on the dev machine. The app image
# and the Argo workflow pods share ONE image (financial-agent-app: one image,
# four commands, plus both eval containers) — vm-images imports that single
# artifact into k3s containerd and lists what both roles will run.

VM_IMAGE_TAR ?= /tmp/financial-agent-app.tar

vm-images: ## Build the app+workflow image and import it into k3s containerd
	docker build -f Dockerfile.k8s -t $(IMAGE) .
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
	@# vLLM last: weights must already be at /home/ubuntu/models/qwen-ft (runbook)
	kubectl apply -k k8s/vllm/overlays/k3s-gpu
	kubectl -n $(NAMESPACE) rollout status deployment/vllm --timeout=900s
	@# local ports 31xxx on purpose: kind maps 30080/30501/30800 on the dev laptop
	@echo "Up. Tunnel from the laptop: ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<vm-ip>"

vm-eval: eval-run ## Run the grounding eval DAG on the VM (same submit/follow as eval-run)

vm-local-model: ## Toggle app-plane local-model routing (ON=true|false); eval arms are unaffected
	@test -n "$(ON)" || { echo "usage: make vm-local-model ON=true|false"; exit 1; }
	kubectl -n $(NAMESPACE) patch configmap app-config --type merge -p '{"data":{"USE_LOCAL_MODEL":"$(ON)"}}'
	kubectl -n $(NAMESPACE) rollout restart deployment/api deployment/worker deployment/streamlit
	@echo "USE_LOCAL_MODEL=$(ON) (live patch — kubectl apply -k k8s/overlays/k3s restores the committed false)"

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
