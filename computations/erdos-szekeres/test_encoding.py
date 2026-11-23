"""Empirical cross-checks of encode.py against real point sets.

1. For random integer point sets, sorted by x, take the orientation assignment.
   It must satisfy every signotope clause. It must satisfy all no-convex-k-gon
   clauses iff brute force finds no k points in convex position.
   Note: with these parameters essentially every random set contains a
   k-gon, so this check is one-sided; item 2 uses a balanced generator
   (random subsets of the explicit ES sets supply the k-gon-free side) and
   re-checks encode.py there too.
2. encode_compact.py on a balanced mix of random sets: with the auxiliary
   variables set to their defining statements, every definitional clause holds
   and the whole formula holds iff there is no convex k-gon (soundness); and
   with the orientations fixed, the formula is satisfiable (by any aux values)
   iff there is no convex k-gon (it forbids every k-gon), checked with a SAT
   solver.
3. The symmetry-breaking transform from problems/erdos-szekeres.md, applied
   to a hull vertex p0, must preserve every triple orientation (after
   relabelling) and give X(0,b,c) = true.
"""
import itertools
import random
from fractions import Fraction

from construct import check, es_set, orient
from encode import build
import encode_compact


def assignment(pts):
    pts = sorted(pts)
    return pts, {t: orient(*(pts[i] for i in t)) > 0 for t in itertools.combinations(range(len(pts)), 3)}


def satisfies(var, clauses, val):
    inv = {v: t for t, v in var.items()}
    lit = lambda l: val[inv[abs(l)]] if l > 0 else not val[inv[abs(l)]]
    return all(any(lit(l) for l in cl) for cl in clauses)


def random_general(N, R, rng):
    while True:
        pts = [(rng.randrange(R), rng.randrange(R)) for _ in range(N)]
        if len({p[0] for p in pts}) < N:
            continue
        if all(orient(*t) != 0 for t in itertools.combinations(pts, 3)):
            return pts


def symmetry_transform(pts):
    """Return (new_pts, label map old->new) per the lemma; p0 = lowest point (a hull vertex)."""
    p0 = min(pts, key=lambda p: (p[1], p[0]))
    others = [p for p in pts if p != p0]
    # affine (dx, dy) -> (dx + L*dy, -dx), det = L > 0, so orientations are kept.
    # p0 is lowest-then-leftmost, so every other point has dy > 0, or dy = 0
    # and dx > 0. With L > max|dx| all of them get new x > 0.
    L = 1 + max(abs(p[0] - p0[0]) for p in others)
    A = {p: ((p[0] - p0[0]) + L * (p[1] - p0[1]), -(p[0] - p0[0])) for p in others}
    # psi(x,y) = (y/x, -1/x), then reflect y -> -y: (y/x, 1/x)
    T = {p: (Fraction(a[1], a[0]), Fraction(1, a[0])) for p, a in A.items()}
    xs = [t[0] for t in T.values()]
    M = 10 ** 6 * (1 + max(abs(c) for t in T.values() for c in t))
    new0 = (min(xs) - M, M * M)
    new = {p0: new0, **T}
    return new


ES_SETS = {n: es_set(n) for n in (5, 6, 7)}


def mixed_instance(rng):
    """Random instance with both outcomes well represented.

    Uniform random sets with N close to ES(k) (mostly contain a k-gon), and
    random subsets of the explicit Erdos-Szekeres sets (never contain one).
    """
    if rng.random() < 0.5:
        N, k = rng.choice([(4, 4), (6, 5), (7, 5), (8, 6), (9, 6), (10, 7), (12, 7), (14, 7)])
        return random_general(N, 200, rng), k
    k = rng.choice([5, 6, 7])
    E = ES_SETS[k]
    return rng.sample(E, rng.randint(k, min(len(E), 14))), k


def compact_check(rng, trials=400):
    from pysat.solvers import Solver
    agree = n_gon = 0
    for trial in range(trials):
        raw, k = mixed_instance(rng)
        N = len(raw)
        pts, val = assignment(raw)
        # the old encoding on the same instance (its own random test above is one-sided)
        ovar, ocl = build(N, k, sym=False)
        n_sig = 8 * len(list(itertools.combinations(range(N), 4)))
        var, aux, clauses, nv = encode_compact.build(N, k, sym=False)
        t = encode_compact.aux_truth(N, k, val)
        full = {**{var[x]: val[x] for x in var}, **{aux[x]: t[x] for x in aux}}
        lit = lambda l: full[abs(l)] if l > 0 else not full[abs(l)]
        res = check(pts, k)
        has_gon = res is not None and "convex" in res
        assert satisfies(ovar, ocl[n_sig:], val) == (not has_gon), ("old encoding", pts, k)
        bad = [cl for cl in clauses if not any(lit(l) for l in cl)]
        # only prohibition clauses (all literals negative aux) may fail, and only if there is a k-gon
        assert all(all(l < 0 and abs(l) > len(var) for l in cl) for cl in bad), "definitional clause fails"
        assert (len(bad) == 0) == (not has_gon), (pts, k, has_gon, len(bad))
        with Solver(name="cadical153", bootstrap_with=clauses) as s:
            sat = s.solve(assumptions=[var[x] if val[x] else -var[x] for x in var])
        assert sat == (not has_gon), (pts, k, has_gon, sat)
        agree += 1
        n_gon += has_gon
    print(f"compact encoding (and encode.py): aux-truth assignment and SAT check agree with brute force on {agree} random point sets "
          f"({n_gon} with a convex k-gon, {agree - n_gon} without)")
    # the explicit Erdos-Szekeres sets (2^(n-2) points, no convex n-gon) satisfy the full compact formula
    for n in (5, 6, 7):
        pts, val = assignment(es_set(n))
        N = len(pts)
        var, aux, clauses, nv = encode_compact.build(N, n, sym=False)
        t = encode_compact.aux_truth(N, n, val)
        full = {**{var[x]: val[x] for x in var}, **{aux[x]: t[x] for x in aux}}
        assert all(any(full[abs(l)] == (l > 0) for l in cl) for cl in clauses)
    print("ES lower-bound sets satisfy the compact no-k-gon formula (n=5,6,7; N=8,16,32)")


def main():
    rng = random.Random(1)
    agree = 0
    for trial in range(300):
        N, k = rng.choice([(8, 5), (9, 5), (10, 5), (7, 4), (12, 6)])
        pts, val = assignment(random_general(N, 60, rng))
        var, clauses = build(N, k, sym=False)
        n_sig = 8 * len(list(itertools.combinations(range(N), 4)))
        sig, gon = clauses[:n_sig], clauses[n_sig:]
        assert satisfies(var, sig, val), "signotope axiom violated by a real point set"
        has_gon = check(pts, k) is not None and "convex" in check(pts, k)
        assert satisfies(var, gon, val) == (not has_gon), (pts, k, has_gon)
        agree += 1
    print(f"encoding agrees with brute force on {agree} random point sets")

    # the Erdos-Szekeres sets themselves must satisfy the full no-k-gon formula
    for n in (5, 6):
        pts, val = assignment(es_set(n))
        var, clauses = build(len(pts), n, sym=False)
        assert satisfies(var, clauses, val)
    print("ES lower-bound sets satisfy the no-k-gon formula (n=5,6)")

    compact_check(rng)

    for trial in range(200):
        pts = random_general(rng.choice([5, 7, 9]), 50, rng)
        new = symmetry_transform(pts)
        for t in itertools.combinations(pts, 3):
            assert (orient(*t) > 0) == (orient(*(new[p] for p in t)) > 0), "orientation changed"
        order = sorted(pts, key=lambda p: new[p][0])
        assert len({new[p][0] for p in pts}) == len(pts)
        p0 = min(pts, key=lambda p: (p[1], p[0]))
        assert order[0] == p0
        assert all(orient(new[order[0]], new[b], new[c]) > 0 for b, c in itertools.combinations(order[1:], 2))
    print("symmetry-breaking transform preserves all orientations and gives X(0,b,c)=true on 200 random sets")


if __name__ == "__main__":
    main()
