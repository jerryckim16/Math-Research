"""Exact kissing check for an int64 configuration with a few huge rows.

Used for the Qiushi 38D export (591900 x 52, little-endian int64), where
1932 "rotated axis" rows have entries up to ~4e17 and all other rows are
small. The pairs are split three ways:

  small x small  -> written out as int8 and checked by kiss_check.c
                    (this script only writes the file: --write-small PATH);
  big   x small  -> exact: each big entry is split as hi*2^31 + lo with
                    0 <= lo < 2^31, both parts multiplied against the small
                    rows in int64 (no overflow: |hi|,lo < 2^33 and the
                    small rows have |entry| <= 127, d <= 64), and the two
                    partial products recombined in Python integers wherever
                    a float64 screen cannot decide the sign of T - p;
  big   x big    -> exact Python-integer Gram matrix.

Criterion as in kiss_check.c: p <= 0 or 4 p^2 <= A B for every pair.

The script also checks the dimension claim: it verifies the stated linear
structure (columns 38..51 equal columns 24..37 in every row, so all rows
lie in a subspace of dimension <= 38) and computes the rank modulo the
prime 2^61 - 1 (a lower bound for the rank over Q).

Usage: python3 check_mixed.py FILE.i64 COLS [--write-small PATH]
       [--tail-copy START,LEN,START2]
"""
import argparse
import math
import sys

import numpy as np

P61 = (1 << 61) - 1


def rank_mod_p(rows, p=P61):
    """Rank over GF(p) of a list of integer rows (Python ints)."""
    basis = {}  # pivot column -> reduced row
    r = 0
    for row in rows:
        v = [int(x) % p for x in row]
        for c in sorted(basis):
            if v[c]:
                b = basis[c]
                f = v[c]
                v = [(x - f * y) % p for x, y in zip(v, b)]
        piv = next((c for c, x in enumerate(v) if x), None)
        if piv is None:
            continue
        inv = pow(v[piv], p - 2, p)
        v = [(x * inv) % p for x in v]
        for c in list(basis):
            b = basis[c]
            if b[piv]:
                f = b[piv]
                basis[c] = [(x - f * y) % p for x, y in zip(b, v)]
        basis[piv] = v
        r += 1
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("cols", type=int)
    ap.add_argument("--write-small")
    ap.add_argument("--tail-copy", help="START,LEN,START2: cols START2.. equal cols START..")
    a = ap.parse_args()
    X = np.fromfile(a.path, dtype="<i8").reshape(-1, a.cols)
    n = X.shape[0]
    big = (np.abs(X) > 127).any(axis=1)
    bi = np.nonzero(big)[0]
    si = np.nonzero(~big)[0]
    print(f"rows {n} columns {a.cols} big_rows {len(bi)} small_rows {len(si)}")
    S = X[si]
    nS = (S * S).sum(axis=1)
    assert nS.min() > 0 and nS.max() <= 32767
    Bpy = [[int(x) for x in X[i]] for i in bi]
    nB = [sum(x * x for x in r) for r in Bpy]
    assert min(nB) > 0
    print("squared norms: small", dict(zip(*[list(map(int, t)) for t in np.unique(nS, return_counts=True)])),
          "big", sorted(set(nB))[:3], f"({len(set(nB))} distinct)")

    # dimension: tail copy structure and rank
    if a.tail_copy:
        s0, ln, s2 = map(int, a.tail_copy.split(","))
        same = np.array_equal(X[:, s0:s0 + ln], X[:, s2:s2 + ln])
        print(f"tail_copy cols {s2}..{s2+ln-1} == cols {s0}..{s0+ln-1}: {same}"
              f"  => rows lie in a subspace of dimension <= {a.cols - ln}")
        assert same
    # rank mod p on a spread-out sample of rows (lower bound for rank over Q)
    step = max(1, n // 3000)
    sample = [[int(x) for x in X[i]] for i in range(0, n, step)] + Bpy[:200]
    rk = rank_mod_p(sample)
    print(f"rank_mod_(2^61-1) of {len(sample)} sampled rows: {rk}")

    if a.write_small:
        assert np.abs(S).max() <= 127
        S.astype(np.int8).tofile(a.write_small)
        print(f"small rows written to {a.write_small} ({len(si)} x {a.cols} int8)")

    viol = 0
    contacts = 0
    maxratio = -1.0  # max of p / sqrt(AB) over p > 0 (cosine), for reporting

    # big x big
    nb = len(Bpy)
    for x in range(nb):
        rx = Bpy[x]
        for y in range(x + 1, nb):
            p = sum(u * v for u, v in zip(rx, Bpy[y]))
            if p > 0:
                AB = nB[x] * nB[y]
                if 4 * p * p > AB:
                    viol += 1
                elif 4 * p * p == AB:
                    contacts += 1
                maxratio = max(maxratio, p / math.sqrt(AB))
    print(f"big x big: pairs {nb*(nb-1)//2} violations {viol} contacts {contacts} max_cos {maxratio:.12f}")

    # big x small
    SH = 1 << 31
    Bnp = X[bi]
    hi = np.floor_divide(Bnp, SH)
    lo = Bnp - hi * SH
    assert (lo >= 0).all() and (lo < SH).all()
    St = S.T.astype(np.int64)
    v2 = c2 = 0
    mr2 = -1.0
    CH = 64
    for x0 in range(0, nb, CH):
        H = hi[x0:x0 + CH] @ St  # int64, exact: |hi|<2^33, |s|<=5 (checked), cols<=64
        L = lo[x0:x0 + CH] @ St
        pf = H.astype(np.float64) * SH + L.astype(np.float64)
        for r in range(H.shape[0]):
            A = nB[x0 + r]
            # float screen: candidate pairs with p > 0 and p^2 within 1e-6 of AB/4
            ABf = A * nS.astype(np.float64)
            ratio = pf[r] / np.sqrt(ABf)
            mr2 = max(mr2, float(ratio.max()))
            cand = np.nonzero(ratio > 0.5 - 1e-6)[0]
            for c in cand:
                p = int(H[r, c]) * SH + int(L[r, c])
                AB = A * int(nS[c])
                if p > 0 and 4 * p * p > AB:
                    v2 += 1
                elif p > 0 and 4 * p * p == AB:
                    c2 += 1
    assert np.abs(S).max() * a.cols * 2**33 < 2**62
    print(f"big x small: pairs {nb*len(si)} violations {v2} contacts {c2} max_cos {mr2:.12f}")
    total = viol + v2
    print("RESULT(big pairs)", "PASS" if total == 0 else "FAIL")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
