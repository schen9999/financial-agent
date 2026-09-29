#!/usr/bin/env python3
"""Put exact output-token counts into a llama-server `vllm bench serve` result.

`vllm bench serve` v0.10.2 reads a response's usage only from a stream chunk
without choices; llama-server puts usage in the same chunk as its last
(empty) choice, so the client counts output tokens by re-tokenizing the
generated text, which undercounts (about 1% on 2026-09-29, F16, c=8).
Output throughput and TPOT depend on that count; TTFT, ITL and E2E do not.

With --ignore-eos, llama-server bans end-of-generation tokens, so every
completed request generates exactly --random-output-len tokens. This
script checks that on the server's own counter (llamacpp:tokens_predicted
over the timed run = output_len x (prompts + 1), the +1 being the client's
initial test request), then recomputes the count-dependent metrics with the
client's formulas at the true length:

  output_throughput        = output_len x completed / duration
  total_token_throughput   = (total_input_tokens + output tokens) / duration
  TPOT per request         = (E2E - TTFT) / (output_len - 1), E2E - TTFT
                             being the sum of that request's ITLs

The client's own figures are kept under "client_retokenized". Input: a
result saved with --save-detailed; the bulky per-request arrays are
replaced by per-request TTFT and decode seconds (enough to recompute).

Usage (called by scripts/vm_bench_cpu_gguf.sh):
  bench_fix_llamacpp.py <bench.json> <output-len> <tokens-predicted> <prompt-tokens-processed>
"""
import json
import statistics
import sys

COUNT_KEYS = ("total_output_tokens", "output_throughput", "total_token_throughput",
              "mean_tpot_ms", "median_tpot_ms", "std_tpot_ms",
              "p50_tpot_ms", "p90_tpot_ms", "p99_tpot_ms")
DETAIL_KEYS = ("input_lens", "output_lens", "ttfts", "itls", "generated_texts", "errors")


def percentile(xs, p):
    """numpy.percentile's default (linear) method."""
    s = sorted(xs)
    k = (len(s) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def fix(d, output_len, predicted, processed):
    n = d["num_prompts"]
    errors = [e for e in d.get("errors", []) if e]
    if d["completed"] != n:
        raise ValueError(f"completed {d['completed']} of {n}; first errors: {errors[:2]}")
    if predicted != output_len * (n + 1):
        raise ValueError(f"server generated {predicted} tokens, want {output_len} x ({n} + 1)")
    ttfts = d["ttfts"]
    decode = [sum(itl) for itl in d["itls"]]
    e2e_ms = [1000 * (t + s) for t, s in zip(ttfts, decode)]
    # TTFT comes from its own perf_counter() call, microseconds off the chunk time
    if abs(statistics.mean(e2e_ms) - d["mean_e2el_ms"]) > 1e-4 * d["mean_e2el_ms"]:
        raise ValueError("per-request TTFT + ITLs do not reproduce the client's mean E2E")
    tpots = [1000 * s / (output_len - 1) for s in decode]
    out = {k: v for k, v in d.items() if k not in DETAIL_KEYS}
    out["client_retokenized"] = {k: d[k] for k in COUNT_KEYS}
    tokens = output_len * n
    out.update({
        "total_output_tokens": tokens,
        "output_throughput": tokens / d["duration"],
        "total_token_throughput": (d["total_input_tokens"] + tokens) / d["duration"],
        "mean_tpot_ms": statistics.mean(tpots), "median_tpot_ms": statistics.median(tpots),
        "std_tpot_ms": statistics.pstdev(tpots),
        "p50_tpot_ms": percentile(tpots, 50), "p90_tpot_ms": percentile(tpots, 90),
        "p99_tpot_ms": percentile(tpots, 99),
        "output_token_source": "llama-server tokens_predicted (ignore_eos); "
                               "client re-tokenized count under client_retokenized",
        "llamacpp_tokens_predicted": predicted,
        "llamacpp_prompt_tokens_processed": processed,
        "request_ttfts_s": ttfts, "request_decode_s": decode,
    })
    return out


def main(argv=None):
    path, output_len, predicted, processed = (argv or sys.argv[1:])
    d = json.load(open(path, encoding="utf-8"))
    try:
        print(json.dumps(fix(d, int(output_len), int(predicted), int(processed))))
    except ValueError as e:
        sys.exit(f"refused: {e}")


if __name__ == "__main__":
    main()
