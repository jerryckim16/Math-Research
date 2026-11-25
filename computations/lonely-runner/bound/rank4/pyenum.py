"""Independent pure-Python complete enumeration for one rank-r profile (no
pruning, no symmetry), used to cross-check sect.c on small profiles.
Returns the list of admitted multiplicity vectors (in the given type order)
with (a, g)."""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from rank_exclusion import multiplicity_vectors, section, det  # noqa: E402
from relrank_n import delta_bounds  # noqa: E402
from crosscheck import rank  # noqa: E402


def admitted(types, prof, n, rej=2):
    D = delta_bounds(n)
    r = len(prof)
    out = []
    for mv in multiplicity_vectors(types, prof, n):
        present = [k for k in range(len(types)) if mv[k]]
        if rank([types[k] for k in present]) < r:
            continue
        lines = section(types, mv)
        if any(s <= rej for s in lines.values()):
            continue
        S = lambda d: sum(((d + s) / Fr(2 ** (s - 1))) * (1 if s % 2 else -1) for s in lines.values())
        if all(S(d) < d for d in D):
            continue
        odd = sorted((s, key) for key, s in lines.items() if s % 2)
        chosen, seq = [], []
        for s, key in odd:
            if rank(chosen + [key]) > len(chosen):
                chosen.append(key)
                seq.append(s)
        if tuple(seq) != tuple(prof):
            continue
        G = [[sum(mv[k] * types[k][i] * types[k][j] for k in present) for j in range(r)] for i in range(r)]
        idx = 0
        for J in combinations(present, r):
            idx = gcd(idx, abs(int(det([types[k] for k in J]))))
        out.append((tuple(mv), sum(mv), int(det(G) / idx ** 2)))
    return out
