"""Timed sample of refinement-tree regions (cost probe for the m = 9 projection).

A plan is a JSONL file of regions to run, each with the information needed
for a Knuth / stratified estimate of the whole tree:
  {"branch": chains, "layer": "cube" | "trisub" | ..., "parent": chains,
   "siblings": number of children of the parent under cegar_branches.refine,
   "group": label, "timeout": seconds}
`plan` draws random children (fixed seed) of given parents; `run` executes the
plan's pending regions with cegar.cegar (same options as run_tree.py) and
appends one record per region to --out, flushed at once (resumable: regions
already in --out are skipped).  Records have the fields of
cegar_branches.one plus "probe" (the plan entry), "wall_total" (CEGAR + Z3
full-clause re-solve) and, also for timeouts, "allocs_str" (the allocations
found, one digit string each), so later runs can be seeded from them.

Usage:
  python3 probe_regions.py plan --m 9 --parent "[[2],[2],[6]]" --k 10 --seed 1 \\
          --layer cube --group 226 --timeout 1200 --plan PLAN.jsonl
  python3 probe_regions.py run --plan PLAN.jsonl --out OUT.jsonl --workers 4 \\
          --budget 1500 --arith 2 --lemma-m
  python3 probe_regions.py cvc5 --plan OUT.jsonl --out CVC5_TIMES.jsonl --workers 2 --budget 1500
`cvc5` times recheck_cvc5.check_record (independent encoding, full clauses)
on every closed record of OUT.jsonl not yet in CVC5_TIMES.jsonl (smallest
first) and appends {branch, num_allocs, cvc5, cvc5_seconds}.
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import sys
import time

import cegar
import cegar_branches as cb

key = lambda br: json.dumps(br)


def run_one(args):
    n, m, entry, opts = args
    opts = dict(opts)
    arith = opts.pop("arith", None)
    if arith is not None:
        opts["z3opts"] = {"smt.arith.solver": arith}
    br = entry["branch"]
    tl = entry["timeout"]
    t0 = time.time()
    st = {}
    res = cegar.cegar(n, m, br, tl, stats=st, **opts)
    out = {k: res[k] for k in res if k != "allocs"}
    out.update({"n": n, "m": m, "branch": br, "num_allocs": len(res.get("allocs", [])),
                "c0": bool(opts.get("c0")),
                "opts": {**{k: v for k, v in opts.items() if k != "z3opts"}, "arith": arith},
                "probe": entry})
    if res["status"] == "unsat":
        t1 = time.time()
        out["recheck_full_clauses"] = cegar.recheck(n, m, br, res["allocs"], timeout=tl,
                                                    c0=bool(opts.get("c0")))
        out["recheck_seconds"] = time.time() - t1
        out["allocs"] = res["allocs"]
    elif "allocs" in res:
        out["allocs_str"] = ["".join(map(str, a)) for a in res["allocs"]]
    out["wall_total"] = time.time() - t0
    return out


def cvc5_one(r):
    import recheck_cvc5
    t0 = time.time()
    v = str(recheck_cvc5.check_record(r))
    return {"branch": r["branch"], "m": r["m"], "num_allocs": r["num_allocs"], "cvc5": v,
            "cvc5_seconds": time.time() - t0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["plan", "run", "cvc5"])
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--m", type=int, default=9)
    p.add_argument("--plan", required=True)
    p.add_argument("--parent", default=None)
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--layer", default="cube")
    p.add_argument("--group", default="")
    p.add_argument("--timeout", type=float, default=1200)
    p.add_argument("--out", default=None)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--budget", type=float, default=1500)
    cb.add_opt_args(p)
    a = p.parse_args()
    if a.cmd == "plan":
        parent = json.loads(a.parent)
        kids = cb.refine(parent, a.m)
        rng = random.Random(a.seed)
        pick = rng.sample(kids, min(a.k, len(kids)))
        with open(a.plan, "a") as f:
            for ch in pick:
                f.write(json.dumps({"branch": [list(c) for c in ch], "layer": a.layer,
                                    "parent": parent, "siblings": len(kids), "group": a.group,
                                    "timeout": a.timeout, "seed": a.seed}) + "\n")
        print(len(pick), "of", len(kids), "children planned")
        return
    if a.cmd == "cvc5":
        done = set()
        if os.path.exists(a.out):
            done = {key(json.loads(x)["branch"]) for x in open(a.out)}
        recs = [json.loads(x) for x in open(a.plan)]
        recs = sorted([r for r in recs if r["status"] == "unsat" and key(r["branch"]) not in done],
                      key=lambda r: r["num_allocs"])
        t0 = time.time()
        with cf.ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
            futs = {}
            for r in recs:
                futs[ex.submit(cvc5_one, r)] = r
            for fu in cf.as_completed(futs):
                o = fu.result()
                f.write(json.dumps(o) + "\n")
                f.flush()
                print(o, f"t={time.time() - t0:.0f}", flush=True)
                if o["cvc5"] != "unsat":
                    print("!!!! cvc5 did not return unsat:", o, flush=True)
                if time.time() - t0 > a.budget:
                    for g in futs:
                        g.cancel()
                    break
        return
    plan = [json.loads(x) for x in open(a.plan)]
    done = set()
    if os.path.exists(a.out):
        done = {key(json.loads(x)["branch"]) for x in open(a.out)}
    queue = [e for e in plan if key(e["branch"]) not in done]
    print(len(queue), "regions pending", flush=True)
    t0 = time.time()
    with cf.ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
        running = {}
        while queue or running:
            while queue and len(running) < a.workers:
                left = a.budget - (time.time() - t0)
                fit = [k for k, e in enumerate(queue) if e["timeout"] <= left]
                if not fit:                     # nothing fits in the remaining budget
                    queue = []
                    break
                e = queue.pop(fit[0])
                running[ex.submit(run_one, (a.n, a.m, e, cb.opts_of(a)))] = e
            if not running:
                break
            done_f, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for fu in done_f:
                e = running.pop(fu)
                r = fu.result()
                f.write(json.dumps(r) + "\n")
                f.flush()
                print(r["branch"], r["status"], r.get("iters"), r["num_allocs"],
                      round(r.get("seconds", 0), 1), r.get("recheck_full_clauses"),
                      f"t={time.time() - t0:.0f}", flush=True)
                if r["status"] == "COUNTEREXAMPLE_CANDIDATE":
                    print("!!!!!!!! COUNTEREXAMPLE CANDIDATE !!!!!!!!", json.dumps(r), flush=True)
                if r["status"] == "unsat" and r.get("recheck_full_clauses") != "unsat":
                    print("!!!! full-clause Z3 recheck did not return unsat:", r["branch"], flush=True)
    print(f"elapsed {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    sys.exit(main())
