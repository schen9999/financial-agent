#!/bin/bash
# Create the public Streamlit UI's two Secrets on the operator (once; re-run
# with --rotate to replace them). Prints the certificate's SHA-256
# fingerprint, nothing else secret:
#   - streamlit-basic-auth: an htpasswd line for user "reviewer" with a random
#     password (openssl passwd -6, SHA-512 crypt). The password is kept in
#     ~/public-ui/credentials (0600) on the operator and never printed; read it
#     in your own terminal: ssh oke-operator cat public-ui/credentials
#   - streamlit-tls: a self-signed certificate (RSA 2048, 365 days) for the
#     LB's TLS listener. The certificate is kept in ~/public-ui/tls.crt; the
#     key exists only in a 0600 temp dir and is shredded after the Secret is made.
# Operator rule: secrets go to kubectl as files, never on stdin.
set -euo pipefail
umask 077
NS=financial-agent
DIR="$HOME/public-ui"
mkdir -p "$DIR"
if kubectl -n "$NS" get secret streamlit-basic-auth >/dev/null 2>&1 && [ "${1:-}" != "--rotate" ]; then
  echo "secrets exist; pass --rotate to replace them"
  openssl x509 -in "$DIR/tls.crt" -noout -fingerprint -sha256
  exit 0
fi
TMP=$(mktemp -d)
trap 'shred -u "$TMP"/* 2>/dev/null || true; rmdir "$TMP"' EXIT

openssl rand -base64 24 | tr -d '/+=\n' > "$DIR/credentials.new"
printf 'reviewer:%s\n' "$(openssl passwd -6 -stdin < "$DIR/credentials.new")" > "$TMP/htpasswd"
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -subj "/CN=financial-agent-ui" \
  -keyout "$TMP/tls.key" -out "$TMP/tls.crt" 2>/dev/null

kubectl -n "$NS" delete secret streamlit-basic-auth streamlit-tls --ignore-not-found >/dev/null
kubectl -n "$NS" create secret generic streamlit-basic-auth --from-file=htpasswd="$TMP/htpasswd" >/dev/null
kubectl -n "$NS" create secret tls streamlit-tls --cert="$TMP/tls.crt" --key="$TMP/tls.key" >/dev/null
mv "$DIR/credentials.new" "$DIR/credentials"
cp "$TMP/tls.crt" "$DIR/tls.crt"
echo "created streamlit-basic-auth (user reviewer; password in ~/public-ui/credentials) and streamlit-tls"
openssl x509 -in "$DIR/tls.crt" -noout -fingerprint -sha256
