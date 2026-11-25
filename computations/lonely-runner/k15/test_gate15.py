"""Tests for gate15.c and tau.c (k15 pilot tools).

1. gate15 per-row cascade counts n_l (l = 2, 4, 8) equal a brute force from
   Def. 2.1 (all 2^k lifts of every member, sieve.Level.is_proper), for k = 7
   (k + 1 = 8 a power of two) at several small primes, on every level-one
   orbit (sieve.level1_improper).
2. gate15's shift-kill flags equal an independent Python transcription of
   Lemma S, and Lemma S is SOUND on samples: for shift-killed improper w,
   random integer tuples u == w (mod N) are lonely (lonely.find_witness).
3. tau.c with cuts equals tau.c without cuts and a brute-force minimum cover
   size at small (k, p).
Run: python3 -m unittest -v test_gate15  (from this directory)
"""
import itertools
import os
import random
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sieve  # noqa: E402
import lonely  # noqa: E402

_B = {}


def build(name):
    if name not in _B:
        out = os.path.join(tempfile.mkdtemp(prefix="k15_"), name)
        subprocess.run(["cc", "-O2", "-o", out, os.path.join(HERE, name + ".c")], check=True)
        _B[name] = out
    return _B[name]


def gate15(k, p, lmax, rows, dump=False):
    env = dict(os.environ)
    if dump:
        env["G15_DUMP"] = "1"
    r = subprocess.run([build("gate15"), str(k), str(p), str(lmax)], input="".join(" ".join(map(str, v)) + "\n" for v in rows),
                       capture_output=True, text=True, check=True, env=env)
    out = []
    for line in r.stdout.splitlines():
        if line.startswith("SURV") or line.startswith("BADROW"):
            continue
        out.append(list(map(int, line.split())))
    return out


def shift_killed_py(w, l, k):
    d = 4
    while d <= l:
        if l % d == 0:
            s = 0
            for x in w:
                if x % d:
                    g = gcd(x, d)
                    s += g * (-(-2 * d // ((k + 1) * g)))
            if s < d:
                return True
        d *= 2
    return False


def brute_cascade(k, p, v, lmax):
    S = [tuple(v)]
    counts, fails = [], []
    l = 1
    while l < lmax:
        hi = sieve.Level(k, p, 2 * l)
        N = l * p
        T = []
        for w in S:
            for js in itertools.product((0, 1), repeat=k):
                u = tuple(x + j * N for x, j in zip(w, js))
                if not hi.is_proper(u):
                    T.append(u)
        l *= 2
        S = T
        counts.append(len(S))
        fails.append(sum(1 for u in S if not shift_killed_py(u, l, k)) if l >= 4 else None)
    return counts, fails, S


class TestGate15(unittest.TestCase):
    def test_cascade_matches_bruteforce_k7(self):
        k = 7
        for p in (17, 19, 23, 29, 31):
            orbits, _ = sieve.level1_improper(k, p)
            res = gate15(k, p, 8, orbits)
            self.assertEqual(len(res), len(orbits))
            for v, r in zip(orbits, res):
                counts, fails, _ = brute_cascade(k, p, v, 8)
                self.assertEqual(r[1:4], counts, (p, v))
                self.assertEqual([r[6], r[7]], fails[1:3], (p, v))

    def test_shift_lemma_sound_on_samples(self):
        k = 7
        rng = random.Random(1)
        tested = 0
        for p in (17, 19, 23):
            orbits, _ = sieve.level1_improper(k, p)
            for v in orbits:
                _, _, S = brute_cascade(k, p, v, 8)
                for w in S:
                    if shift_killed_py(w, 8, k):
                        for _ in range(3):
                            u = [x + 8 * p * rng.randrange(0, 4) for x in w]
                            ok, _ = lonely.find_witness(u, Fraction(1, k + 1))
                            self.assertTrue(ok, (p, w, u))
                            tested += 1
        self.assertGreater(tested, 0)

    def test_tau(self):
        for k, p in ((5, 29), (5, 31), (6, 37), (7, 41), (7, 43)):
            h = (p - 1) // 2
            cov = {v: {a for a in range(1, h + 1) if (k + 1) * min(a * v % p, p - a * v % p) < p} for v in range(1, h + 1)}
            best = None
            for s in range(1, h + 1):
                for C in itertools.combinations(range(1, h + 1), s):
                    if set().union(*(cov[c] for c in C)) == set(range(1, h + 1)):
                        best = s
                        break
                if best:
                    break
            for cuts in ("0", "1"):
                out = subprocess.run([build("tau"), str(k), str(p), str(h)], capture_output=True, text=True, check=True,
                                     env=dict(os.environ, TAU_CUTS=cuts)).stdout.split()
                self.assertEqual(int(out[out.index("tau") + 1]), best, (k, p, cuts))


if __name__ == "__main__":
    unittest.main()
