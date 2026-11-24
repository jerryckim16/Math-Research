"""Rebuild A. Kravatskiy's 352,992-point kissing configuration in R^32 from his
explicit certificate (repository alexlegeartis/KissingNumbers @ 907f9b1f,
verifications/improved/dim32-35-signed-layers/nonantipodal32/
certificate32_352992_explicit.json, the "original discovery certificate"),
with our own code. Untrusted data: only its JSON is parsed; no repository code
is run.

Certificate fields and the points they define (squared norm 32 throughout):
  dense_generator (17 ints, 32-bit masks): the binary code C they span;
      for each word c the point ((-1)^(bit i of c))_i.        131,072 points
  full_even_supports (1701 masks): all 128 sign patterns of +-2 on the 8
      coordinates of each support with an even number of minus signs.
                                                                217,728 points
  exceptional_signed_points (2208 pairs [support mask, minus mask]): +-2 on
      the support, minus exactly where the minus mask has a bit.  2,208 points
  roots: all +-4 e_i +-4 e_j (the certificate's construction says the 1,984
      roots of the parent are kept; 2 * 32 * 31 = 1,984).        1,984 points
Bit order: bit j of a mask is coordinate j ("lsb", the default for all
masks, as in build_kravatskiy33.py) or 31 - j ("msb", an option). A passing
set of 352,992 points proves the bound whatever the order; a wrong order can
only make a valid set fail.

Usage: python3 -I build_kravatskiy32.py certificate.json OUT.i8
         [--dense-order lsb|msb] [--support-order lsb|msb]
"""
import hashlib
import itertools
import json
import sys

import numpy as np

SHA = "a21b8ee4086cdbbc90651bcab378b888d0c3f10643aa0d63b5d208cafe471d1a"
D = 32


def coords(mask, order):
    assert 0 <= mask < 2**D
    js = [j for j in range(D) if mask >> j & 1]
    return sorted(js if order == "lsb" else [D - 1 - j for j in js])


def main(path, out, dorder="lsb", order="lsb"):
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "sha256 mismatch"
    c = json.loads(raw)
    assert c["format"] == "signed_octad_kissing_explicit_v1" and c["dimension"] == D
    gen = [int(g) for g in c["dense_generator"]]
    assert len(gen) == 17
    words = {0}
    for g in gen:
        words |= {w ^ g for w in words}
    assert len(words) == 2**17
    dense = np.zeros((2**17, D), dtype=np.int64)
    for r, w in enumerate(sorted(words)):
        for j in coords(w, dorder):
            dense[r, j] = 1
    dense = 1 - 2 * dense
    signs = np.array(list(itertools.product((1, -1), repeat=8)), dtype=np.int64)
    even = signs[(signs < 0).sum(1) % 2 == 0]
    fam = []
    for m in c["full_even_supports"]:
        cs = coords(int(m), order)
        assert len(cs) == 8
        b = np.zeros((128, D), dtype=np.int64)
        b[:, cs] = 2 * even
        fam.append(b)
    full = np.concatenate(fam)
    exc = []
    for m, neg in c["exceptional_signed_points"]:
        m, neg = int(m), int(neg)
        assert neg & ~m == 0, "minus mask outside support"
        v = np.zeros(D, dtype=np.int64)
        cs, ns = coords(m, order), set(coords(neg, order))
        assert len(cs) == 8
        for j in cs:
            v[j] = -2 if j in ns else 2
        exc.append(v)
    exc = np.array(exc)
    roots = []
    for i, j in itertools.combinations(range(D), 2):
        for si, sj in itertools.product((4, -4), repeat=2):
            v = np.zeros(D, dtype=np.int64)
            v[i], v[j] = si, sj
            roots.append(v)
    roots = np.array(roots)
    X = np.concatenate([dense, full, exc, roots])
    assert X.shape == (int(c["points"]), D) == (352992, D)
    assert ((X * X).sum(1) == 32).all()
    print(f"dense order {dorder}, support order {order}: dense {len(dense)} + full {len(full)} ({len(fam)} supports) + exceptional "
          f"{len(exc)} + roots {len(roots)} = {len(X)}")
    X.astype(np.int8).tofile(out)
    print(f"-> {out}")


if __name__ == "__main__":
    a = sys.argv
    dorder = a[a.index("--dense-order") + 1] if "--dense-order" in a else "lsb"
    order = a[a.index("--support-order") + 1] if "--support-order" in a else "lsb"
    assert dorder in ("lsb", "msb") and order in ("lsb", "msb")
    main(a[1], a[2], dorder, order)
