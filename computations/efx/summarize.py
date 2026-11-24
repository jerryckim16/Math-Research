"""Aggregate data/*.jsonl into the coverage tables of problems/efx-allocations.md."""
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rand = collections.defaultdict(lambda: [0, 0])
climb = collections.defaultdict(list)
cands = []
for f in sorted(glob.glob(os.path.join(HERE, "data", "*.jsonl"))):
    for line in open(f):
        r = json.loads(line)
        if r.get("COUNTEREXAMPLE_CANDIDATE") or r.get("status") == "COUNTEREXAMPLE_CANDIDATE":
            cands.append((os.path.basename(f), r))
        if r.get("mode") == "random" and r.get("final"):
            for k, (t, bad) in r["stats"].items():
                fam, m = k.split("/")
                rand[(m, r["B"], fam)][0] += t
                rand[(m, r["B"], fam)][1] += bad
        if r.get("mode") == "climb" and "best" in r:
            climb[(r["m"], r["objective"], r["family"] if r["family"] == "diagonal" else "mixed")].append(r)

print("## random search (exact check of every instance)")
print("| m | B | family | instances | without EFX |")
print("| --- | --- | --- | --- | --- |")
tot = collections.Counter()
for (m, B, fam), (t, bad) in sorted(rand.items()):
    print(f"| {m[1:]} | {B} | {fam} | {t:,} | {bad} |")
    tot[(m, B)] += t
print()
for (m, B), t in sorted(tot.items()):
    print(f"total m={m[1:]} B={B}: {t:,}")
print("\n## climbs")
for k, rs in sorted(climb.items()):
    best = min(x["best"] for x in rs)
    extra = ""
    if k[1] == "count":
        extra = f", min #EFX allocations {min(x['count'] for x in rs)} of {4 ** k[0]:,}"
    print(f"m={k[0]} objective={k[1]} start={k[2]}: {len(rs)} runs, all EFX: "
          f"{all(x['efx_exists'] for x in rs)}, best objective {best:.3g}{extra}")
print("\n## counterexample candidates:", len(cands))
for f, r in cands:
    print(f, json.dumps(r)[:500])
