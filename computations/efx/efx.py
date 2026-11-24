"""Exact EFX(0) tools for additive valuations.

Definition (zero-tolerant, as in problems/efx-allocations.md): a complete
allocation X = (X_1..X_n) of goods 0..m-1 is EFX iff for all i != j and every
g in X_j,  v_i(X_i) >= v_i(X_j) - v_i(g).

* `exists(v)`        -> (bool, witness)   fast C enumeration, early exit
* `full(v)`          -> (bool, score, count, alloc)  full C enumeration
* `verify(v, alloc)` -> bool   independent pure-Python check from the definition
* `brute(v)`         -> bool   independent pure-Python n^m enumeration (tiny cases)

`v` is a list of n rows of m nonnegative integers (or Fractions for `verify`
and `brute`).  An allocation is a list `alloc` of length m: alloc[g] = owner.
"""
import ctypes
import itertools
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(HERE, "efxcore.c")
_LIB = os.path.join(HERE, "libefx.so")


def _load():
    if (not os.path.exists(_LIB)) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
        subprocess.check_call(["gcc", "-O3", "-march=native", "-shared", "-fPIC",
                               "-o", _LIB, _SRC])
    lib = ctypes.CDLL(_LIB)
    lib.efx_eval.restype = ctypes.c_int
    lib.efx_eval.argtypes = [ctypes.c_int, ctypes.c_int,
                             ctypes.POINTER(ctypes.c_int64), ctypes.c_int,
                             ctypes.POINTER(ctypes.c_int),
                             ctypes.POINTER(ctypes.c_double),
                             ctypes.POINTER(ctypes.c_longlong)]
    return lib


_lib = _load()


def _call(v, mode, seed=None):
    n = len(v)
    m = len(v[0]) if n else 0
    flat = [int(x) for row in v for x in row]
    if any(x < 0 for x in flat):
        raise ValueError("valuations must be nonnegative")
    if m and max(flat) * m >= 2 ** 62:
        raise ValueError("values too large for exact int64 arithmetic")
    arr = (ctypes.c_int64 * max(1, n * m))(*flat)
    wit = (ctypes.c_int * max(1, m))(*(list(seed) if seed else [-1] * max(1, m)))
    sc = ctypes.c_double(0.0)
    cnt = ctypes.c_longlong(0)
    r = _lib.efx_eval(n, m, arr, mode, wit, ctypes.byref(sc), ctypes.byref(cnt))
    if r < 0:
        raise ValueError("bad input")
    return bool(r), list(wit)[:m], sc.value, cnt.value


def exists(v):
    """Return (True, witness) if an EFX allocation exists, else (False, None)."""
    ok, wit, _, _ = _call(v, 0)
    return (True, wit) if ok else (False, None)


def full(v):
    """Full enumeration: (exists, score, number of EFX allocations, best alloc).

    score = max over complete allocations of min_i (v_i(X_i) - max_{j!=i}
    r_i(X_j)) / v_i(all goods); EFX exists iff score >= 0.  It is a float
    heuristic for search; `exists` (the bool) is exact.
    """
    ok, wit, sc, cnt = _call(v, 1)
    return ok, sc, cnt, wit


def score(v, seed=None):
    """Heuristic search objective only: (exists, score, alloc), with pruning.

    `seed` (an allocation) only speeds up the branch-and-bound.  `exists` is
    exact: it is True iff an EFX allocation was met during the enumeration,
    which in mode 2 can be skipped by pruning only when the pruned partition
    cannot beat a seed/incumbent; so call `exists()` for the exact answer.
    """
    ok, wit, sc, _ = _call(v, 2, seed)
    return ok, sc, wit


def verify(v, alloc):
    """Independent check of the EFX definition for one allocation (exact)."""
    n = len(v)
    m = len(v[0])
    if len(alloc) != m or any(not (0 <= a < n) for a in alloc):
        return False
    bundles = [[g for g in range(m) if alloc[g] == i] for i in range(n)]
    for i in range(n):
        own = sum(v[i][g] for g in bundles[i])
        for j in range(n):
            if j == i:
                continue
            tot_j = sum(v[i][g] for g in bundles[j])
            for g in bundles[j]:
                if own < tot_j - v[i][g]:
                    return False
    return True


def brute(v, want_all=False):
    """Pure-Python n^m enumeration directly from the definition."""
    n = len(v)
    m = len(v[0])
    found = []
    for alloc in itertools.product(range(n), repeat=m):
        if verify(v, list(alloc)):
            if not want_all:
                return True
            found.append(alloc)
    return found if want_all else False


if __name__ == "__main__":
    import json
    import sys
    data = json.load(sys.stdin)
    ok, wit = exists(data)
    print(json.dumps({"efx_exists": ok, "witness": wit,
                      "verified": ok and verify(data, wit)}))
