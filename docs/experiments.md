# Experiments: the full records moved from the README

Moved verbatim from the README on 2026-10-08 (the README now carries the
conclusions only). Numbers that may be quoted, and how: [numbers-of-record.md](numbers-of-record.md).

## Why this project exists

I built this to answer a question I couldn't find a good answer to: *can an LLM agent produce investment briefs that are actually grounded in real sources -- and how would you even know?*

The answer required building both the agent and the measurement layer to audit it.

## What I Measured (and What I Found)

### Grounding Eval (LLM-as-judge)

I built an evaluation framework that audits the quantitative and forward-looking claims in each brief's Executive Summary and Outlook against the retrieved source context (the four pre-written sections are judge input, not audited directly). A Sonnet judge (temperature 0) labels each claim `SUPPORTED`, `UNSUPPORTED`, or `INFERENCE`.

**Current (image `f3043751`, 40 tickers, judge v2, three judgings per run).** Measured without the judge first: wrong stock figures 1/565 hosted vs 1/432 for the self-served model on the A10, currency-label errors 0 and 0 (22 and 11 before the stock-data fix), figures bound to stock data 4.47 vs 3.05 per brief. Judge-flagged, mean (range) of three judgings: hosted `4hsn2` 2.55% (1.47–3.76%), A10 `nstp9` 3.57% (3.27–3.75%); no difference detected. The CPU arm `8vpq6` (2.89%) is from the previous image and compared only within it. The judge's calibration on these runs: precision ~29%, recall ~11% (majority vote), with true-rate estimates of 3.8% (CI 1.9–9.7%) and 8.7% (CI 5.4–18.5%), wide. Details in [docs/numbers-of-record.md](numbers-of-record.md).

*Former numbers of record:* the one-judging three-way on image `1f51dad` (2026-10-05 to 2026-10-07: `9jzmj` 1.70%, `8vpq6` 3.63%, `p9jr2` 2.45%), and before it (2026-09-06 to 2026-10-05) hosted `j4cnp` 12/392 = 3.06% (CI 1.8–5.3%), judge v2, reweighted true-rate estimate 5.7% (CI 3.5–9.9%). It ran under a 512-token RAG answer cap, so it is a different pipeline from the later runs; it is not a before/after with them. It stays the hosted arm of the fine-tune A/B below.

**The fine-tune A/B: 8.15% vs 3.06%, Fisher p = 0.0023 (judge v2).** On the same image and index, with the QLoRA fine-tune writing two of the four sections, the local-model arm `lsnnc` measured 30/368 = 8.15% unsupported (CI 5.8–11.4%) against `j4cnp`'s 3.06%. It fails the 5% gate, the excess sits in the two sections the fine-tune writes, and it ships disabled ([details below](#qlora-fine-tuning-experiment)).

*Judge-version note:* every unsupported rate in this README names its judge prompt version. **v1** rates are lower bounds (2026-09-04 human validation: v1 recall on UNSUPPORTED 1/9). **v2** rates are judge-flagged rates. The calibration of record is the 2026-10-07 one above, measured on the current runs; the September calibration (2026-09-24: kappa 0.580, precision 60%, CI 35.7–80.2%; population-weighted recall 32.5% on the baseline run, CI 16.0–52.4%) is a dated record and applies to the runs of its time, with their reweighted true-rate estimates. A/B directions are unaffected when both arms share the judge ([docs/eval-methodology.md](eval-methodology.md)).

*Dated history (judge v1, pre-retrieval-fix; not current):* before the synthesis prompt's grounding rules, the first measurement found 49% of claims unsupported (pre-harness, no recorded denominator). After them, the 2026-08-24 10-ticker re-measure found 0/84. Both predate judge v2 and the 2026-09-04 retrieval fix, and v1 rates are lower bounds.

### Self-served open-weight model vs hosted (October 2026)

**Question:** can a self-served open-weight model write the whole brief —
sections, synthesis and RAG answers — as well as hosted Claude, and what
does it cost? **Answer, on this sample:** it gets stock figures wrong
about as rarely as hosted (1/432 vs 1/565, no judge involved), it states
fewer figures, no judge-flagged grounding difference was detected, and on
CPU it is the cheapest per brief but 13.7× slower per ticker.

**Setup.** Qwen3.6-35B-A3B (a mixture-of-experts model, 35B parameters,
3B active), one Q4_K_M GGUF file served by llama.cpp b11347 from two
endpoints: CPU inside the OKE cluster (8 CPU / 30 GiB) and node 2's A10
(all layers on the GPU). With `SLM_FULL` every agent call goes to the
endpoint; the judge stays hosted. Why llama.cpp rather than vLLM: Qwen
publishes this model in BF16 and FP8 only, and the community 4-bit builds
leave at most about 1 GiB of an A10's 24 GB after the weights — no usable
context for the KV cache — while node 2's driver (CUDA 12.8) has no
matching vLLM image for the minimum version that supports the
architecture. That was computed from the published artifacts, not booted
([dated finding](eval-methodology.md#dated-finding-computed-not-booted-no-4-bit-qwen36-35b-a3b-fits-one-a10-under-vllm-2026-10-02)).

**Current: image `f3043751`** (stock-data fix plus currency-labelling
prompt rule), hosted `4hsn2` vs the A10 `nstp9`, 40 tickers, judge v2
judged three times. The A10 run passed its traffic proof; both CPU runs on
this image failed theirs and are not citable, so the CPU arm stays on the
previous image (table below). Only same-image arms are compared.

| | Hosted `4hsn2` | A10 `nstp9` |
|---|---|---|
| Wrong stock figures per checked number (numeric check, adjudicated) | 1/565 | 1/432 |
| Currency-label errors (22 and 11 before the fix) | 0 | 0 |
| Figures bound to stock data per brief (no judge) | 4.47 | 3.05 |
| Unsupported, all claims, mean (range) of three judgings | 2.55% (1.47–3.76%) | 3.57% (3.27–3.75%) |
| Unsupported, numeric claims, mean (range) | 0.86% (0.73–1.11%) | 2.42% (2.38–2.47%) |
| Pipeline time per ticker | 26.7 s | 34.6 s |
| Model cost per brief (dated, model cost only) | $0.0357 (n = 3) | $0.0303 (a ceiling) |

The two wrong figures are one kind: the current price given as the 52-week
low (UPST, EVGO). Figures stated: hosted +1.43 per brief (CI +0.93 to
+1.93). Judge-flagged grounding: no difference detected (paired CI −4.39 to
+1.78 points), read beside the judge's noise (up to 2× between judgings)
and its calibration on these runs (precision ~29%, recall ~11%).

**Previous image `1f51dad`: the three-way with CPU** (one judging each; the
former numbers of record). Both SLM runs passed a traffic proof: the tokens
the harness logged equal the endpoint's own counters exactly, so every call
reached the self-served model and nothing else used it during the run.
No run needed a retry. Tests are exact two-sided Fisher (rates) and paired
per-ticker sign tests (density), not adjusted across the three pairs.

| | Hosted `9jzmj` | CPU `8vpq6` | A10 `p9jr2` |
|---|---|---|---|
| Unsupported, all claims (judge-flagged) | 7/411 = 1.70% | 9/248 = 3.63% | 6/245 = 2.45% |
| Unsupported, numeric claims | 2/277 = 0.72% | 3/161 = 1.86% | 3/155 = 1.94% |
| Model errors among numeric claims (adjudicated by type) | 2/277 | 1/161 | 2/155 |
| Numeric claims per ticker | 6.9 | 4.0 | 3.9 |
| Pipeline time per ticker | 25.9 s | 355.1 s | 31.1 s |
| Model cost per brief (dated, model cost only) | $0.0370 (n = 3) | $0.0107 | $0.0293 (a ceiling) |

- **Grounding:** no pair separates on any denominator (p ≥ 0.126 all
  claims, ≥ 0.35 numeric claims). That is "not detected at this sample
  size", not "equivalent": the SLM arms' upper bounds reach 5–7%.
- **Density:** both SLM arms state about 3 fewer figures per ticker than
  hosted (paired p ≤ 1e-8), so their rates are over fewer checkable
  figures. CPU and GPU do not differ (+0.15 per ticker, CI −0.35 to
  +0.68): the same model writes the same kind of brief on either hardware.
- **Error types** (every judge-flagged numeric claim adjudicated): the
  CPU arm misquoted one value (CHGG, truncated), the A10 arm put two
  correct figures under the wrong label (SFIX, CRBU), and hosted asserted
  two things the context did not hold (AFRM, NVO). Source conflicts
  between yfinance and the filing recur (BEAM, OMER).
- **Numeric check** (no LLM): every true error in all three arms came
  from the two upstream data defects, fixed in `f3043751`; it also caught
  the Toyota figure the judge accepted.
- **Speed and cost:** the A10 is 10–15× faster than CPU at every call site
  and 1.2× hosted's per-ticker time (1.3× on `f3043751`). The CPU endpoint was saturated; the
  A10 averaged 38% utilization at parallelism 2, so its cost per brief is a
  ceiling. Costs exclude the harness, storage and the judge.
- **Tool use** (the ReAct `/ask` agent, ten questions per route, no
  judge): all three routes called the right tool and completed every
  question. Ten questions cannot rank them.

Full tables, per-section results, the known limitations and every command:
[the current runs](eval-methodology.md#numbers-of-record-on-the-stock-data-fix-image-three-judgings-per-run-and-the-judge-v2-calibration-on-those-runs-2026-10-0607) and
[the `1f51dad` three-way](eval-methodology.md#gpu-slm-extended-run-p9jr2-2026-10-05-the-three-way-comparison-with-hosted-9jzmj-and-cpu-8vpq6);
the deployment: [architecture.md](architecture.md#deployed-topology-october-2026).

### Reranking A/B Experiment

I added optional cross-encoder reranking to the RAG pipeline and ran a controlled 4-arm eval across 10 tickers to measure whether it improved grounding. A dated record: Jun 2026, judge v1, pre-retrieval-fix, local `grounding_check.py` runs (pre-Argo, so no workflow run IDs); intervals from `eval/stats.py`:

| Arm | Claims | Grounding | Unsupported (judge v1, Wilson 95% CI) | Retrieval Latency |
|---|---:|---:|---:|---:|
| Baseline (top-3, no rerank) | 66 | 92.4% | 0/66 = 0.0% (0.0–5.5%) | 4.1s |
| Plain top-5 (no rerank) | 74 | 86.5% | 1/74 = 1.4% (0.2–7.3%) | 4.5s |
| Rerank 20→3 | 84 | 78.6% | 0/84 = 0.0% (0.0–4.4%) | 20.7s |
| Rerank 20→5 | 69 | 85.5% | 0/69 = 0.0% (0.0–5.3%) | 20.4s |

**Conclusion:** reranking adds 4--5x retrieval latency with no reliable grounding benefit. It ships default-off. The measurement framework is the deliverable -- it's what demonstrates the feature isn't needed, rather than assuming it would help.

### QLoRA Fine-Tuning Experiment

Can a small local model replace Claude Haiku on section generation at lower cost?

I fine-tuned **Qwen2.5-1.5B-Instruct** with QLoRA on 104 deterministic, Claude-free training pairs built from real SEC filings and financial data. When enabled, the fine-tuned model is routed 2 of 4 brief sections (Financial Health and Risk Factors); the other two stay on Haiku because deterministic targets couldn't be built for them -- an honest finding about the data, not a gap to paper over. **The measured verdict (2026-09-05/06, 40-ticker in-cluster A/B, judge v2, same image and index): the fine-tune fails the 5% grounding gate -- 8.15% unsupported (`lsnnc`, 30/368, Wilson 95% CI 5.8–11.4%) vs a 3.06% hosted baseline (`j4cnp`, 12/392, CI 1.8–5.3%), Fisher p = 0.0023 -- and the failure concentrates in exactly the two sections it owns (19.82%, 22/111, CI 13.5–28.2%, vs 0.50%, 1/202, CI 0.1–2.8%, on attributed claims; same two runs), so it ships default-off.** These are judge-flagged v2 rates; reweighted true-rate estimates are 8.3% (CI 5.5–12.5%) vs 5.7% (CI 3.5–9.9%), and the direction stands because both arms share the judge. The rest of this section is the experiment record.

**No measurable full-brief cost reduction.** Measured with the committed cost
harness (`scripts/cost_report.py`; details in [benchmarks.md](../benchmarks.md)),
Sonnet synthesis dominates the bill: hosted $0.0316/brief vs hybrid
$0.0321/brief (both on the pre-retrieval-fix pipeline; the current cost of
record is **$0.0366/brief**, 2026-09-06 post-retrieval-fix) -- the saving on
the two local sections is within run-to-run variance. Shipped default-off.

**Aug 2026 re-measure ([benchmarks.md](../benchmarks.md)):** the grounding
regression reproduced in direction -- grounding (supported share) 86.2% hosted
(56/65, Wilson 95% CI 75.7–92.5%) vs 77.8% hybrid (56/72, CI 66.9–85.8%);
judge v1, 9 tickers balanced, pre-retrieval-fix, local `grounding_check.py`
run with no workflow run ID. The local model runs behind a pluggable OpenAI-compatible backend
(`LOCAL_MODEL_BACKEND=openai`); on this AVX2-only dev CPU the prebuilt vLLM
image SIGILLs (root-caused to its AVX-512 requirement), so locally the code
path is exercised via Ollama's `/v1` endpoint.

**Sep 2026 GPU serving + in-cluster A/B:** vLLM v0.10.2 served the merged
fine-tune pinned to one A10 on an OCI VM -- plain Docker (2026-09-02), then
in-cluster on single-node k3s (2026-09-03) -- and the gated eval DAG ran a
40-ticker A/B against it (2026-09-05/06, judge v2, same image and index both
arms): **8.15% unsupported (`lsnnc`, 30/368, CI 5.8–11.4%) vs the hosted
baseline 3.06% (`j4cnp`, 12/392, CI 1.8–5.3%), Fisher p = 0.0023** -- the
local-model arm fails the 5% gate, the hosted baseline passes, and
per-section attribution places the excess entirely in the two
fine-tune-owned sections (**19.82%, 22/111, CI 13.5–28.2% vs 0.50%, 1/202,
CI 0.1–2.8%**, p = 4.6e-10). An earlier 10-ticker pass agreed in direction
but could not separate the arms (dated records in
[docs/eval-methodology.md](eval-methodology.md)). A measured negative
result, and the reason `USE_LOCAL_MODEL` ships off.

**Four-arm comparison (2026-09-23, a dated comparison set, not numbers of
record; 40 tickers, judge v2, identical pinned sampling).** To separate
training from model size, the same harness scored four arms that differ
only in who writes Financial Health and Risk Factors: each local model
writes those two sections, while Haiku writes the other two and Sonnet the
synthesis in every arm. Unsupported rates: the hosted baseline (`kcf7s`,
4/383 = 1.04%, CI 0.4–2.7%; its same-image rerun `dvvxk` 7/389 = 1.80%, CI 0.9–3.7%), the fine-tune (`v924f`, 25/385 = 6.49%, CI 4.4–9.4%), its
untuned base Qwen2.5-1.5B-Instruct (`4nfsm`, 31/400 = 7.75%, CI 5.5–10.8%),
and untuned Qwen2.5-7B-Instruct (`cnkp2`, 18/393 = 4.58%, CI 2.9–7.1%). The
fine-tune matched its own base (p = 0.58); within Qwen2.5, 1.5B → 7B
improved with borderline significance (p = 0.076) at 3.7x lower serving
throughput on the same A10; and every open-weight arm trailed hosted (7B vs
hosted p = 0.0039). Judge-flagged v2 rates; comparisons hold in
direction because all arms share the judge. Details: [docs/eval-methodology.md](eval-methodology.md).

I also re-implemented the same fine-tune with a hand-written PyTorch training loop (`fine_tune_pytorch_loop.ipynb`) -- custom `Dataset`, manual gradient accumulation and `optimizer.step()`, hand-written cosine LR, no Hugging Face `Trainer`. Benchmarked against the `Trainer` on identical data and config (`adamw_torch`, cosine schedule, grad-accum 8), the two loss curves track each other closely over 21 optimizer steps -- both start around 1.4--1.5 and trend down together, finishing at **0.50 (native)** and **0.35 (Trainer)**. The curves cross repeatedly, so that final-step gap sits within the run-to-run noise at this scale (~7 optimizer steps/epoch, plus shuffle order and 4-bit-kernel non-determinism) rather than a systematic difference -- confirming the hand-written loop reproduces the Trainer's training dynamics at the gradient-accumulation and optimizer-step level.

![Native PyTorch loop vs HF Trainer -- training loss over 21 optimizer steps, same data and config](native_loop_vs_trainer.png)

![Native PyTorch QLoRA loop -- micro-batch loss vs the smoother optimizer-step loss](native_loop_detail.png)

### Multi-Agent Orchestration Experiment

Does breaking the single agent into a supervisor-orchestrated team improve
grounding, or just add cost?

I refactored the brief pipeline into a supervisor graph: a **planner** decomposes
the ticker into SEC retrieval sub-questions and coverage points, a **research**
agent executes the plan against the existing RAG and model-routing code, an inline
**grounding-critic** scores the drafted brief with the same LLM-as-judge used by
the offline eval, and a **supervisor** sends the brief back for revision (bounded
at 2 passes) until it clears a grounding threshold. It is flag-gated behind
`MULTI_AGENT_ENABLED` (default off), with the original single-agent pipeline kept
as the A/B control. The inline critic and the offline judge share one definition,
so there is a single source of truth for grounding.

I ran both paths over the standard 10-ticker set, scored by the same
temperature-0 Sonnet judge, with retrieval held at baseline (reranking off, top-3)
on both sides so the only differences were the planner-driven queries and the
critic loop. Critic threshold: 5% unsupported. A dated record: Jun 2026,
judge v1, pre-retrieval-fix, local runs (pre-Argo, no workflow run IDs);
intervals from `eval/stats.py`.

| Path | Claims | Unsupported (judge v1, Wilson 95% CI) | Latency/brief | Revisions/brief |
|---|---:|---:|---:|---:|
| Single-agent (control) | 73 | 1/73 = 1.4% (0.2–7.4%) | 26.1s | 0.00 |
| Multi-agent | 71 | 0/71 = 0.0% (0.0–5.1%) | 43.9s | 0.00 |
| Delta | | -1.4 pts | +68% | n/a |

The multi-agent path also costs more per brief (an extra Haiku planner call
and a Sonnet critic call on every brief). The cost ratio this experiment
recorded came from an uncommitted harness, so it is kept only as a historical
note in [docs/PHASE0_AUDIT.md](PHASE0_AUDIT.md) and not quoted here; the
current re-runnable cost of record for the single-agent pipeline is
**$0.0366/brief** (2026-09-06, post-retrieval-fix; `scripts/cost_report.py`).

Two findings, stated plainly:

1. **The critic fired 0 revisions across all 10 real drafts.** The base pipeline
   already drives unsupported claims to the floor (1/73 on the control arm
   above; a later re-measure on 2026-08-24 found 0/84, Wilson 95% CI
   0.0–4.4%, judge v1, pre-retrieval-fix, local run with no workflow run ID) on the
   Executive Summary and Outlook sections this eval scores, so the critic looked at
   every first draft, found nothing to fix, and passed it. There was no headroom
   for the revision loop to recover.

2. **The one single-agent unsupported claim did not reproduce.** Across 73
   single-agent claims exactly one was flagged (on WMT). Re-running WMT produced a
   different draft with zero unsupported claims, confirming the lone flag was
   temperature-0.2 generation variance, not a systematic weakness in the base
   synthesis prompt.

The orchestration adds cost and latency (the planner adds a Haiku call, and the
inline critic adds a Sonnet judge to every brief) for a grounding benefit that,
on this workload, was null.

**Conclusion: it ships default-off.** On this workload the multi-agent path showed
no grounding benefit because the single-agent baseline was already at the
grounding floor, leaving nothing for the critic to recover. That is a statement
about this corpus, not a general claim about multi-agent orchestration. The
revision loop itself is verified working (an injected bad draft with a fabricated
price target is caught by the live judge, sent back, and cleaned on the second
pass); it is dormant in practice, not broken. The harness is retained to
re-measure if a harder corpus, thinner retrieval, a weaker base model, or longer
briefs ever create real grounding headroom. If that happens, a three-way
comparison (baseline / planner-only / planner+critic) is the documented next step
to attribute any gain to the planner versus the critic. As with the reranking
experiment, the deliverable is the measurement that shows when the feature is and
is not worth its cost.

## Benchmark summary (from the README, 2026-10-08)


| Measurement | Result |
|---|---|
| Numbers of record, deterministic (40 tickers, image `f3043751`, no judge) | wrong stock figures 1/565 hosted vs 1/432 A10; currency-label errors 0 and 0 (22 and 11 before the fix); figures bound to stock data 4.47 vs 3.05 per brief |
| Grounding, numbers of record (40 tickers, judge v2, three judgings) | judge-flagged unsupported, mean (range): hosted `4hsn2` 2.55% (1.47–3.76%) vs A10 `nstp9` 3.57% (3.27–3.75%), no difference detected; CPU `8vpq6` 2.89% on the previous image `1f51dad`. Judge precision ~29%, recall ~11% on these runs |
| Grounding, former numbers of record (one judging, image `1f51dad`) | hosted `9jzmj` 7/411 = 1.70% (CI 0.8–3.5%), CPU `8vpq6` 9/248 = 3.63% (CI 1.9–6.8%), A10 `p9jr2` 6/245 = 2.45% (CI 1.1–5.2%); no pair separates |
| Grounding, former number of record (2026-09-05/06, 512-token RAG cap) | 12/392 = 3.06% unsupported (Wilson 95% CI 1.8–5.3%), hosted baseline `j4cnp`; reweighted true-rate estimate 5.7% (CI 3.5–9.9%); not a before/after with the later runs |
| Grounding, dated (2026-08-24, 10 tickers, judge v1, pre-retrieval-fix) | 49% pre-fix → 0/84 unsupported (CI 0.0–4.4%) — a lower bound on an exhibit-indexing pipeline; retired as current |
| Cost/brief, hosted (exact API tokens + RAG estimate) | **$0.0366** (2026-09-06, post-retrieval-fix; re-runnable: `make cost-report`) |
| Grounding (supported share), hosted vs local-hybrid (9-ticker balanced A/B, Aug 2026, judge v1, pre-retrieval-fix, local run — no workflow run ID) | 86.2% (56/65, CI 75.7–92.5%) vs 77.8% (56/72, CI 66.9–85.8%) — expected regression, local stays default-off |
| Grounding, hosted vs in-cluster vLLM fine-tune (40-ticker A/B, 2026-09-05/06, judge v2) | `j4cnp` 3.06% (12/392, CI 1.8–5.3%) vs `lsnnc` 8.15% (30/368, CI 5.8–11.4%) unsupported, Fisher p = 0.0023 — local-model arm fails the 5% gate; ships default-off. Per-section: 0.50% (1/202, CI 0.1–2.8%) vs 19.82% (22/111, CI 13.5–28.2%) on fine-tune-owned claims (p = 4.6e-10). Judge-flagged rates; reweighted true-rate estimates 5.7% vs 8.3%, direction unaffected (same judge); see [docs/eval-methodology.md](eval-methodology.md) |
| Four-arm comparison (2026-09-23, 40 tickers, judge v2, identical pinned sampling) — a dated comparison set, not numbers of record | Unsupported: hosted `kcf7s` 1.04% (4/383, CI 0.4–2.7%) and its same-image rerun `dvvxk` 1.80% (7/389, CI 0.9–3.7%); fine-tune `v924f` 6.49% (25/385, CI 4.4–9.4%); untuned Qwen2.5-1.5B `4nfsm` 7.75% (31/400, CI 5.5–10.8%); untuned Qwen2.5-7B `cnkp2` 4.58% (18/393, CI 2.9–7.1%). Fine-tune vs its base p = 0.58; 1.5B vs 7B p = 0.076 (borderline); 7B vs hosted p = 0.0039 |
| Judge v2 calibration of record (2026-10-07, on `4hsn2` + `nstp9`) | precision on UNSUPPORTED 29.4% (CI 8.3–52.9%), population-weighted recall 11.4% (CI 3.1–27.9%), majority of three judgings; v2 rates are judge-flagged rates |
| Judge v2 September calibration (2026-09-24), a dated record since 2026-10-07 | kappa 0.580; UNSUPPORTED precision 60.0% (35.7–80.2%), population-weighted recall 32.5% on `j4cnp` (16.0–52.4%), judge-SUPPORTED stratum from a blind relabel of 123 claims; v2 rates are judge-flagged rates |
| Critic recall on injected failures | 20/20 = 100% (CI 83.9–100%) on both runs (2026-09-04); adjudicated precision 24/24 |
| Cost/brief, hosted vs local-hybrid (pre-retrieval-fix pipeline) | $0.0316 vs $0.0321 — no measurable full-brief saving (Sonnet dominates) |
| Local CPU serving (environment-limited: 2-core AVX2 laptop) | ~7.7 tok/s aggregate saturation; NOT comparable to GPU/hosted |
| CPU inference, Xeon on `vm-a10-inst-2` (2026-09-28; a dated measurement, not a number of record: vLLM v0.10.2 CPU backend, 14 cores, BF16, same shape as the A10 run) | financial-lora: 22.9 vs 708.3 output tok/s on the node's A10 at concurrency 8; 15.0 vs 111.1 at concurrency 1, where time to first token is about 115x the A10's and time per output token about 5x. Intel Xeon Platinum 8358 (no AMX), not tuned, no quality eval; see [docs/eval-methodology.md](eval-methodology.md#cpu-inference-benchmark-2026-09-28-a-dated-measurement) |

