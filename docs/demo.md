# Demo: self-served model vs hosted, on OCI (November 2026)

For a technical review of the methodology and a plain-terms read of cost
and capacity. Follow-up to the first demo, which showed the fine-tuned
model on vLLM on an A10. Every number here is from a committed run; the
run IDs and links lead to the full record.

## Conclusions

- **The eval harness and a self-served model run on CPU on OKE.** The
  provided OKE cluster (four E5 CPU nodes, no GPUs) runs the app, the
  Argo eval harness and a llama.cpp endpoint serving Qwen3.6-35B-A3B
  (Q4_K_M) on 8 vCPU and 30 GiB, in-cluster only. One command runs a model
  across 40 tickers, has a Claude judge check every brief against its
  sources, fails the run above 5% unsupported, and proves from the model
  server's own per-request log that the self-served model, and nothing
  else, produced the run.
- **CPU serving is sized right at 8 vCPU.** On the OKE node, prompt
  processing speeds up 1.8× from 4 to 8 vCPU and then not at all;
  generation runs at about 13 tok/s at every level (llama-bench,
  2026-10-08). More throughput would come from more replicas on separate
  nodes — an inference, not measured.
- **On CPU a brief costs about 1.1 cents and takes about 6 minutes**
  (model cost only, run `8vpq6`, previous image `1f51dad`): $0.0107 a
  brief and 355 s, against hosted's $0.0370 and 26 s (13.7× faster than
  the CPU) and the A10's $0.0293 at most and 31 s, on the same image. Cheapest, and
  batch work, not interactive. Two CPU runs on the current image (`5bdz5`,
  `4kkgm`) are not citable: each failed the traffic proof in force when it
  ran and the 5% gate; a third run was declined under the no-third-attempt
  rule. The CPU's citable numbers are on `1f51dad`.
- **On CPU the model writes what it writes on the A10, and fewer figures
  than hosted** (`1f51dad`, judged three times): unsupported 2.89% CPU,
  2.25% A10, 2.16% hosted (means), no difference detected on either pair;
  figures bound to stock data 3.00 per brief on CPU against 4.62 hosted
  (hosted +1.62, CI +1.02 to +2.23) and 2.83 on the A10 (+0.17, CI −0.28 to
  +0.62). Moving the model from CPU to GPU changed its speed, not
  detectably what it writes.
- **The comparison on the current image (`f3043751`): A10 against hosted,
  measured without the judge first.** Wrong stock figures per checked
  number: 1/565 hosted, 1/432 on the A10, not separated. Currency-label
  errors: 22 and 11 before the stock-data fix, 0 and 0 after. Figures
  bound to stock data: 4.47 per brief hosted against 3.05, +1.43 (CI +0.93
  to +1.93).
- **Judge-flagged grounding, secondary: no difference detected.** Each
  run judged three times: hosted 2.55%, A10 3.57% unsupported (means; no
  difference detected, which is not the same as equivalent). Read it with
  the judge's limits: the same briefs re-judged moved by up to 2×, and on
  these runs the judge's precision is about 29% and its recall about 11%.
- **Two eval layers, because each misses what the other catches.** The
  judge accepted Toyota's revenue as "$52.0 billion" from a source value
  of 51.96 trillion in the filer's reporting currency (yen by its
  magnitude, inferred), labelled USD. The deterministic numeric check
  flagged it. The check, in turn, cannot see a correct figure under the
  wrong label in general; the judge flagged both such cases in the A10 run
  on the previous image.
- **Hosted stays the production path.** The self-served model is a
  measured alternative, not an adopted one. The fine-tuned 1.5B model from
  the first demo still ships disabled: it failed the grounding gate.
- **Not done:** a citable CPU run on the current image (both failed their
  traffic proofs under the counter method; a third run was declined under
  the rule recorded before the second: no third attempt), the Terraform-created OKE cluster (written, never
  applied: no compartment yet), vLLM serving on OKE, and the pipeline fixes
  recorded as known limitations, which wait until after the demo.

## How this maps to harness engineering on OCI CPU

Sanjay Basu's
[Harness Engineering using OCI CPU & OKE](https://blogs.oracle.com/cloud-infrastructure/harness-engineering-using-oci-cpu-oke)
(OCI blog, 2026-09-28) argues that an agent harness, meaning an agent loop
with tools composed into larger programs, spends its time waiting on
inference served somewhere else. Its limits are CPU, memory bandwidth and
latency, not accelerators. So the harness belongs on CPU nodes in OKE,
inference is sized separately, and GPUs should not sit idle behind the
harness. The post sketches a layout: an E6 control plane; reasoners fanned
out on A2 Arm and scaled by KEDA on queue depth; a "meter" that checks
finished traces as a separate batch job; OCI Queue or Streaming triggers
behind an approval gate; egress limited to model endpoints; and API keys
in OCI Vault. It reports no benchmark of a harness on any shape.

| His term | Ours | Where |
|---|---|---|
| Harness: an agent loop with tools | The ReAct `/ask` agent, a LangGraph loop over four tools (stock data, news, SEC filings, filing retrieval). The brief pipeline, which is what the eval measures, has no loop: it fetches the data, writes four sections in parallel, then the synthesis | [agent/react_agent.py](../agent/react_agent.py), `/ask` in [api.py](../api.py); [agent/core.py](../agent/core.py) `run_research_checked` |
| Hand-wired DAG: fixed and auditable | The Argo eval workflow: one pod per ticker, two at a time, then the aggregate and the gate. The brief pipeline is hand-wired in the same sense | [argo/base/eval-workflow.yaml](../argo/base/eval-workflow.yaml) |
| Goal-plus-judge loop | The multi-agent supervisor graph: draft, have the shared LLM judge check the Executive Summary and Outlook, revise while above 5% unsupported, at most two revisions. It shipped default-off because evals showed no grounding gain at higher cost and latency. The eval's 5% gate uses the same judge, but it scores a finished run and does not loop | [agent/graph.py](../agent/graph.py), [agent/grounding.py](../agent/grounding.py); `MULTI_AGENT_ENABLED`, `CRITIC_MAX_UNSUPPORTED_PCT`, `MAX_REVISIONS` in [k8s/base/10-configmap.yaml](../k8s/base/10-configmap.yaml); `max-unsupported-pct` in the eval workflow |
| Meter: self-checks on finished traces, as a separate batch job | The Argo eval harness, a batch run apart from the app that judges finished briefs against their sources and gates the run. The traffic proof, which after the run matches every request in the model server's log to a harness call. The numeric check rerun over a finished run's briefs. The numeric check also runs inline on every brief, in warn mode | the eval workflow; [scripts/traffic_proof_tasks.py](../scripts/traffic_proof_tasks.py); [agent/numeric_check.py](../agent/numeric_check.py), [scripts/numeric_backtest.py](../scripts/numeric_backtest.py) |
| Restricted egress | Only the other direction, inbound to the model: the A10 endpoint requires a key, and its port admits only the OKE cluster's egress IP. The harness's own egress is not restricted (next steps, below) | [k8s/llamacpp/overlays/k3s-gpu](../k8s/llamacpp/overlays/k3s-gpu/kustomization.yaml); [deploy-runbook.md, "Demo live run"](deploy-runbook.md#demo-live-run-november-2026-gpu-smoke-from-the-oke-harness) |

**What our measurements add.** The post reports no benchmark, so these
are ours. All are model-side measurements of one system, and each has its
own caveats:

- **A GPU behind this harness sits partly idle.** On the A10 run of record
  `nstp9` (image `f3043751`, two briefs in flight, the run's setting) the
  A10 averaged about 36% utilization (35.7%; median sample 0%). Each eval
  pod also spends time outside the model: fetching data, retrieving
  filings, waiting on the judge. That is the likely reason, not a measured
  breakdown. At four briefs in flight (`xgtxx`) it averaged 45%. Nothing
  faster has been run.
- **In-cluster CPU inference is cheapest per brief, and slow.** On the
  previous image `1f51dad` (`8vpq6`, traffic proof EXACT): $0.0107 a brief,
  model cost only, at 355 s per ticker against hosted's 26 s (13.7×). The
  endpoint was saturating its 8 vCPU. It suits batch work, not
  interactive work. The CPU's citable numbers are on that image only.
- **More cores on one node stop helping at 8 vCPU** (llama-bench on the
  OKE E5 node, 2026-10-08, a dated measurement with no judge). Prompt
  processing speeds up 1.8× from 4 to 8 vCPU, then not at all. Generation
  stays at about 13 tok/s at every level. Memory bandwidth is the usual
  limit on generation, but that is an inference: this run does not
  measure it. More replicas on separate nodes might add throughput, which
  is also an inference and not measured.
- **The instruction set decides whether an engine runs at all.** vLLM's
  prebuilt CPU image needs AVX-512. It crashed with SIGILL on the AVX2-only
  dev laptop ([benchmarks.md](../benchmarks.md)), and its CPU backend ran on
  node 2's AVX-512 Xeon (2026-09-28, dated). This bears on the post's note
  about X12 and AVX-512. llama.cpp is the engine that ran on the OKE E5
  nodes.

One difference: in the post the harness calls inference off-box, but ours
also serves a model in-cluster on CPU. Our measurements say in-cluster CPU
inference suits batch work. That is consistent with sizing inference
separately from the harness, but it does not prove it.

**Not built, as next steps:**

- **KEDA scaling of the Celery worker on Redis queue depth.** The worker
  runs one replica, and request-time load has not been measured.
- **API keys from OCI Vault instead of Kubernetes Secrets.** Today the
  operator creates the Secrets by hand from a temp file that is shredded
  afterwards. Vault would remove that step and add rotation and audit.
- **Separate node pools: E6 for the control plane, A2 for the reasoners.**
  We used the four E5 nodes provided with the cluster, which is not ours
  to reshape. Arm nodes would also need multi-arch images, and the app
  image is built for `linux/amd64` only.
- **Pod egress restricted to model endpoints.** Today no overlay defines a
  NetworkPolicy, so app and eval pods can reach anything. The Terraform
  path's worker security list allows all egress, for image pulls and OCI
  services. The provided cluster's VCN rules belong to the tenancy and are
  not in the repo. The allowlist would also have to admit the data
  sources (Yahoo, SEC, news), and the cluster's CNI would have to enforce
  NetworkPolicy, which has not been checked.
- **Blast-radius metering, an approval gate, Queue or Streaming
  triggers.** These suit harnesses that generate their graphs just in time.
  Ours deliberately stays at the hand-wired, auditable end, where the graph
  is fixed in reviewed code.

## The numbers

**The CPU arm, previous image `1f51dad`** (40 tickers, judge v2 judged
three times; both CPU runs on `f3043751` failed their traffic proofs, so
the CPU is compared only within this image):

| | CPU `8vpq6` | A10 `p9jr2` | Hosted `9jzmj` |
|---|---|---|---|
| Where | OKE, 8 vCPU E5 | VM.GPU.A10.1, k3s | Anthropic API |
| Time per brief (pipeline) | 355.1 s | 31.1 s | 25.9 s |
| Model cost per brief | $0.0107 | $0.0293, a ceiling | $0.0370 (n = 3) |
| Figures bound to stock data per brief | 3.00 | 2.83 | 4.62 |
| Unsupported, three judgings: mean | 2.89% (2.13–3.63%) | 2.25% | 2.16% |
| Traffic proof | EXACT | EXACT | n/a |

Against hosted, the CPU's judge-flagged rate shows no difference detected
(hosted − CPU −0.74 points, CI −2.67 to +1.03); against the A10, +0.16
points (CI −1.96 to +2.26). Hosted states more figures (+1.62 bound per
brief, CI +1.02 to +2.23); the CPU and the A10 do not differ (+0.17, CI
−0.28 to +0.62). Source:
[eval-methodology.md, the three-way comparison](eval-methodology.md#gpu-slm-extended-run-p9jr2-2026-10-05-the-three-way-comparison-with-hosted-9jzmj-and-cpu-8vpq6).

**The comparison on the current image `f3043751`** (stock-data fix plus
currency-labelling prompt rule), same 40 tickers, judge v2 judged three
times, October 2026. Deterministic measures first.

| | Hosted Claude | Qwen3.6-35B-A3B, A10 |
|---|---|---|
| Run | `4hsn2` | `nstp9` |
| Wrong stock figures per checked number (numeric check, adjudicated) | 1/565 | 1/432 |
| Currency-label errors (before the fix: 22 and 11) | 0 | 0 |
| Figures bound to stock data per brief (no judge) | 4.47 | 3.05 |
| Unsupported, all judged claims: mean (range) of three judgings | 2.55% (1.47–3.76%) | 3.57% (3.27–3.75%) |
| Unsupported, claims with a figure: mean (range) | 0.86% (0.73–1.11%) | 2.42% (2.38–2.47%) |
| Time per brief (pipeline) | 26.7 s | 34.6 s |
| Model cost per brief | $0.0357 (n = 3) | $0.0303, a ceiling |
| Traffic proof | n/a | EXACT |

Hosted states +1.43 more figures bound to stock data per brief (CI +0.93
to +1.93); the one wrong figure on each side is the current price given as
the 52-week low. Judge-flagged grounding: paired ticker-level bootstrap on
rates averaged over the three judgings, −1.22 points (CI −4.39 to +1.78) —
no difference detected. The judge's calibration on these runs: precision
about 29% (CI 8.3–52.9%), recall about 11% (CI 3.1–27.9%), majority vote,
180 blind labels. Source:
[eval-methodology.md, the current runs](eval-methodology.md#numbers-of-record-on-the-stock-data-fix-image-three-judgings-per-run-and-the-judge-v2-calibration-on-those-runs-2026-10-0607).

**In plain terms, for cost and capacity**

- **Cost to produce one brief** (model only; the harness, storage and the
  judge are excluded): about 1.1 cents on CPU (previous image), at most 3.0
  cents on an A10, 3.6 cents through the hosted API.
- **Throughput measured on one machine** (two briefs at a time, the run's
  setting): one 4-OCPU slice of an E5 node produced 17 briefs an hour at
  full load (previous image); one A10 produced 66 an hour while busy only
  36% of the time. Higher A10 throughput has not been measured and is not
  projected.
- **Prices:** OCI list prices read from Oracle's price API on 2026-10-05:
  E5 $0.03 per OCPU-hour and $0.002 per GB-hour, A10 $2.00 per hour for
  the whole VM ([cost.md](cost.md)).

## Running order

About 20 minutes plus questions. The GPU smoke takes about 10 minutes
(`m7qvv` took 9 min 56 s), so it starts first and the middle of the demo
fills the wait. If time is short, cut step 6 and shorten step 5.

| Step | Minutes | What | Shows |
|---|---|---|---|
| 0 | 1 | His post, and what we measured against it | [the mapping above](#how-this-maps-to-harness-engineering-on-oci-cpu): his terms to ours, and the A10's idle share and the CPU's batch-only speed as our measurements |
| 1 | 2 | Conclusions (above) | the answer first: the harness and the model on CPU on OKE |
| 2 | 1 | Launch the GPU smoke live | the one command, and why the live run is the A10's (below) |
| 3 | 3 | The harness on OKE CPU while it runs | [architecture.md, "Deployed topology"](architecture.md#deployed-topology-october-2026): what runs where; the Argo UI over a port-forward (fan-out per ticker, aggregate, gate); the CPU endpoint and its 8 vCPU sizing |
| 4 | 3 | CPU cost and time, with the A10 and hosted beside it | the `1f51dad` table and the plain-terms block |
| 5 | 3 | The comparison on the current image | the deterministic measures first, then the judge with its noise and calibration; why "not detected" is not "equivalent" |
| 6 | 2 | The Toyota case | the judge's reasoning, then the numeric-check flag |
| 7 | 3 | Back to the live run | the aggregate table, the gate line, the attempts block, and the per-request traffic proof |
| 8 | 2 | Limitations and next steps | the README's "Next steps"; the known limitations |

## The live run

One GPU smoke: ten tickers, the self-served model on node 2's A10, judged
by Claude, gated, with the traffic proof. A CPU smoke takes about 6
minutes per brief, 38 minutes for the ten (`xnwjm`), and does not fit the
call; the A10 runs the same model file and engine in about 10. Every
command is in
[deploy-runbook.md, "Demo live run"](deploy-runbook.md#demo-live-run-november-2026-gpu-smoke-from-the-oke-harness).

**Preflight, the day before and 30 minutes before:**
[demo-preflight.md](demo-preflight.md), each check's command and expected
output in order, stopping at the first failure. In short: the Anthropic
balance covers the runs (`make anthropic-estimate`: $0.90 a smoke on this
image; the day before, rehearsal + demo + one spare, $2.71, budget $4.06
with margin); OKE nodes and pods Ready; the nightly CronWorkflow
suspended and nothing running; the image is the pinned `f3043751`; the
app's `SLM_FULL` is off; node 2's endpoint healthy and keyed, holding
about 20.5 GB of the A10, vLLM at 0; 401 and 200 from OKE; one Yahoo
price from the cluster; no key on a shared screen; tunnels up. The day
before, the preflight ends with a full rehearsal run, its per-request
proof, and then the freeze tag.

**Launch** (operator), at step 2 of the running order:

```bash
make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml
```

About 10 minutes. Nothing else may call the GPU endpoint until the proof's
log is captured: other traffic fails the proof, by design.

**On screen while it runs:** the operator pane with the run's progress;
the Argo UI graph (ten eval pods, two at a time, then the aggregate); a
node 2 pane with `watch -n 2 nvidia-smi`, the A10 moving with the calls.
At step 7: the aggregate table, the gate line, `stock block empty: 0/10`,
the call table with no truncation, loop, parse, format or error flags,
the attempts block (0 retries), then the per-request proof
(`scripts/traffic_proof_tasks.py`, preflight check 13):
`TRAFFIC PROOF (per-request): TASK-EXACT`. The make target's last line is
the `/metrics` counter proof, which is reported and does not decide: the
counter has drifted by a few tokens on both endpoints with every request
matched, so it may print FAIL on a clean run.

**If something fails** — each case ends at the fallback below; say what
failed, and debug no further than the first check:

| What happens | First check | Then |
|---|---|---|
| Node 2 is down | `ssh` to node 2; `/health` on the node | fallback (a VM restart is a console job, and the model load is too long to wait out) |
| The endpoint answers 401 to the harness | the key in OKE's Secret vs node 2's | fallback (re-keying is not a live step) |
| No HTTP answer (000) from OKE | `/health` on node 2 itself | answers there: the network rule — fallback; does not: pod restarting — wait a minute or two, else fallback |
| Yahoo 429 (`stock block empty` above 0) | the preflight's price request | show the count, quote nothing from the run, no retry — fallback for the numbers |
| The smoke fails its gate | which ticker holds the unsupported claims | smoke variance from judge listing (`m7qvv` failed on NVDA and MSFT watch-items); arms are compared on 40-ticker runs — go to `nstp9`; no re-run for a pass |
| The Anthropic balance runs out | the attempts block | fallback |
| Per-request proof FAIL | the unmatched pairs it lists | the proof doing its job; the run is not citable — fallback |
| Counter proof FAIL, per-request TASK-EXACT | both lines | the counter's known drift; the per-request verdict decides — the run stands |

**vLLM stays at 0 on node 2 until after the demo**, with llama.cpp
running there: vLLM answers on the same port without a key, ufw does not
guard k3s NodePorts, and the network rule for that port stays open to
the cluster until the demo. If vLLM is ever needed before then, the
runbook's contingency closes the rule first and restores it before the
rehearsal.

**After the demo**, in this order, because vLLM answers on the same port
without a key and ufw does not guard k3s NodePorts: capture the live run;
close the port-forwards; close ufw 30880 on node 2; ask the tenancy owner
to remove the security-list rule for 30880 and confirm the port no longer
answers from OKE; only then restore vLLM if wanted.

## Fallback if the live run fails

Show the recorded GPU smoke and extended run instead, and say what failed.

- `eval/runs/gpu-smoke-f304375.log`: the current image's GPU smoke
  `m7qvv` (10 tickers, 4/60 unsupported, gate failed on qualitative
  watch-items, numeric 0/30, TRAFFIC PROOF: EXACT).
- `eval/runs/gpu-smoke.log`: the `k6zxd` aggregate, gate and traffic proof
  (previous image `1f51dad`, 10 tickers, 3/63 unsupported, TRAFFIC PROOF:
  EXACT).
- `eval/runs/gpu-extended-f304375.log`: the `nstp9` run of record for the
  A10 arm (40 tickers, image `f3043751`, 10/267 on its first judging,
  TRAFFIC PROOF: EXACT).
- A smoke is a platform check, not a comparison: its rate varies run to
  run with how many qualitative claims the judge lists (`k6zxd`'s three
  unsupported claims were all AAPL watch-items). Compare arms only on the
  40-ticker runs.

## Prepared answers

**Does the self-served model ground as well as hosted?** Start with what
needs no judge: wrong stock figures 1/565 hosted vs 1/432 on the A10, and
0 currency-label errors on both. It states fewer figures (3.05 vs 4.47
bound to stock data per brief), so it has fewer chances to be wrong. The
judge found no difference: 2.55% vs 3.57% unsupported, averaged over three
judgings. With about 250–400 judged claims per run that does not show
equivalence, and the judge itself is a weak instrument here (next answer).

**How much do you trust the judge?** As a coarse screen, not a measuring
instrument. Two measurements. First, noise: the same briefs, re-judged
with the same inputs, prompt and temperature 0, moved by up to 2× (hosted
15/399 one time, 6/408 the next), so every run is now judged three times
and reported as a mean with its range. Second, calibration: 180 claims
from these runs labelled blind by a human. When the judge flags a claim,
the human agrees it is unsupported about 29% of the time (CI 8–53%); of
the claims the human calls unsupported, the judge flags about 11% (CI
3–28%). Most of the disagreement is one pattern: the briefs' hedged "watch
X" lines, which the judge calls unsupported and a human calls inference.
The estimated true unsupported rate is 3.8% hosted (CI 1.9–9.7%) and 8.7%
on the A10 (CI 5.4–18.5%) — wide, and not tested against each other. That
is why the numbers lead with the deterministic check, which needs no
judgement, and why "no difference detected" is the strongest grounding
claim made.

**The true-rate estimate is 8.7% for the GPU arm vs 3.8% hosted. Is the
SLM worse?** Not shown. Those are point estimates from 180 blind labels by
a single labeller, split across the two runs (72 and 108 labels), and they
were not tested against each other. Their intervals are wide and overlap:
5.4–18.5% and 1.9–9.7%. The direction fits a recorded pattern: most of the
A10 arm's human-unsupported claims are hedged qualitative Outlook lines
(among them a "services margins" watch-item copied from the prompt's
example, limitation 8), the same kind of claim behind most of the
judge-human disagreement. On the measures
that need no judge, there is no difference in errors: wrong stock figures
1/432 on the A10 and 1/565 hosted, and no currency-label errors on either.
What does separate is how many figures each states (3.05 vs 4.47 per
brief). To answer the question properly would take a larger labelled
sample per arm and a pre-stated test.

**How do you know the self-served model actually produced the run?** The
traffic proof. Since 2026-10-07 it matches the llama.cpp server's own log,
request by request, against the calls the harness logged: every task the
server ran from the workflow's start to the capture after the run must
match a harness call on its prompt and completion tokens, and every call a
task, or the run is not citable. Any other traffic on the endpoint leaves
an unmatched task. Before that date the proof compared the harness's token
totals with the server's `/metrics` counters. That counter drifts by a few
tokens with nothing else on the endpoint (measured in a controlled replay:
1, 2 and 2 tokens short of exact per-request sums), and it failed both CPU
runs on the current image, by 1 and 4 tokens, although every one of their
270 requests matched the server's log. They were judged under the rule in
force when they ran, so they stay failed; they are not re-scored. The A10
run of record `nstp9` was EXACT under the counter (270 calls, 352,522
prompt and 98,665 completion tokens), and the A10 run at parallelism 4
(`xgtxx`) was the first judged by the per-request match: 270 of 270.

**Why aren't there CPU numbers on the current image?** Two CPU runs on
`f3043751` (`5bdz5`, `4kkgm`, 2026-10-06) are not citable: each failed the
traffic proof in force when it ran, the server's `/metrics` counter, by +1
and −4 prompt tokens, and each failed the 5% grounding gate. Checked
afterwards against the server's own log, all 270 requests of each matched
a harness call; that check became the rule on 2026-10-07, after both runs,
so their verdicts stand and no figure from them is quoted. A third run was
declined under the rule set before the second: no third attempt. The CPU's
citable numbers are on the previous image, `1f51dad` (`8vpq6`).

**Why llama.cpp and not vLLM for this model?** From the records, computed
and not booted ([dated finding](eval-methodology.md#dated-finding-computed-not-booted-no-4-bit-qwen36-35b-a3b-fits-one-a10-under-vllm-2026-10-02)):
Qwen publishes Qwen3.6-35B-A3B in BF16 and FP8 only, and FP8 has no
native support on the A10's Ampere generation and is over 24 GB anyway.
The community 4-bit builds take 20.3–21.9 GiB for the language model
alone; the best leaves about 1 GiB of the A10 at 95% utilization for the
CUDA context, activations and KV cache, against a harness that sends up
to about 8 concurrent requests of up to about 5k tokens. And node 2's
driver supports CUDA 12.8, and vLLM 0.19.0 — the first version with the
fix for this architecture's quantized layers — publishes no CUDA 12.8
image (0.19.x defaults to 12.9, 0.20 and later to 13.0). The
same Q4_K_M file runs entirely on the A10 under llama.cpp's CUDA 12.8
build, using 20,488 of 23,028 MiB.

**What does the Toyota case show about the judge?** That an LLM judge
reasons about plausibility and can accept a wrong figure with a confident
explanation. The stock data held Toyota's revenue as 51,957,024,686,080 —
51.96 trillion in the filer's reporting currency (yen by its magnitude,
inferred) — labelled USD. The hosted brief wrote "$52.0 billion", and the
judge marked it SUPPORTED with this reason: "Source data shows revenue of
51,957,024,686,080.0 JPY, which the Financial Health pre-written section
rounds to '$52.0 billion'". The judge read the figure as yen itself, and
still accepted a dollar figure 1,000 times smaller.
The deterministic numeric check compared the figure with the stock field
and flagged it. That is why both layers exist: the check covers every
stock figure in every section, with no judgement; the judge covers what
the check cannot see, such as a correct figure attached to the wrong
quantity (two in the A10 run on the previous image) or a claim the
sources do not hold. The root cause, the currency mislabel in the upstream
data, is fixed in image `f3043751`: currency-label findings went from 22
and 11 to 0 and 0. Before the fix, the check caught that defect
only when a brief's figure departs from the mislabelled field: the CPU
arm's faithful copy, "$51.96 trillion", passed both layers
([debugging story](debugging-story.md#the-limits-of-each-layer)).

**What does a brief cost, and what is excluded?** Model cost only: $0.0107
on a 4-OCPU slice of an E5 node (the CPU endpoint's request, on the
previous image `1f51dad`); at most $0.0303 on an A10 (the whole VM at
$2.00 an hour, divided over the briefs the run produced) and $0.0357
through the hosted API (n = 3), both on image `f3043751`. The cost of record stays $0.0366 from September. The harness pods, storage and the judge are excluded on every
arm.

**Why was the A10 only 36–38% busy, and how fast could it go?** The run kept
two briefs in flight at a time, and each eval pod also spends time outside
the model — fetching data, retrieving filings, waiting on the judge; that
is the likely reason, not a measured breakdown. At that setting
the A10 averaged 36% utilization and produced 66 briefs an hour (38% and
68 on the previous image). At four briefs in flight (`xgtxx`, 2026-10-08,
per-request proof TASK-EXACT) it produced 100.8 an hour at 45% mean
utilization, $0.0198 a brief, still a ceiling, and what it wrote did not
change measurably (figures bound to stock data 3.10 vs 3.05 per brief).
Nothing faster than that has been run, so nothing faster is claimed.

**Is this on OKE?** The harness, the app and the CPU model endpoint run on
a provided OKE cluster. The A10 endpoint runs on a GPU VM with single-node
k3s, called from the cluster over one port that admits only the cluster's
egress IP. The Terraform that creates a full OKE cluster with an A10 node
pool is written and validated but has never been applied: there is no
compartment for it yet.

**Why does the fine-tuned model from the first demo ship disabled?** In
the 40-ticker A/B it had 8.15% unsupported claims against hosted's 3.06%
(judge v2), failing the 5% gate, with the excess in the two sections it
writes. Claim-level Fisher gives p = 0.0023; at the ticker level the paired
interval on ticker-averaged rates (8.68% vs 2.32%) is +2.08 to +10.95
points, and the sign test gives p = 0.078. That result stands; the self-served model here is
a different, larger model writing the whole brief.

**Is n = 40 enough?** For the density gap, yes (figures bound to stock
data, sign test p = 0.0001). For the fine-tune, only partly: claim-level
Fisher gives p = 0.0023, but claims cluster within briefs. At the ticker
level the paired interval excludes zero (+2.08 to +10.95 points on
ticker-averaged rates) while the sign test does not reach 0.05 (p = 0.078).
The ship-off decision rests on the gate failure (8.15% against the 5% gate)
and the concentration in the sections the fine-tune writes, not on one
p-value. Not enough to detect a difference of a point or two in the
unsupported rate. Say "not detected", never "equivalent".

**What would you fix first in the app plane?** Four gaps, all found by
reading the code for [reliability.md](reliability.md), none yet hit in a
recorded run, and none changed before the demo (the image stays
`f3043751`). First, a worker crash loses the job in flight: Celery
acknowledges a task when the worker takes it, so I would acknowledge late
and make the task idempotent. Second, the async path never writes the
brief to Postgres, only the synchronous one does. Third, a job lost to a
crash or a Redis restart reports "processing" or "queued" forever; it needs
a deadline and an honest status. Fourth, the Anthropic client runs with no
request timeout. Each fix gets a test that reproduces the failure first.
Ranked by what a user would notice, the worker crash comes first.

**What would you do next?** Fix the recorded pipeline limitations, with
new baselines on every arm, the CPU arm among them under the per-request
proof; apply the OKE Terraform when a compartment exists. The
full list is in the README's "Next steps".

## Where the evidence is

- Results and method: [eval-methodology.md](eval-methodology.md), the
  three-way section, with the cost section, the error types, the numeric
  check and every command.
- What may be quoted: [numbers-of-record.md](numbers-of-record.md).
- Topology: [architecture.md](architecture.md#deployed-topology-october-2026).
- Procedures: [deploy-runbook.md](deploy-runbook.md), "OKE (provided
  cluster)" and the self-served SLM steps.
