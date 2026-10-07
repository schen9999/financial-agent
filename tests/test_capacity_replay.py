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


def test_percentile_and_table():
    assert cr.percentile([1, 2, 3, 4], 0.5) == 2.5
    s = {"levels": [{"P": 1, "requests": 270, "errors": 0, "wall_s": 600, "requests_per_min": 27.0,
                     "output_tok_per_s": 160.0, "prompt_tok_per_s": 580.0, "latency_p50_s": 1.8,
                     "latency_p95_s": 5.0, "requests_with_cache_hits": 0, "server_matches_requests": True}]}
    assert "| 1 | 270 (0) | 10.0 min | 27.0 | 160.0 | 580.0 | 1.8 s / 5.0 s | 0 | yes |" in cr.table(s)
    json.dumps(s)
