"""Hyperplane prefix lemma: a sharper last-but-one prefix inequality in the
flag bound, and the resulting gate targets for n = 15 and n = 17.

Setting (problems/lonely-runner.md, Approach 11; notes/lonely-runner/bound.md
section 2): v a primitive positive counterexample to LRC(n), LRC(m) for m < n,
Lambda = P Z^n, d = n - 1, a KZ basis b_1..b_d of Lambda in the E metric,
t_i = ||b_i*||_E^2, B_r = (2r/((n+1)(n+1-r)))^2.

Lemma H.  sum_{i <= d-1} t_i > B'_{d-1} := min(B_d - 1/3, 4(2/5 - 1/(n+1))^2).
  Let alpha in Z^n be the primitive normal of V = span(v, z_1..z_{d-1}).
  (i)  sum(alpha) even: V contains a point of (1/2) 1 + Z^n, separation 1/2.
  (ii) sum(alpha) odd, ||alpha||_1 >= 5: s_l = 1/2 + m_l + sgn(alpha_l)/(2||alpha||_1)
       lies in V for a suitable integer m (gcd(alpha) = 1), separation >= 2/5.
  (iii) ||alpha||_1 = 3: t_d = 1/h_E(alpha)^2 = 1/sum q_l alpha_l^2 <= 1/3, and
       Prop. 3.4 at r = d gives sum_{i<=d-1} t_i > B_d - t_d >= B_d - 1/3.
  In (i), (ii) Prop. 3.4's rounding step with separation sigma gives
  sum_{i<=d-1} t_i > 4(sigma - 1/(n+1))^2.

Lemma M (product minimisation, generalising Allikvere Lemma 3.6).  If
t_{i+1} >= (3/4) t_i, sum_{i<=r} t_i >= F_r with increments e_i = F_i - F_{i-1}
> 0 and e_{i+1}/e_i > 3/4 for all i, then prod t >= min over the 2^(d-1)
block points (each block (a,b] geometric with ratio 3/4 and sum F_b - F_a).
Proof: the vertex/block argument of Lemma 3.6, whose structural step needs
only e_i / w_i strictly increasing (w_i = (3/4)^(i-1)); see bound.md.

Everything exact; logs in Decimal (50 digits).
"""
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flag_n import B, ln, lcm_upto, R_N  # noqa: E402

RHO = Fr(3, 4)


def B_prime(n):
    d = n - 1
    case_short = B(n, d) - Fr(1, 3)
    case_long = 4 * (Fr(2, 5) - Fr(1, n + 1)) ** 2
    case_even = B(n, d)                      # separation 1/2
    return min(case_short, case_long, case_even), (case_short, case_long, case_even)


def block_min(F):
    """min over all block points of prod t; F[0] = 0, F[1..d]."""
    d = len(F) - 1
    e = [F[i] - F[i - 1] for i in range(1, d + 1)]
    assert all(x > 0 for x in e)
    assert all(e[i + 1] / e[i] > RHO for i in range(d - 1)), "block structure needs e ratio > 3/4"
    w = [RHO ** i for i in range(d)]
    best = None
    for mask in range(2 ** (d - 1)):
        ends = [i + 1 for i in range(d - 1) if mask >> i & 1] + [d]
        a, P = 0, Fr(1)
        for b in ends:
            zeta = (F[b] - F[a]) / sum(w[a:b])
            for i in range(a, b):
                P *= w[i] * zeta
            a = b
        if best is None or P < best[0]:
            best = (P, ends)
    return best


def targets(n, r=None):
    r = R_N[n] if r is None else r
    d = n - 1
    F0 = [B(n, j) for j in range(0, d + 1)]
    K0, e0 = block_min(F0)
    F1 = list(F0)
    Bp, cases = B_prime(n)
    F1[d - 1] = max(F0[d - 1], Bp)
    K1, e1 = block_min(F1)
    L = lcm_upto(n + 1)
    tgt = lambda K: n * (-ln(K) / 2 + ln(r) - ln(n)) - ln(L)
    return {"B_{d-1}": F0[d - 1], "B'_{d-1}": Bp, "cases": cases,
            "plain K": K0, "plain blocks all singletons": len(e0) == d,
            "plain target": tgt(K0), "new K": K1, "new min blocks": e1,
            "new target": tgt(K1), "gain": tgt(K0) - tgt(K1)}


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or [15, 17]:
        print(f"== n = {n}")
        for k, v in targets(n).items():
            print(" ", k, ":", v)
