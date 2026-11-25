"""tau_k(p): the least number of folded speed classes covering every folded
time class 1..(p-1)/2, where class v covers time a iff (k+1)*d_p(a v) < p
(Allikvere, arXiv:2609.02604v2, Sec. 4, eq. (cover)).

Exact: SAT (pysat, CaDiCaL) with a cardinality constraint "at most s classes",
class 1 forced into the cover (unit symmetry: v covers a iff uv covers u^-1 a,
so any cover can be scaled to contain class 1).  tau = least satisfiable s.
For s = tau the cover found is re-checked directly; for s = tau-1 UNSAT is
the solver's verdict (not independently certified).
Usage: python3 tau.py k pmin pmax
"""
import sys
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType


def dp(x, p):
    r = x % p
    return min(r, p - r)


def covers(k, p):
    h = (p - 1) // 2
    return {v: {a for a in range(1, h + 1) if (k + 1) * dp(a * v, p) < p} for v in range(1, h + 1)}


def tau(k, p, smax=None):
    h = (p - 1) // 2
    cov = covers(k, p)
    by_time = {a: [v for v in cov if a in cov[v]] for a in range(1, h + 1)}
    lo = -(-h // len(cov[1]))
    s = lo
    while True:
        cnf = CardEnc.atmost(lits=list(range(1, h + 1)), bound=s, top_id=h, encoding=EncType.seqcounter)
        with Solver(name="cadical153", bootstrap_with=cnf.clauses) as S:
            S.add_clause([1])
            for a in range(1, h + 1):
                S.add_clause(by_time[a])
            if S.solve():
                C = [v for v in S.get_model() if 0 < v <= h]
                assert len(C) <= s and set().union(*(cov[v] for v in C)) == set(range(1, h + 1))
                return s, sorted(C)
        s += 1
        if smax and s > smax:
            return None, None


if __name__ == "__main__":
    k, a, b = map(int, sys.argv[1:4])
    for p in range(max(a, k + 2), b + 1):
        if any(p % q == 0 for q in range(2, int(p ** .5) + 1)):
            continue
        t, C = tau(k, p)
        print(p, t, " ".join(map(str, C)), flush=True)
