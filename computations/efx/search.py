"""Adversarial counterexample search for EFX with 4 additive agents.

Usage:
  python3 search.py random --m 10 --n 4 --seconds 1200 --seed 1 --out FILE
  python3 search.py climb  --m 9  --n 4 --seconds 1200 --seed 1 --out FILE
                           [--objective score|count] [--family near_identical]

Every instance is decided by the exact C checker (efx.exists).  Any instance
with no EFX allocation is re-checked by full enumeration and, for m <= 9, by
the independent pure-Python brute force, and written to the output file with
"COUNTEREXAMPLE_CANDIDATE": true.  Summaries are appended to the output JSONL
every few seconds, so a killed run loses little.

Families (all nonnegative integers):
  uniform        iid U{0..B}
  sparse         iid, each value zero with prob 1/2
  heavy          iid floor(B * U^4)  (few large goods)
  near_identical common base row + small independent noise (AFM's "diagonal")
  common_top     near_identical with one shared huge good
  bivalued       each value in {a, b} (per instance)
  lexi           each agent values goods by distinct powers of 2 (random order)
  graphical      each good valued by at most two agents (multigraph instances)
  two_types      agents of two near-types
  diagonal       shared top good + nearly equal rest + tiny noise (AFM's hard region)
  mixed          random choice of the above
"""
import argparse
import json
import math
import random
import time

import efx

FAMILIES = ["uniform", "sparse", "heavy", "near_identical", "common_top",
            "bivalued", "lexi", "graphical", "two_types", "diagonal"]


def sample(fam, n, m, rng, B=1000):
    if fam == "mixed":
        fam = rng.choice(FAMILIES)
    if fam == "uniform":
        return [[rng.randint(0, B) for _ in range(m)] for _ in range(n)]
    if fam == "sparse":
        return [[rng.randint(1, B) if rng.random() < 0.5 else 0 for _ in range(m)]
                for _ in range(n)]
    if fam == "heavy":
        return [[int(B * rng.random() ** 4) for _ in range(m)] for _ in range(n)]
    if fam in ("near_identical", "common_top"):
        base = [rng.randint(B // 2, B) for _ in range(m)]
        if fam == "common_top":
            base[0] = rng.randint(B, 10 * B)
        eps = rng.choice([1, 3, 10, 30])
        return [[max(0, b + rng.randint(-eps, eps)) for b in base] for _ in range(n)]
    if fam == "diagonal":
        # AFM's hard region: shared top good, the rest nearly equal, tiny
        # per-agent noise (cf. their exhibits vA, vB; scale 10^4)
        L = rng.randint(100, 1100)
        T = int(L * rng.choice([1.05, 1.2, 2, 5, 20, 90]))
        base = [T] + sorted((L + rng.randint(-L // 10, L // 10) for _ in range(m - 1)),
                            reverse=True)
        eps = rng.choice([1, 2, 5, 20])
        return [[max(0, b + rng.randint(-eps, eps)) for b in base] for _ in range(n)]
    if fam == "bivalued":
        a = rng.randint(2, B)
        b = rng.randint(0, a - 1)
        return [[a if rng.random() < 0.5 else b for _ in range(m)] for _ in range(n)]
    if fam == "lexi":
        rows = []
        for _ in range(n):
            p = list(range(m))
            rng.shuffle(p)
            rows.append([2 ** p[g] for g in range(m)])
        return rows
    if fam == "graphical":
        v = [[0] * m for _ in range(n)]
        for g in range(m):
            k = rng.choice([1, 2, 2, 2])
            for i in rng.sample(range(n), k):
                v[i][g] = rng.randint(1, B)
        return v
    if fam == "two_types":
        t = [[rng.randint(0, B) for _ in range(m)] for _ in range(2)]
        eps = rng.choice([0, 1, 5])
        return [[max(0, x + rng.randint(-eps, eps)) for x in t[rng.randint(0, 1)]]
                for _ in range(n)]
    raise ValueError(fam)


def confirm(v):
    """Re-verify a claimed counterexample in every way available."""
    ok_fast, _ = efx.exists(v)
    ok_full, sc, cnt, _ = efx.full(v)
    rec = {"exists_fast": ok_fast, "exists_full": ok_full, "count": cnt, "score": sc}
    n, m = len(v), len(v[0])
    if n ** m <= 4 ** 9:
        rec["exists_brute"] = efx.brute(v)
    return rec


def report_counterexample(out, v, extra):
    rec = confirm(v)
    rec.update(extra)
    rec["COUNTEREXAMPLE_CANDIDATE"] = not (rec["exists_fast"] or rec["exists_full"]
                                           or rec.get("exists_brute", False))
    rec["v"] = v
    print("!!!!!!!! NO EFX ALLOCATION FOUND !!!!!!!!", json.dumps(rec), flush=True)
    out.write(json.dumps(rec) + "\n")
    out.flush()


def run_random(a, out):
    rng = random.Random(a.seed)
    t0 = time.time()
    stats = {}
    last = t0
    tested = 0
    while time.time() - t0 < a.seconds:
        fam = a.family if a.family != "mixed" else rng.choice(FAMILIES)
        m = a.m if a.m > 0 else rng.randint(abs(a.m) // 2, abs(a.m))
        v = sample(fam, a.n, m, rng, a.B)
        ok, wit = efx.exists(v)
        tested += 1
        st = stats.setdefault(f"{fam}/m{m}", [0, 0])
        st[0] += 1
        if not ok:
            st[1] += 1
            report_counterexample(out, v, {"mode": "random", "family": fam})
        elif rng.random() < 1e-3:
            assert efx.verify(v, wit), ("witness failed verification", v, wit)
        if time.time() - last > 30:
            last = time.time()
            out.write(json.dumps({"mode": "random", "progress": True, "seed": a.seed,
                                  "n": a.n, "B": a.B, "elapsed": round(last - t0),
                                  "tested": tested, "stats": stats}) + "\n")
            out.flush()
    out.write(json.dumps({"mode": "random", "final": True, "seed": a.seed, "n": a.n,
                          "B": a.B, "elapsed": round(time.time() - t0), "tested": tested,
                          "stats": stats}) + "\n")
    out.flush()


def objective(v, kind, seed_alloc):
    if kind == "score":
        _, sc, wit = efx.score(v, seed_alloc)
        return sc, wit
    ok, sc, cnt, wit = efx.full(v)
    n, m = len(v), len(v[0])
    # fewer EFX allocations is "worse"; break ties by score
    return (cnt / n ** m) + 1e-3 * sc if ok else sc, wit


def run_climb(a, out):
    rng = random.Random(a.seed)
    t0 = time.time()
    runs = 0
    global_best = None
    while time.time() - t0 < a.seconds:
        runs += 1
        fam = a.family if a.family != "mixed" else rng.choice(FAMILIES)
        v = sample(fam, a.n, a.m, rng, a.B)
        cur, wit = objective(v, a.objective, None)
        best, bestv = cur, [r[:] for r in v]
        T0 = a.temp
        steps = a.steps
        for step in range(steps):
            if time.time() - t0 > a.seconds:
                break
            T = T0 * (1 - step / steps)
            w = [r[:] for r in v]
            kind = rng.random()
            i = rng.randrange(a.n)
            g = rng.randrange(a.m)
            if kind < 0.25:
                w[i][g] = max(0, min(a.B, w[i][g] + rng.randint(-a.B // 20 - 1, a.B // 20 + 1)))
            elif kind < 0.5:  # small relative move (keeps near-identical structure)
                w[i][g] = max(0, w[i][g] + rng.choice([-1, 1]) * max(1, int(w[i][g] * rng.random() * 0.02)))
            elif kind < 0.7:
                w[i][g] = rng.randint(0, a.B)
            elif kind < 0.85:
                h = rng.randrange(a.m)
                w[i][g], w[i][h] = w[i][h], w[i][g]
            else:  # copy a value from another agent (pushes toward identical rows)
                j = rng.randrange(a.n)
                w[i][g] = w[j][g]
            val, wwit = objective(w, a.objective, wit)
            if val <= cur or (T > 0 and rng.random() < math.exp(-(val - cur) / T)):
                v, cur, wit = w, val, wwit
                if cur < best:
                    best, bestv = cur, [r[:] for r in v]
                    if a.objective == "score" and best < 0:
                        break
        ok, _ = efx.exists(bestv)
        rec = {"mode": "climb", "objective": a.objective, "family": fam, "m": a.m,
               "n": a.n, "B": a.B, "seed": a.seed, "run": runs, "best": best,
               "efx_exists": ok, "v": bestv, "elapsed": round(time.time() - t0)}
        if a.objective == "count":
            okf, sc, cnt, _ = efx.full(bestv)
            rec["count"], rec["score"] = cnt, sc
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if not ok:
            report_counterexample(out, bestv, {"mode": "climb", "family": fam})
        if global_best is None or best < global_best:
            global_best = best
    out.write(json.dumps({"mode": "climb", "final": True, "runs": runs,
                          "global_best": global_best, "m": a.m, "seed": a.seed,
                          "objective": a.objective,
                          "elapsed": round(time.time() - t0)}) + "\n")
    out.flush()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["random", "climb"])
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--m", type=int, default=8,
                   help="number of goods; negative -M means random m in [M/2, M]")
    p.add_argument("--B", type=int, default=1000)
    p.add_argument("--seconds", type=float, default=60)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--family", default="mixed")
    p.add_argument("--objective", default="score", choices=["score", "count"])
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--temp", type=float, default=0.002)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    with open(a.out, "a") as out:
        (run_random if a.mode == "random" else run_climb)(a, out)
