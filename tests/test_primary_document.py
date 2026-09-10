"""Primary-document resolution (sec_common) — the fix for the iXBRL
exhibit-fetch defect: /ix?doc= wrapped index links were missed by the href
scrape, so the fallback fetched Exhibit 4.x instead of the 10-K body."""
from agent.tools.sec_common import (primary_document_url, scrape_document_url,
                                    unwrap_ixbrl)

# AAPL-shaped iXBRL index page: main doc only via /ix?doc=, exhibits plain.
AAPL_INDEX = """
<a href="/ix?doc=/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm">10-K</a>
<a href="/Archives/edgar/data/320193/000032019325000079/a10-kexhibit4109272025.htm">EX-4.1</a>
<a href="/Archives/edgar/data/320193/000032019325000079/a10-kexhibit31109272025.htm">EX-31.1</a>
"""

# Plain-HTML filer: main document linked directly.
PLAIN_INDEX = """
<a href="/Archives/edgar/data/999999/000099999925000001/annualreport2025.htm">10-K</a>
<a href="/Archives/edgar/data/999999/000099999925000001/exh991.htm">EX-99.1</a>
"""


def test_primary_document_url_plain_filename():
    url = primary_document_url("0000320193", "0000320193-25-000079", "aapl-20250927.htm")
    assert url == ("https://www.sec.gov/Archives/edgar/data/320193/"
                   "000032019325000079/aapl-20250927.htm")


def test_primary_document_url_unwraps_ixbrl_wrapper():
    wrapped = "/ix?doc=/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm"
    url = primary_document_url("320193", "0000320193-25-000079", wrapped)
    assert url == ("https://www.sec.gov/Archives/edgar/data/320193/"
                   "000032019325000079/aapl-20250927.htm")
    assert "ix?doc" not in url


def test_primary_document_absent_returns_none_for_fallback():
    assert primary_document_url("320193", "0000320193-25-000079", None) is None
    assert primary_document_url("320193", "0000320193-25-000079", "  ") is None


def test_scrape_picks_ixbrl_main_doc_not_exhibit():
    url = scrape_document_url(AAPL_INDEX)
    assert url.endswith("aapl-20250927.htm")
    assert "exhibit" not in url and "ix?doc" not in url


def test_scrape_plain_html_filer():
    assert scrape_document_url(PLAIN_INDEX).endswith("annualreport2025.htm")


def test_scrape_exhibits_only_degrades_to_first():
    exhibits_only = '<a href="/Archives/edgar/data/1/000000000000000001/a10-kexhibit41.htm">x</a>'
    assert scrape_document_url(exhibits_only).endswith("a10-kexhibit41.htm")
    assert scrape_document_url("<html>no links</html>") is None


def test_unwrap_passthrough():
    assert unwrap_ixbrl("plain.htm") == "plain.htm"
