import sys
from fractions import Fraction
from math import gcd
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



def badset(m, t, H):
    K = m + 1
    a, q = t.numerator, t.denominator
    return frozenset(x for x in range(1, H + 1) if K * min(x * a % q, q - x * a % q) < q)


def fam(m, extra_k=(2,), Q=None):
    H = 2 * m
    Q = Q or 2 * m + 2
    F = set()
    for q in range(2, Q + 1):
        for a in range(1, q // 2 + 1):
            if gcd(a, q) == 1:
                F.add(badset(m, Fraction(a, q), H))
    for k in extra_k:
        for j in range(1, m + 1):
            for d in range(j):
                if gcd(d, j) == 1 or j == 1:
                    F.add(badset(m, Fraction(d, j) + Fraction(1, k * j * (m + 1)), H))
    F = sorted(F, key=len)
    return [B for B in F if not any(C < B for C in F)]


if __name__ == "__main__":
    for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        N = 2 * m + 1
        if all(N % d for d in range(2, int(N ** .5) + 1)):
            continue
        F = fam(m)
        # transversals of size <= m (start from empty set: use M=... hack)
        out = []

        def dfs(T, forb):
            if out:
                return
            best = None
            for B in F:
                if B & T:
                    continue
                av = B - forb
                if best is None or len(av) < len(best):
                    best = av
            if best is None:
                out.append(sorted(T)); return
            if len(T) == m:
                return
            f = set(forb)
            for x in sorted(best):
                dfs(T | {x}, frozenset(f)); f.add(x)
        dfs(frozenset(), frozenset())
        print(m, N, "transversal:" if out else "NONE (family suffices)", out[:1], flush=True)
