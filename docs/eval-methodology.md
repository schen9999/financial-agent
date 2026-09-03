# Eval methodology — the grounding-eval DAG

The centerpiece of this project is not the UI; it is that grounding is
**measured by a committed, re-runnable harness and gated in CI fashion**.
The number of record: **49% pre-fix → 0/84 unsupported in the current
eval** (always quoted with the pre-fix context and denominator, never as a
bare 0%).

## What is measured

`grounding_check.py` runs the full agent pipeline per ticker and checks
every factual claim in the brief against the retrieved sources; a claim
with no supporting chunk counts as unsupported. The metric is the
unsupported-claim rate across the run.

## The DAG (argo/base/eval-workflow.yaml)

```
main (DAG)
 ├── eval-ticker   fan-out: one pod per ticker (withParam over the
 │                 `tickers` parameter, default 10 large-caps)
 └── aggregate     depends on all fan-out results
```

- **Fan-out pods** run `grounding_check.py --tickers {{ticker}} --arms
  baseline` in the same app image as the services. `parallelism: 2`
  bounds concurrency (each pod imports the torch/embedding stack); one
  retry per ticker (`retryPolicy: OnFailure`) absorbs transient upstream
  flakiness.
- **Results travel as output parameters** (small JSON per ticker), so no
  artifact repository is required on the local cluster.
- **Artifact archival is wired but off by default**: when
  `EVAL_ARTIFACTS_PUT_URL` is set (a write-capable Object Storage PAR,
  Phase 2), the aggregate step PUTs `aggregate.json` + `results.json`
  under `eval-runs/<run-id>/` in the versioned eval-artifacts bucket —
  failed runs included (they are the most valuable to keep). Best-effort
  by design: an upload failure prints a WARNING and never changes the
  gate's exit code. Unit-tested with a mocked client
  (tests/test_eval_artifacts.py). No upload has run yet — first real
  archival happens in Phase 2.
- **The aggregate step is a gate**: `scripts/eval_aggregate.py
  --max-unsupported-pct 5 --min-claims 30` fails the workflow if the
  unsupported rate breaches 5% **or** the run produced too few claims to
  be meaningful (min-claims guards against a quiet run passing vacuously).
  A failed gate fails the whole workflow — visibly.

## Rigor rules

- **Eval pods never touch the live cache**: `BYPASS_CACHE=true` is set in
  the pod env (and by the harness itself). A cache hit would measure the
  cache, not the pipeline.
- **A/B comparisons hold retrieval constant** (same chunk count per arm)
  and run the full suite — never a subset for one arm.
- **Any new number quoted in docs must come from a committed,
  re-runnable harness** (this DAG, `scripts/cost_report.py`, or
  `scripts/vllm_benchmark.py`). See
  [numbers-of-record.md](numbers-of-record.md).

## Scheduling and submission

- **Nightly**: `grounding-eval-nightly` CronWorkflow, `30 3 * * *`
  America/New_York, `concurrencyPolicy: Forbid`, 3+3 run history,
  1h starting deadline.
- **On demand**: `make eval-run` submits `argo/eval-run.yaml` (a one-shot
  Workflow referencing the `grounding-eval` WorkflowTemplate) and follows
  it to completion, printing the aggregate output. `eval-run.yaml` lives
  outside kustomize on purpose: the image is resolved by whichever
  overlay applied the WorkflowTemplate, so submission is
  environment-agnostic.
- **Arm selection**: the template takes an `arms` parameter (default
  `baseline` — the gate arm the nightly cron runs). The harness pins the
  model-routing flags per arm so A/B arms can't leak into each other;
  `argo/eval-run-local.yaml` submits the `local-model` arm
  (`make eval-run EVAL_RUN_FILE=argo/eval-run-local.yaml`) — first run
  2026-09-03, gate failed; see the dated A/B below.

## Dated A/B on the single-VM target (2026-09-03)

Same VM, same harness, ~40 minutes apart, 10/10 tickers each, no
retries. vLLM traffic confirmed for the local arm: 20 POST
`/v1/chat/completions` (2 trained sections × 10 tickers).

| Arm | Workflow | Claims | Sup/Uns/Inf | Unsupported | Gate (≤5%) |
|---|---|---|---|---|---|
| `baseline` (hosted) | grounding-eval-6zwqf | 66 | 51/2/13 | 3.03% | PASSED |
| `local-model` (in-cluster vLLM fine-tune, 2 sections) | grounding-eval-local-dkghz | 65 | 48/8/9 | **12.31%** | **FAILED** |

The fine-tune serves in-cluster but does not pass the grounding gate on
the two sections it owns. Consequence: `USE_LOCAL_MODEL` stays off in
production config — hosted models remain the production path — and this
A/B is the measured reason (consistent in direction with the Phase 0
audit's decision to ship the local model off). These are dated run
records from the committed harness; the numbers-of-record table is
unchanged.

## Boundary

Argo owns eval orchestration; Celery owns request-time async. The eval
DAG runs the pipeline in its own pods — it does not call the API service
and cannot contend with user traffic for the cache or the broker.
