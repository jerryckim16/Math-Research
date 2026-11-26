#!/bin/sh
# Reproduce the exhaustive window computations of notes/lonely-runner/general-n.md.
# Usage: sh run_windows.sh BUILD_DIR
#   writes results/window_147_100.txt (every n-set in [1, floor(147n/100)], n <= 84)
#   and    results/window_29_20.txt  (every n-set in [1, floor(29n/20)], n <= 80)
#   and    results/window_19_10.txt  (every n-set in [1, floor(19n/10)], n <= 67)
# The full dense window [1,2m] (m <= 47) is reproduced by
#   for m in $(seq 2 47); do $B/dwsolve $m $((4*m)); done
set -e
B=${1:-/tmp/dwbuild}
mkdir -p "$B"
here=$(dirname "$0")
gcc -O2 -Wall -o "$B/dwsolve" "$here/dwsolve.c"
mkdir -p "$here/results"
: > "$here/results/window_147_100.txt"
for n in $(seq 1 84); do
  "$B/dwsolve" "$n" $((3 * n + 2)) top=$((147 * n / 100 > 0 ? 147 * n / 100 : 1)) | tail -1 >> "$here/results/window_147_100.txt"
done
: > "$here/results/window_29_20.txt"
for n in $(seq 1 80); do
  "$B/dwsolve" "$n" $((3 * n + 2)) top=$((29 * n / 20 > 0 ? 29 * n / 20 : 1)) | tail -1 >> "$here/results/window_29_20.txt"
done
: > "$here/results/window_19_10.txt"
for n in $(seq 1 67); do
  "$B/dwsolve" "$n" $((3 * n + 2)) top=$((19 * n / 10)) | tail -1 >> "$here/results/window_19_10.txt"
done
grep -c DW_HOLDS "$here/results/window_147_100.txt" "$here/results/window_29_20.txt" "$here/results/window_19_10.txt"
