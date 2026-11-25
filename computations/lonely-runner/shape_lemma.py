"""Shape lemma R_n < r_n for Allikvere's flag bound (arXiv:2609.02604v2,
Lemma 3.7), machine-checked in exact rational arithmetic for n = 13, 14, 15.

The paper proves R_13 < 101/200 and R_14 < 1/2.  Here the same argument is
run for general n, and every identity and numeric inequality it needs is
checked exactly (Fractions and integer polynomials, no floating point in any
check).  For n = 15 this gives R_15 < 49/100; the written proof is in
problems/lonely-runner.md (Approach 10).  n = 13 and 14 are regression tests:
the script must reproduce the paper's polynomials, intervals and bounds.

Notation (paper, eq. (F) and proof of Lemma 3.7).  For u in (0,1]:
    q(u) = 1 + 2u - u^2,   a(u) = q(u) / u^(2/n),   w(u) = u^2 / q(u),
    H(u_1..u_n) = (sum_i w(u_i)) * prod_i a(u_i),
and R_n(x)^2 = n^2 / H(u) with u_i = x_i / max_j x_j.  So R_n < r iff
H > (n/r)^2 =: T on {u in (0,1]^n : max u_i = 1}.

Proof outline (each step's check is the function named in brackets).
  0. H attains its minimum on the domain [prose; uses step 3's a > 8/5].
  1. Interior coordinates.  For a coordinate u in (0,1) with the others
     fixed, phi(u) = a(u)(C + w(u)), C = sum_{j != i} w(u_j) in (0,(n-1)/2],
     satisfies (n/2) u^(1+2/n) phi'(u) = -beta(u),
     beta = C*D(u) - (n-1)u^2, D(u) = (n-1)u^2 - (n-2)u + 1   [check_phi_identity].
     beta has exactly one root u_0 in (0,1), and u_0 < alpha, the smaller
     root of D [prose + check_alpha + check_w_le_half].  So at a minimizer
     every interior coordinate solves beta = 0 in (0, alpha), which is
     L(u) := q D / (n u^2 (1+u)) = 1/A, A = sum_i w(u_i)   [check_crit_identity],
     and L is strictly decreasing on (0, alpha)   [check_L_decreasing].
     Hence all interior coordinates share one value t.
  2. a(u) > 8/5 on (0,1]: a decreases, increases, decreases with turning
     points the roots of D, a(1) = 2   [check_a_lower].
  3. Two or more coordinates equal to one: H >= (k/2) 2^k (8/5)^(n-k)
     >= 4 (8/5)^(n-2) > T   [check_two_or_more].
  4. Exactly one coordinate equal to one: H = H1(t) with
     H1(t) = (1 + 2t + (2n-3)t^2) q(t)^(n-2) / t^(2(n-1)/n)   [check_H1_form],
     whose log-derivative on (0,1) has the sign of an increasing cubic
     [check_H1_logderiv]; its root t0 lies in an explicit rational interval,
     and a monotone bound gives H1(t0) > T   [check_one].
"""
from fractions import Fraction as Fr
from math import log, sqrt


# ---------------------------------------------------------------- polynomials
class P:
    """Univariate polynomial with Fraction coefficients, c[i] * x^i."""

    def __init__(self, c):
        c = [Fr(x) for x in c]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = c or [Fr(0)]

    def __add__(s, o):
        o = o if isinstance(o, P) else P([o])
        m = max(len(s.c), len(o.c))
        return P([(s.c[i] if i < len(s.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(m)])

    __radd__ = __add__

    def __neg__(s):
        return P([-x for x in s.c])

    def __sub__(s, o):
        return s + (-(o if isinstance(o, P) else P([o])))

    def __rsub__(s, o):
        return (-s) + o

    def __mul__(s, o):
        o = o if isinstance(o, P) else P([o])
        r = [Fr(0)] * (len(s.c) + len(o.c) - 1)
        for i, x in enumerate(s.c):
            for j, y in enumerate(o.c):
                r[i + j] += x * y
        return P(r)

    __rmul__ = __mul__

    def __pow__(s, k):
        r = P([1])
        for _ in range(k):
            r = r * s
        return r

    def __eq__(s, o):
        o = o if isinstance(o, P) else P([o])
        return s.c == o.c

    def __call__(s, x):
        r = Fr(0)
        for a in reversed(s.c):
            r = r * x + a
        return r

    def deriv(s):
        return P([i * s.c[i] for i in range(1, len(s.c))] or [0])

    def divmod(s, d):
        num = list(s.c)
        out = [Fr(0)] * max(1, len(num) - len(d.c) + 1)
        while len(num) >= len(d.c) and any(num):
            k = len(num) - len(d.c)
            f = num[-1] / d.c[-1]
            out[k] = f
            for i, y in enumerate(d.c):
                num[i + k] -= f * y
            num.pop()
        return P(out), P(num or [0])

    def __repr__(s):
        return " + ".join(f"({x})u^{i}" for i, x in enumerate(s.c) if x)


X = P([0, 1])
Q = 1 + 2 * X - X * X          # q(u)
DQ = Q.deriv()                 # q'(u) = 2 - 2u


def D_(n):
    return (n - 1) * X * X - (n - 2) * X + 1


def target(n):
    """T = (n / r_n)^2 for the radius r_n claimed at n."""
    r = {13: Fr(101, 200), 14: Fr(1, 2), 15: Fr(49, 100)}[n]
    return (n / r) ** 2


# ---------------------------------------------------------------- the checks
def check_phi_identity(n):
    """phi = u^(-2/n) (C q + u^2).  Then
    (n/2) u^(1+2/n) phi' = (n/2) u (C q' + 2u) - (C q + u^2),
    and this must equal -beta = -(C D - (n-1)u^2) as a polynomial in u for
    every C; both sides are affine in C, so compare the C^0 and C^1 parts."""
    D = D_(n)
    c1 = Fr(n, 2) * X * DQ - Q          # coefficient of C
    c0 = Fr(n, 2) * X * (2 * X) - X * X  # C-free part
    return c1 == -D and c0 == (n - 1) * X * X


def check_w_le_half():
    """1/2 - w(u) = (1 + 3u)(1 - u) / (2 q(u)) >= 0 on [0,1]: so each w <= 1/2
    and C <= (n-1)/2, hence beta(1) = 2C - (n-1) <= 0."""
    return (Q - 2 * X * X) == (1 + 3 * X) * (1 - X)


def alpha_interval(n, den=10000):
    """Rational lo < alpha < hi, alpha = smaller root of D_n, with D_n
    decreasing on [0, (n-2)/(2(n-1))] and D(lo) > 0 > D(hi)."""
    D = D_(n)
    vertex = Fr(n - 2, 2 * (n - 1))
    a = ((n - 2) - sqrt((n - 2) ** 2 - 4 * (n - 1))) / (2 * (n - 1))  # float, only to pick the grid
    lo, hi = Fr(int(a * den), den), Fr(int(a * den) + 1, den)
    ok = D(0) > 0 and D(lo) > 0 and D(hi) < 0 and hi < vertex and (n - 2) ** 2 - 4 * (n - 1) > 0
    return lo, hi, ok


def check_alpha(n):
    return alpha_interval(n)[2]


def check_crit_identity(n):
    """With beta = 0, C = (n-1)u^2/D, and A = C + w = n u^2 (1+u) / (D q)
    because (n-1) q + D = n (1+u).  (D > 0 on (0, alpha).)"""
    return (n - 1) * Q + D_(n) == n * (1 + X)


def L_poly(n):
    """L(u) = q D / (n u^2 (1+u)).  L'(u) = N(u) / (n u^3 (1+u)^2) with
    N = (qD)' u (1+u) - q D (2 + 3u).  Return P_n := -N/2."""
    G = Q * D_(n)
    N = G.deriv() * X * (1 + X) - G * (2 + 3 * X)
    return Fr(-1, 2) * N


def check_L_decreasing(n):
    """P_n(u) > 0 on (0, alpha): P_n(0) > 0 and, for 0 < u < hi,
    P_n(u) >= P_n(0) + sum over negative coefficients c_i hi^i > 0."""
    Pn = L_poly(n)
    _, hi, ok = alpha_interval(n)
    c0 = Pn.c[0]
    lower = c0 + sum(c * hi ** i for i, c in enumerate(Pn.c) if i > 0 and c < 0)
    return ok and c0 > 0 and lower > 0, lower


def check_a_lower(n):
    """a'/a = (n u q' - 2 q) / (n u q) and n u q' - 2q = -2 D_n, so a decreases
    on (0, alpha), increases on (alpha, alpha2), decreases on (alpha2, 1];
    min over (0,1] is min(a(alpha), a(1) = 2).  a(alpha) > q(lo) / hi^(2/n)
    (q increasing, u^(-2/n) decreasing on (0,1)); compare n-th powers:
    q(lo)^n > (8/5)^n hi^2."""
    lo, hi, ok = alpha_interval(n)
    ident = n * X * DQ - 2 * Q == -2 * D_(n)
    D = D_(n)
    alpha2_lt_1 = D(1) == 2 and D(Fr(1)) > 0  # D(1) = 2 > 0: second root < 1
    return ok and ident and alpha2_lt_1 and Q(lo) ** n > Fr(8, 5) ** n * hi ** 2 and Fr(2) > Fr(8, 5)


def check_two_or_more(n, T=None):
    """k >= 2 coordinates equal one: sum w >= k/2, prod a >= 2^k (8/5)^(n-k).
    The bound (k/2) 2^k (8/5)^(n-k) increases in k (ratio (k+1)/k * 5/4 > 1),
    so it is >= 4 (8/5)^(n-2)."""
    T = target(n) if T is None else T
    b = lambda k: Fr(k, 2) * 2 ** k * Fr(8, 5) ** (n - k)
    mono = all(b(k + 1) > b(k) for k in range(2, n))
    return mono and b(2) > T, b(2)


def H1_parts(n):
    """H1(t) = E(t) q(t)^(n-2) t^(-2(n-1)/n), E = 1 + 2t + (2n-3) t^2."""
    return 1 + 2 * X + (2 * n - 3) * X * X


def check_H1_form(n):
    """(1/2 + (n-1) t^2/q) * 2 * (q t^(-2/n))^(n-1) = E q^(n-2) t^(-2(n-1)/n)
    reduces to q + 2(n-1) t^2 = E."""
    return Q + 2 * (n - 1) * X * X == H1_parts(n)


def H1_cubic(n):
    """d/dt log H1 = E'/E + (n-2) q'/q - 2(n-1)/(n t).  Times n t E q:
    M(t) = n t q E' + n (n-2) t E q' - 2 (n-1) q E.  Claim M = 2(n-1)(1-t) K(t)
    with K a cubic; return (K, remainder)."""
    E = H1_parts(n)
    M = n * X * Q * E.deriv() + n * (n - 2) * X * E * DQ - 2 * (n - 1) * Q * E
    K, rem = M.divmod(2 * (n - 1) * (1 - X))
    return K, rem


def check_H1_logderiv(n):
    """On (0,1): n t E q > 0 and 1 - t > 0, so sign(log H1)' = sign K.  K must be
    a cubic with K(0) < 0 and all other coefficients > 0 (increasing on t > 0)."""
    K, rem = H1_cubic(n)
    return rem == 0 and len(K.c) == 4 and K.c[0] < 0 and all(c > 0 for c in K.c[1:])


def t0_interval(n, den=100000):
    K, _ = H1_cubic(n)
    lo, hi = Fr(0), Fr(1)
    while hi - lo > Fr(1, den):
        m = (lo + hi) / 2
        if K(m) < 0:
            lo = m
        else:
            hi = m
    # round outward to the grid 1/den
    lo = Fr((lo.numerator * den) // lo.denominator, den)
    hi = Fr(-((-hi.numerator * den) // hi.denominator), den)
    return lo, hi, K(lo) < 0 < K(hi)


def check_one(n, den=100000, T=None):
    """Exactly one coordinate equal to one.  H1 decreases on (0,t0) and
    increases on (t0,1), so H1 >= H1(t0).  E and q increase on (0,1) and
    t^(-2(n-1)/n) decreases, so H1(t0) >= E(lo) q(lo)^(n-2) / hi^(2(n-1)/n).
    Compare n-th powers: E(lo)^n q(lo)^(n(n-2)) > T^n hi^(2(n-1))."""
    lo, hi, ok = t0_interval(n, den)
    E = H1_parts(n)
    T = target(n) if T is None else T
    lhs = E(lo) ** n * Q(lo) ** (n * (n - 2))
    rhs = T ** n * hi ** (2 * (n - 1))
    approx = float(E(lo)) * float(Q(lo)) ** (n - 2) / float(hi) ** (2 * (n - 1) / n)
    return ok and lhs > rhs, (lo, hi, approx)


def prove(n):
    """Run every check for n; return a dict of results (all booleans True
    means the shape lemma R_n < r_n holds by the argument in the docstring)."""
    out = {}
    out["phi_identity"] = check_phi_identity(n)
    out["w_le_half"] = check_w_le_half()
    out["alpha"] = check_alpha(n)
    out["crit_identity"] = check_crit_identity(n)
    out["L_decreasing"] = check_L_decreasing(n)[0]
    out["a_gt_8_5"] = check_a_lower(n)
    out["two_or_more"] = check_two_or_more(n)[0]
    out["H1_form"] = check_H1_form(n)
    out["H1_logderiv"] = check_H1_logderiv(n)
    out["one"] = check_one(n)[0]
    return out


if __name__ == "__main__":
    for n in (13, 14, 15):
        lo, hi, _ = alpha_interval(n)
        K, _ = H1_cubic(n)
        tl, th, Hb = check_one(n)[1]
        res = prove(n)
        print(f"n={n}: T = (n/r)^2 = {float(target(n)):.4f}")
        print(f"   alpha in ({lo}, {hi});  P_n = {L_poly(n)};  P_n lower bound on (0,alpha) = {float(check_L_decreasing(n)[1]):.4f}")
        print(f"   two-or-more bound 4(8/5)^(n-2) = {float(check_two_or_more(n)[1]):.2f}")
        print(f"   H1 cubic K = {K};  t0 in ({tl}, {th});  H1(t0) >= {Hb:.3f}")
        print(f"   all checks: {all(res.values())}  {res}")
