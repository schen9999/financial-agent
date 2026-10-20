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
  sources and fails the run above 5% unsupported; a per-request match
  against the model server's own log, a separate step today, shows that
  the self-served model, and nothing else, produced the run.
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
  than hosted** (`1f51dad`, judged three times): unsupported 2.89% CPU `8vpq6`,
  2.25% A10 `p9jr2`, 2.16% hosted `9jzmj` (means of pooled rates; not the
  `4hsn2` ticker-averaged 2.16% on the current image), no difference
  detected on either pair;
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

Moved to [harness-mapping.md](harness-mapping.md) (2026-10-19).

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

## The live run

One GPU smoke: ten tickers, the self-served model on node 2's A10, judged
by Claude, gated, with the traffic proof. A CPU smoke takes about 6
minutes per brief, 38 minutes for the ten (`xnwjm`), and does not fit the
call; the A10 runs the same model file and engine in about 10. Every
command is in
[deploy-runbook.md, "Demo live run"](deploy-runbook.md#demo-live-run-november-2026-gpu-smoke-from-the-oke-harness).

**Preflight, on the rehearsal day (rehearsal and freeze 2026-10-24, spare day 2026-10-25) and 30 minutes before:**
[demo-preflight.md](demo-preflight.md), each check's command and expected
output in order, stopping at the first failure. In short: the Anthropic
balance covers the runs (`make anthropic-estimate`: $0.90 a smoke on this
image; on the rehearsal day, rehearsal + demo + one spare, $2.71, budget $4.06
with margin); OKE nodes and pods Ready; the nightly CronWorkflow
suspended and nothing running; the image is the pinned `f3043751`; the
app's `SLM_FULL` is off; node 2's endpoint healthy and keyed, holding
about 20.5 GB of the A10, vLLM at 0; 401 and 200 from OKE; one Yahoo
price from the cluster; no key on a shared screen; tunnels up. On the
rehearsal day, the preflight ends with a full rehearsal run, the live CPU ask
beside it, the run's per-request proof, and then the freeze tag.

**Launch** (operator), at the start of the demo:

```bash
make slm-eval-run ENDPOINT=gpu EVAL_RUN_FILE=argo/eval-run-slm-gpu-smoke.yaml
```

About 10 minutes. Nothing else may call the GPU endpoint until the proof's
log is captured: other traffic fails the proof, by design.

**On screen while it runs:** the operator pane with the run's progress;
the Argo UI graph (ten eval pods, two at a time, then the aggregate); a
node 2 pane with `watch -n 2 nvidia-smi`, the A10 moving with the calls;
partway through, a second operator pane with the live CPU ask (below).
At the end: the aggregate table, the gate line, `stock block empty: 0/10`,
the call table with no truncation, loop, parse, format or error flags,
the attempts block (0 retries), then the per-request proof
(`scripts/traffic_proof_tasks.py`, preflight check 14):
`TRAFFIC PROOF (per-request): TASK-EXACT`. The make target's last line is
the `/metrics` counter proof, which is reported and does not decide: the
counter has drifted by a few tokens on both endpoints with every request
matched, so it may print FAIL on a clean run.

**If something fails** — each case ends at the fallback (the recorded runs); say what
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
| Live CPU ask prints `refusing:` | the line names the setting | nothing was sent; skip the step, say so, show the recorded CPU tool-use pane instead (below) |
| Live CPU ask: `FATAL: slm-cpu … unreachable` | preflight check 4 (`llamacpp` Running) | skip the step; the recorded pane |
| Live CPU ask: `NOT OK — hosted Anthropic call attempted` | the tool it was in | the guard stopping a hosted call, by design; say so, no re-run |
| Live CPU ask: the `query_sec_filing` result is an error naming Hugging Face, `HF_HUB_OFFLINE` or a missing model file | check 13's embedding line | the model is not in the image's cache and the hub is switched off, by design; skip the step, or run `ALT=2` (no embedding) if time allows |
| Live CPU ask: a tool result `Could not find SEC CIK …` or `SEC lookup failed …` | check 13's EDGAR line | EDGAR throttling, as on 2026-08-24, when MSFT's CIK lookups failed (commit `0aa2678`); show it as it is, no live retry; the recorded pane |
| Live CPU ask: `10-K check … MISMATCH` and `NOT OK … 10-K MISMATCH` | the two dates on the line | a newer Walmart 10-K than the indexed one (not expected before about March 2027); the filing date and the risk factors would come from different filings, so do not show the answer; say why, and use the recorded pane |
| Live CPU ask still running when its turn comes | the pane's last tool line | go on, and read it out at the end |
| Live CPU ask: one tool only, or a weak answer | the tool lines | show it as it is: a single unjudged question, not a measurement |

### Live CPU: one /ask question on the CPU endpoint

The GPU smoke is the live eval; this is the live CPU moment. One question,
answered by the ReAct `/ask` agent (the harness in the blog post's sense:
one agent loop with tools) with every model call on the CPU llama.cpp
endpoint in the OKE cluster. It runs from the api pod, the same way
preflight check 9 runs `server_facts`:

```bash
make live-cpu-ask          # operator, second pane, while the GPU smoke runs
```

[scripts/live_cpu_ask.py](../scripts/live_cpu_ask.py) prints the endpoint
and the alias the server reports, the question, each tool call and its
result as the agent makes them, the answer, each model call's endpoint,
alias, tokens and seconds, and a last line `LIVE CPU ASK: OK — wall <n> s,
…`. The pinned image predates the script, so `make` passes the file in as
`python -c`'s argument (not on stdin, which the operator's kubectl
credential plugin consumes).

- **The question** (default): Walmart — "When was Walmart's most recent
  10-K filed, and what does it say about the risks of its omnichannel and
  eCommerce investments?" It
  needs two tools, `get_sec_filings` (EDGAR) and `query_sec_filing`
  (retrieval over the filing, whose answer is itself written by the CPU
  model). It calls no Yahoo: the smoke fetches Yahoo for ten tickers from
  the same egress IP at the same time, and that IP has drawn 429s.
- **Why Walmart: both tools describe the same filing until March 2027.**
  `get_sec_filings` always returns the latest 10-K; `query_sec_filing`
  answers from the 10-K indexed in Pinecone, and every namespace was
  rebuilt on 2026-09-04 (`scripts/reindex_filings.py`; Walmart passed its
  risk-factor verification). Walmart's latest 10-K was filed on 2026-03-13
  for the year to 31 January 2026, before the reindex, and the next is due
  about March 2027 (EDGAR, read 2026-10-16). The first default, Visa, would
  not hold: its fiscal year ends 30 September, its 10-K of 2025-11-06 is
  the indexed one, and its next is likely in the first half of November,
  inside the demo window. Then the filing date on screen would come from
  the new 10-K and the risk-factor answer from the old one. The script
  checks this: it reads the 10-K date from `get_sec_filings`' result and
  prints `10-K check … indexed filing: 2026-03-13 -> same filing`; any
  other date prints `MISMATCH` and fails the run (`NOT OK … 10-K
  MISMATCH`).
- **Alternates**, `make live-cpu-ask ALT=1` and `ALT=2`. `ALT=1`: "What
  is Apple's current P/E ratio, and what does its fiscal 2025 10-K say
  about the risks of relying on outsourcing partners, located in a few
  places, mostly in Asia, to manufacture its products?"
  (`get_stock_data` + `query_sec_filing`). It uses Yahoo, so only outside
  the smoke. It is named by fiscal year, with no filing-date part, because
  Apple files its next 10-K around the end of October and its index holds
  the fiscal 2025 one. It asks for one risk the 10-K states directly, as
  the default does, not an open-ended list. `ALT=2`: Microsoft's recent
  news and its latest 10-Q date
  (`get_company_news` + `get_sec_filings`; NewsAPI returned nothing for 32
  of 40 tickers in `4hsn2`, so the news half may come back empty).
- **What routes to the CPU, from the code.** `make live-cpu-ask` sets
  `SLM_FULL=true SLM_ENDPOINT=cpu` for that one process only. Under it
  the ReAct model is `SLMChatModel` (`agent/react_agent.py`), and the
  retrieval answer inside `query_sec_filing` goes to the same endpoint per
  query (`agent/tools/rag.py`). Each request reads `SLM_ENDPOINT` and uses
  `SLM_CPU_URL`, the in-cluster Service (`agent/tools/slm.py`). The api
  server itself keeps `SLM_FULL=false` (preflight check 7).
- **Hosted calls under that setting: none expected, and blocked.** The
  only Anthropic objects on this path are constructed and never called:
  the hosted ReAct model is not built, and llama_index's global
  `Settings.llm` (Haiku) is bypassed by the per-query model. The script
  makes every Anthropic SDK request raise for its whole run. If one were
  attempted, it would print `NOT OK — hosted Anthropic call attempted` and
  exit 1. It spends no Anthropic credit, so the budget lines are
  unchanged. Not model calls, but outside the cluster: EDGAR and Pinecone
  for the tools. The embedding model (`BAAI/bge-small-en-v1.5`) is baked
  into the image by `Dockerfile.k8s` at `f3043751`, and `make
  live-cpu-ask` runs with `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`, so
  the ask does not contact Hugging Face. The image is private, so that is
  read from the Dockerfile and confirmed in the pod by check 13, not by
  inspecting the image from outside. EDGAR has throttled the harness
  before: MSFT's CIK lookups failed in the 2026-08-24 run (commit
  `0aa2678`), so check 13 makes one EDGAR request first. LangSmith tracing is off for the
  process.
- **Why it cannot touch the GPU smoke's proof.** That proof matches every
  task in node 2's llama-server log, from the smoke's creation to the
  capture, against the smoke's own harness calls. The ask's process has
  no address or key for node 2: `SLM_GPU_URL` and `SLM_GPU_API_KEY` are
  blanked in its environment, and the script refuses to start unless they
  are empty and the endpoint is `cpu`. Its requests go to a different
  server with its own log, inside the cluster. It also exits NOT OK if
  any model call is recorded against an endpoint other than `slm-cpu`. And
  if something did reach node 2, the proof would show an unmatched task
  and fail. It would not pass with the ask's traffic mixed in.
- **What it is:** a demonstration, not a citable run. No judge, no traffic
  proof, one question. Its wall time is one observation. The CPU's
  citable numbers stay `8vpq6` on `1f51dad`.
- **How long it takes, from a dated trial** (operator, 2026-10-16 about
  18:31Z, image `f3043751`, the Visa question this step then used): `OK`,
  wall 93.3 s, `get_sec_filings` then `query_sec_filing`, three model calls
  all on `slm-cpu` (ReAct 13.4 s, retrieval answer 40.7 s, ReAct 38.3 s),
  hosted calls attempted 0. About 95 s fits easily inside the GPU smoke's
  ~10 minutes.
- **A second dated trial, and why the wording changed** (operator,
  2026-10-16 about 18:49Z, the Walmart question in its first wording,
  "…what does that 10-K list as the main risk factors?"): `OK`, wall
  72.5 s, `10-K check` 2026-03-13 against the indexed 2026-03-13, same
  filing; model calls ReAct 6.0 s, retrieval answer 35.2 s, ReAct 30.4 s;
  0 hosted calls. The answer drifted: only its omnichannel/eCommerce
  point was a real risk factor. It recast Walmart's "Shared Value"
  framework (Opportunity, Sustainability, Community) as risks and
  mislabelled a category ("Legal, Tax, Regulatory…", then strategic
  risks). With the top three retrieved chunks, an open-ended "main risk
  factors" invites that, so the default now asks about the one risk that
  retrieval returned cleanly. Neither trial is a citable run.
- **Trials of the narrowed questions** (operator, 2026-10-16, image
  `f3043751`, after the narrowing merged; dated, not citable runs):
  - **Apple alternate** (`ALT=1`, about 19:06Z): `OK`, wall 95.8 s,
    `get_stock_data` + `query_sec_filing`; ReAct 7.6 s, retrieval answer
    58.8 s, ReAct 28.4 s; 0 hosted calls. The answer stayed on topic: the
    P/E from Yahoo, and the outsourcing risk with detail
    the question did not ask for, from the retrieved filing text (mainland
    China, India, Japan, South Korea, Taiwan and Vietnam; single- or
    limited-source components; natural disasters, public health, labor,
    power and cyber disruptions). No drift.
  - **Walmart default** (about 19:09Z): `OK`, wall 33.8 s, `10-K check`
    same filing (2026-03-13); ReAct 6.1 s, retrieval answer 4.5 s, ReAct
    22.5 s; 0 hosted calls. On topic: execution risk and the cost of the
    omnichannel and eCommerce investments. **33.8 s is a warm time:** the
    retrieval answer took 4.5 s against 35.2 s on the first Walmart run
    20 minutes earlier, very likely llama.cpp reusing its prompt cache for
    the same retrieved chunks (likely, not checked in the server log). The
    cold time is about 70 s (the first Walmart run, 72.5 s). On the day
    the endpoint will have served the smoke's other prompts in between, so
    plan for cold.
  - **A model addition to watch for:** the Walmart answer's closing line
    mentions "Walmart+". That word is in none of the four chunks of
    Walmart's Pinecone namespace and not in `get_sec_filings`' 10-K
    summary (checked 2026-10-16 with read-only retrieval, no model call),
    so the model added it from its own knowledge. Harmless here, but it is
    not from the sources: if it comes up, say so.
- **Not done: a 1-ticker CPU smoke beside the GPU smoke.** Considered and
  not built. `make slm-eval-run` finds its workflow afterwards as the
  newest one in the namespace, so with two running it would capture the
  other run's logs and workflow into the GPU proof's inputs. It would also
  add a second run's Yahoo fetches from the same egress, and judge
  spend, to the live window.

**Fallback for this step:** `eval/runs/tool-use-2026-10-05/tool_use_pane.txt`
and `tool_use_cpu.json` (10 one-tool questions on the CPU route, every one
completed on `slm-cpu`; dated, not under a traffic proof).

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

## Where the evidence is

- Results and method: [eval-methodology.md](eval-methodology.md), the
  three-way section, with the cost section, the error types, the numeric
  check and every command.
- What may be quoted: [numbers-of-record.md](numbers-of-record.md).
- Topology: [architecture.md](architecture.md#deployed-topology-october-2026).
- Procedures: [deploy-runbook.md](deploy-runbook.md), "OKE (provided
  cluster)" and the self-served SLM steps.
