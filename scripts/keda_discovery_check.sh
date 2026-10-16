#!/usr/bin/env bash
# API discovery health around a KEDA install (make keda-check).
#
# KEDA registers the aggregated APIService v1beta1.external.metrics.k8s.io.
# If that APIService is registered but its backend is not serving (or is
# left behind by an uninstall), every discovery client — kubectl, helm,
# the namespace controller, garbage collection — gets "unable to retrieve
# the complete list of server APIs", and namespace deletion can hang.
#
#   scripts/keda_discovery_check.sh installed     # after make keda-install
#   scripts/keda_discovery_check.sh uninstalled   # after make keda-uninstall
#   scripts/keda_discovery_check.sh discovery     # checks 1-2 only (before install)
#
# Exit 0 only if every check passes. Read-only: get/list calls only.
set -uo pipefail

MODE=${1:-}
case "$MODE" in installed|uninstalled|discovery) ;; *) echo "usage: $0 installed|uninstalled|discovery"; exit 2;; esac
KEDA_NS=${KEDA_NAMESPACE:-keda}
APISVC=v1beta1.external.metrics.k8s.io
fail=0
ok()  { echo "  OK    $*"; }
bad() { echo "  FAIL  $*"; fail=1; }

echo "== 1. discovery: kubectl api-resources (full list, stderr captured)"
err=$(mktemp); trap 'rm -f "$err"' EXIT
if kubectl api-resources >/dev/null 2>"$err"; then rc=0; else rc=$?; fi
if grep -qi "unable to retrieve the complete list of server APIs" "$err"; then
  bad "discovery incomplete:"; sed 's/^/        /' "$err"
elif [ "$rc" -ne 0 ]; then
  bad "kubectl api-resources exit $rc:"; sed 's/^/        /' "$err"
else
  ok "api-resources complete (exit 0, no discovery error on stderr)"
fi

echo "== 2. every APIService Available=True"
notavail=$(kubectl get apiservice -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.conditions[?(@.type=="Available")].status}{"\n"}{end}' | awk '$2!="True"')
if [ -n "$notavail" ]; then bad "not available:"; echo "$notavail" | sed 's/^/        /'; else ok "all $(kubectl get apiservice --no-headers | wc -l) APIServices Available"; fi

if [ "$MODE" = discovery ]; then
  :
elif [ "$MODE" = installed ]; then
  echo "== 3. $APISVC"
  svc=$(kubectl get apiservice "$APISVC" -o jsonpath='{.spec.service.namespace}/{.spec.service.name}' 2>/dev/null)
  [ "$svc" = "$KEDA_NS/keda-operator-metrics-apiserver" ] && ok "served by $svc" || bad "backed by '${svc:-<absent>}', expected $KEDA_NS/keda-operator-metrics-apiserver"
  if kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1" >/dev/null 2>"$err"; then ok "GET /apis/external.metrics.k8s.io/v1beta1 answers"; else bad "GET /apis/external.metrics.k8s.io/v1beta1: $(head -1 "$err")"; fi
  for d in keda-operator keda-operator-metrics-apiserver keda-admission-webhooks; do
    a=$(kubectl -n "$KEDA_NS" get deploy "$d" -o jsonpath='{.status.availableReplicas}' 2>/dev/null)
    [ "${a:-0}" -ge 1 ] && ok "deploy/$d available ($a)" || bad "deploy/$d not available"
  done
  m=$(kubectl get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.service.namespace}/{.spec.service.name}' 2>/dev/null)
  echo "  info  v1beta1.metrics.k8s.io (resource metrics, not KEDA's) backed by ${m:-<absent>}"
else
  echo "== 3. KEDA remnants"
  if kubectl get apiservice "$APISVC" >/dev/null 2>&1; then bad "$APISVC still registered (a dangling APIService breaks discovery)"; else ok "$APISVC absent"; fi
  crds=$(kubectl get crd -o name | grep -E 'keda\.sh$' || true)
  [ -z "$crds" ] && ok "no keda.sh CRDs left" || { bad "keda.sh CRDs left:"; echo "$crds" | sed 's/^/        /'; }
  vwc=$(kubectl get validatingwebhookconfiguration keda-admission -o name 2>/dev/null)
  [ -z "$vwc" ] && ok "ValidatingWebhookConfiguration keda-admission absent" || bad "keda-admission webhook configuration left"
  cr=$(kubectl get clusterrole,clusterrolebinding -o name | grep -i keda || true)
  [ -z "$cr" ] && ok "no keda ClusterRoles/Bindings left" || { bad "keda cluster RBAC left:"; echo "$cr" | sed 's/^/        /'; }
  rb=$(kubectl -n kube-system get rolebinding -o name | grep -i keda || true)
  [ -z "$rb" ] && ok "no keda RoleBinding left in kube-system" || { bad "keda RoleBinding left in kube-system:"; echo "$rb" | sed 's/^/        /'; }
  if kubectl get ns "$KEDA_NS" >/dev/null 2>&1; then bad "namespace $KEDA_NS still exists ($(kubectl get ns "$KEDA_NS" -o jsonpath='{.status.phase}'))"; else ok "namespace $KEDA_NS gone"; fi
fi

echo
if [ "$fail" -eq 0 ]; then echo "DISCOVERY CHECK ($MODE): PASS"; else echo "DISCOVERY CHECK ($MODE): FAIL"; fi
exit "$fail"
