#!/usr/bin/env bash
# scripts/vm_bootstrap.sh — take a fresh Ubuntu 22.04 or 24.04 VM with an NVIDIA A10
# (driver preinstalled) to "make vm-up ready" in one run.
#
# STATUS: NOT YET EXECUTED (Phase 1.75). Authored 2026-09-09 from the steps
# applied by hand on the VM 2026-09-02/03 (docs/deploy-runbook.md, single-VM
# section, "hand-fix ledger"). Per CLAUDE.md nothing here counts as EXECUTED
# until it has run on the box and the closing checklist was confirmed from
# terminal output.
#
# Steps, in order — every one is idempotent, so re-running is always safe:
#   1. base packages (make, jq, rsync, ufw, curl, gnupg, git, python3)
#   2. ufw: default deny incoming, allow 22/tcp ONLY, enable
#   3. Docker CE + docker-buildx-plugin (BuildKit: Dockerfile.k8s relies on a
#      per-Dockerfile ignore file, a BuildKit-only feature; the Makefile sets
#      DOCKER_BUILDKIT=1 on its build lines); login user added to `docker`
#   4. nvidia-container-toolkit + Docker runtime (nvidia-ctk) — the plain
#      Docker path that validated the serving args on 2026-09-02
#   5. k3s with `default-runtime: nvidia` in /etc/rancher/k3s/config.yaml;
#      restart when the config (or the toolkit) changed under a running k3s
#   6. /etc/rancher/k3s/k3s.yaml -> ~/.kube/config; KUBECONFIG export in ~/.bashrc
#   7. NVIDIA device plugin (static manifest, pinned to DEVICE_PLUGIN_VERSION)
#   8. hostPath parents the k3s overlays mount: /home/ubuntu/models
#      (k8s/vllm/overlays/k3s-gpu) and /home/ubuntu/eval-findings (argo/overlays/k3s)
#   9. strip `extra_special_tokens` from models/*/tokenizer_config.json when
#      weights are present (the transformers bundled in vllm v0.10.2 crashes on
#      the list form). Runs after the weights rsync: re-run the script then.
#  10. checklist: nvidia-smi, kubectl get nodes (+ nvidia.com/gpu allocatable),
#      docker buildx version, ufw, k3s, kubeconfig, dirs, tokenizer.
#      Exit status is non-zero if any row FAILs.
#
# Run ON the VM, from the repo checkout, as the login user (ubuntu) — NOT
# root; sudo is used where needed (passwordless on the OCI Ubuntu image):
#     bash scripts/vm_bootstrap.sh
# Afterwards log out and back in (docker group + KUBECONFIG take effect at
# login) or `newgrp docker` before `make vm-images && make vm-up`.
#
# Optional env: K3S_VERSION (pins INSTALL_K3S_VERSION; default: whatever
# get.k3s.io serves, matching the unpinned 2026-09-03 install),
# DEVICE_PLUGIN_VERSION (default v0.17.0), MODELS_DIR, EVAL_FINDINGS_DIR.
set -euo pipefail

DEVICE_PLUGIN_VERSION="${DEVICE_PLUGIN_VERSION:-v0.17.0}"
K3S_VERSION="${K3S_VERSION:-}"
MODELS_DIR="${MODELS_DIR:-/home/ubuntu/models}"                       # k3s-gpu overlay: hostPath $MODELS_DIR/qwen-ft
EVAL_FINDINGS_DIR="${EVAL_FINDINGS_DIR:-/home/ubuntu/eval-findings}"  # argo k3s overlay: hostPath $EVAL_FINDINGS_DIR/<wf>
K3S_CONFIG=/etc/rancher/k3s/config.yaml
K3S_KUBECONFIG=/etc/rancher/k3s/k3s.yaml
CONTAINERD_TOML=/var/lib/rancher/k3s/agent/etc/containerd/config.toml
DEVICE_PLUGIN_URL="https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/${DEVICE_PLUGIN_VERSION}/deployments/static/nvidia-device-plugin.yml"
BASHRC_LINE='export KUBECONFIG=$HOME/.kube/config'

ME=$(id -un)
log() { printf '\n[bootstrap] %s\n' "$*"; }
die() { printf '[bootstrap] ERROR: %s\n' "$*" >&2; exit 1; }
# sudo drops the environment: pass the apt knobs explicitly so nothing prompts
# (needrestart on 22.04 would otherwise pop an interactive menu mid-run).
apt_get() { sudo env DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a apt-get -y -qq "$@"; }

[ "$(id -u)" -ne 0 ] || die "run as the login user (ubuntu), not root — the script uses sudo where needed"
command -v sudo >/dev/null || die "sudo not found"
sudo -v || die "sudo credentials required"

RUNTIME_CHANGED=0   # toolkit installed or k3s config written in this run -> k3s + device plugin restart

# ── 0. driver is a precondition, not a step (the VM image ships driver 570) ──
log "0/9 NVIDIA driver (preinstalled on the VM image; this script never installs drivers)"
command -v nvidia-smi >/dev/null || die "nvidia-smi not found. On a plain Ubuntu image run: sudo apt-get update && sudo apt-get install -y ubuntu-drivers-common && sudo ubuntu-drivers install --gpgpu && sudo reboot, then re-run this script."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | sed 's/^/    /'

# ── 1. base packages ─────────────────────────────────────────────────────────
log "1/9 base packages"
apt_get update
apt_get install ca-certificates curl gnupg git make jq rsync ufw python3
sudo install -m 0755 -d /etc/apt/keyrings

# ── 2. ufw: 22/tcp only ──────────────────────────────────────────────────────
# The VCN security list (22 only) is the authoritative gate; ufw is
# defense-in-depth. NodePorts bind on the VM and are reached only through
# ssh -L tunnels. vm-up went green on 2026-09-03 with exactly this baseline
# (single-node pod/service traffic is unaffected).
log "2/9 ufw: default deny incoming, allow 22/tcp only"
sudo ufw default deny incoming >/dev/null
sudo ufw default allow outgoing >/dev/null
sudo ufw allow 22/tcp >/dev/null        # BEFORE enable — never lock the ssh session out
sudo ufw --force enable >/dev/null      # --force skips the interactive "may disrupt ssh" prompt
sudo ufw status | sed 's/^/    /'

# ── 3. Docker CE + buildx ────────────────────────────────────────────────────
# Docker's own apt repo: Ubuntu's docker.io package ships no buildx plugin.
log "3/9 Docker CE + docker-buildx-plugin"
need_docker=0
command -v docker >/dev/null || need_docker=1
sudo docker buildx version >/dev/null 2>&1 || need_docker=1
if [ "$need_docker" = 1 ]; then
  if [ ! -f /etc/apt/keyrings/docker.asc ]; then
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
  fi
  if [ ! -f /etc/apt/sources.list.d/docker.list ]; then
    codename=$(. /etc/os-release && echo "$VERSION_CODENAME")
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${codename} stable" \
      | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
    apt_get update
  fi
  apt_get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin
fi
sudo systemctl enable --now docker >/dev/null
if ! id -nG "$ME" | grep -qw docker; then
  sudo usermod -aG docker "$ME"
  echo "    added $ME to the docker group — effective at next login (or: newgrp docker)"
fi

# ── 4. nvidia-container-toolkit ──────────────────────────────────────────────
log "4/9 nvidia-container-toolkit"
if ! command -v nvidia-ctk >/dev/null; then
  if [ ! -f /etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg ]; then
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
      | sudo gpg --dearmor -o /etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg
  fi
  if [ ! -f /etc/apt/sources.list.d/nvidia-container-toolkit.list ]; then
    curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
      | sed 's#deb https://#deb [signed-by=/etc/apt/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
      | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list >/dev/null
    apt_get update
  fi
  apt_get install nvidia-container-toolkit
  RUNTIME_CHANGED=1   # k3s only detects the nvidia runtime at (re)start
fi
# Docker side — the runbook's "Validated so far (2026-09-02)" used exactly this.
if ! sudo docker info --format '{{json .Runtimes}}' 2>/dev/null | grep -q '"nvidia"'; then
  sudo nvidia-ctk runtime configure --runtime=docker
  sudo systemctl restart docker
fi

# ── 5. k3s with default-runtime: nvidia ──────────────────────────────────────
# k3s auto-registers the nvidia containerd runtime it finds via the toolkit,
# but only pods with runtimeClassName: nvidia would use it. Making it the
# DEFAULT lets the device plugin's static manifest (no runtimeClassName) see
# the GPUs and keeps the vLLM manifests free of a RuntimeClass — the shape
# the k3s-gpu overlay assumes. Written BEFORE install so a fresh k3s starts
# with it; on an existing k3s a changed config triggers a restart.
log "5/9 k3s (default-runtime: nvidia in $K3S_CONFIG)"
sudo install -m 0755 -d /etc/rancher/k3s
K3S_CONFIG_CONTENT=$(cat <<'YAML'
# Written by scripts/vm_bootstrap.sh — single-node k3s on the A10 VM.
# default-runtime: every pod runs under the nvidia containerd runtime that k3s
# auto-detects from nvidia-container-toolkit (device plugin + vLLM need it;
# no RuntimeClass in the manifests). Re-running the script re-asserts this.
default-runtime: nvidia
YAML
)
if [ ! -f "$K3S_CONFIG" ] || [ "$(sudo cat "$K3S_CONFIG")" != "$K3S_CONFIG_CONTENT" ]; then
  printf '%s\n' "$K3S_CONFIG_CONTENT" | sudo tee "$K3S_CONFIG" >/dev/null
  RUNTIME_CHANGED=1
fi
if ! command -v k3s >/dev/null; then
  if [ -n "$K3S_VERSION" ]; then
    curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="$K3S_VERSION" sh -
  else
    curl -sfL https://get.k3s.io | sh -
  fi
elif [ "$RUNTIME_CHANGED" = 1 ]; then
  echo "    runtime config changed under an installed k3s — restarting k3s"
  sudo systemctl restart k3s
else
  sudo systemctl start k3s   # no-op when already running
fi

# ── 6. kubeconfig for the login user ─────────────────────────────────────────
log "6/9 kubeconfig: $K3S_KUBECONFIG -> ~/.kube/config (+ KUBECONFIG in ~/.bashrc)"
for i in $(seq 1 30); do
  sudo test -f "$K3S_KUBECONFIG" && break
  echo "    waiting for k3s to write $K3S_KUBECONFIG ($i/30)..."; sleep 2
done
sudo test -f "$K3S_KUBECONFIG" || die "$K3S_KUBECONFIG never appeared — check: sudo journalctl -u k3s"
mkdir -p "$HOME/.kube"
if ! sudo cmp -s "$K3S_KUBECONFIG" "$HOME/.kube/config"; then
  sudo cp "$K3S_KUBECONFIG" "$HOME/.kube/config"
  sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"
fi
chmod 600 "$HOME/.kube/config"
export KUBECONFIG="$HOME/.kube/config"
if ! grep -qxF "$BASHRC_LINE" "$HOME/.bashrc" 2>/dev/null; then
  printf '\n# k3s kubeconfig (scripts/vm_bootstrap.sh)\n%s\n' "$BASHRC_LINE" >> "$HOME/.bashrc"
fi
# Right after a (re)start the apiserver answers before the node is Ready — retry.
for i in $(seq 1 36); do
  kubectl wait --for=condition=Ready node --all --timeout=10s >/dev/null 2>&1 && break
  echo "    waiting for the k3s node to be Ready ($i/36)..."; sleep 5
done
kubectl wait --for=condition=Ready node --all --timeout=60s

# ── 7. NVIDIA device plugin ──────────────────────────────────────────────────
log "7/9 NVIDIA device plugin ${DEVICE_PLUGIN_VERSION}"
plugin_existed=0
kubectl -n kube-system get ds nvidia-device-plugin-daemonset >/dev/null 2>&1 && plugin_existed=1
kubectl apply -f "$DEVICE_PLUGIN_URL"
if [ "$plugin_existed" = 1 ] && [ "$RUNTIME_CHANGED" = 1 ]; then
  # A plugin pod started under runc before the runtime change never sees NVML.
  kubectl -n kube-system rollout restart ds/nvidia-device-plugin-daemonset
fi
GPU_ALLOC=""
for i in $(seq 1 24); do
  GPU_ALLOC=$(kubectl get nodes -o jsonpath='{.items[0].status.allocatable.nvidia\.com/gpu}' 2>/dev/null || true)
  [ -n "$GPU_ALLOC" ] && [ "$GPU_ALLOC" != "0" ] && break
  echo "    waiting for nvidia.com/gpu to become allocatable ($i/24)..."; sleep 5
done

# ── 8. hostPath parents ──────────────────────────────────────────────────────
# Owned by the login user so the weights rsync needs no sudo. Existing dirs
# are left untouched (ownership included). vLLM mounts $MODELS_DIR/qwen-ft
# with type: Directory — the rsync creates that leaf; the eval overlay's
# hostPath is DirectoryOrCreate and creates $EVAL_FINDINGS_DIR/<wf> itself.
log "8/9 hostPath parents: $MODELS_DIR, $EVAL_FINDINGS_DIR"
for d in "$MODELS_DIR" "$EVAL_FINDINGS_DIR"; do
  [ -d "$d" ] || sudo install -d -o "$(id -u)" -g "$(id -g)" "$d"
done

# ── 9. tokenizer_config.json: strip extra_special_tokens ─────────────────────
# The merged checkpoint ships extra_special_tokens as a JSON list (newer
# transformers layout); the transformers bundled in vllm v0.10.2 crashes on
# it ("'list' object has no attribute 'keys'"). The special tokens stay fully
# defined in tokenizer.json, so deleting the key is the whole fix (hit on
# the VM 2026-09-02). The repo's untracked financial-lora-merged/ still
# carries the list form, so this must run after EVERY rsync — re-run the
# script; steps 1–8 no-op.
log "9/9 tokenizer_config.json: strip extra_special_tokens (vllm v0.10.2)"
shopt -s nullglob
TOK_FILES=("$MODELS_DIR"/*/tokenizer_config.json)
shopt -u nullglob
if [ ${#TOK_FILES[@]} -eq 0 ]; then
  echo "    no weights under $MODELS_DIR yet — rsync them (runbook step 2), then re-run this script"
else
  for f in "${TOK_FILES[@]}"; do
    python3 - "$f" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    cfg = json.load(fh)
if "extra_special_tokens" in cfg:
    del cfg["extra_special_tokens"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cfg, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"    stripped extra_special_tokens: {path}")
else:
    print(f"    already clean: {path}")
PY
  done
fi

# ── checklist ────────────────────────────────────────────────────────────────
log "checklist (vm-up readiness)"
FAIL=0
check() {  # status label detail
  printf '  [%s] %-28s %s\n' "$1" "$2" "$3"
  [ "$1" != FAIL ] || FAIL=1
}

if smi=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null); then
  check PASS "nvidia-smi" "$(echo "$smi" | paste -sd, -)"
else
  check FAIL "nvidia-smi" "not working"
fi

if sudo ufw status | grep -q '^Status: active' && sudo ufw status | grep -q '^22/tcp'; then
  extra=$(sudo ufw status | grep ALLOW | grep -vc '^22/tcp' || true)
  if [ "$extra" = 0 ]; then check PASS "ufw" "active, 22/tcp only"
  else check WARN "ufw" "active, but $extra allow rule(s) beyond 22/tcp — review: sudo ufw status numbered"; fi
else
  check FAIL "ufw" "inactive or 22/tcp not allowed"
fi

if bx=$(docker buildx version 2>/dev/null); then
  check PASS "docker buildx version" "$bx"
elif bx=$(sudo docker buildx version 2>/dev/null); then
  check WARN "docker buildx version" "$bx (via sudo — re-login for the docker group before make vm-images)"
else
  check FAIL "docker buildx version" "buildx plugin missing"
fi

if sudo docker info --format '{{json .Runtimes}}' 2>/dev/null | grep -q '"nvidia"'; then
  check PASS "docker nvidia runtime" "registered (nvidia-ctk)"
else
  check FAIL "docker nvidia runtime" "not registered"
fi

if systemctl is-active --quiet k3s; then check PASS "k3s" "active"; else check FAIL "k3s" "not active"; fi

if sudo grep -q 'default_runtime_name = "nvidia"' "$CONTAINERD_TOML" 2>/dev/null; then
  check PASS "containerd default runtime" "nvidia ($CONTAINERD_TOML)"
else
  check WARN "containerd default runtime" "no default_runtime_name = \"nvidia\" in $CONTAINERD_TOML — the nvidia.com/gpu row below is the real test"
fi

if [ -f "$HOME/.kube/config" ] && kubectl config current-context >/dev/null 2>&1; then
  check PASS "kubeconfig" "$HOME/.kube/config, context $(kubectl config current-context)"
else
  check FAIL "kubeconfig" "$HOME/.kube/config missing or unusable"
fi
if grep -qxF "$BASHRC_LINE" "$HOME/.bashrc"; then
  check PASS "KUBECONFIG in ~/.bashrc" "$BASHRC_LINE"
else
  check FAIL "KUBECONFIG in ~/.bashrc" "line missing"
fi

echo "  kubectl get nodes:"
kubectl get nodes -o custom-columns='NAME:.metadata.name,STATUS:.status.conditions[-1].type,VERSION:.status.nodeInfo.kubeletVersion,GPU(nvidia.com/gpu):.status.allocatable.nvidia\.com/gpu' | sed 's/^/    /'
if [ -n "$GPU_ALLOC" ] && [ "$GPU_ALLOC" != "0" ]; then
  check PASS "nvidia.com/gpu allocatable" "$GPU_ALLOC (the A10.2 exposes 2; the k3s-gpu overlay requests 1)"
else
  check FAIL "nvidia.com/gpu allocatable" "none — device plugin logs: kubectl -n kube-system logs ds/nvidia-device-plugin-daemonset"
fi

if kubectl get storageclass local-path >/dev/null 2>&1; then
  check PASS "StorageClass local-path" "present (Postgres PVC, 50Gi)"
else
  check FAIL "StorageClass local-path" "missing — k3s should bundle it"
fi

for d in "$MODELS_DIR" "$EVAL_FINDINGS_DIR"; do
  if [ -d "$d" ]; then check PASS "dir $d" "$(stat -c '%U:%G %a' "$d")"; else check FAIL "dir $d" "missing"; fi
done

if [ -d "$MODELS_DIR/qwen-ft" ]; then
  if [ ${#TOK_FILES[@]} -gt 0 ] && ! grep -q '"extra_special_tokens"' "$MODELS_DIR"/*/tokenizer_config.json 2>/dev/null; then
    check PASS "weights + tokenizer" "$MODELS_DIR/qwen-ft present, extra_special_tokens absent"
  else
    check FAIL "weights + tokenizer" "extra_special_tokens still present or tokenizer_config.json missing"
  fi
else
  check WARN "weights + tokenizer" "$MODELS_DIR/qwen-ft absent — rsync the merged checkpoint, re-run this script (runbook step 2), then make vm-up"
fi

echo
if [ "$FAIL" = 1 ]; then
  die "checklist has FAIL rows — fix them before make vm-images / make vm-up"
fi
echo "[bootstrap] vm-up ready (any WARN rows above still apply). Next: log out/in (or newgrp docker),"
echo "[bootstrap] rsync the weights if not done, then: make vm-images && make vm-up"
