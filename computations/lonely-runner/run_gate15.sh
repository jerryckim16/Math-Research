#!/bin/bash
# Level-one completeness at one k = 15 gate of Allikvere's "Sixteen lonely runners"
# (Zenodo 10.5281/zenodo.23304361), step 17.  Usage:  run_gate15.sh p
#   WORK    scratch directory (default ./work15): archives in $WORK/z16, results in $WORK/c15/p<p>
#   BINDIR  directory with covergen builds covergenW<n> made with -DWFIX=<n> (default $WORK)
# The archive's SHA-256 must equal the record's SHA256SUMS.txt entry (CRLF stripped).
# Generation: covergen.c with LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1,
# 32 depth-2 shards, 4 at a time.  RESUMABLE: a shard listed in times.txt is finished and is
# skipped; any other shard is rerun from scratch ("> out<i>.txt" truncates).  A shard is
# recorded as finished only if covergen exits 0, and before the comparison every shard's
# cover-file line count must equal minimal_covers in its log (the run aborts otherwise).
# Comparison: completeness_check.py with LRC_COMPARE_FILES=1 (disk-based); cover files are
# deleted afterwards.
set -u
p=$1
WORK=${WORK:-$PWD/work15}; BINDIR=${BINDIR:-$WORK}
HERE=$(cd "$(dirname "$0")" && pwd)
h=$(( (p-1)/2 )); w=$(( (h+1+63)/64 )); B=$BINDIR/covergenW$w
A=$WORK/z16/evidence15_${p}_s0.tgz
mkdir -p "$WORK/z16"
[ -f "$A" ] || curl -sSL -o "$A" "https://zenodo.org/api/records/23304361/files/evidence15_${p}_s0.tgz/content"
[ -f "$WORK/z16/SHA256SUMS.txt" ] || curl -sSL -o "$WORK/z16/SHA256SUMS.txt" "https://zenodo.org/api/records/23304361/files/SHA256SUMS.txt/content"
want=$(tr -d "\r" < "$WORK/z16/SHA256SUMS.txt" | grep "  evidence15_${p}_s0.tgz$" | cut -c1-64); got=$(sha256sum "$A" | cut -c1-64)
D=$WORK/c15/p$p; mkdir -p "$D"; cd "$D"
echo "$want $got" > sha.txt
[ -n "$want" ] && [ "$want" = "$got" ] || { echo SHA_MISMATCH > done; exit 1; }
[ -f start ] || date -u +%s > start
touch times.txt
seq 0 31 | xargs -P4 -I{} sh -c "grep -q \"^{} \" times.txt && exit 0; s=\$(date +%s); LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1 LRC_SHARD_DEPTH=2 LRC_NSHARDS=32 LRC_SHARD={} $B 15 $p > out{}.txt 2> err{}.txt && echo {} \$((\$(date +%s)-s)) >> times.txt"
date -u +%s > gen_done
# Every shard must be finished and complete before the comparison: listed in times.txt
# (written only if covergen exits 0, via &&), and its cover count equal to minimal_covers
# in its log.  Any failure aborts the gate (done = SHARD_CHECK_FAILED, details in check.err).
bad=0
for i in $(seq 0 31); do
  grep -q "^$i " times.txt || { echo "shard $i not finished" >> check.err; bad=1; continue; }
  n=$(wc -l < out$i.txt); m=$(grep -o "minimal_covers [0-9]*" err$i.txt | tail -1 | awk '{print $2}')
  [ "$n" = "$m" ] || { echo "shard $i: $n lines vs minimal_covers $m" >> check.err; bad=1; }
done
[ $bad = 0 ] || { echo SHARD_CHECK_FAILED > done; exit 1; }
echo "all 32 shards: line count = minimal_covers" > shard_check.txt
cat $(for i in $(seq 0 31); do echo out$i.txt; done) > all.txt
LRC_COMPARE_FILES=1 python3 "$HERE/completeness_check.py" "$A" "$D/all.txt" > "$D/compl.json" 2> "$D/compl.err"
rm -f "$D/all.txt" "$D"/out*.txt
date -u +%s > "$D/done"
