"""Exact checker for Lemma H of notes/lonely-runner/general-n-explicit.md.

Lemma H (2-coprime Hall condition for two progressions).  Let I, J be
arithmetic progressions of m >= 2 terms with common difference 2 inside
[1, N].  Put
    j     = the largest j >= 0 with p_1 p_2 ... p_j <= N, where p_1 = 3,
            p_2 = 5, ... are the odd primes;
    gstar = prod_{i <= j} (1 - 1/p_i);
    x     = m * gstar - (2^j - 1),   k0 = floor(x) + 1;
    ell   = the largest l >= 0 with m^l <= N;
    a_p   = ceil(m / p)  for odd primes p < m.
Suppose that every integer k with k0 < k <= (m+1)/2 lies in an interval
[k1, k2] (k1 <= k <= k2) with
    (LAM)  sum_{p odd prime, p < m} min(k1, a_p) * min(m+1-k2, a_p) + ell*k1
               <  k1 * (m + 1 - k2).
Then I and J have a perfect matching in which matched numbers share no odd
prime factor.

check_H(m, N) decides the hypothesis exactly (integers and Fractions) and
returns the interval cover it used, so that a second run can re-verify it.
All arithmetic is exact (Python integers and Fractions).  For m > P0 the
primes in (P0, m) are covered by the explicit tail bound in LamData.
"""
from fractions import Fraction
import sys

import numpy as np


def primes_upto(x):
    if x < 2:
        return np.zeros(0, dtype=np.int64)
    s = np.ones(x + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(x ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0].astype(np.int64)


_SMALL = [int(p) for p in primes_upto(10000) if p > 2]


def per_element(m, N):
    """j, gstar, k0 of Lemma H (every k <= k0 is handled by one element)."""
    j, prod, g = 0, 1, Fraction(1)
    for p in _SMALL:
        if prod * p > N:
            break
        prod *= p
        g *= Fraction(p - 1, p)
        j += 1
    x = m * g - (2 ** j - 1)
    k0 = (x.numerator // x.denominator) + 1
    return j, g, k0


def ell_of(m, N):
    ell = 0
    while m ** (ell + 1) <= N:
        ell += 1
    return ell


P0_DEFAULT = 20011    # odd primes up to P0 are summed exactly


class LamData:
    """Odd primes p < m grouped by a_p = ceil(m/p): values a and counts.

    If m - 1 > P0, only the odd primes p <= P0 are summed exactly, and the
    remaining terms (p prime, P0 < p < m) are replaced by the upper bound
        sum_{odd n, P0 < n < m} (m/n + 1)^2
          <= m^2/(2 P0) + m ln(m/P0) + m/2,
    using min(k1,a_p) min(u,a_p) <= a_p^2 <= (m/p+1)^2, and for odd n > P0
    the bounds 1/n^2 <= (1/2) int_{n-2}^{n} dx/x^2 and
    1/n <= (1/2) int_{n-2}^{n} dx/x.  ln(y) is bounded above by
    0.6932 * bitlength(ceil(y)).  The tail is an exact Fraction.
    """

    def __init__(self, m, P0=P0_DEFAULT):
        assert m >= 2
        top = min(m - 1, P0)
        ps = primes_upto(top)
        ps = [int(p) for p in ps if p > 2]
        cnt = {}
        for p in ps:
            a = -((-m) // p)
            cnt[a] = cnt.get(a, 0) + 1
        self.m = m
        self.items = sorted(cnt.items())
        self.tail = Fraction(0)
        if m - 1 > P0:
            y = -((-m) // P0)
            ln_ub = Fraction(6932, 10000) * y.bit_length()
            self.tail = Fraction(m * m, 2 * P0) + m * ln_ub + Fraction(m, 2)

    def lhs(self, k1, k2):
        """upper bound for sum_p min(k1,a_p) min(m+1-k2,a_p) (exact)."""
        u = self.m + 1 - k2
        s = 0
        for a, c in self.items:
            s += min(a, k1) * min(a, u) * c
        return s + self.tail


def lam_ok(L, ell, k1, k2):
    m = L.m
    return L.lhs(k1, k2) + ell * k1 < k1 * (m + 1 - k2)


def check_H(m, N, verbose=False):
    """Return (ok, info).  ok=True iff the hypothesis of Lemma H holds."""
    j, g, k0 = per_element(m, N)
    kmax = (m + 1) // 2
    info = dict(m=m, N=N, j=j, gstar=float(g), k0=k0, kmax=kmax)
    if k0 >= kmax:
        info["pieces"] = []
        return True, info
    ell = ell_of(m, N)
    info["ell"] = ell
    L = LamData(m)
    pieces = []
    k = max(k0 + 1, 1)
    while k <= kmax:
        if not lam_ok(L, ell, k, k):
            info["fail_k"] = k
            info["pieces"] = pieces
            return False, info
        lo, hi = k, kmax
        if lam_ok(L, ell, k, hi):
            r = hi
        else:
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if lam_ok(L, ell, k, mid):
                    lo = mid
                else:
                    hi = mid
            r = lo
        pieces.append((k, r))
        k = r + 1
    info["pieces"] = pieces
    return True, info


def verify_pieces(m, N, pieces):
    """Independent re-check of a returned cover (used by the tests)."""
    j, g, k0 = per_element(m, N)
    kmax = (m + 1) // 2
    ell = ell_of(m, N)
    L = LamData(m)
    need = max(k0 + 1, 1)
    for (k1, k2) in sorted(pieces):
        if k1 > need:
            return False
        if not lam_ok(L, ell, k1, k2):
            return False
        need = max(need, k2 + 1)
    return need > kmax


def min_m(N, lo=2, hi=None):
    """Smallest m >= lo with check_H(m, N) true, assuming monotonicity found
    by bisection (the answer is re-checked exactly; the caller decides how to
    use it)."""
    if hi is None:
        hi = max(lo, 4)
        while not check_H(hi, N)[0]:
            hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if check_H(mid, N)[0]:
            hi = mid
        else:
            lo = mid
    return hi


if __name__ == "__main__":
    m, N = int(sys.argv[1]), int(sys.argv[2])
    ok, info = check_H(m, N)
    print(ok, {k: v for k, v in info.items() if k != "pieces"}, "pieces:", len(info.get("pieces", [])))
