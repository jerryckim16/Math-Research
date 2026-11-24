"""Rigorous verification of the one-variable inequality behind the (3-sqrt5)/2 bound.

Claim (Alweiss-Huang-Sellke, Claim 1 of arXiv:2211.11731; Boppana 1985/2023):
with phi = (sqrt5 - 1)/2 and H(x) = -x log x - (1-x) log(1-x),

    G(x) := phi * H(x^2) - x * H(x) >= 0      for all x in [0, 1],

with equality exactly at x in {0, phi, 1}.  (AHS only need x in [phi, 1].)
Equivalently h(x^2) >= ((1+sqrt5)/2) x h(x), Boppana's inequality.

Proof structure (every numbered step is checked below; nothing uses floats
without outward rounding):

  R0  (0, 1/100]:  analytic.  H(x^2) >= 2 x^2 log(1/x) and
      x H(x) <= x^2 log(1/x) + x^2  (because -(1-x)log(1-x) <= x), so
      G(x) >= x^2 [ (2 phi - 1) log(1/x) - 1 ],  and (2phi-1) log 100 > 1.
  R1  [1 - 1/4096, 1):  analytic, y = 1-x, u = 1-x^2 = 2y - y^2 in
      [y(2-b), 2y] (b = 1/4096) and 2y <= 1/e, so H(x^2) = H(u) >= u log(1/u)
      >= y(2-b)(log(1/y) - log 2) (t log(1/t) increases on [0,1/e]), and
      x H(x) <= H(y) <= y log(1/y) + y.  Hence
      G >= y [ (phi(2-b) - 1) log(1/y) - phi(2-b) log 2 - 1 ],
      which is increasing in log(1/y) >= log 4096, checked > 0 at y = b.
  R2  [1/2, 4/5] (contains phi):  G(phi) = 0 and G'(phi) = 0 exactly
      (phi^2 = 1 - phi; see the problem file), and G'' > 0 on [1/2, 4/5] by
      interval arithmetic, so G(x) = int_phi^x (x-s) G''(s) ds > 0 for x != phi.
  R3  [1/100, 1/2] and [4/5, 1-1/4096]:  adaptive bisection; on each cell
      G is enclosed by the mean-value form G(m) + G'(cell)(cell - m) intersected
      with the natural extension; the cell is accepted when the lower bound > 0.

Run:  python3 verify_boppana.py      (about a few seconds)
"""
from __future__ import annotations

from fractions import Fraction

from interval import I, IF, H, Hnaive, ilog, isqrt_, LN2, frac_lo, frac_hi

# ------------------------------------------------------------------ phi
# phi is the positive root of p(t) = t^2 + t - 1.  Bracket it by floats and
# certify the bracket with exact rational arithmetic.
_s5 = isqrt_(I(5.0))
PHI = (_s5 - 1.0) / 2.0
assert Fraction(PHI.lo) ** 2 + Fraction(PHI.lo) - 1 < 0 < Fraction(PHI.hi) ** 2 + Fraction(PHI.hi) - 1


def G(x: I) -> I:
    x2 = x.sq()
    return PHI * H(x2) - x * H(x)


def Gp(x: I) -> I:
    # G'(x) = 2 phi x log((1-x^2)/x^2) - H(x) - x log((1-x)/x)
    x2 = x.sq()
    return 2.0 * PHI * x * ilog((1.0 - x2) / x2) - H(x) - x * ilog((1.0 - x) / x)


def Gpp(x: I) -> I:
    # G''(x) = phi [2 log((1-x^2)/x^2) - 4/(1-x^2)] - 2 log((1-x)/x) + 1/(1-x)
    x2 = x.sq()
    return PHI * (2.0 * ilog((1.0 - x2) / x2) - 4.0 / (1.0 - x2)) - 2.0 * ilog((1.0 - x) / x) + 1.0 / (1.0 - x)


def enclose_G(a: float, b: float) -> I:
    X = I(a, b)
    m = 0.5 * (a + b)
    M = I(m)
    mv = G(M) + Gp(X) * (X - M)
    nat = PHI * Hnaive(X.sq()) - X * Hnaive(X)
    return mv.intersect(nat) if (mv.hi >= nat.lo and nat.hi >= mv.lo) else mv


def prove_positive(f_enclose, a: float, b: float, min_width=1e-12, max_cells=10**6):
    """Adaptive bisection: returns (#cells, min lower bound) or raises."""
    stack = [(a, b)]
    cells = 0
    minlb = float("inf")
    while stack:
        lo, hi = stack.pop()
        e = f_enclose(lo, hi)
        if e.lo > 0:
            cells += 1
            minlb = min(minlb, e.lo)
            continue
        if hi - lo < min_width or cells > max_cells:
            raise AssertionError(f"could not certify on [{lo}, {hi}]: {e}")
        mid = 0.5 * (lo + hi)
        stack.append((mid, hi))
        stack.append((lo, mid))
    return cells, minlb


def run(verbose=True):
    out = {}
    # R0
    c = (2.0 * PHI - 1.0) * ilog(I(100.0)) - 1.0
    assert c.lo > 0, c
    out["R0"] = f"(2phi-1) log 100 - 1 in {c} > 0"
    # R1
    b = IF(Fraction(1, 4096))
    k = PHI * (2.0 - b)
    assert (k - 1.0).lo > 0
    # 2y <= 1/e for y <= b:  2b < 1/e  <=>  log(2b) < -1
    assert ilog(2.0 * b).hi < -1.0
    val = (k - 1.0) * ilog(I(4096.0)) - k * LN2 - 1.0
    assert val.lo > 0, val
    out["R1"] = f"(phi(2-b)-1) log 4096 - phi(2-b) log 2 - 1 in {val} > 0"
    # R2
    cells, lb = prove_positive(lambda lo, hi: Gpp(I(lo, hi)), 0.5, 0.8)
    assert 0.5 < PHI.lo and PHI.hi < 0.8
    out["R2"] = f"G''>0 on [1/2,4/5]: {cells} cells, min lower bound {lb:.4g}"
    # R3
    c1, lb1 = prove_positive(enclose_G, 0.01, 0.5)
    c2, lb2 = prove_positive(enclose_G, 0.8, 1.0 - 1.0 / 4096)
    out["R3"] = (f"G>0 on [1/100,1/2]: {c1} cells (min lb {lb1:.3g}); "
                 f"on [4/5,1-1/4096]: {c2} cells (min lb {lb2:.3g})")
    if verbose:
        for k_, v in out.items():
            print(k_, ":", v)
        print("VERIFIED: phi*H(x^2) >= x*H(x) on [0,1], equality only at 0, phi, 1.")
    return out


if __name__ == "__main__":
    run()
