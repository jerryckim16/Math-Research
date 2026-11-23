"""Tests for lonely.py, sieve.py and level1.c.  Run: python3 -m unittest -v"""
import random
import unittest
from fractions import Fraction
from itertools import product, combinations_with_replacement
from math import gcd, log, comb

from lonely import (find_witness, check_witness, check_no_witness_certificate,
                    max_loneliness, norm_frac)
import sieve
from sieve import Level, level1_improper, lift, project, B_bound_ok, log_B, run_gate


def ml_grid(v, G):
    """Lower bound for ML(v): best value over the grid t = m/G."""
    return max(min(norm_frac(Fraction(m * x, G)) for x in v) for m in range(G))


class TestChecker(unittest.TestCase):
    def test_tight_1_to_n(self):
        for n in range(1, 11):
            v = list(range(1, n + 1))
            ml, t = max_loneliness(v)
            self.assertEqual(ml, Fraction(1, n + 1))
            ok, w = find_witness(v)
            self.assertTrue(ok and check_witness(v, w))
            # no witness for any larger threshold
            d = Fraction(1, n + 1) + Fraction(1, 1000)
            ok, cert = find_witness(v, d)
            self.assertFalse(ok)
            self.assertTrue(check_no_witness_certificate(v, cert, d))

    def test_known_tight_1347(self):
        # Goddyn-Wong tight example for 4 speeds
        self.assertEqual(max_loneliness([1, 3, 4, 7])[0], Fraction(1, 5))

    def test_ml_attained_and_dominates_grid(self):
        rng = random.Random(1)
        for _ in range(150):
            n = rng.randint(1, 5)
            v = rng.sample(range(1, 25), n)
            ml, t = max_loneliness(v)
            self.assertEqual(min(norm_frac(x * t) for x in v), ml)
            self.assertGreaterEqual(ml, ml_grid(v, 600))
            # grid containing t* attains ML; all such t* have denominators
            # v_i + v_j, so grid lcm-free check: denominators divide some s
            self.assertEqual(ml_grid(v, t.denominator), ml)

    def test_decision_matches_ml(self):
        rng = random.Random(2)
        for _ in range(300):
            n = rng.randint(1, 5)
            v = rng.sample(range(1, 30), n)
            ml, _ = max_loneliness(v)
            for d in (ml, ml + Fraction(1, 10 ** 6), ml - Fraction(1, 10 ** 6),
                      Fraction(1, n + 1), Fraction(rng.randint(1, 49), 100)):
                if d <= 0:
                    continue
                ok, res = find_witness(v, d)
                self.assertEqual(ok, ml >= d, (v, d, ml))
                if ok:
                    self.assertTrue(check_witness(v, res, d))
                elif isinstance(res, list):
                    self.assertTrue(check_no_witness_certificate(v, res, d))

    def test_certificate_rejects_tampering(self):
        v = [1, 2, 3]
        d = Fraction(1, 3)
        ok, cert = find_witness(v, d)
        self.assertFalse(ok)
        self.assertTrue(check_no_witness_certificate(v, cert, d))
        self.assertFalse(check_no_witness_certificate(v, cert[:-1], d))
        i, m, j = cert[0]
        # claim a failure at an index where the candidate actually passes
        good = [jj for jj in range(3)
                if norm_frac(v[jj] * (m + d) / v[i]) >= d]
        if good:
            bad_cert = [(i, m, good[0])] + cert[1:]
            self.assertFalse(check_no_witness_certificate(v, bad_cert, d))

    def test_lrc_small_bounded(self):
        # computed up to a small N (fast unit-test version of exhaustive.py)
        for n, N in ((2, 25), (3, 18), (4, 12)):
            for v in combinations_with_replacement(range(1, N + 1), n):
                if len(set(v)) == n:
                    self.assertTrue(find_witness(v)[0], v)


def brute_improper(k, p, l):
    """I(k,p,l) by direct definition over all of Z_{p,l}^k (no symmetry,
    no bitsets): returns the set of canonical representatives."""
    N = l * p
    L = Level(k, p, l)
    elems = [x for x in range(N) if x % p]
    out = set()
    for w in product(elems, repeat=k):
        if l > 1 and any(
                gcd(l, *[w[j] for j in range(k) if j != i]) > 1 for i in range(k)):
            continue
        wit = False
        for m in range(N):
            if all((k + 1) * min((x * m) % N, N - (x * m) % N) >= N for x in w):
                wit = True
                break
        if not wit:
            out.add(L.canon(w))
    return out


class TestSieve(unittest.TestCase):
    def test_level1_matches_bruteforce(self):
        for k, p in ((2, 5), (3, 7), (3, 11), (3, 13), (4, 11), (4, 13), (5, 7)):
            S, _ = level1_improper(k, p)
            self.assertEqual(set(S), brute_improper(k, p, 1), (k, p))

    def test_lift_matches_bruteforce(self):
        for k, p, c in ((3, 7, 2), (3, 11, 2), (3, 5, 4), (4, 7, 2), (4, 11, 5), (2, 7, 3)):
            S, _ = level1_improper(k, p)
            S2, _ = lift(S, k, p, 1, c)
            self.assertEqual(set(S2), brute_improper(k, p, c), (k, p, c))

    def test_two_step_lift_matches_bruteforce(self):
        for k, p in ((3, 7), (3, 13)):
            S, _ = level1_improper(k, p)
            S, _ = lift(S, k, p, 1, 2)
            S, _ = lift(S, k, p, 2, 2)
            self.assertEqual(set(S), brute_improper(k, p, 4))
            self.assertEqual(S, [])  # J(3,p) empty at these primes

    def test_tight_tuple_survives_until_k_plus_1(self):
        # Remark 3.2 of arXiv:2604.23906: (1..k) is improper at level l
        # unless (k+1) | l (for p > k+1).
        for k, p in ((3, 11), (4, 13), (6, 17)):
            for l in range(1, 2 * (k + 1) + 1):
                L = Level(k, p, l)
                w = list(range(1, k + 1))
                self.assertEqual(L.is_proper(w), l % (k + 1) == 0 or L.gcd_condition(w), (k, p, l))

    def test_witness_transfers_to_integers(self):
        # Rosenfeld's observation: a witness m/N for w transfers to every
        # integer tuple u = w mod N.
        rng = random.Random(3)
        for _ in range(300):
            k, p, l = rng.randint(2, 5), rng.choice([7, 11, 13]), rng.randint(1, 4)
            N = l * p
            L = Level(k, p, l)
            w = [rng.choice([x for x in range(N) if x % p]) for _ in range(k)]
            for m in range(N):
                if all((k + 1) * min((x * m) % N, N - (x * m) % N) >= N for x in w):
                    u = [x + N * rng.randint(0, 50) for x in w]
                    self.assertTrue(check_witness(u, Fraction(m, N), Fraction(1, k + 1)))
                    break

    def test_c_engine_matches_python(self):
        for k, p in ((3, 13), (4, 23), (5, 41), (6, 43), (7, 31)):
            self.assertEqual(sieve.level1_improper_c(k, p), level1_improper(k, p))

    def test_B_bound(self):
        self.assertEqual(comb(4, 2), 6)
        # B_3 = (6^2/3)^3 = 1728
        self.assertFalse(B_bound_ok(3, [1727]))
        self.assertTrue(B_bound_ok(3, [1728]))
        for k in range(3, 16):
            self.assertAlmostEqual(log_B(k), k * ((k - 1) * log(comb(k + 1, 2)) - log(k)))
        # value quoted for k=13 in arXiv:2609.02604's abstract: log B_13 < 670.3498
        self.assertTrue(670.34 < log_B(13) < 670.3498)

    def test_small_cases_end_to_end(self):
        for k, chain in ((3, [2, 2]), (4, [2, 2, "p", 5])):
            used = []
            p = k + 2
            while not B_bound_ok(k, used):
                if all(p % q for q in range(2, p)):
                    ok, _, _ = run_gate(k, p, chain)
                    if ok:
                        used.append(p)
                p += 1
            self.assertTrue(B_bound_ok(k, used))


class TestCoverGenAndLiftFree(unittest.TestCase):
    def test_covergen_matches_naive(self):
        for k, p in ((3, 13), (4, 23), (5, 37), (6, 43), (7, 61), (8, 47)):
            self.assertEqual(sieve.level1_improper_covers(k, p)[0],
                             sieve.level1_improper_c(k, p)[0], (k, p))

    def test_liftfree_matches_python_lift(self):
        import check_allikvere as ca
        for k, p, c in ((4, 13, 5), (5, 23, 2), (5, 23, 3), (6, 19, 2)):
            S, _ = level1_improper(k, p)
            ours, _ = lift(S, k, p, 1, c)
            wf = ca.witness_free_lifts(k, p, c, S)
            Lc = Level(k, p, c)
            theirs = sorted({Lc.canon(w) for ws in wf.values() for w in ws
                             if not ca.gcd_clause(w, c)})
            self.assertEqual(ours, theirs, (k, p, c))

    def test_flag_constants_match_paper(self):
        from flag_bound import flag_constants, log_bound
        K14, r14 = flag_constants(14)
        self.assertEqual(K14, Fraction(2289670297, 97243124257250844122250000000000000000))
        self.assertEqual(r14, Fraction(847, 513))
        self.assertEqual(flag_constants(13)[1], Fraction(1175, 688))
        self.assertAlmostEqual(log_bound(14, 0.5), 414.7793645567, places=6)
        self.assertTrue(flag_constants(15)[1] > Fraction(4, 3))


if __name__ == "__main__":
    unittest.main()
