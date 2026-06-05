import os
import re
import requests
import hashlib
from langchain.tools import tool
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pinecone import Pinecone, ServerlessSpec
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


def _get_pinecone_index(index_name: str):
    """Gets or creates a Pinecone index."""
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    existing = [i.name for i in pc.list_indexes()]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=384,  # bge-small-en-v1.5 dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    return pc.Index(index_name)


def _fetch_filing_text(ticker: str, form_type: str) -> str | None:
    """Fetches narrative text from SEC filing for a given ticker and form type."""
    headers = {"User-Agent": "FinancialAgent agent@financial.com"}

    try:
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

                index_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{accession_dashed}-index.htm"
                index_response = requests.get(index_url, headers=headers, timeout=15)

                htm_files = re.findall(r'href="(/Archives/edgar/data/[^"]+\.htm)"', index_response.text)

                doc_url = None
                for href in htm_files:
                    if "index" not in href.lower() and "ex" not in href.lower().split("/")[-1]:
                        doc_url = f"https://www.sec.gov{href}"
                        break

                if not doc_url and htm_files:
                    doc_url = f"https://www.sec.gov{htm_files[0]}"

                if doc_url:
                    filing_response = requests.get(doc_url, headers=headers, timeout=15)
                    clean = re.sub(r'<[^>]+>', ' ', filing_response.text)
                    clean = re.sub(r'\s+', ' ', clean).strip()
                    if len(clean) > 5000:
                        start = min(3000, len(clean) // 10)
                        return clean[start:start + 15000]
                    return clean[:15000]

    except Exception as e:
        return f"Error fetching filing: {str(e)}"

    return None


@tool
def query_sec_filing(input: str) -> str:
    """
    Uses RAG with Pinecone vector store to answer specific questions about
    a company's SEC filings. Input format: 'TICKER: your question here'
    Example: 'AAPL: What are the main risk factors?'
    Filings are indexed in Pinecone for fast persistent retrieval.
    """
    try:
        if ":" not in input:
            return "Invalid input format. Use 'TICKER: your question'"

        ticker, question = input.split(":", 1)
        ticker = ticker.strip().upper()
        question = question.strip()

        # Configure LlamaIndex
        _configure_settings()

        # Use a sanitized index name
        index_name = f"sec-filings"

        # Get Pinecone index
        pinecone_index = _get_pinecone_index(index_name)
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Check if ticker already indexed using namespace
        namespace = ticker.lower()

        # Try querying existing index first
        try:
            index = VectorStoreIndex.from_vector_store(
                vector_store=PineconeVectorStore(
                    pinecone_index=pinecone_index,
                    namespace=namespace
                )
            )
            query_engine = index.as_query_engine(similarity_top_k=3)
            response = query_engine.query(question)

            if str(response) and len(str(response)) > 50:
                return f"[From Pinecone cache] {str(response)}"
        except Exception:
            pass

        # Fetch and index filing
        filing_text = _fetch_filing_text(ticker, "10-K")
        if not filing_text:
            filing_text = _fetch_filing_text(ticker, "10-Q")
        if not filing_text:
            return f"Could not retrieve SEC filings for {ticker}"

        # Index into Pinecone with ticker namespace
        document = Document(
            text=filing_text,
            metadata={"ticker": ticker, "source": "SEC EDGAR"}
        )

        ns_vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index,
            namespace=namespace
        )
        ns_storage_context = StorageContext.from_defaults(vector_store=ns_vector_store)
        index = VectorStoreIndex.from_documents(
            [document],
            storage_context=ns_storage_context
        )

        query_engine = index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(question)

        return f"[Indexed to Pinecone] {str(response)}"

    except Exception as e:
        return f"RAG query failed: {str(e)}"