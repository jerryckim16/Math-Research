"""Exact (integer/rational) Lonely Runner checker for one speed tuple.

Notation: ||x|| = distance from x to the nearest integer.  For a tuple
v = (v_1, ..., v_n) of positive integers and a rational threshold delta,
we decide whether there is a real t with ||v_i t|| >= delta for all i.
The Lonely Runner Conjecture (n moving runners plus one at rest) is the
statement that this holds with delta = 1/(n+1) for every such v.

Everything here uses Python integers / fractions.Fraction: no floating point.

Decision procedure (find_witness)
---------------------------------
For a single speed v the "good set" G_v = {t : ||v t|| >= delta} is the union
over m in Z of the closed intervals [(m+delta)/v, (m+1-delta)/v] (empty when
delta > 1/2).  Let G = intersection of the G_{v_i}.

Claim: G is nonempty iff some left endpoint (m+delta)/v_i, with
0 <= m < v_i, lies in G.

Proof.  (<=) trivial.  (=>) take t in G.  For each i let [L_i, R_i] be an
interval of G_{v_i} containing t, and let s = max_i L_i.  Then
L_i <= s <= t <= R_i for every i, so s is in G, and s is a left endpoint
(m+delta)/v_j for some j, m.  Every G_{v_i} is invariant under t -> t+1
(the v_i are integers), so s mod 1 is also in G and is a left endpoint
with 0 <= m < v_j.  QED.

So the search over the finitely many left endpoints is complete.  When it
fails, the list of (candidate, failing index) pairs is a checkable
certificate that no witness exists (see check_no_witness_certificate).

Maximum loneliness (max_loneliness)
-----------------------------------
ML(v) = max_t min_i ||v_i t||.  Claim: the maximum is attained at some
t = a/(v_i + v_j) with i, j in {1..n} (i = j allowed) and 0 <= a < v_i + v_j.

Proof.  f(t) = min_i ||v_i t|| is continuous and 1-periodic, so it has a
global maximiser t*, and f(t*) > 0 (f is not identically 0: f > 0 at
t = 1/(2 * prod v_i) ... indeed at any t not in the finite set of zeros).
Let A be the set of indices attaining the min at t*.  If t* is a peak of
some ||v_i t|| (i in A), then t* = (2m+1)/(2 v_i), of the required form
with i = j.  It cannot be a zero (f(t*) > 0).  Otherwise every g_i, i in A,
is linear near t* with slope +v_i or -v_i.  If all of them had positive
slope, f would increase just to the right of t* (non-active g's stay larger
by continuity); if all negative, f would increase just to the left.  So
there are i, j in A with g_i(t) = v_i t - a' and g_j(t) = b' - v_j t near
t* (a', b' integers) and g_i(t*) = g_j(t*), giving (v_i + v_j) t* = a' + b'.
QED.
"""

from fractions import Fraction
from math import gcd


def frac_dist_ge(num, den, a, b):
    """Return True iff ||num/den|| >= a/b (all integers, den, b > 0)."""
    r = num % den
    d = min(r, den - r)
    return b * d >= a * den


def norm_frac(x):
    """||x|| for a Fraction x."""
    f = x - (x.numerator // x.denominator)
    return min(f, 1 - f)


def find_witness(v, delta=None):
    """Return (True, t) with t a Fraction witness, or (False, certificate).

    v: sequence of positive integers.  delta: Fraction, default 1/(len(v)+1).
    The certificate is a list of (i, m, j): candidate t = (m+delta)/v_i fails
    at index j, i.e. ||v_j t|| < delta.
    """
    v = [int(x) for x in v]
    if any(x <= 0 for x in v):
        raise ValueError("speeds must be positive integers")
    n = len(v)
    if delta is None:
        delta = Fraction(1, n + 1)
    delta = Fraction(delta)
    a, b = delta.numerator, delta.denominator
    if 2 * a > b:  # delta > 1/2: G_v is empty
        return False, "delta > 1/2"
    cert = []
    for i, vi in enumerate(v):
        den = b * vi
        for m in range(vi):
            num = m * b + a  # t = num/den
            bad = None
            for j, vj in enumerate(v):
                if not frac_dist_ge(vj * num, den, a, b):
                    bad = j
                    break
            if bad is None:
                return True, Fraction(num, den)
            cert.append((i, m, bad))
    return False, cert


def check_witness(v, t, delta=None):
    """Independent check that t is a witness: all ||v_i t|| >= delta."""
    if delta is None:
        delta = Fraction(1, len(v) + 1)
    t = Fraction(t)
    return all(norm_frac(vi * t) >= delta for vi in v)


def check_no_witness_certificate(v, cert, delta=None):
    """Check a certificate from find_witness: it must cover every left
    endpoint (i, m), 0 <= m < v_i, and each claimed failure must be real."""
    if delta is None:
        delta = Fraction(1, len(v) + 1)
    delta = Fraction(delta)
    if cert == "delta > 1/2":
        return delta > Fraction(1, 2)
    need = {(i, m) for i, vi in enumerate(v) for m in range(vi)}
    seen = set()
    for (i, m, j) in cert:
        t = (m + delta) / v[i]
        if not norm_frac(v[j] * t) < delta:
            return False
        seen.add((i, m))
    return seen == need


def max_loneliness(v):
    """Return (ML(v), t*) exactly, as Fractions (see module docstring)."""
    v = [int(x) for x in v]
    best, best_t = Fraction(-1), None
    n = len(v)
    for i in range(n):
        for j in range(i, n):
            s = v[i] + v[j]
            for a in range(s):
                # min_k ||v_k a/s|| = dmin/s, computed with integers
                dmin = min(min((vk * a) % s, s - (vk * a) % s) for vk in v)
                val = Fraction(dmin, s)
                if val > best:
                    best, best_t = val, Fraction(a, s)
    return best, best_t


def is_counterexample(v):
    """True iff v violates LRC with threshold 1/(n+1)."""
    ok, _ = find_witness(v)
    return not ok


def primitive(v):
    g = 0
    for x in v:
        g = gcd(g, x)
    return [x // g for x in v]
