"""scripts/capacity_replay.py: the plan reproduces the recorded run's ledger,
prompts are cut to the recorded length exactly, every request's prefix is
distinct, and the level table reads the server-side check."""
import json

from scripts import capacity_replay as cr

ROOT = cr.Path(__file__).resolve().parents[1]
LOG = ROOT / "eval/runs/slm-proof-nstp9/grounding-eval-extended-slm-gpu-nstp9.log"


def test_plan_reproduces_the_nstp9_ledger():
    plan = cr.make_plan("nstp9", LOG, ROOT / "eval/runs/nstp9-contexts", "slm-gpu")
    c = plan["calls"]
    assert len(c) == 270                                   # the traffic proof's call count
    assert sum(x["prompt_tokens"] for x in c) == 352522 and sum(x["completion_tokens"] for x in c) == 98665
    assert max(x["prompt_tokens"] + x["completion_tokens"] for x in c) == 4215


def test_ledger_dedupes_repeated_lines_and_skips_the_aggregate():
    line = '[pod/wf-eval-one-1/main] EVAL_LLM_CALL {"endpoint": "slm-gpu", "error": null, "seq": 1, "site": "s", "prompt_tokens": 5, "completion_tokens": 2}'
    agg = line.replace("eval-one-1", "aggregate-9")
    assert len(cr.ledger_calls("\n".join([line, line, agg]), "slm-gpu")) == 1


def test_prompts_are_exact_length_with_a_distinct_prefix():
    pool = list(range(1000, 1100))
    for n in (3, 50, 250):
        p = cr.build_prompt(pool, [1, 2, 3], n, offset=17)
        assert len(p) == n and p[:3] == [1, 2, 3]
    assert cr.build_prompt(pool, [1, 2, 3, 4], 2, offset=0) == [1, 2]


def test_level_stats_counts_server_side_and_reads_the_counter_gap():
    rows = [{"i": 0, "site": "s", "target_prompt": 10, "target_completion": 4, "sent_prompt": 10,
             "latency_s": 2.0, "error": None, "prompt_n": 10, "predicted_n": 4, "tokens_cached": 13},
            {"i": 1, "site": "s", "target_prompt": 20, "target_completion": 5, "sent_prompt": 20,
             "latency_s": 4.0, "error": None, "prompt_n": 18, "predicted_n": 5, "tokens_cached": 24}]
    delta = {"prompt_tokens_total": 27.0, "tokens_predicted_total": 9.0, "prompt_tokens_cached_total": 2.0}
    lv = cr.level_stats(rows, delta, wall=60.0)
    assert lv["requests_with_cache_reuse"] == 1          # sent - prompt_n, not tokens_cached
    assert lv["counter_minus_requests"] == {"prompt": -1.0, "generated": 0.0}
    assert not lv["server_matches_requests"] and lv["requests_per_min"] == 2.0
    lv["P"] = 1
    assert "| 1 | 2 (0) | 1.0 min | 2.0 | 0.1 | 0.5 | 3.0 s / 3.9 s | 1 | -1, +0 |" in cr.table({"levels": [lv]})
    assert cr.percentile([1, 2, 3, 4], 0.5) == 2.5
    json.dumps(lv)
