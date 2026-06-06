import os
import json
import hashlib
import numpy as np
import redis
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
CACHE_TTL = 60 * 60 * 24  # 24 hours
SIMILARITY_THRESHOLD = 0.92  # Cosine similarity threshold for cache hit

# Initialize Redis client
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=False,
    ssl_cert_reqs=None
)

# Initialize embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def _cosine_similarity(a: list, b: list) -> float:
    """Computes cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def _get_query_embedding(query: str) -> list:
    """Generates embedding for a query string."""
    return embed_model.get_text_embedding(query)


def get_cached_response(ticker: str) -> dict | None:
    """
    Checks Redis for a semantically similar cached research brief.
    Returns cached result if similarity exceeds threshold, else None.
    """
    query = f"financial research brief for {ticker.upper()}"
    query_embedding = _get_query_embedding(query)

    # Scan all cache keys for this type
    keys = redis_client.keys("research:*")

    best_match = None
    best_score = 0.0

    for key in keys:
        try:
            cached = redis_client.get(key)
            if not cached:
                continue

            data = json.loads(cached.decode("utf-8"))
            cached_embedding = data.get("embedding")
            if not cached_embedding:
                continue

            score = _cosine_similarity(query_embedding, cached_embedding)
            if score > best_score:
                best_score = score
                best_match = data

        except Exception:
            continue

    if best_score >= SIMILARITY_THRESHOLD and best_match:
        print(f"Cache HIT for {ticker} (similarity: {best_score:.3f})")
        return {
            "result": best_match["result"],
            "ticker": best_match["ticker"],
            "cache_hit": True,
            "similarity_score": best_score
        }

    print(f"Cache MISS for {ticker} (best similarity: {best_score:.3f})")
    return None


def set_cached_response(ticker: str, result: str):
    """
    Stores a research brief and its embedding in Redis.
    """
    query = f"financial research brief for {ticker.upper()}"
    embedding = _get_query_embedding(query)

    cache_key = f"research:{ticker.upper()}"
    data = {
        "ticker": ticker.upper(),
        "result": result,
        "embedding": embedding
    }

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(data)
    )
    print(f"Cached response for {ticker.upper()}")


def get_cache_stats() -> dict:
    """
    Returns cache statistics for metrics/monitoring.
    """
    keys = redis_client.keys("research:*")
    return {
        "cached_tickers": len(keys),
        "tickers": [k.decode("utf-8").replace("research:", "") for k in keys]
    }