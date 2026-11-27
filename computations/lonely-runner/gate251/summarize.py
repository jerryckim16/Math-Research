"""Aggregate the per-shard records of a gate run.

usage: python3 -I summarize.py WORKDIR/pP OUT_DIR
Writes OUT_DIR/shards.jsonl (one record per shard, sorted) and
OUT_DIR/summary.json (totals, histogram, covers by size, re-check totals,
the bases closing at level >= 9 with their traces, completeness of the shard
set).  Exits 1 unless every shard 0..NSH-1 has an ok record.
"""
import glob
import json
import os
import sys


def main():
    D, out = sys.argv[1], sys.argv[2]
    nsh, depth = map(int, open(os.path.join(D, "nshards.txt")).read().split())
    recs = {}
    for f in glob.glob(os.path.join(D, "shard_*.json")):
        r = json.load(open(f))
        recs[r["shard"]] = r
    missing = [i for i in range(nsh) if i not in recs or not recs[i]["ok"]]
    hist, sizes = {}, {}
    tot = {"bases": 0, "minimal_covers": 0, "nodes": 0, "seconds": 0, "sampled_1pct": 0,
           "recheck_level2_batch_survivors": 0, "recheck_per_base": 0}
    for r in recs.values():
        for a, n in r["closed_hist"].items():
            hist[a] = hist.get(a, 0) + n
        for c, n in r["covers_by_size"].items():
            sizes[c] = sizes.get(c, 0) + n
        for key in ("bases", "minimal_covers", "nodes", "seconds", "sampled_1pct"):
            tot[key] += r[key] or 0
        tot["recheck_level2_batch_survivors"] += r["recheck"]["level2_batch_survivors"]
        tot["recheck_per_base"] += r["recheck"]["per_base"]
    high = []
    for i in sorted(recs):                      # logs of finished shards only
        f = os.path.join(D, f"log{i}.json")
        if not os.path.exists(f):
            continue
        for l in open(f):
            j = json.loads(l)
            high.append({"base": j["base"], "empty_at": j["empty_at"], "trace": j["trace"]})
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "shards.jsonl"), "w") as f:
        for i in sorted(recs):
            f.write(json.dumps(recs[i]) + "\n")
    summary = {"nshards": nsh, "depth": depth, "shards_ok": nsh - len(missing), "missing_or_failed": missing,
               "totals": tot, "closed_hist": dict(sorted(hist.items(), key=lambda t: int(t[0]))),
               "covers_by_size": dict(sorted(sizes.items(), key=lambda t: int(t[0]))),
               "bases_closing_at_level_ge9": len(high),
               "max_level": max((int(a) for a in hist), default=None)}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=1)
    with open(os.path.join(out, "level_ge9_bases.jsonl"), "w") as f:
        for h in high:
            f.write(json.dumps(h) + "\n")
    print(json.dumps({k: summary[k] for k in ("shards_ok", "closed_hist", "covers_by_size", "max_level")}))
    print("totals", tot)
    sys.exit(0 if not missing else 1)


if __name__ == "__main__":
    main()
