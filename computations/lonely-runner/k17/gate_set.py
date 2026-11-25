"""Cheapest admissible gate set for LRC(k) from measured data (heuristic cost).

Inputs (this directory):
  knuth_k<k>.txt : "p est_nodes stderr nodes_per_sec" -- Knuth estimates of the
                   covergen.c tree, LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1, 20000
                   probes (heuristic; the k = 14 estimate at p = 251 was within
                   1% of the exact count, problem file Approach 13).
  tau_k<k>.txt   : tau.c screen lines "k K p P ... tau T ..." (TAU_FROM = k-2):
                   "tau k-2" or less  -> a cover on <= k-2 classes was FOUND:
                                         tau_k(p) <= k-2, J(k,p) non-empty
                                         (Lemma T, notes/lonely-runner/gates.md);
                   "tau >k-2"         -> exhaustive: tau_k(p) >= k-1 (proved);
                   "TIMEOUT"          -> undetermined (no small cover found in
                                         the time limit; treated as admissible
                                         CANDIDATE, not proved).
Cost model (heuristic): level-one CPU = nodes / RATE, RATE = 1.8e6 nodes/s (the
exact sharded k = 14, p = 251 run, 4 processes on 4 cores).  Beyond the
measured range, nodes are extrapolated by a power law fitted to the measured
candidate primes in the top half of the range.  Cascade and kill are not
included (at k = 15 they are a small fraction: Allikvere's cascade wall times
are seconds to minutes).
Selection: admissible primes sorted by cost / ln p, taken until sum ln p >
target.  This is the greedy solution of the knapsack "minimise cost subject
to sum ln p >= target"; it is optimal up to the last prime taken (the
fractional relaxation is solved exactly by the same order).
Usage: python3 gate_set.py K TARGET [TARGET2 ...]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 1.8e6


def primes(a, b):
    return [p for p in range(a, b + 1) if p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1))]


def load(k):
    kn, tau = {}, {}
    for l in open(os.path.join(HERE, f"knuth_k{k}.txt")):
        if l.startswith("#") or not l.strip():
            continue
        a = l.split()
        kn[int(a[0])] = float(a[1])
    for l in open(os.path.join(HERE, f"tau_k{k}.txt")):
        if l.startswith("#") or not l.strip():
            continue
        a = l.split()
        p = int(a[3])
        if "TIMEOUT" in a:
            tau[p] = "undetermined"
        else:
            t = a[a.index("tau") + 1]
            tau[p] = "admissible (proved)" if t.startswith(">") else "near-gcd only (tau <= %d)" % (k - 2)
    return kn, tau


def fit(ps, ys):
    lx = [math.log(x) for x in ps]
    ly = [math.log(y) for y in ys]
    n = len(ps)
    mx, my = sum(lx) / n, sum(ly) / n
    b = sum((a - mx) * (c - my) for a, c in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    return b, my - b * mx


def main():
    k = int(sys.argv[1])
    targets = [float(x) for x in sys.argv[2:]]
    kn, tau = load(k)
    cand = [p for p in sorted(kn) if tau.get(p, "unscreened") != "near-gcd only (tau <= %d)" % (k - 2)]
    top = [p for p in cand if p >= sorted(kn)[len(kn) // 2]]
    b, a = fit(top, [kn[p] for p in top])
    print(f"k = {k}: measured primes {min(kn)}..{max(kn)}; fit nodes ~ exp({a:.2f}) p^{b:.2f} over {len(top)} candidate primes {top[0]}..{top[-1]}")
    pmax = max(kn)

    def nodes(p):
        return kn[p] if p in kn else math.exp(a) * p ** b

    for T in targets:
        pool = []
        for p in primes(k + 2, 6000):
            st = tau.get(p, "unscreened" if p <= pmax else "extrapolated")
            if st.startswith("near-gcd"):
                continue
            pool.append((nodes(p) / RATE / 3600 / math.log(p), p, st))
        pool.sort()
        s = tot = 0.0
        chosen = []
        for _, p, st in pool:
            if s > T:
                break
            s += math.log(p)
            tot += nodes(p) / RATE / 3600
            chosen.append((p, st))
        sts = {}
        for p, st in chosen:
            sts[st] = sts.get(st, 0) + 1
        print(f"target {T:.5f}: {len(chosen)} gates, primes {min(p for p, _ in chosen)}..{max(p for p, _ in chosen)}, "
              f"sum ln p = {s:.3f}, level-one cost ~ {tot:,.0f} CPU-h ({tot / 8766:,.1f} CPU-years); status counts {sts}")
        print("  gates:", " ".join(str(p) for p, _ in sorted(chosen)))


if __name__ == "__main__":
    main()
