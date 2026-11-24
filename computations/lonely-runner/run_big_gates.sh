#!/bin/sh
# Download -> stream-check -> delete, one archive at a time (step 5).
# Usage: run_big_gates.sh DIR SAMPLE JOBS "p p p ..."
D=$1; S=$2; J=$3; shift 3
mkdir -p results/lrc14_gates
for p in $1; do
  out=results/lrc14_gates/gate_${p}_stream.json
  [ -s "$out" ] && continue
  f=evidence_${p}_s0.tgz
  downloaded=0
  if [ ! -s "$D/$f" ]; then
    free=$(df --output=avail -BG / | tail -1 | tr -dc 0-9)
    [ "$free" -lt 12 ] && { echo "low disk ($free G), stop" >&2; exit 1; }
    curl -sS -m 3600 -L -o "$D/$f.part" "https://zenodo.org/records/22667683/files/$f?download=1" && mv "$D/$f.part" "$D/$f" || { echo "download failed $p" >&2; continue; }
    downloaded=1
  fi
  python3 check_gate_stream.py "$D/SHA256SUMS.txt" "$D/$f" "$S" "$J" > "$out.tmp" 2> "results/lrc14_gates/gate_${p}_stream.err" && mv "$out.tmp" "$out"
  [ $downloaded = 1 ] && rm -f "$D/$f"
done
