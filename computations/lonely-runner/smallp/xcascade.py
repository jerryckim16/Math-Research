"""General-k extended cascade (our code; liftfree.c from the repo).

Retained set F'_l(r): lifts of F'_{l/c}(r) by c that are witness-free on
(1/(lp))Z (liftfree.c), fail the gcd clause at level l, and are not closed
by the weighted shift lemma (Lemma S, notes/lonely-runner/small-primes.md)
for any divisor d >= 2 of l (if XSHIFT) -- 'extended properness', inherited
by lifts, so F'_L(r) empty gives Lemma 2.2(ii) at level L (arXiv:2609.02604v2).
With XSHIFT off this is the plain cascade of Def. 2.1 / Lemma E.
Usage: python3 xcascade.py k p CHAIN [noshift] < bases   (CHAIN e.g. 2,3,3,2)
       python3 xcascade.py k tight PMIN PMAX CHAIN [noshift]
         (the tight tuple (1..k) at every prime in [PMIN, PMAX])
"""
import json
import os
import subprocess
import sys
import tempfile
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
_LF = None


def lf():
    global _LF
    if _LF is None:
        _LF = os.path.join(tempfile.mkdtemp(prefix="xc_"), "liftfree")
        subprocess.run(["cc", "-O3", "-o", _LF, os.path.join(HERE, "..", "liftfree.c")], check=True)
    return _LF


def wf_lifts(k, M, c, tuples):
    if not tuples:
        return []
    inp = "\n".join(" ".join(map(str, t)) for t in tuples) + "\n"
    res = subprocess.run([lf(), str(k), str(M), str(c)], input=inp, capture_output=True, text=True, check=True)
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


def shift_ok(w, d, k):
    E = [x for x in w if x % d]
    if len(E) < 2:
        return False
    return sum(gcd(x, d) * (-(-2 * d // ((k + 1) * gcd(x, d)))) for x in E) < d


def divisors(l):
    return [d for d in range(2, l + 1) if l % d == 0]


def cascade(k, p, base, chain, xshift=True, cap=200000):
    cur, l, tr = [tuple(base)], 1, []
    for c in chain:
        ws = wf_lifts(k, l * p, c, cur)
        l *= c
        ds = divisors(l) if xshift else []
        nxt = set()
        for lst in ws:
            for w in lst:
                if gcd_clause(w, l) or any(shift_ok(w, d, k) for d in ds):
                    continue
                nxt.add(w)
        cur = sorted(nxt)
        tr.append((l, len(cur)))
        if not cur or len(cur) > cap:
            break
    return tr, (tr[-1][0] if not cur else None)


def isprime(n):
    return n > 1 and all(n % q for q in range(2, int(n ** .5) + 1))


if __name__ == "__main__":
    k = int(sys.argv[1])
    if sys.argv[2] == "tight":
        pmin, pmax = int(sys.argv[3]), int(sys.argv[4])
        chain = [int(x) for x in sys.argv[5].split(",")]
        xs = len(sys.argv) <= 6 or sys.argv[6] != "noshift"
        for p in range(pmin, pmax + 1):
            if isprime(p) and p > k + 1:
                tr, dead = cascade(k, p, range(1, k + 1), chain, xs)
                print(json.dumps({"k": k, "p": p, "xshift": xs, "trace": tr, "empty_at": dead}), flush=True)
    else:
        p = int(sys.argv[2])
        chain = [int(x) for x in sys.argv[3].split(",")]
        xs = len(sys.argv) <= 4 or sys.argv[4] != "noshift"
        for line in sys.stdin:
            if line.strip():
                b = [int(x) for x in line.split()]
                tr, dead = cascade(k, p, b, chain, xs)
                print(json.dumps({"k": k, "p": p, "base": b, "xshift": xs, "trace": tr, "empty_at": dead}), flush=True)
