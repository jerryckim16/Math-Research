"""Independent re-implementation of the rank-three exclusion in the proof of
"Low-rank exclusions" (App. B of Allikvere, Sixteen lonely runners, Zenodo
10.5281/zenodo.23304361), written from the TeX description only.

For each greedy support profile (s1,s2,s3) left by the greedy support bound,
enumerate all multiplicity vectors m_t >= 0 over the 13 nonzero projective
column types t in {-1,0,1}^3 with row supports s1, s2, s3 and at most 15
nonzero columns.  For each matrix of rank 3, compute the complete ternary
section of its row space (all rational combinations lambda^T H that are
ternary), reject sections containing a support-one line, and evaluate
S_O(delta) = sum_odd w(s) - sum_even w(s), w(s) = (delta+s)/2^(s-1), at the
two rational endpoints of delta.  The paper's claim: the maximum per profile
is the listed affine function of delta, and it is < delta.

Exact Fractions throughout.
"""
from fractions import Fraction as Fr
from itertools import product, combinations

DLO, DHI = Fr(5137, 1000), Fr(2569, 500)


def canon(v):
    for x in v:
        if x:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)


TYPES = sorted({canon(t) for t in product((-1, 0, 1), repeat=3) if any(t)})
assert len(TYPES) == 13
PROFILES = [(3, 3, 3), (3, 3, 5), (3, 3, 7), (3, 3, 9), (3, 3, 11), (3, 3, 13), (3, 3, 15), (3, 5, 5), (5, 5, 5)]


def multiplicity_vectors(s):
    out = []
    m = [0] * 13

    def rec(k, rem, sup):
        if k == 13:
            if list(sup) == list(s):
                out.append(tuple(m))
            return
        t = TYPES[k]
        for c in range(0, rem + 1):
            ns = [sup[i] + (c if t[i] else 0) for i in range(3)]
            if any(ns[i] > s[i] for i in range(3)):
                break
            m[k] = c
            rec(k + 1, rem - c, ns)
        m[k] = 0
    rec(0, 15, [0, 0, 0])
    return out


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def solve3(cols, x):
    """lambda with lambda . cols[k] = x[k] (Cramer)."""
    D = det3(*cols)
    res = []
    for i in range(3):
        M = [list(c) for c in cols]
        # replace i-th coordinate: we solve C lambda = x where rows of C are cols
        A = [[cols[k][j] for j in range(3)] for k in range(3)]
        for k in range(3):
            A[k][i] = x[k]
        res.append(Fr(det3(*A), D))
    return res


def section(mv):
    present = [TYPES[k] for k in range(13) if mv[k]]
    basis = None
    for J in combinations(present, 3):
        if det3(*J) != 0:
            basis = J
            break
    if basis is None:
        return None  # rank < 3
    lines = {}
    for x in product((-1, 0, 1), repeat=3):
        if not any(x):
            continue
        lam = solve3(basis, x)
        vals = [sum(l * t for l, t in zip(lam, T)) for T in TYPES]
        if all(vals[k] in (-1, 0, 1) for k in range(13) if mv[k]):
            key = canon(tuple(vals[k] if mv[k] else 0 for k in range(13)))
            s = sum(mv[k] for k in range(13) if mv[k] and vals[k] != 0)
            lines[key] = s
    return lines


def S(lines, d):
    tot = Fr(0)
    for s in lines.values():
        wv = (d + s) / Fr(2 ** (s - 1))
        tot += wv if s % 2 else -wv
    return tot


def run():
    report = {}
    total = 0
    for prof in PROFILES:
        mvs = multiplicity_vectors(prof)
        total += len(mvs)
        best = {DLO: None, DHI: None}
        for mv in mvs:
            L = section(mv)
            if L is None or any(s == 1 for s in L.values()):
                continue
            for d in (DLO, DHI):
                val = S(L, d)
                if best[d] is None or val > best[d]:
                    best[d] = val
        report[prof] = (len(mvs), {float(d): (float(best[d]), best[d] < d) for d in best})
    return total, report


if __name__ == "__main__":
    total, rep = run()
    for k, v in rep.items():
        print(k, v)
    print("total multiplicity vectors:", total)
