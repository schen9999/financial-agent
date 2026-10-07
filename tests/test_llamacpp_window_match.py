"""scripts/llamacpp_window_match.py on the committed CPU proof failures:
every server task pairs with a ledger call, and only the /metrics counter
is off (5bdz5 +1, 4kkgm -4 against the server's own per-task log)."""
import json
from pathlib import Path

from scripts import llamacpp_window_match as wm

RUNS = Path(__file__).resolve().parents[1] / "eval" / "runs"


def _match(run):
    d = RUNS / f"slm-proof-{run}"
    load = lambda p: json.loads(next(d.glob(p)).read_text(encoding="utf-8"))  # noqa: E731
    tasks = wm.server_tasks((d / "llamacpp-server-window.log").read_text(encoding="utf-8"))
    log = (d / f"grounding-eval-extended-slm-cpu-{run}.log").read_text(encoding="utf-8", errors="replace")
    return wm.match(tasks, wm.ledger_calls(log, "slm-cpu"), load("*-before.json"), load("*-after.json"))


def test_every_request_pairs_and_only_the_counter_drifts():
    for run, prompt, drift in (("5bdz5", 346635, +1), ("4kkgm", 353901, -4)):
        m = _match(run)
        assert m["server_tasks"] == m["harness_calls"] == 270
        assert m["unmatched_server"] == m["unmatched_harness"] == []
        assert m["server_prompt_sum"] == m["harness_prompt_sum"] == prompt
        assert m["server_generated_sum"] == m["harness_completion_sum"]
        assert m["counter_delta"]["prompt_tokens_total"] - m["server_processed_sum"] == drift
