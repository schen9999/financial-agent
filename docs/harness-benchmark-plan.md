# Harness benchmark: pre-registered plan

Status: **designed 2026-10-19, not yet run.** No result below is a
measurement; every figure used to set parameters is cited to
[numbers-of-record.md](numbers-of-record.md). Written before any run, so the
reading rules cannot be fitted to the results.

## Why

The post
[Harness Engineering using OCI CPU & OKE](https://blogs.oracle.com/cloud-infrastructure/harness-engineering-using-oci-cpu-oke)
argues that an agent harness is CPU-, memory-bandwidth- and
network-latency-bound, spends most of its time waiting on inference, and
belongs on CPU nodes. It reports no benchmark of a harness on any shape.
This project's CPU figures so far measure model inference, not the harness
([report.md](report.md), "Sizing the CPU harness"). This plan measures the
harness itself: what it costs in CPU and memory per brief, how many briefs
an hour it sustains on an E5 node, and where it saturates, with the model
removed as the bottleneck.

## Questions

1. **Overhead.** With model latency set to zero, what wall time and how
   many CPU-seconds does one brief cost the harness?
2. **Wait vs work.** With realistic model latency, is the worker busy on
   CPU or waiting? The post predicts waiting.
3. **Throughput and saturation.** How do briefs per hour scale with worker
   replicas and per-pod concurrency, and where does scaling stop on E5?
4. **Sizing rule.** How many vCPU and how much memory does the harness need
   per N briefs an hour?

## System under test

The brief request path, as deployed: the API takes `POST /research/async`,
a Celery worker runs `run_research_checked` (data fetch, retrieval, four
sections in parallel, synthesis, numeric check), and Redis and PostgreSQL
store results. Image and overlays unchanged; provided OKE cluster, E5.Flex
nodes. Today each worker pod runs `--concurrency=1` and KEDA scales 1 to 4
pods, so at most 4 briefs are in flight; that cap is a variable here, not a
fixed condition.

Out of scope for this plan: the `/ask` ReAct loop (its tool-calling
trajectories need a recorded-trajectory stub; phase 2), and the Argo eval
harness (it calls the hosted judge, which spends credit and adds hosted
latency).

## Method

**Model stub.** An OpenAI-compatible server in the cluster answers
`/v1/models`, `/props` and `/v1/chat/completions` for every LLM call site.
The app reaches it through the existing self-served route (`SLM_FULL=true`,
`SLM_ENDPOINT=cpu`, `SLM_CPU_URL` pointed at the stub): a configuration
change, no new image. Responses must parse at every site; the stub serves
recorded outputs per call site from a committed self-served run where the
ledger holds them, otherwise text of the recorded length. It logs every
request with its prompt and completion token counts. It has no capacity
limit: each request waits only its own delay, so the harness, not the
stub, is what saturates.

**Latency profiles** (per request, from single-request llama-bench rates
of the same Q4_K_M model, 2026-10-08 and 2026-10-16):

| Profile | Delay per request | Stands for |
|---|---|---|
| L0 | none | pure harness overhead |
| L1 | prompt tokens / 2,299.5 + completion tokens / 110.4 seconds | the model on the A10 |
| L2 | prompt tokens / 109.8 + completion tokens / 13.3 seconds | the model on an E5 node at 8 vCPU |

Single-request rates ignore batching and contention; that is deliberate,
because the stub stands in for an endpoint sized not to be the bottleneck.

**Inputs.** Live data sources (yfinance, NewsAPI, EDGAR, Pinecone), so data
I/O is part of the harness's wait, as in production. The research path
checks the brief cache first, so the driver deletes the `research:*` keys
before every submission. The 40 extended tickers are cycled.

**Load.** Closed loop: the driver keeps the queue at 3× the in-flight
capacity and records each brief's submit, start and finish time.

**Sweep.**

| Variable | Levels |
|---|---|
| Worker replicas R (KEDA off, fixed) | 1, 2, 4 |
| Per-pod concurrency c (`--concurrency`) | 1, 2, 4 |
| Latency profile | L0 and L1 on every (R, c); L2 on (4, 4) only, because at CPU speed one cell takes hours |
| Repeats | 2 per cell, 40 briefs each, after a 5-brief warm-up |

Plus one run with KEDA on (1 to 4 replicas, c = 1) at L1, to check the
autoscaler under real brief load, which has not been measured.

## Measurements

| Metric | How |
|---|---|
| Briefs per hour; brief latency p50 and p95 | driver timestamps |
| CPU-seconds per brief, per pod | `usage_usec` from the pod's cgroup `cpu.stat`, read before and after each cell (exact, not sampled) |
| CPU and memory over time | the existing `kubectl top` loop every 15 s (runbook, "OKE (provided cluster)" step 8) |
| Peak memory per pod | cgroup `memory.peak` where the node kernel provides it, else the `kubectl top` maximum |
| Requests in flight at the stub | stub log |
| Queue depth | Redis `LLEN celery` every 15 s |
| Errors | Celery task states; the stub's error log |

## Validity checks (a cell that fails one is reported, not used)

- **No hosted traffic.** Stub requests equal the harness's own LLM call
  count, and the hosted call count is zero: the same one-for-one rule as
  the traffic proof.
- **Data present.** `stock block empty` is 0 for the cell. Yahoo has
  returned 429 from the cluster's egress IP before.
- **Errors under 1%** of briefs.
- **Node headroom.** No node memory pressure or eviction during the cell.

## Reading rules, fixed before any run

- **Overhead** (Q1) is the L0 median wall time and CPU-seconds per brief at
  (R, c) = (1, 1).
- **Wait vs work** (Q2): at L1, if the worker's CPU-seconds per brief are
  under 25% of its wall time per brief, the harness is waiting, which
  supports the post. Above 75% it is CPU-bound. Between, it is mixed, and
  stated as such.
- **Saturation** (Q3): the smallest (R, c) after which doubling capacity
  raises throughput by less than 10%. Little's law (briefs in flight =
  throughput × latency) is checked on every cell. A gap of more than 10%
  means queueing inside the harness and is reported.
- **Sizing rule** (Q4): vCPU = CPU-seconds per brief × briefs per hour /
  3,600, stated with the memory per in-flight brief, from the L1 cells.
- Results are dated measurements on one shape and one image, entered in
  numbers-of-record by the same rules as every other run. Nothing here
  supports a claim about another shape.

## Cost and risk

- **Anthropic: $0.** Every LLM call goes to the stub; the judge does not
  run. The no-hosted-traffic check enforces this.
- **OCI: none new.** The provided cluster and its four E5 nodes.
- **Risk:** the sweep changes live configuration (worker command,
  replicas, `SLM_FULL`). Every change goes through the repository's
  overlays and scripts, and is reverted by one target at the end. Not run
  during the demo freeze.

## Implementation

1. `scripts/model_stub.py` and `k8s/model-stub/`: the stub server and its
   Deployment and Service (ClusterIP), mounted from a ConfigMap on a public
   Python base image, so the app image does not change.
2. `make bench-stub-on` and `make bench-stub-off`: point the self-served
   route at the stub and back, and fix replicas and concurrency per cell.
3. `scripts/harness_bench.py`: the closed-loop driver, run as a Job in the
   cluster; writes one JSON line per brief and a cgroup snapshot per pod per
   cell.
4. `scripts/harness_bench_report.py`: the tables, Little's-law check and
   reading rules above, from the committed run files.
5. Run, capture to `eval/runs/harness-bench-<date>/`, then record the
   results in numbers-of-record and replace this page's status line.

Before step 1, confirm in the code: which call sites use structured output
(the stub must return valid JSON there), and that the numeric check and
retrieval need no hosted model under `SLM_FULL`.

## Beyond this plan

The same plan, unchanged, run on E6, A2 (which needs multi-arch images) and
X12 would answer, for this harness, the shape comparison the post declines
to make without a benchmark. That needs node pools this project does not
have.
