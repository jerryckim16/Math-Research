"""Second, independent implementation of the exact kissing check (numpy).

Same criterion as kiss_check.c: integer rows a_i, p = a_i.a_j, A, B squared
norms; the rows form a kissing configuration iff p <= isqrt(floor(AB/4)) for
all i < j.

Arithmetic: inner products are formed by float32 matrix products (BLAS
SGEMM) on integer inputs. This is exact when every squared norm is < 2^24:
every product a_k b_k and every partial sum, in any summation order, is an
integer of absolute value <= sum_k |a_k b_k| <= |a||b| < 2^24 (Cauchy-
Schwarz), hence exactly representable. The script checks that precondition.
Every pair flagged as a violation is recomputed in exact int64 arithmetic
before it is reported.

Work is split over row tiles; each worker process uses a single BLAS thread.

Usage: python3 kiss_check_np.py FILE.i8 d [--workers 4] [--tile 4096]
"""
import argparse
import math
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np  # noqa: E402

_G = {}


def _init(path, d):
    raw = np.fromfile(path, dtype=np.int8).reshape(-1, d)
    _G["X"] = raw.astype(np.float32)
    _G["I"] = raw.astype(np.int64)
    nrm = (_G["I"] ** 2).sum(axis=1)
    _G["nrm"] = nrm
    classes, cls = np.unique(nrm, return_inverse=True)
    _G["cls"] = cls
    _G["classes"] = classes
    k = len(classes)
    T = np.zeros((k, k), dtype=np.int64)
    for a in range(k):
        for b in range(k):
            T[a, b] = math.isqrt(int(classes[a]) * int(classes[b]) // 4)
    _G["T"] = T
    # contact value T where 4 T^2 == AB, else 2^25 (no |p| reaches it)
    C = np.where(4 * T * T == np.outer(classes, classes), T, 2**25).astype(np.float32)
    _G["C"] = C


def _tile(args):
    i0, i1, j0, j1 = args
    X, I, cls, T = _G["X"], _G["I"], _G["cls"], _G["T"]
    G = X[i0:i1] @ X[j0:j1].T  # float32, exact (see module docstring)
    thr = T[cls[i0:i1][:, None], cls[j0:j1][None, :]].astype(np.float32)
    if i0 == j0:  # diagonal tile: only pairs i < j
        G[np.tril_indices(i1 - i0, 0, j1 - j0)] = -1e9
    k = len(_G["classes"])
    maxp = np.full((k, k), -10**9, dtype=np.int64)
    if k == 1:  # fast path: one norm class, scalar threshold
        t, c = float(T[0, 0]), float(_G["C"][0, 0])
        maxp[0, 0] = int(G.max())
        cont = int(np.count_nonzero(G == c))
        if maxp[0, 0] <= t:
            return 0, cont, maxp, None
    ci = cls[i0:i1]
    cj = cls[j0:j1]
    for a in np.unique(ci):
        ra = ci == a
        for b in np.unique(cj):
            sub = G[np.ix_(ra, cj == b)]
            if sub.size:
                maxp[a, b] = max(maxp[a, b], int(sub.max()))
    # contacts: p == T(A,B) with 4 T^2 == AB (angle exactly 60 degrees)
    cmat = _G["C"][cls[i0:i1][:, None], cls[j0:j1][None, :]]
    cont = int(np.count_nonzero(G == cmat))
    # candidate violations, recomputed exactly in int64
    ii, jj = np.nonzero(G > thr)
    viol = 0
    first = None
    if len(ii):
        gi, gj = ii + i0, jj + j0
        p = (I[gi] * I[gj]).sum(axis=1)
        assert np.array_equal(p.astype(np.float32), G[ii, jj]), "float32 product not exact"
        A, B = _G["nrm"][gi], _G["nrm"][gj]
        bad = (p > 0) & (4 * p * p > A * B)
        assert bad.all()
        viol = int(bad.sum())
        first = (int(gi[0]), int(gj[0]))
    return viol, cont, maxp, first


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("d", type=int)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tile", type=int, default=4096)
    a = ap.parse_args()
    _init(a.path, a.d)
    n = _G["X"].shape[0]
    nrm = _G["nrm"]
    if (nrm == 0).any():
        print("zero row present\nRESULT FAIL")
        return 1
    if nrm.max() >= 2**24:
        print("squared norm too large for the float32 path")
        return 2
    t = a.tile
    tasks = [(i0, min(i0 + t, n), j0, min(j0 + t, n))
             for i0 in range(0, n, t) for j0 in range(i0, n, t)]
    if a.workers > 1:
        import multiprocessing as mp
        ctx = mp.get_context("fork")
        with ctx.Pool(a.workers) as pool:
            res = pool.map(_tile, tasks, chunksize=1)
    else:
        res = [_tile(x) for x in tasks]
    k = len(_G["classes"])
    viol = sum(r[0] for r in res)
    cont = sum(r[1] for r in res)
    maxp = np.full((k, k), -10**9, dtype=np.int64)
    firsts = [r[3] for r in res if r[3] is not None]
    for r in res:
        maxp = np.maximum(maxp, r[2])
    print(f"rows {n}\ncolumns {a.d}\nnorm_classes {k}")
    cnt = np.bincount(_G["cls"])
    for c in range(k):
        print(f"  squared_norm {int(_G['classes'][c])} count {int(cnt[c])}")
    print(f"pairs {n * (n - 1) // 2}")
    for x in range(k):
        for y in range(x, k):
            m = max(maxp[x, y], maxp[y, x])
            if m > -10**9:
                print(f"  class_pair {int(_G['classes'][x])},{int(_G['classes'][y])} "
                      f"max_inner_product {int(m)} threshold {int(_G['T'][x, y])}")
    print(f"contacts_60deg {cont}\nviolations {viol}")
    if firsts:
        print("first_violation %d %d" % min(firsts))
    print("RESULT", "PASS" if viol == 0 else "FAIL")
    return 0 if viol == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
