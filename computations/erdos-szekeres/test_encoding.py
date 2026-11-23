"""Empirical cross-checks of encode.py against real point sets.

1. For random integer point sets, sorted by x, take the orientation assignment.
   It must satisfy every signotope clause. It must satisfy all no-convex-k-gon
   clauses iff brute force finds no k points in convex position.
2. The symmetry-breaking transform from problems/erdos-szekeres.md, applied
   to a hull vertex p0, must preserve every triple orientation (after
   relabelling) and give X(0,b,c) = true.
"""
import itertools
import random
from fractions import Fraction

from construct import check, es_set, orient
from encode import build


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
