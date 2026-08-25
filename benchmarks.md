# Local-model serving benchmarks

> ## ⚠️ Read this first: CPU-mode numbers, not comparable to the hosted backend
>
> Everything in this file was measured on a **2017 dual-core laptop CPU**
> (Intel i7-7500U, 2C/4T, AVX2, no GPU) serving the model **CPU-only**. The
> latency and tokens/sec numbers characterize *this environment*, not the
> model or the serving stack — they say nothing about GPU serving, and they
> are **NOT comparable** to the hosted Anthropic API (datacenter GPUs behind
> an HTTP API). Latency columns in the comparison table are marked
> **environment-limited, not comparable** accordingly.
>
> The **valid** cross-backend comparisons are **cost per brief** and
> **grounding score** — those don't depend on how fast this laptop is.

## The vLLM gap, documented

The plan of record was vLLM serving the merged QLoRA checkpoint
(`k8s/vllm/vllm.yaml`, `make vllm-deploy`). What happened on this machine:

1. vLLM has no native Windows support → run the official CPU release image
   (`public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2`) in the WSL2 kind
   cluster, with the merged fp16 checkpoint copied to the node and hostPath-
   mounted.
2. The container **crashed with SIGILL (exit code 132)** immediately after
   platform detection: vLLM's prebuilt CPU binaries require **AVX-512**, and
   the i7-7500U (Kaby Lake) has **AVX2 only**. No AVX2 image tag is published.
3. The remaining route — building vLLM's CPU backend from source targeting
   AVX2 — was ruled out on this machine: the build needs tens of GB of
   toolchain/layer space and the host disk hit 100% during Phase 3 (resolved
   by cleanup; see the commit history), and a 2-core source build of vLLM is
   a multi-hour job with real OOM risk.

**Closest honest alternative, used for every number below:** the same
fine-tuned model (Q4 GGUF quantization of the identical QLoRA merge, 1.6 GB)
served by **Ollama 0.32.15's OpenAI-compatible `/v1/chat/completions`** on the
host, driven through the **same new backend code path**
(`LOCAL_MODEL_BACKEND=openai` in `agent/tools/local_model.py`) that would
target vLLM. On AVX-512-capable hardware, switching to actual vLLM is
configuration only: `make vllm-deploy`, then point `LOCAL_MODEL_URL` at the
vLLM Service — no code change. The vLLM manifests are committed and were
verified to schedule, mount the model, and reach the server process on this
machine; they could not be verified past the AVX-512 SIGILL here.

Two honesty notes on the substitution:
- Ollama serves the **Q4-quantized GGUF** (what the repo has always used for
  `USE_LOCAL_MODEL`), while vLLM would serve the **fp16 safetensors** merge.
  Quantization can shift output quality slightly; the grounding A/B below
  therefore measures the deployed-in-practice artifact, not the fp16 one.
- `scripts/vllm_benchmark.py` measures any OpenAI-compatible endpoint; the
  table below happens to measure Ollama/llama.cpp rather than vLLM.

## Throughput / latency — concurrency sweep (environment-limited)

`python scripts/vllm_benchmark.py --url http://localhost:11434 --model
financial-lora --concurrency 1 4 8 --requests-per-level 16 --max-tokens 256`
— section-generation-shaped prompts (the fine-tune's actual workload), token
counts from server-reported usage, warmup request excluded.

| Concurrency | Requests | p50 (s) | p95 (s) | tok/s per request | aggregate tok/s |
|---:|---:|---:|---:|---:|---:|
| 1 | 16 | 13.32 | 15.52 | 6.06 | 6.14 |
| 4 | 16 | 37.44 | 43.77 | 2.32 | 7.66 |
| 8 | 16 | 74.05 | 80.54 | 1.62 | 7.76 |

Reading: the 2-core CPU saturates at ~7.7 aggregate tok/s. Added concurrency
does not add throughput — it queues (p50 scales ~linearly with concurrency
while aggregate tok/s stays flat). On this hardware the local model is a
cost/privacy play, not a latency play; a GPU deployment would change these
numbers by orders of magnitude, which is exactly why they are labeled
environment-limited.

## Hosted API vs. local model — the comparisons that are valid

### Grounding — full 10-ticker suite, LLM-as-judge, cache bypassed (2026-08-24)

`LOCAL_MODEL_BACKEND=openai python grounding_check.py --arms baseline local-model`
— same retrieval (top-3, no rerank) on both arms; the only difference is who
writes the 2 trained sections. MSFT failed its data fetch after retries and was
excluded from BOTH arms (9 tickers balanced).

| Arm | Tickers | Claims | Supported | Unsupported | Inference | Grounding | Unsup % | Pipeline latency* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hosted (all-Haiku sections) | 9 | 65 | 56 | 0 | 9 | **86.2%** | 0.0% | 27.3s |
| Local hybrid (2 sections on fine-tuned Qwen2.5-1.5B) | 9 | 72 | 56 | 2 | 14 | **77.8%** | 2.8% | 223.0s* |

\* **environment-limited, not comparable** — the local arm's latency is a
2-core CPU serving penalty (plus timeout-retry inflation; the `max_tokens`
bound on the OpenAI path was added after this run), not a property of the
model or of vLLM. The grounding scores are the valid comparison.

**The expected regression is real and reproduces in direction:** the earlier
experiment recorded 88.6% hosted vs 85.4% hybrid; today's judge run scored
86.2% vs 77.8% (this judge pass labeled more claims INFERENCE overall —
grounding % is sensitive to that split; unsupported stayed low on both arms:
0 vs 2 claims). The local model writes less-grounded sections. Nothing here is
hidden: the hybrid trades grounding for local serving.

### Cost per brief — exact API-reported tokens, priced from `model_prices.json` (n=3)

| Backend | Exact (LangChain calls) | RAG-internal (estimated) | **Total/brief** | Total latency (incl. fetch)* |
|---|---:|---:|---:|---:|
| Hosted (all-Haiku sections) | $0.0253 | $0.0063 | **$0.0316** | 45.7s |
| Local hybrid | $0.0258 | $0.0063 | **$0.0321** | 110.0s* |

\* environment-limited (CPU serving), not comparable.

**Honest reframing of the earlier "54% cost reduction":** that figure was the
*section-generation* (Haiku-only) spend. At full-brief level, Sonnet synthesis
dominates (~$0.020/brief), so localizing 2 of 4 Haiku sections saves only
~$0.002/brief on sections (measured: Haiku spend $0.0046 → $0.0028) — **within
run-to-run Sonnet token variance at n=3, i.e. no measurable full-brief
saving**. Token evidence the flag engaged: hybrid Haiku output tokens halved
(569→310, 651→291, 524→338 across the 3 tickers). On this workload the
fine-tune's case is data-privacy/offline serving, not cost — and it costs
grounding. It stays default-off.

## Reproduce

```bash
# throughput sweep (any OpenAI-compatible endpoint)
python scripts/vllm_benchmark.py --url http://localhost:11434 --model financial-lora

# grounding A/B, full 10-ticker suite, cache bypassed
LOCAL_MODEL_BACKEND=openai python grounding_check.py --arms baseline local-model

# cost per brief, exact API-reported tokens priced from scripts/model_prices.json
python scripts/cost_report.py                                   # hosted (all-Haiku sections)
USE_LOCAL_MODEL=true LOCAL_MODEL_BACKEND=openai python scripts/cost_report.py   # hybrid
```
