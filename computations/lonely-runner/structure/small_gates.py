"""Binary cascade for LRC(k) at small primes k+2 <= p <= 2k+1 (k = 15 by default).

Lemma S (proved in notes/lonely-runner/structure.md): for a prime p with
k+2 <= p <= 2k+2, a tuple v in (Z_p^*)^k is (k,p,1)-improper iff the folded
classes {+-v_i} cover all (p-1)/2 classes.  So level one is enumerated directly:
all multisets of size k on the classes 1..(p-1)/2 that contain every class.

Cascade: at each level l = 1, 2, 4, ..., lift every unit-orbit representative by 2
(liftfree.c, witness test on the (1/(2lp))Z grid), drop lifts proper by the gcd
clause at level 2l, reduce the survivors to unit orbits of Z_{2lp} (permutation,
sign and unit invariance, F2), repeat.  If some level is empty, J(k,p) is empty
(F1 + Lemma E), so by Lemma D (needs LRC(k-1)) p divides v_1...v_k for every
counterexample v.
Usage: python3 small_gates.py [k] p [p ...]
"""
import itertools
import json
import os
import subprocess
import sys
import tempfile
import time
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
LR = os.path.dirname(HERE)
_BIN = None


def liftfree_bin():
    global _BIN
    if _BIN is None:
        _BIN = os.path.join(tempfile.mkdtemp(prefix="lrs_"), "liftfree")
        subprocess.run(["cc", "-O3", "-o", _BIN, os.path.join(LR, "liftfree.c")], check=True)
    return _BIN


def units(N):
    return [u for u in range(1, N) if gcd(u, N) == 1]


def canon(w, N, U):
    best = None
    for u in U:
        t = tuple(sorted(min((u * x) % N, N - (u * x) % N) for x in w))
        if best is None or t < best:
            best = t
    return best


def gcd_clause(w, l):
    if l == 1:
        return False
    for i in range(len(w)):
        g = l
        for j, x in enumerate(w):
            if j != i:
                g = gcd(g, x)
                if g == 1:
                    break
        if g > 1:
            return True
    return False


def has_witness(w, N, k):
    for m in range(1, N):
        if all((k + 1) * min((m * x) % N, N - (m * x) % N) >= N for x in w):
            return True
    return False


def level_one(k, p):
    n = (p - 1) // 2
    assert k + 2 <= p <= 2 * k + 2 and k >= n
    U = units(p)
    reps = set()
    for extra in itertools.combinations_with_replacement(range(1, n + 1), k - n):
        reps.add(canon(tuple(range(1, n + 1)) + extra, p, U))
    return sorted(reps)


def lift_by_2(k, M, reps):
    """Witness-free lifts to modulus 2M, streamed: yields lift tuples."""
    inp = "\n".join(" ".join(map(str, t)) for t in reps) + "\n"
    proc = subprocess.Popen([liftfree_bin(), str(k), str(M), "2"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(inp)
    for line in out.splitlines():
        yield tuple(map(int, line.split()[1:]))


def run(k, p, lmax=64, check_level1=True):
    t0 = time.time()
    reps = level_one(k, p)
    rec = {"k": k, "p": p, "level1_orbits": len(reps)}
    if check_level1:   # every listed row really is witness-free at level 1
        rec["level1_rows_improper"] = all(not has_witness(r, p, k) for r in reps)
    trace, l = [], 1
    while reps and l < lmax:
        M = l * p
        l *= 2
        N = l * p
        U = units(N)
        nxt, nwf, ngcd = set(), 0, 0
        for w in lift_by_2(k, M, reps):
            nwf += 1
            if gcd_clause(w, l):
                ngcd += 1
                continue
            nxt.add(canon(w, N, U))
        reps = sorted(nxt)
        trace.append({"level": l, "witness_free_lifts": nwf, "gcd_proper": ngcd,
                      "improper_orbits": len(reps)})
        print(json.dumps({"p": p, **trace[-1]}), file=sys.stderr, flush=True)
    rec["trace"] = trace
    rec["J_empty_by"] = trace[-1]["level"] if not reps else None
    rec["survivors_head"] = reps[:5]
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


if __name__ == "__main__":
    args = list(map(int, sys.argv[1:]))
    k = args[0] if len(args) > 1 and args[0] < args[1] and args[0] <= 30 and args[0] < 17 else 15
    ps = args[1:] if k == args[0] and len(args) > 1 else args
    for p in ps:
        print(json.dumps(run(k, p)), flush=True)
