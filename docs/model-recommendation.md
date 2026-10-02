# Model recommendation: who writes the sections

2026-09-28. Every figure below comes from
[numbers-of-record.md](numbers-of-record.md),
[eval-methodology.md](eval-methodology.md), or the committed script named
beside it. One eval run was added later: the W4A16 row, a dated
2026-09-29 run (eval-methodology, "Quantization benchmark"). The CPU
serving column comes from a 2026-09-28 benchmark on the same node
(eval-methodology, "CPU inference benchmark"), except the GGUF row, a
2026-09-29 benchmark (same section as W4A16); no eval ran with CPU
serving. The numeric-accuracy figures (section 3) come from the
2026-10-01 adjudication of the deterministic numeric check's flags over
the same runs and a pre-registered frozen-input replication
(eval-methodology, "Numeric check: adjudicated flags and the W4A16
replication").

## 1. Question

Which model should write the Financial Health and Risk Factors sections of
the Financial Research Agent's brief: hosted Claude Haiku, or an
open-weight model served by vLLM on an OCI A10?

Scope: the open-weight arms were a **partial swap**. The local model wrote
only those two sections. In every arm Haiku wrote Recent Developments and
SEC Filing Highlights, Sonnet wrote the synthesis (Executive Summary and
Outlook), and Sonnet judged it. This is not a full open-weight pipeline,
and nothing here says how one would perform.

## 2. Recommendation

- **Production: keep hosted Haiku.** It has the lowest unsupported rate
  (1.04% and 1.80% on two runs), and every open-weight arm trailed it
  (p = 0.0039 or lower against `kcf7s`). It also states the fewest wrong
  stock figures: 1.2% and 0.7% of checked numbers on those runs
  (adjudicated). On those two runs, every wrong figure traces to two
  defects in the stock data, not to the model.
- **If data must stay in the tenancy: Qwen2.5-7B-Instruct.** It is the
  best open-weight arm at 4.58%, but it clears the 5% gate on the point
  estimate only (CI 2.9-7.1%). On the two sections it writes, its gap to
  hosted is borderline: 3.61% vs 0.50%, p = 0.050, just above 0.05 and
  so not significant at that level. On numeric accuracy it is also the
  best open-weight arm: 3.9% of checked figures wrong (CI 1.7-6.9%),
  against 14.9% to 22.3% for the 1.5B models on the same image. It
  serves at about a quarter of the
  1.5B's throughput, but mean brief time was unchanged (32.7 s vs 32.8 s
  hosted). Below 363 briefs an hour, the A10 costs more than the hosted
  sections it replaces.
- **Do not use the 1.5B, tuned or untuned.** Both fail the gate, and the
  QLoRA fine-tune did not beat its own base model (6.49% vs 7.75%,
  p = 0.58). It does not improve numeric accuracy either: 15.7% of
  checked figures wrong for the fine-tune `v924f` (CI 11.7-19.6%) vs
  14.9% for its base (CI 11.5-18.6%), not compared by a test.
- **W4A16 vs BF16 does not change this.** On identical inputs, the
  pre-registered replication does not show the 4-bit fine-tune stating
  more wrong stock figures than BF16: +5.3 pts, CI -1.1 to +11.6, and
  adjudication leaves that unchanged. Its interval cannot rule out a gap
  of up to 11.6 pts either, so this is neither a measured regression nor
  a shown equivalence. Both precisions fail the grounding gate anyway.

## 3. Results

Four arms, same 40 tickers, judge v2, all from the image built 2026-09-23
(`dvvxk` ran 2026-09-24 on the same image). Node `vm-a10-inst-2`
(VM.GPU.A10.1, single-node k3s), vLLM v0.10.2, identical pinned sampling.
A dated comparison set, not numbers of record.

| Arm (writes FH + RF) | Run | Unsupported, judge-flagged (v2) | 95% CI | Output tok/s (A10) | Output tok/s (Xeon CPU) | Mean E2E per request (A10) | Mean brief time | Cost of FH + RF per brief |
|---|---|---|---|---|---|---|---|---|
| Hosted (Haiku) | `kcf7s`; rerun `dvvxk` | 4/383 = 1.04%; 7/389 = 1.80% | 0.4-2.7%; 0.9-3.7% | n/a | n/a | not measured | 32.8 s; 34.4 s | at most $0.0055 (full brief $0.0366, cost of record) |
| Qwen2.5-7B-Instruct | `cnkp2` | 18/393 = 4.58% | 2.9-7.1% | 194.6 | not run | 10517 ms | 32.7 s | A10: $0.0182 one at a time; $0.00057 busy |
| Qwen2.5-1.5B-Instruct | `4nfsm` | 31/400 = 7.75% | 5.5-10.8% | 711.3 | 22.9 | 2878 ms | 34.0 s | A10: $0.0189; $0.00031 |
| QLoRA fine-tune (1.5B, merged) | `v924f` | 25/385 = 6.49% | 4.4-9.4% | 711.5 | 22.9 | 2877 ms | 34.1 s | A10: $0.0190; $0.00041 |
| QLoRA fine-tune, GPTQ W4A16 (dated, 2026-09-29) | `r5nzh` | 23/344 = 6.69% | 4.5-9.8% | 1075.7 | n/a (GPU format) | 1903 ms | 34.0 s | not computed |
| QLoRA fine-tune, GGUF F16 / Q8_0 / Q4_K_M on llama.cpp (dated, 2026-09-29) | none | not evaluated | n/a | not run | 52.3 / 51.7 / 64.5 | n/a | not measured | not computed |

Exact two-sided Fisher, no multiplicity correction: fine-tune vs its base
p = 0.58; 7B vs hosted `kcf7s` p = 0.0039; 1.5B vs 7B p = 0.076 (not
significant at 0.05). The two hosted runs on the same image: p = 0.55.

**W4A16 (2026-09-29, a dated addition).** The fine-tune quantized to
4-bit weights (GPTQ W4A16, group size 128) and served on the same A10,
image and settings six days after the other arms. Its only supported
claim is against the BF16 fine-tune: 23/344 vs 25/385, p = 1.00 (on
FH + RF, 15/96 vs 15/112, p = 0.70): no detectable difference at this
sample size, which is not proof of equivalence. That finding covers the
judge's audited sections (Exec Summary + Outlook; the FH + RF split is
audited claims attributed back to those sections) only. Numeric accuracy
is covered by the numeric check, below. The quantized arm also
produced fewer checkable claims (344 vs 385). It serves faster: 1075.7
vs 708.3 output tok/s at concurrency 8 against a 2026-09-28 BF16 rerun
with the same prompts (the table's 711.5 is the 2026-09-23 file). Its
weights take 1.61 GB on disk against 3.09 GB; 0.93 GB of that is the
FP16 embedding stored twice, because llm-compressor saved it untied (the
copy is byte-identical, so no weights changed). It fails the gate as the BF16
fine-tune does, so the recommendation is unchanged. Cost per brief was
not computed for it. Method and tables: eval-methodology,
["Quantization benchmark"](eval-methodology.md#quantization-benchmark-2026-09-29-a-dated-measurement).

**Numeric accuracy (adjudicated 2026-10-01, a dated addition).** The
deterministic numeric check binds every stock-data figure a brief states
to the stock data the pipeline supplied. One adjudicator read all 359
flags from these runs under rules committed beforehand: 342 were true
errors, 2 were false positives, and 15 were other defects. So the
flag rates are close to the true-error rates. Wrong figures per distinct
checked number, all sections, counting true errors only, with a
brief-level cluster bootstrap 95% CI:

| Arm | Run | Wrong stock figures | 95% CI | Excluding the two upstream data defects |
|---|---|---|---|---|
| Hosted (Haiku) | `kcf7s`; rerun `dvvxk` | 7/571 = 1.2%; 4/550 = 0.7% | 0.0-3.2%; 0.0-1.7% | 0/571; 0/550 |
| Qwen2.5-7B-Instruct | `cnkp2` | 20/511 = 3.9% | 1.7-6.9% | 9/511 = 1.8% |
| Qwen2.5-1.5B-Instruct | `4nfsm` | 63/422 = 14.9% | 11.5-18.6% | 55/422 = 13.0% |
| QLoRA fine-tune | `v924f` | 56/357 = 15.7% | 11.7-19.6% | 49/357 = 13.7% |
| QLoRA fine-tune, GPTQ W4A16 (2026-09-29) | `r5nzh` | 73/327 = 22.3% | 17.2-27.9% | 60/327 = 18.4% |

The two upstream defects are foreign filers' home-currency revenue and
net income labeled USD, and profit margin passed as a raw fraction. They
are recorded in `eval/numeric_check/upstream-findings.md` and not yet
fixed. On the live runs, W4A16 `r5nzh` vs BF16 `v924f` on the two
sections they write is +12.6 pts in true errors (CI +2.9 to +21.7,
p = 0.012), truncated sections excluded (estimated). That figure is
exploratory and post hoc: one draw per ticker, and the truncation subset
was chosen after the pilot. The pre-registered replication on identical
inputs (10 seeded samples per ticker) remains the primary result, and it
gives +5.3 pts (CI -1.1 to +11.6): the regression does not replicate. All 120 of its sampled flags
were true errors, so adjudication leaves that unchanged. Method, precision
and the full tables: eval-methodology,
["Numeric check: adjudicated flags and the W4A16 replication"](eval-methodology.md#numeric-check-adjudicated-flags-and-the-w4a16-replication-2026-10-01-dated).

Throughput and E2E latency are from `vllm bench serve` on the A10 at 1024
input / 256 output tokens, concurrency 8. Hosted Haiku was not
benchmarked at that shape. Brief time is the eval's mean per-brief
pipeline time (retrieval, then the four sections in parallel, then
synthesis), with two tickers in flight at a time. Mean retrieval time
alone varied from 8.5 to 13.3 s across these runs, so brief-time
differences of a second or two carry no signal. Cost columns are in
section 4.

**CPU serving (2026-09-28, a dated measurement).** The Xeon column is the
same client and shape at concurrency 8, run on the node's own CPU: an
Intel Xeon Platinum 8358 (Ice Lake, no AMX or AVX512_BF16), 14 of its 15
cores pinned, vLLM v0.10.2's CPU backend, BF16, not tuned. A same-day A10
rerun gave 708.3 output tok/s for the fine-tune, about 31 times the CPU's
22.9. The 7B was not run on the CPU, since the 1.5B models were under the
~30 tok/s bar set for trying it. At concurrency 1 (one brief at a time),
writing the two local sections of one brief takes an estimated 4.8 s on
the A10 and 35.0 s on the CPU for the fine-tune (29.1 s for the 1.5B base),
from the measured TTFT and TPOT and the token counts T in section 4. A mean
brief is about 34 s, so on this CPU the two sections are not short: they
alone take about as long as the whole brief. Brief time with CPU serving
was not measured. At concurrency 1 the CPU gap is mostly prompt
processing: mean TTFT is about 115 times the A10's (5985 vs 52 ms), time
per output token about 5 times (43.4 vs 8.8 ms). So prompt length, INT8
weights and AMX-capable Xeons are the next levers; none was measured.

**CPU engine and precision (2026-09-29, a dated measurement).** The same
client and shape on the same cores, with the fine-tune converted to GGUF
and served by llama.cpp (build b11223). Changing only the engine, vLLM
BF16 to llama.cpp F16, raised output throughput at concurrency 8 from
22.9 to 52.3 tok/s and cut median TTFT at concurrency 1 from 6110 to
2582 ms. Changing only the precision on llama.cpp, F16 to Q8_0 to
Q4_K_M, gave 52.3, 51.7 and 64.5 tok/s at concurrency 8 and a median
time per output token at concurrency 1 of 35.3, 26.7 and 19.0 ms. The
estimated time for one brief's two local sections at concurrency 1
drops from 35.0 s (vLLM BF16) to 23.8 s (llama.cpp F16) and 14.0 s
(Q4_K_M), still well above the A10's 4.8 s. The two effects are
separate: vLLM BF16 against llama.cpp Q4_K_M is not a quantization
speedup. GGUF quantization quality was not evaluated; only the W4A16 arm
ran through the grounding eval. The recommendation does not change: it
rests on grounding, and the 1.5B fails the gate whatever serves it.
Method and tables: eval-methodology,
["Quantization benchmark"](eval-methodology.md#quantization-benchmark-2026-09-29-a-dated-measurement).
Method, table and caveats: eval-methodology, ["CPU
inference benchmark"](eval-methodology.md#cpu-inference-benchmark-2026-09-28-a-dated-measurement).

**Locally served sections only.** The fairer comparison: the other
sections came from the same models in every arm. Claims are attributed
to the section they restate with a heuristic (`eval/multi_arm_stats.py`),
covering 78-83% of claims per arm. The buckets are diagnostic; the table
above is the measured result.

| Arm | FH + RF claims unsupported | 95% CI | p vs hosted |
|---|---|---|---|
| Hosted (Haiku), `kcf7s` | 1/199 = 0.50% | 0.1-2.8% | n/a |
| Qwen2.5-7B-Instruct, `cnkp2` | 6/166 = 3.61% | 1.7-7.7% | 0.050 |
| Qwen2.5-1.5B-Instruct, `4nfsm` | 16/146 = 10.96% | 6.9-17.1% | 6.9e-06 |
| QLoRA fine-tune, `v924f` | 15/112 = 13.39% | 8.3-20.9% | 1.3e-06 |
| QLoRA fine-tune W4A16, `r5nzh` (dated, 2026-09-29) | 15/96 = 15.62% | 9.7-24.2% | 2.6e-07 |

7B vs 1.5B on these sections: p = 0.014. Fine-tune vs its base:
p = 0.57. Every unsupported claim in this bucket came from Financial
Health; Risk Factors had none in any arm. The 7B's Risk Factors text was
restated in only 3 claims, so its row is almost entirely Financial Health.

## 4. Cost per brief

`python scripts/cost_per_brief_selfhost.py --gpu-hourly-usd 2.00`. The A10
price is the OCI list price, $2.00 per GPU-hour (part B95909, retrieved
2026-09-24, [cost.md](cost.md)). Boot volume and any other charges are
excluded. These are estimates derived from the 2026-09-23 benchmark, not
a measured cost on OCI (still "to be measured in Phase 2").

With H = A10 dollars per hour:

- **(a) Busy, at the benchmarked concurrency:** cost = H / 3600 × T / R.
  T is the FH + RF output tokens per brief. R is the output tok/s from
  the benchmark.
- **(b) One brief at a time:** cost = H / 3600 × P. P is the mean
  pipeline seconds per brief. The A10 is billed for the whole brief,
  including the time retrieval, Haiku and Sonnet take.
- **Break-even:** B = H / C briefs per hour. C is the hosted cost of the
  same two sections.

T was not recorded at run time. The estimate re-tokenizes the recorded
FH + RF text in each run's findings with the Qwen2.5 tokenizer, plus one
end-of-sequence token per section. The upper bound is the recorded cap,
2 × max_tokens 512 = 1024. C is not recorded per section either: the
harness gives $0.0055 per brief for all four Haiku sections together
(mean of AAPL, NVDA and JPM, `cost_record_post_fix.json`, 2026-09-06). So
C is at most $0.0055, and B is at least 363.

| Arm | T mean (cap) | (a) A10 per brief (at cap) | (a) capacity, briefs/hour (at cap) | (b) A10 per brief | (b) most briefs/hour |
|---|---|---|---|---|---|
| Qwen2.5-7B-Instruct | 198 (1024) | $0.00057 ($0.0029) | 3535 (684) | $0.0182 | 110 |
| Qwen2.5-1.5B-Instruct | 398 (1024) | $0.00031 ($0.0008) | 6432 (2501) | $0.0189 | 106 |
| QLoRA fine-tune | 530 (1024) | $0.00041 ($0.0008) | 4836 (2501) | $0.0190 | 106 |

- **One brief at a time (demo use)**, the A10 costs $0.018-0.019 per
  brief for the two sections: at least 3.3 times the hosted cost of the
  same sections. A serial pipeline also tops out near 110 briefs an hour,
  below break-even.
- **An always-on A10 costs $2.00 an hour, idle or busy.** It pays off
  only at a sustained 363 or more briefs an hour (about 6 a minute), with
  many briefs in flight at once. The 7B's estimated capacity at
  concurrency 8 is 3535 briefs an hour (684 at the cap).
- **The saving has a ceiling.** Self-hosting replaces at most $0.0055 of
  the $0.0366 full brief (the cost of record, measured with Haiku
  sections and Sonnet synthesis). RAG, the other two sections and the
  synthesis stay on hosted models.
- **The fine-tune overruns.** 18 of its 80 sections hit the 512-token
  cap (13 Risk Factors, 5 Financial Health) and were truncated there.
  Neither base model hit it: at most 609 tokens per brief for the 1.5B
  and 238 for the 7B. The prompts ask for 3-5 sentences and 2-3 bullets.
- (a) uses throughput measured at 1024 input / 256 output tokens. Real
  section requests differ in length, so (a) is an estimate. The hosted
  figure comes from 3 briefs on 2026-09-06; the token counts come from
  40 briefs on 2026-09-23.

## 5. Caveats

- **Rates are judge-flagged (judge v2).** Population-weighted recall on
  UNSUPPORTED is 32.5% (CI 16.0-52.4%), measured on the 2026-09-05/06
  baseline `j4cnp`, whose reweighted true rate (5.7%) is above its flagged
  3.06%. That calibration is not extended to these runs, so no true-rate
  estimate is given here. Every arm used the same judge, so the ranking
  holds in direction. See eval-methodology,
  ["Calibration of record"](eval-methodology.md#calibration-of-record-2026-09-24).
- **The hosted rate moved between images** with no code change on its
  path: 24/778 = 3.08% on the 2026-09-05 image vs 11/772 = 1.42% on the
  2026-09-23 image, p = 0.039, cause unconfirmed
  ([dated finding](eval-methodology.md#dated-finding-hosted-arm-rate-fell-between-images-2026-09-25)).
  All four arms here come from the 2026-09-23 image.
- **Numeric verdicts come from one adjudicator,** who could see the arm
  and model of each flag. There was no second rater. Precision is the
  check's against that adjudicator, and it says nothing about errors the
  check cannot bind. The currency verdicts compared figures with real USD
  values the adjudicator supplied, not with committed data.
- **Partial swap:** only FH + RF changed between arms (section 1).
- **One run per open-weight arm**, 40 tickers, live inputs (news and
  filings fetched at run time).
- **Not a model-size curve.** Hosted Haiku is a different model family
  (size undisclosed). Only the three Qwen2.5 arms share a family.
- **Serving was single-node k3s** on one A10 (2026-09-23). Serving on OKE
  has not run.

## 6. Next steps

- CPU serving was measured on the node's Xeon (section 3). A Xeon with
  AMX would be a separate measurement; it has not run. Quantized weights
  were measured on 2026-09-29 (section 3): W4A16 on the A10, with a
  grounding arm, and GGUF on the CPU, without one. A grounding arm for
  the GGUF builds would be a separate run.
- A full open-weight pipeline, with open-weight synthesis and judge, would
  be a separate study.
- Audit the locally served sections directly. The numeric check now
  covers the stock-data figures in every section (section 3). For
  everything else, the judge still reads only the synthesis, and section
  rates come from heuristic attribution.
- Fix the two upstream stock-data defects in a separate dated change,
  with a fresh baseline (`eval/numeric_check/upstream-findings.md`).

## Appendix: sources

| Figure | Source |
|---|---|
| Rates, CIs, all-claims p-values | numbers-of-record, "Four-arm model comparison"; [eval-methodology](eval-methodology.md#four-arm-model-comparison-2026-09-23--a-dated-comparison-set); per-claim rows `eval/runs/{kcf7s,dvvxk,v924f,4nfsm,cnkp2}-claims.jsonl` |
| Hosted rerun p = 0.55; hosted rate across images | numbers-of-record, dated run records; `eval/compare_runs.py` |
| FH + RF rates, CIs, p-values, coverage | `python eval/multi_arm_stats.py --run hosted eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings --run lora eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings --run 1.5b eval/runs/4nfsm-claims.jsonl eval/runs/raw/4nfsm-findings --run 7b eval/runs/cnkp2-claims.jsonl eval/runs/raw/cnkp2-findings` |
| Output tok/s, E2E latency | `eval/runs/bench/<served-name>.json` from `scripts/vm_bench_serve.sh` (the script refuses to run unless the pod serves that name; `model_id` in the JSON is the fixed in-pod mount path) |
| Brief time, retrieval time | `eval/runs/<run>-aggregate.txt`, TOTAL row, Pipe(s) and Retr(s) (`grounding_check.py` `pipeline_s`) |
| Output tok/s (Xeon CPU), section time at concurrency 1 | `eval/runs/bench/cpu-2026-09-28/*.json` and `eval/runs/bench/a10-2026-09-28/*.json` from `scripts/vm_bench_cpu.sh` and `scripts/vm_bench_serve.sh`, tabulated by `scripts/bench_table.py` (command in eval-methodology, "CPU inference benchmark") |
| Cost per brief (A10), T, break-even | `python scripts/cost_per_brief_selfhost.py --gpu-hourly-usd 2.00` over the findings, bench JSONs, aggregates and `cost_record_post_fix.json` |
| W4A16 row: rate, CI, p-values, FH + RF | `eval/runs/r5nzh-claims.jsonl` and `eval/runs/raw/r5nzh-findings/`, `eval/multi_arm_stats.py` (command in eval-methodology, "Quantization benchmark") |
| W4A16 row: output tok/s, E2E latency, weights size | `eval/runs/bench/a10-quant-2026-09-29/*.json` from `scripts/vm_bench_serve.sh`, `scripts/bench_table.py --matrix`; quantization record `quant_meta.json` there |
| GGUF rows and the CPU engine/precision paragraph | `eval/runs/bench/cpu-gguf-2026-09-29/*.json` from `scripts/vm_bench_cpu_gguf.sh` (token counts corrected by `scripts/bench_fix_llamacpp.py`), `scripts/bench_table.py --matrix` (command in eval-methodology, "Quantization benchmark") |
| Numeric accuracy table, W4A16 live gap and replication | `python scripts/numeric_adjudicated.py --date 2026-10-01` over `eval/numeric_check/adjudication.csv` (verdicts a27264b); output `eval/runs/numeric-adjudicated-2026-10-01.{json,md}`; registered replication `eval/runs/numeric-backtest-2026-09-29.md` |
| $0.0366 full brief | cost of record, 2026-09-06, `scripts/cost_report.py` |
| A10 price | [cost.md](cost.md), OCI price-list API, retrieved 2026-09-24 |
