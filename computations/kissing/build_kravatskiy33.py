"""Rebuild A. Kravatskiy's 370,528-point kissing configuration in R^33 from his
compact witness (repository alexlegeartis/KissingNumbers @ 907f9b1f, package
verifications/improved/dim33-joint-signed-refill, witness.npz), with our own
code. The witness is untrusted data, read with numpy's .npy reader
(allow_pickle=False). None of the repository's code is run.

Witness fields and the points they define (squared norm 32 throughout):
  dense_generator (17 x uint64), dense_shift, dense_positions (32 ints):
      the binary code C spanned by the 17 generators (32-bit masks), shifted
      by dense_shift. For each word c, the point with entry (-1)^(bit i of c)
      at coordinate dense_positions[i] (i = 0..31), 0 elsewhere.
      2^17 = 131,072 points.
  supports (1837 x uint64), parity (1837 x int8):
      for each support, all 128 sign patterns of +-2 on its 8 coordinates
      whose number of minus signs has the given parity. 235,136 points.
  sparse (4320 x 33 int16): explicit rows (signed octads, signed stars with
      a +-4 centre and four +-2 leaves, signed roots +-4 +-4).
Bit conventions: bit i (LSB = 0) of a dense word goes to dense_positions[i]
(which is the identity here), and bit j of a support mask is coordinate j
("lsb", the default). With this reading the set passes our check. The
mirrored support reading (bit j = coordinate 32 - j, "msb", kept as an
option and as a negative control) fails with 130,552 violations. The check
is of the points we build: a passing set of 370,528 points is a kissing
configuration whatever the reading, so a misreading could only make a valid
set fail, never make an invalid set pass.

Output: OUT.i8 (370,528 x 33 int8). Usage:
  python3 -I build_kravatskiy33.py witness.npz OUT.i8 [--support-order msb|lsb]
"""
import hashlib
import itertools
import sys

import numpy as np

SHA = "90d130ba1bb96172fae7b7ae10d1169747b76f2e720946bc2350c99a08d427c9"
D = 33


def main(path, out, order="lsb"):
    assert hashlib.sha256(open(path, "rb").read()).hexdigest() == SHA, "sha256 mismatch"
    with np.load(path, allow_pickle=False) as z:
        assert set(z.files) == {"supports", "parity", "dense_generator", "dense_shift",
                                "dense_positions", "sparse"}
        sup = [int(x) for x in z["supports"]]
        par = [int(x) for x in z["parity"]]
        gen = [int(x) for x in z["dense_generator"]]
        shift = int(z["dense_shift"])
        pos = [int(x) for x in z["dense_positions"]]
        sparse = z["sparse"].astype(np.int64)
    assert len(gen) == 17 and len(pos) == 32 and len(set(pos)) == 32
    assert all(0 <= p < D for p in pos) and all(g < 2**32 for g in gen) and shift < 2**32
    # dense layer: span of the generators (must have 2^17 distinct words)
    words = {0}
    for g in gen:
        words |= {w ^ g for w in words}
    assert len(words) == 2**17, "generators are not independent"
    words = sorted(w ^ shift for w in words)
    W = np.array(words, dtype=np.uint64)
    bits = ((W[:, None] >> np.arange(32, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(np.int64)
    dense = np.zeros((len(words), D), dtype=np.int64)
    dense[:, pos] = 1 - 2 * bits
    # complete signed octad families
    assert len(sup) == 1837 == len(par)
    fam = []
    signs = np.array(list(itertools.product((1, -1), repeat=8)), dtype=np.int64)
    neg = (signs < 0).sum(1) % 2
    for s, p in zip(sup, par):
        coords = sorted((D - 1 - j) if order == "msb" else j for j in range(D) if s >> j & 1)
        assert len(coords) == 8 and s < 2**D and p in (0, 1)
        block = np.zeros((128, D), dtype=np.int64)
        block[:, coords] = 2 * signs[neg == p]
        fam.append(block)
    octs = np.concatenate(fam)
    assert sparse.shape == (4320, D)
    X = np.concatenate([dense, octs, sparse])
    nrm = (X * X).sum(1)
    assert X.shape == (370528, D) and (nrm == 32).all() and np.abs(X).max() <= 4
    print(f"dense {dense.shape[0]} + octad families {octs.shape[0]} + sparse {sparse.shape[0]}"
          f" = {X.shape[0]} rows, all squared norm 32")
    X.astype(np.int8).tofile(out)
    print(f"-> {out}")


if __name__ == "__main__":
    order = sys.argv[sys.argv.index("--support-order") + 1] if "--support-order" in sys.argv else "lsb"
    assert order in ("msb", "lsb")
    main(sys.argv[1], sys.argv[2], order)
