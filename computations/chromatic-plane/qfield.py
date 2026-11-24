"""Exact arithmetic in the multiquadratic field Q(sqrt3, sqrt5, sqrt11).

An element is a tuple of 8 Fractions, the coefficients on the basis
sqrt(m) for the 8 squarefree products m of {3, 5, 11}:
index bit 0 <-> 3, bit 1 <-> 5, bit 2 <-> 11, so index 0 <-> 1,
index 1 <-> sqrt3, index 3 <-> sqrt15, index 7 <-> sqrt165, etc.

These 8 numbers are linearly independent over Q (square roots of distinct
squarefree positive integers are Q-linearly independent; Besicovitch 1940).
Hence an element is zero iff all 8 coefficients are zero, and equality
tests below are exact. Floats are used only by `approx`, for filtering
candidates; every claim that matters is decided by exact comparison.
"""
from fractions import Fraction
from math import sqrt

PRIMES = (3, 5, 11)
N = 8


def _radicand(mask):
    r = 1
    for i, p in enumerate(PRIMES):
        if mask >> i & 1:
            r *= p
    return r


RADICAND = tuple(_radicand(m) for m in range(N))
FLOAT_BASIS = tuple(sqrt(r) for r in RADICAND)
# sqrt(a) * sqrt(b) = common * sqrt(a xor b)
MULT = [[(_radicand(a & b), a ^ b) for b in range(N)] for a in range(N)]

ZERO = (Fraction(0),) * N


def const(q):
    q = Fraction(q)
    return (q,) + (Fraction(0),) * (N - 1)


def root(m, coef=1):
    """coef * sqrt(m), for m a squarefree product of 3, 5, 11."""
    mask = RADICAND.index(m)
    v = [Fraction(0)] * N
    v[mask] = Fraction(coef)
    return tuple(v)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    out = [Fraction(0)] * N
    for i in range(N):
        ai = a[i]
        if not ai:
            continue
        row = MULT[i]
        for j in range(N):
            bj = b[j]
            if not bj:
                continue
            c, k = row[j]
            out[k] += c * ai * bj
    return tuple(out)


def is_zero(a):
    return not any(a)


def approx(a):
    return sum(float(x) * f for x, f in zip(a, FLOAT_BASIS))


# ----- points in the plane: pairs (x, y) of field elements -----

def padd(p, q):
    return (add(p[0], q[0]), add(p[1], q[1]))


def psub(p, q):
    return (sub(p[0], q[0]), sub(p[1], q[1]))


def norm2(p):
    return add(mul(p[0], p[0]), mul(p[1], p[1]))


def rotate(p, rot):
    """Rotate p by the rotation with exact (cos, sin) = rot."""
    c, s = rot
    x, y = p
    return (sub(mul(c, x), mul(s, y)), add(mul(s, x), mul(c, y)))


def compose(r1, r2):
    """Rotation r1 followed by r2 (angles add)."""
    c1, s1 = r1
    c2, s2 = r2
    return (sub(mul(c1, c2), mul(s1, s2)), add(mul(s1, c2), mul(c1, s2)))


def inverse(r):
    return (r[0], neg(r[1]))


def is_rotation(r):
    """Exact check cos^2 + sin^2 = 1."""
    return norm2(r) == const(1)


def papprox(p):
    return (approx(p[0]), approx(p[1]))


def is_unit_distance(p, q):
    """Exact test |p - q|^2 == 1."""
    return norm2(psub(p, q)) == const(1)
