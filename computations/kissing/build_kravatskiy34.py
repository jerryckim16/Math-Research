"""Rebuild A. Kravatskiy's 391,004-point kissing configuration in R^34 from
its chain of edits (repository alexlegeartis/KissingNumbers @ 907f9b1f,
verifications/improved/), with our own code. Untrusted data: only JSON is
parsed; none of the repository's code is run.

Chain (read from the files and the packages' READMEs):
  dim32-35-signed-layers/rotated34/certificate.json (390,992 points):
    dense_generator (17 masks, 32 bits), dense_coset_shift,
    dense_coordinates (the 32 coordinates other than 0 and 2),
    full_even_supports (2,013 masks, bit j = coordinate j), stars (64 rows),
    removed_root_lines (28 [i, j, s]: the roots +-4(e_i + s e_j)),
    heavy_numerators_over_85 (4 rows h with |h|^2 = 361,250; the points are
    (4/425) h, squared norm 32), counts, points, ...
  -> dim34-octad-switches/witness.json (391,004 points):
    "octads": 4 [index, old support, new support] (coordinate lists);
    "stars": 7 templates [[centre, 4 leaves], parity]: centre +-4, leaves +-2
    with that parity of minus signs. These 7 x 16 = 112 stars replace the
    parent's 64. The roots are then all +-4 e_i +-4 e_j that have inner
    product <= 16 with every star and with every head (README: "48 roots
    become blocked and 12 are restored").
Points at the base scale (squared norm 32): dense (-1)^(bit i of w ^ shift) at
dense_coordinates[i]; octads +-2 on each support, even number of minus signs;
stars; roots. Heads: the integer rows h (a positive multiple of the point).

Final hash. The author's replay writes the edited certificate as
json.dumps(c, sort_keys=True) + "\\n" and records its sha256 4b605a02...
(dim34-octad-switches/verification.json). We apply the same edits to the
parent JSON with our own code and compare the hash: equality means our
reading of the recipe gives his final certificate byte for byte. The
check of the points does not depend on that comparison.

Outputs: OUT.i8 (391,000 integer rows x 34, int8) and OUT_field.json (the 4
heads, for kiss_check_field.py, which checks every pair involving a head).
Usage: python3 -I build_kravatskiy34.py KRAVDIR OUT [--variant NAME]
  negative controls (must FAIL): unswitched (new stars on the parent's
  unswitched supports), oldroots (new stars with the parent's root deletions).
"""
import copy
import hashlib
import itertools
import json
import os
import sys

import numpy as np

D = 34
PARENT_SHA = "36a9017be6de898d16bdfdad1b686db1d991a9be8a77a804134d770794a5f7ea"
WITNESS_SHA = "87da7c9bab1f0a0f3dc627b8e88a5cfde3815745a1c74e7ce70c405c2e6d1dd3"
FINAL_SHA = "4b605a02c36617c5b5f353e60640eac799a699f2a0edae0e62d2653e0f840e64"


def read(path, digest):
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == digest, f"{path}: sha256 mismatch"
    return json.loads(raw)


def mask(cs):
    assert len(cs) == len(set(cs)) == 8 and all(0 <= j < D for j in cs)
    return sum(1 << j for j in cs)


def edit(old, w, variant=None):
    """Apply the witness to the parent certificate (a dict); return the new dict."""
    c = copy.deepcopy(old)
    sup = c["full_even_supports"]
    done = set()
    for i, before, after in w["octads"]:
        assert i not in done and sup[i] == mask(before), "switch does not match parent"
        done.add(i)
        if variant != "unswitched":
            sup[i] = mask(after)
    stars = []
    for (centre, *leaves), par in w["stars"]:
        assert len(leaves) == 4 and len({centre, *leaves}) == 5 and par in (0, 1)
        for a in (-4, 4):
            for s in itertools.product((-2, 2), repeat=4):
                if s.count(-2) % 2 != par:
                    continue
                v = [0] * D
                v[centre] = a
                for j, x in zip(leaves, s):
                    v[j] = x
                stars.append(v)
    assert len({tuple(v) for v in stars}) == len(stars) == 16 * len(w["stars"])
    c["stars"] = stars
    heads = c["heavy_numerators_over_85"]
    removed = set()
    for i, j in itertools.combinations(range(D), 2):
        for a, b in itertools.product((-1, 1), repeat=2):
            # root 4(a e_i + b e_j) vs star x: 4(a x_i + b x_j) <= 16;
            # vs head (4/425) h: (16/425)(a h_i + b h_j) <= 16
            if any(a * x[i] + b * x[j] > 4 for x in stars) or any(a * h[i] + b * h[j] > 425 for h in heads):
                removed.add((i, j, a, b))
    assert all((i, j, -a, -b) in removed for i, j, a, b in removed)
    lines = sorted({(i, j, a * b) for i, j, a, b in removed})
    if variant == "oldroots":
        lines = [tuple(x) for x in old["removed_root_lines"]]
    c["removed_root_lines"] = lines
    c["counts"].update(stars=len(stars), roots=2 * D * (D - 1) - 2 * len(lines))
    c["points"] = sum(c["counts"].values())
    c["comparison"] = {"preceding_points": 390992, "gain": c["points"] - 390992}
    return c


def points(c):
    gens, shift, pos = c["dense_generator"], c["dense_coset_shift"], c["dense_coordinates"]
    assert len(gens) == 17 and len(pos) == len(set(pos)) == 32 and set(range(D)) - set(pos) == {0, 2}
    words = [0]
    for g in gens:
        assert 0 < g < 2**32
        words += [x ^ g for x in words]
    assert len(set(words)) == 2**17
    W = np.array(sorted(x ^ shift for x in words), dtype=np.int64)
    dense = np.zeros((len(W), D), dtype=np.int64)
    dense[:, pos] = 1 - 2 * ((W[:, None] >> np.arange(32)) & 1)
    signs = np.array(list(itertools.product((2, -2), repeat=8)), dtype=np.int64)
    signs = signs[(signs < 0).sum(1) % 2 == 0]
    sup = c["full_even_supports"]
    assert len(set(sup)) == len(sup) == 2013
    mid = np.zeros((len(sup) * 128, D), dtype=np.int64)
    for t, m in enumerate(sup):
        assert m.bit_count() == 8 and m < 2**D
        mid[t * 128:(t + 1) * 128, [j for j in range(D) if m >> j & 1]] = signs
    dead = {(i, j, s) for i, j, s in c["removed_root_lines"]}
    roots = []
    for i, j in itertools.combinations(range(D), 2):
        for a, b in itertools.product((-4, 4), repeat=2):
            if (i, j, (a * b) // 16) not in dead:
                v = [0] * D
                v[i], v[j] = a, b
                roots.append(v)
    X = np.concatenate([dense, mid, np.array(c["stars"], dtype=np.int64), np.array(roots, dtype=np.int64)])
    H = np.array(c["heavy_numerators_over_85"], dtype=np.int64)
    assert ((X * X).sum(1) == 32).all() and ((H * H).sum(1) == 361250).all()
    assert len({r.tobytes() for r in X}) == len(X), "repeated rows"
    return X, H


def main(kdir, out, variant=None):
    old = read(os.path.join(kdir, "k34_parent_rotated34.json"), PARENT_SHA)
    w = read(os.path.join(kdir, "k34_witness.json"), WITNESS_SHA)
    assert old["points"] == 390992 and len(w["octads"]) == 4 and len(w["stars"]) == 7
    c = edit(old, w, variant)
    h = hashlib.sha256((json.dumps(c, sort_keys=True) + "\n").encode()).hexdigest()
    X, H = points(c)
    print(f"variant {variant}: counts {c['counts']} points {c['points']} (rows built {len(X) + len(H)})")
    print(f"final certificate sha256 {h} {'== author' if h == FINAL_SHA else '!= author'}")
    if variant is None:
        assert h == FINAL_SHA and len(X) + len(H) == 391004 and c["counts"]["roots"] == 2152
    X.astype(np.int8).tofile(out + ".i8")
    rows = [[h.tolist(), [0] * D, [0] * D, [0] * D] for h in H]
    json.dump({"d": D, "rows": rows}, open(out + "_field.json", "w"))
    print(f"-> {out}.i8 ({len(X)} rows), {out}_field.json ({len(H)} heads)")


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "unswitched", "oldroots")
    main(a[1], a[2], var)
