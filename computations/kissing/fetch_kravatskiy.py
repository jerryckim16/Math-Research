"""Download A. Kravatskiy's 25-33D kissing configurations (the values in the
17 Nov 2026 snapshot of Cohn's table kept in the same repository, or newer),
and pin them by sha256: complete coordinate files for 26, 27, 28, 30, 31;
the exact witness for 25, the parent file plus trade for 29, and the
compact witnesses for 32 and 33; with --with-34-39, the parent files and
edit recipes from which build_kravatskiy34.py ... build_kravatskiy39.py
rebuild the 34-39D records; with --with-40-43, the affine-shell data from
which build_kravatskiy4043.py rebuilds the 40-43D records; with --with-45,
the 45D family table and class geometry read by build_kravatskiy45.py.

Source: https://github.com/alexlegeartis/KissingNumbers at commit
907f9b1f4c5f8bb4196ea03775f60cc260189789 (2026-11-23), fetched 2026-11-24
from raw.githubusercontent.com. Not an arXiv paper: a public repository.
The files are treated as untrusted data: each is checked against the sha256
pinned below before load_kravatskiy.py parses it (numpy, allow_pickle=False).
None of the repository's code is run.

Usage: python3 -I fetch_kravatskiy.py OUTDIR [--with-34-39] [--with-40-43] [--with-45]
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

# 34-39D: every file the chain rebuilders read (local name, repository path
# under verifications/improved/, sha256). Where the author's own scripts pin
# a hash for a file, it is the same as the one below.
EXTRA_34_39 = [
    # 34D: parent certificate (390,992 points) and the edit recipe
    ("k34_parent_rotated34.json", "dim32-35-signed-layers/rotated34/certificate.json",
     "36a9017be6de898d16bdfdad1b686db1d991a9be8a77a804134d770794a5f7ea"),
    ("k34_witness.json", "dim34-octad-switches/witness.json",
     "87da7c9bab1f0a0f3dc627b8e88a5cfde3815745a1c74e7ce70c405c2e6d1dd3"),
    # 35D: code data (dense code, 2,202 supports with parities), dense
    # positions and heads, 7 octad switches, final stars/roots/heads
    ("k35_code_data.json", "dim35-shared-root-heads/code_data.json",
     "0f44ca2ff564941d58f92cbb0c47ada139612196fd3d69a547d5318f78009d05"),
    ("k35_full_parities.json", "dim35-shared-root-heads/full_parities.json",
     "e156ae604938772d9d41e9b2a39af5602fcc7f8bf7f242c35695a4f2a9218c24"),
    ("k35_shared_positive.npz", "dim35-shared-root-heads/shared_positive.npz",
     "9d4b35ac5d18f40011282ec2e83753bdffee947351584a77a910baef875768cf"),
    ("k35_switch_witness.json", "dim35-octad-switches/witness.json",
     "3e8a212b8a8ee4c6d81a45134dae67b99fbfbc4a4f990fc174c42af987e01e16"),
    ("k35_replacement.npz", "dim35-joint-star-root/replacement.npz",
     "ffb73e3082a0ed5a1f94ce8e5c32febb0683e151bcd1aee3838eb52a6e76320c"),
    # 36D: Coxeter-Todd base certificate and the three edit steps
    ("k36_nonlocal.json", "dim36-ct-nonlocal/certificate.json",
     "c4598a0dfc49365ae2b082745454c38b53b76703e5eef5dafbd71e2d06c59180"),
    ("k36_triangle.json", "dim36-ct-triangle-refill/certificate.json",
     "8ef795fd0b034e913e28c05b36f43c80cf274f78dd2af2bb8a07b1488bc8c306"),
    ("k36_double.json", "dim36-ct-double-trine/witness.json",
     "ad81a8abdfb10889b7f7826b5f4823fa355f415e7cca4083d092167faed13b08"),
    ("k36_final.json", "dim36-ct-neutral-reheat/witness.json",
     "5327877dfd99b826787391c9ecdb76db9f58747ae693f8540ef03f0b3b678c93"),
    # 37D: Yang et al.'s length-38 code, 168 radical six-supports, flat refill
    ("k37_dense_parent38.json", "dim37-qr-flat-repack/dense_parent38.json",
     "addcc62d2757f68c31fda2af630e1f41a46948c58d42a24d981e2b8291336108"),
    ("k37_six.txt", "dim37-qr-flat-repack/six.txt",
     "f8f9fbe495ae1696b8b1d4f34ad0f001a066390d7886d2cd360ca8bb75122f39"),
    ("k37_win.txt", "dim37-qr-flat-repack/win.txt",
     "956a00ddc257713eabaff9f05d14e0f050d87591d317eba2cbb6db3cedb1d532"),
    # 38D: Lin's 3,088 supports, Yang et al.'s length-39 code, fibre syndromes,
    # 10 octad switches and 18 star templates
    ("k38_supports_3088.txt", "dim37-38-qr-merge/supports_3088.txt",
     "ccb530f90e914df84cbc8d19a71d30c79146d23a2e8e86e7a813d4d92a5a6a8b"),
    ("k38_dense_parent39.json", "dim37-38-qr-merge/dense_parent39.json",
     "72877e1101a4d33f96646f43d64a6688c3bb2baa56ada85df3c76017c4d14365"),
    ("k38_offset_witness.txt", "dim38-qr-free-offsets/offset_witness.txt",
     "5aa1467c25cf81d6cd6c7b813719a378e4c35f105b1725e49b727dfcdec1c9d4"),
    ("k38_witness.json", "dim38-qr-octad-switches/witness.json",
     "44ccacbe5d4b5a27f54c236e58c78629e02a5136c90db1e65bf7c32943b54a0e"),
    # 39D: length-39 code and fibres, 7 support switches and 4 stars, heads;
    # the gzipped supports decompress to Lin's supports_3424.txt (sha256
    # 5e750c76..., the file pinned in fetch_lin.py)
    ("k39_parent39.json", "dim39-qr-three-coordinate-heads/parent39.json",
     "72877e1101a4d33f96646f43d64a6688c3bb2baa56ada85df3c76017c4d14365"),
    ("k39_base_certificate.json", "dim39-qr-three-coordinate-heads/base_certificate.json",
     "2c7188449cd0b93bd0e9eec3d408e087b3e4763d22202ed63adf4403bc08ecd9"),
    ("k39_certificate.json", "dim39-qr-three-coordinate-heads/certificate.json",
     "38ca2a117f325bc919bd8f9649ae664b87c4d1ff81b6bf9fbbf1b458b17835a8"),
    ("k39_supports_3424.txt.gz", "dim39-qr-three-coordinate-heads/supports_3424.txt.gz",
     "105c2bc72b3e30129841fdc59ae2c2000d3841cae63d83f34fb8c2cdcbc3bcce"),
]


# 40-43D: the affine-shell data read by build_kravatskiy4043.py (local name,
# repository path, sha256). The author publishes no hashes for these files.
EXTRA_40_43 = [
    ("k40_certificate.json", "dim40-p48q-affine-refill/certificate.json",
     "d0a2cf0f78426227d6f425f00417171be6f26f9b7cbb9c5cba89ef5938e5dce4"),
    ("k40_gram.json", "dim40-p48q-affine-refill/gram.json",
     "39fed03448ab268281fe3adca9b034ddab65517043e0c9c719dc3774fa611878"),
    ("k40_points.npz", "dim40-p48q-affine-refill/points.npz",
     "dfe4e78c885cbffde6f6c0c030d86f9c79d9b1f8e4353d97c183d4649b9f1a26"),
    ("k41_configuration.npz", "dim41-43-affine-sections/configuration_41.npz",
     "1a63c971f8357d81236e07dbc6c4d70e4b0ec03ada0e3b8aa9811bc08a6daaf8"),
    ("k42_configuration.npz", "dim41-43-affine-sections/configuration_42.npz",
     "3aefb185461e52af9de83eace3b44b7f2f11171ada39da821a2fcb55b4a85713"),
    ("k43_configuration.npz", "dim41-43-affine-sections/configuration_43.npz",
     "bea1c397aa6b69c47f786564e402423bc892f5966e4e9899808b6598f2669870"),
]


# 45D (7,655,056 points): the family table (class index, r3, weight, head
# numerators over one denominator, pure directions) and the class geometry
# (body Gram matrix and the 3^8 class residues) read by build_kravatskiy45.py.
# Both sha256 equal the author's dim41-46-p48-heads/data/SHA256SUMS.txt.
EXTRA_45 = [
    ("k45_configuration.npz", "dim41-46-p48-heads/coordinated45/configuration.npz",
     "bb4bddd2edba731a06934715dbe62c78ab15fb56b75b0e1bb08aacf799b268b5"),
    ("k45_geometry.npz", "dim41-46-p48-heads/coordinated45/geometry.npz",
     "6c854f55c485866505fffce7ed8efc792c43bc5489a31d447089e4086e65444f"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(out, with3439=False, with4043=False, with45=False):
    os.makedirs(out, exist_ok=True)
    for n, d, rel, digest in FILES:
        path = os.path.join(out, f"krav{d}_{n}.npz")
        if not os.path.exists(path) or sha256(path) != digest:
            urllib.request.urlretrieve(RAW + rel, path)
        got = sha256(path)
        if got != digest:
            raise SystemExit(f"{rel}: sha256 {got} != pinned {digest}")
        print(f"{d} {n} sha256 OK -> {path}")
    for name, rel, digest in (EXTRA + (EXTRA_34_39 if with3439 else [])
                              + (EXTRA_40_43 if with4043 else []) + (EXTRA_45 if with45 else [])):
        path = os.path.join(out, name)
        if not os.path.exists(path) or sha256(path) != digest:
            urllib.request.urlretrieve(RAW + rel, path)
        if sha256(path) != digest:
            raise SystemExit(f"{rel}: sha256 mismatch")
        print(f"{rel} sha256 OK -> {path}")


if __name__ == "__main__":
    main(sys.argv[1], "--with-34-39" in sys.argv, "--with-40-43" in sys.argv, "--with-45" in sys.argv)
