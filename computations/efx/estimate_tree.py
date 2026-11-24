"""Stratified / Knuth-style projection of a full refinement-tree run from a
random sample of regions (probe_regions.py output).

Strata (by how many of the 4 agents share a top good; agent 0's top is good 0,
agents 1..3 have argmax branch b_1 <= b_2 <= b_3):
  L1  : b_i distinct and nonzero -> AFM hand Lemma L1 (proved, checked by us
        for m = 9); no computation;
  S2  : exactly one pair shares a top;  S22: two pairs ((0,b,b));
  S3  : three agents share a top ((0,0,b) or (k,k,k));  S4: (0,0,0).
Every branch outside L1 is sent straight to its cubes (as AFM did), so the
projection is (number of cubes in the stratum) x (mean cost per cube).

Cost of a sampled cube:
  closed cube         -> its CEGAR seconds, Z3 full-clause re-solve seconds
                         (measured) and cvc5 seconds 7.8e-4 * a^2 (a =
                         allocations; the m = 8 fit, problem file);
  timed-out cube      -> lower bound: the time limit spent, plus, if children
                         (next refinement layer) were sampled, Knuth's estimate
                         siblings x mean(child cost), where a timed-out child
                         again counts only its time limit (lower bound).
So every number printed is biased LOW whenever a timeout occurs in its
sample; the script says how many.

With --cvc5-times=FILE (probe_regions.py cvc5 output) the coefficient c of
the rule t = c a^2 is also fitted to the measured m-specific cvc5 times
(least squares through 0) and the cvc5 total is printed for both rules.

Usage: python3 estimate_tree.py PROBE.jsonl [...] [--map=S2=226,016,445,116 --map=S3=777 ...]
                               [--cvc5-times=FILE] [--no-knuth]
--no-knuth ignores the sampled children: a timed-out cube then costs only its
time limit (the strict lower bound).
"""
import itertools
import json
import statistics
import sys
from collections import Counter, defaultdict

import cegar_branches as cb

CVC5_COEF = 7.8e-4


def stratum(top):
    if len(set(top)) == 3 and 0 not in top:
        return "L1"
    mult = sorted(Counter((0,) + tuple(top)).values(), reverse=True)
    if mult[0] == 4:
        return "S4"
    if mult[0] == 3:
        return "S3"
    if mult[:2] == [2, 2]:
        return "S22"
    return "S2"


def cube_counts(m, n=4):
    out = Counter()
    for b in itertools.combinations_with_replacement(range(m), n - 1):
        out[stratum(b)] += len(cb.refine([[x] for x in b], m))
    return out


def leaf_costs(r):
    """(cegar, z3_resolve, cvc5_est) of one record that is a closed leaf."""
    a = r["num_allocs"]
    return r["seconds"], r.get("recheck_seconds", 0.0), CVC5_COEF * a * a


def main():
    files = [x for x in sys.argv[1:] if not x.startswith("--")]
    maps = {}
    for x in sys.argv[1:]:
        if x.startswith("--map="):
            k, v = x[6:].split("=")
            maps[k] = v.split(",")
    recs = [r for f in files for r in map(json.loads, open(f)) if "probe" in r]   # sampled records only
    ct = next((x.split("=", 1)[1] for x in sys.argv if x.startswith("--cvc5-times=")), None)
    fit = None
    if ct:
        ts = [t for t in map(json.loads, open(ct)) if "cvc5_seconds" in t]   # skip lower bounds
        fit = sum(t["cvc5_seconds"] * t["num_allocs"] ** 2 for t in ts) / sum(t["num_allocs"] ** 4 for t in ts)
        print(f"cvc5 fit on {len(ts)} measured records (a = {min(t['num_allocs'] for t in ts)}-"
              f"{max(t['num_allocs'] for t in ts)}): t = {fit:.2e} a^2 (m = 8 rule: {CVC5_COEF:.1e});"
              f" all verdicts: {sorted(set(t['cvc5'] for t in ts))}")
    m = recs[0]["m"]
    key = lambda br: json.dumps(br)
    seen = set()          # a region run twice (repeatability check) counts once: first record
    recs = [r for r in recs if not (key(r["branch"]) in seen or seen.add(key(r["branch"])))]
    children = defaultdict(list)
    for r in recs:
        if r["probe"]["layer"] != "cube":
            children[key(r["probe"]["parent"])].append(r)
    groups = defaultdict(list)
    n_to = Counter()
    for r in recs:
        if r["probe"]["layer"] != "cube":
            continue
        g = r["probe"]["group"]
        if r["status"] == "unsat":
            c = leaf_costs(r)
            groups[g].append((c, "closed", r["num_allocs"]))
            continue
        if r["status"] != "timeout":
            print("!!! status", r["status"], r["branch"])
            continue
        n_to[g] += 1
        kids = [] if "--no-knuth" in sys.argv else children.get(key(r["branch"]), [])
        own = (r["seconds"], 0.0, 0.0)
        if not kids:
            groups[g].append((own, "timeout, no children sampled", r["num_allocs"]))
            continue
        sib = kids[0]["probe"]["siblings"]
        kc = []
        for k in kids:
            if k["status"] == "unsat":
                kc.append(leaf_costs(k))
            else:
                n_to[g] += 1
                kc.append((k["seconds"], 0.0, 0.0))
        mean = [sib * statistics.mean(x[t] for x in kc) for t in range(3)]
        groups[g].append(((own[0] + mean[0], mean[1], mean[2]),
                          f"timeout; Knuth over {len(kids)}/{sib} children", r["num_allocs"]))
    print(f"m = {m}: per-group cube costs (CPU-s; lower bounds where timeouts occur)")
    for g, xs in sorted(groups.items()):
        cs = [x[0] for x in xs]
        print(f"  group {g}: {len(xs)} cubes, {n_to[g]} timeouts in sample (cubes + children); "
              f"mean CEGAR {statistics.mean(c[0] for c in cs):.0f}, "
              f"Z3 re-solve {statistics.mean(c[1] for c in cs):.0f}, "
              f"cvc5 est {statistics.mean(c[2] for c in cs):.0f}; "
              f"median CEGAR {statistics.median(c[0] for c in cs):.0f}")
    cc = cube_counts(m)
    print("cubes per stratum:", dict(cc))
    tot = [0.0, 0.0, 0.0]
    for s, gs in sorted(maps.items()):
        cs = [x[0] for g in gs for x in groups.get(g, [])]
        if not cs:
            continue
        mean = [statistics.mean(c[t] for c in cs) for t in range(3)]
        sub = [cc[s] * x / 3600 for x in mean]
        tot = [u + v for u, v in zip(tot, sub)]
        print(f"  {s}: {cc[s]} cubes x mean from groups {gs} ({len(cs)} samples) -> "
              f"CEGAR {sub[0]:.0f} CPU-h, Z3 re-solve {sub[1]:.0f}, cvc5 {sub[2]:.0f}")
    print(f"TOTAL (sample-mean projection; timeouts only at their limit): CEGAR {tot[0]:.0f} CPU-h, Z3 re-solve {tot[1]:.0f}, "
          f"cvc5 {tot[2]:.0f} (m = 8 rule), sum {sum(tot):.0f} CPU-h")
    if fit:
        print(f"  with the fitted cvc5 rule: cvc5 {tot[2] * fit / CVC5_COEF:.0f} CPU-h, "
              f"sum {tot[0] + tot[1] + tot[2] * fit / CVC5_COEF:.0f} CPU-h")


if __name__ == "__main__":
    main()
