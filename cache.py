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
    """Build a Redis client by parsing the URL into components and calling
    redis.Redis() directly, bypassing redis.from_url()/parse_url() entirely.
    This avoids ValueError from legacy ssl_cert_reqs query params and
    non-standard URL schemes that newer redis-py rejects."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    needs_ssl = parsed.scheme.lower() == "rediss" or "ssl_cert_reqs" in query_params

    host = parsed.hostname or "localhost"
    port = parsed.port or (6380 if needs_ssl else 6379)
    password = parsed.password or None
    username = parsed.username or None
    try:
        db = int(parsed.path.strip("/")) if parsed.path.strip("/") else 0
    except ValueError:
        db = 0

    common = dict(
        host=host, port=port, password=password, username=username,
        db=db, decode_responses=False,
        socket_keepalive=True,
        health_check_interval=30,
        retry_on_timeout=True,
    )
    if needs_ssl:
        _ssl_ctx = ssl.create_default_context()
        _ssl_ctx.check_hostname = False
        _ssl_ctx.verify_mode = ssl.CERT_NONE
        return redis.Redis(**common, ssl=True, ssl_context=_ssl_ctx)
    return redis.Redis(**common)


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
    Falls back to None on any Redis error so the app keeps working.
    """
    try:
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
                "similarity_score": best_score,
            }

        print(f"Cache MISS for {ticker} (best similarity: {best_score:.3f})")
        return None

    except Exception as e:
        print(f"Cache lookup failed, falling through to LLM: {e}")
        return None


def set_cached_response(ticker: str, result: str):
    """
    Stores a research brief and its embedding in Redis.
    Silently skips on any Redis error — caching is best-effort.
    """
    try:
        query = f"financial research brief for {ticker.upper()}"
        embedding = _get_query_embedding(query)

        cache_key = f"research:{ticker.upper()}"
        data = {
            "ticker": ticker.upper(),
            "result": result,
            "embedding": embedding,
        }

        redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
        print(f"Cached response for {ticker.upper()}")
    except Exception as e:
        print(f"Cache write failed (non-fatal): {e}")


def get_cache_stats() -> dict:
    """
    Returns cache statistics for metrics/monitoring.
    """
    keys = redis_client.keys("research:*")
    return {
        "cached_tickers": len(keys),
        "tickers": [k.decode("utf-8").replace("research:", "") for k in keys]
    }