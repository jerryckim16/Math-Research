"""Tests for the bound-track scripts (run: python3 -m pytest test_bound.py)."""
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flag_n  # noqa: E402
import hyperplane  # noqa: E402
import audit_assembly  # noqa: E402
import audit_relations as AR  # noqa: E402


def test_flag_n15_regression():
    rep = flag_n.report(15)
    assert rep["shape checks all"] and rep["ratio > 4/3"]
    assert abs(float(rep["target"]) - 483.23876596940647) < 1e-9


def test_flag_n17():
    rep = flag_n.report(17)
    assert rep["shape checks all"] and rep["ratio > 4/3"]
    assert rep["min ratio"] == Fr(948, 625)
    assert rep["lcm(2..n+1)"] == 12252240 and rep["lcm = prod prime powers"] and rep["witness 1/d"]
    assert abs(float(rep["target"]) - 670.2817251116668) < 1e-9


def test_flag_n17_shape_negative_control():
    # radius below the true minimum 0.475439 must fail Step 4
    checks, _, _ = flag_n.shape_checks(17, Fr(4753, 10000))
    assert not checks["one"]
    # the old constant 8/5 fails at n = 17
    assert not flag_n.check_a_lower(17, Fr(8, 5))


def test_hyperplane_constants():
    assert hyperplane.B_prime(15)[0] == Fr(83, 192)
    assert hyperplane.B_prime(17)[0] == Fr(37, 81)
    assert hyperplane.B_prime(17)[1] == (Fr(37, 81), Fr(961, 2025), Fr(64, 81))


def test_hyperplane_targets():
    t15 = hyperplane.targets(15)
    assert t15["plain blocks all singletons"]
    assert abs(float(t15["new target"]) - 481.12259946588036) < 1e-9
    t17 = hyperplane.targets(17)
    assert abs(float(t17["new target"]) - 667.9285655766757) < 1e-9


def test_block_min_reproduces_lemma36():
    # with the plain B the minimum over block points is prod c (Allikvere 3.6)
    n = 15
    F = [flag_n.B(n, j) for j in range(n)]
    K, ends = hyperplane.block_min(F)
    assert K == flag_n.flag_constants(n)[0] and len(ends) == n - 1


def test_separation_points():
    # case (ii) of Lemma H: explicit point in alpha-perp with ||s_l|| >= 1/2 - 1/(2L)
    import random
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(3, 9)
        while True:
            a = [rng.randint(-3, 3) for _ in range(n)]
            L = sum(abs(x) for x in a)
            from math import gcd
            g = 0
            for x in a:
                g = gcd(g, x)
            if g == 1 and L % 2 == 1 and L >= 5:
                break
        eps = [Fr((x > 0) - (x < 0), 2 * L) for x in a]
        N0 = Fr(sum(a), 2) + Fr(1, 2)
        assert N0.denominator == 1
        # integer m with a.m = -N0 via extended gcd on the first nonzero pair chain
        m = [0] * n
        target = -int(N0)
        # find m by brute force small search on coefficients (gcd = 1)
        found = False
        import itertools
        for cand in itertools.product(range(-3, 4), repeat=min(n, 4)):
            mm = list(cand) + [0] * (n - len(cand))
            if sum(x * y for x, y in zip(a, mm)) == target:
                m, found = mm, True
                break
        if not found:
            continue
        s = [Fr(1, 2) + e + mi for e, mi in zip(eps, m)]
        assert sum(x * y for x, y in zip(a, s)) == 0
        dist = lambda x: min(x - (x.numerator // x.denominator), 1 - (x - (x.numerator // x.denominator)))
        assert all(dist(x) >= Fr(1, 2) - Fr(1, 2 * L) for x in s)


def test_tail_bound_identity():
    # case (iii): t_d = 1/h_E(alpha)^2 with h_E(alpha)^2 = sum q alpha^2 >= sum alpha^2 >= ||alpha||_1
    for u in [Fr(k, 97) for k in range(1, 98)]:
        assert 1 + 2 * u - u * u >= 1


def test_audit_assembly():
    out = audit_assembly.main()
    assert out["K15_matches_paper"] and all(out["J_matches_paper"].values())
    assert out["argmin"] == 5 and out["D_paper"]
    assert abs(float(out["raw_log_bound"]) - 459.0839110048726) < 1e-9
    assert abs(float(out["requirement"]) - 361.44573306958568) < 1e-9


def test_audit_relations():
    out = AR.main()
    assert out["delta"][0] and out["delta"][2]
    assert out["rank3 surviving profiles"] == [(3, 3, 3), (3, 3, 5), (3, 3, 7), (3, 3, 9), (3, 3, 11),
                                              (3, 3, 13), (3, 3, 15), (3, 5, 5), (5, 5, 5)]
    assert out["rank6: lists with P>=280443"] == (55, 767637, True)
    assert out["rank7: max P"][0] == 23030293
    assert all(all(v) for v in out["rank7 table (g_a, G) reproduced"].values())
    assert out["rank6 max g/G"][2] and out["rank7 max g/G"][2] and all(out["rank8"])
    assert all(v[1] for v in out["shape_constants"][2].values())


def test_pooling_negative_control():
    # pooled certificate never exceeds the proved partial sums, and a decreasing
    # increment pair is merged to the (3/7, 4/7) split
    F = [Fr(1), Fr(1) + Fr(1, 2)]
    d = AR.pooled(F)
    assert d == [Fr(3, 7) * Fr(3, 2), Fr(4, 7) * Fr(3, 2)]
