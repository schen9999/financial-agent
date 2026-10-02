"""Eval arms: the env overrides each grounding_check.py arm applies.

Lives outside grounding_check.py so tests can import it — the harness itself
mutates the environment and reconfigures stdout at import time. Config in
agent/core, agent/tools/rag and agent/tools/reranker is read at call time, so
toggling these in-process re-routes the next call.
"""
import os

ARMS = {
    "baseline": {
        "label": "Baseline (top_k=3, no rerank)",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3"},
    },
    "context5": {
        "label": "Plain top-5 (no rerank)",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "5"},
    },
    "rerank3": {
        "label": "Rerank 20 -> 3",
        "env": {"RERANKING_ENABLED": "true", "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "3"},
    },
    "rerank5": {
        "label": "Rerank 20 -> 5",
        "env": {"RERANKING_ENABLED": "true", "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "5"},
    },
    "local-model": {
        # Fine-tuned Qwen2.5-1.5B (Ollama) serves the 2 trained sections
        # (Financial Health, Risk Factors); Haiku keeps Recent Developments and
        # SEC Filing Highlights. Requires `ollama serve` + the model loaded.
        "label": "Local model (2 sec) + Haiku",
        "env": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3", "USE_LOCAL_MODEL": "true"},
    },
}

# Every arm explicitly sets the flags it depends on so values can't leak across
# arms within one process. Fill in the ones an arm leaves unset with inert
# defaults (e.g. a baseline arm still resets RERANKING_ENABLED / USE_LOCAL_MODEL).
ARM_ENV_DEFAULTS = {
    "RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3",
    "RERANK_CANDIDATES": "20", "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "false",
}


def arm_env(arm: str) -> dict:
    """The complete env an arm runs under: inert defaults, then its overrides."""
    return {**ARM_ENV_DEFAULTS, **ARMS[arm]["env"]}


def apply_arm_env(arm: str):
    # Reset every controlled flag to its inert default, then apply this arm's
    # overrides — so no flag leaks from the previously-run arm.
    for k, v in arm_env(arm).items():
        os.environ[k] = v


def uses_local_model(arm: str) -> bool:
    return ARMS[arm]["env"].get("USE_LOCAL_MODEL") == "true"
