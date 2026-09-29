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
over the timed run = output_len x (completed + 1), the +1 being the
client's initial test request), then recomputes the count-dependent
metrics with the client's formulas at the true length:

  output_throughput        = output_len x completed / duration
  total_token_throughput   = (total_input_tokens + output tokens) / duration
  TPOT per request         = (E2E - TTFT) / (output_len - 1), E2E - TTFT
                             being the sum of that request's ITLs

Lost requests. llama-server answers with "Keep-Alive: timeout=5, max=100"
but closes the connection itself, its FIN in the same packet as the
stream's final "data: [DONE]" chunk (every one of 217 served connections
in a packet capture, 2026-09-29). The client pools the connection as
reusable; a request that picks it up before the FIN is read is written to
a closing socket and fails with aiohttp's ServerDisconnectedError while
awaiting the response headers, never reaching the server. The client does
not retry. Seen on 2026-09-29: 0-1 of 200 lost per F16 concurrency-8 run
(SSE pings on or off), 3 of 200 on Q8_0, whose requests end faster. A
lost request frees its concurrency slot at once, so the server's load is
unchanged. A run is accepted with such losses only if every error is that
one, the server count above holds for the completed requests (proving the
lost ones generated nothing), and at most 1% of prompts are lost (at
least one allowed). A 5% limit was considered once the mechanism was
measured and not adopted: no committed result needs it (the Q8_0 run with
3 of 200 lost was refused and its rerun lost none). Indices of the lost
requests go in "lost_requests"; the metrics, as the client computes them,
cover the completed requests. Any other error refuses the run.

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
TRANSPORT_LOSS = "ServerDisconnectedError"
MAX_LOST_PCT = 1


def percentile(xs, p):
    """numpy.percentile's default (linear) method."""
    s = sorted(xs)
    k = (len(s) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def is_transport_loss(error):
    """Disconnected while awaiting the response headers: never served."""
    return TRANSPORT_LOSS in error and "resp.start" in error


def fix(d, output_len, predicted, processed):
    n, done = d["num_prompts"], d["completed"]
    errors = d.get("errors") or [""] * n
    lost = [i for i, e in enumerate(errors) if e]
    other = [errors[i] for i in lost if not is_transport_loss(errors[i])]
    if other or done + len(lost) != n:
        raise ValueError(f"completed {done} of {n}; first errors: "
                         f"{(other or [errors[i] for i in lost])[:2]}")
    if len(lost) > max(1, n * MAX_LOST_PCT // 100):
        raise ValueError(f"lost {len(lost)} of {n} requests to {TRANSPORT_LOSS} "
                         f"(limit {MAX_LOST_PCT}%)")
    if predicted != output_len * (done + 1):
        raise ValueError(f"server generated {predicted} tokens, want {output_len} x ({done} + 1)")
    ok = [i for i in range(n) if not errors[i]]
    ttfts = [d["ttfts"][i] for i in ok]
    decode = [sum(d["itls"][i]) for i in ok]
    e2e_ms = [1000 * (t + s) for t, s in zip(ttfts, decode)]
    # TTFT comes from its own perf_counter() call, microseconds off the chunk time
    if abs(statistics.mean(e2e_ms) - d["mean_e2el_ms"]) > 1e-4 * d["mean_e2el_ms"]:
        raise ValueError("per-request TTFT + ITLs do not reproduce the client's mean E2E")
    tpots = [1000 * s / (output_len - 1) for s in decode]
    out = {k: v for k, v in d.items() if k not in DETAIL_KEYS}
    out["client_retokenized"] = {k: d[k] for k in COUNT_KEYS}
    tokens = output_len * done
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
        "lost_requests": lost,
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
