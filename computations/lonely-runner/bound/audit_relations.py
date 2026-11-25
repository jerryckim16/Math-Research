"""Independent checks of the finite/numeric steps of the relation-rank
analysis in J. Allikvere, "Sixteen lonely runners" (Zenodo
doi:10.5281/zenodo.23304361), Appendices A-D, written from the TeX source.
None of the author's code or data is executed or imported.

Everything is exact (Fractions / integers) except `delta_interval`, which uses
mpmath interval arithmetic.

  delta_interval      5137/1000 < delta = 1/(1-cos(pi/8)) - 8 < 2569/500
  greedy(r)           Lemma "greedy support bound": support lists s_1<=..<=s_r
                      (odd, 3..15) whose greedy upper bound on the positive
                      odd weight exceeds delta at some endpoint survive
  shape_constants     the rational AM-GM bounds C'_r < D_r (App. A.1)
  pooled(F)           weighted PAV pooling of App. A.2; G(r,a) factors
  full_row_index      Lemma "parity and the saturation index" bound
  rank6/7/8 tables    the g_a / G(r,a) maxima quoted in App. D
"""
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
from math import prod

DLO, DHI = Fr(5137, 1000), Fr(2569, 500)
ODD = [3, 5, 7, 9, 11, 13, 15]


def delta_interval():
    from mpmath import iv, mp
    iv.prec = 200
    c = 1 - iv.cos(iv.pi / 8)
    d = 1 / c - 8
    from mpmath.libmp import to_rational
    lo, hi = (Fr(*to_rational(x)) for x in d._mpi_)   # exact enclosure ends
    # polynomial claimed in the paper, X^4+16X^3+40X^2-416X-1784, vanishes on d
    P = d ** 4 + 16 * d ** 3 + 40 * d ** 2 - 416 * d - 1784
    pa, pb = (Fr(*to_rational(x)) for x in P._mpi_)
    return DLO < lo and hi < DHI, (float(lo), float(hi)), pa <= 0 <= pb


def w(s, d):
    return (d + s) / Fr(2 ** (s - 1))


def greedy_bound(ss, d):
    return w(ss[0], d) + sum(2 * 3 ** (j - 2) * w(ss[j - 1], d) for j in range(2, len(ss) + 1))


def survives(ss):
    """Not excluded: bound > delta at some endpoint (bound - delta is affine
    in delta, so checking both endpoints decides the whole interval)."""
    return any(greedy_bound(ss, d) > d for d in (DLO, DHI))


def greedy(r):
    lists = list(combinations_with_replacement(ODD, r))
    surv = [s for s in lists if survives(s)]
    return lists, surv


def shape_constants():
    """(C'_r)^240 < D_r^240 as an exact rational inequality (App. A.1)."""
    L, U = Fr(7793654, 10 ** 8), Fr(7793655, 10 ** 8)
    q = lambda z: 1 + 2 * z - z * z
    ok_root = 15 * L * L - 14 * L + 1 > 0 > 15 * U * U - 14 * U + 1 and U < Fr(1, 10)
    rows = {4: Fr(11, 4), 5: Fr(359, 100), 6: Fr(47, 10), 7: Fr(31, 5), 8: Fr(206, 25)}
    res = {}
    for r, D in rows.items():
        m = 14 - r
        w0 = 1 - Fr(r, 15) - Fr(m, 240)
        assert 240 * w0 == int(240 * w0)
        lhs = Fr(900) ** 240 * w0 ** int(240 * w0) * Fr(1, 15) ** (16 * r) * Fr(1, 240) ** m \
            * U ** (30 * m) / q(L) ** (240 * m)
        res[r] = (w0, lhs < D ** 240)
    # h(1/16) > h(1) = 1/2, i.e. (1/16)^(1/8)/q(1/16) > 1/2  <=>  (1/16) > (q/2)^8
    hcmp = Fr(1, 16) > (q(Fr(1, 16)) / 2) ** 8
    return ok_root, hcmp, res


def B(j):
    return Fr(j * j, 64 * (16 - j) ** 2) if j else Fr(0)


def cc(j):
    return B(j) - B(j - 1)


def pooled(F):
    """Weighted PAV of App. A.2 on increments e_i = F_i - F_{i-1}, weights
    a_i = (4/3)^(i-1); returns d (list)."""
    m = len(F)
    e = [F[0]] + [F[i] - F[i - 1] for i in range(1, m)]
    a = [Fr(4, 3) ** i for i in range(m)]
    blocks = [[i] for i in range(m)]
    def avg(b):
        return sum(e[i] for i in b) / sum(a[i] for i in b)
    changed = True
    while changed:
        changed = False
        for k in range(len(blocks) - 1):
            if avg(blocks[k]) > avg(blocks[k + 1]):
                blocks[k:k + 2] = [blocks[k] + blocks[k + 1]]
                changed = True
                break
    d = [None] * m
    for b in blocks:
        A = avg(b)
        for i in b:
            d[i] = a[i] * A
    # certificate properties (eq. pooled-certificate)
    assert all(x > 0 for x in d)
    assert all(3 * d[i + 1] >= 4 * d[i] for i in range(m - 1))
    s = Fr(0)
    for j in range(m):
        s += d[j]
        assert s <= F[j]
    return d


def G(r, a):
    """gamma from Lemma support-prefix: F_j = B_j (j < 17-a), B_{j+1} (j >= 17-a)."""
    m = 14 - r
    F = [B(j) if j < 17 - a else B(j + 1) for j in range(1, m + 1)]
    d = pooled(F)
    return prod(d) / prod(cc(j) for j in range(1, m + 1))


def full_row_index(r, a):
    return (a - 1) ** r if a % 2 == 0 else a * (a - 2) ** (r - 1)


def main():
    out = {}
    out["delta"] = delta_interval()
    for r in (1, 2, 3, 4, 5, 6, 7, 8):
        lists, surv = greedy(r)
        out[f"greedy r={r}"] = (len(lists), len(surv), max((prod(s) for s in surv), default=None))
    _, s3 = greedy(3)
    out["rank3 surviving profiles"] = s3
    lists6, s6 = greedy(6)
    big = [s for s in s6 if prod(s) >= 280443]
    out["rank6: lists with P>=280443"] = (len(big), max(prod(s) for s in big), max(prod(s) for s in big) < 4 * 280443)
    _, s7 = greedy(7)
    out["rank7: max P"] = max((prod(s), s) for s in s7)
    out["shape_constants"] = shape_constants()
    # gamma factors
    out["G(6,9)"] = G(6, 9)
    out["gamma(r,r+3) = 1 + c_{m+1}/c_m ?"] = all(G(r, r + 3) == 1 + cc(15 - r) / cc(14 - r) for r in range(4, 9))
    g6 = {7: 36015, 8: 36015, 9: 117649, 10: 178605}
    g6.update({a: 280442 for a in range(11, 16)})
    q6 = {a: Fr(g6[a]) / G(6, a) for a in g6}
    out["rank6 max g/G"] = max(q6.values()), max(q6, key=q6.get), max(q6.values()) == Fr(5764801, 130)
    paper7 = {8: (823543, Fr(1)), 9: (1058841, Fr(1)), 10: (4782969, Fr(81, 31)),
              11: (5845851, Fr(21870000, 5330171)), 12: (19487171, Fr(915062500, 139157109)),
              13: (23030293, Fr(838338336, 78048425)), 14: (23030293, Fr(1004152032, 54327427)),
              15: (23030293, Fr(5597956, 154275))}
    chk7 = {}
    for a, (ga, Ga) in paper7.items():
        chk7[a] = (min(23030293, full_row_index(7, a)) == ga, G(7, a) == Ga)
    out["rank7 table (g_a, G) reproduced"] = chk7
    q7 = {a: Fr(paper7[a][0]) / G(7, a) for a in paper7}
    out["rank7 max g/G"] = max(q7.values()), max(q7, key=q7.get), max(q7.values()) == Fr(185218112079, 62500)
    g8_hi = max(full_row_index(8, a) for a in range(11, 16))
    g8_lo = max(full_row_index(8, a) for a in range(9, 11))
    gam8 = (4 * (Fr(1, 9) - Fr(1, 16)) ** 2 - B(5)) / cc(6)
    out["rank8"] = (g8_hi == 15 * 13 ** 7, g8_lo <= 9 ** 8, gam8 == Fr(6100, 2349),
                    G(8, 11) == gam8, max(Fr(9 ** 8), 15 * 13 ** 7 / gam8) == Fr(442188799299, 1220))
    return out


if __name__ == "__main__":
    for k, v in main().items():
        print(k, ":", v)
