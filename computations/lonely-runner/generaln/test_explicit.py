"""Tests for notes/lonely-runner/general-n-explicit.md.

Run from this directory:  python3 -m pytest -q test_explicit.py
Negative controls: a corrupted matching certificate is rejected; Lemma H's
hypothesis is false on a pair of progressions that has no 2-coprime perfect
matching; the matching criterion fails one step above M*(n).
"""
import os
import random
import subprocess
import sys
from fractions import Fraction
from itertools import combinations
from math import gcd

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from lonely import find_witness  # noqa: E402
import check_matching as cm  # noqa: E402
import explicit_core as ec  # noqa: E402


@pytest.fixture(scope="module")
def mc(tmp_path_factory):
    exe = str(tmp_path_factory.mktemp("bin") / "matchcrit")
    subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "matchcrit.c")], check=True)
    return exe


def run(exe, *args):
    return subprocess.run([exe] + [str(a) for a in args], capture_output=True, text=True, check=True).stdout


def mstar_table(mc, a, b):
    out = run(mc, "scan", a, b)
    return {int(l.split()[0]): int(l.split()[1]) for l in out.splitlines()}


def odd_part_coprime(a, b):
    g = gcd(a, b)
    while g % 2 == 0:
        g //= 2
    return g == 1


def has_perfect_matching(left, right, ok):
    match = {}

    def aug(u, seen):
        for v in right:
            if ok(u, v) and v not in seen:
                seen.add(v)
                if v not in match or aug(match[v], seen):
                    match[v] = u
                    return True
        return False

    return all(aug(u, set()) for u in left)


def test_certificates_and_sharpness(mc):
    tab = mstar_table(mc, 1, 250)
    for n, Ms in tab.items():
        assert Ms >= n + 1 or n == 1
        if n == 1:
            continue
        n_, M_, pairs = cm.parse(run(mc, "cert", n, Ms))
        ok, why = cm.check_certificate(n, Ms, pairs)
        assert ok, (n, Ms, why)
        if Ms < 2 * n:   # criterion fails just above M*
            assert "FAIL" in run(mc, "test", n, Ms + 1)


def test_certificates_large(mc):
    for n, F in [(2252, 12), (12000, 12), (30011, 14)]:
        n_, M_, pairs = cm.parse(run(mc, "cert", n, 2 * n - F))
        assert cm.check_certificate(n, 2 * n - F, pairs)[0]


def test_negative_control_certificate(mc):
    n, M = 40, 78
    _, _, pairs = cm.parse(run(mc, "cert", n, M))
    assert cm.check_certificate(n, M, pairs)[0]
    bad = dict(pairs)
    s = 6
    bad[s] = next(t for t in range(n + 2, 2 * n + 3) if gcd(s, t) > 1 and t != 2 * s)
    assert not cm.check_certificate(n, M, bad)[0]
    bad = dict(pairs)
    bad[1], bad[2] = bad[2], bad[2]   # repeated t
    assert not cm.check_certificate(n, M, bad)[0]


def test_criterion_implies_lonely_small(mc):
    # Sanity check of Lemma C against the exact witness search (small n).
    tab = mstar_table(mc, 2, 8)
    for n in range(2, 9):
        Ms = tab[n]
        for V in combinations(range(1, Ms + 1), n):
            ok, _ = find_witness(list(V), Fraction(1, n + 1))
            assert ok, V


def test_lemma_H_negative_control():
    I, J = [105, 107], [63, 65]
    assert not has_perfect_matching(I, J, odd_part_coprime)
    assert not ec.check_H(2, 107)[0]


def test_lemma_H_against_bruteforce():
    rng = random.Random(1)
    tested = 0
    for _ in range(400):
        m = rng.randint(2, 40)
        N = rng.randint(2 * m, 1200)
        if not ec.check_H(m, N)[0]:
            continue
        a = rng.randint(1, N - 2 * (m - 1))
        b = rng.randint(1, N - 2 * (m - 1))
        I = [a + 2 * i for i in range(m)]
        J = [b + 2 * i for i in range(m)]
        assert has_perfect_matching(I, J, odd_part_coprime), (m, N, a, b)
        tested += 1
    assert tested > 50


def test_lemma_H_cover_reverified_and_monotone():
    for m, N in [(44, 256), (179, 131072), (397, 10 ** 6), (843, 8 * 10 ** 6)]:
        ok, info = ec.check_H(m, N)
        assert ok
        assert ec.verify_pieces(m, N, info["pieces"])
        for N2 in [N // 2, N // 7, 3 * m]:
            assert ec.check_H(m, N2)[0]
    assert not ec.check_H(396, 10 ** 6)[0]


def tau_from_blocks(n, M, m):
    """Lemma G (uniform blocks of length 2m), with brute-force block matchings."""
    A, L = M // 2, 2 * m
    q = -(-A // L)
    C = 2 * n + 3 - L
    tau = {}
    for jb in range(1, q + 1):
        I = list(range((jb - 1) * L + 1, jb * L + 1))
        J = list(range(C - jb * L, C - (jb - 1) * L))
        match = {}

        def aug(u, seen):
            for v in J:
                if gcd(u, v) == 1 and v not in seen:
                    seen.add(v)
                    if v not in match or aug(match[v], seen):
                        match[v] = u
                        return True
            return False

        for u in I:
            assert aug(u, set()), (n, M, m, jb)
        for v, u in match.items():
            tau[u] = v
    return {s: tau[s] for s in range(1, A + 1)}


def test_lemma_G_construction():
    for n, m in [(1023, 80), (4000, 83), (20000, 179)]:
        assert ec.check_H(m, 2 * n + 2)[0]
        M = 2 * n + 4 - 8 * m
        tau = tau_from_blocks(n, M, m)
        ok, why = cm.check_certificate(n, M, tau)
        assert ok, (n, M, m, why)


def test_theoremL_first_rows():
    import theoremL
    assert theoremL.least_m(2 * 127 + 2, 10 ** 6) == 44
    assert theoremL.least_m(2 * 131071 + 2, 10 ** 7) == 397
