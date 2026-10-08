#!/bin/bash
# Bring up (or re-apply) the public Streamlit UI on the provided OKE cluster.
# Operator, repo root. Needs: the gitignored allowlist
# (k8s/overlays/oke-provided-public-ui/allowlist.txt) and the two Secrets
# (scripts/public_ui_secrets.sh). Refuses while an eval runs.
#
# PUBLIC_UI_MODE (default sl):
#   sl      security-list management mode All, no NSG (in use since
#           2026-10-08: the controller may manage security lists, may not
#           create NSGs). Guards: BEFORE the apply, every rule on the LB
#           subnet's security list that admits 443 must come from an
#           allowlist CIDR exactly (scripts/public_ui_guard.py sl); AFTER it,
#           the same, plus a rule for every allowlist entry, the LB attached
#           to no NSG and listening on 443 with TLS only. Any failure after
#           the apply puts the Service back to ClusterIP at once.
#   nsg     NSG mode (refused in this tenancy: 404 on CreateNetworkSecurityGroup)
#   attach  join the existing NSG ATTACH_NSG_NAME (refused while it admits 0.0.0.0/0)
#
#   bash scripts/public_ui_up.sh            # diff, then apply
#   bash scripts/public_ui_up.sh --diff     # diff only
set -euo pipefail
NS=financial-agent
OV=k8s/overlays/oke-provided-public-ui
MODE=${PUBLIC_UI_MODE:-sl}
LB_SUBNET_NAME=${LB_SUBNET_NAME:-pub_lb-tbhcuw}
BACKEND_NSG_NAME=${BACKEND_NSG_NAME:-workers-tbhcuw}

running=$(kubectl -n "$NS" get workflows --no-headers 2>/dev/null | awk '$2=="Running"{print $1}')
if [ -n "$running" ]; then echo "refusing: eval running: $running"; exit 1; fi
for s in streamlit-basic-auth streamlit-tls; do
  kubectl -n "$NS" get secret "$s" >/dev/null 2>&1 || { echo "missing Secret $s: run scripts/public_ui_secrets.sh"; exit 1; }
done

CL=$(kubectl config view --minify -o json | python3 -c 'import json,sys; a=json.load(sys.stdin)["users"][0]["user"]["exec"]["args"]; print(a[a.index("--cluster-id")+1])')
VCN=$(oci ce cluster get --cluster-id "$CL" --query 'data."vcn-id"' --raw-output)
VC=$(oci network vcn get --vcn-id "$VCN" --query 'data."compartment-id"' --raw-output)
SUBNET=$(oci network subnet list --compartment-id "$VC" --vcn-id "$VCN" --display-name "$LB_SUBNET_NAME" --query 'data[0].id' --raw-output)
SL=$(oci network subnet get --subnet-id "$SUBNET" --query 'data."security-list-ids"[0]' --raw-output)

revert() {
  echo "REVERTING: Service back to ClusterIP ($1)"
  kubectl apply -k k8s/overlays/oke-provided >/dev/null
  kubectl -n "$NS" get svc streamlit
  exit 1
}

case "$MODE" in
  sl)
    oci network security-list get --security-list-id "$SL" | python3 scripts/public_ui_guard.py sl --port 443 \
      || { echo "refusing: $LB_SUBNET_NAME's security list already admits 443 wider than the allowlist"; exit 1; }
    python3 scripts/public_ui_render.py --lb-subnet "$SUBNET" --security-list ;;
  nsg)
    NSG=$(oci network nsg list --compartment-id "$VC" --vcn-id "$VCN" --display-name "$BACKEND_NSG_NAME" --query 'data[0].id' --raw-output)
    python3 scripts/public_ui_render.py --lb-subnet "$SUBNET" --backend-nsg "$NSG" ;;
  attach)
    NSG=$(oci network nsg list --compartment-id "$VC" --vcn-id "$VCN" --display-name "$ATTACH_NSG_NAME" --query 'data[0].id' --raw-output)
    open_rules=$(oci network nsg rules list --nsg-id "$NSG" --all --query "length(data[?direction=='INGRESS' && source=='0.0.0.0/0' && protocol!='1'])" --raw-output)
    if [ "$open_rules" != "0" ]; then
      echo "refusing: $ATTACH_NSG_NAME still has $open_rules non-ICMP ingress rule(s) from 0.0.0.0/0"; exit 1
    fi
    python3 scripts/public_ui_render.py --lb-subnet "$SUBNET" --attach-nsg "$NSG" ;;
  *) echo "unknown PUBLIC_UI_MODE $MODE"; exit 2 ;;
esac

kubectl diff -k "$OV" | sed -E 's/ocid1\.[a-z0-9.]+/<ocid>/g' || true
[ "${1:-}" = "--diff" ] && exit 0
kubectl apply -k "$OV"
kubectl -n "$NS" rollout status deploy/streamlit --timeout=300s
ip=""
for i in $(seq 1 60); do
  ip=$(kubectl -n "$NS" get svc streamlit -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  [ -n "$ip" ] && break
  sleep 10
done
if [ -z "$ip" ]; then
  kubectl -n "$NS" describe svc streamlit | sed -n '/Events/,$p' | sed -E 's/ocid1\.[a-z0-9.]+/<ocid>/g' | tail -8
  revert "no external IP after 10 min"
fi
echo "external IP: $ip"
if [ "$MODE" = "sl" ]; then
  sleep 30   # let the controller finish its security-list update
  oci network security-list get --security-list-id "$SL" | python3 scripts/public_ui_guard.py sl --port 443 --require \
    || revert "security list not limited to the allowlist"
  LB=$(oci lb load-balancer list --compartment-id "$VC" --all --query "data[?\"display-name\"=='$(kubectl -n "$NS" get svc streamlit -o jsonpath='{.metadata.uid}')'].id | [0]" --raw-output)
  oci lb load-balancer get --load-balancer-id "$LB" | python3 scripts/public_ui_guard.py lb --port 443 \
    || revert "load balancer has an NSG or a listener other than TLS 443"
fi
echo "public UI up at https://$ip/ (guards passed)"
