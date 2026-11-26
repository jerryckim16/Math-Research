"""Gate-set scenario for LRC(17) with mid-range divisibility gates (heuristic).

Pool:
  * J-empty candidates p >= 313 (not shown to have tau_17 <= 15): cost = level-one
    CPU-h only, as in k17/gate_set.py (nodes / 1.8e6 per s; power-law beyond 1597).
  * mid-range primes with a measured sweep (results/sweep_casc_p<P>.jsonl and
    results/sweep_mcmc_p<P>.txt): cost = level-one CPU-h
      + ORBIT_US microseconds per level-one orbit (orbit expansion/dedup, assumed)
      + orbits * mean(sec per base) of the sampled cascade (the cheaper of chain
        3,3,2,2 and the two-stage strategy of run_adaptive.sh; summarize.py).
    Only primes whose every sampled base closed are admitted ("closes on the sample";
    this is NOT a proof that the gate closes).
Greedy by cost / ln p until sum ln p > target (as in gate_set.py).
Usage: python3 gate_scenario.py TARGET [ORBIT_US]
"""
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k17"))
import gate_set as GS  # noqa: E402


def sweep():
    import summarize
    out = {}
    for p, d in summarize.per_prime().items():
        out[p] = dict(orbits=d["orbits"], closed=d["closed_all"], sec=sum(d["best"]) / len(d["best"]))
    return out


def main():
    T = float(sys.argv[1])
    orbit_us = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    kn, tau = GS.load(17)
    cand = [p for p in sorted(kn) if tau.get(p, "unscreened") != "near-gcd only (tau <= 15)"]
    top = [p for p in cand if p >= sorted(kn)[len(kn) // 2]]
    b, a = GS.fit(top, [kn[p] for p in top])

    def l1(p):
        return (kn[p] if p in kn else math.exp(a) * p ** b) / GS.RATE / 3600

    sw = sweep()
    pool = []
    for p in GS.primes(19, 6000):
        st = tau.get(p, "unscreened" if p <= max(kn) else "extrapolated")
        if p in sw and st.startswith("near-gcd"):
            d = sw[p]
            if not d["closed"]:
                continue
            cost = l1(p) + d["orbits"] * (orbit_us * 1e-6 + d["sec"]) / 3600
            pool.append((cost / math.log(p), p, cost, "mid (sampled)"))
        elif st.startswith("near-gcd"):
            continue
        elif p >= 313:
            pool.append((l1(p) / math.log(p), p, l1(p), "J-empty candidate"))
    pool.sort()
    s = tot = 0.0
    chosen = []
    for _, p, c, kind in pool:
        if s > T:
            break
        s += math.log(p)
        tot += c
        chosen.append((p, c, kind))
    mids = [x for x in chosen if x[2].startswith("mid")]
    print(f"target {T}: {len(chosen)} gates, sum ln p = {s:.3f}, total ~ {tot:.3g} CPU-h "
          f"({tot / 8766:.3g} CPU-years); mid-range gates used: {len(mids)} "
          f"(cost {sum(c for _, c, _ in mids):.3g} CPU-h), max prime {max(p for p, _, _ in chosen)}")
    print("  mid:", " ".join(f"{p}:{c:.2g}" for p, c, _ in sorted(mids)))
    print("  J-empty:", " ".join(str(p) for p, _, k in sorted(chosen) if not k.startswith("mid")))


if __name__ == "__main__":
    main()
