#!/usr/bin/env bash
# Node 2's GPU llama.cpp endpoint as the OKE cluster sees it: run on the
# operator host, whose egress IP is the cluster's (129.80.187.92), the one
# source the 30880 security-list rule admits. Expect HTTP 401 without the
# key and HTTP 200 with it, serving the plain alias (no -hybrid suffix).
# Read-only: one Secret read for the key, two GETs. The key goes into a
# 0600 header file, is never printed, and the file is shredded on exit.
# The operator's kubectl needs an interactive shell (runbook, "OKE
# (provided cluster)"), so from the laptop:
#   scp scripts/gpu_exposure_check.sh oke-operator:/tmp/ && \
#     ssh -T -n oke-operator 'bash -ic "bash /tmp/gpu_exposure_check.sh"'
# Recorded output: eval/runs/gpu-exposure-check-2026-10-05.txt
set -u
NODE2=${1:-132.145.161.150}
umask 077
H=$(mktemp)
trap 'shred -u "$H" 2>/dev/null' EXIT
K=$(kubectl -n financial-agent get secret slm-endpoints -o jsonpath='{.data.SLM_GPU_API_KEY}' </dev/null | base64 -d)
test -n "$K" || { echo "ERROR: SLM_GPU_API_KEY empty"; exit 1; }
printf 'Authorization: Bearer %s\n' "$K" > "$H"
unset K
echo "=== $(date -u +%FT%TZ) from $(curl -s -m 5 https://ifconfig.me) ==="
echo "--- GET http://$NODE2:30880/v1/models, no key"
curl -s -m 15 -w '\nHTTP %{http_code}\n' "http://$NODE2:30880/v1/models"
echo "--- GET http://$NODE2:30880/v1/models, with the key (SLM_GPU_API_KEY from Secret slm-endpoints)"
curl -s -m 15 -H @"$H" -w '\nHTTP %{http_code}\n' "http://$NODE2:30880/v1/models"
