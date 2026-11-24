"""Convert a pinned Kravatskiy coordinate file (.npz, see fetch_kravatskiy.py)
into the input formats of our own checkers. Our own parser: only numpy's
.npy reader with allow_pickle=False is used; no repository code is run.

Two layouts occur at commit 907f9b1f:
  points   int16 (n, d)                 point = points / 2
  rational, radical int16 (n, d), radicand 3
                                        point = (rational + sqrt3 * radical) / 2
The positive factor 1/2 does not change angles, so we keep the integer
numerators. The stored metadata (squared_norm 128, inner_product_limit 64,
coordinate_denominator 2) is only compared with what we compute; the checks
themselves use the angle criterion p <= 0 or 4p^2 <= AB on the numerators.

Output:
  OUT.i8          int8 rows with no radical part (all rows if there is none)
  OUT_field.json  rows with a radical part, in kiss_check_field.py's format
                  [C0, C1, C2, C3] = [rational, 0, radical, 0]  (only if any)

Negative controls (--variant, for files with sqrt3 rows; each must FAIL):
  dupfield   append a second copy of the first sqrt3 row
  conjfield  replace the first sqrt3 row (R + sqrt3 S)/2 by its conjugate
             (R - sqrt3 S)/2 (same norm, different point; reported outcome)

Usage: python3 -I load_kravatskiy.py IN.npz OUTPREFIX N D [--variant V]
       (N, D: the claimed count and dimension, asserted)
"""
import json
import sys

import numpy as np


def main(path, prefix, n, d, variant=None):
    with np.load(path, allow_pickle=False) as z:
        keys = set(z.files)
        if keys == {"points", "squared_norm", "inner_product_limit",
                    "coordinate_denominator"}:
            rat = z["points"]
            rad = np.zeros_like(rat)
        elif keys == {"rational", "radical", "radicand", "squared_norm",
                      "inner_product_limit", "coordinate_denominator"}:
            rat, rad = z["rational"], z["radical"]
            assert int(z["radicand"]) == 3
        else:
            raise SystemExit(f"unexpected keys {sorted(keys)}")
        meta = {k: int(z[k]) for k in ("squared_norm", "inner_product_limit",
                                        "coordinate_denominator")}
    assert rat.dtype == np.int16 and rad.dtype == np.int16
    assert rat.shape == (n, d) and rad.shape == (n, d), (rat.shape, n, d)
    assert np.abs(rat).max() <= 127 and np.abs(rad).max() <= 127
    rat64, rad64 = rat.astype(np.int64), rad.astype(np.int64)
    # exact squared norm of the numerator: |R|^2 + 3|S|^2 + 2 sqrt3 R.S
    n0 = (rat64 * rat64).sum(1) + 3 * (rad64 * rad64).sum(1)
    n3 = 2 * (rat64 * rad64).sum(1)
    assert (n3 == 0).all(), "a squared norm has a sqrt3 part"
    norms = sorted(set(n0.tolist()))
    is_field = (rad != 0).any(1)
    bulk = rat[~is_field].astype(np.int8)
    bulk.tofile(prefix + ".i8")
    print(f"rows={n} d={d} numerator_squared_norms={norms} metadata={meta}")
    print(f"bulk rows (no sqrt3 part): {bulk.shape[0]} -> {prefix}.i8")
    if is_field.any():
        rows = [[r.tolist(), [0] * d, s.tolist(), [0] * d]
                for r, s in zip(rat64[is_field], rad64[is_field])]
        if variant == "dupfield":
            rows.append(rows[0])
        elif variant == "conjfield":
            rows[0] = [rows[0][0], rows[0][1], [-x for x in rows[0][2]], rows[0][3]]
        elif variant is not None:
            raise SystemExit("unknown variant")
        with open(prefix + "_field.json", "w") as f:
            json.dump({"d": d, "rows": rows}, f)
        print(f"field rows (sqrt3 part): {len(rows)} -> {prefix}_field.json")


if __name__ == "__main__":
    v = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else None
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), v)
