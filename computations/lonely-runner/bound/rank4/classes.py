"""Symmetry quotient of admitted rank-r sections from sect.c output.

Equivalence (as in Allikvere's N15_RANK4_SHAPE_CLASSES): all row sign
changes and all row permutations preserving the support profile, followed by
column sign normalisation; the class key is the smallest count vector.
"""
import sys
from itertools import permutations, product


def parse(path):
    types, recs, prof = None, [], None
    for line in open(path):
        if line.startswith("TYPES"):
            types = [tuple(int(x) for x in t.split(",")) for t in line.split()[1:]]
        elif line.startswith("ADM"):
            f = dict(kv.split("=") for kv in line.split()[1:])
            recs.append({"a": int(f["a"]), "g": int(f["g"]), "idx": int(f["idx"]),
                         "A": int(f["A"]), "B": int(f["B"]),
                         "m": tuple(int(x) for x in f["m"].split(","))})
        elif line.startswith("SUMMARY"):
            prof = tuple(int(x) for x in line.split("prof=")[1].split()[0].split(","))
    return types, recs, prof


def canon_col(c):
    for x in c:
        if x:
            return tuple(c) if x > 0 else tuple(-y for y in c)
    return tuple(c)


def group(prof):
    r = len(prof)
    perms = [p for p in permutations(range(r)) if all(prof[p[i]] == prof[i] for i in range(r))]
    return [(p, s) for p in perms for s in product((1, -1), repeat=r)]


def act(types, index, m, p, s):
    out = [0] * len(types)
    for k, c in enumerate(m):
        if c:
            t = types[k]
            nt = canon_col(tuple(s[i] * t[p[i]] for i in range(len(t))))
            out[index[nt]] += c
    return tuple(out)


def classes(types, recs, prof):
    index = {t: k for k, t in enumerate(types)}
    G = group(prof)
    cl = {}
    for rec in recs:
        key = min(act(types, index, rec["m"], p, s) for p, s in G)
        cl.setdefault(key, []).append(rec)
    return cl


def matrix_to_counts(types, M):
    index = {t: k for k, t in enumerate(types)}
    out = [0] * len(types)
    for col in zip(*M):
        if any(col):
            out[index[canon_col(col)]] += 1
    return tuple(out)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        types, recs, prof = parse(path)
        cl = classes(types, recs, prof)
        print(path, prof, "records", len(recs), "classes", len(cl))
        for key, rs in sorted(cl.items(), key=lambda kv: kv[1][0]["g"]):
            print("  g=%d a=%d size=%d" % (rs[0]["g"], rs[0]["a"], len(rs)))
