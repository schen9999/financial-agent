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

## Capacity at higher parallelism

**Not yet run.** A GPU run at parallelism 4 is planned to measure what
the A10 sustains when it is kept busier. Until it runs, no throughput or
cost figure above parallelism 2 is claimed, and none is projected from
the 36–38% utilization.

## What has not run

- vLLM on OKE: the Terraform cluster with the A10 node pool
  (`terraform/oci/`) has never been applied.
- vLLM serving Qwen3.6-35B-A3B on one A10 (computed infeasible above,
  not booted).
- The A10 at any parallelism above 2.
