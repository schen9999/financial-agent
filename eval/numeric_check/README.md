# Numeric-check adjudication

`adjudication.csv` holds every distinct finding from the numeric-check
backtest (`scripts/numeric_backtest.py`; identical repeats inside a brief are
collapsed into `occurrences`). A human fills `verdict`; the script never does.

| verdict | meaning |
|---|---|
| `TRUE_ERROR` | The brief states the stock field wrong (or leaves a real template placeholder). |
| `FALSE_POSITIVE` | The check is wrong: misbinding, or a right number judged wrong. |
| `OTHER_DEFECT` | A real defect that is not a wrong number, e.g. a truncated brief whose figure is cut off ("net loss of -$3"). |

`scope` is `partial` for runs whose files persist only the Exec Summary and
Outlook (9j2dj); those rows are adjudicated like any other but kept out of
per-arm and pooled figures. `scope` is `replication` for the pre-registered
frozen-input replication (`replication-plan.md`; outputs in
`eval/runs/replay-replication-<date>/`): `run` is `<replay>/<arm>/s<sample>`,
`arm` is `bf16` or `w4a16`, only Financial Health and Risk Factors exist
there, and the rows are a stratified sample of 60 per arm (the draw is in
`replication-sample.json`). Its precision is reported separately, per arm,
and applied to that arm's flag count. The 3-sample pilot
(`eval/runs/replay-pilot-<date>/`) is not labelled.

Precision, from the filled CSV, two ways (OTHER_DEFECT counted as a true
positive, and OTHER_DEFECT excluded), per run, per arm and per (arm, model),
with Wilson 95% CIs; the unit is a distinct finding:

    python scripts/numeric_backtest.py --precision

Re-running the backtest keeps verdicts already entered (matched on run,
ticker, section, kind, field, stated, sentence).

See `upstream-findings.md` for two stock-data defects (reporting currency,
profit-margin fraction) that bear on some verdicts.

Label with the terminal labeler (live hosted rows first, then live
local-model, then replication; resumes at the first unlabeled row; shows no
tally or precision while labeling):

    python eval/numeric_check/label_cli.py

`note` holds free-text adjudicator notes (key `n`); re-running the backtest
keeps them alongside the verdicts.

## Adjudication rules (written before labeling, 2026-09-30)

1. TRUE_ERROR: the brief states a wrong figure for that company, field and
   period, beyond normal rounding.
2. FALSE_POSITIVE: the brief's statement is correct and the check misread
   it: wrong field bound, unit parsed wrong, a different period, another
   company, or a correctly computed derived figure.
3. OTHER_DEFECT: the brief is broken but not because a number is wrong,
   e.g. text truncated mid-figure ("net loss of -$3").
4. Placeholders ("[City Name]" and similar): TRUE_ERROR. The check claimed a
   placeholder was present, and it was.
5. Currency (TM, TSM, NVO, BABA, SAP; revenue and net_income only): compare
   the brief's dollar figure to the company's real value in USD. A figure
   in yen/TWD/DKK/CNY/EUR magnitude written as dollars is TRUE_ERROR. A
   correct USD conversion flagged only because the source is mislabeled is
   FALSE_POSITIVE.
6. Profit margin with |source| > 1: the source is a fraction (-2.49 means
   -249%). A brief that writes "-2.49%" is TRUE_ERROR.
7. Rounding: a figure correct to its own stated precision ("$16.8B" for
   16.83B) is FALSE_POSITIVE.
8. Unsure: choose the best verdict and add a note starting "doubt:". If
   doubt notes exceed about 5% of rows labeled so far, stop and revise these
   rules in a dated amendment before continuing; do not relabel silently.
