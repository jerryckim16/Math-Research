"""Small rigorous interval arithmetic on IEEE doubles (pure Python, no deps).

Soundness argument
------------------
* IEEE-754 double +, -, *, / and sqrt are correctly rounded (error <= 1/2 ulp).
  Every result here is pushed one ulp outward with math.nextafter, so the
  returned interval contains the exact real result of the operation applied to
  any reals in the input intervals.
* log is NOT taken from libm.  We use the exact decomposition x = m * 2^e
  (math.frexp is exact), shift m into [1/sqrt2, sqrt2), and evaluate
      log m = 2 * sum_{j>=0} z^(2j+1)/(2j+1),   z = (m-1)/(m+1),  |z| < 0.1716,
  in interval arithmetic, adding a rigorous enclosure of the tail
      |tail after N terms| <= 2 |z|^(2N+1) / ((2N+1)(1 - z^2)).
  log 2 is enclosed by the same series computed in exact rational arithmetic
  (log 2 = 2 atanh(1/3)), then rounded outward.
* exp (used only for optional checks) uses exp(x) = exp(r)^(2^k) with a Taylor
  series and Lagrange remainder, all in interval arithmetic.

Everything is deterministic and depends only on IEEE arithmetic of the host.
`test_frankl.py` cross-checks the enclosures against exact Fraction bounds and,
if available, against mpmath.iv.
"""
from __future__ import annotations

import math
from fractions import Fraction

INF = math.inf


def _dn(x: float) -> float:
    return math.nextafter(x, -INF)


def _up(x: float) -> float:
    return math.nextafter(x, INF)


class I:
    """Closed interval [lo, hi] with float endpoints."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        if isinstance(lo, Fraction) or isinstance(hi, Fraction) or isinstance(lo, int) and abs(lo) > 2**53:
            lo, hi = frac_lo(Fraction(lo)), frac_hi(Fraction(hi))
        self.lo = float(lo)
        self.hi = float(hi)
        if not (self.lo <= self.hi):
            raise ValueError(f"bad interval [{lo}, {hi}]")
        # exact conversion check for ints/floats given directly
        if isinstance(lo, int) and float(lo) != lo:
            self.lo = _dn(self.lo)
        if isinstance(hi, int) and float(hi) != hi:
            self.hi = _up(self.hi)

    # ----- helpers
    @staticmethod
    def _c(o):
        return o if isinstance(o, I) else I(o)

    def __repr__(self):
        return f"I[{self.lo!r}, {self.hi!r}]"

    def width(self):
        return self.hi - self.lo

    def mid(self):
        return 0.5 * (self.lo + self.hi)

    def contains(self, x):
        return self.lo <= x <= self.hi

    # ----- arithmetic
    def __add__(self, o):
        o = I._c(o)
        return I(_dn(self.lo + o.lo), _up(self.hi + o.hi))

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, o):
        o = I._c(o)
        return I(_dn(self.lo - o.hi), _up(self.hi - o.lo))

    def __rsub__(self, o):
        return I._c(o) - self

    def __mul__(self, o):
        o = I._c(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return I(_dn(min(ps)), _up(max(ps)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = I._c(o)
        if o.lo <= 0.0 <= o.hi:
            raise ZeroDivisionError(f"division by interval containing 0: {o}")
        qs = (self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi)
        return I(_dn(min(qs)), _up(max(qs)))

    def __rtruediv__(self, o):
        return I._c(o) / self

    def sq(self):
        if self.lo >= 0:
            return I(_dn(self.lo * self.lo), _up(self.hi * self.hi))
        if self.hi <= 0:
            return I(_dn(self.hi * self.hi), _up(self.lo * self.lo))
        m = max(-self.lo, self.hi)
        return I(0.0, _up(m * m))

    def __pow__(self, k: int):
        assert isinstance(k, int) and k >= 0
        r = I(1.0)
        for _ in range(k):
            r = r * self
        return r

    def hull(self, o):
        o = I._c(o)
        return I(min(self.lo, o.lo), max(self.hi, o.hi))

    def intersect(self, o):
        lo, hi = max(self.lo, o.lo), min(self.hi, o.hi)
        if lo > hi:
            raise ValueError("empty intersection (enclosure bug)")
        return I(lo, hi)


# ---------------------------------------------------------------- conversions
def frac_lo(q: Fraction) -> float:
    """Largest float <= q."""
    f = float(q)
    if Fraction(f) > q:
        f = _dn(f)
    return f


def frac_hi(q: Fraction) -> float:
    f = float(q)
    if Fraction(f) < q:
        f = _up(f)
    return f


def IF(q) -> I:
    """Tight interval around a rational."""
    q = Fraction(q)
    return I(frac_lo(q), frac_hi(q))


# ---------------------------------------------------------------- sqrt
def isqrt_(x: I) -> I:
    if x.lo < 0:
        raise ValueError("sqrt of negative")
    return I(_dn(math.sqrt(x.lo)) if x.lo > 0 else 0.0, _up(math.sqrt(x.hi)))


# ---------------------------------------------------------------- log
def _ln2_fraction_bounds(nterms: int = 40):
    # log 2 = 2 atanh(1/3) = 2 sum z^(2j+1)/(2j+1), z = 1/3
    z = Fraction(1, 3)
    s = Fraction(0)
    for j in range(nterms):
        s += z ** (2 * j + 1) / (2 * j + 1)
    s *= 2
    tail = 2 * z ** (2 * nterms + 1) / ((2 * nterms + 1) * (1 - z * z))
    return s, s + tail


_L2LO, _L2HI = _ln2_fraction_bounds()
LN2 = I(frac_lo(_L2LO), frac_hi(_L2HI))
_SQRT2 = math.sqrt(2.0)


def _log_point(x: float, nterms: int = 14) -> I:
    """Rigorous enclosure of log(x) for a single float x > 0."""
    if not (x > 0.0) or math.isinf(x):
        raise ValueError(f"log of {x}")
    m, e = math.frexp(x)  # exact: x = m * 2**e, 0.5 <= m < 1
    if m < 0.7071067811865476:  # < 1/sqrt2 (exactness not needed: any split is fine)
        m *= 2.0
        e -= 1
    if m == 1.0:
        return LN2 * e if e else I(0.0)
    M = I(m)
    z = (M - 1.0) / (M + 1.0)
    z2 = z.sq()
    s = I(0.0)
    p = z
    for j in range(nterms):
        s = s + p / float(2 * j + 1)
        p = p * z2
    az = max(abs(z.lo), abs(z.hi))
    # tail bound 2|z|^(2N+1)/((2N+1)(1-z^2)), computed with upward rounding
    t = I(az) ** (2 * nterms + 1) / (I(2 * nterms + 1) * (1.0 - I(z2.hi)))
    s = s * 2.0
    s = I(_dn(s.lo - t.hi), _up(s.hi + t.hi))
    return s + LN2 * e if e else s


def ilog(x: I) -> I:
    if x.lo <= 0:
        raise ValueError(f"log of interval with nonpositive part {x}")
    return I(_log_point(x.lo).lo, _log_point(x.hi).hi)


# ---------------------------------------------------------------- exp
def _exp_point(x: float) -> I:
    # exp(x) = 2^k exp(r),  r = x - k log 2  (as an interval), |r| <~ 0.35
    if abs(x) > 700:
        raise ValueError("exp argument out of range")
    k = int(round(x / 0.6931471805599453))
    r = I(x) - LN2 * k
    s = I(1.0)
    term = I(1.0)
    n = 22
    for j in range(1, n):
        term = term * r / float(j)
        s = s + term
    a = max(abs(r.lo), abs(r.hi))
    # Lagrange remainder |r|^n/n! * e^{|r|} <= |r|^n/n! * 2   (|r| < log 2)
    rem = I(a) ** n / float(math.factorial(n)) * 2.0
    s = I(_dn(s.lo - rem.hi), _up(s.hi + rem.hi))
    return s * I(math.ldexp(1.0, k))  # power of two: exact


def iexp(x: I) -> I:
    return I(_exp_point(x.lo).lo, _exp_point(x.hi).hi)


# ---------------------------------------------------------------- entropy
def H(x: I) -> I:
    """Binary entropy (natural log) enclosure for x subset of (0,1).

    H(x) = -x log x - (1-x) log(1-x).  We return the hull of the natural
    interval extension and, using concavity / symmetry, the exact range
    information: H is increasing on [0,1/2] and decreasing on [1/2,1].
    """
    if x.lo <= 0.0 or x.hi >= 1.0:
        raise ValueError("H needs (0,1)")

    def Hp(p: float) -> I:
        P = I(p)
        return -(P * _log_point(p)) - (1.0 - P) * ilog(1.0 - P)

    a, b = Hp(x.lo), Hp(x.hi)
    if x.hi <= 0.5:
        return I(a.lo, b.hi)
    if x.lo >= 0.5:
        return I(b.lo, a.hi)
    return I(min(a.lo, b.lo), LN2.hi)


def Hprime(x: I) -> I:
    """H'(x) = log((1-x)/x), decreasing."""
    return ilog((1.0 - x) / x)


def Hnaive(x: I) -> I:
    return -(x * ilog(x)) - (1.0 - x) * ilog(1.0 - x)
