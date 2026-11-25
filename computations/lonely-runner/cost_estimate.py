"""Measured-basis cost estimate for the level-one step of LRC(15) (16 runners).

Inputs
  * Allikvere's per-gate CPU for LRC(14) (k = 14): gates.json from
    fifteen_runners_manuscript_source.zip, Zenodo 10.5281/zenodo.22667683
    (generation + precondition + kill CPU seconds; cascade wall time excluded).
  * results/knuth_covergen_k14_k15.txt: Knuth random-probe estimates of the
    search-tree size of OUR covergen.c for k = 14 and k = 15 at the same
    primes (20,000 probes each; estimator validated against exact counts
    for k = 7, 8, 9 within 0.3%).

Model (heuristic, stated so it can be refuted)
  cost_15(p) ~= cost_14(p) * N15(p) / N14(p),
i.e. Allikvere's generator would grow from k = 14 to k = 15 by the same
factor as our (less pruned) tree.  Both factors are fitted as power laws in
p over 251 <= p <= 569 and extrapolated to the k = 15 gate range.

Usage: python3 cost_estimate.py path/to/gates.json
"""
import json
import sys
from math import log, exp, comb

HERE = __file__.rsplit("/", 1)[0]


def fit(xs, ys):
    lx = [log(x) for x in xs]
    ly = [log(y) for y in ys]
    n = len(xs)
    mx, my = sum(lx) / n, sum(ly) / n
    b = sum((a - mx) * (c - my) for a, c in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    return b, my - b * mx  # y = exp(a) x^b


def primes(a, b):
    return [p for p in range(a, b + 1) if p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1))]


def main():
    g = json.load(open(sys.argv[1]))
    cost14 = {}
    for p, d in g.items():
        t = d["timing"]
        cost14[int(p)] = (t.get("ir_gen_cpu_secs", 0) + t.get("km1_gen_cpu_secs", 0)
                          + t.get("precondition_secs", 0) + d.get("kills_cpu_secs", 0)) / 3600
    N = {}
    for line in open(HERE + "/results/knuth_covergen_k14_k15.txt"):
        k, p, _, est = line.split()[:4]
        N[(int(k), int(p))] = float(est)
    ps = sorted({p for (_, p) in N})
    ratio = {p: N[(15, p)] / N[(14, p)] for p in ps}
    print("p    N14(ours)   N15(ours)   ratio  Allikvere k=14 CPU-h")
    for p in ps:
        print(f"{p:4d} {N[(14,p)]:.3e} {N[(15,p)]:.3e} {ratio[p]:6.2f} {cost14.get(p, float('nan')):8.2f}")
    big = [p for p in sorted(cost14) if 251 <= p <= 569]
    b14, a14 = fit(big, [cost14[p] for p in big])
    br, ar = fit(ps, [ratio[p] for p in ps])
    print(f"fit: cost_14(p) ~ p^{b14:.2f} over 251..569 (decomposition gates); ratio N15/N14 ~ p^{br:.2f}")

    def c14(p):
        return cost14[p] if p in cost14 and p >= 251 else exp(a14) * p ** b14

    def c15(p):
        return c14(p) * exp(ar) * p ** br

    lcm16 = 720720
    for label, target in (("flag bound with proved r_15 = 49/100 (Approaches 10-11), minus ln lcm(2..16)", 496.7268 - log(lcm16)),
                          ("MSS/Rosenfeld B_15 (proved input), minus ln lcm(2..16)", 964.7525 - log(lcm16))):
        s, tot, gates = 0.0, 0.0, []
        for p in primes(251, 5000):
            if s > target:
                break
            s += log(p)
            tot += c15(p)
            gates.append(p)
        print(f"{label}: target {target:.2f}: {len(gates)} gates {gates[0]}..{gates[-1]}, "
              f"estimated level-one+kill CPU ~ {tot:,.0f} h ({tot/8766:.1f} CPU-years)")


    # Second model (step 11): OUR generator.  Level one only (no kill, no
    # cascade).  Our k = 15 plain tree N15(p) (Knuth, fitted as a power law),
    # times the node fraction left by LRC_PRUNE=1 + LRC_IRR=2 as measured at
    # k = 14 (0.496 at p = 251, 0.334 at p = 401; Knuth, results/
    # knuth_twobranch_k14.txt), fitted log-linearly in p, at the measured
    # 1.7e6 nodes/s per core.  Heuristic: assumes the k = 14 cut fraction
    # carries over to k = 15.
    b15, a15 = fit(ps, [N[(15, p)] for p in ps])
    fr = {251: 0.496, 401: 0.334}
    bf = (log(fr[401]) - log(fr[251])) / (log(401) - log(251))
    af = log(fr[251]) - bf * log(251)
    rate = 1.7e6
    s, tot, gates = 0.0, 0.0, []
    for p in primes(251, 5000):
        if s > 496.7268 - log(lcm16):
            break
        s += log(p)
        n15 = N[(15, p)] if (15, p) in N else exp(a15) * p ** b15
        tot += n15 * min(1.0, exp(af) * p ** bf) / rate / 3600
        gates.append(p)
    print(f"our covergen (LRC_PRUNE=1, LRC_IRR=2), level one only, proved target: {len(gates)} gates "
          f"{gates[0]}..{gates[-1]}: ~ {tot:,.0f} CPU-h ({tot/8766:.1f} CPU-years); N15 ~ p^{b15:.2f}, cut fraction ~ p^{bf:.2f}")


if __name__ == "__main__":
    main()
