"""Exact pairwise kissing check for points with coordinates in Q(sqrt2, sqrt3).

Input (written by build_qiushi2527.py):
  BULK.i8     raw int8 rows (pure-integer points), n_S x d
  FIELD.json  {"d": d, "rows": [[C0, C1, C2, C3], ...]}, each C_k a list of d
              Python integers; the point is x = C0 + C1 sqrt2 + C2 sqrt3 + C3 sqrt6
              (up to a positive factor, which does not change angles).
Pairs inside BULK are NOT checked here (kiss_check.c / kiss_check_np.py do
that). This program checks every pair (field row, bulk row) and every pair
of distinct field rows, so together the two checks cover all pairs.

Criterion (as in kiss_check.c): with p = x.y and A = |x|^2, B = |y|^2 the
angle is >= 60 degrees iff p <= 0 or 4p^2 <= AB.  Here
  p = P0 + P1 sqrt2 + P2 sqrt3 + P3 sqrt6, with integers
  P0 = X0.Y0 + 2 X1.Y1 + 3 X2.Y2 + 6 X3.Y3,   P1 = X0.Y1 + X1.Y0 + 3(X2.Y3 + X3.Y2),
  P2 = X0.Y2 + X2.Y0 + 2(X1.Y3 + X3.Y1),      P3 = X0.Y3 + X3.Y0 + X1.Y2 + X2.Y1.
Every squared norm is computed exactly and must be a positive integer (its
sqrt2, sqrt3, sqrt6 parts must vanish); the program aborts otherwise.

Two independent decision procedures (--mode):
  float     float64 GEMM on the normalised real coordinates. A pair is accepted
            when its cosine is < 1/2 - 1e-9 and flagged when > 1/2 + 1e-9; the
            rest are decided exactly by `exact_nested`. Rounding: every row's
            float coordinates are within 4*2^-52*kappa*|x| of the true ones,
            kappa = |sum_k |C_k| sqrt k| / |x| (checked <= 4), so the computed
            cosine is within (d + 40)*2^-52*16 < 1e-11 of the true one.
            exact_nested: sign of a + b sqrt2 + c sqrt3 + d sqrt6 by repeated
            squaring in Python integers (exact; zero iff a = b = c = d = 0).
  interval  exact integer P0..P3 for every pair (float64 GEMM on 24-bit limbs,
            exact because every partial sum is an integer below 2^53, checked),
            then integer interval bounds for sqrt2, sqrt3, sqrt6 and for
            sqrt(AB)/2 at scale 2^12 (int64, vectorised); undecided pairs are
            refined with Python integers at scales 2^64 ... 2^1024, and a pair
            still undecided is tested for exact equality 4p^2 = AB.
Both report the number of violating pairs and of exact contacts (4p^2 = AB);
a passing check needs 0 violations.

Usage: python3 kiss_check_field.py BULK.i8 FIELD.json --mode float|interval [--workers 4]
"""
import argparse
import json
import math
import multiprocessing as mp
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

R2, R3, R6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
DELTA = 1e-9
G = {}


# ---------------------------------------------------------------- exact algebra
def pair_coeffs(x, y):
    """Exact (P0, P1, P2, P3) of x.y for x, y given as 4 lists of ints."""
    def dot(a, b):
        return sum(s * t for s, t in zip(a, b))
    X0, X1, X2, X3 = x
    Y0, Y1, Y2, Y3 = y
    return (dot(X0, Y0) + 2 * dot(X1, Y1) + 3 * dot(X2, Y2) + 6 * dot(X3, Y3),
            dot(X0, Y1) + dot(X1, Y0) + 3 * (dot(X2, Y3) + dot(X3, Y2)),
            dot(X0, Y2) + dot(X2, Y0) + 2 * (dot(X1, Y3) + dot(X3, Y1)),
            dot(X0, Y3) + dot(X3, Y0) + dot(X1, Y2) + dot(X2, Y1))


def square(P):
    a, b, c, d = P
    return (a * a + 2 * b * b + 3 * c * c + 6 * d * d, 2 * a * b + 6 * c * d,
            2 * a * c + 4 * b * d, 2 * a * d + 2 * b * c)


def sign2(u, v):
    """sign of u + v sqrt2 (integers)."""
    su, sv = (u > 0) - (u < 0), (v > 0) - (v < 0)
    if su == 0 or sv == 0 or su == sv:
        return su or sv
    return su if u * u > 2 * v * v else sv      # u^2 = 2v^2 impossible unless both 0


def sign4(a, b, c, d):
    """sign of (a + b sqrt2) + sqrt3 (c + d sqrt2)."""
    sa, sb = sign2(a, b), sign2(c, d)
    if sa == 0 or sb == 0 or sa == sb:
        return sa or sb
    s = sign2(a * a + 2 * b * b - 3 * c * c - 6 * d * d, 2 * a * b - 6 * c * d)
    assert s != 0
    return sa if s > 0 else sb


def exact_nested(P, A, B):
    """-1 pass (strict), 0 contact, +1 violation."""
    if sign4(*P) <= 0:
        return -1
    Q = square(P)
    return sign4(4 * Q[0] - A * B, 4 * Q[1], 4 * Q[2], 4 * Q[3])


def exact_interval(P, A, B):
    """Same verdict by rigorous integer intervals, plus an equality test."""
    Q = None
    for s in (64, 128, 256, 512, 1024):
        r = [None, math.isqrt(2 << (2 * s)), math.isqrt(3 << (2 * s)), math.isqrt(6 << (2 * s))]
        lo = hi = P[0] << s
        for k in (1, 2, 3):
            lo += P[k] * (r[k] if P[k] >= 0 else r[k] + 1)
            hi += P[k] * (r[k] + 1 if P[k] >= 0 else r[k])
        if hi <= 0:
            return -1
        tlo = math.isqrt((A * B) << (2 * s - 2))      # tlo <= 2^s sqrt(AB)/2 < tlo + 1
        if hi < tlo:
            return -1
        if lo > tlo + 1:
            return 1
        if Q is None:
            Q = square(P)
            if 4 * Q[0] == A * B and Q[1] == Q[2] == Q[3] == 0 and lo > 0:
                return 0                                 # p > 0 and 4p^2 = AB
    raise ArithmeticError("undecided pair")


# ---------------------------------------------------------------- loading
def load(bulk_path, field_path):
    meta = json.load(open(field_path))
    d = int(meta["d"])
    rows = [[[int(t) for t in comp] for comp in r] for r in meta["rows"]]
    assert all(len(r) == 4 and all(len(c) == d for c in r) for r in rows)
    Bk = np.fromfile(bulk_path, dtype=np.int8).astype(np.int64).reshape(-1, d)
    nB = (Bk * Bk).sum(1)
    assert np.all(nB > 0)
    norms = []
    for r in rows:
        N = pair_coeffs(r, r)
        assert N[1] == N[2] == N[3] == 0 and N[0] > 0, "squared norm not a positive integer"
        norms.append(N[0])
    return d, Bk, nB, rows, norms


def real_rows(rows, norms):
    X = np.array([[float(r[0][c]) + float(r[1][c]) * R2 + float(r[2][c]) * R3 + float(r[3][c]) * R6
                   for c in range(len(r[0]))] for r in rows])
    K = np.array([[abs(float(r[0][c])) + abs(float(r[1][c])) * R2 + abs(float(r[2][c])) * R3
                   + abs(float(r[3][c])) * R6 for c in range(len(r[0]))] for r in rows])
    nr = np.sqrt(np.array([float(n) for n in norms]))
    kappa = np.linalg.norm(K, axis=1) / nr
    assert kappa.max() <= 4, kappa.max()
    return X / nr[:, None]


# ---------------------------------------------------------------- float mode
def float_block(lo_hi):
    lo, hi = lo_hi
    Uf, Ub, rows, norms, Bk, nB = G["Uf"], G["Ub"], G["rows"], G["norms"], G["Bk"], G["nB"]
    viol = cont = npairs = amb = 0
    cmax = -2.0
    for i in range(lo, hi):
        cb = Ub @ Uf[i]
        cf = Uf[i + 1:] @ Uf[i]
        npairs += len(cb) + len(cf)
        cmax = max(cmax, float(cb.max()), float(cf.max()) if len(cf) else -2.0)
        x = rows[i]
        for j in np.flatnonzero(cb >= 0.5 - DELTA):
            y = [Bk[j].tolist(), [0] * len(x[0]), [0] * len(x[0]), [0] * len(x[0])]
            v = exact_nested(pair_coeffs(x, y), norms[i], int(nB[j]))
            amb += 1
            viol += v > 0
            cont += v == 0
        for j in np.flatnonzero(cf >= 0.5 - DELTA) + i + 1:
            v = exact_nested(pair_coeffs(x, rows[j]), norms[i], norms[j])
            amb += 1
            viol += v > 0
            cont += v == 0
    return npairs, viol, cont, amb, cmax


# ---------------------------------------------------------------- interval mode
LB = 24
S = 12


def limbs(M):
    """Signed 24-bit limbs of an object/int matrix: M = sum_l L_l 2^(24 l)."""
    M = np.asarray(M, dtype=object)
    sg = np.where(M < 0, -1, 1)
    A = np.abs(M)
    out = []
    while True:
        out.append((sg * (A % (1 << LB))).astype(np.int64))
        A = A >> LB
        if not A.any():
            return out


def exact_products(xl, Ys):
    """sum_c x_c Y[:, c] exactly: xl = limbs of x (int64 vectors), Ys = list of
    limb matrices of Y.  Returns int64 if it fits, else an object array."""
    parts = []
    for a, xa in enumerate(xl):
        for b, Yb in enumerate(Ys):
            if not xa.any() or not Yb.any():
                continue
            bound = int(np.abs(xa).sum()) * int(np.abs(Yb).max(initial=0))
            assert bound < 2**53
            v = (Yb.astype(np.float64) @ xa.astype(np.float64))
            parts.append((a + b, np.rint(v).astype(np.int64)))
    if not parts:
        return np.zeros(Ys[0].shape[0], dtype=np.int64)
    if all(sh == 0 for sh, _ in parts):
        return sum(v for _, v in parts)
    tot = np.zeros(len(parts[0][1]), dtype=object)
    for sh, v in parts:
        tot = tot + v.astype(object) * (1 << (LB * sh))
    return tot


def interval_decide(P, A, Bv, idx_fn):
    """P: 4 arrays (int64 or object), A: int, Bv: int64 array of partner norms.
    Vectorised integer-interval screen at scale 2^S; returns (viol, cont)."""
    r = [None, math.isqrt(2 << 2 * S), math.isqrt(3 << 2 * S), math.isqrt(6 << 2 * S)]
    obj = any(p.dtype == object for p in P) or A * int(Bv.max()) >= 2**38
    if obj or max(int(np.abs(p).max()) for p in P) >= 2**40:
        P = [p.astype(object) for p in P]
        Bv = Bv.astype(object)
    lo = P[0] * (1 << S)
    hi = P[0] * (1 << S)
    for k in (1, 2, 3):
        pos = P[k] >= 0
        lo = lo + np.where(pos, P[k] * r[k], P[k] * (r[k] + 1))
        hi = hi + np.where(pos, P[k] * (r[k] + 1), P[k] * r[k])
    tlo = np.array([math.isqrt(A * int(b) << (2 * S - 2)) for b in Bv], dtype=object)
    if not obj:
        tlo = tlo.astype(np.int64)
    sure = (hi <= 0) | (hi < tlo)    # strict: exact contacts go to exact_interval
    viol = cont = 0
    und = np.flatnonzero(~np.asarray(sure, dtype=bool))
    for j in und:
        v = exact_interval([int(p[j]) for p in P], A, int(Bv[j]))
        viol += v > 0
        cont += v == 0
    return viol, cont, len(und)


def interval_block(lo_hi):
    lo, hi = lo_hi
    rows, norms, BkL, nB = G["rows"], G["norms"], G["BkL"], G["nB"]
    FL, fn = G["FL"], G["fnorm"]
    viol = cont = npairs = und = 0
    zero = None
    for i in range(lo, hi):
        x = rows[i]
        xl = [limbs(np.array(c, dtype=object)) for c in x]
        # partner = bulk (only Y0 nonzero)
        D = [exact_products(xl[k], BkL) for k in range(4)]
        P = [D[0], D[1], D[2], D[3]]
        v, c, u = interval_decide(P, norms[i], nB, None)
        viol += v
        cont += c
        und += u
        npairs += len(nB)
        if i + 1 < len(rows):
            Y = [[L[i + 1:] for L in FL[k]] for k in range(4)]
            dd = {(a, b): exact_products(xl[a], Y[b]) for a in range(4) for b in range(4)}
            P = [dd[0, 0] + 2 * dd[1, 1] + 3 * dd[2, 2] + 6 * dd[3, 3],
                 dd[0, 1] + dd[1, 0] + 3 * (dd[2, 3] + dd[3, 2]),
                 dd[0, 2] + dd[2, 0] + 2 * (dd[1, 3] + dd[3, 1]),
                 dd[0, 3] + dd[3, 0] + dd[1, 2] + dd[2, 1]]
            v, c, u = interval_decide(P, norms[i], fn[i + 1:], None)
            viol += v
            cont += c
            und += u
            npairs += len(rows) - i - 1
    return npairs, viol, cont, und, zero


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bulk")
    ap.add_argument("field")
    ap.add_argument("--mode", choices=("float", "interval"), required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    d, Bk, nB, rows, norms = load(a.bulk, a.field)
    nS, nT = len(Bk), len(rows)
    print(f"bulk rows {nS}, field rows {nT}, d {d}")
    print(f"field squared norms (distinct): {sorted(set(norms))[:12]}{' ...' if len(set(norms)) > 12 else ''}")
    G.update(rows=rows, norms=norms, Bk=Bk, nB=nB)
    if a.mode == "float":
        G["Uf"] = real_rows(rows, norms)
        G["Ub"] = Bk / np.sqrt(nB)[:, None]
        fn = float_block
    else:
        G["BkL"] = [Bk]                       # |entries| <= 127: a single limb
        big = max(max(abs(t) for c in r for t in c) for r in rows)
        nl = 1
        while big >> (LB * nl):
            nl += 1
        FL = []
        for k in range(4):
            Mk = np.array([r[k] for r in rows], dtype=object)
            L = limbs(Mk)
            L += [np.zeros_like(L[0])] * (nl - len(L))
            FL.append(L)
        G["FL"] = FL
        G["fnorm"] = np.array(norms, dtype=object)
        if max(norms) < 2**62:
            G["fnorm"] = G["fnorm"].astype(np.int64)
        fn = interval_block
    step = max(1, nT // (16 * a.workers))
    blocks = [(s, min(nT, s + step)) for s in range(0, nT, step)]
    with mp.get_context("fork").Pool(a.workers) as pool:
        res = pool.map(fn, blocks)
    npairs = sum(r[0] for r in res)
    viol = sum(r[1] for r in res)
    cont = sum(r[2] for r in res)
    ex = sum(r[3] for r in res)
    expect = nT * nS + nT * (nT - 1) // 2
    assert npairs == expect, (npairs, expect)
    print(f"pairs_checked {npairs} (field x bulk {nT * nS}, field x field {nT * (nT - 1) // 2})")
    print(f"exactly_decided_pairs {ex}")
    if a.mode == "float":
        print(f"max_cosine_float {max(r[4] for r in res):.12f}")
    print(f"violations {viol}")
    print(f"contacts_60deg {cont}")
    print(f"RESULT {'PASS' if viol == 0 else 'FAIL'}")
    return 0 if viol == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
