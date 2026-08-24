# Kubernetes (kind) deployment

Runs the **full designed topology** — FastAPI, Celery worker, Redis, Postgres,
Streamlit UI, MCP server — on a single-node [kind](https://kind.sigs.k8s.io/)
cluster. Per the Phase 0 audit this is the first environment where that topology
runs complete (ECS runs a reduced single-container deployment; local dev runs
Streamlit in-process without a worker).

## Layout

```
k8s/
  kind-config.yaml        # single node; NodePorts 30080/30501/30800 mapped to host
  secret.env.template     # documents the app-secrets keys (real values come from .env)
  manifests/
    00-namespace.yaml
    10-configmap.yaml     # in-cluster REDIS_URL + feature flags at audited defaults
    20-redis.yaml         # cache (exact key research:{TICKER}) + Celery broker
    21-postgres.yaml      # research_briefs, PVC-backed, generated password
    30-api.yaml           # FastAPI (NodePort 30080)
    31-worker.yaml        # Celery worker (first env where async actually completes)
    32-streamlit.yaml     # UI, in-process pipeline, unchanged app.py (NodePort 30501)
    33-mcp.yaml           # MCP streamable-HTTP (NodePort 30800, endpoint /mcp)
Dockerfile.k8s            # one app image for api/worker/streamlit/mcp (CPU torch)
Makefile                  # cluster-up / deploy / smoke-test / cluster-down
scripts/k8s_smoke_test.sh
```

## Prerequisites

Linux environment with `docker`, `kind`, `kubectl`, `make`, `jq`, `openssl`, and
a filled-in `.env` in the repo root (same keys as `.env.example`). On this
project's dev machine that environment is a WSL2 Ubuntu 24.04 distro named
`financial-agent` (Docker CE runs inside it under systemd; no Docker Desktop).

```bash
# From Windows, enter the distro at the repo:
wsl -d financial-agent
cd "/mnt/c/Users/Samuel Chen/Documents/Projects/financial-agent"
```

## Workflow

```bash
make cluster-up    # create the kind cluster (idempotent)
make deploy        # build image, kind load, secrets from .env, apply, wait for rollout
make smoke-test    # end-to-end: sync brief, cache hit/miss, Celery async, MCP, UI
make cluster-down  # delete the cluster
make status        # pods/services/events
make logs C=api    # tail one component
```

After `make deploy`:

| Component | URL (host) |
|---|---|
| FastAPI | http://localhost:30080 (docs at /docs) |
| Streamlit UI | http://localhost:30501 |
| MCP (streamable-HTTP) | http://localhost:30800/mcp |

## Design notes

- **One image, four commands.** `Dockerfile.k8s` builds from the full
  `requirements.txt` (the ECS image's `requirements-api.txt` lacks streamlit and
  mcp); api/worker/streamlit/mcp differ only in the manifest `command`. The ECS
  `Dockerfile` is untouched. Torch is installed from the CPU wheel index —
  ~4-5 GB smaller than the default CUDA-bundled Linux wheel, and this cluster
  has no GPU.
- **Secrets via .env templating, never committed.** `make deploy` materializes
  `app-secrets` from your local `.env` (`kubectl create secret --from-env-file`)
  and generates `infra-secrets` (random Postgres password + `DATABASE_URL`)
  once, in-cluster only. `k8s/secret.env.template` documents the keys.
- **envFrom ordering as config override.** Pods load `app-secrets` →
  `infra-secrets` → `app-config`; later sources win, so the in-cluster
  `REDIS_URL`/`DATABASE_URL` override whatever the developer's `.env` carries.
- **Flags at audited defaults.** The ConfigMap restates
  `RERANKING_ENABLED=false`, `USE_LOCAL_MODEL=false`, `MULTI_AGENT_ENABLED=false`
  (see `docs/PHASE0_AUDIT.md` for why each ships off). Toggling is a ConfigMap
  edit + `kubectl rollout restart`, not a rebuild.
- **Streamlit stays in-process.** The UI pod runs `app.py` unchanged — the
  pipeline executes inside the Streamlit pod exactly as on Streamlit Cloud.
  That's why its resources look like the API's, and why it needs the same
  secrets.
- **Probes.** HTTP probes for api (`/health`) and streamlit (`/_stcore/health`);
  exec probes for redis (`redis-cli ping`), postgres (`pg_isready`), and the
  worker (`celery inspect ping` targeted at the pod's own node name); tcpSocket
  for MCP (its endpoint speaks MCP framing, not plain GET). Generous
  startupProbes cover the slow torch + embedding-model import.
- **Single replica each.** The node has 4 CPUs / ~8 GB; requests total ~1.2 CPU
  / ~3 GB with limits allowing bursts. Scaling the worker horizontally is a
  `replicas` bump — tasks are queue-distributed — but is pointless on one node.
