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


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
