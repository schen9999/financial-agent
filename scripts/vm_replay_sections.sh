#!/usr/bin/env bash
# Frozen-input replay driver for vm-a10-inst-2 (run in tmux).
# BF16 -> replay, W4A16 -> replay, then always restore the default BF16 serve.
# Executed 2026-09-30 04:20-04:25 UTC on vm-a10-inst-2 from ~/replay (outputs
# copied to eval/runs/replay-2026-09-30/). Needs scripts/replay_sections.py
# at ~/replay/; run inside tmux: tmux new -s replay 'bash scripts/vm_replay_sections.sh 2>&1 | tee ~/replay/run.log'
set -euo pipefail
cd ~/financial-agent
D=$(date -u +%F)
OUT=/replay/out/replay-$D
ts() { date -u +%FT%TZ; }

restore() {
  echo "== $(ts) restore default serve (make vm-vllm)"
  make vm-vllm || echo "!! restore failed: check deployment/vllm"
  echo "== $(ts) EXIT"
}
trap restore EXIT

replay() {
  docker run --rm --network host \
    -v ~/replay:/replay \
    -v ~/financial-agent/eval/runs/raw/v924f-findings:/repo/eval/runs/raw/v924f-findings:ro \
    -w /app financial-agent-app:local \
    python /replay/replay_sections.py \
      --findings-dir /repo/eval/runs/raw/v924f-findings \
      --out "$OUT" --samples 3 --seed-base 42 --concurrency 8 "$@"
}

echo "== $(ts) serve BF16 (make vm-vllm)"
make vm-vllm
echo "== $(ts) replay bf16"
replay --arm bf16 --served-name financial-lora

echo "== $(ts) serve W4A16"
make vm-vllm MODEL_DIR=qwen-ft-w4a16 SERVED_NAME=financial-lora-w4a16 MAX_LEN=4096
echo "== $(ts) replay w4a16"
replay --arm w4a16 --served-name financial-lora-w4a16

echo "== $(ts) replays done: $OUT"
