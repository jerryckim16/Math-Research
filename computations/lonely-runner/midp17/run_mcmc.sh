#!/bin/bash
# Ladder count + 2000 uniform level-one samples per prime, two seeds; 3 jobs at a time.
# Usage: bash run_mcmc.sh P1 P2 ...   (outputs results/mcmc_p<P>_s<seed>.txt)
cd "$(dirname "$0")" || exit 1
cc -O3 -march=native -o mcmc1 mcmc1.c -lm
for p in "$@"; do for s in 1 2; do echo "$p $s"; done; done |
  xargs -P 3 -L 1 sh -c 'nice -n 10 ./mcmc1 17 $0 $1 20000 2000 2000 20000 > results/mcmc_p$0_s$1.txt'
