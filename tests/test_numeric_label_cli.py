"""eval/numeric_check/label_cli.py: order, resume, undo, notes, reminders;
the CSV changes only in the answered fields and no tally is ever shown."""
import csv
import io

from eval.numeric_check.label_cli import (CURRENCY_REMINDER, KEYS, MARGIN_REMINDER,
                                          AdjudicationFile, highlight, reminders, run, show)
from scripts.numeric_backtest import ADJ_FIELDS, VERDICTS, _merge_verdicts


def _row(id_, run_, scope, arm, ticker="AAPL", field="market_cap", source="1000.0",
         sentence='Cap is "$1,000", per filings.', stated="$1,000"):
    return {"id": id_, "run": run_, "scope": scope, "arm": arm, "model": "m",
            "ticker": ticker, "section": "Financial Health", "kind": "mismatch",
            "field": field, "sentence": sentence, "stated": stated,
            "source": source, "ratio": "0.1", "occurrences": 1,
            "verdict": "", "note": ""}


def _write(path, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=ADJ_FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def _feed(answers):
    it = iter(answers)
    return lambda: next(it)


def _fixture(tmp_path):
    # File order deliberately differs from adjudication order.
    rows = [_row(1, "lsnnc", "full", "local-model"),
            _row(2, "replay/bf16/s0", "replication", "bf16"),
            _row(3, "j4cnp", "full", "baseline"),
            _row(4, "9j2dj", "partial", "baseline"),
            _row(5, "v924f", "full", "local-model")]
    path = tmp_path / "adjudication.csv"
    _write(path, rows)
    return path


def test_keys_are_the_backtest_verdicts():
    assert set(KEYS.values()) == set(VERDICTS)


def test_order_live_hosted_then_live_local_then_replication(tmp_path):
    af = AdjudicationFile(_fixture(tmp_path))
    assert [af.rows[k]["id"] for k in af.order] == ["3", "4", "1", "5", "2"]


def test_label_quit_resume_changes_only_verdicts(tmp_path):
    path = _fixture(tmp_path)
    before = path.read_bytes()
    out = io.StringIO()
    run(path, inp=_feed(["t", "f", "q"]), out=out)
    after = _read(path)
    assert after["3"]["verdict"] == "TRUE_ERROR"
    assert after["4"]["verdict"] == "FALSE_POSITIVE"
    assert all(after[i]["verdict"] == "" for i in ("1", "5", "2"))
    # Clearing the answered fields restores the original bytes exactly.
    for r in after.values():
        r["verdict"] = ""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=ADJ_FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(sorted(after.values(), key=lambda r: int(r["id"])))
    assert buf.getvalue().encode("utf-8") == before
    # Resume at the first unlabeled row in adjudication order (id 1).
    out = io.StringIO()
    run(path, inp=_feed(["o", "q"]), out=out)
    assert _read(path)["1"]["verdict"] == "OTHER_DEFECT"
    assert out.getvalue().split("=" * 78)[1].lstrip().startswith("id 1 ")


def test_undo_restores_the_verdict_and_returns_to_its_row(tmp_path):
    path = _fixture(tmp_path)
    out = io.StringIO()
    run(path, inp=_feed(["t", "u", "f", "q"]), out=out)
    rows = _read(path)
    assert rows["3"]["verdict"] == "FALSE_POSITIVE"
    assert rows["4"]["verdict"] == ""
    assert "undid verdict on id 3" in out.getvalue()


def test_undo_with_nothing_to_undo(tmp_path):
    path = _fixture(tmp_path)
    out = io.StringIO()
    run(path, inp=_feed(["u", "q"]), out=out)
    assert "nothing to undo" in out.getvalue()


def test_note_is_saved_appended_and_undoable(tmp_path):
    path = _fixture(tmp_path)
    run(path, inp=_feed(["n", 'Brief says "JPY", see TM', "q"]), out=io.StringIO())
    assert _read(path)["3"]["note"] == 'Brief says "JPY", see TM'
    run(path, inp=_feed(["n", "second", "n", "third", "u", "t", "q"]), out=io.StringIO())
    rows = _read(path)
    assert rows["3"]["note"] == 'Brief says "JPY", see TM | second'
    assert rows["3"]["verdict"] == "TRUE_ERROR"
    run(path, inp=_feed(["n", "", "q"]), out=io.StringIO())
    assert _read(path)["4"]["note"] == ""


def test_no_tally_or_precision_is_shown(tmp_path):
    path = _fixture(tmp_path)
    out = io.StringIO()
    run(path, inp=_feed(["t", "f", "o", "t", "q"]), out=out)
    text = out.getvalue()
    assert "precision" not in text.lower()
    for v in VERDICTS:
        assert v not in text


def test_reminders():
    for field in ("revenue", "net_income"):
        assert reminders(_row(1, "r", "full", "baseline", ticker="TM", field=field))             == [CURRENCY_REMINDER]
    assert reminders(_row(1, "r", "full", "baseline", ticker="TM", field="market_cap")) == []
    assert reminders(_row(1, "r", "full", "baseline", ticker="AAPL", field="revenue")) == []
    margin = dict(field="profit_margin", ticker="LCID")
    assert reminders(_row(1, "r", "full", "baseline", source="-2.49214", **margin))         == [MARGIN_REMINDER]
    assert reminders(_row(1, "r", "full", "baseline", source="0.453", **margin)) == []
    assert reminders(_row(1, "r", "full", "baseline", source="", **margin)) == []


def _doubt_file(tmp_path, labeled, doubts, extra_notes=()):
    """`labeled` rows with verdicts (the first `doubts` carry a doubt note),
    then one unlabeled row per extra note."""
    rows = []
    for i in range(labeled):
        r = _row(i + 1, "j4cnp", "full", "baseline")
        r["verdict"] = VERDICTS[i % len(VERDICTS)]
        r["note"] = "doubt: which period?" if i < doubts else ""
        rows.append(r)
    for j, note in enumerate(extra_notes, labeled + 1):
        r = _row(j, "j4cnp", "full", "baseline")
        r["note"] = note
        rows.append(r)
    rows.append(_row(len(rows) + 1, "j4cnp", "full", "baseline"))
    path = tmp_path / "adjudication.csv"
    _write(path, rows)
    return AdjudicationFile(path)


def _progress(af):
    out = io.StringIO()
    show(af, af.first_unlabeled(), out)
    return out.getvalue()


def test_doubt_counter_on_progress_line(tmp_path):
    text = _progress(_doubt_file(tmp_path, 12, 1))
    assert "labeled 12/13   doubt notes: 1/12" in text
    assert "rule 8" not in text  # under 20 labeled: never warns


def test_doubt_warning_only_above_five_percent_of_at_least_twenty(tmp_path):
    assert "rule 8" not in _progress(_doubt_file(tmp_path, 19, 3))  # 15.8%, < 20
    assert "rule 8" not in _progress(_doubt_file(tmp_path, 20, 1))  # 5.0%, not above
    warned = _progress(_doubt_file(tmp_path, 20, 2))                 # 10%
    assert warned.count("rule 8") == 1
    assert "doubt notes: 2/20" in warned


def test_doubt_counts_labeled_doubt_notes_only(tmp_path):
    af = _doubt_file(tmp_path, 20, 0, extra_notes=["doubt: unlabeled row"])
    af.rows[0]["note"] = "rounding? no doubt: here"   # doubt: not at a start
    af.rows[1]["note"] = "checked 10-K | Doubt: FY24 or FY25"
    af.rows[2]["note"] = "  doubt:leading space"
    assert af.doubt_count() == 2
    # Verdicts never enter the count.
    for r in af.rows:
        if r["verdict"]:
            r["verdict"] = "FALSE_POSITIVE"
    assert af.doubt_count() == 2


def test_highlight_marks_every_occurrence():
    mark = lambda s: f"[{s}]"  # noqa: E731
    assert highlight("$1.2 then $1.2", "$1.2", mark) == "[$1.2] then [$1.2]"
    assert highlight("nothing here", "$9", mark) == "nothing here"


def test_backtest_regeneration_keeps_notes(tmp_path):
    path = tmp_path / "adjudication.csv"
    old = _row(1, "j4cnp", "full", "baseline")
    old.update(verdict="TRUE_ERROR", note="checked the 10-K")
    _write(path, [old])
    fresh = _row(9, "j4cnp", "full", "baseline")
    assert _merge_verdicts([fresh], path) == 1
    assert fresh["verdict"] == "TRUE_ERROR"
    assert fresh["note"] == "checked the 10-K"
