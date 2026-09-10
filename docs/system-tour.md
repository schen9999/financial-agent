# System tour

A guided tour of the financial research agent for someone joining the
project. It walks the system in six stops — what it is for, how it is
deployed on the OCI VM, the one experiment that carries the biggest
decision, the retrieval defect that reshaped the numbers, how the judge
that produces every rate is calibrated, and how to run and observe all of
it — and closes with the known limitations. The deeper references are
[architecture.md](architecture.md), [eval-methodology.md](eval-methodology.md),
[numbers-of-record.md](numbers-of-record.md), and
[deploy-runbook.md](deploy-runbook.md).

**Numbers policy.** Every number here is copied from
[numbers-of-record.md](numbers-of-record.md) with its judge-version tag
and date; nothing is quoted that is not on record there. Three scope
statements hold throughout: OKE is authored in Terraform (`fmt` +
`validate` pass) and has never been applied; nothing has run on more than
one node; the Haiku synthesis change is an experiment
(`scripts/compare_synthesis.py`) whose switch is held back, so synthesis
ships on Sonnet.

## 1. Purpose

The agent takes a ticker, pulls live stock data, news, and the SEC 10-K,
writes four sections (Financial Health, SEC Filing Highlights, Risk
Factors, Recent Developments), and synthesizes an Executive Summary and
Outlook. It serves someone who needs a first-pass research brief and
needs to know which sentences are backed by a source.

The question the project actually answers is the second half of that:
*can an LLM agent write briefs grounded in real sources, and how would
you know?* The measurement layer is therefore as much the deliverable as
the agent. Every quantitative or forward-looking claim in a brief is
audited by a judge model against the retrieved context and labeled
SUPPORTED, UNSUPPORTED, or INFERENCE; the unsupported-claim rate is a
gate that fails a run visibly.

Headline figures (numbers-of-record, "Current"):

- Grounding: **49% unsupported pre-fix → 0/84 unsupported in the current
  eval (95% CI 0.0–4.4%), judge v1**. Always quoted with the pre-fix
  context and the denominator, never as a bare 0%. Judge v1's recall on
  UNSUPPORTED measured 1/9 against human labels (2026-09-04), so this
  rate is a lower bound (section 5).
- Cost per brief: **$0.0366** (2026-09-06, post-retrieval-fix; 3-ticker
  mean over AAPL/NVDA/JPM from the committed `scripts/cost_report.py`).
- Pipeline latency: **26.29 s mean (~26 s) per brief** (Phase 0
  re-measure). A repeat request for the same ticker within 24 h is
  served from the exact-key cache.

## 2. The single-VM k3s topology on OCI

The full designed topology runs on one OCI VM (VM.GPU.A10.2: two A10 24 GB
cards, single-node k3s, reachable only by ssh). It is the first
environment where the whole topology runs together — the retired ECS
deployment was a single FastAPI container plus RDS, with no Celery,
Redis, Streamlit, or MCP in production.

Six services in namespace `financial-agent`:

| Service | Role |
|---|---|
| FastAPI | sync `POST /research`, async `POST /research/async` |
| Celery worker | request-time async only (`/research/async` → Redis broker → worker) |
| Redis | exact-key cache per ticker (`research:{TICKER}`, 24 h TTL) and the Celery broker/results; deliberately PVC-less on every target |
| Postgres | `research_briefs`; the one PVC, 50 Gi on k3s's `local-path` StorageClass |
| Streamlit | UI; runs the pipeline in-process (no Streamlit→FastAPI hop) |
| MCP server | streamable-HTTP at `/mcp`; ClusterIP on every target |

Beside them:

- **vLLM** (`k8s/vllm/overlays/k3s-gpu`): vLLM v0.10.2 serving the merged
  Qwen2.5-1.5B fine-tune from a hostPath, `nvidia.com/gpu: 1`, pinned to
  one of the two A10s with `CUDA_VISIBLE_DEVICES=0`, the same image and
  serving args the oke-gpu overlay commits to. On record: served in
  plain Docker (2026-09-02) and in-cluster on k3s (2026-09-03), both
  confirmed from the box. It backs the default-off `USE_LOCAL_MODEL`
  flag through the `LOCAL_MODEL_BACKEND=openai` seam.
- **Argo Workflows** (namespace `argo`): the `grounding-eval`
  WorkflowTemplate (fan-out of one pod per ticker, `parallelism: 2`, an
  aggregate step that is the gate) and the `grounding-eval-nightly`
  CronWorkflow (`30 3 * * *` America/New_York).

Four of the app pods run one image with four commands (Dockerfile.k8s);
the eval pods run the same image. Two boundaries are fixed: Celery is
request-time async only and Argo is eval orchestration only, never
merged; and eval pods set `BYPASS_CACHE=true`, so an eval measures the
pipeline, never the cache.

The manifests are one kustomize base with three overlays — `kind`
(local), `k3s` (this VM), `oke` (Phase 2) — and `scripts/render_diff.py`
proves the kind render never drifts when an overlay changes. The k3s
overlay's deltas are environmental only: NodePorts behind ssh tunnels
(mcp stays ClusterIP), an imported local image with `imagePullPolicy:
Never`, Postgres on `local-path`, hostPath weights, and the GPU pin.
The oke overlay and the Terraform for the OKE cluster, both node pools,
OCIR, the bucket, and the Block Volume storage class exist and validate
but have not been applied.

On record for this box: the gated eval DAG ran green on the VM on
2026-09-03 (hosted models, judge v1: 3.03% unsupported, 2/66), and every
run in section 3 executed on this node.

## 3. The 40-ticker A/B: hosted models vs the fine-tuned local model

**Setup.** The fine-tune is Qwen2.5-1.5B-Instruct, QLoRA, trained on
deterministic, Claude-free pairs built from real filings and financial
data. When `USE_LOCAL_MODEL` is on it writes two of the four sections
(Financial Health, Risk Factors); Haiku keeps the other two in both
arms, and Sonnet writes the synthesis in both arms. The question was
whether it could replace Haiku on those two sections without losing
grounding. The gate is the unsupported-claim rate: at most 5%, with a
minimum claim count so a quiet run cannot pass vacuously. Both arms ran
on the VM with the same image, the same post-retrieval-fix index, and
the same judge (v2), over 40 tickers chosen to stress coverage
(`eval/tickers_extended.txt`: large-cap, volatile-earnings, small-cap,
clinical-stage biotech, and five non-US ADRs that ran on stock + news
only, in both arms).

**Result** (numbers-of-record, "40-ticker A/B, hosted vs in-cluster vLLM
fine-tune", 2026-09-05/06, judge v2):

| Arm | Workflow | Unsupported | Wilson 95% CI | Gate (≤ 5%) | Est. cost |
|---|---|---|---|---|---|
| baseline (hosted) | `grounding-eval-extended-j4cnp` | 12/392 = **3.06%** | 1.8–5.3% | PASSED | $2.36 |
| local-model (in-cluster vLLM fine-tune, 2 sections) | `grounding-eval-extended-local-lsnnc` | 30/368 = **8.15%** | 5.8–11.4% | FAILED | $2.44 |

Fisher exact **p = 0.0023**. The intervals are disjoint and the local
arm's interval sits entirely above the gate; this is the first A/B that
separates the arms on its own.

**Where the failure lives** (numbers-of-record, "Per-section attribution
of the 40-ticker A/B", 2026-09-05/06, judge v2; `eval/section_attribution.py`).
Each judged claim is attributed to the pre-written section it restates
(normalized containment, else word-overlap ≥ 0.6, else unattributed — a
heuristic over paraphrased text, coverage ~78–79%):

| Arm | Fine-tune-owned (FH + RF) | Other sections | Unattributed |
|---|---|---|---|
| baseline | 1/202 = 0.50% (0.1–2.8%) | 3/104 = 2.88% (1.0–8.1%) | 8/86 = 9.30% (4.8–17.3%) |
| local-model | **22/111 = 19.82%** (13.5–28.2%) | 2/180 = 1.11% (0.3–4.0%) | 6/77 = 7.79% (3.6–16.0%) |
| Fisher exact | **p = 4.6e-10** | p = 0.36 | p = 0.79 |

The excess unsupported rate is concentrated entirely in the content the
fine-tune authored; the arms are statistically indistinguishable
everywhere else (p = 0.36 and p = 0.79). The buckets are diagnostic; the
overall A/B is the measured result. The attribution counts carry a
second signal: the baseline's synthesis restates FH/RF content
near-verbatim (202 attributed claims) while the fine-tune's phrasing is
restated less (111) — its sections diverge from their sources.

**Earlier measurements agree in direction** (numbers-of-record, dated
records):

- 10-ticker A/B on the VM, 2026-09-03, judge v1: 3.03% (2/66, CI
  0.8–10.4%) vs 12.31% (8/65, CI 6.4–22.5%), Fisher p = 0.0545 — the
  intervals overlap, so that run could not separate the arms alone.
- Aug 2026, 9-ticker balanced, grounding score: 86.2% hosted vs 77.8%
  local-hybrid.
- Cost, hosted vs hybrid on the pre-retrieval-fix pipeline: $0.0316 vs
  $0.0321 per brief — the sections saving is within run-to-run variance
  because Sonnet synthesis dominates the bill.

**Decision.** `USE_LOCAL_MODEL` ships off, as a measured negative
result: the model serves, the harness measured it, and it fails the gate
in exactly the text it owns.

**Caveat that travels with the table.** These are judge-v2 rates. v2 is
calibrated held-out at 75% recall / 60% precision on UNSUPPORTED (blind
labels, n = 50, 2026-09-06), so the absolute rates are approximate point
estimates; the A/B direction and the per-section attribution are
unaffected because both arms share the judge. Also on record: the
baseline's interval (1.8–5.3%) still includes the 5% gate at N = 392.

## 4. The 2026-09-04 retrieval defect and its effect on earlier numbers

**Mechanism.** On EDGAR filing index pages, inline-XBRL filers link the
primary document through an `/ix?doc=` viewer wrapper. The fetcher's
href regex matched only plain `.htm` links, the exhibit-name filter then
rejected every remaining file, and the fallback selected the first
file left — an Exhibit 4.x (Apple's was its bylaws). Two more layers hid
the problem: undecoded HTML entities broke the "Item 1A" heading anchor,
and a bare `item 1a` anchor also matched forward-looking-statement
cross-references. For weeks the automated eval scored a pipeline whose
"10-K" context was, for most tickers, an exhibit.

**How it was found.** Not by the eval. The human labeling pass for the
judge validation (2026-09-04) read retrieved contexts claim by claim and
found RSU agreements, indentures, and bonus plans where risk factors
should have been. The judge cannot notice this on its own: it judges a
claim against whatever context it is given.

**Fix and verification** (numbers-of-record, "Retrieval defect fix"). The
fetcher now resolves the primary document from the SEC submissions JSON
(`primaryDocument`, scrape kept as fallback, `/ix?doc=` unwrapped),
cleaning decodes entities, and the section anchor requires title
adjacency. `scripts/reindex_filings.py` verifies that top-3 risk-factor
retrieval carries risk prose and no exhibit/TOC boilerplate: **pre-fix
3/40 tickers passed; post-fix 32/40.** The remaining 8 are itemized in
eval-methodology.md: the five ADRs (20-F filers, the deliberate coverage
gap), two tickers whose windows still include a TOC-listing chunk, and
one verifier false positive.

**Effect on earlier numbers.**

- Every grounding number dated before 2026-09-04 measured the pipeline
  against exhibit text for most tickers. They stand as dated records of
  that pipeline, including the 0/84 (judge v1) number of record.
- Post-fix baselines, judge v2, 40 tickers: 3.10% unsupported (12 U of
  387 claims, CI 1.8–5.3%) on `9j2dj` (2026-09-05, 27 min, est. $2.35)
  and 3.06% (12/392) on `j4cnp` after an image rebuild, Fisher p = 1.0 —
  the baseline is stable run to run.
- Cost moved from $0.0316/brief (pre-fix pipeline) to $0.0366/brief
  (2026-09-06), because real Item 1A prose is longer than exhibit text.
  $0.0316 is quoted only as a dated pre-fix record.

## 5. Judge validation and the calibration caveat every rate carries

An LLM judge is a measurement instrument, so it is calibrated against
human labels, and the calibration is stated next to every rate it
produces.

**Judge v1** (numbers-of-record, "Judge validation (v1, 50-claim sample,
2026-09-04)"). 50 claims, author-labeled, not blind: Cohen's kappa
**0.321**; recall on UNSUPPORTED **1/9 = 11.1%** (CI 2.0–43.5%);
precision **1/3 = 33.3%** (CI 6.1–79.2%). The failure mode: INFERENCE
was a catch-all — most human-UNSUPPORTED claims were filed as
INFERENCE, which the gate does not count. Consequence: every judge-v1
rate in this repository (0/84, 3.03%, 12.31%) is a lower bound on what a
human reading would find.

**Judge v2** (numbers-of-record, "Judge validation (v2, held-out, labeled
2026-09-06)"). Five rules written from v1's failure modes and frozen
before the sample existed; 50 claims drawn from the 40-ticker A/B runs
with zero overlap with the dev set, labeled blind with no model
consultation: kappa **0.580**; recall on UNSUPPORTED **9/12 = 75.0%**
(CI 46.8–91.1%); precision **9/15 = 60.0%** (CI 35.7–80.2%). v2 trades
the catch-all for a mild over-flag of INFERENCE as UNSUPPORTED (5 of 6
false positives). Consequence: v2's errors run both ways, so v2 rates
are approximate point estimates, not bounds. A/B directions are
unaffected when both arms share the judge.

**Injected-failure check** (numbers-of-record, "Critic recall on injected
failures", 2026-09-04). Orthogonal to human labels: twenty fixtures with
known ground truth (a number swapped in the audited text, supporting
lines dropped, a plausible claim inserted). Recall **20/20 = 100%** (CI
83.9–100%) on both runs; raw precision against the injection tags
20/24 = 83.3%, and **adjudicated precision 24/24 = 100%** (CI
86.2–100%) — every off-needle flag was a genuine unsupported claim,
either a cascade from the injection or pre-existing. A gated CI job
(`.github/workflows/critic-injection.yml`, manual dispatch or schedule
only, because it spends judge credits) re-runs this on judge-adjacent
changes and asserts recall ≥ 0.8; if it regresses, the bar does not move
— the number gets reported.

**How to read any rate in this repository.** A judge-v1 rate is a lower
bound. A judge-v2 rate is an approximate point estimate whose errors run
both ways. Either way, an A/B direction is trustworthy when both arms
share the judge, and every rate carries its Wilson interval and every
two-arm comparison its Fisher p-value (`eval/stats.py`).

## 6. Running and observing the system

**Locally, on kind** (from the `financial-agent` WSL2 distro, repo root,
filled-in `.env`; details in [deploy-runbook.md](deploy-runbook.md)):

```bash
make cluster-up        # single-node kind (idempotent; restarts a stopped node)
make deploy            # build, kind load, secrets from .env, apply k8s/overlays/kind, wait
make smoke-test        # 13/13 assertions on record: sync brief, Celery async, cache hit + miss, MCP
make argo-install      # Argo controller + server, pinned via argo/install
make argo-deploy       # RBAC, grounding-eval WorkflowTemplate, nightly CronWorkflow
make eval-run          # submit the 10-ticker eval DAG and follow it to the gate verdict
make cost-report       # re-runnable cost/brief harness (needs .env)
```

Endpoints on kind: API http://localhost:30080, Streamlit
http://localhost:30501, MCP http://localhost:30800/mcp. kind has no GPU
and the dev CPU cannot run vLLM (no AVX-512); `USE_LOCAL_MODEL` is
exercised locally through Ollama, the committed fallback backend.

**On the VM** (single-VM section of the runbook). A fresh box is brought
to readiness by `scripts/vm_bootstrap.sh` (written 2026-09-09, not yet
executed; the actions it wraps were applied by hand on 2026-09-02/03),
the weights are rsynced to `/home/ubuntu/models/qwen-ft`, then:

```bash
make vm-images                       # build the app image and import it into k3s containerd
make vm-up                           # app overlay + secrets, Argo, then vLLM
make vm-eval                         # the eval DAG on the VM (same submit/follow as eval-run)
make vm-local-model ON=true|false    # toggle app-plane routing to vLLM; eval arms are unaffected
```

The VM binds nothing publicly; reach it through an ssh tunnel with
non-30xxx local ports (kind owns 30080/30501/30800 on the laptop):

```bash
ssh -L 31080:localhost:30080 -L 31501:localhost:30501 -L 31880:localhost:30880 ubuntu@<vm-ip>
```

**Observing the topology:**

```bash
kubectl -n financial-agent get pods,svc,pvc     # six services + vllm; mcp ClusterIP; postgres PVC Bound
kubectl -n argo get pods                         # workflow-controller + argo-server
kubectl -n financial-agent get cronworkflow      # grounding-eval-nightly, 30 3 * * * America/New_York
kubectl -n financial-agent get workflows         # retained run history
nvidia-smi                                       # vLLM's process on one A10, the other idle
curl -s http://localhost:31880/v1/models         # lists financial-lora (through the tunnel)
```

**Observing a brief and the cache.** A first request for a ticker is a
cold run (~26 s mean on record); a repeat within 24 h returns the same
bytes from the Redis key `research:<TICKER>`. This is an exact-key
cache, not a semantic one.

```bash
curl -s -X POST http://localhost:31080/research -H 'Content-Type: application/json' -d '{"ticker":"<TICKER>"}'
```

**Observing the eval plane.** `make eval-run` (or `make vm-eval`) submits
`argo/eval-run.yaml` and follows it; the aggregate output carries the
gate verdict, the rate with its Wilson interval, and a labeled per-run
cost estimate. The 40-ticker variants are
`argo/eval-run-extended.yaml` and `argo/eval-run-extended-local.yaml`;
one 40-ticker arm took 27 min on record (`9j2dj`, 2026-09-05, est.
$2.35), and the two A/B arms were estimated at $2.36 + $2.44. Every run
spends Anthropic credits in every arm (Haiku sections and the Sonnet
judge); a low balance fails the run loudly rather than skipping tickers.
After any run, capture the per-claim findings while the pods exist
(runbook, "Findings capture"). The nightly gate's first fire (2026-08)
failed at 5.62% on one NVDA outlier draft; the re-measure was 0/10, so
the threshold stayed at 5% — a red run is examined, not tuned away.

**Recomputing the recorded numbers from committed artifacts.** All three
run offline in seconds and were re-run on 2026-09-09:

```bash
# 40-ticker A/B rates, intervals, and Fisher p (12/392 vs 30/368)
python -c "from eval.stats import format_rate_ci, fisher_exact; \
print(format_rate_ci(12, 392), format_rate_ci(30, 368), fisher_exact(12, 380, 30, 338))"

# three-bucket section attribution (prints p-values at four decimals; the
# fine-tune-owned bucket shows as p = 0.0000, the record's 4.6e-10)
python eval/section_attribution.py \
  --run eval/runs/j4cnp-claims.jsonl eval/runs/raw/j4cnp-findings \
  --run eval/runs/lsnnc-claims.jsonl eval/runs/raw/lsnnc-findings

# judge v2 held-out agreement: kappa 0.580, recall 75%, precision 60%
python eval/agreement.py --labeled eval/judge_validation/holdout_sample.csv \
                         --key eval/judge_validation/holdout_key.csv
```

**Tests.** `python -m pytest tests/`: 1645 lines, 111 tests collected —
110 passed + 1 skipped, the credit-gated judge test that runs only under
`CRITIC_INJECTION=1` (as of 2026-09-09).

## Known limitations and next steps

**The fine-tune fails, and why.** Three things, all on record. It is a
1.5B model trained on a small, deterministic, Claude-free pair set, and
it owns the two sections where the failure concentrates: 19.82% vs 0.50%
unsupported on attributed claims (p = 4.6e-10, judge v2, 2026-09-05/06),
while the sections Haiku writes are indistinguishable between arms. The
held-out labeling also showed what the failure looks like in prose: a
scale-conversion error on a market cap and a literal unfilled template
placeholder in a local-arm section — neither invented from nothing, both
wrong. And the direction reproduced across three independent
measurements: 86.2% vs 77.8% (Aug 2026), 3.03% vs 12.31% (2026-09-03,
judge v1), 3.06% vs 8.15% (2026-09-05/06, judge v2). How much more data
or a larger base model would close is unknown; this configuration does
not, and the harness is what established that.

**Is the current configuration ship-ready?** The hosted path, yes, as it
runs on the VM: gated nightly, cache bypassed in eval, secrets never in
git, one image for every role, and the test suite above. The fine-tune,
no — it ships default-off as a measured negative result. Two qualifiers
belong in any ship note: the hosted baseline's interval (1.8–5.3% at N =
392) still includes the 5% gate, and the judge that produces the rate is
calibrated at 75% recall / 60% precision on the class the gate rides on.
And this is one node: nothing has run on OKE or on more than one node.

**The section-audit gap.** The judge audits the synthesis (Executive
Summary + Outlook), not the four pre-written sections. A fine-tune
section error that the synthesis drops never reaches the gate — the
CRBU market-cap and placeholder errors above were both absent from the
audited text. The measured 8.15% therefore understates the fine-tune's
raw section error rate. Auditing the sections directly is an open piece
of harness work.

**Judge reliability.** Nobody knows the judge is right; what is known is
how wrong it is, and that travels with every number. v1 measured kappa
0.321 and 1/9 recall on UNSUPPORTED, so every v1 rate is a lower bound.
v2, validated held-out and blind on a sample it had never seen, measures
kappa 0.580, 75% recall, 60% precision, with errors in both directions.
On injected failures with known ground truth it caught 20/20, every
off-needle flag adjudicated as a real unsupported claim. The limits: one
labeler (the author), n = 50 so the UNSUPPORTED cells are single digits
and the intervals are wide, and the v1 labels were not blind. The human
labeling pass is also what found the retrieval defect the judge had been
blind to for weeks — the strongest evidence in the project that the
labels, not the judge, are the ground truth.

**Next steps, in the order the data asks for them.**

1. Widen the judge calibration: a second labeler and a larger held-out
   sample, because n = 50 single-author labels leave the intervals wide.
2. Close the retrieval coverage gap the reindex verification itemizes:
   five ADRs on 20-F filings, two tickers with TOC chunks in the window.
3. Land the Haiku synthesis change only after a quality re-eval on the
   VM, then re-measure cost with `scripts/cost_report.py` before quoting
   any new figure; until then $0.0366 stands.
4. OKE: apply the authored Terraform and run the same DAG there (Phase 2
   in the runbook). Cost per brief on OCI and vLLM throughput on the A10
   under OKE are to-be-measured cells in the record.
5. The fine-tune: more and better training data before any re-run, or
   retire it. The serving path is proven; the model is not.
