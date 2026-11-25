"""Rebuild A. Kravatskiy's 415,360-point kissing configuration in R^35 from
its chain of edits (repository alexlegeartis/KissingNumbers @ 907f9b1f,
verifications/improved/), with our own code. The files are untrusted data:
JSON is parsed with the json module, .npz with numpy (allow_pickle=False).
None of the repository's code is run.

Chain (each step read from the files and the packages' READMEs):
  dim35-shared-root-heads (415,336 points)
    code_data.json      dense_generator (17 masks, 32 bits), dense_coset_shift,
                        full_parity_supports: 2,202 [35-bit support mask, parity]
                        (these parities are those of an earlier stage)
    full_parities.json  the same 2,202 masks with the parities of the
                        415,336-point stage ("derives valid octad parities")
    shared_positive.npz dense_positions (32 coordinates; the three others,
                        0, 3, 18, carry the heads' magnitude-3 entries), heads
  -> dim35-octad-switches (415,358 points)
    witness.json        "octads": 7 [index, old support, new support]; the new
                        supports take all 128 even signings, the others keep
                        their parity from full_parities.json (that package's
                        README and its verify.py, read, not run). Its
                        star and root edits are superseded by the next step.
  -> dim35-joint-star-root (415,360 points)
    replacement.npz     the complete final stars (262), roots (2,158) and
                        heads (12, unchanged) as integer rows.
Points (integer coordinates):
  dense   131,072: entry (-1)^(bit i of w ^ shift) at dense_positions[i], w in
          the span of the generators; squared norm 32
  octads  2,202 x 128: +-2 on each support, number of minus signs of the
          support's parity; squared norm 32
  stars, roots: as listed (squared norm 32); heads: as listed (two entries
          +-3, 33 entries +-1; squared norm 51).
Mask convention: bit j = coordinate j (the switch witness lists supports as
coordinate lists, and its "old" lists equal the decoded masks, which checks
the convention for those 7 supports).

Usage: python3 -I build_kravatskiy35.py KRAVDIR OUT.i8 [--variant NAME]
  variants (negative controls, must FAIL): unswitched (keep the 7 old
  supports, i.e. apply the final star/root layer to the wrong parent),
  oldparity (take the parities from code_data.json instead of
  full_parities.json, i.e. from the wrong stage of the chain).
"""
import hashlib
import itertools
import json
import os
import sys

import numpy as np

D = 35
SHA = {
    "k35_code_data.json": "0f44ca2ff564941d58f92cbb0c47ada139612196fd3d69a547d5318f78009d05",
    "k35_full_parities.json": "e156ae604938772d9d41e9b2a39af5602fcc7f8bf7f242c35695a4f2a9218c24",
    "k35_shared_positive.npz": "9d4b35ac5d18f40011282ec2e83753bdffee947351584a77a910baef875768cf",
    "k35_switch_witness.json": "3e8a212b8a8ee4c6d81a45134dae67b99fbfbc4a4f990fc174c42af987e01e16",
    "k35_replacement.npz": "ffb73e3082a0ed5a1f94ce8e5c32febb0683e151bcd1aee3838eb52a6e76320c",
}


def read(kdir, name):
    path = os.path.join(kdir, name)
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA[name], f"{name}: sha256 mismatch"
    return path, raw


def span(gens):
    words = [0]
    for g in gens:
        words += [w ^ g for w in words]
    assert len(set(words)) == len(words), "generators not independent"
    return words


def coords(mask):
    return [j for j in range(D) if mask >> j & 1]


def octad_block(cs, parity):
    signs = np.array(list(itertools.product((2, -2), repeat=8)), dtype=np.int64)
    signs = signs[(signs < 0).sum(1) % 2 == parity]
    b = np.zeros((128, D), dtype=np.int64)
    b[:, cs] = signs
    return b


def build(kdir, variant=None):
    c = json.loads(read(kdir, "k35_code_data.json")[1])
    sw = json.loads(read(kdir, "k35_switch_witness.json")[1])
    fp = json.loads(read(kdir, "k35_full_parities.json")[1])
    with np.load(read(kdir, "k35_shared_positive.npz")[0], allow_pickle=False) as z:
        pos = [int(x) for x in z["dense_positions"]]
        heads0 = z["heads"].astype(np.int64)
    with np.load(read(kdir, "k35_replacement.npz")[0], allow_pickle=False) as z:
        assert set(z.files) == {"stars", "roots", "heads"}
        S, R, H = (z[k].astype(np.int64) for k in ("stars", "roots", "heads"))
    assert S.shape == (262, D) and R.shape == (2158, D) and H.shape == (12, D)
    assert np.array_equal(H, heads0), "final heads differ from the parent's"
    assert len(pos) == len(set(pos)) == 32 and set(range(D)) - set(pos) == {0, 3, 18}
    # dense layer
    gens = [int(g) for g in c["dense_generator"]]
    shift = int(c["dense_coset_shift"])
    assert len(gens) == 17 and all(0 < g < 2**32 for g in gens) and 0 <= shift < 2**32
    W = np.array(sorted(w ^ shift for w in span(gens)), dtype=np.int64)
    dense = np.zeros((len(W), D), dtype=np.int64)
    dense[:, pos] = 1 - 2 * ((W[:, None] >> np.arange(32)) & 1)
    # octad layer: parent supports and parities, then the 7 switches
    sup = [[int(m), int(p)] for m, p in c["full_parity_supports"]]
    assert [m for m, _ in sup] == [int(m) for m, _ in fp], "parity table has other supports"
    if variant != "oldparity":
        sup = [[int(m), int(p)] for m, p in fp]
    assert len(sup) == 2202 and all(p in (0, 1) for _, p in sup)
    seen = set()
    for i, old, new in sw["octads"]:
        assert i not in seen and sup[i][0] == sum(1 << j for j in old), "switch does not match parent"
        seen.add(i)
        if variant != "unswitched":
            sup[i] = [sum(1 << j for j in new), 0]
    assert len(seen) == 7
    masks = [m for m, _ in sup]
    assert len(set(masks)) == 2202 and all(m.bit_count() == 8 and m < 2**D for m in masks)
    octs = np.concatenate([octad_block(coords(m), p) for m, p in sup])
    X = np.concatenate([dense, octs, S, R, H])
    nrm = (X * X).sum(1)
    assert X.shape == (415360, D)
    assert (nrm[:-12] == 32).all() and (nrm[-12:] == 51).all()
    assert len({r.tobytes() for r in X}) == len(X), "repeated rows"
    print(f"variant {variant}: dense {len(dense)} + octads {len(octs)} ({len(sup)} supports, "
          f"{sum(p for _, p in sup)} odd) + stars {len(S)} + roots {len(R)} + heads {len(H)} = {len(X)}")
    return X


if __name__ == "__main__":
    a = sys.argv
    var = a[a.index("--variant") + 1] if "--variant" in a else None
    assert var in (None, "unswitched", "oldparity")
    X = build(a[1], var)
    X.astype(np.int8).tofile(a[2])
    print(f"-> {a[2]}")
