#!/usr/bin/env bash
# CPU benchmark of GGUF builds of the fine-tune on the VM's Xeon, served by
# llama.cpp's llama-server (official CPU image, pinned by digest), with the
# same pinning, port, client and shape as scripts/vm_bench_cpu.sh (vLLM CPU,
# BF16). vLLM's CPU backend is not the engine for 4-bit on this Xeon, so the
# precision ladder runs on llama.cpp, and the F16 file is there to separate
# engine from precision: vLLM BF16 vs llama.cpp F16 is the engine effect;
# llama.cpp F16 vs Q8_0 vs Q4_K_M is the precision effect. Never read vLLM
# BF16 vs llama.cpp Q4_K_M as a quantization speedup.
#
# Usage (on the VM, from the repo root):
#   bash scripts/vm_bench_cpu_gguf.sh convert qwen-ft            # -> qwen-ft-gguf/
#   bash scripts/vm_bench_cpu_gguf.sh serve qwen-ft-gguf/financial-lora-q4_k_m.gguf financial-lora-q4_k_m
#   SEED=1 bash scripts/vm_bench_cpu_gguf.sh bench financial-lora-q4_k_m 8 200 > <dir>/financial-lora-q4_k_m-c8.json
#   SEED=2 bash scripts/vm_bench_cpu_gguf.sh bench financial-lora-q4_k_m 1 50  > <dir>/financial-lora-q4_k_m-c1.json
#   bash scripts/vm_bench_cpu_gguf.sh stop
#   bash scripts/vm_bench_cpu_gguf.sh sweep qwen-ft-gguf/financial-lora-q4_k_m.gguf financial-lora-q4_k_m <dir>
#
# convert: convert_hf_to_gguf.py --outtype f16 on /home/ubuntu/models/<dir>,
#   then llama-quantize to Q8_0 and Q4_K_M (no importance matrix), into
#   <dir>-gguf/financial-lora-{f16,q8_0,q4_k_m}.gguf with gguf_meta.json
#   (images, build, sizes, sha256).
# serve: container llama-cpu, --parallel 8 and a context of 8 x 1536 tokens
#   (each request needs 1024 + 256; the margin covers re-tokenization), T
#   threads bound one per physical core (default 14 = vCPUs 2,4,...,28,
#   strict placement for generation and prompt processing), in cpuset
#   2-29, 64 GB, 127.0.0.1:8100, Prometheus /metrics on. Everything else is
#   llama-server's default, prompt caching and SSE pings included. (Turning
#   the pings off did not stop the occasional lost request described in
#   scripts/bench_fix_llamacpp.py: tried 2026-09-29, one run of two still
#   lost one.)
# bench: `vllm bench serve` from the vLLM CPU image, exactly as
#   vm_bench_cpu.sh: random 1024 in / 256 out, --ignore-eos, rate inf,
#   /v1/completions, tokenizer /models/financial-lora (qwen-ft), client on
#   vCPUs 0-1, untimed 16-prompt warmup on WARMUP_SEED. The timed run adds
#   --save-detailed (what the client saves, not what it sends) for the
#   token-count correction below.
# sweep: concurrency SWEEP_CONC (1 2 4 8 16) at SWEEP_THREADS (14), one
#   fresh server per thread count with --parallel 16, seed T*100 + C and
#   max(32, 8*C) prompts per cell, as in vm_bench_cpu.sh sweep: the same
#   cells get the same prompts on both engines.
#
# Prompt reuse: llama-server reuses a slot's cached prefix and keeps a RAM
# prompt cache by default, the counterpart of vLLM's prefix caching, so the
# seed discipline is the same (warmup on its own seed, one seed per timed
# run). It exports no hit counter; the JSON records the prompt tokens the
# server actually processed over the timed run (llamacpp:prompt_tokens_total)
# and the tokens it generated (llamacpp:tokens_predicted_total; 256 x
# (prompts + 1): the client's initial test request is inside the timed run).
#
# Token counting: llama-server sends usage in the same chunk as the last
# (empty) choice, and the v0.10.2 client reads usage only from a choice-less
# chunk, so the client counts output tokens by re-tokenizing the text, which
# undercounts. scripts/bench_fix_llamacpp.py refuses the run unless every
# request completed and the server generated exactly 256 tokens each, then
# recomputes output throughput and TPOT at 256 with the client's formulas
# (the client's figures stay in the JSON under client_retokenized).
set -euo pipefail
SERVER_IMAGE=${LLAMA_SERVER_IMAGE:-ghcr.io/ggml-org/llama.cpp:server-b11223@sha256:8fdfad183be053cdb72d4b6a5930c3a2475730f932855ee9260193422c2564ed}
FULL_IMAGE=${LLAMA_FULL_IMAGE:-ghcr.io/ggml-org/llama.cpp:full-b11223@sha256:faa6d3bbf5bead65550bf888138118cd253d865fb50a32e7555ba35ac4e719bf}
CLIENT_IMAGE=${VLLM_CPU_IMAGE:-public.ecr.aws/q9t5s3a7/vllm-cpu-release-repo:v0.10.2}
MODELS=${MODELS_ROOT:-/home/ubuntu/models}
TOKENIZER_DIR=${TOKENIZER_DIR:-qwen-ft}   # mounted as /models/financial-lora, as in the A10 run
SERVER_CPUS=${SERVER_CPUS:-2-29}
THREADS=${THREADS:-14}
CLIENT_CPUS=${CLIENT_CPUS:-0-1}
MEM=${MEM:-64g}
PARALLEL=${PARALLEL:-8}
SLOT_CTX=${SLOT_CTX:-1536}
PORT=${PORT:-8100}
SEED=${SEED:-0}
WARMUP_SEED=${WARMUP_SEED:-1000}
OUTPUT_LEN=256
SWEEP_CONC=${SWEEP_CONC:-1 2 4 8 16}
SWEEP_THREADS=${SWEEP_THREADS:-14}
NAME=llama-cpu

# Cumulative server counter $1: prompt_tokens (evaluated, cached tokens
# excluded) or tokens_predicted (generated)
counter() {
  curl -sf "http://127.0.0.1:$PORT/metrics" \
    | awk -v k="llamacpp:$1_total" 'index($0, k) == 1 { printf "%d\n", $NF }'
}

# Hex affinity mask for vCPUs 2,4,...,2T (one per physical core from core 1)
cpu_mask() {
  local m=0 c
  for c in $(seq 2 2 $((2 * $1))); do m=$((m | (1 << c))); done
  printf '0x%x' "$m"
}

convert() {
  local dir=$1 out="$MODELS/$1-gguf"
  test -d "$MODELS/$dir" || { echo "$MODELS/$dir not found" >&2; exit 1; }
  [ ! -e "$out" ] || { echo "$out exists; remove it first" >&2; exit 1; }
  mkdir -p "$out"
  # USER: the host uid has no passwd entry in the image, and Python's
  # getpass (called during conversion) reads $USER before falling back to it
  local run=(docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e USER=llama
             -v "$MODELS/$dir:/in:ro" -v "$out:/out" "$FULL_IMAGE")
  "${run[@]}" --convert --outtype f16 --outfile /out/financial-lora-f16.gguf /in >&2
  "${run[@]}" --quantize /out/financial-lora-f16.gguf /out/financial-lora-q8_0.gguf Q8_0 >&2
  "${run[@]}" --quantize /out/financial-lora-f16.gguf /out/financial-lora-q4_k_m.gguf Q4_K_M >&2
  local build
  build=$(docker run --rm "$SERVER_IMAGE" --version 2>&1 | sed -n 's/^version: .*(build \([0-9]*\), commit \([0-9a-f]*\)).*/b\1 \2/p')
  python3 - "$out" "$MODELS/$dir" "$FULL_IMAGE" "$SERVER_IMAGE" "$build" <<'PY'
import hashlib, json, pathlib, sys, time
out, src, full, server, build = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), *sys.argv[3:]
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
files = {t.upper(): {"file": f"financial-lora-{t}.gguf", "bytes": (out / f"financial-lora-{t}.gguf").stat().st_size,
                     "sha256": sha(out / f"financial-lora-{t}.gguf")} for t in ("f16", "q8_0", "q4_k_m")}
meta = {"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source_dir": str(src),
        "source_weights_sha256": {p.name: sha(p) for p in sorted(src.glob("*.safetensors"))},
        "convert": "convert_hf_to_gguf.py --outtype f16", "quantize": "llama-quantize from the F16 file, no imatrix",
        "full_image": full, "server_image": server, "llama_cpp_build": build, "files": files}
(out / "gguf_meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
print(json.dumps(meta, indent=2))
PY
}

serve() {
  local file=$1 served=$2
  test -f "$MODELS/$file" || { echo "$MODELS/$file not found" >&2; exit 1; }
  ! docker ps -q -f name='^vllm-cpu$' | grep -q . || { echo "vllm-cpu is running (same cores and port); stop it first" >&2; exit 1; }
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  local mask
  mask=$(cpu_mask "$THREADS")
  # --no-healthcheck: the image's probe curls port 8080 (not ours) every 30 s
  docker run -d --name "$NAME" --network host --cpuset-cpus "$SERVER_CPUS" --memory "$MEM" \
    --no-healthcheck -v "$MODELS/$(dirname "$file"):/models/gguf:ro" "$SERVER_IMAGE" \
    -m "/models/gguf/$(basename "$file")" --alias "$served" --host 127.0.0.1 --port "$PORT" \
    --ctx-size $((PARALLEL * SLOT_CTX)) --parallel "$PARALLEL" \
    --threads "$THREADS" --threads-batch "$THREADS" --cpu-mask "$mask" --cpu-strict 1 \
    --metrics --no-webui >/dev/null
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

# The running server's value for command-line flag $1
server_arg() {
  docker inspect -f '{{join .Args " "}}' "$NAME" | grep -o -- "$1 [^ ]*" | cut -d' ' -f2
}

bench() {
  local served=$1 conc=$2 num=$3 seed=$4
  [ "$seed" != "$WARMUP_SEED" ] || { echo "SEED and WARMUP_SEED must differ" >&2; exit 1; }
  curl -sf "http://127.0.0.1:$PORT/v1/models" | grep -q "\"$served\"" \
    || { echo "$NAME does not serve $served" >&2; exit 1; }
  local model src precision build out
  model=$(server_arg -m)
  src=$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/models/gguf"}}{{.Source}}{{end}}{{end}}' "$NAME")
  precision=$(basename "$model" .gguf | sed 's/.*-//' | tr '[:lower:]' '[:upper:]')
  build=$(docker run --rm "$SERVER_IMAGE" --version 2>&1 | sed -n 's/^version: .*(build \([0-9]*\).*/b\1/p')
  out=$(mktemp -d)
  local client=(docker run --rm --network host --cpuset-cpus "$CLIENT_CPUS"
                -v "$MODELS/$TOKENIZER_DIR:/models/financial-lora:ro" -v "$out:/out"
                --entrypoint vllm "$CLIENT_IMAGE" bench serve)
  local args=(--backend vllm --base-url "http://127.0.0.1:$PORT" --endpoint /v1/completions
              --model /models/financial-lora --served-model-name "$served"
              --dataset-name random --random-input-len 1024 --random-output-len "$OUTPUT_LEN"
              --ignore-eos --request-rate inf --max-concurrency "$conc"
              --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,99)
  "${client[@]}" "${args[@]}" --seed "$WARMUP_SEED" --num-prompts 16 >/dev/null 2>&1 \
    || { echo "warmup failed" >&2; exit 1; }
  local p0 p1 g0 g1
  p0=$(counter prompt_tokens); g0=$(counter tokens_predicted)
  "${client[@]}" "${args[@]}" --seed "$seed" --num-prompts "$num" --save-result --save-detailed \
    --result-dir /out --result-filename bench.json --metadata device=cpu backend=llama.cpp \
    "backend_version=$build" "dtype=$precision" "quantization=$precision" \
    "weights_bytes=$(stat -c %s "$src/$(basename "$model")")" "weights_file=$(basename "$model")" \
    "pinned_cores=$(server_arg --threads)" "server_cpuset=$SERVER_CPUS" \
    "cpu_mask=$(server_arg --cpu-mask)" "parallel=$(server_arg --parallel)" \
    "ctx_size=$(server_arg --ctx-size)" "server_image=$SERVER_IMAGE" \
    "seed=$seed" "warmup_seed=$WARMUP_SEED" "cpu_model=$(lscpu | sed -n 's/^Model name: *//p')" >&2
  p1=$(counter prompt_tokens); g1=$(counter tokens_predicted)
  python3 "$(dirname "$0")/bench_fix_llamacpp.py" "$out/bench.json" "$OUTPUT_LEN" \
    $((g1 - g0)) $((p1 - p0))
}

case "${1:-}" in
convert)
  convert "${2:?usage: vm_bench_cpu_gguf.sh convert <model-dir>}"
  ;;
serve)
  serve "${2:?usage: vm_bench_cpu_gguf.sh serve <gguf-file> <served-name>}" \
        "${3:?usage: vm_bench_cpu_gguf.sh serve <gguf-file> <served-name>}"
  ;;
bench)
  bench "${2:?usage: vm_bench_cpu_gguf.sh bench <served-name> <concurrency> <num-prompts>}" \
        "${3:?usage: vm_bench_cpu_gguf.sh bench <served-name> <concurrency> <num-prompts>}" \
        "${4:?usage: vm_bench_cpu_gguf.sh bench <served-name> <concurrency> <num-prompts>}" "$SEED"
  ;;
stop)
  docker rm -f "$NAME"
  ;;
sweep)
  FILE=${2:?usage: vm_bench_cpu_gguf.sh sweep <gguf-file> <served-name> <out-dir>}
  SERVED=${3:?usage: vm_bench_cpu_gguf.sh sweep <gguf-file> <served-name> <out-dir>}
  OUT=${4:?usage: vm_bench_cpu_gguf.sh sweep <gguf-file> <served-name> <out-dir>}
  mkdir -p "$OUT"
  for T in $SWEEP_THREADS; do
    THREADS=$T PARALLEL=16
    serve "$FILE" "$SERVED" >&2
    for C in $SWEEP_CONC; do
      N=$((8 * C > 32 ? 8 * C : 32))
      echo "sweep: threads $T, concurrency $C, $N prompts, seed $((T * 100 + C))" >&2
      bench "$SERVED" "$C" "$N" $((T * 100 + C)) > "$OUT/$SERVED-t$T-c$C.json"
    done
    docker rm -f "$NAME" >/dev/null
  done
  ;;
*)
  echo "usage: vm_bench_cpu_gguf.sh convert <model-dir> | serve <gguf-file> <served-name> | bench <served-name> <concurrency> <num-prompts> | stop | sweep <gguf-file> <served-name> <out-dir>" >&2
  exit 1
  ;;
esac
