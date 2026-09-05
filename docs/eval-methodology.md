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
failure modes, so nothing below validates v2.** A held-out sample will
be drawn from the 40-ticker run.

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
