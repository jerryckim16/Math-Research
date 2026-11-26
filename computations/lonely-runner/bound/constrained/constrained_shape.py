"""Constrained shape bounds for LRC(n) (n = 17: 18 runners), exact arithmetic.

A counterexample shape u = v / max v, sorted 1 = u_1 >= u_2 >= ... >= u_n > 0,
is NOT lonely: no real tau has ||tau u_i|| >= theta := 1/(n+1) for all i.
(Loneliness is scale invariant, so it is a property of u.)  Write
s = u_2, t = u_3, m = u_n, b = 2 theta, g = 1 - 2 theta.

Sweep lemmas (proofs in notes/lonely-runner/constrained-shape.md, section 2).
Each condition below implies that u is lonely, so a counterexample shape
violates all of them:
  C1  m >= 1/n.
  L1  s <= 1/n                                  (uses LRC(n-1)).
  C2  l2 := (1-theta)/s - theta/m >= b.         (sharp form of BHS (a))
  C3  l3 := (1-theta)/t - theta/m >= 0 and P(s l3)/s >= b,
      P(L) := min(g, max(0, (L - b)/2)).        (implies BNV Thm 1, BHS (b))
The region F of (s, t, m) violating C1, L1, C2, C3 (with 1 >= s >= t >= m > 0)
contains the (u_2, u_3, u_n) of every counterexample shape.

Functionals (from bound/flag_n.py and bound/relrank_n.py):
  R_n(u)^2 = n^2 / H(u),  H = (sum_i w(u_i)) prod_i a(u_i),
      w = u^2/q, a = q / u^(2/n), q = 1 + 2u - u^2      (flag shape factor);
  Phi_r(u) = 4 n^2 (prod u)^(2/n) / ((sum u^2) prod_{i >= r+2} q(u_i))
      (relation-rank Schur shape factor; C_r is an upper bound for it).

Lambda-separation.  For A > 0:  ln A = min_{lam > 0} (lam A - 1 - ln lam), and
-ln A = max_{lam > 0} (1 + ln lam - lam A), both attained at lam = 1/A.
  * Phi_r: A = sum u^2 in [1, n], so lam ranges over [1/n, 1] and
      ln Phi_r(u) = max_lam [ln(4n^2) + 1 + ln lam - lam
                     + sum_{i=2}^{r+1} h1(u_i) + sum_{i>=r+2} h2(u_i)],
      h1 = (2/n) ln x - lam x^2,  h2 = h1 - ln q(x).
  * R_n: A = sum w in (1/2, n/2], lam in [2/n, 2] and
      ln H(u) = min_lam [-1 - ln lam + sum_i gl(u_i)],
      gl = lam w(x) + ln q(x) - (2/n) ln x.
Every coordinate other than 1, s, t, m is bounded by its one-variable optimum
(relaxing the order constraints only enlarges the domain), which leaves a
4-dimensional box branch-and-bound over (lam, s, t, m).  All box bounds use
monotonicity of each term (w, q increasing on [0, 1]; ln increasing) with
rigorous rational enclosures of ln (mpmath interval arithmetic, rounded
outward to 2^-80); all comparisons are exact Fractions.
"""
from fractions import Fraction as Fr
from functools import lru_cache
import math

GRID = 2 ** 80


# ------------------------------------------------------------------ rigorous ln
@lru_cache(maxsize=None)
def _ln_enclosure(x):
    from mpmath import iv
    from mpmath.libmp import to_rational
    iv.prec = 110
    y = iv.log(iv.mpf(x.numerator) / x.denominator)
    lo = Fr(*to_rational(y._mpi_[0]))
    hi = Fr(*to_rational(y._mpi_[1]))
    L = Fr(math.floor(lo * GRID), GRID)
    H = Fr(-math.floor(-hi * GRID), GRID)
    assert L <= lo <= hi <= H
    return L, H


def lnL(x):
    return _ln_enclosure(Fr(x))[0]


def lnU(x):
    return _ln_enclosure(Fr(x))[1]


def q(x):
    return 1 + 2 * x - x * x


def w(x):
    return x * x / q(x)


# ------------------------------------------------------------------ sweep lemmas
class Consts:
    """theta defaults to 1/(n+1); a larger theta is used only by the
    negative-control tests (C1 then reads m >= theta/(1-theta))."""
    def __init__(self, n, theta=None):
        self.n = n
        self.th = Fr(1, n + 1) if theta is None else Fr(theta)
        self.b = 2 * self.th
        self.g = 1 - 2 * self.th

    def P(self, L):
        return min(self.g, max(Fr(0), (L - self.b) / 2))


def lonely_point(c, s, t, m, use=("C1", "L1", "C2", "C3")):
    """Exact test at one point: True if one of the conditions certifies that a
    sorted shape with u_2 = s, u_3 = t, u_n = m is lonely."""
    th, b = c.th, c.b
    if "C1" in use and m >= c.th / (1 - c.th):
        return True
    if "L1" in use and s <= (Fr(1, c.n) - c.th) / c.th:
        return True
    if m <= 0:
        return False
    if "C2" in use and (1 - th) / s - th / m >= b:
        return True
    if "C3" in use:
        l3 = (1 - th) / t - th / m
        if l3 >= 0 and c.P(s * l3) / s >= b:
            return True
    return False


def box_excluded(c, s0, s1, t0, t1, m0, m1, use=("C1", "L1", "C2", "C3")):
    """True if EVERY sorted shape with s in [s0,s1], t in [t0,t1], m in [m0,m1]
    (and s >= t >= m) is lonely by one fixed condition, or the box has no such
    point.  Each test uses the worst corner, by monotonicity:
      l2 decreases in s, increases in m;  l3 decreases in t, increases in m;
      P(s l3)/s = min(g/s, (l3 - b/s)/2) >= min(g/s1, (l3_min - b/s0)/2)."""
    th, b = c.th, c.b
    if t0 > s1 or m0 > t1:
        return True
    if "C1" in use and m0 >= c.th / (1 - c.th):
        return True
    if "L1" in use and s1 <= (Fr(1, c.n) - c.th) / c.th:
        return True
    if m0 <= 0 or s0 <= 0:
        return False
    if "C2" in use and (1 - th) / s1 - th / m0 >= b:
        return True
    if "C3" in use:
        l3 = (1 - th) / t1 - th / m0
        if l3 >= 0 and min(c.g / s1, (l3 - b / s0) / 2) >= b:
            return True
    return False


# ------------------------------------------------------------------ 1-D optima
def x_concave(n):
    """A rational x_c with x_c^2 < 1/(3n).  On (0, x_c]:
      h2'' = -2/(n x^2) - 2 lam + (2q + q'^2)/q^2 <= -2/(n x^2) + 6 < 0, since
      q >= 1 and |q'| <= 2 on [0,1]; and, for gl = lam w + ln q - (2/n) ln x,
      gl'' = lam w'' - (2q + q'^2)/q^2 + 2/(n x^2) >= -6 + 2/(n x^2) > 0,
      since w'' = 2 (1 + 3x^2 + 2x^3)/q^3 > 0 (exact identity, see
      check_w_second_derivative).  So h2 is concave and gl convex there."""
    xc = Fr(math.isqrt(10 ** 12 // (3 * n)), 10 ** 6)
    while xc * xc * 3 * n >= 1:
        xc -= Fr(1, 10 ** 6)
    return xc


def check_w_second_derivative():
    """w = x^2/q, q' = 2 - 2x:  w' = (2x q - x^2 q')/q^2 = 2x(1+x)/q^2 and
    w'' q^3 = (2 + 4x) q - 4x(1+x) q' = 2 (1 + 3x^2 + 2x^3).  Both are
    polynomial identities of degree <= 3; checked exactly at 8 points."""
    pts = [Fr(k, 7) for k in range(8)]
    a = all(2 * x * q(x) - x * x * (2 - 2 * x) == 2 * x * (1 + x) for x in pts)
    b = all((2 + 4 * x) * q(x) - 4 * x * (1 + x) * (2 - 2 * x) == 2 * (1 + 3 * x * x + 2 * x ** 3) for x in pts)
    return a and b


def _rigorous_cells(cell_bound, lo, hi, threshold, maximize, min_width):
    """Max (or min) of cell bounds over a refinement of [lo, hi]: a cell is
    split while its bound is on the wrong side of threshold and it is wider
    than min_width.  Returns the rigorous bound for f on [lo, hi]."""
    sign = 1 if maximize else -1
    out, cells = None, [(lo, hi)]
    while cells:
        x0, x1 = cells.pop()
        B = sign * cell_bound(x0, x1)
        if B > sign * threshold and x1 - x0 > min_width:
            mid = (x0 + x1) / 2
            cells += [(x0, mid), (mid, x1)]
            continue
        out = B if out is None else max(out, B)
    return sign * out


def _stationary(fprime, lo, hi):
    """Float bisection for a root of a decreasing fprime on (lo, hi)."""
    a, b = float(lo), float(hi)
    for _ in range(200):
        mid = (a + b) / 2
        if fprime(mid) > 0:
            a = mid
        else:
            b = mid
    return Fr((a + b) / 2).limit_denominator(10 ** 12)


@lru_cache(maxsize=None)
def M2(n, lam0):
    """Upper bound of sup_{0<x<=1} h2(x), h2 = (2/n) ln x - lam x^2 - ln q(x),
    valid for all lam >= lam0 (h2 decreases in lam).  Concave part: tangent
    at a near-stationary rational x0; rest: monotone cell bounds."""
    xc = x_concave(n)
    lam = lam0
    fp = lambda x: 2 / (n * x) - 2 * float(lam) * x - (2 - 2 * x) / (1 + 2 * x - x * x)
    x0 = _stationary(fp, Fr(1, 10 ** 9), xc)
    x0 = min(max(x0, Fr(1, 10 ** 9)), xc)
    f0 = Fr(2, n) * lnU(x0) - lam * x0 * x0 - lnL(q(x0))
    d0 = Fr(2, n) / x0 - 2 * lam * x0 - (2 - 2 * x0) / q(x0)          # exact
    conc = f0 + max(d0 * (xc - x0), -d0 * x0, Fr(0))
    def cb(a, b):
        return Fr(2, n) * lnU(b) - lam * a * a - lnL(q(a))
    rest = _rigorous_cells(cb, xc, Fr(1), conc, True, Fr(1, 2 ** 16))
    return max(conc, rest)


def M1(n, lam0, t1):
    """Upper bound of max_{0<x<=t1} (2/n) ln x - lam x^2 for lam >= lam0
    (concave in x; maximiser x* = (n lam0)^(-1/2))."""
    if t1 * t1 * n * lam0 <= 1:          # t1 <= x*
        return Fr(2, n) * lnU(t1) - lam0 * t1 * t1
    return -Fr(1, n) * lnL(n * lam0) - Fr(1, n)


@lru_cache(maxsize=None)
def Mg(n, lam0):
    """Lower bound of inf_{0<x<=1} gl(x), gl = lam w(x) + ln q(x) - (2/n) ln x,
    valid for all lam >= lam0 (gl increases in lam).  Convex part: tangent at
    a near-stationary rational x0; rest: monotone cell bounds."""
    xc = x_concave(n)
    lam = lam0
    fp = lambda x: -(float(lam) * 2 * x * (1 + x) / (1 + 2 * x - x * x) ** 2 + (2 - 2 * x) / (1 + 2 * x - x * x) - 2 / (n * x))
    x0 = _stationary(fp, Fr(1, 10 ** 9), xc)
    x0 = min(max(x0, Fr(1, 10 ** 9)), xc)
    f0 = lam * w(x0) + lnL(q(x0)) - Fr(2, n) * lnU(x0)
    d0 = lam * 2 * x0 * (1 + x0) / q(x0) ** 2 + (2 - 2 * x0) / q(x0) - Fr(2, n) / x0   # exact gl'(x0)
    conv = f0 + min(d0 * (xc - x0), -d0 * x0, Fr(0))
    def cb(a, b):
        return lam * w(a) + lnL(q(a)) - Fr(2, n) * lnU(b)
    rest = _rigorous_cells(cb, xc, Fr(1), conv, False, Fr(1, 2 ** 16))
    return min(conv, rest)


# ------------------------------------------------------------------ box bounds
def phi_box_ub(c, r, lam0, lam1, s0, s1, t0, t1, m0, m1):
    """Upper bound of ln Phi_r over the box (r >= 2, r <= n - 2)."""
    n = c.n
    h1s = Fr(2, n) * lnU(s1) - lam0 * s0 * s0
    h1t = Fr(2, n) * lnU(t1) - lam0 * t0 * t0
    h2m = Fr(2, n) * lnU(m1) - lam0 * m0 * m0 - (lnL(q(m0)) if m0 > 0 else 0)
    return (lnU(4 * n * n) + 1 + lnU(lam1) - lam0 + h1s + h1t
            + (r - 2) * M1(n, lam0, t1) + (n - r - 2) * M2(n, lam0) + h2m)


def lnH_box_lb(c, lam0, lam1, s0, s1, t0, t1, m0, m1):
    """Lower bound of ln H over the box."""
    n = c.n
    def gb(x0, x1):
        return lam0 * w(x0) + (lnL(q(x0)) if x0 > 0 else 0) - Fr(2, n) * lnU(x1)
    g1 = lam0 / 2 + lnL(2)
    return -1 - lnU(lam1) + g1 + gb(s0, s1) + gb(t0, t1) + gb(m0, m1) + (n - 4) * Mg(n, lam0)


# ------------------------------------------------------------------ branch and bound
def branch_and_bound(n, kind, target, r=None, use=("C1", "L1", "C2", "C3"), max_depth=60, max_boxes=5 * 10 ** 6):
    """kind = 'phi': prove ln Phi_r < ln(target) on F, i.e. C_r^F <= target.
    kind = 'R':   prove R_n < target on F, i.e. H > (n/target)^2.
    Returns a dict; 'proved' is True only if every box was closed."""
    c = Consts(n)
    if kind == "phi":
        lamI = (Fr(1, n), Fr(1))
        goal = lnL(target)                    # need ub < goal
    else:
        lamI = (Fr(2, n), Fr(2))
        goal = 2 * lnU(Fr(n) / target)        # need lb > goal  (H > (n/target)^2)
    root = (lamI[0], lamI[1], Fr(1, n), Fr(1), Fr(0), Fr(1), Fr(0), Fr(1, n))
    scale = (lamI[1] - lamI[0], Fr(1), Fr(1), Fr(1, n))
    stack = [(root, 0)]
    stats = {"boxes": 0, "excluded_lonely": 0, "closed_by_bound": 0, "max_depth": 0}
    worst = None
    while stack:
        box, d = stack.pop()
        stats["boxes"] += 1
        stats["max_depth"] = max(stats["max_depth"], d)
        if stats["boxes"] > max_boxes:
            return {"proved": False, "reason": "box limit", "stats": stats, "box": box}
        l0, l1, s0, s1, t0, t1, m0, m1 = box
        if box_excluded(c, s0, s1, t0, t1, m0, m1, use):
            stats["excluded_lonely"] += 1
            continue
        if kind == "phi":
            v = phi_box_ub(c, r, l0, l1, s0, s1, t0, t1, m0, m1)
            ok = v < goal
            margin = goal - v
        else:
            v = lnH_box_lb(c, l0, l1, s0, s1, t0, t1, m0, m1)
            ok = v > goal
            margin = v - goal
        if ok:
            stats["closed_by_bound"] += 1
            worst = margin if worst is None else min(worst, margin)
            continue
        if d >= max_depth:
            return {"proved": False, "reason": "depth limit", "stats": stats, "box": box}
        widths = [(l1 - l0) / scale[0], (s1 - s0) / scale[1], (t1 - t0) / scale[2], (m1 - m0) / scale[3]]
        k = max(range(4), key=lambda i: widths[i])
        lo, hi = box[2 * k], box[2 * k + 1]
        mid = (lo + hi) / 2
        a = list(box); a[2 * k + 1] = mid
        bb = list(box); bb[2 * k] = mid
        stack.append((tuple(a), d + 1))
        stack.append((tuple(bb), d + 1))
    return {"proved": True, "stats": stats, "min_margin": worst}
