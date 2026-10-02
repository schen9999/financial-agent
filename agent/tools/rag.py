import os
import re
import threading
import time
import requests
import hashlib
from langchain.tools import tool
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

from agent.tracing import traceable
from agent.tools.sec_common import (SEC_USER_AGENT, clean_filing_html,
                                    is_toc_listing_chunk, lookup_cik,
                                    primary_document_url, scrape_document_url,
                                    skip_front_matter)
from agent.tools.reranker import (
    reranking_enabled,
    rerank_candidates,
    rerank_top_n,
    baseline_top_k,
    query_engine_kwargs,
)

from agent import llm_ledger
from agent.tools.slm import llama_index_llm, slm_full_enabled

load_dotenv()

_settings_configured = False

# Retrieved chunk texts per question, for the eval's RAG-faithfulness metric
# (the answer judged against exactly what it was written from). Kept only
# while the ledger is enabled (eval), keyed by question — the harness pops
# both entries right after each ticker's retrieval.
_sources_lock = threading.Lock()
_sources: dict[str, list[str]] = {}


def pop_sources(question: str) -> list[str] | None:
    with _sources_lock:
        return _sources.pop(question, None)


class _HostedRagUsage:
    """llama_index event handler: records the hosted (Anthropic) RAG answer
    call's token usage in the ledger. Observation only; skips the SLM
    adapter's own responses (it records itself)."""

    def __init__(self):
        from llama_index.core.instrumentation.event_handlers import BaseEventHandler
        from llama_index.core.instrumentation.events.llm import (LLMChatEndEvent,
                                                                  LLMChatStartEvent)

        starts: dict[str, float] = {}

        class _Handler(BaseEventHandler):
            @classmethod
            def class_name(cls) -> str:
                return "HostedRagUsage"

            def handle(self, event, **kwargs):
                if not llm_ledger.enabled():
                    return
                if isinstance(event, LLMChatStartEvent):
                    starts[event.span_id] = time.perf_counter()
                elif isinstance(event, LLMChatEndEvent) and event.response is not None:
                    raw = event.response.raw or {}
                    t0 = starts.pop(event.span_id, None)
                    if raw.get("slm"):
                        return
                    usage = raw.get("usage")
                    stop = raw.get("stop_reason")
                    llm_ledger.record(
                        llm_ledger.current_site("rag"), "anthropic", raw.get("model"),
                        prompt_tokens=getattr(usage, "input_tokens", None),
                        completion_tokens=getattr(usage, "output_tokens", None),
                        latency_s=(time.perf_counter() - t0) if t0 else None,
                        finish_reason="length" if stop == "max_tokens" else stop,
                        text=event.response.message.content)

        self.handler = _Handler()


def _ensure_settings():
    """Configure the llama_index LLM + embedding model once, on first use.

    Done lazily (not at import time) so importing this module stays cheap and
    does not download the HuggingFace embedding model, matching the lazy pattern
    used for the judge LLM in agent/grounding.py and the planner in agent/graph.py.
    """
    global _settings_configured
    if _settings_configured:
        return
    Settings.llm = Anthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    from llama_index.core.instrumentation import get_dispatcher
    get_dispatcher().add_event_handler(_HostedRagUsage().handler)
    _settings_configured = True


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
    headers = {"User-Agent": SEC_USER_AGENT}

    try:
        # Primary: authoritative mapping (shared, cached); the browse-edgar
        # scrape survives as fallback only — it fails under EDGAR throttling
        # (the MSFT failure surfaced by the judge-validation labeling).
        cik = lookup_cik(ticker)
        if not cik:
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
        primary_docs = filings.get("primaryDocument", [])

        for i, form in enumerate(forms):
            if form == form_type:
                accession = accession_numbers[i].replace("-", "")
                accession_dashed = accession_numbers[i]

                # Primary: the submissions JSON names the real main document
                # (index-page scraping picked Exhibit 4.x for iXBRL filers —
                # see sec_common.primary_document_url).
                doc_url = primary_document_url(
                    cik, accession_dashed,
                    primary_docs[i] if i < len(primary_docs) else None)

                if not doc_url:
                    index_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{accession_dashed}-index.htm"
                    index_response = requests.get(index_url, headers=headers, timeout=15)
                    doc_url = scrape_document_url(index_response.text)

                if doc_url:
                    filing_response = requests.get(doc_url, headers=headers, timeout=15)
                    clean = clean_filing_html(filing_response.text)
                    # Skip cover-page front matter (shared with sec.py); short
                    # filings under 5000 chars are returned whole.
                    return skip_front_matter(clean, 15000, min_len_to_skip=5000)

    except Exception:
        return None

    return None


class _DropTocListings(BaseNodePostprocessor):
    """Query-time filter: drop retrieved chunks that read as TOC listings
    (see sec_common.is_toc_listing_chunk). Applied before the cross-encoder
    when reranking is on, so listing junk never occupies a top-N slot.
    Query-time on purpose — already-indexed namespaces need no reindex."""

    @classmethod
    def class_name(cls) -> str:
        return "DropTocListings"

    def _postprocess_nodes(self, nodes, query_bundle=None):
        return [n for n in nodes if not is_toc_listing_chunk(n.node.get_content())]


def _run_rag_query(index, question: str):
    """Query the index through the configured retrieval pipeline, logging
    retrieval latency so the reranking on/off cost is always visible.

    Reranking OFF: single-stage top-3 cosine retrieval (original behaviour).
    Reranking ON:  over-retrieve `RERANK_CANDIDATES`, then a cross-encoder
                   reranks down to `RERANK_TOP_N`.
    """
    enabled = reranking_enabled()
    kwargs = query_engine_kwargs()
    kwargs["node_postprocessors"] = (
        [_DropTocListings()] + kwargs.get("node_postprocessors", []))
    if slm_full_enabled():
        # Per query, never via the process-global Settings.llm (hosted Haiku).
        kwargs["llm"] = llama_index_llm(llm_ledger.current_site("rag"))
    query_engine = index.as_query_engine(**kwargs)

    t0 = time.perf_counter()
    response = query_engine.query(question)
    elapsed = time.perf_counter() - t0
    if llm_ledger.enabled():
        with _sources_lock:
            _sources[question] = [n.node.get_content() for n in (response.source_nodes or [])]

    if enabled:
        print(
            f"[rag] retrieval reranking=ON {elapsed:.3f}s "
            f"candidates={rerank_candidates()} top_n={rerank_top_n()}"
        )
    else:
        k = baseline_top_k()
        print(f"[rag] retrieval reranking=OFF {elapsed:.3f}s candidates={k} top_n={k}")
    return response


@tool
@traceable(
    run_type="retriever",
    name="query_sec_filing",
    tags=["rag_retrieval"],
)
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

        # Build the LLM + embedding model on first use rather than at import.
        _ensure_settings()

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
            response = _run_rag_query(index, question)

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

        response = _run_rag_query(index, question)

        return f"[Indexed to Pinecone] {str(response)}"

    except Exception as e:
        return f"RAG query failed: {str(e)}"