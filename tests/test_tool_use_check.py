"""eval/tool_use_check.py — mechanical scoring of the ReAct tool loop."""
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from eval.tool_use_check import QUESTIONS, score_trace


def _call(name, i="c1"):
    return {"name": name, "args": {"ticker": "AAPL"}, "id": i, "type": "tool_call"}


def test_question_set_is_fixed_and_covers_every_tool():
    assert len(QUESTIONS) == 10
    assert {q[2] for q in QUESTIONS} == {"get_stock_data", "get_company_news",
                                         "get_sec_filings", "query_sec_filing"}


def test_correct_complete_loop():
    trace = [HumanMessage("q"), AIMessage("", tool_calls=[_call("get_stock_data")]),
             ToolMessage("{}", tool_call_id="c1"), AIMessage("P/E is 38.6.")]
    s = score_trace(trace, "get_stock_data")
    assert (s["tool_calls"], s["invalid_tool_calls"]) == (1, 0)
    assert s["expected_called"] and s["expected_first"] and s["completed"]


def test_wrong_tool_and_invalid_call_counted():
    bad = AIMessage("", tool_calls=[_call("get_company_news")],
                    invalid_tool_calls=[{"name": "get_stock_data", "args": "{x", "id": "c2",
                                         "error": "bad json", "type": "invalid_tool_call"}])
    s = score_trace([HumanMessage("q"), bad, ToolMessage("[]", tool_call_id="c1"),
                     AIMessage("News says...")], "get_stock_data")
    assert (s["tool_calls"], s["invalid_tool_calls"]) == (1, 1)
    assert not s["expected_called"] and s["completed"]


def test_no_tool_call_answer_is_complete_but_wrong():
    s = score_trace([HumanMessage("q"), AIMessage("I think it's about 30.")], "get_stock_data")
    assert s["completed"] and not s["expected_called"] and s["tool_calls"] == 0


def test_ending_on_pending_tool_call_or_empty_is_incomplete():
    assert not score_trace([HumanMessage("q"), AIMessage("", tool_calls=[_call("get_stock_data")])],
                           "get_stock_data")["completed"]
    assert not score_trace([HumanMessage("q"), AIMessage("  ")], "get_stock_data")["completed"]
    assert not score_trace([], "get_stock_data")["completed"]
