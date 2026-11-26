"""Tests for the general-n computations (notes/lonely-runner/general-n.md).

Run from this directory:  python3 -m pytest -q test_generaln.py
Includes negative controls: the solver must find counterexamples at the
too-high threshold 1/m, Theorem 1's case split must fail beyond its range,
and the Theorem D family must fail for composite 2m+1.
"""
import os
import subprocess
import sys
from fractions import Fraction
from itertools import combinations
from math import gcd

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from lonely import find_witness, max_loneliness, check_witness  # noqa: E402
import jacobsthal  # noqa: E402
import theorem1  # noqa: E402


@pytest.fixture(scope="module")
def solver(tmp_path_factory):
    exe = str(tmp_path_factory.mktemp("bin") / "dwsolve")
    subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "dwsolve.c")], check=True)
    return exe


def run(exe, *args):
    out = subprocess.run([exe] + [str(a) for a in args], capture_output=True, text=True, check=True).stdout
    return out.splitlines()


def test_dw_small(solver):
    for m in range(2, 21):
        last = run(solver, m, 4 * m)[-1]
        assert "result=DW_HOLDS" in last, last


def test_negative_control_threshold(solver):
    # threshold 1/m instead of 1/(m+1): [1..m] (ML = 1/(m+1)) is a counterexample
    for m in range(2, 9):
        lines = run(solver, m, 4 * m, "k=%d" % m)
        assert "result=COUNTEREXAMPLE" in lines[-1]
        ce = [l for l in lines if l.startswith("COUNTEREXAMPLE")][0]
        V = list(map(int, ce.split(":")[1].split()))
        ok, _ = find_witness(V, Fraction(1, m))
        assert not ok  # independently confirmed: no witness at 1/m
        assert len(V) <= m and max(V) <= 2 * m


def test_negative_control_window(solver):
    # m speeds, window [1, H] with H > 2m, threshold 1/m: still must fail
    lines = run(solver, 5, 30, "k=5", "top=14")
    assert "result=COUNTEREXAMPLE" in lines[-1]


def test_python_bruteforce_agrees():
    # independent of dwsolve.c: every m-subset of [1,2m] is lonely, m <= 7
    for m in range(1, 8):
        for V in combinations(range(1, 2 * m + 1), m):
            ok, t = find_witness(V)
            assert ok and check_witness(V, t), V


def is_prime(N):
    return N > 1 and all(N % d for d in range(2, int(N ** 0.5) + 1))


def test_theorem_D_family(solver):
    # denominators <= 2m+2 suffice when 2m+1 is prime (Bonfioli's Theorem D) ...
    for m in range(2, 24):
        last = run(solver, m, 2 * m + 2, "fixed", "cap=0")[-1]
        if is_prime(2 * m + 1):
            assert "NO_TRANSVERSAL" in last, (m, last)
        elif m >= 7:
            # ... and fail for every composite 2m+1 >= 15 in this range
            assert "TRANSVERSALS_EXIST" in last, (m, last)


def test_theorem_D_times_exactly():
    # the three time families of Theorem D's proof, checked directly, m prime case
    for m in (2, 3, 5, 6):
        N = 2 * m + 1
        times = [Fraction(1, 2 * m + 2)] + [Fraction(1, q) for q in range(2, m + 2)]
        times += [Fraction(c, N) for c in range(1, N)]
        for k in range(1, m + 1):
            for V in combinations(range(1, 2 * m + 1), k):
                assert any(check_witness(V, t, Fraction(1, m + 1)) for t in times), V


def test_bonfioli_composite_example():
    V = [1, 2, 4, 5, 6, 7, 8]
    assert max_loneliness(V)[0] == Fraction(2, 13)
    assert not any(all(8 * min(v * c % 15, 15 - v * c % 15) >= 15 for v in V) for c in range(1, 15))


def test_jacobsthal_exact_and_bound():
    G, g = jacobsthal.G_table(2000)
    for s in range(1, 401):
        # brute-force definition on one period of rad(s), cyclically
        r = 1
        for p in range(2, s + 1):
            if s % p == 0 and all(p % q for q in range(2, int(p ** 0.5) + 1)):
                r *= p
        run_, best = 0, 0
        for x in range(2 * r):
            if gcd(x, r) == 1:
                run_ = 0
            else:
                run_ += 1
                best = max(best, run_)
        assert g[s] == best + 1, s
    ps = jacobsthal.primes_upto(2001)
    for s in range(2, 2001):
        pf = jacobsthal.prime_factors(s, ps)
        ratio = Fraction(1)
        for p in pf:
            ratio *= Fraction(p, p - 1)
        bound = (2 ** len(pf) - 1) * ratio
        assert g[s] <= -((-bound.numerator) // bound.denominator), s  # Lemma J
        assert g[s] <= jacobsthal.tail_bound(len(pf), ps)  # bound used in the tail
    assert [(x, G[x]) for x in range(1, 201) if G[x] != G[x - 1]] == [(1, 1), (2, 2), (6, 4), (30, 6)]


def test_corollary_thresholds():
    assert jacobsthal.n0_for_alpha(29, 20, 5000) == 81
    assert jacobsthal.n0_for_alpha(7, 5, 2000) == 21
    assert jacobsthal.n0_for_alpha(29, 20, 5000, sharp=True) == 61
    assert jacobsthal.n0_for_alpha(147, 100, 10000, sharp=True) == 85
    with pytest.raises(AssertionError):
        jacobsthal.n0_for_alpha(3, 2)


def test_theorem1_case_split():
    total, stats = theorem1.check_range(13)
    assert total > 5000 and set(stats) == {"small", "pair", "div"}


def test_theorem1_fails_beyond_range():
    # negative control: with max V near 2n the proof's case split must fail
    n = 12
    found = False
    for V in combinations(range(1, 2 * n + 1), n):
        if max(V) < 2 * n - 2:
            continue
        t, how = theorem1.proof_witness(V)
        if t is None:
            found = True
            assert find_witness(V)[0]  # still lonely, by another time
            break
    assert found


def test_fixed_mode_complete_vs_bruteforce(solver):
    # every m-set hitting all bad sets (q <= Q) must contain a reported leaf,
    # and every m-superset of a leaf must hit all bad sets
    for m, Q in [(7, 16), (10, 22), (12, 26)]:
        K = m + 1
        bads = []
        for q in range(2, Q + 1):
            for a in range(1, q // 2 + 1):
                if gcd(a, q) == 1:
                    bads.append({x for x in range(1, 2 * m + 1) if K * min(x * a % q, q - x * a % q) < q})
        brute = {V for V in combinations(range(1, 2 * m + 1), m) if all(set(V) & B for B in bads)}
        leaves = [set(map(int, l.split(":")[1].split()))
                  for l in run(solver, m, Q, "fixed", "cap=100000") if l.startswith("TRANSVERSAL")]
        ext = set()
        for L in leaves:
            assert all(L & B for B in bads)
            rest = [x for x in range(1, 2 * m + 1) if x not in L]
            for add in combinations(rest, m - len(L)):
                ext.add(tuple(sorted(L | set(add))))
        assert ext == brute and brute, m
