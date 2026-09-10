"""Critic recall on injected failures — PAID test, gated.

Runs the real temperature-0 Sonnet judge over the committed 20-fixture
perturbation set (eval/perturbed/fixtures.jsonl) and asserts recall >= 0.8.
Costs ~20 judge calls, so it is skipped unless explicitly armed:

  CRITIC_INJECTION=1 python -m pytest tests/test_critic_injection.py -q -s

The .github/workflows/critic-injection.yml job arms it in CI.
Measured 2026-09-04 on the committed fixture set: recall 20/20
(95% CI 83.9-100%), precision vs tags 71.4% (52.9-84.7%, lower bound).
Do not lower the 0.8 bar if this regresses — report the number.
"""
import json
import os
import pathlib

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("CRITIC_INJECTION") != "1",
    reason="paid Sonnet judge calls — set CRITIC_INJECTION=1 (and provide "
           "ANTHROPIC_API_KEY) to run",
)

FIXTURES = pathlib.Path(__file__).resolve().parents[1] / "eval" / "perturbed" / "fixtures.jsonl"


def test_recall_on_injected_failures_at_least_080():
    from eval.critic_check import run_fixtures

    fixtures = [json.loads(ln) for ln in
                FIXTURES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(fixtures) == 20
    result = run_fixtures(fixtures)
    print(json.dumps({k: result[k] for k in
                      ("n", "detected", "recall", "recall_ci_95",
                       "precision", "precision_ci_95")}, indent=2))
    assert result["recall"] >= 0.8, (
        f"critic recall on injected failures dropped to {result['recall']:.2f} "
        f"(CI {result['recall_ci_95']}). Do NOT lower the bar — investigate, "
        f"and report the measured number in docs/numbers-of-record.md."
    )
