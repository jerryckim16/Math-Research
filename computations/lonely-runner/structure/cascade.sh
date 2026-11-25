#!/bin/bash
# cascade.sh k p maxlevel outdir : binary cascade of the Lemma S level-one family
# (small_gates.level_one) using liftfree.c (witness-free lifts) + orbit_filter.c
# (gcd clause, unit-orbit canonical form; CASCADE_NG=1 adds Lemma NG) + sort -u.  Writes outdir/L<l>.txt per
# level and prints one JSON line per level.  Binaries are built in outdir.
set -euo pipefail
k=$1; p=$2; maxl=$3; out=$4
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
cc -O3 -o "$out/liftfree" "$here/../liftfree.c"
cc -O3 -o "$out/orbit_filter" "$here/orbit_filter.c"
python3 -c "import sys; sys.path.insert(0,'$here'); import small_gates as s
for r in s.level_one($k,$p): print(*r)" > "$out/L1.txt"
echo "{\"k\": $k, \"p\": $p, \"level\": 1, \"orbits\": $(wc -l < "$out/L1.txt")}"
l=1
while [ "$l" -lt "$maxl" ] && [ -s "$out/L$l.txt" ]; do
  M=$((l*p)); l2=$((2*l)); t0=$(date +%s)
  "$out/liftfree" "$k" "$M" 2 < "$out/L$l.txt" 2> "$out/lf$l2.err" \
    | "$out/orbit_filter" "$k" "$p" "$l2" idx ${CASCADE_NG:+ng} 2> "$out/of$l2.err" \
    | LC_ALL=C sort -u -S 2G -T "$out" > "$out/L$l2.txt"
  wf=$(grep -o 'witness_free [0-9]*' "$out/lf$l2.err" | awk '{print $2}')
  g=$(grep -o 'gcd_proper [0-9]*' "$out/of$l2.err" | awk '{print $2}')
  ngs=$(grep -o 'ng_settled [0-9]*' "$out/of$l2.err" | awk '{print $2}')
  echo "{\"k\": $k, \"p\": $p, \"level\": $l2, \"witness_free_lifts\": $wf, \"gcd_proper\": $g, \"ng_settled\": ${ngs:-0}, \"orbits\": $(wc -l < "$out/L$l2.txt"), \"seconds\": $(( $(date +%s) - t0 ))}"
  l=$l2
done
