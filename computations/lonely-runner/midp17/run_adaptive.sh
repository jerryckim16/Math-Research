#!/bin/bash
# Two-stage per-base strategy on the sweep samples: first the chain "2" (level 2 only);
# bases whose level-2 retained set is nonempty are rerun from level one with 3,3,2,2.
# (The level at which a base closes may differ from base to base; see the note, section 2.)
# Usage: bash run_adaptive.sh P1 P2 ...   (needs results/sweep_mcmc_p<P>.txt; mcmc via run_sweep.sh)
# Outputs results/ad2_p<P>.jsonl and results/ad3322_p<P>.jsonl.
cd "$(dirname "$0")" || exit 1
NS=${NS:-600}
for p in "$@"; do
  grep '^M' "results/sweep_mcmc_p$p.txt" |
    python3 run_casc.py run "$p" 2 "$NS" "results/ad2_p$p.jsonl" 3 200000 500000000
  python3 -c "import json,sys; [print(' '.join(map(str,r['base']))) for r in map(json.loads, open(sys.argv[1])) if not r['empty_at']]" "results/ad2_p$p.jsonl" |
    python3 run_casc.py run "$p" 3,3,2,2 "$NS" "results/ad3322_p$p.jsonl" 3 200000 500000000
done
