"""Machine checks of the ANALYTIC glue in Costa-Sadhu, arXiv:2610.02295 v1, Theorem 1.2
(c_UC >= 1 - m0 = 0.3828852549667978).  Companion of costa_sadhu_thm12.py, which
re-certifies the FINITE computations (Certificates A.4-A.7).

What "machine-checked" means here (the labels used in run_all()'s table):

  sympy-exact   an identity is reduced to 0 by exact rational-function arithmetic
                (sympy.cancel), with log(u), log(1-u), ... replaced by independent
                symbols, or a derivative is computed by sympy from an explicit formula.
                An identity that holds with the logs as free symbols holds a fortiori.
  sturm         exact Sturm-sequence root count of a rational polynomial on an interval.
  z3            an implication between real-arithmetic facts (the "skeleton" of a case
                analysis) is checked unsatisfiable-when-negated by the z3 SMT solver
                (nonlinear real arithmetic, exact rationals).  The facts fed in as
                hypotheses are themselves proved by the other checks, as listed.
  interval      outward-rounded interval arithmetic (interval.py, own log/exp).
  arb           FLINT/Arb ball arithmetic at 200 bits (python-flint): an independent
                second evaluation of the transcendental scalars.
  hand          the step is a standard analysis fact (Taylor bound with positive
                terms, "f(0) = 0 and f' > 0 => f > 0", FTC / Tonelli, Jensen, weak
                limits, continuity at the boundary) that we state explicitly but do not
                formalise.  Every claim says which of its steps are hand steps.

Requirements: pip install sympy z3-solver python-flint (python-flint optional: Arb
cross-check of two scalars).  Run: python3 analytic_glue.py [claim-id prefix].

No Lean: the Lean toolchain and the Mathlib cache hosts are blocked from this
container (see problems/frankl-union-closed.md, Approach 6).

Notation (as in the paper, Section 6): H(p) = -p log p - (1-p) log(1-p) (natural log),
tau = l0^2 = 1985281/4000000, r(x,y) = xy(1 + tau(1-x)(1-y)), g(x) = r(x,x),
G(u) = e^u H(e^-u), W0(u) = e^{2u} H(g(e^-u)), x = e^-s, y = e^-sigma, 0 < s <= sigma,
F0 = alpha0 G(s+sigma) - (G(s)+G(sigma))/(2 m0) + beta0 sqrt(W0(s) W0(sigma)),
D = G(s) + G(sigma) - G(s+sigma), u = s + sigma, lam = s/u.
Throughout, S(x) := -log(1-x)/x, so that (with x = e^-u) G = u + (1-x) S(x).
"""
from __future__ import annotations

import math
import sys
import time
from fractions import Fraction as Fr
from math import comb, isqrt

import sympy as sp

from interval import I, IF, ilog, LN2, _L2LO, _L2HI
from costa_sadhu_thm12 import (L0, TAU, M0, ALPHA0, BETA0, BERN_MIN, S_I, Hr)

try:
    import z3
except ImportError:          # pragma: no cover
    z3 = None
try:
    import flint
except ImportError:          # pragma: no cover
    flint = None

RESULTS = []   # (id, statement, method, status)


def claim(cid, statement, method):
    def deco(f):
        def run():
            f()
            RESULTS.append((cid, statement, method, "OK"))
        run.cid, run.statement, run.method = cid, statement, method
        return run
    return deco


# ============================================================ sympy helpers
u, v, w, z, x, y, a, b, q, lam, t = sp.symbols("u v w z x y a b q lam t", positive=True)
La, Lb, Lc, Ld, Le = sp.symbols("La Lb Lc Ld Le")      # stand-ins for logarithms
TAU_S = sp.Rational(TAU.numerator, TAU.denominator)
M0_S = sp.Rational(M0.numerator, M0.denominator)
A0_S = sp.Rational(ALPHA0.numerator, ALPHA0.denominator)
B0_S = sp.Rational(BETA0.numerator, BETA0.denominator)


def Hs(p):
    """Binary entropy as an explicit sympy expression."""
    return -p * sp.log(p) - (1 - p) * sp.log(1 - p)


def zero_with_logs(expr, logmap):
    """Exact check that expr == 0 after replacing each log(...) atom by an independent symbol.

    logmap: {log-argument: symbol}.  Every log atom of expr must be listed (asserted), so
    nothing transcendental is left to sympy's heuristics; the remainder is a rational
    function over Q in the variables and the log symbols, which sympy.cancel decides."""
    expr = sp.sympify(expr)
    for _ in range(3):   # normalise log arguments to factored form, then split products/quotients
        expr = expr.replace(lambda e: isinstance(e, sp.log),
                            lambda e: sp.log(sp.factor(sp.together(e.args[0]))))
        expr = sp.expand_log(expr, force=True)
    logs = expr.atoms(sp.log)
    rep = {}
    for L in logs:
        arg = sp.factor(L.args[0])
        hit = [s for k, s in logmap.items() if sp.simplify(sp.factor(k) - arg) == 0]
        assert len(hit) == 1, f"unexpected log atom {L}"
        rep[L] = hit[0]
    e = sp.cancel(sp.together(expr.xreplace(rep)))
    return e == 0


def poly_zero(expr):
    return sp.expand(expr) == 0


def sturm_roots(p, lo, hi=None):
    """Number of distinct real roots of p in (lo, hi] (hi=None: (lo, oo)), by an explicit
    Sturm sequence over Q (sign variations at the ends)."""
    P = sp.Poly(p, lam)
    seq = sp.sturm(P)

    def var(vals):
        vals = [s for s in vals if s != 0]
        return sum(1 for i in range(len(vals) - 1) if (vals[i] > 0) != (vals[i + 1] > 0))
    at_lo = [s.eval(lo) for s in seq]
    if hi is None:
        at_hi = [s.LC() for s in seq]     # sign at +oo
    else:
        at_hi = [s.eval(hi) for s in seq]
    n = var(at_lo) - var(at_hi)
    # cross-check with sympy's own exact root counter
    if hi is not None:
        assert n == P.count_roots(lo, hi) - (1 if P.eval(lo) == 0 else 0)
    return n


def z3_valid(hyps, goal, vars_):
    """Check (and hyps) => goal over the reals with z3; True iff the negation is unsat."""
    s = z3.Solver()
    s.set("timeout", 60000)
    s.add(*hyps)
    s.add(z3.Not(goal))
    r = s.check()
    assert r == z3.unsat, f"z3: {r} {s.model() if r == z3.sat else ''}"
    return True


def Q(fr):
    fr = Fr(fr)
    return z3.RealVal(f"{fr.numerator}/{fr.denominator}")


# ============================================================ G: the closed-form route
@claim("G.1", "G(u)=u+(1-x)S(x), G'(u)=S(x), G''(u)=S(x)-1/(1-x)  (x=e^-u, S=-log(1-x)/x)",
       "sympy-exact")
def check_G_derivs():
    # G as a function of x = e^-u is H(x)/x;  d/du = -x d/dx.
    Gx = Hs(x) / x
    S = -sp.log(1 - x) / x
    m = {x: La, 1 - x: Lb}
    # u = -log x
    assert zero_with_logs(Gx - (-sp.log(x) + (1 - x) * S), m)
    G1 = -x * sp.diff(Gx, x)
    assert zero_with_logs(G1 - S, m)
    G2 = -x * sp.diff(G1, x)
    assert zero_with_logs(G2 - (S - 1 / (1 - x)), m)
    # series form of the paper (Lemma 5.2) agrees: sum x^k/(k(k+1)) = 1 + (1-x)log(1-x)/x
    k = sp.symbols("k", integer=True, positive=True)
    ser = sp.summation(x**k / (k * (k + 1)), (k, 1, sp.oo))
    ser = sp.piecewise_fold(ser)
    if isinstance(ser, sp.Piecewise):
        ser = ser.args[0][0]
    assert zero_with_logs(ser - (1 + (1 - x) * sp.log(1 - x) / x), m)


@claim("G.2", "on 0<x<1: S(x)>1 (so G'>1) and psi(x):=x+(1-x)log(1-x)>0 (so G''<0 and G(u)-u<1)",
       "sympy-exact + hand(MVT)")
def check_G_signs():
    m = {x: La, 1 - x: Lb}
    # f = -log(1-x) - x: f(0)=0, f' = x/(1-x) > 0  =>  S > 1
    f = -sp.log(1 - x) - x
    assert f.subs(x, 0) == 0 and zero_with_logs(sp.diff(f, x) - x / (1 - x), m)
    # psi(0)=0, psi' = -log(1-x) > 0
    psi = x + (1 - x) * sp.log(1 - x)
    assert psi.subs(x, 0) == 0 and zero_with_logs(sp.diff(psi, x) + sp.log(1 - x), m)
    S = -sp.log(1 - x) / x
    # G'' = S - 1/(1-x) = -psi/(x(1-x))
    assert zero_with_logs(S - 1 / (1 - x) + psi / (x * (1 - x)), m)
    # G - u = (1-x)S = 1 - psi/x   (< 1)
    assert zero_with_logs((1 - x) * S - (1 - psi / x), m)
    # -G'' - x/(1-x) = 1 - S < 0, i.e. -G''(v) < 1/(e^v-1) < 1/v  (paper: series; here closed form)
    assert zero_with_logs(-(S - 1 / (1 - x)) - x / (1 - x) - (1 - S), m)
    assert sp.limit(Hs(x) / x, x, 1, "-") == 0          # G(0+) = 0


# ============================================================ Lemma 4.1
@claim("4.1.a", "-Lam''/Lam' - 1/u - 1/(1-u) = N/(u(1-u) lam H),  N = q(1-lam)+u lam(1-u lam), "
       "lam = log((1-u)/u), q = -log(1-u), H = u lam + q, H' = lam", "sympy-exact")
def check_41_identity():
    m = {u: La, 1 - u: Lb}
    H = Hs(u)
    lam_ = sp.log(1 - u) - sp.log(u)
    q_ = -sp.log(1 - u)
    assert zero_with_logs(H - (u * lam_ + q_), m)
    assert zero_with_logs(sp.diff(H, u) - lam_, m)
    Lam1 = sp.diff(sp.log(H), u)
    Lam2 = sp.diff(Lam1, u)
    N = q_ * (1 - lam_) + u * lam_ * (1 - u * lam_)
    assert zero_with_logs(-Lam2 / Lam1 - 1 / u - 1 / (1 - u) - N / (u * (1 - u) * lam_ * H), m)


@claim("4.1.b", "N > 0 for 0<u<1/2 (both cases lam<=1 and lam>1)",
       "sympy-exact + sturm + z3 + hand(Taylor e^lam > 1+lam+lam^2/2+lam^3/6, MVT)")
def check_41_positivity():
    m = {u: La, 1 - u: Lb}
    # (i) q <= u/(1-u): f = u/(1-u) + log(1-u), f(0) = 0, f' = u/(1-u)^2 >= 0
    f = u / (1 - u) + sp.log(1 - u)
    assert f.subs(u, 0) == 0 and zero_with_logs(sp.diff(f, u) - u / (1 - u) ** 2, m)
    # (ii) algebra of (4.lambda-lower)
    L = sp.symbols("L")
    assert poly_zero(sp.together((u / (1 - u)) * (1 - L) + u * L * (1 - u * L)
                                 - (u / (1 - u)) * (1 - u * L * (L + 1) + u**2 * L**2)) * (1 - u))
    # (iii) u = 1/(1+e^lam) solves lam = log((1-u)/u)
    uu = 1 / (1 + sp.exp(lam))
    assert sp.simplify(sp.log((1 - uu) / uu) - lam) == 0
    # (iv) 1 - lam^2/2 + lam^3/6 > 0 on [1, oo): no root there (Sturm) and value 2/3 at 1;
    #      its minimum on [1,oo) is 1/3 at lam = 2
    p = 1 - lam**2 / 2 + lam**3 / 6
    assert p.subs(lam, 1) > 0 and sturm_roots(6 * p, 1) == 0
    assert p.subs(lam, 2) == sp.Rational(1, 3) and poly_zero(sp.diff(p, lam) - lam * (lam / 2 - 1))
    # (v) z3 skeleton.  Hypotheses (each proved above / elementary):
    #     0<u<1/2, lam>0, q>0, q <= u/(1-u), and for lam>1: u*lam*(lam+1) < 1
    #     (from u < e^-lam and e^lam > lam(lam+1), (iii)-(iv) + Taylor).
    U, Lm, Qv = z3.Reals("u lam q")
    N = Qv * (1 - Lm) + U * Lm * (1 - U * Lm)
    base = [U > 0, U < Q(Fr(1, 2)), Lm > 0, Qv > 0, Qv * (1 - U) <= U]
    z3_valid(base + [Lm <= 1], N > 0, None)
    z3_valid(base + [Lm > 1, U * Lm * (Lm + 1) < 1], N > 0, None)


def lemma41_interval_crosscheck(lo_exp=40, n_per_octave=16):
    """Independent cross-check (not needed for the proof): N(u)/u > 0 on [2^-lo_exp, 1/2],
    N/u = S - lam (S - 1 + u lam), S = -log(1-u)/u, by interval arithmetic on cells."""
    cells, mn = 0, float("inf")
    stack = []
    for e in range(1, lo_exp):
        A, B = 2.0 ** -(e + 1), 2.0 ** -e
        h = (B - A) / n_per_octave
        stack += [(A + i * h, A + (i + 1) * h) for i in range(n_per_octave)]
    while stack:
        lo, hi = stack.pop()
        U = I(lo, hi)
        S = S_I(U)
        Lm = ilog((1.0 - U) / U)
        if hi >= 0.5:
            Lm = I(0.0, Lm.hi)         # lam >= 0 on (0, 1/2]
        val = S - Lm * (S - 1.0 + U * Lm)
        if val.lo > 0:
            cells += 1
            mn = min(mn, val.lo)
            continue
        assert hi - lo > 1e-15, (lo, hi, val)
        mid = 0.5 * (lo + hi)
        stack += [(lo, mid), (mid, hi)]
    return cells, mn


@claim("4.1.x", "cross-check: N(u)/u > 0 on [2^-40, 1/2] by interval cells", "interval")
def check_41_interval():
    cells, mn = lemma41_interval_crosscheck()
    assert mn > 0


# ============================================================ Lemma 4.4
Hf = sp.Function("H")


@claim("4.4.a", "d/dv log H(e^-v) = -M(e^-v),  d2/dv2 log H(e^-v) = e^-v M'(e^-v)  (M = uH'/H, H abstract)",
       "sympy-exact")
def check_44_chain():
    Mz = z * sp.diff(Hf(z), z) / Hf(z)
    f1 = -z * sp.diff(sp.log(Hf(z)), z)          # d/dv, z = e^-v
    assert sp.simplify(f1 + Mz) == 0
    f2 = -z * sp.diff(f1, z)
    assert sp.simplify(f2 - z * sp.diff(Mz, z)) == 0


@claim("4.4.b", "log H(e^-v) = -v + log G(v) and (log G)'' = G''/G - (G'/G)^2 < 0, hence M' < 0 on (0,1)",
       "sympy-exact + G.2")
def check_44_concave():
    Gf = sp.Function("G")
    assert sp.simplify(sp.diff(sp.log(Gf(v)), v, 2)
                       - (sp.diff(Gf(v), v, 2) / Gf(v) - (sp.diff(Gf(v), v) / Gf(v)) ** 2)) == 0
    # log H(x) = log x + log(H(x)/x) = -v + log G(v) is the definition G(v) = e^v H(e^-v);
    # G > 0 (H > 0 on (0,1)) and G'' < 0 (claim G.2) give (log G)'' < 0.


def lemma44_interval_crosscheck(lo_exp=40, n_per_octave=16):
    """Independent cross-check: K(u) := (lam - 1/(1-u)) H - u lam^2 < 0 on [2^-lo_exp, 1-2^-lo_exp]
    (M' = K/H^2).  Checked as K/u < 0 for u <= 1/2 and K < 0 for u >= 1/2."""
    stack = []
    for e in range(1, lo_exp):
        A, B = 2.0 ** -(e + 1), 2.0 ** -e
        h = (B - A) / n_per_octave
        for i in range(n_per_octave):
            stack.append((A + i * h, A + (i + 1) * h))
            stack.append((1.0 - (A + (i + 1) * h), 1.0 - (A + i * h)))
    cells, worst = 0, -float("inf")
    while stack:
        lo, hi = stack.pop()
        U = I(lo, hi)
        H = Hr(U)
        Lm = ilog((1.0 - U) / U)
        K = (Lm - 1.0 / (1.0 - U)) * H - U * Lm.sq()
        if hi <= 0.5:
            K = K / U
        if K.hi < 0:
            cells += 1
            worst = max(worst, K.hi)
            continue
        assert hi - lo > 1e-15, (lo, hi, K)
        mid = 0.5 * (lo + hi)
        stack += [(lo, mid), (mid, hi)]
    return cells, worst


@claim("4.4.x", "cross-check: M'(u) < 0 on [2^-40, 1-2^-40] by interval cells", "interval")
def check_44_interval():
    cells, worst = lemma44_interval_crosscheck()
    assert worst < 0


# ============================================================ Lemma 6.1
def _r():
    return x * y * (1 + TAU_S * (1 - x) * (1 - y))


@claim("6.1.a", "r_x = y[1+tau(1-2x)(1-y)], r_y = x[1+tau(1-x)(1-2y)], r_xy = 1+tau(1-2x)(1-2y), "
       "W r_xy - r_x r_y/(xy) = tau xy, and r_xy/(r_x r_y) = 1/r + tau/(W U V)", "sympy-exact")
def check_61_identities():
    r = _r()
    W = 1 + TAU_S * (1 - x) * (1 - y)
    U_ = 1 + TAU_S * (1 - 2 * x) * (1 - y)
    V_ = 1 + TAU_S * (1 - x) * (1 - 2 * y)
    assert poly_zero(sp.diff(r, x) - y * U_) and poly_zero(sp.diff(r, y) - x * V_)
    assert poly_zero(sp.diff(r, x, y) - (1 + TAU_S * (1 - 2 * x) * (1 - 2 * y)))
    assert poly_zero(W * sp.diff(r, x, y) - U_ * V_ - TAU_S * x * y)
    assert sp.cancel(sp.diff(r, x, y) / (sp.diff(r, x) * sp.diff(r, y)) - 1 / r - TAU_S / (W * U_ * V_)) == 0


@claim("6.1.b", "on [0,1]^2: W >= 1, U,V >= 1-tau > 0; g' = 2x[1+tau(1-x)(1-2x)] >= 2x(1-tau/8); "
       "g(45/64) - 1/2 = 42978321721/2684354560000; g(z) >= z^2, g(1) = 1",
       "sympy-exact + z3")
def check_61_monotone():
    g = sp.expand(_r().subs(y, x))
    assert poly_zero(sp.diff(g, x) - 2 * x * (1 + TAU_S * (1 - x) * (1 - 2 * x)))
    assert poly_zero((1 - x) * (1 - 2 * x) + sp.Rational(1, 8) - 2 * (x - sp.Rational(3, 4)) ** 2)
    assert g.subs(x, sp.Rational(45, 64)) - sp.Rational(1, 2) == sp.Rational(42978321721, 2684354560000)
    assert poly_zero(g - x**2 - TAU_S * x**2 * (1 - x) ** 2) and g.subs(x, 1) == 1
    X, Y = z3.Reals("x y")
    box = [X >= 0, X <= 1, Y >= 0, Y <= 1]
    T = Q(TAU)
    z3_valid(box, 1 + T * (1 - 2 * X) * (1 - Y) >= 1 - T, None)
    z3_valid(box, 1 + T * (1 - X) * (1 - Y) >= 1, None)
    assert TAU < 1


@claim("6.1.c", "A.4 re-derived by a different method: the bidegree-(3,3) Bernstein coefficients of "
       "WUV - tau(1-r) on [0,45/64]^2, obtained by solving the monomial linear system, are > 0 "
       "with the published minimum", "sympy-exact")
def check_61_bernstein():
    s_, t_ = sp.symbols("s t")
    W = 1 + TAU_S * (1 - x) * (1 - y)
    U_ = 1 + TAU_S * (1 - 2 * x) * (1 - y)
    V_ = 1 + TAU_S * (1 - x) * (1 - 2 * y)
    P = sp.expand((W * U_ * V_ - TAU_S * (1 - _r())).subs({x: sp.Rational(45, 64) * s_,
                                                           y: sp.Rational(45, 64) * t_}))
    cs = sp.symbols("c0:16")
    basis = lambda i, var: sp.binomial(3, i) * var**i * (1 - var) ** (3 - i)
    B = sum(cs[4 * i + j] * basis(i, s_) * basis(j, t_) for i in range(4) for j in range(4))
    sol = sp.solve(sp.Poly(sp.expand(B - P), s_, t_).coeffs(), cs, dict=True)
    assert len(sol) == 1 and len(sol[0]) == 16
    vals = [sol[0][c_] for c_ in cs]
    assert all(val > 0 for val in vals)
    assert min(vals) == sp.Rational(BERN_MIN.numerator, BERN_MIN.denominator)


@claim("6.1.d", "Delta_x(y) = L(x,y) - L(x,x)/2 - L(y,y)/2 has d/dy Delta = L_2(x,y) - L_2(y,y), "
       "L_12 = Lam''(r) r_x r_y + Lam'(r) r_xy, and L_2 = (r_y/r) M(r) with "
       "r_y/r = 1/y - tau(1-x)/(1+tau(1-x)(1-y))  (Lam, H abstract)", "sympy-exact")
def check_61_reduction():
    Lam = sp.Function("Lam")
    r = _r()
    Lxy = Lam(r)
    Delta = Lxy - Lam(r.subs(y, x)) / 2 - Lam(r.subs(x, y)) / 2
    L2 = lambda X_, Y_: sp.diff(Lam(_r()), y).subs({x: X_, y: Y_}, simultaneous=True)
    yy = sp.symbols("yy", positive=True)
    lhs = sp.diff(Delta, y)
    rhs = sp.diff(Lam(_r()), y) - L2(y, y)
    assert sp.simplify(lhs - rhs) == 0
    L12 = sp.diff(Lam(r), x, y)
    Lp = lambda e: sp.Subs(sp.Derivative(Lam(yy), yy), yy, e).doit()
    Lpp = lambda e: sp.Subs(sp.Derivative(Lam(yy), yy, 2), yy, e).doit()
    assert sp.simplify(L12 - (Lpp(r) * sp.diff(r, x) * sp.diff(r, y) + Lp(r) * sp.diff(r, x, y))) == 0
    # L_2 = A_x(y) M(r) with Lam = log H
    L2H = sp.diff(sp.log(Hf(r)), y)
    Hp_at = sp.Subs(sp.Derivative(Hf(yy), yy), yy, r).doit()
    A = 1 / y - TAU_S * (1 - x) / (1 + TAU_S * (1 - x) * (1 - y))
    assert sp.cancel(sp.diff(r, y) / r - A) == 0
    assert sp.simplify(L2H - A * (r * Hp_at / Hf(r))) == 0
    # a -> tau a/(1+tau a(1-y)) has derivative tau/(1+tau a(1-y))^2 > 0
    assert sp.simplify(sp.diff(TAU_S * a / (1 + TAU_S * a * (1 - y)), a)
                       - TAU_S / (1 + TAU_S * a * (1 - y)) ** 2) == 0


@claim("6.1.e", "case logic: Case A (g(y)<1/2) gives L_12<0 on [x,y]; Case B (g(y)>=1/2) gives "
       "A_x M(r) > A_y M(g) from 0<A_x<A_y, M>0 on (0,1/2), M<=0 on [1/2,1), M decreasing",
       "z3 (+ 4.1, 4.4, 6.1.a-d; hand: FTC in s)")
def check_61_logic():
    # Case A: L12 = P * (rho + lam2), P = Lam'(r) r_x r_y > 0, rho = r_xy/(r_x r_y) <= 1/r + 1/(1-r)
    # (6.1.a-c), lam2 = Lam''/Lam' < -1/r - 1/(1-r) (Lemma 4.1, valid as 0 < r <= g(y) < 1/2).
    Pp, rho, l2, R = z3.Reals("P rho l2 r")
    z3_valid([Pp > 0, R > 0, R < Q(Fr(1, 2)), rho * R * (1 - R) <= 1, l2 * R * (1 - R) < -1],
             Pp * (rho + l2) < 0, None)
    # Case B
    Ax, Ay, Mr, Mg, R, Gy = z3.Reals("Ax Ay Mr Mg r gy")
    hyps = [Ax > 0, Ax < Ay, R > 0, R < Gy, Gy < 1, Gy >= Q(Fr(1, 2)),
            z3.Implies(R < Q(Fr(1, 2)), Mr > 0), Mg <= 0,
            z3.Implies(R >= Q(Fr(1, 2)), z3.And(Mg < Mr, Mr <= 0))]
    z3_valid(hyps, Ax * Mr > Ay * Mg, None)


# ============================================================ W0 monotonicity
@claim("W0.a", "W0'(v) = (2H(q) - z q_z H'(q))/z^2 (q = g(z), z = e^-v, H abstract); "
       "z q_z = 2q - 2 tau z^3(1-z); H(q) - qH'(q) = -log(1-q); hence "
       "z^2 W0' = -2 log(1-q) + 2 tau z^3(1-z) H'(q)", "sympy-exact")
def check_W0_identities():
    g = z**2 * (1 + TAU_S * (1 - z) ** 2)
    W0 = Hf(g) / z**2
    dW = -z * sp.diff(W0, z)
    yy = sp.symbols("yy", positive=True)
    Hp_at = sp.Subs(sp.Derivative(Hf(yy), yy), yy, g).doit()
    assert sp.simplify(dW - (2 * Hf(g) - z * sp.diff(g, z) * Hp_at) / z**2) == 0
    assert poly_zero(z * sp.diff(g, z) - 2 * g + 2 * TAU_S * z**3 * (1 - z))
    m = {q: La, 1 - q: Lb}
    assert zero_with_logs(Hs(q) - q * sp.diff(Hs(q), q) + sp.log(1 - q), m)
    # assemble with the explicit H
    expr = 2 * Hs(q) - (2 * q - 2 * TAU_S * z**3 * (1 - z)) * sp.diff(Hs(q), q)
    assert zero_with_logs(expr - (-2 * sp.log(1 - q) + 2 * TAU_S * z**3 * (1 - z) * sp.diff(Hs(q), q)), m)
    # H'(q) - log(1-q) = -log q  (>= 0 for q <= 1)
    assert zero_with_logs(sp.diff(Hs(q), q) - sp.log(1 - q) + sp.log(q), m)


@claim("W0.b", "z^3(1-z) <= 27/256 on [0,1] (27/256 - z^3 + z^4 = (z-3/4)^2(z^2+z/2+3/16)), "
       "so c := 2 tau z^3(1-z) <= 54 tau/256 < 2; then -2log(1-q) + c H'(q) > 0 for 0<q<1",
       "sympy-exact + z3")
def check_W0_sign():
    assert poly_zero(sp.Rational(27, 256) - z**3 + z**4
                     - (z - sp.Rational(3, 4)) ** 2 * (z**2 + z / 2 + sp.Rational(3, 16)))
    assert sp.discriminant(z**2 + z / 2 + sp.Rational(3, 16), z) < 0
    assert 54 * TAU / 256 < 2
    # skeleton: A := -log(1-q) > 0, B := H'(q); q <= 1/2 => B >= 0; q > 1/2 => B >= -A
    # (B - log(1-q) = -log q >= 0, W0.a);  0 <= c < 2.
    A, B, C, Qq = z3.Reals("A B c q")
    z3_valid([A > 0, C >= 0, C < 2, Qq > 0, Qq < 1,
              z3.Implies(Qq <= Q(Fr(1, 2)), B >= 0), z3.Implies(Qq > Q(Fr(1, 2)), B >= -A)],
             2 * A + C * B > 0, None)


# ============================================================ Lemma 6.2
k2 = Fr(178, 25)        # (178/25) = k^2


@claim("6.2.a", "reduction: (6.tuned-second) / (2xy) is F0 > 0, and F0 = G(u)/8e8 - D/(2m0) + beta0 P "
       "(P = sqrt(W0(s)W0(sigma)))", "sympy-exact")
def check_62_reduction():
    # with x = e^-s, y = e^-sigma (positive symbols x, y; s = -log x etc.)
    G = lambda X_: Hs(X_) / X_            # G(-log X) = H(X)/X
    W0 = lambda X_: Hs(sp.expand(X_**2 * (1 + TAU_S * (1 - X_) ** 2))) / X_**2
    m = {x: La, y: Lb, 1 - x: Lc, 1 - y: Ld, 1 - x * y: Le}
    lhs_over = (2 * A0_S * Hs(x * y)) / (2 * x * y) - (x * Hs(y) + y * Hs(x)) / (M0_S * 2 * x * y)
    rhs = A0_S * G(x * y) - (G(x) + G(y)) / (2 * M0_S)
    assert zero_with_logs(lhs_over - rhs, m)
    # the product term: sqrt(H(g(x))H(g(y)))/(xy) = sqrt(W0(s)W0(sigma)) as xy > 0 -- squares agree:
    Hg = sp.Function("Hg")
    assert sp.simplify((Hg(x) * Hg(y)) / (x * y) ** 2 - (Hg(x) / x**2) * (Hg(y) / y**2)) == 0
    # F0 = G(u)/8e8 - D/(2m0) + beta0 P, with alpha0 = 1/(2m0) + 1/8e8
    Gs, Gsig, Gu, P = sp.symbols("Gs Gsig Gu P")
    F0 = A0_S * Gu - (Gs + Gsig) / (2 * M0_S) + B0_S * P
    D = Gs + Gsig - Gu
    assert sp.expand(F0 - (Gu / 800000000 - D / (2 * M0_S) + B0_S * P)) == 0


@claim("6.2.b", "D <= G(s) - s < G(s) and D < 1 (via G' > 1 and G(v) - v < 1)",
       "sympy-exact(G.2) + z3 + hand(MVT)")
def check_62_D():
    # G(s+sigma) - G(sigma) >= s  (MVT with G' > 1);  G(s) - s < 1  (G.2).  Skeleton:
    Gs, Gsig, Gu, S_, Sig = z3.Reals("Gs Gsig Gu s sigma")
    D = Gs + Gsig - Gu
    hyp = [S_ > 0, Sig >= S_, Gu - Gsig >= S_, Gs - S_ < 1]
    z3_valid(hyp, z3.And(D <= Gs - S_, D < Gs, D < 1), None)


def _sqrt_lower(n: Fr, digits=40) -> Fr:
    """A rational lower bound for sqrt(n) (n > 0 rational), exact integer arithmetic."""
    sc = 10**digits
    return Fr(isqrt(n.numerator * sc * sc // n.denominator), sc)


@claim("6.2.c", "Case 1 (G(sigma) >= (178/25)G(s)): F0 - [G(u)/8e8 + c1 G(s)] = (G(s)-D)/(2m0) "
       "+ beta0(P - (8/5)Q) + (8 beta0/5)(Q - k G(s)) with Q = sqrt(G(s)G(sigma)), k = sqrt(178)/5; "
       "c1 = (8 beta0/5)k - 1/(2m0) > 0 EXACTLY (c1 >= 2.8908190756e-6)",
       "sympy-exact + exact rationals + z3 (+ A.5, 6.2.b)")
def check_62_case1():
    Gs, Gsig, Gu, P, Qq, D = sp.symbols("Gs Gsig Gu P Q D")
    kk = sp.sqrt(178) / 5
    c1 = sp.Rational(8, 5) * B0_S * kk - 1 / (2 * M0_S)
    F0 = Gu / 800000000 - D / (2 * M0_S) + B0_S * P
    cert = (Gs - D) / (2 * M0_S) + B0_S * (P - sp.Rational(8, 5) * Qq) + sp.Rational(8, 5) * B0_S * (Qq - kk * Gs)
    assert sp.expand(F0 - (Gu / 800000000 + c1 * Gs) - cert) == 0
    # c1 > 0 exactly:  (8 beta0 sqrt(178)/25)^2 > (1/(2 m0))^2, both sides positive
    assert (Fr(8, 25) * BETA0) ** 2 * 178 > (1 / (2 * M0)) ** 2
    c1_lo = Fr(8, 25) * BETA0 * _sqrt_lower(Fr(178)) - 1 / (2 * M0)
    assert c1_lo >= Fr("2.8908190756e-6"), float(c1_lo)
    # margin comparison quoted in the problem file: m0 alpha0 - 1/2 = m0/8e8 (the y -> 1 edge)
    assert M0 * ALPHA0 - Fr(1, 2) == M0 / 800000000
    # z3 version of the whole implication, without square roots:
    #   P >= 0, P^2 = W0(s)W0(sigma) >= (64/25) G(s)G(sigma) >= (64/25)(178/25) G(s)^2,
    #   0 <= D < G(s), G(u) > 0  =>  F0 > 0.
    Gs_, Gu_, P_, D_ = z3.Reals("Gs Gu P D")
    F0z = Gu_ / 800000000 - D_ / (2 * Q(M0)) + Q(BETA0) * P_
    z3_valid([Gs_ > 0, Gu_ > 0, D_ >= 0, D_ < Gs_, P_ >= 0,
              P_ * P_ >= Q(Fr(64, 25) * k2) * Gs_ * Gs_], F0z > 0, None)
    return float(c1_lo)


def _w0_2_bounds_arb():
    flint.ctx.prec = 200
    tau = flint.arb(flint.fmpq(TAU.numerator, TAU.denominator))
    zz = (flint.arb(-2)).exp()
    g = zz * zz * (1 + tau * (1 - zz) ** 2)
    Hg = -g * g.log() - (1 - g) * (1 - g).log()
    return (flint.arb(4)).exp() * Hg


@claim("6.2.d", "Case 2 (s,sigma >= 2): F0 - [G(u)/8e8 + (beta0 W0(2) - 1/(2m0))] = (1-D)/(2m0) "
       "+ beta0(P - W0(2)); P >= W0(2) by W0 increasing; scalar beta0 W0(2) - 1/(2m0) >= 0.4053615705664",
       "sympy-exact + z3 + interval + arb")
def check_62_case2():
    Gu, P, D, W2 = sp.symbols("Gu P D W2")
    F0 = Gu / 800000000 - D / (2 * M0_S) + B0_S * P
    assert sp.expand(F0 - (Gu / 800000000 + (B0_S * W2 - 1 / (2 * M0_S)))
                     - ((1 - D) / (2 * M0_S) + B0_S * (P - W2))) == 0
    from costa_sadhu_thm12 import W0_point, B0_I, INV2M0
    s2 = B0_I * W0_point(2.0) - INV2M0
    assert s2.lo >= 0.4053615705664 - 1e-13 and s2.lo > 0
    if flint is not None:
        W2a = _w0_2_bounds_arb()
        s2a = flint.arb(flint.fmpq(BETA0.numerator, BETA0.denominator)) * W2a \
            - 1 / flint.arb(flint.fmpq(2 * M0.numerator, M0.denominator))
        assert s2a > flint.arb("0.4053615705664")
        assert abs(float(s2a.mid()) - 0.5 * (s2.lo + s2.hi)) < 1e-12
    Gu_, P_, D_, W2_ = z3.Reals("Gu P D W2")
    z3_valid([Gu_ > 0, D_ < 1, P_ >= W2_, Q(BETA0) * W2_ - 1 / (2 * Q(M0)) > 0],
             Gu_ / 800000000 - D_ / (2 * Q(M0)) + Q(BETA0) * P_ > 0, None)


@claim("6.2.e", "Case 3 (s,sigma <= 2^-10): D < uH(lam); W0(w) >= 2w log(1/2u); "
       "H(lam) <= 2 sqrt(lam(1-lam)); and the final bound; scalar 8 beta0 log2 - 1/(2m0) > 0 EXACTLY",
       "sympy-exact + exact rationals + z3 + hand(FTC/Tonelli, e^t >= 1+t+t^2/2, log t <= t-1)")
def check_62_case3():
    s_, sg = sp.symbols("s sigma", positive=True)
    aa, bb = sp.symbols("aa bb", positive=True)
    # (i) the double integral int_0^s int_0^sigma db da/(a+b)
    inner = sp.integrate(1 / (aa + bb), (bb, 0, sg))
    assert sp.simplify(inner - (sp.log(aa + sg) - sp.log(aa))) == 0
    outer = sp.integrate(sp.log(aa + sg) - sp.log(aa), (aa, 0, s_))
    target = (s_ + sg) * sp.log(s_ + sg) - s_ * sp.log(s_) - sg * sp.log(sg)
    assert zero_with_logs(outer - target, {s_: La, sg: Lb, s_ + sg: Lc})
    # ... and it equals u H(lam), u = s + sigma, lam = s/u
    U_ = s_ + sg
    assert zero_with_logs(target - U_ * Hs(s_ / U_), {s_: La, sg: Lb, s_ + sg: Lc})
    # mixed derivative of (A,B) -> G(A)+G(B)-G(A+B) is -G''(A+B)
    Gf = sp.Function("G")
    assert sp.simplify(sp.diff(Gf(aa) + Gf(bb) - Gf(aa + bb), aa, bb)
                       + sp.Subs(sp.Derivative(Gf(t), t, 2), t, aa + bb).doit()) == 0
    # (ii) e^{2w}(1 - g(e^-w)) = e^{2w} - 1 - tau(1 - e^-w)^2  (polynomial identity in z = e^-w)
    g = z**2 * (1 + TAU_S * (1 - z) ** 2)
    assert sp.cancel((1 - g) / z**2 - (1 / z**2 - 1 - TAU_S * (1 - z) ** 2)) == 0
    # (iii) sqrt(s sigma) = u sqrt(lam(1-lam))
    assert sp.simplify(sp.sqrt(s_ * sg) - U_ * sp.sqrt((s_ / U_) * (1 - s_ / U_))) == 0
    # (iv) H(lam) <= 2 sqrt(lam(1-lam)): with A = sqrt(lam), B = sqrt(1-lam) (A^2 + B^2 = 1)
    #      -lam log lam <= 2(A - lam), -(1-lam)log(1-lam) <= 2(B - (1-lam))  [log t <= t-1, hand]
    #      and A + B - 1 - AB = -(1-A)(1-B) <= 0.
    assert poly_zero(aa + bb - 1 - aa * bb + (1 - aa) * (1 - bb))
    # (v) skeleton of e^{2w} r_w >= 2w and W0(w) >= 2w log(1/(2u)):
    #     E := e^{2w} >= 1+2w+2w^2 (hand), e := 1-e^-w in [0, w] (hand), tau < 1;
    #     e^{2w} r_w = E - 1 - tau e^2 (by (ii)).
    W_, E_, e_ = z3.Reals("w E e")
    z3_valid([W_ > 0, E_ >= 1 + 2 * W_ + 2 * W_ * W_, e_ >= 0, e_ <= W_],
             E_ - 1 - Q(TAU) * e_ * e_ >= 2 * W_, None)
    # (vi) the final combination: F0 - [G(u)/8e8 + 2uR(beta0 Lg - 1/(2m0))]
    #      = (uH - D)/(2m0) + beta0(P - 2uR Lg) + u(2R - H)/(2m0),
    #      R = sqrt(lam(1-lam)), H = H(lam), Lg = log(1/(2u)).
    Gu, P, D, uu, R, Hl, Lg = sp.symbols("Gu P D u R Hl Lg")
    F0 = Gu / 800000000 - D / (2 * M0_S) + B0_S * P
    lhs = F0 - (Gu / 800000000 + 2 * uu * R * (B0_S * Lg - 1 / (2 * M0_S)))
    rhs = (uu * Hl - D) / (2 * M0_S) + B0_S * (P - 2 * uu * R * Lg) + uu * (2 * R - Hl) / (2 * M0_S)
    assert sp.expand(lhs - rhs) == 0
    # (vii) log(1/(2u)) >= 8 log 2 for u <= 2^-9, and 8 beta0 log 2 > 1/(2 m0) with the exact
    #       rational lower bound _L2LO <= log 2 (atanh series, interval.py)
    assert 8 * BETA0 * _L2LO - 1 / (2 * M0) >= Fr("0.2421300730523")
    assert _L2LO < _L2HI and _L2HI - _L2LO < Fr(1, 10**30)
    if flint is not None:
        flint.ctx.prec = 200
        lo = flint.arb(flint.fmpq(_L2LO.numerator, _L2LO.denominator))
        assert lo < flint.arb(2).log()          # our rational bound is below Arb's log 2
    # z3 skeleton of the final step (the strict "<" comes from D < uH(lam)):
    Gu_, P_, D_, U2, R_, H_, Lg_ = z3.Reals("Gu P D u R H Lg")
    l2 = Q(_L2LO)
    z3_valid([Gu_ > 0, U2 > 0, U2 <= Q(Fr(1, 512)), R_ > 0, D_ < U2 * H_, H_ <= 2 * R_,
              P_ >= 2 * U2 * R_ * Lg_, Lg_ >= 8 * l2],
             Gu_ / 800000000 - D_ / (2 * Q(M0)) + Q(BETA0) * P_ > 0, None)


def h_sqrt_interval_crosscheck(n=4096):
    """Cross-check of H(lam) <= 2 sqrt(lam(1-lam)) on [1/n, 1/2] (symmetric), by cells."""
    from interval import isqrt_
    worst = float("inf")
    for i in range(1, n // 2):
        L = I(i / n, (i + 1) / n)
        lb = 2.0 * isqrt_(I(i / n) * (1.0 - I(i / n)))      # 2 sqrt(lam(1-lam)) increasing on [0,1/2]
        gap = (lb - I(Hr(L).hi)).lo                          # H increasing on [0,1/2]
        assert gap > 0, (i, gap)
        worst = min(worst, gap)
    return worst


@claim("6.2.x", "cross-check: H(lam) <= 2 sqrt(lam(1-lam)) on [1/4096, 1/2] by 2047 interval cells",
       "interval")
def check_62_hsqrt():
    assert h_sqrt_interval_crosscheck() > 0


@claim("6.2.f", "the residual region: not(Case 1, 2, 3) and 0 < s <= sigma imply 2^-11 < t < 17, "
       "0 <= xi < 15/17 (t = (s+sigma)/2, xi = (sigma-s)/(sigma+s)), which A.6 + A.7 cover",
       "z3 (+ A.5 G(16v) >= (178/25)G(v), G increasing)")
def check_62_residual():
    S_, Sg, Gs, Gsg, G16 = z3.Reals("s sigma Gs Gsig G16")
    K = Q(k2)
    hyps = [S_ > 0, Sg >= S_, Gs > 0,
            G16 >= K * Gs,                                    # A.5 at v = s
            z3.Implies(Sg >= 16 * S_, Gsg >= G16),            # G increasing
            z3.Not(Gsg >= K * Gs),                            # not Case 1
            z3.Not(z3.And(S_ >= 2, Sg >= 2)),                 # not Case 2
            z3.Not(z3.And(S_ <= Q(Fr(1, 1024)), Sg <= Q(Fr(1, 1024))))]   # not Case 3
    T = (S_ + Sg) / 2
    # xi < 15/17  <=>  17(sigma - s) < 15(sigma + s)   (sigma + s > 0);  xi >= 0 <=> sigma >= s
    goal = z3.And(T > Q(Fr(1, 2048)), T < 17, 17 * (Sg - S_) < 15 * (Sg + S_), Sg - S_ >= 0)
    z3_valid(hyps, goal, None)
    # the paper's intermediate bounds as well: 2^-14 < s < 2, 2^-10 < sigma < 32
    z3_valid(hyps, z3.And(S_ > Q(Fr(1, 16384)), S_ < 2, Sg > Q(Fr(1, 1024)), Sg < 32), None)


# ============================================================ Prop 6.3 (+ theorem)
@claim("6.3.a", "weights and constants: alpha0+beta0 = 1, 0 < alpha0, beta0 < 1, 2m0(1-1/8e8) > 1, "
       "1 - m0 = 0.3828852549667978, and gamma = (1-c)/m0 > 1 for 0 < c < 1-m0", "exact rationals + z3")
def check_63_constants():
    assert ALPHA0 + BETA0 == 1 and 0 < ALPHA0 < 1 and 0 < BETA0 < 1
    assert 2 * M0 * (1 - Fr(1, 800000000)) > 1 and 1 - M0 == Fr("0.3828852549667978")
    C = z3.Real("c")
    z3_valid([C > 0, C < 1 - Q(M0)], (1 - C) / Q(M0) > 1, None)
    # Jensen for finite mixtures (Lemma 2.1 before the weak limit):
    # sum l_i a_i^2 - (sum l_i a_i)^2 = sum l_i (a_i - abar)^2 when sum l_i = 1  (n = 3 shown)
    l1, l2, a1, a2, a3 = sp.symbols("l1 l2 a1 a2 a3")
    l3 = 1 - l1 - l2
    abar = l1 * a1 + l2 * a2 + l3 * a3
    assert sp.expand(l1 * a1**2 + l2 * a2**2 + l3 * a3**2 - abar**2
                     - (l1 * (a1 - abar) ** 2 + l2 * (a2 - abar) ** 2 + l3 * (a3 - abar) ** 2)) == 0


def prop63_instance(xs, mix, m0=None):
    """Interval lower bound of
        alpha0 sum p_i p_j H(x_i x_j) + beta0 sum_k l_k sum_ij Q_k(i)Q_k(j) H(r(x_i,x_j))
        - m(P)/m0 sum p_i H(x_i)
    for P = sum_k l_k Q_k on the support xs (floats in (0,1)), rho = sum_k l_k Q_k (x) Q_k.
    mix = [(l_k, [Q_k(i)])] with exact Fractions."""
    from costa_sadhu_thm12 import TAU_I
    m0 = M0 if m0 is None else m0
    n = len(xs)
    p = [sum(l * Qk[i] for l, Qk in mix) for i in range(n)]
    assert sum(p) == 1
    X = [I(xi) for xi in xs]
    Hx = [Hr(Xi) for Xi in X]
    Hxx = [[Hr(X[i] * X[j]) for j in range(n)] for i in range(n)]
    Hr_ = [[Hr(X[i] * X[j] * (1.0 + TAU_I * (1.0 - X[i]) * (1.0 - X[j]))) for j in range(n)] for i in range(n)]
    ind = I(0.0)
    for i in range(n):
        for j in range(n):
            ind = ind + IF(p[i] * p[j]) * Hxx[i][j]
    ex5 = I(0.0)
    for l, Qk in mix:
        for i in range(n):
            for j in range(n):
                if Qk[i] and Qk[j]:
                    ex5 = ex5 + IF(l * Qk[i] * Qk[j]) * Hr_[i][j]
    mP = I(0.0)
    hP = I(0.0)
    for i in range(n):
        mP = mP + IF(p[i]) * X[i]
        hP = hP + IF(p[i]) * Hx[i]
    return IF(ALPHA0) * ind + IF(BETA0) * ex5 - mP * hP / IF(m0)


def prop63_random(trials=200, seed=1):
    import random
    rnd = random.Random(seed)
    worst = float("inf")
    for _ in range(trials):
        n = rnd.randint(1, 5)
        xs = sorted({rnd.choice([rnd.random(), 0.69 + 0.002 * rnd.random(), 1 - 1e-3 * rnd.random()])
                     for _ in range(n)})
        xs = [min(max(xx, 1e-6), 1 - 1e-6) for xx in xs]
        n = len(xs)
        K = rnd.randint(1, 3)
        mix = []
        ls = [Fr(rnd.randint(1, 9)) for _ in range(K)]
        tot = sum(ls)
        for l in ls:
            w_ = [Fr(rnd.randint(0, 9)) for _ in range(n)]
            if sum(w_) == 0:
                w_[0] = Fr(1)
            sw = sum(w_)
            mix.append((l / tot, [wi / sw for wi in w_]))
        lb = prop63_instance(xs, mix)
        assert lb.lo > 0, (xs, mix, lb)
        worst = min(worst, lb.lo)
    return worst


@claim("6.3.x", "sanity test (not a proof): Prop. 6.3's inequality certified on 200 random finitely "
       "supported P with rho a finite mixture of Q (x) Q (an element of C_3(P)); a point mass at "
       "e^-t_c is certified positive, and negative when 1/m0 is raised by 1e-7 (negative control)",
       "interval (instances)")
def check_63_instances():
    prop63_random()
    import math as _m
    xc = _m.exp(-0.369781418829901)
    pm = [(Fr(1), [Fr(1)])]
    assert prop63_instance([xc], pm).lo > 0
    assert prop63_instance([xc], pm, m0=1 / (1 / M0 + Fr(1, 10**7))).hi < 0


@claim("L.ex5", "Liu's Example 5 (arXiv:2306.08824 Sec. 2): X = 0 w.p. sbar + f(sbar)(1[u>1/2] - 1[u<=1/2]), "
       "U uniform, gives P(X=0) = sbar and Pi_{s,t}(0,0) = sbar tbar + f(sbar) f(tbar); with "
       "f = l x(1-x) in x = sbar this is r_l(x,y) = xy(1 + l^2(1-x)(1-y)); admissible iff 0 <= f <= min(s, sbar)",
       "sympy-exact")
def check_liu_example5():
    s_, t_, fs, ft, l_ = sp.symbols("s t fs ft l")
    sb, tb = 1 - s_, 1 - t_
    # U uniform: the two halves u <= 1/2 (sign -1) and u > 1/2 (sign +1) each have probability 1/2;
    # given U, X and Y are independent (conditionally i.i.d. protocol).
    pX0 = sp.Rational(1, 2) * (sb - fs) + sp.Rational(1, 2) * (sb + fs)
    assert sp.expand(pX0 - sb) == 0
    pi00 = sp.Rational(1, 2) * (sb - fs) * (tb - ft) + sp.Rational(1, 2) * (sb + fs) * (tb + ft)
    assert sp.expand(pi00 - (sb * tb + fs * ft)) == 0
    # complemented coordinates x = sbar, y = tbar, f(x) = l x (1-x)
    assert sp.expand((x * y + (l_ * x * (1 - x)) * (l_ * y * (1 - y)))
                     - x * y * (1 + l_**2 * (1 - x) * (1 - y))) == 0
    # both probabilities sbar -+ f lie in [0,1] iff f <= sbar and f <= s;  and l x(1-x) <= min(x,1-x)
    # for 0 <= l <= 1 (z3)
    X, Lz = z3.Reals("x l")
    z3_valid([X >= 0, X <= 1, Lz >= 0, Lz <= 1],
             z3.And(Lz * X * (1 - X) <= X, Lz * X * (1 - X) <= 1 - X, Lz * X * (1 - X) >= 0), None)
    assert L0 <= 1


# ============================================================ driver
ALL = [check_G_derivs, check_G_signs,
       check_41_identity, check_41_positivity, check_41_interval,
       check_44_chain, check_44_concave, check_44_interval,
       check_61_identities, check_61_monotone, check_61_bernstein, check_61_reduction, check_61_logic,
       check_W0_identities, check_W0_sign,
       check_62_reduction, check_62_D, check_62_case1, check_62_case2, check_62_case3, check_62_hsqrt, check_62_residual,
       check_63_constants, check_63_instances, check_liu_example5]


def run_all(verbose=True, only=None):
    say = print if verbose else (lambda *a_: None)
    if z3 is None:
        raise SystemExit("z3-solver is required (pip install z3-solver)")
    RESULTS.clear()
    t_all = time.time()
    for chk in ALL:
        if only and not chk.cid.startswith(only):
            continue
        t0 = time.time()
        chk()
        say(f"[OK] {chk.cid:6s} {chk.method:40s} {time.time()-t0:6.1f}s  {chk.statement}")
    say(f"all {len(RESULTS)} analytic-glue claims checked in {time.time()-t_all:.1f}s"
        f"  (sympy {sp.__version__}, z3 {z3.get_version_string()},"
        f" python-flint {flint.__version__ if flint else 'absent'})")
    return list(RESULTS)


if __name__ == "__main__":
    run_all(only=sys.argv[1] if len(sys.argv) > 1 else None)
