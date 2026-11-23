"""Explicit Erdos-Szekeres lower-bound sets, verified by brute force.

Builds 2^(n-2) points in general position with no n points in convex
position, using the classical construction (Erdos-Szekeres 1961) with exact
integer coordinates, then checks every n-subset exhaustively.

g(a, b): C(a+b-4, a-2) points with no a-cup and no b-cap. It is built from
X = g(a-1, b) and Y = g(a, b-1), with Y placed so that every X-to-Y slope
exceeds every slope inside X or inside Y.

Top level: blocks B_i = g(i+2, n-i), i = 0..n-2, placed left to right along a
steep concave chain. Every inter-block slope exceeds every intra-block slope,
and the slopes between consecutive blocks decrease.
"""
import itertools
import sys
from fractions import Fraction
from math import comb


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def max_abs_slope(P):
    m = Fraction(0)
    for p, q in itertools.combinations(P, 2):
        m = max(m, abs(Fraction(q[1] - p[1], q[0] - p[0])))
    return m


def bbox(P):
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    return min(xs), max(xs), min(ys), max(ys)


def place_right_steep(X, Y):
    """Shift Y so that every slope from X to Y exceeds every slope inside X and Y."""
    M = max(max_abs_slope(X), max_abs_slope(Y), Fraction(1)) + 1
    x0, x1, y0, y1 = bbox(X)
    u0, u1, v0, v1 = bbox(Y)
    dx = x1 - u0 + 1                         # Y strictly right of X
    width = (u1 + dx) - x0                   # max horizontal distance X -> Y
    # need (dy + v0 - y1) / width > M  for the worst pair
    dy = int(M * width) + 1 + y1 - v0 + 1
    return X + [(p[0] + dx, p[1] + dy) for p in Y]


def g(a, b):
    if a <= 2 or b <= 2:
        return [(0, 0)]
    return place_right_steep(g(a - 1, b), g(a, b - 1))


def es_set(n):
    blocks = [g(i + 2, n - i) for i in range(n - 1)]
    M = max([max_abs_slope(B) for B in blocks if len(B) > 1] + [Fraction(1)]) + 1
    W = max(bbox(B)[1] - bbox(B)[0] for B in blocks) + 1
    H = max(bbox(B)[3] - bbox(B)[2] for B in blocks) + 1
    k = len(blocks)
    # consecutive macro slopes s_0 > s_1 > ... > s_{k-2} > M; consecutive
    # ratios are >= 1 + 1/k. Blocks are tiny compared with the step, so every
    # point-to-point slope between blocks l < l' stays within a factor
    # (1 +- 1/(10k)) of the macro chord slope.
    base = 2 * (int(M) + 2)
    slopes = [base * (k - l) for l in range(k - 1)]
    step = 100 * k * (W + H) * base
    pts, cx, cy = [], 0, 0
    for l, B in enumerate(blocks):
        bx0, _, by0, _ = bbox(B)
        pts += [(p[0] - bx0 + cx, p[1] - by0 + cy) for p in B]
        if l < k - 1:
            cx += step
            cy += slopes[l] * step
    return pts


def check(pts, n):
    N = len(pts)
    # general position
    for t in itertools.combinations(range(N), 3):
        if orient(*(pts[i] for i in t)) == 0:
            return f"collinear triple {t}"
    # 4-subsets in convex position: no point inside the triangle of the others
    def in_tri(p, a, b, c):
        s1, s2, s3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
        return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)
    conv4 = {}
    for q in itertools.combinations(range(N), 4):
        P = [pts[i] for i in q]
        conv4[q] = not any(in_tri(P[i], *[P[j] for j in range(4) if j != i]) for i in range(4))
    # an n-set in general position is in convex position iff all its 4-subsets are
    for S in itertools.combinations(range(N), n):
        if all(conv4[q] for q in itertools.combinations(S, 4)):
            return f"convex {n}-gon {S}"
    return None


if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        pts = es_set(n)
        assert len(pts) == 2 ** (n - 2) == sum(comb(n - 2, i) for i in range(n - 1))
        bad = check(pts, n)
        print(f"n={n}: {len(pts)} points, max |coord| = {max(max(abs(c) for c in p) for p in pts)}, "
              f"{'FAIL: ' + bad if bad else f'no {n} points in convex position'}")
        if n == 6 and not bad:
            print("points:", pts)
