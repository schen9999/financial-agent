"""Fail-loud guards for the eval harness.

Kept import-light (stdlib only) so both the harness and the test suite can
use it without pulling the model stack.
"""


def check_fatal_api_error(exc: BaseException) -> None:
    """Raise SystemExit for API errors that retrying cannot fix and that
    would otherwise surface as silently skipped tickers.

    Currently: the Anthropic 400 "credit balance is too low". Measured
    failure mode (2026-09-03): the per-ticker retry exhausted on it, the
    ticker was recorded as skipped, and the gate failed with a message
    indistinguishable from a data problem.
    """
    if "credit balance" in str(exc).lower():
        raise SystemExit(
            "FATAL: Anthropic credit balance too low — stopping this eval run now.\n"
            f"  underlying error: {exc}\n"
            "  Without this guard the failure surfaces as skipped tickers and a\n"
            "  confusing gate failure. Top up credits, then re-run.\n"
            "  (In the Argo DAG this fails the pod, and the workflow, loudly.)"
        )
