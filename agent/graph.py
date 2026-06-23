"""Multi-agent supervisor graph for brief generation.

A LangGraph StateGraph that decomposes brief generation into four cooperating
agents, gated behind MULTI_AGENT_ENABLED (default off — the single-agent path in
core.py stays the production default and the A/B control):

    START → planner → research → critic → supervisor → (research | END)

  planner     decomposes the ticker into a research plan: the SEC RAG
              sub-questions that ground the two filing-based sections (today
              hardcoded in core.py) plus coverage points. The plan is
              load-bearing — research executes it.
  research    executes the plan against the EXISTING retrieval + model-routing
              code (core._rag_contexts / _haiku_section / _synthesis_prompt).
              On a revision pass it reuses the already-grounded middle sections
              and only re-synthesises the Executive Summary + Outlook with the
              critic's feedback, so the brief schema never changes.
  critic      runs the SHARED LLM-as-judge (agent.grounding.grade_brief) over the
              drafted Exec Summary + Outlook — one judge definition, also used by
              the offline eval harness.
  supervisor  compares the unsupported-claim rate against CRITIC_MAX_UNSUPPORTED_PCT
              and decides pass / revise / stop, bounding the retry loop at
              MAX_REVISIONS passes.

LangGraph traces each node as its own LangSmith span (planner / research /
critic / supervisor), so the nodes carry no extra @traceable decorator; only the
top-level run_multi_agent entry is decorated. The brief output schema is
identical to the single-agent path: research reuses core._synthesis_prompt,
which owns the format.
"""
import os
import json
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from agent.core import (
    fetch_research_data,
    _rag_contexts,
    _SECTIONS,
    _haiku_section,
    _synthesis_prompt,
    _trim_stock, _trim_news, _trim_sec, _data_context,
    _llm as _sonnet,
    DEFAULT_HIGHLIGHTS_QUERY,
    DEFAULT_RISKS_QUERY,
)
from agent.grounding import grade_brief, extract_exec_and_outlook
from agent.tracing import traceable


# ── Plan schema ──────────────────────────────────────────────────────────────────

class ResearchPlan(BaseModel):
    """Structured plan the planner emits and the research node executes."""
    highlights_query: str = Field(
        default="",
        description="SEC-filing RAG sub-question that should ground the 'SEC Filing "
                    "Highlights' section (no ticker prefix; e.g. 'Summarize the latest "
                    "10-K and 10-Q takeaways for the cloud and AI segments').",
    )
    risks_query: str = Field(
        default="",
        description="SEC-filing RAG sub-question that should ground the 'Risk Factors' "
                    "section (no ticker prefix).",
    )
    coverage: list[str] = Field(
        default_factory=list,
        description="3-5 specific points the finished brief must cover for this company.",
    )
    sub_questions: list[str] = Field(
        default_factory=list,
        description="Research sub-questions that motivate the brief.",
    )


# ── Graph state ──────────────────────────────────────────────────────────────────

class BriefState(TypedDict, total=False):
    ticker: str
    # pre-fetched raw data (optional — supplied by the streaming caller to avoid a
    # double fetch; otherwise the planner fetches it).
    raw_stock: dict
    raw_news: list
    raw_sec: dict
    # trimmed data + derived context (set by planner, reused by research/critic)
    stock: dict
    news: list
    sec: dict
    company: str
    context: str
    # planner output
    plan: dict
    # research output
    rag_highlights: str
    rag_risks: str
    sections: list
    source_context: str
    brief: str
    # critic output
    critique: dict
    # control
    feedback: str
    decision: str
    revisions: int
    max_revisions: int
    threshold: float


# ── Planner ──────────────────────────────────────────────────────────────────────

_PLANNER_SYSTEM = """You are the planning agent for an investment-brief pipeline. \
Given a company and the raw data already gathered about it, produce a concise \
research plan. The brief has a fixed structure (Financial Health, Recent \
Developments, SEC Filing Highlights, Risk Factors, plus an Executive Summary and \
Outlook) — you do NOT choose the sections. Your job is to tailor the two SEC-filing \
RAG sub-questions to what matters most for THIS company, and to list the coverage \
points the brief must hit. Keep sub-questions specific and answerable from 10-K / \
10-Q filings."""


def _planner_user(company: str, ticker: str, context: str) -> str:
    return (
        f"Company: {company} ({ticker})\n\n"
        f"Data already gathered:\n{context}\n\n"
        "Produce the research plan."
    )


_planner_llm = None


def _get_planner_llm():
    """Lazily build the structured-output planner (Haiku — cheap, plan is short)."""
    global _planner_llm
    if _planner_llm is None:
        base = ChatAnthropic(
            model="claude-haiku-4-5-20251001",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0,
        )
        _planner_llm = base.with_structured_output(ResearchPlan)
    return _planner_llm


def _make_plan(company: str, ticker: str, context: str) -> dict:
    """Call the planner LLM; fall back to the default RAG sub-questions (today's
    hardcoded behaviour) if the planner errors or returns blanks, so a planner
    hiccup can never break a brief."""
    try:
        plan: ResearchPlan = _get_planner_llm().invoke([
            SystemMessage(content=_PLANNER_SYSTEM),
            HumanMessage(content=_planner_user(company, ticker, context)),
        ])
        return {
            "highlights_query": plan.highlights_query.strip() or DEFAULT_HIGHLIGHTS_QUERY,
            "risks_query": plan.risks_query.strip() or DEFAULT_RISKS_QUERY,
            "coverage": plan.coverage,
            "sub_questions": plan.sub_questions,
        }
    except Exception as e:
        print(f"[multi_agent] planner fell back to default queries: {type(e).__name__}: {e}")
        return {
            "highlights_query": DEFAULT_HIGHLIGHTS_QUERY,
            "risks_query": DEFAULT_RISKS_QUERY,
            "coverage": [],
            "sub_questions": [],
        }


def planner_node(state: BriefState) -> dict:
    ticker = state["ticker"]
    if "raw_stock" in state:
        stock_data = state["raw_stock"]
        news_data = state.get("raw_news")
        sec_data = state["raw_sec"]
    else:
        stock_data, news_data, sec_data = fetch_research_data(ticker)

    stock = _trim_stock(stock_data)
    news = _trim_news(news_data)
    sec = _trim_sec(sec_data)
    company = stock.get("company_name", ticker)
    context = _data_context(stock, news, sec)

    plan = _make_plan(company, ticker, context)
    return {
        "stock": stock, "news": news, "sec": sec,
        "company": company, "context": context, "plan": plan,
    }


# ── Research ─────────────────────────────────────────────────────────────────────

def _generate_sections(ticker: str, company: str, context: str,
                       highlights: str | None, risks: str | None) -> list[str]:
    """Generate the four middle sections in parallel, reusing core's per-section
    generator (which carries the Haiku / local-model routing)."""
    section_contexts = {
        "### Financial Health": context,
        "### Recent Developments": context,
        "### SEC Filing Highlights": highlights or context,
        "### Risk Factors": risks or context,
    }
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(_haiku_section, heading, instr, company, ticker,
                            section_contexts[heading])
            for heading, instr in _SECTIONS
        ]
        return [f.result() for f in futures]


def _build_source_context(stock: dict, news, sec: dict,
                          highlights: str | None, risks: str | None) -> str:
    """Assemble the grounding source the critic judges against — mirrors the
    offline harness so inline and offline grounding scores are comparable."""
    return "\n\n".join([
        f"STOCK DATA:\n{json.dumps(stock, indent=2)}",
        f"NEWS ARTICLES:\n{json.dumps(news, indent=2)}",
        f"SEC FILING SUMMARIES:\n{json.dumps(sec, indent=2)}",
        f"RAG — SEC HIGHLIGHTS:\n{highlights or '(not available)'}",
        f"RAG — RISK FACTORS:\n{risks or '(not available)'}",
    ])


def research_node(state: BriefState) -> dict:
    ticker = state["ticker"]
    company = state["company"]
    context = state["context"]
    plan = state.get("plan", {})

    # First pass retrieves and writes the grounded middle sections. Revision
    # passes reuse them and only re-synthesise the Exec Summary + Outlook, so the
    # critic's feedback can't disturb the already-grounded sections or the schema.
    if not state.get("sections"):
        highlights, risks = _rag_contexts(
            ticker, plan.get("highlights_query"), plan.get("risks_query")
        )
        sections = _generate_sections(ticker, company, context, highlights, risks)
        source_context = _build_source_context(
            state["stock"], state["news"], state["sec"], highlights, risks
        )
    else:
        highlights = state.get("rag_highlights")
        risks = state.get("rag_risks")
        sections = state["sections"]
        source_context = state["source_context"]

    prompt = _synthesis_prompt(ticker, company, sections)
    feedback = state.get("feedback")
    if feedback:
        prompt = f"{feedback}\n\n{prompt}"

    brief = _sonnet.invoke([HumanMessage(content=prompt)]).content

    return {
        "rag_highlights": highlights, "rag_risks": risks,
        "sections": sections, "source_context": source_context,
        "brief": brief,
    }


# ── Critic ───────────────────────────────────────────────────────────────────────

def critic_node(state: BriefState) -> dict:
    """Score the drafted brief with the shared grounding judge."""
    section_block = "\n\n".join(state["sections"])
    exec_and_outlook = extract_exec_and_outlook(state["brief"])
    grade = grade_brief(state["source_context"], section_block, exec_and_outlook)
    return {
        "critique": {
            "supported": grade.supported,
            "unsupported": grade.unsupported,
            "inference": grade.inference,
            "total": grade.total,
            "unsupported_pct": grade.unsupported_pct,
            "unsupported_claims": grade.unsupported_claims,
            "findings": grade.findings,
        }
    }


# ── Supervisor ───────────────────────────────────────────────────────────────────

def _revision_feedback(critique: dict) -> str:
    claims = critique.get("unsupported_claims", [])
    bullets = "\n".join(f'- "{c}"' for c in claims) or "- (see audit)"
    return (
        "=== REVISION REQUIRED ===\n"
        "A grounding audit flagged the following claims in the previous Executive "
        "Summary / Outlook as NOT supported by the source data:\n"
        f"{bullets}\n"
        "Rewrite the Executive Summary and Outlook so every statement is grounded in "
        "the pre-written sections and source data — remove or soften each flagged "
        "claim. Keep the EXACT same brief format and reproduce the four middle "
        "sections verbatim."
    )


def supervisor_node(state: BriefState) -> dict:
    """Decide whether the brief is done, needs revision, or has exhausted its
    revision budget."""
    critique = state["critique"]
    threshold = state.get("threshold", 5.0)
    revisions = state.get("revisions", 0)
    max_revisions = state.get("max_revisions", 2)

    if critique["unsupported_pct"] <= threshold:
        return {"decision": "pass"}
    if revisions >= max_revisions:
        return {"decision": "stop"}
    return {
        "decision": "revise",
        "revisions": revisions + 1,
        "feedback": _revision_feedback(critique),
    }


def _route_after_supervisor(state: BriefState) -> str:
    return "research" if state.get("decision") == "revise" else END


# ── Build / run ──────────────────────────────────────────────────────────────────

_compiled_graph = None


def build_graph() -> StateGraph:
    """Construct the (uncompiled) supervisor graph. Exposed for tests."""
    g = StateGraph(BriefState)
    g.add_node("planner", planner_node)
    g.add_node("research", research_node)
    g.add_node("critic", critic_node)
    g.add_node("supervisor", supervisor_node)

    g.add_edge(START, "planner")
    g.add_edge("planner", "research")
    g.add_edge("research", "critic")
    g.add_edge("critic", "supervisor")
    g.add_conditional_edges(
        "supervisor", _route_after_supervisor,
        {"research": "research", END: END},
    )
    return g


def get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph().compile()
    return _compiled_graph


@traceable(run_type="chain", name="run_research_multi_agent",
           tags=["full_brief", "multi_agent"],
           metadata={"request_type": "full_brief", "path": "multi_agent",
                     "synthesis_model": "claude-sonnet-4-6",
                     "section_model": "claude-haiku-4-5-20251001"})
def run_multi_agent(ticker: str, stock_data: dict | None = None,
                    news_data=None, sec_data: dict | None = None) -> str:
    """Run the multi-agent graph and return the final brief string (same schema as
    the single-agent path). If stock/news/sec data is supplied it's reused instead
    of refetched (the streaming caller already has it)."""
    init: BriefState = {
        "ticker": ticker.upper(),
        "revisions": 0,
        "max_revisions": int(os.getenv("MAX_REVISIONS", "2")),
        "threshold": float(os.getenv("CRITIC_MAX_UNSUPPORTED_PCT", "5")),
    }
    if stock_data is not None:
        init["raw_stock"] = stock_data
        init["raw_news"] = news_data
        init["raw_sec"] = sec_data

    final = get_compiled_graph().invoke(init)
    return final["brief"]


def multi_agent_enabled() -> bool:
    """Whether brief generation routes through the multi-agent supervisor graph.
    Defaults off so the single-agent path stays the production default + A/B control."""
    return os.getenv("MULTI_AGENT_ENABLED", "false").strip().lower() == "true"
