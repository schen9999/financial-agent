# Harness benchmark: pre-registered plan and results

Status: **designed and implemented 2026-10-19; RUN 2026-10-20, 02:49 to
06:55 UTC: all 40 cell repeats valid.** Results below, from the committed
captures in `eval/runs/harness-bench-2026-10-20/` (`report.md` there is the
report script's output on them). The plan text above "Results" is
unchanged from before the run.

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
   Deployment and Service (ClusterIP), mounted from a ConfigMap on the
   pinned app image, so no image changes or is pulled.
2. `make bench-stub-on` and `make bench-stub-off`: point the self-served
   route at the stub and back, and fix replicas and concurrency per cell.
3. `scripts/harness_bench.py`: the closed-loop driver, run as a Job in the
   cluster, one JSON line per brief; `scripts/harness_bench_cell.sh` sets
   each cell and takes the cgroup snapshots, `scripts/harness_bench_sweep.sh`
   runs the sweep.
4. `scripts/harness_bench_report.py`: the tables, Little's-law check and
   reading rules above, from the committed run files.
5. Run, capture to `eval/runs/harness-bench-<date>/`, then record the
   results in numbers-of-record and replace this page's status line.

Before step 1, confirm in the code: which call sites use structured output
(the stub must return valid JSON there), and that the numeric check and
retrieval need no hosted model under `SLM_FULL`.

Confirmed 2026-10-19: the brief path makes no structured-output call (the
only `structured()` caller is the multi-agent planner, off by default); its
calls are two RAG answers (llama_index, through `llama_index_llm`), four
sections and one synthesis, all through `chat_completion`. Retrieval embeds
locally (HuggingFace) and queries Pinecone; the numeric check is
deterministic. Foreign filers (BABA, NVO, SAP, TM, TSM) make no RAG call, so
a brief costs 7 calls, or 5 for those five.

## Implementation decisions (fixed 2026-10-19, before any run)

Where the code had to choose, the choice and its reason, recorded before
any cell runs so none can be fitted to results:

- **Stub image and corpus.** The stub (`scripts/model_stub.py`, stdlib only)
  runs on the pinned app image, which is already on the nodes, instead of a
  public Python image: no new pull. Its corpus (`k8s/model-stub/corpus.json`,
  built by `scripts/build_stub_corpus.py`) is GPU run `nstp9` on image
  f3043751: the 270 recorded harness answers with their recorded token
  counts, matching nstp9's traffic proof call for call. The synthesis answer
  is the recorded Executive Summary and Outlook around the pre-written
  sections copied from the live prompt, as the real model is told to write
  it, so the synthesis format guard sees a well-formed brief.
- **Delay from recorded counts.** Each request waits the profile's delay for
  the recorded prompt and completion tokens of that ticker and site, not the
  live prompt's: the stub has no tokenizer, and the same brief then costs the
  same model time in every cell.
- **Cache.** `BYPASS_CACHE=true` on the worker (the eval harness's own flag)
  instead of deleting `research:*` keys: the cache is neither read nor
  written, so concurrent briefs for one ticker cannot hit each other.
- **No hosted traffic, enforced.** The worker's `ANTHROPIC_API_KEY` is
  overridden with a non-key for the whole benchmark, so a hosted call cannot
  succeed. The check: stub requests equal the calls the completed briefs
  should make (7 or 5 each), and the stub logged no errors.
- **Load and windows.** The driver keeps R × c × 4 briefs outstanding (3 ×
  capacity waiting in the queue). Warm-up is the first max(5, R × c)
  completions, so every Celery process has paid its first-task import; the
  next 40 completions are measured while the loop is still full; briefs
  still outstanding after that are drained and not measured. Task state is
  read from the Celery result backend in Redis, not polled through the API
  under test.
- **Per-process budget.** Changing c changes the pod's process count, so the
  pod's limits scale with it: 1.5 CPU and 2 GiB per process, the deployed
  per-pod values. Without this, c = 2 and 4 would measure the memory limit
  (each process loads the embedding model), not the harness. Requests are
  unchanged.
- **CPU-seconds per brief** = the worker pods' cgroup CPU usage from just
  before the driver starts to just after it ends, divided by every brief
  completed in that time (warm-up and tail included), so every CPU-second is
  attributed. Pods are restarted at the start of each cell, so a counter
  reset means a container restart and the repeat is invalid.
- **Wait vs work (Q2)** compares that figure with the median brief latency
  (start to finish, excluding queue time).
- **Little's law** compares throughput × mean latency with R × c.
- **Saturation (Q3)** lists every saturated cell at the smallest saturated
  capacity when replicas and concurrency tie.

How to run it: [deploy-runbook.md](deploy-runbook.md), "Harness benchmark".

## Results (2026-10-20)

A dated measurement on one cluster (the provided OKE cluster, four
VM.Standard.E5.Flex nodes at 16 vCPU), one image (f3043751), with the model
replaced by the stub. It supports no claim about another shape, and none
about a real model endpoint's capacity: the stub never saturates, a real
endpoint does.

**Validity.** All 40 repeats (20 cells, two each) passed every check: stub
requests equal the calls their briefs should make (326 to 805 per repeat),
stock block empty 0, errors 0, no container restart and no eviction or
memory-pressure event. Anthropic spend $0.

**Q1, overhead (L0 at (1,1)).** Median brief 1.0 s, 0.65 worker CPU-seconds
per brief. The time is the live data path: stock data 0.2 to 0.4 s, news
and SEC 0.5 to 0.7 s, retrieval 0.4 to 1.4 s per brief (worker timing
lines).

**Q2, wait vs work (L1, A10-speed model).** Worker CPU is 5% to 16% of
brief wall time in all nine cells, under the 25% line: the harness is
waiting, which supports the post. Median brief latency stays at 18.6 to
19.1 s in every cell.

**Q3, throughput and saturation.**

| Capacity R × c | L1 briefs/h (cells) | L0 briefs/h (cells) |
|---|---|---|
| 1 | 199 (1,1) | 3,693 (1,1) |
| 2 | 401 (1,2), 407 (2,1) | 7,614 (1,2), 7,308 (2,1) |
| 4 | 798 (1,4), 810 (2,2), 817 (4,1) | 6,255 (1,4), 16,961 (2,2), 16,067 (4,1) |
| 8 | 1,621 (2,4), 1,604 (4,2) | 14,072 (2,4), 16,124 (4,2) |
| 16 | 3,063 (4,4) | 25,415 (4,4) |

- At L1, throughput rises with capacity at 89% to 104% per doubling, so it
  does not saturate within the sweep: (4,4) runs 15.4 times (1,1). The
  two repeats of each L1 cell agree within 9%, and in every fixed L1 cell
  the time-averaged number of briefs running equals R × c (Little's law
  holds within 5%).
- At L0, by the pre-registered rule, it saturates at (2,2) and (4,1),
  about 16,000 to 17,000 briefs an hour. L0 throughput at high capacity
  is imprecise: 40 briefs finish in seconds, and the two repeats of (4,4)
  differ by 66%. The report flags these short windows.
- **Four processes per pod cost CPU.** At c = 4, worker CPU-seconds per
  brief rise to 1.64 to 3.06 at L1 and 3.2 to 9.0 at L0, with throttling
  at 47% to 54% of periods at L0, and L0 (1,4) is slower than (1,2). The
  likely cause, not yet tested: each Celery process starts 8 PyTorch
  threads (`torch.get_num_threads()` on a 16-vCPU node), so four
  processes run 32 threads in a 6-CPU pod.

**Q4, sizing (L1).** vCPU = CPU-seconds per brief × briefs per hour /
3,600:

| Cell | Briefs/h | Worker CPU-s per brief | Worker vCPU | Memory per process (MiB, sampled) |
|---|---|---|---|---|
| (1,1) | 199 | 0.97 | 0.05 | 826 |
| (2,2) | 810 | 1.11 | 0.25 | 648 |
| (4,1) | 817 | 1.30 | 0.29 | 724 |
| (4,2) | 1,604 | 2.26 | 1.01 | 639 |
| (4,4) | 3,063 | 3.06 | 2.60 | 602 |

At one or two processes per pod the harness needs about 0.25 to 0.36 vCPU
per 1,000 briefs an hour; at four, 0.46 to 0.85, rising with the
replica count. Memory is 586 to 826 MiB per
process across all cells: the nodes' kernel has no cgroup `memory.peak`, so
this is the larger of the `kubectl top` maximum (sampled every 15 s) and
the end-of-cell `memory.current`, a lower bound. The API pod uses 0.02
CPU-seconds per brief or less.

**L2 (CPU-speed model) at (4,4).** 286 briefs an hour, median brief 178 s,
worker CPU 2% of wall time: at CPU inference speed the model is the whole
story. This is an upper bound on the harness side only; the stub has no
capacity limit and one 8-vCPU llama.cpp endpoint does.

**KEDA (1 to 4 replicas, c = 1, L1).** 704 briefs an hour, 86% of a fixed
four replicas (817), with 3.0 to 4.0 briefs running on average while it
scales up; the two repeats differ by 27%. The first measurement of the
autoscaler under brief load.

**Not measured.** The `/ask` ReAct path and the Argo eval harness (out of
scope); a real endpoint under this load; any other shape. During the run the
idle CPU llama.cpp pod stayed deployed on the cluster.

**Follow-up, not pre-registered.** One (4,4) run with `OMP_NUM_THREADS=1`
would test the PyTorch-thread explanation. If run, it is reported as
exploratory, beside these results, never in place of them.

Declared 2026-10-20, before it runs (`scripts/harness_bench_sweep.sh
omp1`): L0 and L1 at (4,4), two repeats each, same stub, image and limits,
with `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` on the worker; the cell
log records `torch.get_num_threads()` from a worker. Same validity checks.
Reading: the explanation is supported if worker CPU-seconds per brief at
L1 (4,4) fall to 1.3 or less (the c = 1 level, (4,1)) and throttling
falls; partly supported if they fall but stay above 1.3; not supported if
they do not fall. L0 is reported beside it, with its short-window caveat.
Throughput is reported but is not the test: at L1 it is set by the model
delay. One thread per process may slow the embedding step at c = 1, which
this run does not measure.

## Beyond this plan

The same plan, unchanged, run on E6, A2 (which needs multi-arch images) and
X12 would answer, for this harness, the shape comparison the post declines
to make without a benchmark. That needs node pools this project does not
have.
