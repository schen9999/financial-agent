#!/bin/bash
# Bring up (or re-apply) the public Streamlit UI on the provided OKE cluster.
# Operator, repo root. Needs: the gitignored allowlist
# (k8s/overlays/oke-provided-public-ui/allowlist.txt) and the two Secrets
# (scripts/public_ui_secrets.sh). Steps: refuse while an eval runs; look up
# the LB subnet and the workers' NSG by display name; render the gitignored
# files; show the diff; apply; wait for the external IP.
#   bash scripts/public_ui_up.sh            # diff, then apply
#   bash scripts/public_ui_up.sh --diff     # diff only
#   ATTACH_NSG_NAME=pub_lb-tbhcuw bash scripts/public_ui_up.sh
#                                           # fallback: join the owner's LB NSG
set -euo pipefail
NS=financial-agent
OV=k8s/overlays/oke-provided-public-ui
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
if [ -n "${ATTACH_NSG_NAME:-}" ]; then
  # Fallback (the controller may not create NSGs): join the owner's LB NSG,
  # but only once its ingress is limited to the allowlist.
  NSG=$(oci network nsg list --compartment-id "$VC" --vcn-id "$VCN" --display-name "$ATTACH_NSG_NAME" --query 'data[0].id' --raw-output)
  open_rules=$(oci network nsg rules list --nsg-id "$NSG" --all --query "length(data[?direction=='INGRESS' && source=='0.0.0.0/0' && protocol!='1'])" --raw-output)
  if [ "$open_rules" != "0" ]; then
    echo "refusing: $ATTACH_NSG_NAME still has $open_rules non-ICMP ingress rule(s) from 0.0.0.0/0 (the owner's three changes are not in yet)"
    exit 1
  fi
  python3 scripts/public_ui_render.py --lb-subnet "$SUBNET" --attach-nsg "$NSG"
else
  NSG=$(oci network nsg list --compartment-id "$VC" --vcn-id "$VCN" --display-name "$BACKEND_NSG_NAME" --query 'data[0].id' --raw-output)
  python3 scripts/public_ui_render.py --lb-subnet "$SUBNET" --backend-nsg "$NSG"
fi

kubectl diff -k "$OV" | sed -E 's/ocid1\.[a-z0-9.]+/<ocid>/g' || true
[ "${1:-}" = "--diff" ] && exit 0
kubectl apply -k "$OV"
kubectl -n "$NS" rollout status deploy/streamlit --timeout=300s
for i in $(seq 1 60); do
  ip=$(kubectl -n "$NS" get svc streamlit -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  [ -n "$ip" ] && { echo "external IP: $ip"; exit 0; }
  sleep 10
done
echo "no external IP after 10 min; events:"
kubectl -n "$NS" describe svc streamlit | sed -n '/Events/,$p' | sed -E 's/ocid1\.[a-z0-9.]+/<ocid>/g'
exit 1
