import os
from dotenv import load_dotenv
load_dotenv()

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL environment variable is not set")
REDIS_URL_WITH_SSL = REDIS_URL + "?ssl_cert_reqs=CERT_NONE" if "?" not in REDIS_URL else REDIS_URL + "&ssl_cert_reqs=CERT_NONE"

celery_app = Celery(
    "financial_agent",
    broker=REDIS_URL_WITH_SSL,
    backend=REDIS_URL_WITH_SSL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
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