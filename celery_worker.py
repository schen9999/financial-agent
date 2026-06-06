import os
import ssl
from dotenv import load_dotenv
load_dotenv()

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")

celery_app = Celery(
    "financial_agent",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)

if REDIS_URL.startswith("rediss://"):
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