# Did v924f and r5nzh run the same pipeline? (checked 2026-09-29)

Question: does the BF16 fine-tune run `v924f` (2026-09-23) differ from the
W4A16 run `r5nzh` (2026-09-29) only in the weights' precision? Checked on
`vm-a10-inst-2` over ssh (read-only: kubectl, crictl, docker inspect, git)
and in this repo. **Answer: yes.** Same app image, same WorkflowTemplate
object, equivalent eval-run parameters, identical vLLM serving args; the
weights directory, served name and date differ.

## App image

| Evidence | Finding |
|---|---|
| r5nzh pods (41, still present) | every pod's `imageID` is `sha256:290d2933a9e3e3ea575ffac2a2f62c7b52fcb82de4dfcb32626664de7841f8a0`, 2026-09-29 05:03:29-05:27:04 UTC |
| k3s image `290d2933` | tag `financial-agent-app:local`, config `created` 2026-09-23T22:13:05.128620766Z, 11 layers, top layer `sha256:15ca2a51…` |
| docker build on the node | `financial-agent-app:local` id `94f17c4d4fae`, created 2026-09-23T22:13:05.128620766Z, 11 layers, same top layer: the same image |
| import time (containerd config blob mtime) | `290d2933` 2026-09-23 22:13:14 UTC; the only other app images, now untagged, were imported 20:47:07 and 22:04:52 the same day. No app image was imported after 22:13:14 |
| v924f run window (pod log timestamps in `eval/runs/raw/v924f.log`) | 2026-09-23 22:43:57-23:07:29 UTC, after the 22:13:14 import |

v924f's pods were deleted, so its imageID is not recorded directly. It is
inferred: the app pods use the local tag with pullPolicy Never, the tag
resolved to `290d2933` from 22:13:14 on, and no later import exists.

## Code in the image

The node's checkout was at `c309627` (branch model-compare) from 22:12:58
UTC (reflog: `pull: Fast-forward`) until 2026-09-24 00:25, so the 22:13:05
build used `c309627`. Checked directly: sha256 of all 27 `.py` files
under `agent/`, `eval/`, `grounding_check.py` and `cache.py` inside the
image equals `git show c309627:<path>`; 0 differ, none missing from
`agent/`.

The node's checkout later moved to `d029397` (2026-09-24 07:49, HEAD
during r5nzh). That does not reach the pods, which run the image's code,
and `git diff c309627 d029397 -- agent/` is empty anyway. The rest of
that diff is committed run data, offline analysis scripts
(`eval/build_fourarm_holdout.py`, `eval/multi_arm_stats.py`), bench
helpers, and a Makefile readiness poll in `vm-vllm`; `argo/`, `k8s/`,
`grounding_check.py`, `Dockerfile.k8s` and `requirements.txt` are
unchanged.

## Eval configuration

| Evidence | Finding |
|---|---|
| WorkflowTemplate `grounding-eval` | created 2026-09-23T20:48:19Z, `generation` 1: its spec has not changed since creation, so both runs used the same template |
| Eval-run files | v924f: `argo/eval-run-extended-local.yaml` at `c309627`; r5nzh: `argo/eval-run-extended-local-w4a16.yaml` (added in fb68d6c). They differ only in comments and `generateName`. r5nzh's live Workflow spec: same template ref, `activeDeadlineSeconds` 10800, `arms=local-model`, the same 40 tickers |
| Sampling | both aggregate headers print `{"max_tokens": 512, "min_p": 0.0, "repetition_penalty": 1.1, "temperature": 0.1, "top_k": 20, "top_p": 0.8}` |

## vLLM serving

ReplicaSets of `deployment/vllm` (history limit 10, 4 present, none
pruned):

| ReplicaSet created | Weights (hostPath) | Args |
|---|---|---|
| 2026-09-23 20:48:19 (BF16; the only fine-tune BF16 template; serving during v924f, the next ReplicaSet appears 23:09:44) | `/home/ubuntu/models/qwen-ft` | `--served-model-name=financial-lora --dtype=bfloat16 --max-model-len=4096 --max-num-seqs=8 --gpu-memory-utilization=0.90` |
| 2026-09-29 04:58:01 (W4A16) | `/home/ubuntu/models/qwen-ft-w4a16` | `--served-model-name=financial-lora-w4a16 --dtype=bfloat16 --max-model-len=4096 --max-num-seqs=8 --gpu-memory-utilization=0.90` |

Both on `vllm/vllm-openai:v0.10.2`, same node.

## What does differ

- The weights: BF16 `qwen-ft` vs GPTQ W4A16 `qwen-ft-w4a16` (with
  `--dtype=bfloat16`, activations stay 16-bit).
- The served name (recorded in each aggregate header).
- The date, six days apart: live inputs (news, yfinance, RAG answer text)
  can drift between runs; the stock dict each brief was checked against is
  the one that run fetched, so the numeric check compares each brief with
  its own inputs.
