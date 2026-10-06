# Traffic proof FAIL on `grounding-eval-extended-slm-cpu-5bdz5` (2026-10-06)

**Verdict stands: FAIL, not citable.** The EXACT rule is unchanged.

The server's prompt-token counter moved 346,636 over the run
(`…-before.json` 733,224 → `…-after.json` 1,079,860; the cached-prompt
counter did not move); the harness logged 346,635 prompt tokens over 270
calls. Completion tokens agree (98,042).

What the server's own log shows (`llamacpp-server-window.log`: the CPU
endpoint pod's log from 05:50 UTC, pulled read-only from the cluster; the
pod has not restarted since 2026-10-03):

- 270 tasks ran, matching the harness's 270 `slm-cpu` calls pair for pair
  on (prompt, completion) tokens; summed, 346,635 prompt + 98,042
  completion — the harness's figures exactly.
- Every task's own count is consistent (tokens at release = prompt +
  generated − 1, all 270).
- No outside traffic: the counters were identical at the CPU smoke's
  after-snapshot and this run's before-snapshot (733,224); no task ran
  after the last eval call (08:22:32); nothing in the harness calls a
  token-counting route other than chat completions; the pod's probes hit
  `/health` only.

So the counter moved by one token outside any logged request. **Cause not
determined.** The evidence that would settle it is each response's own
`timings` (prompt and cache token counts), which the LLM ledger does not
record — recording it changes image code, so it is a post-demo ledger
change.
