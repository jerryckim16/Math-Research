"""Download the Qiushi Engine 32-39D kissing configurations, pin and unpack.

Source: release `configuration-vectors-2026-10-12` of
https://github.com/Oxelra-AI/Qiushi-Engine-Kissing-Number-Research
(repository HEAD 39911e4b38c01c4631e06b12a3e0b23a84e403f8 when fetched,
2026-11-24). The files are treated as untrusted data: each is checked
against the sha256 pinned below (which also equals the sha256 the authors
publish in the release's configurationN.json) before it is decompressed.

Usage: python3 -I fetch_qiushi.py OUTDIR
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


def main(out):
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


if __name__ == "__main__":
    main(sys.argv[1])
