"""Cross-encoder reranking for the two-stage SEC-filing retrieval pipeline.

Stage 1 (Pinecone vector search) over-retrieves a candidate pool; stage 2
reranks those candidates with a cross-encoder and keeps only the top-N most
relevant chunks for generation. Reranking is gated behind RERANKING_ENABLED so
the baseline single-stage path is unchanged when the flag is off.

This module is a thin factory around LlamaIndex's built-in
SentenceTransformerRerank postprocessor: the model is loaded lazily and cached,
so nothing is downloaded or held in memory unless reranking is actually used.
Config is read from the environment on every call so A/B arms can toggle the
flags within a single process.
"""
import os

from llama_index.core.postprocessor import SentenceTransformerRerank

# Cross-encoder model — CPU-friendly, ~280 MB, downloaded once on first use.
_DEFAULT_MODEL = "BAAI/bge-reranker-base"

_reranker = None  # cached SentenceTransformerRerank instance


def reranking_enabled() -> bool:
    """Whether the cross-encoder reranking stage is active. Defaults to off so
    the live Streamlit/Celery/cache paths behave exactly as before."""
    return os.getenv("RERANKING_ENABLED", "false").strip().lower() == "true"


def rerank_candidates() -> int:
    """How many candidates stage 1 over-retrieves before reranking (top-k)."""
    try:
        return int(os.getenv("RERANK_CANDIDATES", "20"))
    except ValueError:
        return 20


def rerank_top_n() -> int:
    """How many reranked chunks are passed to generation (final top-n)."""
    try:
        return int(os.getenv("RERANK_TOP_N", "3"))
    except ValueError:
        return 3


def rerank_model() -> str:
    return os.getenv("RERANK_MODEL", _DEFAULT_MODEL)


def baseline_top_k() -> int:
    """Top-k for the single-stage (no-rerank) path. Defaults to 3 so production
    behaviour is unchanged; the eval harness can set BASELINE_TOP_K to compare a
    plain top-5 retrieval against reranking-to-5."""
    try:
        return int(os.getenv("BASELINE_TOP_K", "3"))
    except ValueError:
        return 3


def get_reranker() -> SentenceTransformerRerank:
    """Lazily build and cache the cross-encoder reranker. The model is loaded
    only on first call (i.e. only when reranking is enabled). top_n is refreshed
    from the environment each call so A/B arms can vary it in-process."""
    global _reranker
    if _reranker is None:
        _reranker = SentenceTransformerRerank(
            model=rerank_model(),
            top_n=rerank_top_n(),
        )
    else:
        _reranker.top_n = rerank_top_n()
    return _reranker


def query_engine_kwargs() -> dict:
    """Build the kwargs for index.as_query_engine() for the current config.

    Reranking ON:  over-retrieve `RERANK_CANDIDATES` and attach the cross-encoder
                   postprocessor (which trims to `RERANK_TOP_N`).
    Reranking OFF: the original single-stage behaviour — top-3 by cosine.
    """
    if reranking_enabled():
        return {
            "similarity_top_k": rerank_candidates(),
            "node_postprocessors": [get_reranker()],
        }
    return {"similarity_top_k": baseline_top_k()}
