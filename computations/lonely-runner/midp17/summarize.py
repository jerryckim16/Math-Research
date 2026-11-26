"""Markdown table of the sweep (heuristic numbers).  Usage: python3 summarize.py > results/sweep_table.md

Per prime: tau_17 (smallp/results/tau17.txt), level-one orbits (ladder estimate,
#multisets / h), closing levels of the 600 sampled bases with chain 3,3,2,2, mean
cascade seconds per base for 3,3,2,2 and for the two-stage strategy (chain 2, then
3,3,2,2 on the bases still open; run_adaptive.sh), and the extrapolated cascade
CPU-h = orbits * mean (best strategy) with a bootstrap 95% interval (which also
includes +-2 relative errors of the orbit estimate).
"""
import json
import os
import random
import re
import statistics

import rio

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "results")


def tau():
    t = {}
    for l in open(os.path.join(HERE, "..", "smallp", "results", "tau17.txt")):
        a = l.split()
        if len(a) >= 2:
            t[int(a[0])] = int(a[1])
    return t


def knuth():
    kn = {}
    for l in open(os.path.join(HERE, "..", "k17", "knuth_k17.txt")):
        if not l.startswith("#") and l.strip():
            a = l.split()
            kn[int(a[0])] = float(a[1])
    return kn


def boot(xs, n=2000, seed=1):
    rnd = random.Random(seed)
    m = sorted(statistics.mean(rnd.choices(xs, k=len(xs))) for _ in range(n))
    return m[int(0.025 * n)], m[int(0.975 * n)]


def per_prime():
    """p -> dict(orbits, rel, closed_all, best_mean, rows) from the sweep files"""
    out = {}
    ps = sorted(int(re.search(r"p(\d+)", f).group(1)) for f in os.listdir(R) if f.startswith("sweep_casc_p") and f.endswith((".jsonl", ".jsonl.gz")))
    for p in ps:
        m = rio.opn(os.path.join(R, f"sweep_mcmc_p{p}.txt")).read()
        orb = float(re.search(r"orbits_approx ([0-9.e+]+)", m).group(1))
        rel = float(re.search(r"rel_err_binomial ([0-9.]+)", m).group(1))
        a = [json.loads(l) for l in rio.opn(os.path.join(R, f"sweep_casc_p{p}.jsonl"))]
        s1 = [r["sec"] for r in a]
        best, s2, ok = s1, None, False
        f2 = os.path.join(R, f"ad2_p{p}.jsonl")
        if rio.exists(f2):
            a2 = {tuple(r["base"]): r for r in map(json.loads, rio.opn(f2))}
            f3 = os.path.join(R, f"ad3322_p{p}.jsonl")
            a3 = {tuple(r["base"]): r for r in map(json.loads, rio.opn(f3))} if rio.exists(f3) else {}
            s2, ok = [], True
            for b, r in a2.items():
                t = r["sec"]
                if not r["empty_at"]:
                    if b not in a3 or not a3[b]["empty_at"]:
                        ok = False
                        continue
                    t += a3[b]["sec"]
                s2.append(t)
            if ok and statistics.mean(s2) < statistics.mean(s1):
                best = s2
        out[p] = dict(orbits=orb, rel=rel, closed_all=all(r["empty_at"] for r in a), best=best, s1=s1, s2=s2,
                      s2ok=ok, rows=a)
    return out


def main():
    T, K = tau(), knuth()
    print("| $p$ | $\\tau_{17}$ | orbits | closed at 3 / 9 / 18 | s/base (3,3,2,2) | s/base (2, then 3,3,2,2) | cascade CPU-h (best; 95%) | level one CPU-h |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p, d in per_prime().items():
        orb, rel, a = d["orbits"], d["rel"], d["rows"]
        cl = {}
        for r in a:
            cl[r["empty_at"] or 0] = cl.get(r["empty_at"] or 0, 0) + 1
        s2txt = "n/a" if d["s2"] is None else f"{statistics.mean(d['s2']):.2e}" + ("" if d["s2ok"] else " (incomplete)")
        lo, hi = boot(d["best"])
        c = orb * statistics.mean(d["best"]) / 3600
        unclosed = cl.get(0, 0)
        closed = f"{cl.get(3, 0)} / {cl.get(9, 0)} / {cl.get(18, 0)}" + (f" / 36: {cl[36]}" if cl.get(36) else "") \
            + (f" (open {unclosed})" if unclosed else "")
        print(f"| {p} | {T.get(p, '≤ 15')} | {orb:.2e} | {closed} | {statistics.mean(d['s1']):.2e} | {s2txt} | "
              f"{c:.2g} ({orb * (1 - 2 * rel) * lo / 3600:.2g}–{orb * (1 + 2 * rel) * hi / 3600:.2g}) | "
              f"{K[p] / 1.8e6 / 3600:.2g} |")


if __name__ == "__main__":
    main()
