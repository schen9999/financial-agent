"""Shared SEC EDGAR helpers used by both the direct filing tool (sec.py) and the
RAG retrieval path (rag.py): the required User-Agent and the front-matter
skipping that gets past cover-page / table-of-contents boilerplate.

Keeping these in one place avoids drift between the two SEC code paths.
"""
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
    """Strip HTML tags and collapse whitespace from raw filing markup."""
    clean = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", clean).strip()


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
    for marker in (r"item\s*1a", r"item\s*7\b"):
        start = _section_anchor(body, marker)
        if start is not None:
            return body[start:start + window]
    return body[:window]
