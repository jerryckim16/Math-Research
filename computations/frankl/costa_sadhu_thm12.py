"""Independent re-verification of the finite computations behind
Costa-Sadhu, arXiv:2610.02295, Theorem 1.2:

    c_UC >= 1 - m0 = 0.3828852549667978,
    m0 = 3085573725166011/5*10^15,  l0 = 1409/2000,  tau0 = l0^2,
    alpha0 = 1/(2 m0) + 1/800000000,  beta0 = 1 - alpha0.

Proof structure (their Section 6 + Appendix A, Certificates A.4-A.7):
  Lemma 6.1 (tuned product)  H(r(x,y))^2 >= H(g(x)) H(g(y)),
        r = xy(1 + tau0 (1-x)(1-y)), g(x) = r(x,x);
        analytic, except the exact facts checked in exact_checks() below
        (identity, g(45/64) > 1/2, Bernstein certificate A.4).
  Lemma 6.2 (second inequality)  F0(s, sigma) > 0, where x = e^-s, y = e^-sigma,
        F0 = alpha0 G(s+sigma) - (G(s)+G(sigma))/(2 m0) + beta0 sqrt(W0(s) W0(sigma)),
        G(u) = e^u H(e^-u),  W0(u) = e^{2u} H(g(e^-u)).
        Cases 1-3 are analytic given the 1D facts of Certificate A.5
        (two global inequalities + three scalar margins), checked in
        one_dimensional_checks().  The rest, 2^-11 < t < 17, 0 <= xi < 15/17
        (t = (s+sigma)/2, xi = (sigma-s)/(sigma+s)), is Certificate A.6 (local
        convexity at the near-contact point t_c) + A.7 (finite box cover):
        contact_checks() and cover_region() use OUR OWN local rectangle and
        OUR OWN dyadic cover.

Notation in the code: Gam(u) = sqrt(W0(u)) = e^u sqrt(H(g(e^-u))), and
    m0 F0 = m0 alpha0 G(2t) + m0 beta0 Gam(u) Gam(v) - (G(u)+G(v))/2,
u = t(1+xi) = sigma, v = t(1-xi) = s.  This is the same shape as the Thm 1.1
function in costa_sadhu_checks.py, with (m*, alpha, beta, g) replaced by
(m0, alpha0, beta0, g_l0).  We certify m0 F0 > 0 (m0 > 0).

All transcendental evaluations use interval.py (outward-rounded IEEE doubles,
own log/exp); all thresholds that are rational are compared exactly.
"""
from __future__ import annotations

import sys
import time
from fractions import Fraction as Fr
from math import comb

from interval import I, IF, H, ilog, iexp, isqrt_, LN2, frac_hi, frac_lo, _log_point
from costa_sadhu_checks import (pmul, padd, pscale, X, Y, ONE, c, Hp, Hpp)

# =================================================================== constants
L0 = Fr(1409, 2000)
TAU = L0 ** 2
M0 = Fr(3085573725166011, 5 * 10**15)
ALPHA0 = 1 / (2 * M0) + Fr(1, 800000000)
BETA0 = 1 - ALPHA0
TC = 0.369781418829901          # their contact-point centre (we only use it as a float)
BERN_MIN = Fr(4652778828628843621308587, 8388608000000000000000000)


# =================================================================== exact
def bernstein_33(P, a):
    """Product-Bernstein coefficients of P(a s, a t) (bidegree <= (3,3))."""
    Ps = {(i, j): v * a ** (i + j) for (i, j), v in P.items()}
    assert max(i for i, _ in Ps) <= 3 and max(j for _, j in Ps) <= 3
    return [[sum(Fr(comb(i, k), comb(3, k)) * Fr(comb(j, l), comb(3, l)) * Ps.get((k, l), 0)
                 for k in range(i + 1) for l in range(j + 1)) for j in range(4)] for i in range(4)]


def exact_checks(verbose=True):
    say = print if verbose else (lambda *a: None)
    t = TAU
    assert t == Fr(1985281, 4000000)
    # Theorem 1.2's decimal is exactly 1 - m0
    assert 1 - M0 == Fr("0.3828852549667978")
    assert M0 > Fr(1, 2) and 2 * M0 * (1 - Fr(1, 800000000)) > 1
    assert 0 < ALPHA0 < 1 and 0 < BETA0 < 1
    assert M0 * ALPHA0 - Fr(1, 2) == M0 / 800000000      # = 7.71e-10: the y = 1 margin
    # polynomials (x, y) with tau = tau0
    T = c(t)
    omx, omy = padd(ONE, pscale(X, -1)), padd(ONE, pscale(Y, -1))
    om2x, om2y = padd(ONE, pscale(X, -2)), padd(ONE, pscale(Y, -2))
    W = padd(ONE, pmul(T, pmul(omx, omy)))
    Ux = padd(ONE, pmul(T, pmul(om2x, omy)))      # r_x = y Ux
    Vy = padd(ONE, pmul(T, pmul(omx, om2y)))      # r_y = x Vy
    Rxy = padd(ONE, pmul(T, pmul(om2x, om2y)))    # r_xy
    XY = pmul(X, Y)
    r = pmul(XY, W)

    def dx(p):
        return {(i - 1, j): i * v for (i, j), v in p.items() if i > 0}

    def dy(p):
        return {(i, j - 1): j * v for (i, j), v in p.items() if j > 0}
    assert padd(dx(r), pscale(pmul(Y, Ux), -1)) == {}
    assert padd(dy(r), pscale(pmul(X, Vy), -1)) == {}
    assert padd(dy(dx(r)), pscale(Rxy, -1)) == {}
    # identity (6.x):  W r_xy - Ux Vy = tau xy
    assert padd(pmul(W, Rxy), pscale(pmul(Ux, Vy), -1), pscale(XY, -t)) == {}
    # g' = 2x[1 + tau (1-x)(1-2x)] and (1-x)(1-2x) >= -1/8 (min at x = 3/4)
    gpoly = {(2, 0): 1 + t, (3, 0): -2 * t, (4, 0): t}
    gp = {(1, 0): 2 + 2 * t, (2, 0): -6 * t, (3, 0): 4 * t}
    assert padd(gpoly, pscale(pmul(pmul(X, X), padd(ONE, pmul(T, pmul(omx, omx)))), -1)) == {}
    assert padd(dx(gpoly), pscale(gp, -1)) == {}
    assert padd(gp, pscale(pmul(pscale(X, 2), padd(ONE, pmul(T, pmul(omx, om2x)))), -1)) == {}
    # 2x^2 - 3x + 1 >= -1/8: (2x^2-3x+1) + 1/8 = 2(x - 3/4)^2
    assert padd({(2, 0): Fr(2), (1, 0): Fr(-3), (0, 0): Fr(9, 8)},
                pscale(pmul(padd(X, c(Fr(-3, 4))), padd(X, c(Fr(-3, 4)))), -2)) == {}
    assert 1 - t / 8 > 0
    g = lambda x: x**2 * (1 + t * (1 - x) ** 2)
    assert g(Fr(45, 64)) - Fr(1, 2) == Fr(42978321721, 2684354560000)
    # W0 increasing (proof): z q_z = 2q - 2 tau z^3 (1-z); max z^3(1-z) = 27/256 at 3/4
    zqz = pmul(X, dx(gpoly))
    assert padd(zqz, pscale(gpoly, -2), {(3, 0): 2 * t, (4, 0): -2 * t}) == {}
    # z^3(1-z) <= 27/256 on [0,1]:  27/256 - z^3 + z^4 = (z - 3/4)^2 (z^2 + z/2 + 3/16)
    assert Fr(3, 4) ** 3 * (1 - Fr(3, 4)) == Fr(27, 256) and 27 * t / 256 < 1
    q = {(4, 0): Fr(1), (3, 0): Fr(-1), (0, 0): Fr(27, 256)}  # 27/256 - z^3 + z^4
    fac = pmul(pmul(padd(X, c(Fr(-3, 4))), padd(X, c(Fr(-3, 4)))),
               {(2, 0): Fr(1), (1, 0): Fr(1, 2), (0, 0): Fr(3, 16)})
    assert padd(q, pscale(fac, -1)) == {}          # and z^2 + z/2 + 3/16 > 0 (disc < 0)
    assert Fr(1, 4) - 4 * Fr(3, 16) < 0
    # Case 3 identity: e^{2w}(1 - g(e^-w)) = e^{2w} - 1 - tau (1 - e^-w)^2, i.e.
    # 1 - g(z) = 1 - z^2 - tau z^2 (1-z)^2  (polynomial identity in z)
    assert padd(padd(ONE, pscale(gpoly, -1)),
                pscale(padd(ONE, {(2, 0): Fr(-1)}, pscale(pmul(pmul(X, X), pmul(omx, omx)), -t)), -1)) == {}
    # Certificate A.4: Bernstein coefficients of W Ux Vy - tau (1 - r) on [0, 45/64]^2
    P = padd(pmul(pmul(W, Ux), Vy), pscale(padd(ONE, pscale(r, -1)), -t))
    B = bernstein_33(P, Fr(45, 64))
    flat = [b for row in B for b in row]
    assert all(b > 0 for b in flat)
    assert min(flat) == BERN_MIN, min(flat)
    say("exact: tau0, m0, alpha0, beta0, identity W r_xy - r_x r_y/(xy) = tau xy, g', "
        "g(45/64)-1/2 = 42978321721/2684354560000, W0-monotonicity algebra, "
        f"Bernstein A.4 (16 coefficients > 0, min = published {float(BERN_MIN):.16g}): OK")
    return B


# =================================================================== intervals
TAU_I = IF(TAU)
M0_I = IF(M0)
A0_I = IF(ALPHA0)
B0_I = IF(BETA0)
INV2M0 = IF(1 / (2 * M0))
MA = IF(M0 * ALPHA0)     # m0 alpha0
MB = IF(M0 * BETA0)      # m0 beta0


# ---- accurate entropy / G for arguments near 0 (needed for t up to 17, where
# e^{-2t} ~ 1e-15 and the naive (1-x)log(1-x) loses all relative accuracy)
def S_small(x: I) -> I:
    """S(x) = -log(1-x)/x = sum_{k>=0} x^k/(k+1), for 0 < x <= 1/4: partial sum of N terms
    (N such that x^N < 2^-62) plus the tail, 0 <= tail <= x^N/((N+1)(1-x))."""
    assert x.lo > 0 and x.hi <= 0.25
    s, p, k = I(1.0), I(1.0), 0
    while True:
        k += 1
        p = p * x
        if p.hi < 2.0**-62:
            break
        s = s + p / float(k + 1)
    # p = x^k now; tail = sum_{j>=k} x^j/(j+1) <= x^k/((k+1)(1-x))
    tail = p / (float(k + 1) * (1.0 - x))
    return I(s.lo, (s + tail).hi)


def S_I(x: I) -> I:
    if x.hi <= 0.25:
        return S_small(x)
    return -ilog(1.0 - x) / x


def _H_point(p: float) -> I:
    """H(p) for a float 0 < p < 1, accurate also for tiny p:  H(p) = p(log(1/p) + (1-p) S(p))."""
    if p <= 0.25:
        P = I(p)
        return P * (-_log_point(p) + (1.0 - P) * S_small(P))
    return H(I(p))


def Hr(z: I) -> I:
    """Binary entropy enclosure (monotone pieces), accurate for z near 0 or 1."""
    if z.lo <= 0.0 or z.hi >= 1.0:
        raise ValueError("Hr needs (0,1)")
    if z.hi <= 0.5:
        return I(_H_point(z.lo).lo, _H_point(z.hi).hi)
    if z.lo >= 0.75:
        return Hr(1.0 - z)
    return H(z)


def G_all(u: I):
    """G(u) = e^u H(e^-u) = u + (1-x) S(x), G' = S(x), G'' = S(x) - 1/(1-x), x = e^-u.
    (From G = u + ((1-x)/x)(-log(1-x)) and the series G' = sum_k x^k/(k+1) = S(x).)"""
    x = iexp(-u)
    S = S_I(x)
    return u + (1.0 - x) * S, S, S - 1.0 / (1.0 - x)


def G_val(u: I) -> I:
    a = G_all(I(u.lo))[0]
    b = G_all(I(u.hi))[0]
    return I(a.lo, b.hi)


def g_I(x: I) -> I:
    return x.sq() * (1.0 + TAU_I * (1.0 - x).sq())


def gp_I(x: I) -> I:      # 2x + tau(2x - 6x^2 + 4x^3)
    return 2.0 * x + TAU_I * (2.0 * x - 6.0 * x.sq() + 4.0 * x * x.sq())


def gpp_I(x: I) -> I:     # 2 + tau(2 - 12x + 12x^2)
    return 2.0 + TAU_I * (2.0 - 12.0 * x + 12.0 * x.sq())


def Gam_all(u: I, need2=False):
    """Gam(u) = e^u sqrt(H(g(e^-u))) = sqrt(W0(u)) and its derivatives."""
    x = iexp(-u)
    z = g_I(x)
    if z.hi >= 1.0:
        z = I(z.lo, 1.0 - 2**-52)  # g(x) < 1 for 0 < x < 1 (g increasing, g(1) = 1)
    Hz = Hr(z)
    Gm = isqrt_(Hz) / x
    zp = -x * gp_I(x)
    aa = 1.0 + Hp(z) * zp / (2.0 * Hz)
    G1 = Gm * aa
    if not need2:
        return Gm, G1, None
    zpp = x * gp_I(x) + x.sq() * gpp_I(x)
    q = Hp(z) * zp / Hz
    ap = 0.5 * ((Hpp(z) * zp.sq() + Hp(z) * zpp) / Hz - q.sq())
    G2 = Gm * (aa.sq() + ap)
    return Gm, G1, G2


def W0_point(v) -> I:
    return Gam_all(I(v))[0].sq()


def F_point(t: float, xi: float) -> I:
    """m0 * F0(t(1-xi), t(1+xi)) at a point (t, xi given as floats)."""
    T, XI = I(t), I(xi)
    u = T * (1.0 + XI)
    v = T * (1.0 - XI)
    return MA * G_val(2.0 * T) + MB * Gam_all(u)[0] * Gam_all(v)[0] - 0.5 * (G_val(u) + G_val(v))


def Fderivs_box(T: I, XI: I):
    u = T * (1.0 + XI)
    v = T * (1.0 - XI)
    G2t = G_all(2.0 * T)
    Gu, Gv_ = G_all(u), G_all(v)
    Mu, Mv = Gam_all(u), Gam_all(v)
    Ft = 2.0 * MA * G2t[1] + MB * ((1.0 + XI) * Mu[1] * Mv[0] + (1.0 - XI) * Mu[0] * Mv[1]) \
        - 0.5 * ((1.0 + XI) * Gu[1] + (1.0 - XI) * Gv_[1])
    Fx = MB * T * (Mu[1] * Mv[0] - Mu[0] * Mv[1]) - 0.5 * T * (Gu[1] - Gv_[1])
    return Ft, Fx


def hessian_box(T: I, D: I):
    """Second derivatives of (t,d) -> m0 F0(t-d, t+d)."""
    u = T + D
    v = T - D
    G2t = G_all(2.0 * T)[2]
    Gu2, Gv2 = G_all(u)[2], G_all(v)[2]
    Mu, Mv = Gam_all(u, True), Gam_all(v, True)
    Ftt = 4.0 * MA * G2t + MB * (Mu[2] * Mv[0] + 2.0 * Mu[1] * Mv[1] + Mu[0] * Mv[2]) - 0.5 * (Gu2 + Gv2)
    Fdd = MB * (Mu[2] * Mv[0] - 2.0 * Mu[1] * Mv[1] + Mu[0] * Mv[2]) - 0.5 * (Gu2 + Gv2)
    Ftd = MB * (Mu[2] * Mv[0] - Mu[0] * Mv[2]) - 0.5 * (Gu2 - Gv2)
    return Ftt, Fdd, Ftd


# =================================================================== Certificate A.5
V_SMALL = 2.0**-12     # analytic tail (0, V_SMALL]
V_LARGE = 8.0          # analytic tail [V_LARGE, oo)


def tails_1d(say):
    """Our own analytic tails for W0 >= (8/5) G and G(16v) >= (178/25) G on (0, 2^-12] and [8, oo).

    Small v (L = log 1/v, eps = 1 - e^-v in [v - v^2/2, v], x = e^-v >= 1 - v):
      G(v) = v + (eps/x) log(1/eps)    =>  v + (v - v^2/2) L  <=  G(v)  <=  v + v L/(1-v)
      (eps log(1/eps) increasing on (0, 1/e]);
      W0(v) >= 2v log(1/(2v))   (paper, Lemma 6.2 Case 3, re-derived; needs 2v < 1).
      (i)  W0 - 1.6 G >= v [ L (2 - 1.6/(1-v)) - 2 log 2 - 1.6 ]; the bracket increases as v
           decreases, so it suffices that it is > 0 at v = 2^-12.
      (ii) G(16v) - 7.12 G(v) >= v [ 16 + 16(1-8v)(L - 4 log 2) - 7.12 - 7.12 L/(1-v) ]
           >= v [ 8.88 + L c1 - 64 log 2 ],  c1 = 16(1 - 8 V) - 7.12/(1 - V) > 0, L >= L(V).
    Large v (x = e^-v, q = g(x) <= (1+tau) x^2):
      G(v) <= v + 1,  G(16v) >= 16 v  (Lemma 5.2 bounds u+1-e^-u <= G(u) <= u+1);
      W0 = H(q)/x^2 >= (q/x^2)(log(1/q) + 1 - q) >= 2v - log(1+tau) + 1 - (1+tau) e^{-2v}
           >= 2v - tau + 1 - 2 e^{-2v}.
      (iii) W0 - 1.6 G >= 0.4 v - 0.6 - tau - 2 e^{-2v}, increasing in v: check at v = 8.
      (iv)  16 v - 7.12 (v + 1) = 8.88 v - 7.12 > 0 for v >= 8.
    """
    V = Fr(V_SMALL)
    L = ilog(I(V_SMALL)) * -1.0            # log(1/V)
    one_m = IF(1 - V)
    b1 = L * (2.0 - IF(Fr(8, 5)) / one_m) - 2.0 * LN2 - IF(Fr(8, 5))
    assert b1.lo > 0
    c1 = 16.0 * IF(1 - 8 * V) - IF(Fr(178, 25)) / one_m
    assert c1.lo > 0
    b2 = IF(Fr(222, 25)) + L * c1 - 64.0 * LN2
    assert b2.lo > 0
    assert 16 * V < 1 and 2 * V < 1 and V < Fr(1, 3)   # (b) at 16v needs 16v < 1; eps<=v<=1/e
    b3 = 0.4 * I(V_LARGE) - 0.6 - TAU_I - 2.0 * iexp(I(-2 * V_LARGE))
    assert b3.lo > 0
    assert Fr(888, 100) * Fr(V_LARGE) - Fr(712, 100) > 0
    say(f"1D tails: small-v brackets {b1.lo:.4g}, {b2.lo:.4g} (>0 at v=2^-12); large-v {b3.lo:.4g} (>0 at v=8)")
    return b1, b2, b3


def cover_1d(f, a, b, n0=256, min_w=1e-12):
    """Certify f(lo, hi) > 0 on cells of [a, b]; f returns a rigorous lower bound."""
    h = (b - a) / n0
    assert Fr(a) + n0 * Fr(h) == Fr(b)
    stack = [(a + h * i, a + h * (i + 1)) for i in range(n0)]
    cells, minlb = 0, float("inf")
    while stack:
        lo, hi = stack.pop()
        lb = f(lo, hi)
        if lb > 0:
            cells += 1
            minlb = min(minlb, lb)
            continue
        if hi - lo < min_w:
            raise AssertionError(f"1D cover failed on [{lo}, {hi}]")
        m = 0.5 * (lo + hi)
        stack += [(lo, m), (m, hi)]
    return cells, minlb


def one_dimensional_checks(verbose=True):
    say = print if verbose else (lambda *a: None)
    tails_1d(say)
    c85, c178 = IF(Fr(8, 5)), IF(Fr(178, 25))

    def mono_ok(lo, hi):
        # G' > 0 and Gam' > 0 on the cell (so endpoint evaluation is valid); both are also
        # proved analytically in the paper (Lemma 5.2 / proof of Lemma 6.2)
        Xc = I(lo, hi)
        return G_all(Xc)[1].lo > 0 and Gam_all(Xc)[1].lo > 0

    def f1(lo, hi):   # W0(v) - 1.6 G(v) >= W0(lo) - 1.6 G(hi)
        if not mono_ok(lo, hi):
            return -1.0
        return (W0_point(lo) - c85 * G_all(I(hi))[0]).lo

    def f2(lo, hi):   # G(16 v) - 7.12 G(v) >= G(16 lo) - 7.12 G(hi)
        if not (G_all(I(lo, hi))[1].lo > 0 and G_all(I(16 * lo, 16 * hi))[1].lo > 0):
            return -1.0
        return (G_all(I(16.0 * lo))[0] - c178 * G_all(I(hi))[0]).lo

    t0 = time.time()
    # split [2^-12, 8] into dyadic pieces so that every cell endpoint is an exact float
    out = {}
    for name, f in (("W0 >= 8/5 G", f1), ("G(16v) >= 178/25 G(v)", f2)):
        tot, mn = 0, float("inf")
        for a, b in ((V_SMALL, 2.0**-6), (2.0**-6, 0.5), (0.5, 8.0)):
            n, m = cover_1d(f, a, b, n0=64)
            tot += n
            mn = min(mn, m)
        out[name] = (tot, mn)
        say(f"1D {name} on [2^-12, 8]: {tot} cells, min lower bound {mn:.6g}")
    # three scalar margins of Certificate A.5
    s1 = 1.6 * B0_I * isqrt_(c178) - INV2M0
    s2 = B0_I * W0_point(2.0) - INV2M0
    s3 = 8.0 * B0_I * LN2 - INV2M0
    for s, pub in ((s1, 2.8908190756e-6), (s2, 0.4053615705664), (s3, 0.2421300730523)):
        assert s.lo > 0 and s.hi >= pub, (s, pub)
    say(f"A.5 scalars: {s1}, {s2}, {s3}  ({time.time()-t0:.1f}s)")
    out["scalars"] = (s1, s2, s3)
    return out


# =================================================================== Certificate A.6 (own rectangle)
# Local rectangle Q1 = [5/16, 7/16] x [-1/16, 1/16] in (t, d) (dyadic; contains t_c = 0.36978...).
Q1_T0, Q1_T1, Q1_D = 0.3125, 0.4375, 0.0625


def check_Q1_hessian(n_t=16, n_d=16):
    worst = [1e9, 1e9, 1e9]
    ht, hd = (Q1_T1 - Q1_T0) / n_t, Q1_D / n_d
    stack = [(Q1_T0 + ht * i, Q1_T0 + ht * (i + 1), hd * j, hd * (j + 1))
             for i in range(n_t) for j in range(n_d)]
    boxes = 0
    while stack:
        t0, t1, d0, d1 = stack.pop()
        Ftt, Fdd, Ftd = hessian_box(I(t0, t1), I(d0, d1))
        det = Ftt * Fdd - Ftd.sq()
        if Ftt.lo > 0 and Fdd.lo > 0 and det.lo > 0:
            boxes += 1
            worst = [min(worst[0], Ftt.lo), min(worst[1], Fdd.lo), min(worst[2], det.lo)]
            continue
        if t1 - t0 < 1e-6:
            raise AssertionError(f"Hessian check failed on {(t0, t1, d0, d1)}: {Ftt} {Fdd} {det}")
        tm, dm = 0.5 * (t0 + t1), 0.5 * (d0 + d1)
        stack += [(t0, tm, d0, dm), (tm, t1, d0, dm), (t0, tm, dm, d1), (tm, t1, dm, d1)]
    return boxes, worst


def contact_checks(verbose=True):
    """F := m0 F0(t-d, t+d) is convex on Q1 (Hessian PD; even in d, so d >= 0 suffices),
    hence F(p) >= F(c) + F_t(c)(t - t_c) (F_d(c) = 0 by evenness) with c = (t_c, 0)."""
    say = print if verbose else (lambda *a: None)
    t0 = time.time()
    nb, worst = check_Q1_hessian()
    Fc = F_point(TC, 0.0)
    Ft, Fx = Fderivs_box(I(TC), I(0.0))     # at xi = 0, d/dt F(t, t xi) = F_t(t, 0)
    dist = max(TC - Q1_T0, Q1_T1 - TC) * (1 + 2**-50)
    lb = Fc - I(max(abs(Ft.lo), abs(Ft.hi))) * I(dist)
    assert lb.lo > 0 and Q1_T0 < TC < Q1_T1
    say(f"A.6 (own Q1=[5/16,7/16]x[-1/16,1/16]): Hessian PD on {nb} boxes; min Ftt {worst[0]:.4g},"
        f" Fdd {worst[1]:.4g}, det {worst[2]:.4g}")
    say(f"     m0 F0(t_c,t_c) in {Fc}; |d/dt| <= {max(abs(Ft.lo), abs(Ft.hi)):.3g};"
        f" so m0 F0 >= {lb.lo:.6g} on Q1, i.e. F0 >= {(lb / M0_I).lo:.6g}  ({time.time()-t0:.1f}s)")
    return nb, worst, Fc, Ft, lb


# =================================================================== Certificate A.7 (own cover)
XI_MAX = Fr(15, 17)


def in_Q1(t0, t1, x0, x1):
    return t0 >= Q1_T0 and t1 <= Q1_T1 and Fr(t1) * Fr(x1) <= Fr(Q1_D)


def cover_region(a, b, nt0=64, nx0=16, max_boxes=5 * 10**6, log=None):
    """Prove m0 F0(t(1-xi), t(1+xi)) > 0 on [a,b] x [0, 15/17] minus Q1 (a, b dyadic)."""
    ht = (b - a) / nt0
    assert Fr(a) + nt0 * Fr(ht) == Fr(b), "use dyadic region endpoints"
    stack = [(a + ht * i, a + ht * (i + 1), j / nx0, (j + 1) / nx0)
             for i in range(nt0) for j in range(nx0)]
    done = q1 = 0
    minlb = float("inf")
    where = None
    xi_cap = frac_hi(XI_MAX)
    while stack:
        t0, t1, x0, x1 = stack.pop()
        if Fr(x0) > XI_MAX:
            continue
        if in_Q1(t0, t1, x0, x1):
            q1 += 1
            continue
        xmax = min(x1, xi_cap)
        tc, xc = 0.5 * (t0 + t1), 0.5 * (x0 + xmax)
        Fc = F_point(tc, xc)
        if Fc.lo > 0:
            Ft, Fx = Fderivs_box(I(t0, t1), I(x0, xmax))
            dt = I(max((I(t1) - I(tc)).hi, (I(tc) - I(t0)).hi))
            dx = I(max((I(xmax) - I(xc)).hi, (I(xc) - I(x0)).hi))
            lbI = I(Fc.lo) - I(max(abs(Ft.lo), abs(Ft.hi))) * dt - I(max(abs(Fx.lo), abs(Fx.hi))) * dx
            if lbI.lo > 0:
                done += 1
                if lbI.lo < minlb:
                    minlb, where = lbI.lo, (t0, t1, x0, xmax)
                continue
        if done + len(stack) > max_boxes or t1 - t0 < 1e-10:
            raise AssertionError(f"cover failed near t=[{t0},{t1}] xi=[{x0},{xmax}] Fc={Fc}")
        tm, xm = 0.5 * (t0 + t1), 0.5 * (x0 + xmax)
        stack += [(t0, tm, x0, xm), (tm, t1, x0, xm), (t0, tm, xm, xmax), (tm, t1, xm, xmax)]
    if log:
        log(f"region t in [{a},{b}]: {done} boxes positive (min lb of m0 F0 {minlb:.4g} at {where}), {q1} boxes in Q1")
    return done, q1, minlb, where


# t-regions (dyadic) covering [2^-11, 17]; the xi-range is [0, 15/17] (clipped exactly).
REGIONS = [(2.0**-11, 0.125), (0.125, 0.3125), (0.3125, 0.4375), (0.4375, 1.5), (1.5, 4.0), (4.0, 17.0)]


def run_all(regions=True, verbose=True):
    say = print if verbose else (lambda *a: None)
    exact_checks(verbose)
    one_dimensional_checks(verbose)
    contact_checks(verbose)
    if regions:
        for (a, b) in REGIONS:
            t0 = time.time()
            cover_region(a, b, log=say)
            say(f"   ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    if "--region" in sys.argv:
        i = int(sys.argv[sys.argv.index("--region") + 1])
        t0 = time.time()
        r = cover_region(*REGIONS[i], log=print)
        print(f"REGION {i} {REGIONS[i]} OK {r} {time.time()-t0:.1f}s")
    else:
        run_all(regions="--no-regions" not in sys.argv)
        print("DONE")
