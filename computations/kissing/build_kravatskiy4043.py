"""Rebuild A. Kravatskiy's 40-43D kissing configurations (1,126,365;
1,460,066; 1,991,475; 2,921,073 points) from the affine-shell data in
alexlegeartis/KissingNumbers @ 907f9b1f (verifications/improved/), with our
own code: our own shell enumerator (enum_affine.c), our own class table.
Untrusted data: only JSON and .npz (allow_pickle=False) are parsed; none of
the repository's code is run (its verify.py / final.py were read to learn
the formats).

Format (as in the packages' READMEs and verifiers):
  40D, dim40-p48q-affine-refill: gram.json, a 40 x 40 integer Gram matrix G
      (rank-40 complement of sqrt(3) E8 in P48q); certificate.json, the
      core residue c in {0,1,2}^40 and the layer counts; points.npz, the
      explicit layers norm36 (40,653 rows), norm30 (1,122) and norm6 (0),
      int8 lattice coordinates. Points: the core {x in Z^40 : x == c
      (mod 3), x G x^T = 54} (1,084,590, enumerated here) and the explicit
      rows; inner product x G y^T. Squared norms 54, 36, 30.
  41-43D, dim41-43-affine-sections/configuration_{41,42,43}.npz: gram G
      (41, 42: the same P48q complement as 40D; 43: a P48p complement);
      per family i: residue c_i, radius r_i in {10,...,18}, head z_i
      (integer, width 8 or 3) and population (shell size); a common head
      denominator D; tiny_bodies (43D: 3,165 rows with x G x^T = 30) with
      tiny_heads over tiny_denominator E; pure head directions p.
      A family is every x == c_i (mod 3) with x G x^T = 3 r_i, each paired
      with the head z_i / D; with body metric G/3 the point is (x, z_i/D),
      of squared norm N_i / D^2, N_i = r_i D^2 + |z_i|^2. A tiny point is
      (x, h/E) with r = 10; a pure point is (0, p) (r = 0, D = 1).
      The body spans R^40 (G positive definite, checked exactly) and the
      heads span a space of rank n - 40 (checked exactly), so the points
      lie in R^n.
Exact criterion (class mode). For points of classes a, b with body product
  t = x G y^T (an integer), the scaled inner product is
  s = 6 D_a D_b <v, v'> = 2 D_a D_b t + 6 z_a.z_b, and the pair passes iff
  s <= sqrt(9 N_a N_b), i.e. (s integer) iff
      t <= T(a, b) = floor((isqrt(9 N_a N_b) - 6 z_a.z_b) / (2 D_a D_b)).
  It is an exact contact iff 9 N_a N_b is a square Q^2 and s = Q. The table
  is computed and checked (T passes, T + 1 fails, by s <= 0 or s^2 <= 9NM)
  in Python integers. The checkers evaluate t exactly for every pair
  (partner mode: rows x and x G).

Outputs: OUT_x.i8, OUT_xg.i8 (partner rows), and for 41-43 OUT.lab (uint8,
or uint16 little-endian when there are more than 256 classes) and OUT.tab;
OUT_meta.json (counts, classes).
Usage: python3 -I build_kravatskiy4043.py KRAVDIR DIM OUT ENUM_BIN [--variant NAME]
  negative controls (must FAIL): 40D negcore (core on the residue -c, the
  wrong centre); 41-43D shift (the head list shifted by one family, wrong
  order), purenegate (pure heads negated); 43D tinyscale (tiny heads read
  over the family denominator D instead of E); 43D p48q (the 43D families
  enumerated in the 41/42D P48q gram, the wrong parent lattice; rejected by
  the population count).
"""
import hashlib
import json
import math
import os
import subprocess
import sys
from fractions import Fraction

import numpy as np

SHA = {
    "k40_certificate.json": "d0a2cf0f78426227d6f425f00417171be6f26f9b7cbb9c5cba89ef5938e5dce4",
    "k40_gram.json": "39fed03448ab268281fe3adca9b034ddab65517043e0c9c719dc3774fa611878",
    "k40_points.npz": "dfe4e78c885cbffde6f6c0c030d86f9c79d9b1f8e4353d97c183d4649b9f1a26",
    "k41_configuration.npz": "1a63c971f8357d81236e07dbc6c4d70e4b0ec03ada0e3b8aa9811bc08a6daaf8",
    "k42_configuration.npz": "3aefb185461e52af9de83eace3b44b7f2f11171ada39da821a2fcb55b4a85713",
    "k43_configuration.npz": "bea1c397aa6b69c47f786564e402423bc892f5966e4e9899808b6598f2669870",
}
CLAIM = {40: 1126365, 41: 1460066, 42: 1991475, 43: 2921073}
BMAX = 54  # every body squared norm x G x^T is <= 54, so |t| <= 54


def path(kdir, name):
    p = os.path.join(kdir, name)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    assert h == SHA[name], f"{name}: sha256 mismatch"
    return p


def positive_definite(G):
    """Exact: all pivots of the symmetric Gaussian elimination are > 0."""
    A = [[Fraction(int(v)) for v in row] for row in G]
    n = len(A)
    for k in range(n):
        if A[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            if f:
                for j in range(k, n):
                    A[i][j] -= f * A[k][j]
    return True


def rank(rows):
    A = [[Fraction(int(v)) for v in r] for r in rows]
    rk, cols = 0, len(A[0]) if A else 0
    for c in range(cols):
        piv = next((i for i in range(rk, len(A)) if A[i][c]), None)
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        for i in range(len(A)):
            if i != rk and A[i][c]:
                f = A[i][c] / A[rk][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk


def shell(G, c, n, enum_bin, work, cache):
    """All x == c (mod 3) with x G x^T == n, sorted, via enum_affine."""
    key = (tuple(int(v) for v in c), int(n))
    if key in cache:
        return cache[key]
    inp, out = os.path.join(work, "enum.in"), os.path.join(work, "enum.i8")
    with open(inp, "w") as f:
        f.write(f"40 {int(n)}\n" + "\n".join(" ".join(map(str, map(int, r))) for r in G)
                + "\n" + " ".join(map(str, key[0])) + "\n")
    cnt = int(subprocess.run([enum_bin, inp, out], check=True, capture_output=True,
                             text=True).stdout.split()[0])
    X = np.fromfile(out, dtype=np.int8).reshape(-1, 40)
    assert len(X) == cnt
    X = np.unique(X, axis=0)
    assert len(X) == cnt, "enumerator produced a repeated row"
    if cnt:
        Xi = X.astype(np.int64)
        assert np.all((Xi - np.array(key[0])) % 3 == 0)
        assert np.all(((Xi @ G) * Xi).sum(1) == n)
    cache[key] = X
    return X


def table(classes):
    """classes: list of (r, D, z). Returns {(a, b): (T, C)} (C = 32767: no contact)."""
    N = [r * D * D + sum(v * v for v in z) for r, D, z in classes]
    assert all(v > 0 for v in N)
    # body norms x G x^T = 3r <= BMAX, so |t| <= BMAX (Cauchy-Schwarz in G)
    # and clamping T to [-BMAX-1, BMAX+1] changes no outcome
    assert all(0 <= 3 * r <= BMAX for r, _, _ in classes)
    out = {}
    for a, (ra, Da, za) in enumerate(classes):
        for b, (rb, Db, zb) in enumerate(classes):
            zz = sum(x * y for x, y in zip(za, zb))
            M9 = 9 * N[a] * N[b]
            Q = math.isqrt(M9)
            den = 2 * Da * Db
            T = (Q - 6 * zz) // den
            for t, ok in ((T, True), (T + 1, False)):
                s = den * t + 6 * zz
                assert (s <= 0 or s * s <= M9) == ok
            C = 32767
            if Q * Q == M9 and Q > 0 and (Q - 6 * zz) % den == 0:
                C = (Q - 6 * zz) // den
                assert C == T
            if not -BMAX <= C <= BMAX:
                C = 32767
            out[a, b] = (max(-BMAX - 1, min(BMAX + 1, T)), C)
    return out


def write_rows(out, X, G):
    X = np.ascontiguousarray(X, dtype=np.int8)
    XG = X.astype(np.int64) @ G
    assert np.abs(XG).max() <= 127, "partner rows exceed int8"
    X.tofile(out + "_x.i8")
    XG.astype(np.int8).tofile(out + "_xg.i8")


def build40(kdir, out, enum_bin, variant, work):
    G = np.array(json.load(open(path(kdir, "k40_gram.json"))), dtype=np.int64)
    cert = json.load(open(path(kdir, "k40_certificate.json")))
    assert G.shape == (40, 40) and np.array_equal(G, G.T) and positive_definite(G)
    c = np.array(cert["residue"], dtype=np.int64)
    assert c.shape == (40,) and not np.any((c @ G) % 3)
    if variant == "negcore":
        c = (-c) % 3
    core = shell(G, c, 54, enum_bin, work, {})
    print(f"core (residue c, norm 54): {len(core)} rows")
    with np.load(path(kdir, "k40_points.npz"), allow_pickle=False) as z:
        assert set(z.files) == {"norm6", "norm30", "norm36"}
        layers = {k: z[f"norm{k}"] for k in (36, 30, 6)}
    for k, X in layers.items():
        assert X.dtype == np.int8 and X.shape == (cert["counts"][str(k)], 40)
        Xi = X.astype(np.int64)
        assert np.all(((Xi @ G) * Xi).sum(1) == k) and len(np.unique(X, axis=0)) == len(X)
        print(f"explicit layer norm {k}: {len(X)} rows")
    assert len(core) == cert["counts"]["54"]
    X = np.vstack([core, layers[36], layers[30], layers[6]])
    assert len(np.unique(X, axis=0)) == len(X)
    assert len(X) == cert["total"] == CLAIM[40]
    write_rows(out, X, G)
    json.dump({"dim": 40, "rows": len(X), "core": len(core), "norm36": len(layers[36]),
               "norm30": len(layers[30]), "variant": variant}, open(out + "_meta.json", "w"))
    print(f"40D: {len(X)} points, 40 columns, partner (Gram) mode, norms 54/36/30")


def build4143(kdir, dim, out, enum_bin, variant, work):
    with np.load(path(kdir, f"k{dim}_configuration.npz"), allow_pickle=False) as z:
        assert set(z.files) == {"gram", "residues", "radii", "heads", "populations", "denominator",
                                "tiny_bodies", "tiny_heads", "tiny_denominator", "pure"}
        assert all(z[k].dtype.kind in "iu" for k in z.files)
        A = {k: z[k].astype(np.int64) for k in z.files}
    G = A["gram"]
    if variant == "p48q":
        assert dim == 43
        with np.load(path(kdir, "k41_configuration.npz"), allow_pickle=False) as z:
            G = z["gram"].astype(np.int64)
    assert G.shape == (40, 40) and np.array_equal(G, G.T) and positive_definite(G)
    D, E = int(A["denominator"]), int(A["tiny_denominator"])
    res, radii, heads, pops = A["residues"], A["radii"], A["heads"], A["populations"]
    tb, th, pure = A["tiny_bodies"], A["tiny_heads"], A["pure"]
    F, w = heads.shape
    assert D > 0 and E > 0 and res.shape == (F, 40) and radii.shape == pops.shape == (F,)
    assert np.all((0 <= res) & (res < 3)) and not np.any((res @ G) % 3)
    assert th.shape == (len(tb), w) and pure.shape[1] == w and tb.shape[1:] == (40,)
    assert rank(np.vstack([heads, th, pure])) == dim - 40, "head span has the wrong rank"
    if variant == "shift":
        heads = np.roll(heads, 1, axis=0)
    if variant == "purenegate":
        pure = -pure
    if variant == "tinyscale":
        E = D
    cache, rows, labels, classes = {}, [], [], []
    for i in range(F):
        X = shell(G, res[i], 3 * int(radii[i]), enum_bin, work, cache)
        assert len(X) == int(pops[i]), f"family {i}: {len(X)} != population {int(pops[i])}"
        rows.append(X)
        labels.append(np.full(len(X), len(classes)))
        classes.append((int(radii[i]), D, [int(v) for v in heads[i]]))
    print(f"{F} families, {sum(map(len, rows))} body points, {len(cache)} distinct shells enumerated")
    if len(tb):
        assert np.abs(tb).max() < 128
        tbi = tb.astype(np.int64)
        assert np.all(((tbi @ G) * tbi).sum(1) == 30)
        keys = sorted(set(map(tuple, th.tolist())))
        idx = {k: j for j, k in enumerate(keys)}
        lab = np.array([idx[tuple(h)] for h in th.tolist()])
        for j, k in enumerate(keys):
            Xj = tb[lab == j]
            assert len(np.unique(Xj, axis=0)) == len(Xj)
            rows.append(Xj.astype(np.int8))
            labels.append(np.full(len(Xj), len(classes)))
            classes.append((10, E, [int(v) for v in k]))
        print(f"{len(tb)} tiny points in {len(keys)} head classes")
    for p in pure:
        assert np.any(p != 0)
        rows.append(np.zeros((1, 40), dtype=np.int8))
        labels.append(np.full(1, len(classes)))
        classes.append((0, 1, [int(v) for v in p]))
    X = np.vstack(rows)
    lab = np.concatenate(labels)
    k = len(classes)
    assert len(X) == CLAIM[dim], f"{len(X)} != claimed {CLAIM[dim]}"
    write_rows(out, X, G)
    (lab.astype(np.uint8) if k <= 256 else lab.astype("<u2")).tofile(out + ".lab")
    tab = table(classes)
    with open(out + ".tab", "w") as f:
        f.write(f"{k}\n")
        for (a, b), (T, C) in sorted(tab.items()):
            f.write(f"{a} {b} {T} {C}\n")
    json.dump({"dim": dim, "rows": len(X), "families": F, "tiny": len(tb), "pure": len(pure),
               "classes": k, "D": D, "E": E, "variant": variant,
               "class_list": [[r, d_, z_] for r, d_, z_ in classes]}, open(out + "_meta.json", "w"))
    print(f"{dim}D: {len(X)} points = {int(pops.sum())} family + {len(tb)} tiny + {len(pure)} pure; "
          f"{k} classes; head rank {dim - 40}")


def main():
    kdir, dim, out, enum_bin = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    variant = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else None
    work = out + "_enumwork"
    os.makedirs(work, exist_ok=True)
    if dim == 40:
        assert variant in (None, "negcore")
        build40(kdir, out, enum_bin, variant, work)
    else:
        assert dim in (41, 42, 43) and variant in (None, "shift", "purenegate", "tinyscale", "p48q")
        build4143(kdir, dim, out, enum_bin, variant, work)


if __name__ == "__main__":
    main()
