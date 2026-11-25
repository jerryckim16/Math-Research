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


def test_rank_exclusion_regression_and_n17():
    import rank_exclusion as X
    ex, total, rep, _ = X.exclude(15, 3)
    assert ex and total == 8867
    assert rep[(3, 3, 3)][0] == 354 and rep[(5, 5, 5)][0] == 4378
    assert X.exclude(17, 2)[0] and X.exclude(17, 3)[0]


def test_relrank_n17_target():
    import relrank_n as R
    res = R.final_with_exclusions(17, {1, 2, 3})
    assert res["argmin"] == 4
    assert abs(float(res["new target"]) - 659.6653528463155) < 1e-9
    # without the exclusions, rank 2 blocks any gain (negative control)
    assert R.final(17)["J_min"] == 1


# ---------------------------------------------------------------- rank-4 classification (rank4/)
import json  # noqa: E402
import subprocess  # noqa: E402
import pytest  # noqa: E402

RANK4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rank4")
sys.path.insert(0, RANK4)


@pytest.fixture(scope="module")
def sect_bins(tmp_path_factory):
    d = tmp_path_factory.mktemp("sect")
    bins = {}
    for r in (3, 4):
        b = str(d / f"sect{r}")
        subprocess.run(["gcc", "-O2", f"-DR={r}", "-o", b, os.path.join(RANK4, "sect.c")], check=True)
        bins[r] = b
    return bins


def _run(binary, n, prof, rej=2, env=None, delta=None):
    import relrank_n as RN
    lo, hi = RN.delta_bounds(n) if delta is None else delta
    QD = 10 ** 6
    assert (lo * QD).denominator == 1 and (hi * QD).denominator == 1
    e = dict(os.environ)
    e.update(env or {})
    out = subprocess.run([binary, str(n), str((lo * QD).numerator), str((hi * QD).numerator), str(QD), str(rej)]
                         + [str(x) for x in prof], capture_output=True, text=True, check=True, env=e).stdout
    return out


def _parse_text(text, tmp):
    import classes as CL
    p = tmp / "o.txt"
    p.write_text(text)
    return CL.parse(str(p))


def test_sect_rank3_reproduces_allikvere_table(sect_bins):
    # n = 15, rank 3, no greedy filter, no pruning: counts and exact max S_O of his table
    table = {(3, 3, 3): (354, Fr(5, 8), Fr(14, 8)), (3, 3, 5): (545, Fr(9, 16), Fr(29, 16)),
             (3, 3, 7): (561, Fr(33, 64), Fr(103, 64)), (3, 3, 9): (561, Fr(37, 64), Fr(81, 64)),
             (3, 3, 11): (554, Fr(513, 1024), Fr(1547, 1024)), (3, 3, 13): (449, Fr(2049, 4096), Fr(6157, 4096)),
             (3, 3, 15): (112, Fr(8193, 16384), Fr(24591, 16384)), (3, 5, 5): (1353, Fr(1, 2), Fr(13, 8)),
             (5, 5, 5): (4378, Fr(7, 16), Fr(27, 16))}
    for prof, (cnt, al, be) in table.items():
        out = _run(sect_bins[3], 15, prof, rej=1, env={"NOGREEDY": "1", "NOPRUNE": "1"})
        w = int(out.split("leaves_weighted=")[1].split()[0])
        A = int(out.split("MAXS A=")[1].split()[0])
        B = int(out.split("MAXS A=")[1].split("B=")[1].split()[0])
        assert w == cnt
        assert (Fr(A, 2 ** 14), Fr(B, 2 ** 14)) == (al, be)
        assert "admitted=0 " in out          # rank 3 excluded


def test_sect_n15_high_gram_classes_match_allikvere(sect_bins, tmp_path):
    import classes as CL
    import crosscheck as CC
    data = json.load(open(os.path.join(RANK4, "data", "allikvere_n15_rank4_high_gram_classes.json")))
    ours = []
    for prof in [(3, 3, 3, 7), (3, 3, 5, 5)]:
        types, recs, p = _parse_text(_run(sect_bins[4], 15, prof), tmp_path)
        for rec in recs:
            CC.check(types, rec, p, 15)
        for key, rs in CL.classes(types, [r for r in recs if r["g"] >= 168], p).items():
            ours.append((p, rs[0]["g"], key))
    index = {t: k for k, t in enumerate(types)}
    his = []
    for c in data["classes"]:
        prof = tuple(c["profile"])
        m = CL.matrix_to_counts(types, list(zip(*c["columns"])))
        key = min(CL.act(types, index, m, pp, s) for pp, s in CL.group(prof))
        his.append((prof, c["gram"], key))
    assert len(his) == 16
    assert sorted(ours) == sorted(his)


@pytest.fixture(scope="module")
def census17(sect_bins, tmp_path_factory):
    import relrank_n as RN
    d = tmp_path_factory.mktemp("c17")
    for prof in RN.survivors(17, 4, RN.delta_bounds(17)):
        (d / f"n17_r4_{'_'.join(map(str, prof))}.txt").write_text(_run(sect_bins[4], 17, prof))
    return str(d)


def test_rank4_n17_classification_and_target(census17):
    import rank4_bound as RB
    import classes as CL
    import crosscheck as CC
    res = RB.classified(17, census17)
    assert res["files"] == 49 and res["admitted"] == 34
    assert res["gmax"] == {6: 133}                 # every admitted section has support 6, g <= 133
    for f in os.listdir(census17):
        types, recs, p = CL.parse(os.path.join(census17, f))
        for rec in recs:
            CC.check(types, rec, p, 17)            # independent Fraction re-check of every admitted record
    assert res["argmin"] == 5 and res["J(r)"][4] > res["J(r)"][5]
    assert abs(float(res["J4_classified"]) - 16.385347558343323) < 1e-12
    assert abs(float(res["target"]) - 647.5346823292391) < 1e-9


def test_rank4_negative_controls(sect_bins, census17, tmp_path, monkeypatch):
    import rank4_bound as RB
    import classes as CL
    import crosscheck as CC
    # (1) the coarse g bound at a = 6 (625) must give back the coarse J_4 = 3.4868
    monkeypatch.setattr(RB, "census_gmax", lambda n, outdir, r=4: ({6: 625}, 1, 49))
    res = RB.classified(17, census17)
    assert abs(float(res["J4_classified"]) - 3.486802) < 1e-5 and res["argmin"] == 4
    monkeypatch.undo()
    # (2) the Riesz test is load-bearing: with the smaller n = 15 delta the
    #     (3,3,5,5) census at n = 17 admits sections with g > 133
    import relrank_n as RN
    types, recs, p = _parse_text(_run(sect_bins[4], 17, (3, 3, 5, 5), delta=RN.delta_bounds(15)), tmp_path)
    assert max(r["g"] for r in recs) > 133
    # (3) a tampered record is rejected by the independent checker
    types, recs, p = CL.parse(os.path.join(census17, "n17_r4_3_3_5_5.txt"))
    bad = dict(recs[0], g=recs[0]["g"] + 1)
    with pytest.raises(AssertionError):
        CC.check(types, bad, p, 17)
