# GPU inference on the A10

What has been served on an NVIDIA A10 (24 GB, VM.GPU.A10.1), how fast,
at what cost, and what has not run. Measured facts only; every figure
links to its record. Anything inferred is marked **(inferred)**. None of
these figures is a number of record unless it says so.

## What has run on the A10

| Date | Engine | Model | Where | Record |
|---|---|---|---|---|
| 2026-09-02 | vLLM v0.10.2 | the merged QLoRA fine-tune of Qwen2.5-1.5B (`financial-lora`) | plain Docker, one A10 | [deploy-runbook.md](deploy-runbook.md) |
| 2026-09-03 | vLLM v0.10.2 | `financial-lora` | in-cluster, single-node k3s (`k8s/vllm/overlays/k3s-gpu`) | [eval-methodology.md](eval-methodology.md#dated-ab-on-the-single-vm-target-2026-09-03) |
| 2026-09-23 | vLLM v0.10.2 | `financial-lora`; untuned Qwen2.5-1.5B and Qwen2.5-7B (swapped with `make vm-vllm`) | both VM.GPU.A10.1 nodes, k3s | [numbers-of-record.md](numbers-of-record.md#dated-run-records) |
| 2026-09-29 | vLLM v0.10.2 | `financial-lora` quantized GPTQ W4A16 (llm-compressor, Marlin kernels) | `vm-a10-inst-2`, k3s | [eval-methodology.md](eval-methodology.md#a10-bf16-vs-w4a16) |
| 2026-10-03 onward | llama.cpp b11347 (CUDA 12.8.1 build) | Qwen3.6-35B-A3B, `ggml-org` Q4_K_M GGUF, all layers on the A10 (llama-server held 20,488 of 23,028 MiB) | `vm-a10-inst-2`, k3s, keyed on NodePort 30880 | [deploy-runbook.md](deploy-runbook.md#slm-endpoints-qwen36-35b-a3b-on-llamacpp-cpu-on-oke-gpu-on-node-2) |

## vLLM on the fine-tune: BF16 vs W4A16 (a dated measurement)

The fine-tuned Qwen2.5-1.5B, BF16 against its GPTQ W4A16 quantization,
vLLM v0.10.2, one A10 on `vm-a10-inst-2` (k3s pod), 2026-09-28 (BF16) and
2026-09-29 (W4A16). Same client, prompt shape, seeds and prompts on both
sides: concurrency 8 × 200 prompts (seed 1) and concurrency 1 × 50 (seed
2), each after a 16-prompt warmup, with the app pods scaled to 0. Source:
[eval-methodology.md, "A10: BF16 vs W4A16"](eval-methodology.md#a10-bf16-vs-w4a16);
raw results in
[`eval/runs/bench/a10-2026-09-28/`](../eval/runs/bench/a10-2026-09-28/) and
[`eval/runs/bench/a10-quant-2026-09-29/`](../eval/runs/bench/a10-quant-2026-09-29/).

| | BF16 | W4A16 | Ratio |
|---|---|---|---|
| Output tok/s, concurrency 8 | **708.3** | **1,075.7** | 1.52× |
| Output tok/s, concurrency 1 | 111.1 | 190.9 | 1.72× |
| Median time per output token, concurrency 1 | 8.8 ms | 5.0 ms | |
| Median time per output token, concurrency 8 | 10.5 ms | 6.4 ms | |
| **Median time to first token, concurrency 8** | **197 ms** | **286 ms** | slower |
| Median time to first token, concurrency 1 | 52 ms | 58 ms | slower |
| Weights on disk | 3.09 GB | 1.61 GB | |

- Decode got faster and prefill got slower: the 4-bit build trades a
  higher time to first token for throughput.
- Serving speed only. On grounding, the W4A16 arm (`r5nzh`, 6.69%) and the
  BF16 fine-tune (`v924f`, 6.49%) showed no detectable difference (Fisher
  p = 1.00, judge v2, 40 tickers;
  [eval-methodology.md](eval-methodology.md#grounding-w4a16-vs-the-bf16-fine-tune)).
- The fine-tune itself is not used: it failed the grounding gate against
  hosted models (8.15% vs 3.06% unsupported, p = 0.0023, judge v2), so
  `USE_LOCAL_MODEL` ships off
  ([numbers-of-record.md](numbers-of-record.md#dated-run-records)).

## Why the Qwen3.6 model runs on llama.cpp, not vLLM

Computed from the published artifacts, **not booted**
([dated finding](eval-methodology.md#dated-finding-computed-not-booted-no-4-bit-qwen36-35b-a3b-fits-one-a10-under-vllm-2026-10-02)):

- Qwen publishes Qwen3.6-35B-A3B in BF16 and FP8 only. FP8 has no native
  support on the A10's Ampere generation, and its weights exceed 24 GB.
- The community 4-bit builds take 20.3–21.9 GiB for the language model
  alone. The best case leaves 1.04 GiB of the A10 at 95% memory
  utilization for the CUDA context, activations and KV cache, against a
  harness sending up to about 8 concurrent requests of up to about 5k
  tokens.
- Node 2's driver (570.124.06) supports CUDA 12.8. vLLM 0.19.0, the first
  version with the fix for this architecture's quantized layers,
  publishes no CUDA 12.8 image.

llama.cpp's CUDA 12.8.1 build serves the same Q4_K_M GGUF with all layers
on the A10.

## Why Qwen3.6-35B-A3B and not MiniMax or a smaller Qwen (computed, not booted, 2026-10-15)

**Why it was chosen, as recorded at selection time (2026-10-02, before
any run).** The reason is in the owner's planning notes of 2026-10-02,
written right after Sanjay Basu replied "you serve a minimax or qwen"; the
commits that introduced the model (`1a417be`, `02ddf2e`, `eb7b1b9`) record
what was chosen and how it is pinned, not why. The notes give four reasons:

- **MiniMax:** every open MiniMax model is a large MoE (M2.5 230B total,
  10B active; M2.7 about 108 GB at 4 bits; M3 428B), estimated then not to
  fit the A10 (24 GB) or the largest E5 node (~58 GiB allocatable).
- **Qwen3.6-35B-A3B:** about 3B active parameters per token, chosen for
  CPU generation speed: the efficient-MoE profile MiniMax has, at a size
  that can be served here.
- **One file for both:** one ~20 GB Q4 file fits both one E5 node and one
  A10, so the same model and harness compare CPU against GPU serving.
- **Basu named Qwen as acceptable.**

The dense Qwen models were not explicitly weighed at selection time. The
fit table below and the measured CPU numbers came afterwards: they support
the choice, they were not the reasoning behind it, and nothing here says
how a dense model would have performed. What follows are fit facts,
computed from the published files, and the measured speed of the one model
that ran.

**Fit, computed from the published files.** File sizes are each repo's
GGUF files at a pinned revision, all shards summed, the vision projector
and draft-model files excluded (`scripts/hf_gguf_fit.py`, output
`eval/runs/gguf-fit-2026-10-15.txt`). Parameter counts are from each
model card (linked), and the totals were checked against the safetensors
metadata. Budgets: the A10's 23,028 MiB (22.49 GiB) as nvidia-smi reports
it; the largest allocatable memory on an OKE E5 node, about 58 GiB; the
CPU endpoint's pod limit today, 30 GiB.

**Every "fits" below is as served, not weights only.** "As served" means
the file plus what llama.cpp allocates for the harness's context, about 8
concurrent requests of up to about 5k tokens, taken as 8 × 5,120 = 40,960
tokens (`scripts/kv_state_fit.py`, output
`eval/runs/kv-state-fit-2026-10-15.txt`, from each model's `config.json`
at a pinned revision):

- the KV cache of every full-attention layer, at f16 (llama.cpp's default);
- the recurrent state of every linear-attention (Gated DeltaNet) layer,
  at f32, per request (the Qwen3.5/3.6 models are hybrids, with three
  linear layers to each full one);
- a 1 GiB allowance for compute buffers and the CUDA context. This is an
  **assumption**, not measured per model.

A build whose file fits but which does not fit with the rest is marked
**weights only: does not fit as served**. Cross-check on the one deployed
configuration: for the GPU endpoint as deployed (4 slots sharing 32,768
tokens), the file plus KV plus state comes to 20,367 MiB, against the
20,488 MiB llama-server held (2026-10-03). The difference is 121 MiB, and
the 1 GiB allowance is above it.

| Model (card) | Total / active parameters | Quantized build @ revision | Smallest build | Q4_K_M | Q8_0 | KV + state at 8 × 5,120 tokens | The A10 (22.49 GiB), as served | An E5 node (~58 GiB), as served |
|---|---|---|---|---|---|---|---|---|
| [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) (MoE) | 35B / 3B | [`ggml-org/Qwen3.6-35B-A3B-GGUF`](https://huggingface.co/ggml-org/Qwen3.6-35B-A3B-GGUF) @`baec3eb` | — | **19.02 GiB** | 34.37 GiB | 0.78 + 0.49 GiB | Q4_K_M fits as served, 1.20 GiB left (ran: 20,488 MiB held at 4 × 8,192 tokens); Q8_0 no (file exceeds) | Q4_K_M and Q8_0 fit as served (36.71 and 21.36 GiB left) |
| [Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) (dense) | 27B / 27B | [`ggml-org/Qwen3.6-27B-GGUF`](https://huggingface.co/ggml-org/Qwen3.6-27B-GGUF) @`8a7ee08` | — | 17.78 GiB | 26.63 GiB | 2.50 + 1.17 GiB | Q4_K_M **marginal**: 0.04 GiB left, inside the uncertainty of the assumed allowance; Q8_0 no (file exceeds) | Q4_K_M and Q8_0 fit as served (35.55 and 26.70 GiB left) |
| [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) (dense) | 9.7B / 9.7B | [`unsloth/Qwen3.5-9B-GGUF`](https://huggingface.co/unsloth/Qwen3.5-9B-GGUF) @`3885219` | UD-IQ2_XXS 2.97 GiB | 5.29 GiB | 8.87 GiB | 1.25 + 0.39 GiB | every build listed fits as served (Q8_0: 10.97 GiB left) | every build listed fits as served |
| [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) (dense) | 4.7B / 4.7B | [`unsloth/Qwen3.5-4B-GGUF`](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF) @`e87f176` | UD-IQ2_XXS 1.42 GiB | 2.55 GiB | 4.17 GiB | 1.25 + 0.39 GiB | every build listed fits as served (Q8_0: 15.67 GiB left) | every build listed fits as served |
| [MiniMax-M2.7](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) (MoE) | 229B / 10B ¹ | [`unsloth/MiniMax-M2.7-GGUF`](https://huggingface.co/unsloth/MiniMax-M2.7-GGUF) @`d2a05cc` | UD-IQ1_M 56.53 GiB | 130.54 GiB (UD-Q4_K_M) | 226.44 GiB | 9.69 GiB (KV only) | no build (the smallest file exceeds by 34.04 GiB) | UD-IQ1_M **weights only: does not fit as served** (9.22 GiB short) |
| [MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5) (MoE) | 229B / 10B ¹ | [`unsloth/MiniMax-M2.5-GGUF`](https://huggingface.co/unsloth/MiniMax-M2.5-GGUF) @`7c50dca` | UD-TQ1_0 51.94 GiB | 128.84 GiB | 226.44 GiB | 9.69 GiB (KV only) | no build (the smallest file exceeds by 29.45 GiB) | UD-TQ1_0 **weights only: does not fit as served** (4.62 GiB short) |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3) (MoE, multimodal) | ~428B / ~23B | [`unsloth/MiniMax-M3-GGUF`](https://huggingface.co/unsloth/MiniMax-M3-GGUF) @`abdce34` | UD-IQ1_M 120.43 GiB | 246.73 GiB (UD-Q4_K_M) | 422.46 GiB | 4.69 GiB (KV only ²) | no build | no build (the smallest file exceeds by 62.43 GiB) |

¹ The [MiniMax-M2 card](https://huggingface.co/MiniMaxAI/MiniMax-M2) states
230B total and 10B active; the M2.5 and M2.7 cards state neither, but their
`config.json` files match M2's in every size field (62 layers, hidden size
3,072, 256 experts, 8 per token) and their safetensors totals are 228.7B
parameters each. Every M2.x layer is full attention (`attn_type_list` all
1), so their KV cache at this context is large: 248 KiB per token.
² M3's sparse-attention index keys are not counted; it is out of both
budgets on its file alone.

- **No MiniMax open-weight build fits either budget as served** (the
  2026-10-02 estimate, now computed). None fits
  the A10 even on weights. On an E5 node the smallest M2.5 and M2.7 builds
  (about 2 bits per weight on average: UD-TQ1_0 1.95, UD-IQ1_M 2.12, file
  bytes over parameters) fit on weights alone, with 6.06 and 1.47 GiB
  left. Their KV cache at the harness's context takes 9.69 GiB, so they
  fall 4.62 and 9.22 GiB short as served. A smaller context or fewer
  concurrent requests would change that; no such configuration was
  computed or run. None fits the CPU endpoint's 30 GiB pod even on
  weights. The M2.x Q4_K_M builds (about 129–131 GiB) are under node 2's
  240 GB of host memory, so they could run there only with most experts in
  host RAM: a **hybrid** layout in this project's terms. None of this was
  booted.
- **The smaller Qwens fit both budgets as served at Q4_K_M, the 27B on the
  A10 only marginally** (0.04 GiB left, less than the uncertainty in the
  assumed 1 GiB allowance, so it may not fit). The 9B and 4B have room to
  spare at Q8_0. In the 30 GiB CPU pod, every Qwen Q4_K_M fits as served;
  the 27B's Q8_0 is weights only (1.30 GiB short). None was served or
  evaluated in this project, so nothing is said about its speed or what it
  would write.
- **The model that ran fits the A10 as served with 1.20 GiB left** at 8 ×
  5,120 tokens (computed). As deployed, at 4 × 8,192 tokens, it held
  20,488 MiB (measured).
- MiniMax-M3 is above both budgets in every build, the 1-bit-class ones
  included.

**What 3B active means for CPU generation, measured on the one model that
ran.** On the OKE E5 node (AMD EPYC 9J14, llama-bench, 2026-10-08,
[below](#cpu-core-scaling-2026-10-08-llama-bench-no-judge)) the model
generates 12.8–13.3 tok/s at 4, 8 and 15 vCPU, while prompt processing
goes from 61.1 to 109.8 tok/s between 4 and 8 vCPU. Computed from those
numbers: the Q4_K_M file averages 4.71 bits per weight (20,419,565,568
bytes over the 34,660,610,688 parameters in its GGUF metadata), so the
~3B parameters active per token are roughly 1.8 GB of weights, and at
13.3 tok/s that is roughly 23 GB/s of weight reads — an average-based
approximation (the tensors are quantized unevenly), not a measured memory
bandwidth. Generation not scaling with cores fits a memory-bound limit; that
is an inference, as in the core-scaling section. Per generated token, the
other models compute with 10B (MiniMax M2.x), ~23B (M3), 27B, 9.7B or 4.7B
parameters against this model's 3B. That is a count of weights touched,
not a speed: none of them was run, so no tok/s is given for any of them.
The flat ~13 tok/s is the E5 shape's figure: the same file on node 2's
Xeon generated 10.8 to 22.1 tok/s, rising with threads from 4 to 28
([below](#same-model-file-on-an-intel-cpu-an-amd-cpu-and-an-nvidia-gpu-2026-10-16-llama-bench-no-judge),
2026-10-16, a comparison of shapes, not chips).

Reproduce:

```bash
# file sizes (weights only)
python scripts/hf_gguf_fit.py --budget A10=22.49 --budget E5-node=58 --budget cpu-pod=30 \
  --quants Q4_K_M UD-Q4_K_M Q8_0 --smallest \
  ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6 \
  ggml-org/Qwen3.6-27B-GGUF@8a7ee08e8b9bfb857107ecc25a5599d2f38b76f8 \
  unsloth/Qwen3.5-9B-GGUF@3885219b6810b007914f3a7950a8d1b469d598a5 \
  unsloth/Qwen3.5-4B-GGUF@e87f176479d0855a907a41277aca2f8ee7a09523 \
  unsloth/MiniMax-M2.7-GGUF@d2a05ccf69491b03db0cc40b335aec14bdaf7198 \
  unsloth/MiniMax-M2.5-GGUF@7c50dca0e5592483ad308ecffc876aecac725660 \
  unsloth/MiniMax-M3-GGUF@abdce34b5ab2e7dd9260130415c01a1f25561210
# as served: + KV cache and recurrent state at 8 x 5,120 tokens + 1 GiB allowance
# (one "CONFIG_REPO@REV|GGUF_REPO@REV|QUANT" per build; the 11 builds of the
# committed output are in eval/runs/kv-state-fit-2026-10-15.txt)
python -m scripts.kv_state_fit --seqs 8 --tokens 5120 --budget A10=22.49 --budget E5-node=58 --budget cpu-pod=30 \
  "Qwen/Qwen3.6-35B-A3B@995ad96eacd98c81ed38be0c5b274b04031597b0|ggml-org/Qwen3.6-35B-A3B-GGUF@baec3ebee244827cda0f4557eafa8b28f7545fa6|Q4_K_M" \
  "Qwen/Qwen3.6-27B@6a9e13bd6fc8f0983b9b99948120bc37f49c13e9|ggml-org/Qwen3.6-27B-GGUF@8a7ee08e8b9bfb857107ecc25a5599d2f38b76f8|Q4_K_M" \
  "MiniMaxAI/MiniMax-M2.7@d494266a4affc0d2995ba1fa35c8481cbd84294b|unsloth/MiniMax-M2.7-GGUF@d2a05ccf69491b03db0cc40b335aec14bdaf7198|UD-IQ1_M" \
  "MiniMaxAI/MiniMax-M2.5@f710177d938eff80b684d42c5aa84b382612f21f|unsloth/MiniMax-M2.5-GGUF@7c50dca0e5592483ad308ecffc876aecac725660|UD-TQ1_0"
```

## The A10 against hosted, image `f3043751` (current)

The A10 run of record on the current image (stock-data fix plus
currency-labelling prompt rule): GPU `nstp9` (2026-10-06, 40 tickers, two
briefs at a time, traffic proof EXACT) against hosted `4hsn2` on the same
image. Source: [eval-methodology.md, the current runs](eval-methodology.md#numbers-of-record-on-the-stock-data-fix-image-three-judgings-per-run-and-the-judge-v2-calibration-on-those-runs-2026-10-0607).

| | Hosted (`4hsn2`) | A10 (`nstp9`) |
|---|---|---|
| Pipeline time per brief, mean | 26.7 s | 34.6 s (1.3× hosted's) |
| Briefs per hour, run's wall time, parallelism 2 | — | 66.0 |
| Model cost per brief | $0.0357 (n = 3, API cost, same pipeline code) | **at most $0.0303** (the whole VM at $2.00/h × 2,183 s for 40 briefs) |
| A10 utilization during the run | — | mean 35.7%, median sample 0%, above 0% in 41% of samples |
| Wrong stock figures per checked number (numeric check, adjudicated) | 1/565 | 1/432 |
| Figures bound to stock data per brief (no judge) | 4.47 | 3.05 |
| Grounding (judge v2, judge-flagged, mean of three judgings) | 2.55% | 3.57% |

- The A10 again sat mostly idle at two briefs at a time, so its cost per
  brief is a ceiling, not an estimate of the floor.
- Hosted cost is `scripts/cost_report.py` run locally on the unchanged
  pipeline code; A10 cost is `scripts/cost_per_brief_slm.py` on the run's
  workflow object, with utilization from `scripts/nvsmi_summary.py`
  (output `eval/runs/cost-gpu-nstp9-2026-10-07.txt`).
- Judge-flagged grounding is secondary: on these runs the judge's
  precision is about 29% and its recall about 11%, and it moves by up to
  2× between judgings. No difference was detected.
- There is no citable CPU run on this image (both failed their traffic
  proofs), so the CPU comparison below stays on the previous image.

## Qwen3.6 on CPU vs on the A10, image `1f51dad` (dated)

The same GGUF and the same llama.cpp build on both sides: the CPU
endpoint in the OKE cluster (8 CPU / 30 GiB pod on a VM.Standard.E5.Flex
node) and the A10 on node 2. Both measured as 40-ticker eval runs on image
`1f51dad`, two briefs at a time: CPU `8vpq6` (2026-10-04) and A10 `p9jr2`
(2026-10-05), both with traffic proof EXACT. Source:
[eval-methodology.md, the three-way comparison](eval-methodology.md#gpu-slm-extended-run-p9jr2-2026-10-05-the-three-way-comparison-with-hosted-9jzmj-and-cpu-8vpq6).

| | CPU (`8vpq6`) | A10 (`p9jr2`) |
|---|---|---|
| Pipeline time per brief, mean | 355.1 s | 31.1 s (11.4× faster) |
| Per call site, mean | — | 10–15× faster at every site |
| Briefs per hour, run's wall time, parallelism 2 | 16.8 | 68.2 |
| Model cost per brief | **$0.0107** (the pod's 4 OCPU + 30 GiB at E5 list prices) | **at most $0.0293** (the whole VM at $2.00/h) |
| Endpoint utilization during the run | median 7,806m of its 8,000m CPU limit | GPU mean 38%, median sample 0%, above 0% in 43% of samples |
| Grounding (judge v2, judge-flagged) | 9/248 = 3.63% | 6/245 = 2.45% |
| Figures stated per brief | 4.0 | 3.9 |

- The CPU endpoint was saturated; the A10 was mostly idle at two briefs
  at a time. That makes the A10's cost per brief a ceiling, not an
  estimate of the floor.
- The two runs of the same model do not differ detectably in what they
  write: figures per brief +0.15 (CI −0.35 to +0.68), all-claims Fisher
  p = 0.60.
- Cost is model serving only: harness pods, storage and the judge are
  excluded. Prices are OCI list prices read 2026-10-05
  ([cost.md](cost.md); per-brief records in
  [numbers-of-record.md](numbers-of-record.md#dated-run-records)). The
  CPU figure bills each GiB as one GB of the memory metric **(inferred
  from node capacity; $0.0110 if converted to decimal GB)**.
- The harness on OKE reaches the A10 over node 2's public address on one
  port, so the A10 timings include that network path.

## CPU core scaling (2026-10-08, llama-bench, no judge)

`scripts/llama_bench_cpu.sh` on the OKE CPU endpoint's node (VM.Standard.E5.Flex,
AMD EPYC 9J14): llama-bench from the same llama.cpp build (b11347, `full`
image), the endpoint's own Q4_K_M GGUF, one Job per level with guaranteed
CPU and `-t` equal to the level, the endpoint scaled to 0 meanwhile. 16
vCPU was not schedulable (node allocatable 15,783m), so the top level is
**15 vCPU**. Three repetitions each; results in
`eval/runs/llama-bench-cpu-2026-10-08/`.

| vCPU | Prompt, 2,048 tokens (tok/s) | Generation, 128 tokens (tok/s) |
|---|---|---|
| 4 | 61.1 (±0.03) | 12.9 (±0.02) |
| 8 (the endpoint's size) | 109.8 (±0.09) | 13.3 (±0.01) |
| 15 | 103.6 (±0.26) | 12.8 (±0.02) |

- **Prompt processing scales 1.8× from 4 to 8 vCPU and not beyond**: 15
  vCPU is slightly slower than 8.
- **Generation does not scale at all** (12.8–13.3 tok/s at every level).
  It is bound by something other than cores — memory bandwidth is the usual
  limit for token generation, but this run does not measure it.
- **So 8 vCPU is the right size for this endpoint**; more cores on one
  node do not make it faster. The eval's CPU arm spends most of its time
  generating, which is why it is about 10× slower than the A10.
- The 512-token prompt figures (45.7, 79.6, 75.2) are not quoted: their
  spread across the three repetitions (±27 to ±56 tok/s) shows a cold first
  repetition.
- **Operational finding:** loading the 20.4 GB GGUF cold from the block
  volume took about 15 minutes per Job. On restore, the endpoint was killed
  once at 06:17Z (exit 137, not OOM) before its cold load finished, then
  came up from page cache and reports healthy. A cold restart of the CPU
  endpoint can therefore take two attempts; no manifest was changed.
  Follow-up, 2026-10-15: the oke-cpu overlay now gives the startup probe
  30 minutes and the rollout a 40-minute progress deadline; a cold load
  measured 15 min 15 s under it, with 0 restarts (runbook, "CPU endpoint
  startup probe").

## Same model file on an Intel CPU, an AMD CPU and an Nvidia GPU (2026-10-16, llama-bench, no judge)

A dated measurement with no judge, not a number of record. The same GGUF
(Qwen3.6-35B-A3B Q4_K_M, `ggml-org` @`baec3eb`), the same llama.cpp
release (b11347, `5fc4f3c`) and the same llama-bench settings (`-p
512,2048 -n 128 -r 3`, one Job per level, CPU request = limit, `-t` = the
level) on three OCI shapes. The AMD rows are the 2026-10-08 sweep above
(`scripts/llama_bench_cpu.sh`). The Intel and A10 rows are
`scripts/llama_bench_node2.sh` on node 2, 2026-10-16 05:59–06:12Z, with
the GPU endpoint scaled to 0 for the run and restored after it (llama-server
back at 20,488 MiB, key enforced, alias unchanged; runbook "Cross-shape
llama-bench on node 2"). The Intel levels use the same CPU-only image as
the AMD run, a build with no GPU backend. The A10 level uses the CUDA 12.8.1
build of the same release, all layers on the GPU. Mean (± standard
deviation over the three repetitions); results in
`eval/runs/llama-bench-2026-10-16/` (table: `table.md`, from
`scripts/llama_bench_table.py`) and `eval/runs/llama-bench-cpu-2026-10-08/`.

| Shape (where) | Threads | Prompt, 2,048 tokens (tok/s) | Prompt, 512 tokens (tok/s) | Generation, 128 tokens (tok/s) |
|---|---|---|---|---|
| AMD EPYC 9J14, VM.Standard.E5.Flex (OKE pod) | 4 | 61.1 (±0.03) | not quoted (cold) | 12.9 (±0.02) |
| | 8 | 109.8 (±0.09) | not quoted (cold) | 13.3 (±0.01) |
| | 15 | 103.6 (±0.26) | not quoted (cold) | 12.8 (±0.02) |
| Intel Xeon Platinum 8358, VM.GPU.A10.1 host (k3s pod) | 4 | 43.8 (±0.04) | 44.3 (±0.25) | 10.8 (±0.01) |
| | 8 | 80.4 (±0.16) | 81.5 (±0.32) | 15.9 (±0.01) |
| | 15 | 122.5 (±1.23) | 122.8 (±3.18) | 20.8 (±0.10) |
| | 28 | 116.3 (±0.91) | 119.6 (±0.66) | 22.1 (±0.05) |
| NVIDIA A10, all layers (k3s pod, VM.GPU.A10.1) | 8 | 2,299.5 (±5.71) | 2,289.3 (±81.90) | 110.4 (±0.34) |

**It compares OCI shapes, not chips.** The two CPU rows differ in more than
the processor: a 16-vCPU E5 node (8 OCPU) in OKE against a 30-vCPU
VM.GPU.A10.1 (15 cores, 2 threads each, `lscpu`), different memory sizes
and, unmeasured, different memory bandwidth, each pod sharing its host with
whatever else ran there. A thread count is a pod's CPU limit, not a number
of physical cores. The E5's 512-token prompt figures are not quoted: their
first repetition was a cold load (spread ±27 to ±56 tok/s); its 2,048-token
figures are the prompt comparison.

What the numbers show, and no more:

- **On the Xeon, generation rises with threads, from 10.8 to 22.1 tok/s
  (4 to 28); on the E5 it stayed about 13 at every level.** Why is not
  measured.
- **Xeon prompt processing flattens past 15 threads** (122.5 at 15, 116.3
  at 28). The VM has 15 physical cores with 2 threads each, which is a
  likely explanation, not a measured one.
- **At the same thread count**, prompt processing is lower on the Xeon at 4
  and 8 threads (43.8 and 80.4 against 61.1 and 109.8) and higher at 15
  (122.5 against 103.6); generation is lower at 4 (10.8 against 12.9) and
  higher at 8 and 15 (15.9 and 20.8 against 13.3 and 12.8).
- **The A10 is about 5× the best CPU on generation** (110.4 against 22.1,
  the Xeon at 28 threads) **and about 19× on prompt processing** (2,299.5
  against 122.5, the Xeon at 15 threads, 2,048 tokens).
- These are single-request llama-bench rates, not served throughput: the
  endpoint's capacity under the eval's concurrency is the replay sweep
  below, and the eval-measured runs are in the sections above.

## Capacity at higher parallelism

**Replay sweep, 2026-10-07** (`scripts/capacity_replay.py`, outputs in
`eval/runs/capacity-sweep-2026-10-07/`). The 270 LLM calls of the A10 run
of record `nstp9` replayed against the GPU endpoint on node 2 (from node 2
itself, so no network path), at a fixed client concurrency P, one level
after the other, nothing else using the endpoint. The ledger records each
call's token counts but not its text, so each replayed request is
**length-matched**: a token-exact prompt of the recorded length, cut from
`nstp9`'s own retrieved contexts behind a distinct per-request marker, and
exactly the recorded number of completion tokens (`n_predict`,
`ignore_eos`). Prompt cache off; one connection per request; counts from the
server's own per-request timings.

| P | Wall for 270 calls | Requests/min | Output tok/s | Prompt tok/s | Latency p50 / p95 | A10 util mean (median) | VRAM | Errors |
|---|---|---|---|---|---|---|---|---|
| 1 | 19.7 min | 13.7 | 83.6 | 298.6 | 2.1 s / 9.8 s | 90.9% (94%) | 20,540 MiB | 0 |
| 2 | 15.2 min | 17.8 | 108.2 | 386.5 | 3.4 s / 16.6 s | 86.6% (92%) | 20,540 MiB | 0 |
| 4 | 13.0 min | 20.8 | 126.6 | 452.5 | 5.8 s / 29.5 s | 82.0% (89%) | 20,540 MiB | 0 |

- **The server, kept busy, does about 1.5× more work at P=4 than at P=1**
  (output tokens per second 126.6 vs 83.6), and latency per call rises
  about 3× (p95 29.5 s vs 9.8 s; synthesis calls median 27.3 s vs 9.3 s).
  Every level ran the whole of `nstp9`'s call mix, which is 40 briefs of
  model work: 13.0 minutes at P=4 against 19.7 at P=1.
- **Eval-time idle is harness wait, not a GPU limit.** Under direct
  replay the A10 is busy 82–91% of the time at every P; during the eval
  runs it averaged about 36% (`nstp9` 35.7%, `p9jr2` 38%), because each
  eval pod spends most of its time outside the model — fetching data,
  retrieval, the judge — and two pods leave long gaps between calls.
- VRAM does not move with P: llama.cpp allocates the 32,768-token KV cache
  at start (`--kv-unified`, shared by the 4 slots).
- **P=8 was not run.** The endpoint serves 4 slots (`--parallel 4`), so
  a client at P=8 only queues the extra requests at the server and measures
  nothing P=4 does not. Serving 8 at once needs `--parallel 8` and a larger
  shared context: `nstp9`'s largest call is 4,215 tokens (p95 3,698), and
  8 × 4,215 = 33,720 exceeds the 32,768 tokens the 4 slots share now. That
  is an endpoint restart with a new context size on the demo's GPU node,
  which this sweep was approved without.
- **Capacity-derived cost per brief: a PROJECTION, not a run's cost.**
  Each level replayed 40 briefs' worth of LLM calls (6.75 calls per brief,
  from `nstp9`'s ledger) back to back. At $2.00 per hour for the whole
  VM.GPU.A10.1: P=1 122.0 briefs an hour, $0.0164 per brief; P=2 157.9,
  $0.0127; **P=4 184.8, $0.0108**. That is model serving only, at
  sustained load, with none of the eval's non-model time — a floor the
  eval-measured ceiling ($0.0303, `nstp9` at parallelism 2) would approach
  only if the GPU were kept as busy as in the replay
  (`capacity_replay.py summary --plan … --hourly-usd 2.00`).
- **Eval-measured at parallelism 4: `xgtxx` (2026-10-08, image
  `f3043751`, per-request traffic proof TASK-EXACT).** 40 briefs in 1,429 s:
  **100.8 briefs an hour** against `nstp9`'s 66.0 at parallelism 2;
  **$0.0198 per brief**, still a ceiling (the A10 averaged 45.0%, median
  19%, against 35.7% in `nstp9`); pipeline time per brief 61.8 s against
  34.6 s, as calls queue for the 4 slots. What it writes did not change:
  figures bound to stock data 3.10 vs `nstp9`'s 3.05 per brief (CI on the
  difference −0.42 to +0.33); judge-flagged unsupported, three judgings,
  2.12% (1.54–2.97%) vs 3.57%, paired difference +1.75 points for `nstp9`
  (CI −1.07 to +4.73), not separated; numeric check: one flag, the same
  OMER filing-vs-yfinance sentence as before (draft FALSE_POSITIVE, for
  review).
- These are model-only figures from a replay. The
  40-ticker GPU eval at parallelism 4 (`6z5xz`, 2026-10-07) failed its
  traffic proof — the prompt counter 8 above the server's own per-task log,
  every request matched (`eval/runs/slm-proof-6z5xz/INVESTIGATION.md`) —
  so none of its figures, timings included, are quoted.
- **The counter drift reproduced, under control.** At every level the
  requests' own timings sum exactly to the tokens sent (352,522 prompt,
  98,665 generated), with no cache reuse, while the server's `/metrics`
  prompt counter moved 1, 2 and 2 tokens less. The generated-token counter
  matched exactly. This is the same small counter error behind the two
  failed CPU traffic proofs (`eval/runs/slm-proof-4kkgm/INVESTIGATION.md`),
  now seen on the GPU endpoint with nothing else running: the counter, not
  outside traffic. No rule change: the proof still requires EXACT, and the
  fix is the post-demo ledger change that records each response's own
  timings.

```bash
python scripts/capacity_replay.py plan --run nstp9   --log eval/runs/slm-proof-nstp9/grounding-eval-extended-slm-gpu-nstp9.log   --out eval/runs/capacity-plan-nstp9.json
python3 scripts/capacity_replay.py run --plan eval/runs/capacity-plan-nstp9.json   --url http://127.0.0.1:30880 --key-file ~/.llama-key --levels 1 2 4 --out ~/capacity-sweep-<date>   # node 2
python scripts/capacity_replay.py summary --dir eval/runs/capacity-sweep-2026-10-07 \n  --plan eval/runs/capacity-plan-nstp9.json --hourly-usd 2.00
python scripts/nvsmi_summary.py eval/runs/capacity-sweep-2026-10-07/nvsmi.csv   --window P1 2026-10-07T21:54:33Z 2026-10-07T22:14:14Z   --window P2 2026-10-07T22:14:44Z 2026-10-07T22:29:56Z   --window P4 2026-10-07T22:30:26Z 2026-10-07T22:43:25Z
```

## What has not run

- vLLM on OKE: the Terraform cluster with the A10 node pool
  (`terraform/oci/`) has never been applied.
- vLLM serving Qwen3.6-35B-A3B on one A10 (computed infeasible above,
  not booted).
- A whole eval on the A10 above parallelism 4.
