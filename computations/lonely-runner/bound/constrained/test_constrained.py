"""Tests for the constrained shape bounds (run: python3 -m pytest test_constrained.py).

The slow tests re-run the four claimed proofs (C_5^F <= 2855/1000: 13.5 M
boxes, about 16 min on one core; C_4, C_6, R_17: about 9, 14 and 3 min);
set CONSTRAINED_FAST=1 to skip them (the other 9 tests take about 90 s)."""
import os
import random
import sys
from fractions import Fraction as Fr

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import constrained_shape as CS  # noqa: E402
import assemble  # noqa: E402

FAST = os.environ.get("CONSTRAINED_FAST") == "1"
N = 17


# ------------------------------------------------------------------ exact loneliness oracle
def lonely_integer(v, n, theta=None):
    """Exact decision for positive integer speeds v: is there tau with
    ||tau v_i|| >= theta (default 1/(n+1)) for all i?  The good set in [0,1)
    is a finite union of closed intervals whose endpoints are
    (k + theta)/v_i and (k + 1 - theta)/v_i, so it is non-empty iff one of
    these points is good."""
    th = Fr(1, n + 1) if theta is None else Fr(theta)
    def good(tau):
        for x in v:
            y = (tau * x) % 1
            if y < th or y > 1 - th:
                return False
        return True
    for x in v:
        for k in range(x):
            for e in (k + th, k + 1 - th):
                if good(e / x):
                    return True
    return False


def shape_of(v):
    v = sorted(v, reverse=True)
    return [Fr(x, v[0]) for x in v]


def test_sweep_lemmas_against_exact_oracle():
    """Whenever C1, C2 or C3 certifies a shape, the exact oracle finds a
    lonely time (C1-C3 use no lower case of the conjecture)."""
    rng = random.Random(17)
    c = CS.Consts(N)
    hits = {"C1": 0, "C2": 0, "C3": 0}
    for trial in range(1500):
        top = rng.randint(40, 400)
        v = rng.sample(range(1, top + 1), N - 1) + [top]
        if len(set(v)) < N:
            continue
        u = shape_of(v)
        s, t, m = u[1], u[2], u[-1]
        for cond in hits:
            if CS.lonely_point(c, s, t, m, use=(cond,)):
                hits[cond] += 1
                assert lonely_integer(v, N), (cond, v)
    assert all(h > 0 for h in hits.values()), hits


def test_sweep_C3_strictly_extends_C2():
    """Some shapes are certified by C3 and not by C1 or C2 (rational check)."""
    c = CS.Consts(N)
    found = 0
    rng = random.Random(3)
    for _ in range(20000):
        top = rng.randint(100, 2000)
        s = Fr(rng.randint(top // 20, top), top)
        t = Fr(rng.randint(1, s.numerator * top // s.denominator), top) if s.numerator else s
        m = Fr(rng.randint(1, max(1, top // 17)), top)
        if not (s >= t >= m):
            continue
        if CS.lonely_point(c, s, t, m, use=("C3",)) and not CS.lonely_point(c, s, t, m, use=("C1", "C2")):
            found += 1
    assert found > 0


def test_oracle_and_lemma_negative_control():
    """With a threshold theta' slightly above 1/(n+1), the tight instance
    (1, ..., n) (ML = 1/(n+1) exactly) is NOT lonely: the oracle must say so,
    the true lemmas (run at theta') must not certify it, and a broken C2
    (window b replaced by 0) must wrongly certify it -- which the oracle
    catches."""
    thp = Fr(1, N + 1) + Fr(1, 10 ** 4)
    v = list(range(1, N + 1))
    assert lonely_integer(v, N) and not lonely_integer(v, N, thp)
    c = CS.Consts(N, thp)
    u = shape_of(v)
    s, t, m = u[1], u[2], u[-1]
    assert not CS.lonely_point(c, s, t, m)
    l2 = (1 - c.th) / s - c.th / m
    assert l2 >= 0          # the broken lemma "l2 >= 0 => lonely" fires ...
    assert not lonely_integer(v, N, thp)   # ... and is refuted by the oracle


def test_tight_instance_not_excluded():
    """(1..n)/n is a tight instance (ML = 1/(n+1) exactly): it is lonely in the
    closed sense, and C1 certifies it (u_n = 1/n).  Its open-sense variant is
    the boundary of the feasible region: m < 1/n fails exactly here."""
    c = CS.Consts(N)
    u = shape_of(list(range(1, N + 1)))
    assert u[-1] == Fr(1, N) and CS.lonely_point(c, u[1], u[2], u[-1], use=("C1",))


# ------------------------------------------------------------------ 1-D lemmas
def test_w_identity_and_concavity_radius():
    assert CS.check_w_second_derivative()
    xc = CS.x_concave(N)
    assert xc * xc * 3 * N < 1 and (xc + Fr(1, 10 ** 6)) ** 2 * 3 * N >= 1


def test_one_dimensional_bounds_bracket_float_optimum():
    import math
    for lam in [Fr(1, 17), Fr(1, 2), Fr(9, 10)]:
        ub = CS.M2(N, lam)
        best = max(2 / N * math.log(x) - float(lam) * x * x - math.log(1 + 2 * x - x * x)
                   for x in [k / 100000 for k in range(1, 100001)])
        assert best <= float(ub) <= best + 1e-6
    for lam in [Fr(2, 17), Fr(1), Fr(2)]:
        lb = CS.Mg(N, lam)
        best = min(float(lam) * x * x / (1 + 2 * x - x * x) + math.log(1 + 2 * x - x * x) - 2 / N * math.log(x)
                   for x in [k / 100000 for k in range(1, 100001)])
        assert best - 1e-6 <= float(lb) <= best


# ------------------------------------------------------------------ the proofs
PROOFS = [("phi", 5, Fr(2855, 1000)), ("phi", 4, Fr(2243, 1000)), ("phi", 6, Fr(3652, 1000)), ("R", None, Fr(433, 1000))]


@pytest.mark.skipif(FAST, reason="CONSTRAINED_FAST=1")
@pytest.mark.parametrize("kind,r,target", PROOFS)
def test_branch_and_bound_proofs(kind, r, target):
    res = CS.branch_and_bound(N, kind, target, r=r)
    assert res["proved"], res


def test_negative_control_below_sup_fails():
    """A target below the constrained float sup must NOT be provable: the
    rational shape below satisfies none of C1, L1, C2, C3 (so it is in F) and
    has Phi_5 > 2.85 (float search optimum, rounded)."""
    import math
    c = CS.Consts(N)
    u = [Fr(1), Fr(37974, 100000), Fr(32671, 100000)] + [Fr(30443, 100000)] * 3 + [Fr(6783, 100000)] * 10 + [Fr(2338, 100000)]
    assert not CS.lonely_point(c, u[1], u[2], u[-1])
    uf = [float(x) for x in u]
    logphi = (math.log(4 * N * N) + 2 / N * sum(math.log(x) for x in uf) - math.log(sum(x * x for x in uf))
              - sum(math.log(1 + 2 * x - x * x) for x in uf[6:]))
    assert math.exp(logphi) > 2.85
    res = CS.branch_and_bound(N, "phi", Fr(285, 100), r=5, max_boxes=300000)
    assert not res["proved"]


def test_negative_control_unconstrained_fails():
    """Without the constraints the unconstrained sup C_5 ~ 3.0098 is
    recovered: a target of 2.9 must fail, and 3.0098 lies below the old
    proved C_5 <= 3.0098 (bound/relrank_n.shape_constant)."""
    res = CS.branch_and_bound(N, "phi", Fr(29, 10), r=5, use=(), max_boxes=300000)
    assert not res["proved"]


def test_assembly_regression_and_new_target():
    base = assemble.rank_target()
    assert abs(float(base["target"]) - 647.534682) < 1e-6 and base["argmin"] == 5
    new = assemble.rank_target(overrides={5: Fr(2855, 1000)})
    assert new["argmin"] == 5
    assert abs(float(new["target"]) - 647.085815) < 1e-6
