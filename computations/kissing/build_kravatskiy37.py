"""Rebuild A. Kravatskiy's 544,666-point kissing configuration in R^37
(repository alexlegeartis/KissingNumbers @ 907f9b1f, package
verifications/improved/dim37-qr-flat-repack) with our own code. Untrusted
data: only JSON and text are parsed; none of the repository's code is run.

Chain (read from the package's README and files; its verify*.py and
supports37.py read, not run). Coordinates 0..35 are "ordinary", 36 is the
marked axis.
  533,864 (QR compression, verify37.py): dense_parent38.json, 14 generators
      and 11 representatives (hex, 38 bits) of Yang et al.'s length-38 code
      (arXiv:2609.35051v1, App. B). A codeword x gives the dense point with
      2(-1)^(bit 2+j of x) at ordinary coordinate j and geometry[x & 3] at
      coordinate 36, geometry = [4, 1, -4, -1] (the two-bit word b0 + 2 b1);
      squared norm 145 or 160. 16,384 x 11 = 180,224 points.
      Middle layer: Brouwer's 2,742 weight-8 supports on the 36 ordinary
      coordinates (a36.8.8.2742H), regenerated as in supports37.py from 8
      seeds under the diagonal PSL(2,11) action on three projective lines
      plus 3 extra masks; we regenerate them with our own code and compare
      with the published hash of the sorted list (ORDER_SHA). All 128
      even-sign +-2 patterns per support. All 2 * 37 * 36 roots +-4 +-4.
  544,474 (radical layer, verify_predecessor.py): remove the 144 roots that
      use coordinate 36; add, for each of the 168 six-supports in six.txt,
      +-2 on the support with an even number of minus signs and +-2 sqrt2 at
      coordinate 36 (64 points each, squared norm 32), and the poles +-e_36.
  544,666 (this package): delete the three supports inside U = 12..23 (384
      points) and add 576 points from win.txt: line 1 is a basis of a group
      G of 12-bit sign masks (|G| = 256); each further line "mask neg n"
      gives the points +-2 on coordinates 12 + k (bit k of mask), with minus
      exactly at the bits of neg ^ (g & mask), g in G (n distinct points).
Mask conventions: bit j of a 36-bit support = ordinary coordinate j; bit k of
a 12-bit flat mask = coordinate 12 + k (the 3 deleted supports are exactly
the three supports inside U, as the package asserts). The dense placement
(bits 2.. -> coordinates 0..35) is ours: dense x dense products depend only
on Hamming distances, and the other dense pairs are bounded by magnitudes.

Outputs: OUT.i8 (533,914 integer rows x 37) and OUT_field.json (the 10,752
radical rows C0 + C1 sqrt2 for kiss_check_field.py).
Usage: python3 -I build_kravatskiy37.py KRAVDIR OUT [--variant NAME]
  negative controls (must FAIL): keepflat (the 576 new points added without
  deleting the 3 old supports in U, i.e. applied to the wrong parent),
  geometry (tail map [4, -1, -4, 1] instead of [4, 1, -4, -1]).
"""
import hashlib
import itertools
import json
import os
import sys
from collections import deque

import numpy as np

D = 37
SHA = {
    "k37_dense_parent38.json": "addcc62d2757f68c31fda2af630e1f41a46948c58d42a24d981e2b8291336108",
    "k37_six.txt": "f8f9fbe495ae1696b8b1d4f34ad0f001a066390d7886d2cd360ca8bb75122f39",
    "k37_win.txt": "956a00ddc257713eabaff9f05d14e0f050d87591d317eba2cbb6db3cedb1d532",
}
# supports37.py: orbit seeds with orbit sizes, the 3 extra masks, and the
# sha256 of the sorted list written as 9-digit upper-case hex lines
SEEDS = ((0x0000035B1, 132), (0x000027E10, 165), (0x003024115, 660), (0x003115404, 660),
         (0x00F081104, 660), (0x0270001C8, 165), (0x0271C8000, 165), (0x07D101000, 132))
EXTRAS = (0x0000FF000, 0x000FF0000, 0x000F0F000)
ORDER_SHA = "75de16ebd0f473d39d851a6daf367b3e0ea00478984513f9ccc68ef7de5405fa"


def read(kdir, name):
    raw = open(os.path.join(kdir, name), "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA[name], f"{name}: sha256 mismatch"
    return raw.decode("ascii")


def brouwer2742():
    """Weight-8 supports on 3 x 12 positions: orbits of 8 seeds under PSL(2,11)
    acting diagonally on three copies of the projective line P^1(F_11).
    Position p (0..11) of a block holds the label lab[p]: labels 0..9 at
    positions 0..9, label 10 at position 11, infinity at position 10."""
    INF = 11
    lab = list(range(10)) + [INF, 10]
    at = {l: p for p, l in enumerate(lab)}

    def act(f):
        img = [at[f(lab[p])] for p in range(12)]
        return [img[i % 12] + 12 * (i // 12) for i in range(36)]

    trans = act(lambda x: INF if x == INF else (x + 1) % 11)
    inv = act(lambda x: INF if x == 0 else 0 if x == INF else (-pow(x, -1, 11)) % 11)
    gens = [trans, inv]
    out = set()
    for seed, size in SEEDS:
        orb, todo = {seed}, deque([seed])
        while todo:
            x = todo.popleft()
            for g in gens:
                y = sum(1 << g[i] for i in range(36) if x >> i & 1)
                if y not in orb:
                    orb.add(y)
                    todo.append(y)
        assert len(orb) == size and not orb & out
        out |= orb
    assert len(out) == 2739 and not out & set(EXTRAS)
    res = sorted(out | set(EXTRAS))
    assert hashlib.sha256("".join(f"{x:09X}\n" for x in res).encode()).hexdigest() == ORDER_SHA, \
        "regenerated supports differ from the published list"
    return res


def even_signs(k, mag=2):
    s = np.array(list(itertools.product((mag, -mag), repeat=k)), dtype=np.int64)
    return s[(s < 0).sum(1) % 2 == 0]


def build(kdir, variant=None):
    par = json.loads(read(kdir, "k37_dense_parent38.json"))
    gens = [int(x, 16) for x in par["generators_hex"]]
    reps = [int(x, 16) for x in par["representatives_hex"]]
    assert par["length"] == 38 and len(gens) == 14 and len(reps) == 11
    Hk = [0]
    for g in gens:
        Hk += [h ^ g for h in Hk]
    assert len(set(Hk)) == 16384 and min(h.bit_count() for h in Hk if h) == 12
    words = np.array(sorted({h ^ r for r in reps for h in Hk}), dtype=np.int64)
    assert len(words) == 180224
    geometry = [4, -1, -4, 1] if variant == "geometry" else [4, 1, -4, -1]
    dense = np.zeros((len(words), D), dtype=np.int64)
    dense[:, :36] = 2 - 4 * ((words[:, None] >> (2 + np.arange(36))) & 1)
    dense[:, 36] = np.array(geometry)[words & 3]
    # middle layer
    sup = brouwer2742()
    u = ((1 << 12) - 1) << 12
    inside = [s for s in sup if s & u == s]
    assert [s >> 12 for s in inside] == [255, 3855, 4080]
    if variant != "keepflat":
        sup = [s for s in sup if s & u != s]
    ev8 = even_signs(8)
    mid = np.zeros((len(sup) * 128, D), dtype=np.int64)
    for t, s in enumerate(sup):
        mid[t * 128:(t + 1) * 128, [j for j in range(36) if s >> j & 1]] = ev8
    roots = []
    for i, j in itertools.combinations(range(36), 2):
        for a, b in itertools.product((4, -4), repeat=2):
            v = [0] * D
            v[i], v[j] = a, b
            roots.append(v)
    poles = [[0] * 36 + [1], [0] * 36 + [-1]]
    # flat refill
    lines = [list(map(int, ln.split())) for ln in read(kdir, "k37_win.txt").split("\n") if ln.strip()]
    G = {0}
    for b in lines[0]:
        assert 0 < b < 4096
        G |= {x ^ b for x in G}
    assert len(G) == 256
    flat = set()
    for m, neg, n in lines[1:]:
        assert m.bit_count() == 8 and neg & m == neg
        pts = {(m, neg ^ (g & m)) for g in G}
        assert len(pts) == n and not pts & flat
        flat |= pts
    assert len(flat) == 576
    fl = []
    for m, neg in sorted(flat):
        v = [0] * D
        for k in range(12):
            if m >> k & 1:
                v[12 + k] = -2 if neg >> k & 1 else 2
        fl.append(v)
    X = np.concatenate([dense, mid, np.array(roots + poles + fl, dtype=np.int64)])
    # radical layer: C0 on the six-support, C1 = +-2 at coordinate 36
    six = [int(x) for x in read(kdir, "k37_six.txt").split()]
    assert len(six) == len(set(six)) == 168 and all(m.bit_count() == 6 and m < 2**36 for m in six)
    ev6 = even_signs(6)
    field = []
    for m in six:
        cs = [j for j in range(36) if m >> j & 1]
        for sg in ev6:
            c0 = [0] * D
            for j, x in zip(cs, sg):
                c0[j] = int(x)
            for e in (2, -2):
                c1 = [0] * D
                c1[36] = e
                field.append([c0, c1, [0] * D, [0] * D])
    nrm = (X * X).sum(1)
    assert set(nrm.tolist()) == {1, 32, 145, 160}
    assert len({r.tobytes() for r in X}) == len(X), "repeated rows"
    n = len(X) + len(field)
    print(f"variant {variant}: dense {len(dense)} + middle {len(mid)} ({len(sup)} supports) + roots {len(roots)}"
          f" + poles 2 + flat {len(fl)} + radical {len(field)} = {n}")
    if variant is None:
        assert n == 544666
    return X, field


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "keepflat", "geometry")
    X, field = build(a[1], var)
    X.astype(np.int8).tofile(a[2] + ".i8")
    json.dump({"d": D, "rows": field}, open(a[2] + "_field.json", "w"))
    print(f"-> {a[2]}.i8 ({len(X)} rows), {a[2]}_field.json ({len(field)} rows)")
