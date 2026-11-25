"""Independent exact re-check of the top-level arithmetic of the refined
product bound in J. Allikvere, "Sixteen lonely runners" (Zenodo
doi:10.5281/zenodo.23304361, Oct 2026, unrefereed), Section "The refined
product bound" and Appendix "Combining the rank bounds".

Written from the TeX source only; none of the author's code is used.

Checks (exact rationals; logarithms via Decimal at 50 digits, with the
rounding direction stated):
  K_15 = prod c_j, B_j = j^2 / (64 (16-j)^2)       (paper value)
  tau_r = prod_{j=15-r}^{14} c_j, alpha = (122/125)^2
  J_r = alpha / (W_r tau_r) for the table W_r       (paper's five fractions)
  J_* = min J_r (rank five)
  15 log(61 / (1875 sqrt(K_15 J_*)))  vs 459.084, and minus log D vs 361.44573307
  the interface: (prod v)^(2/15) <= W tau / (900 K)  <=>  bound with alpha.
"""
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
from math import lcm

getcontext().prec = 60


def B(j):
    return Fr(j * j, 64 * (16 - j) ** 2) if j else Fr(0)


c = {j: B(j) - B(j - 1) for j in range(1, 15)}
K15 = Fr(1)
for j in range(1, 15):
    K15 *= c[j]
K15_paper = Fr(233570089, 12695029890685690413859209216000000000000)

ALPHA = Fr(122, 125) ** 2
W = {4: Fr(42), 5: Fr(359, 100) * 666, 6: Fr(47, 10) * Fr(5764801, 130),
     7: Fr(31, 5) * Fr(185218112079, 62500), 8: Fr(609, 50) * Fr(442188799299, 1220)}
J_paper = {4: Fr(1851807744, 12337325), 5: Fr(4355451813888, 29029584727),
           6: Fr(3199923781632, 18971047711), 7: Fr(326658886041600000, 1053870975711983),
           8: Fr(1205136095095554048000, 3575244986833960583)}


def tau(r):
    p = Fr(1)
    for j in range(15 - r, 15):
        p *= c[j]
    return p


def J(r):
    return ALPHA / (W[r] * tau(r))


def ln(x):
    x = Fr(x)
    return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()


def raw_log_bound(Jstar):
    # 15 log(61/(1875 sqrt(K J)))
    return 15 * (ln(Fr(61, 1875)) - ln(K15 * Jstar) / 2)


Q0 = [29, 31, 191, 211, 223, 233, 239, 241, 251, 257, 263, 271, 277, 283, 293, 307]


def D():
    d = 1
    for i in range(2, 17):
        d = lcm(d, i)
    for q in Q0:
        d *= q
    return d


def main():
    out = {}
    out["K15_matches_paper"] = K15 == K15_paper
    out["min_c_ratio"] = min(c[j + 1] / c[j] for j in range(1, 14))
    out["J_matches_paper"] = {r: J(r) == J_paper[r] for r in W}
    Jstar = min(J(r) for r in W)
    out["Jstar"] = Jstar
    out["argmin"] = min(W, key=J)
    out["Jstar_gt_150"] = Jstar > 150
    out["raw_log_bound"] = raw_log_bound(Jstar)
    out["D_paper"] = D() == 2533505785515279655930328637893852203566480
    out["requirement"] = raw_log_bound(Jstar) - ln(D())
    # the plain flag bound with r_15 = 61*15/1875 = 0.488 (no relations, J = 1)
    out["flag_only_r0488"] = raw_log_bound(Fr(1))
    # what each rank alone would give
    out["per_rank_bound"] = {r: raw_log_bound(J(r)) for r in W}
    return out


if __name__ == "__main__":
    for k, v in main().items():
        print(k, ":", v)
