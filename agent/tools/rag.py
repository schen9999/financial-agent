import os
import requests
from langchain.tools import tool
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

load_dotenv()


def _configure_settings():
    """Configure LlamaIndex to use Anthropic LLM and local embeddings."""
    Settings.llm = Anthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )


def _fetch_filing_text(ticker: str, form_type: str) -> str | None:
    """Fetches narrative text from SEC filing for a given ticker and form type."""
    headers = {"User-Agent": "FinancialAgent agent@financial.com"}

    try:
        # Get CIK
        response = requests.get(
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&ticker={ticker}&type={form_type}&dateb=&owner=include&count=1&output=atom",
            headers=headers
        )
        text = response.text
        cik_start = text.find("CIK=") + 4
        cik_end = text.find("&", cik_start)
        if cik_start <= 4:
            return None
        cik = text[cik_start:cik_end].zfill(10)

        # Get filing metadata
        response = requests.get(
            f"https://data.sec.gov/submissions/CIK{cik}.json",
            headers=headers
        )
        data = response.json()
        filings = data.get("filings", {}).get("recent", {})
        forms = filings.get("form", [])
        accession_numbers = filings.get("accessionNumber", [])

        for i, form in enumerate(forms):
            if form == form_type:
                accession = accession_numbers[i].replace("-", "")
                accession_dashed = accession_numbers[i]

                # Get filing index to find the right document
                index_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{accession_dashed}-index.htm"
                index_response = requests.get(index_url, headers=headers, timeout=15)

                # Find the main .htm document from the index
                import re
                htm_files = re.findall(r'href="(/Archives/edgar/data/[^"]+\.htm)"', index_response.text)

                doc_url = None
                for href in htm_files:
                    # Skip the index file itself, look for the main filing
                    if "index" not in href.lower() and "ex" not in href.lower().split("/")[-1]:
                        doc_url = f"https://www.sec.gov{href}"
                        break

                if not doc_url:
                    # Fallback to first htm file
                    if htm_files:
                        doc_url = f"https://www.sec.gov{htm_files[0]}"

                if doc_url:
                    filing_response = requests.get(doc_url, headers=headers, timeout=15)
                    clean = re.sub(r'<[^>]+>', ' ', filing_response.text)
                    clean = re.sub(r'\s+', ' ', clean).strip()

                    # Skip past the boilerplate header (first ~2000 chars usually metadata)
                    # and grab narrative content from the middle of the document
                    if len(clean) > 5000:
                        # Take a chunk from deeper in the document where narrative lives
                        start = min(3000, len(clean) // 10)
                        return clean[start:start + 15000]
                    return clean[:15000]

    except Exception as e:
        return f"Error fetching filing: {str(e)}"

    return None


@tool
def query_sec_filing(input: str) -> str:
    """
    Uses RAG to answer a specific question about a company's SEC filings.
    Input should be in the format: 'TICKER: your question here'
    For example: 'AAPL: What are the main risk factors?'
    Use this to extract specific insights from 10-K and 10-Q filings.
    """
    try:
        # Parse input
        if ":" not in input:
            return "Invalid input format. Use 'TICKER: your question'"

        ticker, question = input.split(":", 1)
        ticker = ticker.strip().upper()
        question = question.strip()

        # Fetch filing text
        filing_text = _fetch_filing_text(ticker, "10-K")
        if not filing_text:
            filing_text = _fetch_filing_text(ticker, "10-Q")
        if not filing_text:
            return f"Could not retrieve SEC filings for {ticker}"

        # Configure LlamaIndex
        _configure_settings()

        # Build index and query
        document = Document(text=filing_text, metadata={"ticker": ticker})
        index = VectorStoreIndex.from_documents([document])
        query_engine = index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(question)

        return str(response)

    except Exception as e:
        return f"RAG query failed: {str(e)}"