"""CEGAR search for EFX counterexamples over a polyhedral valuation region (Z3, QF_LRA).

The question "is there an additive valuation profile v in region R with no
complete EFX(0) allocation?" is the satisfiability of

    R(v)  AND  AND_{A complete allocation}  Phi_A(v),
    Phi_A(v) = OR_{i != j, g in A_j}  v_i(A_i) < v_i(A_j) - v_i(g)      (A not EFX)

We never write all n^m clauses.  Loop:
  1. ask Z3 for v in R satisfying the clauses collected so far;
  2. unsat  -> no counterexample in R (proof modulo Z3's QF_LRA verdict;
               the allocation list is saved as a certificate and re-solved
               from scratch by `recheck`);
  3. sat    -> scale the rational model to integers per agent (exact; EFX is
               invariant under per-agent positive scaling) and run the exact
               checker; no EFX allocation -> COUNTEREXAMPLE (re-verified by
               full enumeration and the independent brute force); otherwise add
               Phi_A for the found allocation(s) and repeat.

Region R always contains: v >= 0, every row sums to 1 (Lemma "Normalization"
of Alkassar-Fouz-Mehlhorn arXiv:2608.08590: an all-zero row can be replaced by
any positive row), agent 0 sorted v_0(0) >= ... >= v_0(m-1) (relabel goods).
Optionally (--branch b1 b2 b3 ...), agent i>=1 has good b_i as a maximum
good.  The branches with b_1 <= ... <= b_{n-1} cover the space up to
permuting agents 1..n-1.

Clause reduction used (sound; cf. AFM Lemma M items 1 and 3): if the region
implies v_i(g) >= v_i(h) for g, h in the target A_j, the remove-g disjunct
implies the remove-h disjunct and is dropped (see _keep_goods); disjuncts for
singleton targets are dropped (they say v_i(A_i) < 0, false under v >= 0).
`recheck` re-solves with the full unreduced clauses, so a final unsat does
not depend on this reduction.  With lemma_m=True also AFM Lemma M items 2-3
(dominance between disjuncts, disjuncts false on the region); see
reduced_disjuncts and test_efx.test_lemma_m_equivalence.

Options (all off by default; measured in problem file, Approach 4a):
c0 (Lemma C0': agent 0 has the largest top-two sum; a fixed symmetric set
intersected with every region, so a run must use it everywhere or nowhere),
lemma_m, multi / seed_points (heuristic choice of extra allocations),
z3opts (e.g. {"smt.arith.solver": 2}).

Usage:
  python3 cegar.py --n 4 --m 7                       # whole space
  python3 cegar.py --n 4 --m 8 --branch 0 0 0 --timeout 600
"""
import argparse
import json
import math
import sys
import time
from fractions import Fraction

import z3

import efx


def build_vars(n, m):
    return [[z3.Real(f"v_{i}_{g}") for g in range(m)] for i in range(n)]


def prefixes_of(n, m, branch):
    """Known value chains per agent: agent 0 fully sorted; agent i >= 1 has
    the chain branch[i-1] (an int b_i or a list [b_i, s_i, ...]) meaning
    v_i(p_0) >= v_i(p_1) >= ... >= v_i(p_last) >= v_i(h) for all other h."""
    pre = [list(range(m))] + [[] for _ in range(n - 1)]
    if branch:
        for i, b in enumerate(branch, start=1):
            pre[i] = list(b) if isinstance(b, (list, tuple)) else [b]
    return pre


def c0_pairs(n, m, branch):
    """Lemma C0' (problem file, Approach 4): agent 0 has the largest normalised
    top-two sum.  Returns, per agent i >= 1, the pairs {x, y} whose sum must be
    <= v_0(0) + v_0(1): (p_0, p_1) if agent i's chain has length >= 2, else
    (p_0, g) for every g != p_0 (their max is i's top-two sum)."""
    pres = prefixes_of(n, m, branch)
    out = []
    for i in range(1, n):
        p = pres[i]
        if len(p) >= 2:
            out.append((i, [(p[0], p[1])]))
        elif len(p) == 1:
            out.append((i, [(p[0], g) for g in range(m) if g != p[0]]))
        else:
            out.append((i, [(g, h) for g in range(m) for h in range(g + 1, m)]))
    return out


def region(V, n, m, branch=None, extra=None, sort0=True, c0=False):
    cons = []
    for i in range(n):
        cons += [V[i][g] >= 0 for g in range(m)]
        cons.append(z3.Sum(V[i]) == 1)
    pres = prefixes_of(n, m, branch) if sort0 else [[] for _ in range(n)]
    for i, p in enumerate(pres):
        cons += [V[i][p[t]] >= V[i][p[t + 1]] for t in range(len(p) - 1)]
        if p:
            cons += [V[i][p[-1]] >= V[i][h] for h in range(m) if h not in p]
    if c0:
        assert sort0 and m >= 2
        for i, prs in c0_pairs(n, m, branch):
            cons += [V[0][0] + V[0][1] >= V[i][x] + V[i][y] for x, y in prs]
    if extra:
        cons += extra(V)
    return cons


def _keep_goods(bundle, chain):
    """Goods g of a target bundle whose remove-g disjunct must be kept.

    The remove-g disjunct  own < v(B) - v(g)  is implied by (so may be
    replaced by) the remove-h disjunct whenever v(g) >= v(h) is known.  Goods
    in the chain dominate all goods outside it, and earlier chain goods
    dominate later ones.  So: if B has goods outside the chain, keep exactly
    those; otherwise keep only B's last good in chain order."""
    pos = {g: t for t, g in enumerate(chain)}
    outside = [g for g in bundle if g not in pos]
    if outside:
        return outside
    return [max(bundle, key=lambda g: pos[g])]


def known_ge(chain, x, y):
    """v(x) >= v(y) is implied by the region's syntactic order for an agent
    whose known chain is `chain` (agent 0: the full sort range(m))."""
    if x == y:
        return True
    pos = {g: t for t, g in enumerate(chain)}
    return x in pos and (y not in pos or pos[x] <= pos[y])


def dominated(T, U, chain):
    """Is there an injective map phi: T -> U with v(x) <= v(phi(x)) known for
    all x in T?  Then v(T) <= v(U) on the region (v >= 0).  Bipartite matching."""
    if len(T) > len(U):
        return False
    U = list(U)
    match = {}

    def aug(x, seen):
        for k, u in enumerate(U):
            if k not in seen and known_ge(chain, u, x):
                seen.add(k)
                if k not in match or aug(match[k], seen):
                    match[k] = x
                    return True
        return False
    return all(aug(x, set()) for x in T)


def reduced_disjuncts(bundles, i, chain, lemma_m):
    """(j, g) pairs whose disjunct  v_i(A_i) < v_i(A_j) - v_i(g)  is kept.
    Item 1 of AFM Lemma M (minimal g in the known order) and singleton targets
    always; with lemma_m also items 2 (dominance between disjuncts, removed
    sequentially so each removed disjunct implies a kept one) and 3 (trimmed
    target known-dominated by the own bundle, so the disjunct is false)."""
    ds = []
    for j in range(len(bundles)):
        if j == i or len(bundles[j]) <= 1:
            continue
        for g in _keep_goods(bundles[j], chain):
            ds.append((j, g, [x for x in bundles[j] if x != g]))
    if not lemma_m:
        return [(j, g) for j, g, _ in ds]
    ds = [d for d in ds if not dominated(d[2], bundles[i], chain)]
    keep = list(ds)
    for d in ds:
        if any(e is not d and dominated(d[2], e[2], chain) for e in keep):
            keep = [e for e in keep if e is not d]
    return [(j, g) for j, g, _ in keep]


def clause(V, alloc, n, m, branch=None, sort0=True, lemma_m=False):
    bundles = [[g for g in range(m) if alloc[g] == i] for i in range(n)]
    pre = prefixes_of(n, m, branch) if sort0 else [[] for _ in range(n)]
    lits = []
    for i in range(n):
        own = z3.Sum([V[i][g] for g in bundles[i]]) if bundles[i] else z3.RealVal(0)
        for j, g in reduced_disjuncts(bundles, i, pre[i], lemma_m):
            tj = z3.Sum([V[i][h] for h in bundles[j]])
            lits.append(own < tj - V[i][g])
    return z3.Or(lits) if lits else z3.BoolVal(False)


def model_to_int(mdl, V, n, m):
    rows = []
    for i in range(n):
        fr = []
        for g in range(m):
            x = mdl.eval(V[i][g], model_completion=True)
            fr.append(Fraction(x.numerator_as_long(), x.denominator_as_long()))
        den = 1
        for x in fr:
            den = den * x.denominator // math.gcd(den, x.denominator)
        rows.append([int(x * den) for x in fr])
    return rows


def exact_exists(v):
    """Exact existence, also for values too big for the int64 C checker."""
    flat = [x for r in v for x in r]
    if max(flat) * len(v[0]) < 2 ** 62:
        return efx.full(v)
    # fall back to pure Python (big integers)
    allocs = efx.brute(v, want_all=True)
    return (bool(allocs), None, len(allocs), list(allocs[0]) if allocs else None)


def sample_region(n, m, branch, k, rng, c0=False):
    """k random float points of the region (heuristic, for seeding and for
    extra points around a model; soundness never depends on them).  Mixes
    uniform rows with near-identical rows (AFM's hard "diagonal")."""
    import numpy as np
    pres = prefixes_of(n, m, branch)
    pts = []
    for _ in range(k):
        w = np.sort(rng.dirichlet(np.full(m, rng.choice([0.3, 1.0, 3.0]))))[::-1]
        eps = rng.choice([1.0, 0.3, 0.1, 0.03, 0.01, 0.003])
        v = np.zeros((n, m))
        for i in range(n):
            u = w + eps * rng.random(m) * w.mean()
            if rng.random() < 0.2:
                u = rng.dirichlet(np.ones(m))
            u = np.sort(u)[::-1]
            p = pres[i]
            rest = [g for g in range(m) if g not in p]
            if rng.random() < 0.3:
                rng.shuffle(rest)
            for t, g in enumerate(list(p) + rest):
                v[i, g] = u[t]
            v[i] /= v[i].sum()
        if c0:
            t2 = [v[i].max() + np.sort(v[i])[-2] for i in range(n)]
            a = int(np.argmax(t2))
            if a != 0:
                v[0] = np.sort(v[a])[::-1]
        pts.append(v)
    return pts


class Cover:
    """Float check: which points are (strictly) EFX under some stored allocation."""

    def __init__(self, n, m):
        import numpy as np
        self.np, self.n, self.m = np, n, m
        self.masks = np.zeros((0, n, m), dtype=bool)

    def add(self, a):
        np = self.np
        mk = np.zeros((1, self.n, self.m), dtype=bool)
        for g, o in enumerate(a):
            mk[0, o, g] = True
        self.masks = np.concatenate([self.masks, mk])

    def covered(self, v, tol=1e-9):
        np = self.np
        if len(self.masks) == 0:
            return False
        M = self.masks                                   # s, k, g
        vb = np.einsum('ig,skg->sik', v, M)              # s, i, k
        mins = np.where(M[:, :, None, :], v[None, None, :, :], np.inf).min(-1)  # s, k, i
        r = vb - mins.transpose(0, 2, 1)                 # s, i, k  (-inf if empty)
        idx = np.arange(self.n)
        own = vb[:, idx, idx]
        r[:, idx, idx] = -np.inf
        return bool(((own - r.max(-1)) >= tol).all(-1).any())


def float_to_int(v, scale=10**9):
    return [[int(round(x * scale)) for x in row] for row in v]


def cegar(n, m, branch=None, timeout=600, max_iter=10**9, log=None, extra=None,
          seed_allocs=(), stats=None, sort0=True, c0=False, lemma_m=False,
          multi=0, seed_points=0, z3opts=None, rng_seed=0):
    """multi: extra random points per model (convex combinations of the model
    with random region points), each uncovered one adds its best EFX
    allocation; seed_points: random region points processed the same way
    before the first solve.  Both only choose WHICH allocations enter the
    certificate; the unsat verdict is about the stored list alone."""
    V = build_vars(n, m)
    if z3opts:
        for k, val in z3opts.items():
            z3.set_param(k, val)
    s = z3.Solver()
    s.set("timeout", int(timeout * 1000))
    s.add(region(V, n, m, branch, extra, sort0, c0))
    allocs = []
    seen = set()
    cov = Cover(n, m) if (multi or seed_points) else None
    t0 = time.time()

    def add_alloc(a):
        a = tuple(a)
        if a in seen:
            return False
        seen.add(a)
        allocs.append(list(a))
        s.add(clause(V, a, n, m, branch, sort0, lemma_m))
        if cov is not None:
            cov.add(a)
        return True

    def try_point(pf):
        """pf: float point.  Returns a counterexample record or None."""
        if cov.covered(pf):
            return None
        vi = float_to_int(pf)
        ok, sc, cnt, wit = exact_exists(vi)
        if not ok:
            rec = {"status": "COUNTEREXAMPLE_CANDIDATE", "v": vi, "branch": branch,
                   "source": "extra point", "brute": efx.brute(vi) if n ** m <= 4 ** 9 else None}
            print("!!!!!!!! CEGAR: NO EFX ALLOCATION !!!!!!!!", json.dumps(rec), flush=True)
            return rec
        assert efx.verify(vi, wit)
        add_alloc(wit)
        return None

    for a in seed_allocs:
        add_alloc(a)
    if seed_points or multi:
        import numpy as np
        rng = np.random.default_rng(rng_seed)
    if seed_points:
        for pf in sample_region(n, m, branch, seed_points, rng, c0 and sort0):
            rec = try_point(pf)
            if rec:
                return rec
    if stats is not None:
        stats["seeded"] = len(allocs)
        stats["seed_seconds"] = time.time() - t0
    it = 0
    while it < max_iter:
        it += 1
        rem = timeout - (time.time() - t0)
        if rem <= 0:
            return {"status": "timeout", "iters": it, "allocs": allocs,
                    "seconds": time.time() - t0}
        s.set("timeout", int(rem * 1000))
        r = s.check()
        if r == z3.unsat:
            return {"status": "unsat", "iters": it, "allocs": allocs,
                    "seconds": time.time() - t0}
        if r == z3.unknown:
            return {"status": "timeout", "iters": it, "allocs": allocs,
                    "seconds": time.time() - t0}
        v = model_to_int(s.model(), V, n, m)
        ok, sc, cnt, wit = exact_exists(v)
        if not ok:
            rec = {"status": "COUNTEREXAMPLE_CANDIDATE", "v": v, "iters": it,
                   "branch": branch, "brute": efx.brute(v) if n ** m <= 4 ** 9 else None}
            print("!!!!!!!! CEGAR: NO EFX ALLOCATION !!!!!!!!", json.dumps(rec), flush=True)
            return rec
        a = tuple(wit)
        assert efx.verify(v, list(a))
        if stats is not None:
            stats["models"] = stats.get("models", 0) + 1
            if cnt is not None and cnt < stats.get("min_count", 10**18):
                stats["min_count"], stats["min_count_v"] = cnt, v
                stats["min_count_score"] = sc
        if a in seen:
            raise RuntimeError("solver returned a point violating a stored clause")
        add_alloc(a)
        if multi:
            import numpy as np
            vf = np.array([[x / sum(row) for x in row] for row in v], dtype=float)
            for k, pf in enumerate(sample_region(n, m, branch, multi, rng, c0 and sort0)):
                t = 0.5 ** (k % 8 + 1)
                rec = try_point((1 - t) * vf + t * pf)
                if rec:
                    return rec
        if log and it % 50 == 0:
            print(f"  iter {it} allocs {len(allocs)} t={time.time()-t0:.1f}s", file=log, flush=True)
    return {"status": "maxiter", "iters": it, "allocs": allocs, "seconds": time.time() - t0}


def recheck(n, m, branch, allocs, full_clauses=True, timeout=3600, c0=False):
    """Re-solve from scratch: region AND all stored clauses must be unsat.

    With full_clauses=True the clauses are rebuilt WITHOUT the agent-0
    reduction (all i != j, g in A_j, singletons included), so the verdict does
    not depend on the reduction lemma.
    """
    V = build_vars(n, m)
    s = z3.Solver()
    s.set("timeout", int(timeout * 1000))
    s.add(region(V, n, m, branch, c0=c0))
    for a in allocs:
        bundles = [[g for g in range(m) if a[g] == i] for i in range(n)]
        lits = []
        for i in range(n):
            own = z3.Sum([V[i][g] for g in bundles[i]]) if bundles[i] else z3.RealVal(0)
            for j in range(n):
                if j == i or not bundles[j]:
                    continue
                tj = z3.Sum([V[i][g] for g in bundles[j]])
                for g in bundles[j]:
                    lits.append(own < tj - V[i][g])
        s.add(z3.Or(lits) if full_clauses else clause(V, a, n, m, branch))
    return str(s.check())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--m", type=int, default=7)
    p.add_argument("--branch", type=int, nargs="*", default=None)
    p.add_argument("--branch-json", default=None,
                   help='chains per agent 1..n-1, e.g. "[[0,1],[0,1],[0,1]]"')
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--out", default=None)
    p.add_argument("--box", default=None,
                   help="JSON integer profile c; search only the box |v - c/rowsum| <= delta "
                        "(no sorting / branch constraints: a local exhaustive search)")
    p.add_argument("--delta", type=float, default=0.01)
    p.add_argument("--recheck", action="store_true")
    a = p.parse_args()
    if a.branch_json:
        a.branch = json.loads(a.branch_json)
    st = {}
    extra, sort0 = None, True
    if a.box:
        c = json.loads(a.box)
        a.n, a.m = len(c), len(c[0])
        cn = [[Fraction(x, sum(r)) for x in r] for r in c]
        d = Fraction(a.delta).limit_denominator(10**6)

        def extra(V):
            return [z3.And(V[i][g] >= z3.RealVal(cn[i][g] - d), V[i][g] <= z3.RealVal(cn[i][g] + d))
                    for i in range(a.n) for g in range(a.m)]
        sort0 = False
    res = cegar(a.n, a.m, a.branch or None, a.timeout, log=sys.stderr, stats=st,
                extra=extra, sort0=sort0)
    summ = {k: res[k] for k in res if k != "allocs"}
    summ.update({"n": a.n, "m": a.m, "branch": a.branch, "box": a.box, "delta": a.delta, "z3": z3.get_version_string(),
                 "num_allocs": len(res.get("allocs", [])), "stats": st})
    if a.recheck and res["status"] == "unsat":
        summ["recheck_full_clauses"] = recheck(a.n, a.m, a.branch, res["allocs"])
    print(json.dumps(summ))
    if a.out:
        with open(a.out, "a") as f:
            f.write(json.dumps({**summ, "allocs": res.get("allocs")}) + "\n")
