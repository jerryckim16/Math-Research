#!/bin/bash
# Larger closure samples: N fresh level-one samples (seed 4; short ladder) per prime, then the
# two-stage strategy (chain 2, then 3,3,2,2 on the bases still open).
# Usage: N=10000 bash run_big.sh P1 P2 ...  -> results/big_mcmc_p<P>.txt, results/big2_p<P>.jsonl,
#        results/big3322_p<P>.jsonl
cd "$(dirname "$0")" || exit 1
N=${N:-10000}
JOBS=${JOBS:-3}
cc -O3 -march=native -o mcmc1 mcmc1.c -lm
for p in "$@"; do echo "$p"; done |
  xargs -P "$JOBS" -I{} sh -c "nice -n 10 ./mcmc1 17 {} 4 2000 2000 $N 20000 > results/big_mcmc_p{}.txt"
for p in "$@"; do
  grep '^M' "results/big_mcmc_p$p.txt" |
    python3 run_casc.py run "$p" 2 "$N" "results/big2_p$p.jsonl" "$JOBS" 200000 500000000
  python3 -c "import json,sys; [print(' '.join(map(str,r['base']))) for r in map(json.loads, open(sys.argv[1])) if not r['empty_at']]" "results/big2_p$p.jsonl" |
    python3 run_casc.py run "$p" 3,3,2,2 "$N" "results/big3322_p$p.jsonl" "$JOBS" 200000 500000000
done
