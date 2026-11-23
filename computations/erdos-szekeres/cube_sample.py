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
  The leaf cube is then solved by CaDiCaL (CLI, cube added as unit clauses)
  with a time cap. For the cost function c(leaf) = solve time,
  E[c(leaf)/p] = sum over leaves of c(leaf), so the mean of c/p over probes
  is an unbiased estimate of the total conquer CPU time, and the mean of 1/p
  estimates the number of (non-refuted) leaves. Timed-out cubes are
  recorded with c = cap, which makes the time estimate a LOWER bound for
  those probes. Heavy tails in c and in 1/p are reported, not smoothed.

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


def _init(cnf_path, n_orient):
    global _S, _NOR
    _S = Solver(name="glucose4", bootstrap_with=CNF(from_file=cnf_path).clauses)
    _NOR = n_orient


def lookahead(assum):
    """Return ('refuted', None) or ('ok', (assum', branch_var))."""
    assum = list(assum)
    while True:
        ok, lits = _S.propagate(assumptions=assum)
        if not ok:
            return "refuted", None
        assigned = {abs(l) for l in lits}
        base = sum(1 for v in assigned if v <= _NOR)
        best, bv, forced = -1, None, None
        for v in range(1, _NOR + 1):
            if v in assigned:
                continue
            okp, lp = _S.propagate(assumptions=assum + [v])
            okn, ln = _S.propagate(assumptions=assum + [-v])
            if not okp and not okn:
                return "refuted", None
            if not okp or not okn:
                forced = -v if not okp else v
                break
            np_ = sum(1 for l in lp if abs(l) <= _NOR) - base
            nn_ = sum(1 for l in ln if abs(l) <= _NOR) - base
            sc = (1 + np_) * (1 + nn_)
            if sc > best:
                best, bv = sc, v
        if forced is not None:
            assum.append(forced)
            continue
        if bv is None:  # every orientation variable assigned
            return "ok", (assum, None)
        return "ok", (assum, bv)


def probe(args):
    """Random root-to-leaf walk; returns (cube literals, weight 1/p, path info)."""
    depth, seed = args
    rng = random.Random(seed)
    assum, weight, decisions = [], 1, 0
    t0 = time.time()
    while decisions < depth:
        st, res = lookahead(assum)
        if st == "refuted":
            # only reachable at the root, or if a child refuted after the parent chose it
            return {"refuted": True, "cube": assum, "weight": weight, "decisions": decisions,
                    "la_time": time.time() - t0}
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
    return {"refuted": False, "cube": assum, "weight": weight, "decisions": decisions,
            "la_time": time.time() - t0}


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
    a = ap.parse_args()
    n_or = comb(a.N, 3)
    workdir = a.workdir or os.path.dirname(os.path.abspath(a.out or a.cnf))
    seeds = [(a.depth, a.seed * 100003 + i) for i in range(a.samples)]
    out = open(a.out, "a") if a.out else sys.stdout
    with ProcessPoolExecutor(a.workers, initializer=_init, initargs=(a.cnf, n_or)) as ex:
        probes = list(ex.map(probe, seeds))
    with ProcessPoolExecutor(a.workers) as ex:
        jobs = [(a.cnf, p["cube"], a.cap, workdir) for p in probes]
        results = list(ex.map(solve_cube, jobs))
    for p, (st, dt) in zip(probes, results):
        rec = {"depth": a.depth, "decisions": p["decisions"], "cube_len": len(p["cube"]),
               "weight": p["weight"], "la_time": round(p["la_time"], 2), "status": st,
               "time": round(dt, 3), "cap": a.cap, "cube": p["cube"]}
        out.write(json.dumps(rec) + "\n")
        out.flush()


if __name__ == "__main__":
    main()
