#!/usr/bin/env bash
# The harness-benchmark sweep (docs/harness-benchmark-plan.md, "Sweep"), on
# the operator host, after `make bench-stub-on`. Each cell repeat goes
# through scripts/harness_bench_cell.sh; a failed cell is logged and the
# sweep moves on (its directory is kept and the report marks it invalid).
#
#   scripts/harness_bench_sweep.sh core    # L0 and L1 at (1,1) (4,1) (4,4)
#   scripts/harness_bench_sweep.sh rest    # every other planned cell
#   scripts/harness_bench_sweep.sh all     # core then rest
#
# Cells already captured under OUT_ROOT with a BENCH_SUMMARY are skipped, so
# an interrupted sweep resumes where it stopped.
set -uo pipefail
WHICH=${1:-core}
OUT_ROOT=${OUT_ROOT:-$HOME/harness-bench/$(date -u +%Y-%m-%d)}
REPEATS=${REPEATS:-2}
HERE=$(cd "$(dirname "$0")" && pwd)

CORE="L0:1:1 L1:1:1 L0:4:1 L1:4:1 L0:4:4 L1:4:4"
REST=""
for P in L0 L1; do for R in 1 2 4; do for C in 1 2 4; do
  case " $CORE " in *" $P:$R:$C "*) ;; *) REST="$REST $P:$R:$C";; esac
done; done; done
REST="$REST L2:4:4 KEDA:4:1"

case "$WHICH" in
  core) CELLS=$CORE ;; rest) CELLS=$REST ;; all) CELLS="$CORE $REST" ;;
  *) echo "usage: $0 core|rest|all"; exit 2 ;;
esac

mkdir -p "$OUT_ROOT"
for spec in $CELLS; do
  IFS=: read -r P R C <<< "$spec"
  for REP in $(seq 1 "$REPEATS"); do
    if [ "$P" = KEDA ]; then name="L1-keda-c$C-r$REP"; else name="$P-r$R-c$C-r$REP"; fi
    if grep -qs BENCH_SUMMARY "$OUT_ROOT/$name/driver.log"; then
      echo "skip $name (captured)"; continue
    fi
    if [ "$P" = KEDA ]; then
      KEDA=1 "$HERE/harness_bench_cell.sh" L1 "$R" "$C" "$REP" "$OUT_ROOT" < /dev/null \
        || echo "CELL FAILED: $name" | tee -a "$OUT_ROOT/sweep.log"
    else
      "$HERE/harness_bench_cell.sh" "$P" "$R" "$C" "$REP" "$OUT_ROOT" < /dev/null \
        || echo "CELL FAILED: $name" | tee -a "$OUT_ROOT/sweep.log"
    fi
  done
done
echo "sweep '$WHICH' finished: $OUT_ROOT"
