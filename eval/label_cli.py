#!/usr/bin/env python3
"""Terminal labeler for a judge-validation CSV (blind to judge labels).

Walks the rows whose human_label is blank, shows the row's position,
ticker, the audited section the claim sits in, the claim, then the context
a page at a time, and takes one keystroke-word per row:

  s / u / i   label SUPPORTED / UNSUPPORTED / INFERENCE
  b           go back and relabel the previous row answered this session
  k           skip (stays blank; the next session comes back to it)
  q           quit (every answer is already saved)
  /term       find every match of term in the context (case-insensitive):
              each is shown with its line number and two lines either
              side, the term highlighted; paging then resumes

At a "more" prompt, Enter shows the next page; a label key answers
without paging further.

A row's existing label is never shown, including when going back with b:
relabeling is as blind as the first pass.

Blinding: this tool never opens a *_key.csv and refuses one passed as
--csv. The section shown is found in the row's own context (the audited
text block), not taken from any judge output.

Saving: after every answer the file is rewritten atomically (temp file in
the same directory, then os.replace), UTF-8. Only the human_label field of
the answered row changes; every other byte, quoting and line endings
included, is kept exactly, because the file is edited by byte span rather
than re-serialized. Restarting resumes at the first blank row.

Usage:
  python eval/label_cli.py
  python eval/label_cli.py --csv eval/judge_validation/holdout_sample.csv
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

REPO = Path(__file__).resolve().parents[1]
DEFAULT_CSV = REPO / "eval" / "judge_validation" / "calibration_batch.csv"
KEYS = {"s": "SUPPORTED", "u": "UNSUPPORTED", "i": "INFERENCE"}
LABEL_COL = "human_label"


def record_spans(text: str) -> list[list[tuple[int, int]]]:
    """Per CSV record, the (start, end) span of each field in `text`.
    Quoted fields may contain commas and newlines; a record ends at a
    newline (or \\r\\n) outside quotes. Spans cover the raw field bytes,
    quotes included, so a field can be replaced without touching the rest."""
    records, fields = [], []
    start, i, n, quoted = 0, 0, len(text), False
    while i < n:
        ch = text[i]
        if quoted:
            if ch == '"':
                if i + 1 < n and text[i + 1] == '"':
                    i += 1
                else:
                    quoted = False
        elif ch == '"':
            quoted = True
        elif ch == ",":
            fields.append((start, i))
            start = i + 1
        elif ch in "\r\n":
            end = i
            fields.append((start, end))
            records.append(fields)
            fields = []
            if ch == "\r" and i + 1 < n and text[i + 1] == "\n":
                i += 1
            start = i + 1
        i += 1
    if start < n or fields:
        fields.append((start, n))
        records.append(fields)
    return records


def field_value(raw: str) -> str:
    return next(csv.reader(io.StringIO(raw)))[0] if raw else ""


class LabelFile:
    """A CSV edited in place by field span; only the label column changes."""

    def __init__(self, path: Path):
        if path.name.endswith("_key.csv"):
            raise SystemExit(f"refusing to open {path.name}: labeling must not read a key file")
        self.path = path
        self.text = path.read_bytes().decode("utf-8")
        spans = record_spans(self.text)
        header = [field_value(self.text[a:b]) for a, b in spans[0]]
        header[0] = header[0].lstrip("﻿")
        if LABEL_COL not in header:
            raise SystemExit(f"{path.name} has no {LABEL_COL} column")
        self.header = header
        self.col = header.index(LABEL_COL)
        self.rows = [r for r in spans[1:] if not (len(r) == 1 and r[0][0] == r[0][1])]

    def row(self, k: int) -> dict:
        fields = [field_value(self.text[a:b]) for a, b in self.rows[k]]
        return dict(zip(self.header, fields))

    def label(self, k: int) -> str:
        a, b = self.rows[k][self.col]
        return field_value(self.text[a:b]).strip()

    def set_label(self, k: int, value: str) -> None:
        a, b = self.rows[k][self.col]
        self.text = self.text[:a] + value + self.text[b:]
        self.rows = [r for r in record_spans(self.text)[1:]
                     if not (len(r) == 1 and r[0][0] == r[0][1])]
        self._save()

    def _save(self) -> None:
        fd, tmp = tempfile.mkstemp(prefix=f".{self.path.name}.", dir=self.path.parent)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(self.text.encode("utf-8"))
            shutil.copymode(self.path, tmp)
            os.replace(tmp, self.path)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    def first_blank(self, after: int = -1) -> int | None:
        return next((k for k in range(after + 1, len(self.rows)) if not self.label(k)), None)

    def labeled_count(self) -> int:
        return sum(1 for k in range(len(self.rows)) if self.label(k))


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace('"', "")).strip().lower()


def locate_section(claim: str, context: str) -> str:
    """Which audited heading (### ...) the claim text appears under, from the
    row's own context only; 'not located' when the claim is paraphrased."""
    m = re.search(r"=== AUDITED TEXT[^\n]*===\n(.*?)(?=\n=== |\Z)", context, re.S)
    if not m:
        return "not located"
    needle = _norm(claim)
    for head, body in re.findall(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", m.group(1), re.M | re.S):
        if needle and needle in _norm(body):
            return head.strip()
    return "not located"


def ask(prompt: str, inp, out) -> str:
    out.write(prompt)
    out.flush()
    return inp().strip().lower()


def _highlighter(out):
    if getattr(out, "isatty", lambda: False)():
        return lambda s: f"\033[7m{s}\033[0m"
    return lambda s: f">>{s}<<"


def search(lines: list[str], term: str, out, width: int = 2) -> int:
    """Write every line matching `term` (case-insensitive) with `width`
    lines of context, the match highlighted. Returns the match count."""
    pat = re.compile(re.escape(term), re.I)
    hits = [n for n, line in enumerate(lines) if pat.search(line)]
    if not hits:
        out.write(f"no match for '{term}'\n")
        return 0
    mark = _highlighter(out)
    out.write(f"{len(hits)} line(s) match '{term}':\n")
    for h in hits:
        out.write(f"--- line {h + 1}/{len(lines)}\n")
        for n in range(max(0, h - width), min(len(lines), h + width + 1)):
            text = pat.sub(lambda m: mark(m.group(0)), lines[n]) if n == h else lines[n]
            out.write(f"{n + 1:>5}{'>' if n == h else ' '} {text}\n")
    return len(hits)


def show_and_ask(lf: LabelFile, k: int, page: int, inp, out) -> str:
    r = lf.row(k)
    done = lf.labeled_count()
    out.write("\n" + "=" * 78 + "\n")
    out.write(f"row {k + 1}/{len(lf.rows)} (id {r.get('id', '?')})   "
              f"labeled {done}/{len(lf.rows)}\n")
    out.write(f"ticker : {r.get('ticker', '?')}\n")
    out.write(f"section: {locate_section(r.get('claim', ''), r.get('context', ''))}\n")
    out.write(f"claim  : {r.get('claim', '')}\n")
    out.write("-" * 78 + "\n")
    lines = r.get("context", "").splitlines()
    pos, show = 0, True
    while True:
        if show:
            out.write("\n".join(lines[pos:pos + page]) + "\n")
            pos += page
            show = False
        if pos < len(lines):
            a = ask(f"-- more ({pos}/{len(lines)} lines): Enter = next page, "
                    f"/term = search, s/u/i/b/k/q -- ", inp, out)
            if a == "":
                show = True
                continue
        else:
            a = ask("label [s]upported [u]nsupported [i]nference, "
                    "[b]ack, s[k]ip, [q]uit, /term search: ", inp, out)
        if a.startswith("/"):
            if a[1:].strip():
                search(lines, a[1:].strip(), out)
            else:
                out.write("usage: /term\n")
            continue
        if a in KEYS or a in ("b", "k", "q"):
            return a
        out.write("unrecognized; use s, u, i, b, k, q or /term\n")


def run(path: Path, page: int = 40, inp=input, out=sys.stdout) -> None:
    lf = LabelFile(path)
    history: list[int] = []  # rows answered or skipped this session
    k = lf.first_blank()
    if k is None:
        out.write(f"all {len(lf.rows)} rows labeled in {path.name}\n")
        return
    while k is not None:
        a = show_and_ask(lf, k, page, inp, out)
        if a == "q":
            break
        if a == "b":
            if not history:
                out.write("nothing to go back to this session\n")
                continue
            k = history.pop()
            continue
        if a in KEYS:
            lf.set_label(k, KEYS[a])
        history.append(k)
        k = lf.first_blank(after=max(history))
    left = len(lf.rows) - lf.labeled_count()
    out.write(f"\nsaved {path.name}: {lf.labeled_count()}/{len(lf.rows)} labeled, "
              f"{left} blank\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    ap.add_argument("--page", type=int, default=40, help="context lines per page")
    args = ap.parse_args(argv)
    # Contexts carry characters a Windows cp1252 console cannot encode (e.g.
    # U+2212); show a replacement rather than crash mid-row.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        run(Path(args.csv), args.page)
    except (KeyboardInterrupt, EOFError):
        print("\nquit (every answer is already saved)")


if __name__ == "__main__":
    main()
