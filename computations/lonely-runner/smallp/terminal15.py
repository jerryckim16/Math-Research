"""Independent re-derivation (our code only) of the terminal step of
Allikvere's k = 15 'weighted shift modulo 4' preliminary-prime certificates
("Sixteen lonely runners", Zenodo 10.5281/zenodo.23304361, Prop. 2.x
'Previously verified primes'; pilot records small_prime_pilot_20260910).

Input: his persistent level-one orbit representatives (read as DATA from
SUMMARY.json, key persistent_orbits.representatives).  For each rep r
(folded classes mod p) we compute, straight from Def. 2.1 (witness grid
(1/(lp))Z, threshold 1/16; gcd clause), with liftfree.c (repo code):
  F2 = level-2 lifts of r that are witness-free and fail the gcd clause (l=2)
  F4 = witness-free level-4 lifts of F2 (gcd clause re-applied at l=4)
  W4 = members of F4 closed by the weighted shift lemma with d = 4
       (sum over i with 4 !| u_i of g_i*ceil(4/(8 g_i)) < 4, >= 2 exceptions)
  R4 = F4 minus W4 (residual)
  R8 = witness-free level-8 lifts of R4 (no gcd/shift test; his "alltimes")
and also, our extension: R8x = members of R8 not closed by the gcd clause
or the shift lemma with d in {4, 8}.
Also checks every rep is in I(15,p,1) (no witness on (1/p)Z).
Prints totals to compare with his terminal_<p>.out line
"TOTAL bases l2 l4 weighted residual residual_l8_alltimes".
Usage: python3 terminal15.py SUMMARY.json [limit]
"""
import json
import os
import subprocess
import sys
import tempfile
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
K = 15


def liftfree_bin():
    out = os.path.join(tempfile.mkdtemp(prefix="lrc15_"), "liftfree")
    subprocess.run(["cc", "-O3", "-o", out, os.path.join(HERE, "..", "liftfree.c")], check=True)
    return out


LF = None


def wf_lifts(M, c, tuples):
    """witness-free lifts to level c*M (modulus c*M) of tuples mod M; list of lists."""
    if not tuples:
        return []
    inp = "\n".join(" ".join(map(str, t)) for t in tuples) + "\n"
    res = subprocess.run([LF, str(K), str(M), str(c)], input=inp, capture_output=True, text=True, check=True)
    out = [[] for _ in tuples]
    for line in res.stdout.splitlines():
        xs = list(map(int, line.split()))
        out[xs[0]].append(tuple(xs[1:]))
    return out


def gcd_clause(w, l):
    if l == 1:
        return False
    for i in range(len(w)):
        g = l
        for j, x in enumerate(w):
            if j != i:
                g = gcd(g, x)
        if g > 1:
            return True
    return False


def shift_ok(w, d, k=K):
    """Weighted shift lemma: >= 2 exceptions and sum g*ceil(2d/((k+1)g)) < d."""
    E = [x for x in w if x % d]
    if len(E) < 2:
        return False
    cost = 0
    for x in E:
        g = gcd(x, d)
        cost += g * (-(-2 * d // ((k + 1) * g)))
    return cost < d


def has_witness_level1(r, p):
    for m in range(1, p):
        if all((K + 1) * min((m * x) % p, p - (m * x) % p) >= p for x in r):
            return True
    return False


def main():
    S = json.load(open(sys.argv[1]))
    p = S["gate"]["p"]
    reps = [tuple(map(int, s.split())) for s in S["persistent_orbits"]["representatives"]]
    if len(sys.argv) > 2:
        reps = reps[:int(sys.argv[2])]
    global LF
    LF = liftfree_bin()
    bad1 = sum(1 for r in reps if has_witness_level1(r, p))
    tot = dict(bases=len(reps), level1_with_witness=bad1, l2=0, l4=0, weighted=0, residual=0,
               residual_l8_alltimes=0, residual_l8_ext=0, open_bases=0)
    B = 2000
    for s in range(0, len(reps), B):
        chunk = reps[s:s + B]
        f2 = wf_lifts(p, 2, chunk)
        f2 = [[w for w in ws if not gcd_clause(w, 2)] for ws in f2]
        flat2 = [(i, w) for i, ws in enumerate(f2) for w in ws]
        tot["l2"] += len(flat2)
        f4 = wf_lifts(2 * p, 2, [w for _, w in flat2])
        rows4 = []
        for (i, _), ws in zip(flat2, f4):
            for w in ws:
                if not gcd_clause(w, 4):
                    rows4.append((i, w))
        tot["l4"] += len(rows4)
        res = [(i, w) for i, w in rows4 if not shift_ok(w, 4)]
        tot["weighted"] += len(rows4) - len(res)
        tot["residual"] += len(res)
        f8 = wf_lifts(4 * p, 2, [w for _, w in res])
        openb = set()
        for (i, _), ws in zip(res, f8):
            tot["residual_l8_alltimes"] += len(ws)
            for w in ws:
                if not (gcd_clause(w, 8) or shift_ok(w, 4) or shift_ok(w, 8)):
                    tot["residual_l8_ext"] += 1
            if ws:
                openb.add(i + s)
        tot["open_bases"] += len(openb)
        print(json.dumps({"done": s + len(chunk), **tot}), flush=True)
    print(json.dumps({"p": p, "FINAL": tot}))


if __name__ == "__main__":
    main()
