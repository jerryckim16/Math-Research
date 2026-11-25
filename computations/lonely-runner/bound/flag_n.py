"""Plain flag-bound gate target for general n (n = 15 regression, n = 17 the
18-runner case LRC(17)), in exact arithmetic.

Allikvere's flag bound (arXiv:2609.02604v2, Thm 3.8), general n, verified in
problems/lonely-runner.md Approach 11: assume LRC(m) for all m < n, v a
primitive positive counterexample to LRC(n), c_{i+1}/c_i > 4/3 where
B_r = (2r/((n+1)(n+1-r)))^2, c_i = B_i - B_{i-1}.  With K_n = prod c_i and
A_n = K_n^(-1/2): prod v_i < (A_n r_n / n)^n whenever R_n < r_n.

The shape lemma R_n < r_n is proved by the n-general argument of
../shape_lemma.py (Approach 10); here its checks are re-run for n = 17 with
r_17 = 951/2000 (target T = (n/r)^2 passed explicitly).

Forced divisor (Rosenfeld Lemma 4 / Allikvere Lemma 3.9): for 2 <= d <= n+1,
if no v_i is divisible by d then t = 1/d is a witness (each ||v_i/d|| >= 1/d
>= 1/(n+1)); so each maximal prime power <= n+1 divides prod v, and so does
lcm(2..n+1).  For n = 17: lcm(2..18) = 12252240 = 2^4 3^2 5 7 11 13 17.
"""
import sys
import os
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
from math import lcm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import shape_lemma as SL  # noqa: E402  (exact checks, n-general)

getcontext().prec = 50
R_N = {13: Fr(101, 200), 14: Fr(1, 2), 15: Fr(49, 100), 17: Fr(951, 2000)}


def B(n, r):
    return Fr(2 * r, (n + 1) * (n + 1 - r)) ** 2 if r else Fr(0)


def flag_constants(n):
    c = [B(n, i) - B(n, i - 1) for i in range(1, n)]
    K = Fr(1)
    for x in c:
        K *= x
    return K, min(c[i + 1] / c[i] for i in range(len(c) - 1)), c


def ln(x):
    x = Fr(x)
    return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()


def lcm_upto(m):
    L = 1
    for i in range(2, m + 1):
        L = lcm(L, i)
    return L


def forced_divisor_ok(n):
    """lcm(2..n+1) is the product of the maximal prime powers <= n+1, and the
    witness t = 1/d works for every d <= n+1 (||a/d|| >= 1/d for d not | a)."""
    L = lcm_upto(n + 1)
    pp = 1
    for p in range(2, n + 2):
        if all(p % q for q in range(2, p)):
            q = p
            while q * p <= n + 1:
                q *= p
            pp *= q
    witness = all(min(a % d, d - a % d) * (n + 1) >= d for d in range(2, n + 2)
                  for a in range(1, d))      # ||a/d|| >= 1/(n+1) when d does not divide a
    return L, L == pp, witness


AMIN = {13: Fr(8, 5), 14: Fr(8, 5), 15: Fr(8, 5), 17: Fr(3, 2)}


def check_a_lower(n, amin):
    """As shape_lemma.check_a_lower, with the constant 8/5 replaced by amin
    (8/5 fails for n = 17: a(alpha) ~ 1.55).  a decreases on (0, alpha),
    increases between the roots of D_n, decreases on the rest of (0,1];
    min a = min(a(alpha), a(1) = 2), and a(alpha) > q(lo)/hi^(2/n):
    compare n-th powers q(lo)^n > amin^n hi^2."""
    lo, hi, ok = SL.alpha_interval(n)
    X, Q, DQ = SL.X, SL.Q, SL.DQ
    ident = n * X * DQ - 2 * Q == -2 * SL.D_(n)
    return ok and ident and SL.D_(n)(1) == 2 and Q(lo) ** n > amin ** n * hi ** 2 and 2 > amin


def check_two_or_more(n, T, amin):
    """k >= 2 ones: H >= (k/2) 2^k amin^(n-k), increasing in k (ratio
    (k+1)/k * 2/amin > 1), so H >= 4 amin^(n-2) > T."""
    b = lambda k: Fr(k, 2) * 2 ** k * amin ** (n - k)
    return all(b(k + 1) > b(k) for k in range(2, n)) and b(2) > T, b(2)


def shape_checks(n, r, den=10 ** 6):
    T = (n / r) ** 2
    amin = AMIN[n]
    out = {
        "phi_identity": SL.check_phi_identity(n),
        "w_le_half": SL.check_w_le_half(),
        "alpha": SL.check_alpha(n),
        "crit_identity": SL.check_crit_identity(n),
        "L_decreasing": SL.check_L_decreasing(n)[0],
        "a_gt_amin": check_a_lower(n, amin),
        "two_or_more": check_two_or_more(n, T, amin)[0],
        "H1_form": SL.check_H1_form(n),
        "H1_logderiv": SL.check_H1_logderiv(n),
    }
    ok1, info = SL.check_one(n, den=den, T=T)
    out["one"] = ok1
    return out, info, T


def log_bound(n, r, K=None):
    if K is None:
        K, _, _ = flag_constants(n)
    return n * (-ln(K) / 2 + ln(r) - ln(n))


def report(n):
    K, rmin, _ = flag_constants(n)
    r = R_N[n]
    checks, info, T = shape_checks(n, r)
    lb = log_bound(n, r)
    L, Lok, wit = forced_divisor_ok(n)
    return {
        "K_n": K, "ln A_n": -ln(K) / 2, "min ratio": rmin, "ratio > 4/3": rmin > Fr(4, 3),
        "r_n": r, "T": float(T), "shape checks all": all(checks.values()), "checks": checks,
        "H1(t0) lower bound": info[2], "t0 interval": (info[0], info[1]),
        "ln bound": lb, "lcm(2..n+1)": L, "lcm = prod prime powers": Lok, "witness 1/d": wit,
        "target": lb - ln(L),
    }


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or [15, 17]:
        print(f"== n = {n}")
        for k, v in report(n).items():
            print(" ", k, ":", v)
