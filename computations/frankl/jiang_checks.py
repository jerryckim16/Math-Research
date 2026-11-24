"""Independent re-verification of the finite computations in
Jiang, arXiv:2609.08291 ("p >= 1531541/4000000 = 0.38288525").

Reduction (their Prop. "Entropy reduction", analytic, read): p >= 1 - m follows from
  (K)  K(x,y) = h(xy + a(x)a(y)(min(x,y) - xy)) >= psi(x) psi(y),
  (M)  2m [w0 h(xy) + w4 psi(x) psi(y)] >= x h(y) + y h(x)      on [0,1]^2.
Their computer part (Appendix B, Python Decimal, 35 digits) has four phases, all
re-done here with OUR OWN code (outward-rounded doubles, interval.py, plus the
accurate G / H evaluation of costa_sadhu_thm12.py):
  scalars  - the 12 scalar signs used by the analytic boundary estimates;
  bridge   - h(A y) >= s(A) phi(y) on [1/16, A]  (1D mean-value cover);
  kernel   - h(r) - phi(x) phi(y) > 0 on [1/16, 15/16]^2, via the three coordinate
             maps (a = 1 on [1/16,1/2]; x = x(p), a = p on [1/2, 1/sqrt2]; a = 0 on
             [1/sqrt2, 15/16]) and the six unordered pairs of maps;
  mixture  - F(t,xi) = k0 G(2t) + m w4 P(u) P(v) - (G(u)+G(v))/2 > 0 on
             [0.001, 16] x [0, 1], u = t(1+xi), v = t(1-xi), with the two analytic
             edge bounds (edge1, edge2) next to xi = 1.
The analytic parts (reduction, ceiling, geometric concavity, profile ordering,
lower/upper strips, small t, large t, edge estimates) were read, not machine-checked.
"""
from __future__ import annotations

import sys
import time
from fractions import Fraction as Fr

from interval import I, IF, H, ilog, iexp, isqrt_, LN2
from costa_sadhu_thm12 import G_all, G_val, Hr

# ------------------------------------------------------------------ parameters (exact)
M = Fr(2468459, 4000000)
W0 = Fr(8102221, 10**7)
W4 = Fr(1897779, 10**7)
A_ = Fr(716, 1000)
B_ = Fr(721, 1000)
Z_ = Fr(181, 256)
SIG = Fr(99999999, 10**8)
XS = Fr(172727, 250000)
LOW, HIGH = Fr(1, 16), Fr(15, 16)
TMIN, TMAX = Fr(1, 1000), Fr(16)

Mi, W4i, K0 = IF(M), IF(W4), IF(M * W0)
MW4 = IF(M * W4)
Ai, Bi, Zi, SIGi, XSi = IF(A_), IF(B_), IF(Z_), IF(SIG), IF(XS)
HSTAR = H(XSi)
SQH = isqrt_(HSTAR)


def Hp_I(x: I) -> I:
    """h'(x) = log((1-x)/x), decreasing; (1-x)/x has exact range."""
    return ilog((1.0 - x) / x)


KSTAR = Hp_I(XSi) / (2.0 * HSTAR)
HZ2 = H(Zi.sq())           # h(z^2)
INV_BA = 1.0 / (Bi - Ai)
RT_HALF = isqrt_(I(0.5))


def E(x: I) -> I:
    d = x - XSi
    return -KSTAR * d - IF(Fr(7, 10)) * d.sq()


def Ep(x: I) -> I:
    return -KSTAR - IF(Fr(7, 5)) * (x - XSi)


def hI(x: I) -> I:
    return Hr(x)


# ------------------------------------------------------------------ profiles in x
def phi_piece(x: I, k: int):
    """phi = sigma sqrt(D h / h*) e^E on piece k (0: x<=1/2, 1: 1/2<=x<=z, 2: x>=z)."""
    hx, hpx, e, ep = hI(x), Hp_I(x), iexp(E(x)), Ep(x)
    if k == 0:                          # D = h: phi = sigma h e^E / sqrt(h*)
        f = SIGi * hx * e / SQH
        return f, f * (hpx / hx + ep)
    if k == 1:                          # D = ln 2
        f = SIGi * isqrt_(LN2 * hx / HSTAR) * e
        return f, f * (hpx / (2.0 * hx) + ep)
    x2 = x.sq()                         # D = ln2 h(x^2)/h(z^2)
    hx2 = hI(x2)
    f = SIGi * isqrt_(LN2 * hx2 * hx / (HZ2 * HSTAR)) * e
    return f, f * (x * Hp_I(x2) / hx2 + hpx / (2.0 * hx) + ep)


def _pieces(x: I, cuts):
    """Yield (subinterval, index) for the pieces [cuts[k], cuts[k+1]] meeting x.
    cuts are intervals (enclosing exact breakpoints); a piece is used on a superset."""
    for k in range(len(cuts) - 1):
        lo = max(x.lo, cuts[k].lo)
        hi = min(x.hi, cuts[k + 1].hi)
        if lo <= hi:
            yield I(lo, hi), k


def _hull(pairs):
    f = pairs[0][0]
    d = pairs[0][1]
    for a, b in pairs[1:]:
        f, d = f.hull(a), d.hull(b)
    return f, d


PHI_CUTS = [I(0.0), I(0.5), Zi, I(1.0)]


def phi(x: I):
    return _hull([phi_piece(xx, k) for xx, k in _pieces(x, PHI_CUTS)])


def sfun(x: I):
    x2 = x.sq()
    s = isqrt_(hI(x2))
    return s, x * Hp_I(x2) / s


def psi(x: I):
    out = []
    for xx, k in _pieces(x, [I(0.0), Ai, Bi, I(1.0)]):
        if k == 0:
            out.append(phi(xx))
        elif k == 2:
            out.append(sfun(xx))
        else:
            p, pp = phi(xx)
            s, sp = sfun(xx)
            th = (xx - Ai) * INV_BA
            out.append(((1.0 - th) * p + th * s, (1.0 - th) * pp + th * sp + (s - p) * INV_BA))
    return _hull(out)


# ------------------------------------------------------------------ P(u) = psi(e^-u)/e^-u
U_LB = -ilog(Bi)          # x >= B  <=>  u <= -log B
U_LA = -ilog(Ai)
U_LH = LN2                # x <= 1/2 <=> u >= log 2


def P_all(u: I):
    """(P, P') on u (u > 0), by pieces in u:
       u <= -log B: P = sqrt(G(2u)), P' = G'(2u)/sqrt(G(2u))       (psi = s)
       u >= log 2 : P = sigma G(u) e^{E(x)}/sqrt(h*), P' = P (G'/G - x E'(x))  (phi piece 0)
       otherwise  : P = psi(x)/x, P' = psi(x)/x - psi'(x),  x = e^-u."""
    out = []
    if u.lo <= U_LB.hi:
        uu = I(u.lo, min(u.hi, U_LB.hi))
        g = G_all(2.0 * uu)
        sg = isqrt_(g[0])
        out.append((sg, g[1] / sg))
    if u.hi >= U_LB.lo and u.lo <= U_LH.hi:
        uu = I(max(u.lo, U_LB.lo), min(u.hi, U_LH.hi))
        x = iexp(-uu)
        f, fp = psi(x)
        q = f / x
        out.append((q, q - fp))
    if u.hi >= U_LH.lo:
        uu = I(max(u.lo, U_LH.lo), u.hi)
        x = iexp(-uu)
        g = G_all(uu)
        p = SIGi * g[0] * iexp(E(x)) / SQH
        out.append((p, p * (g[1] / g[0] - x * Ep(x))))
    return _hull(out)


def P_val(u: float) -> I:
    return P_all(I(u))[0]


# ------------------------------------------------------------------ scalar checks
def scalar_checks(verbose=True):
    say = print if verbose else (lambda *a: None)
    assert W0 + W4 == 1 and 1 - M == Fr(1531541, 4000000)
    assert M * W0 - Fr(1, 2) == Fr(347439, 40000000000000)          # k0 - 1/2 = 8.69e-9
    assert Fr(1, 2) < XS < Fr(7, 10) and A_ > Z_ and Z_**2 + Z_ > 1
    assert Fr(1, 2) < Z_ and 2 * Z_**2 < 1 < 2 * A_**2                # 1/2 < z < 1/sqrt2 < A
    sA, _ = sfun(Ai)
    pA, _ = phi(Ai)
    C_min = SIGi / SQH * iexp(E(I(0.0)))
    C_b = SIGi / SQH * iexp(E(IF(LOW)))
    P0 = SIGi * LN2 / SQH * iexp(E(I(0.5)))
    C_g = SIGi * isqrt_(2.0 * LN2 / (HSTAR * HZ2)) * iexp(E(I(1.0)))
    Hh = IF(HIGH)
    C_t = SIGi / Hh * isqrt_(LN2 / HZ2 * hI(Hh.sq()) * hI(Hh) / HSTAR) * iexp(E(I(1.0)))
    T = IF(TMIN)
    checks = {
        "E'(1) > 0": Ep(I(1.0)),
        "1 - C_g C_t": 1.0 - C_g * C_t,
        "1 - C_b P0": 1.0 - C_b * P0,
        "1 - 2 C_b P0": 1.0 - 2.0 * C_b * P0,
        "1 - E'(1/2) - h'(z^2)/h(z^2)": 1.0 - Ep(I(0.5)) - Hp_I(Zi.sq()) / HZ2,
        "A - s(A) C_b": Ai - sA * C_b,
        "s(A) - phi(A)": sA - pA,
        "-(h'(A)/(2h(A)) + E'(A))": -(Hp_I(Ai) / (2.0 * hI(Ai)) + Ep(Ai)),
        "k0 - 1/2": K0 - 0.5,
        "2 m w4 (1 - ln 4T) - 1": 2.0 * MW4 * (1.0 - ilog(4.0 * T)) - 1.0,
        "e^{-2T} - B": iexp(-2.0 * T) - Bi,
        "16 m w4 C^2 - 1/2": 16.0 * MW4 * C_min.sq() - 0.5,
    }
    for k, v in checks.items():
        assert v.lo > 0, (k, v)
    for k, v in checks.items():
        say(f"  scalar {k:32s} in [{v.lo:.10g}, {v.hi:.10g}]")
    return checks, C_min


C_MIN = None


# ------------------------------------------------------------------ bridge
def cover_1d(f, a, b, n0, min_w=1e-13):
    """f(lo, hi) -> rigorous lower bound on [lo, hi]."""
    h = (b - a) / n0
    stack = [(a + h * i, a + h * (i + 1) if i < n0 - 1 else b) for i in range(n0)]
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


def verify_bridge(verbose=True):
    sA, _ = sfun(Ai)

    def b(lo, hi):
        Y = I(lo, hi)
        p, pp = phi(Y)
        val = hI(Ai * Y) - sA * p
        if val.lo > 0:
            return val.lo
        c = 0.5 * (lo + hi)
        fc = hI(Ai * I(c)) - sA * phi(I(c))[0]
        d = Ai * Hp_I(Ai * Y) - sA * pp
        rad = max((I(hi) - I(c)).hi, (I(c) - I(lo)).hi)
        return (fc - I(max(abs(d.lo), abs(d.hi))) * I(rad)).lo

    lo = float(LOW)
    hi = float(A_) * (1 + 2**-52)       # float just above 0.716 (covers [1/16, A])
    assert Fr(hi) >= A_
    t0 = time.time()
    n, mn = cover_1d(b, lo, hi, 64)
    if verbose:
        print(f"bridge h(Ay) - s(A)phi(y) > 0 on [1/16, A]: {n} cells, min lower bound {mn:.6g} ({time.time()-t0:.1f}s)")
    return n, mn


# ------------------------------------------------------------------ kernel
def coord(p: I, br: int):
    """(x, a, x', a') for the coordinate map `br` at parameter p in [0,1]."""
    if br == 0:
        sl = IF(Fr(1, 2) - LOW)
        return IF(LOW) + sl * p, I(1.0), sl, I(0.0)
    if br == 2:
        sl = IF(HIGH) - RT_HALF
        return RT_HALF + sl * p, I(0.0), sl, I(0.0)
    p2 = p.sq()
    R = isqrt_((p2 - 1.0).sq() + 1.0)
    d = p2 + R
    x = 1.0 / d
    xp = -2.0 * p / d.sq() * (1.0 + (p2 - 1.0) / R)
    return x, p, xp, I(1.0)


def coord_x_exact_range(br):
    return {0: (LOW, Fr(1, 2)), 1: None, 2: None}[br]


R_LO, R_HI = IF(LOW * LOW).lo, IF(HIGH).hi


def kernel_gap(P: I, Q: I, i: int, j: int, deriv=False):
    x, a, xp, ap = coord(P, i)
    y, b, yp, bp = coord(Q, j)
    # clamp x, y to their true ranges (all maps land in [1/16, 15/16])
    x = x.intersect(I(IF(LOW).lo, IF(HIGH).hi))
    y = y.intersect(I(IF(LOW).lo, IF(HIGH).hi))
    a = a.intersect(I(0.0, 1.0))
    b = b.intersect(I(0.0, 1.0))
    xy = x * y
    if x.hi <= y.lo:
        d, da, db = x, xp, I(0.0)
    elif y.hi <= x.lo:
        d, da, db = y, I(0.0), yp
    else:
        d = I(min(x.lo, y.lo), min(x.hi, y.hi))
        da, db = xp * I(0.0, 1.0), yp * I(0.0, 1.0)
    ab = a * b
    r = xy + ab * (d - xy)
    # true range: xy <= r <= min(x, y), and 1/256 <= r <= 15/16
    r = r.intersect(I(max(xy.lo, R_LO), min(d.hi, R_HI)))
    fx, fxp = phi(x)
    fy, fyp = phi(y)
    val = hI(r) - fx * fy
    if not deriv:
        return val
    hpr = Hp_I(r)
    ra = xp * y + ap * b * (d - xy) + ab * (da - xp * y)
    rb = x * yp + a * bp * (d - xy) + ab * (db - x * yp)
    return val, hpr * ra - fxp * xp * fy, hpr * rb - fx * fyp * yp


def _mv_bound(f_center, dA, dB, radA, radB):
    return (f_center - I(max(abs(dA.lo), abs(dA.hi))) * I(radA)
            - I(max(abs(dB.lo), abs(dB.hi))) * I(radB)).lo


def verify_kernel_square(i, j, n0=8, max_boxes=3 * 10**6, log=None):
    t0 = time.time()
    h = 1.0 / n0
    stack = [(h * k, h * (k + 1), h * l, h * (l + 1)) for k in range(n0) for l in range(n0)]
    done, minlb, where = 0, float("inf"), None
    while stack:
        p0, p1, q0, q1 = stack.pop()
        P, Q = I(p0, p1), I(q0, q1)
        val, dA, dB = kernel_gap(P, Q, i, j, True)
        if val.lo > 0:
            lb = val.lo
        else:
            pc, qc = 0.5 * (p0 + p1), 0.5 * (q0 + q1)
            fc = kernel_gap(I(pc), I(qc), i, j)
            if fc.hi < 0:
                raise AssertionError(f"KERNEL NEGATIVE at maps {(i, j)} p={pc} q={qc}: {fc}")
            lb = _mv_bound(fc, dA, dB, 0.5 * (p1 - p0), 0.5 * (q1 - q0))
        if lb > 0:
            done += 1
            if lb < minlb:
                minlb, where = lb, (p0, p1, q0, q1)
            continue
        if done + len(stack) > max_boxes or p1 - p0 < 1e-12:
            raise AssertionError(f"kernel cover failed at maps {(i, j)} box {(p0, p1, q0, q1)}")
        # split along the coordinate with the larger derivative contribution
        eA = max(abs(dA.lo), abs(dA.hi)) * (p1 - p0)
        eB = max(abs(dB.lo), abs(dB.hi)) * (q1 - q0)
        if eA >= eB:
            pm = 0.5 * (p0 + p1)
            stack += [(p0, pm, q0, q1), (pm, p1, q0, q1)]
        else:
            qm = 0.5 * (q0 + q1)
            stack += [(p0, p1, q0, qm), (p0, p1, qm, q1)]
    if log:
        log(f"kernel maps ({i},{j}): {done} boxes, min lower bound {minlb:.4g} at {where} ({time.time()-t0:.1f}s)")
    return done, minlb, where


# ------------------------------------------------------------------ mixture
def mixture_val(t: float, xi: float) -> I:
    T, X = I(t), I(xi)
    u, v = T * (1.0 + X), T * (1.0 - X)
    return K0 * G_val(2.0 * T) + MW4 * P_all(u)[0] * P_all(v)[0] - 0.5 * (G_val(u) + G_val(v))


def mixture_derivs(T: I, X: I):
    u, v = T * (1.0 + X), T * (1.0 - X)
    pu, pup = P_all(u)
    pv, pvp = P_all(v)
    gu, gv = G_all(u)[1], G_all(v)[1]
    Ft = 2.0 * K0 * G_all(2.0 * T)[1] + MW4 * ((1.0 + X) * pup * pv + (1.0 - X) * pu * pvp) \
        - 0.5 * ((1.0 + X) * gu + (1.0 - X) * gv)
    Fx = T * (MW4 * (pup * pv - pu * pvp) - 0.5 * (gu - gv))
    return Ft, Fx


MIX_KNOTS = [0.001, 0.01, 0.1, 0.3, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]


def verify_mixture_strip(a, b, max_boxes=4 * 10**6, log=None):
    """F > 0 on [a, b] x [0, 1].  a, b floats with a <= exact knot (we cover a superset)."""
    global C_MIN
    if C_MIN is None:
        C_MIN = scalar_checks(verbose=False)[1]
    t0c = time.time()
    k0h = K0 - 0.5
    tail = (-ilog(Bi)).lo
    stack = [(a, b, 0.0, 1.0)]
    done = edges = 0
    minlb, where = float("inf"), None
    while stack:
        t0, t1, x0, x1 = stack.pop()
        vmax = (I(t1) * (1.0 - I(x0))).hi
        # edge bounds (analytic, see eq. edge1/edge2 in the paper)
        gv = G_all(I(vmax))[0].hi if vmax > 0 else 0.0
        g2t = G_all(I(2.0 * t0))[0]
        e1 = (k0h * g2t - 0.5 * I(gv)).lo
        lb = None
        if e1 > 0:
            lb = e1
        elif vmax <= tail:
            e2 = 2.0 * MW4 * C_MIN * G_all(I(t0))[0]
            if gv <= e2.sq().lo:
                lb = (k0h * g2t).lo
        if lb is not None and lb > 0:
            edges += 1
            done += 1
            if lb < minlb:
                minlb, where = lb, (t0, t1, x0, x1, "edge")
            continue
        if x1 >= 1.0:                       # touches v = 0 and no edge bound: split xi only
            xm = 0.5 * (x0 + x1)
            stack += [(t0, t1, x0, xm), (t0, t1, xm, x1)]
            continue
        tc, xc = 0.5 * (t0 + t1), 0.5 * (x0 + x1)
        fc = mixture_val(tc, xc)
        if fc.hi < 0:
            raise AssertionError(f"MIXTURE NEGATIVE at t={tc} xi={xc}: {fc}")
        Ft, Fx = mixture_derivs(I(t0, t1), I(x0, x1))
        lb = _mv_bound(fc, Ft, Fx, 0.5 * (t1 - t0), 0.5 * (x1 - x0))
        if lb > 0:
            done += 1
            if lb < minlb:
                minlb, where = lb, (t0, t1, x0, x1)
            continue
        if done + len(stack) > max_boxes or t1 - t0 < 1e-13:
            raise AssertionError(f"mixture cover failed at {(t0, t1, x0, x1)} fc={fc}")
        eT = max(abs(Ft.lo), abs(Ft.hi)) * (t1 - t0)
        eX = max(abs(Fx.lo), abs(Fx.hi)) * (x1 - x0)
        if eT >= eX:
            tm = 0.5 * (t0 + t1)
            stack += [(t0, tm, x0, x1), (tm, t1, x0, x1)]
        else:
            xm = 0.5 * (x0 + x1)
            stack += [(t0, t1, x0, xm), (t0, t1, xm, x1)]
    if log:
        log(f"mixture t in [{a},{b}]: {done} boxes ({edges} by edge bounds), min lower bound {minlb:.4g} at {where} ({time.time()-t0c:.1f}s)")
    return done, edges, minlb, where


def mixture_strips():
    # [0.001, 16]: the float 0.001 is above 1/1000, so start from a float below it.
    lo = float(TMIN)
    if Fr(lo) > TMIN:
        lo = __import__("math").nextafter(lo, 0.0)
    ks = [lo] + MIX_KNOTS[1:]
    return list(zip(ks[:-1], ks[1:]))


KERNEL_PAIRS = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "quick":
        scalar_checks()
        verify_bridge()
    elif args[0] == "kernel":
        i, j = KERNEL_PAIRS[int(args[1])]
        r = verify_kernel_square(i, j, log=print)
        print(f"KERNEL {(i, j)} OK {r}")
    elif args[0] == "mixture":
        a, b = mixture_strips()[int(args[1])]
        r = verify_mixture_strip(a, b, log=print)
        print(f"MIXTURE STRIP {(a, b)} OK {r}")
