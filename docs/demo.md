# Demo: self-served model vs hosted, on OCI (November 2026)

For a technical review of the methodology and a plain-terms read of cost
and capacity. Follow-up to the first demo, which showed the fine-tuned
model on vLLM on an A10. Every number here is from a committed run; the
run IDs and links lead to the full record.

## Conclusions

- **The eval harness runs on OKE as a gated Argo workflow.** One command
  runs a model across 40 tickers, has a Claude judge check every brief
  against its sources, fails the run above 5% unsupported, and proves
  from the model server's own counters that the self-served model, and
  nothing else, produced the run.
- **A self-served open-weight model writes the whole brief without a
  detected loss in grounding.** Qwen3.6-35B-A3B on llama.cpp, against
  hosted Claude, on the same image and tickers. Unsupported claims as
  flagged by the judge: hosted 1.70%, the same model on CPU 3.63%, on an
  A10 2.45%. No pair is statistically different at this sample size, which
  is not the same as equivalent. It does state fewer figures: about 4 per
  brief against 7.
- **Cost per brief, model only:** CPU $0.0107, A10 at most $0.0293, hosted
  $0.0370. The CPU is cheapest but takes about 6 minutes a brief, so it
  suits batch work. The A10 takes 31 s against hosted's 26 s and ran at
  38% utilization, so $0.029 is a ceiling.
- **Two eval layers, because each misses what the other catches.** The
  judge accepted Toyota's revenue as "$52.0 billion" from a source value
  of ¥51.96 trillion labelled as dollars. The deterministic numeric check
  flagged it. The check, in turn, cannot see a correct figure under the
  wrong label; the judge flagged both such cases in the A10 run.
- **Hosted stays the production path.** The self-served model is a
  measured alternative, not an adopted one. The fine-tuned 1.5B model from
  the first demo still ships disabled: it failed the grounding gate.
- **Not done:** the Terraform-created OKE cluster (written, never applied:
  no compartment yet), vLLM serving on OKE, and the data and pipeline
  fixes recorded as known limitations, which wait until after the demo.

## The numbers

Same image (`1f51dad`), same 40 tickers, same judge (v2), October 2026.

| | Hosted Claude | Qwen3.6-35B-A3B, CPU | Qwen3.6-35B-A3B, A10 |
|---|---|---|---|
| Run | `9jzmj` | `8vpq6` | `p9jr2` |
| Unsupported, all judged claims | 7/411 = 1.70% (CI 0.8–3.5%) | 9/248 = 3.63% (CI 1.9–6.8%) | 6/245 = 2.45% (CI 1.1–5.2%) |
| Unsupported, claims with a figure | 2/277 | 3/161 | 3/155 |
| Figures stated per brief | 6.9 | 4.0 | 3.9 |
| Model errors among figures (adjudicated) | 2 (claims not in the sources) | 1 (a truncated value) | 2 (right figure, wrong label) |
| Time per brief (pipeline) | 25.9 s | 355.1 s | 31.1 s |
| Model cost per brief | $0.0370 (n = 3) | $0.0107 | $0.0293, a ceiling |
| Traffic proof | n/a | EXACT | EXACT |

Fisher tests on every pair: p ≥ 0.126 (all claims), p ≥ 0.35 (claims
with a figure), not adjusted for the three comparisons. The CPU and A10
runs of the same model do not differ in how many figures they state
(+0.15 per brief, CI −0.35 to +0.68): the consistency check — moving
the model from CPU to GPU changed its speed, not detectably what it
writes. Source:
[eval-methodology.md, the three-way comparison](eval-methodology.md#gpu-slm-extended-run-p9jr2-2026-10-05-the-three-way-comparison-with-hosted-9jzmj-and-cpu-8vpq6).

**In plain terms, for cost and capacity**

- **Cost to produce one brief** (model only; the harness, storage and the
  judge are excluded): about 1.1 cents on CPU, at most 2.9 cents on an
  A10, 3.7 cents through the hosted API.
- **Throughput measured on one machine** (two briefs at a time, the run's
  setting): one A10 produced 68 briefs an hour while busy only 38% of the
  time; one 4-OCPU slice of an E5 node produced 17 an hour at full load.
  Higher A10 throughput has not been measured and is not projected.
- **Prices:** OCI list prices read from Oracle's price API on 2026-10-05:
  A10 $2.00 per hour for the whole VM, E5 $0.03 per OCPU-hour and $0.002
  per GB-hour ([cost.md](cost.md)).

## Running order

About 20 minutes plus questions. The GPU smoke takes about 10 minutes (the
last one, `k6zxd`, took 9 min 40 s), so it starts first and the middle of
the demo fills the wait. If time is short, cut step 5 and shorten step 3.

| Step | Minutes | What | Shows |
|---|---|---|---|
| 1 | 3 | Conclusions (above) | the answer first |
| 2 | 1 | Launch the GPU smoke live | the one command; the traffic-proof snapshot taken before it |
| 3 | 3 | The topology and the Argo workflow while it runs | [architecture.md, "Deployed topology"](architecture.md#deployed-topology-october-2026); the Argo UI over a port-forward: fan-out per ticker, aggregate, gate |
| 4 | 4 | The three-way | the table above; why "not detected" is not "equivalent"; figures per brief |
| 5 | 2 | The Toyota case | the judge's reasoning, then the numeric-check flag |
| 6 | 2 | Cost and capacity | the plain-terms block above |
| 7 | 3 | Back to the live run | the aggregate table, the gate line, TRAFFIC PROOF, the attempts block |
| 8 | 2 | Limitations and next steps | the README's "Next steps"; the known limitations |

## The live run

One GPU smoke: ten tickers, the self-served model on node 2's A10, judged
by Claude, gated, with the traffic proof. Every command is in
[deploy-runbook.md, "Demo live run"](deploy-runbook.md#demo-live-run-november-2026-gpu-smoke-from-the-oke-harness).

**Preflight, the day before and 30 minutes before** (stop at the first
failure and take its branch):

1. Anthropic balance covers the run (the smoke's estimate: about $0.95).
2. OKE: four nodes Ready; the app, database, cache and CPU-endpoint pods
   Running; Argo's controller and server Running.
3. The nightly CronWorkflow is still suspended.
4. The deployed image is the pinned `1f51dad`.
5. Node 2: the endpoint's `/health` is ok, it answers 401 without the key,
   and llama-server holds about 20.5 GB of the A10.
6. From OKE: 401 without the key, 200 with it and the plain model alias;
   the harness reads the endpoint's facts.
7. One Yahoo price request from the cluster succeeds.
8. Screen sharing: no command to be shown prints a key (the exposure
   script, `server_facts` and the run's output do not; secret dumps,
   `env` in a pod, `.env` are never run on the shared screen); the
   terminals to be shared are pre-opened with their scrollback cleared.
9. Port-forwards and tunnels up: the Argo UI and Streamlit open on the
   laptop.

The day before, the preflight ends with a full rehearsal run, which also
measures the day's timings.

**Launch** (operator), at step 2 of the running order:

```bash
make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml
```

About 10 minutes. Nothing else may call the GPU endpoint until it
finishes: other traffic fails the proof, by design.

**On screen while it runs:** the operator pane with the run's progress;
the Argo UI graph (ten eval pods, two at a time, then the aggregate); a
node 2 pane with `watch -n 2 nvidia-smi`, the A10 moving with the calls.
At step 7: the aggregate table, the gate line, `stock block empty: 0/10`,
the call table with no truncation, loop, parse, format or error flags,
the attempts block (0 retries) and `TRAFFIC PROOF: EXACT`.

**If something fails** — each case ends at the fallback below; say what
failed, and debug no further than the first check:

| What happens | First check | Then |
|---|---|---|
| Node 2 is down | `ssh` to node 2; `/health` on the node | fallback (a VM restart is a console job, and the model load is too long to wait out) |
| The endpoint answers 401 to the harness | the key in OKE's Secret vs node 2's | fallback (re-keying is not a live step) |
| No HTTP answer (000) from OKE | `/health` on node 2 itself | answers there: the network rule — fallback; does not: pod restarting — wait a minute or two, else fallback |
| Yahoo 429 (`stock block empty` above 0) | the preflight's price request | show the count, quote nothing from the run, no retry — fallback for the numbers |
| The smoke fails its gate | which ticker holds the unsupported claims | smoke variance from judge listing (`7c66k` failed on MSFT alone); arms are compared on 40-ticker runs — go to `p9jr2`; no re-run for a pass |
| The Anthropic balance runs out | the attempts block | fallback |
| TRAFFIC PROOF: FAIL or LOWER-BOUND | what the proof reports | the proof doing its job; the run is not citable — fallback |

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

- `eval/runs/gpu-smoke.log`: the `k6zxd` aggregate, gate and traffic proof
  (10 tickers, 3/63 unsupported, TRAFFIC PROOF: EXACT).
- `eval/runs/gpu-extended.log`: the `p9jr2` run of record for the A10 arm
  (40 tickers, 6/245, TRAFFIC PROOF: EXACT).
- A smoke is a platform check, not a comparison: its rate varies run to
  run with how many qualitative claims the judge lists (`k6zxd`'s three
  unsupported claims were all AAPL watch-items). Compare arms only on the
  40-ticker runs.

## Prepared answers

**Does the self-served model ground as well as hosted?** No difference was
detected: 1.70% hosted, 3.63% CPU, 2.45% A10, every pair p ≥ 0.126. With
about 250–400 judged claims per run the intervals are wide (the A10 arm's
upper bound is 5.2%), so this does not show equivalence. The model also
states fewer figures, about 4 per brief against 7, so its rate is over
fewer checkable claims. The judge-flagged rates undercount: on September
claims the judge's precision was 60% and its population-weighted recall
32.5%, and no true-rate estimate is computed for these runs.

**How do you know the self-served model actually produced the run?** The
traffic proof. Before and after each run the harness reads the llama.cpp
server's own token counters; the tokens the harness logged must equal the
server's difference exactly, and any other traffic on the endpoint fails
the proof. Both SLM runs were EXACT: 270 calls, 350,290 prompt and 98,232
completion tokens on the A10 run, identical on both sides.

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
explanation. The stock data held Toyota's revenue in yen (¥51.96 trillion)
labelled as dollars; the hosted brief wrote "$52.0 billion"; the judge
marked it SUPPORTED, reasoning that the source value of
51,957,024,686,080 JPY, as the pre-written section had it, "rounds to
'$52.0 billion'".
The deterministic numeric check compared the figure with the stock field
and flagged it. That is why both layers exist: the check covers every
stock figure in every section, with no judgement; the judge covers what
the check cannot see, such as a correct figure attached to the wrong
quantity (two in the A10 run) or a claim the sources do not hold. The
root cause, the currency mislabel in the upstream data, is a known
limitation, recorded and not yet fixed.

**What does a brief cost, and what is excluded?** Model cost only: $0.0107
on a 4-OCPU slice of an E5 node, at most $0.0293 on an A10 (the whole VM
at $2.00 an hour, divided over the briefs the run produced), $0.0370
through the hosted API (n = 3; the cost of record stays $0.0366 from
September). The harness pods, storage and the judge are excluded on every
arm.

**Why was the A10 only 38% busy, and how fast could it go?** The run kept
two briefs in flight at a time, and each eval pod also spends time outside
the model — fetching data, retrieving filings, waiting on the judge; that
is the likely reason, not a measured breakdown. At that setting
the A10 averaged 38% utilization and produced 68 briefs an hour. It was
not run at higher concurrency, so no faster figure is claimed; that is a
next step.

**Is this on OKE?** The harness, the app and the CPU model endpoint run on
a provided OKE cluster. The A10 endpoint runs on a GPU VM with single-node
k3s, called from the cluster over one port that admits only the cluster's
egress IP. The Terraform that creates a full OKE cluster with an A10 node
pool is written and validated but has never been applied: there is no
compartment for it yet.

**Why does the fine-tuned model from the first demo ship disabled?** In
the 40-ticker A/B it had 8.15% unsupported claims against hosted's 3.06%
(Fisher p = 0.0023, judge v2), failing the 5% gate, with the excess in the
two sections it writes. That result stands; the self-served model here is
a different, larger model writing the whole brief.

**Is n = 40 enough?** Enough to separate the fine-tune (p = 0.0023) and the
density gap (sign test p ≤ 1e-8); not enough to detect a difference of a
point or two in the unsupported rate. Say "not detected", never
"equivalent".

**What would you do next?** Fix the two upstream data defects (currency,
profit margin as a fraction) and rerun every arm; measure the A10 at
higher concurrency; apply the OKE Terraform when a compartment exists. The
full list is in the README's "Next steps".

## Where the evidence is

- Results and method: [eval-methodology.md](eval-methodology.md), the
  three-way section, with the cost section, the error types, the numeric
  check and every command.
- What may be quoted: [numbers-of-record.md](numbers-of-record.md).
- Topology: [architecture.md](architecture.md#deployed-topology-october-2026).
- Procedures: [deploy-runbook.md](deploy-runbook.md), "OKE (provided
  cluster)" and the self-served SLM steps.
