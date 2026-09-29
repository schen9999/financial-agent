#!/usr/bin/env bash
# Node load during a CPU benchmark, one line every 30 s until killed: the
# 1/5/15-min load average, the GPU vLLM pod's CPU (kubectl top, millicores)
# and the benchmark server container's CPU (docker stats; 100% = one vCPU).
# The quant-bench load-*.log files (2026-09-29) come from this; it writes
# the same line format as the 2026-09-28 load logs.
#
# Usage (on the VM): bash scripts/vm_load_sampler.sh <container> <logfile> & ... kill $!
ctr=${1:?usage: vm_load_sampler.sh <container> <logfile>}
log=${2:?usage: vm_load_sampler.sh <container> <logfile>}
while :; do
  l=$(cut -d' ' -f1-3 /proc/loadavg)
  g=$(kubectl -n financial-agent top pod -l app.kubernetes.io/name=vllm --no-headers 2>/dev/null | awk '{print $2}')
  c=$(docker stats --no-stream --format '{{.CPUPerc}}' "$ctr" 2>/dev/null)
  echo "$(date -u +%H:%M:%S) load=$l gpu_pod=$g cpu_ctr=$c" >> "$log"
  sleep 30
done
