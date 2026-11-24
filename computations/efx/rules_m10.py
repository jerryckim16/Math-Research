"""Failed route (problem file, Approach 6): rule-based allocations when the four
agents have distinct favourite goods.

l1_allocs: AFM's Lemma L1 rule (arXiv:2608.08590): every agent takes its top
  good; for a chosen agent k, the other three (in a chosen order) each take a
  favourite remaining good; k takes all leftovers.  4 x 6 = 24 variants.
rr_allocs: every agent takes its top good, then round robin in one of the 24
  agent orders until the goods run out.
We report how often *no* variant is EFX (exact check by efx.verify).
Usage: python3 rules_m10.py
"""
import itertools
import random

import efx


def tops(v, m):
    t = [max(range(m), key=lambda g: v[i][g]) for i in range(4)]
    return t if len(set(t)) == 4 else None


def l1_allocs(v, m):
    t = tops(v, m)
    if t is None:
        return None
    res = []
    for k in range(4):
        for order in itertools.permutations([i for i in range(4) if i != k]):
            alloc = [-1] * m
            for i in range(4):
                alloc[t[i]] = i
            for i in order:
                rem = [g for g in range(m) if alloc[g] < 0]
                alloc[max(rem, key=lambda g: v[i][g])] = i
            res.append([k if a < 0 else a for a in alloc])
    return res


def rr_allocs(v, m):
    t = tops(v, m)
    if t is None:
        return None
    res = []
    for order in itertools.permutations(range(4)):
        alloc = [-1] * m
        for i in range(4):
            alloc[t[i]] = i
        for i in list(order) * m:
            rem = [g for g in range(m) if alloc[g] < 0]
            if not rem:
                break
            alloc[max(rem, key=lambda g: v[i][g])] = i
        res.append(alloc)
    return res


def run(m, fam, N, seed):
    rng = random.Random(seed)
    tried = f1 = f2 = fu = 0
    while tried < N:
        if fam == "uniform":
            v = [[rng.randint(0, 1000) for _ in range(m)] for _ in range(4)]
        else:
            base = [rng.randint(500, 1000) for _ in range(m)]
            v = [[b + rng.randint(-30, 30) for b in base] for _ in range(4)]
        if any(sorted(r)[-1] == sorted(r)[-2] for r in v):
            continue
        A = l1_allocs(v, m)
        if A is None:
            continue
        tried += 1
        a = any(efx.verify(v, x) for x in A)
        b = any(efx.verify(v, x) for x in rr_allocs(v, m))
        f1 += not a
        f2 += not b
        fu += not (a or b)
    print(f"m={m} {fam}: {tried} instances with distinct strict favourites; "
          f"L1 fails {f1}, tops+RR fails {f2}, both fail {fu}")


if __name__ == "__main__":
    run(9, "uniform", 20000, 9)
    run(10, "uniform", 30000, 7)
    run(10, "near", 30000, 7)
