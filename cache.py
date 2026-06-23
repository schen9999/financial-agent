import os
import json
import redis
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")
CACHE_TTL = 60 * 60 * 24  # 24 hours


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
        return redis.Redis(**common, ssl=True, ssl_cert_reqs=None, ssl_check_hostname=False)
    return redis.Redis(**common)


# Initialize Redis client
redis_client = _make_redis_client(REDIS_URL)


def get_cached_response(ticker: str) -> dict | None:
    """
    Looks up the cached research brief for a ticker by its exact Redis key
    (research:{TICKER}), the same key the writes use. A direct key lookup is
    correct here because each ticker has exactly one brief; the previous
    embedding-similarity scan could return a different ticker's brief since the
    only token that varied in the embedded text was the ticker itself.
    Falls back to None on any Redis error so the app keeps working.
    When BYPASS_CACHE is set (used by the eval harness for clean A/B arms),
    always reports a miss so a run never returns another arm's cached answer.
    """
    if os.getenv("BYPASS_CACHE", "false").strip().lower() == "true":
        print(f"Cache BYPASS (read) for {ticker} -- BYPASS_CACHE=true")
        return None
    try:
        cache_key = f"research:{ticker.upper()}"
        cached = redis_client.get(cache_key)
        if not cached:
            print(f"Cache MISS for {ticker}")
            return None

        data = json.loads(cached.decode("utf-8"))
        print(f"Cache HIT for {ticker}")
        return {
            "result": data["result"],
            "ticker": data["ticker"],
            "cache_hit": True,
        }

    except Exception as e:
        print(f"Cache lookup failed, falling through to LLM: {e}")
        return None


def set_cached_response(ticker: str, result: str):
    """
    Stores a research brief in Redis under research:{TICKER}.
    Silently skips on any Redis error so caching is best-effort.
    Skips writing entirely when BYPASS_CACHE is set so eval runs never pollute
    the live cache with arm-specific briefs.
    """
    if os.getenv("BYPASS_CACHE", "false").strip().lower() == "true":
        print(f"Cache BYPASS (write) for {ticker.upper()} -- BYPASS_CACHE=true")
        return
    try:
        cache_key = f"research:{ticker.upper()}"
        data = {
            "ticker": ticker.upper(),
            "result": result,
        }

        redis_client.setex(cache_key, CACHE_TTL, json.dumps(data))
        print(f"Cached response for {ticker.upper()}")
    except Exception as e:
        print(f"Cache write failed (non-fatal): {e}")


def get_cache_stats() -> dict:
    """
    Returns cache statistics for metrics/monitoring.
    """
    # SCAN instead of the blocking KEYS for consistency with the read path.
    keys = []
    cursor = 0
    while True:
        cursor, batch = redis_client.scan(cursor, match="research:*", count=100)
        keys.extend(batch)
        if cursor == 0:
            break
    return {
        "cached_tickers": len(keys),
        "tickers": [k.decode("utf-8").replace("research:", "") for k in keys]
    }