import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage, HumanMessage

import agent.react_agent as react_agent_module


def test_answer_question_end_to_end():
    """Graph is invoked with ticker context; last AIMessage content is returned."""
    mock_graph = MagicMock()
    mock_graph.invoke.return_value = {
        "messages": [
            HumanMessage(content="Ticker: AAPL. What is the P/E ratio?"),
            AIMessage(content="Apple's trailing P/E ratio is approximately 28.5."),
        ]
    }

    with patch.object(react_agent_module, "_graph", mock_graph):
        result = react_agent_module.answer_question("AAPL", "What is the P/E ratio?")

    assert isinstance(result, str)
    assert len(result) > 0
    assert "28.5" in result
    mock_graph.invoke.assert_called_once()
    invocation = mock_graph.invoke.call_args[0][0]
    assert "AAPL" in invocation["messages"][0].content


def test_answer_question_fallback_on_empty_messages():
    """Returns fallback string when no AIMessage is present in the response."""
    mock_graph = MagicMock()
    mock_graph.invoke.return_value = {"messages": []}

    with patch.object(react_agent_module, "_graph", mock_graph):
        result = react_agent_module.answer_question("AAPL", "anything")

    assert result == "Could not generate an answer."


def test_answer_question_skips_tool_call_messages():
    """AIMessage with tool_calls is not returned as the final answer."""
    tool_call_msg = AIMessage(content="")
    tool_call_msg.tool_calls = [{"name": "get_stock_data", "args": {}, "id": "1"}]
    final_msg = AIMessage(content="The current price is $185.")

    mock_graph = MagicMock()
    mock_graph.invoke.return_value = {
        "messages": [
            HumanMessage(content="Ticker: AAPL. What is the price?"),
            tool_call_msg,
            final_msg,
        ]
    }

    with patch.object(react_agent_module, "_graph", mock_graph):
        result = react_agent_module.answer_question("AAPL", "What is the price?")

    assert "$185" in result
