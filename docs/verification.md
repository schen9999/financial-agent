# Verification — kustomize migration equivalence

CLAUDE.md constraint 1: kind must remain a working local target
throughout the OCI migration, with overlays instead of forked manifests.
This page documents the proof that the kustomize restructure changed
nothing about what actually runs on kind.

## The proof: scripts/render_diff.py

A semantic diff between two rendered manifest sets. Each side is a
multi-doc YAML file or a directory of `*.yaml`; documents are keyed by
`(apiVersion, kind, namespace, name)`, canonicalized with sorted keys,
and compared. Comments, formatting, field order, and resource order do
**not** count as differences; any real config change does. Exit 0 means
semantically identical; differences print as per-resource unified diffs.

## What was proven (2026-08-31, restructure commit 54d652c)

Baselines were the pre-kustomize manifests at commit `6d7ab9a`
(extracted with `git show`); renders were `kubectl kustomize` of the kind
overlays.

| Comparison | Result |
|---|---|
| `k8s/overlays/kind` vs `k8s/manifests/*.yaml` @ 6d7ab9a | IDENTICAL — 14 resources |
| `argo/overlays/kind` vs `argo/{rbac,eval-workflow,eval-cron}.yaml` @ 6d7ab9a | IDENTICAL — 5 resources |
| `k8s/vllm/overlays/kind-cpu` vs `k8s/vllm/vllm.yaml` @ 6d7ab9a | IDENTICAL — 2 resources |

The oke overlays were additionally build-checked (`kubectl kustomize`
exits 0) and content-checked (OCIR image refs on all four app
deployments and both Argo templates, LoadBalancer + flexible-shape
annotations on api/streamlit, `financial-agent-bv` PVCs at 50Gi, and the
full GPU scheduling block on the vLLM deployment).

## How to re-run

```bash
# Baseline (any pre-migration ref works; 6d7ab9a is the last one):
for f in 00-namespace 10-configmap 20-redis 21-postgres 30-api 31-worker 32-streamlit 33-mcp; do
  echo '---'; git show "6d7ab9a:k8s/manifests/$f.yaml"; echo
done > /tmp/baseline-k8s.yaml

kubectl kustomize k8s/overlays/kind > /tmp/render-k8s-kind.yaml
python3 scripts/render_diff.py /tmp/baseline-k8s.yaml /tmp/render-k8s-kind.yaml
```

Same pattern for `argo/overlays/kind` (baselines `argo/rbac.yaml`,
`argo/eval-workflow.yaml`, `argo/eval-cron.yaml`) and
`k8s/vllm/overlays/kind-cpu` (baseline `k8s/vllm/vllm.yaml`).

The script is general: it can equally diff a rendered oke overlay against
a previous render to review a manifest change, or two overlays against
each other to enumerate exactly what differs between targets.

## Companion gates run with the migration

- `python -m pytest tests/` — 43/43 passing at the restructure commit.
- Full kind deploy through the new targets (`make deploy`,
  `make argo-install`, `make argo-deploy`): all six deployments
  available with probes green, NodePorts unchanged
  (30080/30501/30800), Postgres PVC bound, WorkflowTemplate + nightly
  CronWorkflow applied with the schedule intact.
