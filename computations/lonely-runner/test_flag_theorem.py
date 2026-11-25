"""Tests for flag_theorem_check.py.  Run: python3 -m unittest test_flag_theorem -v"""
import random
import unittest
from fractions import Fraction as Fr
from unittest import mock

import flag_theorem_check as T


class TestInclusion(unittest.TestCase):
    def test_identity(self):
        self.assertTrue(T.check_inclusion_identity())

    def test_vertices_and_samples(self):
        rng = random.Random(11)
        for n in (3, 4, 5, 6, 7):
            for _ in range(4):
                v = T.random_primitive(n, rng)
                self.assertTrue(T.check_inclusion_vertices(v), v)
                self.assertTrue(T.check_inclusion_samples(v), v)

    def test_negative_control(self):
        # a fatter 'ellipsoid' (q = 1 + 2u, i.e. without the -u^2) must leave D
        v = [3, 5, 8]
        real = T.setting
        def fat(v):
            S, x, u, q = real(v)
            return S, x, u, [1 + 2 * a for a in u]
        with mock.patch.object(T, "setting", fat):
            self.assertFalse(T.check_inclusion_vertices(v))


class TestCovolume(unittest.TestCase):
    def test_random(self):
        rng = random.Random(12)
        for n in (3, 4, 5, 6):
            for _ in range(5):
                v = T.random_primitive(n, rng)
                self.assertTrue(T.check_covolume(v), v)

    def test_lattice_is_PZn(self):
        # the basis spans P e_k for every k (so it spans P Z^n, not a sublattice)
        v = [2, 3, 7, 11]
        B = T.lattice_basis(v)
        N = sum(a * a for a in v)
        for k in range(4):
            pe = [Fr(int(i == k)) - Fr(v[i] * v[k], N) for i in range(4)]
            # solve pe = sum c_j B_j over the rationals; coefficients must be integers
            cols = list(zip(*B))
            idx = None
            for rows in __import__("itertools").combinations(range(4), 3):
                A = [[B[j][i] for j in range(3)] for i in rows]
                if T.det(A) != 0:
                    idx = rows
                    break
            A = [[B[j][i] for j in range(3)] for i in idx]
            c = T.solve(A, [pe[i] for i in idx])
            self.assertTrue(all(x.denominator == 1 for x in c))

    def test_negative_control(self):
        v = [3, 5, 8]
        with mock.patch.object(T, "F2", lambda v: Fr(1)):
            self.assertFalse(T.check_covolume(v))


class TestMinimization(unittest.TestCase):
    def test_vertex_bruteforce(self):
        for n in range(3, 9):
            ok, nv = T.check_vertices_bruteforce(n)
            self.assertTrue(ok, n)
            self.assertEqual(nv, 2 ** (n - 2))  # one vertex per composition of d

    def test_block_points_n13_15(self):
        for n in (13, 14, 15):
            self.assertTrue(T.check_block_points(n)[0], n)

    def test_random_feasible(self):
        for n in (13, 14, 15):
            self.assertTrue(T.check_random_feasible(n, trials=500), n)

    def test_minimum_value(self):
        # K_14 from the paper, and t = c attains it
        self.assertEqual(T.prodc(14), Fr(2289670297, 97243124257250844122250000000000000000))
        t, _ = T.block_point(15, list(range(1, 15)))
        self.assertEqual(T.prod(t), T.prodc(15))

    def test_negative_control(self):
        # if c_{i+1}/c_i < 1/rho the lemma fails: some block point beats prod c
        fake = lambda n: [Fr(0)] + [Fr(r) + Fr(r * r, 100) for r in range(1, n)]
        with mock.patch.object(T, "prefix_B", fake):
            t, _ = T.block_point(6, [5])  # one geometric block
            self.assertTrue(T.feasible_t(6, t))
            self.assertLess(T.prod(t), T.prodc(6))


class TestAssembly(unittest.TestCase):
    def test_n15(self):
        lb = T.log_bound_decimal(15, Fr(49, 100))
        self.assertAlmostEqual(float(lb), 496.7267719607, places=9)
        self.assertAlmostEqual(float(lb - T.ln_lcm(16)), 483.2387659694, places=9)

    def test_n14_paper(self):
        self.assertAlmostEqual(float(T.log_bound_decimal(14, Fr(1, 2))), 414.77936455669981, places=10)


if __name__ == "__main__":
    unittest.main()
