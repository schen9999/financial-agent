"""Shared SEC EDGAR helpers used by both the direct filing tool (sec.py) and the
RAG retrieval path (rag.py): the required User-Agent and the front-matter
skipping that gets past cover-page / table-of-contents boilerplate.

Keeping these in one place avoids drift between the two SEC code paths.
"""
import html as _html
import re

import requests

# SEC fair-access policy requires a real contact in the User-Agent so EDGAR can
# reach the operator about automated traffic; a fake address can get the client
# rate-limited or blocked. See https://www.sec.gov/os/webmaster-faq#developers.
# TODO: replace the name/email below with a real contact before deploying.
SEC_USER_AGENT = "FinancialAgent your-name your-email@example.com"

# Default timeout (seconds) for every SEC HTTP request.
SEC_TIMEOUT = 15

# ticker -> zero-padded CIK, from SEC's authoritative mapping file. Fetched
# once per process on first use; None means "not fetched yet / fetch failed,
# retry next call" (a failed fetch is never cached as an empty map).
_cik_map: dict[str, str] | None = None


def lookup_cik(ticker: str) -> str | None:
    """CIK for a ticker via https://www.sec.gov/files/company_tickers.json.

    This is the documented, authoritative mapping — used as the PRIMARY
    lookup because scraping browse-edgar HTML proved flaky under EDGAR
    throttling (MSFT lookups failed during the 2026-08-24 eval run, which is
    also why MSFT was the skipped ticker in the 9-ticker balanced A/B).
    Returns None when the ticker is unknown or the mapping cannot be fetched;
    callers keep their scrape fallbacks for that case.
    """
    global _cik_map
    if _cik_map is None:
        try:
            resp = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers={"User-Agent": SEC_USER_AGENT},
                timeout=SEC_TIMEOUT,
            )
            resp.raise_for_status()
            _cik_map = {
                v["ticker"].upper(): str(v["cik_str"]).zfill(10)
                for v in resp.json().values()
            }
        except Exception:
            return None
    return _cik_map.get(ticker.strip().upper())


def clean_filing_html(html: str) -> str:
    """Strip HTML tags, decode entities, and collapse whitespace.

    Entity decoding matters: filings render headings like
    "Item 1A.&#160;&#160;Risk Factors" — without unescaping, the nbsp
    entities break section-heading detection (AAPL's Item 1A was missed for
    exactly this reason, 2026-09-04) and every downstream consumer reads
    &#8220;-style entity soup instead of text."""
    clean = re.sub(r"<[^>]+>", " ", html)
    clean = _html.unescape(clean)
    return re.sub(r"\s+", " ", clean).strip()


# TOC listing entry: "Item 1A. Risk Factors 14" — an item title followed by a
# page number. Distinct from prose ("Item 1A. Risk Factors The following
# summarizes...") and from page-header furniture ("8. Table of Contents
# Alphabet Inc. ITEM 1A. RISK FACTORS Our operations...").
_TOC_ENTRY = re.compile(r"item\s*\d{1,2}[abc]?\.?\s+[A-Za-z][^.0-9]{2,60}?\s+\d{1,3}\b", re.I)


def is_toc_listing_chunk(text: str) -> bool:
    """True when a retrieved chunk reads as a table-of-contents listing
    rather than filing prose — applied at QUERY time (no reindex needed) so
    windows that span a filer's TOC region (MSFT, SANA, 2026-09-04) don't
    feed listing text to generation. Two signatures:
    (a) three or more title+page-number entries, or
    (b) a dense run of "Item N" references with little text between them.
    A single incidental match (prose citing one item + a nearby number)
    never trips it, so genuine Item 1A text — including chunks carrying
    page-header furniture or words like "indenture" — is kept."""
    if len(_TOC_ENTRY.findall(text)) >= 3:
        return True
    item_refs = len(re.findall(r"item\s*\d", text, re.I))
    return item_refs >= 5 and len(text) / item_refs < 120


def unwrap_ixbrl(path_or_url: str) -> str:
    """Strip an inline-XBRL viewer wrapper: '/ix?doc=/Archives/...' -> the
    underlying document path. Non-wrapped inputs pass through unchanged."""
    m = re.search(r"ix\?doc=([^&\"]+)", path_or_url)
    return m.group(1) if m else path_or_url


def primary_document_url(cik: str | int, accession_dashed: str,
                         primary_doc: str | None) -> str | None:
    """Primary-document URL from the submissions JSON fields; None when the
    primaryDocument field is missing/empty (caller falls back to scraping).

    Why this is the primary path (2026-09-04): on the EDGAR index page,
    inline-XBRL filers link the main document through /ix?doc=..., which the
    old href scrape missed — the exhibit-name filter then rejected every
    remaining .htm and the fallback fetched Exhibit 4.x (AAPL's "10-K" came
    back as its Bylaws exhibit). The submissions JSON names the real file.
    """
    if not primary_doc or not str(primary_doc).strip():
        return None
    doc = unwrap_ixbrl(str(primary_doc).strip())
    if doc.startswith("/Archives/"):
        return f"https://www.sec.gov{doc}"
    accession = accession_dashed.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"


def scrape_document_url(index_html: str) -> str | None:
    """Fallback: pick the main document from a filing index page's HTML.
    Handles both plain hrefs and /ix?doc= wrapped ones; prefers a
    non-exhibit, non-index file; degrades to the first .htm found."""
    hrefs = re.findall(r'href="((?:/ix\?doc=)?/Archives/edgar/data/[^"]+\.htm)"',
                       index_html)
    unwrapped = [unwrap_ixbrl(h) for h in hrefs]
    for href in unwrapped:
        name = href.lower().split("/")[-1]
        if "index" not in name and "ex" not in name:
            return f"https://www.sec.gov{href}"
    if unwrapped:
        return f"https://www.sec.gov{unwrapped[0]}"
    return None


def _section_anchor(body: str, marker: str) -> int | None:
    """Offset of the marker occurrence that starts the actual SECTION, not its
    table-of-contents or exhibit-index entry.

    Mechanism of the bug this fixes (2026-09-04, judge-validation labeling):
    the first `item 1a` hit in a 10-K is almost always the TOC line, so the
    indexed window carried TOC + adjacent exhibit boilerplate (RSU agreements,
    indentures, bonus plans) and the real Item 1A text never got indexed. A
    TOC/index hit sits in a dense run of other "Item N" references and page
    numbers; a real section heading is followed by prose. Prefer the first
    occurrence whose following text is NOT item-dense; fall back to the first
    occurrence if every hit looks like a listing.
    """
    fallback = None
    for m in re.finditer(marker, body, re.I):
        if fallback is None:
            fallback = m.start()
        tail = body[m.end(): m.end() + 400]
        other_item_refs = len(re.findall(r"item\s*\d", tail, re.I))
        if other_item_refs <= 1:
            return m.start()
    return fallback


def _intra(word: str) -> str:
    """Regex for `word` tolerating one whitespace char between letters —
    matches headings whose words were split across HTML tags ("RIS K")."""
    return r"\s?".join(word)


def skip_front_matter(text: str, window: int, min_len_to_skip: int | None = None) -> str:
    """Return a `window`-sized slice of filing text past the cover-page boilerplate.

    Short filings are returned as-is. For longer ones we first offset past the
    start (the same proportional skip the RAG path has always used) and then, if a
    substantive section marker (Item 1A Risk Factors or Item 7 MD&A) appears in the
    remaining body, anchor on its real section start — not its table-of-contents
    entry (see _section_anchor) — so the slice carries Item 1A/MD&A content
    instead of the cover page, TOC, or exhibit index.
    """
    threshold = window if min_len_to_skip is None else min_len_to_skip
    if len(text) <= threshold:
        return text[:window]

    offset = min(3000, len(text) // 10)
    body = text[offset:]
    # Title-adjacent markers: a bare "item 1a" also matches cross-references
    # ("...as described in Item 1A of this Form 10-K...", which anchored
    # AAPL's window into Item 1 Business). Requiring the section title right
    # after the item number excludes cross-references; TOC entries still
    # match here and are rejected by _section_anchor's tail-density check.
    # Title words tolerate ONE whitespace inside them (_intra): filers split
    # heading words across HTML spans, and tag-stripping turns that into
    # "ITEM 1A. RIS K FACTORS" (MSFT's 10-K, 2026-09-05) — the section's
    # only title-adjacent occurrence, so the anchor fell back to the TOC.
    for marker in (rf"item\s*1a\.?[\s:\u2013\u2014-]*{_intra('risk')}\s*{_intra('factors')}",
                   rf"item\s*7\.?[\s:\u2013\u2014-]*{_intra('management')}"):
        start = _section_anchor(body, marker)
        if start is not None:
            return body[start:start + window]
    return body[:window]
