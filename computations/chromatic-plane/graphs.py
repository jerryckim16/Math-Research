"""Unit-distance graphs with exact coordinates in Q(sqrt3, sqrt5, sqrt11).

Constructions:
  * moser_spindle(): the 7-vertex Moser spindle (chi = 4).
  * heule_v31(), heule_v151(), heule_v1939(), heule_g(): the explicit
    construction of M. J. H. Heule, "Computing small unit-distance graphs
    with chromatic number 5", arXiv:1805.12181, Section 4.1 ("Finding a small
    symmetric subgraph"), read from the arXiv LaTeX source:
      - theta_i is the rotation by arccos((2i-1)/(2i));
      - V31 = {0} u { theta_1^j theta_3^k (1,0) : j = 0..5, k in {-1,-1/2,0,1/2,1} }
        (de Grey's five 7-wheels with a common centre);
      - V151 = points of V31 (+) V31 at distance <= 1 from the origin;
      - V1939 = V31 (+) V151;
      - G = V1939 u theta_4(V1939), reported there to have chromatic number 5.
    Heule reports |V31| = 31 (60 edges), |V151| = 151 (510 edges), |V1939| = 1939.

Edges are found by a float grid search (candidate filter only) and then every
edge is confirmed EXACTLY (|p - q|^2 == 1 in the field). Missing an edge can
only weaken a non-colourability claim, never make it unsound, so the float
filter does not affect rigour. Vertices are deduplicated by exact coordinates.
"""
from fractions import Fraction as F
from math import floor

import qfield as Q

ONE = Q.const(1)
ZERO = Q.ZERO

# exact rotations (cos, sin)
THETA1 = (Q.const(F(1, 2)), Q.root(3, F(1, 2)))          # 60 degrees
THETA3 = (Q.const(F(5, 6)), Q.root(11, F(1, 6)))          # arccos(5/6)
THETA3_HALF = (Q.root(33, F(1, 6)), Q.root(3, F(1, 6)))   # half of theta3
THETA4 = (Q.const(F(7, 8)), Q.root(15, F(1, 8)))          # arccos(7/8)
IDENTITY = (ONE, ZERO)


def rot_power(r, k):
    out = IDENTITY
    base = r if k >= 0 else Q.inverse(r)
    for _ in range(abs(k)):
        out = Q.compose(out, base)
    return out


def key(p):
    return (p[0], p[1])


def dedupe(points):
    seen = {}
    for p in points:
        seen.setdefault(key(p), p)
    return list(seen.values())


def minkowski(A, B, keep=None):
    out = {}
    for a in A:
        for b in B:
            s = Q.padd(a, b)
            if keep is None or keep(s):
                out.setdefault(key(s), s)
    return list(out.values())


def unit_edges(points, tol=1e-7):
    """All pairs at exact distance 1 (float filter, exact confirmation).

    Returns (edges, n_candidates, n_rejected): n_rejected counts float
    candidates that failed the exact test (expected 0 for these fields;
    reported so a reader can see the filter is not doing hidden work).
    """
    xy = [Q.papprox(p) for p in points]
    grid = {}
    for i, (x, y) in enumerate(xy):
        grid.setdefault((floor(x), floor(y)), []).append(i)
    edges, cand, rejected = [], 0, 0
    for i, (x, y) in enumerate(xy):
        cx, cy = floor(x), floor(y)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((cx + dx, cy + dy), ()):
                    if j <= i:
                        continue
                    d2 = (xy[j][0] - x) ** 2 + (xy[j][1] - y) ** 2
                    if abs(d2 - 1) < tol:
                        cand += 1
                        if Q.is_unit_distance(points[i], points[j]):
                            edges.append((i, j))
                        else:
                            rejected += 1
    return edges, cand, rejected


def verify_edges_exact(points, edges):
    """Independent exact re-check of a claimed edge list."""
    return all(Q.is_unit_distance(points[i], points[j]) for i, j in edges)


# ---------------- constructions ----------------

def unit(x=1):
    return (Q.const(x), ZERO)


def moser_spindle():
    """Moser spindle: two rhombi of unit equilateral triangles, one rotated
    by theta3 (cos = 5/6) about the shared vertex 0, so the far tips are at
    distance 1. Built as (A (+) B) u theta3(A (+) B) as in Heule Sec. 2.1."""
    A = [unit(0), unit(1)]
    B = [unit(0), (Q.const(F(1, 2)), Q.root(3, F(1, 2)))]
    AB = minkowski(A, B)
    pts = dedupe(AB + [Q.rotate(p, THETA3) for p in AB])
    return pts


def heule_v31():
    pts = [unit(0)]
    for j in range(6):
        r1 = rot_power(THETA1, j)
        for k2 in (-2, -1, 0, 1, 2):  # k = k2/2
            r3 = rot_power(THETA3_HALF, k2)
            pts.append(Q.rotate(Q.rotate(unit(1), r3), r1))
    return dedupe(pts)


def _within_unit(p):
    v = Q.approx(Q.norm2(p))
    if abs(v - 1) < 1e-9:
        return Q.norm2(p) == ONE or v < 1  # exact on the boundary
    return v < 1


def heule_v151(v31=None):
    v31 = v31 or heule_v31()
    return minkowski(v31, v31, keep=_within_unit)


def heule_v1939(v31=None, v151=None):
    v31 = v31 or heule_v31()
    v151 = v151 or heule_v151(v31)
    return minkowski(v31, v151)


def heule_g(v1939=None):
    v1939 = v1939 or heule_v1939()
    return dedupe(v1939 + [Q.rotate(p, THETA4) for p in v1939])


def find_triangle(points, edges, anchor=0):
    """A unit triangle (clique of size 3) containing `anchor` if possible."""
    adj = {}
    for i, j in edges:
        adj.setdefault(i, set()).add(j)
        adj.setdefault(j, set()).add(i)
    order = [anchor] + [v for v in adj if v != anchor]
    for a in order:
        for b in sorted(adj.get(a, ())):
            common = adj[a] & adj[b]
            if common:
                return (a, b, min(common))
    return None
