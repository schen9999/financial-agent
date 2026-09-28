#!/usr/bin/env python3
"""cost_per_brief_selfhost.py: A10 cost of serving the two locally written
sections (Financial Health + Risk Factors) per brief, beside the hosted cost
of the same work.

Reads only committed artifacts; runs no model and no eval. Per local run:

  tokens/brief  Output tokens of the FH + RF text recorded in the run's
                findings (`## Pre-written sections`, the raw section
                outputs), counted with the Qwen2.5 tokenizer, plus one
                end-of-sequence token per section unless it hit the cap.
                An estimate: the recorded text, re-tokenized.
  cap           2 x max_tokens from the run's recorded sampling metadata:
                the most the two sections can generate, an upper bound.
  throughput    Output tok/s from eval/runs/bench/<served-name>.json
                (vllm bench serve on the A10, max concurrency 8).
  pipeline s    Mean Pipe(s) from eval/runs/<run>-aggregate.txt: retrieval
                + sections + synthesis per brief, as measured in the eval.

Figures, with H = --gpu-hourly-usd:

  (a) at benchmarked concurrency: H / 3600 x tokens / throughput
      (the A10's time per brief when it is kept busy at concurrency 8)
  (b) one brief at a time: H / 3600 x pipeline s
      (the A10 is billed for the whole brief, including the time the
      pipeline spends on retrieval, the Haiku sections and synthesis)

Hosted side: the Haiku line of the cost of record's run evidence
(cost_record_post_fix.json) covers all four Haiku sections; the harness does
not split it per section, so it is an upper bound on the two-section cost.
Break-even briefs/hour = H / that bound, so it is a lower bound.

Usage:
  python scripts/cost_per_brief_selfhost.py --gpu-hourly-usd 2.00
  python scripts/cost_per_brief_selfhost.py --gpu-hourly-usd 2.00 --run cnkp2
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.label import parse_findings_file  # noqa: E402
from eval.section_attribution import canonical_section  # noqa: E402

DEFAULT_RUNS = ["v924f", "4nfsm", "cnkp2"]
# One tokenizer for all three arms: Qwen2.5-1.5B-Instruct and -7B-Instruct
# ship the same tokenizer, and the merged fine-tune keeps its base's vocab.
DEFAULT_TOKENIZER = "Qwen/Qwen2.5-1.5B-Instruct"
HOSTED_MODEL = "claude-haiku-4-5-20251001"
LOCAL = ("financial-health", "risk-factors")
EXPECTED_ORDER = ["financial-health", "recent-developments",
                  "sec-filing-highlights", "risk-factors"]
_HEAD_RE = re.compile(r"^### [^\n]+$", re.M)
_PIPE_RE = re.compile(r"^\s*TOTAL\s+(?:\d+\s+){4}([\d.]+)\s+([\d.]+)\s*$", re.M)
_LOCAL_MODEL_RE = re.compile(r"^\s*local model\s*:\s*(\S+)", re.M)


def split_sections(block: str) -> dict:
    """Canonical section -> its text as generated (heading line included).
    Raises if the block is not exactly the four sections in pipeline order,
    so a mis-split can never be counted."""
    starts = [m.start() for m in _HEAD_RE.finditer(block)]
    if not starts or block[:starts[0]].strip():
        raise ValueError("section block does not start with a ### heading")
    chunks = [block[s:e].rstrip() for s, e in zip(starts, starts[1:] + [len(block)])]
    names = [canonical_section(c.split("\n", 1)[0][4:]) for c in chunks]
    if names != EXPECTED_ORDER:
        raise ValueError(f"unexpected section headings {names}")
    return dict(zip(names, chunks))


def section_tokens(n_text_tokens: int, max_tokens: int) -> int:
    """Generated tokens for one section: text + EOS, or the cap if reached."""
    return min(n_text_tokens + 1, max_tokens)


def gpu_cost_at_throughput(hourly: float, tokens: float, tok_per_s: float) -> float:
    return hourly / 3600 * tokens / tok_per_s


def gpu_cost_one_at_a_time(hourly: float, pipeline_s: float) -> float:
    return hourly / 3600 * pipeline_s


def read_run(runs_dir: Path, run: str, tokenizer) -> dict:
    findings = sorted((runs_dir / "raw" / f"{run}-findings").glob("*.md"))
    if not findings:
        raise SystemExit(f"no findings for run {run}")
    served, max_tokens, per_brief, at_cap = None, None, [], 0
    for f in findings:
        parsed = parse_findings_file(f.read_text(encoding="utf-8"))
        meta = (parsed or {}).get("metadata", {})
        if "local_model_served_name" not in meta or "section_block" not in parsed:
            raise SystemExit(f"{f.name}: not a local-model findings file")
        name = meta["local_model_served_name"]
        cap = json.loads(meta["local_model_sampling"])["max_tokens"]
        if (served, max_tokens) not in ((None, None), (name, cap)):
            raise SystemExit(f"{run}: findings disagree on model or max_tokens")
        served, max_tokens = name, cap
        secs = split_sections(parsed["section_block"])
        total = 0
        for sec in LOCAL:
            n = len(tokenizer.encode(secs[sec], add_special_tokens=False).ids)
            at_cap += n >= cap
            total += section_tokens(n, cap)
        per_brief.append(total)

    bench = json.loads((runs_dir / "bench" / f"{served}.json").read_text(encoding="utf-8"))
    agg = (runs_dir / f"{run}-aggregate.txt").read_text(encoding="utf-8")
    m_model, m_pipe = _LOCAL_MODEL_RE.search(agg), _PIPE_RE.search(agg)
    if not m_model or m_model.group(1) != served or not m_pipe:
        raise SystemExit(f"{run}: aggregate does not match served model {served}")
    return {
        "run": run, "served": served, "briefs": len(per_brief),
        "tokens_mean": sum(per_brief) / len(per_brief), "tokens_max": max(per_brief),
        "sections_at_cap": at_cap, "cap": 2 * max_tokens,
        "tok_per_s": bench["output_throughput"],
        "bench_concurrency": bench["max_concurrency"],
        "pipeline_s": float(m_pipe.group(2)),
    }


def hosted_four_section_cost(path: Path) -> tuple[float, int]:
    runs = json.loads(path.read_text(encoding="utf-8"))["runs"]
    costs = [r["exact_by_model"][HOSTED_MODEL]["cost_usd"] for r in runs]
    return sum(costs) / len(costs), len(costs)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--gpu-hourly-usd", type=float, required=True,
                    help="A10 price per hour (no default: take it from the current price list)")
    ap.add_argument("--run", action="append", dest="runs",
                    help=f"local-model run ID (repeatable; default {' '.join(DEFAULT_RUNS)})")
    ap.add_argument("--runs-dir", type=Path, default=ROOT / "eval" / "runs")
    ap.add_argument("--hosted-cost-json", type=Path, default=ROOT / "cost_record_post_fix.json")
    ap.add_argument("--tokenizer", default=DEFAULT_TOKENIZER)
    args = ap.parse_args()
    h = args.gpu_hourly_usd
    if h <= 0:
        raise SystemExit("--gpu-hourly-usd must be positive")

    from tokenizers import Tokenizer
    tokenizer = Tokenizer.from_pretrained(args.tokenizer)
    rows = [read_run(args.runs_dir, r, tokenizer) for r in (args.runs or DEFAULT_RUNS)]
    hosted, n_hosted = hosted_four_section_cost(args.hosted_cost_json)

    print(f"A10 at ${h:.2f}/hour; tokens counted with {args.tokenizer}\n")
    for r in rows:
        est, cap = r["tokens_mean"], r["cap"]
        print(f"{r['run']}  {r['served']}  ({r['briefs']} briefs)")
        print(f"  FH+RF output tokens/brief: {est:.0f} mean (max {r['tokens_max']}), "
              f"cap {cap}; sections at cap: {r['sections_at_cap']}")
        print(f"  (a) at concurrency {r['bench_concurrency']}, {r['tok_per_s']:.1f} tok/s: "
              f"${gpu_cost_at_throughput(h, est, r['tok_per_s']):.5f}/brief "
              f"(cap ${gpu_cost_at_throughput(h, cap, r['tok_per_s']):.5f}); "
              f"capacity {3600 * r['tok_per_s'] / est:.0f} briefs/hour "
              f"(cap {3600 * r['tok_per_s'] / cap:.0f})")
        print(f"  (b) one brief at a time, {r['pipeline_s']:.2f} s/brief: "
              f"${gpu_cost_one_at_a_time(h, r['pipeline_s']):.4f}/brief; "
              f"at most {3600 / r['pipeline_s']:.0f} briefs/hour\n")
    print(f"Hosted: all four Haiku sections ${hosted:.4f}/brief "
          f"(mean of {n_hosted}, {args.hosted_cost_json.name}); "
          f"the two local sections cost at most this")
    print(f"Break-even: at least {h / hosted:.0f} briefs/hour sustained "
          f"before the A10 costs less than the hosted sections it replaces")


if __name__ == "__main__":
    main()
