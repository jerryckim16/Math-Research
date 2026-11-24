"""Compare two int8 configurations row-set-wise (exact integer rows).

Reports |A|, |B|, |A n B|, |A \\ B|, |B \\ A|, and for the rows of A \\ B a
breakdown by (number of nonzero entries, max |entry|). Used to relate
Kravatskiy's 32D and 33D configurations to Lin's (arXiv:2611.03682)
as rebuilt by build_lin.py. Pure bookkeeping: validity is decided elsewhere.

Usage: python3 -I compare_rows.py A.i8 B.i8 D [--mirror-lin-octads]
       B may be given as LINnn:<dir32>:<dir33_39> to rebuild Lin's nn-D rows
       with build_lin.build_ers (nn = 32..37 or 39). --mirror-lin-octads then
       maps the octad (middle) layer of Lin's rows by coordinate j -> m-1-j,
       m = number of coordinates of his support strings (32 for nn = 32,
       nn otherwise); dense layer and roots are left unchanged.
"""
import collections
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(spec, d, mirror=False):
    if spec.startswith("LIN"):
        sys.path.insert(0, HERE)
        import build_lin
        _, l32, l33 = spec.split(":")
        n = int(spec[3:5])
        L = np.asarray(build_lin.build_ers(n, l32, l33), dtype=np.int8).reshape(-1, d).copy()
        if mirror:
            ndense, nroots = (327680 if n == 39 else 131072), 2 * n * (n - 1)
            m = 32 if n == 32 else n
            mid = L[ndense:len(L) - nroots]
            mid[:, :m] = mid[:, :m][:, ::-1]
            L[ndense:len(L) - nroots] = mid
        return L
    return np.fromfile(spec, dtype=np.int8).reshape(-1, d)


def shape(rows):
    nz = (rows != 0).sum(1)
    mx = np.abs(rows.astype(np.int16)).max(1)
    return collections.Counter(zip(nz.tolist(), mx.tolist()))


def main(a, b, d, mirror=False):
    A, B = load(a, d), load(b, d, mirror)
    sa = {r.tobytes() for r in A}
    sb = {r.tobytes() for r in B}
    assert len(sa) == len(A) and len(sb) == len(B), "repeated rows"
    only_a = np.array([np.frombuffer(x, dtype=np.int8) for x in sa - sb]).reshape(-1, d)
    only_b = np.array([np.frombuffer(x, dtype=np.int8) for x in sb - sa]).reshape(-1, d)
    print(f"|A| = {len(sa)}, |B| = {len(sb)}, |A n B| = {len(sa & sb)}")
    print(f"A \\ B: {len(only_a)} rows, (nonzeros, max|x|) -> {dict(shape(only_a))}")
    print(f"B \\ A: {len(only_b)} rows, (nonzeros, max|x|) -> {dict(shape(only_b))}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), "--mirror-lin-octads" in sys.argv)
