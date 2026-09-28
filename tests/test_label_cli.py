"""eval/label_cli.py: label, quit, resume; the CSV changes only in human_label."""
import csv
import io

import pytest

from eval.label_cli import LabelFile, locate_section, record_spans, run

CONTEXT = ('=== RETRIEVED SOURCE CONTEXT ===\nrevenue, "quoted" $1,000\n'
           + "\n".join(f"line {n}" for n in range(12))
           + "\n\n=== AUDITED TEXT (Exec Summary + Outlook) ===\n"
             "### Executive Summary\nRevenue was $1.0 billion.\n"
             "### Outlook\nMargins may compress.")


def _write(path, rows, newline="\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(["id", "ticker", "claim", "context", "human_label"])
    w.writerows(rows)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def _feed(answers):
    it = iter(answers)
    return lambda: next(it)


def _strip_labels(data: bytes) -> list[list[str]]:
    rows = list(csv.reader(io.StringIO(data.decode("utf-8"), newline="")))
    return [r[:-1] for r in rows]


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_round_trip_label_quit_resume(tmp_path, newline):
    path = tmp_path / "batch.csv"
    rows = [[0, "AAA", "Revenue was $1.0 billion", CONTEXT, ""],
            [1, "BBB", 'claim with "quotes", commas', CONTEXT, ""],
            [2, "CCC", "Margins may compress", CONTEXT, ""],
            [3, "DDD", "plain", "short context", ""]]
    _write(path, rows, newline)
    before = path.read_bytes()

    out = io.StringIO()
    # row 0: page once, then s; row 1: u; back to row 1, relabel i; row 2: q
    run(path, page=5, inp=_feed(["", "s", "u", "b", "i", "q"]), out=out)
    mid = path.read_bytes()
    lf = LabelFile(path)
    assert [lf.label(k) for k in range(4)] == ["SUPPORTED", "INFERENCE", "", ""]
    assert "row 1/4" in out.getvalue() and "section: Executive Summary" in out.getvalue()

    # resume starts at the first blank row (row 2)
    out2 = io.StringIO()
    run(path, page=100, inp=_feed(["k", "u"]), out=out2)
    assert "row 3/4" in out2.getvalue().split("=" * 78)[1]
    after = path.read_bytes()
    lf = LabelFile(path)
    assert [lf.label(k) for k in range(4)] == ["SUPPORTED", "INFERENCE", "", "UNSUPPORTED"]

    # every byte outside human_label is unchanged: blanking the labels again
    # restores the original file exactly
    for data in (mid, after):
        assert _strip_labels(data) == _strip_labels(before)
    for k in range(4):
        lf.set_label(k, "")
    assert path.read_bytes() == before


def test_refuses_key_file(tmp_path):
    key = tmp_path / "calibration_batch_key.csv"
    key.write_text("id,judge_label\n0,SUPPORTED\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        LabelFile(key)


def test_record_spans_handles_quoted_newlines():
    text = 'a,b\n1,"x\ny, ""z"""\n'
    spans = record_spans(text)
    assert len(spans) == 2
    a, b = spans[1][1]
    assert text[a:b] == '"x\ny, ""z"""'


def test_locate_section_from_context_only():
    assert locate_section("Margins may compress", CONTEXT) == "Outlook"
    assert locate_section("not in the text", CONTEXT) == "not located"


def test_search_highlights_every_match_with_line_numbers():
    from eval.label_cli import search
    out = io.StringIO()
    lines = ["alpha", "revenue up", "beta", "gamma", "Revenue down", "delta"]
    assert search(lines, "revenue", out) == 2
    text = out.getvalue()
    assert "2 line(s) match" in text
    assert "    2> >>revenue<< up" in text and "    5> >>Revenue<< down" in text
    assert search(lines, "missing", io.StringIO()) == 0


def test_search_then_label_and_back_never_shows_existing_label(tmp_path):
    path = tmp_path / "batch.csv"
    _write(path, [[0, "AAA", "Revenue was $1.0 billion", CONTEXT, ""],
                  [1, "BBB", "plain", "short context", ""]])
    out = io.StringIO()
    run(path, page=100, inp=_feed(["/revenue", "u", "b", "s", "q"]), out=out)
    text = out.getvalue()
    assert ">>revenue<<" in text
    assert "UNSUPPORTED" not in text and "SUPPORTED" not in text
    assert LabelFile(path).label(0) == "SUPPORTED"
