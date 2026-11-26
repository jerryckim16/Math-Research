"""Run xcasc.c on sampled level-one bases in parallel and summarise (heuristic).

Usage:
  python3 run_casc.py run P CHAIN NBASES OUT.jsonl [JOBS] [CAP] [NODECAP]  < samples
      samples: lines "M x_1 .. x_17" from mcmc1.c (or plain rows); the first
      NBASES are used; JOBS parallel xcasc processes (default 3).
  python3 run_casc.py summary OUT.jsonl ORBITS [ORBITS_RELERR]
      closure by level, retained orbits per level, time per base, and the
      extrapolated cascade cost ORBITS * mean(sec) with a bootstrap 95% interval.
"""
import json
import os
import random
import statistics
import subprocess
import sys

import rio

HERE = os.path.dirname(os.path.abspath(__file__))


def run(p, chain, n, out, jobs=3, cap=200000, nodecap=None):
    exe = os.path.join(HERE, "xcasc")
    subprocess.run(["cc", "-O3", "-march=native", "-o", exe, os.path.join(HERE, "xcasc.c")], check=True)
    rows = []
    for line in sys.stdin:
        xs = line.split()
        if xs and xs[0] == "M":
            xs = xs[1:]
        if len(xs) == 17:
            rows.append(" ".join(xs))
        if len(rows) >= n:
            break
    env = dict(os.environ)
    if nodecap:
        env["XC_NODECAP"] = str(nodecap)
    procs = []
    for j in range(jobs):
        part = rows[j::jobs]
        f = open(out + f".part{j}", "w")
        pr = subprocess.Popen(["nice", "-n", "10", exe, "17", str(p), chain, str(cap)], stdin=subprocess.PIPE,
                              stdout=f, text=True, env=env)
        pr.stdin.write("\n".join(part) + "\n")
        pr.stdin.close()
        procs.append((pr, f))
    for pr, f in procs:
        pr.wait()
        f.close()
    with open(out, "w") as g:
        for j in range(jobs):
            with open(out + f".part{j}") as f:
                for line in f:
                    rec = json.loads(line)
                    rec["p"] = p
                    rec["chain"] = chain
                    g.write(json.dumps(rec) + "\n")
            os.remove(out + f".part{j}")


def summary(path, orbits, orb_rel=0.0):
    recs = [json.loads(l) for l in rio.opn(path)]
    n = len(recs)
    p = recs[0].get("p")
    chain = recs[0].get("chain")
    levels = []
    for r in recs:
        for lv, _, _ in r["trace"]:
            if lv not in levels:
                levels.append(lv)
    print(f"p = {p}, chain {chain}, bases {n}, level-one witnesses {sum(r['lvl1_witness'] for r in recs)}")
    closed = {}
    for r in recs:
        if r["empty_at"]:
            closed[r["empty_at"]] = closed.get(r["empty_at"], 0) + 1
    print("closed at level:", dict(sorted(closed.items())), " capped:", sum(r["capped"] for r in recs),
          " open at end:", sum(1 for r in recs if not r["empty_at"] and not r["capped"]))
    for lv in levels:
        vals = [t[1] for r in recs for t in r["trace"] if t[0] == lv]
        if vals:
            print(f"  level {lv}: reached by {len(vals)} bases; retained orbits mean {statistics.mean(vals):.2f} "
                  f"median {statistics.median(vals)} max {max(vals)}; nonempty {sum(1 for v in vals if v)}")
    secs = [r["sec"] for r in recs]
    mean = statistics.mean(secs)
    rnd = random.Random(1)
    boots = sorted(statistics.mean(rnd.choices(secs, k=n)) for _ in range(2000))
    lo, hi = boots[50], boots[1949]
    print(f"  sec per base: mean {mean:.4g} (bootstrap 95% {lo:.4g}-{hi:.4g}), median {statistics.median(secs):.4g}, max {max(secs):.4g}")
    cost = orbits * mean / 3600
    print(f"  extrapolated cascade CPU-h = orbits * mean = {cost:.3g} "
          f"(95%: {orbits * (1 - 2 * orb_rel) * lo / 3600:.3g}-{orbits * (1 + 2 * orb_rel) * hi / 3600:.3g})")
    return recs


if __name__ == "__main__":
    if sys.argv[1] == "run":
        a = sys.argv
        run(int(a[2]), a[3], int(a[4]), a[5], int(a[6]) if len(a) > 6 else 3,
            int(a[7]) if len(a) > 7 else 200000, int(a[8]) if len(a) > 8 else None)
    else:
        summary(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 0.0)
