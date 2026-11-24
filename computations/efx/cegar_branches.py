"""Run cegar.py over the argmax branches (b_1 <= ... <= b_{n-1}) for given n, m.

Each branch adds "good b_i is a maximum good of agent i" (i = 1..n-1).  With
agent 0 sorted, these branches cover the normalised space up to permuting
agents 1..n-1 (AFM arXiv:2608.08590, Lemma "Argmax branching"), so if every
branch returns unsat, no counterexample exists for (n, m) (modulo Z3).

Usage: python3 cegar_branches.py --n 4 --m 7 --timeout 300 --out data/x.jsonl
       [--only 0,0,0 1,2,3]   [--workers 2]   [--cubes]

--cubes splits each selected branch further by the second favourites s_i of
agents 1..n-1 (s_i != b_i; among agents with equal b_i the s_i are taken
non-decreasing, by the same agent-permutation symmetry), as in AFM's "cube"
layer.  The cubes of a branch cover it.
Results are appended per branch; finished branches are skipped on restart.
"""
import argparse
import itertools
import json
import multiprocessing as mp
import os

import cegar


def cubes_of(br, m):
    out = []
    for ss in itertools.product(*[[x for x in range(m) if x != b] for b in br]):
        if all(not (br[k] == br[k + 1] and ss[k] > ss[k + 1]) for k in range(len(br) - 1)):
            out.append(tuple((b, x) for b, x in zip(br, ss)))
    return out


def one(args):
    n, m, br, timeout = args
    br = [list(b) if isinstance(b, tuple) else b for b in br]
    res = cegar.cegar(n, m, list(br), timeout)
    out = {k: res[k] for k in res if k != "allocs"}
    out.update({"n": n, "m": m, "branch": list(br), "num_allocs": len(res.get("allocs", []))})
    if res["status"] == "unsat":
        out["recheck_full_clauses"] = cegar.recheck(n, m, list(br), res["allocs"], timeout=timeout)
        out["allocs"] = res["allocs"]
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--m", type=int, default=7)
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--only", nargs="*", default=None)
    p.add_argument("--cubes", action="store_true")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            r = json.loads(line)
            if r["status"] in ("unsat", "COUNTEREXAMPLE_CANDIDATE"):
                done.add(json.dumps(r["branch"]))
    if a.only:
        brs = [tuple(int(x) for x in s.split(",")) for s in a.only]
    else:
        brs = list(itertools.combinations_with_replacement(range(a.m), a.n - 1))
    if a.cubes:
        brs = [c for br in brs for c in cubes_of(br, a.m)]
    norm = lambda br: json.dumps([list(b) if isinstance(b, tuple) else b for b in br])
    todo = [(a.n, a.m, br, a.timeout) for br in brs if norm(br) not in done]
    print(len(todo), "regions to do", flush=True)
    with mp.Pool(a.workers) as pool, open(a.out, "a") as f:
        for r in pool.imap_unordered(one, todo):
            f.write(json.dumps(r) + "\n")
            f.flush()
            print(r["branch"], r["status"], r.get("iters"), round(r.get("seconds", 0), 1),
                  r.get("recheck_full_clauses"), flush=True)
