#!/bin/bash
# CPU core-scaling benchmark of the self-served model (operator; no judge,
# no Anthropic spend). llama-bench from llama.cpp b11347 (the `full` image —
# the endpoint's `server` image has no llama-bench), the endpoint's own
# Q4_K_M GGUF from the llamacpp-models PVC, one Job per level with
# guaranteed CPU (request = limit) and -t = the level, pinned to the
# endpoint's node. The CPU endpoint is scaled to 0 for the duration (no
# contention; the RWO volume attaches to one pod) and restored after.
#   bash scripts/llama_bench_cpu.sh 4 8 15      # levels in vCPU
# Output: ~/llama-bench-cpu-<date>/P<n>.json (llama-bench -o json) + run.log
set -u
NS=financial-agent
IMAGE=ghcr.io/ggml-org/llama.cpp@sha256:eecd2fa8525f683721848bf21df479515636bfd4f4448c3c85af1fec6ade7a13  # full-b11347
MODEL=/models/Qwen3.6-35B-A3B-Q4_K_M.gguf
OUT=~/llama-bench-cpu-$(date -u +%Y%m%d); mkdir -p "$OUT"
log() { echo "[bench $(date -u +%FT%TZ)] $*" | tee -a "$OUT/run.log"; }

running=$(kubectl -n $NS get workflows --no-headers 2>/dev/null | awk '$2=="Running"{print $1}')
[ -n "$running" ] && { echo "refusing: eval running: $running"; exit 1; }
NODE=$(kubectl -n $NS get pods -l app.kubernetes.io/name=llamacpp -o jsonpath='{.items[0].spec.nodeName}')
log "endpoint node $NODE; scaling llamacpp to 0"
kubectl -n $NS scale deploy/llamacpp --replicas=0
kubectl -n $NS wait --for=delete pod -l app.kubernetes.io/name=llamacpp --timeout=300s

restore() {
  log "restoring llamacpp to 1"
  kubectl -n $NS scale deploy/llamacpp --replicas=1
  kubectl -n $NS rollout status deploy/llamacpp --timeout=1800s | tail -1 | tee -a "$OUT/run.log"
}
trap restore EXIT

for N in "$@"; do
  log "level $N vCPU"
  kubectl -n $NS delete job llama-bench-cpu --ignore-not-found >/dev/null
  cat <<EOF | kubectl apply -f - >/dev/null
apiVersion: batch/v1
kind: Job
metadata:
  name: llama-bench-cpu
  namespace: $NS
  labels: {app.kubernetes.io/part-of: financial-agent}
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      nodeName: $NODE
      containers:
        - name: bench
          image: $IMAGE
          command: ["/app/llama-bench", "-m", "$MODEL", "-t", "$N", "-p", "512,2048", "-n", "128", "-r", "3", "-o", "json"]
          resources:
            requests: {cpu: "$N", memory: 26Gi}
            limits: {cpu: "$N", memory: 26Gi}
          volumeMounts: [{name: models, mountPath: /models, readOnly: true}]
      volumes: [{name: models, persistentVolumeClaim: {claimName: llamacpp-models, readOnly: true}}]
EOF
  kubectl -n $NS wait --for=condition=complete job/llama-bench-cpu --timeout=60m \
    || { log "level $N did not complete"; kubectl -n $NS logs job/llama-bench-cpu | tail -5 | tee -a "$OUT/run.log"; exit 1; }
  kubectl -n $NS logs job/llama-bench-cpu | sed -n '/^\[/,/^\]/p' > "$OUT/P$N.json"
  log "level $N done: $(python3 -c "import json; print([(r['n_prompt'], r['n_gen'], round(r['avg_ts'],2)) for r in json.load(open('$OUT/P$N.json'))])")"
done
kubectl -n $NS delete job llama-bench-cpu --ignore-not-found >/dev/null
