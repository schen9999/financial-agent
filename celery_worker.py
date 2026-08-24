import os
import ssl
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
load_dotenv()

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")


def _clean_redis_url(url: str) -> tuple[str, bool]:
    """Rebuild a clean Redis URL from parsed components, dropping any query
    params (e.g. legacy ssl_cert_reqs) that newer redis-py rejects."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    needs_ssl = parsed.scheme.lower() == "rediss" or "ssl_cert_reqs" in query_params
    scheme = "rediss" if needs_ssl else "redis"
    # Reconstruct without query string; DB number stays in path (e.g. /0)
    clean_url = f"{scheme}://{parsed.netloc}{parsed.path}"
    return clean_url, needs_ssl


_BROKER_URL, _NEEDS_SSL = _clean_redis_url(REDIS_URL)

celery_app = Celery(
    "financial_agent",
    broker=_BROKER_URL,
    backend=_BROKER_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)

if _NEEDS_SSL:
    _ssl_opts = {"ssl_cert_reqs": ssl.CERT_NONE}
    celery_app.conf.update(
        broker_use_ssl=_ssl_opts,
        redis_backend_use_ssl=_ssl_opts,
    )


@celery_app.task(bind=True)
def research_task(self, ticker: str) -> dict:
    """
    Async Celery task that runs the financial research agent.
    Submitted via FastAPI and executed by a background worker.
    """
    try:
        self.update_state(state="PROGRESS", meta={"status": f"Researching {ticker}..."})
        from agent.core import run_research
        from agent.tracing import tracing_enabled

        if tracing_enabled():
            from langsmith import trace
            with trace(
                name="research_task",
                run_type="chain",
                tags=["full_brief", "async"],
                metadata={"request_type": "full_brief", "async": True, "ticker": ticker},
            ):
                result = run_research(ticker)
        else:
            result = run_research(ticker)
        return {"status": "complete", "ticker": ticker, "brief": result}
    except Exception:
        # Just re-raise: Celery records FAILURE with proper exception metadata.
        # Manually calling update_state(state="FAILURE", meta={...}) writes a
        # non-exception payload into the result backend; Celery's own failure
        # handler then can't decode it (KeyError: 'exc_type'), which masks the
        # real traceback and makes every later status read raise ValueError.
        raise