"""Rebuild A. Kravatskiy's 232,157-point configuration in R^29 (repository
alexlegeartis/KissingNumbers @ 907f9b1f, package
verifications/improved/dim29-even-grid-exchange) from two pinned data files,
with our own code:
  parent  dim29-takhanov-auxiliary-exchange/data/coordinates29_232154.npz
          (int16 numerators, 232,154 x 29, squared norm 128)
  trade   dim29-even-grid-exchange/trade.npz: 14 primitive integer rays on
          the 13 coordinates `coordinates`, their squared norms, and the 11
          parent row indices `drop` to delete.
Final code = parent rows not in `drop`, then the 14 rays scaled by
sqrt(128 / norm) (an integer: 2, 4 or 8 here), all with squared norm 128.
The package's README states that `verify.py --full` checks all
26,948,320,246 pairs of exactly this code; we do not run it. We compare
the sha256 of our int16 array with the value in the package's manifest
(final_little_endian_int16_sha256), which identifies our rebuild with the
author's code byte for byte if they agree (row order included); the
check itself does not depend on that comparison.

Usage: python3 -I build_kravatskiy29.py PARENT.npz TRADE.npz OUT.i8
"""
import hashlib
import math
import sys

import numpy as np

PARENT_SHA = "5daac8c4449cfaff1e9b73d8d7de9baced5a54f92e84f45a28cc8764a5b5cbd4"
TRADE_SHA = "d85b5cdf65eb128ad55104711cfc57621554de1d31005ad181757b46b2f3f9cd"
FINAL_INT16_SHA = "80aa09bd7b78170e2693cf221980eec312a7ac54e619218d3d5eb90b1fd7eecf"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main(parent, trade, out):
    assert sha(parent) == PARENT_SHA and sha(trade) == TRADE_SHA, "sha256 mismatch"
    with np.load(parent, allow_pickle=False) as z:
        assert set(z.files) == {"points", "squared_norm", "inner_product_limit",
                                "coordinate_denominator"}
        P = z["points"]
    assert P.dtype == np.int16 and P.shape == (232154, 29)
    with np.load(trade, allow_pickle=False) as z:
        assert set(z.files) == {"rays", "squared_norms", "drop", "coordinates"}
        rays, norms, drop, coords = z["rays"], z["squared_norms"], z["drop"], z["coordinates"]
    assert rays.shape == (14, 13) and coords.shape == (13,) and drop.shape == (11,)
    assert len(set(coords.tolist())) == 13 and coords.min() >= 0 and coords.max() < 29
    assert len(set(drop.tolist())) == 11 and drop.min() >= 0 and drop.max() < 232154
    R = rays.astype(np.int64)
    assert ((R * R).sum(1) == norms).all()
    new = np.zeros((14, 29), dtype=np.int64)
    for i in range(14):
        f = math.isqrt(128 // int(norms[i]))
        assert 128 % int(norms[i]) == 0 and f * f * int(norms[i]) == 128
        new[i, coords] = f * R[i]
    keep = np.ones(232154, dtype=bool)
    keep[drop] = False
    F = np.concatenate([P[keep].astype(np.int64), new])
    assert F.shape == (232157, 29) and ((F * F).sum(1) == 128).all() and np.abs(F).max() <= 127
    h = hashlib.sha256(F.astype("<i2").tobytes()).hexdigest()
    print(f"rows {F.shape[0]}: parent 232154 - 11 dropped + 14 new; all squared norms 128")
    print(f"int16 sha256 {h} {'== manifest' if h == FINAL_INT16_SHA else '!= manifest (row order may differ)'}")
    F.astype(np.int8).tofile(out)
    print(f"-> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
