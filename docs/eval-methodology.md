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

| Arm | Workflow | Claims | Sup/Uns/Inf | Unsupported (Wilson 95% CI) | Gate (≤5%) |
|---|---|---|---|---|---|
| `baseline` (hosted) | grounding-eval-6zwqf | 66 | 51/2/13 | 3.03% (0.8–10.4%) | PASSED |
| `local-model` (in-cluster vLLM fine-tune, 2 sections) | grounding-eval-local-dkghz | 65 | 48/8/9 | **12.31%** (6.4–22.5%) | **FAILED** |

Fisher exact (two-sided) on 2/66 vs 8/65: **p = 0.0545** (`eval/stats.py`).

Read this with the statistics in view: the gate verdicts are operational
facts (the run each arm is gated on passed/failed), but the intervals
overlap and p = 0.054 — **this single A/B does not statistically separate
the arms on its own.** The decision to ship `USE_LOCAL_MODEL` off rests
on the direction agreeing across independent measurements (85.4% vs
88.6% at training time, 86.2% vs 77.8% in the Aug 2026 re-measure, and
this run), not on one 10-ticker pass. A larger benchmark to tighten
these intervals is prepared (`eval/tickers_extended.txt` +
`argo/eval-run-extended.yaml`, 40 tickers) and pending a funded run.
These are dated run records from the committed
harness; the numbers-of-record table is unchanged.

## Statistical power

Every reported rate carries a Wilson 95% interval and every two-arm
comparison a Fisher exact p-value (`eval/stats.py`, wired into
`scripts/eval_aggregate.py` and `grounding_check.py`). The reason this
is mandatory at the current scale: **N = 66 claims cannot resolve a 3%
observed rate against a 5% gate** — the Wilson 95% interval for 2/66 is
0.8–10.4%, which contains the gate on both sides, so a "pass" at 3.03%
is fully consistent with a true rate above 5% (and a mild fail with one
below it). Distinguishing 3% from 5% with useful power needs claims in
the several-hundreds — the motivation for the extended benchmark.

## Judge validation — results pending

The Sonnet judge (temperature 0) has had no human validation; until it
does, every grounding number in this repo measures agreement with one
model's reading, not ground truth. The protocol, built and awaiting
labels:

- **Sample**: `eval/judge_validation/sample.csv` — 50 claims,
  stratified over the judge's labels (16 SUPPORTED / 3 UNSUPPORTED /
  31 INFERENCE — all scarce strata kept in full, INFERENCE deliberately
  heavy because that's where judge/human ambiguity lives), drawn from a
  176-claim pool with `eval/label.py --seed 42`.
- **Provenance, stated exactly**: the pool is the committed
  `eval_findings/` per-claim artifacts of the **2026-08-24 local run**
  (baseline + local-model arms, same judge and prompt as every DAG run).
  It is *not* the Sep 3 `grounding-eval-6zwqf` run: that run's per-claim
  findings were written inside the eval pods and never archived — a
  known gap (the artifact-archival feature uploads aggregate/results
  JSON only, not findings).
- **Blinding**: the labeling CSV carries claim + retrieved context +
  audited text only; the judge's verdict and the arm each claim came
  from live in `sample_key.csv`, which is not opened until labeling is
  done. Caveat disclosed: findings files do not persist the four
  pre-written sections the judge additionally saw, so the human labels
  against slightly less context.
- **Analysis**: `eval/agreement.py` reports Cohen's kappa (3-class) and
  the judge's precision/recall on UNSUPPORTED with human labels as
  truth, all with Wilson 95% intervals.

**Results: pending.** No human labels exist yet; no agreement number
may be quoted until `eval/agreement.py` has run on the completed CSV.

### Injected-failure check (measured 2026-09-04)

Orthogonal to human labels: `eval/perturb.py` builds fixtures with
*known* ground truth from committed run artifacts — a supported number
swapped in the audited text, the supporting context lines dropped, or a
plausible fabricated claim inserted — 20 unique tagged fixtures
committed (`eval/perturbed/fixtures.jsonl`, 7/7/6 across the three
types). `eval/critic_check.py` runs the real judge over them:
**recall 20/20 = 100% (95% CI 83.9–100%)**; precision vs the injection
tags 71.4% (95% CI 52.9–84.7%).

Treat that precision as a **lower bound with real run-to-run noise**,
for three audited reasons. (1) An off-needle flag can be a *legitimate
cascade* of the injection: in the one case auditable from a same-day
re-run, swapping NVDA's price to $283.50 made the untouched claim
"sits in the upper-middle of its 52-week range" genuinely unsupported —
the injected price exceeds the context's 52-week high — and the judge
was right to flag it. (2) Fixtures omit the pre-written sections the
judge normally also sees. (3) Even at temperature 0 the judge's claim
segmentation varies between runs: the recorded run produced 8
off-needle flags (5 on one fixture), while a re-run of those 4 fixtures
on identical inputs reproduced all 4 on-needle detections but only 1 of
the 8 off-needle flags. The recorded run's off-needle claim texts were
not persisted (the tool now persists them), so the other 7 cannot be
adjudicated — nothing beyond the audited case is claimed about them.
Recall, the gated metric, reproduced exactly. A gated CI job
(`.github/workflows/critic-injection.yml`) re-runs this on
judge-adjacent changes and asserts recall ≥ 0.8; the bar does not move
if it regresses — the number gets reported instead.

## Boundary

Argo owns eval orchestration; Celery owns request-time async. The eval
DAG runs the pipeline in its own pods — it does not call the API service
and cannot contend with user traffic for the cache or the broker.
