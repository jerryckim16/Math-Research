"""Spot check of the terminal level-14 step of Allikvere's LRC(13) proof
(arXiv:2609.02604v2 Section 4.3; Zenodo 10.5281/zenodo.22066772,
fourteen_lonely_runners_package.zip), read as data only.

For each chosen gate p and each persistent orbit kill record
(kill_orbit*.txt: base tuple, its improper level-2 members, and per member
"witness_improper=N improper_after_gcd7=M"), we recompute with our own
code (liftfree.c + gcd clause):
  * the improper level-2 lifts of the base (must equal the listed members,
    as sets of sorted tuples);
  * for every member, all witness-free lifts to level 14 (c = 7) and how
    many of them fail the gcd clause at l = 14.
Pass: identical numbers and improper_after_gcd7 = 0 everywhere.
Also: the SHA-256 of each kill file against the gate's MANIFEST_SHA256.json
when the manifest lists it.
The level-one rows for k = 13 are not stored in this archive (only logs),
so level-one soundness/completeness and the binary cascade are NOT checked.

Usage: python3 check_lrc13_kills.py fourteen_lonely_runners_package.zip p [p ...]
"""
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile

import check_allikvere as ca
from check_gate_full import binary


def compute(k, p, base):
    wf2 = ca.witness_free_lifts(k, p, 2, [base]).get(0, [])
    members = [w for w in wf2 if not ca.gcd_clause(w, 2)]
    ours = {}
    for w in members:
        res = subprocess.run([binary("liftfree"), str(k), str(2 * p), "7"], input=" ".join(map(str, w)) + "\n",
                             capture_output=True, text=True, check=True)
        lifts = [tuple(map(int, l.split()[1:])) for l in res.stdout.splitlines()]
        ours[tuple(sorted(w))] = (len(lifts), sum(1 for x in lifts if not ca.gcd_clause(x, 14)))
    return members, ours


def main():
    z = zipfile.ZipFile(sys.argv[1])
    names = z.namelist()
    k = 13
    for p in map(int, sys.argv[2:]):
        t0 = time.time()
        kf = sorted(n for n in names if re.search(r"/p%d/kill_orbit\d+\.txt$" % p, n))
        mans = [n for n in names if re.search(r"certificates_p%d/MANIFEST_SHA256\.json$" % p, n)]
        # manifest keys are relative to the directory holding certificates_p<p>/
        man = {}
        for m in mans:
            root = m.rsplit("/", 2)[0] + "/"
            try:
                d = json.loads(z.read(m))
            except Exception:
                continue
            ent = d.get("files", d) if isinstance(d, dict) else {}
            for key, val in (ent.items() if isinstance(ent, dict) else []):
                hv = val if isinstance(val, str) else (val.get("sha256") if isinstance(val, dict) else None)
                if hv:
                    man[root + key] = hv
        rep = {"p": p, "kill_files": len(kf), "mismatches": [], "orbits": []}
        cache = {}
        sha_ok = sha_missing = 0
        for n in kf:
            data = z.read(n)
            hv = man.get(n)
            if hv is None:
                sha_missing += 1
            elif hv == hashlib.sha256(data).hexdigest():
                sha_ok += 1
            else:
                rep["mismatches"].append({"what": "kill file SHA-256 differs from manifest", "file": n})
            txt = (data.decode("utf-16") if data[:2] in (b"\xff\xfe", b"\xfe\xff") else data.decode()).replace("\r\n", "\n")
            base = tuple(map(int, re.search(r"base: ([\d ]+)\n", txt).group(1).split()))
            comps = re.findall(r"=== level-2 tuple: ([\d ]+)\n(.*?)(?==== level-2 tuple|\Z)", txt, re.S)
            cert = {}
            for tup, body in comps:
                wi = sum(int(x) for x in re.findall(r"witness_improper=(\d+)", body))
                ig = sum(int(x) for x in re.findall(r"improper_after_gcd7=(\d+)", body))
                cert[tuple(sorted(map(int, tup.split())))] = (wi, ig)
            if base in cache:
                members, ours = cache[base]
            else:
                members, ours = compute(k, p, base)
                cache[base] = (members, ours)
            ok = ours == cert and all(v[1] == 0 for v in ours.values())
            rep["orbits"].append({"file": n, "base": base, "level2_members": len(members), "ours": sorted(ours.values()),
                                  "cert": sorted(cert.values()), "match": ok})
            if not ok:
                rep["mismatches"].append({"what": "kill differs", "file": n, "base": base,
                                          "ours": {str(a): b for a, b in ours.items()},
                                          "cert": {str(a): b for a, b in cert.items()}})
            continue
            for w in members:
                res = subprocess.run([binary("liftfree"), str(k), str(2 * p), "7"], input=" ".join(map(str, w)) + "\n",
                                     capture_output=True, text=True, check=True)
                lifts = [tuple(map(int, l.split()[1:])) for l in res.stdout.splitlines()]
                ours[tuple(sorted(w))] = (len(lifts), sum(1 for x in lifts if not ca.gcd_clause(x, 14)))
            ok = ours == cert and all(v[1] == 0 for v in ours.values())
            rep["orbits"].append({"base": base, "level2_members": len(members), "ours": sorted(ours.values()),
                                  "cert": sorted(cert.values()), "match": ok})
            if not ok:
                rep["mismatches"].append({"what": "kill differs", "base": base, "ours": {str(a): b for a, b in ours.items()},
                                          "cert": {str(a): b for a, b in cert.items()}})
        rep["kill_file_sha_ok"] = sha_ok
        rep["kill_file_sha_not_in_manifest"] = sha_missing  # e.g. duplicate copies elsewhere in the zip
        rep["pass"] = not rep["mismatches"] and len(kf) > 0
        rep["seconds"] = round(time.time() - t0, 1)
        print(json.dumps(rep), flush=True)


if __name__ == "__main__":
    main()
