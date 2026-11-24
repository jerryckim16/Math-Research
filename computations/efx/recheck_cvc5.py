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

If a record has "c0": true, the region also contains Lemma C0' (problem
file, Approach 4): v_0(0) + v_0(1) >= v_i(x) + v_i(y) for every agent i >= 1
and every pair of goods x != y (all pairs; cegar.py writes an equivalent
shorter form using the chains).

It also checks coverage: for a whole-space run, the set of branches must be
all multisets b_1 <= ... <= b_{n-1} of goods (with --cover).  With --tree it
checks coverage through any number of refinement levels: a node is a tuple of
chains (one per agent 1..n-1); the roots are the argmax branches; a node is
covered if it carries an unsat record, or if all its children under one of
the rules below are covered:
  "all":  every agent's chain is extended by one good not in it, and among
          agents with identical chains the new goods are non-decreasing in
          agent order (swapping two such agents maps the node to itself);
  "k":    only agent k's chain is extended (no symmetry used).
All records used for coverage must agree on n, m and the c0 flag (mixing
regions with and without C0 could leave instances without a representative).

Usage: python3 recheck_cvc5.py FILE.jsonl [FILE2.jsonl ...] [--cover] [--tree] [--workers=4]
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
    if r.get("c0"):
        for i in range(1, n):
            for x in range(m):
                for y in range(x + 1, m):
                    s.add(V[0][0] + V[0][1] >= V[i][x] + V[i][y])
    for a in r["allocs"]:
        if isinstance(a, str):
            a = [int(c) for c in a]
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


def _check_str(r):
    return str(check_record(r))


def node_of(branch):
    return tuple(tuple(b) if isinstance(b, list) else (b,) for b in branch)


def children(node, m, rule):
    if rule == "all":
        opts = [[x for x in range(m) if x not in c] for c in node]
        out = []
        for xs in itertools.product(*opts):
            if all(xs[i] <= xs[j] for i in range(len(node)) for j in range(i + 1, len(node))
                   if node[i] == node[j]):
                out.append(tuple(c + (x,) for c, x in zip(node, xs)))
        return out
    k = rule
    return [tuple(c + (x,) if i == k else c for i, c in enumerate(node))
            for x in range(m) if x not in node[k]]


def tree_coverage(recs):
    n, m, c0 = recs[0]["n"], recs[0]["m"], bool(recs[0].get("c0"))
    assert all((r["n"], r["m"], bool(r.get("c0"))) == (n, m, c0) for r in recs), \
        "records disagree on n, m or c0"
    closed = {node_of(r["branch"]) for r in recs}
    prefixes = set()
    for c in closed:
        for ls in itertools.product(*[range(1, len(ch) + 1) for ch in c]):
            prefixes.add(tuple(ch[:l] for ch, l in zip(c, ls)))
    memo = {}

    def covered(node):
        if node in closed:
            return True
        if node not in prefixes:
            return False
        if node not in memo:
            memo[node] = False
            for rule in ["all"] + list(range(n - 1)):
                if all(covered(ch) for ch in children(node, m, rule)):
                    memo[node] = True
                    break
        return memo[node]
    roots = [tuple((b,) for b in br) for br in itertools.combinations_with_replacement(range(m), n - 1)]
    missing = [r for r in roots if not covered(r)]
    return n, m, c0, len(roots), missing


if __name__ == "__main__":
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    import gzip
    recs = [json.loads(l) for path in paths
            for l in (gzip.open(path, "rt") if path.endswith(".gz") else open(path))]
    recs = [r for r in recs if r.get("allocs") is not None and r["status"] == "unsat"]
    workers = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--workers=")), "1"))
    if workers > 1:
        import multiprocessing as mp
        with mp.Pool(workers) as pool:
            verdicts = pool.map(_check_str, recs, chunksize=1)
    else:
        verdicts = [_check_str(r) for r in recs]
    bad, good = [], []
    for r, res in zip(recs, verdicts):
        if res != "unsat":
            bad.append((r["branch"], str(res)))
        else:
            good.append(r)
    print(f"{len(recs)} unsat records rechecked with cvc5; not unsat: {bad}")
    if "--cover" in sys.argv:
        n, m = recs[0]["n"], recs[0]["m"]
        want = set(itertools.combinations_with_replacement(range(m), n - 1))
        got = {tuple(r["branch"]) for r in good if all(isinstance(b, int) for b in r["branch"])}
        print("coverage of all argmax branches:", "COMPLETE" if want <= got else f"MISSING {sorted(want - got)}")
    if "--tree" in sys.argv:
        n, m, c0, nroots, missing = tree_coverage(good)
        depth = {}
        for r in good:
            d = max(len(node_of(r["branch"])[i]) for i in range(n - 1))
            depth[d] = depth.get(d, 0) + 1
        print(f"tree coverage (n={n}, m={m}, c0={c0}): {nroots - len(missing)}/{nroots} branches covered; "
              f"closed regions by max chain length {dict(sorted(depth.items()))}")
        print("uncovered branches:", missing if missing else "none")
