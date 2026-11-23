"""Summarise cube_sample.py output: Knuth estimates with bootstrap ranges.

Usage: python3 cube_estimate.py results.jsonl [more.jsonl ...]

Groups records by (mode, depth, cap). For probes, the estimate of the total
conquer CPU time is mean(weight * time) and the estimated number of leaves
is mean(weight). A timed-out cube contributes weight * cap, so whenever a
group has timeouts its total is a LOWER bound (marked ">="). The range is a
percentile bootstrap (2000 resamples, 5%-95%) of that mean; with heavy tails
and few samples it is only indicative, and it cannot see tail mass that no
probe hit.
"""
import json
import random
import statistics
import sys
from collections import defaultdict


def fmt_t(s):
    if s < 120:
        return f"{s:.1f} s"
    if s < 7200:
        return f"{s / 60:.1f} min"
    if s < 2 * 86400:
        return f"{s / 3600:.1f} h"
    if s < 2 * 31557600:
        return f"{s / 86400:.1f} d"
    return f"{s / 31557600:.3g} yr"


def main():
    groups = defaultdict(list)
    for path in sys.argv[1:]:
        for line in open(path):
            r = json.loads(line)
            groups[(r.get("mode", "probe"), r["depth"], r["cap"])].append(r)
    rng = random.Random(0)
    for (mode, depth, cap), rs in sorted(groups.items()):
        n = len(rs)
        to = sum(r["status"] == "TIMEOUT" for r in rs)
        sat = sum(r["status"] == "SAT" for r in rs)
        times = [min(r["time"], cap) if r["status"] == "TIMEOUT" else r["time"] for r in rs]
        if mode == "enum":
            tot = sum(times)
            print(f"[enum depth={depth} cap={cap}] leaves={n} SAT={sat} timeouts={to} "
                  f"total={'>=' if to else ''}{fmt_t(tot)} median={fmt_t(statistics.median(times))} max={fmt_t(max(times))}")
            continue
        w = [r["weight"] for r in rs]
        c = [wi * ti for wi, ti in zip(w, times)]
        est = sum(c) / n
        leaves = sum(w) / n
        boots = []
        for _ in range(2000):
            idx = [rng.randrange(n) for _ in range(n)]
            boots.append(sum(c[i] for i in idx) / n)
        boots.sort()
        lo, hi = boots[int(0.05 * len(boots))], boots[int(0.95 * len(boots)) - 1]
        top = max(c) / sum(c) if sum(c) else 0
        lb = ">=" if to else ""
        print(f"[probe depth={depth} cap={cap}] probes={n} SAT={sat} timeouts={to} "
              f"leaves~{leaves:.3g} (min w {min(w)}, max w {max(w)}) "
              f"cube time median={fmt_t(statistics.median(times))} max={fmt_t(max(times))}; "
              f"total CPU {lb}{fmt_t(est)} [bootstrap 5-95%: {lb}{fmt_t(lo)} .. {lb}{fmt_t(hi)}]; "
              f"largest single probe = {100 * top:.0f}% of the sum")


if __name__ == "__main__":
    main()
