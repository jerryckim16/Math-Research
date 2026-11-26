#!/bin/bash
# Sweep: for each prime, one ladder count + NS level-one samples (seed 3), then the
# extended cascade (chain 3,3,2,2) on them.  Outputs results/sweep_mcmc_p<P>.txt and
# results/sweep_casc_p<P>.jsonl.  3 processes at a time.
# Usage: NS=600 NODECAP=500000000 bash run_sweep.sh P1 P2 ...
cd "$(dirname "$0")" || exit 1
NS=${NS:-600}
NODECAP=${NODECAP:-500000000}
cc -O3 -march=native -o mcmc1 mcmc1.c -lm
for p in "$@"; do echo "$p"; done |
  xargs -P 3 -I{} sh -c "nice -n 10 ./mcmc1 17 {} 3 10000 2000 $NS 20000 > results/sweep_mcmc_p{}.txt"
for p in "$@"; do
  grep '^M' "results/sweep_mcmc_p$p.txt" |
    python3 run_casc.py run "$p" 3,3,2,2 "$NS" "results/sweep_casc_p$p.jsonl" 3 200000 "$NODECAP"
done
