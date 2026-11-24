"""Exact dimension of the span of an int8 row matrix (for exports whose
column count exceeds the claimed dimension, e.g. Qiushi 43D: 48 columns).

Method: greedily pick rows that are independent modulo the prime 2^61 - 1
(r of them; this shows rank over Q >= r). Compute an integer basis of the
rational kernel of those r rows with exact Fraction arithmetic, and verify in
exact int64 arithmetic that EVERY row is orthogonal to every kernel vector.
This shows that all rows lie in an r-dimensional subspace, so the rank over
Q equals r exactly.

Usage: python3 span_check.py FILE.i8 COLS
"""
import math
import sys
from fractions import Fraction

import numpy as np

P = (1 << 61) - 1


def independent_rows_mod_p(X, limit):
    basis = {}
    chosen = []
    n = X.shape[0]
    order = range(0, n, max(1, n // 20000))  # a spread-out sample suffices
    for i in order:
        v = [int(x) % P for x in X[i]]
        for c in sorted(basis):
            if v[c]:
                f = v[c]
                v = [(x - f * y) % P for x, y in zip(v, basis[c])]
        piv = next((c for c, x in enumerate(v) if x), None)
        if piv is None:
            continue
        inv = pow(v[piv], P - 2, P)
        v = [(x * inv) % P for x in v]
        for c in list(basis):
            if basis[c][piv]:
                f = basis[c][piv]
                basis[c] = [(x - f * y) % P for x, y in zip(basis[c], v)]
        basis[piv] = v
        chosen.append(i)
        if len(chosen) == limit:
            break
    return chosen


def rational_kernel(rows, m):
    """Integer basis of {x in Q^m : r.x = 0 for all r in rows}."""
    A = [[Fraction(int(x)) for x in r] for r in rows]
    piv_cols = []
    r = 0
    for c in range(m):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    free = [c for c in range(m) if c not in piv_cols]
    ker = []
    for fc in free:
        x = [Fraction(0)] * m
        x[fc] = Fraction(1)
        for i, pc in enumerate(piv_cols):
            x[pc] = -A[i][fc]
        den = 1
        for t in x:
            den = den * t.denominator // math.gcd(den, t.denominator)
        ker.append([int(t * den) for t in x])
    return ker


def main(path, cols):
    cols = int(cols)
    X = np.fromfile(path, dtype=np.int8).reshape(-1, cols)
    chosen = independent_rows_mod_p(X, cols)
    r = len(chosen)
    ker = rational_kernel([X[i] for i in chosen], cols)
    assert len(ker) == cols - r
    # exact check: all rows orthogonal to all kernel vectors (int64, chunked)
    if ker:
        Kmax = max(abs(int(v)) for row in ker for v in row)
        assert Kmax * 127 * cols < 2**62, "kernel entries too large for int64 check"
        K64 = np.array(ker, dtype=np.int64)
        bad = 0
        for s in range(0, X.shape[0], 1 << 18):
            bad += int(np.count_nonzero(X[s:s + (1 << 18)].astype(np.int64) @ K64.T))
        assert bad == 0, f"{bad} row/kernel products nonzero"
    print(f"rows {X.shape[0]} columns {cols}: rank mod 2^61-1 of chosen rows = {r}; "
          f"{len(ker)} kernel vectors orthogonal to all rows (exact) => rank over Q = {r}")
    return r


if __name__ == "__main__":
    main(*sys.argv[1:3])
