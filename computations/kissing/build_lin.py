"""Build Q. Lin's kissing configurations (arXiv:2611.03682v1) from his
certificate files, with our own parser, as integer row matrices.

Construction (Edel-Rains-Sloane three layers, as stated in Lin's README and
paper), in R^n:
  dense  : ((-1)^{c_i}) on coordinates 0..m-1 for every word c of a binary
           code D (n = 32..37: Cheng-Sloane [32,17,8] code, m = 32;
           n = 39: union of 10 cosets of a [39,15] code, m = 39);
  middle : for each weight-8 support S, the 128 vectors equal to +-2 on S
           with an even number of minus signs;
  roots  : +-4 e_i +- 4 e_j (2 n (n-1) vectors).
n = 38: the first 591612 rows (Kravatskiy's 591612-point configuration:
caps and rotated axes) of the Qiushi 38D export, plus +-(v, 0) for each of
Lin's 6855 norm-48 Leech vectors v (padded with 28 zeros).

Nothing here assumes the configuration is valid; validity is decided by
kiss_check.c / check_mixed.py on the output. The builder only checks the
claimed counts.

Usage: python3 -I build_lin.py LIN_DIR_32 LIN_DIR_33_39 QIUSHI_DIR OUTDIR
(LIN_DIR_* are the unpacked Zenodo archives; QIUSHI_DIR holds qiushi38.i64.)
"""
import itertools
import os
import sys

import numpy as np

CLAIMS = {32: 352320, 33: 370240, 34: 390980, 35: 415308, 37: 499816, 38: 605322, 39: 768916}
SUPPORTS = {32: "certificates/supports_1713.txt", 33: "certificates/d33/supports_1852.txt",
            34: "certificates/d34/supports_2013.txt", 35: "certificates/d35/supports_2202.txt",
            37: "certificates/d37/supports_2860.txt", 39: "certificates/d39/supports_3424.txt"}


def data_lines(path):
    for line in open(path, encoding="ascii"):
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("$"):
            yield s


def code_from_binary_generator(path, m):
    """All 2^k codewords of the binary code spanned by 0/1 strings (leftmost
    character = coordinate 0)."""
    gens = []
    for s in data_lines(path):
        assert len(s) == m and set(s) <= {"0", "1"}, s
        gens.append(sum(1 << i for i, ch in enumerate(s) if ch == "1"))
    return span(gens), len(gens)


def span(gens):
    words = [0]
    for g in gens:
        words = words + [w ^ g for w in words]
    return words


def hex_rows(path):
    return [int(s, 16) for s in data_lines(path)]


def dense_vectors(words, m, n):
    """Words as ints (bit i = coordinate i) -> rows (+-1 on coords < m)."""
    w = np.array(words, dtype=np.uint64)
    bits = ((w[:, None] >> np.arange(m, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(np.int8)
    out = np.zeros((len(words), n), dtype=np.int8)
    out[:, :m] = 1 - 2 * bits
    return out


def middle_vectors(path, n):
    supports = []
    for s in data_lines(path):
        assert len(s) == n and set(s) <= {"0", "1"} and s.count("1") == 8, s
        supports.append([i for i, ch in enumerate(s) if ch == "1"])
    assert len(set(map(tuple, supports))) == len(supports), "repeated support"
    signs = np.array([sg for sg in itertools.product((1, -1), repeat=8) if sg.count(-1) % 2 == 0],
                     dtype=np.int8)  # 128 even sign patterns
    out = np.zeros((len(supports) * 128, n), dtype=np.int8)
    for k, S in enumerate(supports):
        out[k * 128:(k + 1) * 128, S] = 2 * signs
    return out, len(supports)


def root_vectors(n):
    rows = []
    for i, j in itertools.combinations(range(n), 2):
        for a in (4, -4):
            for b in (4, -4):
                v = [0] * n
                v[i], v[j] = a, b
                rows.append(v)
    return np.array(rows, dtype=np.int8)


def build_ers(n, lin32, lin33):
    base = lin32 if n == 32 else lin33
    if n == 39:
        kernel = hex_rows(os.path.join(lin33, "certificates/d39/dense_kernel.txt"))
        reps = hex_rows(os.path.join(lin33, "certificates/d39/dense_representatives.txt"))
        C = span(kernel)
        assert len(set(C)) == 2 ** len(kernel) == 32768
        words = sorted({r ^ c for r in reps for c in C})
        assert len(words) == 327680, len(words)
        m = 39
    else:
        gen = os.path.join(base, "gen32_17.txt" if n == 32 else "certificates/gen32_17.txt")
        words, k = code_from_binary_generator(gen, 32)
        assert k == 17 and len(set(words)) == 131072
        m = 32
    dense = dense_vectors(words, m, n)
    mid, nsup = middle_vectors(os.path.join(base, SUPPORTS[n]), n)
    roots = root_vectors(n)
    X = np.concatenate([dense, mid, roots])
    print(f"n={n}: dense {len(dense)} + middle 128x{nsup}={len(mid)} + roots {len(roots)} = {len(X)}"
          f" (claimed {CLAIMS[n]})")
    assert len(X) == CLAIMS[n]
    return X


def build_38(lin33, qdir):
    Q = np.fromfile(os.path.join(qdir, "qiushi38.i64"), dtype="<i8").reshape(-1, 52)
    base = Q[:591612]
    L = np.array([[int(x) for x in s.split()] for s in
                  data_lines(os.path.join(lin33, "certificates/d38/equator_lines_6855.txt"))], dtype=np.int64)
    assert L.shape == (6855, 24)
    eq = np.zeros((2 * len(L), 52), dtype=np.int64)
    eq[0::2, :24] = L
    eq[1::2, :24] = -L
    X = np.concatenate([base, eq])
    print(f"n=38: Kravatskiy base {len(base)} + 2x{len(L)} equatorial = {len(X)} (claimed {CLAIMS[38]})")
    assert len(X) == CLAIMS[38]
    return X


def main(lin32, lin33, qdir, out):
    os.makedirs(out, exist_ok=True)
    for n in (32, 33, 34, 35, 37, 39):
        build_ers(n, lin32, lin33).tofile(os.path.join(out, f"lin{n}.i8"))
    build_38(lin33, qdir).astype("<i8").tofile(os.path.join(out, "lin38.i64"))


if __name__ == "__main__":
    main(*sys.argv[1:5])
