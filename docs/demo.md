# Demo: self-served model vs hosted, on OCI (November 2026)

For a technical review of the methodology and a plain-terms read of cost
and capacity. Follow-up to the first demo, which showed the fine-tuned
model on vLLM on an A10. Every number here is from a committed run; the
run IDs and links lead to the full record.

## Conclusions

- **Measured without the judge, the self-served model gets stock figures
  wrong about as rarely as hosted, and states fewer of them.** Qwen3.6-35B-A3B
  on llama.cpp on an A10, against hosted Claude, same image (`f3043751`),
  40 tickers. Wrong stock figures per checked number: 1/565 hosted, 1/432
  on the A10, not separated. Currency-label errors: 22 and 11 before the
  stock-data fix, 0 and 0 after. Figures bound to stock data: 4.47 per
  brief hosted against 3.05, +1.43 (CI +0.93 to +1.93).
- **Judge-flagged grounding, secondary: no difference detected.** Each
  run judged three times: hosted 2.55%, A10 3.57% unsupported (means; no
  difference detected, which is not the same as equivalent). Read it with
  the judge's limits: the same briefs re-judged moved by up to 2×, and on
  these runs the judge's precision is about 29% and its recall about 11%.
  The same model on CPU (previous image) was indistinguishable from the A10
  there.
- **The eval harness runs on OKE as a gated Argo workflow.** One command
  runs a model across 40 tickers, has a Claude judge check every brief
  against its sources, fails the run above 5% unsupported, and proves
  from the model server's own counters that the self-served model, and
  nothing else, produced the run.
- **Cost per brief, model only:** hosted $0.0357, A10 at most $0.0303
  (image `f3043751`); CPU $0.0107 (previous image). The CPU is cheapest but
  takes about 6 minutes a brief, so it suits batch work. The A10 takes 35 s
  against hosted's 27 s and ran at 36% utilization, so $0.030 is a ceiling.
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
- **Not done:** the Terraform-created OKE cluster (written, never applied:
  no compartment yet), vLLM serving on OKE, a citable CPU run on the
  current image (both failed their traffic proofs), and the pipeline fixes
  recorded as known limitations, which wait until after the demo.

## The numbers

Image `f3043751` (stock-data fix plus currency-labelling prompt rule),
same 40 tickers, judge v2 judged three times, October 2026. Deterministic
measures first.

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

**The CPU arm, previous image `1f51dad`** (the former numbers of record,
one judging each; both CPU runs on `f3043751` failed their traffic proofs):

| | Hosted `9jzmj` | CPU `8vpq6` | A10 `p9jr2` |
|---|---|---|---|
| Unsupported, three judgings: mean | 2.16% | 2.89% | 2.25% |
| Figures bound to stock data per brief | 4.62 | 3.00 | 2.83 |
| Time per brief (pipeline) | 25.9 s | 355.1 s | 31.1 s |
| Model cost per brief | $0.0370 (n = 3) | $0.0107 | $0.0293, a ceiling |

On that image the CPU and A10 runs of the same model do not differ in what
they write (figures bound +0.17 per brief, CI −0.28 to +0.62; grounding
+0.16 points, CI −1.96 to +2.26): moving the model from CPU to GPU changed
its speed, not detectably what it writes. Source:
[eval-methodology.md, the three-way comparison](eval-methodology.md#gpu-slm-extended-run-p9jr2-2026-10-05-the-three-way-comparison-with-hosted-9jzmj-and-cpu-8vpq6).

**In plain terms, for cost and capacity**

- **Cost to produce one brief** (model only; the harness, storage and the
  judge are excluded): about 1.1 cents on CPU (previous image), at most 3.0
  cents on an A10, 3.6 cents through the hosted API.
- **Throughput measured on one machine** (two briefs at a time, the run's
  setting): one A10 produced 66 briefs an hour while busy only 36% of the
  time; one 4-OCPU slice of an E5 node produced 17 an hour at full load
  (previous image).
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
| 4 | 4 | The numbers | the deterministic measures first, then the judge with its noise and calibration; why "not detected" is not "equivalent" |
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
4. The deployed image is the pinned `f3043751`.
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
| The smoke fails its gate | which ticker holds the unsupported claims | smoke variance from judge listing (`7c66k` failed on MSFT alone); arms are compared on 40-ticker runs — go to `nstp9`; no re-run for a pass |
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
- `eval/runs/gpu-extended-f304375.log`: the `nstp9` run of record for the
  A10 arm (40 tickers, image `f3043751`, 10/267 on its first judging,
  TRAFFIC PROOF: EXACT).
- `eval/runs/gpu-smoke.log` is from the previous image `1f51dad`; the
  current image's GPU smoke `m7qvv` failed its gate on qualitative
  watch-items (4/60, numeric 0/30, proof EXACT), smoke variance.
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
traffic proof. Before and after each run the harness reads the llama.cpp
server's own token counters; the tokens the harness logged must equal the
server's difference exactly, and any other traffic on the endpoint fails
the proof. The A10 run of record was EXACT: 270 calls, 352,522 prompt and
98,665 completion tokens, identical on both sides. Both CPU runs on the
current image failed it, by 1 and 4 tokens: every one of their 270
requests matched the server's own log, but the server's counter drifted,
and the rule does not bend for an explained miss.

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

**What does a brief cost, and what is excluded?** Model cost only: at most
$0.0303 on an A10 (the whole VM at $2.00 an hour, divided over the briefs
the run produced) and $0.0357 through the hosted API (n = 3), both on
image `f3043751`; $0.0107 on a 4-OCPU slice of an E5 node, on the previous
image. The cost of record stays $0.0366 from September. The harness pods, storage and the judge are excluded on every
arm.

**Why was the A10 only 36–38% busy, and how fast could it go?** The run kept
two briefs in flight at a time, and each eval pod also spends time outside
the model — fetching data, retrieving filings, waiting on the judge; that
is the likely reason, not a measured breakdown. At that setting
the A10 averaged 36% utilization and produced 66 briefs an hour (38% and
68 on the previous image). It was
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
density gap (figures bound to stock data, sign test p = 0.0001); not enough to detect a difference of a
point or two in the unsupported rate. Say "not detected", never
"equivalent".

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

**What would you do next?** Record per-request token counts so a CPU run
can pass the traffic proof, and rerun the CPU arm on the current image;
measure the A10 at higher concurrency; apply the OKE Terraform when a compartment exists. The
full list is in the README's "Next steps".

## Where the evidence is

- Results and method: [eval-methodology.md](eval-methodology.md), the
  three-way section, with the cost section, the error types, the numeric
  check and every command.
- What may be quoted: [numbers-of-record.md](numbers-of-record.md).
- Topology: [architecture.md](architecture.md#deployed-topology-october-2026).
- Procedures: [deploy-runbook.md](deploy-runbook.md), "OKE (provided
  cluster)" and the self-served SLM steps.
