"""Independent re-check of CEGAR certificates with cvc5 (second solver, second encoding).

A certificate is a JSONL record {n, m, branch, status: "unsat", allocs}.  This
script does not import cegar.py.  It rebuilds from the record alone:
  region:  v >= 0; each row sums to 1; agent 0 sorted v_0(0) >= ... >= v_0(m-1);
           for agent i >= 1 with chain [p_0, ..., p_k] (or a bare int b):
           v_i(p_0) >= ... >= v_i(p_k) >= v_i(h) for all other goods h;
  clauses: for each stored allocation A, the FULL unreduced disjunction over
           i != j, g in A_j of  v_i(A_i) < v_i(A_j) - v_i(g);
and asks cvc5 for satisfiability.  It also checks that every stored
allocation is a complete allocation (length m, owners in 0..n-1).
The script prints the number of unsat records and lists every record that
is not unsat.

It also checks coverage: for a whole-space run, the set of branches must be
all multisets b_1 <= ... <= b_{n-1} of goods (with --cover).

Usage: python3 recheck_cvc5.py data/cegar_branches_n4_m7.jsonl [--cover]
"""
import itertools
import json
import sys

from cvc5.pythonic import And, Or, Real, RealVal, Solver, Sum, sat, unsat


def check_record(r):
    n, m = r["n"], r["m"]
    V = [[Real(f"x{i}_{g}") for g in range(m)] for i in range(n)]
    s = Solver()
    for i in range(n):
        for g in range(m):
            s.add(V[i][g] >= 0)
        s.add(Sum(V[i]) == 1)
    for g in range(m - 1):
        s.add(V[0][g] >= V[0][g + 1])
    for i, b in enumerate(r["branch"] or [], start=1):
        chain = b if isinstance(b, list) else [b]
        for t in range(len(chain) - 1):
            s.add(V[i][chain[t]] >= V[i][chain[t + 1]])
        for h in range(m):
            if h not in chain:
                s.add(V[i][chain[-1]] >= V[i][h])
    for a in r["allocs"]:
        assert len(a) == m and all(0 <= x < n for x in a), "malformed allocation"
        B = [[g for g in range(m) if a[g] == i] for i in range(n)]
        lits = []
        for i in range(n):
            own = Sum([V[i][g] for g in B[i]]) if B[i] else RealVal(0)
            for j in range(n):
                if j != i:
                    for g in B[j]:
                        lits.append(own < Sum([V[i][h] for h in B[j] if h != g] or [RealVal(0)]))
        s.add(Or(lits) if lits else RealVal(0) > RealVal(1))
    return s.check()


if __name__ == "__main__":
    path = sys.argv[1]
    recs = [json.loads(l) for l in open(path)]
    recs = [r for r in recs if r.get("allocs") is not None and r["status"] == "unsat"]
    bad = []
    for r in recs:
        res = check_record(r)
        if res != unsat:
            bad.append((r["branch"], str(res)))
    print(f"{len(recs)} unsat records rechecked with cvc5; not unsat: {bad}")
    if "--cover" in sys.argv:
        n, m = recs[0]["n"], recs[0]["m"]
        want = set(itertools.combinations_with_replacement(range(m), n - 1))
        got = {tuple(r["branch"]) for r in recs}
        print("coverage of all argmax branches:", "COMPLETE" if want <= got else f"MISSING {sorted(want - got)}")
