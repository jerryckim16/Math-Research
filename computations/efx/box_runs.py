"""Local exhaustive searches: CEGAR (Z3) in l_inf boxes around the hardest points found.

For each of the K lowest-score profiles in the given climb logs, run cegar in
the box {v : rows sum to 1, v >= 0, |v_i(g) - c_i(g)/sum_g c_i(g)| <= delta}
for an increasing ladder of delta, stopping at the first timeout.  An unsat
answer means (modulo Z3) that no counterexample exists in that box, a local
certificate around a point where EFX is nearly tight.

Usage: python3 box_runs.py --logs data/climb_score_m10_*.jsonl --k 5 --timeout 300 --out data/box_m10.jsonl
"""
import argparse
import json
from fractions import Fraction

import z3

import cegar


def run_box(c, delta, timeout):
    n, m = len(c), len(c[0])
    cn = [[Fraction(x, sum(r)) for x in r] for r in c]
    d = Fraction(delta).limit_denominator(10**6)

    def extra(V):
        return [z3.And(V[i][g] >= z3.RealVal(cn[i][g] - d), V[i][g] <= z3.RealVal(cn[i][g] + d))
                for i in range(n) for g in range(m)]
    st = {}
    res = cegar.cegar(n, m, None, timeout, extra=extra, sort0=False, stats=st)
    return res, st


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--logs", nargs="+", required=True)
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--deltas", type=float, nargs="+", default=[0.005, 0.01, 0.02, 0.05, 0.1])
    p.add_argument("--out", required=True)
    a = p.parse_args()
    pts = []
    for f in a.logs:
        for line in open(f):
            r = json.loads(line)
            if "best" in r and r.get("objective") == "score" and r["efx_exists"]:
                pts.append((r["best"], r["v"], f))
    pts.sort(key=lambda t: t[0])
    seen = set()
    chosen = []
    for sc, v, f in pts:
        if json.dumps(v) not in seen:
            seen.add(json.dumps(v))
            chosen.append((sc, v, f))
        if len(chosen) >= a.k:
            break
    with open(a.out, "a") as out:
        for sc, v, f in chosen:
            for d in a.deltas:
                if all(sum(r) == 0 for r in v):
                    break
                if any(sum(r) == 0 for r in v):
                    break  # zero row: skip (normalisation undefined)
                res, st = run_box(v, d, a.timeout)
                rec = {"center": v, "center_score": sc, "src": f, "delta": d,
                       "status": res["status"], "iters": res.get("iters"),
                       "seconds": res.get("seconds"), "num_allocs": len(res.get("allocs", [])),
                       "min_count": st.get("min_count")}
                if res["status"] == "COUNTEREXAMPLE_CANDIDATE":
                    rec["v"] = res["v"]
                    rec["COUNTEREXAMPLE_CANDIDATE"] = True
                out.write(json.dumps(rec) + "\n")
                out.flush()
                print(sc, d, res["status"], res.get("iters"), round(res.get("seconds") or 0, 1), flush=True)
                if res["status"] != "unsat":
                    break
