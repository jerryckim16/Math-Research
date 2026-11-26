#!/bin/bash
# Full LRC(17) gate run at a mid-range prime (default p = 251), one shard at a time:
#   covergen (orderly, depth-D shards) | expand | xcascq x2 | xcascq 3,3,2,2
# plus the 1% batch re-check with k17struct/cascade_verify.c.  Nothing but
# counts, histograms, the open bases (should be none) and the bases closing at
# level >= 9 is kept.  A shard counts as finished (listed in times.txt) only
# if every stage exits 0 and every count check passes (gate251/shard_check.py).
#
# Usage:  [LO=a HI=b] [NSH=1024] [DEPTH=6] [JOBS=4] run_gate251.sh WORKDIR [P]
#   With LO/HI: run shards LO..HI only (one harness-tracked task per range, each < 2 h).
#   WORKDIR holds the binaries (built here) and the per-shard outputs.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
LR=$(dirname "$HERE")
WORK=$1; P=${2:-251}; K=${K:-17}
NSH=${NSH:-1024}; DEPTH=${DEPTH:-6}; JOBS=${JOBS:-4}
mkdir -p "$WORK/bin" "$WORK/p$P"
H=$(( (P - 1) / 2 )); WF=$(( (H + 1 + 63) / 64 ))
B=$WORK/bin
[ -x "$B/cg$WF" ] || gcc -O2 -march=native -DWFIX=$WF -o "$B/cg$WF" "$LR/covergen.c" -lm || exit 1
[ -x "$B/expand" ] || gcc -O2 -o "$B/expand" "$HERE/expand.c" || exit 1
[ -x "$B/xcascq" ] || gcc -O2 -o "$B/xcascq" "$HERE/xcascq.c" || exit 1
[ -x "$B/cv" ] || gcc -O3 -march=native -o "$B/cv" "$LR/k17struct/cascade_verify.c" || exit 1
D=$WORK/p$P; cd "$D" || exit 1
if [ -f nshards.txt ] && [ "$(cat nshards.txt)" != "$NSH $DEPTH" ]; then echo "NSHARDS_CHANGED" > done; exit 1; fi
echo "$NSH $DEPTH" > nshards.txt
touch times.txt
[ -f start ] || date -u +%s > start
export B K P NSH DEPTH HERE WF D
run_shard() {
  i=$1
  grep -q "^$i " times.txt && return 0
  s=$(date +%s)
  rm -f "log$i.json" "open1_$i.txt" "smp$i.txt"
  ( set -o pipefail
    LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1 LRC_SHARD_DEPTH=$DEPTH LRC_NSHARDS=$NSH LRC_SHARD=$i \
      "$B/cg$WF" $K $P 2> "cg$i.err" \
    | EX_SAMPLE="smp$i.txt" EX_EVERY=100 "$B/expand" $K $P 2> "ex$i.err" \
    | XC_QUIET=1 "$B/xcascq" $K $P 2 2> "x1_$i.err" \
    | tee "open1_$i.txt" \
    | XC_QUIET=1 XC_LOG="log$i.json" XC_LOGMIN=9 "$B/xcascq" $K $P 3,3,2,2 > "open2_$i.txt" 2> "x2_$i.err" ) || { echo "$i pipeline_failed" >> failed.txt; return 1; }
  # 1% re-check with cascade_verify: sampled bases closed at level 2 must have no level-2 survivor (batch).
  LC_ALL=C sort -u "open1_$i.txt" > "o1s_$i.txt"
  LC_ALL=C sort -u "smp$i.txt" > "smps_$i.txt"
  LC_ALL=C comm -23 "smps_$i.txt" "o1s_$i.txt" | "$B/cv" $K $P 1 2 ng 2> "cv2_$i.err" | wc -l > "cv2_$i.n" || return 1
  # sampled bases still open after x2, and every base closing at level >= 9 (logged by stage 2):
  # per-base chain 3,3,2,2 with cascade_verify; the closing level must equal xcascq's.
  { LC_ALL=C comm -12 "smps_$i.txt" "o1s_$i.txt"
    [ -f "log$i.json" ] && python3 -I -c "import json,sys; [print(' '.join(map(str, json.loads(l)['base']))) for l in open(sys.argv[1])]" "log$i.json"
  } | LC_ALL=C sort -u > "vb_$i.txt"
  python3 -I "$HERE/verify_bases.py" "$B" $K $P < "vb_$i.txt" > "vb_$i.json" || { echo "$i verify_failed" >> failed.txt; return 1; }
  python3 -I "$HERE/shard_check.py" "$D" "$i" $(( $(date +%s) - s )) || { echo "$i check_failed" >> failed.txt; return 1; }
  rm -f "open1_$i.txt" "o1s_$i.txt" "smp$i.txt" "smps_$i.txt"
  echo "$i $(( $(date +%s) - s ))" >> times.txt
}
export -f run_shard
seq "${LO:-0}" "${HI:-$((NSH-1))}" | xargs -P "$JOBS" -I{} bash -c 'run_shard {}'
if [ -n "${LO:-}" ] || [ -n "${HI:-}" ]; then echo "RANGE ${LO:-0}-${HI:-end} done: $(wc -l < times.txt) of $NSH shards finished"; exit 0; fi
for i in $(seq 0 $((NSH-1))); do grep -q "^$i " times.txt || { echo "PARTIAL: shard $i not finished"; exit 0; }; done
date -u +%s > gen_done
echo ALL_SHARDS_DONE
