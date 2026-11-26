#!/bin/bash
# Classify the retained tuples at the last nonempty level of the bases that needed the
# most levels in the sweep (chain 3,3,2,2): dump that level with xcasc and run classify.py.
# Usage: bash run_classify.sh   -> results/classify_p<P>_L<L>.txt
cd "$(dirname "$0")" || exit 1
cc -O3 -march=native -o xcasc xcasc.c
job() {  # p, closing level C, penultimate level L, chain prefix up to L
  python3 -c "import json,sys,rio; [print(' '.join(map(str,r['base']))) for r in map(json.loads, rio.opn(sys.argv[1])) if r['empty_at']==int(sys.argv[2])]" \
    "results/sweep_casc_p$1.jsonl" "$2" |
    nice -n 10 ./xcasc 17 "$1" "$4" 1000000 "$3" | python3 classify.py 17 "$1" "$3" > "results/classify_p$1_L$3.txt"
}
export -f job
printf '%s\n' "97 18 9 3,3" "151 18 9 3,3" "149 18 9 3,3" "127 36 18 3,3,2" "131 36 18 3,3,2" \
  "157 9 3 3" "173 9 3 3" "199 9 3 3" "239 9 3 3" |
  xargs -P 3 -L 1 bash -c 'job $0 $1 $2 $3'
