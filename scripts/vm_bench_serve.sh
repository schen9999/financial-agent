#!/usr/bin/env bash
# Latency/throughput benchmark of whatever the k3s vLLM deployment serves,
# with fixed settings so models are comparable. Runs `vllm bench serve`
# INSIDE the vllm pod against localhost:8000 (no tunnel or NodePort in the
# path), after an untimed warmup, and prints the result JSON.
#
# Usage (on the VM, after `make vm-vllm ...`):
#   bash scripts/vm_bench_serve.sh <served-name> > eval/runs/bench/<served-name>.json
#   CONCURRENCY=1 NUM_PROMPTS=50 SEED=2 bash scripts/vm_bench_serve.sh <served-name> \
#       > eval/runs/bench/<served-name>-c1.json
#
# Settings (identical for every model; change them only for all models):
#   random dataset, 1024 input / 256 output tokens, --ignore-eos (every
#   request generates exactly 256 tokens), 200 prompts, request rate inf,
#   max concurrency 8 (= the deployment's --max-num-seqs), seed 0,
#   /v1/completions, tokenizer from the served weights (/models/financial-lora
#   in the pod), warmup 16 prompts at the same settings, discarded.
#   CONCURRENCY, NUM_PROMPTS and SEED override the timed run's values.
#
# Prefix caching is on (the vLLM default), so a prompt the pod has already
# seen skips most of its prefill. The warmup uses WARMUP_SEED (default
# 1000), never the timed SEED, and the prefix-cache hit and query tokens
# over the timed run are written into the result JSON (expect ~0 hits). A
# seed's first N prompts are the same for any --num-prompts >= N, and the
# pod keeps its cache until restarted, so use a seed the pod has not served.
# The 2026-09-23 files ran with the warmup on the timed seed (WARMUP_SEED=0):
# their first 16 timed prompts were already cached.
set -euo pipefail
NAME=${1:?usage: vm_bench_serve.sh <served-model-name>}
NS=${NAMESPACE:-financial-agent}
CONC=${CONCURRENCY:-8}
NUM=${NUM_PROMPTS:-200}
SEED=${SEED:-0}
WARMUP_SEED=${WARMUP_SEED:-1000}
POD=$(kubectl -n "$NS" get pod -l app.kubernetes.io/name=vllm \
      --field-selector=status.phase=Running -o name | head -1)
[ -n "$POD" ] || { echo "no running vllm pod" >&2; exit 1; }

SERVED=$(kubectl -n "$NS" exec "$POD" -- python3 -c \
  'import json,urllib.request; print(" ".join(m["id"] for m in json.load(urllib.request.urlopen("http://localhost:8000/v1/models"))["data"]))')
case " $SERVED " in *" $NAME "*) ;; *) echo "pod serves [$SERVED], not $NAME" >&2; exit 1;; esac

ARGS=(--backend vllm --base-url http://localhost:8000 --endpoint /v1/completions
      --model /models/financial-lora --served-model-name "$NAME"
      --dataset-name random --random-input-len 1024 --random-output-len 256
      --ignore-eos --request-rate inf --max-concurrency "$CONC"
      --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99)

# Recorded in the result JSON (files from 2026-09-23 predate this and carry none)
VERSION=$(kubectl -n "$NS" exec "$POD" -- python3 -c 'import vllm; print(vllm.__version__)')
GPU=$(kubectl -n "$NS" exec "$POD" -- nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
DTYPE=$(kubectl -n "$NS" get "$POD" -o jsonpath='{.spec.containers[0].args}' | grep -o 'dtype=[a-z0-9]*' | cut -d= -f2)
# Weight precision as served (the quantization_config vLLM read from the
# weights' config.json, e.g. w4a16-g128, or none) and the weight files' size
# on disk; recorded since 2026-09-28 (quant-bench), earlier files carry neither
read -r QUANT WEIGHTS_BYTES < <(kubectl -n "$NS" exec "$POD" -- python3 -c 'import glob, json, os
d = "/models/financial-lora"
q = json.load(open(d + "/config.json")).get("quantization_config")
name = "none"
if q:
    g = next(iter(q["config_groups"].values()))
    act = (g.get("input_activations") or {}).get("num_bits", 16)
    name = "w%da%d-g%s" % (g["weights"]["num_bits"], act, g["weights"]["group_size"])
print(name, sum(os.path.getsize(p) for p in glob.glob(d + "/*.safetensors")))')

# Cumulative prefix-cache counter (hits|queries, in tokens) from the pod's /metrics
prefix_cache() {
  kubectl -n "$NS" exec "$POD" -- python3 -c 'import sys, urllib.request
k = "vllm:prefix_cache_%s_total" % sys.argv[1]
for line in urllib.request.urlopen("http://localhost:8000/metrics").read().decode().splitlines():
    if line.startswith(k):
        print(int(float(line.split()[-1])))' "$1"
}

[ "$SEED" != "$WARMUP_SEED" ] || { echo "SEED and WARMUP_SEED must differ" >&2; exit 1; }
kubectl -n "$NS" exec "$POD" -- vllm bench serve "${ARGS[@]}" --seed "$WARMUP_SEED" \
  --num-prompts 16 >/dev/null 2>&1 || { echo "warmup failed" >&2; exit 1; }
kubectl -n "$NS" exec "$POD" -- rm -f /tmp/bench.json
H0=$(prefix_cache hits); Q0=$(prefix_cache queries)
kubectl -n "$NS" exec "$POD" -- vllm bench serve "${ARGS[@]}" --seed "$SEED" --num-prompts "$NUM" \
  --save-result --result-dir /tmp --result-filename bench.json \
  --metadata device=gpu backend=vllm "backend_version=$VERSION" "dtype=$DTYPE" "gpu_model=$GPU" \
  "quantization=$QUANT" "weights_bytes=$WEIGHTS_BYTES" \
  "seed=$SEED" "warmup_seed=$WARMUP_SEED" >&2
H1=$(prefix_cache hits); Q1=$(prefix_cache queries)
kubectl -n "$NS" exec "$POD" -- python3 -c 'import json, sys
d = json.load(open("/tmp/bench.json"))
d["prefix_cache_hit_tokens"], d["prefix_cache_query_tokens"] = int(sys.argv[1]), int(sys.argv[2])
print(json.dumps(d))' $((H1 - H0)) $((Q1 - Q0))
