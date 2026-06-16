import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from display_utils import strip_source_citations, strip_source_citations_stream


def test_removes_bare_field_citation():
    out = strip_source_citations("Apple is a leader `market_cap: 4342023192576.0` in tech.")
    assert "`" not in out
    assert "market_cap" not in out
    assert out == "Apple is a leader in tech."


def test_removes_parenthesized_citation():
    out = strip_source_citations(
        "It trades at a premium (`market_cap: 4342023192576.0`) valuation."
    )
    assert "`" not in out and "market_cap" not in out
    assert "()" not in out
    assert out == "It trades at a premium valuation."


def test_removes_multiple_citations_and_tidies_punctuation():
    text = ("NVIDIA shows strength `revenue: 253491003392.0` , with margins "
            "`profit_margin: 0.62966` .")
    out = strip_source_citations(text)
    assert "`" not in out
    assert "revenue" not in out and "profit_margin" not in out
    assert " ," not in out and " ." not in out


def test_removes_inline_code_span_and_content():
    # The whole inline-code span (delimiters + content) is removed, not unwrapped.
    out = strip_source_citations("The ticker `AAPL` is notable.")
    assert "`" not in out
    assert out == "The ticker is notable."


def test_removes_backtick_span_with_inner_markdown():
    # The real bug: citation spans whose content is itself markdown. Removing the
    # whole span prevents the inner **bold** from leaking into the rendered prose.
    text = ("commanding a market capitalization of `**$5.15 trillion**` and "
            "robust revenue of `**$253.5 billion**`.")
    out = strip_source_citations(text)
    assert "`" not in out
    assert "$5.15 trillion" not in out and "$253.5 billion" not in out
    assert "**" not in out  # no stray bold markers left behind
    assert out == "commanding a market capitalization of and robust revenue of."


def test_preserves_legit_bold_but_removes_backtick_bold():
    # Legitimate **bold** (risk headers) is untouched; only backtick-wrapped
    # content is stripped.
    text = "- **Competition** is intense `competitor_count: 5`."
    out = strip_source_citations(text)
    assert "**Competition**" in out      # legit bold preserved
    assert "competitor_count" not in out  # backtick citation removed
    assert "`" not in out


def test_leaves_clean_prose_untouched():
    prose = ("## Apple Inc. (AAPL)\n\n### Executive Summary\nApple trades at "
             "$295.63 with a 27.2% margin.\n\n- A risk bullet.")
    assert strip_source_citations(prose) == prose


def test_preserves_markdown_structure():
    md = "### Risk Factors\n- **Competition** is intense.\n- Margins matter."
    assert strip_source_citations(md) == md


def test_empty_and_none():
    assert strip_source_citations("") == ""
    assert strip_source_citations(None) is None


# ── streaming wrapper ─────────────────────────────────────────────────────────

def _run_stream(chunks):
    return "".join(strip_source_citations_stream(iter(chunks)))


def test_stream_matches_whole_text_strip():
    full = "Apple leads `market_cap: 4342023192576.0` the market today."
    # however the text is chunked, the streamed result strips the citation
    assert "market_cap" not in _run_stream([full])
    assert "`" not in _run_stream([full])


def test_stream_citation_split_across_chunks():
    # the citation is split mid-span across token boundaries
    chunks = ["Apple leads `market", "_cap: 4342023", "192576.0` the market."]
    out = _run_stream(chunks)
    assert "`" not in out
    assert "market_cap" not in out
    assert "Apple leads" in out and "the market." in out


def test_stream_backtick_split_across_chunks():
    # opening and closing backticks arrive in different chunks
    chunks = ["premium (`", "pe_ratio: 35.8", "`) valuation"]
    out = _run_stream(chunks)
    assert "`" not in out and "pe_ratio" not in out
    assert "premium" in out and "valuation" in out


def test_stream_clean_prose_passthrough():
    chunks = ["### Summary\n", "Apple trades at $295.63 ", "with strong margins."]
    assert _run_stream(chunks) == "### Summary\nApple trades at $295.63 with strong margins."
