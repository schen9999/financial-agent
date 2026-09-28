# Model recommendation: who writes the sections

2026-09-28. Every figure below comes from
[numbers-of-record.md](numbers-of-record.md),
[eval-methodology.md](eval-methodology.md), or the committed script named
beside it. No new eval runs went into this page.

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
  (p = 0.0039 or lower against `kcf7s`).
- **If data must stay in the tenancy: Qwen2.5-7B-Instruct.** It is the
  best open-weight arm at 4.58%, but it clears the 5% gate on the point
  estimate only (CI 2.9-7.1%). It serves at about a quarter of the 1.5B's
  throughput, though mean brief time did not change (32.7 s vs 32.8 s
  hosted). On the two sections it writes, it trails hosted 3.61% vs 0.50%
  (p = 0.050, borderline). Below 363 briefs an hour, the A10 costs more
  than the hosted sections it replaces.
- **Do not use the 1.5B, tuned or untuned.** Both fail the gate, and the
  QLoRA fine-tune did not beat its own base model (6.49% vs 7.75%,
  p = 0.58).

## 3. Results

Four arms, same 40 tickers, judge v2, all from the image built 2026-09-23
(`dvvxk` ran 2026-09-24 on the same image). Node `vm-a10-inst-2`
(VM.GPU.A10.1, single-node k3s), vLLM v0.10.2, identical pinned sampling.
A dated comparison set, not numbers of record.

| Arm (writes FH + RF) | Run | Unsupported, judge-flagged (v2) | 95% CI | Output tok/s (A10) | Mean E2E per request (A10) | Mean brief time | Cost of FH + RF per brief |
|---|---|---|---|---|---|---|---|
| Hosted (Haiku) | `kcf7s`; rerun `dvvxk` | 4/383 = 1.04%; 7/389 = 1.80% | 0.4-2.7%; 0.9-3.7% | n/a | not measured | 32.8 s; 34.4 s | at most $0.0055 (full brief $0.0366, cost of record) |
| Qwen2.5-7B-Instruct | `cnkp2` | 18/393 = 4.58% | 2.9-7.1% | 194.6 | 10517 ms | 32.7 s | A10: $0.0182 one at a time; $0.00057 busy |
| Qwen2.5-1.5B-Instruct | `4nfsm` | 31/400 = 7.75% | 5.5-10.8% | 711.3 | 2878 ms | 34.0 s | A10: $0.0189; $0.00031 |
| QLoRA fine-tune (1.5B, merged) | `v924f` | 25/385 = 6.49% | 4.4-9.4% | 711.5 | 2877 ms | 34.1 s | A10: $0.0190; $0.00041 |

Exact two-sided Fisher, no multiplicity correction: fine-tune vs its base
p = 0.58; 7B vs hosted `kcf7s` p = 0.0039; 1.5B vs 7B p = 0.076 (not
significant at 0.05). The two hosted runs on the same image: p = 0.55.

Throughput and E2E latency are from `vllm bench serve` on the A10 at 1024
input / 256 output tokens, concurrency 8. Hosted Haiku was not
benchmarked at that shape. Brief time is the eval's mean per-brief
pipeline time (retrieval, then the four sections in parallel, then
synthesis), with two tickers in flight at a time. Mean retrieval time
alone varied from 8.5 to 13.3 s across these runs, so brief-time
differences of a second or two carry no signal. Cost columns are in
section 4.

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
- **Partial swap:** only FH + RF changed between arms (section 1).
- **One run per open-weight arm**, 40 tickers, live inputs (news and
  filings fetched at run time).
- **Not a model-size curve.** Hosted Haiku is a different model family
  (size undisclosed). Only the three Qwen2.5 arms share a family.
- **Serving was single-node k3s** on one A10 (2026-09-23). Serving on OKE
  has not run.

## 6. Next steps

- Add a CPU inference column (the node's Xeon) for the 1.5B, if that run
  is made.
- A full open-weight pipeline, with open-weight synthesis and judge, would
  be a separate study.
- Audit the locally served sections directly. Today the judge reads only
  the synthesis, and section rates come from heuristic attribution.

## Appendix: sources

| Figure | Source |
|---|---|
| Rates, CIs, all-claims p-values | numbers-of-record, "Four-arm model comparison"; [eval-methodology](eval-methodology.md#four-arm-model-comparison-2026-09-23--a-dated-comparison-set); per-claim rows `eval/runs/{kcf7s,dvvxk,v924f,4nfsm,cnkp2}-claims.jsonl` |
| Hosted rerun p = 0.55; hosted rate across images | numbers-of-record, dated run records; `eval/compare_runs.py` |
| FH + RF rates, CIs, p-values, coverage | `python eval/multi_arm_stats.py --run hosted eval/runs/kcf7s-claims.jsonl eval/runs/raw/kcf7s-findings --run lora eval/runs/v924f-claims.jsonl eval/runs/raw/v924f-findings --run 1.5b eval/runs/4nfsm-claims.jsonl eval/runs/raw/4nfsm-findings --run 7b eval/runs/cnkp2-claims.jsonl eval/runs/raw/cnkp2-findings` |
| Output tok/s, E2E latency | `eval/runs/bench/<served-name>.json` from `scripts/vm_bench_serve.sh` (the script refuses to run unless the pod serves that name; `model_id` in the JSON is the fixed in-pod mount path) |
| Brief time, retrieval time | `eval/runs/<run>-aggregate.txt`, TOTAL row, Pipe(s) and Retr(s) (`grounding_check.py` `pipeline_s`) |
| Cost per brief (A10), T, break-even | `python scripts/cost_per_brief_selfhost.py --gpu-hourly-usd 2.00` over the findings, bench JSONs, aggregates and `cost_record_post_fix.json` |
| $0.0366 full brief | cost of record, 2026-09-06, `scripts/cost_report.py` |
| A10 price | [cost.md](cost.md), OCI price-list API, retrieved 2026-09-24 |
