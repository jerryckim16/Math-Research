"""Negative controls on real data: write a damaged copy of an int8
configuration that a correct checker must reject.

Modes:
  dup   : row 0 is overwritten by a copy of row 1 (a repeated point);
  merge : find a contact partner j of row 0 (p = T exactly, angle 60 deg)
          and overwrite row 0 by row_0 + row_j, which makes an angle of
          30 degrees with row_j (and the bounds still fit int8 / int16);
  flip  : negate one nonzero coordinate of row 0 (a small rotation that
          usually, but not always, breaks some contact; reported only).

Usage: python3 perturb.py IN.i8 d MODE OUT.i8
"""
import math
import sys

import numpy as np


def main(src, d, mode, dst):
    d = int(d)
    X = np.fromfile(src, dtype=np.int8).reshape(-1, d).copy()
    I = X.astype(np.int64)
    nrm = (I * I).sum(axis=1)
    if mode == "dup":
        X[0] = X[1]
    elif mode == "merge":
        p = I[1:] @ I[0]
        T = np.array([math.isqrt(int(nrm[0]) * int(b) // 4) for b in nrm[1:]])
        cand = np.nonzero((p == T) & (4 * T * T == nrm[0] * nrm[1:]))[0]
        assert len(cand), "row 0 has no contact partner"
        j = int(cand[0]) + 1
        new = I[0] + I[j]
        assert np.abs(new).max() <= 127
        X[0] = new.astype(np.int8)
        print(f"merge: row 0 := row 0 + row {j}")
    elif mode == "flip":
        k = int(np.nonzero(X[0])[0][0])
        X[0, k] = -X[0, k]
        print(f"flip: row 0 coordinate {k} negated")
    else:
        raise SystemExit("mode must be dup, merge or flip")
    X.tofile(dst)


if __name__ == "__main__":
    main(*sys.argv[1:5])
