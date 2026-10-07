#!/bin/bash
# The only way to run Terraform in terraform/oci-provided/ (the PROVIDED OKE
# cluster: import and plan only, never apply; CLAUDE.md, the 2026-10-07
# exception). Allowed: init, fmt, validate, plan, show, providers, state
# list|show. Everything else — apply, destroy, import (the CLI form writes
# state outside a plan), taint, untaint, refresh, state mv|rm|push, console,
# workspace, force-unlock — is refused, and so is -auto-approve anywhere.
#   bash scripts/tf_provided.sh init
#   bash scripts/tf_provided.sh plan -generate-config-out=generated.tf
#   bash scripts/tf_provided.sh plan -detailed-exitcode     # 0 = zero diff
set -euo pipefail
DIR="$(cd "$(dirname "$0")/.." && pwd)/terraform/oci-provided"
[ $# -ge 1 ] || { echo "usage: tf_provided.sh <init|fmt|validate|plan|show|providers|state list|state show> [args]"; exit 2; }
for a in "$@"; do
  case "$a" in -auto-approve|-auto-approve=*) echo "refused: -auto-approve"; exit 3;; esac
done
cmd="$1"
case "$cmd" in
  init|fmt|validate|plan|show|providers) ;;
  state)
    case "${2:-}" in list|show) ;; *) echo "refused: state ${2:-} (only list and show)"; exit 3;; esac ;;
  *) echo "refused: terraform $cmd (import and plan only; apply never — CLAUDE.md)"; exit 3;;
esac
if [ "$cmd" = "plan" ]; then
  for a in "$@"; do
    case "$a" in -out|-out=*) echo "refused: plan -out (a saved plan exists only to be applied)"; exit 3;; esac
  done
fi
exec terraform -chdir="$DIR" "$@"
