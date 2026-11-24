"""Machine checks of the ANALYTIC glue in Jiang, arXiv:2609.08291 v1
(c_UC >= 1 - m = 1531541/4000000 = 0.38288525).  Companion of jiang_checks.py, which
re-certifies the FINITE computations (12 scalar signs, bridge, kernel cover, mixture cover).

Same conventions as analytic_glue.py (Costa-Sadhu Thm 1.2):

  sympy-exact   identity reduced to 0 by exact rational-function arithmetic (sympy.cancel)
                after every log(.) atom is replaced by an independent symbol (logsub below),
                or a derivative of an explicit formula / of abstract functions computed by sympy.
  z3            implication between real-arithmetic facts ("skeleton"), negation unsat in z3
                (nonlinear real arithmetic, exact rationals).  The hypotheses are facts proved
                by the other checks or by the named hand steps, as listed per claim.
  interval      outward-rounded interval arithmetic (interval.py / jiang_checks.py).
  arb           FLINT/Arb balls at 200 bits (python-flint): an independent second evaluation.
  exact         exact rational arithmetic (fractions.Fraction).
  hand(name)    a standard analysis fact we state but do not formalise (MVT, IVT, Jensen,
                concavity, Taylor bound, continuity at a boundary point, ...).
  read only     probability / measure-theory steps that are read in the source, not encoded.

Run: python3 analytic_glue_jiang.py [claim-id prefix].  Needs sympy, z3-solver; python-flint
for the Arb cross-checks.  Source: arXiv:2609.08291 v1 LaTeX (frankl_038288525_proof.tex),
Sections 2-7 and Appendix A; equation labels below are the paper's \\label names.

Notation (paper): h = binary entropy (nats), h* = h(x*), k* = h'(x*)/(2h*),
E(x) = -k*(x-x*) - (7/10)(x-x*)^2, D piecewise (h | ln2 | ln2 h(x^2)/h(z^2)),
phi = sigma sqrt(D h/h*) e^E, s = sqrt(h(x^2)), psi = phi | blend | s (breaks A, B),
a = 1 | sqrt((1-2x^2)/(2x(1-x))) | 0 (breaks 1/2, 1/sqrt2), r = xy + a(x)a(y)(min - xy),
K = h(r), G(u) = h(e^-u) e^u, P(u) = psi(e^-u) e^u, u = t(1+xi), v = t(1-xi),
F = k0 G(2t) + m w4 P(u)P(v) - (G(u)+G(v))/2, k0 = m w0.
"""
from __future__ import annotations

import math
import sys
import time
from fractions import Fraction as Fr

import sympy as sp

from interval import I, IF, ilog, iexp, H, LN2, _L2LO, _L2HI
import jiang_checks as jc
import analytic_glue as ag

z3 = ag.z3
flint = ag.flint
Q = ag.Q


def z3_valid(hyps, goal, vars_=None):
    """(and hyps) => goal over the reals: analytic_glue.z3_valid, which first shows the hypotheses
    jointly satisfiable (non-vacuity guard) and then that the negated goal is unsat."""
    return ag.z3_valid(hyps, goal, vars_)


RESULTS = []


def claim(cid, statement, method):
    def deco(f):
        def run():
            f()
            RESULTS.append((cid, statement, method, "OK"))
        run.cid, run.statement, run.method = cid, statement, method
        return run
    return deco


# ============================================================ sympy helpers
x, y, q, t, u, v, c, p = sp.symbols("x y q t u v c p", positive=True)
al, be, xi = sp.symbols("alpha beta xi", real=True)
_PRIME_SYMS = {}


def _logc(cst):
    """log of a positive rational, as an integer combination of symbols log(prime)."""
    cst = sp.Rational(cst)
    assert cst > 0, cst
    out = 0
    for pr, e in sp.factorint(cst.p).items():
        out += e * _PRIME_SYMS.setdefault(pr, sp.Symbol(f"Lp{pr}"))
    for pr, e in sp.factorint(cst.q).items():
        out -= e * _PRIME_SYMS.setdefault(pr, sp.Symbol(f"Lp{pr}"))
    return out


def logsub(expr, bases):
    """Replace every log(arg) by sum e_i * S_i (+ logs of primes), where arg factors as
    const * prod B_i^{e_i} with B_i (up to sign) in `bases` = {B_i: S_i}.  Asserts that every
    factor is listed and that the constant (after absorbing signs) is positive, so nothing
    transcendental is left to sympy's heuristics."""
    def rep(L):
        arg = sp.factor(sp.together(L.args[0]))
        num, den = sp.fraction(arg)
        out, sign, cst = 0, 1, sp.Integer(1)
        for part, sgn_e in ((num, 1), (den, -1)):
            k, facs = sp.factor_list(part)
            cst = cst * (k if sgn_e == 1 else 1 / k)
            for f, e in facs:
                for B, S in bases.items():
                    if sp.expand(f - B) == 0:
                        out += sgn_e * e * S
                        break
                    if sp.expand(f + B) == 0:
                        out += sgn_e * e * S
                        sign *= (-1) ** e
                        break
                else:
                    raise AssertionError(f"unlisted log factor {f} in {L}")
        cst = cst * sign
        return out + _logc(cst)
    return sp.sympify(expr).replace(lambda e: isinstance(e, sp.log), rep)


def zero_logs(expr, bases):
    e = logsub(expr, bases)
    assert not e.atoms(sp.log)
    return sp.cancel(sp.together(e)) == 0


def hs(z_):
    return -z_ * sp.log(z_) - (1 - z_) * sp.log(1 - z_)


hf = sp.Function("h")          # abstract h (for structural identities)
LX, L1X = sp.symbols("Lx L1x")  # log x, log(1-x)

# exact parameters (sympy rationals)
def R_(fr):
    fr = Fr(fr)
    return sp.Rational(fr.numerator, fr.denominator)


M_S, W0_S, W4_S = R_(jc.M), R_(jc.W0), R_(jc.W4)
A_S, B_S, Z_S, SIG_S, XS_S = R_(jc.A_), R_(jc.B_), R_(jc.Z_), R_(jc.SIG), R_(jc.XS)
L_S, U_S, T_S = sp.Rational(1, 16), sp.Rational(15, 16), sp.Rational(1, 1000)
K0_S = M_S * W0_S


def nonneg_all(*vs):
    return [w >= 0 for w in vs]


# ============================================================ §3 Entropy reduction
@claim("R.1", "E_U Q_U(x) = x and E_U[Q_U(x)Q_U(y)] = xy + a b (min(x,y) - xy) = r(x,y), "
       "Q_U(x) = x + a(1[U<=x] - x)  (eq. Q, Qproduct)", "sympy-exact (piecewise integral over U)")
def check_R1():
    a_, b_, U = sp.symbols("a b U", real=True)
    X, Y = sp.symbols("X Y", positive=True)

    def Qx(xx, aa, ind):
        return xx + aa * (ind - xx)
    # E Q = int_0^x (x + a(1-x)) + int_x^1 (x - a x)
    EQ = sp.integrate(Qx(X, a_, 1), (U, 0, X)) + sp.integrate(Qx(X, a_, 0), (U, X, 1))
    assert sp.expand(EQ - X) == 0
    # x <= y:  U <= x: both indicators 1;  x < U <= y: only y;  U > y: none
    E2 = (sp.integrate(Qx(X, a_, 1) * Qx(Y, b_, 1), (U, 0, X))
          + sp.integrate(Qx(X, a_, 0) * Qx(Y, b_, 1), (U, X, Y))
          + sp.integrate(Qx(X, a_, 0) * Qx(Y, b_, 0), (U, Y, 1)))
    assert sp.expand(E2 - (X * Y + a_ * b_ * (X - X * Y))) == 0
    # y <= x: symmetric
    E3 = (sp.integrate(Qx(X, a_, 1) * Qx(Y, b_, 1), (U, 0, Y))
          + sp.integrate(Qx(X, a_, 1) * Qx(Y, b_, 0), (U, Y, X))
          + sp.integrate(Qx(X, a_, 0) * Qx(Y, b_, 0), (U, X, 1)))
    assert sp.expand(E3 - (X * Y + a_ * b_ * (Y - X * Y))) == 0


@claim("R.2", "0 <= a,b <= 1 and 0 <= x,y <= 1 give Q_U(x) in [0,1] (both indicator values) and "
       "xy <= r <= min(x,y), 0 <= r <= 1", "z3")
def check_R2():
    X, Y, A, B, Ind = z3.Reals("x y a b ind")
    box = [X >= 0, X <= 1, Y >= 0, Y <= 1, A >= 0, A <= 1, B >= 0, B <= 1]
    Qv = X + A * (Ind - X)
    z3_valid(box + [z3.Or(Ind == 0, Ind == 1)], z3.And(Qv >= 0, Qv <= 1), None)
    Mn = z3.If(X <= Y, X, Y)
    r = X * Y + A * B * (Mn - X * Y)
    z3_valid(box, z3.And(X * Y <= r, r <= Mn, r >= 0, r <= 1), None)


@claim("R.3", "finite forms of the two averaging steps: (i) E[psi(S)psi(T)] = sum_v l_v c_v^2 >= "
       "(sum_v l_v c_v)^2 for S,T cond. iid given V (variance identity, eq. conditional-jensen); "
       "(ii) integrating x h(y) + y h(x) against P x P gives 2 (E x)(E h)", "sympy-exact")
def check_R3():
    l1, l2, c1, c2, c3 = sp.symbols("l1 l2 c1 c2 c3", real=True)
    l3 = 1 - l1 - l2
    cb = l1 * c1 + l2 * c2 + l3 * c3
    lhs = l1 * c1**2 + l2 * c2**2 + l3 * c3**2 - cb**2
    rhs = l1 * (c1 - cb)**2 + l2 * (c2 - cb)**2 + l3 * (c3 - cb)**2
    assert sp.expand(lhs - rhs) == 0
    ps = sp.symbols("p1 p2 p3", real=True)
    xs = sp.symbols("x1 x2 x3", real=True)
    hh = sp.symbols("h1 h2 h3", real=True)
    pp = [ps[0], ps[1], 1 - ps[0] - ps[1]]
    tot = sum(pp[i] * pp[j] * (xs[i] * hh[j] + xs[j] * hh[i]) for i in range(3) for j in range(3))
    assert sp.expand(tot - 2 * sum(pp[i] * xs[i] for i in range(3)) * sum(pp[i] * hh[i] for i in range(3))) == 0


def reduction_skeleton(n=3, p_is_max=True):
    """Prop. 'Entropy reduction', last paragraph, with n coordinates: per-coordinate
    inequalities + chain rule + max entropy => p >= 1 - m."""
    Hs_ = z3.Reals(" ".join(f"H{i}" for i in range(n)))
    Z0 = z3.Reals(" ".join(f"Z0_{i}" for i in range(n)))
    Z4 = z3.Reals(" ".join(f"Z4_{i}" for i in range(n)))
    I0 = z3.Reals(" ".join(f"I0_{i}" for i in range(n)))
    Ps = z3.Reals(" ".join(f"Psi_{i}" for i in range(n)))
    pi = z3.Reals(" ".join(f"p{i}" for i in range(n)))
    P, Ln, W0, W4, Mz = z3.Reals("p lnN w0 w4 m")
    hy = [Ln > 0, W0 >= 0, W4 >= 0, W0 + W4 == 1, Mz > 0, sum(Hs_) == Ln]   # H(X) = ln N (chain rule)
    for i in range(n):
        hy += [Hs_[i] >= 0, pi[i] >= 0, pi[i] <= 1,
               (pi[i] <= P) if p_is_max else (P <= pi[i]),
               Z0[i] >= I0[i],                               # (ind-lower)
               Z4[i] >= Ps[i],                               # (rule4-lower)
               Mz * (W0 * I0[i] + W4 * Ps[i]) >= (1 - pi[i]) * Hs_[i]]   # (M) integrated, / 2
    hy += [sum(Z0) <= Ln, sum(Z4) <= Ln]                     # chain rule + H(Z) <= ln N
    return hy, P >= 1 - Mz


@claim("R.4", "assembly of Prop. 'Entropy reduction': per-coordinate bounds (ind-lower), (rule4-lower), "
       "(M) integrated, chain rule, H(Z_0), H(Z_4) <= ln N = H(X) > 0, p = max p_i  =>  p >= 1-m "
       "(3 coordinates; the argument is coordinatewise-linear)", "z3")
def check_R4():
    hy, goal = reduction_skeleton()
    z3_valid(hy, goal, None)


# ============================================================ §4 ceiling (not on the proof path)
@claim("C.1", "ceiling: f = q h(q) - h(q^2)/2 has f' = -(1-q)ln(1-q) - q ln(1+q), "
       "f'' = ln((1-q)/(1+q)) + 1/(1+q), f''' = -2/(1-q^2) - 1/(1+q)^2, "
       "f = (1-q)^2 ln(1-q)/2 + (1-q^2) ln(1+q)/2, f(q*) = (1-q*) ln(1+q*)/2 at the stationary point, "
       "f'(1/2) = ln(4/3)/2, f''(1/2) = 2/3 - ln 3", "sympy-exact")
def check_C1():
    Lq, Lm, Lp = sp.symbols("Lq Lm Lp")
    bases = {q: Lq, 1 - q: Lm, 1 + q: Lp}
    f = q * hs(q) - hs(q**2) / 2
    f1 = -(1 - q) * sp.log(1 - q) - q * sp.log(1 + q)
    f2 = sp.log((1 - q) / (1 + q)) + 1 / (1 + q)
    f3 = -2 / (1 - q**2) - 1 / (1 + q)**2
    assert zero_logs(sp.diff(f, q) - f1, bases)
    assert zero_logs(sp.diff(f, q, 2) - f2, bases)
    assert zero_logs(sp.diff(f, q, 3) - f3, bases)
    assert zero_logs(f - ((1 - q)**2 * sp.log(1 - q) / 2 + (1 - q**2) * sp.log(1 + q) / 2), bases)
    # at the stationary point (1-q)Lm = -q Lp, i.e. Lm = -q Lp/(1-q)
    fs = logsub((1 - q)**2 * sp.log(1 - q) / 2 + (1 - q**2) * sp.log(1 + q) / 2, bases)
    assert sp.cancel(fs.subs(Lm, -q * Lp / (1 - q)) - (1 - q) * Lp / 2) == 0
    e = logsub(f1.subs(q, sp.Rational(1, 2)) - sp.log(sp.Rational(4, 3)) / 2, {})
    assert sp.expand(e) == 0
    e = logsub(f2.subs(q, sp.Rational(1, 2)) - (sp.Rational(2, 3) - sp.log(3)), {})
    assert sp.expand(e) == 0


@claim("C.2", "ceiling chain: psi(1) = 0, (M) at y = 1 => m w0 >= 1/2 (E); (M) at x = y = q with "
       "psi(q)^2 <= K(q,q) <= ln 2 => (C);  f'(q) > q(1-2q) on (0,1/2] from -ln(1-q) > q, ln(1+q) < q",
       "z3 (+ hand: the two log bounds)")
def check_C2():
    Mz, W0, W4, hx, psx, ps1, l2, hq, hq2, psq, Kqq, qq = z3.Reals("m w0 w4 hx psx ps1 l2 hq hq2 psq Kqq q")
    base = [Mz > 0, W0 >= 0, W4 >= 0, W0 + W4 == 1, l2 > 0]
    # endpoint: K(1,1) = 0 >= psi(1)^2 => psi(1) = 0;  (M) at (x,1): 2m[w0 h(x) + w4 psi(x)psi(1)] >= h(x)
    z3_valid(base + [hx > 0, ps1 * ps1 <= 0, 2 * Mz * (W0 * hx + W4 * psx * ps1) >= hx], 2 * Mz * W0 >= 1, None)
    # diagonal
    z3_valid(base + [2 * Mz * W0 >= 1, qq > 0, qq < 1, hq2 >= 0, hq2 <= l2, psq * psq <= Kqq, Kqq <= l2,
                     2 * Mz * (W0 * hq2 + W4 * psq * psq) >= 2 * qq * hq],
             1 - Mz <= Fr(1, 2) - (qq * hq - hq2 / 2) / l2, None)
    La1, Lb1 = z3.Reals("A1 B1")       # A1 = -ln(1-q) > q,  B1 = ln(1+q) < q
    z3_valid([qq > 0, qq <= Fr(1, 2), La1 > qq, Lb1 < qq],
             (1 - qq) * La1 - qq * Lb1 > qq * (1 - 2 * qq), None)


# ============================================================ §5 profile definitions
@claim("P.1", "parameters and continuity: A = 179/250; 1/16 < 1/2 < z < 1/sqrt2 < A < B < 15/16 < 1; "
       "z^2 + z > 1; a(1/2) = 1, a(1/sqrt2) = 0, 0 <= a <= 1 on (1/2, 1/sqrt2); D continuous at 1/2 "
       "and z; theta(A) = 0, theta(B) = 1; E'' = -7/5 and E'(1) > 0 => E' > 0 on [0,1]",
       "exact + sympy-exact + z3 (+ interval/Arb for E'(1))")
def check_P1():
    assert jc.A_ == Fr(179, 250)
    assert L_S < sp.Rational(1, 2) < Z_S and 2 * Z_S**2 < 1 < 2 * A_S**2 and A_S < B_S < U_S < 1
    assert 2 * U_S**2 > 1 and Z_S**2 + Z_S > 1
    aa = sp.sqrt((1 - 2 * x**2) / (2 * x * (1 - x)))
    assert sp.simplify(aa.subs(x, sp.Rational(1, 2)) - 1) == 0
    assert sp.simplify(aa.subs(x, 1 / sp.sqrt(2))) == 0
    X = z3.Real("x")
    z3_valid([X > Fr(1, 2), 2 * X * X < 1],
             z3.And(1 - 2 * X * X > 0, 2 * X * (1 - X) > 0, 1 - 2 * X * X <= 2 * X * (1 - X)), None)
    # D: h(1/2) = ln 2 exactly; ln2 h(z^2)/h(z^2) = ln 2 (cancellation)
    assert sp.expand(logsub(hs(sp.Rational(1, 2)) - sp.log(2), {})) == 0
    th = (x - A_S) / (B_S - A_S)
    assert th.subs(x, A_S) == 0 and th.subs(x, B_S) == 1
    ks = sp.Symbol("ks")              # k* = h'(x*)/(2 h(x*)), a constant
    E = -ks * (x - XS_S) - sp.Rational(7, 10) * (x - XS_S)**2
    assert sp.diff(E, x, 2) == sp.Rational(-7, 5)
    Ep1 = sp.diff(E, x)
    X, KS = z3.Reals("x ks")
    Epz = -KS - Q(Fr(7, 5)) * (X - Q(jc.XS))
    # E'(1) > 0 is a scalar check; E' is affine decreasing, so E' > 0 on [0, 1]
    z3_valid([X >= 0, X <= 1, -KS - Q(Fr(7, 5)) * (1 - Q(jc.XS)) > 0], Epz > 0, None)
    assert sp.expand(Ep1 - (-ks - sp.Rational(7, 5) * (x - XS_S))) == 0


# ============================================================ §5.1 geometric concavity
@claim("G.1", "Lemma 'geometric': h - x h' = l := -ln(1-x); h^2 q' = h h' + x h h'' - x h'^2 = h' l - h/(1-x) "
       "= h'(l - x/(1-x)) - l/(1-x), q = x h'/h", "sympy-exact")
def check_G1():
    bases = {x: LX, 1 - x: L1X}
    h_ = hs(x)
    hp, hpp = sp.diff(h_, x), sp.diff(h_, x, 2)
    ell = -sp.log(1 - x)
    assert zero_logs(hp - sp.log((1 - x) / x), bases) and zero_logs(hpp + 1 / (x * (1 - x)), bases)
    assert zero_logs(h_ - x * hp - ell, bases)
    qf = x * hp / h_
    lhs = h_**2 * sp.diff(qf, x)
    assert zero_logs(lhs - (h_ * hp + x * h_ * hpp - x * hp**2), bases)
    assert zero_logs(lhs - (hp * ell - h_ / (1 - x)), bases)
    assert zero_logs(lhs - (hp * (ell - x / (1 - x)) - ell / (1 - x)), bases)


@claim("G.2", "q' < 0 on (0,1): l < x/(1-x) and l > 0 (f(0)=0, f' > 0), h' > 0 below 1/2 and <= 0 above; "
       "z3 sign skeleton for both cases", "sympy-exact + hand(MVT, monotone log) + z3")
def check_G2():
    bases = {x: LX, 1 - x: L1X}
    f = x / (1 - x) + sp.log(1 - x)
    assert f.subs(x, 0) == 0 and zero_logs(sp.diff(f, x) - x / (1 - x)**2, bases)
    g = -sp.log(1 - x)
    assert g.subs(x, 0) == 0 and zero_logs(sp.diff(g, x) - 1 / (1 - x), bases)
    X, Hp, Ell, Hh = z3.Reals("x hp l h")
    common = [X > 0, X < 1, Ell > 0, Hh > 0]
    N = Hp * Ell - Hh * (1 / (1 - X))
    z3_valid(common + [X >= Fr(1, 2), Hp <= 0], N < 0, None)
    # x < 1/2: substitute h = x h' + l
    z3_valid(common + [X < Fr(1, 2), Hp > 0, Ell < X / (1 - X), Hh == X * Hp + Ell], N < 0, None)


def q_numerator_crosscheck(lo_exp=10, hi_exp=30, n_per_octave=8):
    """Interval cross-check (not needed for the proof): N(x) = h'(x) l(x) - h(x)/(1-x) < 0 on
    [2^-lo_exp, 1 - 2^-hi_exp], cells geometric in x near 0 and in 1-x near 1, bisected on failure.
    (Below 2^-10 the naive enclosure loses the O(x^2) cancellation; the analytic proof G.2 does not care.)"""
    def N(X):
        return ilog((1.0 - X) / X) * (-ilog(1.0 - X)) - H(X) / (1.0 - X)

    def geo(k0, k1):
        out = []
        for k in range(k0, k1, -1):
            a0 = 2.0**-k
            out += [a0 * (1 + j / n_per_octave) for j in range(n_per_octave)]
        return out
    left = geo(lo_exp, 1)
    right = [1.0 - e for e in reversed(geo(hi_exp, 1))]
    edges = left + [0.5] + right[1:] + [1.0 - 2.0**-hi_exp]
    edges = sorted(set(edges))
    cells, worst = 0, -math.inf
    stack = list(zip(edges[:-1], edges[1:]))
    while stack:
        a0, b0 = stack.pop()
        val = N(I(a0, b0))
        if val.hi < 0:
            cells += 1
            worst = max(worst, val.hi)
            continue
        assert b0 - a0 > 1e-12, (a0, b0, val)
        m_ = 0.5 * (a0 + b0)
        stack += [(a0, m_), (m_, b0)]
    return cells, worst


@claim("G.3", "f(t) = ln h(e^t): f' = q(e^t), f'' = e^t q'(e^t); d/dx ln(h(xy)/s(x)) = (q(xy) - q(x^2))/x "
       "(h abstract); xy <= x^2 when 0 < y <= A <= x; cross-check h^2 q' < 0 on [2^-10, 1-2^-30] by intervals",
       "sympy-exact + z3 + hand(concavity at the midpoint) (+ interval cross-check)")
def check_G3():
    tt = sp.Symbol("tt", real=True)
    qf = lambda w: w * sp.Subs(sp.Derivative(hf(sp.Symbol("w_")), sp.Symbol("w_")), sp.Symbol("w_"), w).doit() / hf(w)
    f = sp.log(hf(sp.exp(tt)))
    f1 = sp.diff(f, tt)
    assert sp.simplify(f1 - qf(sp.exp(tt))) == 0
    W = sp.Symbol("W", positive=True)
    qW = W * sp.diff(hf(W), W) / hf(W)
    qprime = sp.diff(qW, W)
    assert sp.simplify(sp.diff(f, tt, 2) - (sp.exp(tt) * qprime).subs(W, sp.exp(tt))) == 0
    rat = sp.log(hf(x * y)) - sp.log(hf(x**2)) / 2
    target = (qW.subs(W, x * y) - qW.subs(W, x**2)) / x
    assert sp.simplify(sp.diff(rat, x) - target) == 0
    X, Y = z3.Reals("x y")
    z3_valid([Y > 0, Y <= Q(jc.A_), X >= Q(jc.A_), X < 1], X * Y <= X * X, None)
    cells, worst = q_numerator_crosscheck()
    assert cells > 0 and worst < 0


# ============================================================ §5.2 profile ordering
@claim("O.1", "for x >= z: (phi/s)^2 = sigma^2 ln2 h(x) e^{2E}/(h(z^2) h*); (ln(phi/s))' = h'/(2h) + E'; "
       "(h'/(2h) + E')' = (h''h - h'^2)/(2h^2) - 7/5 < 0 (h abstract; h'' < 0, h > 0)", "sympy-exact + z3")
def check_O1():
    hstar, hz2, sg, l2, ks = sp.symbols("hstar hz2 sigma l2 ks", positive=True)
    E = -ks * (x - XS_S) - sp.Rational(7, 10) * (x - XS_S)**2
    D = l2 * hf(x**2) / hz2
    phi2 = sg**2 * D * hf(x) / hstar * sp.exp(2 * E)
    s2 = hf(x**2)
    assert sp.simplify(phi2 / s2 - sg**2 * l2 * hf(x) * sp.exp(2 * E) / (hz2 * hstar)) == 0
    # ln(phi/s) = ln sigma + (1/2)(ln l2 + ln h(x) - ln hz2 - ln h*) + E
    lr = sp.log(sg) + (sp.log(l2) + sp.log(hf(x)) - sp.log(hz2) - sp.log(hstar)) / 2 + E
    d1 = sp.diff(lr, x)
    assert sp.simplify(d1 - (sp.diff(hf(x), x) / (2 * hf(x)) + sp.diff(E, x))) == 0
    d2 = sp.diff(d1, x)
    hp, hpp = sp.diff(hf(x), x), sp.diff(hf(x), x, 2)
    assert sp.simplify(d2 - ((hpp * hf(x) - hp**2) / (2 * hf(x)**2) - sp.Rational(7, 5))) == 0
    Hh, Hp, Hpp = z3.Reals("h hp hpp")
    z3_valid([Hh > 0, Hpp < 0], (Hpp * Hh - Hp * Hp) / (2 * Hh * Hh) - Q(Fr(7, 5)) < 0, None)


@claim("O.2", "profile order (eq. profile-order): L = ln(phi/s) has L(A) < 0 [s(A) > phi(A)], L'(A) < 0 "
       "[scalar], L'' < 0 [O.1] => L < 0 on [A,1) [hand: MVT twice]; then phi <= (1-th)phi + th s <= s for "
       "th in [0,1]; on [0,A] psi = phi; so phi <= psi <= s on [A,1] and psi >= phi >= 0 everywhere",
       "z3 + hand(MVT) + interval/Arb scalars")
def check_O2():
    Ph, S, Th = z3.Reals("phi s th")
    z3_valid([Ph >= 0, Ph <= S, Th >= 0, Th <= 1],
             z3.And(Ph <= (1 - Th) * Ph + Th * S, (1 - Th) * Ph + Th * S <= S, (1 - Th) * Ph + Th * S >= 0), None)
    ch, _ = jc.scalar_checks(verbose=False)
    assert ch["s(A) - phi(A)"].lo > 0 and ch["-(h'(A)/(2h(A)) + E'(A))"].lo > 0


# ============================================================ §5.3 passing to (K)
def passing_skeleton(case, with_bridge=True):
    K, hxy, sx, sy, sA, hAy, phx, phy, psx, psy = z3.Reals("K hxy sx sy sA hAy phx phy psx psy")
    hy = [sx > 0, sy > 0, sA > 0, phx >= 0, phy >= 0, psx >= 0, psy >= 0]
    if case == "low":       # x, y <= A: psi = phi, (original-K)
        hy += [psx == phx, psy == phy, K >= phx * phy]
    elif case == "high":    # x, y >= A: a = 0, K = h(xy) >= s(x)s(y) (Lemma geometric), psi <= s
        hy += [K == hxy, hxy >= sx * sy, psx <= sx, psy <= sy]
    else:                   # x >= A >= y: ratio monotone, bridge, psi(x) <= s(x), psi(y) = phi(y)
        hy += [K == hxy, hxy * sA >= hAy * sx, psx <= sx, psy == phy, hAy >= 0]
        if with_bridge:
            hy += [hAy >= sA * phy]
    return hy, K >= psx * psy


@claim("T.1", "Section 'Passing from the original to the stronger kernel bound': the three cases "
       "(x,y <= A; x,y >= A; x >= A >= y) give K >= psi(x)psi(y) from (original-K), Lemma 'geometric', "
       "(profile-order) and (bridge); a = 0 on [A,1] since 2A^2 > 1", "z3 + exact")
def check_T1():
    assert 2 * jc.A_**2 > 1
    for case in ("low", "high", "mixed"):
        hy, goal = passing_skeleton(case)
        z3_valid(hy, goal, None)


# ============================================================ §6 strips
@claim("S.1", "AND inequality h(x^2) <= 2h(x) (eq. and): 2h(x) - h(x^2) = (1-x^2) H3((1-x)/(1+x), x/(1+x), x/(1+x)) "
       "(grouping identity, logs as symbols), a nonnegative entropy; concavity-scaling h(cx) >= c h(x): "
       "g(c) = h(cx) - c h(x) has g(0) = g(1) = 0 and g'' = -x/(c(1-cx)) < 0",
       "sympy-exact + hand(entropy >= 0; concave with zero ends)")
def check_S1():
    Lp_ = sp.Symbol("L1px")
    bases = {x: LX, 1 - x: L1X, 1 + x: Lp_}
    pr = [(1 - x) / (1 + x), x / (1 + x), x / (1 + x)]
    H3 = -sum(pi_ * sp.log(pi_) for pi_ in pr)
    assert sp.simplify(sum(pr) - 1) == 0
    assert zero_logs(2 * hs(x) - hs(x**2) - (1 - x**2) * H3, bases)
    Lc = sp.Symbol("Lc")
    Lcx, L1cx = sp.symbols("Lcx L1cx")
    g = hs(c * x) - c * hs(x)
    g2 = sp.diff(g, c, 2)
    assert zero_logs(g2 + x / (c * (1 - c * x)), {c: Lc, x: LX, 1 - c * x: L1cx, 1 - x: L1X})
    assert sp.simplify(g.subs(c, 1)) == 0


@claim("S.2", "eq. lower-profile / P0 / linear-profile: (ln(phi/x))' = D'/(2D) + h'/(2h) + E' - 1/x; "
       "on [z,1/sqrt2] D'/(2D) = x h'(x^2)/h(x^2) <= h'(z^2)/h(z^2) ((h'/h)' < 0, 2z^2 < 1); "
       "with E'(x) <= E'(1/2), -1/x <= -1 and the scalar 1 - E'(1/2) - h'(z^2)/h(z^2) > 0 the derivative is < 0; "
       "phi <= C_b h on [0,L], phi <= P0 on [0,1/2], phi(y) <= 2 P0 y on [1/2,1]",
       "sympy-exact + z3 + hand(MVT, monotone exp)")
def check_S2():
    Df = sp.Function("D")
    hstar, sg, l2, hz2, ks = sp.symbols("hstar sigma l2 hz2 ks", positive=True)
    E = -ks * (x - XS_S) - sp.Rational(7, 10) * (x - XS_S)**2
    lr = sp.log(sg) + (sp.log(Df(x)) + sp.log(hf(x)) - sp.log(hstar)) / 2 + E - sp.log(x)
    tgt = sp.diff(Df(x), x) / (2 * Df(x)) + sp.diff(hf(x), x) / (2 * hf(x)) + sp.diff(E, x) - 1 / x
    assert sp.simplify(sp.diff(lr, x) - tgt) == 0
    D3 = l2 * hf(x**2) / hz2
    W = sp.Symbol("W", positive=True)
    assert sp.simplify(sp.diff(D3, x) / (2 * D3) - x * sp.diff(hf(W), W).subs(W, x**2) / hf(x**2)) == 0
    assert sp.simplify(sp.diff(sp.diff(hf(x), x) / hf(x), x)
                       - (sp.diff(hf(x), x, 2) * hf(x) - sp.diff(hf(x), x)**2) / hf(x)**2) == 0
    # z3: x h'(x^2)/h(x^2) <= h'(x^2)/h(x^2) <= h'(z^2)/h(z^2) on [z, 1/sqrt2]
    X, R2, Rz, T1, T2, Ep, Ep12, Rzz = z3.Reals("x r2 rz t1 t2 ep ep12 rzz")
    z3_valid([X > 0, X <= 1, R2 >= 0, R2 <= Rz], X * R2 <= Rz, None)
    # the first term is 0 on [1/2, z] and <= 0 above 1/sqrt2; Rz = h'(z^2)/h(z^2) > 0 since 2z^2 < 1
    z3_valid([T1 == 0, Rz > 0], T1 <= Rz, None)
    z3_valid([T1 <= 0, Rz > 0], T1 <= Rz, None)
    # derivative < 0 on each piece: T1 <= Rz (all three pieces), T2 <= 0, E' <= E'(1/2), x >= 1/2
    z3_valid([T1 <= Rz, T2 <= 0, Ep <= Ep12, X >= Fr(1, 2), X <= 1, 1 - Ep12 - Rz > 0],
             T1 + T2 + Ep - 1 / X < 0, None)
    ch, _ = jc.scalar_checks(verbose=False)
    assert ch["1 - E'(1/2) - h'(z^2)/h(z^2)"].lo > 0
    # lower-profile: phi = sigma h e^E/sqrt(h*) <= C_b h  (E(x) <= E(L), x <= L);  P0: h <= ln2, E <= E(1/2)
    Hh, eE, eL, sq, Phi, ln2, eH = z3.Reals("h eE eL sq phi ln2 eH")
    z3_valid([Hh >= 0, eE > 0, eE <= eL, sq > 0, Phi == Q(jc.SIG) * Hh * eE / sq],
             Phi <= (Q(jc.SIG) / sq * eL) * Hh, None)
    z3_valid([Hh >= 0, Hh <= ln2, eE > 0, eE <= eH, sq > 0, Phi == Q(jc.SIG) * Hh * eE / sq],
             Phi <= Q(jc.SIG) * ln2 / sq * eH, None)
    # linear-profile: phi(y)/y <= phi(1/2)/(1/2) <= 2 P0
    Py, Yv, Ph12, P0 = z3.Reals("py y ph12 P0")
    z3_valid([Yv >= Fr(1, 2), Py / Yv <= 2 * Ph12, Ph12 <= P0, Py >= 0], Py <= 2 * P0 * Yv, None)


def lower_strip_skeleton(case, bound_2CbP0=Fr(1)):
    K, hx, phx, phy, Cb, P0, X, Y, k, hxk = z3.Reals("K hx phx phy Cb P0 x y k hxk")
    hy = [hx >= 0, phx >= 0, phy >= 0, Cb > 0, P0 > 0, X >= 0, X <= Y, Y <= 1,
          phx <= Cb * hx, 2 * Cb * P0 < Q(bound_2CbP0)]
    if case == "y<=1/2":         # r = x, phi(y) <= P0
        hy += [Y <= Fr(1, 2), K == hx, phy <= P0]
    else:                         # r = x k, k in [y,1], h(xk) >= k h(x), phi(y) <= 2 P0 y
        hy += [Y >= Fr(1, 2), k >= Y, k <= 1, K == hxk, hxk >= k * hx, phy <= 2 * P0 * Y]
    return hy, K >= phx * phy


@claim("S.3", "lower strip (x <= L, x <= y): a(x) = 1; if y <= 1/2 then r = x; else r = x k, "
       "k = y + a(y)(1-y) in [y,1]; with (lower-profile), (P0), (linear-profile), (concavity-scaling) and "
       "2 C_b P0 < 1: K >= phi(x)phi(y)", "sympy-exact + z3 + interval/Arb scalar")
def check_S3():
    a_, b_ = sp.symbols("a b", positive=True)
    X, Y = sp.symbols("X Y", positive=True)
    r = X * Y + a_ * b_ * (X - X * Y)              # x <= y
    assert sp.expand(r.subs({a_: 1, b_: 1}) - X) == 0
    assert sp.expand(r.subs(a_, 1) - X * (Y + b_ * (1 - Y))) == 0
    Yz, Bz, kz = z3.Reals("y b k")
    z3_valid([Yz >= 0, Yz <= 1, Bz >= 0, Bz <= 1, kz == Yz + Bz * (1 - Yz)], z3.And(kz >= Yz, kz <= 1), None)
    for case in ("y<=1/2", "y>=1/2"):
        hy, goal = lower_strip_skeleton(case)
        z3_valid(hy, goal, None)
    ch, _ = jc.scalar_checks(verbose=False)
    assert ch["1 - 2 C_b P0"].lo > 0


def upper_strip_checks(ctgc_bound=Fr(1)):
    """(upper-linear), D/h <= 2 ln2/h(z^2) (three pieces), phi <= C_g h, and the chain."""
    Phx, X, Uu, hx, hU, hx2, hU2, eE, e1, sg, l2, hz2, hst, Ct = z3.Reals(
        "phx x U hx hU hx2 hU2 eE e1 sg l2 hz2 hst Ct")
    pos = [sg > 0, l2 > 0, hz2 > 0, hst > 0, eE > 0, hx >= 0, hx2 >= 0, Phx >= 0]
    # phi(x)^2 = sg^2 l2 h(x^2) h(x) e^{2E}/(hz2 hst);  C_t^2 = sg^2 l2 h(U^2) h(U) e1^2/(U^2 hz2 hst)
    z3_valid(pos + [X >= Uu, Uu > 0, hx <= hU, hx2 <= hU2, eE <= e1, Ct >= 0,
                    Phx * Phx == sg * sg * l2 * hx2 * hx * eE * eE / (hz2 * hst),
                    Ct * Ct == sg * sg * l2 * hU2 * hU * e1 * e1 / (Uu * Uu * hz2 * hst)],
             Phx <= Ct * X, None)
    Dy, hy_, hz, hy2, Yv = z3.Reals("Dy hy hz hy2 y")
    tgt = Dy <= 2 * l2 / hz2 * hy_
    z3_valid([hy_ > 0, l2 > 0, hz2 > 0, hz2 <= l2, Dy == hy_], tgt, None)                         # y <= 1/2
    z3_valid([hy_ > 0, l2 > 0, hz2 > 0, hy_ >= hz, hz2 <= 2 * hz, Dy == l2], tgt, None)          # 1/2 <= y <= z
    z3_valid([hy_ > 0, l2 > 0, hz2 > 0, hy2 <= 2 * hy_, Dy == l2 * hy2 / hz2], tgt, None)        # y >= z
    Phy, Cg = z3.Reals("phy Cg")
    z3_valid([hy_ >= 0, Dy >= 0, Dy <= 2 * l2 / hz2 * hy_, sg > 0, l2 > 0, hz2 > 0, hst > 0, eE > 0, eE <= e1,
              Phy >= 0, Phy * Phy == sg * sg * Dy * hy_ * eE * eE / hst, Cg >= 0,
              Cg * Cg == sg * sg * 2 * l2 / (hst * hz2) * e1 * e1],
             Phy <= Cg * hy_, None)
    K, hxy = z3.Reals("K hxy")
    return [Phx >= 0, Phy >= 0, X >= 0, X <= 1, hy_ >= 0, Ct >= 0, Cg >= 0, Phx <= Ct * X, Phy <= Cg * hy_,
            Ct * Cg < Q(ctgc_bound), K == hxy, hxy >= X * hy_], K >= Phx * Phy


@claim("S.4", "upper strip (x >= U, any y): a(x) = 0, 2U^2 > 1 so h(x), h(x^2) decrease; phi(x) <= C_t x; "
       "D(y)/h(y) <= 2 ln2/h(z^2) on the three pieces (uses h(z^2) <= ln2, h(z^2) <= 2h(z), h(y^2) <= 2h(y)); "
       "phi(y) <= C_g h(y); C_t C_g < 1 and h(xy) >= x h(y) give K >= phi(x)phi(y)",
       "z3 + exact + interval/Arb scalar")
def check_S4():
    assert 2 * Fr(15, 16)**2 > 1
    hy, goal = upper_strip_checks()
    z3_valid(hy, goal, None)
    ch, _ = jc.scalar_checks(verbose=False)
    assert ch["1 - C_g C_t"].lo > 0


@claim("S.5", "middle coordinate map x(t) = 1/(t^2 + R), R = sqrt((t^2-1)^2+1): solves x^2 + t^2 x(1-x) = 1/2, "
       "so a(x(t)) = t; x(0) = 1/sqrt2, x(1) = 1/2; x'(t) = -(2t/d^2)(1 + (t^2-1)/R) (eq. coordinate-derivative); "
       "every positive root with t in [0,1] lies in [1/2, 1/sqrt2]; |x'| <= 4; the three maps cover "
       "[1/16, 15/16] (IVT)", "sympy-exact + z3 + hand(IVT)")
def check_S5():
    Rs = sp.Symbol("R", positive=True)
    rel = Rs**2 - ((t**2 - 1)**2 + 1)
    X = 1 / (t**2 + Rs)
    num = sp.numer(sp.together(X**2 + t**2 * X * (1 - X) - sp.Rational(1, 2)))
    assert sp.reduced(sp.expand(num), [rel], Rs, t)[1] == 0
    Rt = sp.sqrt((t**2 - 1)**2 + 1)
    Xt = 1 / (t**2 + Rt)
    assert sp.simplify(Xt.subs(t, 0) - 1 / sp.sqrt(2)) == 0 and sp.simplify(Xt.subs(t, 1) - sp.Rational(1, 2)) == 0
    d = t**2 + Rt
    assert sp.simplify(sp.diff(Xt, t) - (-(2 * t) / d**2 * (1 + (t**2 - 1) / Rt))) == 0
    # (1 - 2x^2)/(2x(1-x)) = t^2 on the curve:
    num2 = sp.numer(sp.together((1 - 2 * X**2) - t**2 * 2 * X * (1 - X)))
    assert sp.reduced(sp.expand(num2), [rel], Rs, t)[1] == 0
    Xz, Tz, Rz = z3.Reals("x t R")
    z3_valid([Tz >= 0, Tz <= 1, Xz > 0, Xz * Xz + Tz * Tz * Xz * (1 - Xz) == Fr(1, 2)],
             z3.And(Xz >= Fr(1, 2), 2 * Xz * Xz <= 1), None)
    z3_valid([Tz >= 0, Tz <= 1, Rz >= 1, Rz * Rz == (Tz * Tz - 1) ** 2 + 1],
             z3.And(Tz * Tz + Rz >= 1, 2 * Tz * (1 + z3.If(Tz * Tz - 1 >= 0, Tz * Tz - 1, 1 - Tz * Tz) / Rz) <= 4), None)


@claim("S.6", "bridge on [0, L]: h(Ay) >= A h(y) and phi(y) <= C_b h(y) give h(Ay) - s(A)phi(y) >= (A - s(A)C_b)h(y) >= 0; "
       "kernel range: xy <= r <= min(x,y) so 1/256 <= r <= 15/16 on the compact square", "z3 + interval/Arb scalar")
def check_S6():
    hAy, hy_, sA, phy, Cb, Av = z3.Reals("hAy hy sA phy Cb A")
    z3_valid([hy_ >= 0, sA > 0, Cb > 0, hAy >= Av * hy_, phy <= Cb * hy_, Av - sA * Cb > 0],
             z3.And(hAy - sA * phy >= (Av - sA * Cb) * hy_, hAy - sA * phy >= 0), None)
    X, Y, A, B = z3.Reals("x y a b")
    Mn = z3.If(X <= Y, X, Y)
    r = X * Y + A * B * (Mn - X * Y)
    z3_valid([X >= Fr(1, 16), X <= Fr(15, 16), Y >= Fr(1, 16), Y <= Fr(15, 16), A >= 0, A <= 1, B >= 0, B <= 1],
             z3.And(r >= Fr(1, 256), r <= Fr(15, 16)), None)
    ch, _ = jc.scalar_checks(verbose=False)
    assert ch["A - s(A) C_b"].lo > 0


# ============================================================ §7 mixture
@claim("M.1", "change of variables: t = -ln(xy)/2, xi = ln(y/x)/(-ln(xy)) give u = t(1+xi) = -ln x, v = -ln y, "
       "and 0 < x <= y, xy < 1 give t > 0, 0 <= xi <= 1; (M)/(2xy) is exactly F; both sides of (M) vanish "
       "when xy = 0 or x = y = 1 (h(0) = h(1) = 0, psi(0) = psi(1) = 0)", "sympy-exact + z3")
def check_M1():
    Lx, Ly = sp.symbols("Lx Ly", real=True)
    tt = -(Lx + Ly) / 2
    xx = (Ly - Lx) / (-(Lx + Ly))
    assert sp.cancel(tt * (1 + xx) + Lx) == 0 and sp.cancel(tt * (1 - xx) + Ly) == 0
    Lxz, Lyz = z3.Reals("Lx Ly")
    tz = -(Lxz + Lyz) / 2
    z3_valid([Lxz <= Lyz, Lyz <= 0, Lxz + Lyz < 0],
             z3.And(tz > 0, (Lyz - Lxz) >= 0, (Lyz - Lxz) <= -(Lxz + Lyz)), None)
    psf = sp.Function("psi")
    X, Y = sp.symbols("X Y", positive=True)
    Mexpr = 2 * M_S * (W0_S * hf(X * Y) + W4_S * psf(X) * psf(Y)) - (X * hf(Y) + Y * hf(X))
    G = lambda w: hf(w) / w            # G(-ln w)
    P = lambda w: psf(w) / w
    F = K0_S * G(X * Y) + M_S * W4_S * P(X) * P(Y) - (G(X) + G(Y)) / 2
    assert sp.simplify(Mexpr / (2 * X * Y) - F) == 0
    assert sp.limit(hs(x), x, 0, "+") == 0 and sp.limit(hs(x), x, 1, "-") == 0
    # boundary: x = 0 or x = y = 1 with h(0) = h(1) = 0, psi(0) = psi(1) = 0
    for sub in ({X: 0}, {X: 1, Y: 1}):
        e = Mexpr.subs(sub).subs({hf(0): 0, hf(1): 0, psf(0): 0, psf(1): 0})
        assert sp.simplify(e) == 0


@claim("M.2", "G facts (eq. Gseries, Gproperties): G = u - (e^u-1)ln(1-e^-u) = u + 1 - sum e^{-ju}/(j(j+1)), "
       "G' = 1 + sum e^{-ju}/(j+1) = -ln(1-e^-u)/e^-u, G'' = -sum j e^{-ju}/(j+1); sum 1/(j(j+1)) = 1; "
       "G' > 0, G'' < 0, G >= u, -G'' <= 1/(e^u-1) <= 1/u (reuses analytic_glue G.1, G.2)",
       "sympy-exact + hand(MVT, e^u >= 1+u) + z3")
def check_M2():
    ag.check_G_derivs()
    ag.check_G_signs()
    j = sp.symbols("j", integer=True, positive=True)
    bases = {x: LX, 1 - x: L1X}

    def ssum(term):
        s_ = sp.piecewise_fold(sp.summation(term, (j, 1, sp.oo)))
        if isinstance(s_, sp.Piecewise):
            s_ = s_.args[0][0]
        return s_
    assert sp.summation(1 / (j * (j + 1)), (j, 1, sp.oo)) == 1
    S1 = ssum(x**j / (j + 1))
    assert zero_logs(1 + S1 - (-sp.log(1 - x) / x), bases)            # G' = S(x)
    S2 = ssum(j * x**j / (j + 1))
    S = -sp.log(1 - x) / x
    assert zero_logs(-S2 - (S - 1 / (1 - x)), bases)                  # G'' = S - 1/(1-x)
    # G closed form in u: x = e^-u, G = -ln x - (1/x - 1) ln(1-x)
    assert zero_logs(hs(x) / x - (-sp.log(x) - (1 / x - 1) * sp.log(1 - x)), bases)
    Uz, Eu, G2 = z3.Reals("u eu g2")
    z3_valid([Uz > 0, Eu >= 1 + Uz, -G2 <= 1 / (Eu - 1)], -G2 <= 1 / Uz, None)


@claim("M.3", "eq. Gsmall: J = G + u ln u has J'' = G'' + 1/u >= 0 and J(u)/u -> 1 (u -> 0+); convexity with J(0) = 0 "
       "gives J(u)/u nondecreasing, so G(u) >= u(1 - ln u); interval cross-check on [2^-8, 64]",
       "sympy-exact (limit) + z3 + hand(chord slopes of a convex function) (+ interval cross-check)")
def check_M3():
    J = (u - (sp.exp(u) - 1) * sp.log(1 - sp.exp(-u)) + u * sp.log(u))
    assert sp.limit(J / u, u, 0, "+") == 1
    assert sp.limit(u * sp.log(u), u, 0, "+") == 0
    G2, Uz = z3.Reals("g2 u")
    z3_valid([Uz > 0, -G2 <= 1 / Uz], G2 + 1 / Uz >= 0, None)
    n, worst = gsmall_crosscheck()
    assert n > 0 and worst > 0


def gsmall_crosscheck(lo=2.0**-8, hi=64.0):
    """G(u) - u(1 - ln u) > 0 on [lo, hi] (cross-check only): on a cell, G increasing => G >= G(a); u(1 - ln u)
    is increasing on (0,1] and decreasing on [1, oo), so its max on a cell is at the endpoint nearer to 1.
    Cells are bisected on failure.  Near 0 the gap is only ~u^2|ln u|/2, so the range starts at 2^-8."""
    from costa_sadhu_thm12 import G_val
    stack = [(lo * 2.0**k, min(hi, lo * 2.0**(k + 1))) for k in range(64) if lo * 2.0**k < hi]
    cells, worst = 0, math.inf
    while stack:
        a0, b0 = stack.pop()
        pt = 1.0 if a0 < 1.0 < b0 else (b0 if b0 <= 1.0 else a0)
        P_ = I(pt)
        val = G_val(I(a0)) - P_ * (1.0 - ilog(P_))
        if val.lo > 0:
            cells += 1
            worst = min(worst, val.lo)
            continue
        assert b0 - a0 > 1e-9 * b0, (a0, b0, val)
        m_ = 0.5 * (a0 + b0)
        stack += [(a0, m_), (m_, b0)]
    return cells, worst


@claim("M.4", "eq. Gdeficit: G(u)+G(v)-G(u+v) = [J(u)+J(v)-J(u+v)] + (u+v) h(u/(u+v)), the bracket <= 0 by "
       "J(w) <= w/(u+v) J(u+v); h(p) <= ln(1 + 2 sqrt(p(1-p))) <= 2 sqrt(p(1-p)) [(sqrt p + sqrt(1-p))^2 = "
       "1 + 2 sqrt(p(1-p)), Jensen]; (u+v) 2 sqrt(p(1-p)) = 2 sqrt(uv)",
       "sympy-exact + z3 + hand(Jensen, ln(1+r) <= r) (+ interval cross-check of h <= 2 sqrt(p(1-p)))")
def check_M4():
    Lu, Lv, Luv = sp.symbols("Lu Lv Luv")
    bases = {u: Lu, v: Lv, u + v: Luv}
    Gs_ = sp.Function("G")
    J = lambda w: Gs_(w) + w * sp.log(w)
    lhs = Gs_(u) + Gs_(v) - Gs_(u + v)
    rhs = (J(u) + J(v) - J(u + v)) + (u + v) * hs(u / (u + v))
    assert zero_logs(lhs - rhs, bases)
    Ju, Jv, Juv, Uz, Vz = z3.Reals("Ju Jv Juv u v")
    z3_valid([Uz > 0, Vz > 0, Ju <= Uz / (Uz + Vz) * Juv, Jv <= Vz / (Uz + Vz) * Juv], Ju + Jv - Juv <= 0, None)
    pp = sp.Symbol("pp", positive=True)
    assert sp.simplify(sp.expand((sp.sqrt(pp) + sp.sqrt(1 - pp))**2) - (1 + 2 * sp.sqrt(pp * (1 - pp)))) == 0
    e = (u + v) * 2 * sp.sqrt((u / (u + v)) * (1 - u / (u + v))) - 2 * sp.sqrt(u * v)
    assert sp.simplify(e) == 0
    # Jensen form: h(p)/2 = p ln(1/sqrt p) + (1-p) ln(1/sqrt(1-p))
    Lpp, L1pp = sp.symbols("Lpp L1pp")
    jen = pp * sp.log(1 / sp.sqrt(pp)) + (1 - pp) * sp.log(1 / sp.sqrt(1 - pp))
    jen = sp.expand_log(jen, force=True)
    assert zero_logs(hs(pp) / 2 - jen, {pp: Lpp, 1 - pp: L1pp})
    gap = ag.h_sqrt_interval_crosscheck(n=1024)
    assert gap > 0


@claim("M.5", "eq. Ptail: on x >= B, P(u)^2 = G(2u) (psi = s); P(u) >= C G(u) since D >= h [z^2 + z > 1 => "
       "1 - x <= x^2 <= x for x >= z, h >= h(x) on [1-x, x]; ln2 >= h(z^2)], E increasing, psi >= phi",
       "sympy-exact + z3 + exact + hand(concavity/symmetry of h, h <= ln2)")
def check_M5():
    W = sp.Symbol("W", positive=True)
    s_ = sp.sqrt(hf(W**2))
    P = s_ / W
    G2u = hf(W**2) / W**2         # G(2u) with W = e^-u
    assert sp.simplify(P**2 - G2u) == 0
    assert Z_S**2 + Z_S > 1
    Xz = z3.Real("x")
    z3_valid([Xz >= Q(jc.Z_), Xz <= 1], z3.And(1 - Xz <= Xz * Xz, Xz * Xz <= Xz), None)
    Dx, hx, hx2, l2, hz2, Phx, sg, hst, eE, e0, C = z3.Reals("Dx hx hx2 l2 hz2 phx sg hst eE e0 C")
    tgt = Dx >= hx
    z3_valid([hx >= 0, Dx == hx], tgt, None)
    z3_valid([hx <= l2, Dx == l2], tgt, None)
    z3_valid([hx2 >= hx, hx >= 0, l2 >= hz2, hz2 > 0, Dx == l2 * hx2 / hz2], tgt, None)
    z3_valid([Dx >= hx, hx >= 0, sg > 0, hst > 0, eE >= e0, e0 > 0, Phx >= 0, C > 0,
              Phx * Phx == sg * sg * Dx * hx * eE * eE / hst, C * C == sg * sg * e0 * e0 / hst],
             Phx >= C * hx, None)
    # P = psi(x)/x >= phi(x)/x >= C h(x)/x = C G
    Ps, Ph, Gv, Xv = z3.Reals("ps ph g xv")
    z3_valid([Xv > 0, Ps >= Ph, Ph >= C * hx, Gv == hx / Xv, C > 0], Ps / Xv >= C * Gv, None)


def small_t_skeleton(with_bracket=True):
    Tt, Uz, Vz, G2t, Gu, Gv, G2u, G2v, Pu, Pv, R, cc, k0, mw4 = z3.Reals(
        "t u v G2t Gu Gv G2u G2v Pu Pv R c k0 mw4")
    hy = [Uz >= 0, Vz >= 0, Uz + Vz == 2 * Tt, R >= 0, R * R == Uz * Vz, G2t >= 0,
          Gu + Gv <= G2t + 2 * R,                       # (Gdeficit)
          G2u >= 2 * Uz * cc, G2v >= 2 * Vz * cc, cc > 0,  # (Gsmall) + 2u, 2v <= 4T
          Pu >= 0, Pv >= 0, Pu * Pu == G2u, Pv * Pv == G2v,   # (Ptail)
          k0 > Fr(1, 2), mw4 > 0]
    if with_bracket:
        hy.append(2 * mw4 * cc - 1 > 0)
    else:
        hy.append(2 * mw4 * cc - 1 <= 0)
    F = k0 * G2t + mw4 * Pu * Pv - (Gu + Gv) / 2
    return hy, F >= (k0 - Fr(1, 2)) * G2t


@claim("M.6", "small t <= T = 1/1000 (eq. smallt): u, v <= 2T and e^{-2T} > B so psi = s; with (Gdeficit), "
       "(Gsmall), (Ptail): F >= (k0-1/2)G(2t) + [2 m w4 (1 - ln 4T) - 1] sqrt(uv) >= (k0-1/2)G(2t); the two "
       "scalars are proved EXACTLY: e^{-1/500} >= 1 - 1/500 > 721/1000, and ln 250 > 4 (e < 2.72) gives "
       "2 m w4 (1 + ln 250) - 1 > 10 m w4 - 1 > 0", "z3 + exact + hand(e^-x >= 1-x, Taylor tail of e, monotone log)")
def check_M6():
    hy, goal = small_t_skeleton()
    z3_valid(hy, goal, None)
    assert 1 - Fr(1, 500) > jc.B_
    e_hi = sum(Fr(1, math.factorial(k)) for k in range(0, 12)) + Fr(2, math.factorial(12))
    assert e_hi < Fr(272, 100) and Fr(272, 100)**4 < 250              # e^4 < 250, ln 250 > 4
    assert 2 * jc.M * jc.W4 * (1 + 4) - 1 > 0
    assert 4 * jc.TMIN == Fr(1, 250)
    if flint is not None:
        flint.ctx.prec = 200
        assert flint.arb(e_hi.numerator) / e_hi.denominator > flint.arb(1).exp()
        assert flint.arb(250).log() > 4


def large_t_skeleton(tmin=16):
    Tt, Uz, Vz, G2t, Gu, Gv, Pu, Pv, C, k0, mw4 = z3.Reals("t u v G2t Gu Gv Pu Pv C k0 mw4")
    hy = [Tt >= tmin, Uz >= Tt, 2 * Tt >= Uz, Vz >= 0, G2t >= Gu, Gu >= Uz, Gv >= 0, C > 0,
          Pu >= C * Gu, Pv >= C * Gv, k0 > Fr(1, 2), mw4 > 0,
          16 * mw4 * C * C - Fr(1, 2) > 0, mw4 * C * C <= Fr(1, 25)]   # scalar + its true size (< 0.04)
    F = k0 * G2t + mw4 * Pu * Pv - (Gu + Gv) / 2
    return hy, F >= 0


@claim("M.7", "large t >= 16 (eq. larget): u >= t, 2t >= u, G increasing, G(u) >= u >= 16, P >= C G give "
       "F >= (k0-1/2)G(u) + [m w4 C^2 G(u) - 1/2] G(v) >= 0 with the scalar 16 m w4 C^2 > 1/2",
       "z3 + interval/Arb scalar")
def check_M7():
    hy, goal = large_t_skeleton()
    z3_valid(hy, goal, None)
    ch, C_ = jc.scalar_checks(verbose=False)
    assert ch["16 m w4 C^2 - 1/2"].lo > 0 and (IF(jc.M * jc.W4) * C_.sq()).hi < 0.04


def edge_skeleton(which, with_tail=True):
    Tt, Uz, Vz, G2t, Gu, Gv, Gt, G2v, Pu, Pv, C, k0, mw4 = z3.Reals("t u v G2t Gu Gv Gt G2v Pu Pv C k0 mw4")
    F = k0 * G2t + mw4 * Pu * Pv - (Gu + Gv) / 2
    hy = [G2t >= Gu, Pu >= 0, Pv >= 0, Gv >= 0, k0 > Fr(1, 2), mw4 > 0]
    if which == 1:
        return hy, F >= (k0 - Fr(1, 2)) * G2t - Gv / 2
    hy += [C > 0, Pu >= C * Gu, Gu >= Gt, Gt >= 0, Gv <= (2 * mw4 * C * Gt) ** 2]
    if with_tail:                       # v <= -ln B: P(v) = sqrt(G(2v)) >= sqrt(G(v))
        hy += [Pv * Pv == G2v, G2v >= Gv]
    return hy, F >= (k0 - Fr(1, 2)) * G2t


@claim("M.8", "edge bounds (eq. edge1, edge2) and their box form (App. A 'Bounds for an entire edge box'): "
       "G(u) <= G(2t), PP >= 0 => (edge1); v <= -ln B, G(v) <= [2 m w4 C G(t)]^2 => m w4 P(u)P(v) >= G(v)/2 => "
       "(edge2); on a box, G monotone turns v_max, t_- tests into pointwise ones", "z3")
def check_M8():
    for which in (1, 2):
        hy, goal = edge_skeleton(which)
        z3_valid(hy, goal, None)
    # box form: v <= vmax, t >= t-, G increasing
    Gv, Gvm, Gt, Gtm, mw4, C, V, Vm, lnB = z3.Reals("Gv Gvm Gt Gtm mw4 C v vm lnB")
    z3_valid([Gv <= Gvm, Gt >= Gtm, Gtm >= 0, mw4 > 0, C > 0, Gvm <= (2 * mw4 * C * Gtm) ** 2, V <= Vm, Vm <= lnB],
             z3.And(Gv <= (2 * mw4 * C * Gt) ** 2, V <= lnB), None)
    # and the implementation's tests in jiang_checks.verify_mixture_strip use exactly these quantities
    import inspect
    src = inspect.getsource(jc.verify_mixture_strip)
    for frag in ("vmax = (I(t1) * (1.0 - I(x0))).hi", "tail = (-ilog(Bi)).lo", "vmax <= tail",
                 "e2 = 2.0 * MW4 * C_MIN * G_all(I(t0))[0]", "gv <= e2.sq().lo", "g2t = G_all(I(2.0 * t0))[0]"):
        assert frag in src, frag


@claim("M.9", "derivative formulas of App. A: phi' = phi[D'/(2D) + h'/(2h) + E'] (phiprime), s' = x h'(x^2)/s, "
       "psi' on [A,B], P'(u) = psi(x)/x - psi'(x), P on the pieces used by jiang_checks.P_all, F_t and F_xi "
       "(eq. Ft, Fxi), r_alpha, r_beta for x < y and y < x, Delta_alpha, Delta_beta", "sympy-exact")
def check_M9():
    Df, Ef, Rf = sp.Function("D"), sp.Function("E"), sp.Function("R")
    hstar, sg = sp.symbols("hstar sigma", positive=True)
    # phi = sg R e^E with R^2 = D h / h*  (R' from R^2)
    Rx = sp.Symbol("Rx", positive=True)
    Rp = sp.diff(Df(x) * hf(x), x) / (2 * hstar * Rx)
    phi = sg * Rx * sp.exp(Ef(x))
    dphi = sg * (Rp * sp.exp(Ef(x)) + Rx * sp.diff(Ef(x), x) * sp.exp(Ef(x)))
    claimed = phi * (sp.diff(Df(x), x) / (2 * Df(x)) + sp.diff(hf(x), x) / (2 * hf(x)) + sp.diff(Ef(x), x))
    diff_ = sp.cancel(sp.together(dphi - claimed))
    assert sp.cancel(sp.together(diff_.subs(hstar, Df(x) * hf(x) / Rx**2))) == 0
    W = sp.Symbol("W", positive=True)
    s_ = sp.sqrt(hf(x**2))
    assert sp.simplify(sp.diff(s_, x) - x * sp.diff(hf(W), W).subs(W, x**2) / s_) == 0
    phf, sf = sp.Function("phi"), sp.Function("s")
    th = (x - A_S) / (B_S - A_S)
    psi = (1 - th) * phf(x) + th * sf(x)
    assert sp.simplify(sp.diff(psi, x) - ((1 - th) * sp.diff(phf(x), x) + th * sp.diff(sf(x), x)
                                          + (sf(x) - phf(x)) / (B_S - A_S))) == 0
    psf = sp.Function("psi")
    Pu = psf(sp.exp(-u)) * sp.exp(u)
    assert sp.simplify(sp.diff(Pu, u) - (psf(W) / W - sp.diff(psf(W), W)).subs(W, sp.exp(-u))) == 0
    Gf = sp.Function("G")
    # P on u <= -ln B: sqrt(G(2u)), P' = G'(2u)/sqrt(G(2u))
    Pt = sp.sqrt(Gf(2 * u))
    assert sp.simplify(sp.diff(Pt, u) - sp.diff(Gf(W), W).subs(W, 2 * u) / sp.sqrt(Gf(2 * u))) == 0
    # P on u >= ln 2: sg G(u) e^{E(e^-u)}/sqrt(h*), P' = P (G'/G - x E'(x)), x = e^-u
    Pl = sg * Gf(u) * sp.exp(Ef(sp.exp(-u))) / sp.sqrt(hstar)
    tgt = Pl * (sp.diff(Gf(u), u) / Gf(u) - sp.exp(-u) * sp.diff(Ef(W), W).subs(W, sp.exp(-u)))
    assert sp.simplify(sp.diff(Pl, u) - tgt) == 0
    # and the paper's identity P = sg G e^E/sqrt(h*) on x <= 1/2 (D = h): phi(x)/x with x = e^-u
    assert sp.simplify(sg * hf(W) * sp.exp(Ef(W)) / sp.sqrt(hstar) / W
                       - sg * (hf(W) / W) * sp.exp(Ef(W)) / sp.sqrt(hstar)) == 0
    # F_t, F_xi
    Pf = sp.Function("P")
    tt, k0, mw4 = sp.symbols("t k0 mw4", positive=True)
    U_, V_ = tt * (1 + xi), tt * (1 - xi)
    F = k0 * Gf(2 * tt) + mw4 * Pf(U_) * Pf(V_) - (Gf(U_) + Gf(V_)) / 2
    d = lambda fn, at: sp.diff(fn(W), W).subs(W, at)
    Ft = 2 * k0 * d(Gf, 2 * tt) + mw4 * ((1 + xi) * d(Pf, U_) * Pf(V_) + (1 - xi) * Pf(U_) * d(Pf, V_)) \
        - ((1 + xi) * d(Gf, U_) + (1 - xi) * d(Gf, V_)) / 2
    Fx = tt * (mw4 * (d(Pf, U_) * Pf(V_) - Pf(U_) * d(Pf, V_)) - (d(Gf, U_) - d(Gf, V_)) / 2)
    assert sp.simplify(sp.diff(F, tt) - Ft) == 0 and sp.simplify(sp.diff(F, xi) - Fx) == 0
    # r_alpha, r_beta; Delta
    xf, af, yf, bf = (sp.Function(n_) for n_ in ("x", "a", "y", "b"))
    X, A_, Y, B_ = xf(al), af(al), yf(be), bf(be)
    for dmin in (X, Y):
        r = X * Y + A_ * B_ * (dmin - X * Y)
        dal, dbe = sp.diff(dmin, al), sp.diff(dmin, be)
        ra = sp.diff(X, al) * Y + sp.diff(A_, al) * B_ * (dmin - X * Y) + A_ * B_ * (dal - sp.diff(X, al) * Y)
        rb = X * sp.diff(Y, be) + A_ * sp.diff(B_, be) * (dmin - X * Y) + A_ * B_ * (dbe - X * sp.diff(Y, be))
        assert sp.simplify(sp.diff(r, al) - ra) == 0 and sp.simplify(sp.diff(r, be) - rb) == 0
        gap = hf(r) - phf(X) * phf(Y)
        Da = d(hf, r) * ra - d(phf, X) * sp.diff(X, al) * phf(Y)
        Db = d(hf, r) * rb - phf(X) * d(phf, Y) * sp.diff(Y, be)
        assert sp.simplify(sp.diff(gap, al) - Da) == 0 and sp.simplify(sp.diff(gap, be) - Db) == 0


# ============================================================ scalars: second evaluation (Arb)
def arb_scalars(prec=200, T=Fr(1, 1000), large_t=16, sigma=None):
    """The 12 scalar signs of jiang_checks.scalar_checks, re-evaluated in Arb (independent of interval.py)."""
    flint.ctx.prec = prec
    A = lambda fr: flint.arb(Fr(fr).numerator) / Fr(fr).denominator
    h = lambda w: -w * w.log() - (1 - w) * (1 - w).log()
    hp = lambda w: ((1 - w) / w).log()
    m, w0, w4 = A(jc.M), A(jc.W0), A(jc.W4)
    Av, Bv, zv, xs = A(jc.A_), A(jc.B_), A(jc.Z_), A(jc.XS)
    sg = A(jc.SIG if sigma is None else sigma)
    L_, U_ = A(Fr(1, 16)), A(Fr(15, 16))
    l2 = flint.arb(2).log()
    hst = h(xs)
    ks = hp(xs) / (2 * hst)
    E = lambda w: -ks * (w - xs) - A(Fr(7, 10)) * (w - xs) ** 2
    Ep = lambda w: -ks - A(Fr(7, 5)) * (w - xs)
    hz2 = h(zv * zv)
    one, half = flint.arb(1), A(Fr(1, 2))
    sA = h(Av * Av).sqrt()
    phiA = sg * (l2 * h(Av * Av) * h(Av) / (hz2 * hst)).sqrt() * E(Av).exp()
    C_min = sg / hst.sqrt() * E(flint.arb(0)).exp()
    C_b = sg / hst.sqrt() * E(L_).exp()
    P0 = sg * l2 / hst.sqrt() * E(half).exp()
    C_g = sg * (2 * l2 / (hst * hz2)).sqrt() * E(one).exp()
    C_t = sg / U_ * (l2 / hz2 * h(U_ * U_) * h(U_) / hst).sqrt() * E(one).exp()
    Tv = A(T)
    return {
        "E'(1) > 0": Ep(one),
        "1 - C_g C_t": 1 - C_g * C_t,
        "1 - C_b P0": 1 - C_b * P0,
        "1 - 2 C_b P0": 1 - 2 * C_b * P0,
        "1 - E'(1/2) - h'(z^2)/h(z^2)": 1 - Ep(half) - hp(zv * zv) / hz2,
        "A - s(A) C_b": Av - sA * C_b,
        "s(A) - phi(A)": sA - phiA,
        "-(h'(A)/(2h(A)) + E'(A))": -(hp(Av) / (2 * h(Av)) + Ep(Av)),
        "k0 - 1/2": m * w0 - half,
        "2 m w4 (1 - ln 4T) - 1": 2 * m * w4 * (1 - (4 * Tv).log()) - 1,
        "e^{-2T} - B": (-2 * Tv).exp() - Bv,
        "16 m w4 C^2 - 1/2": large_t * m * w4 * C_min ** 2 - half,
    }


@claim("SC", "all 12 scalar signs re-evaluated in Arb (200 bits), positive and overlapping the interval.py enclosures "
       "of jiang_checks.scalar_checks", "arb + interval")
def check_SC():
    ch, _ = jc.scalar_checks(verbose=False)
    if flint is None:
        return
    ab = arb_scalars()
    assert set(ab) == set(ch)
    for k, val in ab.items():
        assert val > 0, (k, val)
        lo, hi = float(val.lower()), float(val.upper())
        assert lo <= ch[k].hi and ch[k].lo <= hi, (k, val, ch[k])


# ============================================================ stress test of the statements
def mp_model(dps=40):
    """40-digit mpmath model of Jiang's construction (written from the paper, independent of jiang_checks)."""
    import mpmath as mp
    mp.mp.dps = dps
    F_ = lambda fr: mp.mpf(Fr(fr).numerator) / Fr(fr).denominator
    A, B, z, sig, xs = F_(jc.A_), F_(jc.B_), F_(jc.Z_), F_(jc.SIG), F_(jc.XS)
    h = lambda w: mp.mpf(0) if w in (0, 1) else -w * mp.log(w) - (1 - w) * mp.log1p(-w)
    hp = lambda w: mp.log((1 - w) / w)
    ks = hp(xs) / (2 * h(xs))
    E = lambda w: -ks * (w - xs) - mp.mpf(7) / 10 * (w - xs) ** 2
    D = lambda w: h(w) if w <= 0.5 else (mp.log(2) if w <= z else mp.log(2) * h(w * w) / h(z * z))
    phi = lambda w: sig * mp.sqrt(D(w) * h(w) / h(xs)) * mp.e ** E(w)
    s = lambda w: mp.sqrt(h(w * w))
    psi = lambda w: phi(w) if w <= A else (s(w) if w >= B else
                                           (1 - (w - A) / (B - A)) * phi(w) + (w - A) / (B - A) * s(w))
    a = lambda w: 1 if w <= 0.5 else (mp.sqrt((1 - 2 * w * w) / (2 * w * (1 - w))) if w < 1 / mp.sqrt(2) else 0)
    r = lambda X, Y: X * Y + a(X) * a(Y) * (min(X, Y) - X * Y)
    return mp, dict(m=F_(jc.M), w0=F_(jc.W0), w4=F_(jc.W4), A=A, B=B, z=z, xs=xs, h=h, psi=psi, r=r)


def statement_stress(n=2000, seed=5, dps=40):
    """Sanity test (not a proof): (K) and (M) at random points of [0,1]^2 in 40-digit mpmath, with extra points
    near (x*, x*), near y = 1, near the strips and near the breakpoints.  Returns (min K - psi psi,
    min [(M) gap]/(xy) on xy > 0)."""
    import random
    mp, md = mp_model(dps)
    rnd = random.Random(seed)
    m, w0, w4, A, B, z, xs = (md[k] for k in ("m", "w0", "w4", "A", "B", "z", "xs"))
    h, psi, r = md["h"], md["psi"], md["r"]
    mK, mM = mp.inf, mp.inf
    for i in range(n):
        mode = rnd.random()
        X, Y = mp.mpf(rnd.random()), mp.mpf(rnd.random())
        if mode < 0.2:
            X, Y = xs + mp.mpf(rnd.uniform(-1, 1)) * 10 ** rnd.randint(-6, -2), xs + mp.mpf(rnd.uniform(-1, 1)) * 10 ** rnd.randint(-6, -2)
        elif mode < 0.35:
            Y = 1 - mp.mpf(10) ** (-rnd.uniform(1, 12))
        elif mode < 0.45:
            X = mp.mpf(10) ** (-rnd.uniform(1, 12))
        elif mode < 0.55:
            X = rnd.choice([A, B, z, mp.mpf(0.5), 1 / mp.sqrt(2), mp.mpf(1) / 16, mp.mpf(15) / 16]) + mp.mpf(rnd.uniform(-1e-6, 1e-6))
        if not (0 < X < 1 and 0 < Y < 1):
            continue
        mK = min(mK, h(r(X, Y)) - psi(X) * psi(Y))
        gapM = 2 * m * (w0 * h(X * Y) + w4 * psi(X) * psi(Y)) - X * h(Y) - Y * h(X)
        mM = min(mM, gapM / (X * Y))
    return float(mK), float(mM)


def reduction_instance(fam, n, m_override=None, dps=30):
    """Exact-law evaluation (mpmath) of the two couplings of Prop. 'Entropy reduction' on the uniform law
    of a finite family `fam` (list of distinct bitmasks over n coordinates; bit i = 1 means i in the set;
    X_i = 0 means i not in the set).  Shared-uniform rule: averaging the fresh U_i gives the pair kernel
    P(00) = r(S,T), P(0.) = S, P(.0) = T at each coordinate (R.1), so the joint law is a finite sum.
    Returns (lhs, rhs, per-coordinate minima, p, H(Z0), H(Z4), ln N) with
      lhs = w0 H(Z0) + w4 H(Z4),  rhs = (1-p)/m H(X),  p = max_i p_i,
      per-coordinate: min_i [H((Z0)_i | (Z0)_<i) - E_{PxP} h(ST)], min_i [H((Z4)_i|(Z4)_<i) - E K(S,T)],
                      min_i [E K(S,T) - (E_{P_i} psi)^2]."""
    mp, md = mp_model(dps)
    h, psi, r = md["h"], md["psi"], md["r"]
    m = md["m"] if m_override is None else m_override
    w0, w4 = md["w0"], md["w4"]
    N = len(fam)
    bit = lambda A_, i: (A_ >> i) & 1
    pref = lambda A_, i: A_ & ((1 << i) - 1)

    def ent(dist):
        return -mp.fsum(pv * mp.log(pv) for pv in dist.values() if pv > 0)

    def cond_ent_coord(law):
        """sum_i H(Z_i | Z_<i) for a law on bitmasks, returned per coordinate."""
        out = []
        for i in range(n):
            joint, marg = {}, {}
            for zz, pv in law.items():
                k1, k0 = pref(zz, i + 1), pref(zz, i)
                joint[k1] = joint.get(k1, 0) + pv
                marg[k0] = marg.get(k0, 0) + pv
            out.append(ent(joint) - ent(marg))
        return out
    # native conditional zero-probabilities x_i(alpha)
    xi_ = {}
    for i in range(n):
        cnt = {}
        for A_ in fam:
            c0, c1 = cnt.get(pref(A_, i), (0, 0))
            cnt[pref(A_, i)] = (c0 + (1 - bit(A_, i)), c1 + bit(A_, i))
        for k, (c0, c1) in cnt.items():
            xi_[(i, k)] = mp.mpf(c0) / (c0 + c1)
    w = mp.mpf(1) / N
    HX = mp.log(N)
    p_i = [mp.mpf(sum(bit(A_, i) for A_ in fam)) / N for i in range(n)]
    p = max(p_i)
    # independent rule
    Z0 = {}
    for A_ in fam:
        for B_ in fam:
            Z0[A_ | B_] = Z0.get(A_ | B_, 0) + w * w
    # shared-uniform rule: pair process with the averaged kernel
    pairs = {(0, 0): mp.mpf(1)}
    tiny = mp.mpf(10) ** (-dps + 8)
    EK, Epsi2, Eh = [], [], []
    for i in range(n):
        new, ek, eh = {}, mp.mpf(0), mp.mpf(0)
        for (al_, be_), pv in pairs.items():
            S, T = xi_[(i, al_)], xi_[(i, be_)]
            rr = r(S, T)
            ek += pv * h(rr)
            for bx, by, q_ in ((0, 0, rr), (0, 1, S - rr), (1, 0, T - rr), (1, 1, 1 - S - T + rr)):
                assert q_ > -tiny, q_                    # r in [max(0, S+T-1), min(S,T)] (R.2)
                if q_ > tiny:                            # drop rounding-level phantom transitions
                    key = (al_ | (bx << i), be_ | (by << i))
                    new[key] = new.get(key, 0) + pv * q_
        # E_{P_i} psi and E_{P x P} h(ST): P_i = law of x_i(X_<i) under the uniform family law
        Pi = {}
        for A_ in fam:
            Pi[xi_[(i, pref(A_, i))]] = Pi.get(xi_[(i, pref(A_, i))], 0) + w
        Epsi2.append(mp.fsum(pv * psi(xx) for xx, pv in Pi.items()) ** 2)
        Eh.append(mp.fsum(pa * pb * h(xa * xb) for xa, pa in Pi.items() for xb, pb in Pi.items()))
        EK.append(ek)
        pairs = new
    Z4 = {}
    for (al_, be_), pv in pairs.items():
        Z4[al_ | be_] = Z4.get(al_ | be_, 0) + pv
    # the marginal of each coordinate of the shared rule is the native law (checked)
    for side in (0, 1):
        marg = {}
        for k, pv in pairs.items():
            marg[k[side]] = marg.get(k[side], 0) + pv
        assert all(abs(marg.get(A_, 0) - w) < mp.mpf(10) ** (-dps + 10) for A_ in fam) and len(marg) == N
    c0, c4 = cond_ent_coord(Z0), cond_ent_coord(Z4)
    H0, H4 = mp.fsum(c0), mp.fsum(c4)
    lhs = w0 * H0 + w4 * H4
    rhs = (1 - p) / m * HX
    per = (min(c0[i] - Eh[i] for i in range(n)), min(c4[i] - EK[i] for i in range(n)),
           min(EK[i] - Epsi2[i] for i in range(n)))
    return lhs, rhs, per, p, H0, H4, HX


def random_families(count, seed=3, union_closed=False):
    import random
    rnd = random.Random(seed)
    out = []
    while len(out) < count:
        n = rnd.randint(1, 4)
        k = rnd.randint(1, min(8, 2**n))
        fam = set(rnd.sample(range(2**n), k))
        if union_closed:
            fam.add(0)
            changed = True
            while changed:
                changed = False
                for A_ in list(fam):
                    for B_ in list(fam):
                        if A_ | B_ not in fam:
                            fam.add(A_ | B_)
                            changed = True
        if len(fam) >= 2:
            out.append((sorted(fam), n))
    return out


@claim("R.x", "sanity test (not a proof) of the READ-ONLY probability layer of the reduction: on 150 random families "
       "(n <= 4; 75 arbitrary, 75 union-closed) the exact laws of both couplings satisfy, per coordinate, "
       "H((Z0)_i|.) >= E h(ST), H((Z4)_i|.) >= E K(S,T) >= (E psi)^2, the marginals of the shared rule are "
       "uniform on F, w0 H(Z0) + w4 H(Z4) >= (1-p)/m H(X), and for union-closed F: H(Z0), H(Z4) <= ln N, p >= 1-m",
       "numerical (mpmath, exact finite laws)")
def check_reduction_instances():
    for uc in (False, True):
        for fam, n in random_families(75, seed=3 + uc, union_closed=uc):
            lhs, rhs, per, p, H0, H4, HX = reduction_instance(fam, n)
            assert lhs >= rhs - 1e-25 and min(per) >= -1e-25, (fam, n, lhs, rhs, per)
            if uc:
                assert H0 <= HX + 1e-25 and H4 <= HX + 1e-25 and p >= 1 - float(jc.M)


@claim("x", "sanity test (not a proof) of the STATEMENTS (K) and (M) at 2000 random points each (40-digit mpmath; "
       "extra points near (x*,x*), y -> 1, x -> 0 and the breakpoints)", "numerical (mpmath)")
def check_stress():
    mK, mM = statement_stress()
    assert mK > 0 and mM > 0, (mK, mM)


# ============================================================ driver
ALL = [check_R1, check_R2, check_R3, check_R4,
       check_C1, check_C2,
       check_P1,
       check_G1, check_G2, check_G3,
       check_O1, check_O2,
       check_T1,
       check_S1, check_S2, check_S3, check_S4, check_S5, check_S6,
       check_M1, check_M2, check_M3, check_M4, check_M5, check_M6, check_M7, check_M8, check_M9,
       check_SC, check_stress, check_reduction_instances]


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
        say(f"[OK] {chk.cid:5s} {chk.method:48s} {time.time()-t0:6.1f}s  {chk.statement}")
    say(f"all {len(RESULTS)} Jiang analytic-glue claims checked in {time.time()-t_all:.1f}s"
        f"  (sympy {sp.__version__}, z3 {z3.get_version_string()},"
        f" python-flint {flint.__version__ if flint else 'absent'})")
    return list(RESULTS)


if __name__ == "__main__":
    run_all(only=sys.argv[1] if len(sys.argv) > 1 else None)
