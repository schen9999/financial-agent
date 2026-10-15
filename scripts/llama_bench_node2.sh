#!/bin/bash
# Node 2 (vm-a10-inst-2, single-node k3s) mirror of scripts/llama_bench_cpu.sh,
# the 2026-10-08 OKE E5 sweep: llama-bench from llama.cpp b11347, the
# endpoint's own Q4_K_M GGUF (hostPath), -p 512,2048 -n 128 -r 3 -o json,
# one Job per level with guaranteed CPU (request = limit) and -t = the level.
# No judge, no Anthropic spend.
#   CPU levels: the SAME `full` CPU image as the E5 run (identical binary; no
#     GPU backend compiled in, so nothing can offload to the A10 — stronger
#     than -ngl 0 on the CUDA build, which may still offload prompt matmuls).
#     The literal level `max` resolves to the node's free CPU (allocatable
#     minus every running pod's requests), printed beside nproc.
#   GPU level `gpu`: the `full-cuda12` image of the same release (CUDA 12.8.1,
#     as the endpoint's server-cuda12 image), one A10, -ngl 99, -t 8 (the
#     endpoint's --threads).
# The GPU endpoint (deploy/llamacpp) is scaled to 0 for the whole run (it holds
# ~20.5 GB of the A10, and a CPU sweep beside a live endpoint would share the
# memory bandwidth it measures) and restored to 1 on exit. vLLM must already be
# at 0 and stays there. Refuses if the endpoint served a request in the last
# 15 minutes (an OKE run may be in flight; check the operator first, runbook).
#   bash scripts/llama_bench_node2.sh 4 8 15 max gpu
# Output: ~/llama-bench-node2-<date>/{cpu-P<n>.json,gpu.json,run.log,host.txt}
set -u
NS=financial-agent
CPU_IMAGE=ghcr.io/ggml-org/llama.cpp@sha256:eecd2fa8525f683721848bf21df479515636bfd4f4448c3c85af1fec6ade7a13   # full-b11347 (the E5 run's image)
GPU_IMAGE=ghcr.io/ggml-org/llama.cpp@sha256:d4e6e6971b816f622c7af3bd427b860f4e45353a4ee487a14d8ef6006eb3039e   # full-cuda12-b11347 (CUDA 12.8.1)
WEIGHTS=/home/ubuntu/models/qwen3.6-35b-a3b-gguf
MODEL=/models/Qwen3.6-35B-A3B-Q4_K_M.gguf
OUT=~/llama-bench-node2-$(date -u +%Y%m%d); mkdir -p "$OUT"
log() { echo "[bench $(date -u +%FT%TZ)] $*" | tee -a "$OUT/run.log"; }

# ── guards ──────────────────────────────────────────────────────────────────
vllm=$(kubectl -n $NS get deploy vllm -o jsonpath='{.spec.replicas}' 2>/dev/null || echo 0)
[ "${vllm:-0}" = "0" ] || { echo "refusing: vllm replicas=$vllm, must be 0 (CLAUDE.md Targets)"; exit 1; }
recent=$(kubectl -n $NS logs deploy/llamacpp -c llama-server --since=15m 2>/dev/null | grep -c "launch_slot_" || true)
[ "${recent:-0}" = "0" ] || { echo "refusing: the endpoint started $recent tasks in the last 15 min"; exit 1; }
[ -f "$WEIGHTS/Qwen3.6-35B-A3B-Q4_K_M.gguf" ] || { echo "refusing: no GGUF at $WEIGHTS"; exit 1; }

# ── host record: CPU, memory, GPU, OCI shape (no IPs, no OCIDs) ─────────────
{
  echo "## date"; date -u +%FT%TZ
  echo "## nproc"; nproc
  echo "## lscpu"; lscpu
  echo "## free -g"; free -g
  echo "## nvidia-smi"; nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
  echo "## OCI shape"; curl -s -m 5 -H "Authorization: Bearer Oracle" http://169.254.169.254/opc/v2/instance/shape; echo
  echo "## OCI shapeConfig"; curl -s -m 5 -H "Authorization: Bearer Oracle" http://169.254.169.254/opc/v2/instance/shapeConfig; echo
  echo "## GGUF"; stat -c '%n %s bytes' "$WEIGHTS/Qwen3.6-35B-A3B-Q4_K_M.gguf"
} > "$OUT/host.txt" 2>&1
log "host recorded: $(grep -m1 'Model name' "$OUT/host.txt" | sed 's/  */ /g'), nproc $(nproc)"

log "scaling llamacpp to 0 (vllm stays 0)"
kubectl -n $NS scale deploy/llamacpp --replicas=0
kubectl -n $NS wait --for=delete pod -l app.kubernetes.io/name=llamacpp --timeout=300s

restore() {
  kubectl -n $NS delete job llama-bench-node2 --ignore-not-found >/dev/null
  log "restoring llamacpp to 1"
  kubectl -n $NS scale deploy/llamacpp --replicas=1
  kubectl -n $NS rollout status deploy/llamacpp --timeout=1800s | tail -1 | tee -a "$OUT/run.log"
  nvidia-smi --query-compute-apps=process_name,used_memory --format=csv,noheader | tee -a "$OUT/run.log"
  log "vllm replicas: $(kubectl -n $NS get deploy vllm -o jsonpath='{.spec.replicas}' 2>/dev/null || echo absent)"
}
trap restore EXIT

free_cpu() {  # allocatable minus requests of every non-finished pod, in whole vCPU
  node=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
  alloc=$(kubectl get node "$node" -o jsonpath='{.status.allocatable.cpu}')
  kubectl get pods -A --field-selector spec.nodeName="$node",status.phase!=Succeeded,status.phase!=Failed \
    -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.resources.requests.cpu}{"\n"}{end}{end}' \
    | python3 -c "
import sys
def m(v):
    v = v.strip()
    return 0 if not v else int(v[:-1]) if v.endswith('m') else int(float(v) * 1000)
used = sum(m(l) for l in sys.stdin)
print((m('$alloc') - used) // 1000)"
}

for L in "$@"; do
  if [ "$L" = "gpu" ]; then
    NAME=gpu; IMG=$GPU_IMAGE; T=8
    ARGS='"-ngl", "99", '; RES='requests: {cpu: "8", memory: 26Gi, nvidia.com/gpu: "1"}
            limits: {cpu: "8", memory: 26Gi, nvidia.com/gpu: "1"}'
  else
    [ "$L" = "max" ] && { L=$(free_cpu); log "max resolves to $L free vCPU (nproc $(nproc))"; }
    NAME=cpu-P$L; IMG=$CPU_IMAGE; T=$L; ARGS=''
    RES="requests: {cpu: \"$L\", memory: 26Gi}
            limits: {cpu: \"$L\", memory: 26Gi}"
  fi
  log "level $NAME (-t $T)"
  kubectl -n $NS delete job llama-bench-node2 --ignore-not-found >/dev/null
  cat <<EOF | kubectl apply -f - >/dev/null
apiVersion: batch/v1
kind: Job
metadata:
  name: llama-bench-node2
  namespace: $NS
  labels: {app.kubernetes.io/part-of: financial-agent}
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: bench
          image: $IMG
          command: ["/app/llama-bench", "-m", "$MODEL", ${ARGS}"-t", "$T", "-p", "512,2048", "-n", "128", "-r", "3", "-o", "json"]
          resources:
            $RES
          volumeMounts: [{name: models, mountPath: /models, readOnly: true}]
      volumes: [{name: models, hostPath: {path: $WEIGHTS, type: Directory}}]
EOF
  kubectl -n $NS wait --for=condition=complete job/llama-bench-node2 --timeout=60m \
    || { log "level $NAME did not complete"; kubectl -n $NS describe job llama-bench-node2 | tail -5 | tee -a "$OUT/run.log";
         kubectl -n $NS logs job/llama-bench-node2 2>&1 | tail -5 | tee -a "$OUT/run.log"; exit 1; }
  kubectl -n $NS logs job/llama-bench-node2 | sed -n '/^\[/,/^\]/p' > "$OUT/$NAME.json"
  log "level $NAME done: $(python3 -c "import json; print([(r['n_prompt'], r['n_gen'], r['n_threads'], r['n_gpu_layers'], r['backends'], round(r['avg_ts'],2)) for r in json.load(open('$OUT/$NAME.json'))])")"
done
