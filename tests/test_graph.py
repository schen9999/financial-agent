"""Tests for the multi-agent supervisor graph (agent/graph.py).

All LLM / network calls are mocked — these tests exercise the graph wiring:
the planner's output shape, the critic→research revision loop, and supervisor
termination (the loop is bounded and always halts).
"""
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import agent.graph as graph
from agent.graph import (
    planner_node, supervisor_node, _make_plan, ResearchPlan, build_graph,
)
from agent.grounding import GradeResult


# ── Helpers ──────────────────────────────────────────────────────────────────────

_BRIEF = """## Apple Inc. (AAPL) — Investment Brief

### Executive Summary
Apple is a large-cap tech company. The stock is notable now. Watch services margin.

### Financial Health
Revenue is strong.

### Recent Developments
New product launch.

### SEC Filing Highlights
Filing notes.

### Risk Factors
- Supply chain.

### Outlook
Cautiously constructive; watch China exposure.
"""

_SECTIONS = [
    "### Financial Health\nRevenue is strong.",
    "### Recent Developments\nNew product launch.",
    "### SEC Filing Highlights\nFiling notes.",
    "### Risk Factors\n- Supply chain.",
]


def _grade(unsupported_pct, unsupported=0):
    """Build a GradeResult with a chosen unsupported rate."""
    return GradeResult(
        findings="(stub findings)",
        supported=10, unsupported=unsupported, inference=0,
        total=10 + unsupported,
        unsupported_pct=unsupported_pct,
        inference_claims=[],
        unsupported_claims=[f"claim {i}" for i in range(unsupported)],
    )


def _seed_state(max_revisions=2, threshold=5.0):
    """Initial graph state with raw data pre-seeded so the planner never fetches."""
    return {
        "ticker": "AAPL",
        "revisions": 0,
        "max_revisions": max_revisions,
        "threshold": threshold,
        "raw_stock": {"company_name": "Apple Inc.", "current_price": 190},
        "raw_news": [],
        "raw_sec": {},
    }


def _run_graph_with(grade_side_effect):
    """Compile and invoke the graph with every LLM/retrieval call mocked.
    `grade_side_effect` is the sequence of GradeResults the critic returns.
    Returns (final_state, sonnet_mock)."""
    sonnet = MagicMock()
    sonnet.invoke.return_value = MagicMock(content=_BRIEF)
    fixed_plan = {
        "highlights_query": "key takeaways", "risks_query": "primary risks",
        "coverage": [], "sub_questions": [],
    }
    compiled = build_graph().compile()
    with patch.multiple(
        graph,
        _make_plan=MagicMock(return_value=fixed_plan),
        _rag_contexts=MagicMock(return_value=("highlights text", "risks text")),
        _generate_sections=MagicMock(return_value=_SECTIONS),
        _sonnet=sonnet,
        grade_brief=MagicMock(side_effect=grade_side_effect),
    ):
        final = compiled.invoke(_seed_state())
    return final, sonnet


# ── Planner output shape ─────────────────────────────────────────────────────────

def test_planner_node_output_shape():
    """planner_node returns trimmed data + a plan dict with the expected keys."""
    plan_obj = ResearchPlan(
        highlights_query="cloud and AI segment takeaways",
        risks_query="regulatory and supply-chain risks",
        coverage=["valuation", "growth drivers"],
        sub_questions=["How fast is services growing?"],
    )
    planner_llm = MagicMock()
    planner_llm.invoke.return_value = plan_obj

    with patch.object(graph, "_get_planner_llm", return_value=planner_llm):
        out = planner_node(_seed_state())

    assert {"stock", "news", "sec", "company", "context", "plan"} <= out.keys()
    assert out["company"] == "Apple Inc."
    plan = out["plan"]
    assert set(plan.keys()) == {"highlights_query", "risks_query", "coverage", "sub_questions"}
    assert plan["highlights_query"] == "cloud and AI segment takeaways"
    assert plan["coverage"] == ["valuation", "growth drivers"]


def test_make_plan_falls_back_to_defaults_on_error():
    """A planner LLM failure yields the default RAG sub-questions, never a crash."""
    failing = MagicMock()
    failing.invoke.side_effect = RuntimeError("planner API down")

    with patch.object(graph, "_get_planner_llm", return_value=failing):
        plan = _make_plan("Apple Inc.", "AAPL", "some context")

    from agent.core import DEFAULT_HIGHLIGHTS_QUERY, DEFAULT_RISKS_QUERY
    assert plan["highlights_query"] == DEFAULT_HIGHLIGHTS_QUERY
    assert plan["risks_query"] == DEFAULT_RISKS_QUERY
    assert plan["coverage"] == []


def test_make_plan_blank_query_falls_back():
    """A blank highlights_query from the planner is replaced by the default."""
    plan_obj = ResearchPlan(highlights_query="   ", risks_query="real risk query")
    llm = MagicMock()
    llm.invoke.return_value = plan_obj

    with patch.object(graph, "_get_planner_llm", return_value=llm):
        plan = _make_plan("Apple Inc.", "AAPL", "ctx")

    from agent.core import DEFAULT_HIGHLIGHTS_QUERY
    assert plan["highlights_query"] == DEFAULT_HIGHLIGHTS_QUERY
    assert plan["risks_query"] == "real risk query"


# ── Supervisor decision logic (unit) ─────────────────────────────────────────────

def test_supervisor_passes_when_grounded():
    """Unsupported rate at/under threshold → pass, no revision."""
    state = {"critique": _grade(0.0).__dict__, "threshold": 5.0,
             "revisions": 0, "max_revisions": 2}
    out = supervisor_node(state)
    assert out["decision"] == "pass"
    assert "revisions" not in out  # not incremented


def test_supervisor_revises_when_ungrounded_and_budget_left():
    """Over threshold with budget remaining → revise, increment, attach feedback."""
    state = {"critique": _grade(40.0, unsupported=4).__dict__, "threshold": 5.0,
             "revisions": 0, "max_revisions": 2}
    out = supervisor_node(state)
    assert out["decision"] == "revise"
    assert out["revisions"] == 1
    assert "REVISION REQUIRED" in out["feedback"]
    assert "claim 0" in out["feedback"]


def test_supervisor_stops_at_revision_budget():
    """Over threshold but budget exhausted → stop (accept best effort)."""
    state = {"critique": _grade(40.0, unsupported=4).__dict__, "threshold": 5.0,
             "revisions": 2, "max_revisions": 2}
    out = supervisor_node(state)
    assert out["decision"] == "stop"
    assert "revisions" not in out


# ── Full-graph critic retry loop ─────────────────────────────────────────────────

def test_critic_loop_revises_once_then_passes():
    """Judge fails the first draft, passes the revision → research runs twice."""
    final, sonnet = _run_graph_with([_grade(40.0, unsupported=3), _grade(0.0)])

    assert sonnet.invoke.call_count == 2      # initial draft + one revision
    assert final["revisions"] == 1
    assert final["decision"] == "pass"
    assert final["brief"] == _BRIEF

    # The revision pass must carry the critic's feedback at the top of the prompt.
    second_prompt = sonnet.invoke.call_args_list[1].args[0][0].content
    assert second_prompt.startswith("=== REVISION REQUIRED ===")


def test_critic_loop_terminates_at_max_revisions():
    """Judge always fails → loop stops after max_revisions, never unbounded."""
    final, sonnet = _run_graph_with([_grade(40.0, unsupported=3)] * 10)

    # 1 initial draft + max_revisions(2) revisions = 3 synthesis calls, then stop.
    assert sonnet.invoke.call_count == 3
    assert final["revisions"] == 2
    assert final["decision"] == "stop"


def test_no_revision_when_first_draft_is_grounded():
    """A grounded first draft ends immediately — research runs exactly once."""
    final, sonnet = _run_graph_with([_grade(0.0)])

    assert sonnet.invoke.call_count == 1
    assert final["revisions"] == 0
    assert final["decision"] == "pass"
