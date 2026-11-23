"""Binary cascade of the tight 15-speed tuple (1,...,15) at every prime in a
range (default: the 79 candidate gate primes 251..743 for LRC(15)).

For each p: lift (1..15) mod p by 2 to levels 2, 4, 8, 16 (32 if needed),
keeping the (15,p,l)-improper lifts (witness-free on the (1/lp)Z grid, gcd
clause failed), computed with liftfree.c.  Reports the counts per level.
Only this one orbit is examined: this is NOT a gate check (other level-one
orbits are not generated here).
Usage: python3 tight_orbit_k15.py [pmin pmax]
"""
import json
import sys
import check_allikvere as ca

k = 15
pmin, pmax = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (251, 743)
for p in range(pmin, pmax + 1):
    if p < 2 or any(p % q == 0 for q in range(2, int(p ** 0.5) + 1)):
        continue
    cur, l, tr = [tuple(range(1, k + 1))], 1, []
    while cur and l < 32:
        wf = ca.witness_free_lifts(k, l * p, 2, cur)
        l *= 2
        cur = sorted({w for ws in wf.values() for w in ws if not ca.gcd_clause(w, l)})
        tr.append((l, len(cur)))
    print(json.dumps({"p": p, "trace": tr, "dies_by": tr[-1][0] if not cur else None}), flush=True)
