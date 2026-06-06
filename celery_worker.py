import os
import ssl
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from dotenv import load_dotenv
load_dotenv()

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")


def _clean_redis_url(url: str) -> tuple[str, bool]:
    """Strip legacy ssl_cert_reqs query param; return (clean_url, needs_ssl)."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    needs_ssl = parsed.scheme == "rediss" or "ssl_cert_reqs" in query_params
    query_params.pop("ssl_cert_reqs", None)
    clean_query = urlencode({k: v[0] for k, v in query_params.items()})
    scheme = "rediss" if needs_ssl else parsed.scheme
    clean_url = urlunparse(parsed._replace(scheme=scheme, query=clean_query))
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
        result = run_research(ticker)
        return {"status": "complete", "ticker": ticker, "brief": result}
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise