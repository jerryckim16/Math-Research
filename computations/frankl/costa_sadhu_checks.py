"""Independent re-verification of Costa-Sadhu, arXiv:2610.02295, Theorem 1.1:
    c_UC >= c_L = 1 - x* H(x*) / H(x*^2) > 0.382709087918735,
x* the root in (0,1) of p(x) = x^4 - 2x^3 + 3x^2 - 1.

Their proof = Liu's criterion (Prop. 2.2, Liu arXiv:2306.08824 Prop. 3)
            + Lemma R (product inequality, analytic modulo a Bernstein check)
            + Lemma S (two-variable inequality, analytic boundary lemmas +
              a finite interval box cover + a Hessian check at the tangency).

This file re-does every *finite computation* of that proof with our own code:

  exact_checks()     exact rational arithmetic:
     * p'(x) = 2x(2x^2-3x+3) > 0 on (0,1]  (discriminant 9-24 < 0)
     * g(43/64) - 1/2 = 305/2^24
     * identity W r_xy = U V + x y               (Lemma 4.2)
     * Bernstein matrix of W U V - (1 - r) after x=(43/64)s, y=(43/64)t
       equals the published one and is entrywise > 0   (Lemma 4.3 / Prop A.2)
  interval_checks()  outward-rounded interval arithmetic (interval.py):
     * enclosures of x*, m*, beta, t*, c_L and c0 = m* alpha
     * the four scalar inequalities of Lemmas 5.3/5.4
     * Hessian of F positive definite on the symmetric local rectangle
       |t - t_c| <= 0.06, |d| <= 0.06 (F is even in d)
     * positivity of F~(t, xi) = F(t, t xi) on the compact remainder
       (our own adaptive cover, mean-value-form bounds).

The analytic parts (Liu's criterion, Lemma 2.1, Lemma 4.1, Lemma 4.4, the case
analysis in Lemma R, Lemmas 5.2-5.4, the reduction of Prop. 5.1) were read and
are not re-checked by computer.  See problems/frankl-union-closed.md.
"""
from __future__ import annotations

import sys
import time
from fractions import Fraction as Fr
from math import comb

from interval import I, IF, H, ilog, iexp, isqrt_, LN2

# =================================================================== exact
def pmul(a, b):
    r = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            r[(i + k, j + l)] = r.get((i + k, j + l), 0) + c * d
    return {k: v for k, v in r.items() if v != 0}


def padd(*ps):
    r = {}
    for p in ps:
        for k, v in p.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def pscale(p, c):
    return {k: c * v for k, v in p.items()}


X = {(1, 0): Fr(1)}
Y = {(0, 1): Fr(1)}
ONE = {(0, 0): Fr(1)}


def c(v):
    return {(0, 0): Fr(v)}


PUBLISHED_BERNSTEIN = [
    [Fr(7), Fr(41, 12), Fr(8221, 6144), Fr(20653, 131072)],
    [Fr(41, 12), Fr(18803, 9216), Fr(402175, 393216), Fr(1894129, 6291456)],
    [Fr(8221, 6144), Fr(402175, 393216), Fr(52130497, 75497472), Fr(587913113, 1610612736)],
    [Fr(20653, 131072), Fr(1894129, 6291456), Fr(587913113, 1610612736), Fr(6389233321, 17179869184)],
]


def exact_checks(verbose=True):
    XY = pmul(X, Y)
    W = padd(c(2), pscale(X, -1), pscale(Y, -1), XY)
    U = padd(c(2), pscale(X, -2), pscale(Y, -1), pscale(XY, 2))
    V = padd(c(2), pscale(X, -1), pscale(Y, -2), pscale(XY, 2))
    r = pmul(XY, W)
    rxy = padd(c(2), pscale(X, -2), pscale(Y, -2), pscale(XY, 4))
    # Lemma 4.2 identity
    assert padd(pmul(W, rxy), pscale(padd(pmul(U, V), XY), -1)) == {}
    # derivative formulas r_x = yU, r_y = xV, r_xy (check by formal differentiation)
    def dx(p):
        return {(i - 1, j): i * v for (i, j), v in p.items() if i > 0}

    def dy(p):
        return {(i, j - 1): j * v for (i, j), v in p.items() if j > 0}
    assert padd(dx(r), pscale(pmul(Y, U), -1)) == {}
    assert padd(dy(r), pscale(pmul(X, V), -1)) == {}
    assert padd(dy(dx(r)), pscale(rxy, -1)) == {}
    # g(43/64) - 1/2
    g = lambda x: 2 * x**2 - 2 * x**3 + x**4
    assert g(Fr(43, 64)) - Fr(1, 2) == Fr(305, 2**24)
    # p' > 0 on (0,1]: p'(x) = 2x(2x^2 - 3x + 3), quadratic has negative discriminant
    assert 3**2 - 4 * 2 * 3 < 0
    # Bernstein matrix of P(s,t) = (WUV - (1 - r))(43/64 s, 43/64 t)
    P = padd(pmul(pmul(W, U), V), pscale(ONE, -1), r)
    a = Fr(43, 64)
    Ps = {(i, j): v * a ** (i + j) for (i, j), v in P.items()}
    assert max(i for i, _ in Ps) <= 3 and max(j for _, j in Ps) <= 3
    B = [[sum(Fr(comb(i, k), comb(3, k)) * Fr(comb(j, l), comb(3, l)) * Ps.get((k, l), 0)
              for k in range(i + 1) for l in range(j + 1)) for j in range(4)] for i in range(4)]
    assert B == PUBLISHED_BERNSTEIN, B
    assert all(b > 0 for row in B for b in row)
    if verbose:
        print("exact: Lemma 4.2 identity, derivative formulas, g(43/64)-1/2=305/2^24,"
              " Bernstein matrix (equals published, all > 0): OK")
    return B


# =================================================================== intervals
def g_I(x: I) -> I:
    return x.sq() * (1.0 + (1.0 - x).sq())


def gp_I(x: I) -> I:  # g'(x) = 4x - 6x^2 + 4x^3
    return 4.0 * x - 6.0 * x.sq() + 4.0 * x * x.sq()


def gpp_I(x: I) -> I:  # g''(x) = 4 - 12x + 12x^2
    return 4.0 - 12.0 * x + 12.0 * x.sq()


def Hp(z: I) -> I:
    return ilog((1.0 - z) / z)


def Hpp(z: I) -> I:
    return -1.0 / (z * (1.0 - z))


def p_frac(x: Fr) -> Fr:
    return x**4 - 2 * x**3 + 3 * x**2 - 1


def xstar_bracket():
    lo, hi = Fr(1, 2), Fr(1)
    assert p_frac(lo) < 0 < p_frac(hi)
    for _ in range(70):
        m = (lo + hi) / 2
        if p_frac(m) < 0:
            lo = m
        else:
            hi = m
    return lo, hi


def constants():
    lo, hi = xstar_bracket()
    xs = I(Fr(lo), Fr(hi))
    A0 = H(xs.sq())
    Hx = H(xs)
    ms = xs * Hx / A0
    A0p = 2.0 * xs * Hp(xs.sq())
    B0p = gp_I(xs) * Hp(g_I(xs))
    beta = (A0 * (1.0 / xs + Hp(xs) / Hx) - A0p) / (B0p - A0p)
    alpha = 1.0 - beta
    ts = -ilog(xs)
    cL = 1.0 - ms
    c0 = ms * alpha
    return dict(xs=xs, ms=ms, beta=beta, alpha=alpha, ts=ts, cL=cL, c0=c0)


K = None  # filled by setup()


def setup():
    global K
    K = constants()
    return K


# ---- G(u) = e^u H(e^{-u}),  Gamma5(u) = sqrt(H(g(e^{-u}))) e^u, with derivatives
def G_all(u: I):
    x = iexp(-u)
    Hx = H(x)
    Gv = Hx / x
    G1 = Gv - Hp(x)
    G2 = G1 - 1.0 / (1.0 - x)
    return Gv, G1, G2


def G_val(u: I) -> I:
    # G is increasing: evaluate at endpoints for a tight enclosure
    a = G_all(I(u.lo))[0]
    b = G_all(I(u.hi))[0]
    return I(a.lo, b.hi)


def Gam_all(u: I, need2=False):
    x = iexp(-u)
    z = g_I(x)
    if z.hi >= 1.0:
        z = I(z.lo, 1.0 - 2**-52)  # g(x) < 1 for x < 1 (g - 1 = (x-1)(x^3-x^2+x+1))
    Hz = H(z)
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


def F_point(t: float, xi: float) -> I:
    T, XI = I(t), I(xi)
    u = T * (1.0 + XI)
    v = T * (1.0 - XI)
    return K["ms"] * (K["alpha"] * G_val(2.0 * T) + K["beta"] * Gam_all(u)[0] * Gam_all(v)[0]) \
        - 0.5 * (G_val(u) + G_val(v))


def Fderivs_box(T: I, XI: I):
    u = T * (1.0 + XI)
    v = T * (1.0 - XI)
    ms, al, be = K["ms"], K["alpha"], K["beta"]
    G2t = G_all(2.0 * T)
    Gu, Gv_ = G_all(u), G_all(v)
    Mu, Mv = Gam_all(u), Gam_all(v)
    Ft = 2.0 * ms * al * G2t[1] + ms * be * ((1.0 + XI) * Mu[1] * Mv[0] + (1.0 - XI) * Mu[0] * Mv[1]) \
        - 0.5 * ((1.0 + XI) * Gu[1] + (1.0 - XI) * Gv_[1])
    Fx = ms * be * T * (Mu[1] * Mv[0] - Mu[0] * Mv[1]) - 0.5 * T * (Gu[1] - Gv_[1])
    return Ft, Fx


def hessian_box(T: I, D: I):
    u = T + D
    v = T - D
    ms, al, be = K["ms"], K["alpha"], K["beta"]
    G2t = G_all(2.0 * T)[2]
    Gu2, Gv2 = G_all(u)[2], G_all(v)[2]
    Mu, Mv = Gam_all(u, True), Gam_all(v, True)
    Ftt = 4.0 * ms * al * G2t + ms * be * (Mu[2] * Mv[0] + 2.0 * Mu[1] * Mv[1] + Mu[0] * Mv[2]) - 0.5 * (Gu2 + Gv2)
    Fdd = ms * be * (Mu[2] * Mv[0] - 2.0 * Mu[1] * Mv[1] + Mu[0] * Mv[2]) - 0.5 * (Gu2 + Gv2)
    Ftd = ms * be * (Mu[2] * Mv[0] - Mu[0] * Mv[2]) - 0.5 * (Gu2 - Gv2)
    return Ftt, Fdd, Ftd


# Local rectangle Q0 = [5/16, 7/16] x [-1/16, 1/16] in (t, d): dyadic endpoints,
# so every box endpoint below is an exact float.  (Costa-Sadhu use |t-0.36992|<=0.06.)
Q0_T0, Q0_T1, Q0_D = 0.3125, 0.4375, 0.0625


def check_Q0(n_t=16, n_d=16):
    """Hessian PD on [Q0_T0,Q0_T1] x [-Q0_D,Q0_D]; by symmetry d >= 0 suffices
    (F(t,-d) = F(t,d): Ftt, Fdd even in d, Ftd odd, so the determinant is even)."""
    worst = [1e9, 1e9, 1e9]
    ht, hd = (Q0_T1 - Q0_T0) / n_t, Q0_D / n_d   # powers of two: exact
    stack = [(Q0_T0 + ht * i, Q0_T0 + ht * (i + 1), hd * j, hd * (j + 1))
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


def in_Q0(t0, t1, x0, x1):
    # every (t, xi) in the box has t in [Q0_T0, Q0_T1] and d = t xi <= t1 x1 <= Q0_D
    return t0 >= Q0_T0 and t1 <= Q0_T1 and Fr(t1) * Fr(x1) <= Fr(Q0_D)


def cover_region(a, b, nu, nt0=64, nx0=16, max_boxes=5 * 10**6, log=None):
    """Prove F~ > 0 on R = {a<=t<=b, 0<=xi<=1, t(1-xi) >= nu}, except boxes inside Q0.
    a, b, nu must be dyadic floats; all box endpoints are exact dyadics, and the
    clipping xi <= 1 - nu/t1 is rounded upward (covers a superset of R)."""
    from interval import frac_hi
    ht = (b - a) / nt0
    assert Fr(a) + nt0 * Fr(ht) == Fr(b), "use dyadic region endpoints"
    stack = [(a + ht * i, a + ht * (i + 1), j / nx0, (j + 1) / nx0)
             for i in range(nt0) for j in range(nx0)]
    done = q0 = 0
    minlb = float("inf")
    Fnu = Fr(nu)
    while stack:
        t0, t1, x0, x1 = stack.pop()
        if Fr(t1) * (1 - Fr(x0)) < Fnu:      # max of v over the box < nu: box misses R
            continue
        if in_Q0(t0, t1, x0, x1):
            q0 += 1
            continue
        xmax = min(x1, frac_hi(1 - Fnu / Fr(t1)))  # points of R in the box have xi <= 1 - nu/t1
        tc, xc = 0.5 * (t0 + t1), 0.5 * (x0 + xmax)
        Fc = F_point(tc, xc)
        if Fc.lo > 0:
            Ft, Fx = Fderivs_box(I(t0, t1), I(x0, xmax))
            # rigorous: F(t,xi) >= F(tc,xc) - sup|Ft| |t-tc| - sup|Fxi| |xi-xc|
            dt, dx = I(t1) - I(tc), I(xmax) - I(xc)
            dt = I(max(dt.hi, (I(tc) - I(t0)).hi))
            dx = I(max(dx.hi, (I(xc) - I(x0)).hi))
            lbI = I(Fc.lo) - I(max(abs(Ft.lo), abs(Ft.hi))) * dt - I(max(abs(Fx.lo), abs(Fx.hi))) * dx
            if lbI.lo > 0:
                done += 1
                minlb = min(minlb, lbI.lo)
                continue
        if done + len(stack) > max_boxes or t1 - t0 < 1e-9:
            raise AssertionError(f"cover failed near t=[{t0},{t1}] xi=[{x0},{xmax}] Fc={Fc}")
        tm, xm = 0.5 * (t0 + t1), 0.5 * (x0 + xmax)
        stack += [(t0, tm, x0, xm), (tm, t1, x0, xm), (t0, tm, xm, xmax), (tm, t1, xm, xmax)]
    if log:
        log(f"region t in [{a},{b}], v >= {nu}: {done} boxes positive (min lb {minlb:.4g}), {q0} boxes in Q0")
    return done, q0, minlb


# Our regions (dyadic).  Together with Lemma 5.3 (t <= 0.002), Lemma 5.4(a)
# (0.002<=t<=1.4, v<=5e-5), 5.4(b) (1.4<=t<=4.1, v<=0.1), 5.4(c) (t>=4.1) and Q0
# they cover t>0, 0<=d<=t:  1/512 < 0.002, 2^-15 < 5e-5, 45/32 > 1.4, 3/32 < 0.1,
# 33/8 > 4.1.
REGIONS = [(1 / 512, 0.125, 2.0**-15), (0.125, 0.3125, 2.0**-15), (0.3125, 0.4375, 2.0**-15),
           (0.4375, 1.40625, 2.0**-15), (1.40625, 4.125, 0.09375)]


# ---- exact-rational enclosure (for the 3e-17 margin of c_L > 0.382709087918735)
def _flog(q: Fr, N=40):
    """Rational bounds (lo, hi) for log q, q > 0."""
    from interval import _L2LO, _L2HI
    e = 0
    while q > Fr(4, 3):
        q /= 2; e += 1
    while q < Fr(2, 3):
        q *= 2; e -= 1
    z = (q - 1) / (q + 1)               # |z| <= 1/5
    s = 2 * sum(z ** (2 * j + 1) / (2 * j + 1) for j in range(N))
    tail = 2 * abs(z) ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))
    lo, hi = s - tail, s + tail
    if e >= 0:
        return lo + e * Fr(_L2LO), hi + e * Fr(_L2HI)
    return lo + e * Fr(_L2HI), hi + e * Fr(_L2LO)


def _rnd(q: Fr, up: bool, bits=200) -> Fr:
    import math
    n = q * 2**bits
    return Fr(math.ceil(n) if up else math.floor(n), 2**bits)


def _fH(lo: Fr, hi: Fr):
    """Rational bounds for H on [lo, hi] subset of (0,1), via monotonicity pieces."""
    def pt(x, up):
        a, b = _flog(x)
        c_, d = _flog(1 - x)
        return _rnd(-x * (a if up else b) - (1 - x) * (c_ if up else d), up)
    if hi <= Fr(1, 2):
        return pt(lo, False), pt(hi, True)
    if lo >= Fr(1, 2):
        return pt(hi, False), pt(lo, True)
    raise ValueError


def cL_exact_bounds():
    lo, hi = xstar_bracket()  # width 2^-71
    Hl, Hh = _fH(lo, hi)            # x* > 1/2: H decreasing
    Al, Ah = _fH(lo * lo, hi * hi)  # x*^2 < 1/2: H increasing
    assert hi * hi < Fr(1, 2) and lo > Fr(1, 2)
    ms_lo, ms_hi = lo * Hl / Ah, hi * Hh / Al
    return 1 - ms_hi, 1 - ms_lo


def interval_checks(verbose=True, regions=True):
    say = print if verbose else (lambda *a: None)
    k = setup()
    say("x*   in", k["xs"]); say("m*   in", k["ms"]); say("beta in", k["beta"])
    say("t*   in", k["ts"]); say("c_L  in", k["cL"]); say("c0   in", k["c0"])
    cl_lo, cl_hi = cL_exact_bounds()
    assert cl_lo > Fr("0.382709087918735") and k["cL"].lo <= cl_hi and cl_lo <= k["cL"].hi
    say(f"c_L in [{float(cl_lo)!r}, {float(cl_hi)!r}] (exact rationals; c_L - 0.382709087918735 >= {float(cl_lo - Fr('0.382709087918735')):.3g})")
    assert 0 < k["beta"].lo and k["beta"].hi < 1
    c0 = k["c0"]
    assert c0.lo > 0.5
    # Lemma 5.3: zeta(0.002) > 0 and e^0.002 < 2 c0
    t = IF(Fr(2, 1000))
    zeta = 2.0 * c0 * (1.0 - ilog(2.0 * t)) - 1.0 - iexp(t) * (-ilog(t) + t)
    assert zeta.lo > 0 and iexp(t).hi < (2.0 * c0).lo
    say("zeta(0.002) in", zeta)
    # Lemma 5.4 (a), (b), (c)
    a_ = (c0 - 0.5) * G_val(IF(Fr(4, 1000))) - 0.5 * G_val(IF(Fr(5, 100000)))
    b_ = (c0 - 0.5) * G_val(IF(Fr(28, 10))) - 0.5 * G_val(IF(Fr(1, 10)))
    c_ = c0 * (IF(Fr(92, 10)) - iexp(IF(Fr(-82, 10)))) - IF(Fr(51, 10))
    assert a_.lo > 0 and b_.lo > 0 and c_.lo > 0
    say("Lemma 5.4 scalars:", a_, b_, c_)
    # tangency point inside the local rectangle
    assert Q0_T0 < k["ts"].lo and k["ts"].hi < Q0_T1
    t0 = time.time()
    nb, worst = check_Q0()
    say(f"Q0 Hessian PD: {nb} boxes; min Ftt {worst[0]:.4g}, Fdd {worst[1]:.4g}, det {worst[2]:.4g}"
        f" ({time.time()-t0:.1f}s)")
    out = {"Q0": (nb, worst)}
    if regions:
        assert Fr(REGIONS[0][0]) < Fr(2, 1000) and Fr(2.0**-15) < Fr(5, 100000)
        assert Fr(45, 32) > Fr(14, 10) and Fr(3, 32) < Fr(1, 10) and Fr(33, 8) > Fr(41, 10)
        for (a, b, nu) in REGIONS:
            t0 = time.time()
            out[(a, b, nu)] = cover_region(a, b, nu, log=say)
            say(f"   ({time.time()-t0:.1f}s)")
            sys.stdout.flush()
    return out


if __name__ == "__main__":
    if "--region" in sys.argv:          # run one region of the cover only
        setup()
        i = int(sys.argv[sys.argv.index("--region") + 1])
        t0 = time.time()
        r = cover_region(*REGIONS[i], log=print)
        print(f"REGION {i} {REGIONS[i]} OK {r} {time.time()-t0:.1f}s")
    else:
        exact_checks()
        interval_checks(regions="--no-regions" not in sys.argv)
        print("DONE")
