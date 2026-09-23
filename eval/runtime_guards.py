"""Fail-loud guards for the eval harness.

Kept import-light (stdlib only) so both the harness and the test suite can
use it without pulling the model stack.
"""
import json
import urllib.request


def check_local_model_served(url: str, name: str, timeout: float = 15.0) -> list[str]:
    """Confirm the OpenAI-compatible server at `url` lists `name` on
    /v1/models; return the served ids, or raise SystemExit.

    Guards the local-model arm against measuring the wrong model: after a
    model swap, LOCAL_MODEL_NAME and the vLLM deployment can disagree, and
    every section request would then 404 (or, worse, a stale deployment
    would answer). One check before any ticker runs, instead of discovering
    it from a gate failure afterwards.
    """
    endpoint = f"{url.rstrip('/')}/v1/models"
    try:
        with urllib.request.urlopen(endpoint, timeout=timeout) as resp:
            ids = [m.get("id") for m in json.load(resp).get("data", [])]
    except Exception as e:  # noqa: BLE001 — any failure here is fatal by design
        raise SystemExit(
            f"FATAL: local-model arm, but {endpoint} is unreachable or not an "
            f"OpenAI-compatible /v1/models: {type(e).__name__}: {e}\n"
            "  Is vLLM rolled out? (make vm-vllm)"
        )
    if name not in ids:
        raise SystemExit(
            f"FATAL: local-model arm expects LOCAL_MODEL_NAME={name!r}, but "
            f"{endpoint} serves {ids}.\n"
            "  Swap models with `make vm-vllm ...` — it rolls out vLLM and sets "
            "LOCAL_MODEL_NAME together."
        )
    return ids


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
