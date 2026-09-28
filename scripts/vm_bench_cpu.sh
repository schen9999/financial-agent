#!/usr/bin/env bash
# CPU inference benchmark on the VM's Xeon: the same model and the same
# `vllm bench serve` client and shape as scripts/vm_bench_serve.sh (the A10
# run), served by the vLLM CPU backend in plain Docker on the host, outside
# k3s, with explicit core pinning. Measurement only: no tuning beyond the
# GPU deployment's own serving args.
#
# Usage (on the VM, from the repo root):
#   bash scripts/vm_bench_cpu.sh serve <model-dir> <served-name>
#   SEED=1 bash scripts/vm_bench_cpu.sh bench <served-name> 8 200 \
#       > eval/runs/bench/cpu-<date>/<served-name>-c8.json
#   SEED=2 bash scripts/vm_bench_cpu.sh bench <served-name> 1 50 \
#       > eval/runs/bench/cpu-<date>/<served-name>-c1.json
#   bash scripts/vm_bench_cpu.sh stop
#
# serve: starts container vllm-cpu from /home/ubuntu/models/<model-dir>,
#   mounted at /models/<served-name>, with the GPU deployment's args (bf16,
#   max-model-len 4096, max-num-seqs 8), waits for /v1/models, then sends
#   one chat completion as a smoke test.
# bench: the A10 settings (random dataset, 1024 input / 256 output tokens,
#   --ignore-eos, request rate inf, /v1/completions, tokenizer
#   /models/financial-lora), run from a separate client container on the
#   reserved core, after an untimed 16-prompt warmup.
#
# Prefix caching is on (the vLLM default on both backends, as in the GPU
# deployment), so a prompt the server has already seen skips most of its
# prefill. The warmup therefore uses WARMUP_SEED, never the timed SEED, and
# the prefix-cache hit and query tokens over the timed run are written into
# the result JSON (expect ~0 hits: random prompts share no prefixes). A
# given seed's first N prompts are the same for any --num-prompts >= N, so
# give each timed run on one server its own seed. Pinning, seeds and backend
# go in with --metadata.
#
# Pinning (defaults fit a VM.GPU.A10.1: 15 cores, SMT siblings 2k,2k+1):
#   server  --cpuset-cpus 2-29 (14 physical cores, 28 vCPUs), one OMP
#           thread per physical core (2,4,...,28)
#   client  --cpuset-cpus 0-1 (core 0, shared with k3s and idle pods)
set -euo pipefail
IMAGE=${VLLM_CPU_IMAGE:-public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2}
MODELS=${MODELS_ROOT:-/home/ubuntu/models}
TOKENIZER_DIR=${TOKENIZER_DIR:-qwen-ft}   # mounted as /models/financial-lora, as in the A10 run
SERVER_CPUS=${SERVER_CPUS:-2-29}
OMP_BIND=${OMP_BIND:-$(seq -s, 2 2 28)}
CLIENT_CPUS=${CLIENT_CPUS:-0-1}
MEM=${MEM:-64g}
KV_GB=${KV_GB:-8}
PORT=${PORT:-8100}
SEED=${SEED:-0}
WARMUP_SEED=${WARMUP_SEED:-1000}
NAME=vllm-cpu
CORES=$(tr ',' '\n' <<<"$OMP_BIND" | wc -l)

# Cumulative prefix-cache counter (hits|queries, in tokens) from /metrics
prefix_cache() {
  curl -sf "http://127.0.0.1:$PORT/metrics" \
    | awk -v k="vllm:prefix_cache_$1_total" 'index($0, k) == 1 { printf "%d\n", $NF }'
}

case "${1:-}" in
serve)
  DIR=${2:?usage: vm_bench_cpu.sh serve <model-dir> <served-name>}
  SERVED=${3:?usage: vm_bench_cpu.sh serve <model-dir> <served-name>}
  test -d "$MODELS/$DIR" || { echo "$MODELS/$DIR not found" >&2; exit 1; }
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker run -d --name "$NAME" --network host \
    --cpuset-cpus "$SERVER_CPUS" --memory "$MEM" --shm-size 4g \
    -e VLLM_CPU_KVCACHE_SPACE="$KV_GB" -e VLLM_CPU_OMP_THREADS_BIND="$OMP_BIND" \
    -v "$MODELS/$DIR:/models/$SERVED:ro" --entrypoint vllm "$IMAGE" \
    serve "/models/$SERVED" --served-model-name "$SERVED" --dtype bfloat16 \
    --max-model-len 4096 --max-num-seqs 8 --host 127.0.0.1 --port "$PORT" >/dev/null
  for _ in $(seq 180); do
    docker ps -q -f name="^$NAME\$" | grep -q . || { docker logs --tail 50 "$NAME" >&2; echo "server exited" >&2; exit 1; }
    curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null && break
    sleep 5
  done
  curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null || { echo "server not ready after 15 min" >&2; exit 1; }
  curl -sf "http://127.0.0.1:$PORT/v1/chat/completions" -H 'Content-Type: application/json' \
    -d "{\"model\":\"$SERVED\",\"messages\":[{\"role\":\"user\",\"content\":\"In one sentence, what is free cash flow?\"}],\"max_tokens\":48,\"temperature\":0}"
  echo
  ;;
bench)
  SERVED=${2:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}
  CONC=${3:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}
  NUM=${4:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}
  [ "$SEED" != "$WARMUP_SEED" ] || { echo "SEED and WARMUP_SEED must differ" >&2; exit 1; }
  curl -sf "http://127.0.0.1:$PORT/v1/models" | grep -q "\"$SERVED\"" \
    || { echo "$NAME does not serve $SERVED" >&2; exit 1; }
  VERSION=$(docker run --rm --entrypoint python3 "$IMAGE" -c 'import vllm; print(vllm.__version__)')
  OUT=$(mktemp -d)
  CLIENT=(docker run --rm --network host --cpuset-cpus "$CLIENT_CPUS"
          -v "$MODELS/$TOKENIZER_DIR:/models/financial-lora:ro" -v "$OUT:/out"
          --entrypoint vllm "$IMAGE" bench serve)
  ARGS=(--backend vllm --base-url "http://127.0.0.1:$PORT" --endpoint /v1/completions
        --model /models/financial-lora --served-model-name "$SERVED"
        --dataset-name random --random-input-len 1024 --random-output-len 256
        --ignore-eos --request-rate inf --max-concurrency "$CONC"
        --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99)
  "${CLIENT[@]}" "${ARGS[@]}" --seed "$WARMUP_SEED" --num-prompts 16 >/dev/null 2>&1 \
    || { echo "warmup failed" >&2; exit 1; }
  H0=$(prefix_cache hits); Q0=$(prefix_cache queries)
  "${CLIENT[@]}" "${ARGS[@]}" --seed "$SEED" --num-prompts "$NUM" --save-result --result-dir /out \
    --result-filename bench.json --metadata device=cpu backend=vllm-cpu \
    "backend_version=$VERSION" dtype=bfloat16 "pinned_cores=$CORES" \
    "server_cpuset=$SERVER_CPUS" "omp_threads_bind=$OMP_BIND" "seed=$SEED" \
    "warmup_seed=$WARMUP_SEED" "cpu_model=$(lscpu | sed -n 's/^Model name: *//p')" >&2
  H1=$(prefix_cache hits); Q1=$(prefix_cache queries)
  python3 -c 'import json, sys
d = json.load(open(sys.argv[1]))
d["prefix_cache_hit_tokens"], d["prefix_cache_query_tokens"] = int(sys.argv[2]), int(sys.argv[3])
print(json.dumps(d))' "$OUT/bench.json" $((H1 - H0)) $((Q1 - Q0))
  ;;
stop)
  docker rm -f "$NAME"
  ;;
*)
  echo "usage: vm_bench_cpu.sh serve <model-dir> <served-name> | bench <served-name> <concurrency> <num-prompts> | stop" >&2
  exit 1
  ;;
esac
