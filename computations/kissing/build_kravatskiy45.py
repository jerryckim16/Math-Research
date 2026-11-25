"""Rebuild A. Kravatskiy's 45D kissing configuration (7,655,056 points) from
the coordinated family table in alexlegeartis/KissingNumbers @ 907f9b1f
(verifications/improved/dim41-46-p48-heads/coordinated45/), with our own
code: our own shell enumerator (enum_affine.c) and our own class table.
Untrusted data: only .npz (allow_pickle=False) is parsed; none of the
repository's code is run (its verify.py and coordinates.py were read to
learn the format).

Format (coordinated45/README.txt, coordinates.py):
  configuration.npz: per family i a class index classes[i] in 0..6560
      (one of the 3^8 discriminant classes), r3[i] in {10, 12, 14, 16, 18},
      weights[i] (the population), head_numerators[i] (8 integers) over the
      common head_denominator D; 16 pure_directions p (integers); an exact
      span projector (not needed here: the head rank is computed directly).
  geometry.npz: body_gram G (40 x 40 integer) and body_residues (6561 x 40).
  Family i is every x in Z^40 with x == body_residues[classes[i]] (mod 3)
  and x G x^T = 3 r3[i], each paired with the head z_i / D. The author's
  exact coordinates are (x L / sqrt3, h) / sqrt(r + |h|^2) with L L^T = G,
  h = z_i / D: body metric G/3, the 41-43D convention of
  build_kravatskiy4043.py with r = r3. A pure point is (0, p) (r = 0, D = 1).
  With G positive definite (checked exactly) and heads of rational rank 5
  (checked exactly), the points lie in R^40 + R^5 = R^45.
Exact criterion: as in build_kravatskiy4043.py (class + partner mode), with
the same entry() function for the table: points of classes a, b with body
product t = x G y^T pass iff t <= T(a, b); T is checked (T passes, T + 1
fails) in Python integers. kiss_check.c evaluates t exactly for every pair.

Classes: one per family (2,187) plus one per pure point (16), 2,203 in all
(uint16 labels). The table has 2,203^2 = 4,853,209 entries; it is computed
on the upper triangle (T and C are symmetric in a, b) and written in
(a, b) order.

Checks against the author's published data: every family's enumerated
shell has exactly the published weight; the layer table (families and
points per r3) equals replay.json; the total is 7,655,056.

Outputs: OUT_x.i8, OUT_xg.i8 (partner rows x G), OUT.lab (uint16 LE),
OUT.tab, OUT_meta.json.
Usage: python3 -I build_kravatskiy45.py KRAVDIR OUT ENUM_BIN [--work DIR] [--jobs J]
  (DIR keeps the shell enumerations for reuse; J parallel enum_affine runs,
  each single-threaded)
       python3 -I build_kravatskiy45.py --retable BASE VARIANT OUT
  head-only negative controls (must FAIL): shift (the head list shifted by
  one family, wrong order), headscale (family heads read over D/2 instead of
  D, i.e. doubled).
"""
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_kravatskiy4043 as b43  # noqa: E402

SHA = {
    "k45_configuration.npz": "bb4bddd2edba731a06934715dbe62c78ab15fb56b75b0e1bb08aacf799b268b5",
    "k45_geometry.npz": "6c854f55c485866505fffce7ed8efc792c43bc5489a31d447089e4086e65444f",
}
CLAIM = 7655056
# replay.json of the package: r3 -> (families, points)
LAYERS = {10: (1200, 18900), 12: (778, 385110), 14: (168, 1542240), 16: (40, 4624200),
          18: (1, 1084590)}
PURE = 16


def path(kdir, name):
    p = os.path.join(kdir, name)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    assert h == SHA[name], f"{name}: sha256 mismatch"
    return p


def load(kdir):
    with np.load(path(kdir, "k45_configuration.npz"), allow_pickle=False) as z:
        assert set(z.files) == {"classes", "r3", "weights", "head_numerators", "head_denominator",
                                "pure_directions", "span_projector_numerator",
                                "span_projector_denominator"}
        assert all(z[k].dtype.kind in "iu" for k in z.files)
        A = {k: z[k].astype(np.int64) for k in z.files}
    with np.load(path(kdir, "k45_geometry.npz"), allow_pickle=False) as z:
        assert {"body_gram", "body_residues"} <= set(z.files)
        assert z["body_gram"].dtype.kind in "iu" and z["body_residues"].dtype.kind in "iu"
        G = z["body_gram"].astype(np.int64)
        R = z["body_residues"].astype(np.int64) % 3  # "a mod 3 = body_residues[c] mod 3"
    return A, G, R


def write_table(classes, out):
    """Stream the table: upper triangle by entry(), mirrored, written in
    (a, b) order, the same format as build_kravatskiy4043.write_table."""
    k = len(classes)
    N = b43.norms(classes)
    T = np.zeros((k, k), dtype=np.int32)
    C = np.zeros((k, k), dtype=np.int32)
    for a in range(k):
        ca, Na = classes[a], N[a]
        for b in range(a, k):
            T[a, b], C[a, b] = b43.entry(ca, classes[b], Na, N[b])
        T[a:, a], C[a:, a] = T[a, a:], C[a, a:]
    assert np.array_equal(T, T.T) and np.array_equal(C, C.T)
    with open(out + ".tab", "w") as f:
        f.write(f"{k}\n")
        for a in range(k):
            f.write("".join(f"{a} {b} {T[a, b]} {C[a, b]}\n" for b in range(k)))
    return T, C


def build(kdir, out, enum_bin, work, jobs):
    A, G, R = load(kdir)
    assert G.shape == (40, 40) and np.array_equal(G, G.T) and b43.positive_definite(G)
    assert R.shape == (3 ** 8, 40)
    cl, r3, w, Z = A["classes"], A["r3"], A["weights"], A["head_numerators"]
    D, pure = int(A["head_denominator"]), A["pure_directions"]
    F = len(cl)
    assert D > 0 and cl.shape == r3.shape == w.shape == (F,) and Z.shape == (F, 8)
    assert pure.shape == (PURE, 8) and np.all(np.any(pure != 0, axis=1))
    assert np.all((0 <= cl) & (cl < 3 ** 8)) and np.all(np.isin(r3, list(LAYERS)))
    res = R[cl]
    assert not np.any((res @ G) % 3), "a class residue fails G c == 0 (mod 3)"
    assert b43.rank(np.vstack([Z, pure])) == 5, "head span does not have rank 5"
    keys = sorted({(int(c), int(r)) for c, r in zip(cl, r3)})
    print(f"{F} families, {len(keys)} distinct shells (class, r3)", flush=True)
    # enumerate every distinct shell, J single-threaded enum_affine runs at once
    env = dict(os.environ, OMP_NUM_THREADS="1")
    with ThreadPoolExecutor(jobs) as ex:  # largest shells first
        list(ex.map(lambda key: b43.enum_file(G, R[key[0]], 3 * key[1], enum_bin, work, env),
                    sorted(keys, key=lambda k: -k[1])))
    cache, rows, labels, classes = {}, [], [], []
    for i in range(F):
        X = b43.shell(G, res[i], 3 * int(r3[i]), enum_bin, work, cache)
        assert len(X) == int(w[i]), f"family {i}: {len(X)} != weight {int(w[i])}"
        rows.append(X)
        labels.append(np.full(len(X), len(classes), dtype=np.uint16))
        classes.append((int(r3[i]), D, [int(v) for v in Z[i]]))
    layers = {r: (int(np.sum(r3 == r)), int(w[r3 == r].sum())) for r in LAYERS}
    assert layers == LAYERS, layers
    print(f"layers r3 -> (families, points): {layers} (= replay.json)", flush=True)
    for p in pure:
        rows.append(np.zeros((1, 40), dtype=np.int8))
        labels.append(np.full(1, len(classes), dtype=np.uint16))
        classes.append((0, 1, [int(v) for v in p]))
    X = np.vstack(rows)
    del rows, cache
    lab = np.concatenate(labels)
    k = len(classes)
    assert len(X) == CLAIM == int(w.sum()) + PURE, f"{len(X)} != claimed {CLAIM}"
    assert k == F + PURE and k < 2 ** 16
    Xi_max = int(np.abs(X).max())
    b43.write_rows(out, X, G)
    lab.astype("<u2").tofile(out + ".lab")
    T, C = write_table(classes, out)
    json.dump({"dim": 45, "rows": len(X), "families": F, "tiny": 0, "pure": PURE,
               "classes": k, "D": D, "E": None, "variant": None, "max_abs_entry": Xi_max,
               "class_list": [[r, d_, z_] for r, d_, z_ in classes]}, open(out + "_meta.json", "w"))
    print(f"45D: {len(X)} points = {int(w.sum())} family + {PURE} pure; {k} classes; head rank 5; "
          f"T in [{T.min()}, {T.max()}], {int(np.sum(C != 32767))} contact entries")


def retable(base, variant, out):
    """Head-only negative controls: a new table for the rows and labels of BASE."""
    meta = json.load(open(base + "_meta.json"))
    assert meta["dim"] == 45 and meta["variant"] is None
    cl = [(r, d_, list(z_)) for r, d_, z_ in meta["class_list"]]
    F = meta["families"]
    if variant == "shift":  # head list shifted by one family (wrong order)
        cl[:F] = [(r, d_, cl[(i - 1) % F][2]) for i, (r, d_, _) in enumerate(cl[:F])]
    elif variant == "headscale":  # family heads read over D/2 instead of D (doubled)
        assert all(d_ % 2 == 0 for _, d_, _ in cl[:F])
        cl[:F] = [(r, d_ // 2, z_) for r, d_, z_ in cl[:F]]
    else:
        raise SystemExit(f"unknown variant {variant}")
    write_table(cl, out)
    print(f"45D variant {variant}: table -> {out}.tab (rows, labels: {base})")


def main():
    if sys.argv[1] == "--retable":
        return retable(sys.argv[2], sys.argv[3], sys.argv[4])
    kdir, out, enum_bin = sys.argv[1], sys.argv[2], sys.argv[3]
    work = sys.argv[sys.argv.index("--work") + 1] if "--work" in sys.argv else out + "_enumwork"
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
    os.makedirs(work, exist_ok=True)
    build(kdir, out, enum_bin, work, jobs)


if __name__ == "__main__":
    main()
