"""scripts/traffic_proof_tasks.py: the per-request traffic proof passes only
when every server task in the window matches a harness call and vice versa;
the /metrics counter is reported, never deciding. Synthetic logs only (the
runs judged by the counter proof are not re-scored)."""
import json

from scripts import traffic_proof_tasks as tp


def _task(n, prompt, gen, processed=None):
    processed = prompt if processed is None else processed
    return (f"I slot print_timing: id  0 | task {n} | prompt eval time =   10.0 ms /  {processed} tokens (x)\n"
            f"I slot print_timing: id  0 | task {n} |        eval time =   20.0 ms /  {gen} tokens (x)\n"
            f"I slot      release: id  0 | task {n} | stop processing: n_tokens = {prompt + gen - 1}, truncated = 0\n")


def _call(pod, seq, prompt, comp, err=None):
    c = {"endpoint": "slm-gpu", "seq": seq, "prompt_tokens": prompt, "completion_tokens": comp, "error": err}
    return f"[pod/{pod}/main] EVAL_LLM_CALL {json.dumps(c)}\n"


def test_exact_match_passes_and_cached_prefix_counts_as_prompt():
    server = _task(1, 100, 20) + _task(2, 300, 40, processed=219)       # 81 tokens reused from cache
    log = _call("wf-eval-one-1", 1, 100, 20) + _call("wf-eval-one-1", 2, 300, 40) \
        + _call("wf-aggregate-9", 1, 100, 20)                            # aggregate reprint ignored
    r = tp.verdict(tp.server_tasks(server), tp.harness_calls(log, "slm-gpu"))
    assert r["verdict"] == "TASK-EXACT" and r["server_cached_prefix_tokens"] == 81


def test_extra_server_task_or_missing_task_fails():
    log = _call("p", 1, 100, 20)
    assert tp.verdict(tp.server_tasks(_task(1, 100, 20) + _task(2, 50, 5)),
                      tp.harness_calls(log, "slm-gpu"))["unmatched_server"] == [(50, 5)]
    r = tp.verdict(tp.server_tasks(""), tp.harness_calls(log, "slm-gpu"))
    assert r["verdict"] == "FAIL" and r["unmatched_harness"] == [(100, 20)]
    incomplete = "I slot print_timing: id  0 | task 7 | prompt eval time =   1.0 ms /  9 tokens (x)\n"
    assert tp.verdict(tp.server_tasks(_task(1, 100, 20) + incomplete),
                      tp.harness_calls(log, "slm-gpu"))["incomplete_tasks"] == [7]


def test_counter_is_reported_not_deciding():
    r = tp.verdict(tp.server_tasks(_task(1, 100, 20)), tp.harness_calls(_call("p", 1, 100, 20), "slm-gpu"))
    before = {"counters": {"prompt_tokens_total": 0, "prompt_tokens_cached_total": 0, "tokens_predicted_total": 0}}
    after = {"counters": {"prompt_tokens_total": 102, "prompt_tokens_cached_total": 0, "tokens_predicted_total": 20}}
    c = tp.counter_report(before, after, r)
    assert c["counter_minus_harness_prompt"] == 2 and r["verdict"] == "TASK-EXACT"
