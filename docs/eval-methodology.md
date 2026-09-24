# Eval methodology — the grounding-eval DAG

The centerpiece of this project is not the UI; it is that grounding is
**measured by a committed, re-runnable harness and gated in CI fashion**.
The number of record: **49% pre-fix → 0/84 unsupported in the current
eval (judge v1)** (always quoted with the pre-fix context and denominator, never as a
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
findings-capture section). Calibration: judge v2 measured 75% recall /
60% precision on UNSUPPORTED against blind human labels (n=50, held
out), so absolute v2 rates are approximate. **Not the number of
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
direction). Calibration: judge v2 measured 75% recall / 60% precision
on UNSUPPORTED against blind human labels (n=50, held out), so the
absolute rates here and in the per-section table below are
approximate; the A/B direction and the per-section attribution are
unaffected because both arms share the judge.

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
  against each local arm: p = 7.8e-05, 2.6e-06, 0.0039.
- **The 7B gate pass is on the point estimate only.** `cnkp2`'s 4.58% is
  under the 5% gate, but its interval (2.9–7.1%) spans it, so the run is
  consistent with a true rate above the gate.

Not supported: a size curve. The hosted arm is a different model family
(Anthropic Haiku, size undisclosed), not a larger Qwen, so the four arms
are not points on one scaling line; only the three Qwen2.5 arms share a
family.

Calibration: judge v2 measured 75% recall / 60% precision on UNSUPPORTED
against blind human labels (n=50, held out, 2026-09-06), so every rate
here is an approximate point estimate; comparisons are unaffected in
direction because all arms share the judge. A four-arm held-out sample is
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
  this N. financial-lora `v924f` 6.49% vs `lsnnc` 8.15% (5.8–11.4%),
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
Stats: `python eval/multi_arm_stats.py --run hosted eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings --run financial-lora eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings --run qwen1.5b-base eval/runs/4nfsm-claims.jsonl eval/runs/raw/4nfsm-findings --run qwen7b-base eval/runs/cnkp2-claims.jsonl eval/runs/raw/cnkp2-findings`.

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
(judge-v2 rates; approximate per the held-out calibration, direction
unaffected — both arms share the judge).

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
- Judge recall on UNSUPPORTED: **9/12 = 75.0% (95% CI 46.8–91.1%)**
- Judge precision on UNSUPPORTED: **9/15 = 60.0% (95% CI 35.7–80.2%)**

Against v1's dev-set result (kappa 0.321, UNSUPPORTED recall 1/9 =
11.1%, precision 1/3 = 33.3% — non-blind, and measured under dev
conditions): held-out, blind v2 lands at kappa 0.580 with recall 75%
and precision 60%. Stated plainly: **v2 trades v1's INFERENCE
catch-all for a mild over-flag of INFERENCE-as-UNSUPPORTED** — 5 of
v2's 6 UNSUPPORTED false positives were human-INFERENCE claims. The
consequence for reading rates differs from v1's: v1 rates were
one-directional lower bounds (recall 11%); **v2's errors run both
ways** (missed 3 of 12, over-flagged 6, net 15 flagged vs 12 human on
this sample), so v2 rates are approximate point estimates, not bounds.

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
reproduced exactly. A gated CI job
(`.github/workflows/critic-injection.yml`) re-runs this on
judge-adjacent changes and asserts recall ≥ 0.8; the bar does not move
if it regresses — the number gets reported instead.

## Boundary

Argo owns eval orchestration; Celery owns request-time async. The eval
DAG runs the pipeline in its own pods — it does not call the API service
and cannot contend with user traffic for the cache or the broker.
