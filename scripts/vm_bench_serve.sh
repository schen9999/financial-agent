#!/usr/bin/env bash
# Latency/throughput benchmark of whatever the k3s vLLM deployment serves,
# with fixed settings so models are comparable. Runs `vllm bench serve`
# INSIDE the vllm pod against localhost:8000 (no tunnel or NodePort in the
# path), after an untimed warmup, and prints the result JSON.
#
# Usage (on the VM, after `make vm-vllm ...`):
#   bash scripts/vm_bench_serve.sh <served-name> > eval/runs/bench/<served-name>.json
#
# Settings (identical for every model; change them only for all models):
#   random dataset, 1024 input / 256 output tokens, --ignore-eos (every
#   request generates exactly 256 tokens), 200 prompts, request rate inf,
#   max concurrency 8 (= the deployment's --max-num-seqs), seed 0,
#   /v1/completions, tokenizer from the served weights (/models/financial-lora
#   in the pod), warmup 16 prompts at the same settings, discarded.
set -euo pipefail
NAME=${1:?usage: vm_bench_serve.sh <served-model-name>}
NS=${NAMESPACE:-financial-agent}
POD=$(kubectl -n "$NS" get pod -l app.kubernetes.io/name=vllm \
      --field-selector=status.phase=Running -o name | head -1)
[ -n "$POD" ] || { echo "no running vllm pod" >&2; exit 1; }

SERVED=$(kubectl -n "$NS" exec "$POD" -- python3 -c \
  'import json,urllib.request; print(" ".join(m["id"] for m in json.load(urllib.request.urlopen("http://localhost:8000/v1/models"))["data"]))')
case " $SERVED " in *" $NAME "*) ;; *) echo "pod serves [$SERVED], not $NAME" >&2; exit 1;; esac

ARGS=(--backend vllm --base-url http://localhost:8000 --endpoint /v1/completions
      --model /models/financial-lora --served-model-name "$NAME"
      --dataset-name random --random-input-len 1024 --random-output-len 256
      --ignore-eos --request-rate inf --max-concurrency 8 --seed 0
      --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99)

kubectl -n "$NS" exec "$POD" -- vllm bench serve "${ARGS[@]}" --num-prompts 16 >/dev/null 2>&1 \
  || { echo "warmup failed" >&2; exit 1; }
kubectl -n "$NS" exec "$POD" -- rm -f /tmp/bench.json
kubectl -n "$NS" exec "$POD" -- vllm bench serve "${ARGS[@]}" --num-prompts 200 \
  --save-result --result-dir /tmp --result-filename bench.json >&2
kubectl -n "$NS" exec "$POD" -- cat /tmp/bench.json
