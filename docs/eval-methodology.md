# Eval methodology — the grounding-eval DAG

The centerpiece of this project is not the UI; it is that grounding is
**measured by a committed, re-runnable harness and gated in CI fashion**.
The grounding number of record: **12/392 = 3.06% unsupported (Wilson 95%
CI 1.8–5.3%)**, hosted baseline `j4cnp` (2026-09-05/06), judge v2, fixed
retrieval, 40 tickers. That is the judge-flagged rate; the reweighted true-rate estimate 5.7% (CI 3.5–9.9%),
from the v2 calibration of record: precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED). The former "49% pre-fix → 0/84"
(judge v1, pre-retrieval-fix, 2026-08-24) is a dated record only. Never a
bare rate or a bare 0%.

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

## Extended baseline: 40 tickers (2026-09-05)

`grounding-eval-extended-9j2dj` — the first run at meaningful N, on
**judge v2** against the **post-retrieval-fix index** (real Item 1A
prose): **387 claims** across 40/40 tickers in 27 min (est. $2.35),
**357 S / 12 U / 18 I = 3.10% unsupported (95% CI 1.8–5.3%)** — the
point estimate is below the 5% gate; **the interval includes the
gate.** INFERENCE share fell to 4.7% (18/387) from ~20% under v1,
consistent with v2's narrowed INFERENCE definition. Coverage notes:
the five ADRs ran without SEC context (20-F filers); per-ticker claim
counts ranged 1–23; UPST is the outlier at 3/14 unsupported. Artifacts:
`eval/runs/9j2dj-full.log`, `9j2dj-workflow.yaml`, per-claim rows in
`9j2dj-claims.jsonl` — full claim text and judge rationale for all
rows, recovered post-hoc from containerd snapshots into
`raw/9j2dj-findings/` (contexts by sha256 in `9j2dj-contexts/`; one
UNSUPPORTED verdict was free-form, carried with claim=null; findings
dumps are now a standing part of every run — see the runbook's
findings-capture section). Calibration: this is a judge-flagged rate
(judge v2 calibration of record: precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED)); no reweighted estimate is computed for
this run. **Not the number of
record**: superseded as a baseline by `j4cnp` (below, same tickers on
the rebuilt image).

## 40-ticker A/B: hosted baseline vs in-cluster fine-tune (2026-09-05/06)

Both arms ran on the **same VM image** and the **same post-retrieval-fix
index**, judge **v2**, over the 40 extended tickers
(`eval/tickers_extended.txt`). The five ADRs (TSM, NVO, BABA, TM, SAP)
ran on **stock + news data only** in both arms — 20-F filers, no SEC
context (verified from the archived contexts: every RAG field
"(not available)"). Per-claim rows: `eval/runs/j4cnp-claims.jsonl` and
`eval/runs/lsnnc-claims.jsonl`; contexts by sha256 beside them.

| Arm | Workflow | Claims | Sup/Uns/Inf | Unsupported (Wilson 95% CI) | Gate (≤5%) | Est. cost |
|---|---|---|---|---|---|---|
| `baseline` (hosted) | grounding-eval-extended-j4cnp | 392 | 354/12/26 | 3.06% (1.8–5.3%) | PASSED | $2.36 |
| `local-model` (in-cluster vLLM fine-tune, 2 sections) | grounding-eval-extended-local-lsnnc | 368 | 324/30/14 | **8.15%** (5.8–11.4%) | **FAILED** | $2.44 |

Fisher exact (two-sided) on 12/392 vs 30/368: **p = 0.0023**
(`eval/stats.py`). Unlike the 10-ticker A/B of 2026-09-03 (p = 0.054),
**this A/B separates the arms on its own**: the intervals are disjoint
and the local arm's interval sits entirely above the gate. The ship-off
decision for `USE_LOCAL_MODEL` now rests on this clearly separated
40-ticker A/B (the earlier, underpowered measurements agree in
direction). Calibration: these are judge-flagged rates (judge v2
calibration of record: precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED)). Reweighted true-rate estimates (`eval/reweight_calibration.py`):
`j4cnp` 5.7% (CI 3.5–9.9%), `lsnnc` 8.3% (CI 5.5–12.5%). The A/B
direction (3.06% vs 8.15%, p = 0.0023) and the per-section attribution
stand: the same judge scored both arms, so its misses apply to both.
Per-section reweighted estimates appear as a sensitivity row under the
table below.

### Where the local arm fails: the sections the fine-tune owns

The fine-tune writes only Financial Health and Risk Factors; Haiku keeps
the other two sections in both arms. Attributing each judged claim to
the pre-written section it restates (`eval/section_attribution.py`,
committed: normalized containment, else word-overlap ≥ 0.6, else
unattributed — a heuristic over paraphrased text, coverage ~78–79%; the
overall A/B above is the measured result, the buckets are diagnostic):

| Arm | Fine-tune-owned (FH + RF) | Other sections | Unattributed |
|---|---|---|---|
| `baseline` | 1/202 = 0.50% (0.1–2.8%) | 3/104 = 2.88% (1.0–8.1%) | 8/86 = 9.30% (4.8–17.3%) |
| `local-model` | **22/111 = 19.82%** (13.5–28.2%) | 2/180 = 1.11% (0.3–4.0%) | 6/77 = 7.79% (3.6–16.0%) |
| Fisher exact | **p = 4.6e-10** | p = 0.36 | p = 0.79 |
| *Sensitivity: reweighted true-rate estimate, baseline vs local-model* | *3.6% (1.5–7.9%) vs 14.6% (9.5–20.0%)* | *5.0% (2.8–9.2%) vs 4.1% (2.0–8.3%)* | *11.2% (7.3–18.3%) vs 9.0% (6.0–13.8%)* |

The headline is the judge-flagged comparison above (0.50% vs 19.82%,
p = 4.6e-10). The sensitivity row reweights each bucket with
`eval/reweight_calibration.py --by-section`, which assumes one
judge-SUPPORTED miss rate (4/123 in the calibration of record) shared across
both arms and all sections; the sample cannot say whether misses
differ by arm or section. Under that assumption the baseline's FH + RF
estimate is almost entirely the assumed miss rate applied to its 199
judge-SUPPORTED claims, which is why the gap narrows.

The excess unsupported rate is concentrated **entirely in the content
the fine-tune authored**; the arms are statistically indistinguishable
everywhere else. Note the attribution shift itself: the baseline's
synthesis restates FH/RF content near-verbatim (202 claims attributed)
while the fine-tune's phrasing is restated less (111) — one more sign
the fine-tune's sections diverge from their sources.

### Run-to-run variance and observations

- Baseline stability: `9j2dj` (previous image) 12/387 = 3.10% vs `j4cnp`
  12/392 = 3.06%, Fisher p = 1.0 — the baseline is stable across the
  image rebuild and the MSFT reindex.
- WMT is the local arm's outlier: 9/16 unsupported.
- CALM on `j4cnp` stalled in the pipeline: 185.61 s (retrieval 27.15 s)
  vs the ~30 s typical — an observation, not yet diagnosed.
- Neither run produced a duplicate judge label (the `9j2dj` JPM
  double-label); four free-form verdicts without CLAIM lines are carried
  in the rows with `claim=null` (j4cnp: EDIT/OCGN/UNH UNSUPPORTED;
  lsnnc: VERV INFERENCE).
- Local-model arm, found during held-out labeling (observation, no
  fix): the fine-tune's CRBU Financial Health section states a "$16.8
  billion" market cap for a $1.57 stock and "[City Name]" as
  headquarters. The archived context shows `market_cap: 168315792.0` —
  **$168.3 million**: the digits trace to the real value but at 100×
  the magnitude (a scale-conversion error, not an invention), while the
  stock JSON has no headquarters field at all — "[City Name]" is a
  literal unfilled template placeholder. **The judge flagged neither**,
  and by design could not: it audits the synthesis's Exec Summary +
  Outlook, and the Sonnet synthesis dropped both errors (the audited
  text contains no market-cap or headquarters claim). Scope consequence,
  stated plainly: fine-tune section errors count against the gate only
  when the synthesis repeats them, so the measured 8.15% understates
  the fine-tune's raw section error rate.

## Four-arm model comparison (2026-09-23) — a dated comparison set

**A dated comparison set, not numbers of record.** Four runs on node 2
(`vm-a10-inst-2`, VM.GPU.A10.1, single-node k3s), all on 2026-09-23 (US
time; the last run finished 00:13 UTC on the 24th), branch `model-compare`
image, 40 extended tickers, judge **v2**. The arms differ **only in who
writes the Financial Health and Risk Factors sections**: in every arm Haiku
writes Recent Developments and SEC Filing Highlights, Sonnet writes the
synthesis, and Sonnet judges it. The hosted arm uses Haiku for all four
sections; the three local arms serve FH + RF from vLLM v0.10.2 on the one
A10 (max-model-len 4096, `--gpu-memory-utilization=0.90`, max-num-seqs 8),
swapped with `make vm-vllm`, with identical pinned sampling
(temperature 0.1, max_tokens 512, top_p 0.8, top_k 20,
repetition_penalty 1.1, min_p 0.0). Each local run's served name, model dir,
and sampling are recorded in its findings metadata and aggregate.

| Arm (FH + RF writer) | Workflow | Claims | Sup/Uns/Inf | Unsupported (Wilson 95% CI) | Gate (≤5%) | Est. cost |
|---|---|---|---|---|---|---|
| hosted (Haiku) | grounding-eval-extended-kcf7s | 383 | 364/4/15 | 1.04% (0.4–2.7%) | PASSED | $2.33 |
| hosted (Haiku), rerun 2026-09-24, same image | grounding-eval-extended-dvvxk | 389 | 353/7/29 | 1.80% (0.9–3.7%) | PASSED | $2.34 |
| financial-lora (Qwen2.5-1.5B + LoRA, merged) | grounding-eval-extended-local-v924f | 385 | 346/25/14 | 6.49% (4.4–9.4%) | FAILED | $2.49 |
| qwen2.5-1.5b-instruct (base) | grounding-eval-extended-local-4nfsm | 400 | 352/31/17 | 7.75% (5.5–10.8%) | FAILED | $2.27 |
| qwen2.5-7b-instruct (base) | grounding-eval-extended-local-cnkp2 | 393 | 353/18/22 | 4.58% (2.9–7.1%) | PASSED (point estimate only) | $1.98 |

Exact two-sided Fisher on unsupported vs not, all six pairs (all judged
claims; no multiplicity correction):

| Pair | Counts | p |
|---|---|---|
| hosted `kcf7s` vs financial-lora `v924f` | 4/383 vs 25/385 | 7.8e-05 |
| hosted `kcf7s` vs qwen2.5-1.5b `4nfsm` | 4/383 vs 31/400 | 2.6e-06 |
| hosted `kcf7s` vs qwen2.5-7b `cnkp2` | 4/383 vs 18/393 | 0.0039 |
| financial-lora `v924f` vs qwen2.5-1.5b `4nfsm` | 25/385 vs 31/400 | 0.5794 |
| financial-lora `v924f` vs qwen2.5-7b `cnkp2` | 25/385 vs 18/393 | 0.2737 |
| qwen2.5-1.5b `4nfsm` vs qwen2.5-7b `cnkp2` | 31/400 vs 18/393 | 0.0764 |

Against the other hosted run on the same image (the 2026-09-24 rerun
`dvvxk`) and against both hosted runs pooled (`kcf7s` + `dvvxk`, 11/772 =
1.42%), same test (`--pool`, added 2026-09-28):

| Pair | Counts | p |
|---|---|---|
| hosted rerun `dvvxk` vs financial-lora `v924f` | 7/389 vs 25/385 | 0.0010 |
| hosted rerun `dvvxk` vs qwen2.5-1.5b `4nfsm` | 7/389 vs 31/400 | 8.5e-05 |
| hosted rerun `dvvxk` vs qwen2.5-7b `cnkp2` | 7/389 vs 18/393 | 0.0401 |
| hosted pooled vs financial-lora `v924f` | 11/772 vs 25/385 | 7.5e-06 |
| hosted pooled vs qwen2.5-1.5b `4nfsm` | 11/772 vs 31/400 | 1.2e-07 |
| hosted pooled vs qwen2.5-7b `cnkp2` | 11/772 vs 18/393 | 0.0022 |

What the set supports, and only this:

- **The fine-tune matched its own base model.** financial-lora `v924f`
  6.49% (4.4–9.4%) vs qwen2.5-1.5b-instruct `4nfsm` 7.75% (5.5–10.8%),
  p = 0.58: the LoRA neither helped nor hurt grounding measurably.
- **Within Qwen2.5, 1.5B → 7B improved, with borderline significance.**
  `4nfsm` 7.75% (5.5–10.8%) vs `cnkp2` 4.58% (2.9–7.1%), p = 0.076 on all
  claims — not significant at 0.05. On the sections the local model
  writes (below) the gap is larger (p = 0.014), but that is one of several
  buckets tested and carries no multiplicity correction.
- **Every open-weight arm trailed hosted.** `kcf7s` 1.04% (0.4–2.7%)
  against each local arm: p = 7.8e-05, 2.6e-06, 0.0039. It holds against
  the higher of the two hosted runs too: the 7B, the closest arm, trails
  the rerun `dvvxk` 1.80% (0.9–3.7%) at p = 0.040 and both hosted runs
  pooled, 11/772 = 1.42% (0.8–2.5%), at p = 0.0022.
- **The 7B gate pass is on the point estimate only.** `cnkp2`'s 4.58% is
  under the 5% gate, but its interval (2.9–7.1%) spans it, so the run is
  consistent with a true rate above the gate.

Not supported: a size curve. The hosted arm is a different model family
(Anthropic Haiku, size undisclosed), not a larger Qwen, so the four arms
are not points on one scaling line; only the three Qwen2.5 arms share a
family.

Calibration: every rate here is a judge-flagged rate (judge v2 calibration of record:
precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED)). No reweighted estimate is computed: the held-out miss rates
were measured on `j4cnp`/`lsnnc` claims and are not extended to other
models. Comparisons hold in direction because all arms share the judge. A four-arm held-out sample is
drawn for re-validating the judge on this claim set (below) and is not yet
labeled.

### Per section: where the local arms' unsupported claims come from

Attribution by `eval/multi_arm_stats.py` (the `eval/section_attribution.py`
heuristic unchanged: normalized containment, else word-overlap ≥ 0.6, else
unattributed; free-form verdicts without a CLAIM line count as
unattributed). Buckets are diagnostic; the table above is the measured
result.

| Section (writer in local arms) | hosted `kcf7s` | financial-lora `v924f` | qwen2.5-1.5b `4nfsm` | qwen2.5-7b `cnkp2` |
|---|---|---|---|---|
| **Financial Health (local model)** | 1/181 = 0.55% (0.1–3.1%) | **15/85 = 17.65%** (11.0–27.1%) | **16/127 = 12.60%** (7.9–19.5%) | 6/163 = 3.68% (1.7–7.8%) |
| **Risk Factors (local model)** | 0/18 = 0.00% (0.0–17.6%) | 0/27 = 0.00% (0.0–12.5%) | 0/19 = 0.00% (0.0–16.8%) | 0/3 = 0.00% (0.0–56.1%) |
| Recent Developments (Haiku) | 1/45 = 2.22% (0.4–11.6%) | 2/111 = 1.80% (0.5–6.3%) | 3/83 = 3.61% (1.2–10.1%) | 4/62 = 6.45% (2.5–15.4%) |
| SEC Filing Highlights (Haiku) | 0/72 = 0.00% (0.0–5.1%) | 0/80 = 0.00% (0.0–4.6%) | 1/89 = 1.12% (0.2–6.1%) | 0/78 = 0.00% (0.0–4.7%) |
| Unattributed (synthesis phrasing) | 2/67 = 2.99% (0.8–10.2%) | 8/82 = 9.76% (5.0–18.1%) | 11/82 = 13.41% (7.7–22.4%) | 8/87 = 9.20% (4.7–17.1%) |

FH + RF combined, pairwise Fisher: hosted 1/199 vs financial-lora 15/112
(p = 1.3e-06), vs 1.5B base 16/146 (p = 6.9e-06), vs 7B base 6/166
(p = 0.0500); financial-lora vs 1.5B base p = 0.57; financial-lora vs 7B
base p = 0.0044; 1.5B base vs 7B base p = 0.014. All other claims
combined: the lowest p is 0.028 (hosted vs 1.5B base), and the three
local arms are indistinguishable from each other (p ≥ 0.31).

Every unsupported claim in the locally written sections is attributed to
Financial Health; Risk Factors contributed none in any arm. The 7B's risk
section is almost never restated by the synthesis (3 attributed claims,
against 18–27 elsewhere), so its Risk Factors cell says nothing. As on
2026-09-05/06, the fine-tune's Financial Health text is restated less than
its base's (85 vs 127 claims attributed). The unattributed bucket runs
higher in all three local arms (9.2–13.4%) than hosted (3.0%), with wide
intervals: synthesis-original claims may be degrading when the input
sections are weaker, which this attribution can't resolve.

### Serving benchmark on the A10 (2026-09-23)

`scripts/vm_bench_serve.sh` on node 2, run inside the vLLM pod against
localhost:8000, one model at a time on the same deployment args as the
eval runs. Identical settings for all three: `vllm bench serve`, random
dataset, 1024 input / 256 output tokens with `--ignore-eos`, 200 prompts,
request rate inf, max concurrency 8, seed 0, `/v1/completions`, after an
untimed 16-prompt warmup. All 200 requests succeeded in every run (204,065
input / 51,200 output tokens each). Raw results:
`eval/runs/bench/<served-name>.json`.

| Model | Output tok/s | Total tok/s | Req/s | TTFT mean / p99 (ms) | TPOT mean (ms) | E2E latency mean / p99 (ms) |
|---|---|---|---|---|---|---|
| financial-lora | 711.5 | 3547.3 | 2.78 | 162 / 348 | 10.65 | 2877 / 3001 |
| qwen2.5-1.5b-instruct | 711.3 | 3546.4 | 2.78 | 146 / 348 | 10.71 | 2878 / 3033 |
| qwen2.5-7b-instruct | 194.6 | 970.4 | 0.76 | 485 / 1461 | 39.34 | 10517 / 10982 |

financial-lora and its base serve identically (same architecture; the LoRA
is merged). The 7B runs at about 27% of the 1.5B's output throughput, and
its mean end-to-end latency per 256-token request is about 3.7× higher, on
the same GPU and batch limit. These are dated measurements on k3s. The
OKE serving benchmark in numbers-of-record stays "to be measured in Phase 2".
These runs warmed up on their own timed prompts, so the first 16 of each
were already in vLLM's prefix cache. A clean rerun of financial-lora on
2026-09-28 gave 708.3 output tok/s (0.5% lower) and a mean TTFT of 198 ms
instead of 162: the throughput figures stand, the TTFT is understated. See
"CPU inference benchmark", dated finding.

### Observations

- **No run saw byte-identical source data.** Across the four runs the
  retrieved context differs for all 40 tickers. News is fetched live
  (differs for 40/40), and the RAG fields are an LLM-written answer over
  the retrieved chunks, whose wording varies run to run (differs for the
  35 tickers that have SEC context; the five ADRs had none in every run).
  Stock data differed for 2 tickers. This noise hits every arm alike, as
  in earlier A/Bs; it is not a per-arm confound, but the arms are not
  paired on identical inputs.
- **Hosted ran lower than on 2026-09-05.** `kcf7s` 1.04% (0.4–2.7%) vs
  `j4cnp` 3.06% (1.8–5.3%), p = 0.074: within run-to-run variance at
  this N. The 2026-09-24 rerun of the hosted arm on the same image and settings,
  `dvvxk`, gave 7/389 = 1.80% (0.9–3.7%): p = 0.55 vs `kcf7s` and 0.35
  vs `j4cnp` (`eval/multi_arm_stats.py`; artifacts `eval/runs/dvvxk-*`,
  `eval/runs/raw/dvvxk-findings/`). The Sep 23 image's two hosted runs
  are `kcf7s` and `dvvxk`. financial-lora `v924f` 6.49% vs `lsnnc` 8.15% (5.8–11.4%),
  p = 0.40, also consistent.
- Free-form verdicts without a CLAIM line are carried with `claim=null`:
  `v924f` AFRM and VERV SUPPORTED, LCID and TM UNSUPPORTED; `4nfsm` GOOGL
  and PTON UNSUPPORTED.
- `v924f` and `4nfsm` show workflow phase Failed: that is the gate
  failing (aggregate exit 1), not an infrastructure failure. All four
  runs completed 40/40 tickers with no skips.

Artifacts: findings `eval/runs/raw/{kcf7s,v924f,4nfsm,cnkp2}-findings/`
(the hostPath copies, byte-identical to each aggregate pod's findings
dump), aggregates `eval/runs/<run>-aggregate.txt`, per-claim rows
`eval/runs/<run>-claims.jsonl` (`eval/parse_run_log.py`, no count
mismatches against the pod logs), contexts `eval/runs/<run>-contexts/`.
Stats: `python eval/multi_arm_stats.py --run hosted eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings --run financial-lora eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings --run qwen1.5b-base eval/runs/4nfsm-claims.jsonl eval/runs/raw/4nfsm-findings --run qwen7b-base eval/runs/cnkp2-claims.jsonl eval/runs/raw/cnkp2-findings`;
the `dvvxk` and pooled-hosted comparisons add
`--run hosted-rerun eval/runs/dvvxk-claims.jsonl eval/runs/raw/dvvxk-findings --pool hosted-pooled hosted hosted-rerun`.

### Dated finding: hosted-arm rate fell between images (2026-09-25)

**What moved.** The hosted arm's unsupported rate is lower on the
2026-09-23 image than on the 2026-09-05 image, two runs each, same 40
tickers, judge v2:

| Image (inferred build commit) | Runs | Unsupported (Wilson 95% CI) |
|---|---|---|
| 2026-09-05 (d88af26) | `9j2dj`, `j4cnp` | 24/778 = 3.08% (2.1–4.5%) |
| 2026-09-23 (c309627) | `kcf7s`, `dvvxk` | 11/772 = 1.42% (0.8–2.5%) |

Fisher exact, two-sided: **p = 0.039**. Counts are per-claim deduped, the
rule the Sep 23 runs were scored with; `9j2dj`'s own DAG aggregate
counted 387 claims because the judge repeated one JPM SUPPORTED label
(24/779, same p).

**What did not change.** Neither image records its build commit; they
are inferred from commit and image timestamps (d88af26 carries the MSFT
reindex fix `j4cnp` ran after; c309627 was committed three minutes
before the Sep 23 image was built). The diff d88af26..c309627 has no
change on the hosted generation, judge or retrieval path: `agent/core.py`,
`agent/grounding.py` (judge prompt v2, Sonnet, temperature 0),
`agent/tools/` apart from `local_model.py` (used only by the local
arm), the model IDs, the hosted temperatures, `requirements.txt`,
`Dockerfile.k8s`, and the Argo and k8s eval config are all unchanged.
The one hosted-path code change is per-claim dedupe counting (4bc4e35),
and it changes no count: raw and deduped counts are identical for
`j4cnp`, `kcf7s` and `dvvxk` (it differs only on `9j2dj`, by the one JPM
label above).

**Did the inputs drift?** The working hypothesis after the diff was
live-input drift (NewsAPI, yfinance, RAG wording) plus run-to-run
variance. Comparing the retrieved source context block by block for the
same 40 tickers, across images and, as a reference, within the Sep 23
image:

| Block | `j4cnp` vs `kcf7s` (across images) | `kcf7s` vs `dvvxk` (same image) |
|---|---|---|
| Stock data | 2/40 identical | 3/40 identical |
| News articles | 29/40 identical | 36/40 identical |
| SEC filing summaries | 39/40 identical | 38/40 identical |
| RAG SEC highlights | 5/40 identical | 6/40 identical |
| RAG risk factors | 6/40 identical | 5/40 identical |

- SEC filing inputs did not drift. The filing forms and dates match for
  39/40 tickers against both Sep 23 runs; the exceptions are RDFN, whose
  EDGAR fetch came back empty in `kcf7s`, and SFIX, whose new 10-K (filed
  2026-09-24) `dvvxk` picked up. RAG answers are available for the same
  35 tickers in every run.
- The RAG answer text differs as much between two runs of one image as
  between images, so its wording is run-to-run variation, not drift.
- News differs across images for 11 tickers beyond the within-image
  level; stock data differs almost everywhere in both comparisons.

So the context check **does not support input drift as the main cause**:
apart from news on 11 tickers, the cross-image input differences are the
size of ordinary run-to-run differences. The cause is **unconfirmed**.
What remains: run-to-run variance (this is one test at p = 0.039), the
news change on those 11 tickers, and model behaviour on the provider's
side behind unchanged model IDs, which the repository cannot show.

Split by that news change (2026-09-27, `eval/compare_runs.py pooled --news-split eval/runs/raw/j4cnp-findings eval/runs/raw/kcf7s-findings`): the 11 news-changed tickers went from 8/218 = 3.67% to 1/224 = 0.45% (p = 0.019), the other 29 from 16/560 = 2.86% to 10/548 = 1.82% (p = 0.32), so the drop concentrates where the news changed; this is a post hoc split of mostly large-cap names, suggestive rather than confirmation.

**What it changes.** Nothing of record. The grounding number of record
stays `j4cnp` 12/392 = 3.06%, and the calibration of record still
reweights to `j4cnp`'s population (354 S / 12 U / 26 I). The hosted
baseline to compare against is dated: quote the image with the rate.

Reproduce (reads committed artifacts only):

```
python eval/compare_runs.py pooled \
    --group sep5  eval/runs/9j2dj-claims.jsonl eval/runs/j4cnp-claims.jsonl \
    --group sep23 eval/runs/kcf7s-claims.jsonl eval/runs/dvvxk-claims.jsonl
python eval/compare_runs.py counts --run j4cnp eval/runs/raw/j4cnp-findings \
    --run kcf7s eval/runs/raw/kcf7s-findings --run dvvxk eval/runs/raw/dvvxk-findings \
    --run 9j2dj eval/runs/raw/9j2dj-findings
python eval/compare_runs.py contexts --a j4cnp eval/runs/raw/j4cnp-findings \
    --b kcf7s eval/runs/raw/kcf7s-findings
python eval/compare_runs.py contexts --a kcf7s eval/runs/raw/kcf7s-findings \
    --b dvvxk eval/runs/raw/dvvxk-findings
```

### Held-out validation sample for this set

`eval/build_fourarm_holdout.py` (seed 20260923) drew 78 claims stratified
by arm × judge verdict: 6 UNSUPPORTED / 6 INFERENCE / 8 SUPPORTED per arm
(hosted has only 4 UNSUPPORTED, all taken), at most 3 claims per
(arm, ticker). Population: 1,555 claims with a CLAIM line; 6 overlapping
the dev or v2 held-out sets excluded. Allocation is equal, not
proportional; stratum population and sample sizes are in
`eval/judge_validation/fourarm_holdout_method.json` for reweighting. The
labeling CSV is blind (no run, arm, or verdict); the key is separate.
**Reserved for judge validation on this claim set only.** Not yet
labeled.

## CPU inference benchmark (2026-09-28): a dated measurement

One data point: the same weights and the same benchmark client and shape,
served from the node's Xeon and from its A10. This is a measurement, not
optimization work; nothing was tuned for the CPU.

**Setup.**

- **Node** `vm-a10-inst-2`, a VM.GPU.A10.1: a KVM guest with 15 cores (30
  vCPUs) of an Intel Xeon Platinum 8358 @ 2.60GHz, one socket, one NUMA
  node, 235 GiB of memory, and one A10. The CPU flags include AVX-512 (F,
  BW, VL, DQ, VNNI) but not AVX512_BF16 or AMX.
- **CPU server:** vLLM's official CPU image
  `public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2`, the vLLM version
  the GPU deployment runs, in plain Docker on the host outside k3s, with
  the GPU deployment's serving args (`--dtype bfloat16 --max-model-len 4096
  --max-num-seqs 8`), prefix caching at its default (on) and an 8 GB KV
  cache. Pinned to 14 of the 15 physical cores (`--cpuset-cpus 2-29`, 28
  vCPUs) with one OMP thread per physical core, 64 GB memory limit.
  `scripts/vm_bench_cpu.sh`.
- **A10:** the running k3s deployment (`vllm/vllm-openai:v0.10.2`, same
  args), benchmarked from inside the pod by `scripts/vm_bench_serve.sh`.
- **Precision:** BF16 on both. The fine-tune's weights are stored as FP16
  and cast to BF16 at load, on both backends.
- **Client:** `vllm bench serve` v0.10.2 on both: random dataset, 1024
  input / 256 output tokens with `--ignore-eos`, request rate inf,
  `/v1/completions`, the fine-tune's tokenizer. For the CPU it ran in a
  separate container pinned to core 0 (vCPUs 0-1). Concurrency 8 with 200
  prompts (seed 1) and concurrency 1 with 50 prompts (seed 2), on each
  backend, each after an untimed 16-prompt warmup on seed 1000. The prompts
  are identical across backends: each pair of files has the same total
  input tokens (204,537 and 50,992).
- **Quiet node:** api, worker, streamlit and mcp were scaled to 0 for the
  runs and restored after. Postgres, Redis, Argo and the GPU vLLM pod
  stayed up and idle. Sampled every 30 s through the CPU runs, the GPU pod
  used 5-19 millicores (median 13) and the CPU server container a median
  1389% (its 14 OMP threads). Logs: `load-*.log` beside the results.
- **Models:** financial-lora (the merged fine-tune) on both, and the
  untuned Qwen2.5-1.5B-Instruct on the CPU. The 7B was not run: the
  fine-tune's CPU output throughput at concurrency 8, 22.9 tok/s, is under
  the ~30 tok/s set as the bar for trying it.

Raw results: `eval/runs/bench/a10-2026-09-28/` and
`eval/runs/bench/cpu-2026-09-28/`. Steps to reproduce: deploy-runbook,
"CPU inference benchmark". The table and the per-brief line below are
produced by:

```bash
A=eval/runs/bench/a10-2026-09-28; D=eval/runs/bench/cpu-2026-09-28
python scripts/bench_table.py \
  "$A/financial-lora-c8.json=A10, financial-lora" "$A/financial-lora-c1.json=A10, financial-lora" \
  "$D/financial-lora-c8.json=CPU, financial-lora" "$D/financial-lora-c1.json=CPU, financial-lora" \
  "$D/qwen2.5-1.5b-instruct-c8.json=CPU, qwen2.5-1.5b-instruct" \
  "$D/qwen2.5-1.5b-instruct-c1.json=CPU, qwen2.5-1.5b-instruct" \
  --section-tokens 530 --section-tokens 398 --section-tokens 1024
```

| Run | Device | Backend | dtype | Pinned cores | Concurrency | Prompts | Output tok/s | Total tok/s | Req/s | TTFT mean / median / p99 ms | TPOT mean / median / p99 ms | E2E mean / median / p99 ms | Prefix-cache hits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A10, financial-lora | NVIDIA A10 | vllm 0.10.2 | bfloat16 | n/a | 8 | 200 | 708.3 | 3538.1 | 2.767 | 198 / 197 / 354 | 10.6 / 10.5 / 11.1 | 2890 / 2892 / 3038 | 1.0% |
| A10, financial-lora | NVIDIA A10 | vllm 0.10.2 | bfloat16 | n/a | 1 | 50 | 111.1 | 553.5 | 0.434 | 52 / 52 / 55 | 8.8 / 8.8 / 8.9 | 2305 / 2306 / 2315 | 1.9% |
| CPU, financial-lora | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | vllm-cpu 0.10.2 | bfloat16 | 14 | 8 | 200 | 22.9 | 114.2 | 0.089 | 13819 / 12325 / 41866 | 297.1 / 304.4 / 328.3 | 89584 / 89949 / 102255 | 0.4% |
| CPU, financial-lora | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | vllm-cpu 0.10.2 | bfloat16 | 14 | 1 | 50 | 15.0 | 74.8 | 0.059 | 5985 / 6110 / 6128 | 43.4 / 43.4 / 44.1 | 17061 / 17166 / 17364 | 1.7% |
| CPU, qwen2.5-1.5b-instruct | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | vllm-cpu 0.10.2 | bfloat16 | 14 | 8 | 200 | 22.9 | 114.2 | 0.089 | 13820 / 12326 / 41879 | 297.0 / 304.2 / 328.0 | 89562 / 89891 / 102235 | 0.4% |
| CPU, qwen2.5-1.5b-instruct | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | vllm-cpu 0.10.2 | bfloat16 | 14 | 1 | 50 | 15.1 | 75.2 | 0.059 | 5985 / 6110 / 6131 | 43.0 / 43.0 / 43.6 | 16961 / 17077 / 17242 | 1.7% |

- **A10 vs CPU, financial-lora.** At concurrency 8 the A10 produced 708.3
  output tok/s and the CPU 22.9, about 31 times as many. At concurrency 1,
  111.1 vs 15.0, about 7 times. The gap is widest in prefill: mean TTFT for
  a 1024-token prompt at concurrency 1 was 52 ms on the A10 and 5985 ms on
  the CPU. Decode is closer: TPOT 8.8 vs 43.4 ms.
- **Batching adds little on this CPU.** From concurrency 1 to 8, CPU output
  throughput rose from 15.0 to 22.9 tok/s while mean TPOT rose from 43 to
  297 ms. On the A10 it rose from 111.1 to 708.3.
- **The fine-tune and its base serve identically on the CPU**, as on the
  A10 (same architecture, LoRA merged).

**Per brief.** A serial estimate of the time to write one brief's two
locally served sections at concurrency 1: 2 × mean TTFT + T × mean TPOT,
with T the Financial Health + Risk Factors output tokens per brief from
[model-recommendation.md](model-recommendation.md), section 4 (fine-tune
mean 530, 1.5B base 398, cap 1024). Fine-tune: A10 4.8 s, CPU 35.0 s (9.2 s
and 56.4 s at the cap). 1.5B base on the CPU: 29.1 s. The fine-tune arm's
mean brief time with A10 serving was 34.1 s (`v924f`). On the A10 the two
sections are short next to the brief; on this CPU they alone take about as
long as a whole brief. It is an estimate: TTFT was measured at 1024 input
tokens, not on the real section prompts, and the pipeline sends the two
sections in parallel rather than one after the other. Brief time with CPU
serving was not measured.

**Caveats.**

- One node, one VM shape, measured once, on a shared-tenancy KVM guest.
- No AMX or AVX512_BF16 on this Ice Lake Xeon: vLLM runs BF16 through
  AVX-512 conversions. Newer Xeons with AMX would likely differ; not
  measured. Only this Intel Xeon was measured; nothing here speaks for AMD
  or Arm CPUs.
- Not tuned: the GPU deployment's args and vLLM's CPU defaults, 14 cores,
  no quantization, no thread or KV-cache sweeps, no other CPU server. The
  two backends differ in more than hardware: they run different attention
  and matmul kernels (the CPU server logs Torch SDPA attention).
- No quality eval. Same weights and dtype on both, so output quality was
  not re-measured, and numerical differences between the backends' kernels
  were not checked. The four-arm grounding rates were measured with A10
  serving only.
- Synthetic shape (random tokens, 1024 in / 256 out), as in the A10
  benchmark. Concurrency 1 used 50 prompts on both backends, 200 at
  concurrency 8.
- Core 0 was shared by the benchmark client, k3s and the idle pods.

### Dated finding: warmup prompts were cached in the first pass (2026-09-28)

The first CPU pass, and the A10 files of 2026-09-23, warmed up on the timed
seed. With `vllm bench serve`, seed 0 gives the same first N prompts at any
prompt count, so the 16 warmup prompts were the first 16 timed prompts,
and with prefix caching on (the vLLM default on both backends) those
skipped most of their prefill. The first CPU pass also ran concurrency 1
after concurrency 8 on the same server, so all 50 of its prompts had been
served before. Checked with the client's own dataset code
(`RandomDataset`, seed 0: the 16 warmup prompts are the first 16 of 200,
and the first 50 of 200 are the 50-prompt set). Both scripts now warm up
on a separate seed and record the timed run's prefix-cache hit share; the
clean runs above show 0.4-1.9%, which fits the client's initial test
request re-sending the first prompt.

| Run, financial-lora | First pass: output tok/s, mean TTFT | Clean: output tok/s, mean TTFT |
|---|---|---|
| A10, concurrency 8 | 711.5, 162 ms (2026-09-23) | 708.3, 198 ms |
| A10, concurrency 1 | 113.2, 19 ms | 111.1, 52 ms |
| CPU, concurrency 8 | 23.7, 13195 ms | 22.9, 13819 ms |
| CPU, concurrency 1 | 20.8, 1025 ms | 15.0, 5985 ms |

The cache mostly distorted TTFT, and throughput where prefill dominates
(the CPU at concurrency 1). On the A10 at concurrency 8, throughput moved
by 0.5%, so the 2026-09-23 A10 throughput figures, and the cost estimate
built on them, stand; their TTFT is understated. First-pass files, run
through `scripts/bench_table.py` for the figures above:
`eval/runs/bench/cpu-2026-09-28/first-pass/` (the 2026-09-23 A10 file is
`eval/runs/bench/financial-lora.json`).

## Quantization benchmark (2026-09-29, a dated measurement)

What quantizing the fine-tune does to serving speed on the node's A10
and Xeon, and to grounding quality with A10 serving. Same node as the CPU
benchmark above (`vm-a10-inst-2`), same benchmark client and shape.
Nothing here is a number of record. GGUF quantization quality was not
evaluated; only the W4A16 arm ran through the grounding eval.

**Engine vs precision.** On the A10 only the precision changes: BF16 and
W4A16 both run on vLLM v0.10.2 with the committed serving args. On the
CPU, 4-bit runs on a different engine (llama.cpp), so the CPU results are
two separate effects. vLLM BF16 vs llama.cpp F16 is the engine effect:
the same weights at 16 bits on both (stored FP16; vLLM casts them to
BF16, llama.cpp keeps F16, so the 16-bit formats also differ). llama.cpp
F16 vs Q8_0 vs Q4_K_M is the precision effect, on one engine. vLLM BF16
vs llama.cpp Q4_K_M mixes the two and is not a quantization speedup.

**Quantized weights (A10).** GPTQ W4A16 with llm-compressor 0.7.1
`oneshot`: int4 weights, symmetric, group size 128, activations 16-bit,
every Linear layer except `lm_head`. The output is a compressed-tensors
checkpoint (compressed-tensors 0.11.0, the version vLLM v0.10.2 pins).
`scripts/quantize_w4a16.py`, run in a throwaway venv on the node's A10
(256 s). Its record, `quant_meta.json`, is committed beside the results.

- **Calibration set:** `data/sections_dataset.jsonl`, the fine-tune's own
  training pairs (78 Financial Health, 26 Risk Factors). All 104 rows were
  used, in a seed-42 order, each rendered with the chat template over the
  user and assistant turns: 69,986 tokens, none truncated at 2048. The
  file has 104 rows, so the planned 256 samples were not possible, and the
  script refuses to fill the gap with repeats.
- **Size:** 1.61 GB on disk, against 3.09 GB for the FP16 checkpoint.
  llm-compressor saved the tied embedding untied: `lm_head` is a separate
  FP16 tensor, byte-identical to `embed_tokens`, which is byte-identical
  to the source's. So 0.93 GB of the 1.61 GB is the FP16 embedding twice
  over. The untying changes the size on disk, not the weights.
- **Serving:** `make vm-vllm MODEL_DIR=qwen-ft-w4a16
  SERVED_NAME=financial-lora-w4a16 MAX_LEN=4096` needed no code or
  manifest change and no `--quantization` flag, since vLLM reads the
  scheme from the weights' `config.json`. The pod logged
  `Using MarlinLinearKernel for CompressedTensorsWNA16`, and 18.07 GiB of
  KV cache against the BF16 deployment's 16.72 GiB.

### A10: BF16 vs W4A16

`scripts/vm_bench_serve.sh` against the k3s pod, the 2026-09-28 A10 shape
and seeds: concurrency 8 × 200 prompts (seed 1) and concurrency 1 × 50
(seed 2), each after a 16-prompt warmup on seed 1000, with api, worker,
streamlit and mcp scaled to 0; the W4A16 pod was fresh. The prompts are identical to
the 2026-09-28 BF16 files (same total input tokens: 204,537 and 50,992).
BF16 is the 2026-09-28 run from the CPU benchmark above, on the same node
and pod spec.

```bash
python scripts/bench_table.py --matrix eval/runs/bench/a10-2026-09-28 \
  eval/runs/bench/a10-quant-2026-09-29 \
  --weights-bytes eval/runs/bench/a10-2026-09-28=3087466808
```

| Engine | Precision | Device | Output tok/s (c=8) | Mean E2E s (c=1) | TTFT p50 ms (c=1) | Weights on disk (GB) |
|---|---|---|---|---|---|---|
| vllm 0.10.2 | bfloat16 | NVIDIA A10 | 708.3 | 2.3 | 52 | 3.09 |
| vllm 0.10.2 | w4a16-g128 | NVIDIA A10 | 1075.7 | 1.3 | 58 | 1.61 |

(The BF16 files predate the `weights_bytes` metadata; 3,087,466,808 bytes
is `qwen-ft/model.safetensors` on the node.) The full per-run table
(`python scripts/bench_table.py` over the same four files) adds:

- **Decode is faster.** Median TPOT at concurrency 1 was 5.0 ms against
  8.8 ms (1.72× the output tok/s: 190.9 vs 111.1), and 6.4 against
  10.5 ms at concurrency 8 (1.52×: 1075.7 vs 708.3).
- **Prefill is not.** Median TTFT rose at both concurrencies: 58 vs 52 ms
  at concurrency 1, 286 vs 197 ms at concurrency 8.
- **Prefix cache:** 0.5% and 1.9% of prompt tokens hit, about the
  client's initial test request re-sending the first prompt.

Raw results: `eval/runs/bench/a10-quant-2026-09-29/` (the JSON `date`
field is the pod's local time, UTC−7; the runs were 05:00-05:02 UTC).

### Grounding: W4A16 vs the BF16 fine-tune

`grounding-eval-extended-local-w4a16-r5nzh`, 2026-09-29 05:03-05:27 UTC,
submitted from `argo/eval-run-extended-local-w4a16.yaml` (the local-arm
file with a different name prefix; a test holds the two equal otherwise)
while vLLM served `qwen-ft-w4a16` as `financial-lora-w4a16`. Arm
`local-model`, judge v2, the 40 extended tickers, 40/40 completed with no
skips. Same node, WorkflowTemplate, pinned local sampling (the aggregate
header prints it) and app image as the four-arm set: the image built
2026-09-23 22:13 UTC, not rebuilt since. The comparison of interest is
W4A16 vs the BF16 fine-tune `v924f`, and that is the only claim this run
supports.

| Arm (writes FH + RF) | Workflow | Claims | Sup/Uns/Inf | Unsupported, judge-flagged (Wilson 95% CI) | Gate (≤5%) |
|---|---|---|---|---|---|
| financial-lora, BF16 (2026-09-23) | grounding-eval-extended-local-v924f | 385 | 346/25/14 | 6.49% (4.4–9.4%) | FAILED |
| financial-lora, GPTQ W4A16 (2026-09-29) | grounding-eval-extended-local-w4a16-r5nzh | 344 | 308/23/13 | 6.69% (4.5–9.8%) | FAILED |

Exact two-sided Fisher, W4A16 vs BF16: all claims 23/344 vs 25/385,
**p = 1.00**. Financial Health + Risk Factors (the sections the model
writes; attributed claims): 15/96 = 15.62% (9.7–24.2%) vs 15/112 =
13.39% (8.3–20.9%), p = 0.70. All other claims: 8/248 vs 10/273,
p = 0.82.

- **No detectable difference at this sample size.** That is not
  equivalence: each arm's interval spans about five points, so a
  difference of a few points would not show at this size.
- **Scope: the judge's audited sections only.** The judge audits the
  claims in the Executive Summary and Outlook. The Financial Health + Risk
  Factors figures above are those audited claims attributed back to the
  section they restate, not an audit of the Financial Health or Risk
  Factors text itself. So "no detectable difference" covers grounding of
  the Exec Summary + Outlook only. Section-level numeric accuracy (the
  stock-data figures every section states) is covered by the
  deterministic numeric check (`agent/numeric_check.py`, backtest
  `scripts/numeric_backtest.py`). Its flags were adjudicated on
  2026-10-01; the numeric W4A16 vs BF16 result is in
  ["Numeric check: adjudicated flags and the W4A16 replication"](#numeric-check-adjudicated-flags-and-the-w4a16-replication-2026-10-01-dated).
- **Hosted, for reference, not a new claim.** The W4A16 arm trails the
  hosted runs as the BF16 fine-tune does: p = 4.6e-05 vs `kcf7s`, 0.0011
  vs `dvvxk`, 1.1e-05 vs both pooled (11/772).
- **Six days apart.** `v924f` ran 2026-09-23, `r5nzh` 2026-09-29, on the
  same image and node. The hosted arm on this image moved from 1.04% to
  1.80% between two days (p = 0.55), so run-to-run variation of that size
  is expected.
- **Fewer checkable claims.** The quantized arm produced 344 judged
  claims against the BF16 arm's 385, and 69 against 85 restated
  Financial Health. Claim counts come from the synthesis, so the rates
  sit on different denominators and the per-section buckets differ in
  size across arms.
- Five free-form verdicts carry `claim=null` (AMZN, MSFT and NVDA
  UNSUPPORTED, OMER INFERENCE, VERV SUPPORTED); they count in the totals
  and land in "unattributed". The aggregate's estimated run cost was
  $2.40.
- Judge-flagged rates (judge v2; calibration of record: precision 60%
  (9/15, CI 35.7–80.2%), population-weighted recall 32.5% on the baseline
  run (CI 16.0–52.4%)). No reweighted estimate: the calibration miss
  rates were measured on `j4cnp`/`lsnnc` claims and are not extended to
  other models. The comparison holds in direction because both arms share
  the judge.

Stats (every pair, the pooled hosted test and the per-section breakdown):

```bash
python eval/multi_arm_stats.py \
  --run hosted eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings \
  --run financial-lora eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings \
  --run lora-w4a16 eval/runs/r5nzh-claims.jsonl eval/runs/raw/r5nzh-findings \
  --run qwen1.5b-base eval/runs/4nfsm-claims.jsonl eval/runs/raw/4nfsm-findings \
  --run qwen7b-base eval/runs/cnkp2-claims.jsonl eval/runs/raw/cnkp2-findings \
  --run hosted-rerun eval/runs/dvvxk-claims.jsonl eval/runs/raw/dvvxk-findings \
  --pool hosted-pooled hosted hosted-rerun
```

Artifacts: aggregate `eval/runs/r5nzh-aggregate.txt`, findings
`eval/runs/raw/r5nzh-findings/` (the hostPath copy, identical to the pods'
dumps), rows `eval/runs/r5nzh-claims.jsonl` (`eval/parse_run_log.py`, no
count mismatches), contexts `eval/runs/r5nzh-contexts/`.
`tests/test_multi_arm_stats.py` holds the committed rows to 23/344 and
p = 1.00.

### CPU: engine and precision (llama.cpp GGUF)

vLLM's CPU backend is not the engine for 4-bit on this Xeon, so the
precision ladder ran on llama.cpp's `llama-server`: the official CPU image
at build b11223, pinned by digest, in plain Docker outside k3s.
`scripts/vm_bench_cpu_gguf.sh`.

- **Weights:** `convert_hf_to_gguf.py --outtype f16` on the merged
  fine-tune (pre-tokenizer recognized as `qwen2`), then `llama-quantize`
  from that F16 file to Q8_0 and Q4_K_M, without an importance matrix.
  Sizes 3.09, 1.65 and 0.99 GB; images, hashes and build in
  `gguf_meta.json` beside the results.
- **Server:** the vLLM CPU run's pinning (cpuset 2-29, 14 threads, one per
  physical core, strict placement), port and memory limit; `--parallel 8`
  with 1536 tokens of context per slot (1024 in + 256 out, with margin);
  llama-server's defaults otherwise, prompt caching included.
- **Client and prompts:** the vLLM CPU run's `vllm bench serve`
  invocation, seeds and warmup, from the same client image and core. The
  prompts match the 2026-09-28 vLLM BF16 CPU files (total input tokens
  204,537 and 50,992), except one run that lost a request (below).
- **Quiet node:** api, worker, streamlit and mcp scaled to 0, the GPU pod
  idle on the BF16 fine-tune (5-17 millicores); the server container ran
  at a median of about 1397% (its 14 threads). Load logs beside the
  results, from `scripts/vm_load_sampler.sh`.

```bash
python scripts/bench_table.py --matrix eval/runs/bench/a10-2026-09-28 \
  eval/runs/bench/a10-quant-2026-09-29 \
  eval/runs/bench/cpu-2026-09-28/financial-lora-c8.json \
  eval/runs/bench/cpu-2026-09-28/financial-lora-c1.json \
  eval/runs/bench/cpu-gguf-2026-09-29 \
  --weights-bytes eval/runs/bench/a10-2026-09-28=3087466808 \
  --weights-bytes eval/runs/bench/cpu-2026-09-28=3087466808
```

| Engine | Precision | Device | Output tok/s (c=8) | Mean E2E s (c=1) | TTFT p50 ms (c=1) | Weights on disk (GB) |
|---|---|---|---|---|---|---|
| vllm 0.10.2 | bfloat16 | NVIDIA A10 | 708.3 | 2.3 | 52 | 3.09 |
| vllm 0.10.2 | w4a16-g128 | NVIDIA A10 | 1075.7 | 1.3 | 58 | 1.61 |
| vllm-cpu 0.10.2 | bfloat16 | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | 22.9 | 17.1 | 6110 | 3.09 |
| llama.cpp b11223 | F16 | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | 52.3 | 11.5 | 2582 | 3.09 |
| llama.cpp b11223 | Q4_K_M | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | 64.5 | 6.8 | 2018 | 0.99 |
| llama.cpp b11223 | Q8_0 | Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz | 51.7 | 9.4 | 2680 | 1.65 |

(The vLLM BF16 rows are the 2026-09-28 files; the full per-run table is
`python scripts/bench_table.py eval/runs/bench/cpu-gguf-2026-09-29`.)

- **Engine effect (vLLM BF16 vs llama.cpp F16, both 16-bit):** output
  throughput at concurrency 8 went from 22.9 to 52.3 tok/s. At
  concurrency 1, median TTFT for a 1024-token prompt went from 6110 to
  2582 ms, and median TPOT from 43.4 to 35.3 ms. Of the 5.5 s difference
  in mean E2E at concurrency 1 (17.1 vs 11.5 s), 3.5 s is prompt
  processing (mean TTFT 5985 vs 2523 ms).
- **Precision effect (llama.cpp F16 → Q8_0 → Q4_K_M):** at concurrency 1,
  median TPOT fell from 35.3 to 26.7 to 19.0 ms (22.2, 27.1 and 37.5
  output tok/s), and mean E2E from 11.5 to 9.4 to 6.8 s. At concurrency 8,
  Q8_0 gained nothing over F16 (51.7 vs 52.3 tok/s) and Q4_K_M reached
  64.5. Prefill barely moved (median TTFT at concurrency 1: 2582, 2680,
  2018 ms).
- **Per brief** (the serial estimate above, 2 × mean TTFT + T × mean
  TPOT, T = 530 tokens for the fine-tune): F16 23.8 s, Q8_0 19.4 s, Q4_K_M
  14.0 s on this CPU, against vLLM BF16 35.0 s on the CPU and 4.8 s on the
  A10 (41.2, 32.6 and 23.4 s at the 1024-token cap).
- GGUF quantization quality was not evaluated; only the W4A16 arm ran
  through the grounding eval. Q4_K_M without an importance matrix is a
  lossier build than W4A16 with GPTQ; nothing here says how it would
  score.

Raw results: `eval/runs/bench/cpu-gguf-2026-09-29/`.

### CPU sweep: concurrency × threads

vLLM BF16 on the CPU (`scripts/vm_bench_cpu.sh sweep`): concurrency 1, 2,
4, 8 and 16 at 7 and 14 OMP threads, one per physical core from core 1
(vCPUs 2,4,...,14 or 2,4,...,28; the cpuset stays 2-29). One fresh server
per thread count with `--max-num-seqs 16`, the only serving arg the sweep
changes, so concurrency 16 is admitted. Each cell is its own timed run
with its own seed (threads × 100 + concurrency) and max(32, 8 ×
concurrency) prompts, after the usual warmup; quiet node as above. Cells
hold 32-128 prompts, fewer than the 200/50 of the main runs.

```bash
python scripts/bench_table.py --sweep eval/runs/bench/cpu-sweep-2026-09-29
```

Output tok/s / median TTFT ms / median TPOT ms:

| Concurrency | 7 threads | 14 threads |
|---|---|---|
| 1 | 9.9 / 11776 / 56.4 | 14.9 / 6124 / 44.0 |
| 2 | 10.8 / 12699 / 100.7 | 17.3 / 6672 / 72.4 |
| 4 | 12.2 / 23646 / 241.5 | 19.5 / 12277 / 160.2 |
| 8 | 13.1 / 35029 / 477.8 | 23.0 / 15505 / 281.0 |
| 16 | 12.1 / 46670 / 1126.1 | 25.4 / 23848 / 539.4 |

- **Threads.** Doubling from 7 to 14 threads raised output throughput by
  1.5× at concurrency 1 (9.9 to 14.9 tok/s) and 2.1× at concurrency 16
  (12.1 to 25.4), and roughly halved median TTFT at every concurrency.
- **Concurrency.** At 7 threads throughput peaked at concurrency 8 (13.1)
  and fell at 16 (12.1). At 14 threads it was still rising at 16 (25.4,
  against 23.0 at 8), so this sweep does not show where it saturates.
  Batching costs latency: median TTFT at 14 threads went from 6.1 s at
  concurrency 1 to 23.8 s at 16.
- **Consistent with the main runs.** The 14-thread cells at concurrency 1
  and 8 (14.9 and 23.0 tok/s) match the 2026-09-28 files (15.0 and 22.9)
  within 1%, on different seeds and a different `--max-num-seqs`.
- **llama.cpp Q4_K_M sweep: concurrency 1 only.** 37.9 tok/s, median
  TTFT 1987 ms, median TPOT 18.9 ms at 14 threads, in line with the main
  Q4_K_M run (37.5 tok/s). The concurrency-2 cell lost 4 of 32 requests to
  the keep-alive close below (12.5%, over the limit), so it was refused and the
  rest of that sweep did not run. It was not retried: retrying until a
  run passes would select runs by luck. No llama.cpp concurrency or
  thread scaling was measured.

Raw results: `eval/runs/bench/cpu-sweep-2026-09-29/` (load logs beside
them).

### Method notes (llama.cpp)

- **Output tokens are counted on the server.** `vllm bench serve` v0.10.2
  reads a response's usage only from a stream chunk without choices;
  llama-server sends usage with the last (empty) choice, so the client
  counts output tokens by re-tokenizing the generated text, which ran
  0.5-4.5% low here (50,733 of 51,200 for F16 at concurrency 8, 12,222 of
  12,800 at concurrency 1).
  With `--ignore-eos`, llama-server bans end-of-generation tokens, so
  every completed request generates exactly 256.
  `scripts/bench_fix_llamacpp.py` refuses a run unless the server's own
  `llamacpp:tokens_predicted` counter equals 256 × (completed + 1) (the +1
  is the client's test request), then recomputes output throughput and
  TPOT with the client's formulas at 256. The client's own figures stay
  in each JSON under `client_retokenized`. TTFT and E2E do not depend on
  the count.
- **Lost requests (keep-alive).** llama-server answers with
  `Keep-Alive: timeout=5, max=100` but closes the connection itself, its
  FIN in the same packet as the stream's final `data: [DONE]` chunk
  (every one of 217 served connections in a packet capture). The client
  pools the connection as reusable; a request that picks it up before the
  FIN is read goes to a closing socket and fails with
  `ServerDisconnectedError` before any response header, never reaching the
  server. The client does not retry. It lost 0-1 of 200 requests per F16
  concurrency-8 run and 3 of 200 in one Q8_0 run. Turning off
  llama-server's SSE keep-alive pings was tried and did not stop it (the
  next run lost one), so the committed server keeps its default. A lost
  request frees its concurrency slot at once, so the server's load is
  unchanged. A run is accepted with losses only if every error is this
  one, the server's token count proves the lost requests generated
  nothing, and at most 1% of prompts are lost (at least one allowed); the
  indices are recorded in `lost_requests`, and the table prints the run
  as "199 of 200". A 5% limit was considered after the cause was measured
  and not adopted, because no result needed it: every committed run
  passes at 1%, the Q8_0 run with 3 losses was refused and rerun (0
  lost), and the sweep cell below fails either way. One committed run has
  a loss: Q4_K_M at concurrency 8, request 8, 199 of 200.
- **Refused and diagnostic runs are not kept.** Three F16 concurrency-8
  runs were refused (one lost request each; the first also under the
  uncorrected count, the third with pings off) and one Q8_0
  concurrency-8 run (3 lost). Two diagnostic runs passed but are not
  results: F16 with pings off (0 lost) and Q8_0 under packet capture
  (0 lost). Only runs by the committed scripts that passed the current
  checks are committed.

## Numeric check: adjudicated flags and the W4A16 replication (2026-10-01, dated)

What the deterministic numeric check's flags are worth once a human has
read every one, and what that changes in the W4A16 vs BF16 comparison.
Nothing here is a number of record.

**The check.** `agent/numeric_check.py` binds every stock-data figure a
brief states (market cap, revenue, net income, profit margin, price,
52-week range) to the stock dict the pipeline gave the generators, and
flags a figure outside tolerance (a *mismatch*) or a template placeholder
left in the text. News and filing numbers are out of scope. In the app it
runs as `NUMERIC_CHECK` (`off|warn|block`, default `warn`). The rate below
is distinct mismatches per distinct checked number, both counted within a
brief. `scripts/numeric_backtest.py` runs the check over the committed
findings of the nine live runs and the frozen-input replays
(`eval/runs/numeric-backtest-2026-09-29.md`).

**Adjudication.** Every live flag (359 rows, nine runs) and the
pre-registered stratified sample of the replication's flags (60 per arm)
got one verdict each: TRUE_ERROR, FALSE_POSITIVE or OTHER_DEFECT (a broken
brief whose problem is not a wrong number, such as a truncated "-$3"). The
eight rules were committed before any row was labeled (4ef7ec6,
`eval/numeric_check/README.md`), and the 479 verdicts were committed
before any figure below was computed (a27264b). One adjudicator, using
`eval/numeric_check/label_cli.py`, which shows run, arm and model, so the
labeling was not blind to arm. The adjudicator also saw the check's
stated value, source value and ratio, and every row shown was a flag (no
unflagged numbers were mixed in), so the labeling was not blind to the
check's output either. Full blinding was not possible: a verdict needs the
source value. That differs from the judge's held-out validation, where
the human labels were blind to the judge's labels. There was no second
rater, so there is no agreement figure. The adjudicator recorded no doubt notes (rule 8: 0 of
479) and no notes of any kind.

```bash
python scripts/numeric_backtest.py --precision          # registered precision, Wilson CIs
python scripts/numeric_adjudicated.py --date 2026-10-01 # everything below
```

Output: `eval/runs/numeric-adjudicated-2026-10-01.{json,md}`. The script
reads the verdicts and never writes them. It rebuilds each flag from the
raw files and fails if any flag lacks a verdict, if any verdict lacks a
flag, or if the replication frame differs from the registered sample
record. Its unadjudicated replication gap equals the committed one to the
digit.

### Precision

Unit: one adjudication row, i.e. a distinct finding. Two ways: OTHER_DEFECT
as a true positive, and OTHER_DEFECT excluded. The cluster bootstrap
resamples whole briefs (10,000 draws, seed 42). Where every flag in a
group got the same verdict, there is nothing to resample, and the Wilson
lower bound is the only bound. Wilson treats flags as independent, so
that bound is optimistic.

| Group (full runs) | Rows | TRUE_ERROR / FALSE_POSITIVE / OTHER_DEFECT | Precision, OD as TP (Wilson; cluster bootstrap) | Precision, OD excluded (Wilson; cluster bootstrap) |
|---|---|---|---|---|
| Hosted (`j4cnp`, `kcf7s`, `dvvxk`; `2nh8v` had no flags) | 19 | 19 / 0 / 0 | 19/19 = 100% (83.2–100%; n/a) | 19/19 = 100% (83.2–100%; n/a) |
| Local-model, all five runs | 340 | 323 / 2 / 15 | 338/340 = 99.4% (97.9–99.8%; 98.5–100%) | 323/325 = 99.4% (97.8–99.8%; 98.4–100%) |
| of which W4A16 `r5nzh` | 88 | 74 / 2 / 12 | 86/88 = 97.7% (92.1–99.4%; 93.9–100%) | 74/76 = 97.4% (90.9–99.3%; 93.3–100%) |
| All live | 359 | 342 / 2 / 15 | 357/359 = 99.4% (98.0–99.9%; 98.6–100%) | 342/344 = 99.4% (97.9–99.8%; 98.5–100%) |

Every other run's flags were all TRUE_ERROR, apart from one OTHER_DEFECT
each in `lsnnc`, `v924f` and `4nfsm` (two cut-off figures and an "N/A"
margin). Twelve of the 14 non-TRUE_ERROR verdicts are in `r5nzh`:

- **OTHER_DEFECT (12):** ten from one BLNK section that counts up "over
  the past N years … net losses of $N00 billion". That section hit the
  512-token cap. The other two are a per-share figure bound to net income
  (AMZN) and a sign contradiction (SNAP).
- **FALSE_POSITIVE (2):** a cumulative "since inception" loss (LCID) and
  a cash-position sentence bound to net income (OMER).

Replication, using the registered estimator (stratum-weighted precision of
the 60-per-arm sample, `replication_applied_precision`, unchanged since
registration): 60 of 60 TRUE_ERROR in each arm (sample Wilson 94.0–100%).
The weighted precision is 100% both ways, so the estimated true mismatches
equal the flag counts, 430 (BF16) and 405 (W4A16). W4A16's `current_price`
stratum (2 of its 405 flags) drew no sample and is **unlabeled**. The
registered estimator gives it the labeled strata's weighted precision.

So the check's flags are almost all real errors. This is precision only.
The check misses errors it cannot bind, and rule 5 had the adjudicator
judge currency rows against real USD values from outside the committed
data.

### Mismatch rates on TRUE_ERROR flags only

All sections, full runs. "Excl. upstream" also drops the TRUE_ERRORs that
trace to the two upstream data defects (next subsection). Both of those
defects get fixed in a later dated change, not here.

| Run / arm | Flags (unadjudicated) | TRUE_ERROR only (cluster bootstrap 95%) | TRUE_ERROR excl. upstream (cluster bootstrap 95%) |
|---|---|---|---|
| Hosted `j4cnp` | 8/543 = 1.5% | 8/543 = 1.5% (0.4–2.9%) | 1/543 = 0.2% (0.0–0.6%) |
| Hosted `kcf7s` | 7/571 = 1.2% | 7/571 = 1.2% (0.0–3.2%) | 0/571 |
| Hosted `dvvxk` | 4/550 = 0.7% | 4/550 = 0.7% (0.0–1.7%) | 0/550 |
| Hosted `2nh8v` (10 tickers) | 0/132 | 0/132 | 0/132 |
| Qwen2.5-7B `cnkp2` | 20/511 = 3.9% | 20/511 = 3.9% (1.7–6.9%) | 9/511 = 1.8% (0.4–3.8%) |
| Qwen2.5-1.5B `4nfsm` | 63/422 = 14.9% | 63/422 = 14.9% (11.5–18.6%) | 55/422 = 13.0% (9.8–16.5%) |
| Fine-tune BF16 `lsnnc` (2026-09-05 image) | 85/363 = 23.4% | 84/363 = 23.1% (15.2–31.7%) | 72/363 = 19.8% (12.0–28.8%) |
| Fine-tune BF16 `v924f` | 57/357 = 16.0% | 56/357 = 15.7% (11.7–19.6%) | 49/357 = 13.7% (9.9–17.7%) |
| Fine-tune W4A16 `r5nzh` | 87/327 = 26.6% | 73/327 = 22.3% (17.2–27.9%) | 60/327 = 18.4% (13.1–24.1%) |
| **Hosted arm, pooled** | 19/1796 = 1.1% | 19/1796 = 1.1% (0.4–1.8%) | 1/1796 = 0.1% (0.0–0.2%) |
| **Local-model arm, pooled** | 312/1980 = 15.8% | 296/1980 = 14.9% (12.7–17.3%) | 245/1980 = 12.4% (10.3–14.8%) |

The local-model arm minus the hosted arm (pooled, paired by ticker,
cluster bootstrap) is +13.9 pts on TRUE_ERROR only (CI +11.2 to +16.8),
against +14.7 on flags. Excluding upstream it is +12.3 (CI +9.4 to +15.5).
Bootstrap p < 0.0002 for all three. The local-model arm pools four
different models, so the per-run rows are the ones to compare.

**Live same-image gap, W4A16 `r5nzh` minus BF16 `v924f`.** Financial
Health + Risk Factors only, one draw per ticker:

| Counting | Sections | `r5nzh` | `v924f` | Difference (bootstrap 95% CI) | Bootstrap p |
|---|---|---|---|---|---|
| Flags | all | 65/117 = 55.6% | 44/113 = 38.9% | +16.6 pts (+5.2 to +27.4) | 0.0026 |
| Flags | truncated excluded (estimated) | 51/103 = 49.5% | 35/100 = 35.0% | +14.5 pts (+4.7 to +23.8) | 0.005 |
| TRUE_ERROR only | all | 52/117 = 44.4% | 43/113 = 38.0% | +6.4 pts (−4.1 to +15.8) | 0.21 |
| TRUE_ERROR only | truncated excluded (estimated); exploratory, post hoc | 49/103 = 47.6% | 35/100 = 35.0% | +12.6 pts (+2.9 to +21.7) | 0.012 |

On all sections, adjudication removes most of the live gap: it was
mostly the degenerate BLNK section. That section hit the cap, so
excluding truncated sections had already removed it, and the
truncation-excluded gap barely moves. Truncation for live runs is
estimated by re-tokenizing the saved text.

**The truncation-excluded live gap is exploratory and post hoc:** +12.6
pts in true errors (CI +2.9 to +21.7, p = 0.012). It rests on one draw
per ticker, and the truncation-excluded subset was chosen after the pilot
had been seen. Its interval excluding zero is therefore not a test. The
pre-registered replication (+5.3 pts, CI −1.1 to +11.6) remains the
primary result.

**Replication.** The pre-registered replication is the confirmatory test,
and its result stays primary: **the W4A16 regression does not replicate
on identical inputs**. W4A16 − BF16 = +5.3 pts (paired ticker-cluster
bootstrap CI −1.1 to +11.6, p = 0.098), on the replayed Financial Health
+ Risk Factors, truncated sections excluded, unadjudicated flags
(`replay-replication-2026-09-30`, 40 tickers × 10 seeded samples per arm).
The adjudication-adjusted figures are secondary. Each flag is weighted by
its field stratum's TRUE_ERROR share, and the paired ticker draws are the
same as the registered bootstrap's, with each stratum's labels resampled
alongside:

- Unlabeled stratum at the weighted share (the registered treatment):
  +5.3 pts (CI −1.1 to +11.6). Adjusted rates: W4A16 45.6%, BF16 40.3%.
- Unlabeled stratum counted as 0% true: +5.1 pts (CI −1.5 to +11.4).
- Precision the 60/60 samples cannot rule out: if one arm sat at its
  Wilson lower bound (94.0%) and the other at 100%, the point gap would
  be +2.6 pts (W4A16 at the bound) or +7.8 pts (BF16 at the bound). The
  bootstrap cannot show this, because a 60/60 sample resamples to 60/60.

The replication's secondary all-sections gap (+10.7 pts, CI −0.3 to
+21.5) is not adjusted: the sample was drawn from the primary metric's
flags only.

Adjudication leaves the replication result as it was. The live one-draw
gap survives adjudication on the truncation-excluded estimate, but that
figure is exploratory and post hoc (above), and the replication was built
to test exactly that gap. It does not exclude zero.
The pilot had already shown how far one draw can sit from the same model
on the same inputs. On these sections (all sections, flags), the
replayed BF16 samples gave 41.9–52.7% against `v924f`'s single live draw
of 38.9%. The supported statement: **on identical inputs, W4A16 is not
shown to state more wrong stock figures than BF16, and it is not shown to
state the same number either.** The interval allows up to +11.6 pts.
This is not a measured regression.

### TRUE_ERRORs tracing to the upstream data findings

`eval/numeric_check/upstream-findings.md` records two defects in the stock
dict:

- **(a) Currency.** Home-currency revenue and net income for foreign
  filers are labeled USD.
- **(b) Margin fraction.** profit_margin is a raw fraction, so a margin
  above 100% in magnitude can be written 100x too small.

The rule used to attribute a TRUE_ERROR to one of them (`upstream_cause`)
is mechanical:

- **Currency:** TM, TSM, NVO or BABA revenue/net_income whose stated
  figure is a power-of-ten rescaling of the mislabeled source.
- **Margin fraction:** a profit_margin with |source| > 1, stated at
  ratio ~0.01.

SAP is listed, not attributed, because EUR and USD are within 2x.
Margins off by 10x on those tickers (-15.73% for -1.57) are listed too.

| Arm | TRUE_ERRORs (mismatches) | Currency | Margin fraction | Upstream total | Listed, not attributed |
|---|---|---|---|---|---|
| Hosted (live) | 19 (19) | 7 | 11 | **18** | 0 |
| Local-model (live) | 323 (296) | 35 | 16 | 51 | SAP 3, margin at 10x 3 |
| of which BF16 fine-tune `lsnnc` + `v924f` | 144 (140) | 12 | 7 | 19 | SAP 2 |
| of which W4A16 `r5nzh` | 74 (73) | 10 | 3 | 13 | SAP 1, margin 1 |
| of which Qwen2.5-1.5B `4nfsm` | 81 (63) | 6 | 2 | 8 | margin 2 |
| of which Qwen2.5-7B `cnkp2` | 24 (20) | 7 | 4 | 11 | 0 |
| Replication BF16 (sample of 60) | 60 (60) | 4 | 1 | 5 | 0 |
| Replication W4A16 (sample of 60) | 60 (60) | 3 | 2 | 5 | SAP 1 |

Eighteen of the hosted arm's 19 TRUE_ERRORs are the upstream data showing
through. The one that is not is `j4cnp` OCGN, a 52-week low stated as
$1.36 against $1.01. Hosted models make the margin-fraction error as
often as the local ones. For the local-model arm, the upstream share is
small (51 of 323). Its own errors are mostly power-of-ten slips: 239 of
the 245 other TRUE_ERROR mismatches, mainly market cap (117) and net
income (86).

## Dated A/B on the single-VM target (2026-09-03)

Same VM, same harness, same judge (v1), ~40 minutes apart, 10/10
tickers each, no retries. vLLM traffic confirmed for the local arm: 20 POST
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
this run), not on one 10-ticker pass. **Superseded 2026-09-06**: the
40-ticker A/B (above) separates the arms at p = 0.0023 and now carries
the decision. These are dated run records from the committed harness.

## Statistical power

Every reported rate carries a Wilson 95% interval and every two-arm
comparison a Fisher exact p-value (`eval/stats.py`, wired into
`scripts/eval_aggregate.py` and `grounding_check.py`). The reason this
is mandatory at the current scale: **N = 66 claims cannot resolve a 3%
observed rate against a 5% gate** — the Wilson 95% interval for 2/66 is
0.8–10.4%, which contains the gate on both sides, so a "pass" at 3.03%
is fully consistent with a true rate above 5% (and a mild fail with one
below it). Distinguishing 3% from 5% with useful power needs claims in
the several-hundreds — the motivation for the extended benchmark, which
delivered exactly that: at N = 392 vs 368 the 40-ticker A/B separates
3.06% from 8.15% at p = 0.0023 where the 10-ticker pass could not
(judge-flagged v2 rates; reweighted estimates 5.7% vs 8.3%, see the
held-out validation; direction unaffected, both arms share the judge).

## Retrieval defect, discovered 2026-09-04

**Mechanism.** On EDGAR filing index pages, inline-XBRL filers link the
primary document through an `/ix?doc=` viewer wrapper. The fetcher's
href regex matched only plain `/Archives/...htm` links, the
exhibit-name filter then rejected every remaining `.htm` file, and the
`htm_files[0]` fallback selected **Exhibit 4.x** — so for most tickers
the indexed "10-K" was an exhibit (AAPL's was its Bylaws). Two
compounding layers: undecoded HTML entities
(`Item 1A.&#160;&#160;Risk Factors`) hid section headings from the
window anchor, and a bare `item 1a` anchor also matched
forward-looking-statement cross-references.

**Fix and verification.** The fetcher now resolves the primary document
from the submissions JSON `primaryDocument` field (scrape kept as
fallback, `/ix?doc=` unwrapped), cleaning decodes entities, and the
anchor requires title adjacency. Verified by
`scripts/reindex_filings.py` (top-3 risk-factors retrieval must carry
risk prose and no exhibit/TOC boilerplate): **pre-fix 3 PASS / 32
VERIFY-FAILED / 5 FETCH-FAILED (ADRs); post-fix 32 PASS / 8 failed** —
the 5 ADRs (20-F filers, the deliberate coverage gap), MSFT and SANA
(windows still include a TOC-listing chunk), and UPST (verifier false
positive: "indenture" used legitimately in SPE-financing risk prose).

**What this means for the numbers.** All grounding numbers dated before
2026-09-04 measured the pipeline against exhibit text for most tickers;
they remain valid as dated records **of that pipeline**. The defect was
surfaced by the human labeling pass — reading retrieved contexts and
finding exhibit boilerplate (RSU agreements, indentures, bonus plans)
where risk factors should be — not by the automated eval, which had
scored that retrieval for weeks without noticing.

## Judge validation — v1 results (2026-09-04)

- **Sample**: `eval/judge_validation/sample.csv` — 50 claims,
  stratified over the judge's labels (16 SUPPORTED / 3 UNSUPPORTED /
  31 INFERENCE), drawn from a 176-claim pool with
  `eval/label.py --seed 42`.
- **Provenance, stated exactly**: the pool is the committed
  `eval_findings/` per-claim artifacts of the **2026-08-24 local run**
  (baseline + local-model arms, same judge and prompt as every DAG run).
  It is *not* the Sep 3 `grounding-eval-6zwqf` run: that run's per-claim
  findings were written inside the eval pods and never archived.
- **Labeling method, stated verbatim**: "Labels were assigned by the
  author after reviewing every claim against its retrieved context. Two
  LLMs (Gemini Pro on 42 claims, Claude Fable 5.1 on all 50) were
  consulted for a proposed label and rationale; the author made the
  final call on every row. Labeling was not blind to model output."
- **Analysis**: `eval/agreement.py`, human labels as ground truth,
  Wilson 95% intervals throughout.

**Result (judge v1):**

```
Confusion (rows = judge, cols = human):
                 SUPPORTED  UNSUPPORTED  INFERENCE
SUPPORTED               13            2          1
UNSUPPORTED              0            1          2
INFERENCE               10            6         15
```

- Cohen's kappa (3-class): **0.321**
- Judge recall on UNSUPPORTED: **1/9 = 11.1% (95% CI 2.0–43.5%)**
- Judge precision on UNSUPPORTED: **1/3 = 33.3% (95% CI 6.1–79.2%)**

**The finding, stated plainly: INFERENCE is a catch-all.** The judge
filed 6 of the 9 human-UNSUPPORTED claims as INFERENCE — and INFERENCE
also absorbed 10 human-SUPPORTED claims. Because the gate counts only
UNSUPPORTED, **the gate understates the true unsupported rate by an
unknown factor**: every judge-v1-reported unsupported rate in this repo
(0/84, 3.03%, 12.31%) is a lower bound on what a human reading would
find. The Sep 3 A/B *direction* is unaffected — both arms were scored
by the same judge — but its absolute rates inherit the caveat.

**Labeling rubric applied by the author, verbatim**: positional
adjectives verifiable from two context numbers are SUPPORTED when they
hold and UNSUPPORTED when they don't; comparators with no comparator in
context are INFERENCE for mild ones (premium, elevated, reasonable) and
UNSUPPORTED for superlatives; conditionals and watch-items are
INFERENCE; declaratives naming an entity or figure not in context are
UNSUPPORTED; derived percentages within 0.15pp of the computed value
pass.

**Sample limitations**: stratified toward judge-INFERENCE rows (31/50);
ticker skew (JPM 11 and V 9 of 50); repeated draws from the same
sentences (claims sampled from the same briefs share text); n=50, so
the UNSUPPORTED cells are single digits and the intervals are wide;
labels are the author's, informed by non-blind LLM consultation, not an
independent panel.

### Judge v1 vs v2 on the 50-claim dev set (measured 2026-09-04)

Judge v2 (see `agent/grounding.py`: five rules, each targeting a
failure mechanism from the v1 validation; not tuned beyond those rules)
and — for a clean comparison — **judge v1 under the identical doc-level
view** were both re-run over the same 50 claims via `eval/rejudge.py`
(19 judge calls each; claims matched back by normalized containment;
keys: `sample_key_v1_rejudged.csv`, `sample_key_v2.csv`). **These 50
claims are a development set: v2's rules were written from their
failure modes, so nothing below validates v2.** The held-out validation
that does is in "Judge v2 held-out validation" below.

```
                       v1 original key   v1 rejudged      v2 rejudged
inputs                 sections visible  doc-level, no    doc-level, no
                                         sections         sections
claims scored          50                28 matched        31 matched
                                         (22 unmatched)    (19 unmatched)
confusion (J rows      13/ 2/ 1          15/ 0/ 0          20/ 3/ 1
 S,U,I × human S,U,I)   0/ 1/ 2           0/ 1/ 0           0/ 4/ 0
                       10/ 6/15           4/ 4/ 4           0/ 1/ 2
kappa                  0.321             0.498             0.648
UNSUPPORTED recall     1/9 = 11.1%       1/5 = 20.0%       4/8 = 50.0%
                       (2.0–43.5%)       (3.6–62.4%)       (21.5–78.5%)
UNSUPPORTED precision  1/3 = 33.3%       1/1 = 100%        4/4 = 100%
                       (6.1–79.2%)       (20.7–100%)       (34.2–100%)
```

**The fair comparison is v1-rejudged vs v2** — same inputs, same
doc-level view, prompt as the only variable. On the 24 claims matched
under *both* segmentations: v1-rejudged kappa **0.381**, UNSUPPORTED
recall 1/5, precision 1/1; v2 kappa **0.647**, UNSUPPORTED recall 2/5,
precision 2/2. Read plainly: **the input view did a real share of the
work** — v1's kappa moved 0.321 → 0.498 just from the doc-level
re-judge, before any rule changed — and the v2 rules added a further
genuine kappa gain on identical rows (0.381 → 0.647). On the metric
that matters most, UNSUPPORTED recall, the fair-pair gain is **one
claim (1/5 → 2/5)** — not resolvable at n=5; the headline 4/8 includes
rows v1-rejudged failed to match. v1 also segments less stably (22
unmatched vs 19).

**Human-UNSUPPORTED claims v2 files as SUPPORTED** (dev-set ids; no
fixes, mechanisms recorded for the held-out check):

| id | Ticker | Claim | Mechanism |
|---|---|---|---|
| 20 | AAPL | "9-month net sales up 17% year-over-year through Q3 2026" | Rule-b component ambiguity: the nine-month table offers several "net sales" candidates (products-only grows 16.9%); v2's chosen combination passes the 0.15pp recompute, the human's did not |
| 22 | JPM | "the regulatory and cybersecurity risk environment flagged in the company's own filings" | Rule-4 gap: the only filing content is a TOC ("Item 1A. Risk Factors… Item 1C. Cybersecurity"), which v2 accepted as the filings "flagging" those risks — rule 4 names exhibit boilerplate but not TOC section titles used as support |
| 23 | WMT | "Q2 2026 net sales rose 7.2% year-over-year" | Recompute passes (175,684/163,981 = +7.14%, within 0.15pp of 7.2%); the discrepancy candidate is the period label — the table's quarter ends July 2026, which is fiscal 2027 for WMT, so "Q2 2026" mislabels the period (rule-c miss against a fiscal-calendar quirk) |

### Judge v2 held-out validation (labeled 2026-09-06)

- **Sample**: `eval/judge_validation/holdout_sample.csv` — 50 claims
  drawn by `eval/build_holdout.py` (seed 42) from the 40-ticker A/B
  runs (`j4cnp` baseline + `lsnnc` local-model), stratified by (arm,
  judge label) to 15 UNSUPPORTED / 15 INFERENCE / 20 SUPPORTED with a
  cap of 3 claims per ticker. **Held out**: zero overlap with the
  50-claim dev set, checked by normalized claim text and
  source-context sha256 (4 recurring-text claims excluded at draw
  time). v2's rules were frozen before this sample existed.
- **Labeling method, stated verbatim**: "The held-out sample was
  labeled blind by the author against the retrieved context and
  pre-written sections only, with no model consultation, using the
  rubric in this document."
- **Analysis**: `eval/agreement.py --labeled holdout_sample.csv --key
  holdout_key.csv`, human labels as ground truth, Wilson 95% intervals.

**Result (judge v2, held out):**

```
Confusion (rows = judge, cols = human):
                 SUPPORTED  UNSUPPORTED  INFERENCE
SUPPORTED               15            1          4
UNSUPPORTED              1            9          5
INFERENCE                1            2         12
```

- Cohen's kappa (3-class): **0.580**
- Judge precision on UNSUPPORTED: **9/15 = 60.0% (95% CI 35.7–80.2%)**
- Judge recall on UNSUPPORTED, population-weighted: **32.5% on `j4cnp`
  (95% CI 16.0–52.4%)**, on the calibration set of record below

Precision conditions on the judge label, so it needs no reweighting.
Recall does. Stated plainly: v2 over-flags INFERENCE as UNSUPPORTED (5
of its 6 UNSUPPORTED false positives were human-INFERENCE claims), but
once the sample is weighted back to the runs it misses more than it
over-flags, so **every v2 unsupported rate is a judge-flagged rate and
the true rate is estimated higher.** Against v1's dev-set result (kappa
0.321, UNSUPPORTED recall 1/9 = 11.1%, precision 1/3 = 33.3%,
non-blind, and measured under dev conditions, unweighted), v2 is the
better instrument on kappa and precision; the recall comparison is not
like for like.

**Superseded (dated 2026-09-06): recall 9/12 = 75.0% (CI 46.8–91.1%).**
That figure was computed on the sample as drawn. The sample was
stratified by judge label (20 SUPPORTED / 15 UNSUPPORTED / 15
INFERENCE), while judge-SUPPORTED is ~90% of claims in the runs, so the
unweighted figure gave the judge-SUPPORTED stratum 20/50 of the weight
instead of ~90%. It is not quoted as current anywhere.

#### Calibration of record (2026-09-24)

The set, per judge-label stratum:

- **Judge-SUPPORTED: 4/123 human-UNSUPPORTED**, from the blind relabel of
  123 judge-SUPPORTED claims (the calibration batch's 103 and the
  held-out sample's 20, shuffled together with the source hidden;
  `eval/judge_validation/relabel_S.csv`, see the dated finding below).
- **Judge-UNSUPPORTED: 9/15 and judge-INFERENCE: 2/15**, the held-out
  sample's labels of 2026-09-06.
- The calibration batch's first-pass labels are discarded and kept on
  record only (dated finding below).

`eval/reweight_calibration.py` weights each judge-label stratum by that
run's judge-label counts (`eval/label.py` `count_labels_deduped` over
the findings, cross-checked against the claims file). Per stratum k:
p_k = human-UNSUPPORTED / n_k. Estimated truly unsupported claims
T = sum_k N_k p_k; recall = N_U p_U / T; true rate = T / N. 95%
intervals: Monte Carlo over independent Jeffreys Beta(x + 0.5,
n - x + 0.5) posteriors per stratum, 200,000 draws, fixed seed 20260924;
the run counts N_k are treated as fixed.

| Run | Judge counts S / U / I | Judge-flagged rate | Recall (95% CI) | Estimated true rate (95% CI) |
|---|---|---|---|---|
| `j4cnp` baseline | 354 / 12 / 26 | 3.06% | 32.5% (16.0–52.4%) | 5.7% (3.5–9.9%) |
| `lsnnc` local-model | 324 / 30 / 14 | 8.15% | 59.2% (36.0–77.9%) | 8.3% (5.5–12.5%) |
| pooled | 678 / 42 / 40 | 5.53% | 47.9% (26.5–68.3%) | 6.9% (4.5–11.1%) |

Reproduce (`--use` takes only the judge-UNSUPPORTED and judge-INFERENCE
rows from the held-out sample; its judge-SUPPORTED rows are in the
relabel set):

```
python eval/reweight_calibration.py \
    --labeled eval/judge_validation/relabel_S.csv \
    --key eval/judge_validation/relabel_S_key.csv --use ALL \
    --labeled eval/judge_validation/holdout_sample.csv \
    --key eval/judge_validation/holdout_key.csv --use UNSUPPORTED,INFERENCE \
    --run j4cnp eval/runs/j4cnp-claims.jsonl eval/runs/raw/j4cnp-findings \
    --run lsnnc eval/runs/lsnnc-claims.jsonl eval/runs/raw/lsnnc-findings \
    --by-section
```

Reading it:

- With 123 judge-SUPPORTED labels the stratum that decides most of T is
  now well measured; the judge-UNSUPPORTED and judge-INFERENCE strata
  are still 15 labels each and now drive most of the interval width.
- The A/B direction stands. `j4cnp` 3.06% vs `lsnnc` 8.15% (p = 0.0023)
  and the per-section attribution compare two arms scored by the same
  judge, so its misses apply to both. The reweighted estimates (5.7% vs
  8.3%) are closer together because the same miss rate on
  judge-SUPPORTED claims adds to both; the calibration cannot tell
  whether misses differ by arm or by section.
- The recall on `lsnnc` is higher because more of its truly unsupported
  claims are ones the judge does flag (30 judge-UNSUPPORTED vs 12).
- Two interval bounds sit on a Monte Carlo rounding boundary: the
  `j4cnp` recall upper bound prints 52.4% (52.6% in an independent run
  of the same math) and the true-rate lower bound 3.5% (3.4%). The
  committed seed's output is what is quoted.

**Superseded (dated 2026-09-24): the held-out-only reweight.** Computed
first the same day from the held-out sample alone (judge-SUPPORTED
1/20): `j4cnp` recall 25.4% (CI 7.4–58.4%), true rate 7.2% (CI
3.1–22.0%); `lsnnc` recall 49.9% (CI 18.4–83.1%), true rate 9.8% (CI
5.3–24.2%); pooled recall 39.1% (CI 13.0–74.0%), true rate 8.5% (CI
4.2–23.1%). Replaced by the calibration of record above, which measures
the judge-SUPPORTED stratum on 123 claims instead of 20.

#### Dated finding: calibration batch first pass discarded, caught by a blind relabel (2026-09-24)

The 150-claim calibration batch (method below) was labeled once with
`eval/label_cli.py`. On judge-SUPPORTED claims the first pass found
42/103 = 40.8% (CI 31.8–50.4%) human-UNSUPPORTED, against 1/20 in the
held-out sample (Fisher p = 0.0016). It showed no drift by labeling
position (rows 1–34: 9/19, rows 35–150: 33/84, p = 0.61) and no arm
effect (38.9% baseline vs 42.9% local-model), but it concentrated in
Outlook claims (18/30 = 60.0%, against 19/67 = 28.4% in Executive
Summary).

To separate a labeling-standard shift from sampling, every
judge-SUPPORTED row of both sets (103 + 20) was relabeled blind, shuffled
together with the source hidden (`eval/build_relabel_s.py`, seed
20260925). Results (`python eval/relabel_agreement.py`):

| Source | Original | Blind relabel | Test-retest |
|---|---|---|---|
| Held-out sample (20) | 1/20 = 5.0% (CI 0.9–23.6%), labeled 2026-09-06 | 1/20 = 5.0% (CI 0.9–23.6%) | 17/20 exact, kappa 0.592 |
| Calibration batch (103) | 42/103 = 40.8% (CI 31.8–50.4%), first pass | 3/103 = 2.9% (CI 1.0–8.2%) | 62/103 exact, kappa 0.242 |

- The relabeled sources agree: 1/20 vs 3/103, Fisher p = 0.51; together
  4/123 = 3.3% (CI 1.3–8.1%).
- The batch's first pass moved one way: of its 42 UNSUPPORTED labels, 3
  stayed, 31 went to SUPPORTED and 8 to INFERENCE; no label moved toward
  UNSUPPORTED. The withdrawn labels include plainly sourced figures
  (an accumulated deficit, a user count, a segment revenue line).
- On relabel, Outlook claims were 0/35 UNSUPPORTED with 9/35 INFERENCE:
  the forward-looking claims the first pass had called UNSUPPORTED are
  the INFERENCE the rubric describes.

Conclusion: the first pass applied an over-strict standard. Its labels
are discarded and kept on record only (`calibration_batch.csv`, labels
as entered). The batch's judge-UNSUPPORTED and judge-INFERENCE rows came
from the same pass (21/23 judge-UNSUPPORTED rows labeled UNSUPPORTED,
against 9/15 in the held-out sample, p = 0.039), so they are discarded
too; those strata use the held-out labels. A blind relabel sample for
them (`relabel_UI.csv`, 77 rows, `eval/build_relabel_ui.py`, seed
20260926) is built and was not labeled. The lesson that stays: a
labeling pass is not trusted until a blind relabel of an overlapping
sample agrees with it.

#### Calibration batch: draw method (2026-09-24)

`eval/build_calibration_batch.py` (seed 20260924) draws 150 claims from
`j4cnp` + `lsnnc` into `eval/judge_validation/calibration_batch.csv`,
weighted toward the judge-SUPPORTED stratum that decides recall. Method,
also in `calibration_batch_method.json`:

- **Pool**: every claim with a CLAIM line (756 parsed), minus 57 that
  overlap the dev set (claim text or source-context sha256) or the
  held-out set (claim text).
- **Strata**: judge label, then arm in proportion to the run's
  judge-label count. Targets were 100 SUPPORTED / 25 INFERENCE / 25
  UNSUPPORTED; after exclusions only 23 UNSUPPORTED and 24 INFERENCE
  claims remain eligible, so both are taken whole and the shortfall of 3
  goes to SUPPORTED (103), keeping 150. Within each (label, arm) cell the
  draw is simple random.
- **Ticker cap**: 4 per ticker on SUPPORTED, applied only if not binding.
  It binds (EDIT, LCID, NTLA, TSLA at 5, UNH at 6; 6 draws would be
  displaced), so it is **not applied** and the SUPPORTED draw stays
  simple random. 38 tickers appear in the SUPPORTED draw.
- **Blinding**: the CSV has `id, ticker, claim, context, human_label`
  only. No provenance column (unlike `holdout_sample.csv`): 22 of the 23
  eligible UNSUPPORTED claims are local-model, so the run would hint at
  the judge label. Rows are shuffled. The census of the scarce strata
  still concentrates some tickers (WMT, the local-model outlier, has 15
  rows); label every row on its own evidence.
- **Labeling**: the first pass was labeled with `eval/label_cli.py`, blind to judge labels (the tool never reads a `*_key.csv`); it is discarded, see above.
- **Key**: `calibration_batch_key.csv` (run, arm, judge label and reason,
  with the strata in a `#` header block) is gitignored like the four-arm
  key; it stays out of the public repository. `eval/agreement.py` and `eval/reweight_calibration.py` read
  it as is.

| Judge label, arm | Run population | Eligible pool | Drawn |
|---|---|---|---|
| SUPPORTED, `j4cnp` baseline | 354 | 341 | 54 |
| SUPPORTED, `lsnnc` local-model | 324 | 311 | 49 |
| UNSUPPORTED, `j4cnp` baseline | 12 | 1 | 1 |
| UNSUPPORTED, `lsnnc` local-model | 30 | 22 | 22 |
| INFERENCE, `j4cnp` baseline | 26 | 18 | 18 |
| INFERENCE, `lsnnc` local-model | 14 | 6 | 6 |

Within SUPPORTED the arms were drawn in proportion to their counts
(54/49 vs 354/324), which is why the batch's judge-SUPPORTED rows could
join the relabel set directly.

### Injected-failure check (measured 2026-09-04)

Orthogonal to human labels: `eval/perturb.py` builds fixtures with
*known* ground truth from committed run artifacts — a supported number
swapped in the audited text, the supporting context lines dropped, or a
plausible fabricated claim inserted — 20 unique tagged fixtures
committed (`eval/perturbed/fixtures.jsonl`, 7/7/6 across the three
types). Two full runs of `eval/critic_check.py` (both 2026-09-04):
**recall 20/20 = 100% (95% CI 83.9–100%) on both.** Run 1 persisted
only counts (raw precision vs tags 71.4%, flags unauditable); run 2
persisted every flag and all 4 off-needle flags were adjudicated
against their fixture contexts:

| Fixture | Off-needle claim | Evidence vs fixture context | Class |
|---|---|---|---|
| 0 META (swap 559.02→814.91) | "trades meaningfully below its 52-week high of $790.80" | high 790.8 is in context, but the injected price 814.91 exceeds it | cascade |
| 2 NVDA (insert) | "Supply chain concentration around TSMC…" | no TSMC/supply-chain/foundry mention anywhere in the (unperturbed) context | pre-existing |
| 9 NVDA (swap 208.48→283.50) | "sit in the upper-middle of its 52-week range" | injected price exceeds the 52-week high of 236.54 | cascade |
| 16 NVDA (drop 208.48 lines) | "sit in the upper-middle of its 52-week range" | the current-price line was dropped; range position is unverifiable | cascade |

Run 2: raw precision vs the injection tags 20/24 = 83.3% (95% CI
64.1–93.3%); **adjudicated precision — cascades and pre-existing are
true unsupported claims — 24/24 = 100% (95% CI 86.2–100%), zero false
positives.** The judge's claim segmentation still varies between
temperature-0 runs (8, then 4 off-needle flags on identical inputs), so
per-run flag counts are noisy even though the gated metric, recall,
reproduced exactly. A CI job
(`.github/workflows/critic-injection.yml`) re-runs this on manual dispatch
only (the weekly Sunday schedule was removed 2026-09-28), never on push, PR
or a schedule because it spends judge credits, and asserts recall ≥ 0.8;
the bar does not move if it
regresses — the number gets reported instead.

## Boundary

Argo owns eval orchestration; Celery owns request-time async. The eval
DAG runs the pipeline in its own pods — it does not call the API service
and cannot contend with user traffic for the cache or the broker.
