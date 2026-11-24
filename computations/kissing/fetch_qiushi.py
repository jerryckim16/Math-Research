"""Download the Qiushi Engine 32-39D kissing configurations, pin and unpack.

Source: release `configuration-vectors-2026-10-12` of
https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research
(repository HEAD 39911e4b38c01c4631e06b12a3e0b23a84e403f8 when fetched,
2026-11-24). The files are treated as untrusted data: each is checked
against the sha256 pinned below (which also equals the sha256 the authors
publish in the release's configurationN.json) before it is decompressed.

Usage: python3 -I fetch_qiushi.py OUTDIR [--with-43] [--with-25-27]
--with-43 also fetches the 43D export (release `section-vectors-2026-10-11`,
2,553,792 x 48 int8, 55 MB compressed) and checks the sha256 of the raw
file against the value in the authors' section43-verification.json.
--with-25-27 also fetches the six repository data files from which
build_qiushi2527.py rebuilds the 25D and 27D configurations (no complete
export of those exists), from raw.githubusercontent.com at the pinned commit,
into OUTDIR/src2527/. Their sha256 equal the values in the authors'
constructions/d25/verification.json and constructions/d27/verification.json.
Writes OUTDIR/configurationN.json, OUTDIR/configurationN.i8.gz (or .i64.gz)
and the decompressed raw files OUTDIR/qiushiN.i8 (OUTDIR/qiushi38.i64).
"""
import gzip
import hashlib
import os
import sys
import urllib.request

BASE = ("https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research/"
        "releases/download/configuration-vectors-2026-10-12/")

# (dimension, file, sha256 of the .gz, rows, columns, dtype)
FILES = [
    (32, "configuration32.i8.gz", "f30dfb6fbab85188e294c3350880f37827e08b31f086de45eb3b71f5bd4616f7", 347584, 32, "i8"),
    (33, "configuration33.i8.gz", "40a6ce91a87fcb1bbc709fe6818fb42350dd5b944d8bb44b46093af75ef27dc0", 363968, 33, "i8"),
    (34, "configuration34.i8.gz", "e3e8500d8f420bd95738ba3b30fc5c187edd4b29a66c66dce7a6533b63be8ecd", 384196, 34, "i8"),
    (35, "configuration35.i8.gz", "8dc1a68c61ab6ff39cd11a567b7df2f4388e9fff0ddee44b605f12170936dc12", 409676, 35, "i8"),
    (36, "configuration36.i8.gz", "7f15909a028fcf1b05d1af4d494c8625cc4da5e589f5525b9bf60ea68e18065d", 484760, 36, "i8"),
    (37, "configuration37.i8.gz", "97cd948a35314c4aa014b5ba689803f9a6587248331758dafaa2c480bca93d25", 498024, 37, "i8"),
    (38, "configuration38.i64.gz", "0117193cfe67b4ef369aa4c9b8f9f1b42ec38602af7f96de0df8300632063eca", 591900, 52, "i64"),
    (39, "configuration39.i8.gz", "02591a7a0082e5463898b5c5497dd39818c1ab7f9b8f42597aa2660dcd26b60e", 763668, 39, "i8"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


BASE43 = ("https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research/"
          "releases/download/section-vectors-2026-10-11/")
GZ43 = ("section43.i8.gz", "482660ef7fe595bd069d55d609c736bd54acaa786a6a5cab16581639260b7cbd")
RAW43 = "101491f3864debc2c778ebbe370fe80b033cc9039802de59c54575ea3d4bf4bd"


def fetch43(out):
    gz = os.path.join(out, GZ43[0])
    if not os.path.exists(gz) or sha256(gz) != GZ43[1]:
        urllib.request.urlretrieve(BASE43 + GZ43[0], gz)
    if sha256(gz) != GZ43[1]:
        raise SystemExit("section43.i8.gz: sha256 mismatch")
    raw = os.path.join(out, "qiushi43.i8")
    with gzip.open(gz, "rb") as f, open(raw, "wb") as g:
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            g.write(chunk)
    if sha256(raw) != RAW43 or os.path.getsize(raw) != 2553792 * 48:
        raise SystemExit("qiushi43.i8: raw sha256 or size mismatch")
    print(f"43 {GZ43[0]} sha256 OK (gz and raw) rows=2553792 cols=48 -> {raw}")


COMMIT = "39911e4b38c01c4631e06b12a3e0b23a84e403f8"
RAW = ("https://raw.githubusercontent.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research/"
       + COMMIT + "/constructions/")
SRC2527 = [
    ("d25/baseline-heads.json", "b6b1dff1172ca723595c19bc4daf49448f0e8d04d506033786a8e96afbf515d6"),
    ("d25/repair-points.json", "daeabf4a2614779749bf9a5c30f55d502c830e45a88ef2b52fdbbc7f87703677"),
    ("d27/data/heads27_Y.npy", "e137a6e3b11e6f70a0bc631b474f4ea340078f453893c56d5452513da5264bd1"),
    ("d27/data/heads27_side.npy", "b0e1457e2793db1ddd2fcc23a9110f8f956757ee08e017fac99200cae5199fb2"),
    ("d27/data/heads27_layer2_u.npy", "7d7a4bcd341d9104bad1dc17ac2f6e4daec71c0b2a9ab4b98e1766c12235bca2"),
    ("d27/data/heads27_layer2_line.npy", "f7b018510118faeda6d4d73b28a86ca0c6162bbf0d88da1244262b2c39b95fb7"),
]


def fetch2527(out):
    d = os.path.join(out, "src2527")
    os.makedirs(d, exist_ok=True)
    for rel, digest in SRC2527:
        path = os.path.join(d, os.path.basename(rel))
        if not os.path.exists(path) or sha256(path) != digest:
            urllib.request.urlretrieve(RAW + rel, path)
        if sha256(path) != digest:
            raise SystemExit(f"{rel}: sha256 mismatch")
        print(f"25/27 {rel} sha256 OK -> {path}")


def main(out, with43=False, with2527=False):
    os.makedirs(out, exist_ok=True)
    for dim, name, digest, rows, cols, dt in FILES:
        gz = os.path.join(out, name)
        meta = os.path.join(out, f"configuration{dim}.json")
        if not os.path.exists(meta):
            urllib.request.urlretrieve(BASE + f"configuration{dim}.json", meta)
        if not os.path.exists(gz) or sha256(gz) != digest:
            urllib.request.urlretrieve(BASE + name, gz)
        got = sha256(gz)
        if got != digest:
            raise SystemExit(f"{name}: sha256 {got} != pinned {digest}")
        raw = os.path.join(out, f"qiushi{dim}.{dt}")
        width = 1 if dt == "i8" else 8
        with gzip.open(gz, "rb") as f:
            data = f.read()
        if len(data) != rows * cols * width:
            raise SystemExit(f"{name}: {len(data)} bytes, expected {rows}x{cols}x{width}")
        with open(raw, "wb") as f:
            f.write(data)
        print(f"{dim} {name} sha256 OK rows={rows} cols={cols} -> {raw}")
    if with43:
        fetch43(out)
    if with2527:
        fetch2527(out)


if __name__ == "__main__":
    main(sys.argv[1], "--with-43" in sys.argv[2:], "--with-25-27" in sys.argv[2:])
