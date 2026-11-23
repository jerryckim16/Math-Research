#!/bin/sh
# Batch re-check of LRC(14) gate certificates (see check_gate_full.py).
# Usage: run_lrc14_batch.sh DIR_WITH_ARCHIVES  "p[:sample] p[:sample] ..."
D=$1; shift
mkdir -p results/lrc14_gates
for spec in $1; do
  p=${spec%%:*}; s=""; [ "$spec" != "$p" ] && s=${spec#*:}
  out=results/lrc14_gates/gate_$p.json
  [ -s "$out" ] && continue
  python3 check_gate_full.py "$D/SHA256SUMS.txt" "$D/evidence_${p}_s0.tgz" 4 $s > "$out.tmp" 2> "results/lrc14_gates/gate_$p.err" && mv "$out.tmp" "$out"
done
