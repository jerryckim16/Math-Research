"""Resumable refinement driver on top of cegar_branches.py (n = 4 by default).

Roots are the argmax branches b_1 <= ... <= b_{n-1}.  A region that times out
is split with cegar_branches.refine (every agent's next favourite; equal
chains sorted), first into cubes, then into finer layers.  Every finished
region (unsat certificate, or timeout) is appended to --out and flushed at
once, so a restart loses only the regions in flight; on restart, unsat
regions are skipped and timed-out ones are expanded.  Coverage is checked
independently by `recheck_cvc5.py --tree`.

Usage: python3 run_tree.py --m 8 --out RUN.jsonl --budget 1440 --workers 4 \\
           --timeouts 300,300,300 --c0 --lemma-m [--multi K] [--seed-points P]
           [--only 0,0,2 ...] [--split-roots]

--split-roots skips the root (branch-level) regions and starts from their
cubes; used to re-close large branch-level certificates as small cubes.
"""
import argparse
import concurrent.futures as cf
import itertools
import json
import os
import time

import cegar_branches as cb

p = argparse.ArgumentParser()
p.add_argument("--n", type=int, default=4)
p.add_argument("--m", type=int, default=8)
p.add_argument("--out", required=True)
p.add_argument("--budget", type=float, default=1440, help="seconds; no new region starts after budget - timeout")
p.add_argument("--workers", type=int, default=4)
p.add_argument("--timeouts", default="300", help="per depth (max chain length 1, 2, ...); last value repeats")
p.add_argument("--max-depth", type=int, default=4)
p.add_argument("--only", nargs="*", default=None, help="restrict roots, e.g. 0,0,0")
p.add_argument("--split-roots", action="store_true",
               help="do not run the roots themselves: start from their children (cubes)")
cb.add_opt_args(p)
a = p.parse_args()
touts = [float(x) for x in a.timeouts.split(",")]
key = lambda node: json.dumps([list(c) for c in node])
depth = lambda node: max(len(c) for c in node)
recs = {}
if os.path.exists(a.out):
    for line in open(a.out):
        r = json.loads(line)
        st = r["status"]
        if st == "unsat" and r.get("recheck_full_clauses") != "unsat":
            st = "recheck_failed"          # never counted as closed
        recs[key(tuple(tuple(b) if isinstance(b, list) else (b,) for b in r["branch"]))] = st
roots = [tuple((b,) for b in br) for br in
         ([tuple(int(x) for x in s.split(",")) for s in a.only] if a.only else
          itertools.combinations_with_replacement(range(a.m), a.n - 1))]


def todo(node):
    """Regions still to run below node (parents before children; breadth-first overall)."""
    st = recs.get(key(node))
    if a.split_roots and depth(node) == 1:
        st = "timeout"                     # treated as split, whatever its own record says
    if st is None:
        return [node]
    if st == "timeout" and depth(node) < a.max_depth:
        return [x for ch in cb.refine([list(c) for c in node], a.m) for x in todo(ch)]
    return []


t0 = time.time()
queue = [x for r in roots for x in todo(r)]
print(len(queue), "regions queued", flush=True)
with cf.ProcessPoolExecutor(a.workers) as ex, open(a.out, "a") as f:
    running = {}
    while queue or running:
        while queue and len(running) < a.workers:
            node = queue.pop(0)
            tl = touts[min(depth(node), len(touts)) - 1]
            if time.time() - t0 > a.budget - tl:
                queue = []
                break
            br = [c[0] for c in node] if depth(node) == 1 else [list(c) for c in node]
            running[ex.submit(cb.one, (a.n, a.m, br, tl, cb.opts_of(a)))] = node
        if not running:
            break
        done, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
        for fu in done:
            node = running.pop(fu)
            r = fu.result()
            f.write(json.dumps(r) + "\n")
            f.flush()
            recs[key(node)] = r["status"]
            if r["status"] == "unsat" and r.get("recheck_full_clauses") != "unsat":
                recs[key(node)] = "recheck_failed"
                print("!!!! full-clause Z3 recheck did not return unsat:", r["branch"], flush=True)
            print(r["branch"], r["status"], r.get("iters"), round(r.get("seconds", 0), 1),
                  r.get("recheck_full_clauses"), f"t={time.time() - t0:.0f}", flush=True)
            if r["status"] == "COUNTEREXAMPLE_CANDIDATE":
                print("!!!!!!!! COUNTEREXAMPLE CANDIDATE !!!!!!!!", json.dumps(r), flush=True)
            if r["status"] == "timeout":
                queue = queue + todo(node)
st = {}
for s in recs.values():
    st[s] = st.get(s, 0) + 1
print("records by status:", st, f"elapsed {time.time() - t0:.0f}s", flush=True)
