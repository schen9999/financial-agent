"""Query-time TOC-listing filter (sec_common.is_toc_listing_chunk) — drops
listing chunks, keeps genuine Item 1A prose even with page-header furniture
or legitimately risky vocabulary ('indenture')."""
from agent.tools.sec_common import is_toc_listing_chunk

MSFT_TOC = (
    "PART I Item 1. Business 3 Item 1A. Risk Factors 14 Item 1B. Unresolved "
    "Staff Comments 29 Item 1C. Cybersecurity 29 Item 2. Properties 31 "
    "Item 3. Legal Proceedings 31 Item 4. Mine Safety Disclosures 31 "
)

SANA_TOC = (
    "Item 1. Business 1 Item 1A. Risk Factors 70 Item 1B. Unresolved Staff "
    "Comments 144 Item 1C. Cybersecurity 144 Item 2. Properties 145 "
    "Item 3. Legal Proceedings 145 "
)

GENUINE_WITH_FURNITURE = (
    "references to our websites are intended to be inactive textual "
    "references only. 8. Table of Contents Alphabet Inc. ITEM 1A. RISK "
    "FACTORS Our operations and financial results are subject to various "
    "risks and uncertainties, including those described below, that could "
    "adversely affect our business, financial condition, results of "
    "operations, cash flows, and the trading price of our stock. " * 3
)

UPST_INDENTURE_PROSE = (
    "We sell loans to special purpose entities, which issue notes or "
    "certificates pursuant to indentures and trust agreements. We also "
    "finance certain loans on our balance sheet through warehouse credit "
    "facilities, and adverse developments in securitization markets could "
    "materially affect our liquidity and results of operations. " * 4
)


def test_msft_shaped_toc_dropped():
    assert is_toc_listing_chunk(MSFT_TOC) is True


def test_sana_shaped_toc_dropped():
    assert is_toc_listing_chunk(SANA_TOC) is True


def test_genuine_prose_with_page_header_furniture_kept():
    assert is_toc_listing_chunk(GENUINE_WITH_FURNITURE) is False


def test_upst_indenture_prose_kept():
    assert is_toc_listing_chunk(UPST_INDENTURE_PROSE) is False


def test_single_incidental_item_reference_kept():
    prose = ("As described in Item 1A, competitive pressure intensified in "
             "2026 and our margins declined 3 points. Pricing actions only "
             "partially offset input-cost inflation, and management expects "
             "continued pressure on gross margin through the first half of "
             "the coming fiscal year as inventory purchased at peak freight "
             "rates sells through. Customer concentration remains high.")
    assert is_toc_listing_chunk(prose) is False
