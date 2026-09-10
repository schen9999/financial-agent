"""eval/runtime_guards.py — credit-balance errors must fail loudly."""
import pytest

from eval.runtime_guards import check_fatal_api_error


def test_credit_balance_error_raises_system_exit():
    err = Exception(
        "Error code: 400 - {'error': {'message': 'Your credit balance is too "
        "low to access the Anthropic API.'}}"
    )
    with pytest.raises(SystemExit) as exc:
        check_fatal_api_error(err)
    assert "credit balance too low" in str(exc.value)
    assert "skipped tickers" in str(exc.value)


def test_ordinary_errors_pass_through():
    assert check_fatal_api_error(ConnectionError("connection reset")) is None
    assert check_fatal_api_error(TimeoutError("timed out")) is None
