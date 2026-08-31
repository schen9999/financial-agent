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
  artifact repository is required on the local cluster. Wiring artifacts
  to the OCI Object Storage bucket is a Phase 2 task.
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

## Boundary

Argo owns eval orchestration; Celery owns request-time async. The eval
DAG runs the pipeline in its own pods — it does not call the API service
and cannot contend with user traffic for the cache or the broker.
