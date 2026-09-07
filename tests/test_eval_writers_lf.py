"""Eval context snapshots are named by the sha256 of their bytes.

eval/parse_run_log.py hashes the context *string* and writes it to
<contexts_dir>/<sha>.txt. Without newline="\\n" the default text-mode write on
Windows emits CRLF, so the bytes on disk no longer hash to the filename (every
context file committed before 2026-09-07 was in that state). This drives the
real writer and checks the on-disk bytes.
"""
import hashlib

from eval.parse_run_log import rows_from_findings_dir

FINDINGS_MD = """# AAPL — baseline

## Metadata

ticker: AAPL
arm: baseline
judge_prompt_version: v2

## Retrieved source context

STOCK DATA:
{
  "ticker": "AAPL",
  "pe_ratio": 35.4
}

NEWS ARTICLES:
[]

## Audited (Exec Summary + Outlook)

### Executive Summary
Apple trades at a P/E of 35.4.

## Judge findings

CLAIM: "P/E of 35.4"
LABEL: SUPPORTED
REASON: pe_ratio 35.4 appears in the stock data.
"""


def test_context_snapshot_bytes_hash_to_filename(tmp_path):
    findings_dir = tmp_path / "findings"
    findings_dir.mkdir()
    (findings_dir / "AAPL_baseline.md").write_text(
        FINDINGS_MD, encoding="utf-8", newline="\n")
    contexts_dir = tmp_path / "contexts"

    rows = rows_from_findings_dir("test-run", findings_dir, {}, contexts_dir)

    files = list(contexts_dir.glob("*.txt"))
    assert len(files) == 1
    path = files[0]
    raw = path.read_bytes()
    # The context spans several lines, so a CRLF translation would show here.
    assert b"\n" in raw
    assert b"\r" not in raw
    assert hashlib.sha256(raw).hexdigest() == path.stem
    assert rows and all(r["context_sha256"] == path.stem for r in rows)
