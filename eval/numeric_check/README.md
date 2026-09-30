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
