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
| Grounding | 49% pre-fix → 0/84 unsupported in current eval (95% CI 0.0–4.4%) | `grounding_check.py` via the Argo grounding-eval DAG (nightly + `make eval-run`); interval: `eval/stats.py` |
| Cost per brief | $0.0316 | `scripts/cost_report.py` (`make cost-report`) |
| Cost per brief on OCI | to be measured in Phase 2 | same harness, re-run on OKE |
| vLLM serving on the A10 (throughput/latency) | to be measured in Phase 2 | `scripts/vllm_benchmark.py` against the oke-gpu deployment |

Quoting rules for the grounding number: always with the pre-fix context
and the denominator — never a bare "0%".

## Retired

| Retired number / claim | Why retired | Say instead |
|---|---|---|
| $0.0269 per brief | superseded by the committed cost harness | $0.0316 (source above) |
| "54% cost reduction" | sections-only framing; the full-brief comparison does not support it | nothing — the claim is retired without replacement |
| bare "0% unsupported" | drops the pre-fix baseline and the denominator | "49% pre-fix → 0/84 unsupported in current eval" |
| "semantic cache" | the Redis cache is an exact-key cache (`research:{TICKER}`) | "exact-key cache per ticker" |
| "Celery/Redis ran in production on ECS" | ECS reality was a single FastAPI container + RDS | "K8s is the first full-topology deployment" |
| "vLLM will serve the model" as a pending claim | superseded — vLLM served the fine-tune on an A10 (Docker 2026-09-02, in-cluster k3s 2026-09-03) and the eval A/B against it failed the gate | "vLLM served the fine-tune on an A10; the in-cluster A/B was 3.03% (0.8–10.4%) vs 12.31% (6.4–22.5%), p=0.054 — ships default-off" (dated records in eval-methodology.md; OKE serving still ungated) |

## Framing rules that travel with the numbers

- Cross-encoder reranking and the multi-agent supervisor **shipped
  default-off because evals showed no grounding gain at higher
  cost/latency** — state it that way, not as unfinished work.
- When vLLM actually serves on the A10 (Phase 2), CLAUDE.md is updated
  first and the claim becomes legitimate everywhere.
