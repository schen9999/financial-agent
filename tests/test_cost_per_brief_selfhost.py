"""scripts/cost_per_brief_selfhost.py: the A10 cost-per-brief arithmetic,
the four-section split that must refuse a mis-parsed block, the token cap,
and reading one run from committed-shape artifacts. A whitespace tokenizer
stands in for Qwen2.5 so nothing is downloaded."""
import importlib.util
import json
import pathlib

import pytest

_MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "cost_per_brief_selfhost.py"
_spec = importlib.util.spec_from_file_location("cost_per_brief_selfhost", _MOD_PATH)
cps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cps)


class _Enc:
    def __init__(self, ids):
        self.ids = ids


class WordTokenizer:
    """One token per whitespace-separated word."""
    def encode(self, text, add_special_tokens=False):
        return _Enc(text.split())


BLOCK = """### Financial Health
one two three

### Recent Developments
haiku text here

### SEC Filing Highlights
more haiku text

### Risk Factors
- a b"""

FINDINGS = """# {t} — local-model

## Metadata

ticker: {t}
arm: local-model
judge_prompt_version: v2
local_model_served_name: {served}
local_model_sampling: {{"max_tokens": {cap}, "temperature": 0.1}}

## Retrieved source context

ctx

## Pre-written sections (judge input)

{block}

## Audited (Exec Summary + Outlook)

### Executive Summary
x

## Judge findings

f
"""

AGGREGATE = """  judge prompt      : v2
  local model       : {served} (dir d, openai @ http://vllm:8000)
  Ticker    Sup  Uns  Inf  Tot  Retr(s)  Pipe(s)
  --------------------------------------------
  AAPL        7    0    0    7    14.11    35.79
  --------------------------------------------
  TOTAL     353   18   22  393    10.74    32.72
"""


def _write_run(tmp_path, run="r1", served="m7b", cap=512, blocks=(BLOCK,), tok_s=200.0):
    fdir = tmp_path / "raw" / f"{run}-findings"
    fdir.mkdir(parents=True)
    for i, block in enumerate(blocks):
        (fdir / f"T{i}_local-model.md").write_text(
            FINDINGS.format(t=f"T{i}", served=served, cap=cap, block=block), encoding="utf-8")
    (tmp_path / "bench").mkdir(exist_ok=True)
    (tmp_path / "bench" / f"{served}.json").write_text(
        json.dumps({"output_throughput": tok_s, "max_concurrency": 8}), encoding="utf-8")
    (tmp_path / f"{run}-aggregate.txt").write_text(AGGREGATE.format(served=served), encoding="utf-8")
    return run


def test_split_sections_keeps_heading_and_order():
    secs = cps.split_sections(BLOCK)
    assert list(secs) == cps.EXPECTED_ORDER
    assert secs["financial-health"] == "### Financial Health\none two three"
    assert secs["risk-factors"] == "### Risk Factors\n- a b"


def test_split_sections_refuses_extra_heading():
    # A model sub-heading would shift text between sections: refuse, don't count.
    block = BLOCK.replace("one two three", "one\n### Liquidity\ntwo")
    with pytest.raises(ValueError):
        cps.split_sections(block)


def test_split_sections_refuses_leading_text():
    with pytest.raises(ValueError):
        cps.split_sections("preamble\n" + BLOCK)


def test_section_tokens_adds_eos_until_cap():
    assert cps.section_tokens(100, 512) == 101
    assert cps.section_tokens(511, 512) == 512
    assert cps.section_tokens(512, 512) == 512   # truncated: no EOS


def test_cost_formulas():
    # (a) H/3600 * T/R: 1024 tokens at 194.6 tok/s on a $2.00/h A10
    assert cps.gpu_cost_at_throughput(2.00, 1024, 194.6) == pytest.approx(0.0029231, rel=1e-4)
    # (b) H/3600 * P
    assert cps.gpu_cost_one_at_a_time(2.00, 32.72) == pytest.approx(0.0181778, rel=1e-4)
    assert cps.gpu_cost_one_at_a_time(3600.0, 1.0) == 1.0


def test_read_run_counts_only_local_sections(tmp_path):
    run = _write_run(tmp_path)
    r = cps.read_run(tmp_path, run, WordTokenizer())
    # FH "### Financial Health one two three" = 6 words + EOS; RF "### Risk Factors - a b" = 6 + EOS
    assert r["tokens_mean"] == 14
    assert r["cap"] == 1024
    assert r["sections_at_cap"] == 0
    assert r["served"] == "m7b"
    assert r["tok_per_s"] == 200.0
    assert r["pipeline_s"] == 32.72


def test_read_run_counts_capped_sections(tmp_path):
    run = _write_run(tmp_path, cap=5)
    r = cps.read_run(tmp_path, run, WordTokenizer())
    assert r["sections_at_cap"] == 2
    assert r["tokens_mean"] == 10


def test_read_run_rejects_aggregate_for_another_model(tmp_path):
    run = _write_run(tmp_path)
    agg = tmp_path / f"{run}-aggregate.txt"
    agg.write_text(AGGREGATE.format(served="other-model"), encoding="utf-8")
    with pytest.raises(SystemExit):
        cps.read_run(tmp_path, run, WordTokenizer())


def test_read_run_rejects_mixed_caps(tmp_path):
    run = _write_run(tmp_path, blocks=(BLOCK, BLOCK))
    f = tmp_path / "raw" / f"{run}-findings" / "T1_local-model.md"
    f.write_text(f.read_text(encoding="utf-8").replace('"max_tokens": 512', '"max_tokens": 256'),
                 encoding="utf-8")
    with pytest.raises(SystemExit):
        cps.read_run(tmp_path, run, WordTokenizer())


def test_hosted_four_section_cost_is_mean_haiku_line(tmp_path):
    p = tmp_path / "cost.json"
    p.write_text(json.dumps({"runs": [
        {"exact_by_model": {cps.HOSTED_MODEL: {"cost_usd": 0.006}, "claude-sonnet-4-6": {"cost_usd": 1.0}}},
        {"exact_by_model": {cps.HOSTED_MODEL: {"cost_usd": 0.004}}},
    ]}), encoding="utf-8")
    assert cps.hosted_four_section_cost(p) == (pytest.approx(0.005), 2)


def test_committed_cost_record_gives_the_cited_bound():
    # The page cites "at most $0.0055" and break-even "at least 363" at $2.00/h.
    root = pathlib.Path(__file__).resolve().parents[1]
    c, n = cps.hosted_four_section_cost(root / "cost_record_post_fix.json")
    assert n == 3
    assert round(c, 4) == 0.0055
    assert round(2.00 / c) == 363
