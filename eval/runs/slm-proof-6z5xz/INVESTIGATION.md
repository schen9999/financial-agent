# Traffic proof FAIL on `grounding-eval-extended-slm-gpu-p4-6z5xz` (2026-10-07)

**Verdict stands: FAIL, not citable** — neither its grounding rate nor its
timings. The EXACT rule is unchanged.

The run: the GPU extended run at parallelism 4 (`argo/eval-run-extended-slm-gpu-p4.yaml`,
image `f3043751`), 22:48–23:10Z; 40/40 tickers on the first attempt, 0
retries, no failed calls, stock block empty 0/40, gate passed. The proof
compared the harness's 353,983 prompt tokens with the server's 353,991
(the `/metrics` prompt counter's movement 352,290 plus the cached-prompt
counter's 1,701): **8 more on the server**. Completion tokens agree
(99,329).

Call by call (`scripts/llamacpp_window_match.py --endpoint slm-gpu`,
against `llamacpp-server-window.log`, node 2's llama.cpp pod log from
22:45Z, pulled read-only after the run):

- 270 server tasks, matched pair for pair with the 270 ledger calls, none
  unmatched; summed 353,983 prompt + 99,329 completion — the harness's
  figures exactly.
- 21 tasks reused an 81-token cached prefix (1,701 tokens), exactly the
  cached counter's movement: at parallelism 4 sibling section calls of one
  ticker run together and share their prompt's opening.
- The server's own log therefore processed 352,282 tokens; the prompt
  counter moved 352,290: **8 above the per-task log**, every request
  accounted for, nothing else on the endpoint.

So, as in `5bdz5` (+1) and `4kkgm` (−4) on the CPU endpoint, and as in the
2026-10-07 capacity replay on this endpoint (−1, −2, −2 with no cache and
no other traffic), only the process-wide counter drifts. Cause not
determined. Settling the proof needs each response's own `timings` in the
LLM ledger (a post-demo image change).

Captured here: counter snapshots, workflow object, pod log, server log
window. Also `eval/runs/raw/6z5xz-findings/`, `eval/runs/6z5xz-claims.jsonl`
and `-contexts/`, the attempts record, the make output
(`eval/runs/gpu-p4-f304375.log`), the chain log and nvidia-smi every 5 s
(`eval/runs/gpu-nvsmi-p4-f304375.csv`). No re-judges were run: the run is
not citable.

```bash
python scripts/llamacpp_window_match.py --dir eval/runs/slm-proof-6z5xz     --log eval/runs/slm-proof-6z5xz/grounding-eval-extended-slm-gpu-p4-6z5xz.log --endpoint slm-gpu
```
