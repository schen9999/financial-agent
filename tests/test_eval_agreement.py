"""eval/label.py parsing + sampling and eval/agreement.py metrics."""
import pytest

from eval.agreement import cohens_kappa, precision_recall_unsupported
from eval.label import parse_claims, parse_findings_file, stratified_sample

FINDINGS_MD = """# AAPL — baseline

## Retrieved source context

STOCK DATA: {"pe_ratio": 35.4}

## Audited (Exec Summary + Outlook)

### Executive Summary
Apple trades at a P/E of 35.4.

## Judge findings

CLAIM: "P/E of 35.4"
LABEL: SUPPORTED
REASON: pe_ratio 35.4 appears in the stock data.

**CLAIM:** "Revenue will grow 12% next year"
**LABEL:** UNSUPPORTED
**REASON:** No growth forecast appears in the context.
"""


EXTENDED_FINDINGS_MD = """# AAPL — baseline

## Metadata

ticker: AAPL
arm: baseline
judge_prompt_version: v2
context_sha256: abc123

## Retrieved source context

STOCK DATA: {"pe_ratio": 35.4}

## Pre-written sections (judge input)

### Valuation
The stock trades at a premium multiple.

## Audited (Exec Summary + Outlook)

### Executive Summary
Apple trades at a P/E of 35.4.

## Judge findings

CLAIM: "P/E of 35.4"
LABEL: SUPPORTED
REASON: pe_ratio 35.4 appears in the stock data.
"""


def test_parse_findings_file_sections():
    parsed = parse_findings_file(FINDINGS_MD)
    assert parsed and "pe_ratio" in parsed["context"]
    assert "Executive Summary" in parsed["audited"]
    assert "CLAIM" in parsed["findings"]
    assert "metadata" not in parsed and "section_block" not in parsed


def test_parse_findings_file_extended_format():
    parsed = parse_findings_file(EXTENDED_FINDINGS_MD)
    assert parsed["metadata"]["judge_prompt_version"] == "v2"
    assert parsed["metadata"]["context_sha256"] == "abc123"
    assert "premium multiple" in parsed["section_block"]
    # Extended blocks must not leak into the original three.
    assert "premium multiple" not in parsed["context"]
    assert "judge_prompt_version" not in parsed["context"]
    assert "pe_ratio" in parsed["context"]
    assert "Executive Summary" in parsed["audited"]


def test_render_findings_md_round_trips():
    import hashlib

    from eval.label import render_findings_md

    ctx = 'STOCK DATA: {"pe_ratio": 35.4}'
    text = render_findings_md(
        "AAPL", "baseline", "v2", ctx, "### Valuation\nPremium multiple.",
        "### Executive Summary\nApple trades at a P/E of 35.4.",
        'CLAIM: "P/E of 35.4"\nLABEL: SUPPORTED\nREASON: in stock data.')
    parsed = parse_findings_file(text)
    assert parsed["metadata"]["ticker"] == "AAPL"
    assert parsed["metadata"]["arm"] == "baseline"
    assert parsed["metadata"]["judge_prompt_version"] == "v2"
    assert parsed["metadata"]["context_sha256"] == (
        hashlib.sha256(ctx.encode()).hexdigest())
    assert parsed["context"] == ctx
    assert "Premium multiple" in parsed["section_block"]
    assert parse_claims(parsed["findings"])[0]["label"] == "SUPPORTED"


def test_parse_claims_plain_and_bold():
    claims = parse_claims(parse_findings_file(FINDINGS_MD)["findings"])
    assert [c["label"] for c in claims] == ["SUPPORTED", "UNSUPPORTED"]
    assert claims[0]["claim"] == "P/E of 35.4"
    assert "growth forecast" in claims[1]["reason"]


def test_stratified_sample_keeps_scarce_strata_and_is_deterministic():
    rows = ([{"label": "SUPPORTED", "i": i} for i in range(40)]
            + [{"label": "UNSUPPORTED", "i": i} for i in range(3)]
            + [{"label": "INFERENCE", "i": i} for i in range(10)])
    s1 = stratified_sample(rows, 20, seed=7)
    s2 = stratified_sample(rows, 20, seed=7)
    assert s1 == s2 and len(s1) == 20
    assert sum(1 for r in s1 if r["label"] == "UNSUPPORTED") == 3  # all kept
    assert sum(1 for r in s1 if r["label"] == "INFERENCE") == 10  # all kept


def test_cohens_kappa_known_value():
    # po=0.75; marginals -> pe=0.5; kappa = 0.5
    pairs = [("SUPPORTED", "SUPPORTED"), ("SUPPORTED", "SUPPORTED"),
             ("UNSUPPORTED", "UNSUPPORTED"), ("UNSUPPORTED", "SUPPORTED")]
    assert cohens_kappa(pairs) == pytest.approx(0.5)


def test_cohens_kappa_perfect_and_empty():
    assert cohens_kappa([("SUPPORTED", "SUPPORTED")] * 5) == 1.0
    with pytest.raises(ValueError):
        cohens_kappa([])


def test_precision_recall_unsupported_counts():
    pairs = [("UNSUPPORTED", "UNSUPPORTED"),  # tp
             ("UNSUPPORTED", "SUPPORTED"),    # fp
             ("SUPPORTED", "UNSUPPORTED"),    # fn
             ("SUPPORTED", "SUPPORTED")]
    pr = precision_recall_unsupported(pairs)
    assert (pr["tp"], pr["fp"], pr["fn"]) == (1, 1, 1)
    assert pr["precision_n"] == 2 and pr["recall_n"] == 2
