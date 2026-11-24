"""Rebuild the Qiushi 25D (197,580) and 27D (201,567) kissing configurations
from the authors' repository data, with our own code.

Source: Yang et al., arXiv:2609.35051v1, Sections "motion" (25D) and
"A two-layer configuration with 201567 points" (27D), and the files
constructions/d25/{construction.tex, baseline-heads.json, repair-points.json}
and constructions/d27/data/*.npy of
github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research at commit
39911e4b38c01c4631e06b12a3e0b23a84e403f8 (sha256-pinned in fetch_qiushi.py).
None of the authors' code is run or imported. The Leech shell is our own
(known.leech_min_scaled, same Golay generator polynomial as the authors').

The coordinates lie in Q(sqrt2, sqrt3). Each point is stored, up to a
positive scalar factor (which does not change angles), as four integer
vectors C0..C3 with  x = C0 + C1*sqrt2 + C2*sqrt3 + C3*sqrt6.
Output: TAG_bulk.i8, the pure-integer rows with int8 entries and squared
norm <= 32767 (raw int8, for kiss_check.c / kiss_check_np.py), and
TAG_field.json, the other rows as [C0, C1, C2, C3] lists of Python integers
(the 25D rational caps have entries near 7e18, so no fixed-width format).
The configuration is bulk + field; pairs involving a field row are checked
by kiss_check_field.py.

25D (paper normalisation: squared norm 4; we multiply by sqrt8, then by
small integers). n = g/sqrt48 with g the integer "extra_equator_lean".
  unchanged shell (z,0)                              bulk
  P0 = (-2n,0)            ~ (-g, 0)                  bulk
  poles (0,+-2)           ~ (0, +-1)                 bulk
  Q = (sqrt3 n, -1)       ~ (g, -4)                  bulk
  R- = 2l/sqrt(10209)     ~ l                        bulk
  R+ = 2k/sqrt(1007176)   ~ k                        field (entries > 127)
  moved (w,0) -> (r+an, b), w.g = 24 (w in the 32-scale):
     12*sqrt8*(r+an, b) = (12w - 6g + (3sqrt2 + sqrt3) g, 12sqrt3 - 12sqrt2)
  class cap (u + t v, +-sqrt8), t = (3-sqrt3)/6, times 6:
     (6u + 3v - sqrt3 v, +-12 sqrt2)
  rational cap (q, +-sqrt8) with q = num/den:  (num, +-2 den sqrt2)
  caps (x_984, +1) and (x_1008, -1) are replaced by R+ and R-.
27D (paper normalisation: squared norm 32):
  shell (z,0,0,0) for z not an owner                 bulk
  first-layer cap 3*(y/3, 4v/sqrt3) = (y, 4sqrt3 v), v in the triple of y
  second-layer cap 2*(sqrt3 u/2, +-sqrt8 e_l) = (sqrt3 u, +-4 sqrt2 e_l)
  pure tail (0, 4Rv), v in V = {+-e_i +- e_j}, R = rotation by 45 deg
     4R v = (2sqrt2 (v0 - v1), 2sqrt2 (v0 + v1), 4 v2)

Usage: python3 -I build_qiushi2527.py SRCDIR OUTDIR [--variant NAME]
SRCDIR holds baseline-heads.json, repair-points.json, heads27_*.npy.
Variants (negative controls, each must FAIL the check):
  25: q25_extra   adds (sqrt3 n, +1), the mirror image of Q;
      q25_norepair keeps the two old caps instead of R+ and R-;
  27: q27_owner   puts back the equatorial point of one second-layer owner;
      q27_label   relabels one second-layer owner onto the line of an owner
                  with u.u' = 16.
"""
import json
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import known  # noqa: E402


def shell():
    M = np.array(known.leech_min_scaled(), dtype=np.int64)
    assert M.shape == (196560, 24) and np.all((M * M).sum(1) == 32)
    return M


def row(d, c0=None, c1=None, c2=None, c3=None):
    r = np.zeros((4, d), dtype=object)
    for k, c in enumerate((c0, c1, c2, c3)):
        if c is not None:
            r[k] = [int(x) for x in c]
    return r


def finish(bulk, field, d, out, tag, claimed):
    bulk = np.array(bulk, dtype=np.int64).reshape(-1, d)
    assert np.abs(bulk).max() <= 127 and (bulk * bulk).sum(1).max() <= 32767
    nS = len(bulk)
    rows = [[[int(x) for x in comp] for comp in r] for r in field]
    assert all(len(r) == 4 and all(len(c) == d for c in r) for r in rows)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f"{tag}_field.json"), "w") as f:
        json.dump({"d": d, "basis": ["1", "sqrt2", "sqrt3", "sqrt6"], "rows": rows}, f)
    bulk.astype(np.int8).tofile(os.path.join(out, f"{tag}_bulk.i8"))
    total = nS + len(rows)
    print(f"{tag}: d={d} points={total} (bulk {nS}, field {len(rows)}), claimed {claimed}"
          f" -> {'count OK' if total == claimed else 'COUNT DIFFERS'}")
    return total


def build25(src, out, variant=None):
    data = json.load(open(os.path.join(src, "baseline-heads.json")))
    rep = json.load(open(os.path.join(src, "repair-points.json")))["points"]
    M = shell()
    pos = {tuple(r): i for i, r in enumerate(M.tolist())}
    heads = data["heads"]
    assert len(heads) == 1016 and [h["index"] for h in heads] == list(range(1016))
    owners = [pos[tuple(h["owner"])] for h in heads]          # KeyError if not in shell
    assert len(set(owners)) == 1016
    g = np.array(data["extra_equator_lean"], dtype=np.int64)
    assert g @ g == 48
    D = set(owners)
    keep = [i for i in range(196560) if i not in D]
    gz = M @ g
    moved = [i for i in keep if gz[i] == 24]
    assert len(moved) == 552
    # construction.tex: U = {u : u.v = -3} (32-scale: u.g = -24) lies in D and w = u + g
    U = np.flatnonzero(gz == -24)
    assert len(U) == 552 and set(U.tolist()) <= D
    assert {pos[tuple((M[u] + g).tolist())] for u in U} == set(moved)
    mset = set(moved)
    bulk = [list(M[i]) + [0] for i in keep if i not in mset]
    bulk.append(list(-g) + [0])                     # P0
    bulk.append([0] * 24 + [1])                     # N
    bulk.append([0] * 24 + [-1])                    # S
    bulk.append(list(g) + [-4])                     # Q
    k = np.array(rep["upper"]["integer_vector"], dtype=np.int64)
    l = np.array(rep["lower"]["integer_vector"], dtype=np.int64)
    assert k @ k == rep["upper"]["squared_norm"] == 1007176
    assert l @ l == rep["lower"]["squared_norm"] == 10209
    field = []
    for i in moved:
        w = M[i]
        field.append(row(25, list(12 * w - 6 * g) + [0], list(3 * g) + [-12], list(g) + [12]))
    replaced = {(984, 1), (1008, -1)} if variant != "q25_norepair" else set()
    for s in (1, -1):
        for h in heads:
            if (h["index"], s) in replaced:
                continue
            u = np.array(h["owner"], dtype=np.int64)
            if h["kind"] == "class":
                v = np.array(h["lean"], dtype=np.int64)
                field.append(row(25, list(6 * u + 3 * v) + [0], [0] * 24 + [12 * s], list(-v) + [0]))
            else:
                q = [Fraction(c) for c in h["coordinates"]]
                den = 1
                for c in q:
                    den = _lcm(den, c.denominator)
                num = [int(c * den) for c in q]
                assert sum(x * x for x in num) == 24 * den * den
                field.append(row(25, num + [0], [0] * 24 + [2 * den * s]))
    if replaced:
        bulk.append(list(l))                        # R-
        field.append(row(25, list(k)))              # R+
    if variant == "q25_extra":
        field.append(row(25, list(g) + [4]))        # (sqrt3 n, +1)
    tag = "qiushi25" if variant is None else variant
    return finish(bulk, field, 25, out, tag, 197580)


def _lcm(a, b):
    from math import gcd
    return a * b // gcd(a, b)


TRIPLES = [[(1, 1, 0), (-1, 0, -1), (0, -1, 1)],
           [(1, -1, 0), (-1, 0, 1), (0, 1, -1)],
           [(-1, -1, 0), (1, 0, -1), (0, 1, 1)],
           [(-1, 1, 0), (1, 0, 1), (0, -1, -1)]]


def build27(src, out, variant=None):
    Y = np.load(os.path.join(src, "heads27_Y.npy"), allow_pickle=False).astype(np.int64)
    side = np.load(os.path.join(src, "heads27_side.npy"), allow_pickle=False).astype(np.int64)
    Uo = np.load(os.path.join(src, "heads27_layer2_u.npy"), allow_pickle=False).astype(np.int64)
    line = np.load(os.path.join(src, "heads27_layer2_line.npy"), allow_pickle=False).astype(np.int64)
    assert Y.shape == (2258, 24) and side.shape == (2258,) and Uo.shape == (311, 24) and line.shape == (311,)
    assert set(side.tolist()) <= {0, 1, 2, 3} and set(line.tolist()) <= {0, 1, 2}
    assert np.all((Y * Y).sum(1) == 192) and np.all((Uo * Uo).sum(1) == 32)
    M = shell()
    pos = {tuple(r): i for i, r in enumerate(M.tolist())}
    P = Y @ M.T
    hits = [np.flatnonzero(r > 48) for r in P]
    assert all(len(h) <= 1 for h in hits)
    first = [int(h[0]) for h in hits if len(h)]
    assert len(first) == len(set(first)) == 2090
    second = [pos[tuple(u)] for u in Uo.tolist()]
    assert len(set(second)) == 311 and not set(second) & set(first)
    gone = set(first) | set(second)
    if variant == "q27_owner":
        gone.discard(second[0])
    bulk = [list(M[i]) + [0, 0, 0] for i in range(196560) if i not in gone]
    lab = line.copy()
    if variant == "q27_label":
        UU = Uo @ Uo.T
        i, j = [int(x) for x in np.argwhere((UU == 16) & (line[:, None] != line[None, :]))[0]]
        lab[i] = line[j]
        print(f"q27_label: owner {i} moved to line {line[j]} (u.u' = 16 with owner {j})")
    field = []
    for y, s in zip(Y, side):
        for v in TRIPLES[s]:
            field.append(row(27, list(y) + [0, 0, 0], None, [0] * 24 + [4 * c for c in v]))
    for u, l in zip(Uo, lab):
        for e in (1, -1):
            t = [0, 0, 0]
            t[l] = 4 * e
            field.append(row(27, None, [0] * 24 + t, list(u) + [0, 0, 0]))
    V = [tuple(v) for v in {(a, b, 0) for a in (1, -1) for b in (1, -1)}
         | {(a, 0, b) for a in (1, -1) for b in (1, -1)} | {(0, a, b) for a in (1, -1) for b in (1, -1)}]
    assert len(V) == 12
    for v in sorted(V):
        field.append(row(27, [0] * 24 + [0, 0, 4 * v[2]], [0] * 24 + [2 * (v[0] - v[1]), 2 * (v[0] + v[1]), 0]))
    tag = "qiushi27" if variant is None else variant
    return finish(bulk, field, 27, out, tag, 201567)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    var = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else None
    if var is None:
        build25(src, out)
        build27(src, out)
    elif var.startswith("q25"):
        build25(src, out, var)
    else:
        build27(src, out, var)
