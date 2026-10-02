# Pre-registered replication: W4A16 vs BF16 on frozen inputs

Registered 2026-09-30, committed before any replication output was
generated. The result is reported as it comes out; there will be no further
replications of this comparison.

## Question

On identical inputs, does the GPTQ W4A16 fine-tune (`financial-lora-w4a16`)
state more wrong stock-data figures in the sections it writes than the BF16
fine-tune (`financial-lora`)?

## What was known at registration (the pilot)

A 3-sample frozen-input replay, labelled **pilot** everywhere
(`eval/runs/replay-pilot-2026-09-30/`, seed base 42), ran first. Its
results were seen before this plan was written:

- W4A16 - BF16, all sections: +9.0 pts (paired ticker-cluster bootstrap
  CI -0.9 to +19.5).
- W4A16 - BF16, sections that hit the 512-token cap excluded: +10.0 pts
  (CI +3.2 to +16.7).
- About 23% of sections hit the cap in both arms (56/240 BF16, 55/240
  W4A16).

The choice of truncated-sections-excluded as the primary metric was made
after seeing the pilot. The replication is the confirmatory test: fresh
seeds, more samples, and the pilot's outputs do not enter it.

## Design

- **Inputs:** the 40 contexts of the BF16 live run `v924f`, rebuilt byte for
  byte from `eval/runs/raw/v924f-findings/*_local-model.md` (the replay
  script refuses any context that does not re-render to the file's
  `context_sha256`).
- **Sections:** Financial Health and Risk Factors only (the two the local
  model writes), with prompts built by `agent.core._haiku_section` inside
  the app image (`sha256:290d2933…`, the image v924f and r5nzh ran).
- **Arms:** BF16 `financial-lora` (`/home/ubuntu/models/qwen-ft`) and W4A16
  `financial-lora-w4a16` (`/home/ubuntu/models/qwen-ft-w4a16`), each served
  by `make vm-vllm` on vm-a10-inst-2 with the committed args (vLLM v0.10.2,
  `--dtype=bfloat16 --max-model-len=4096 --max-num-seqs=8
  --gpu-memory-utilization=0.90`). BF16 runs first, then W4A16; the default
  BF16 serve is restored afterwards.
- **Sampling:** LocalChat's production parameters (temperature 0.1,
  max_tokens 512, top_p 0.8, top_k 20, repetition_penalty 1.1, min_p 0.0),
  concurrency 8.
- **Samples:** 10 per ticker per arm: 40 x 10 x 2 sections = 800
  generations per arm.
- **Seeds:** `seed = 1000000 + 10000 * k + 10 * ticker_index + section_index`
  for k = 1..10, ticker_index over the tickers sorted by file name,
  section_index 0 (Financial Health) or 1 (Risk Factors): 1010000-1100391,
  disjoint from the pilot's 10042-30433. The same seed is sent to both arms
  for the same (ticker, section, sample).
- **Command:** `LABEL=replication SAMPLES=10 SEED_BASE=1000000 bash
  scripts/vm_replay_sections.sh` in tmux on the node; outputs copied to
  `eval/runs/replay-replication-<UTC date>/{bf16,w4a16}/`.
- **A failed run** (non-zero exit or a missing output file) is rerun in full
  with the same seeds, and the failure is reported. A completed run is
  final.

## Analysis (fixed now)

Code at registration: `agent/numeric_check.py` blob `890a4277`,
`scripts/numeric_backtest.py` blob `6f804b4b`, `scripts/replay_sections.py`
blob `fe0c7ba8`, `scripts/vm_replay_sections.sh` blob `7b973799`. None of
these changes before the replication is analysed.

- **Unit:** a brief = one (ticker, sample) with its two sections.
- **Truncated section:** vLLM `finish_reason == "length"`, from each output
  file's metadata. Each arm drops its own truncated sections.
- **Primary metric:** mismatches per checked number, truncated sections
  excluded: distinct mismatch findings / distinct checked numbers, counted
  per brief and summed over the arm (unadjudicated numeric-check flags).
- **Primary test:** W4A16 - BF16 in that metric, with a 95% percentile CI
  from a paired ticker-cluster bootstrap: resample the 40 tickers with
  replacement, 10,000 draws, seed 42, each drawn ticker contributing all 10
  samples of both arms (`bootstrap_difference` in
  `scripts/numeric_backtest.py`).
- **Decision rule and wording** (`replication_statement`):
  - CI above zero: "The W4A16 regression replicates on identical inputs: …"
  - CI contains zero: "The W4A16 regression does not replicate on identical
    inputs: …"
  - CI below zero: "On identical inputs W4A16 has fewer mismatches than
    BF16: …"
- **Secondary, reported but not decisive:** the same difference over all
  sections, per-arm rates with ticker-cluster CIs, briefs flagged, checked
  vs unchecked coverage, truncation per arm, and the per-sample spread.

## Adjudication

- Sample: 60 rows per arm, drawn from that arm's primary-metric mismatch
  flags (placeholders excluded), stratified by field with proportional
  allocation (largest remainders), `random.Random(42)` per arm over a
  deterministically sorted frame (`replication_sample`). The frame, the
  allocation and the drawn rows are written to
  `eval/numeric_check/replication-sample.json`.
- The pilot's flags are not labelled. The 359 live rows stay in
  `adjudication.csv` beside the 120 replication rows (`scope=replication`).
- Precision per arm is the stratum-weighted precision of the labelled
  sample, reported two ways (OTHER_DEFECT as a true positive, and
  excluded), applied to that arm's primary flag count to give estimated
  true mismatches and an adjusted rate, always with the sample size stated
  (`replication_applied_precision`).

## Reporting

The replication result goes into `eval/runs/numeric-backtest-<date>.md`
under the live-run comparison, as generated from the numbers, whichever
way it comes out. Nothing here is a number of record.
