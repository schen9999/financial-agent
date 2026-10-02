#!/usr/bin/env bash
# Frozen-input replay driver for vm-a10-inst-2 (run in tmux).
# BF16 -> replay, W4A16 -> replay, then always restore the default BF16 serve.
# Needs scripts/replay_sections.py at ~/replay/. Outputs land in
# ~/replay/out/replay-<LABEL>-<UTC date>/{bf16,w4a16}/ and are copied back to
# eval/runs/ by hand.
#   pilot (2026-09-30 04:20-04:25 UTC, then written to replay-<date>, renamed
#   replay-pilot-<date>): LABEL=pilot SAMPLES=3 SEED_BASE=42
#   replication (eval/numeric_check/replication-plan.md):
#   LABEL=replication SAMPLES=10 SEED_BASE=1000000
# tmux new -s replay 'LABEL=... bash vm_replay_sections.sh 2>&1 | tee ~/replay/run.log'
set -euo pipefail
LABEL=${LABEL:-pilot}
SAMPLES=${SAMPLES:-3}
SEED_BASE=${SEED_BASE:-42}
cd ~/financial-agent
D=$(date -u +%F)
OUT=/replay/out/replay-$LABEL-$D
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
      --out "$OUT" --samples "$SAMPLES" --seed-base "$SEED_BASE" --concurrency 8 "$@"
}

echo "== $(ts) $LABEL: samples $SAMPLES, seed base $SEED_BASE"
echo "== $(ts) serve BF16 (make vm-vllm)"
make vm-vllm
echo "== $(ts) replay bf16"
replay --arm bf16 --served-name financial-lora

echo "== $(ts) serve W4A16"
make vm-vllm MODEL_DIR=qwen-ft-w4a16 SERVED_NAME=financial-lora-w4a16 MAX_LEN=4096
echo "== $(ts) replay w4a16"
replay --arm w4a16 --served-name financial-lora-w4a16

echo "== $(ts) replays done: $OUT"
