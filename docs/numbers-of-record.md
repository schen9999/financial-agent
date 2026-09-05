# Numbers of record

One table of numbers that may be quoted, one table of numbers and claims
that are retired. Rule: **a number may only appear in docs if a
committed, re-runnable harness produced it.** Anything not yet measured
on OCI is written exactly as: to be measured in Phase 2.

## Current

Every rate carries its Wilson 95% interval (computed by the committed
`eval/stats.py`); the pre-fix 49% figure predates the harness and has no
recorded denominator, so no interval can honestly be attached to it.

| Metric | Number of record | Source (committed harness) |
|---|---|---|
| Grounding | 49% pre-fix → 0/84 unsupported in current eval (95% CI 0.0–4.4%). Judge v1; v1 recall on UNSUPPORTED measured 1/9 against human labels, so this rate is a lower bound | `grounding_check.py` via the Argo grounding-eval DAG (nightly + `make eval-run`); interval: `eval/stats.py` |
| Judge validation (v1, 50-claim sample, 2026-09-04) | Cohen's kappa 0.321; recall on UNSUPPORTED 1/9 = 11.1% (95% CI 2.0–43.5%); precision 1/3 = 33.3% (95% CI 6.1–79.2%). Human-UNSUPPORTED claims mostly filed as INFERENCE. Author-adjudicated labels, not blind (method + limitations: eval-methodology, "Judge validation") | `eval/agreement.py` on `eval/judge_validation/sample.csv` |
| Cost per brief | $0.0316. Observed, no fix: RAG answer synthesis over identical cached context differed across runs (XOM, 2026-08-24 sample rows 3 and 25), so token counts — and this cost — carry that run-to-run variance | `scripts/cost_report.py` (`make cost-report`) |
| Critic recall on injected failures | 20/20 = 100% (95% CI 83.9–100%) on both runs (2026-09-04, runs 1 and 2). Run 2, with every flag persisted and adjudicated: raw precision vs injection tags 20/24 = 83.3% (95% CI 64.1–93.3%); **adjudicated precision 24/24 = 100% (95% CI 86.2–100%)** — all 4 off-needle flags were genuinely unsupported (3 injection cascades, 1 pre-existing), 0 false positives (adjudication table: eval-methodology, "Injected-failure check") | `eval/perturb.py` fixtures + `eval/critic_check.py`; re-runnable in CI (`critic-injection.yml`, asserts recall ≥ 0.8) |
| Cost per brief on OCI | to be measured in Phase 2 | same harness, re-run on OKE |
| vLLM serving on the A10 (throughput/latency) | to be measured in Phase 2 | `scripts/vllm_benchmark.py` against the oke-gpu deployment |

Quoting rules for the grounding number: always with the pre-fix context
and the denominator — never a bare "0%".

## Dated run records

Quotable with their dates; each from a committed harness. These are run
records, not headline numbers of record.

| Record | Value | Source (committed harness) |
|---|---|---|
| Extended baseline, 40 tickers (2026-09-05, `grounding-eval-extended-9j2dj`) | Judge v2, post-retrieval-fix index: 387 claims (357 S / 12 U / 18 I), **3.10% unsupported (95% CI 1.8–5.3%)** — point estimate below the 5% gate; the interval includes the gate. INFERENCE share 4.7% vs ~20% under v1. 40/40 tickers (the five ADRs ran without SEC context); per-ticker claims ranged 1–23; UPST the outlier at 3/14 unsupported. 27 min, est. $2.35. NOT the number of record — that decision waits for the local-model arm and the held-out judge validation | grounding-eval DAG; artifacts `eval/runs/9j2dj-*`, per-claim rows `eval/runs/9j2dj-claims.jsonl` |
| Grounding A/B, hosted vs in-cluster vLLM fine-tune (2026-09-03, 10 tickers) | 3.03% (2/66, CI 0.8–10.4%) vs 12.31% (8/65, CI 6.4–22.5%) unsupported, Fisher p=0.0545; local-model arm failed the 5% gate, baseline passed. Judge v1; v1 recall on UNSUPPORTED measured 1/9 against human labels, so both rates are lower bounds — the A/B *direction* is unaffected because both arms used the same judge | grounding-eval DAG runs (eval-methodology dated A/B); intervals `eval/stats.py` |
| Grounding, hosted vs local-hybrid (Aug 2026, 9-ticker balanced) | 86.2% vs 77.8% | `grounding_check.py` A/B, benchmarks.md |
| Cost, hosted vs hybrid | $0.0316 vs $0.0321 per brief — sections saving within run-to-run variance | `scripts/cost_report.py`, benchmarks.md |
| Cost harness, early run (2026-08-24, 3-ticker mean) | $0.0336/brief = $0.0272 exact (4 Haiku sections + Sonnet synthesis) + $0.0064 RAG-internal estimate — a dated run record; the cost of record is $0.0316 (Current table) | `scripts/cost_report.py` |
| First nightly gate fire (2026-08) | 5.62% unsupported, one NVDA outlier draft; re-measure 0/10 → variance, threshold kept at 5% | Argo run + NVDA re-measure, README red-night playbook |
| Local CPU serving (environment-limited) | ~7.7 tok/s aggregate saturation; p50 13.3s→74.1s at concurrency 1→8; not comparable to GPU/hosted | `scripts/vllm_benchmark.py`, benchmarks.md |
| Pipeline latency | 26.29s mean (~26s) per brief | `grounding_check.py` pipeline timing, Phase 0 re-measure |
| K8s smoke test | 13/13 assertions | `scripts/k8s_smoke_test.sh` |
| Retrieval defect fix (2026-09-04) | Pre-fix: 3/40 tickers' risk retrieval passed verification (32 served exhibit/TOC text; 5 ADRs unfetchable). Post-fix: 32/40 pass; remaining 8 itemized in eval-methodology "Retrieval defect". Grounding numbers dated before 2026-09-04 measured the pipeline against exhibit text for most tickers and stand as dated records of that pipeline | `scripts/reindex_filings.py` verify pass |
| Cost harness, post-retrieval-fix run (2026-09-04, 3-ticker mean) | $0.0364/brief = $0.0280 exact + $0.0084 RAG-internal estimate — richer risk contexts lengthen inputs; the cost of record remains $0.0316 pending a full re-measure decision | `scripts/cost_report.py` |
| Test suite | 1222 lines, 80 tests (79 free + 1 credit-gated) | `python -m pytest tests/ --collect-only` |

## Retired

| Retired number / claim | Why retired | Say instead |
|---|---|---|
| $0.0269 per brief | superseded by the committed cost harness | $0.0316 (source above) |
| "54% cost reduction" | sections-only framing; the full-brief comparison does not support it | nothing — the claim is retired without replacement |
| bare "0% unsupported" | drops the pre-fix baseline and the denominator | "49% pre-fix → 0/84 unsupported in current eval (judge v1)" |
| "semantic cache" | the Redis cache is an exact-key cache (`research:{TICKER}`) | "exact-key cache per ticker" |
| "Celery/Redis ran in production on ECS" | ECS reality was a single FastAPI container + RDS | "K8s is the first full-topology deployment" |
| "vLLM will serve the model" as a pending claim | superseded — vLLM served the fine-tune on an A10 (Docker 2026-09-02, in-cluster k3s 2026-09-03) and the eval A/B against it failed the gate | "vLLM served the fine-tune on an A10; the in-cluster A/B was 3.03% (0.8–10.4%) vs 12.31% (6.4–22.5%), judge v1, p=0.054 — ships default-off" (dated records in eval-methodology.md; OKE serving still ungated) |

## Framing rules that travel with the numbers

- Cross-encoder reranking and the multi-agent supervisor **shipped
  default-off because evals showed no grounding gain at higher
  cost/latency** — state it that way, not as unfinished work.
- When vLLM actually serves on the A10 (Phase 2), CLAUDE.md is updated
  first and the claim becomes legitimate everywhere.
