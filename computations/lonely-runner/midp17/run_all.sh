#!/bin/bash
# Extended cascade (chain 2,3,3,2) on the 4000 MCMC level-one samples of each prime.
# Usage: bash run_all.sh P1 P2 ...   -> results/casc_p<P>.jsonl  (3 xcasc processes)
cd "$(dirname "$0")" || exit 1
for p in "$@"; do
  cat results/mcmc_p${p}_s1.txt results/mcmc_p${p}_s2.txt |
    python3 run_casc.py run "$p" 2,3,3,2 4000 results/casc_p$p.jsonl 3 200000 4000000000
done
