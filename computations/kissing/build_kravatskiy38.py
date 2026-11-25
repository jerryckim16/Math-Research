"""Rebuild A. Kravatskiy's 652,076-point kissing configuration in R^38 from
its chain of edits (repository alexlegeartis/KissingNumbers @ 907f9b1f,
verifications/improved/), with our own code. Untrusted data: only JSON and
text are parsed; none of the repository's code is run.

Chain (read from the files and the packages' READMEs):
  dim37-38-qr-merge   dense_parent39.json: 15 generators (hex, 39 bits) of the
                      binary code of Yang et al., arXiv:2609.35051v1, App. B;
                      supports_3088.txt: Lin's 3,088 weight-8 supports in 38
                      coordinates (character i = coordinate i).
  -> dim38-qr-free-offsets (652,028 points): offset_witness.txt, three lines
                      "k s_1 ... s_k" of 24-bit syndromes, for the heads
                      +3, 0, -3 in that order (11 + 10 + 10 fibres).
  -> dim38-qr-octad-switches (652,076 points): witness.json, 10 support
                      replacements {i, remove, add} and 18 star templates
                      [centre, 4 leaves].
Points (integer coordinates):
  dense  31 fibres x 8,192: K = {v >> 2 : v in the code, v & 3 = 0} (37-bit
         words, 2^13 of them, min. distance 12). The syndrome of a 39-bit
         word x is its normal form modulo the code (zero at the code's pivot
         positions, which are canonical) read at the 24 non-pivot positions.
         A fibre with syndrome s and head h is {(h; 2(-1)^(bit j of b ^ k) at
         coordinate j + 1) : k in K}, where b is any 37-bit word with
         syndrome(b << 2) = s (the fibre does not depend on the choice).
         Squared norm 148 + h^2. Coordinate 0 is the marked coordinate.
  octads 3,088 x 128: +-2 on each support (after the 10 replacements), an
         even number of minus signs; squared norm 32.
  stars  18 x 16: centre +-4, leaves +-2 with an ODD number of minus signs
         (README: "all eight odd-parity leaf signings"; its verify.py does
         the same, while its audit.py builds even-parity leaves:
         --variant evenstars builds that version too).
  roots  every +-4 e_i +-4 e_j (i < j) whose inner product with every star
         is <= 16: 2 * 38 * 37 - 240 = 2,572.
Bit conventions: the dense placement (bit j -> coordinate j + 1) and the sign
convention only matter up to an isometry for dense x dense pairs, and the
dense x sparse pairs are bounded by magnitudes alone; a wrong convention can
only make a valid set fail, so a passing set proves the bound anyway.

Usage: python3 -I build_kravatskiy38.py KRAVDIR OUT.i8 [--variant NAME]
  variants: evenstars (audit.py's even leaf parity; should pass), and the
  negative controls (must FAIL): unswitched (the final stars and roots on the
  parent's unswitched supports), halfswitch (only the first 6 replacements).
"""
import hashlib
import itertools
import json
import os
import sys

import numpy as np

D = 38
SHA = {
    "k38_supports_3088.txt": "ccb530f90e914df84cbc8d19a71d30c79146d23a2e8e86e7a813d4d92a5a6a8b",
    "k38_dense_parent39.json": "72877e1101a4d33f96646f43d64a6688c3bb2baa56ada85df3c76017c4d14365",
    "k38_offset_witness.txt": "5aa1467c25cf81d6cd6c7b813719a378e4c35f105b1725e49b727dfcdec1c9d4",
    "k38_witness.json": "44ccacbe5d4b5a27f54c236e58c78629e02a5136c90db1e65bf7c32943b54a0e",
}
HEADS = (3, 0, -3)


def read(kdir, name):
    raw = open(os.path.join(kdir, name), "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA[name], f"{name}: sha256 mismatch"
    return raw


def span(gens):
    words = [0]
    for g in gens:
        words += [w ^ g for w in words]
    assert len(set(words)) == len(words), "generators not independent"
    return words


def echelon(gens):
    """Fully reduced echelon basis {pivot: vector} of the span of gens."""
    piv = {}
    for g in gens:
        for p, v in piv.items():
            if g >> p & 1:
                g ^= v
        if g:
            p = g.bit_length() - 1
            for q in list(piv):
                if piv[q] >> p & 1:
                    piv[q] ^= g
            piv[p] = g
    return piv


def solve(cols, s):
    """Some x (bit j = use column j) with XOR of the used columns == s."""
    basis = {}  # pivot -> (vector, combination)
    for j, c in enumerate(cols):
        comb = 1 << j
        for p in sorted(basis, reverse=True):
            if c >> p & 1:
                c ^= basis[p][0]
                comb ^= basis[p][1]
        if c:
            basis[c.bit_length() - 1] = (c, comb)
    x = 0
    for p in sorted(basis, reverse=True):
        if s >> p & 1:
            s ^= basis[p][0]
            x ^= basis[p][1]
    assert s == 0, "syndrome not reachable"
    return x


def build(kdir, variant=None):
    par = json.loads(read(kdir, "k38_dense_parent39.json"))
    gens = [int(h, 16) for h in par["generators_hex"]]
    assert par["length"] == 39 and len(gens) == 15 and all(0 < g < 2**39 for g in gens)
    V = span(gens)
    piv = echelon(gens)
    assert len(piv) == 15
    free = [i for i in range(39) if i not in piv]

    def syndrome(x):
        for p, v in piv.items():
            if x >> p & 1:
                x ^= v
        assert all(not x >> p & 1 for p in piv)
        return sum((x >> i & 1) << j for j, i in enumerate(free))

    assert all(syndrome(v) == 0 for v in gens)
    K = sorted(v >> 2 for v in V if v & 3 == 0)
    assert len(K) == 8192 and min(k.bit_count() for k in K if k) == 12
    cols = [syndrome(1 << (2 + j)) for j in range(37)]
    lines = read(kdir, "k38_offset_witness.txt").decode("ascii").split("\n")
    lines = [ln for ln in lines if ln.strip()]
    assert len(lines) == 3
    Kar = np.array(K, dtype=np.int64)
    bits = np.arange(37)
    dense = []
    nf = []
    for h, ln in zip(HEADS, lines):
        k, *ss = map(int, ln.split())
        assert k == len(ss) == len(set(ss)) and all(0 <= s < 2**24 for s in ss)
        nf.append(k)
        for s in ss:
            b = solve(cols, s)
            assert syndrome(b << 2) == s
            words = Kar ^ b
            blk = np.zeros((8192, D), dtype=np.int64)
            blk[:, 0] = h
            blk[:, 1:] = 2 - 4 * ((words[:, None] >> bits) & 1)
            dense.append(blk)
    assert nf == [11, 10, 10]
    dense = np.concatenate(dense)
    # octads
    rows = read(kdir, "k38_supports_3088.txt").decode("ascii").split("\n")
    rows = [r for r in rows if r]
    assert len(rows) == 3088 and all(len(r) == D and set(r) <= {"0", "1"} and r.count("1") == 8 for r in rows)
    sup = [tuple(i for i, ch in enumerate(r) if ch == "1") for r in rows]
    w = json.loads(read(kdir, "k38_witness.json"))
    reps = w["replacements"]
    assert len(reps) == 10 and len({r["i"] for r in reps}) == 10
    if variant == "unswitched":
        reps = []
    elif variant == "halfswitch":
        reps = reps[:6]
    for r in reps:
        assert sup[r["i"]] == tuple(r["remove"]), "replacement does not match parent"
        sup[r["i"]] = tuple(sorted(r["add"]))
    assert len(set(sup)) == 3088 and all(len(s) == 8 for s in sup)
    signs = np.array(list(itertools.product((2, -2), repeat=8)), dtype=np.int64)
    signs = signs[(signs < 0).sum(1) % 2 == 0]
    octs = np.zeros((3088 * 128, D), dtype=np.int64)
    for t, s in enumerate(sup):
        octs[t * 128:(t + 1) * 128, list(s)] = signs
    # stars
    leafpar = 0 if variant == "evenstars" else 1
    stars = []
    assert len(w["stars"]) == 18
    for centre, *leaves in w["stars"]:
        assert len(leaves) == 4 and len({centre, *leaves}) == 5 and all(0 <= x < D for x in (centre, *leaves))
        for a in (4, -4):
            for ls in itertools.product((2, -2), repeat=4):
                if sum(x < 0 for x in ls) % 2 != leafpar:
                    continue
                v = [0] * D
                v[centre] = a
                for j, x in zip(leaves, ls):
                    v[j] = x
                stars.append(v)
    stars = np.array(stars, dtype=np.int64)
    # roots not blocked by a star
    roots = []
    for i, j in itertools.combinations(range(D), 2):
        for a, b in itertools.product((4, -4), repeat=2):
            if (a * stars[:, i] + b * stars[:, j]).max() <= 16:
                v = [0] * D
                v[i], v[j] = a, b
                roots.append(v)
    roots = np.array(roots, dtype=np.int64)
    X = np.concatenate([dense, octs, stars, roots])
    nrm = (X * X).sum(1)
    nd = len(dense)
    assert (nrm[nd:] == 32).all() and set(nrm[:nd].tolist()) == {148, 157}
    assert len({r.tobytes() for r in X}) == len(X), "repeated rows"
    print(f"variant {variant}: dense {nd} (fibres {nf}) + octads {len(octs)} + stars {len(stars)}"
          f" + roots {len(roots)} (removed {2 * D * (D - 1) - len(roots)}) = {len(X)}")
    if variant is None:
        assert (len(X), len(stars), len(roots)) == (652076, 288, 2572)
    return X


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "evenstars", "unswitched", "halfswitch")
    X = build(a[1], var)
    X.astype(np.int8).tofile(a[2])
    print(f"-> {a[2]}")
