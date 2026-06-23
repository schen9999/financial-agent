"""Shared SEC EDGAR helpers used by both the direct filing tool (sec.py) and the
RAG retrieval path (rag.py): the required User-Agent and the front-matter
skipping that gets past cover-page / table-of-contents boilerplate.

Keeping these in one place avoids drift between the two SEC code paths.
"""
import re

# SEC fair-access policy requires a real contact in the User-Agent so EDGAR can
# reach the operator about automated traffic; a fake address can get the client
# rate-limited or blocked. See https://www.sec.gov/os/webmaster-faq#developers.
# TODO: replace the name/email below with a real contact before deploying.
SEC_USER_AGENT = "FinancialAgent your-name your-email@example.com"

# Default timeout (seconds) for every SEC HTTP request.
SEC_TIMEOUT = 15


def clean_filing_html(html: str) -> str:
    """Strip HTML tags and collapse whitespace from raw filing markup."""
    clean = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", clean).strip()


def skip_front_matter(text: str, window: int, min_len_to_skip: int | None = None) -> str:
    """Return a `window`-sized slice of filing text past the cover-page boilerplate.

    Short filings are returned as-is. For longer ones we first offset past the
    start (the same proportional skip the RAG path has always used) and then, if a
    substantive section marker (Item 1A Risk Factors or Item 7 MD&A) appears in the
    remaining body, anchor on it so the slice carries real content instead of the
    cover page or table of contents.
    """
    threshold = window if min_len_to_skip is None else min_len_to_skip
    if len(text) <= threshold:
        return text[:window]

    offset = min(3000, len(text) // 10)
    body = text[offset:]
    for marker in (r"item\s*1a", r"item\s*7\b"):
        m = re.search(marker, body, re.I)
        if m:
            return body[m.start():m.start() + window]
    return body[:window]
