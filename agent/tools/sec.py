import requests
from langchain.tools import tool


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
    """Looks up the SEC CIK number for a given ticker."""
    url = "https://efts.sec.gov/LATEST/search-index?q=%22{}%22&dateRange=custom&startdt=2020-01-01&enddt=2025-12-31&forms=10-K".format(ticker.upper())

    headers = {"User-Agent": "FinancialAgent agent@financial.com"}

    try:
        response = requests.get(
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&ticker={ticker}&type=10-K&dateb=&owner=include&count=1&search_text=&output=atom",
            headers=headers
        )
        # Extract CIK from response
        text = response.text
        cik_start = text.find("CIK=") + 4
        cik_end = text.find("&", cik_start)
        if cik_start > 4 and cik_end > cik_start:
            return text[cik_start:cik_end].zfill(10)
    except Exception:
        pass

    # Fallback: use EDGAR company search
    try:
        response = requests.get(
            "https://efts.sec.gov/LATEST/search-index?q=%22{}%22&forms=10-K".format(ticker.upper()),
            headers=headers
        )
    except Exception:
        pass

    return None


def _get_latest_filing(cik: str, form_type: str) -> dict:
    """Fetches the most recent filing of a given type for a CIK."""
    headers = {"User-Agent": "FinancialAgent agent@financial.com"}

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers)

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
            accession = accession_numbers[i].replace("-", "")
            doc = descriptions[i]
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"

            return {
                "form_type": form_type,
                "filing_date": dates[i],
                "url": filing_url,
                "summary": _extract_filing_summary(filing_url, headers)
            }

    return {"message": f"No {form_type} found"}


def _extract_filing_summary(url: str, headers: dict) -> str:
    """Fetches and returns the first 2000 characters of a filing."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        text = response.text

        # Strip HTML tags roughly
        import re
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean).strip()

        return clean[:2000] + "..." if len(clean) > 2000 else clean
    except Exception as e:
        return f"Could not extract filing text: {str(e)}"