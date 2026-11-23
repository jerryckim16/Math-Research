"""Re-derive the constants of Allikvere's flag bound (arXiv:2609.02604v2,
Theorem 3.8) in exact rational arithmetic, and extend them to n = 15.

Theorem 3.8 (as stated there).  Assume LRC(m) for all m < n, let v be a
primitive positive counterexample to LRC(n), and suppose c_{i+1}/c_i > 4/3
for 1 <= i < n-1, where B_r = (2r/((n+1)(n+1-r)))^2, c_i = B_i - B_{i-1}.
With K_n = prod_{i=1}^{n-1} c_i and A_n = K_n^{-1/2}:
    v_1...v_n < (A_n r_n / n)^n   whenever R_n < r_n on the simplex.
The paper proves r_13 = 101/200 and r_14 = 1/2 (Lemma 3.7, "shape bound").

For n = 15 the paper gives nothing.  Here we compute K_15 and the ratio
condition exactly; r_15 needs a shape lemma we do NOT prove.  We only
evaluate the paper's one-variable reduction numerically (heuristic) to see
what bound such a lemma would give.
"""
from fractions import Fraction
from math import log, comb


def flag_constants(n):
    B = [Fraction(0)] + [Fraction(2 * r, (n + 1) * (n + 1 - r)) ** 2 for r in range(1, n)]
    c = [B[i] - B[i - 1] for i in range(1, n)]
    ratios = [c[i + 1] / c[i] for i in range(len(c) - 1)]
    K = Fraction(1)
    for x in c:
        K *= x
    return K, min(ratios)


def log_bound(n, r_n):
    K, _ = flag_constants(n)
    logA = -0.5 * (log(K.numerator) - log(K.denominator))
    return n * (logA + log(r_n) - log(n))


def lcm_upto(m):
    from math import lcm
    out = 1
    for i in range(2, m + 1):
        out = lcm(out, i)
    return out


def shape_one_variable(n, steps=200000):
    """min over t of H(1,t,...,t) from the proof of Lemma 3.7; returns
    (t*, H_min, R = n/sqrt(H_min)).  Numerical, heuristic: the reduction to
    this one-variable family is proved in the paper only for n = 13, 14."""
    best = None
    for s in range(1, steps):
        t = 0.3 * s / steps
        q = 1 + 2 * t - t * t
        H = (0.5 + (n - 1) * t * t / q) * 2 * (q / t ** (2 / n)) ** (n - 1)
        if best is None or H < best[1]:
            best = (t, H)
    return best[0], best[1], n / best[1] ** 0.5


if __name__ == "__main__":
    K14_paper = Fraction(2289670297, 97243124257250844122250000000000000000)
    for n in (13, 14, 15):
        K, rmin = flag_constants(n)
        print(f"n={n}: K_n = {K}  min c_(i+1)/c_i = {rmin} = {float(rmin):.6f} (> 4/3: {rmin > Fraction(4, 3)})")
        print(f"      ln B_n (MSS/Rosenfeld) = {n * ((n - 1) * log(comb(n + 1, 2)) - log(n)):.4f}")
        if n == 14:
            print("      K_14 equals the paper's value:", K == K14_paper)
        t, H, R = shape_one_variable(n)
        print(f"      one-variable shape family: t*={t:.5f} H_min={H:.3f} R={R:.5f} (heuristic)")
    print("paper constants: n=13, r=101/200:", round(log_bound(13, 101 / 200), 6), "(paper: < 341.031991)")
    print("                 n=14, r=1/2    :", round(log_bound(14, 0.5), 6), "(paper: 414.77936455669981...)")
    print("                 n=14 target after log 360360:", round(log_bound(14, 0.5) - log(360360), 6), "(paper: 401.9846)")
    for r in (0.49, 0.5):
        print(f"n=15 with r_15 = {r}: ln bound = {log_bound(15, r):.4f}; minus ln lcm(2..16) = {log(lcm_upto(16)):.4f} -> target {log_bound(15, r) - log(lcm_upto(16)):.4f}")
