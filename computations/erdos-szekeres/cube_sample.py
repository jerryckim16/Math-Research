"""Cube-and-conquer cost estimate by random probing of a lookahead cube tree.

Usage:
  python3 cube_sample.py formula.cnf N --depth D --samples S --cap T \
      [--workers W] [--seed R] [--out results.jsonl] [--norient]

The cube tree (never built in full)
  A node is a set of decision literals on orientation variables (1..C(N,3)).
  At each node a march-style lookahead runs over every unassigned orientation
  variable v: unit-propagate the node plus v, and the node plus -v. If one
  side conflicts, the other literal is forced (failed literal) and the
  lookahead restarts; if both conflict, the node is refuted. Otherwise branch
  on the v maximising (1 + #new orientation literals under v) *
  (1 + #new under -v). Leaves are nodes at depth D (or refuted earlier).
  Propagation is by glucose4 (pysat) on the full formula.

Estimator (Knuth 1975, "Estimating the efficiency of backtrack programs")
  A probe walks from the root to a leaf choosing a child uniformly at random.
  The probability of reaching that leaf is p = prod 1/(#children), with
  refuted children never chosen (they cost nothing to the conquer phase).
  A walk that reaches a node refuted by the lookahead stops there; that leaf
  costs 0 (status REFUTED). The leaf cube is otherwise solved by CaDiCaL (CLI, cube added as unit clauses)
  with a time cap. For the cost function c(leaf) = solve time,
  E[c(leaf)/p] = sum over leaves of c(leaf), so the mean of c/p over probes
  is an unbiased estimate of the total conquer CPU time, and the mean of 1/p
  estimates the number of (non-refuted) leaves. Timed-out cubes are
  recorded with c = cap, which makes the time estimate a LOWER bound for
  those probes. Heavy tails in c and in 1/p are reported, not smoothed.

--nested d1,d2,...: solve the prefixes of each probe path at several depths
(one record per probe and depth), giving a hardness-versus-depth profile
from the same random paths.

This is an estimation tool, not a proof tool: nothing it outputs is a
certificate.
"""
import argparse
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from math import comb

from pysat.formula import CNF
from pysat.solvers import Solver

_S = None
_NOR = None
_FIXED = set()


def _init(cnf_path, n_orient):
    global _S, _NOR, _FIXED
    clauses = CNF(from_file=cnf_path).clauses
    _S = Solver(name="glucose4", bootstrap_with=clauses)
    _NOR = n_orient
    # top-level unit clauses (symmetry breaking); propagate() does not report them
    _FIXED = {abs(c[0]) for c in clauses if len(c) == 1}


def _state(assum):
    ok, lits = _S.propagate(assumptions=assum)
    if not ok:
        return None, None
    assigned = {abs(l) for l in lits} | _FIXED
    return assigned, sum(1 for l in lits if abs(l) <= _NOR)


def lookahead(assum):
    """Return ('refuted', None) or ('ok', (assum', branch_var)).

    One pass over the unassigned orientation variables. A failed literal is
    added to the node and the pass continues (scores already computed are
    then slightly stale, which only affects the heuristic, not soundness of
    the estimate).
    """
    assum = list(assum)
    assigned, base = _state(assum)
    if assigned is None:
        return "refuted", None
    best, bv = -1, None
    for v in range(1, _NOR + 1):
        if v in assigned:
            continue
        okp, lp = _S.propagate(assumptions=assum + [v])
        okn, ln = _S.propagate(assumptions=assum + [-v])
        if not okp and not okn:
            return "refuted", None
        if not okp or not okn:
            assum.append(-v if not okp else v)
            assigned, base = _state(assum)
            if assigned is None:
                return "refuted", None
            if bv is not None and bv in assigned:
                best, bv = -1, None
            continue
        np_ = sum(1 for l in lp if abs(l) <= _NOR) - base
        nn_ = sum(1 for l in ln if abs(l) <= _NOR) - base
        sc = (1 + np_) * (1 + nn_)
        if sc > best:
            best, bv = sc, v
    return "ok", (assum, bv)


def probe(args):
    """Random root-to-leaf walk; returns (cube literals, weight 1/p, path info)."""
    depth, seed = args
    rng = random.Random(seed)
    assum, weight, decisions = [], 1, 0
    prefixes = [(0, 1, [])]  # (depth, weight, cube) after each decision, for --nested
    t0 = time.time()
    while decisions < depth:
        st, res = lookahead(assum)
        if st == "refuted":
            # only reachable at the root, or if a child refuted after the parent chose it
            return {"refuted": True, "cube": assum, "weight": weight, "decisions": decisions,
                    "la_time": time.time() - t0, "prefixes": prefixes}
        assum, v = res
        if v is None:
            break
        kids = []
        for lit in (v, -v):
            ok, _ = _S.propagate(assumptions=assum + [lit])
            if ok:
                kids.append(lit)
        # lookahead guarantees both sides propagate without conflict
        weight *= len(kids)
        assum = assum + [rng.choice(kids)]
        decisions += 1
        prefixes.append((decisions, weight, list(assum)))
    return {"refuted": False, "cube": assum, "weight": weight, "decisions": decisions,
            "la_time": time.time() - t0, "prefixes": prefixes}


def enumerate_leaves(depth):
    """All leaves of the cube tree to the given depth (small depths only)."""
    leaves = []

    def rec(assum, d):
        st, res = lookahead(assum)
        if st == "refuted":
            leaves.append({"refuted": True, "cube": assum, "weight": 1, "decisions": d, "la_time": 0})
            return
        assum, v = res
        if d == depth or v is None:
            leaves.append({"refuted": False, "cube": assum, "weight": 1, "decisions": d, "la_time": 0})
            return
        for lit in (v, -v):
            rec(assum + [lit], d + 1)

    rec([], 0)
    return leaves


def solve_cube(args):
    cnf_path, cube, cap, workdir = args
    with open(cnf_path) as f:
        header = f.readline().split()
        body = f.read()
    nv, nc = int(header[2]), int(header[3])
    fd, path = tempfile.mkstemp(suffix=".cnf", dir=workdir)
    with os.fdopen(fd, "w") as g:
        g.write(f"p cnf {nv} {nc + len(cube)}\n")
        g.write(body)
        for l in cube:
            g.write(f"{l} 0\n")
    t0 = time.time()
    r = subprocess.run(["cadical", "-q", "-t", str(cap), path], stdout=subprocess.DEVNULL)
    dt = time.time() - t0
    os.unlink(path)
    status = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "TIMEOUT")
    return status, dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("N", type=int)
    ap.add_argument("--depth", type=int, required=True)
    ap.add_argument("--samples", type=int, required=True)
    ap.add_argument("--cap", type=int, default=600)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--nested", default=None,
                    help="comma-separated depths: solve the prefixes of each probe path at these depths")
    ap.add_argument("--enumerate", action="store_true",
                    help="solve every leaf at the given depth instead of sampling (calibration)")
    a = ap.parse_args()
    n_or = comb(a.N, 3)
    workdir = a.workdir or os.path.dirname(os.path.abspath(a.out or a.cnf))
    seeds = [(a.depth, a.seed * 100003 + i) for i in range(a.samples)]
    out = open(a.out, "a") if a.out else sys.stdout
    if a.enumerate:
        _init(a.cnf, n_or)
        probes = enumerate_leaves(a.depth)
    else:
        with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(a.cnf, n_or)) as ex:
            probes = list(ex.map(probe, seeds))
    if a.nested:
        ds = sorted(int(x) for x in a.nested.split(","))
        expanded = []
        for i, p in enumerate(probes):
            pre = {d: (w, cube) for (d, w, cube) in p.get("prefixes", [])}
            for d in ds:
                if d in pre:
                    w, cube = pre[d]
                    expanded.append({"refuted": False, "cube": cube, "weight": w, "decisions": d,
                                     "la_time": p["la_time"], "path": i, "depth": d})
                elif p["refuted"] and p["decisions"] < d:
                    # the walk hit a node refuted by lookahead above depth d: a zero-cost leaf
                    expanded.append({"refuted": True, "cube": p["cube"], "weight": p["weight"],
                                     "decisions": p["decisions"], "la_time": p["la_time"], "path": i, "depth": d})
        probes = expanded
    # results are written as each cube finishes, so an interrupted run keeps its data
    from concurrent.futures import as_completed

    def emit(p, st, dt):
        rec = {"mode": "enum" if a.enumerate else "probe", "refuted": p["refuted"],
               "depth": p.get("depth", a.depth), "path": p.get("path"), "decisions": p["decisions"],
               "cube_len": len(p["cube"]), "weight": p["weight"], "la_time": round(p["la_time"], 2),
               "status": st, "time": round(dt, 3), "cap": a.cap, "cube": p["cube"]}
        out.write(json.dumps(rec) + "\n")
        out.flush()

    for p in probes:
        if p["refuted"]:  # refuted by the lookahead's unit propagation: costs nothing to conquer
            emit(p, "REFUTED", 0.0)
    todo = [p for p in probes if not p["refuted"]]
    with ProcessPoolExecutor(a.workers) as ex:
        futs = {ex.submit(solve_cube, (a.cnf, p["cube"], a.cap, workdir)): p for p in todo}
        for f in as_completed(futs):
            st, dt = f.result()
            emit(futs[f], st, dt)

if __name__ == "__main__":
    main()
