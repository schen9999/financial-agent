#!/usr/bin/env python3
"""Terminal labeler for the numeric-check adjudication CSV.

Walks eval/numeric_check/adjudication.csv in adjudication order: live
(full or partial scope) hosted rows, then live local-model rows, then the
replication sample, by id within each group. It starts at the first row in
that order whose verdict is blank. Per row it shows run, scope, model,
ticker, section, field, the full sentence with the stated figure
highlighted, the stated and source values, ratio, kind and occurrences.
For a revenue or net_income row of a currency-affected ticker (rule 5), or
a profit_margin whose |source| > 1 (rule 6), it also prints a one-line
reminder of that adjudication rule (eval/numeric_check/README.md).

  t / f / o   verdict TRUE_ERROR / FALSE_POSITIVE / OTHER_DEFECT
  n           add a note to this row (the verdict is still asked for)
  u           undo the last verdict or note entered this session and
              return to its row
  q           save and quit

No tally of verdicts and no precision is shown while labeling. The progress
line counts the rows that have a verdict, never which verdicts they got,
and the labeled rows carrying a doubt note (a note, or a " | "-joined part
of one, starting "doubt:"; rule 8). Once at least 20 rows are labeled and
doubt notes exceed 5% of them, one warning line is printed under the
progress line (no pause).

Saving: after every verdict and every note the file is rewritten
atomically (temp file in the same directory, then os.replace), UTF-8, with
the same csv writer scripts/numeric_backtest.py uses (minimal quoting, "\\n"
line endings). Only the answered fields change. Restarting resumes at the
first unlabeled row.

Usage:
  python eval/numeric_check/label_cli.py
  python eval/numeric_check/label_cli.py --csv path/to/adjudication.csv
"""
import argparse
import csv
import io
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CSV = HERE / "adjudication.csv"
KEYS = {"t": "TRUE_ERROR", "f": "FALSE_POSITIVE", "o": "OTHER_DEFECT"}
LIVE_SCOPES = ("full", "partial")
# Rule 8: warn when doubt notes exceed this share of labeled rows, once
# enough rows are labeled that one early doubt cannot trip it.
DOUBT_PREFIX = "doubt:"
DOUBT_SHARE = 0.05
DOUBT_MIN_LABELED = 20

# Tickers whose revenue/net_income the stock dict carries in the filer's
# home currency but labels USD (upstream-findings.md (a)).
CURRENCY_TICKERS = {"TM", "TSM", "NVO", "BABA", "SAP"}
CURRENCY_FIELDS = {"revenue", "net_income"}
# One-line reminders of the adjudication rules in README.md.
CURRENCY_REMINDER = ("rule 5 (currency): compare to the real USD value; yen/TWD/DKK/"
                     "CNY/EUR magnitude as dollars = TRUE_ERROR, correct USD "
                     "flagged by the mislabeled source = FALSE_POSITIVE")
MARGIN_REMINDER = ("rule 6 (margin, |source| > 1): the source is a fraction "
                   '(-2.49 = -249%); a brief writing "-2.49%" = TRUE_ERROR')


class AdjudicationFile:
    """The adjudication CSV, rewritten whole on every change."""

    def __init__(self, path: Path):
        self.path = path
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.fields = list(reader.fieldnames or [])
            self.rows = list(reader)
        missing = {"id", "scope", "arm", "verdict", "note"} - set(self.fields)
        if missing:
            raise SystemExit(f"{path.name} lacks column(s) {sorted(missing)}; "
                             "regenerate it with scripts/numeric_backtest.py")
        self.order = sorted(range(len(self.rows)), key=self._order_key)

    def _order_key(self, k: int) -> tuple:
        r = self.rows[k]
        if r["scope"] in LIVE_SCOPES:
            group = 0 if r["arm"] == "baseline" else 1
        else:
            group = 2
        return (group, int(r["id"]))

    def set(self, k: int, field: str, value: str) -> None:
        self.rows[k][field] = value
        self._save()

    def _save(self) -> None:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=self.fields, lineterminator="\n")
        w.writeheader()
        w.writerows(self.rows)
        fd, tmp = tempfile.mkstemp(prefix=f".{self.path.name}.", dir=self.path.parent)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(buf.getvalue().encode("utf-8"))
            shutil.copymode(self.path, tmp)
            os.replace(tmp, self.path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    def first_unlabeled(self) -> int | None:
        return next((k for k in self.order if not self.rows[k]["verdict"].strip()), None)

    def labeled_count(self) -> int:
        return sum(1 for r in self.rows if r["verdict"].strip())

    def doubt_count(self) -> int:
        """Labeled rows with a doubt note; reads notes only, never verdicts."""
        return sum(1 for r in self.rows if r["verdict"].strip() and has_doubt(r["note"]))


def has_doubt(note: str) -> bool:
    return any(part.strip().lower().startswith(DOUBT_PREFIX) for part in note.split(" | "))


def reminders(r: dict) -> list[str]:
    out = []
    if r.get("ticker") in CURRENCY_TICKERS and r.get("field") in CURRENCY_FIELDS:
        out.append(CURRENCY_REMINDER)
    if r.get("field") == "profit_margin":
        try:
            if abs(float(r.get("source", ""))) > 1:
                out.append(MARGIN_REMINDER)
        except ValueError:
            pass
    return out


def _highlighter(out):
    if getattr(out, "isatty", lambda: False)():
        return lambda s: f"\033[7m{s}\033[0m"
    return lambda s: f">>{s}<<"


def highlight(sentence: str, stated: str, mark) -> str:
    if not stated or stated not in sentence:
        return sentence
    return re.sub(re.escape(stated), lambda m: mark(m.group(0)), sentence)


def fmt_source(source: str) -> str:
    """Large sources get digit grouping and a magnitude so they can be read
    against the stated figure; everything else is shown as stored."""
    try:
        v = float(source)
    except ValueError:
        return source
    for scale, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M")):
        if abs(v) >= scale:
            return f"{source}  (= {v:,.0f} = {v / scale:.4g}{suffix})"
    return source


def show(af: AdjudicationFile, k: int, out) -> None:
    r = af.rows[k]
    mark = _highlighter(out)
    labeled, doubts = af.labeled_count(), af.doubt_count()
    out.write("\n" + "=" * 78 + "\n")
    out.write(f"id {r['id']}   position {af.order.index(k) + 1}/{len(af.rows)}   "
              f"labeled {labeled}/{len(af.rows)}   doubt notes: {doubts}/{labeled}\n")
    if labeled >= DOUBT_MIN_LABELED and doubts > DOUBT_SHARE * labeled:
        out.write(f"!! doubt notes exceed {DOUBT_SHARE:.0%} of labeled rows: rule 8 says "
                  "stop and write a dated amendment before continuing\n")
    out.write(f"run        : {r['run']}   scope: {r['scope']}   arm: {r['arm']}\n")
    out.write(f"model      : {r['model']}\n")
    out.write(f"ticker     : {r['ticker']}   section: {r['section']}   "
              f"field: {r['field'] or '-'}\n")
    out.write("-" * 78 + "\n")
    out.write(highlight(r["sentence"], r["stated"], mark) + "\n")
    out.write("-" * 78 + "\n")
    out.write(f"stated     : {r['stated']}\n")
    out.write(f"source     : {fmt_source(r['source']) or '-'}\n")
    out.write(f"ratio      : {r['ratio'] or '-'}   kind: {r['kind']}   "
              f"occurrences: {r['occurrences']}\n")
    if r["note"].strip():
        out.write(f"note       : {r['note']}\n")
    for line in reminders(r):
        out.write(f"!! {line}\n")


def run(path: Path, inp=input, out=sys.stdout) -> None:
    af = AdjudicationFile(path)
    undo: list[tuple[int, str, str]] = []  # (row, field, previous value)
    k = af.first_unlabeled()
    if k is None:
        out.write(f"all {len(af.rows)} rows labeled in {path.name}\n")
        return
    while k is not None:
        show(af, k, out)
        while True:
            out.write("[t]rue error  [f]alse positive  [o]ther defect  "
                      "[n]ote  [u]ndo  [q]uit: ")
            out.flush()
            a = inp().strip().lower()
            if a in KEYS or a in ("n", "u", "q"):
                break
            out.write("unrecognized; use t, f, o, n, u or q\n")
        if a == "q":
            break
        if a == "u":
            if not undo:
                out.write("nothing to undo this session\n")
                continue
            k, field, old = undo.pop()
            af.set(k, field, old)
            out.write(f"undid {field} on id {af.rows[k]['id']}\n")
            continue
        if a == "n":
            out.write("note (Enter alone cancels): ")
            out.flush()
            text = inp().strip()
            if text:
                old = af.rows[k]["note"]
                undo.append((k, "note", old))
                af.set(k, "note", f"{old} | {text}" if old.strip() else text)
            continue
        undo.append((k, "verdict", af.rows[k]["verdict"]))
        af.set(k, "verdict", KEYS[a])
        k = af.first_unlabeled()
    left = len(af.rows) - af.labeled_count()
    out.write(f"\nsaved {path.name}: {af.labeled_count()}/{len(af.rows)} labeled, "
              f"{left} unlabeled\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    args = ap.parse_args(argv)
    # Sentences carry characters a Windows cp1252 console cannot encode;
    # show a replacement rather than crash mid-row.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        run(Path(args.csv))
    except (KeyboardInterrupt, EOFError):
        print("\nquit (every answer is already saved)")


if __name__ == "__main__":
    main()
