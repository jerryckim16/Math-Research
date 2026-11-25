"""Tests for shape_lemma.py.  Run: python3 -m unittest test_shape_lemma -v"""
import random
import unittest
from fractions import Fraction as Fr

import shape_lemma as S
from shape_lemma import P, X


def H_float(u, n):
    q = [1 + 2 * x - x * x for x in u]
    sw = sum(x * x / qq for x, qq in zip(u, q))
    pa = 1.0
    for x, qq in zip(u, q):
        pa *= qq / x ** (2 / n)
    return sw * pa


class TestPaperRegression(unittest.TestCase):
    """The machinery must reproduce what the paper states for n = 13, 14."""

    def test_interior_polynomials(self):
        self.assertEqual(S.L_poly(13), P([1, -3, -9, -23, 12, 6]))
        self.assertEqual(2 * S.L_poly(14), P([2, -7, -20, -50, 26, 13]))

    def test_cubics(self):
        self.assertEqual(S.H1_cubic(13)[0], P([-1, 8, 21, 276]))
        self.assertEqual(S.H1_cubic(14)[0], P([-1, 9, 23, 325]))

    def test_intervals(self):
        lo, hi, _ = S.t0_interval(14)
        self.assertTrue(Fr(782, 10000) <= lo and hi <= Fr(783, 10000))
        lo, hi, _ = S.t0_interval(13)
        self.assertTrue(Fr(849, 10000) <= lo and hi <= Fr(850, 10000))
        self.assertTrue(S.alpha_interval(13)[1] < Fr(103, 1000))
        lo, hi, _ = S.alpha_interval(14)
        self.assertTrue(Fr(926, 10000) <= lo and hi <= Fr(927, 10000))

    def test_paper_lemmas_reproved(self):
        for n in (13, 14):
            self.assertTrue(all(S.prove(n).values()), n)


class TestN15(unittest.TestCase):
    def test_all_checks(self):
        res = S.prove(15)
        self.assertTrue(all(res.values()), res)

    def test_exact_objects(self):
        self.assertEqual(S.L_poly(15), P([1, -4, -11, -27, 14, 7]))
        self.assertEqual(S.H1_cubic(15)[0], P([-1, 10, 25, 378]))
        self.assertEqual(S.H1_parts(15), P([1, 2, 27]))
        self.assertEqual(S.target(15), Fr(1500, 49) ** 2)
        lo, hi, ok = S.t0_interval(15)
        self.assertTrue(ok and Fr(7247, 100000) <= lo and hi <= Fr(7248, 100000))

    def test_negative_controls(self):
        # the one-coordinate minimum is about 944.96, so a target above it
        # must fail, and the coarse two-or-more bound must not be what decides
        self.assertFalse(S.check_one(15, T=Fr(946))[0])
        self.assertTrue(S.check_one(15, T=Fr(944))[0])
        self.assertFalse(S.check_two_or_more(15, T=Fr(1802))[0])
        # r_15 = 0.487 (T = (15/0.487)^2 ~ 948.7) is not provable this way
        self.assertFalse(S.check_one(15, T=(Fr(15) / Fr(487, 1000)) ** 2)[0])

    def test_numeric_minimum_sanity(self):
        """Float search (not part of the proof): random points and coordinate
        descent never go below the target, and the best value found is the
        one-variable family's ~944.96."""
        n, T = 15, float(S.target(15))
        rng = random.Random(5)
        best = 1e18
        for _ in range(40):
            u = [rng.uniform(0.01, 1) for _ in range(n)]
            u[rng.randrange(n)] = 1.0
            for _ in range(15):
                for i in range(n):
                    if u[i] == 1.0 and u.count(1.0) == 1:
                        continue
                    lo, hi = 1e-4, 1.0
                    for _ in range(40):  # ternary search, phi is unimodal in u_i
                        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
                        a = H_float(u[:i] + [m1] + u[i + 1:], n)
                        b = H_float(u[:i] + [m2] + u[i + 1:], n)
                        lo, hi = (lo, m2) if a < b else (m1, hi)
                    u[i] = (lo + hi) / 2
            h = H_float(u, n)
            self.assertGreater(h, T)
            best = min(best, h)
        self.assertAlmostEqual(best, 944.96, delta=0.05)

    def test_consequence(self):
        from flag_bound import flag_constants, log_bound, lcm_upto
        from math import log
        self.assertTrue(flag_constants(15)[1] > Fr(4, 3))
        lb = log_bound(15, 0.49)
        self.assertAlmostEqual(lb, 496.727, delta=0.001)
        self.assertAlmostEqual(lb - log(lcm_upto(16)), 483.239, delta=0.001)


class TestSympyCrossCheck(unittest.TestCase):
    """Optional: the identities with the real exponent u^(2/n)."""

    def test_identities(self):
        try:
            import sympy as sp
        except ImportError:
            self.skipTest("sympy not installed")
        u, C, t = sp.symbols("u C t", positive=True)
        for n in (13, 14, 15):
            N = sp.Integer(n)
            q = 1 + 2 * u - u ** 2
            phi = q / u ** (2 / N) * (C + u ** 2 / q)
            beta = C * ((N - 1) * u ** 2 - (N - 2) * u + 1) - (N - 1) * u ** 2
            self.assertEqual(sp.simplify(N / 2 * u ** (1 + 2 / N) * sp.diff(phi, u) + beta), 0)
            qt = q.subs(u, t)
            H1 = (sp.Rational(1, 2) + (N - 1) * t ** 2 / qt) * 2 * (qt / t ** (2 / N)) ** (N - 1)
            E = 1 + 2 * t + (2 * N - 3) * t ** 2
            self.assertEqual(sp.simplify(H1 - E * qt ** (N - 2) / t ** (2 * (N - 1) / N)), 0)
            K = sum(c * t ** i for i, c in enumerate(S.H1_cubic(n)[0].c))
            dlog = sp.diff(sp.log(E * qt ** (N - 2) / t ** (2 * (N - 1) / N)), t)
            self.assertEqual(sp.simplify(dlog - 2 * (N - 1) * (1 - t) * K / (N * t * E * qt)), 0)


if __name__ == "__main__":
    unittest.main()
