#!/bin/bash
# Chain comparison on 120 heavy p = 151 bases (those that needed level 18 with 2,3,3,2).
# Output: results/chain151_<chain>.jsonl
cd "$(dirname "$0")" || exit 1
for ch in 2,3,3 3,2,3 3,3,2; do
  python3 run_casc.py run 151 $ch 120 results/chain151_$ch.jsonl 3 400000 8000000000 < results/heavy151.txt
done
