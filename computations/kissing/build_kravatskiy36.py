"""Rebuild A. Kravatskiy's 506,628-point kissing configuration in R^36 (three
orthogonal copies of the Coxeter-Todd lattice K12) from its chain of edits
(repository alexlegeartis/KissingNumbers @ 907f9b1f, verifications/improved/),
with our own code. Untrusted data: only JSON is parsed; none of the
repository's code is run (its verify*.py were read to learn the formats).

Chain (each file pins its parent by sha256, checked here):
  dim36-ct-nonlocal/certificate.json (502,821): gram_12 (Gram matrix Q of
      K12, minimum 4), sublattice_matrix M (M Q M^T = 3Q; phi = I - M has
      order 3 and preserves Q), label_first/label_second (6 coordinate pairs
      giving a vector v the label sum_k ((v_a_k + v_b_k) mod 3) 3^k, so 729
      cosets of M K12), outer_cosets (5,100 label triples "cells").
  -> dim36-ct-triangle-refill/certificate.json (502,902): removed_points and
      added_points (root triples [l0, l1, l2, p0, p1, p2]) and
      switched_triangles ([cell, norm-8 vector]).
  -> dim36-ct-double-trine/witness.json (502,929): remove_rows (root
      triples) and insert_full_triples (cells taking all 27 phase triples).
  -> dim36-ct-neutral-reheat/witness.json (506,628): add ([l0, l1, l2,
      27-bit phase mask]), remove_root (root triples), remove_base ([cell, j,
      3-bit phase mask]), restore_base ([cell, j, block, label, 3-bit mask]).
Geometry (as in the packages; points are triples (x0, x1, x2) of K12 vectors
in the lattice basis, inner product sum_b x_b Q y_b^T, squared norm 12):
  shells: all v in Z^12 with v Q v^T <= 8 (our own Fincke-Pohst enumeration;
      the counts 756, 4032, 20412 of norms 4, 6, 8 are the K12 theta series),
      in the author's enumeration order, which is ascending in
      (v_11, v_10, ..., v_0); the minimal vectors S[l] of each label keep that
      order (indices j refer to it). Labels of minimum 4 have 3 minimal
      vectors s, s phi, s phi^2 with s the first; phase p means s phi^p.
  axial: the 756 norm-4 vectors times M (norm 12), in each block: 2,268.
  cells of minima {0,6,6}: all products of the minimal vectors.
  cells of minima {0,4,8}: for each norm-8 minimal vector v (index j) of the
      large block, the three phases of the small block's root next to v, or,
      if (cell, v) is switched, the phases of the negated label (label digits
      negated mod 3) in the empty block. ids (cell, j, phase).
  root triples: cells of minima {4,4,4} with all 27 phase triples, edited by
      the chain above.
  restore_base [cell, j, c, l, mask]: v_j in the large block, phases of label
      l in block c.
Outputs: OUT_x.i8 (rows x, 36 lattice coordinates) and OUT_xg.i8 (rows
x (I3 kron Q)), for the Gram (partner) mode of kiss_check.c and
kiss_check_np.py: the inner product of points i, j is x_i . (x_j G).
Usage: python3 -I build_kravatskiy36.py KRAVDIR OUT [--variant NAME]
  negative controls (must FAIL): noremove (the final added triples without
  the declared root removals), stale (final edits applied to the 502,902
  stage, skipping the double-trine step), phase (first minimal vector
  replaced by the second as phase 0, i.e. a wrong phase origin).
"""
import hashlib
import itertools
import json
import math
import os
import sys
from fractions import Fraction

import numpy as np

SHA = {
    "k36_nonlocal.json": "c4598a0dfc49365ae2b082745454c38b53b76703e5eef5dafbd71e2d06c59180",
    "k36_triangle.json": "8ef795fd0b034e913e28c05b36f43c80cf274f78dd2af2bb8a07b1488bc8c306",
    "k36_double.json": "ad81a8abdfb10889b7f7826b5f4823fa355f415e7cca4083d092167faed13b08",
    "k36_final.json": "5327877dfd99b826787391c9ecdb76db9f58747ae693f8540ef03f0b3b678c93",
}


def read(kdir, name):
    raw = open(os.path.join(kdir, name), "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA[name], f"{name}: sha256 mismatch"
    return json.loads(raw)


def short_vectors(Q, bound):
    """All v != 0 in Z^n with v Q v^T <= bound (exact, Fractions)."""
    n = len(Q)
    # Q = L D L^T with L unit lower triangular: v Q v^T = sum_k D_k (v_k + sum_{i>k} L_ik v_i)^2
    L = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    D = [Fraction(0)] * n
    for j in range(n):
        D[j] = Q[j][j] - sum(L[j][k] ** 2 * D[k] for k in range(j))
        assert D[j] > 0
        for i in range(j + 1, n):
            L[i][j] = (Q[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j))) / D[j]
    out = []
    v = [0] * n

    def rec(k, rem):
        if k < 0:
            if any(v):
                out.append(tuple(v))
            return
        c = sum((L[i][k] * v[i] for i in range(k + 1, n)), Fraction(0))
        r = math.isqrt(int(rem / D[k])) + 2
        z0 = math.floor(-c)
        for z in range(z0 - r, z0 + r + 2):
            cost = D[k] * (z + c) ** 2
            if cost <= rem:
                v[k] = z
                rec(k - 1, rem - cost)
        v[k] = 0

    rec(n - 1, Fraction(bound))
    return out


def build(kdir, variant=None):
    nl = read(kdir, "k36_nonlocal.json")
    tr = read(kdir, "k36_triangle.json")
    db = read(kdir, "k36_double.json")
    fw = read(kdir, "k36_final.json")
    assert tr["source_sha256"] == SHA["k36_nonlocal.json"]
    assert fw["SHA256"]["triangle/certificate.json"] == SHA["k36_triangle.json"]
    assert fw["SHA256"]["double/witness.json"] == SHA["k36_double.json"]
    Q = np.array(nl["gram_12"], dtype=np.int64)
    M = np.array(nl["sublattice_matrix"], dtype=np.int64)
    assert (Q == Q.T).all() and (M @ Q @ M.T == 3 * Q).all()
    phi = np.eye(12, dtype=np.int64) - M
    assert (phi @ Q @ phi.T == Q).all() and (phi @ phi @ phi == np.eye(12, dtype=np.int64)).all()
    fa, fb = nl["label_first"], nl["label_second"]
    assert sorted(fa + fb) == list(range(12)) and ((M[:, fa] + M[:, fb]) % 3 == 0).all()
    sv = short_vectors(Q.tolist(), 8)
    sv.sort(key=lambda v: v[::-1])
    V = np.array(sv, dtype=np.int64)
    nv = ((V @ Q) * V).sum(1)
    assert {k: int((nv == k).sum()) for k in (4, 6, 8)} == {4: 756, 6: 4032, 8: 20412} and len(V) == 25200
    V = np.concatenate([V, np.zeros((1, 12), dtype=np.int64)])
    nv = np.append(nv, 0)
    pw = 3 ** np.arange(6)
    lab = ((V[:, fa] + V[:, fb]) % 3) @ pw
    N0 = np.full(729, 99, dtype=np.int64)
    np.minimum.at(N0, lab, nv)
    S = [V[(lab == k) & (nv == N0[k])] for k in range(729)]
    from collections import Counter
    assert Counter(zip(N0.tolist(), map(len, S))) == {(0, 1): 1, (4, 3): 252, (6, 18): 224, (8, 81): 252}
    T = {}
    for k in np.flatnonzero(N0 == 4):
        s0 = S[k][1] if variant == "phase" else S[k][0]
        T[int(k)] = np.array([s0, s0 @ phi, s0 @ phi @ phi])
        assert {tuple(x) for x in T[int(k)]} == {tuple(x) for x in S[k]}

    def neg(n):
        return sum(((-(n // 3 ** j)) % 3) * 3 ** j for j in range(6))

    cells = nl["outer_cosets"]
    assert len(cells) == 5100 and cells[0] == [0, 0, 0] and len({tuple(c) for c in cells}) == 5100
    z = np.zeros(12, dtype=np.int64)
    # base layer with ids
    ax = V[nv == 4] @ M
    base, ids = [], []
    for b in range(3):
        for v in ax:
            row = [z, z, z]
            row[b] = v
            base.append(np.concatenate(row))
            ids.append(None)
    moved = {(a, tuple(v)) for a, v in tr["switched_triangles"]}
    for i, c in enumerate(cells[1:], 1):
        q = [int(N0[k]) for k in c]
        if q == [4, 4, 4]:
            continue
        if sorted(q) == [0, 6, 6]:
            for t in itertools.product(*(S[k] for k in c)):
                base.append(np.concatenate(t))
                ids.append(None)
            continue
        assert sorted(q) == [0, 4, 8]
        a, h, e = q.index(4), q.index(8), q.index(0)
        for j, v in enumerate(S[c[h]]):
            blk, tag = (e, neg(c[a])) if (i, tuple(v)) in moved else (a, c[a])
            for ph in range(3):
                row = [z, z, z]
                row[blk] = T[tag][ph]
                row[h] = v
                base.append(np.concatenate(row))
                ids.append((i, j, ph))
    assert len(base) == 403704
    # root triples through the chain
    rt = {tuple(c) + p for c in cells if [int(N0[k]) for k in c] == [4, 4, 4]
          for p in itertools.product(range(3), repeat=3)}
    assert len(rt) == 99117
    rem, add = {tuple(r) for r in tr["removed_points"]}, {tuple(r) for r in tr["added_points"]}
    assert rem <= rt and not add & rt and len(rem) == 1309 and len(add) == 1390
    rt = (rt - rem) | add
    assert len(rt) + len(base) == 502902
    if variant != "stale":
        rem = {tuple(r) for r in db["remove_rows"]}
        add = {tuple(c) + p for c in db["insert_full_triples"] for p in itertools.product(range(3), repeat=3)}
        assert rem <= rt and not add & rt
        rt = (rt - rem) | add
        assert len(rt) == 99225
    # final witness
    rd = {tuple(r) for r in fw["remove_root"]}
    assert len(rd) == len(fw["remove_root"]) == 7496
    if variant != "stale":
        assert rd <= rt
    if variant == "noremove":
        rd = set()
    ad = set()
    for a, b, c, m in fw["add"]:
        assert 0 < m < 2**27
        ad |= {(a, b, c, x % 3, x // 3 % 3, x // 9) for x in range(27) if m >> x & 1}
    assert not ad & rt or variant == "stale"
    roots = sorted((rt - rd) | ad)
    ix = {v: i for i, v in enumerate(ids) if v is not None}
    keep = np.ones(len(base), dtype=bool)
    for a, j, m in fw["remove_base"]:
        assert 0 < m < 8
        for ph in range(3):
            if m >> ph & 1:
                assert keep[ix[a, j, ph]]
                keep[ix[a, j, ph]] = False
    rest = []
    for a, j, c, l, m in fw["restore_base"]:
        q = [int(N0[k]) for k in cells[a]]
        g = q.index(8)
        assert sorted(q) == [0, 4, 8] and c != g and int(N0[l]) == 4 and 0 < m < 8
        assert all(not keep[ix[a, j, ph]] for ph in range(3))
        for ph in range(3):
            if m >> ph & 1:
                row = [z, z, z]
                row[g] = S[cells[a][g]][j]
                row[c] = T[l][ph]
                rest.append(np.concatenate(row))
    X = np.concatenate([np.array(base)[keep],
                        np.array([np.concatenate([T[k][p] for k, p in zip(r[:3], r[3:])]) for r in roots]),
                        np.array(rest)])
    G = np.kron(np.eye(3, dtype=np.int64), Q)
    XG = X @ G
    nrm = (X * XG).sum(1)
    assert (nrm == 12).all()
    print(f"variant {variant}: base {int(keep.sum())} (of {len(base)}) + root triples {len(roots)}"
          f" + restored {len(rest)} = {len(X)}")
    if variant is None:
        assert len(X) == fw["points"] == 506628
        assert len({r.tobytes() for r in X}) == len(X)
    assert np.abs(X).max() <= 127 and np.abs(XG).max() <= 127
    return X, XG


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "noremove", "stale", "phase")
    X, XG = build(a[1], var)
    X.astype(np.int8).tofile(a[2] + "_x.i8")
    XG.astype(np.int8).tofile(a[2] + "_xg.i8")
    print(f"-> {a[2]}_x.i8, {a[2]}_xg.i8 ({len(X)} rows x 36)")
