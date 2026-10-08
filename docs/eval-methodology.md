# Eval methodology — the grounding-eval DAG

The centerpiece of this project is not the UI; it is that grounding is
**measured by a committed, re-runnable harness and gated in CI fashion**.
The grounding number of record: **12/392 = 3.06% unsupported (Wilson 95%
CI 1.8–5.3%)**, hosted baseline `j4cnp` (2026-09-05/06), judge v2, fixed
retrieval, 40 tickers. That is the judge-flagged rate; the reweighted true-rate estimate 5.7% (CI 3.5–9.9%),
from the v2 September calibration (2026-09-24): precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED). The former "49% pre-fix → 0/84"
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
(judge v2 September calibration (2026-09-24): precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED)); no reweighted estimate is computed for
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
September calibration (2026-09-24): precision 60% (9/15, CI 35.7–80.2%); population-weighted recall 32.5% on the baseline run (CI 16.0–52.4%), with the judge-SUPPORTED stratum from a blind relabel of 123 claims (4 human-UNSUPPORTED)). Reweighted true-rate estimates (`eval/reweight_calibration.py`):
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
judge-SUPPORTED miss rate (4/123 in the September calibration (2026-09-24)) shared across
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

Calibration: every rate here is a judge-flagged rate (judge v2 September calibration (2026-09-24):
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
stays `j4cnp` 12/392 = 3.06%, and the September calibration (2026-09-24) still
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
- Judge-flagged rates (judge v2; September calibration (2026-09-24): precision 60%
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

## Self-served SLM arm (`slm-full-*`): method (set up 2026-10-02) and the 2026-10-03 smokes

This section is the method `slm-full` runs are reported under. Run so far:
one 10-ticker CPU smoke (`nb6r6`, 2026-10-03, "Smokes on image `2dd1aa3`"
below). Since then, on image `1f51dad`: CPU smoke `wnrjr`, CPU extended
`8vpq6` (2026-10-04), GPU smoke `k6zxd` and GPU extended `p9jr2`
(2026-10-05), all with traffic proof EXACT — "CPU SLM extended run
`8vpq6`" and "GPU SLM extended run `p9jr2`" below. Model: Qwen3.6-35B-A3B (MoE, 35B total / 3B active,
vision-language; served text-only), one artifact for both endpoints:
`ggml-org/Qwen3.6-35B-A3B-GGUF` @`baec3eb` `Qwen3.6-35B-A3B-Q4_K_M.gguf`
(20,419,565,568 bytes, sha256 `671e47e0…40c7`), on llama.cpp `llama-server`
build b11347 (`5fc4f3c`).

**What it routes.** Under `SLM_FULL=true` every agent LLM call goes to one
OpenAI-compatible endpoint (`agent/tools/slm.py`): the four sections, the
synthesis, the SEC RAG answer synthesis (per query; `Settings.llm` is never
touched), and — outside the eval — the multi-agent planner and synthesis
and the ReAct `/ask` agent. The grounding judge stays Sonnet,
`JUDGE_PROMPT_VERSION` v2, inputs unchanged, so the v2 calibration applies
to the main rate. The multi-agent critic also stays Sonnet: it is the one
hosted dependency of the SLM path, and only when `MULTI_AGENT_ENABLED` is on.
There is no hosted fallback; config errors, HTTP errors and unparseable
structured output raise.

**Arms and endpoints.** `slm-full-cpu` → llama.cpp CPU build on OKE
(`k8s/llamacpp/overlays/oke-cpu`: 8 threads, 8 CPU / 30Gi, VM.Standard.E5.Flex);
`slm-full-gpu` → CUDA 12.8.1 build on node 2's A10
(`k8s/llamacpp/overlays/k3s-gpu`, all layers on the GPU). Same GGUF, same
engine release, same server args except threads / GPU layers, so CPU vs GPU
compares hardware only. If the GPU needs `--n-cpu-moe`, the endpoint serves
`…-hybrid-ncmoe<n>` and every table labels that run **hybrid**, never GPU.
The GPU layout is evidenced by llama-server's own memory in `nvidia-smi`,
not by a log line: b11347 logs no layer offload at default verbosity. On
2026-10-03 `/app/llama-server` held 20,488 MiB of the A10's 23,028 MiB
with `--n-gpu-layers all --n-cpu-moe 0` — the whole GGUF on the GPU
(`make vm-llamacpp` prints and checks this).
Retrieval is the baseline arm's (no rerank, top-3), and both arms run the
same RAG pipeline: llama_index's default `compact` response mode, one
answer call per query (the three retrieved chunks fit one prompt under
either arm's context window), same prompt template, temperature and cap.

**Request settings, sent explicitly on every call** (llama-server applies
its own defaults to anything omitted, `min_p` 0.05 among them). Temperature
mirrors the hosted call each site replaces (sections 0.1, synthesis 0.2,
RAG 0.1, planner and ReAct 0); `top_p` 0.8 and `top_k` 20 from the Qwen3.6
card; `min_p` 0, presence/frequency penalty 0, `repeat_penalty` 1.0 (none),
DRY / XTC / typical / top-n-sigma neutral. Thinking off per request
(`chat_template_kwargs.enable_thinking: false`, `LOCAL_MODEL_THINKING`);
Qwen3.6 thinks by default and does not support the `/no_think` switch.
`max_tokens` per site, sized from the largest committed outputs
(`python eval/findings_scan.py eval/runs/raw/*-findings`, chars/4): sections
768 (hosted max 331), synthesis 4096 (hosted max 1,719), planner and ReAct
1024. RAG answers get one budget in both arms: `RAG_MAX_TOKENS` = 2048
(`agent/tools/slm.py`), read by the SLM `rag` profile and passed to the
hosted llama_index Anthropic LLM (`agent/tools/rag.py`); a test holds the
two together (`tests/test_rag_settings.py`). Through image `2dd1aa3` both
arms ran llama_index's Anthropic default of 512, which truncated 13 of the
20 SLM answers on smoke `nb6r6` and none of the hosted smoke's 20 (`x2cx8`,
max 456 tokens). **Consequence for the hosted arm: a hosted run on an image
with the 2048 cap is not the `j4cnp` pipeline exactly — hosted answers that
were cut at 512 now complete.** On the 40-ticker set that is at least the
SFIX risk-factors answer, which stops mid-structure in `j4cnp` (on a
dangling `## Tax-Related Risks` heading), `kcf7s` (`## Tax`) and `dvvxk`
(`**Intellectual Property**:`). Runs before the ledger recorded no finish
reason, so a cut that happened to land on a sentence end cannot be counted;
"at least one of ~70 answers per run" is all the committed findings show.
`j4cnp` was the number of record until 2026-10-05, measured under the 512
cap; the same-image three-way below replaced it. (Committed
RAG answers reach 693 tokens by chars/4 under that cap, so chars/4
overstates Claude's token count.) The value is sized from a measurement
("RAG natural-length pre-check" below: the smoke's 20 SLM answers ran to a
max of 854 tokens when nothing cut them), and truncations stay counted per
run. The full set is in each run's provenance.

**Counted per run** (the LLM ledger, `agent/llm_ledger.py`; findings
metadata, result rows, aggregate): calls, prompt/completion tokens and
latency per call site, per-step wall time, truncations (`finish_reason`
length), repetition loops (a run of 5–60 words repeated three times back to
back; retroactively, `eval/findings_scan.py` finds 0 in every committed
hosted, 1.5B-base and 7B-base run and 19 in the fine-tune arms' sections —
`lsnnc` 3, `r5nzh` 5, `v924f` 11, each one sentence restated back to back),
parse failures (unparseable tool calls; planner JSON, retried once),
format failures (Executive Summary / Outlook missing: retried once, then
the ticker fails loudly — 0 of the 370 committed findings files would have),
retries, and `stock block empty`. Failed tickers keep their ledger.

**Traffic proof.** llama-server has no request counter, but its token
counters are exact: over a run, Δ`tokens_predicted_total` and
Δ(`prompt_tokens_total` + `prompt_tokens_cached_total`) equal the summed
`usage` the harness recorded (verified against a live llama-server b11347).
`make slm-eval-run` snapshots `/metrics` before and after and reconciles
them with the harness's tokens over **every attempt**
(`scripts/slm_traffic_proof.py`): the aggregate's `SLM_TRAFFIC` line, which
covers the final attempt of each ticker, plus the calls of every failed
attempt Argo retried, read back from the pod logs (next paragraph). EXACT,
LOWER-BOUND (excess only from calls the harness saw fail), or FAIL; a
failed attempt that left no complete call record can never be explained
away as LOWER-BOUND. Each SLM ticker also fails if any agent call was
served by anything but its arm's endpoint. **A run is citable as an SLM
result only on EXACT, or on LOWER-BOUND with every excess token attributed
to calls the harness itself logged as failed.** Any FAIL — including an
explained one — is not citable.

**Retried attempts stay visible** (since the image after `30c832b`; added
after smoke `9jddz`). The workflow retries a failed eval pod once and hands
the aggregate only the final attempt, so a failed attempt used to vanish
from the report and from the proof. Now every eval pod writes, to its own
log, `EVAL_ATTEMPT_BEGIN`, one `EVAL_LLM_CALL` line per LLM call as it
returns (tokens and the truncation / loop / parse / format / error flags),
and `EVAL_ATTEMPT_END` with the outcome and cause on every exit Python
still controls; the attempt number is Argo's `{{retries}}`, checked on
Argo v3.7.18. `eval/attempts.py` reads the workflow object and the pod
logs and reports the number of retries, the tickers, and for each failed
attempt Argo's message, the cause from the pod log, its LLM calls per site
and its failure counts — labelled as from failed attempts, never merged
into the final-attempt table. `make eval-run` prints that report under the
aggregate's output and writes it to `~/<workflow>-attempts.json` for the
capture steps; the aggregate itself names the retried tickers (the
aggregate pod cannot read other pods' logs and is given no RBAC to, so the
detail comes from the run report). A pod that is killed (deadline, out of memory) leaves its
calls but no END record: its record is marked incomplete and its listed
calls are a lower bound.

**RAG faithfulness — a separate, unvalidated metric.** The main judge treats
the RAG answers as source text, so an unfaithful RAG answer reads as
supported there. With `EVAL_RAG_FAITHFULNESS=true` (on in `oke-provided`,
every arm) each RAG answer is judged against exactly the chunks it was
written from (`eval/rag_faithfulness.py`, prompt `rf-v1`, Sonnet,
temperature 0). No human labels exist for `rf-v1`: report it as a
judge-flagged rate, in its own column, never folded into the grounding rate.

**Reporting.** Each SLM arm against the hosted baseline arm run on the SAME
pinned OKE image (`argo/eval-run-extended.yaml`); unsupported rate with
Wilson 95% CI, Fisher exact vs that baseline, per-section attribution
(`eval/section_attribution.py`), parse/format failures, stock-block-empty
count, the judge v2 calibration note; CPU vs GPU in one table only with the
quant stated (both Q4_K_M here). **Numeric claims are co-primary with the
rate**: numeric claims per ticker (claims that quote a figure) and the
unsupported rate over numeric claims sit beside every all-claims rate,
with claims per ticker (mean, min) — in the aggregate, and in
`eval/multi_arm_stats.py`, which runs `eval/claim_density.py` itself —
because an arm that states fewer checkable facts gets a lower unsupported
rate for free, and the count of qualitative claims is judge noise ("Dated
finding: claim density" below). Retries and failed attempts are reported
with the run. Dated runs only.

### Smokes on image `2dd1aa3` (2026-10-03): dated, to be re-run on the next image

Two 10-ticker smokes on the provided OKE cluster, same pinned image
(`ghcr.io/schen9999/financial-agent-app:2dd1aa38…`), judge v2, RAG cap 512.
They validate the platform and the SLM path; they are not numbers of
record, and 10 tickers cannot separate the arms (the intervals overlap).
Rates are judge-flagged (v2; the September calibration (2026-09-24) applies, and no
reweighted estimate exists for these runs).

| Run | Arm | Unsupported | Wilson 95% CI | Agent LLM calls | Pipeline per ticker | RAG answers cut at 512 |
|---|---|---|---|---|---|---|
| `x2cx8` | hosted baseline | 2/84 = 2.38% | 0.7–8.3% | 70 (7.0/ticker); the aggregate printed 90, see below | 26.4 s | 0 of 20 |
| `nb6r6` | `slm-full-cpu`, traffic proof EXACT | 3/73 = 4.11% | 1.4–11.4% | 70 (7.0/ticker) | 355.9 s | 13 of 20 (highlights 9/10, risks 4/10) |

`nb6r6`'s proof: 70 calls, 92,282 prompt + 22,466 completion tokens on the
harness side and on the server's `/metrics` over the run
(`eval/runs/slm-proof-nb6r6/`). Both smokes re-run on the next image (the
lock fix and the 2048 RAG cap change it), before any extended run.

**Dated finding: the hosted RAG ledger rows of `x2cx8` are double-counted.**
The aggregate reported 20 calls on each RAG site and 9.0 agent calls per
ticker for the hosted arm, against 10 and 7.0 for the SLM arm. The hosted
path makes one RAG answer call per query, like the SLM path. The brief's two
RAG queries run in two threads; both reached `_ensure_settings()` in
`agent/tools/rag.py` before either had finished loading the embedding model,
and each registered its own usage handler, so every hosted RAG answer was
written to the ledger twice. The SLM arm was unaffected (that handler skips
SLM responses; the adapter records its own). Evidence, from the workflow
object (`eval/runs/x2cx8-workflow.json`): every (ticker, site) has exactly
two rows with the same tokens and the same latency (total = 2 × max to
within 0.01 s, all 20 pairs), and TSLA's two risk-answer rows sum to 11.79 s
inside a 7.09 s retrieval stage. Corrected, per real call:

| Site | Calls | Prompt tokens | Completion tokens | Median | p95 | Max | Truncated |
|---|---|---|---|---|---|---|---|
| `rag:highlights` | 10 | 26,568 | 2,728 | 280 | 353 | 365 | 0 |
| `rag:risks` | 10 | 25,352 | 3,613 | 366 | 435 | 456 | 0 |
| both | 20 | 51,920 | 6,341 | 338 | 412 | 456 | 0 |

(completion tokens per answer; p95 interpolated — with 10 answers per site
it sits just under the max). Reproduce:

```bash
python scripts/rag_ledger_from_workflow.py eval/runs/x2cx8-workflow.json
```

Not affected: the grounding counts and the gate; the run's estimated cost
($1.0318), which is built from chars/4 estimates of the sections, synthesis
and judge plus the RAG-faithfulness judge's recorded usage and never
included the RAG answer calls; and the **cost of record** — the handler was
introduced on 2026-10-02 (commit `1a417be`, branch `slm-harness` only),
`scripts/cost_report.py` counts RAG tokens through its own single
`TokenCountingHandler`, and its recorded RAG input tokens for AAPL / NVDA /
JPM (4,868 / 5,927 / 5,003, `cost_record_post_fix.json`) equal the corrected
x2cx8 figures for the same tickers token for token. Fix: a lock around the
one-time setup (which also loads the embedding model once per pod instead
of twice); `tests/test_rag_settings.py` holds one handler and one ledger
row per API call under two concurrent callers.

**Resource readings** (`kubectl top` every 15 s;
`eval/runs/top-hosted-smoke.txt`, `eval/runs/top-cpu-smoke.txt`; e.g.
`grep llamacpp eval/runs/top-cpu-smoke.txt | sort -k2 -n | tail -1`).
Hosted smoke: eval pods 3–6 millicores at steady state, ~600 MiB each; the
one 560m reading is startup (imports and the embedding-model load) — the
same pod reads 6m in the next sample. CPU smoke: the llama.cpp pod peaked
at 7,998m, saturating its 8-CPU limit (8 vCPU = 4 physical cores with SMT),
and at 27,424 MiB of its 30Gi; the harness beside it is near idle (worker ≤
43m, api ≤ 5m, eval pods single-digit millicores at steady state with
490–780m startup spikes). The CPU arm's 355.9 s per ticker against 26.4 s
hosted is therefore the endpoint's time, not the harness's. Untested, for
the later concurrency sweep: the server ran `--threads 8` on 4 physical
cores and no other thread count was tried.

### RAG natural-length pre-check on the GPU endpoint (2026-10-03, a dated check)

A truncated answer only says the model wanted more than the cap. To size
the shared cap, `nb6r6`'s 20 RAG answer calls were replayed with nothing
cutting them: the prompts rebuilt from the smoke's captured log through
the real query-engine path (`scripts/rag_natural_length.py build`), the
`rag` site's sampling unchanged (temperature 0.1, every sampler explicit,
thinking off), `max_tokens` 4096, sent to the GPU endpoint on node 2
(`localhost:30880`, served alias `qwen3.6-35b-a3b-q4km`, build
`b11347-5fc4f3c8c`, all layers on the A10), two at a time, one sample per
prompt. **Prompt check EXACT, 20 of 20**: the GPU server counted exactly
the prompt tokens `nb6r6`'s ledger recorded on the CPU endpoint for each
request, so these are the smoke's prompts and the two endpoints tokenize
them identically. Every answer ended on its own (`finish_reason` stop).

| Site | n | Min | Median | p95 | Max | > 512 | > 800 | > 1024 | Hit 4096 |
|---|---|---|---|---|---|---|---|---|---|
| `rag:highlights` | 10 | 482 | 668 | 795 | 799 | 9 | 0 | 0 | 0 |
| `rag:risks` | 10 | 101 | 449 | 738 | 854 | 3 | 1 | 0 | 0 |
| both | 20 | 101 | 577 | 802 | 854 | 12 | 1 | 0 | 0 |

(completion tokens; p95 interpolated; the max is MSFT `rag:risks`.)

**CPU vs GPU length, where the CPU smoke was not truncated.** Seven of the
smoke's 20 answers ended on their own on the CPU endpoint; the same
prompts on the GPU endpoint gave:

| Ticker, site | CPU smoke `nb6r6` | GPU pre-check | Difference |
|---|---|---|---|
| AMZN `rag:risks` | 325 | 323 | −2 |
| AAPL `rag:highlights` | 487 | 482 | −5 |
| JPM `rag:risks` | 494 | 472 | −22 |
| TSLA `rag:risks` | 403 | 426 | +23 |
| WMT `rag:risks` | 150 | 101 | −49 |
| META `rag:risks` | 333 | 389 | +56 |
| GOOGL `rag:risks` | 326 | 401 | +75 |

Three agree within 22 tokens and four differ by 23 to 75. These are
independent samples at temperature 0.1 on two builds of one engine (CPU
and CUDA), so token-for-token equality is not expected; the lengths are of
the same order in both directions (median difference −2). One more
data point on that variance: AAPL `rag:risks` hit the 512 cap on the CPU
smoke and finished at 486 on the GPU. The pre-check therefore measures a
length distribution from one sample per prompt, not a fixed length per
prompt.

**Cap decision: 2048 for both arms.** 1024 would have cut none of these 20
answers, but the margin over the measured max (854) is 1.2×, on 10
tickers. The extended runs send 4× the prompts over a wider set of
filings, and the hosted arm already shows how far the tail moves: its
10-ticker smoke peaked at 456 tokens, yet on the 40-ticker set the SFIX
risk-factors answer reached the 512 cap. 2048 is 2.4× the measured SLM
max. It is a ceiling, not a target, and truncations are still counted in
every run — a non-zero `Trunc` on a RAG site at 2048 is a finding to
report, not something the cap is assumed to prevent. On the hosted arm the
change only raises `max_tokens` in the request (smoke max 456; see the
`j4cnp` caveat under "Request settings"). On the CPU arm the RAG stage
will take longer than `nb6r6`'s, since answers the smoke cut at 512 now
run to their natural length (median 577); the run-time gate re-measures
that on the re-smoke.

This is a dated check of 20 answers, not a number of record, and not an
eval run: no traffic proof applies and it says nothing about grounding.
Results: `eval/runs/rag-natural-length-gpu-nb6r6.{txt,json}`. Reproduce:

```bash
python scripts/rag_natural_length.py build \
  --log eval/runs/slm-proof-nb6r6/grounding-eval-slm-cpu-nb6r6.log \
  --out eval/runs/rag-natural-length-requests-nb6r6.json
# node 2 (stdlib only), nothing else using the endpoint:
LLAMA_API_KEY=... python3 scripts/rag_natural_length.py run \
  --requests eval/runs/rag-natural-length-requests-nb6r6.json \
  --url http://localhost:30880 --api-key-env LLAMA_API_KEY \
  --out ~/rag-natural-length-gpu-nb6r6.json
```

### Smokes on image `30c832b` (2026-10-03): dated; the CPU run's traffic proof is FAIL, explained

The re-smokes on the image with the lock fix and the 2048 RAG cap, same 10
tickers, judge v2 (judge-flagged rates; no reweighted estimate exists for
these runs). Not numbers of record.

| Run | Arm | Unsupported | Wilson 95% CI | Claims / ticker (mean, min) | Numeric claims / ticker | Numeric unsupported | Agent LLM calls | Pipeline per ticker | RAG answers truncated | Traffic proof |
|---|---|---|---|---|---|---|---|---|---|---|
| `hm527` | hosted baseline | 1/90 = 1.11% | 0.2–6.0% | 9.0, 3 | 6.1 | 0/61 (CI 0.0–5.9%) | 70 (7.0/ticker) | 26.9 s | 0 of 20 (max 564 tokens) | n/a (hosted) |
| `9jddz` | `slm-full-cpu` — **not citable** | 1/53 = 1.89% | 0.3–9.9% | 5.3, 2 | 3.1 | 0/31 (CI 0.0–11.0%) | 70 (7.0/ticker), final attempts | 345.2 s | 0 of 20 (max 877 tokens) | **FAIL, explained** |

What the image changed, as measured: the hosted ledger now shows 10 rows
per RAG site and 70 calls (the double count is gone); no RAG answer was
truncated in either arm (`scripts/rag_ledger_from_workflow.py` on each
run's workflow object). The SLM answers ran to a median of 585 and a max of
877 tokens, in line with the pre-check (577, 854). One hosted answer
reached 564 tokens — above the old 512 cap — so the "not the `j4cnp`
pipeline exactly" caveat already applies on the 10-ticker set.

**`9jddz`: traffic proof FAIL, explained: one retry (NVDA) after credit
exhaustion.** The Anthropic balance ran out during the run. The first NVDA
attempt (`eval-ticker(1:NVDA)(0)`, pod `…-eval-one-2600813302`) finished
its SLM generation, then hit the credit-balance 400 at the judge; the
harness's guard stopped the pod with `FATAL: Anthropic credit balance too
low` (exit 1), as designed. Argo retried NVDA after the balance was
reloaded, and that attempt succeeded. The aggregate and the proof saw only
the final attempts: harness 94,573 prompt + 24,754 completion tokens,
server 104,696 + 27,697 — the server counted 10,123 prompt + 2,943
completion tokens more. NVDA's successful attempt sent 10,109 + 2,939
tokens, so the excess is the size of one NVDA brief to within 14 + 4
tokens. That is consistent with the failed attempt, not a reconciliation:
image `30c832b` did not log a failed attempt's calls, so what that attempt
sent was never recorded. The verdict stays **FAIL** — it is not rewritten
as a pass, and under the proof rule this run is **not citable** as an SLM
result. Its figures are kept here as a dated record, always with that
status; the CPU baseline is the next CPU smoke (`wnrjr`, on `1f51dad`:
traffic proof EXACT — "CPU SLM extended run `8vpq6`" below), on the image that logs
failed attempts.
Re-running the proof with the attempt-aware verifier gives the same
verdict with the reason spelled out:

```bash
python eval/attempts.py --workflow eval/runs/9jddz-workflow.json \
  --log eval/runs/slm-proof-9jddz/grounding-eval-slm-cpu-9jddz.log
python scripts/slm_traffic_proof.py verify \
  --before eval/runs/slm-proof-9jddz/grounding-eval-slm-cpu-9jddz-before.json \
  --after eval/runs/slm-proof-9jddz/grounding-eval-slm-cpu-9jddz-after.json \
  --log eval/runs/slm-proof-9jddz/grounding-eval-slm-cpu-9jddz.log \
  --workflow eval/runs/9jddz-workflow.json     # TRAFFIC PROOF: FAIL
```

Both smokes re-run on the next image (attempt logging and the claim-density
lines change it) before any extended run.

### Dated finding: claim density differs between the arms, and between judge passes (2026-10-03)

The hosted smoke `hm527` produced 90 judged claims and the CPU SLM smoke
`9jddz` 53, over the same 10 tickers on the same image; the earlier SLM
smoke `nb6r6` had 73. AMZN, GOOGL and V each have 2 claims in `9jddz`. The
unsupported rate divides by judged claims, so this matters to every
SLM-vs-hosted comparison. From `eval/claim_density.py`:

| Run | Arm | Claims / ticker (mean, min) | Numeric claims / ticker (mean, min) | Numeric unsupported | Qualitative claims / ticker | Briefs audited on numbers only | Audited words / ticker | Numbers in audited text / ticker |
|---|---|---|---|---|---|---|---|---|
| `x2cx8` | hosted | 8.4, 4 | 5.8, 3 | 0/58 (CI 0.0–6.2%) | 2.6 | 3 of 10 | 338 | 5.9 |
| `hm527` | hosted | 9.0, 3 | 6.1, 3 | 0/61 (CI 0.0–5.9%) | 2.9 | 3 of 10 | 347 | 6.2 |
| `nb6r6` | SLM CPU | 7.3, 2 | 3.5, 2 | 0/35 (CI 0.0–9.9%) | 3.8 | 3 of 10 | 200 | 3.7 |
| `9jddz` | SLM CPU (not citable) | 5.3, 2 | 3.1, 2 | 0/31 (CI 0.0–11.0%) | 2.2 | 5 of 10 | 201 | 3.1 |
| `j4cnp` | hosted, 40 tickers | 9.8, 4 | 6.5, 2 | 4/260 = 1.54% (CI 0.6–3.9%) | 3.2 | 9 of 40 | 338 | 8.1 |

("Numeric" = the judge's quoted claim contains a digit,
`eval.label.numeric_claim_counts`; audited text = Executive Summary +
Outlook without headings and the disclaimer. The numeric rate is a
judge-flagged rate over a subset of the claims: the v2 calibration was
measured over all claims and has not been repeated for this subset, and
`j4cnp`'s rate, the number of record until 2026-10-05, is 12/392 over all
claims.)

Two separate effects:

1. **The SLM writes less, and half the numbers.** Its audited text is about
   200 words against the hosted arm's ~340, with ~3 numbers against ~6, in
   both SLM smokes. It follows the synthesis prompt to the letter: a
   three-sentence Executive Summary that cites two figures in its first
   sentence, and a one-paragraph Outlook with no figure at all (the prompt
   asks for a qualitative Outlook and forbids invented numbers). The hosted
   model writes longer sentences that carry more figures and more named
   specifics. No section is missing in any brief, and nothing was truncated.
   Numeric claims track this directly: the judge extracted almost exactly
   the numbers present (3.1 claims for 3.1 numbers in `9jddz`, 6.1 for 6.2
   in `hm527`).
2. **Whether the judge audits qualitative phrases varies from brief to
   brief, and that swings the count.** The v2 prompt asks for quantitative
   figures, named milestones and forward-looking numbers. Sometimes the
   judge also lists qualitative phrases as claims, sometimes it declares
   them out of scope. `nb6r6` and `9jddz` have the same amount of SLM text;
   numeric claims fell by 4 (35 to 31) and qualitative claims by 16 (38 to
   22). GOOGL is the clearest case: 11 claims in `nb6r6`, of which 9 are
   phrases such as "dominant market position" and "strong cash generation"
   (two of them labelled UNSUPPORTED), and 2 claims in `9jddz`, where the
   judge wrote that everything but the two figures was qualitative and
   outside the audit. The hosted arm shows the same instability: V has 6
   claims in `x2cx8` and 16 in `hm527`, 10 of them qualitative.

For the three 2-claim briefs in `9jddz` (AMZN, GOOGL, V) both effects
coincide: each has exactly two figures, both in the Executive Summary; the
Outlook is hedged and conditional but, more to the point, contains no
number; and the judge audited numbers only in all three. Hedged wording is
not what removed the claims — the hosted Outlooks are hedged the same way,
and judge v2 treats a hedged claim like any other — the absence of
checkable specifics is.

In one sentence each, for the record:

- **The SLM synthesis states about half the figures of the hosted one —
  3.1 against 6.1 numeric claims per ticker (`9jddz` vs `hm527`) — because
  it follows the synthesis prompt literally.**
- **Judge v2's listing of qualitative claims varies from run to run (GOOGL
  11 claims vs 2 across the two SLM smokes; V 6 vs 16 across the two
  hosted smokes). This is recorded, not fixed: changing the judge's claim
  scope would be a new judge version and would need its own calibration.**

Consequences, applied from the next image on:

- **Numeric claims are the co-primary metric.** Every all-claims rate is
  reported with numeric claims per ticker (mean, min) and the unsupported
  rate over numeric claims; claims per ticker (mean, min) stays beside
  them. The numeric count is the stable part: it follows the numbers in
  the text, not the judge's pass. The aggregate prints these lines (each
  result row carries its numeric counts), and `eval/multi_arm_stats.py`
  leads with the numeric comparison and runs `eval/claim_density.py`
  itself. Supported claims per ticker was considered as the co-primary and
  rejected: it carries the qualitative-claim noise.
- A lower SLM unsupported rate is not evidence of better grounding unless
  the density is comparable; state both. On these smokes the SLM's rate is
  over about half as many checkable figures.
- In all four smokes every unsupported claim was a qualitative one: the
  numeric unsupported count is 0 in each (0/58, 0/61, 0/35, 0/31; note the
  wide intervals). The all-claims rates of the smokes therefore measure
  qualitative claims only — the part the judge lists inconsistently (2 of
  `nb6r6`'s 3 unsupported claims were GOOGL's qualitative phrases).

```bash
python eval/claim_density.py --run x2cx8 eval/runs/raw/x2cx8-findings \
  --run hm527 eval/runs/raw/hm527-findings --run nb6r6 eval/runs/raw/nb6r6-findings \
  --run 9jddz eval/runs/raw/9jddz-findings --run j4cnp eval/runs/raw/j4cnp-findings \
  --tickers AMZN GOOGL V
python eval/multi_arm_stats.py --run hosted-hm527 eval/runs/hm527-claims.jsonl eval/runs/raw/hm527-findings \
  --run slm-cpu-9jddz eval/runs/9jddz-claims.jsonl eval/runs/raw/9jddz-findings
```

### Hosted smokes on the 10-ticker set: smoke-level run-to-run variance (2026-10-03)

Three hosted-baseline smokes on the same 10 tickers, judge v2, on three
consecutive images of the same pipeline. Dated runs; none is a number of
record. Rates are judge-flagged (v2; no reweighted estimate exists for these
runs).

| Run | Image | RAG cap | Unsupported | Wilson 95% CI | Gate (≤ 5%) | Numeric unsupported | Qualitative claims listed | MSFT claims (numeric + qualitative) | MSFT unsupported |
|---|---|---|---|---|---|---|---|---|---|
| `x2cx8` | `2dd1aa3` | 512 ¹ | 2/84 = 2.38% | 0.7–8.3% | passed | 0/58 | 26 | 6 + 1 | 0 |
| `hm527` | `30c832b` | 2048 | 1/90 = 1.11% | 0.2–6.0% | passed | 0/61 | 29 | 9 + 0 | 0 |
| `7c66k` | `1f51dad` | 2048 | 8/101 = 7.92% | 4.1–14.9% | **FAILED** | 0/59 | 42 | 8 + 14 | 8 |

¹ `x2cx8` ran under the 512-token RAG cap, the other two under 2048. No
hosted RAG answer was cut in `x2cx8` (max 456 tokens), so the cap did not
bind in that run.

**This is smoke-level run-to-run variance, and `7c66k`'s gate failure is
one ticker.** All 8 of its unsupported claims are on MSFT; the other nine
tickers have none. The judge listed 14 qualitative claims for MSFT in
`7c66k`, against 1 in `x2cx8` and 0 in `hm527`, and labelled 8 of them
UNSUPPORTED. Numeric unsupported is 0 in all three runs, and all 11
unsupported claims across the three are qualitative. The gate and the
judge are unchanged; `7c66k` stays recorded as a failed gate.

**What did not change between the runs.** MSFT's retrieved chunks are
identical in the three runs for both RAG queries, and the stock, news and
SEC-summary blocks of every ticker are byte-identical between `hm527` and
`7c66k`. The three MSFT syntheses say the same things, several near
verbatim: `hm527`'s Outlook has "The primary tailwind is the secular
enterprise demand for AI-integrated workflows, where Microsoft's deep
customer relationships and existing platform footprint provide a
meaningful distribution advantage", and `x2cx8`'s has "evidence of AI
monetization gaining traction" and "watch the trajectory of profit margins
as AI infrastructure spending scales" — none listed by the judge in those
runs. `x2cx8` also has "uncertain returns on accelerating capital
expenditure" inside a claim the judge labelled SUPPORTED; in `7c66k` the
same wording is two of the eight UNSUPPORTED claims.

**The eight claims** (all from the Outlook or the Executive Summary's
last sentence; full text and the judge's reasons in
`eval/runs/raw/7c66k-findings/MSFT_baseline.md`):

- Absent from the context — the model's own knowledge or an editorial
  assertion: "The primary tailwind is the secular enterprise demand for
  cloud infrastructure and AI-integrated productivity tools"; "Microsoft's
  deeply embedded customer relationships and broad platform footprint
  provide a durable distribution advantage".
- Watch-items and conditions naming a metric the context does not
  contain: "watch the trajectory of cloud and AI services margins …";
  "watch competitive win-rate signals in cloud workloads …"; "… would
  strengthen if margin trends hold or improve alongside evidence of AI
  monetization gaining traction".
- Judge strictness on a qualifier: "accelerating capital expenditures for
  AI infrastructure" and "the uncertain return timeline on accelerating
  capital expenditures" (the context says "substantial capital
  expenditures on an accelerated timeline"); "… the company's historically
  strong profitability" (the context has one period's margin).

**Interpretation.** The same ungrounded MSFT content appeared in all three
syntheses. The lower runs are judge misses, not cleaner briefs — consistent
with judge v2's population-weighted recall on UNSUPPORTED (32.5% on the
baseline run, CI 16.0–52.4%; pooled 47.9%, CI 26.5–68.3%; "Calibration of
record"). A 10-ticker smoke's all-claims rate is dominated by which
qualitative phrases the judge lists in that pass: one ticker moved the
rate from 1.11% to 7.92% with nothing else changing. So a smoke validates
the platform and the plumbing (calls, truncation, retries, traffic proof);
it does not rank arms. **Arms are compared on the extended runs, numeric
co-primary first.**

**Two known limitations, recorded and deliberately not changed.** Fixing
either changes the pipeline and requires new baselines on every arm, so
neither changes during this comparison; both are post-demo work.

1. *Synthesis prompt and judge interact.* The synthesis prompt asks the
   Outlook to "name the key variables an investor should watch" and gives
   metric-style examples; judge v2 labels a hedged watch-item UNSUPPORTED
   when the context lacks the metric it names (check 1: hedging does not
   downgrade a missing fact). Every arm runs the same prompt and the same
   judge, so every arm carries this — whenever the judge lists the
   watch-item at all.
2. *The highlights RAG query reaches only risk-factor text for half the
   smoke tickers.* For AMZN, JPM, MSFT, NVDA and WMT the highlights query
   retrieves only Item 1A chunks in all three runs, so the RAG highlights
   answer is a refusal ("I cannot provide a summary of the latest 10-K and
   10-Q … only excerpts from the Risk Factors section"), and the brief's
   "SEC Filing Highlights" section is itself a refusal for 4–5 of the 10
   briefs each run (5 in `x2cx8`, 4 in `hm527` and `7c66k`). MSFT's Item
   1A anchor is working here (its first chunk starts "ITEM 1A. RISK
   FACTORS"); the limit is what the index holds, not a failed anchor. It
   leaves those briefs' Outlooks with little context to stand on when the
   judge does list their qualitative phrases.

```bash
python eval/claim_density.py --run x2cx8 eval/runs/raw/x2cx8-findings \
  --run hm527 eval/runs/raw/hm527-findings --run 7c66k eval/runs/raw/7c66k-findings --tickers MSFT
python eval/compare_runs.py contexts --a hm527 eval/runs/raw/hm527-findings --b 7c66k eval/runs/raw/7c66k-findings
# RAG highlights refusals, and SEC Filing Highlights sections that are refusals, per run:
grep -lE '^\[From Pinecone cache\] I cannot provide a summary' eval/runs/raw/7c66k-findings/*_baseline.md
for f in eval/runs/raw/7c66k-findings/*_baseline.md; do
  grep -A2 '^### SEC Filing Highlights' $f | grep -qE 'cannot provide|Unable to provide' && basename $f _baseline.md
done
# MSFT's retrieved chunks, identical across the three runs:
python -c "import json; c=[json.load(open(f'eval/runs/raw/{r}-findings/MSFT_baseline.ragf.json',encoding='utf-8'))['answers'] for r in ('x2cx8','hm527','7c66k')]; print(all(a[w]['chunks']==c[0][w]['chunks'] for a in c for w in ('highlights','risks')))"
```

### Hosted extended run `9jzmj` on image `1f51dad` (2026-10-04): the same-image hosted baseline

**Status, stated first: workflow Error at aggregate (controller lacked
configmaps create for template offload); rebuilt offline from all 40 pod
findings dumps; gate evaluated offline; est. run cost not reconstructable.**

`grounding-eval-extended-9jzmj` ran the 40-ticker set on the hosted baseline
arm, judge v2, image `1f51dad` — the image the SLM extended runs use. All 40
eval pods completed on their first attempt; the aggregate step never
started (next section), so the workflow's phase is Error and no in-cluster
aggregate exists. The aggregate below is `scripts/eval_aggregate.py` — the
same code, unchanged since the image commit — run on per-ticker rows rebuilt
from the pods' logs by `scripts/results_from_pod_log.py`.

| | `9jzmj` (rebuilt offline) |
|---|---|
| Unsupported (judge-flagged, v2) | 7/411 = 1.70% (Wilson 95% CI 0.8–3.5%) |
| Numeric claims (co-primary) | 277 = 6.9/ticker (min 1, RDFN); unsupported 2/277 = 0.72% (CI 0.2–2.6%) |
| Claims per ticker | mean 10.3, min 2 (AMZN) |
| Tickers | 40 completed, 0 skipped, stock block empty 0/40, 0 Argo retries |
| Unsupported by ticker | LCID 3, AFRM 2, CHGG 1, NVO 1 |
| Agent LLM calls | 270 (35 tickers × 7, and 5 tickers × 4 with no RAG answer: BABA, NVO, SAP, TM, TSM); no truncation, loop, parse, format or error flags |
| RAG answers | 70; longest 786 tokens (above the old 512 cap) |
| Gate (≤ 5%, ≥ 30 claims) | passed — evaluated offline |
| Estimated run cost | not reconstructable from the pod logs (it needs each brief's full text); $4.0998 per the rows stored in the workflow object, below |

This is a judge-flagged rate with the v2 September calibration (2026-09-24) applying; no
reweighted estimate exists for this run. It is a dated run: `j4cnp` stays
the number of record. `9jzmj` is the hosted arm on the comparison's own
image — the pipeline with the 2048 RAG cap, so not the `j4cnp` pipeline
exactly (see "Request settings").

**Why the rebuild can be trusted.** The rows the aggregate would have
received were Argo output parameters, which are not in the pod logs; what
they were computed from is. For each pod the rebuild takes the label counts
by recounting its findings dump with the harness's own function, the
numeric counts and the stock-block check the same way, the per-site LLM
ledger from the findings metadata, the RAG-faithfulness verdicts from the
pod's `.ragf.json`, retrieval and pipeline time from the pod's result line
and the attempt from its END record. It stops rather than guess if a
pod's printed counts differ from the recount, if its `EVAL_LLM_CALL` lines
disagree with its ledger in calls or tokens, or if an attempt did not end
ok; none of that happened on either run.

**Validation on `7c66k`** (same image, and it has a real in-cluster
aggregate): the aggregate run on rows rebuilt from `7c66k`'s pod logs
reproduces the cluster's printed aggregate **exactly — all 41 lines except
the estimated-cost line**: every per-ticker row, the totals, 8/101 = 7.92%
with its CI, numeric 0/59, the full per-site LLM table, the
RAG-faithfulness line and the GATE FAILED verdict.
`tests/test_results_from_pod_log.py` holds this against the committed
files. On that basis `9jzmj` is citable as the same-image hosted extended
baseline, always with the status line above.

**Second confirmation, from the workflow object itself**
(`eval/runs/9jzmj-workflow.json`, fetched read-only 2026-10-04). The
object still holds the output parameter each eval pod handed back — the
exact rows the aggregate step would have received. Running the same
aggregate on those 40 stored rows prints the same report as the pod-log
rebuild, line for line, plus the one line the rebuild cannot produce:
`est. run cost : $4.0998`. Field by field, the rebuilt rows equal the
stored ones in everything the aggregate reads (counts, numeric counts,
attempt, judge version, stock-block flag, timings to the printed two
decimals, the per-site and per-endpoint ledger, RAG-faithfulness verdicts).
The object also confirms the failure and the attempt count independently
of the logs: 83 nodes — 40 eval pods Succeeded, each on attempt 0, and the
aggregate node in Error with the `configmaps is forbidden` message.

```bash
python scripts/workflow_nodes.py results eval/runs/9jzmj-workflow.json > /tmp/9jzmj-stored-rows.json
python scripts/eval_aggregate.py --input /tmp/9jzmj-stored-rows.json     # same report + est. run cost
python scripts/workflow_nodes.py expand eval/runs/9jzmj-workflow.json > /tmp/9jzmj-expanded.json
python eval/attempts.py --workflow /tmp/9jzmj-expanded.json --log eval/runs/raw/9jzmj.log   # 40 pods, 0 retries
```

```bash
python scripts/results_from_pod_log.py --log eval/runs/raw/7c66k.log \
  --out eval/runs/7c66k-results-rebuilt.json --aggregate-out eval/runs/7c66k-aggregate-rebuilt.txt
#   VALIDATION: EXACT apart from the estimated-cost line
python scripts/results_from_pod_log.py --log eval/runs/raw/9jzmj.log \
  --out eval/runs/9jzmj-results-rebuilt.json --aggregate-out eval/runs/9jzmj-aggregate.txt
# from the committed rows alone (the raw logs are not committed):
python scripts/eval_aggregate.py --input eval/runs/9jzmj-results-rebuilt.json
```

### CPU SLM extended run `8vpq6` against hosted `9jzmj` (2026-10-04): the same-image comparison

`grounding-eval-extended-slm-cpu-8vpq6`: the 40-ticker set on the
`slm-full-cpu` arm (Qwen3.6-35B-A3B Q4_K_M on llama.cpp b11347, CPU
endpoint on the provided OKE cluster), judge v2, image `1f51dad`. Workflow
Succeeded; 40 of 40 tickers on the first attempt, 0 Argo retries;
**TRAFFIC PROOF: EXACT** over every attempt (270 calls, 342,244 prompt +
96,811 completion tokens on the harness and on the server); no truncation,
loop, parse, format or error flag on any call; gate passed. It is a dated,
citable SLM run. Its aggregate step was the first live use of the template
offload on OKE (template 301,083 bytes, 2.30× the inline limit; next
section). The CPU smoke on the same image that fed the run-time gate is
`wnrjr`: 1/58 = 1.72% (Wilson 95% CI 0.3–9.1%), numeric 0/33, traffic proof
EXACT (94,520 + 24,756 tokens), 0 retries.

**Headline: no grounding difference detected at this sample size; numeric
density is the separated result.** Rates are judge-flagged (v2; the
September calibration (2026-09-24) applies and no reweighted estimate exists for either
run). When written (2026-10-04) `j4cnp` stayed the grounding number of
record; since 2026-10-05 this run and `9jzmj`, with GPU `p9jr2`, are the
grounding numbers of record (the same-image three-way, below).

| | Hosted `9jzmj` | CPU SLM `8vpq6` | Test |
|---|---|---|---|
| Unsupported, all claims | 7/411 = 1.70% (CI 0.8–3.5%) | 9/248 = 3.63% (CI 1.9–6.8%) | Fisher exact p = 0.126 |
| Unsupported, numeric claims (co-primary) | 2/277 = 0.72% (CI 0.2–2.6%) | 3/161 = 1.86% (CI 0.6–5.3%) | Fisher exact p = 0.362 |
| — sensitivity: without claims numeric only through "52-week" | 2/271 = 0.74% (CI 0.2–2.7%) | 2/158 = 1.27% (CI 0.3–4.5%) | Fisher exact p = 0.628 |
| Numeric claims per ticker | 6.92 | 4.03 | paired over the 40 tickers: +2.90 (95% bootstrap CI +2.15 to +3.70); hosted higher on 35, equal on 3, lower on 2; exact sign test p = 1e-8 |
| — sensitivity: without "52-week" | 6.78 | 3.95 | paired +2.83 (CI +2.08 to +3.62); 35 / 3 / 2; p = 1e-8 |
| Claims per ticker (mean, min) | 10.3, 2 | 6.2, 2 | |
| Qualitative claims per ticker | 3.3 | 2.1 | |
| Briefs the judge audited on numbers only | 7 of 40 | 16 of 40 | |
| Audited text per ticker | 340 words, 8.9 numbers | 202 words, 4.5 numbers | |
| Unsupported by section: Financial Health | 1/190 | 2/128 | |
| Risk Factors | 0/17 | 0/12 | |
| Recent Developments | 0/36 | 1/17 | |
| SEC Filing Highlights | 0/87 | 0/47 | |
| unattributed (restates no pre-written section) | 6/81 | 6/44 | |
| RAG faithfulness (rf-v1, **unvalidated**, own denominator) | 14/1017 = 1.38% (CI 0.8–2.3%), 70 answers | 6/1415 = 0.42% (CI 0.2–0.9%), 70 answers | Fisher exact p = 0.012 |
| Agent LLM calls | 270 | 270 | |
| Pipeline per ticker, mean (min–max) | 25.9 s (17.6–30.4) | 355.1 s (100.4–432.6) | 13.7× |
| Retrieval per ticker, mean | 5.4 s | 170.0 s | |
| Traffic proof | n/a (hosted) | EXACT | |
| Aggregate | rebuilt offline (above) | in-cluster | |

- **Grounding.** The SLM's rate is higher on every denominator and none of
  the differences is detected: p = 0.126 over all claims, 0.362 over
  numeric claims, 0.628 with the "52-week" phrases removed. This is "no
  difference detected at this sample size", not "equivalent": the
  intervals are wide (the SLM's upper bound is 6.8% over all claims).
- **Density.** The hosted arm states more figures on 35 of the 40 tickers:
  2.90 more numeric claims per ticker (CI +2.15 to +3.70). The SLM's
  audited text is about 40% shorter with half the numbers, as in the
  smokes ("Dated finding: claim density"). The SLM's rate is therefore
  over a little more than half as many checkable figures.
- **RAG faithfulness** is reported side by side with its denominators and
  the unvalidated label, and is not part of the grounding rate. The SLM's
  RAG answers are longer — 1,415 judged claims against 1,017 over the same
  70 answers — so the lower rate is not a validated quality claim: the
  judge has no human-label calibration and the two rates are over
  different amounts of text.

**Latency per call site** (seconds per call, mean and max; the harness's
ledger):

| Site | Hosted mean | Hosted max | CPU SLM mean | CPU SLM max |
|---|---|---|---|---|
| `rag:highlights` (35 calls each) | 4.10 | 5.57 | 186.66 | 251.03 |
| `rag:risks` (35) | 4.47 | 9.17 | 159.76 | 271.11 |
| `section:financial_health` (40) | 2.24 | 3.06 | 46.23 | 82.17 |
| `section:recent_developments` (40) | 2.21 | 2.77 | 50.39 | 90.18 |
| `section:risk_factors` (40) | 2.36 | 3.80 | 62.68 | 106.10 |
| `section:sec_filing_highlights` (40) | 1.96 | 2.96 | 62.79 | 93.22 |
| `synthesis` (40) | 17.86 | 20.47 | 114.45 | 155.76 |

**CPU during `8vpq6`** (`kubectl top` every 15 s, 705 samples,
`eval/runs/top-cpu-ext.txt`): the llama.cpp pod ran at a median of 7,806m
and peaked at 8,000m — its 8-CPU limit — with 27,449 Mi of its 30Gi. The
harness beside it is idle: the 40 eval pods have a median of 1m (10 of 975
readings are startup spikes above 100m, the rest at most 47m), the worker
peaks at 48m and the api at 172m. The 13.7× per-ticker time is the
endpoint's.

**The three numeric unsupported claims of `8vpq6`** — only one is a wrong
number:

- **CHGG — a wrong number (truncation).** Claim: "net income of -$52.9
  million". The context has `net_income: -52997000.0`, which is -$53.0
  million; the SLM wrote -52.997M as -52.9M. The figure was produced in the
  SLM's Financial Health section and carried into the summary. On the same
  data the hosted run wrote "$53 million" (SUPPORTED).
- **BEAM — a context source conflict, judged against the filing.** Claim:
  "reporting a net loss of $86.52 million". The figure is in the context
  and quoted correctly (yfinance `net_income: -86520000.0`). The RAG answer
  from the filing, also in the context, says "net losses of $80.0 million
  (2025)". The judge labelled the claim UNSUPPORTED because the two
  sources disagree and it took the filing as authoritative.
- **META — judge error.** Claim: "strong market sentiment near 52-week
  highs". The price, 728.08, is at 80% of the 52-week range
  (520.26–779.82), 6.6% below the high, and nearer the high than the
  midpoint; the judge wrote that it was closer to the midpoint. The same
  claim on the same data ("shares near 52-week highs") is SUPPORTED in
  `9jzmj`, and MSFT at 82% of its range was SUPPORTED as "near the upper
  end" in `7c66k`. The claim is not a figure at all; it counts as numeric
  only because "52-week" contains digits.

Neither of the hosted arm's two numeric unsupported claims is a wrong
number either: AFRM's is a peer comparison absent from the context, NVO's a
qualitative pipeline statement.

**The "52-week" caveat.** A numeric claim is one whose quoted text contains
a digit (`eval.label.numeric_claim_counts`), so positional phrases such as
"near 52-week highs" count: 6 of the hosted arm's 277 numeric claims and 3
of the SLM's 161. The sensitivity rows above drop them
(`eval/claim_density.py`, strict count); nothing changes direction — the
rate difference shrinks (2/271 vs 2/158) and the density result stands.
Fixing the definition itself is a post-comparison change: it lives in code
the harness runs inside the pinned image, and it is not changed now.

**Two more known limitations, recorded and not changed during the
comparison (post-demo):**

3. *The context can contain conflicting figures from different sources,
   and nothing reconciles or flags them.* BEAM's net income is -$86.52
   million in the yfinance stock block and -$80.0 million in the filing's
   RAG answer (different sources, possibly different periods). The brief
   can quote either, and the judge may hold either against it. Recurring:
   OMER in `p9jr2` is the second instance ("GPU SLM extended run `p9jr2`",
   limitation 3 update).
4. *The SLM truncates where it should round on at least one derived
   figure.* CHGG's -52.997M became -52.9M in the SLM's Financial Health
   section. One observed instance. The numeric check cannot measure how
   often at its 2% tolerance: -52.9M against -52.997M is 0.18% off and
   passes (2026-10-05, "Numeric check on the three-way" below).

```bash
python eval/multi_arm_stats.py \
  --run hosted-9jzmj eval/runs/9jzmj-claims.jsonl eval/runs/raw/9jzmj-findings \
  --run slm-cpu-8vpq6 eval/runs/8vpq6-claims.jsonl eval/runs/raw/8vpq6-findings \
  --rows hosted-9jzmj eval/runs/9jzmj-workflow.json \
  --rows slm-cpu-8vpq6 eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json
python scripts/top_summary.py eval/runs/top-cpu-ext.txt
#   both saved as eval/runs/9jzmj-vs-8vpq6-comparison.txt
python scripts/slm_traffic_proof.py verify \
  --before eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-before.json \
  --after eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-after.json \
  --log eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6.log \
  --workflow eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json   # EXACT
```

### GPU SLM extended run `p9jr2` (2026-10-05): the three-way comparison with hosted `9jzmj` and CPU `8vpq6`

`grounding-eval-extended-slm-gpu-p9jr2`: the 40-ticker set on the
`slm-full-gpu` arm — the same GGUF on the same llama.cpp release as
`8vpq6`, served on node 2's A10 with all layers on the GPU (alias
`qwen3.6-35b-a3b-q4km`, no `-hybrid` suffix, so not a hybrid run), judge
v2, image `1f51dad`. The harness on OKE reaches the endpoint over node 2's
public address, port 30880 admitted from the OKE egress IP only; the
harness's timers include that path. Workflow Succeeded 03:13:00–03:48:12
UTC; 40 of 40 tickers on the first attempt, 0 Argo retries; **TRAFFIC
PROOF: EXACT** (270 calls, 350,290 prompt + 98,232 completion tokens on the
harness and on the server); no truncation, loop, parse, format, retry or
error flag on any call; stock block empty on 0 of 40; gate passed. A dated,
citable SLM run. The GPU smoke on the same image that fed the run-time gate
is `k6zxd` (below).

**Headline: no grounding difference detected on any pair at this sample
size; numeric density separates the GPU from hosted, and does not separate
the GPU from the CPU.** The CPU and GPU arms run the same model, engine
and request settings on different hardware, so they should not differ:
that pair is the consistency check, and it holds. Rates are judge-flagged
(v2; the September calibration (2026-09-24) applies and no reweighted estimate exists
for these runs). The p-values are not adjusted for the three pairwise
comparisons. **Since 2026-10-05 this three-way is the grounding number of
record** ([numbers-of-record.md](numbers-of-record.md)); `j4cnp` is a dated
record with its 512-cap caveat, and no before/after is drawn between them.

| | Hosted `9jzmj` | CPU SLM `8vpq6` | GPU SLM `p9jr2` | GPU vs hosted | GPU vs CPU |
|---|---|---|---|---|---|
| Unsupported, all claims | 7/411 = 1.70% (CI 0.8–3.5%) | 9/248 = 3.63% (CI 1.9–6.8%) | 6/245 = 2.45% (CI 1.1–5.2%) | Fisher p = 0.567 | Fisher p = 0.602 |
| Unsupported, numeric claims (co-primary) | 2/277 = 0.72% (CI 0.2–2.6%) | 3/161 = 1.86% (CI 0.6–5.3%) | 3/155 = 1.94% (CI 0.7–5.5%) | p = 0.355 | p = 1.000 |
| — sensitivity: without claims numeric only through "52-week" | 2/271 = 0.74% (CI 0.2–2.7%) | 2/158 = 1.27% (CI 0.3–4.5%) | 3/148 = 2.03% (CI 0.7–5.8%) | p = 0.351 | p = 0.676 |
| Model errors in numeric claims (wrong value + wrong label + not in context; below) | 2/277 = 0.72% (CI 0.2–2.6%) | 1/161 = 0.62% (CI 0.1–3.4%) | 2/155 = 1.29% (CI 0.4–4.6%) | p = 0.621 | p = 0.617 |
| Numeric claims per ticker | 6.92 | 4.03 | 3.88 | paired +3.05 for hosted (95% bootstrap CI +2.33 to +3.83); hosted higher on 34, equal 5, lower 1; sign test p = 2.1e-9 | paired +0.15 for CPU (CI −0.35 to +0.68); 17 / 6 / 17; p = 1.0 |
| — sensitivity: without "52-week" | 6.78 | 3.95 | 3.70 | +3.08 (CI +2.33 to +3.88); 35 / 4 / 1; p = 1.1e-9 | +0.25 (CI −0.28 to +0.78); 19 / 5 / 16; p = 0.736 |
| Claims per ticker (mean, min) | 10.3, 2 | 6.2, 2 | 6.1, 2 | | |
| Qualitative claims per ticker | 3.3 | 2.1 | 2.2 | | |
| Briefs the judge audited on numbers only | 7 of 40 | 16 of 40 | 15 of 40 | | |
| Audited text per ticker | 340 words, 8.9 numbers | 202 words, 4.5 numbers | 203 words, 4.4 numbers | | |
| Unsupported by section: Financial Health | 1/190 | 2/128 | 3/119 | | |
| Risk Factors | 0/17 | 0/12 | 0/10 | | |
| Recent Developments | 0/36 | 1/17 | 1/29 | | |
| SEC Filing Highlights | 0/87 | 0/47 | 0/51 | | |
| unattributed | 6/81 | 6/44 | 2/36 | | |
| RAG faithfulness (rf-v1, **unvalidated**, own denominator) | 14/1017 = 1.38% (CI 0.8–2.3%) | 6/1415 = 0.42% (CI 0.2–0.9%) | 6/1465 = 0.41% (CI 0.2–0.9%) | p = 0.011 | p = 1.000 |
| Agent LLM calls | 270 | 270 | 270 | | |
| Pipeline per ticker, mean (min–max) | 25.9 s (17.6–30.4) | 355.1 s (100.4–432.6) | 31.1 s (12.5–47.6) | GPU 1.2× slower | CPU 11.4× slower |
| Retrieval per ticker, mean | 5.4 s | 170.0 s | 13.9 s | GPU 2.6× | CPU 12.2× |
| Traffic proof | n/a (hosted) | EXACT | EXACT | | |

Every arm made 270 agent calls: 35 tickers × 7 and 5 × 4. The five ADRs
make no RAG call in any arm (known limitation 5 below).

- **Grounding.** No pair separates on any denominator: all claims, numeric
  claims, the "52-week" sensitivity, or model errors alone. That is "no
  difference detected at this sample size", not "equivalent". The GPU's
  upper bound over all claims is 5.2%, its numeric upper bound 5.5%.
- **Density.** The GPU arm states 3.05 fewer numeric claims per ticker
  than hosted (lower on 34 of 40 tickers), as the CPU arm did, so its rate
  is over a little more than half as many checkable figures. GPU against
  CPU: +0.15 numeric claims per ticker with an interval across zero, 17
  tickers each way and 6 equal, and the same audited length (203 vs 202
  words). Moving the model from CPU to GPU did not change what it writes.
- **RAG faithfulness** is reported side by side, with its denominators and
  the unvalidated label, and is not part of the grounding rate. The GPU
  and CPU arms are indistinguishable (6/1465 vs 6/1415). The SLM's lower
  rate against hosted is over longer answers and is not a validated
  quality claim, as for `8vpq6`.

**Latency per call site** (seconds per call, mean and max, from the
harness's ledger; ratios are slower / faster, from
`eval/multi_arm_stats.py`):

| Site (calls per arm) | Hosted mean | CPU mean | GPU mean (max) | CPU / GPU | GPU / hosted |
|---|---|---|---|---|---|
| `rag:highlights` (35) | 4.10 | 186.66 | 13.94 (24.70) | 13.4× | 3.4× |
| `rag:risks` (35) | 4.47 | 159.76 | 10.69 (25.07) | 14.9× | 2.4× |
| `section:financial_health` (40) | 2.24 | 46.23 | 4.54 (6.23) | 10.2× | 2.0× |
| `section:recent_developments` (40) | 2.21 | 50.39 | 4.77 (7.61) | 10.6× | 2.2× |
| `section:risk_factors` (40) | 2.36 | 62.68 | 5.46 (9.91) | 11.5× | 2.3× |
| `section:sec_filing_highlights` (40) | 1.96 | 62.79 | 5.00 (9.29) | 12.6× | 2.6× |
| `synthesis` (40) | 17.86 | 114.45 | 11.41 (19.50) | 10.0× | hosted 1.6× slower |
| Per ticker, pipeline | 25.86 | 355.06 | 31.15 | 11.4× | 1.2× |
| Per ticker, retrieval | 5.41 | 169.95 | 13.91 | 12.2× | 2.6× |

The GPU is 10–15× faster than the CPU endpoint at every site. Against
hosted it is 2.0–3.4× slower per call everywhere except the synthesis, where
hosted is 1.6× slower: hosted writes the longer brief (340 audited words
against 203). Per ticker that nets out to 1.2×, 31.1 s against 25.9 s. All
three runs used the workflow template's parallelism of 2.

**GPU use** (`eval/runs/gpu-nvsmi-p9jr2.csv`: nvidia-smi on node 2 every
5 s, 709 samples, 02:51:49–03:50:49 UTC; `scripts/nvsmi_summary.py`, each
Argo run's window from its workflow object):

| Window | Samples | Util mean | Median | p95 | Max | Samples above 0% | memory.used |
|---|---|---|---|---|---|---|---|
| Tool-use GPU route, **approximate** (02:59:15–02:59:57) | 8 | 69.5% | 94% | 94% | 94% | 6 (75%) | 20,540 MiB |
| Smoke `k6zxd` (03:01:40–03:11:20) | 116 | 34.8% | 0% | 100% | 100% | 47 (41%) | 20,540 MiB |
| Extended `p9jr2` (03:13:00–03:48:12) | 422 | 38.1% | 0% | 99% | 100% | 182 (43%) | 20,540 MiB |
| Outside every window | 163 | — | — | — | — | 0 | — |

The tool-use window is approximate: the check's JSON carries no
timestamps, so the window runs from the CPU route's output file
(written 02:59:15) to the GPU route's (02:59:57); the GPU route's own
`wall_s` sums to 35.6 s. No GPU activity falls outside the three windows,
which also confirms node 2's clock against the workflow times.
`utilization.gpu` is the share of each sample period in which a kernel
ran, and `memory.used` is the whole GPU's (constant at 20,540 MiB; the
20,488 MiB recorded 2026-10-03 is llama-server's own process memory, a
different measure). **During `p9jr2`, at parallelism 2, the GPU averaged
38% and its median sample was 0%: the A10 has headroom.** That is all the
capture shows; no throughput at higher parallelism is projected from it
without a run. The CPU endpoint during `8vpq6` was the opposite: median
7,806m of its 8,000m limit.

**Cost per brief, the three arms on the same pipeline (2026-10-05).**
Dated measurements, not the cost of record, which stays $0.0366
(2026-09-06). Every figure is model cost only: harness pods, storage and
the judge (eval-only) are excluded on all three arms.

| Arm | Cost per brief | How it was measured | Time per brief |
|---|---|---|---|
| Hosted (Anthropic API) | **$0.0370** | `scripts/cost_report.py`, n = 3 (AAPL, NVDA, JPM): $0.0285 exact + $0.0085 RAG-internal estimate. Run locally on the `1f51dad` pipeline code (nothing under `agent/` or the requirements has changed since), not inside the image | 25.9 s pipeline (`9jzmj`) |
| GPU SLM `p9jr2` | **$0.0293, a ceiling** | the whole VM.GPU.A10.1 at $2.00/h × the run's wall time: 2,112 s for 40 briefs = 52.8 s each, 68.2 briefs an hour at parallelism 2 | 31.1 s pipeline |
| CPU SLM `8vpq6` | **$0.0107** | the llama.cpp pod's request, 4 OCPU + 30 GiB billed as 30 GB, at $0.03/OCPU-h + $0.002/GB-h = $0.1800/h, × 8,576 s for 40 briefs = 214.4 s each, 16.8 briefs an hour | 355.1 s pipeline |
| — sensitivity: memory converted to decimal GB | $0.0110 | 30 GiB = 32.21 GB, $0.1844/h ([cost.md](cost.md): OCI's memory GB taken as binary) | |
| — sensitivity, approximate: the whole node | $0.0219 | 8 OCPU + 64 GiB (the shape's memory, inferred from 62.79 GiB kernel-visible) = $0.3680/h | |

- **The CPU arm is the cheapest per brief, at 13.7× hosted's per-ticker
  latency** (355 s against 26 s). That suits batch work — overnight
  briefs, the eval itself — not interactive use. Its endpoint was
  saturated during the run (median 7,806m of its 8,000m limit), so more
  parallelism would not lower the figure at this pod size.
- **The GPU figure is a ceiling.** The A10 averaged 38% utilization during
  `p9jr2`, median sample 0%, at parallelism 2, and was above 0% in 43%
  of samples while billed for the whole run. Whether higher parallelism
  lowers the figure, and by how much, is not measured; no floor is
  projected without a run.
- **Hosted is n = 3**, the cost harness's three tickers, and its
  RAG-internal part is a tokenizer estimate. It sits within $0.0004 of the
  2026-09-06 record ($0.0366) on the same tickers; the RAG input tokens are
  identical (4,868 / 5,927 / 5,003).
- The SLM figures bill a resource for the run's measured wall time; the
  hosted figure prices tokens. They answer the same question (what one
  brief costs to produce) by different methods. Prices: OCI price-list
  API read 2026-10-05 ([cost.md](cost.md)).

```bash
python scripts/cost_report.py --json-out eval/runs/cost-record-1f51dad-2026-10-05.json
python scripts/cost_per_brief_slm.py \
  eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-workflow.json \
  --label gpu-p9jr2 --hourly-usd 2.00
python scripts/cost_per_brief_slm.py \
  eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json \
  --label cpu-8vpq6-pod --e5 4 30 --ocpu-usd 0.03 --gb-usd 0.002     # add --decimal-gb for $0.0110
python scripts/cost_per_brief_slm.py \
  eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json \
  --label cpu-8vpq6-node-approx --e5 8 64 --ocpu-usd 0.03 --gb-usd 0.002
```

**The three numeric unsupported claims of `p9jr2`**, all in the Executive
Summary. Two are model errors (wrong label), one is a source conflict.
Types: *wrong value* (the figure is not the context's), *wrong label* (the
figure is in the context but attached to the wrong quantity), *source
conflict* (quoted correctly from one source, held against another), *judge
error* (correct against the context), *not in context* (an assertion the
context lacks, no figure misquoted). Model errors are wrong value + wrong
label + not in context — everything except source conflicts and judge
errors: an unsupported claim with no basis in the context is what the
grounding eval exists to catch, and leaving it out would favor the hosted
arm, whose two are of that type. The adjudication is
`eval/runs/numeric-error-types-2026-10-05.json`; `eval/error_types.py`
checks it covers exactly the UNSUPPORTED numeric claims of each run and
prints the counts and tests (`eval/runs/numeric-error-types-2026-10-05.txt`).

- **SFIX — wrong label.** Claim: "…stabilizing the customer base near its
  recent low of $2.61". $2.61 is `current_price`; the only low in the
  context is `week_52_low: 2.1`. The summary calls the current price a low.
  The GPU's own Recent Developments section has it right ("between $2.10
  and $5.75 … near the lower end at $2.61"), and on the same data `8vpq6`
  ("trading near its 52-week low of $2.10 at $2.61") and `9jzmj` ("from its
  52-week high of $5.75 to $2.61") are SUPPORTED.
- **CRBU — wrong label; the judge's stated reason is incorrect, the verdict
  stands.** Claim: "a market capitalization near its 52-week low of
  $1.22". The figure is right: `week_52_low: 1.215` is $1.22 at two
  decimals, and the GPU's Financial Health section quotes $1.215. But a
  per-share price is attached to "market capitalization" ($130.8 million in
  the context), the same class of error as SFIX. The judge's reason ("the
  52-week low is $1.215, not $1.22; $1.22 is the current price") rejects a
  correct rounding; it is recorded as an incorrect judge reason, not as a
  judge error, because the claim is wrong on the label.
- **OMER — context source conflict, judged against the filing.** Claim: "a
  notable net income of $116.53 million". Quoted correctly from yfinance
  (`net_income: 116533000.0`); the filing's RAG answer in the same context
  says "the net loss was $3.4 million" for FY2025. All three arms put the
  $116.5 million in their Financial Health section; only the GPU carried it
  into the audited summary. The same mechanism as BEAM in `8vpq6`.

**By type, across the three runs** (`eval/error_types.py`):

| Type | Hosted `9jzmj` | CPU `8vpq6` | GPU `p9jr2` |
|---|---|---|---|
| Wrong value | 0 | 1 (CHGG) | 0 |
| Wrong label | 0 | 0 | 2 (SFIX, CRBU) |
| Source conflict | 0 | 1 (BEAM) | 1 (OMER) |
| Judge error | 0 | 1 (META) | 0 ¹ |
| Not in context | 2 (AFRM, NVO) | 0 | 0 |
| **Model errors / numeric claims** | **2/277** (CI 0.2–2.6%) | **1/161** (CI 0.1–3.4%) | **2/155** (CI 0.4–4.6%) |

¹ CRBU's verdict stands; its stated reason is incorrect (above).

Model errors, exact two-sided Fisher, unadjusted: hosted vs CPU p = 1.000,
hosted vs GPU p = 0.621, CPU vs GPU p = 0.617 — no pair separates. Hosted's
two are *not in context*: AFRM compares its P/E to "historical averages for
fintech peers" the context does not hold, and NVO's is a qualitative
pipeline statement, numeric only through "GLP-1". The arms differ in the
kind of error (hosted asserts what the context lacks; the GPU attaches
right figures to wrong quantities; the CPU misquotes one value), not
detectably in the count.

**Overlap with `8vpq6`'s three (CHGG, BEAM, META): no ticker overlaps, and
two classes recur.** The source conflict recurs (BEAM, then OMER), and so
does a price-range claim the judge mishandles (META's verdict, CRBU's
reason). On the tickers themselves: CHGG's truncation did not repeat — the
GPU wrote "$52.99 million" in Financial Health and "a net loss of $53
million" in the summary (SUPPORTED). BEAM's conflict is still in the GPU
brief, -$86.52 million in Financial Health and "$86.5 million" in Recent
Developments, but neither section is audited, so it was never judged. META
has no 52-week claim in the GPU's audited text.

**Numeric check on the three-way, adjudicated (dated record, 2026-10-05;
not a number of record).** The deterministic check (`agent/numeric_check.py`,
stock-field figures only, relative tolerance 2%) was run offline over the
three runs' findings (`scripts/numeric_backtest.py --runs 9jzmj 8vpq6
p9jr2`): 12 distinct flags, every section of every brief, not only the
audited ones. All 12 were labelled by one human adjudicator, not blind to
the arm, under the rules written 2026-09-30 (`eval/numeric_check/README.md`),
with no doubt notes (`eval/numeric_check/adjudication-2026-10-05-9jzmj-8vpq6-p9jr2.csv`).

| Run | Flags | TRUE_ERROR | FALSE_POSITIVE | TRUE_ERROR per checked number (cluster bootstrap 95% CI) | Excluding the upstream data findings |
|---|---|---|---|---|---|
| Hosted `9jzmj` | 8 | 8 | 0 | 8/569 = 1.41% (0.0–3.9%) | 0/569 |
| CPU SLM `8vpq6` | 1 | 1 | 0 | 1/389 = 0.26% (0.0–0.8%) | 0/389 |
| GPU SLM `p9jr2` | 3 | 2 | 1 | 2/423 = 0.47% (0.0–1.2%) | 0/423 |

Paired ticker-bootstrap differences in the TRUE_ERROR rate: CPU − hosted
−1.15% (CI −3.44% to 0.00%), GPU − hosted −0.93% (−3.34% to +0.53%), GPU −
CPU +0.22% (−0.06% to +0.74%). No interval excludes zero.

- **Every TRUE_ERROR is attributed to the two upstream data findings**
  by the committed rules (`eval/numeric_check/upstream-findings.md`;
  `upstream_cause` in `scripts/numeric_adjudicated.py`): 6 currency — the
  hosted TM brief states revenue and net income as "$52.0 billion" and
  "$4.5 billion", in three sections, from source values of 51.96 trillion
  and 4.48 trillion in the filer's reporting currency (yen by their
  magnitude, inferred), labelled USD — the brief also wrote them 1,000
  times smaller — and 5 profit-margin fraction ("3.25%" for OMER in all three
  arms, "-2.49%" for LCID in the GPU arm, where the source fraction means
  324.9% and −249.2%). With those excluded, all three arms are at 0: the
  check finds no stock-field error that the upstream data does not
  explain, in any arm.
- The FALSE_POSITIVE is OMER's "net loss of $3.4 million" in the GPU's SEC
  Filing Highlights: the filing's figure, which the check bound to the
  yfinance `net_income` — the same source conflict as the judge's OMER
  claim (above), seen from the other side.
- **Where the adjudication and the judge disagree:** TM in `9jzmj`. The
  audited Executive Summary's "$52.0 billion in annual revenue" and "$4.5
  billion in net income" are SUPPORTED by the judge and TRUE_ERROR here.
  The judge's reason accepts the scale error outright: "Source data shows
  revenue of 51,957,024,686,080.0 JPY, which the Financial Health
  pre-written section rounds to '$52.0 billion'". Two judge misses on
  audited figures, consistent with judge v2's population-weighted recall
  (32.5%); they are not in the judge-flagged rates above. No other flag
  overlaps a judged claim: the other ten sit in sections the judge does
  not audit.

**What the check cannot see.** Two of the numeric problems the judge's
audit found are invisible to it: (1) **truncation under the 2% tolerance**
— CPU's CHGG "-$52.9 million" for -52.997M is 0.18% off and passes (so
the numeric check cannot measure known limitation 4 at its current
tolerance); (2) **wrong labels** — GPU's SFIX "recent low of $2.61" (the
current price) and CRBU "market capitalization near its 52-week low of
$1.22" (a per-share figure) quote correct values, and the check binds
figures to fields, not to what the sentence calls them. It also checks
stock-field figures only: news and filing figures (BEAM's and OMER's
filing-side numbers) are out of its scope.

```bash
python scripts/numeric_backtest.py --runs 9jzmj 8vpq6 p9jr2 --date 2026-10-05
python eval/numeric_check/label_cli.py --csv eval/numeric_check/adjudication-2026-10-05-9jzmj-8vpq6-p9jr2.csv
python scripts/numeric_adjudicated.py --date 2026-10-05 \
  --adjudication eval/numeric_check/adjudication-2026-10-05-9jzmj-8vpq6-p9jr2.csv \
  --runs 9jzmj 8vpq6 p9jr2
#   eval/runs/numeric-adjudicated-2026-10-05-9jzmj-8vpq6-p9jr2.{json,md}
```

**Smoke `k6zxd` (2026-10-05, dated, never an arm comparison).** 10/10
tickers, 3/63 = 4.76% unsupported (Wilson 95% CI 1.6–13.1%), gate passed
(≤ 5%), numeric 0/32 (3.2 per ticker), traffic proof EXACT (70 calls,
95,185 + 25,317 tokens), 0 retries, mean pipeline 30.82 s per ticker, RAG
faithfulness 1/446 over 20 answers (rf-v1, unvalidated). All three
unsupported claims are on AAPL and qualitative: hedged Outlook watch-items
("strong brand loyalty", "sustained margin expansion in services",
"successful diversification of hardware revenue streams"), known limitation
1. The judge listed 11 qualitative claims for AAPL here, against 5 in
`hm527` and 2 in `wnrjr`: smoke-level run-to-run variance from the judge's
listing, the `7c66k` MSFT pattern ("Hosted smokes on the 10-ticker set"),
not a property of the GPU arm. The smoke's run-time projection for the
extended run was mean 37 min, worst 48 min; `p9jr2` took 35 min 12 s.

**Tool-use check** (`eval/tool_use_check.py`, 2026-10-05, image `1f51dad`,
one route after another from the api pod; ten fixed questions per route,
scored from the message trace with no judge; `eval/runs/tool-use-2026-10-05/`,
three JSONs and the saved tmux pane):

| Route | Parse rate | Tool calls (valid / invalid) | Correct tool | Expected tool first | Completed | Errors | Endpoints in the ledger | Wall time, 10 questions |
|---|---|---|---|---|---|---|---|---|
| hosted (Sonnet 4.6) | 1.0 | 12 / 0 | 10/10 | 8/10 | 10/10 | 0 | `anthropic` ² | 104.4 s |
| cpu | 1.0 | 10 / 0 | 10/10 | 10/10 | 10/10 | 0 | `slm-cpu` | 292.8 s |
| gpu | 1.0 | 10 / 0 | 10/10 | 10/10 | 10/10 | 0 | `slm-gpu` | 35.6 s |

On WMT and V the hosted agent called `get_sec_filings` before
`query_sec_filing`; both SLM routes called `query_sec_filing` directly.
**n = 10 per route: this does not show that Qwen picks tools better than
Sonnet.** All three routes parse, pick the right tool and finish on every
question. The check is not under a traffic proof; what served each route
is what its JSON records (the SLM routes' `provenance`: endpoint, URL,
alias `qwen3.6-35b-a3b-q4km`, artifact).

² See known limitation 6: the ledger recorded only the hosted route's two
RAG answer calls.

**Retrieval on the CPU tool-use route.** The pane's `[rag] retrieval
reranking=OFF` lines (stdout only) show the two `query_sec_filing`
retrievals at 35.818 s (WMT) and 40.900 s (V) on the CPU route, against
3.387 s and 2.679 s on hosted and 2.082 s and 4.119 s on GPU. The
retrieval step runs in the api pod; **hypothesis, not tested:** contention
between the api pod and the CPU llama.cpp pod. Recorded as an outlier with
that hypothesis (known limitation 7).

**Known limitations added 2026-10-05, recorded and not changed during the
comparison (post-demo), continuing 1–4 above:**

3. *(update)* The yfinance-vs-filing conflict is **recurring, not a
   one-off**: net income twice in two SLM runs — BEAM (-$86.52 million
   yfinance vs -$80.0 million filing) in `8vpq6` and OMER ($116.53 million
   yfinance net income vs a $3.4 million net loss in the filing) in
   `p9jr2`. Each arm's Financial Health section quotes the yfinance
   figure; whether the judge sees the conflict depends on whether the
   audited summary repeats it.
5. *Foreign filers get no SEC context on any arm.* BABA, NVO, SAP, TM and
   TSM file 20-F, so they make no RAG call — 35 of 40 tickers make the two
   RAG calls, in `9jzmj`, `8vpq6` and `p9jr2` alike — and their briefs run
   on stock and news data only (both RAG fields "(not available)" in the
   contexts). The deliberate coverage gap, recorded since the September runs (`9j2dj`, `j4cnp`).
6. *The LLM ledger does not record the hosted ReAct agent's calls.* On the
   hosted tool-use route `llm_calls` is 0 on 8 of 10 questions; the only
   ledger records are the RAG answer calls behind WMT's and V's
   `query_sec_filing`. The hosted route is therefore attributed by its
   setting (`SLM_FULL=false`), not by the ledger; the SLM routes' calls are
   in the ledger (2 or 3 per question).
7. *Retrieval outliers on the CPU tool-use route* (35.8 s and 40.9 s
   against 2–4 s on the other routes), cause not determined; contention
   with the CPU llama.cpp pod is the working hypothesis.
8. *The synthesis prompt's example leaks into briefs* (added 2026-10-06).
   The Outlook rule gives the example "watch services-margin trend and
   China exposure", and briefs repeat it for companies whose context has
   no services-margin figure: NVDA and MSFT in GPU smoke `m7qvv` ("trend
   of services margins", "trajectory of services margins …") and AFRM in
   `p9jr2` ("Investors should closely monitor the trajectory of services
   margins"), each judged UNSUPPORTED because the term appears nowhere in
   the source data or pre-written sections. A form of limitation 1 with a
   known source. Not changed in the stock-data-fix image (it changes the
   synthesis prompt, so every arm would need new baselines); the fix — an
   example that names no metric, or none — is post-demo.
9. *The current price stated as the 52-week low* (added 2026-10-08). A
   brief says the stock "trades near its 52-week low of $X" with X the
   current price, not the low: UPST in hosted `4hsn2` ($24.35; low
   $22.555), EVGO in GPU `nstp9` ($1.35; low $1.23) and BLNK in hosted
   `vks4c` ($0.51; low $0.45) — on both the hosted model and the
   self-served one. Each is an adjudicated numeric-check TRUE_ERROR, and
   the judge flagged each one UNSUPPORTED. The synthesis prompt passes
   `week_52_low` and `current_price` as fields and says nothing about how to
   state them. The fix — a prompt rule that the 52-week low and high are
   quoted only as those fields, separately from the current price — changes
   the synthesis prompt, so it is post-demo with limitation 8.

```bash
python eval/multi_arm_stats.py \
  --run hosted-9jzmj eval/runs/9jzmj-claims.jsonl eval/runs/raw/9jzmj-findings \
  --run slm-cpu-8vpq6 eval/runs/8vpq6-claims.jsonl eval/runs/raw/8vpq6-findings \
  --run slm-gpu-p9jr2 eval/runs/p9jr2-claims.jsonl eval/runs/raw/p9jr2-findings \
  --rows hosted-9jzmj eval/runs/9jzmj-workflow.json \
  --rows slm-cpu-8vpq6 eval/runs/slm-proof-8vpq6/grounding-eval-extended-slm-cpu-8vpq6-workflow.json \
  --rows slm-gpu-p9jr2 eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-workflow.json
python scripts/nvsmi_summary.py eval/runs/gpu-nvsmi-p9jr2.csv \
  --window "tool-use gpu (approx)" 2026-10-05T02:59:15Z 2026-10-05T02:59:57Z \
  --workflow "smoke k6zxd" eval/runs/slm-proof-k6zxd/grounding-eval-slm-gpu-k6zxd-workflow.json \
  --workflow "extended p9jr2" eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-workflow.json
#   both saved as eval/runs/9jzmj-8vpq6-p9jr2-comparison.txt
python eval/error_types.py eval/runs/numeric-error-types-2026-10-05.json
#   saved as eval/runs/numeric-error-types-2026-10-05.txt
python scripts/slm_traffic_proof.py verify \
  --before eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-before.json \
  --after eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-after.json \
  --log eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2.log \
  --workflow eval/runs/slm-proof-p9jr2/grounding-eval-extended-slm-gpu-p9jr2-workflow.json   # EXACT
```

### Dated finding: hosted run-to-run variance, from two existing runs (2026-10-08)

Two hosted runs on the same image (`f3043751`), the same 40 tickers and the
same pipeline, a day apart, each judged three times: `4hsn2` (2026-10-06)
and `vks4c` (2026-10-08, the reranking A/B's baseline arm). Same image and
inputs except the live data each fetched.

| Measure | `4hsn2` | `vks4c` | Paired difference (4hsn2 − vks4c) |
|---|---|---|---|
| Judge-flagged unsupported, mean of three judgings (range) | 2.55% (1.47–3.76%) | 2.59% (2.26–2.83%) | −0.03 points (CI −1.92 to +2.03) |
| Numeric claims unsupported, mean (range) | 0.86% (0.73–1.11%) | 1.48% (1.09–1.89%) | −0.39 points (CI −2.46 to +1.67) |
| Numeric check TRUE_ERROR (adjudicated) | 1/565 (UPST) | 1/548 (BLNK) | — (one each, the same kind: limitation 9) |
| All numbers stated per brief (no judge) | 6.45 | 6.42 | +0.03 (CI −0.57 to +0.65) |
| Figures bound to stock data per brief (no judge) | 4.47 | 4.33 | +0.15 (CI −0.38 to +0.68) |
| Highlights refusals (35 tickers) | 9 | 5 | — (JPM, MSFT, NVDA, UNH, UPST in both) |

**Reading.** Between two runs of the same hosted pipeline, the
deterministic measures barely move, and the judge-flagged rate moves less
than it does between judgings of one run: the six single judgings span
1.47–3.76%, the two runs' means differ by 0.04 points. The one measure
that moves is the refusal count (9 vs 5; five tickers refuse in both, the
rest vary), so a refusal difference between two runs needs a paired test
— as the reranking A/B's criterion was.

**The planned extra hosted variance runs are dropped.** Their purpose was
to size run-to-run variance before comparing arms. These two runs already
give it on every measure the comparisons use, and the judge's own noise
(three judgings per run) is the larger term; more hosted runs would spend
about $4 each to re-measure the same thing.

```bash
python eval/three_judging_stats.py --runs 4hsn2   --judgings raw eval/runs/rejudge-2026-10-06 eval/runs/rejudge-2026-10-06-r2   --run-judgings vks4c raw eval/runs/rejudge-2026-10-08 eval/runs/rejudge-2026-10-08-r2   --pairs 4hsn2:vks4c                                  # eval/runs/three-judging-2026-10-08-hosted-variance.txt
python eval/density_check.py --runs 4hsn2 vks4c --pairs 4hsn2:vks4c   # eval/runs/density-2026-10-08-hosted-variance.txt
python eval/rag_refusals.py --runs 4hsn2 vks4c
```

### Reranking A/B, pre-registered (2026-10-08, before any run)

**Question:** should cross-encoder reranking (20 cosine candidates reranked
to 3 by `BAAI/bge-reranker-base`) replace plain top-3 retrieval? It shipped
default-off after the June A/B (judge v1, pre-retrieval-fix) showed no
grounding gain at 4–5× the retrieval latency. The judge is too weak a
measure on these runs (calibration of record: recall about 11%), so the
decision rests on measures that need no judge.

**Design.** Two fresh 40-ticker hosted runs on image `f3043751`, submitted
in one window: `argo/eval-run-extended.yaml` (arm baseline) and
`argo/eval-run-extended-rerank3.yaml` (arm rerank3), each judged three
times. A one-ticker memory smoke first (`argo/eval-run-rerank3-smoke.yaml`):
if the eval pod's memory is tight with the cross-encoder loaded, the rerank
arm's pod limit is raised in the WorkflowTemplate, never the image.
Latency comes from a separate warm benchmark
(`scripts/rerank_latency_bench.py` as the Job
`k8s/jobs/rerank-latency-bench`): every eval pod is fresh and loads the
model inside its first timed retrieval, which an app process does once.

**Reranking ships only if all four hold** (`scripts/rerank_ab_decide.py`):

1. **Refusals** (`eval/rag_refusals.py`, the rule fixed 2026-10-07):
   paired by ticker over the tickers with a highlights answer, b = baseline
   refused and rerank3 did not, c = the reverse; **b − c ≥ 3 and exact
   two-sided McNemar p < 0.05**. Refusals of the SEC-highlights answer are
   what better retrieval could fix (limitation 2).
2. **Numeric errors**: TRUE_ERROR per checked number (numeric check,
   adjudicated): **the upper end of the 95% CI of rerank3 − baseline ≤ +0.5
   percentage points**.
3. **Specificity**: figures bound to a stock-data field per brief
   (judge-independent): **the lower end of the 95% CI of rerank3 −
   baseline ≥ −0.5**.
4. **Latency**: the per-ticker time reranking adds, warm (2 × the paired
   median per-query difference, two RAG queries per ticker), **≤ 20% of the
   baseline run's mean pipeline time per ticker**.

Reported, not deciding: judge-flagged grounding over three judgings. It
blocks shipping only if rerank3 is worse with the paired CI excluding zero.
Cost per brief is unchanged by reranking (the same LLM calls; the
cross-encoder runs in the pod) and is not a criterion.

**Result (2026-10-08): DON'T SHIP** — two of the four criteria fail
(`scripts/rerank_ab_decide.py`, output `eval/runs/rerank-ab-decision-2026-10-08.json`).
Runs on image `f3043751`, 40 tickers each, submitted together at 03:24Z:
baseline `grounding-eval-extended-vks4c` and rerank3
`grounding-eval-extended-rerank3-2mzdd`; both 40/40 on the first attempt,
0 retries, stock block empty 0/40, gates passed. The one-ticker memory smoke
(`grounding-eval-rerank3-smoke-262mz`) peaked at 1,487 MiB of the eval pod's
2,048 MiB with the cross-encoder loaded and the pod at its 1.5-CPU limit; the
limit was kept, and no eval pod of the A/B was killed or retried.

| Criterion | Baseline `vks4c` | Rerank3 `2mzdd` | Result |
|---|---|---|---|
| 1. Highlights refusals (35 tickers with a RAG answer) | 5 | 7 | b = 2, c = 4, McNemar p = 0.69: **fails** (reranking refused more) |
| 2. Numeric TRUE_ERROR per checked number (adjudicated) | 1/548 (BLNK: the current price written as the 52-week low) | 0/539 | −0.18 points (CI −0.60 to 0.00): passes |
| 3. Figures bound to stock data per brief | 4.33 | 4.30 | −0.03 (CI −0.40 to +0.35): passes |
| 4. Warm latency added per ticker | — | +11.0 s | 41.5% of the baseline's 26.4 s, limit 20%: **fails** |

- **Latency** (`scripts/rerank_latency_bench.py`, Job `k8s/jobs/rerank-latency-bench`,
  70 queries × 3 repeats, model loaded once in 12.4 s): retrieval alone
  median 0.11 s without reranking, 5.60 s with it (p95 0.18 s vs 14.1 s);
  paired median difference 5.48 s per query, two queries per ticker. The
  cross-encoder on 1.5 CPUs is the cost; in the eval pods, which also load
  it, each reranked retrieval took about 22 s.
- **Judge-flagged grounding, reported** (three judgings): baseline 2.59%
  (2.26–2.83%), rerank3 2.52% (1.71–3.39%); paired baseline − rerank3
  +0.21 points (CI −1.88 to +2.32): no difference, no block.
- Reranking stays default-off. Which tickers refuse varies between runs
  (4hsn2 and 9jzmj each refused 9, this baseline 5), so the refusal count is
  noisy at 35 tickers; the pre-stated test still required a drop, and the
  reranked arm moved the other way.

```bash
python eval/rag_refusals.py --runs vks4c 2mzdd
python scripts/numeric_adjudicated.py --date 2026-10-08 --runs vks4c 2mzdd   --adjudication eval/numeric_check/adjudication-2026-10-08-vks4c-2mzdd.csv
python eval/density_check.py --runs vks4c 2mzdd --pairs 2mzdd:vks4c      # eval/runs/density-2026-10-08-rerank-ab.txt
python eval/three_judging_stats.py --runs vks4c 2mzdd \
  --judgings raw eval/runs/rejudge-2026-10-08 eval/runs/rejudge-2026-10-08-r2 --pairs vks4c:2mzdd
python scripts/rerank_ab_decide.py --baseline vks4c --rerank 2mzdd \
  --adjudication eval/numeric_check/adjudication-2026-10-08-vks4c-2mzdd.csv \
  --latency eval/runs/rerank-latency-2026-10-08.json \
  --judgings-baseline raw eval/runs/rejudge-2026-10-08 eval/runs/rejudge-2026-10-08-r2 \
  --judgings-rerank raw eval/runs/rejudge-2026-10-08 eval/runs/rejudge-2026-10-08-r2
```

### Traffic proof by per-request match (declared 2026-10-07)

The traffic proof shows that the self-served model, and nothing else,
produced an SLM run. Until 2026-10-07 it compared the harness's token sums
with the movement of llama-server's process-wide `/metrics` counters. **From
2026-10-07, declared before any run it judges, it matches the server's own
per-request log against the harness's calls one for one**
(`scripts/traffic_proof_tasks.py`): every task in the endpoint's log window
complete, the multisets of (prompt, completion) tokens equal, nothing
unmatched on either side — verdict TASK-EXACT, otherwise FAIL. The counter
difference is reported beside it and does not decide.

**Evidence for the change.** The A10 capacity replay
(`eval/runs/capacity-sweep-2026-10-07/`) sent the same 352,522 prompt and
98,665 completion tokens three times to the GPU endpoint, with nothing else
on it and the prompt cache off. Each time the server's per-request timings
summed exactly to what was sent; the prompt counter moved 352,521, 352,520
and 352,520 — 1, 2 and 2 short — while the completion counter was exact. The
counter method had failed three runs on the same kind of drift while every
request matched the server's log: CPU `5bdz5` (+1), CPU `4kkgm` (−4), GPU
`6z5xz` (+8) (`eval/runs/slm-proof-4kkgm/INVESTIGATION.md`,
`eval/runs/slm-proof-6z5xz/INVESTIGATION.md`).

**Not retroactive.** `5bdz5`, `4kkgm` and `6z5xz` were judged under the
counter rule and stay not citable; they are not re-scored. The CPU arm of
record stays `8vpq6` (image `1f51dad`, counter proof EXACT). Runs before
2026-10-07 with an EXACT counter proof keep it.

### Dated finding: the judge's run-to-run noise on identical inputs, and density without the judge (2026-10-06)

**Why it was measured.** On the stock-data-fix image (`f3043751`) the
judge-flagged unsupported rate rose on all three arms against the
`1f51dad` runs: hosted 1.70% → 3.76%, GPU 2.45% → 3.75%, CPU 3.63% →
7.17% — almost entirely qualitative Outlook watch-items, none involving a
currency figure, the currency rule's wording, or a margin. To separate the
judge from the briefs, every brief of both three-ways was re-judged
(`eval/rejudge_runs.py`) with the same judge v2 prompt and temperature-0
Sonnet, from the inputs the judge saw the first time (each findings file's
retrieved context, pre-written sections and audited text). The reading was
written into the script before any call: similar rates on re-judge mean a
judge-side shift; the new runs still worse means a brief-side change.

**Result: same inputs, same prompt, temperature 0 — the rate moved by up
to about 2× between two judgings.**

| Run | Image | First judging | Re-judge 1 | Qualitative unsupported (first → re-judge) | Outlook unsupported (first → re-judge) |
|---|---|---|---|---|---|
| hosted `9jzmj` | `1f51dad` | 7/411 = 1.70% | 10/424 = 2.36% | 5/134 → 8/145 | 3 → 4 |
| CPU `8vpq6` | `1f51dad` | 9/248 = 3.63% | 7/241 = 2.90% | 6/87 → 5/81 | 5 → 4 |
| GPU `p9jr2` | `1f51dad` | 6/245 = 2.45% | 7/270 = 2.59% | 3/90 → 5/111 | 2 → 4 |
| hosted `4hsn2` | `f3043751` | 15/399 = 3.76% | 6/408 = 1.47% | 12/129 → 4/136 | 9 → 2 |
| GPU `nstp9` | `f3043751` | 10/267 = 3.75% | 8/245 = 3.27% | 6/101 → 4/77 | 7 → 5 |
| CPU `5bdz5` ¹ | `f3043751` | 19/265 = 7.17% | 9/258 = 3.49% | 17/103 → 8/96 | 12 → 7 |

¹ `5bdz5` is not citable (traffic proof FAIL); it is shown here because the
question was about its judging.

Old against new on re-judge: hosted 10/424 vs 6/408 (Fisher p = 0.45),
GPU 7/270 vs 8/245 (p = 0.79), CPU 7/241 vs 9/258 (p = 0.80). The rise did
not reproduce: under the pre-stated reading it is **judge-side variance,
not a brief-side change**. It is not a directional drift either — the old
briefs moved by small amounts both ways, the new ones down sharply. The
variance sits in the qualitative claims: how many the judge lists, and
which of them it labels UNSUPPORTED. Numeric claims barely move.

**Consequence: three judgings per run** (adopted 2026-10-06 for the new
numbers of record). Each run is judged three times — the original plus two
re-judges (`--tag r2` for the second). A run's rate is reported as the mean
of the three, with the range. Between arms the test is a paired,
ticker-level bootstrap on each ticker's unsupported rate averaged over the
three judgings, which carries both the judge's noise and the clustering of
claims within briefs; pooling the three judgings' per-claim counts into one
Fisher test would treat repeated judgings of the same claims as independent
and make p-values too small. Fisher on each single judging is shown only for
continuity with earlier records, labelled per judging. Cost: one judging of
a 40-ticker run is about $0.88 at the price file's Sonnet rates (chars/4
sizes from the re-judge: 3,690 input and 725 output tokens per brief).

**Density holds without the judge.** The specificity result — hosted
briefs state more figures than the self-served model's — was measured as
numeric claims per brief, a judge-based count. It holds on judge-independent
counts of the audited text, by the numeric check's own parser
(`eval/density_check.py`, output `eval/runs/density-2026-10-06.txt`), and
under re-judge. Paired per ticker, 40 tickers; 95% bootstrap CI; exact sign
test.

| Pair | Figures bound to a stock-data field (conservative) | All numbers stated | Numeric claims, re-judge 1 |
|---|---|---|---|
| hosted `9jzmj` − CPU `8vpq6` | **+1.62** (+1.02 to +2.23), p = 0.0002 | +3.10 (+2.17 to +4.15), p = 4e-9 | +2.98 (+2.20 to +3.77), p = 2e-8 |
| hosted `9jzmj` − GPU `p9jr2` | **+1.80** (+1.32 to +2.30), p = 3e-8 | +3.38 (+2.45 to +4.47), p = 6e-10 | +3.00 (+2.25 to +3.80), p = 1e-8 |
| CPU `8vpq6` − GPU `p9jr2` | +0.17 (−0.28 to +0.62), p = 0.36 | +0.28 (−0.23 to +0.78), p = 0.47 | +0.03 (−0.50 to +0.57), p = 1.0 |
| hosted `4hsn2` − GPU `nstp9` | **+1.43** (+0.93 to +1.93), p = 0.0001 | +2.55 (+1.77 to +3.38), p = 1e-5 | +2.60 (+1.88 to +3.35), p = 6e-6 |
| hosted `4hsn2` − CPU `5bdz5` ¹ | +1.48 (+0.97 to +2.00), p = 8e-6 | +2.75 (+1.95 to +3.65), p = 1e-6 | +2.75 (+2.02 to +3.50), p = 3e-7 |

Means per brief, all numbers stated: hosted 6.80 (`9jzmj`) and 6.45
(`4hsn2`); the self-served model 3.42–3.90. Bound to a stock field: hosted
4.62 and 4.47; the self-served model 2.83–3.05. CPU and GPU — the same model
— do not differ on any count. **From here on the specificity result is
stated from the judge-independent count first, with the bound-to-field
figure as the conservative one, and judge-based density as corroboration.**

Counting correction: a first, ad-hoc pass of the "all numbers" count added
the per-reason binding counts to the tokenizer's count, which already
includes every number when the stock dict is empty; it double-counted the
bound figures (about 11 numbers per hosted brief instead of 6.8). The
committed `eval/density_check.py` counts each number once, and a test pins
it.

```bash
python eval/rejudge_runs.py --date 2026-10-06 --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 5bdz5 \
  --pairs 9jzmj:4hsn2 p9jr2:nstp9 8vpq6:5bdz5            # eval/runs/rejudge-2026-10-06/summary.md
python eval/density_check.py --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 5bdz5 \
  --pairs 9jzmj:8vpq6 9jzmj:p9jr2 8vpq6:p9jr2 4hsn2:5bdz5 4hsn2:nstp9 5bdz5:nstp9 \
  --rejudge eval/runs/rejudge-2026-10-06                 # eval/runs/density-2026-10-06.txt
```

### Numbers of record on the stock-data-fix image, three judgings per run, and the judge v2 calibration on those runs (2026-10-06/07)

**Runs.** Image `f3043751` (stock-data fix plus currency-labelling prompt
rule), 40 tickers, judge v2: hosted `grounding-eval-extended-4hsn2`
(Succeeded, 0 retries, stock block empty 0/40, 26.7 s per ticker) and GPU
SLM `grounding-eval-extended-slm-gpu-nstp9` (Succeeded, 0 retries, traffic
proof EXACT, 34.6 s per ticker; node 2's A10, all layers on the GPU). Both
CPU runs on this image failed their traffic proofs (`5bdz5` +1 token,
`4kkgm` −4; `eval/runs/slm-proof-4kkgm/INVESTIGATION.md`) and are not
citable. The CPU arm of record stays `8vpq6` on the **previous image**
`1f51dad` (proof EXACT) and is compared only with the runs of its own
image (`9jzmj`, `p9jr2`). Every comparison below is same-image.

**Order of the measures.** The deterministic measures come first: the
numeric check (adjudicated), the currency-label count and judge-independent
density need no judge. Judge-flagged grounding is secondary, and is quoted
with the judge's noise between judgings (up to about 2×, previous section)
and its calibration on these runs (below) beside it.

#### Deterministic measures

| Measure | Hosted `4hsn2` | GPU `nstp9` | Same-image difference |
|---|---|---|---|
| Numeric check, TRUE_ERROR per checked number (adjudicated, one human, drafts reviewed) | 1/565 = 0.18% | 1/432 = 0.23% | GPU − hosted +0.05% (CI −0.51% to +0.71%), not separated |
| Currency-label findings (a non-USD reporting-currency figure written in dollars) | 0 (22 on `9jzmj` before the fix) | 0 (11 on `p9jr2`) | — |
| Figures bound to a stock-data field per brief, judge-independent (conservative) | 4.47 | 3.05 | hosted +1.43 (CI +0.93 to +1.93), sign p = 0.0001 |
| All numbers stated per brief, judge-independent | 6.45 | 3.90 | hosted +2.55 (CI +1.77 to +3.38), p = 1.3e-5 |
| Numeric claims per brief, judge-based (re-judge 2), corroboration | 6.85 | 4.05 | hosted +2.80 (CI +2.05 to +3.52), p = 1.9e-6 |

The two TRUE_ERRORs are one kind: the current price written as the 52-week
low (UPST hosted, "near its 52-week low of $24.35", low $22.555; EVGO GPU,
"$1.35", low $1.23). All three judgings flagged both. The check caught them
because the stated figure differs from the bound field; it does not cover
wrong labels in general (SFIX and CRBU in `p9jr2` were invisible to it).
The two FALSE_POSITIVEs are filing figures against yfinance net income
(LCID, OMER): limitation 3, now three companies (BEAM, OMER, LCID). On
`1f51dad` the same density measure gave hosted − CPU +1.62 (CI +1.02 to
+2.23, p = 0.0002) and CPU − GPU +0.17 (CI −0.28 to +0.62): the same model
does not differ between CPU and GPU.

#### Judge-flagged grounding (secondary): three judgings per run

Mean of the three judgings (range); each judging's count in brackets.

| Run | Image | Unsupported, all claims | Numeric claims |
|---|---|---|---|
| hosted `4hsn2` | `f3043751` | 2.55% (1.47–3.76%) [15/399, 6/408, 10/415] | 0.86% (0.73–1.11%) [3/270, 2/272, 2/274] |
| GPU `nstp9` | `f3043751` | 3.57% (3.27–3.75%) [10/267, 8/245, 9/243] | 2.42% (2.38–2.47%) [4/166, 4/168, 4/162] |
| CPU `8vpq6` | `1f51dad` | 2.89% (2.13–3.63%) [9/248, 7/241, 5/235] | 1.25% (0.63–1.86%) [3/161, 2/160, 1/158] |
| hosted `9jzmj` | `1f51dad` | 2.16% (1.70–2.43%) [7/411, 10/424, 10/411] | 0.84% (0.72–1.08%) |
| GPU `p9jr2` | `1f51dad` | 2.25% (1.69–2.59%) [6/245, 7/270, 4/236] | 1.71% (1.26–1.94%) |

Paired ticker-level bootstrap on per-ticker rates averaged over the three
judgings, same image only: `4hsn2` − `nstp9` −1.22 points (CI −4.39 to
+1.78), numeric −1.74 (CI −5.54 to +1.49); on `1f51dad`, `9jzmj` − `8vpq6`
−0.74 (CI −2.67 to +1.03) and `8vpq6` − `p9jr2` +0.16 (CI −1.96 to +2.26).
**No pair separates.** Not detected is not absent: at these rates a
40-ticker run cannot resolve differences of a few points.

#### The judge's calibration on these runs (2026-10-07) — calibration of record

180 claims from `4hsn2` and `nstp9`, labelled blind by one labeller
(`eval/label_cli.py`, no judge verdict shown), drawn from every claim any
of the three judgings listed (775 after excluding 18 already labelled in
earlier sets), in four strata with weights N/n:

| Stratum | Population | Labelled | Human UNSUPPORTED |
|---|---|---|---|
| U: flagged UNSUPPORTED by at least one judging | 29 | 29 (all) | 9 |
| I: INFERENCE in at least one judging | 76 | 30 | 3 |
| W: Outlook watch-item, no digit | 174 | 40 | 2 |
| S: the rest (SUPPORTED wherever listed) | 496 | 81 | 3 |

UNSUPPORTED is the positive class; human SUPPORTED and INFERENCE are not.
Population-weighted, with 95% stratified-bootstrap intervals:

| Judging | Precision | Recall (a claim the judging did not list counts as missed) | Recall over the judging's own listed claims (the September definition) |
|---|---|---|---|
| original | 25.0% (8.3–44.0%) | 13.7% (4.4–30.4%) | 19.9% (7.2–49.7%) |
| re-judge 1 | 30.8% (7.1–57.1%) | 9.2% (1.7–22.9%) | 13.3% (2.7–41.7%) |
| re-judge 2 | 36.8% (16.7–60.0%) | 16.0% (6.2–36.7%) | 28.8% (10.7–78.0%) |
| majority (≥ 2 of 3 say UNSUPPORTED) | 29.4% (8.3–52.9%) | 11.4% (3.1–27.9%) | — |

**True-rate estimate** (post-stratified within each run, from that run's
own labels; denominator: every claim any judging listed; Jeffreys
intervals, a fully labelled stratum exact). **The intervals are wide**:
few labelled rows per run and stratum.

| Run | Estimated human-UNSUPPORTED claims | True rate | 95% CI |
|---|---|---|---|
| hosted `4hsn2` | 18.2 of 485 | 3.8% | 1.9–9.7% |
| GPU `nstp9` | 25.3 of 290 | 8.7% | 5.4–18.5% |

No test between these two estimates is made: they rest on 108 and 72
labels.

**Judge-judge agreement** (no labels needed; all 793 claims listed by any
judging): two judgings list the same claim 72–74% of the time; where both
list it, verdict kappa 0.79–0.86 (Fleiss 0.825 where all three list it);
on flagged-or-not over the union, kappa 0.64–0.68 (Fleiss 0.653). The
judgings flagged 24, 13 and 19 claims; 10 by all three, 12 by exactly one.
The noise is mostly in which claims get listed and flagged, not in the
verdict on a claim both judgings consider.

**Reading.**

- Precision is low because of one interaction: 16 of the 29 judge-flagged
  claims were labelled INFERENCE by the human, and 14 of those 16 are
  qualitative Outlook watch-items — the hedged "watch X" lines the judge
  calls unsupported when the context lacks the metric (limitation 1).
- Recall is low because most human-UNSUPPORTED claims sit in claims the
  judge passed: the supported stratum's 3 of 81 stand for about 18 claims,
  twice the flagged stratum's 9, and the INFERENCE and watch-item strata
  add about 16 more.
- The majority vote is no better than a single judging.
- Against the September calibration (2026-09-24, now a dated record:
  precision 60%, CI 35.7–80.2%; population-weighted recall 32.5% on
  `j4cnp`, CI 16.0–52.4%) both figures are lower, with overlapping
  intervals. The populations differ (September claims, the 512-cap
  pipeline, a different labelling occasion), so this is not a measured
  change in the judge.

**What it means for the numbers.** A judge-flagged rate is a weak signal on
these runs: roughly 3 in 10 flags are human-UNSUPPORTED, and roughly 1 in 9
human-UNSUPPORTED claims is flagged. That is why the deterministic measures
lead and judge-flagged grounding is secondary.

**The three human-UNSUPPORTED claims in the supported stratum** (no note
recorded: the labeller records the label only):

| Run | Ticker | Section | Claim | Original | Re-judge 1 | Re-judge 2 |
|---|---|---|---|---|---|---|
| `4hsn2` | SAP | Executive Summary | SAP S/4HANA (as the named product milestone central to the cloud transition) | SUPPORTED | SUPPORTED | not listed |
| `4hsn2` | CRBU | Outlook | cash runway limited to approximately 12 months | SUPPORTED | SUPPORTED | SUPPORTED |
| `nstp9` | SAP | Executive Summary | ongoing migration to the SAP Business Technology Platform | not listed | not listed | SUPPORTED |

```bash
python eval/three_judging_stats.py --runs 9jzmj 8vpq6 p9jr2 4hsn2 nstp9 \
  --judgings raw eval/runs/rejudge-2026-10-06 eval/runs/rejudge-2026-10-06-r2 \
  --pairs 4hsn2:nstp9 4hsn2:8vpq6 nstp9:8vpq6 8vpq6:p9jr2 9jzmj:p9jr2 9jzmj:8vpq6 9jzmj:4hsn2 p9jr2:nstp9
                                       # eval/runs/three-judging-2026-10-06.txt (cross-image pairs printed, not cited)
python eval/density_check.py --runs 4hsn2 nstp9 8vpq6 p9jr2 \
  --pairs 4hsn2:nstp9 4hsn2:8vpq6 nstp9:8vpq6 8vpq6:p9jr2 \
  --rejudge eval/runs/rejudge-2026-10-06-r2      # eval/runs/density-2026-10-06-numbers-of-record.txt
python scripts/numeric_adjudicated.py --date 2026-10-06 --runs 4hsn2 nstp9 \
  --adjudication eval/numeric_check/adjudication-2026-10-06-4hsn2-nstp9.csv
python eval/build_threejudge_calibration.py --runs 4hsn2 nstp9 \
  --judgings raw eval/runs/rejudge-2026-10-06 eval/runs/rejudge-2026-10-06-r2
python eval/threejudge_report.py                 # eval/runs/threejudge-calibration-2026-10-07.txt
```

### Dated finding: the aggregate step's template outgrew Argo's inline limit (2026-10-04)

**Mechanism (Argo v3.7.18, read from its source).** The controller hands
each step its resolved template in the init container's `ARGO_TEMPLATE`
env var. It clears `inputs.parameters` first and keeps `inputs.artifacts`,
so the aggregate's template carries every ticker's result once, in the raw
input artifact. When that template JSON is longer than
`common.MaxEnvVarLen` = **131,072 bytes**, the controller writes it to a
ConfigMap instead — named after the pod, in the workflow's namespace,
owned by the Workflow — and mounts it at `/argo/config`. That takes
`create` on configmaps in the workflow's namespace. The pinned
`install.yaml` gives the controller only `get, watch, list`, so the step
failed with `configmaps is forbidden: User "system:serviceaccount:argo:argo"
cannot create resource "configmaps" … in the namespace "financial-agent"`.
The workflow's `status.compressedNodes` is a separate mechanism (node-status
compression near the 1 MB object limit), not the cause.

**Size, from the captured smoke workflows** (results JSON-escaped as Go
writes it; the rest of the template is about 1 KB):

| Rows | Bytes per ticker | 10 tickers | Limit crossed from | 40 tickers |
|---|---|---|---|---|
| Hosted (`x2cx8`, `hm527`) | about 4,935 | 0.38× the limit | 27 tickers | about 198 KB, 1.5× |
| SLM CPU (`9jddz`) | about 7,538 | 0.58× | 18 tickers | about 303 KB, 2.3× |
| Hosted before the LLM ledger (`9j2dj`, 2026-09-05) | about 593 | — | not reached | about 24 KB |

Measured on the two 40-ticker runs themselves
(`python scripts/aggregate_template_size.py <workflow.json> …`): `9jzmj`
198,065 bytes (1.51×; the aggregate errored), `8vpq6` 301,083 bytes (2.30×;
the aggregate succeeded, through the offload).

**Cause: the per-ticker LLM ledger added 2026-10-02** (and, on SLM arms,
the endpoint provenance repeated in every row) made each row about eight
times larger. That is why the September 40-ticker runs and every 10-ticker
smoke passed, and the first 40-ticker run since the ledger did not.

**Fixed now, no image change.** `argo/base/rbac.yaml` adds a Role
(`configmaps: [create]`, in `financial-agent`) bound to the controller's
ServiceAccount (`argo` in namespace `argo`) — every overlay inherits it;
`render_diff` shows exactly that Role and RoleBinding added per overlay and
nothing else. `create` is the only verb the controller uses; the ConfigMap
goes with its Workflow through the owner reference. Proven on kind (Argo
v3.7.18) with `scripts/template_offload_probe.py`,
`eval/runs/kind-template-offload-2026-10-04.txt`:

- without the Role, a 150 KB template ends in Error with the same
  `configmaps is forbidden` message as on OKE, and no ConfigMap exists;
- with it, the controller logs `Created configmap`, the ConfigMap holds
  `ARGO_TEMPLATE` (150,343 bytes) owned by the Workflow, the init container
  gets `ARGO_TEMPLATE=offloaded` and the `/argo/config` mount, the pod
  reads all 150,014 payload bytes and the workflow succeeds; the controller
  still cannot update or delete ConfigMaps;
- a 100 KB template stays inline (no ConfigMap);
- deleting the workflow garbage-collects the ConfigMap within seconds.

First live use on OKE: `8vpq6` (2026-10-04), after the Role was applied
there. Its aggregate step ran and succeeded with a 301,083-byte template,
which only the ConfigMap offload can deliver.

**Known post-comparison change (deferred, recorded).** The eval pod's
output parameter should carry only what the aggregate reads: the aggregate
never uses `llm_eval`, `inference_claims`, `timing_s`, `haiku_cost` or the
payload's own `aggregate`/`arms`/`tickers`, the ledger can be written
compactly, and the SLM sampling can travel as a hash; the full result
would ride the findings dump, so an aggregate can always be rebuilt
offline. With that goes a test of the worst-case 40-ticker template size
against 131,072 and a pre-submit warning in `make eval-run`. It changes
`grounding_check.py`, which is in the image, so every arm would re-run on
the new image: it waits until the comparison on `1f51dad` is finished.
Until then a 40-ticker run depends on the template offload.

**Host-side readers and compressed node status.** A 40-ticker workflow
object has `status.compressedNodes` and no `status.nodes`; readers that
only looked at `status.nodes` saw no pods. `scripts/workflow_nodes.py`
reads either form and stops with a plain message when the nodes are
offloaded to Argo's database. `scripts/run_time_projection.py` and
`scripts/rag_ledger_from_workflow.py` use it directly; `eval/attempts.py`
runs inside the eval pods (the harness imports it), so it is left exactly
as built into the pinned image and `make eval-run` / `slm-eval-run` expand
the workflow object before handing it over. Run by hand, pipe the object
through `python3 scripts/workflow_nodes.py expand` first. Validated on
`9jzmj`'s real object (`status.compressedNodes` of 109 KB, no `nodes` key):
unexpanded, `eval/attempts.py` reports 0 eval pods; expanded, 40 eval pods
for 40 tickers and 0 retries, matching the pod log, and the run-time
projection reads all 40 tickers from it.

### Dated finding (computed, not booted): no 4-bit Qwen3.6-35B-A3B fits one A10 under vLLM (2026-10-02)

Qwen publishes Qwen3.6-35B-A3B in BF16 and FP8 only (FP8 has no native
Ampere support, and its weights exceed 24 GB). The community 4-bit builds,
weighed from their safetensors headers with `--language-model-only`
(vision tower skipped) and no MTP draft layers, against the A10's 23,028
MiB (22.49 GiB):

| Repo @ revision | Quant | On disk | Language model | At util 0.90 (20.24 GiB) | At 0.95 (21.36 GiB) |
|---|---|---|---|---|---|
| `palmfuture/Qwen3.6-35B-A3B-GPTQ-Int4` @`00a6698` | GPTQ int4 g128 | 22.73 GiB | 20.32 GiB | weights alone exceed it by 0.08 | 1.04 GiB left |
| `QuantTrio/Qwen3.6-35B-A3B-AWQ` @`119886a` | AWQ int4 g128 | 23.70 GiB | 21.30 GiB | exceed by 1.06 | 0.07 GiB left |
| `cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit` @`00fcea2` | AWQ int4 g32 | 23.24 GiB | 21.90 GiB | exceed by 1.66 | exceed by 0.54 |

Only the routed experts are 4-bit; attention, Gated DeltaNet, shared
experts, embeddings and `lm_head` stay 16-bit (~4.5 GiB). The 1.04 GiB
best case must hold the CUDA context, activations, CUDA graphs, the KV
cache (~20 KiB/token: 10 full-attention layers × 2 KV heads × 256) and the
per-sequence DeltaNet state, against a harness that sends up to ~8
concurrent requests of up to ~5k tokens: no usable context. Separately,
node 2's driver 570.124.06 supports CUDA 12.8; vLLM ≥ 0.19.0 (the card's
minimum; Qwen3.5-architecture support since 0.17.0, quantized-GDN fix in
0.19.0) publishes no CUDA 12.8 image — 0.19.x defaults to CUDA 12.9 and
0.20+ to 13.0, which needs a 580-series driver. vLLM was **not booted**;
these are arithmetic and published-artifact facts. The GPU arm runs
llama.cpp's CUDA 12.8.1 build on the same GGUF instead. Reproduce:

```bash
python scripts/hf_safetensors_breakdown.py palmfuture/Qwen3.6-35B-A3B-GPTQ-Int4 \
  --revision 00a66983516f8f8057741221277eed4141c9e431 --gpu-mib 23028 --util 0.90
# QuantTrio/Qwen3.6-35B-A3B-AWQ @119886a1072372348f73ef0df2d801cdcc0f455b
# cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit @00fcea2d3bcf5389b518d4fc082e5590e0ba4844
```

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

*A dated record since 2026-10-07. The calibration of record for the current
numbers is the three-judging calibration measured on those runs:
["The judge's calibration on these runs"](#the-judges-calibration-on-these-runs-2026-10-07--calibration-of-record).
This one was measured on September claims and still describes the runs of
its time (`j4cnp`, `lsnnc`).*

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
4.2–23.1%). Replaced by the September calibration (2026-09-24) above, which measures
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
