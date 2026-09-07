import requests
from langchain.tools import tool

from agent.tools.sec_common import (
    SEC_USER_AGENT,
    SEC_TIMEOUT,
    clean_filing_html,
    lookup_cik,
    primary_document_url,
    skip_front_matter,
)


@tool
def get_sec_filings(ticker: str) -> dict:
    """
    Fetches the most recent 10-K and 10-Q filing summaries from SEC EDGAR
    for a given ticker symbol. Use this to get in-depth financial disclosures
    and management commentary.
    """
    try:
        # Step 1: Get CIK number from ticker
        cik = _get_cik(ticker)
        if not cik:
            return {"error": f"Could not find SEC CIK for ticker {ticker}"}

        # Step 2: Get recent filings
        results = {}
        for form_type in ["10-K", "10-Q"]:
            filing = _get_latest_filing(cik, form_type)
            results[form_type] = filing

        return results

    except Exception as e:
        return {"error": f"SEC lookup failed for {ticker}: {str(e)}"}


def _get_cik(ticker: str) -> str | None:
    """Looks up the SEC CIK number for a given ticker.

    Primary: the authoritative company_tickers.json mapping (sec_common.
    lookup_cik — deterministic, cached). The browse-edgar scrape and the
    full-text-search guess below survive only as fallbacks for tickers the
    mapping misses."""
    cik = lookup_cik(ticker)
    if cik:
        return cik

    headers = {"User-Agent": SEC_USER_AGENT}

    try:
        response = requests.get(
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&ticker={ticker}&type=10-K&dateb=&owner=include&count=1&search_text=&output=atom",
            headers=headers,
            timeout=SEC_TIMEOUT,
        )
        # Extract CIK from response
        text = response.text
        cik_start = text.find("CIK=") + 4
        cik_end = text.find("&", cik_start)
        if cik_start > 3 and cik_end > cik_start:
            return text[cik_start:cik_end].zfill(10)
    except Exception:
        pass

    # Fallback: use EDGAR full-text search index
    try:
        response = requests.get(
            "https://efts.sec.gov/LATEST/search-index?q=%22{}%22&forms=10-K".format(ticker.upper()),
            headers=headers,
            timeout=SEC_TIMEOUT,
        )
        data = response.json()
        hits = data.get("hits", {}).get("hits", [])
        if hits:
            entity_id = hits[0].get("_source", {}).get("entity_id")
            if entity_id:
                return str(entity_id).zfill(10)
    except Exception:
        pass

    return None


def _get_latest_filing(cik: str, form_type: str) -> dict:
    """Fetches the most recent filing of a given type for a CIK."""
    headers = {"User-Agent": SEC_USER_AGENT}

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers, timeout=SEC_TIMEOUT)

    if response.status_code != 200:
        return {"error": f"Could not fetch filings for CIK {cik}"}

    data = response.json()
    filings = data.get("filings", {}).get("recent", {})

    forms = filings.get("form", [])
    dates = filings.get("filingDate", [])
    accession_numbers = filings.get("accessionNumber", [])
    descriptions = filings.get("primaryDocument", [])

    for i, form in enumerate(forms):
        if form == form_type:
            # Shared resolver: same URL as before for plain filenames, and
            # defensively unwraps an /ix?doc= wrapper if one ever appears.
            filing_url = primary_document_url(
                cik, accession_numbers[i],
                descriptions[i] if i < len(descriptions) else None)
            if not filing_url:
                continue

            return {
                "form_type": form_type,
                "filing_date": dates[i],
                "url": filing_url,
                "summary": _extract_filing_summary(filing_url, headers)
            }

    return {"message": f"No {form_type} found"}


def _extract_filing_summary(url: str, headers: dict) -> str:
    """Fetches a filing and returns ~2000 chars of real narrative content.

    The raw first 2000 chars are almost always cover-page / table-of-contents
    boilerplate, so we skip the front matter the same way the RAG path does
    (shared skip_front_matter helper): offset past the start and anchor on the
    first Item 1A / Item 7 section marker when present.
    """
    try:
        response = requests.get(url, headers=headers, timeout=SEC_TIMEOUT)
        clean = clean_filing_html(response.text)

        summary = skip_front_matter(clean, 2000)
        return summary + "..." if len(clean) > len(summary) else summary
    except Exception as e:
        return f"Could not extract filing text: {str(e)}"