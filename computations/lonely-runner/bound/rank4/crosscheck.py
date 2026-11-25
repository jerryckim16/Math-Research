"""Independent re-check (pure Python, exact Fractions) of admitted sections
written by sect.c.  It shares no code with sect.c: the section is rebuilt by
Cramer solves from one invertible set of present columns
(rank_exclusion.section), and the saturation index is the gcd of all maximal
minors computed with Fractions.

For each record we check: rank r; no line of support <= rej; signed Riesz
S_O(delta) >= delta at some endpoint (i.e. not excluded); the greedy support
sequence equals the profile; the stated a, g, A, B.
"""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from rank_exclusion import section, det  # noqa: E402
from relrank_n import delta_bounds  # noqa: E402
from classes import parse  # noqa: E402


def rank(vecs):
    M = [list(map(Fr, v)) for v in vecs]
    rk, cols = 0, len(M[0]) if M else 0
    for c in range(cols):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def check(types, rec, prof, n, rej=2):
    r = len(prof)
    mv = rec["m"]
    present = [k for k in range(len(types)) if mv[k]]
    lines = section(types, mv)
    assert lines is not None
    assert rank([types[k] for k in present]) == r
    assert all(s > rej for s in lines.values()), "short line"
    D = delta_bounds(n)
    S = lambda d: sum(((d + s) / Fr(2 ** (s - 1))) * (1 if s % 2 else -1) for s in lines.values())
    assert any(S(d) >= d for d in D), "Riesz excluded"
    # S_O * 2^(n-1) = delta*A + B
    A = sum((1 if s % 2 else -1) * 2 ** (n - s) for s in lines.values())
    B = sum((1 if s % 2 else -1) * s * 2 ** (n - s) for s in lines.values())
    assert (A, B) == (rec["A"], rec["B"])
    # greedy: lines keyed by their values on the present types (one entry per type)
    odd = sorted((s, key) for key, s in lines.items() if s % 2)
    chosen, seq = [], []
    for s, key in odd:
        if rank(chosen + [key]) > len(chosen):
            chosen.append(key)
            seq.append(s)
    assert tuple(seq) == tuple(prof), (seq, prof)
    # a and saturated Gram
    a = sum(mv)
    G = [[sum(mv[k] * types[k][i] * types[k][j] for k in present) for j in range(r)] for i in range(r)]
    raw = det(G)
    idx = 0
    for J in combinations(present, r):
        idx = gcd(idx, abs(int(det([types[k] for k in J]))))
    g = raw / idx ** 2
    assert g.denominator == 1
    assert (a, int(g), idx) == (rec["a"], rec["g"], rec["idx"])
    return True


if __name__ == "__main__":
    n = int(sys.argv[1])
    tot = 0
    for path in sys.argv[2:]:
        types, recs, prof = parse(path)
        for rec in recs:
            check(types, rec, prof, n)
            tot += 1
    print("checked", tot, "records: all pass")
