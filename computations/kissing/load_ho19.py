"""Convert B. S. Ho's 11,948-point configuration in R^19 (arXiv:2603.10425v3,
github.com/boonsuan/kissing @ 55225e51, data/dimension19_11948.txt) into an
int8 row file for kiss_check.c, with our own parser (untrusted text).

File format: four header lines ("Dimension: 19", "Number of points: 11948",
"Inner product coefficients: 1,...,1", i.e. the standard inner product, and
"Points:"), then one point per line, 19 comma-separated entries. Each entry
is an integer or +-sqrt(8/19). We require every row to be either all-integer or
all +-sqrt(8/19); a row of the second kind is divided by sqrt(8/19) (a
positive factor, which does not change angles), giving a +-1 sign vector of
squared norm 19. Integer rows keep squared norm 8.

Usage: python3 -I load_ho19.py dimension19_11948.txt OUT.i8
"""
import hashlib
import sys

import numpy as np

SHA = "c2ea852ba1afe388c2151f80f64c48ecb8d3e6fc97025e45ea0ebc6fff557615"
ROOT = "sqrt(8/19)"


def main(path, out):
    raw = open(path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "sha256 mismatch"
    lines = raw.decode("ascii").splitlines()
    assert lines[0].strip() == "Dimension: 19" and lines[1].strip() == "Number of points: 11948"
    assert lines[2].strip() == "Inner product coefficients: " + ",".join(["1"] * 19)
    assert lines[3].strip() == "Points:"
    rows, kinds = [], {"int": 0, "sign": 0}
    for ln in lines[4:]:
        if not ln.strip():
            continue
        t = [x.strip() for x in ln.split(",")]
        assert len(t) == 19, ln
        if all(x in (ROOT, "-" + ROOT) for x in t):
            rows.append([-1 if x.startswith("-") else 1 for x in t])
            kinds["sign"] += 1
        else:
            rows.append([int(x) for x in t])          # raises on anything else
            kinds["int"] += 1
    X = np.array(rows, dtype=np.int64)
    assert X.shape == (11948, 19) and np.abs(X).max() <= 127
    norms = sorted(set((X * X).sum(1).tolist()))
    print(f"rows {len(X)}: integer {kinds['int']}, sign {kinds['sign']}; squared norms {norms}")
    X.astype(np.int8).tofile(out)
    print(f"-> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
