"""Exact checks for the weighted shift lemma (notes/lonely-runner/small-primes.md, Lemma S).

(1) Arc count: for n >= 1 points of a coset x + (1/n)Z (mod 1), the number
    lying in the open arc ||y|| < 1/(k+1) (length 2/(k+1)) is at most
    ceil(2n/(k+1)), with equality for some x.  Checked exactly (Fractions)
    for k = 15 and every n <= 256, by evaluating the count on every interval
    between consecutive breakpoints and at the breakpoints themselves.
(2) Shift multiplicity: for d >= 2, u with g = gcd(u,d), the map
    q -> q*u mod d (q in Z_d) hits every multiple of g exactly g times,
    so the d shifts t0 + q/d move u*t0 through the d/g-point coset
    u*t0 + (g/d)Z, each point g times.  Checked for d <= 128, all u mod d.
(3) Negative control: replacing ceil by floor breaks (1) for some n.
"""
from fractions import Fraction as F
from math import gcd, ceil


def dist(y):
    y = y % 1
    return min(y, 1 - y)


def count(x, n, k):
    return sum(1 for j in range(n) if dist(x + F(j, n)) < F(1, k + 1))


def max_count(n, k):
    # breakpoints in [0, 1/n): x with x + j/n = +-1/(k+1) mod 1
    bps = sorted({(F(s, k + 1) - F(j, n)) % F(1, n) for j in range(n) for s in (1, -1)} | {F(0)})
    pts = list(bps) + [(bps[i] + (bps[i + 1] if i + 1 < len(bps) else F(1, n))) / 2 for i in range(len(bps))]
    return max(count(x, n, k) for x in pts)


def check_arc(k=15, nmax=256):
    bad = []
    for n in range(1, nmax + 1):
        mc = max_count(n, k)
        if mc != -(-2 * n // (k + 1)):
            bad.append((n, mc))
    return bad


def check_mult(dmax=128):
    for d in range(2, dmax + 1):
        for u in range(d):
            g = gcd(u, d)
            hits = {}
            for q in range(d):
                r = q * u % d
                hits[r] = hits.get(r, 0) + 1
            assert set(hits) == set(range(0, d, g)) and set(hits.values()) == {g}, (d, u)
    return True


if __name__ == "__main__":
    bad = check_arc()
    print("arc count = ceil(2n/16) for all n <= 256:", not bad, bad[:5])
    print("shift multiplicity:", check_mult())
    neg = [n for n in range(1, 65) if max_count(n, 15) > 2 * n // 16]
    print("negative control (floor fails at some n):", bool(neg), neg[:5])
