#!/usr/bin/env bash
# Does Celery's warm shutdown finish the in-flight task on SIGTERM, within
# the worker's terminationGracePeriodSeconds? (make worker-shutdown-test)
#
# A probe pod runs the worker's own image, Celery app (celery_worker.py) and
# grace period (read from deploy/worker), plus one extra task,
# `shutdown_probe.sleep`, from a ConfigMap. It consumes ONLY the queue
# "worker-shutdown-probe": the real worker never receives a probe task (it
# would fail on it as unregistered), and nothing calls a model, so no
# Anthropic credit is spent. Tasks are sent from the api pod by name.
#
# Case A (the worker's grace): 2 sleep tasks, the first running, the second
#   prefetched; delete the pod mid-task. Pass: the running task SUCCEEDS
#   after SIGTERM, the pod exits once it is done (before the grace runs
#   out), and the prefetched task is back in the queue, not lost.
# Case B (grace shorter than the task): 1 task; delete the pod. Pass: the
#   kubelet's SIGKILL ends it and the task never completes (state stays
#   STARTED) — what happens to a brief longer than the grace.
#
# Cleans up the probe pod, ConfigMap, queue key and result records.
set -uo pipefail

NS=${NAMESPACE:-financial-agent}
Q=worker-shutdown-probe
SLEEP=${PROBE_SLEEP:-45}         # task length, s; must be < grace for case A
SHORT_GRACE=${PROBE_SHORT_GRACE:-10}
CELERY_APP=shutdown_probe:celery_app

say() { echo "[$(date -u +%H:%M:%SZ)] $*"; }
die() { say "FAIL: $*"; exit 1; }

GRACE=$(kubectl -n "$NS" get deploy worker -o jsonpath='{.spec.template.spec.terminationGracePeriodSeconds}')
IMAGE=$(kubectl -n "$NS" get deploy worker -o jsonpath='{.spec.template.spec.containers[0].image}')
PULL=$(kubectl -n "$NS" get deploy worker -o jsonpath='{.spec.template.spec.imagePullSecrets[0].name}')
POLICY=$(kubectl -n "$NS" get deploy worker -o jsonpath='{.spec.template.spec.containers[0].imagePullPolicy}')
say "deploy/worker: terminationGracePeriodSeconds=$GRACE image=$IMAGE"
[ -n "$GRACE" ] && [ "$SLEEP" -lt "$GRACE" ] || die "need PROBE_SLEEP ($SLEEP) < the worker's grace ($GRACE)"

api_py() { kubectl -n "$NS" exec deploy/api -c api -- python -c "from celery_worker import celery_app
$1" | tail -1; }
llen() { kubectl -n "$NS" exec deploy/redis -- redis-cli -n 0 LLEN "$Q" | tr -d '\r'; }
state() { api_py "print(celery_app.AsyncResult('$1').state)"; }
send() { api_py "print(celery_app.send_task('shutdown_probe.sleep', args=[$SLEEP], queue='$Q').id)"; }

cleanup() {
  kubectl -n "$NS" delete pod shutdown-probe --ignore-not-found --grace-period=0 --wait=false >/dev/null 2>&1
  kubectl -n "$NS" delete configmap shutdown-probe --ignore-not-found >/dev/null 2>&1
  kubectl -n "$NS" exec deploy/redis -- redis-cli -n 0 DEL "$Q" >/dev/null 2>&1
  [ -n "${IDS:-}" ] && api_py "[celery_app.AsyncResult(i).forget() for i in '$IDS'.split()]" >/dev/null 2>&1
}
trap cleanup EXIT
IDS=""

kubectl -n "$NS" create configmap shutdown-probe --dry-run=client -o yaml --from-literal=shutdown_probe.py='import time
from celery_worker import celery_app


@celery_app.task(name="shutdown_probe.sleep")
def sleep(seconds):
    time.sleep(seconds)
    return seconds
' | kubectl apply -f - >/dev/null

PULL_LINE=""; [ -n "$PULL" ] && PULL_LINE="imagePullSecrets: [{name: $PULL}]"
start_probe() {   # $1 = grace seconds
  kubectl -n "$NS" delete pod shutdown-probe --ignore-not-found --wait=true >/dev/null 2>&1
  cat <<EOF | kubectl apply -f - >/dev/null
apiVersion: v1
kind: Pod
metadata:
  name: shutdown-probe
  namespace: $NS
  labels: {app.kubernetes.io/name: shutdown-probe, app.kubernetes.io/part-of: financial-agent}
spec:
  terminationGracePeriodSeconds: $1
  restartPolicy: Never
  $PULL_LINE
  containers:
    - name: worker
      image: $IMAGE
      imagePullPolicy: ${POLICY:-IfNotPresent}
      command: ["celery", "-A", "$CELERY_APP", "worker", "-Q", "$Q", "--concurrency=1", "--loglevel=info", "-n", "probe@%h"]
      env: [{name: PYTHONPATH, value: /probe:/app}]
      envFrom: [{configMapRef: {name: app-config}}]
      resources: {requests: {cpu: 100m, memory: 300Mi}, limits: {memory: 1Gi}}
      readinessProbe:
        exec: {command: ["sh", "-c", "celery -A $CELERY_APP inspect ping -d probe@\$HOSTNAME --timeout 10 | grep -q pong"]}
        periodSeconds: 5
        timeoutSeconds: 20
        failureThreshold: 120
      volumeMounts: [{name: probe, mountPath: /probe}]
  volumes: [{name: probe, configMap: {name: shutdown-probe}}]
EOF
  # Ready = the probe worker answers ping (readinessProbe above)
  kubectl -n "$NS" wait --for=condition=Ready pod/shutdown-probe --timeout=600s >/dev/null || {
    kubectl -n "$NS" get pod shutdown-probe -o wide; kubectl -n "$NS" logs shutdown-probe --tail=40
    die "probe worker not Ready (answering ping) within 600s"; }
}

wait_started() { for _ in $(seq 1 60); do [ "$(state "$1")" = STARTED ] && return 0; sleep 1; done; die "task $1 never STARTED"; }

CASES=${PROBE_CASES:-A B}

# ── Case A: the worker's grace ─────────────────────────────────────────────
if [[ " $CASES " == *" A "* ]]; then
say "A. probe worker, grace ${GRACE}s; 2 x sleep(${SLEEP}s)"
start_probe "$GRACE"
T1=$(send); T2=$(send); IDS="$T1 $T2"
wait_started "$T1"
sleep 5
q0=$(llen); say "   running: $T1 STARTED; prefetched: $T2 $(state "$T2"); queue $Q LLEN $q0 (prefetched tasks are off the list)"
t0=$(date +%s)
kubectl -n "$NS" delete pod shutdown-probe --wait=false >/dev/null
say "   SIGTERM sent (pod deleted)"
kubectl -n "$NS" wait --for=delete pod/shutdown-probe --timeout=$((GRACE + 60))s >/dev/null || die "pod still present after grace"
exit_s=$(( $(date +%s) - t0 ))
s1=$(state "$T1"); s2=$(state "$T2"); q=$(llen)
say "   pod gone after ${exit_s}s; $T1 $s1; $T2 $s2; queue LLEN $q"
[ "$s1" = SUCCESS ] || die "in-flight task ended $s1, expected SUCCESS (warm shutdown did not finish it)"
[ "$exit_s" -lt "$GRACE" ] || die "pod took ${exit_s}s, not less than the grace (${GRACE}s): it may have been SIGKILLed"
[ "$s2" = PENDING ] && [ "$q" = 1 ] || die "prefetched task: state $s2, queue LLEN $q; expected PENDING and back in the queue (1)"
say "A. PASS: in-flight task finished under SIGTERM; pod exited ${exit_s}s after SIGTERM, inside the ${GRACE}s grace; the prefetched task (not in LLEN while prefetched) returned to the queue"
kubectl -n "$NS" exec deploy/redis -- redis-cli -n 0 DEL "$Q" >/dev/null
fi

# ── Case B: grace shorter than the task ────────────────────────────────────
if [[ " $CASES " == *" B "* ]]; then
say "B. probe worker, grace ${SHORT_GRACE}s; 1 x sleep(${SLEEP}s)"
start_probe "$SHORT_GRACE"
T3=$(send); IDS="$IDS $T3"
wait_started "$T3"
t0=$(date +%s)
kubectl -n "$NS" delete pod shutdown-probe --wait=false >/dev/null
kubectl -n "$NS" wait --for=delete pod/shutdown-probe --timeout=$((SHORT_GRACE + 60))s >/dev/null || die "pod still present"
exit_s=$(( $(date +%s) - t0 ))
sleep $((SLEEP + 5))   # long enough that the task would have finished had it survived
s3=$(state "$T3"); q=$(llen)
say "   pod gone after ${exit_s}s; $T3 $s3 ${SLEEP}s later; queue LLEN $q"
[ "$s3" = STARTED ] || die "task beyond the grace ended $s3, expected it lost (STARTED forever)"
say "B. PASS: a task longer than the grace is killed and lost (state STARTED, not requeued)"
fi

echo
echo "WORKER SHUTDOWN TEST ($CASES): PASS — grace ${GRACE}s covers a ${SLEEP}s in-flight task; a task past the grace is lost"
