"""A coarse relation-rank sharpening of the flag bound for general n
(n = 15 for comparison with Allikvere's "Sixteen lonely runners", Zenodo
10.5281/zenodo.23304361; n = 17 for LRC(17)).

This uses ONLY the general lemmas of that paper (re-derived for general n in
notes/lonely-runner/bound.md, section 4), with our own code, and none of his
finite classifications:

  Riesz   sum over ternary lines of O of (-1)^(s+1) (delta+s)/2^(s-1) > delta,
          delta = 1/(1 - cos(2 pi/(n+1))) - (n+1)/2.
  Greedy  positive odd weight <= w(s_1) + sum_j 2*3^(j-2) w(s_j); g <= prod s_j.
  RowIdx  g <= (a-1)^r (a even), a (a-2)^(r-1) (a odd).
  Prefix  sum_{i<=j} t_i > B_{j+1} on the section when j >= n+2-a and the
          relation space V_j^perp has rank n-1-j >= 3 (support-clearance).
  Pool    gamma from weighted PAV (App. A.2) and the weak product lemma.
  Schur   (2R)^2 det(AQA^T) <= C_r det(AA^T), C_r from weighted AM-GM with
          interval arithmetic (mpmath iv) for the one-variable maximum.
  Interface  (prod v)^(2/n) <= W tau_r / (4 n^2 K_n), W = C_r g/gamma.

Relative to the plain flag bound, case r improves ln prod v by (n/2) ln J_r,
J_r = (2 r_n)^2 / (W_r tau_r) (r_n the proved shape radius).  A counterexample
whose full odd relation space O has rank r gets
  J(r) = max(1, J_greedy(r), max_{r' <= r} J_select(r')),
where J_select(r') selects r' independent odd relations (no Riesz input), and
the final gain is (n/2) ln min_{r >= 1} J(r).

Exact rationals throughout except the interval-arithmetic shape constant
(enclosures are converted to exact rational upper bounds).
"""
import os
import sys
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
from math import prod

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flag_n import B, ln, lcm_upto, R_N, flag_constants  # noqa: E402
from audit_relations import pooled  # noqa: E402  (exact PAV + certificate asserts)


# ------------------------------------------------------------------ delta
def delta_bounds(n, den=10 ** 6):
    from mpmath import iv
    from mpmath.libmp import to_rational
    iv.prec = 200
    d = 1 / (1 - iv.cos(2 * iv.pi / (n + 1))) - Fr(n + 1, 2).numerator * 1.0 / Fr(n + 1, 2).denominator
    lo, hi = (Fr(*to_rational(x)) for x in d._mpi_)
    L = Fr((lo.numerator * den) // lo.denominator, den)
    H = Fr(-((-hi.numerator * den) // hi.denominator), den)
    assert L <= lo and hi <= H
    return L, H


def w(s, d):
    return (d + s) / Fr(2 ** (s - 1))


def greedy_bound(ss, d):
    return w(ss[0], d) + sum(2 * 3 ** (j - 2) * w(ss[j - 1], d) for j in range(2, len(ss) + 1))


def survivors(n, r, D):
    odd = [s for s in range(3, n + 1, 2)]
    return [s for s in combinations_with_replacement(odd, r)
            if any(greedy_bound(s, d) > d for d in D)]


def full_row_index(r, a):
    return (a - 1) ** r if a % 2 == 0 else a * (a - 2) ** (r - 1)


# ------------------------------------------------------------------ gamma
def c(n, j):
    return B(n, j) - B(n, j - 1)


def G(n, r, a):
    m = n - 1 - r
    F = []
    for j in range(1, m + 1):
        improved = j >= n + 2 - a and n - 1 - j >= 3
        F.append(B(n, j + 1) if improved else B(n, j))
    d = pooled(F)
    return prod(d) / prod(c(n, j) for j in range(1, m + 1))


def tau(n, r):
    return prod(c(n, j) for j in range(n - r, n))


# ------------------------------------------------------------------ shape constant
def shape_constant(n, r, omegas=None):
    """Rigorous upper bound on sup Phi_r, Phi_r = 4n^2 (prod u)^(2/n) /
    ((sum u^2) prod_{i>=r+2} q(u_i)), 1 = u_1 >= ... >= u_n > 0, via weighted
    AM-GM with weights w0 (u_1), 1/n (u_2..u_{r+1}), omega (the m = n-1-r
    lower ones):  Phi_r <= 4n^2 w0^w0 (1/n)^(r/n) omega^(m omega) hmax^m,
    hmax = max_{0<z<=1} z^beta/q(z), beta = 2/n - 2 omega.  h' has the sign
    of beta + (2beta-2) z + (2-beta) z^2, whose smaller root xi is the only
    interior local maximum; so hmax = max(h(xi), h(1) = 1/2)."""
    from mpmath import iv, mpf
    from mpmath.libmp import to_rational
    iv.prec = 120
    m = n - 1 - r
    if omegas is None:
        omegas = [Fr(k, 4000) for k in range(1, int(4000 * Fr(1, n)))]
    best = None
    for om in omegas:
        w0 = 1 - Fr(r, n) - m * om
        beta = Fr(2, n) - 2 * om
        if w0 <= 0 or beta <= 0:
            continue
        A, Bq, Cq = iv.mpf(beta.numerator) / beta.denominator, None, None
        b = iv.mpf(2 * beta.numerator - 2 * beta.denominator) / beta.denominator
        a2 = iv.mpf(2 * beta.denominator - beta.numerator) / beta.denominator
        disc = b * b - 4 * a2 * A
        if disc.a <= 0:
            hmax = iv.mpf(0.5)
        else:
            xi = (-b - iv.sqrt(disc)) / (2 * a2)
            hx = xi ** A / (1 + 2 * xi - xi * xi)
            hmax = iv.mpf([max(hx.a, mpf(0.5)), max(hx.b, mpf(0.5))]) if True else None
        W0 = iv.mpf(w0.numerator) / w0.denominator
        OM = iv.mpf(om.numerator) / om.denominator
        val = 4 * n * n * W0 ** W0 * (iv.mpf(1) / n) ** (iv.mpf(r) / n) * OM ** (m * OM) * hmax ** m
        ub = Fr(*to_rational(val._mpi_[1]))
        if best is None or ub < best[0]:
            best = (ub, om)
    return best


# ------------------------------------------------------------------ per-rank J
def J_cases(n, rmax_sel=None):
    r_n = R_N[n]
    D = delta_bounds(n)
    out = {}
    for r in range(1, n - 1):
        C, om = shape_constant(n, r)
        t = tau(n, r)
        surv = survivors(n, r, D)
        # greedy (full O of rank r)
        if not surv:
            Jg = None   # rank excluded
        else:
            worst = Fr(0)
            for a in range(r + 1, n + 1):
                ls = [s for s in surv if s[-1] <= a]
                if not ls:
                    continue
                ga = min(max(prod(s) for s in ls), full_row_index(r, a))
                worst = max(worst, Fr(ga) / G(n, r, a))
            Jg = (2 * r_n) ** 2 / (C * worst * t)
        # selection of r independent odd relations (no Riesz input)
        worst_s = max(Fr(full_row_index(r, a)) / G(n, r, a) for a in range(r + 1, n + 1))
        Js = (2 * r_n) ** 2 / (C * worst_s * t)
        out[r] = {"C_r": C, "omega": om, "survivors": len(surv), "J_greedy": Jg, "J_select": Js}
    return D, out


def final(n):
    D, cases = J_cases(n)
    best_sel = Fr(0)
    Jmin, arg = None, None
    rows = {}
    for r in sorted(cases):
        cs = cases[r]
        best_sel = max(best_sel, cs["J_select"])
        if cs["J_greedy"] is None:
            rows[r] = "excluded"
            continue
        Jr = max(Fr(1), cs["J_greedy"], best_sel)
        rows[r] = Jr
        if Jmin is None or Jr < Jmin:
            Jmin, arg = Jr, r
    # ranks n-1: O cannot have rank n (v != 0); rank n-1 is handled by selection
    Jr = max(Fr(1), best_sel)
    rows[n - 1] = Jr
    if Jmin is None or Jr < Jmin:
        Jmin, arg = Jr, n - 1
    K, _, _ = flag_constants(n)
    plain = n * (-ln(K) / 2 + ln(R_N[n]) - ln(n)) - ln(lcm_upto(n + 1))
    gain = n * ln(Jmin) / 2
    return {"delta": D, "cases": cases, "J(r)": rows, "J_min": Jmin, "argmin": arg,
            "plain target": plain, "gain": gain, "new target": plain - gain}


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or [15, 17]:
        res = final(n)
        print(f"== n = {n}: delta in {tuple(float(x) for x in res['delta'])}")
        for r, cs in res["cases"].items():
            f = lambda x: None if x is None else round(float(x), 4)
            print(f"  r={r:2d} C_r<={float(cs['C_r']):.4f} surv={cs['survivors']:5d} "
                  f"J_greedy={f(cs['J_greedy'])} J_select={f(cs['J_select'])} J(r)={f(res['J(r)'][r]) if res['J(r)'][r] != 'excluded' else 'excl'}")
        print("  J_min", float(res["J_min"]), "at rank", res["argmin"])
        print("  plain", res["plain target"], "\n  gain ", res["gain"], "\n  new  ", res["new target"])


def final_with_exclusions(n, excluded_ranks):
    """As final(), with ranks in excluded_ranks removed (each must be proved
    excluded, e.g. by rank_exclusion.exclude(n, r))."""
    D, cases = J_cases(n)
    best_sel, Jmin, arg, rows = Fr(0), None, None, {}
    for r in sorted(cases):
        cs = cases[r]
        best_sel = max(best_sel, cs["J_select"])
        if cs["J_greedy"] is None or r in excluded_ranks:
            rows[r] = "excluded"
            continue
        Jr = max(Fr(1), cs["J_greedy"], best_sel)
        rows[r] = Jr
        if Jmin is None or Jr < Jmin:
            Jmin, arg = Jr, r
    Jr = max(Fr(1), best_sel)
    rows[n - 1] = Jr
    if Jr < Jmin:
        Jmin, arg = Jr, n - 1
    K, _, _ = flag_constants(n)
    plain = n * (-ln(K) / 2 + ln(R_N[n]) - ln(n)) - ln(lcm_upto(n + 1))
    gain = n * ln(Jmin) / 2
    return {"J(r)": rows, "J_min": Jmin, "argmin": arg, "plain target": plain,
            "gain": gain, "new target": plain - gain}
