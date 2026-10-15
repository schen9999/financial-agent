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


# CPU endpoint (slm-cpu), pinned 2026-10-15 before the 40-ticker CPU rerun on
# f3043751: the CPU build logs chunked "prompt processing, progress" lines
# between a task's start and its timings, and its /metrics counter drifted -4
# in 4kkgm while every request matched. Neither may move the verdict.
def _cpu_task(n, prompt, gen):
    return (f"4298.29.805.917 I slot print_timing: id  0 | task {n} | prompt processing, n_tokens =   {prompt // 2}, progress = 0.50, t =  20.40 s / 87.22 tokens per second\n"
            f"4298.48.113.665 I slot print_timing: id  0 | task {n} | prompt processing, n_tokens =   {prompt}, progress = 1.00, t =  38.70 s / 59.19 tokens per second\n"
            f"4300.42.366.427 I slot print_timing: id  0 | task {n} | prompt eval time =   73073.57 ms /  {prompt} tokens (   31.69 ms per token,    31.56 tokens per second)\n"
            f"4300.42.366.434 I slot print_timing: id  0 | task {n} |        eval time =   79883.52 ms /   {gen} tokens (  166.08 ms per token,     6.02 tokens per second)\n"
            f"4300.42.366.440 I slot      release: id  0 | task {n} | stop processing: n_tokens = {prompt + gen - 1}, truncated = 0\n")


def _cpu_call(pod, seq, prompt, comp, err=None):
    c = {"endpoint": "slm-cpu", "seq": seq, "prompt_tokens": prompt, "completion_tokens": comp, "error": err}
    return f"[pod/{pod}/main] EVAL_LLM_CALL {json.dumps(c)}\n"


def test_cpu_log_with_progress_lines_must_pass():
    server = _cpu_task(116379, 2295, 482) + _cpu_task(116380, 2306, 700)
    log = _cpu_call("wf-eval-one-1", 1, 2295, 482) + _cpu_call("wf-eval-one-2", 1, 2306, 700)
    r = tp.verdict(tp.server_tasks(server), tp.harness_calls(log, "slm-cpu"))
    assert r["verdict"] == "TASK-EXACT" and r["server_tasks"] == 2 and r["prompt_tokens"] == 4601


def test_cpu_drifted_counter_is_reported_and_does_not_decide():
    r = tp.verdict(tp.server_tasks(_cpu_task(1, 2295, 482)), tp.harness_calls(_cpu_call("p", 1, 2295, 482), "slm-cpu"))
    before = {"counters": {"prompt_tokens_total": 1000, "prompt_tokens_cached_total": 0, "tokens_predicted_total": 0}}
    after = {"counters": {"prompt_tokens_total": 1000 + 2295 - 4, "prompt_tokens_cached_total": 0,
                          "tokens_predicted_total": 482}}
    c = tp.counter_report(before, after, r)
    assert (c["counter_minus_harness_prompt"], c["counter_minus_harness_completion"]) == (-4, 0)
    assert r["verdict"] == "TASK-EXACT"


def test_cpu_timed_out_call_must_fail_no_lower_bound():
    # The server finished the task after the client gave up (SLM_TIMEOUT): the
    # harness logged the call as errored with no usage. Per-request has no
    # LOWER-BOUND verdict, so this is FAIL even though the excess is explained.
    server = _cpu_task(1, 2295, 482) + _cpu_task(2, 3000, 4096)
    log = _cpu_call("p", 1, 2295, 482) + _cpu_call("p", 2, None, None, err="ReadTimeout")
    r = tp.verdict(tp.server_tasks(server), tp.harness_calls(log, "slm-cpu"))
    assert r["verdict"] == "FAIL" and r["errored_calls"] == 1
    assert r["unmatched_server"] == [(3000, 4096)] and r["unmatched_harness"] == [(0, 0)]


def test_other_endpoints_calls_are_not_counted_against_cpu():
    log = _cpu_call("p", 1, 2295, 482) + _call("p", 2, 100, 20)        # slm-gpu call in the same log
    r = tp.verdict(tp.server_tasks(_cpu_task(1, 2295, 482)), tp.harness_calls(log, "slm-cpu"))
    assert r["verdict"] == "TASK-EXACT" and r["harness_calls"] == 1
