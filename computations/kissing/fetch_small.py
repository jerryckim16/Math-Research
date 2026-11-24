"""Download the 841-point kissing configuration in R^12 of Takhanov,
Assylbekov and Yun (arXiv:2606.18984v2) and pin it by sha256.

Source: https://github.com/k-nic/841_in_12D at commit
eba37f0368f62828780d1f9d90315b367d2a612f (2026-06-22), file
gram841_coordinates.txt (841 lines of 12 decimal literals), fetched
2026-11-24 from raw.githubusercontent.com. Untrusted data: check_decimal.py
parses it with our own code (fractions.Fraction on each literal).

Usage: python3 -I fetch_small.py OUTDIR
"""
import hashlib
import os
import sys
import urllib.request

URL = ("https://raw.githubusercontent.com/k-nic/841_in_12D/"
       "eba37f0368f62828780d1f9d90315b367d2a612f/gram841_coordinates.txt")
SHA = "995264fe8be616cc546f04ef542dbf4ef6effe9ba5dfa4ceec1aa7e069f476a9"


def main(out):
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "tay12_841.txt")
    if not os.path.exists(path) or hashlib.sha256(open(path, "rb").read()).hexdigest() != SHA:
        urllib.request.urlretrieve(URL, path)
    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if got != SHA:
        raise SystemExit(f"gram841_coordinates.txt: sha256 {got} != pinned {SHA}")
    print(f"12D 841 sha256 OK -> {path}")


if __name__ == "__main__":
    main(sys.argv[1])
