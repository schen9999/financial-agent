"""skip_front_matter must anchor on the real Item 1A section, not the
table-of-contents entry — the bug that indexed TOC + exhibit boilerplate
(RSU agreements, indentures, bonus plans) instead of risk-factor text."""
from agent.tools.sec_common import _section_anchor, skip_front_matter

COVER = "UNITED STATES SECURITIES AND EXCHANGE COMMISSION FORM 10-K " * 60  # ~3.5k chars
FWD_LOOKING = (
    "Forward-looking statements involve risks and uncertainties, as more fully "
    "described in Item 1A of this Form 10-K under the heading Risk Factors. "
    "The Company assumes no obligation to update forward-looking statements. "
)
TOC = (
    "TABLE OF CONTENTS Item 1. Business 5 Item 1A. Risk Factors 12 "
    "Item 1B. Unresolved Staff Comments 30 Item 2. Properties 31 "
    "Item 7. Management's Discussion and Analysis 45 Item 8. Financial "
    "Statements 60 Exhibit 10.1 Form of RSU Agreement Exhibit 4.2 "
    "Indenture dated 2020 Exhibit 10.5 Executive Bonus Plan "
)
BUSINESS = "Item 1. Business. The company designs products. " * 40
RISK_SECTION = (
    "Item 1A. Risk Factors. The following risk factors could materially "
    "affect our business. Competition in our markets is intense and "
    "customers face many alternatives. " + "Risk prose sentence. " * 400
)
FILING = COVER + FWD_LOOKING + TOC + BUSINESS + RISK_SECTION

TITLE_MARKER = r"item\s*1a\.?[\s:\u2013\u2014-]*risk\s*factors"


def test_anchor_skips_toc_hit_and_cross_reference():
    body = FILING[3000:]
    start = _section_anchor(body, TITLE_MARKER)
    assert start is not None
    assert body[start:start + 80].startswith("Item 1A. Risk Factors. The following")


def test_cross_reference_alone_does_not_match_title_marker():
    import re
    assert re.search(TITLE_MARKER, FWD_LOOKING, re.I) is None


def test_window_carries_risk_prose_not_exhibit_boilerplate():
    out = skip_front_matter(FILING, 15000, min_len_to_skip=5000)
    assert "The following risk factors could materially" in out
    assert "RSU Agreement" not in out
    assert "Indenture" not in out
    assert "Bonus Plan" not in out


def test_falls_back_to_first_hit_when_only_listing_exists():
    text = COVER + TOC + ("no real section here, only prose. " * 600)
    out = skip_front_matter(text, 15000, min_len_to_skip=5000)
    assert len(out) > 0  # degraded but non-empty — old behaviour preserved


def test_short_filings_returned_whole():
    assert skip_front_matter("short filing", 15000, min_len_to_skip=5000) == "short filing"


def test_entity_spaced_heading_anchors_after_cleaning():
    # AAPL-shaped: the real heading uses &#160; entities between the item
    # label and the title; cleaning must decode them so the anchor matches.
    from agent.tools.sec_common import clean_filing_html
    raw = ("<html>" + COVER + FWD_LOOKING + TOC
           + "Item 1A.&#160;&#160;&#160;&#160;Risk Factors The following "
             "summarizes factors that could have a material adverse effect. "
           + "Risk prose sentence. " * 400 + "</html>")
    out = skip_front_matter(clean_filing_html(raw), 15000, min_len_to_skip=5000)
    assert out.startswith("Item 1A. Risk Factors The following summarizes")


def test_split_word_heading_anchors_on_section():
    # MSFT-shaped: the section title's words are split across HTML spans, so
    # after tag-stripping the only title-adjacent heading reads
    # "ITEM 1A. RIS K FACTORS"; the TOC entry is the only intact spelling.
    text = (COVER + FWD_LOOKING + TOC + BUSINESS
            + "PART I Item 1A ITEM 1A. RIS K FACTORS Our operations and "
              "financial results are subject to various risks. "
            + "Risk prose sentence. " * 400)
    out = skip_front_matter(text, 15000, min_len_to_skip=5000)
    assert "Our operations and financial results" in out[:200]
    assert "RSU Agreement" not in out


def test_clean_filing_html_unescapes_entities():
    from agent.tools.sec_common import clean_filing_html
    assert clean_filing_html("A&#160;B &#8220;q&#8221;") == "A B “q”"
