# Traffic proof FAIL on `grounding-eval-extended-slm-cpu-4kkgm` (2026-10-06)

**Verdict stands: FAIL, not citable.** The EXACT rule is unchanged; there
is no third CPU attempt (runbook, rules recorded before the run).

The proof compared the harness's 353,901 prompt tokens with the server's
353,897 — the `/metrics` prompt counter's movement (353,890; `…-before.json`
1,079,860 → `…-after.json` 1,433,750) plus its cached-prompt counter (7).
Completion tokens agree (99,078).

Call by call (`scripts/llamacpp_window_match.py`, against
`llamacpp-server-window.log`, the CPU endpoint pod's log from 17:50 UTC,
pulled read-only after the run):

- 270 server tasks ran, matching the harness's 270 `slm-cpu` calls pair for
  pair on (prompt, completion) tokens, with none unmatched on either side.
  Summed: 353,901 prompt + 99,078 completion — the harness's figures exactly.
- Prompt tokens per task are read as release `n_tokens` − generated + 1,
  the same consistency as in `5bdz5`; all 270 tasks have every line.
- One task reused a cached prefix: task 148914, 640 prompt tokens, 633
  processed and 7 from the cache (`section:risk_factors`, 204 completion
  tokens). That is the counter's 7 cached tokens exactly.
- The server's own log therefore has 353,894 tokens processed. The
  `/metrics` prompt counter moved 353,890: **4 fewer than the server's
  own per-task log**, with every request accounted for.
- No outside traffic: the before-snapshot equals `5bdz5`'s after-snapshot
  (1,079,860; nothing ran between the runs), and the log window holds
  exactly the 270 tasks.

So, as in `5bdz5`, every request matches and only the `/metrics` counter
drifts. **Cause not determined.**

## Pattern across the traffic proofs

| Endpoint | Run | Kind | Proof | Counters − harness, prompt tokens |
|---|---|---|---|---|
| GPU | `k6zxd` | smoke, 1f51dad | EXACT | 0 (7,883 cached tokens) |
| GPU | `p9jr2` | extended, 1f51dad | EXACT | 0 |
| GPU | `m7qvv` | smoke, f3043751 | EXACT | 0 |
| GPU | `nstp9` | extended, f3043751 | EXACT | 0 |
| CPU | `nb6r6` | smoke, 2dd1aa3 | EXACT | 0 |
| CPU | `9jddz` | smoke, 30c832b | FAIL, explained | not comparable: a failed attempt's calls were unrecorded on that image |
| CPU | `wnrjr` | smoke, 1f51dad | EXACT | 0 |
| CPU | `8vpq6` | extended, 1f51dad | EXACT | 0 |
| CPU | `xnwjm` | smoke, f3043751 | EXACT | 0 |
| CPU | `5bdz5` | extended, f3043751 | FAIL | +1 (no cached tokens) |
| CPU | `4kkgm` | extended, f3043751 | FAIL | −4 (7 cached tokens) |

Counters = the prompt counter's movement plus the cached-prompt
counter's, as the proof computes it; the snapshots are in each run's
`slm-proof-*` folder. Only `5bdz5` and `4kkgm` have a server log window, so
only they are also matched per task; there the per-task log equals the
harness exactly.

- Both unexplained drifts are on the CPU endpoint, on the two most recent
  CPU extended runs, back to back on one pod (counters continuous, no
  restart). The GPU endpoint is EXACT on all four of its runs. Four CPU
  runs on the same endpoint were EXACT, `8vpq6` among them, an extended
  run of the same length.
- The drifts differ in sign (+1, −4), so they are not a fixed offset.
- Cache reuse does not explain them: `5bdz5` had no cached tokens, and
  `k6zxd` (GPU) reused 7,883 and was EXACT.
- Two events are too few to call it CPU-specific. Nothing here changes the
  rule.

Settling it needs each response's own `timings` (prompt and cached token
counts per request) in the LLM ledger, so the harness compares against
per-request server figures rather than a process-wide counter. That changes
image code: it remains a post-demo ledger change.

```bash
python scripts/llamacpp_window_match.py --dir eval/runs/slm-proof-4kkgm \
    --log eval/runs/slm-proof-4kkgm/grounding-eval-extended-slm-cpu-4kkgm.log
python scripts/llamacpp_window_match.py --dir eval/runs/slm-proof-5bdz5 \
    --log eval/runs/slm-proof-5bdz5/grounding-eval-extended-slm-cpu-5bdz5.log
```

## Addendum (2026-10-07): the drift reproduced on the GPU endpoint

The A10 capacity sweep (`eval/runs/capacity-sweep-2026-10-07/`,
`scripts/capacity_replay.py`) replayed `nstp9`'s 270 calls three times
against the GPU endpoint, from node 2 itself, with nothing else using it
and the prompt cache off. Each time the requests' own timings summed
exactly to the tokens sent (352,522 prompt, 98,665 generated) and the
cached-prompt counter did not move, yet `/metrics` `prompt_tokens_total`
moved 352,521, 352,520 and 352,520: 1, 2 and 2 tokens short. The
generated-token counter was exact. So the process-wide prompt counter can
miss by a token or two with no outside traffic and no cache, on either
endpoint (the four GPU eval proofs were nonetheless EXACT). The rule is
unchanged; per-request `timings` in the ledger remain the fix.

