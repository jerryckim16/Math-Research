"""Pack a run_tree.py output file into a compact gzipped certificate file.

Each allocation is written as a string of owner digits ("01230123"); all
other fields are kept, except that timeout records drop nothing (they carry
no allocations).  recheck_cvc5.py reads both forms (and .gz files).

Usage: python3 pack_certs.py RUN.jsonl data/OUT.jsonl.gz
"""
import gzip
import json
import sys

src, dst = sys.argv[1], sys.argv[2]
with open(src) as f, gzip.open(dst, "wt") as g:
    for line in f:
        r = json.loads(line)
        if r.get("allocs") is not None:
            r["allocs"] = ["".join(map(str, a)) for a in r["allocs"]]
        r.pop("stats", None)
        g.write(json.dumps(r, separators=(",", ":")) + "\n")
