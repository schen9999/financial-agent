from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.core import run_research
from agent.react_agent import answer_question
from agent.tools.stock import get_stock_data, get_price_history
from celery.result import AsyncResult
from celery_worker import celery_app, research_task
from database import save_brief, get_briefs_by_ticker, get_recent_briefs, init_db
import uvicorn

app = FastAPI(
    title="Financial Research Agent API",
    description="REST API for autonomous stock research using Claude AI",
    version="1.0.0"
)
init_db()


class ResearchRequest(BaseModel):
    ticker: str


class ResearchResponse(BaseModel):
    ticker: str
    brief: str


class AskRequest(BaseModel):
    ticker: str
    question: str


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check if the API is running."""
    return HealthResponse(status="ok", version="1.0.0")


@app.get("/stock/{ticker}")
def get_stock(ticker: str):
    """
    Fetch live stock data for a given ticker.
    Returns price, market cap, P/E ratio, revenue, and more.
    """
    result = get_stock_data.invoke({"ticker": ticker.upper()})
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/stock/{ticker}/history")
def get_history(ticker: str):
    """
    Fetch 12 months of price history for a given ticker.
    """
    result = get_price_history.invoke({"ticker": ticker.upper()})
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/research", response_model=ResearchResponse)
def research_stock(request: ResearchRequest):
    """
    Run the full AI research agent on a stock ticker.
    Saves the result to PostgreSQL for future retrieval.
    """
    try:
        brief = run_research(request.ticker.upper())
        save_brief(ticker=request.ticker.upper(), brief=brief)
        return ResearchResponse(ticker=request.ticker.upper(), brief=brief)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/{ticker}")
def get_ticker_history(ticker: str):
    """
    Retrieves all past research briefs for a given ticker from PostgreSQL.
    """
    briefs = get_briefs_by_ticker(ticker.upper())
    if not briefs:
        raise HTTPException(status_code=404, detail=f"No history found for {ticker}")
    return [
        {
            "id": b.id,
            "ticker": b.ticker,
            "created_at": b.created_at.isoformat(),
            "brief": b.brief[:500] + "..." if len(b.brief) > 500 else b.brief
        }
        for b in briefs
    ]


@app.get("/history")
def get_recent_history():
    """
    Retrieves the 10 most recent research briefs from PostgreSQL.
    """
    briefs = get_recent_briefs(limit=10)
    return [
        {
            "id": b.id,
            "ticker": b.ticker,
            "created_at": b.created_at.isoformat(),
        }
        for b in briefs
    ]

@app.post("/research/async")
def research_stock_async(request: ResearchRequest):
    """
    Submits a stock research job to the Celery task queue.
    Returns a job ID immediately — use /research/status/{job_id} to poll.
    """
    task = research_task.delay(request.ticker.upper())
    return {"job_id": task.id, "status": "queued", "ticker": request.ticker.upper()}


@app.get("/research/status/{job_id}")
def get_research_status(job_id: str):
    """
    Polls the status of an async research job.
    Returns status: queued | processing | complete | error
    """
    result = AsyncResult(job_id, app=celery_app)

    try:
        state = result.state
        if state == "PENDING":
            return {"job_id": job_id, "status": "queued"}
        elif state in ("STARTED", "PROGRESS"):
            return {"job_id": job_id, "status": "processing", "meta": result.info}
        elif state == "SUCCESS":
            return {"job_id": job_id, "status": "complete", "result": result.result}
        else:
            return {"job_id": job_id, "status": "error", "error": str(result.info)}
    except Exception as e:
        # A malformed backend record (e.g. legacy manually-written FAILURE meta)
        # raises on decode; report it as an errored job instead of a 500.
        return {"job_id": job_id, "status": "error",
                "error": f"could not read job state: {e}"}

@app.post("/ask")
def ask_question(request: AskRequest):
    """
    Answer a free-form question about a stock using the ReAct agent.
    The agent selects whichever tools it needs (stock data, news, SEC filings, RAG).
    """
    try:
        answer = answer_question(request.ticker.upper(), request.question)
        return {
            "ticker": request.ticker.upper(),
            "question": request.question,
            "answer": answer,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)