#!/bin/sh
# Rebuild and rerun the exhaustive check for n <= 6 (n = 6 takes ~3 min on 4 cores).
set -e
cd "$(dirname "$0")"
gcc -O2 -o frankl_enum frankl_enum.c
for n in 1 2 3 4 5; do ./frankl_enum $n; done
for p in 0 1 2 3; do ./frankl_enum 6 $p 4 > /tmp/frankl_n6_$p.out & done
wait
cat /tmp/frankl_n6_*.out
python3 -c "
import re,glob
t={}
for f in glob.glob('/tmp/frankl_n6_*.out'):
    for k,v in re.findall(r'(\w+)=(\d+)', open(f).read()):
        if k in ('labeled_total','labeled_fulluniverse','tight','counterexamples','leaves'): t[k]=t.get(k,0)+int(v)
print('n=6 totals', t)
assert t['labeled_total']==75973751474 and t['labeled_fulluniverse']==75965474236 and t['counterexamples']==0
print('OK: matches Brinkmann-Deklerck counts; no counterexample')
"
