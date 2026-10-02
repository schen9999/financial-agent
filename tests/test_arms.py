"""eval/arms.py — the existing grounding arms must keep running under exactly
the env they always have (golden values), and no flag may leak between arms."""
import os

import pytest

from eval.arms import ARMS, apply_arm_env, arm_env, uses_local_model

# Golden: the full env each pre-existing arm ran under before eval/arms.py.
# Keys added later (e.g. for new arms) must hold their inert value here.
_LEGACY = {
    "baseline":    {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3", "RERANK_CANDIDATES": "20",
                    "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "false"},
    "context5":    {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "5", "RERANK_CANDIDATES": "20",
                    "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "false"},
    "rerank3":     {"RERANKING_ENABLED": "true", "BASELINE_TOP_K": "3", "RERANK_CANDIDATES": "20",
                    "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "false"},
    "rerank5":     {"RERANKING_ENABLED": "true", "BASELINE_TOP_K": "3", "RERANK_CANDIDATES": "20",
                    "RERANK_TOP_N": "5", "USE_LOCAL_MODEL": "false"},
    "local-model": {"RERANKING_ENABLED": "false", "BASELINE_TOP_K": "3", "RERANK_CANDIDATES": "20",
                    "RERANK_TOP_N": "3", "USE_LOCAL_MODEL": "true"},
}
# Inert values of every flag added after the legacy arms.
_INERT_NEW = {"SLM_FULL": "false", "SLM_ENDPOINT": ""}


@pytest.mark.parametrize("arm", sorted(_LEGACY))
def test_legacy_arm_env_unchanged(arm):
    env = arm_env(arm)
    legacy_keys = {k: v for k, v in env.items() if k in _LEGACY[arm]}
    assert legacy_keys == _LEGACY[arm]
    extra = {k: v for k, v in env.items() if k not in _LEGACY[arm]}
    assert all(_INERT_NEW.get(k) == v for k, v in extra.items()), extra


def test_legacy_labels_unchanged():
    assert ARMS["baseline"]["label"] == "Baseline (top_k=3, no rerank)"
    assert ARMS["local-model"]["label"] == "Local model (2 sec) + Haiku"


def test_no_leak_between_arms(monkeypatch):
    for k in list(os.environ):
        if k in arm_env("baseline"):
            monkeypatch.delenv(k, raising=False)
    apply_arm_env("local-model")
    apply_arm_env("rerank5")
    apply_arm_env("baseline")
    for k, v in arm_env("baseline").items():
        assert os.environ[k] == v
        monkeypatch.setenv(k, v)  # restored by monkeypatch on teardown


def test_uses_local_model():
    assert uses_local_model("local-model")
    assert not any(uses_local_model(a) for a in ("baseline", "context5", "rerank3", "rerank5"))


@pytest.mark.parametrize("arm,ep", [("slm-full-cpu", "cpu"), ("slm-full-gpu", "gpu")])
def test_slm_arms(arm, ep):
    from eval.arms import slm_endpoint_name, uses_slm
    env = arm_env(arm)
    assert (env["SLM_FULL"], env["SLM_ENDPOINT"], env["USE_LOCAL_MODEL"]) == ("true", ep, "false")
    # same retrieval settings as the baseline it is compared against
    assert (env["RERANKING_ENABLED"], env["BASELINE_TOP_K"]) == ("false", "3")
    assert uses_slm(arm) and slm_endpoint_name(arm) == f"slm-{ep}"
    assert not any(uses_slm(a) for a in _LEGACY)
