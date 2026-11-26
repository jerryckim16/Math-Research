#!/bin/bash
# Independent re-check of xcasc.c on sampled bases with k17struct/cascade_verify.c (different code:
# full unit-orbit canonical forms, reverse coordinate order, its own gcd and shift-lemma tests).
# For each base: levels 3, 9, 18 along 3,3,2 with cascade_verify | sort -u, and xcasc on the same
# base; prints both orbit-count traces.  Usage: bash crosscheck_cv.sh P < bases  (k = 17)
cd "$(dirname "$0")" || exit 1
P=$1
cc -O3 -march=native -o /tmp/cv_midp17 ../k17struct/cascade_verify.c
cc -O3 -march=native -o xcasc xcasc.c
while read -r line; do
  [ -z "$line" ] && continue
  l3=$(echo "$line" | /tmp/cv_midp17 17 "$P" 1 3 ng 2>/dev/null | LC_ALL=C sort -u)
  n3=$(printf '%s' "$l3" | grep -c .)
  l9=$(printf '%s\n' "$l3" | grep . | /tmp/cv_midp17 17 "$P" 3 3 ng 2>/dev/null | LC_ALL=C sort -u)
  n9=$(printf '%s' "$l9" | grep -c .)
  n18=$(printf '%s\n' "$l9" | grep . | /tmp/cv_midp17 17 "$P" 9 2 ng 2>/dev/null | LC_ALL=C sort -u | grep -c .)
  xc=$(echo "$line" | ./xcasc 17 "$P" 3,3,2 | python3 -c "import json,sys; r=json.loads(sys.stdin.read()); print(' '.join(str(t[1]) for t in r['trace']))")
  echo "base [$line] cascade_verify: $n3 $n9 $n18 | xcasc: $xc"
done
