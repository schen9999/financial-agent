# Demo walkthrough — 20 minutes, OCI hiring team

**Audience:** Basu, the team, and the manager. **When:** on or around
2026-09-18. **Target:** the single OCI VM (VM.GPU.A10.2, single-node k3s,
reached only through ssh tunnels). **Fallback:** the laptop kind cluster
(last page — same script, minus the GPU).

**Rules this script follows.** Every number below is copied from
[numbers-of-record.md](numbers-of-record.md) with its judge-version tag
and date; nothing is quoted that is not already on record there. Nothing
is claimed for OKE (Terraform is authored, `fmt` + `validate` pass, never
applied), for multi-node (never run), or for the Haiku synthesis switch
(an experiment, `scripts/compare_synthesis.py`; the switch is held back
and synthesis ships on Sonnet). Where a number is recorded rather than
produced live, the script says so and says why.

## Timing

| # | Section | Minutes | Cumulative |
|---|---|---|---|
| 1 | What the system does and who it is for | 2 | 2 |
| 2 | Single-VM k3s architecture on OCI | 3 | 5 |
| 3 | The 40-ticker A/B: hosted vs fine-tuned local model | 5 | 10 |
| 4 | The 2026-09-04 retrieval defect | 3 | 13 |
| 5 | Judge v2 held-out validation and the caveat every rate carries | 3 | 16 |
| 6 | Live system walkthrough | 4 | 20 |
| — | Q&A | whatever remains, then open-ended | — |

## Before you start (T-30 min)

1. Tunnel up from the laptop (non-30xxx local ports — kind owns 30080/30501/30800 locally):
   ```bash
   ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<vm-ip>
   ```
   Add `-L 31800:localhost:30800` plus, on the VM,
   `kubectl -n financial-agent port-forward svc/mcp 30800:8000` only if
   the MCP endpoint will be shown.
2. On the VM: `kubectl -n financial-agent get pods` all Running,
   `kubectl -n argo get pods` all Running, `nvidia-smi` showing the vLLM
   process on one card and the other idle.
3. Pick the live-brief ticker: one not requested in the last 24 h (the
   exact-key cache TTL), so the first call is a cold run and the repeat is
   a hit.
4. Check Anthropic credit balance. The live eval submission in section 6
   spends credits on every ticker (Haiku sections + Sonnet judge); the
   harness fails loudly on a low balance rather than skipping tickers.
5. Open in editor tabs, for the recorded beats: `eval/runs/j4cnp-claims.jsonl`,
   `eval/runs/lsnnc-claims.jsonl`, `eval/judge_validation/holdout_sample.csv`,
   and [numbers-of-record.md](numbers-of-record.md).
6. At T-0, in a second VM terminal, submit the 10-ticker eval DAG:
   `make vm-eval`. Its finishing time is not on record, so its completion
   is a bonus for section 6, not a beat the script depends on.

## 1. What the system does and who it is for (2 min)

**Say.** It is a financial research agent: give it a ticker, it pulls
live stock data, news, and the SEC 10-K, writes four sections (Financial
Health, SEC Filing Highlights, Risk Factors, Recent Developments) and
synthesizes an Executive Summary and Outlook. It is for someone who needs
a first-pass research brief and needs to know which sentences are backed
by a source. The question the project actually answers is the second
half: *can an LLM agent write briefs that are grounded in real sources,
and how would you know?* So the deliverable is the measurement layer as
much as the agent.

**Show.** One finished brief in Streamlit (http://localhost:31501),
already cached, so it renders instantly. Point at a sentence with a
figure and say: every claim like this one is audited by a judge model
against the retrieved context, and the audit is a gate.

**Numbers (numbers-of-record, "Current").**
- Grounding: **49% unsupported pre-fix → 0/84 unsupported in the current
  eval (95% CI 0.0–4.4%), judge v1** — quoted always with the pre-fix
  context and the denominator, never as a bare 0%. Judge v1's recall on
  UNSUPPORTED measured 1/9 against human labels (2026-09-04), so this
  rate is a lower bound; section 5 covers what that means.
- Cost per brief: **$0.0366** (2026-09-06, post-retrieval-fix; 3-ticker
  mean over AAPL/NVDA/JPM, from the committed `scripts/cost_report.py`).
- Pipeline latency: **26.29 s mean (~26 s) per brief** (Phase 0
  re-measure). That is why the live brief in section 6 is a cold call
  followed by a cache hit.

## 2. Single-VM k3s architecture on OCI (3 min)

**Say.** One node, one namespace, the full designed topology. Six
services: FastAPI (sync `/research`, async `/research/async`), a Celery
worker, Redis, Postgres, Streamlit, and an MCP server over
streamable-HTTP. Plus two things beside them: vLLM serving the fine-tuned
Qwen2.5-1.5B on one A10, and Argo Workflows owning the evaluation DAG.
Four of the pods run the same image with four different commands; the
eval pods run that image too. Two boundaries worth stating: Celery is
request-time async only and Argo is eval orchestration only, never
merged; and the Redis cache is an exact-key cache per ticker (key
`research:{TICKER}`), rebuildable, so Redis runs without a volume on
every target. Postgres keeps the one PVC, 50 Gi on k3s's local-path.

**Show.** [architecture.md](architecture.md)'s diagram on one screen,
then live on the VM:

```bash
kubectl -n financial-agent get pods,svc,pvc     # six services + vllm; mcp ClusterIP; postgres PVC Bound
kubectl -n argo get pods                         # workflow-controller + argo-server
kubectl -n financial-agent get cronworkflow      # grounding-eval-nightly, 30 3 * * * America/New_York
nvidia-smi                                       # vLLM's process on one A10, the other idle
```

**Say, about OCI specifically.** The manifests are one kustomize base
with three overlays, kind / k3s / oke, and a semantic render diff
(`scripts/render_diff.py`) proves the kind render never drifts when an
overlay changes. This VM is the k3s overlay: NodePorts behind ssh
tunnels, an imported local image, hostPath weights, vLLM pinned to one of
the two cards with the same image and serving args the oke-gpu overlay
commits to. The oke overlay and the Terraform for the OKE cluster, node
pools, OCIR, bucket, and Block Volume storage class exist and validate,
but **have not been applied** — no compartment yet. Say that plainly if
asked; do not describe OKE as running.

**What is on record for this box.** vLLM v0.10.2 served the merged
fine-tune pinned to one A10 in plain Docker (2026-09-02) and in-cluster
on k3s (2026-09-03); the gated eval DAG ran green on the VM the same day
(hosted models, judge v1: 3.03% unsupported, 2/66). Everything in
section 3 ran on this node.

## 3. The 40-ticker A/B: hosted vs fine-tuned local model (5 min)

**Say.** The fine-tune is Qwen2.5-1.5B-Instruct, QLoRA, trained on
deterministic, Claude-free pairs built from real filings and financial
data; it writes two of the four sections (Financial Health, Risk
Factors) and Haiku keeps the other two in both arms. The question was
whether it could replace Haiku on those sections. The gate is the
unsupported-claim rate: at most 5%, with a minimum claim count so a quiet
run cannot pass vacuously. Both arms ran on
this VM, same image, same post-retrieval-fix index, same judge (v2),
over 40 tickers chosen to stress coverage: large-cap, volatile-earnings,
small-cap, clinical-stage biotech, and five non-US ADRs.

**Show — the A/B (numbers-of-record, "40-ticker A/B", 2026-09-05/06, judge v2).**

| Arm | Workflow | Unsupported | Wilson 95% CI | Gate (≤ 5%) | Est. cost |
|---|---|---|---|---|---|
| baseline (hosted) | `grounding-eval-extended-j4cnp` | 12/392 = **3.06%** | 1.8–5.3% | PASSED | $2.36 |
| local-model (in-cluster vLLM fine-tune, 2 sections) | `grounding-eval-extended-local-lsnnc` | 30/368 = **8.15%** | 5.8–11.4% | FAILED | $2.44 |

Fisher exact **p = 0.0023**. The intervals are disjoint and the local
arm's interval sits entirely above the gate. This is the first A/B that
separates the arms on its own.

**Show — where the failure lives (numbers-of-record, "Per-section
attribution of the 40-ticker A/B", 2026-09-05/06, judge v2;
`eval/section_attribution.py`).** Each judged claim is attributed to the
pre-written section it restates (normalized containment, else
word-overlap ≥ 0.6, else unattributed — a heuristic over paraphrased
text, coverage ~78–79%):

| Arm | Fine-tune-owned (FH + RF) | Other sections | Unattributed |
|---|---|---|---|
| baseline | 1/202 = 0.50% (0.1–2.8%) | 3/104 = 2.88% (1.0–8.1%) | 8/86 = 9.30% (4.8–17.3%) |
| local-model | **22/111 = 19.82%** (13.5–28.2%) | 2/180 = 1.11% (0.3–4.0%) | 6/77 = 7.79% (3.6–16.0%) |
| Fisher exact | **p = 4.6e-10** | p = 0.36 | p = 0.79 |

Overall, for reference: 12/392 = 3.06% vs 30/368 = 8.15%, p = 0.0023.
The excess unsupported rate is concentrated entirely in the content the
fine-tune authored; the arms are statistically indistinguishable
everywhere else (p = 0.36 and p = 0.79). The buckets are diagnostic;
the overall A/B is the measured result. One more sign worth saying
aloud: the baseline's synthesis restates FH/RF content near-verbatim
(202 attributed claims) while the fine-tune's phrasing is restated less
(111) — the fine-tune's sections diverge from their sources.

**Say — the earlier measurements agree in direction.**
- 10-ticker A/B on this VM, 2026-09-03, judge v1: 3.03% (2/66, CI
  0.8–10.4%) vs 12.31% (8/65, CI 6.4–22.5%), Fisher p = 0.0545 — the
  intervals overlap, so that run could not separate the arms alone.
- Aug 2026, 9-ticker balanced, grounding score: 86.2% hosted vs 77.8%
  local-hybrid.
- Cost, hosted vs hybrid (pre-retrieval-fix pipeline): $0.0316 vs
  $0.0321 per brief — the sections saving is within run-to-run variance,
  because Sonnet synthesis dominates the bill.

**The decision.** `USE_LOCAL_MODEL` ships off. Say it as measured and
declined, not unfinished: the model serves, the harness measured it, it
failed the gate where it owns the text.

**Caveat to state with the table.** These are judge-v2 rates. v2 is
calibrated held-out at 75% recall / 60% precision on UNSUPPORTED (blind
labels, n = 50, 2026-09-06), so the absolute rates are approximate point
estimates; the A/B direction and the per-section attribution are
unaffected because both arms share the judge. Also on record as an
observation: the baseline's interval (1.8–5.3%) still includes the 5%
gate at N = 392.

**Live-recompute option (offline, seconds, from committed artifacts) —
use it if time allows, it lands well:**

```bash
python -c "from eval.stats import format_rate_ci, fisher_exact; \
print(format_rate_ci(12, 392), format_rate_ci(30, 368), fisher_exact(12, 380, 30, 338))"
python eval/section_attribution.py \
  --run eval/runs/j4cnp-claims.jsonl eval/runs/raw/j4cnp-findings \
  --run eval/runs/lsnnc-claims.jsonl eval/runs/raw/lsnnc-findings
```

Both were dry-run on 2026-09-09 and reproduce the table above. Note the
attribution script prints the fine-tune-owned p-value at four decimals,
as `p = 0.0000` — the same value the record carries as 4.6e-10.

## 4. The 2026-09-04 retrieval defect (3 min)

**Say.** For weeks the automated eval scored a pipeline whose "10-K"
context was, for most tickers, an exhibit. Mechanism: on EDGAR index
pages inline-XBRL filers link the primary document through an `/ix?doc=`
viewer wrapper; the fetcher's regex matched only plain `.htm` links, the
exhibit filter rejected the rest, and the fallback picked the first
remaining file — an Exhibit 4.x (Apple's was its bylaws). Two more
layers hid it: undecoded HTML entities broke the "Item 1A" heading
anchor, and a bare `item 1a` anchor matched forward-looking-statement
cross-references.

**How it was caught.** Not by the eval. By the human labeling pass for
the judge validation (2026-09-04): reading retrieved contexts claim by
claim and finding RSU agreements, indentures, and bonus plans where risk
factors should be. The judge had been scoring that retrieval as
supported or unsupported for weeks without noticing, because it judges a
claim against whatever context it is given. That is the single best
argument in this project for labeling by hand.

**Fix and verification (numbers-of-record, "Retrieval defect fix").**
The fetcher now resolves the primary document from the SEC submissions
JSON, cleaning decodes entities, and the anchor requires title
adjacency. `scripts/reindex_filings.py` verifies that top-3 risk-factor
retrieval carries risk prose and no exhibit/TOC boilerplate:
**pre-fix 3/40 tickers passed; post-fix 32/40.** The remaining 8 are
itemized: the five ADRs (20-F filers, the deliberate coverage gap), two
tickers whose windows still include a TOC-listing chunk, and one
verifier false positive.

**What it did to earlier numbers — say this exactly.**
- Every grounding number dated before 2026-09-04 measured the pipeline
  against exhibit text for most tickers. They stand as dated records of
  that pipeline, including the 0/84 (judge v1) number of record.
- Post-fix baselines, judge v2, 40 tickers: 3.10% unsupported (12 U of
  387 claims, CI 1.8–5.3%) on `9j2dj` (2026-09-05, 27 min, est. $2.35)
  and 3.06% (12/392) on `j4cnp` after an image rebuild, Fisher p = 1.0 —
  the baseline is stable run to run.
- Cost moved: $0.0316/brief (pre-fix pipeline) → $0.0366/brief
  (2026-09-06), because real Item 1A prose is longer than exhibit text.
  $0.0316 is quoted only as a dated pre-fix record.

## 5. Judge v2 held-out validation and the caveat every rate carries (3 min)

**Say.** An LLM judge is a measurement instrument, so it gets
calibrated against humans, and the calibration travels with every rate.

**Judge v1 (dev set, 2026-09-04, numbers-of-record "Judge validation (v1)").**
50 claims, author-labeled, not blind: Cohen's kappa **0.321**; recall on
UNSUPPORTED **1/9 = 11.1%** (CI 2.0–43.5%); precision **1/3 = 33.3%**
(CI 6.1–79.2%). The failure mode: INFERENCE was a catch-all — most
human-UNSUPPORTED claims were filed as INFERENCE, which the gate does not
count. Consequence: every judge-v1 rate in this repo (0/84, 3.03%,
12.31%) is a lower bound on what a human would find.

**Judge v2 (held out, labeled 2026-09-06, numbers-of-record "Judge validation (v2)").**
Five rules written from v1's failure modes, frozen before the sample
existed. 50 claims drawn from the 40-ticker A/B runs, zero overlap with
the dev set, labeled blind with no model consultation: kappa **0.580**;
recall on UNSUPPORTED **9/12 = 75.0%** (CI 46.8–91.1%); precision
**9/15 = 60.0%** (CI 35.7–80.2%). v2 trades the catch-all for a mild
over-flag of INFERENCE as UNSUPPORTED (5 of 6 false positives).
Consequence: v2 errors run both ways, so v2 rates are approximate point
estimates, not bounds. A/B directions are unaffected when both arms
share the judge.

**Show.** Recompute it in front of them from the committed sample — it
is offline and takes a second:

```bash
python eval/agreement.py --labeled eval/judge_validation/holdout_sample.csv \
                         --key eval/judge_validation/holdout_key.csv
```

**Orthogonal check (numbers-of-record "Critic recall on injected failures", 2026-09-04).**
Twenty fixtures with known ground truth (a number swapped in the audited
text, supporting lines dropped, a plausible claim inserted): recall
**20/20 = 100%** (CI 83.9–100%) on both runs; raw precision against the
injection tags 20/24 = 83.3%, and **adjudicated precision 24/24 = 100%**
(CI 86.2–100%) — every off-needle flag was a genuine unsupported claim
(cascades from the injection, or pre-existing). A gated CI job re-runs
this on judge changes and asserts recall ≥ 0.8; if it regresses, the bar
does not move — the number gets reported.

**Limitations to volunteer before anyone asks.** One labeler (the
author); n = 50, so the UNSUPPORTED cells are single digits and the
intervals are wide; the v1 labels were not blind; and the judge audits
the synthesis only, so a fine-tune section error that the synthesis
drops never reaches the gate (an on-record observation from the
held-out labeling: a scale-conversion error on a market cap and a
literal unfilled template placeholder in a local-arm section, both
absent from the audited text). The 8.15% therefore understates the
fine-tune's raw section error rate.

## 6. Live system walkthrough (4 min)

**What is live and what is recorded, and why.**

| Beat | Live or recorded | Why |
|---|---|---|
| Pods, services, PVC, CronWorkflow, `nvidia-smi` | Live | Seconds; proves the topology on this node |
| Cold brief through the API, then the cache hit | Live | ~26 s mean per brief on record; the hit is instant |
| Streamlit render of the same ticker | Live | Instant from the exact-key cache |
| 10-ticker eval DAG submitted at T-0 | Live submission, progress shown; completion is a bonus | Its finishing time is not on record; do not wait on it |
| 40-ticker A/B (both arms) | Recorded | One 40-ticker arm took 27 min on record (`9j2dj`, 2026-09-05); two arms are about an hour of wall clock and est. $2.36 + $2.44 of credits |
| Per-claim rows, section attribution, judge agreement | Recomputed live from committed artifacts | Offline, deterministic, seconds |
| vLLM serving the fine-tune | Live `/v1/models` on the tunnel; the A/B against it is recorded | Serving is cheap to show; the measurement is the hour above |
| Nightly gate history | Recorded | The first nightly fire (2026-08) failed at 5.62% on one NVDA outlier draft; the re-measure was 0/10, so the threshold stayed at 5% — the gate fails visibly and is re-examined, not moved |

**Script.**

```bash
# 1. Topology (10 s)
kubectl -n financial-agent get pods,svc,pvc && nvidia-smi

# 2. Cold brief, then the exact-key cache hit (~30 s + instant)
time curl -s -X POST http://localhost:31080/research -H 'Content-Type: application/json' \
     -d '{"ticker":"<TICKER>"}' | head -c 600
time curl -s -X POST http://localhost:31080/research -H 'Content-Type: application/json' \
     -d '{"ticker":"<TICKER>"}' | head -c 200
# say: same bytes, from Redis key research:<TICKER>; 24 h TTL; not a semantic cache

# 3. Streamlit (http://localhost:31501) — render the same ticker

# 4. vLLM is up (10 s)
curl -s http://localhost:31880/v1/models | head -c 300     # lists financial-lora

# 5. The eval plane (30 s)
kubectl -n financial-agent get workflows                     # the run submitted at T-0, plus retained history
kubectl -n financial-agent get cronworkflow grounding-eval-nightly -o jsonpath='{.spec.schedule} {.spec.timezone}'
# if the T-0 run finished: make vm-eval's aggregate output — the gate verdict, the rate with its CI, the labeled cost estimate
```

**Say while the brief runs.** The request hits FastAPI, which runs the
pipeline in-process for the sync endpoint; the async endpoint enqueues
to Celery through Redis. Eval pods never touch this cache
(`BYPASS_CACHE=true`), so the numbers in section 3 measured the
pipeline, not the cache.

**If the T-0 DAG has not finished**, show its phase and progress and
move on. If it failed the gate, show that too: a red workflow is the
point of the design.

## Q&A — honest, non-defensive answers

**Why did the fine-tune fail?**
Three things, all on record. It is a 1.5B model trained on a small,
deterministic, Claude-free pair set, and it owns the two sections where
the failure concentrates: 19.82% vs 0.50% unsupported on attributed
claims (p = 4.6e-10, judge v2, 2026-09-05/06), while the sections Haiku
writes are indistinguishable between arms. The held-out labeling also
surfaced what the failure looks like in prose: a scale-conversion error
on a market cap and a literal template placeholder, neither invented
from nothing, both wrong. And the direction reproduced across three
independent measurements: 86.2% vs 77.8% (Aug 2026), 3.03% vs 12.31%
(2026-09-03, judge v1), 3.06% vs 8.15% (2026-09-05/06, judge v2). I do
not know how much more data or a larger base model would close; I know
this configuration does not, and the harness is what told me.

**Would you ship this?**
The hosted path, yes, as it runs on this VM: gated nightly, cache
bypassed in eval, secrets never in git, one image for every role, and
1645 lines of tests (111 tests collected: 110 passed + 1 skipped, the
credit-gated judge test, as of 2026-09-09). The fine-tune, no — it ships default-off as a measured
negative result. Two honest qualifiers I would put in the ship note: the
hosted baseline's interval (1.8–5.3% at N = 392) still includes the 5%
gate, and the judge that produces the rate is calibrated at 75% recall /
60% precision on the class the gate rides on. Also: this is one node.
Nothing here has run on OKE or on more than one node.

**What would you do next?**
In order of what the data asks for. Widen the judge calibration: a
second labeler and a larger held-out sample, because n = 50 single-author
labels leave the intervals wide. Close the retrieval coverage gap that
the reindex verification itemizes: five ADRs on 20-F filings, two
tickers with TOC chunks in the window. Land the Haiku synthesis change
only after a quality re-eval on the VM, and re-measure cost with the
committed harness before quoting any new figure. Then OKE: the Terraform
is written and validates; applying it and running the same DAG there is
Phase 2, and the cost on OCI is a to-be-measured cell in the record. For
the fine-tune: more and better training data before any re-run, or
retire it — the serving path is proven, the model is not.

**How do you know the judge is right?**
I do not, fully — I measure how wrong it is and carry that with every
number. v1 was measured at kappa 0.321 and 1/9 recall on UNSUPPORTED
against human labels, which is why every v1 rate is stated as a lower
bound. v2 was rewritten from those failure modes and then validated
held-out, blind, on a sample it had never seen: kappa 0.580, 75% recall,
60% precision. On injected failures with known ground truth it caught
20/20, with every off-needle flag adjudicated as a real unsupported
claim. The limits are stated on the same page: one labeler, n = 50,
errors in both directions for v2, and a scope boundary — it audits the
synthesis, not the raw sections. The human labeling pass is also what
found the retrieval defect the judge had been blind to for weeks, which
is the strongest argument I have that the labeling, not the judge, is
the ground truth.

## If the VM is not ready — the same script from the laptop kind cluster

One page; same beats, same recorded artifacts, one honest substitution:
kind has no GPU and this CPU cannot run vLLM (no AVX-512), so the vLLM
beat is recorded, not live. Nothing else in the script changes.

**Setup (from the `financial-agent` WSL2 distro, repo root, filled-in `.env`):**

```bash
make cluster-up        # single-node kind (idempotent; restarts a stopped node)
make deploy            # build, kind load, secrets from .env, apply k8s/overlays/kind, wait
make smoke-test        # 13/13 assertions on record: sync brief, Celery async, cache hit + miss, MCP
make argo-install      # pinned via argo/install
make argo-deploy       # RBAC, grounding-eval WorkflowTemplate, nightly CronWorkflow (kind overlay)
```

Endpoints are direct, no tunnel: API http://localhost:30080, Streamlit
http://localhost:30501, MCP http://localhost:30800/mcp.

**Section-by-section substitutions.**

| Section | On kind |
|---|---|
| 1 | Unchanged; the cached brief renders from the local Streamlit |
| 2 | `kubectl -n financial-agent get pods,svc,pvc` shows the six services (no vllm pod); say that the k3s and oke overlays are the same base with environmental deltas, proven by `scripts/render_diff.py`; the A10 serving is on record from the VM (2026-09-02 Docker, 2026-09-03 k3s) |
| 3 | Unchanged — every number is recorded, and the recompute commands read committed files |
| 4 | Unchanged |
| 5 | Unchanged — `eval/agreement.py` runs offline |
| 6 | Cold brief + cache hit against :30080, Streamlit at :30501, `make eval-run` submitted at T-0 (10 tickers, hosted models, spends credits; finishing time not on record); skip the `/v1/models` beat and say why |
| Q&A | Unchanged |

**Pre-demo check on the laptop (T-30 min):** `make status` shows all
six pods Running; `make smoke-test` passes 13/13; the same editor tabs
from the VM checklist are open; credit balance checked before
`make eval-run`.

**One thing not to do on kind:** do not run the local-model arm through
Ollama as a stand-in for vLLM and present it as the A/B. The A/B on
record was measured against in-cluster vLLM on the A10; Ollama is the
committed fallback for exercising the code path, not a measurement.
