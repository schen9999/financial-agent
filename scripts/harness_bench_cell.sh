#!/usr/bin/env bash
# One repeat of one harness-benchmark cell, on the operator host
# (docs/harness-benchmark-plan.md; runbook "Harness benchmark").
#
#   scripts/harness_bench_cell.sh PROFILE R C REPEAT [OUT_ROOT]
#   KEDA=1 scripts/harness_bench_cell.sh L1 4 1 1      # autoscaler run, 1..4 pods
#
# Needs `make bench-stub-on` first. For the cell it:
#   1. sets the worker to C Celery processes and R replicas (KEDA paused at R
#      when a ScaledObject exists; KEDA=1 un-pauses it instead), with the
#      pod's CPU and memory limits scaled by C so every process keeps the
#      deployed per-process budget (1.5 CPU, 2 GiB); rollout restart, so
#      every pod starts the cell with fresh cgroup counters
#   2. snapshots cgroup cpu.stat / memory of every worker, api, redis and
#      model-stub pod, plus restart counts
#   3. runs the driver Job (scripts/harness_bench.py) with a `kubectl top`
#      loop every 15 s beside it
#   4. snapshots again and captures the driver, stub and worker logs, pods
#      and events into OUT_ROOT/<cell>-r<REPEAT>/
# Nothing is read from stdin (kubectl's oci credential plugin consumes it).
set -euo pipefail

PROFILE=${1:?PROFILE L0|L1|L2}; R=${2:?replicas}; C=${3:?concurrency}; REPEAT=${4:?repeat}
OUT_ROOT=${5:-$HOME/harness-bench/$(date -u +%Y-%m-%d)}
NS=${NAMESPACE:-financial-agent}
BRIEFS=${BRIEFS:-40}; WARMUP=${WARMUP:-5}
KEDA=${KEDA:-0}
REPO=$(cd "$(dirname "$0")/.." && pwd)

if [ "$KEDA" = 1 ]; then CELL="${PROFILE}-keda-c${C}"; else CELL="${PROFILE}-r${R}-c${C}"; fi
OUT="$OUT_ROOT/${CELL}-r${REPEAT}"
mkdir -p "$OUT"
log() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$OUT/cell.log"; }

kubectl -n "$NS" get deploy/model-stub >/dev/null 2>&1 || { echo "ERROR: no model-stub — make bench-stub-on first"; exit 1; }
[ "$(kubectl -n "$NS" get configmap app-config -o jsonpath='{.data.SLM_CPU_URL}')" = "http://model-stub.$NS.svc:8080" ] || {
  echo "ERROR: app-config SLM_CPU_URL is not the stub — make bench-stub-on first"; exit 1; }

IMAGE=$(kubectl -n "$NS" get deploy/worker -o jsonpath='{.spec.template.spec.containers[0].image}')
HAS_SO=0; kubectl -n "$NS" get scaledobject worker >/dev/null 2>&1 && HAS_SO=1
if [ "$KEDA" = 1 ] && [ "$HAS_SO" = 0 ]; then echo "ERROR: KEDA=1 needs the worker ScaledObject (make keda-worker)"; exit 1; fi

# ── 1. worker shape ─────────────────────────────────────────────────────────
log "cell $CELL repeat $REPEAT: R=$R C=$C profile=$PROFILE keda=$KEDA image=$IMAGE"
CPU_LIM=$((1500 * C))m; MEM_LIM=$((2 * C))Gi
kubectl -n "$NS" patch deployment worker --type json -p "[
  {\"op\":\"replace\",\"path\":\"/spec/template/spec/containers/0/command\",
   \"value\":[\"celery\",\"-A\",\"celery_worker.celery_app\",\"worker\",\"--loglevel=info\",\"--concurrency=$C\"]},
  {\"op\":\"replace\",\"path\":\"/spec/template/spec/containers/0/resources/limits\",
   \"value\":{\"cpu\":\"$CPU_LIM\",\"memory\":\"$MEM_LIM\"}}]" >/dev/null
if [ "$HAS_SO" = 1 ]; then
  if [ "$KEDA" = 1 ]; then
    kubectl -n "$NS" annotate scaledobject worker autoscaling.keda.sh/paused-replicas- >/dev/null 2>&1 || true
  else
    kubectl -n "$NS" annotate --overwrite scaledobject worker autoscaling.keda.sh/paused-replicas="$R" >/dev/null
  fi
fi
[ "$KEDA" = 1 ] || kubectl -n "$NS" scale deployment/worker --replicas="$R" >/dev/null
kubectl -n "$NS" rollout restart deployment/worker >/dev/null
kubectl -n "$NS" rollout status deployment/worker --timeout=900s | tail -1 | tee -a "$OUT/cell.log"
if [ "$KEDA" != 1 ]; then
  for _ in $(seq 1 90); do
    READY=$(kubectl -n "$NS" get deploy/worker -o jsonpath='{.status.readyReplicas}')
    TOTAL=$(kubectl -n "$NS" get pods -l app.kubernetes.io/name=worker --no-headers 2>/dev/null | wc -l)
    [ "${READY:-0}" = "$R" ] && [ "$TOTAL" = "$R" ] && break
    sleep 10
  done
  [ "${READY:-0}" = "$R" ] || { log "ERROR: worker has ${READY:-0} ready pods, wanted $R"; exit 1; }
fi
# The new pods must reach the stub through the app's own client.
kubectl -n "$NS" exec deploy/worker -- python -c \
  "import json; from agent.tools.slm import server_facts; f=server_facts(); assert f['slm_served_name']=='model-stub', f; print('stub reachable from worker:', f['slm_url'])" \
  | tee -a "$OUT/cell.log"

# ── 2. snapshots ────────────────────────────────────────────────────────────
pods() { kubectl -n "$NS" get pods -l "app.kubernetes.io/name in (worker,api,redis,model-stub)" \
           --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{" "}{end}'; }
snapshot() {  # $1 = before|after
  local f="$OUT/cgroup-$1.txt"; : > "$f"
  for p in $(pods); do
    echo "=== pod $p t=$(date -u +%s.%N)" >> "$f"
    kubectl -n "$NS" exec "$p" -c "$(kubectl -n "$NS" get pod "$p" -o jsonpath='{.spec.containers[0].name}')" -- sh -c '
      if [ -f /sys/fs/cgroup/cpu.stat ]; then
        echo "cgroup v2"; cat /sys/fs/cgroup/cpu.stat
        for k in memory.current memory.peak memory.max; do [ -f /sys/fs/cgroup/$k ] && echo "$k $(cat /sys/fs/cgroup/$k)"; done
      else
        echo "cgroup v1"; echo "cpuacct.usage $(cat /sys/fs/cgroup/cpuacct/cpuacct.usage 2>/dev/null || cat /sys/fs/cgroup/cpu,cpuacct/cpuacct.usage)"
        cat /sys/fs/cgroup/cpu/cpu.stat 2>/dev/null || cat /sys/fs/cgroup/cpu,cpuacct/cpu.stat
        echo "memory.usage_in_bytes $(cat /sys/fs/cgroup/memory/memory.usage_in_bytes)"
        echo "memory.max_usage_in_bytes $(cat /sys/fs/cgroup/memory/memory.max_usage_in_bytes)"
      fi' >> "$f" 2>&1 || echo "snapshot failed" >> "$f"
  done
  kubectl -n "$NS" get pods -o json > "$OUT/pods-$1.json"
}
snapshot before
log "snapshot before: $(grep -c '^=== pod' "$OUT/cgroup-before.txt") pods"

# ── 3. driver Job + top loop ────────────────────────────────────────────────
JOB="harness-bench-$(echo "$CELL" | tr 'A-Z' 'a-z')-r${REPEAT}-$(date -u +%H%M%S)"
ARGS="\"--cell\",\"$CELL\",\"--repeat\",\"$REPEAT\",\"--profile\",\"$PROFILE\",\"--replicas\",\"$R\",\"--concurrency\",\"$C\",\"--briefs\",\"$BRIEFS\",\"--warmup\",\"$WARMUP\""
sed -e "s|JOB_NAME|$JOB|" -e "s|APP_IMAGE|$IMAGE|" -e "s|BENCH_ARGS|$ARGS|" \
  "$REPO/k8s/model-stub/driver-job.yaml" > "$OUT/job.yaml"
( while true; do
    echo "--- $(date -u +%s)"; kubectl top pods -n "$NS" --no-headers 2>&1; kubectl top nodes --no-headers 2>&1
    sleep 15
  done ) > "$OUT/top.txt" 2>&1 &
TOP_PID=$!
trap 'kill $TOP_PID 2>/dev/null || true' EXIT
T_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
kubectl create -f "$OUT/job.yaml" >/dev/null
log "driver job $JOB started"
STATUS=running
while [ "$STATUS" = running ]; do
  sleep 20
  S=$(kubectl -n "$NS" get job "$JOB" -o jsonpath='{.status.succeeded}')
  F=$(kubectl -n "$NS" get job "$JOB" -o jsonpath='{.status.failed}')
  [ "${S:-0}" -ge 1 ] && STATUS=succeeded
  [ "${F:-0}" -ge 1 ] && STATUS=failed
done
kill $TOP_PID 2>/dev/null || true
log "driver job $JOB $STATUS"

# ── 4. after ────────────────────────────────────────────────────────────────
snapshot after
kubectl -n "$NS" logs "job/$JOB" > "$OUT/driver.log" 2>&1 || true
kubectl -n "$NS" logs deploy/model-stub --since-time="$T_START" > "$OUT/stub.log" 2>&1 || true
kubectl -n "$NS" logs -l app.kubernetes.io/name=worker --prefix --tail=-1 --since-time="$T_START" \
  --max-log-requests=8 > "$OUT/worker.log" 2>&1 || true
kubectl -n "$NS" get events -o json > "$OUT/events.json" 2>&1 || true
kubectl get nodes -o json > "$OUT/nodes.json" 2>&1 || true
grep -h "BENCH_SUMMARY" "$OUT/driver.log" | head -1 | cut -c1-400 | tee -a "$OUT/cell.log" || true
log "done: $OUT"
[ "$STATUS" = succeeded ]
