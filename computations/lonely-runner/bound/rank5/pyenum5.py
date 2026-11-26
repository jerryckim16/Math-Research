"""Independent pure-Python complete enumeration for one rank-5 profile with
support cap AMAX (no pruning, no symmetry), for cross-checking sectj.c run
with NOSYM=1 and the same AMAX.  Shares no code with the C enumerators: the
domain is rank_exclusion.multiplicity_vectors (cap = AMAX columns), the
section is solved with exact Fractions from the first invertible set of
present types, and every test is re-implemented.

usage: python3 pyenum5.py n AMAX s1 s2 s3 s4 s5 TYPES_FILE
       (TYPES_FILE: any sectj output, for the type order)
Prints one line "a g m" per admitted vector, sorted.
"""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations, product
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND = os.path.dirname(HERE)
sys.path.insert(0, BOUND)
sys.path.insert(0, os.path.join(BOUND, "rank4"))
from rank_exclusion import multiplicity_vectors, det  # noqa: E402
from relrank_n import delta_bounds  # noqa: E402
from crosscheck import rank  # noqa: E402
from classes import parse  # noqa: E402


def inverse(A):
    n = len(A)
    M = [list(map(Fr, A[i])) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]


def admitted(types, prof, n, amax, rej=2):
    D = delta_bounds(n)
    r = len(prof)
    xs = [x for x in product((-1, 0, 1), repeat=r) if any(x) and next(v for v in x if v) > 0]
    out = []
    for mv in multiplicity_vectors(types, prof, amax):
        present = [k for k in range(len(types)) if mv[k]]
        if len(present) < r or rank([types[k] for k in present]) < r:
            continue
        basis = next(J for J in combinations(present, r) if det([types[k] for k in J]) != 0)
        Minv = inverse([types[k] for k in basis])
        lines = []
        for x in xs:
            lam = [sum(Minv[i][j] * x[j] for j in range(r)) for i in range(r)]
            vals = [sum(l * t for l, t in zip(lam, types[k])) for k in present]
            if all(v in (-1, 0, 1) for v in vals):
                sup = sum(mv[k] for k, v in zip(present, vals) if v != 0)
                lines.append((sup, tuple(vals)))
        if any(s <= rej for s, _ in lines):
            continue
        S = lambda d: sum(((d + s) / Fr(2 ** (s - 1))) * (1 if s % 2 else -1) for s, _ in lines)
        if all(S(d) < d for d in D):
            continue
        chosen, seq = [], []
        for s, key in sorted(l for l in lines if l[0] % 2):
            if rank(chosen + [key]) > len(chosen):
                chosen.append(key)
                seq.append(s)
        if tuple(seq) != tuple(prof):
            continue
        G = [[sum(mv[k] * types[k][i] * types[k][j] for k in present) for j in range(r)] for i in range(r)]
        idx = 0
        for J in combinations(present, r):
            idx = gcd(idx, abs(int(det([types[k] for k in J]))))
        out.append((sum(mv), int(det(G) / idx ** 2), tuple(mv)))
    return out


if __name__ == "__main__":
    n, amax = int(sys.argv[1]), int(sys.argv[2])
    prof = tuple(int(x) for x in sys.argv[3:8])
    types, _, _ = parse(sys.argv[8])
    for a, g, mv in sorted(admitted(types, prof, n, amax)):
        print(a, g, ",".join(map(str, mv)))
