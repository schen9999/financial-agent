#!/usr/bin/env bash
# Live test of the KEDA-scaled Celery worker (make keda-scale-test).
#
# Spends no Anthropic credit and enqueues nothing the worker can fail on:
# the only task sent is Celery's builtin `celery.accumulate`, registered on
# every Celery app, which returns its arguments — no agent import, no
# network, no model call (tests/test_keda_worker.py pins that). It never
# sends research_task.
#
# Why the original worker stops consuming for the test: one worker drains
# accumulate tasks in milliseconds, so the queue would never be deep enough
# for KEDA to see. `celery control cancel_consumer` on that worker leaves
# the backlog in the Redis list; KEDA must then scale the Deployment up and
# the NEW pods must drain it. The consumer is added back on every exit
# (trap). If the script is killed hard, restore it by hand:
#   kubectl -n financial-agent rollout restart deployment/worker
# A real async brief submitted during the window waits for a new pod.
#
# Passes only if: the external metric reports the backlog, the HPA scales
# the worker to min(max, ceil(N / listLength)), every task SUCCEEDS on a
# new pod with no error in any worker log, the worker returns to 1 replica,
# every remaining worker consumes the celery queue again, and discovery is
# still healthy.
set -uo pipefail

NS=${NAMESPACE:-financial-agent}
N=${KEDA_TEST_TASKS:-8}
UP_TIMEOUT=${KEDA_UP_TIMEOUT:-900}       # new worker pods: image pull + startupProbe
DOWN_TIMEOUT=${KEDA_DOWN_TIMEOUT:-900}   # 300 s stabilization + 1 pod / 60 s
CELERY=(celery -A celery_worker.celery_app)

say()  { echo "[$(date -u +%H:%M:%SZ)] $*"; }
die()  { say "FAIL: $*"; exit 1; }
jget() { kubectl -n "$NS" get "$@" 2>/dev/null; }

# ── preconditions: KEDA owns the worker, and the worker is idle ─────────────
ready=$(jget scaledobject worker -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
[ "$ready" = True ] || die "ScaledObject worker not Ready (is KEDA installed and make keda-worker applied?)"
HPA=$(jget scaledobject worker -o jsonpath='{.status.hpaName}')
[ -n "$HPA" ] || die "ScaledObject has no HPA"
MIN=$(jget scaledobject worker -o jsonpath='{.spec.minReplicaCount}')
MAX=$(jget scaledobject worker -o jsonpath='{.spec.maxReplicaCount}')
LISTLEN=$(jget scaledobject worker -o jsonpath='{.spec.triggers[0].metadata.listLength}')
LIST=$(jget scaledobject worker -o jsonpath='{.spec.triggers[0].metadata.listName}')
DB=$(jget scaledobject worker -o jsonpath='{.spec.triggers[0].metadata.databaseIndex}')
METRIC=$(jget hpa "$HPA" -o jsonpath='{.spec.metrics[0].external.metric.name}')
EXPECT=$(( (N + LISTLEN - 1) / LISTLEN )); [ "$EXPECT" -gt "$MAX" ] && EXPECT=$MAX; [ "$EXPECT" -lt "$MIN" ] && EXPECT=$MIN
say "ScaledObject worker: min=$MIN max=$MAX list=$LIST db=$DB listLength=$LISTLEN hpa=$HPA metric=$METRIC"
say "test: $N x celery.accumulate -> expect $EXPECT replicas"
[ "$MIN" = 1 ] || die "minReplicaCount is $MIN, expected 1"
[ "$EXPECT" -ge 2 ] || die "N=$N with listLength $LISTLEN would not scale past 1; raise KEDA_TEST_TASKS"

llen()   { kubectl -n "$NS" exec deploy/redis -- redis-cli -n "$DB" LLEN "$LIST" | tr -d '\r'; }
metric() { kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/$NS/$METRIC?labelSelector=scaledobject.keda.sh%2Fname%3Dworker" \
             | python3 -c 'import json,sys; i=json.load(sys.stdin)["items"]; print(i[0]["value"] if i else "none")'; }
spec_replicas()  { jget deploy worker -o jsonpath='{.spec.replicas}'; }
ready_replicas() { r=$(jget deploy worker -o jsonpath='{.status.readyReplicas}'); echo "${r:-0}"; }
# Running and not terminating: a pod being removed keeps phase Running until it exits
worker_pods()    { jget pods -l app.kubernetes.io/name=worker -o json | python3 -c 'import json,sys
for p in json.load(sys.stdin)["items"]:
    if p["status"].get("phase") == "Running" and not p["metadata"].get("deletionTimestamp"): print(p["metadata"]["name"])'; }
all_worker_pods() { jget pods -l app.kubernetes.io/name=worker --no-headers | wc -l; }
# queues a worker consumes, as a space-separated list ("" = none)
queues_of() { kubectl -n "$NS" exec "$1" -c worker -- "${CELERY[@]}" inspect active_queues --json -d "celery@$1" --timeout 10 2>/dev/null \
                | python3 -c 'import json,sys; d=json.load(sys.stdin); print(" ".join(q["name"] for v in d.values() for q in v))'; }
active_of() { kubectl -n "$NS" exec "$1" -c worker -- "${CELERY[@]}" inspect active --json -d "celery@$1" --timeout 10 2>/dev/null \
                | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(len(v) for v in d.values()))'; }

[ "$(spec_replicas)" = 1 ] && [ "$(ready_replicas)" = 1 ] || die "worker is at $(spec_replicas) replicas ($(ready_replicas) ready); run when it is back at 1"
[ "$(llen)" = 0 ] || die "queue '$LIST' holds $(llen) real messages; run when it is empty"
POD=$(worker_pods | head -1)
[ "$(active_of "$POD")" = 0 ] || die "worker $POD is running a task; run when it is idle"
[[ " $(queues_of "$POD") " == *" $LIST "* ]] || die "worker $POD does not consume '$LIST' before the test"
say "precondition ok: 1 idle worker ($POD), queue empty, metric=$(metric)"

T0=$(date +%s)
restore() {
  if kubectl -n "$NS" get pod "$POD" >/dev/null 2>&1 && [[ " $(queues_of "$POD") " != *" $LIST "* ]]; then
    say "restore: add_consumer $LIST on $POD"
    kubectl -n "$NS" exec "$POD" -c worker -- "${CELERY[@]}" control add_consumer "$LIST" -d "celery@$POD" >/dev/null
  fi
}
trap restore EXIT

# ── 1. stop the original worker consuming; enqueue the harmless backlog ─────
kubectl -n "$NS" exec "$POD" -c worker -- "${CELERY[@]}" control cancel_consumer "$LIST" -d "celery@$POD" >/dev/null
[ -z "$(queues_of "$POD")" ] || die "cancel_consumer did not take on $POD"
say "1. $POD stopped consuming '$LIST'"

IDS=$(kubectl -n "$NS" exec deploy/api -c api -- python -c "
import json
from celery_worker import celery_app
print(json.dumps([celery_app.send_task('celery.accumulate', args=[i], queue='$LIST').id for i in range($N)]))" | tail -1)
[ "$(echo "$IDS" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')" = "$N" ] || die "enqueue failed: $IDS"
say "   enqueued $N celery.accumulate tasks; LLEN $LIST = $(llen)"

# ── 2. KEDA sees the backlog ───────────────────────────────────────────────
seen=""; for _ in $(seq 1 12); do m=$(metric); [ "$m" = "$N" ] && { seen=$m; break; }; sleep 5; done
[ -n "$seen" ] || die "external metric $METRIC never reported $N (last: $m)"
say "2. external metric $METRIC = $seen"

# ── 3. the HPA scales the worker up; new pods drain the backlog ────────────
peak=1; t=0
while [ "$(ready_replicas)" -lt 2 ]; do
  s=$(spec_replicas); [ "$s" -gt "$peak" ] && peak=$s
  [ "$t" -ge "$UP_TIMEOUT" ] && die "no second worker Ready within ${UP_TIMEOUT}s (spec.replicas=$s)"
  sleep 10; t=$((t + 10))
done
s=$(spec_replicas); [ "$s" -gt "$peak" ] && peak=$s
say "3. scaled up: spec.replicas peak $peak, $(ready_replicas) ready after ${t}s"
[ "$peak" = "$EXPECT" ] || die "peak spec.replicas $peak, expected $EXPECT"

states=""; for _ in $(seq 1 60); do
  states=$(kubectl -n "$NS" exec deploy/api -c api -- python -c "
import json, collections
from celery_worker import celery_app
ids = json.loads('$IDS')
print(dict(collections.Counter(celery_app.AsyncResult(i).state for i in ids)))" | tail -1)
  [ "$states" = "{'SUCCESS': $N}" ] && break; sleep 5
done
[ "$states" = "{'SUCCESS': $N}" ] || die "task states $states, expected all $N SUCCESS"
[ "$(llen)" = 0 ] || die "queue not drained: LLEN $(llen)"
say "   all $N tasks SUCCESS, queue drained"

SINCE=$(( $(date +%s) - T0 + 30 ))s; errs=0; ran=0
for p in $(worker_pods); do
  log=$(kubectl -n "$NS" logs "$p" -c worker --since="$SINCE")
  e=$(echo "$log" | grep -cE "ERROR|Traceback|unregistered|Received unregistered" || true)
  r=$(echo "$log" | grep -c "Task celery.accumulate\[.*\] succeeded" || true)
  say "   $p: $r accumulate succeeded, $e error lines"
  errs=$((errs + e)); ran=$((ran + r))
  [ "$p" = "$POD" ] && [ "$r" != 0 ] && die "$POD ran tasks while its consumer was cancelled"
done
[ "$errs" = 0 ] || die "$errs error lines in worker logs"
[ "$ran" = "$N" ] || die "worker logs show $ran succeeded, expected $N"
kubectl -n "$NS" exec deploy/api -c api -- python -c "
import json
from celery_worker import celery_app
[celery_app.AsyncResult(i).forget() for i in json.loads('$IDS')]" >/dev/null && say "   results forgotten (Redis keys removed)"

# ── 4. restore the original consumer, then KEDA scales back to min ─────────
restore
[[ " $(queues_of "$POD") " == *" $LIST "* ]] || die "$POD does not consume '$LIST' after restore"
say "4. $POD consumes '$LIST' again; waiting for scale-down to $MIN"
t=0; while [ "$(spec_replicas)" != "$MIN" ] || [ "$(ready_replicas)" != "$MIN" ] || [ "$(all_worker_pods)" != "$MIN" ]; do
  [ "$t" -ge "$DOWN_TIMEOUT" ] && die "still at $(spec_replicas) replicas after ${DOWN_TIMEOUT}s"
  sleep 15; t=$((t + 15))
done
say "   back to $MIN replica, removed pods gone, after ${t}s"

# ── 5. what is left consumes the queue; nothing queued; discovery healthy ──
for p in $(worker_pods); do
  q=$(queues_of "$p"); [[ " $q " == *" $LIST "* ]] || die "remaining worker $p consumes '$q', not '$LIST'"
  say "5. remaining worker $p consumes '$q'"
done
[ "$(llen)" = 0 ] || die "queue holds $(llen) after the test"
bash "$(dirname "$0")/keda_discovery_check.sh" installed >/dev/null || die "discovery check failed after the test (run make keda-check)"
say "   discovery check: PASS"
echo
echo "KEDA SCALE TEST: PASS — $N tasks, metric $seen, 1 -> $peak -> $MIN replicas, $(( $(date +%s) - T0 ))s"
