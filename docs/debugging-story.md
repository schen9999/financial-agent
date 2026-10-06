# Debugging story: a currency error the judge accepted and the numeric check caught

One case, end to end, from the flag to the line of code, using only what
the committed records hold. It is the clearest example of why the eval
has two layers. Three shorter cases follow.

## The symptom

The deterministic numeric check (`agent/numeric_check.py`) compares every
stock-data figure a brief states — price, market cap, revenue, net income,
profit margin, the 52-week range and the rest of the nine STOCK DATA
fields — with the value the pipeline supplied, at a 2% relative tolerance.
Run offline over the three same-image 40-ticker runs (2026-10-05,
`scripts/numeric_backtest.py --runs 9jzmj 8vpq6 p9jr2`), it raised 12
flags. Six were one company in the hosted run `9jzmj`:

| Section | Field | Brief states | Stock field | Ratio |
|---|---|---|---|---|
| Executive Summary | revenue | $52.0 billion | 51,957,024,686,080 | 0.001001 |
| Executive Summary | net_income | $4.5 billion | 4,483,796,959,232 | 0.001004 |
| Financial Health | revenue, net_income | the same two figures | the same | 0.001 |
| SEC Filing Highlights | revenue, net_income | the same two figures | the same | 0.001 |

Toyota (TM): the brief states each figure 1,000 times smaller than the
field, in dollars, in three sections. It is not new. The same "$52.0
billion" flag is in the hosted runs `j4cnp`, `kcf7s` and `dvvxk`
(`eval/numeric_check/upstream-findings.md`).

## What the judge said

The grounding judge audits the Executive Summary and Outlook, so it saw
the first two rows. It marked both SUPPORTED
(`eval/runs/raw/9jzmj-findings/TM_baseline.md`):

> CLAIM: "$52.0 billion in annual revenue" — SUPPORTED. "Source data shows
> revenue of 51,957,024,686,080.0 JPY, which the Financial Health
> pre-written section rounds to '$52.0 billion' — the AI brief reproduces
> this figure directly from the pre-written section."

> CLAIM: "$4.5 billion in net income" — SUPPORTED. "Source data shows
> net_income of 4,483,796,959,232.0, which the pre-written Financial Health
> section rounds to '$4.5 billion'; the brief reproduces this directly."

The judge read the revenue as yen, and still accepted a dollar figure
1,000 times smaller as a rounding of it. Its check was consistency with
the pre-written section, which held the same wrong figure.

## The trace

1. **The brief** repeats its pre-written Financial Health section:
   "robust annual revenue of $52.0 billion and net income of $4.5
   billion".
2. **The section** was written from the STOCK DATA block the pipeline
   supplied:
   ```json
   "currency": "USD",
   "revenue": 51957024686080.0,
   "net_income": 4483796959232.0,
   ```
   The dict says USD. A 51.96-trillion revenue is consistent with yen, not
   dollars — inferred from the magnitude, not checked against a live
   yfinance call.
3. **The stock tool** (`agent/tools/stock.py`) fills `currency` from
   yfinance `info["currency"]` — the trading currency of the listing, USD
   for an ADR — and takes `revenue` and `net_income` from `totalRevenue`
   and `netIncomeToCommon`, which yfinance reports in the filer's financial
   currency. It never reads `info["financialCurrency"]`. So for foreign
   filers the dict labels home-currency figures as USD. TM, TSM, NVO and
   BABA all show it; SAP hides it, because EUR and USD are close in scale.

That is the root cause: a dropped field in the data layer, not a model
error and not a judge bug. Every arm reads the same dict; what each brief
did with it differed (below).

## Why each layer saw what it saw

- **The judge** checks claims against the context by reading it. Here the
  context was internally consistent — the pre-written section agreed with
  the brief — and the judge accepted the agreement, with a confident
  explanation, even after naming the currency. Its population-weighted
  recall on UNSUPPORTED claims is 32.5% on the September baseline
  (calibration of record): misses are expected, and this is one.
- **The numeric check** does not read: it binds each figure in a sentence
  to a stock field and compares numbers. A ratio of 0.001 is far outside
  2%, in every section, including the two the judge never audits.
- **The adjudication** applied rule 5 of the rules written before
  labelling began (2026-09-30, `eval/numeric_check/README.md`): a
  home-currency figure written as dollars is a TRUE_ERROR. The committed
  attribution rule (`upstream_cause` in `scripts/numeric_adjudicated.py`:
  a power-of-ten rescale of a currency-affected field) then assigns all six
  to the upstream currency defect. All 11 TRUE_ERRORs across the three
  runs trace to that defect or to the second one (profit margin passed as
  a raw fraction); excluding them, every arm is at zero.

## The limits of each layer

The same defect reached the CPU arm's TM brief (`8vpq6`) differently: it
wrote "$51.96 trillion in revenue" — the field's value, under the field's
USD label. The numeric check compares a figure with its field, so a
faithful copy matches and is not flagged. The judge marked the claim
SUPPORTED, its reason again naming the currency: "The raw source data
lists revenue as 51,957,024,686,080.0 (JPY), which the pre-written
Financial Health section rounds to '$51.96 trillion'". Read as dollars,
the figure is wrong by the same defect, and both layers passed it. (The
A10 arm's TM brief states neither figure.) The check catches this defect
only when a brief's figure departs from the mislabelled field, as the
hosted brief's did; the fix belongs in the data layer, not in either
eval.

The check has its other blind spots, which the judge covered in the same
runs: a truncation under 2% (the CPU run's CHGG "-$52.9 million" for
-52.997M, 0.18% off) and a correct figure under the wrong label (the A10
run's SFIX "recent low of $2.61", the current price, and CRBU "market
capitalization near its 52-week low of $1.22", a per-share figure). The
judge flagged all three. Neither layer is sufficient alone.

## What was done, and what was not

- **Recorded, 2026-09-29**, when the numeric check's first backtest found
  it (`eval/numeric_check/upstream-findings.md`), together with the
  profit-margin defect.
- **Deliberately not fixed yet.** Both defects live in the stock data the
  pipeline hands every generator, so a fix changes the eval's inputs and
  every committed run stops being comparable with the runs after it. The
  fix — carry `financialCurrency` into the dict and use it for revenue and
  net income in the prompts and the numeric check — goes in after the
  demo, as a dated change with new baselines on every arm.
- **Until then** the numeric check runs at `warn` in the brief pipeline
  (it appends a note), not `block`, and the published numeric results
  state which errors are upstream.

## Three shorter cases

**An Argo permission, found by a 40-ticker run (2026-10-04).** The hosted
extended run `9jzmj` ended in Error at its aggregate step. Argo v3.7.18
hands a step its resolved template in an environment variable limited to
131,072 bytes; a larger template is offloaded by the controller to a
ConfigMap. The per-ticker LLM ledger added on 2026-10-02 grew each result
row about eightfold (about 4.9 KB hosted, 7.5 KB self-served), so the
aggregate crosses the limit at 27 hosted or 18 self-served tickers —
`9jzmj`'s was 198,065 bytes — and the controller had no permission to
create ConfigMaps. Fix: `argo/base/rbac.yaml` grants the controller's
service account `configmaps: [create]` in the `financial-agent` namespace
and nothing wider, proven on kind (`scripts/template_offload_probe.py`);
its first live use on OKE was the CPU run `8vpq6`, whose aggregate
template was 301,083 bytes. `9jzmj` itself was rebuilt offline with the
unchanged aggregate code — validated by reproducing another run's
(`7c66k`) in-cluster aggregate exactly, apart from the estimated-cost
line — so it stands as a citable run with that status. The
cleaner fix — shrink what each eval pod passes to the aggregate — changes
the image and waits until after the demo.

**A double-counted ledger (2026-10-03).** The hosted smoke `x2cx8` printed
an LLM-call table showing twice the real calls at the two RAG sites: a
callback handler was registered twice. A lock in `agent/llm_ledger.py`
fixed it from the next image; the corrected figures — 10 calls per RAG
site and 7.0 agent calls per ticker in both arms — come from the run's
own workflow object (`scripts/rag_ledger_from_workflow.py`). The cost of
record predates the handler and is unaffected.

**A 512-token cap that cut answers (2026-10-03).** Through image `2dd1aa3`
both arms used llama_index's Anthropic default of 512 tokens for RAG
answers. The first self-served smoke, `nb6r6`, had 13 of its 20 RAG
answers cut at the cap; the hosted smoke had none, but hosted runs back to
`j4cnp` had cut the SFIX risk-factors answer mid-structure. Fix: one
shared cap, `RAG_MAX_TOKENS = 2048` (`agent/tools/slm.py`), sized from a
natural-length check on the A10 (longest of the smoke's 20 answers: 854
tokens), passed to both arms, with a test holding them together
(`tests/test_rag_settings.py`). Consequence, stated wherever it matters:
hosted runs on later images are not the `j4cnp` pipeline exactly, which is
why the three-way, not `j4cnp`, is now the grounding number of record.

## Reproduce

```bash
python scripts/numeric_backtest.py --runs 9jzmj 8vpq6 p9jr2 --date 2026-10-05
python scripts/numeric_adjudicated.py --date 2026-10-05 \
  --adjudication eval/numeric_check/adjudication-2026-10-05-9jzmj-8vpq6-p9jr2.csv \
  --runs 9jzmj 8vpq6 p9jr2
grep -n -A2 'CLAIM: "\$52.0 billion' eval/runs/raw/9jzmj-findings/TM_baseline.md
grep -n -A8 'STOCK DATA' eval/runs/raw/9jzmj-findings/TM_baseline.md
```

Full method and tables: [eval-methodology.md](eval-methodology.md), "GPU
SLM extended run `p9jr2`" (the numeric check on the three-way) and "Dated
finding: the aggregate step's template outgrew Argo's inline limit".
