"""Exclusion of low odd-relation ranks by complete-section enumeration,
general rank r and general n (our own implementation of the method in the
proof of "Low-rank exclusions", App. B of Allikvere, Sixteen lonely runners;
audit_rank3.py is the r = 3, n = 15 special case and must agree).

For a counterexample v to LRC(n), let O be the span of the odd ternary
relations, of rank r, with greedy odd basis of supports s_1 <= ... <= s_r
(a profile surviving the greedy support bound, relrank_n.survivors).  The
r x n matrix of these rows has columns in {-1,0,1}^r; up to column sign
(which preserves every support) it is a multiplicity vector over the
(3^r - 1)/2 nonzero projective column types plus zero columns.  The ternary
section T(O) (all ternary vectors of the rational row space) and hence
S_O(delta) = sum_odd w - sum_even w depend only on that multiset.
Riesz: S_O(delta) > delta.  If, for every profile and every multiplicity
vector with that profile (and not containing a forbidden short line),
S_O(delta) < delta at both rational endpoints of delta, rank r is excluded.

Forbidden lines: support 1 (v_l = 0) always; optionally support 2
(v_i = +-v_j; a counterexample has distinct positive coordinates since
LRC(n-1) holds).
"""
import os
import sys
from fractions import Fraction as Fr
from itertools import product, combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relrank_n import delta_bounds, survivors  # noqa: E402


def canon(v):
    for x in v:
        if x:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)


def types(r):
    return sorted({canon(t) for t in product((-1, 0, 1), repeat=r) if any(t)})


def multiplicity_vectors(T, s, ncols):
    r = len(s)
    out, m = [], [0] * len(T)

    def rec(k, rem, sup):
        if k == len(T):
            if tuple(sup) == tuple(s):
                out.append(tuple(m))
            return
        t = T[k]
        for cnt in range(0, rem + 1):
            ns = [sup[i] + (cnt if t[i] else 0) for i in range(r)]
            if any(ns[i] > s[i] for i in range(r)):
                break
            m[k] = cnt
            rec(k + 1, rem - cnt, ns)
        m[k] = 0
    rec(0, ncols, [0] * r)
    return out


def det(M):
    M = [list(map(Fr, row)) for row in M]
    n, d = len(M), Fr(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            if f:
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d


def solve(A, b):
    n = len(A)
    M = [list(map(Fr, A[i])) + [Fr(b[i])] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * bb for a, bb in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def section(T, mv):
    r = len(T[0])
    present = [k for k in range(len(T)) if mv[k]]
    basis = None
    for J in combinations(present, r):
        if det([T[k] for k in J]) != 0:
            basis = J
            break
    if basis is None:
        return None
    lines = {}
    A = [T[k] for k in basis]              # rows: chosen column types; A lam = x
    for x in product((-1, 0, 1), repeat=r):
        if not any(x):
            continue
        lam = solve(A, x)
        vals = {k: sum(l * t for l, t in zip(lam, T[k])) for k in present}
        if all(val in (-1, 0, 1) for val in vals.values()):
            key = canon(tuple(vals[k] for k in present))
            lines[key] = sum(mv[k] for k in present if vals[k] != 0)
    return lines


def S(lines, d):
    tot = Fr(0)
    for s in lines.values():
        wv = (d + s) / Fr(2 ** (s - 1))
        tot += wv if s % 2 else -wv
    return tot


def exclude(n, r, reject_upto=1, profiles=None):
    D = delta_bounds(n)
    T = types(r)
    profiles = survivors(n, r, D) if profiles is None else profiles
    rep, excluded, total = {}, True, 0
    for prof in profiles:
        mvs = multiplicity_vectors(T, prof, n)
        total += len(mvs)
        best = {d: None for d in D}
        for mv in mvs:
            L = section(T, mv)
            if L is None or any(s <= reject_upto for s in L.values()):
                continue
            for d in D:
                val = S(L, d)
                if best[d] is None or val > best[d]:
                    best[d] = val
        ok = all(best[d] is None or best[d] < d for d in D)
        excluded &= ok
        rep[prof] = (len(mvs), {float(d): (None if best[d] is None else float(best[d])) for d in D}, ok)
    return excluded, total, rep, D


if __name__ == "__main__":
    n, r = int(sys.argv[1]), int(sys.argv[2])
    rej = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    ex, total, rep, D = exclude(n, r, rej)
    print(f"n={n} r={r} reject support<={rej} delta in {tuple(map(float, D))}")
    for k, v in rep.items():
        print(" ", k, v)
    print("multiplicity vectors:", total, " rank excluded:", ex)
