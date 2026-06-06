import os
import json
import hashlib
import ssl
import numpy as np
import redis
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")
CACHE_TTL = 60 * 60 * 24  # 24 hours
SIMILARITY_THRESHOLD = 0.92  # Cosine similarity threshold for cache hit


def _make_redis_client(url: str) -> redis.Redis:
    """Build a Redis client, stripping legacy ssl_cert_reqs URL params that
    newer redis-py rejects, and passing SSL settings via ssl_context instead."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    needs_ssl = parsed.scheme == "rediss" or "ssl_cert_reqs" in query_params

    query_params.pop("ssl_cert_reqs", None)
    clean_query = urlencode({k: v[0] for k, v in query_params.items()})
    scheme = "rediss" if needs_ssl else parsed.scheme
    clean_url = urlunparse(parsed._replace(scheme=scheme, query=clean_query))

    if needs_ssl:
        _ssl_ctx = ssl.create_default_context()
        _ssl_ctx.check_hostname = False
        _ssl_ctx.verify_mode = ssl.CERT_NONE
        return redis.from_url(clean_url, decode_responses=False, ssl_context=_ssl_ctx)
    return redis.from_url(clean_url, decode_responses=False)


# Initialize Redis client
redis_client = _make_redis_client(REDIS_URL)

# Initialize embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def _cosine_similarity(a: list, b: list) -> float:
    """Computes cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(np.dot(a, b) / norm)


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

    # Scan all cache keys for this type (SCAN is non-blocking unlike KEYS)
    keys = []
    cursor = 0
    while True:
        cursor, batch = redis_client.scan(cursor, match="research:*", count=100)
        keys.extend(batch)
        if cursor == 0:
            break

    best_match = None
    best_score = 0.0

    if keys:
        values = redis_client.mget(keys)
        for cached in values:
            try:
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