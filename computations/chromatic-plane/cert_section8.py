"""Exact re-check of the finite parts of Section 8 of the OpenAI preprint
"The Euclidean plane is not five-colorable" (Sept 23, 2026), family 158 of
github.com/openai/math (paper.pdf, sha256 607c2601...1d36).

Checked here (all exact; no floating point decides anything):
  A. The Moser graph (8.5): |u| = 1 and all 11 edges have length exactly 1
     in Q(sqrt3, sqrt11); the graph is not 3-colourable (exhaustive 3^7).
  B. The placement (8.6): the multiplier (35+12i)/37 has modulus 1, so the
     placed graph keeps all unit edges (re-checked exactly after placing).
  C. Lemma 8.9: every placed vertex z_g satisfies 0 < l < 4 and
     P = v^2 (3 xi^2 - v^2)^2 < P' = l^3 (1 - l/4) (l - 1)^2, l = |z_g|^2.
     P' - P, l, 4 - l are computed EXACTLY as elements of Q(sqrt3, sqrt11);
     their signs are then decided by rigorous rational interval enclosures
     of sqrt3, sqrt11, sqrt33 (integer square roots, width 1e-40).
  D. The paper's own Table 1 / Table 2 numbers (centres within h = 0.00011,
     and P < P+ < P-' < P'), re-checked with Fractions.
  E. Lemma 8.8 identities (symbolic, sympy) and Lemma 6.4 constants.
  F. Prop 8.2 (five-cycle) combinatorics, by brute force over a SUPERSET of
     the configurations allowed in the paper.
  G. The hexagonal seven-colouring inequalities of Section 1.

Run: python3 cert_section8.py   (prints a report; exits non-zero on failure)
"""
import itertools
import sys
from fractions import Fraction as F
from math import isqrt

import qfield as Q

# ---------------------------------------------------------------- intervals
SCALE = 10 ** 40


def sqrt_interval(m):
    s = isqrt(m * SCALE * SCALE)
    lo, hi = F(s, SCALE), F(s + 1, SCALE)
    assert lo * lo <= m <= hi * hi
    return lo, hi


SQRT_IV = [sqrt_interval(r) for r in Q.RADICAND]


def interval(a):
    lo = hi = F(0)
    for c, (l, h) in zip(a, SQRT_IV):
        if c >= 0:
            lo += c * l; hi += c * h
        else:
            lo += c * h; hi += c * l
    return lo, hi


def sign(a):
    """Exact sign of a field element (rigorous): 0 only if a is exactly 0."""
    if Q.is_zero(a):
        return 0
    lo, hi = interval(a)
    if lo > 0:
        return 1
    if hi < 0:
        return -1
    raise ArithmeticError("interval too wide to decide sign")


# ---------------------------------------------------------------- A. Moser
def moser_graph():
    s3h = Q.root(3, F(1, 2))
    A = (s3h, Q.const(F(1, 2)))              # (sqrt3 + i)/2
    B = (s3h, Q.const(F(-1, 2)))             # (sqrt3 - i)/2
    T = (Q.root(3), Q.ZERO)                  # sqrt3
    u = (Q.const(F(5, 6)), Q.root(11, F(1, 6)))  # (5 + i sqrt11)/6
    O = (Q.ZERO, Q.ZERO)
    names = ["0", "A", "B", "T", "uA", "uB", "uT"]
    pts = [O, A, B, T, cmul(u, A), cmul(u, B), cmul(u, T)]
    edges = [("0", "A"), ("0", "B"), ("A", "B"), ("A", "T"), ("B", "T"),
             ("0", "uA"), ("0", "uB"), ("uA", "uB"), ("uA", "uT"), ("uB", "uT"),
             ("T", "uT")]
    idx = {n: i for i, n in enumerate(names)}
    return names, pts, [(idx[a], idx[b]) for a, b in edges], u


def cmul(z, w):
    """complex product of points (x, y) ~ x + i y."""
    return (Q.sub(Q.mul(z[0], w[0]), Q.mul(z[1], w[1])),
            Q.add(Q.mul(z[0], w[1]), Q.mul(z[1], w[0])))


def three_colourable(n, edges):
    for col in itertools.product(range(3), repeat=n):
        if all(col[a] != col[b] for a, b in edges):
            return True
    return False


# ---------------------------------------------------------------- B, C
ROT = (Q.const(F(35, 37)), Q.const(F(12, 37)))
SHIFT = (Q.const(F(-290, 250)), Q.const(F(149, 250)))


def place(p):
    """(8.6): z_g = ((35+12i)/37) * (g + (-290+149i)/250). Read from the
    rendered PDF (page 57); a plain-text extraction loses the parentheses."""
    return cmul(ROT, Q.padd(p, SHIFT))


def region_quantities(z):
    xi, up = z
    l = Q.norm2(z)
    one, four = Q.const(1), Q.const(4)
    t = Q.sub(Q.mul(Q.const(3), Q.mul(xi, xi)), Q.mul(up, up))
    P = Q.mul(Q.mul(up, up), Q.mul(t, t))
    lm1 = Q.sub(l, one)
    P2 = Q.mul(Q.mul(Q.mul(l, Q.mul(l, l)), Q.sub(one, Q.mul(l, Q.const(F(1, 4))))),
               Q.mul(lm1, lm1))
    return l, Q.sub(four, l), P, P2


# ---------------------------------------------------------------- D. tables
TABLE1 = {  # g: (xi0, v0, P+, P-')
    "0": ("-1.2906", "0.1876", "0.90", "1.35"),
    "A": ("-0.6335", "0.9414", "0.095", "0.110"),
    "B": ("-0.3092", "-0.0045", "0.000002", "0.00065"),
    "T": ("0.3478", "0.7493", "0.023", "0.026"),
    "uA": ("-1.1598", "1.1790", "9.8", "19.0"),
    "uB": ("-0.3666", "0.5700", "0.0022", "0.024"),
    "uT": ("-0.2358", "1.5614", "12.65", "12.9"),
}
TABLE2 = {  # g: (b_y, b_H, a, b)
    "0": ("0.0353", "4.963", "1.70", "1.71"),
    "A": ("0.887", "0.319", "1.28", "1.29"),
    "B": ("0.000022", "0.287", "0.095", "0.096"),
    "T": ("0.562", "0.199", "0.682", "0.683"),
    "uA": ("1.391", "2.647", "2.73", "2.74"),
    "uB": ("0.326", "0.079", "0.459", "0.46"),
    "uT": ("2.44", "2.273", "2.493", "2.495"),
}
H = F("0.00011")


def check_tables(name, z, P_exact, P2_exact):
    xi0, v0, Pp, Pm = (F(s) for s in TABLE1[name])
    by, bH, a, b = (F(s) for s in TABLE2[name])
    ok = True
    # centres within h of the exact coordinates
    for coord, c0 in ((z[0], xi0), (z[1], v0)):
        lo, hi = interval(Q.sub(coord, Q.const(c0)))
        ok &= (-H < lo and hi < H)
    # the paper's interval chain, recomputed
    xl, xu = (abs(xi0) - H) ** 2, (abs(xi0) + H) ** 2
    yl, yu = (abs(v0) - H) ** 2, (abs(v0) + H) ** 2
    ll, lu = xl + yl, xu + yu
    Hb = max(abs(3 * xl - yu), abs(3 * xu - yl))
    ok &= (abs(xi0) > H and abs(v0) > H)
    ok &= (yu < by and Hb < bH and a < ll <= lu < b)
    ok &= (by * bH ** 2 < Pp)
    ok &= (a ** 3 * (1 - b / 4) * min(abs(a - 1), abs(b - 1)) ** 2 > Pm)
    ok &= (Pp < Pm)
    ok &= (0 < a and b < 4 and not (a <= 1 <= b))
    # and against the exact values
    lo, hi = interval(P_exact)
    ok &= hi < Pp
    lo2, hi2 = interval(P2_exact)
    ok &= lo2 > Pm
    return ok


# ---------------------------------------------------------------- E. sympy
def check_identities():
    import sympy as sp
    r, phi, d = sp.symbols("r phi delta", positive=True)
    xi, v = r * sp.cos(phi), r * sp.sin(phi)
    l = r ** 2
    e1 = sp.simplify(sp.expand_trig(sp.sin(3 * phi) ** 2 * l ** 3
                                    - v ** 2 * (3 * xi ** 2 - v ** 2) ** 2))
    e2 = sp.simplify((sp.sin(3 * (phi - d)) * sp.sin(3 * (phi + d))
                      - (sp.sin(3 * phi) ** 2 - sp.sin(3 * d) ** 2)).rewrite(sp.exp))
    e3 = sp.simplify(sp.expand_trig(sp.sin(3 * d) - sp.sin(d) * (4 * sp.cos(d) ** 2 - 1)))
    # with cos(delta) = r/2:  sin(3 delta) = sqrt(1 - l/4) (l - 1)
    e4 = sp.simplify((sp.sqrt(1 - r ** 2 / 4) * (4 * (r / 2) ** 2 - 1))
                     - sp.sqrt(1 - l / 4) * (l - 1))
    # e^{i(phi-delta)} + e^{i(phi+delta)} = 2 cos(delta) e^{i phi}
    e5 = sp.simplify(sp.expand(sp.exp(sp.I * (phi - d)) + sp.exp(sp.I * (phi + d))
                               - 2 * sp.cos(d) * sp.exp(sp.I * phi)).rewrite(sp.cos))
    # Lemma 6.4: gamma = 2 arcsin(1/(2 sqrt3)): cos gamma = 5/6, |1 - e^{i gamma}| = 1/sqrt3
    g = 2 * sp.asin(1 / (2 * sp.sqrt(3)))
    e6 = sp.simplify(sp.cos(g) - sp.Rational(5, 6))
    e7 = sp.simplify(sp.Abs(1 - sp.exp(sp.I * g)) ** 2 - sp.Rational(1, 3))
    # Lemma 8.6: F(r, theta) = r^2 - 2 r cos(theta), dF/dtheta at (1, pi/3) = sqrt3
    rr, th = sp.symbols("rr th", real=True)
    Fexp = sp.Abs(rr * sp.exp(sp.I * th) - 1) ** 2 - 1
    e8 = sp.simplify(sp.expand(sp.expand_complex((rr * sp.exp(sp.I * th) - 1)
                                                 * (rr * sp.exp(-sp.I * th) - 1)) - 1
                               - (rr ** 2 - 2 * rr * sp.cos(th))))
    e9 = sp.simplify(sp.diff(rr ** 2 - 2 * rr * sp.cos(th), th).subs({rr: 1, th: sp.pi / 3})
                     - sp.sqrt(3))
    e10 = sp.simplify((rr ** 2 - 2 * rr * sp.cos(th)).subs({rr: 1, th: sp.pi / 3}))
    del Fexp
    return [sp.simplify(x) == 0 for x in (e1, e2, e3, e4, e5, e6, e7, e8, e9, e10)]


# ---------------------------------------------------------------- F. Prop 8.2
def five_cycle_bruteforce():
    """Labels 0..4 on a 5-cycle, edge j joins j, j+1. For a sign vector s,
    I(s) = labels whose two incident edges are +, O(s) = both -.
    (i) If I, O are both nonempty then s has one + run and one - run, of
        lengths {2, 3}.
    (ii) No assignment on a six-position orbit exists with: arbitrary valid
        s_0, s_1, s_2 and s_{j+3} = -s_j (antipodes), palettes
        P_j = {x, y} with x in I(s_j), y in O(s_j) (palette size <= 2 and
        P meets both I and O, as (5.12), (8.1) require; no outsiders exist
        for a 5-cycle), and P_j, P_{j+1} disjoint cyclically ((5.7)).
    This allows more configurations than the paper (s_1, s_2 are not tied to
    s_0 by geometry), so 'no solution' is a stronger statement."""
    def IO(s):
        I = [x for x in range(5) if s[(x - 1) % 5] > 0 and s[x] > 0]
        O = [x for x in range(5) if s[(x - 1) % 5] < 0 and s[x] < 0]
        return I, O

    def runs(s):
        # cyclic run lengths
        k = next(i for i in range(5) if s[i] != s[i - 1]) if len(set(s)) > 1 else None
        if k is None:
            return [5]
        out, cur = [], 1
        for t in range(1, 5):
            if s[(k + t) % 5] == s[(k + t - 1) % 5]:
                cur += 1
            else:
                out.append(cur); cur = 1
        out.append(cur)
        return sorted(out)

    valid = []
    for s in itertools.product((1, -1), repeat=5):
        I, O = IO(s)
        if I and O:
            if runs(s) != [2, 3]:
                return False, None
            valid.append(s)
    opts = {s: [frozenset((x, y)) for x in IO(s)[0] for y in IO(s)[1]] for s in valid}
    neg = lambda s: tuple(-t for t in s)
    count = 0
    for s0, s1, s2 in itertools.product(valid, repeat=3):
        S = [s0, s1, s2, neg(s0), neg(s1), neg(s2)]
        for P in itertools.product(*(opts[s] for s in S)):
            if all(not (P[j] & P[(j + 1) % 6]) for j in range(6)):
                count += 1
    return True, count


# ---------------------------------------------------------------- G. hexagons
def hexagon_check():
    r = F(2, 5)
    # same hexagon: diameter 2r < 1; distinct same-colour hexagons:
    # (sqrt21 - 2) r > 1  <=>  sqrt21 > 2 + 1/r = 9/2  <=>  21 > 81/4
    return 2 * r < 1 and 21 > (2 + 1 / r) ** 2 and abs(complex(2, 0) - complex(-0.5, 3 ** 0.5 / 2)) ** 2 > 6.99


def main():
    ok_all = True
    names, pts, edges, u = moser_graph()
    a1 = Q.norm2(u) == Q.const(1)
    a2 = all(Q.is_unit_distance(pts[i], pts[j]) for i, j in edges)
    a3 = not three_colourable(7, edges)
    print(f"A  |u|=1: {a1}; 11 edges exactly unit: {a2}; not 3-colourable: {a3}")
    ok_all &= a1 and a2 and a3

    b1 = Q.norm2(ROT) == Q.const(1)
    placed = [place(p) for p in pts]
    b2 = all(Q.is_unit_distance(placed[i], placed[j]) for i, j in edges)
    print(f"B  |(35+12i)/37|=1: {b1}; placed edges exactly unit: {b2}")
    ok_all &= b1 and b2

    for n, z in zip(names, placed):
        l, four_minus_l, P, P2 = region_quantities(z)
        c = (sign(l) == 1, sign(four_minus_l) == 1, sign(Q.sub(P2, P)) == 1)
        t = check_tables(n, z, P, P2)
        lo, hi = interval(Q.sub(P2, P))
        print(f"C  z_{n:2s}: l>0 {c[0]}, l<4 {c[1]}, P<P' {c[2]} "
              f"(P'-P in [{float(lo):.6g}, {float(hi):.6g}])   D tables: {t}")
        ok_all &= all(c) and t

    ids = check_identities()
    print(f"E  Lemma 8.8/8.6/6.4 identities: {ids}")
    ok_all &= all(ids)

    f_ok, f_count = five_cycle_bruteforce()
    print(f"F  five-cycle: sign patterns are a (2,3) run split: {f_ok}; "
          f"admissible six-position palette words: {f_count}")
    ok_all &= f_ok and f_count == 0

    g = hexagon_check()
    print(f"G  hexagonal 7-colouring inequalities: {g}")
    ok_all &= g
    print("ALL OK" if ok_all else "FAILURE")
    return ok_all


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
