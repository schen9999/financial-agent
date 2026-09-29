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
#   bash scripts/vm_bench_cpu.sh sweep <model-dir> <served-name> eval/runs/bench/cpu-sweep-<date>
#
# serve: starts container vllm-cpu from /home/ubuntu/models/<model-dir>,
#   mounted at /models/<served-name>, with the GPU deployment's args (bf16,
#   max-model-len 4096, max-num-seqs 8), waits for /v1/models, then sends
#   one chat completion as a smoke test.
# bench: the A10 settings (random dataset, 1024 input / 256 output tokens,
#   --ignore-eos, request rate inf, /v1/completions, tokenizer
#   /models/financial-lora), run from a separate client container on the
#   reserved core, after an untimed 16-prompt warmup. The OMP binding and
#   max-num-seqs recorded in the result are read from the running server.
# sweep: concurrency SWEEP_CONC (1 2 4 8 16) x OMP threads SWEEP_THREADS
#   (7 14). One fresh server per thread count, with --max-num-seqs 16 so
#   concurrency 16 is admitted (the only serving arg the sweep changes) and
#   T threads bound one per physical core from core 1 (vCPUs 2,4,...,2T;
#   the cpuset stays SERVER_CPUS). Each cell is its own timed run with its
#   own seed, T*100 + C, and max(32, 8*C) prompts, written to
#   <out-dir>/<served-name>-t<T>-c<C>.json.
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
MAX_NUM_SEQS=${MAX_NUM_SEQS:-8}
PORT=${PORT:-8100}
SEED=${SEED:-0}
WARMUP_SEED=${WARMUP_SEED:-1000}
SWEEP_CONC=${SWEEP_CONC:-1 2 4 8 16}
SWEEP_THREADS=${SWEEP_THREADS:-7 14}
NAME=vllm-cpu

# Cumulative prefix-cache counter (hits|queries, in tokens) from /metrics
prefix_cache() {
  curl -sf "http://127.0.0.1:$PORT/metrics" \
    | awk -v k="vllm:prefix_cache_$1_total" 'index($0, k) == 1 { printf "%d\n", $NF }'
}

# The running server's environment variable $1
server_env() {
  docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$NAME" | sed -n "s/^$1=//p"
}

serve() {
  local dir=$1 served=$2
  test -d "$MODELS/$dir" || { echo "$MODELS/$dir not found" >&2; exit 1; }
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  docker run -d --name "$NAME" --network host \
    --cpuset-cpus "$SERVER_CPUS" --memory "$MEM" --shm-size 4g \
    -e VLLM_CPU_KVCACHE_SPACE="$KV_GB" -e VLLM_CPU_OMP_THREADS_BIND="$OMP_BIND" \
    -v "$MODELS/$dir:/models/$served:ro" --entrypoint vllm "$IMAGE" \
    serve "/models/$served" --served-model-name "$served" --dtype bfloat16 \
    --max-model-len 4096 --max-num-seqs "$MAX_NUM_SEQS" --host 127.0.0.1 --port "$PORT" >/dev/null
  for _ in $(seq 180); do
    docker ps -q -f name="^$NAME\$" | grep -q . || { docker logs --tail 50 "$NAME" >&2; echo "server exited" >&2; exit 1; }
    curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null && break
    sleep 5
  done
  curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null || { echo "server not ready after 15 min" >&2; exit 1; }
  curl -sf "http://127.0.0.1:$PORT/v1/chat/completions" -H 'Content-Type: application/json' \
    -d "{\"model\":\"$served\",\"messages\":[{\"role\":\"user\",\"content\":\"In one sentence, what is free cash flow?\"}],\"max_tokens\":48,\"temperature\":0}"
  echo
}

bench() {
  local served=$1 conc=$2 num=$3 seed=$4
  [ "$seed" != "$WARMUP_SEED" ] || { echo "SEED and WARMUP_SEED must differ" >&2; exit 1; }
  curl -sf "http://127.0.0.1:$PORT/v1/models" | grep -q "\"$served\"" \
    || { echo "$NAME does not serve $served" >&2; exit 1; }
  local version bind cores seqs src wbytes out
  version=$(docker run --rm --entrypoint python3 "$IMAGE" -c 'import vllm; print(vllm.__version__)')
  bind=$(server_env VLLM_CPU_OMP_THREADS_BIND)
  cores=$(tr ',' '\n' <<<"$bind" | wc -l)
  seqs=$(docker inspect -f '{{join .Args " "}}' "$NAME" | grep -o -- '--max-num-seqs [0-9]*' | cut -d' ' -f2)
  src=$(docker inspect -f "{{range .Mounts}}{{if eq .Destination \"/models/$served\"}}{{.Source}}{{end}}{{end}}" "$NAME")
  wbytes=$(du -cb "$src"/*.safetensors | tail -1 | cut -f1)
  out=$(mktemp -d)
  local client=(docker run --rm --network host --cpuset-cpus "$CLIENT_CPUS"
                -v "$MODELS/$TOKENIZER_DIR:/models/financial-lora:ro" -v "$out:/out"
                --entrypoint vllm "$IMAGE" bench serve)
  local args=(--backend vllm --base-url "http://127.0.0.1:$PORT" --endpoint /v1/completions
              --model /models/financial-lora --served-model-name "$served"
              --dataset-name random --random-input-len 1024 --random-output-len 256
              --ignore-eos --request-rate inf --max-concurrency "$conc"
              --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99)
  "${client[@]}" "${args[@]}" --seed "$WARMUP_SEED" --num-prompts 16 >/dev/null 2>&1 \
    || { echo "warmup failed" >&2; exit 1; }
  local h0 q0 h1 q1
  h0=$(prefix_cache hits); q0=$(prefix_cache queries)
  "${client[@]}" "${args[@]}" --seed "$seed" --num-prompts "$num" --save-result --result-dir /out \
    --result-filename bench.json --metadata device=cpu backend=vllm-cpu \
    "backend_version=$version" dtype=bfloat16 quantization=none "weights_bytes=$wbytes" \
    "pinned_cores=$cores" "server_cpuset=$SERVER_CPUS" "omp_threads_bind=$bind" \
    "max_num_seqs=$seqs" "seed=$seed" "warmup_seed=$WARMUP_SEED" \
    "cpu_model=$(lscpu | sed -n 's/^Model name: *//p')" >&2
  h1=$(prefix_cache hits); q1=$(prefix_cache queries)
  python3 -c 'import json, sys
d = json.load(open(sys.argv[1]))
d["prefix_cache_hit_tokens"], d["prefix_cache_query_tokens"] = int(sys.argv[2]), int(sys.argv[3])
print(json.dumps(d))' "$out/bench.json" $((h1 - h0)) $((q1 - q0))
}

case "${1:-}" in
serve)
  serve "${2:?usage: vm_bench_cpu.sh serve <model-dir> <served-name>}" \
        "${3:?usage: vm_bench_cpu.sh serve <model-dir> <served-name>}"
  ;;
bench)
  bench "${2:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}" \
        "${3:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}" \
        "${4:?usage: vm_bench_cpu.sh bench <served-name> <concurrency> <num-prompts>}" "$SEED"
  ;;
stop)
  docker rm -f "$NAME"
  ;;
sweep)
  DIR=${2:?usage: vm_bench_cpu.sh sweep <model-dir> <served-name> <out-dir>}
  SERVED=${3:?usage: vm_bench_cpu.sh sweep <model-dir> <served-name> <out-dir>}
  OUT=${4:?usage: vm_bench_cpu.sh sweep <model-dir> <served-name> <out-dir>}
  mkdir -p "$OUT"
  for T in $SWEEP_THREADS; do
    OMP_BIND=$(seq -s, 2 2 $((2 * T))) MAX_NUM_SEQS=16
    serve "$DIR" "$SERVED" >&2
    for C in $SWEEP_CONC; do
      N=$((8 * C > 32 ? 8 * C : 32))
      echo "sweep: threads $T, concurrency $C, $N prompts, seed $((T * 100 + C))" >&2
      bench "$SERVED" "$C" "$N" $((T * 100 + C)) > "$OUT/$SERVED-t$T-c$C.json"
    done
    docker rm -f "$NAME" >/dev/null
  done
  ;;
*)
  echo "usage: vm_bench_cpu.sh serve <model-dir> <served-name> | bench <served-name> <concurrency> <num-prompts> | stop | sweep <model-dir> <served-name> <out-dir>" >&2
  exit 1
  ;;
esac
