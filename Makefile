# Local Kubernetes workflow (single-node kind). Run inside a Linux environment
# with docker + kind + kubectl (on this repo's dev machine: the `financial-agent`
# WSL2 distro). See k8s/README.md for setup and layout.
SHELL := /bin/bash

CLUSTER   ?= financial-agent
NAMESPACE ?= financial-agent
IMAGE     ?= financial-agent-app:local
ENV_FILE  ?= .env

.PHONY: cluster-up deploy smoke-test cluster-down status logs

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
	kubectl apply -f k8s/manifests/00-namespace.yaml
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
	kubectl apply -f k8s/manifests/
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
