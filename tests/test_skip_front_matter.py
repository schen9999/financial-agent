"""skip_front_matter must anchor on the real Item 1A section, not the
table-of-contents entry — the bug that indexed TOC + exhibit boilerplate
(RSU agreements, indentures, bonus plans) instead of risk-factor text."""
from agent.tools.sec_common import _section_anchor, skip_front_matter

COVER = "UNITED STATES SECURITIES AND EXCHANGE COMMISSION FORM 10-K " * 60  # ~3.5k chars
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
FILING = COVER + TOC + BUSINESS + RISK_SECTION


def test_anchor_skips_toc_hit():
    body = FILING[3000:]
    start = _section_anchor(body, r"item\s*1a")
    assert start is not None
    assert body[start:start + 80].startswith("Item 1A. Risk Factors. The following")


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
