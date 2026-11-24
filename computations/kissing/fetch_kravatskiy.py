"""Download A. Kravatskiy's 25-33D kissing configurations (the values in the
17 Nov 2026 snapshot of Cohn's table kept in the same repository, or newer),
and pin them by sha256: complete coordinate files for 26, 27, 28, 30, 31;
the exact witness for 25, the parent file plus trade for 29, and the
compact witnesses for 32 and 33.

Source: https://github.com/alexlegeartis/KissingNumbers at commit
907f9b1f4c5f8bb4196ea03775f60cc260189789 (2026-11-23), fetched 2026-11-24
from raw.githubusercontent.com. Not an arXiv paper: a public repository.
The files are treated as untrusted data: each is checked against the sha256
pinned below before load_kravatskiy.py parses it (numpy, allow_pickle=False).
None of the repository's code is run.

Usage: python3 -I fetch_kravatskiy.py OUTDIR
"""
import hashlib
import os
import sys
import urllib.request

COMMIT = "907f9b1f4c5f8bb4196ea03775f60cc260189789"
RAW = ("https://raw.githubusercontent.com/alexlegeartis/KissingNumbers/"
       + COMMIT + "/verifications/improved/")

# (claimed bound, dimension, repository path, sha256 of the .npz)
FILES = [
    (201188, 26, "dim26-27-radical-orbits/data/coordinates26_201188.npz",
     "aafeba2a5882ebd658925569211d77ef0a0e793ee17f7f8fbfbdbb3939bdd8c3"),
    (209884, 27, "dim26-27-radical-orbits/data/coordinates27_209884.npz",
     "3eb58e11ef143cb9288fd0860238e5fdd0ae5544386d07154fc12c9d204f2d59"),
    (223528, 28, "dim28-takhanov-root-exchange/data/coordinates28_223528.npz",
     "3556adb1c32b26116bd83df0793e4eca0b007ca1c751da47c50d3e37cb66d5d2"),
    (248506, 30, "dim30-row-midpoint-packing/data/coordinates30.npz",
     "3f875bd8ad5f3dff28f3c3dcdcf8fcea32774cb1f7c610f4115d8828de47a4b7"),
    (251524, 31, "dim30-31-midpoint-exchanges/data/coordinates31_251524.npz",
     "8d8b36e55e86965edb61774bfaf5e39e9a55ede31d6545b7ceadb72f7acacbc5"),
]
# Inputs of the two rebuilt configurations (build_kravatskiy25.py, build_kravatskiy29.py)
EXTRA = [
    ("krav25_certificate25.json", "dim25-critical-cluster/source/certificate25.json",
     "5270afec106a2336179fd8c1d21fd5b9e30da100a8d4f1e6ec4ca3ec8b161299"),
    ("krav29_parent_232154.npz", "dim29-takhanov-auxiliary-exchange/data/coordinates29_232154.npz",
     "5daac8c4449cfaff1e9b73d8d7de9baced5a54f92e84f45a28cc8764a5b5cbd4"),
    ("krav29_trade.npz", "dim29-even-grid-exchange/trade.npz",
     "d85b5cdf65eb128ad55104711cfc57621554de1d31005ad181757b46b2f3f9cd"),
    # 32D and 33D compact witnesses (build_kravatskiy32.py, build_kravatskiy33.py)
    ("krav32_certificate.json",
     "dim32-35-signed-layers/nonantipodal32/certificate32_352992_explicit.json",
     "a21b8ee4086cdbbc90651bcab378b888d0c3f10643aa0d63b5d208cafe471d1a"),
    ("krav33_witness.npz", "dim33-joint-signed-refill/witness.npz",
     "90d130ba1bb96172fae7b7ae10d1169747b76f2e720946bc2350c99a08d427c9"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(out):
    os.makedirs(out, exist_ok=True)
    for n, d, rel, digest in FILES:
        path = os.path.join(out, f"krav{d}_{n}.npz")
        if not os.path.exists(path) or sha256(path) != digest:
            urllib.request.urlretrieve(RAW + rel, path)
        got = sha256(path)
        if got != digest:
            raise SystemExit(f"{rel}: sha256 {got} != pinned {digest}")
        print(f"{d} {n} sha256 OK -> {path}")
    for name, rel, digest in EXTRA:
        path = os.path.join(out, name)
        if not os.path.exists(path) or sha256(path) != digest:
            urllib.request.urlretrieve(RAW + rel, path)
        if sha256(path) != digest:
            raise SystemExit(f"{rel}: sha256 mismatch")
        print(f"{rel} sha256 OK -> {path}")


if __name__ == "__main__":
    main(sys.argv[1])
