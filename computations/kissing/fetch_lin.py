"""Download Q. Lin's certificate archives from Zenodo, pin and unpack them.

Sources (Zenodo, fetched 2026-11-24):
  10.5281/zenodo.23552484  kissing-number-32 v1.1.0 (concept DOI 10.5281/zenodo.23527725)
  10.5281/zenodo.23554809  kissing-numbers-33-39 v1.0.0 (concept DOI 10.5281/zenodo.23554808)
cited in arXiv:2611.03682v1. The archives are untrusted data: their sha256 is
checked before unpacking, and only plain files with safe relative paths are
extracted. Nothing in them is executed.

Usage: python3 -I fetch_lin.py OUTDIR
Prints the two unpacked directories (LIN_DIR_32, LIN_DIR_33_39).
"""
import hashlib
import os
import sys
import urllib.request
import zipfile

ARCHIVES = [
    ("lin32.zip",
     "https://zenodo.org/api/records/23552484/files/QH-Lin/kissing-number-32-v1.1.0.zip/content",
     "683fc500f42a5d3627baf45e45012bb6160218f6de13ee2485ed17c0989ab659",
     "QH-Lin-kissing-number-32-f367a9c"),
    ("lin33_39.zip",
     "https://zenodo.org/api/records/23554809/files/QH-Lin/kissing-numbers-33-39-v1.0.0.zip/content",
     "1a1368fea7a087c75e75c00f84288c87d6249b80ddcac99962fb3a4f74df21f5",
     "QH-Lin-kissing-numbers-33-39-57924f8"),
]

# sha256 of the certificate files that build_lin.py reads (paths relative
# to the unpacked directories); the first also matches Lin's README.
FILES = {
    "QH-Lin-kissing-number-32-f367a9c/certificates/supports_1713.txt":
        "539972293fbfc671477cea1805a5bf70a2208a4c1e60ec122347b5ef8a23c807",
    "QH-Lin-kissing-number-32-f367a9c/gen32_17.txt":
        "fdab115465ccfd9b2f0d0c4e72cc60290aac35af5919b3021966de3bccbe389c",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/gen32_17.txt":
        "fdab115465ccfd9b2f0d0c4e72cc60290aac35af5919b3021966de3bccbe389c",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d33/supports_1852.txt":
        "bb3b91ef3a81aa8028f6d170a4743b5788120b7787a5956aaa2c32e5c1ed51df",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d34/supports_2013.txt":
        "7a385086eca6429dfe439a73d5d02cd73fa47a98e5b749d0b595dbd623765559",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d35/supports_2202.txt":
        "f1049f812373dfbf9473189b4cb5ef8b39bd13c20a9476d881aa3d61f2e448ca",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d37/supports_2860.txt":
        "7eef8762bc47991923b0883d557b8cea05027cf31425e6084921494157430610",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d38/equator_lines_6855.txt":
        "bd64fdea42bc973bc428f2a60daaf21da5bab33f0d26b0c261a7d70b732a86c8",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d39/dense_kernel.txt":
        "6e931af754b792bc3355c4339e8a29b2a319c1be16c8c22c9a76b894ef2e9b32",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d39/dense_representatives.txt":
        "ac6e8d4d4fada750a50e72d788c44c88ff577a491a0537329270e218880365c0",
    "QH-Lin-kissing-numbers-33-39-57924f8/certificates/d39/supports_3424.txt":
        "5e750c76c21aa9e350784624d367cc724a392eb8cb006826613d8dc82321d1cf",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(out):
    os.makedirs(out, exist_ok=True)
    for name, url, digest, top in ARCHIVES:
        z = os.path.join(out, name)
        if not os.path.exists(z) or sha256(z) != digest:
            urllib.request.urlretrieve(url, z)
        got = sha256(z)
        if got != digest:
            raise SystemExit(f"{name}: sha256 {got} != pinned {digest}")
        dest = os.path.join(out, name[:-4])
        with zipfile.ZipFile(z) as zf:
            for info in zf.infolist():
                p = info.filename
                if p.startswith("/") or ".." in p.split("/") or not p.startswith(top + "/"):
                    raise SystemExit(f"unsafe path in {name}: {p}")
            zf.extractall(dest)
        print(f"{name} sha256 OK -> {os.path.join(dest, top)}")
    for rel, digest in FILES.items():
        for name, _, _, top in ARCHIVES:
            if rel.startswith(top):
                path = os.path.join(out, name[:-4], rel)
        got = sha256(path)
        if got != digest:
            raise SystemExit(f"{rel}: sha256 {got} != pinned {digest}")
    print(f"{len(FILES)} certificate files sha256 OK")


if __name__ == "__main__":
    main(sys.argv[1])
