"""Tests for the EFX checker.  Run:  python3 -m pytest -q test_efx.py
(or  python3 test_efx.py).

1. C checker == pure-Python n^m brute force on random tiny instances,
   including the exact count of EFX allocations (zeros and ties included).
2. Known theorems reproduced on random instances: n = 2 (Plaut-Roughgarden),
   n = 3 (Chaudhury-Garg-Mehlhorn), identical valuations, m <= n+3.
3. Every witness returned is re-checked by the independent `verify`.
4. Hand-made sanity cases: a non-EFX allocation is rejected; the two
   "diagonal" valuations of Alkassar-Fouz-Mehlhorn (arXiv:2608.08590, Sec. 7)
   give exactly the EFX counts printed there (1680 and 5544).
5. CEGAR certifier: small known cases are unsat, re-check with full clauses
   (Z3) and with the independent cvc5 encoding agrees, and a truncated
   certificate is sat (negative control).
6. Lemma C0' (agent 0 has the largest normalised top-two sum) by brute force:
   the canonicalisation map of the soundness proof sends random instances
   (ties, zeros) into the C0-constrained branch and cube regions as encoded
   by cegar.region, and preserves the exact number of EFX allocations; a
   non-maximising choice of agent 0 violates the region (negative control).
7. AFM Lemma M items 1-3 as implemented in cegar.clause(lemma_m=True): the
   reduced clause has the same truth value as the full clause at random exact
   points of chain regions with many ties.
8. recheck_cvc5.tree_coverage: a split branch is covered by all its cubes,
   not by all but one, and records with mixed C0 flags are refused.
"""
import random

import efx


def rand_inst(n, m, B, rng, zero_p=0.2):
    return [[0 if rng.random() < zero_p else rng.randint(0, B) for _ in range(m)]
            for _ in range(n)]


def test_vs_brute_force():
    rng = random.Random(1)
    for trial in range(400):
        n = rng.randint(1, 4)
        m = rng.randint(0, 7 if n <= 3 else 6)
        B = rng.choice([1, 2, 3, 10, 100])
        v = rand_inst(n, m, B, rng)
        if m == 0:
            continue
        allb = efx.brute(v, want_all=True)
        ok, sc, cnt, wit = efx.full(v)
        assert ok == (len(allb) > 0)
        assert cnt == len(allb), (v, cnt, len(allb))
        ok0, wit0 = efx.exists(v)
        assert ok0 == ok
        if ok:
            assert efx.verify(v, wit0)
            assert efx.verify(v, wit)
            assert sc >= 0
        else:
            assert sc < 0


def test_two_and_three_agents():
    rng = random.Random(2)
    for trial in range(300):
        n = rng.choice([2, 3])
        m = rng.randint(1, 10)
        v = rand_inst(n, m, rng.choice([5, 50, 1000]), rng)
        ok, wit = efx.exists(v)
        assert ok and efx.verify(v, wit)


def test_identical_and_small_m():
    rng = random.Random(3)
    for trial in range(200):
        n = rng.randint(2, 5)
        m = rng.randint(1, 9)
        row = [rng.randint(0, 30) for _ in range(m)]
        v = [row[:] for _ in range(n)]
        ok, wit = efx.exists(v)
        assert ok and efx.verify(v, wit)
    for trial in range(200):
        n = 4
        m = rng.randint(1, 7)  # m <= n + 3 (Mahara)
        v = rand_inst(n, m, 100, rng)
        ok, wit = efx.exists(v)
        assert ok and efx.verify(v, wit)


def test_verify_rejects():
    v = [[5, 1, 1], [5, 1, 1]]
    # agent 0 gets nothing, agent 1 gets all: agent 0 envies {g1,g2} (=2 > 0)
    assert not efx.verify(v, [1, 1, 1])
    # agent 0 gets good 0, agent 1 gets {1,2}: EFX
    assert efx.verify(v, [0, 1, 1])
    # zero-valued goods count (EFX_0): agent 0 values {1} at 1 > 0 = own
    v = [[0, 1, 0], [1, 1, 1]]
    assert not efx.verify(v, [0, 1, 1])


def test_afm_diagonal_counts():
    # Alkassar-Fouz-Mehlhorn, arXiv:2608.08590v1, Sec. "Why it is hard":
    # four identical rows; 1680 resp. 5544 EFX_0 allocations out of 4^9.
    vA = [9200, 120, 100, 99, 98, 97, 96, 95, 95]
    vB = [1200, 1110, 1099, 1099, 1099, 1099, 1098, 1098, 1098]
    okA, _, cA, _ = efx.full([vA] * 4)
    okB, _, cB, _ = efx.full([vB] * 4)
    assert okA and okB
    assert cA == 1680, cA
    assert cB == 5544, cB


def test_cegar_small():
    import cegar
    import recheck_cvc5
    for n, m, br in ((3, 5, None), (4, 5, None), (3, 6, [[0, 1], [0, 2]])):
        res = cegar.cegar(n, m, br, timeout=120)
        assert res["status"] == "unsat", res["status"]
        assert cegar.recheck(n, m, br, res["allocs"]) == "unsat"
        rec = {"n": n, "m": m, "branch": br, "allocs": res["allocs"]}
        assert str(recheck_cvc5.check_record(rec)) == "unsat"
        rec["allocs"] = res["allocs"][:-1]   # drop the last clause: must be sat
        assert str(recheck_cvc5.check_record(rec)) == "sat"


def _top2(row):
    s = sorted(row, reverse=True)
    return s[0] + s[1]


def _canon_c0(v):
    """The map in the proof of Lemma C0' (problem file): normalise, make an
    agent with maximal top-two sum agent 0, sort goods by its values, sort
    agents 1..n-1 by (top good, second good).  Returns the normalised profile
    (Fractions) and the branch and cube labels."""
    from fractions import Fraction
    n, m = len(v), len(v[0])
    w = [[Fraction(x, sum(r)) for x in r] for r in v]
    a = max(range(n), key=lambda i: _top2(w[i]))
    w = [w[a]] + [w[i] for i in range(n) if i != a]
    pi = sorted(range(m), key=lambda g: -w[0][g])          # stable: ties keep order
    w = [[r[pi[g]] for g in range(m)] for r in w]
    def lab(r):
        b = max(range(m), key=lambda g: (r[g], -g))
        s = max((g for g in range(m) if g != b), key=lambda g: (r[g], -g))
        return b, s
    rest = sorted(w[1:], key=lab)
    w = [w[0]] + rest
    return w, [lab(r)[0] for r in rest], [list(lab(r)) for r in rest]


def _in_region(w, branch, c0):
    import z3
    import cegar
    n, m = len(w), len(w[0])
    V = cegar.build_vars(n, m)
    s = z3.Solver()
    s.add(cegar.region(V, n, m, branch, c0=c0))
    s.add([V[i][g] == z3.RealVal(w[i][g]) for i in range(n) for g in range(m)])
    return s.check() == z3.sat


def _to_int(w):
    import math
    out = []
    for r in w:
        d = 1
        for x in r:
            d = d * x.denominator // math.gcd(d, x.denominator)
        out.append([int(x * d) for x in r])
    return out


def test_c0_canonicalisation():
    rng = random.Random(7)
    for trial in range(300):
        m = rng.randint(3, 6)
        B = rng.choice([2, 3, 9, 100])
        v = [[rng.randint(0, B) for _ in range(m)] for _ in range(4)]
        for r in v:
            if sum(r) == 0:
                r[rng.randrange(m)] = 1   # zero rows: AFM Normalization lemma (tested separately below)
        if rng.random() < 0.3:              # near-identical rows with a shared top good
            base = sorted([rng.randint(1, B) for _ in range(m)], reverse=True)
            v = [[x + rng.randint(0, 1) for x in base] for _ in range(4)]
        w, br, cube = _canon_c0(v)
        assert _in_region(w, br, True), (v, w, br)
        assert _in_region(w, cube, True), (v, w, cube)
        assert efx.full(v)[2] == efx.full(_to_int(w))[2]
        # negative control: a strictly non-maximising agent as agent 0 must fail C0
        t2 = [_top2(r) for r in w]
        worse = [i for i in range(1, 4) if t2[i] < t2[0]]
        if worse:
            from fractions import Fraction
            i = worse[0]
            u = [w[i]] + [w[k] for k in range(4) if k != i]
            pi = sorted(range(m), key=lambda g: -u[0][g])
            u = [[r[pi[g]] for g in range(m)] for r in u]
            brs = [max(range(m), key=lambda g: (r[g], -g)) for r in u[1:]]
            order = sorted(range(3), key=lambda k: brs[k])
            u = [u[0]] + [u[1 + k] for k in order]
            assert not _in_region(u, sorted(brs), True)
            assert _in_region(u, sorted(brs), False)
    # zero row replaced by a positive row: an EFX allocation of the new
    # instance is EFX for the old one (the zero agent has no constraint)
    for trial in range(100):
        m = rng.randint(2, 6)
        v = [[rng.randint(0, 5) for _ in range(m)] for _ in range(3)] + [[0] * m]
        ok, wit = efx.exists(v[:3] + [[1] * m])
        assert ok and efx.verify(v, wit)


def test_lemma_m_equivalence():
    import itertools
    import z3
    import cegar
    rng = random.Random(8)
    n = 4
    for trial in range(150):
        m = rng.randint(4, 7)
        chains = []
        for i in range(1, n):
            k = rng.randint(1, 3)
            chains.append(rng.sample(range(m), k))
        pres = cegar.prefixes_of(n, m, chains)
        V = cegar.build_vars(n, m)
        for _ in range(4):
            # an exact point of the region with ties: values in {0..3}, arranged
            w = []
            for i in range(n):
                vals = sorted([rng.randint(0, 3) for _ in range(m)], reverse=True)
                if sum(vals) == 0:
                    vals[0] = 1
                p = pres[i]
                rest = [g for g in range(m) if g not in p]
                rng.shuffle(rest)
                row = [0] * m
                for t, g in enumerate(list(p) + rest):
                    row[g] = vals[t]
                w.append(row)
            sub = [(V[i][g], z3.RealVal(w[i][g])) for i in range(n) for g in range(m)]
            for _ in range(15):
                a = [rng.randrange(n) for _ in range(m)]
                red = z3.is_true(z3.simplify(z3.substitute(cegar.clause(V, a, n, m, chains, lemma_m=True), *sub)))
                old = z3.is_true(z3.simplify(z3.substitute(cegar.clause(V, a, n, m, chains), *sub)))
                full = not efx.verify(w, a)
                assert red == full == old, (w, a, chains)


def test_tree_coverage():
    """recheck_cvc5.tree_coverage: a branch replaced by all its cubes (from
    cegar_branches.refine) is covered; dropping one cube uncovers it; mixing
    c0 flags is refused."""
    import itertools
    import cegar_branches as cb
    import recheck_cvc5 as rc
    m = 5
    rec = lambda br, c0=False: {"n": 4, "m": m, "branch": br, "c0": c0}
    roots = [list(b) for b in itertools.combinations_with_replacement(range(m), 3)]
    split = [0, 0, 0]
    cubes = [[list(c) for c in node] for node in cb.refine([[0], [0], [0]], m)]
    recs = [rec(b) for b in roots if b != split] + [rec(c) for c in cubes]
    assert rc.tree_coverage(recs)[4] == []
    missing = rc.tree_coverage(recs[:-1])[4]
    assert missing == [((0,), (0,), (0,))], missing
    deep = [[list(c) for c in node] for node in cb.refine(cubes[-1], m)]
    assert rc.tree_coverage(recs[:-1] + [rec(d) for d in deep])[4] == []
    try:
        rc.tree_coverage(recs[:-1] + [rec(cubes[-1], c0=True)])
        assert False, "mixed c0 flags must be refused"
    except AssertionError as e:
        assert "disagree" in str(e)


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
