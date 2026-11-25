"""Rebuild A. Kravatskiy's 783,468-point kissing configuration in R^39
(repository alexlegeartis/KissingNumbers @ 907f9b1f, package
verifications/improved/dim39-qr-three-coordinate-heads) with our own code.
Untrusted data: only JSON and text are parsed; none of its code is run.

Inputs and chain (read from the files and the README; verify.py read, not run):
  parent39.json          15 generators and 10 coset representatives (hex,
                         39 bits) of the binary code of Yang et al.,
                         arXiv:2609.35051v1, App. B, Tables 11-12.
  supports_3424.txt.gz   Lin's 3,424 weight-8 supports in 39 coordinates
                         (character i = coordinate i); the decompressed bytes
                         are Lin's certificate file (sha256 5e750c76...).
  base_certificate.json  7 support replacements {remove_index, remove, add}
                         (Kravatskiy's 768,924-point stage) and 4 heavy stars
                         {centre, leaves}; rule: drop the 4 roots on every
                         centre-leaf pair, centre +-4, leaves +-2 with an even
                         number of minus signs.
  certificate.json       marked_axes M = [19, 37, 38] (logical, for the
                         shortening), physical_marks [19, 0, 38] (where the
                         heads sit), physical_body (36 coordinates: body
                         position k is coordinate physical_body[k]),
                         dense_sign_flip f (36 bits), scale L = 10^6, 12 heads
                         h_i (3 integers each), extra_syndromes (4).
Dense layer. syn(x) = normal form of the 39-bit word x modulo the code (zero
at the code's pivot positions), read at the 24 non-pivot positions; this is
canonical. The 36 logical body positions are U = [0..38] minus M, in order.
K = {w restricted to U : w in the code, w zero on M} (4,096 words, min.
distance 12). Fibre syndromes: for head i < 8, the 10 values
syn(rep_j) ^ syn(sum_{bit b of i} e_{M[b]}); for heads 8..11 one extra
syndrome each. A fibre (i, s) is a + K, where a (36 bits over U) is any word
with syn(a placed on U) = s (the coset does not depend on the choice).
Its points are (2L (-1)^(bit k of (word ^ f)) at physical_body[k]; h_i at
physical_marks), squared norm 144 L^2 + |h_i|^2.
Sparse layer (all at scale L, raw squared norm 32): even-sign +-2 octads on
the 3,424 supports after the 7 replacements, KEEPING exactly those signings
whose inner product with every dense point satisfies the kissing bound
(README: "The verifier removes all conflicting signings"; computed here
exactly from the projections of each head's fibres onto the support);
the 64 stars; all +-4 e_i +-4 e_j except on the 14 distinct centre-leaf
pairs (2,908 roots).

Output, for the class mode of kiss_check.c / kiss_check_np.py (see
class_table.py): OUT_body.i8 (n x 36: u = 2 sigma for dense rows, the body
part of the sparse row otherwise), OUT_labels.u8, OUT_classes.json (L and,
per class, w = h_i or L * (sparse marks part), and the body norm). Rows are
x = (L u, w). Also OUT_sparse.i8: the sparse rows alone (n_s x 39, int8, raw
squared norm 32) for the plain integer check.

Usage: python3 -I build_kravatskiy39.py KRAVDIR OUT [--variant NAME]
  negative controls (must FAIL): noflip (dense_sign_flip = 0 but keep the
  octad selection of the true layout), identity (logical body order instead
  of physical_body, same octad selection), unswitched (stars and the 4
  heavy-star root deletions on the unreplaced Lin supports).
"""
import gzip
import hashlib
import itertools
import json
import math
import os
import sys

import numpy as np

D = 39
SHA = {
    "k39_parent39.json": "72877e1101a4d33f96646f43d64a6688c3bb2baa56ada85df3c76017c4d14365",
    "k39_base_certificate.json": "2c7188449cd0b93bd0e9eec3d408e087b3e4763d22202ed63adf4403bc08ecd9",
    "k39_certificate.json": "38ca2a117f325bc919bd8f9649ae664b87c4d1ff81b6bf9fbbf1b458b17835a8",
    "k39_supports_3424.txt.gz": "105c2bc72b3e30129841fdc59ae2c2000d3841cae63d83f34fb8c2cdcbc3bcce",
}
LIN_SUPPORTS_SHA = "5e750c76c21aa9e350784624d367cc724a392eb8cb006826613d8dc82321d1cf"


def read(kdir, name):
    raw = open(os.path.join(kdir, name), "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA[name], f"{name}: sha256 mismatch"
    return raw


def span(gens):
    words = [0]
    for g in gens:
        words += [w ^ g for w in words]
    assert len(set(words)) == len(words)
    return words


def echelon(gens):
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
    basis = {}
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


def angular(p, n, m):
    return p <= 0 or 4 * p * p <= n * m


def build(kdir, variant=None):
    par = json.loads(read(kdir, "k39_parent39.json"))
    base = json.loads(read(kdir, "k39_base_certificate.json"))
    cert = json.loads(read(kdir, "k39_certificate.json"))
    raw = gzip.decompress(read(kdir, "k39_supports_3424.txt.gz"))
    assert hashlib.sha256(raw).hexdigest() == LIN_SUPPORTS_SHA == base["source_sha256"]["supports_3424.txt"]
    gens = [int(x, 16) for x in par["generators_hex"]]
    reps = [int(x, 16) for x in par["representatives_hex"]]
    assert par["length"] == D and len(gens) == 15 and len(reps) == 10
    M = cert["marked_axes"]
    pm = cert["physical_marks"]
    body = cert["physical_body"]
    flip = cert["dense_sign_flip"]
    L = cert["scale"]
    heads = cert["heads"]
    assert M == sorted(set(M)) and len(M) == 3 and len(set(pm)) == 3
    assert sorted(body + pm) == list(range(D)) and 0 <= flip < 2**36 and type(L) is int and L > 0
    assert len(heads) == 12 and all(len(h) == 3 and all(type(x) is int for x in h) for h in heads)
    U = [i for i in range(D) if i not in M]
    piv = echelon(gens)
    assert len(piv) == 15
    free = [i for i in range(D) if i not in piv]

    def syn(x):
        for p, v in piv.items():
            if x >> p & 1:
                x ^= v
        return sum((x >> i & 1) << j for j, i in enumerate(free))

    def onU(a):  # 36-bit word over U -> 39-bit word
        return sum((a >> j & 1) << i for j, i in enumerate(U))

    H = span(gens)
    K = sorted(sum((w >> i & 1) << j for j, i in enumerate(U)) for w in H if not any(w >> m & 1 for m in M))
    assert len(K) == len(set(K)) == 4096
    mdK = min(k.bit_count() for k in K if k)
    A = [syn(r) for r in reps]
    assert len(set(A)) == 10
    Tm = [syn(sum(1 << M[b] for b in range(3) if i >> b & 1)) for i in range(8)]
    offs = [[x ^ t for x in A] for t in Tm] + [[int(s)] for s in cert["extra_syndromes"]]
    assert len(offs) == 12
    cols = [syn(1 << i) for i in U]
    fibres = []
    for i, ss in enumerate(offs):
        for s in ss:
            a = solve(cols, s)
            assert syn(onU(a)) == s
            fibres.append((i, a))
    assert len(fibres) == 84 and len(set(fibres)) == 84
    Kar = np.array(K, dtype=np.int64)
    bits = np.arange(36)
    words_by_head = [np.concatenate([Kar ^ a for h, a in fibres if h == i]) ^ flip for i in range(12)]
    # body position k <-> physical coordinate body[k]
    pos = {j: k for k, j in enumerate(body)}
    nrm = [144 * L * L + sum(x * x for x in h) for h in heads]

    # sparse layer
    rows = raw.decode("ascii").split("\n")
    rows = [r for r in rows if r]
    assert len(rows) == 3424 and all(len(r) == D and set(r) <= {"0", "1"} and r.count("1") == 8 for r in rows)
    sup = [[i for i, ch in enumerate(r) if ch == "1"] for r in rows]
    if variant != "unswitched":
        for v in base["support_replacements"]:
            assert sup[v["remove_index"]] == v["remove"], "replacement does not match parent"
            sup[v["remove_index"]] = sorted(v["add"])
    assert all(len(s) == len(set(s)) == 8 for s in sup)

    cache = {}

    def max_dot(i, a):
        """Exact max over the dense points of head i of the raw inner product
        (in units of L) with the sparse point a = {coordinate: value}."""
        bod = [(pos[j], v) for j, v in a.items() if j in pos]
        key = (i, tuple(k for k, _ in bod))
        if key not in cache:
            W = words_by_head[i]
            proj = np.zeros(len(W), dtype=np.int64)
            for t, (k, _) in enumerate(bod):
                proj |= ((W >> k) & 1) << t
            cache[key] = np.unique(proj)
        pats = cache[key]
        # dense body entry 2L(-1)^bit; inner product with v: 2L v (-1)^bit
        best = None
        val = np.zeros(len(pats), dtype=np.int64)
        for t, (_, v) in enumerate(bod):
            val += 2 * v * (1 - 2 * ((pats >> t) & 1))
        best = int(val.max()) * L
        best += sum(heads[i][b] * a.get(j, 0) for b, j in enumerate(pm))
        return best  # true inner product / L

    def keep(a):
        return all(angular(max_dot(i, a), nrm[i], 32) for i in range(12))

    signs = [s for s in itertools.product((2, -2), repeat=8) if sum(x < 0 for x in s) % 2 == 0]
    octs, drop = [], 0
    for s in sup:
        for sg in signs:
            a = dict(zip(s, sg))
            if keep(a):
                v = [0] * D
                for j, x in a.items():
                    v[j] = x
                octs.append(v)
            else:
                drop += 1
    removed, stars = set(), []
    for v in base["heavy_stars"]:
        c, lv = v["center"], v["leaves"]
        assert c not in lv and len(set(lv)) == 4
        for j in lv:
            removed.add(tuple(sorted((c, j))))
        for a in (4, -4):
            for f in itertools.product((2, -2), repeat=4):
                if sum(x < 0 for x in f) % 2:
                    continue
                row = [0] * D
                row[c] = a
                for j, x in zip(lv, f):
                    row[j] = x
                stars.append(row)
    roots = []
    for i, j in itertools.combinations(range(D), 2):
        if (i, j) in removed:
            continue
        for a, b in itertools.product((4, -4), repeat=2):
            row = [0] * D
            row[i], row[j] = a, b
            roots.append(row)
    Sp = np.array(octs + stars + roots, dtype=np.int64)
    assert ((Sp * Sp).sum(1) == 32).all()
    print(f"variant {variant}: dense {84 * 4096} (84 fibres, kernel min distance {mdK}) + octads {len(octs)} "
          f"(dropped {drop}) + stars {len(stars)} + roots {len(roots)} = {84 * 4096 + len(Sp)}")
    if variant is None:
        assert (len(octs), drop, len(stars), len(roots)) == (436432, 1840, 64, 2908)
    return dict(L=L, heads=heads, fibres=fibres, K=Kar, flip=flip, body=body, pm=pm, sparse=Sp)


def assemble(c, out):
    L, heads, body, pm = c["L"], c["heads"], c["body"], c["pm"]
    bits = np.arange(36)
    parts, labels, classes, key = [], [], [], {}

    def cls(w, n):
        k = (tuple(int(x) for x in w), int(n))
        if k not in key:
            key[k] = len(classes)
            classes.append({"w": list(k[0]), "body_norm": k[1]})
        return key[k]

    for i, a in c["fibres"]:
        W = (c["K"] ^ a) ^ c["flip"]
        parts.append((2 - 4 * ((W[:, None] >> bits) & 1)).astype(np.int8))
        labels.append(np.full(len(W), cls(heads[i], 144), dtype=np.uint8))
    Sp = c["sparse"]
    ub = Sp[:, body]
    um = Sp[:, pm]
    parts.append(ub.astype(np.int8))
    labels.append(np.array([cls(L * m, 32 - int((m * m).sum())) for m in um], dtype=np.uint8))
    X = np.concatenate(parts)
    lab = np.concatenate(labels)
    assert len(classes) <= 256
    assert len(X) == len(lab)
    X.tofile(out + "_body.i8")
    lab.tofile(out + "_labels.u8")
    json.dump({"L": L, "classes": classes}, open(out + "_classes.json", "w"))
    Sp.astype(np.int8).tofile(out + "_sparse.i8")
    print(f"rows {len(X)}, {len(classes)} classes -> {out}_body.i8, _labels.u8, _classes.json, _sparse.i8")


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "noflip", "identity", "unswitched")
    c = build(a[1], None if var in ("noflip", "identity") else var)
    # the two layout controls keep the sparse set built with the true layout
    # and change only how the dense layer is placed
    if var == "noflip":
        c["flip"] = 0
    elif var == "identity":
        c["body"] = [i for i in range(D) if i not in (19, 37, 38)]
        c["pm"] = [19, 37, 38]
    assemble(c, a[2])
