"""Tests for the LRC(15) certificate checker (check_gate15.py).

1. rowcheck15.c (covering formulation) equals a brute force from Def. 2.1 at
   level 1 (sieve.Level(15, p, 1).has_witness, every t = m/p) on random
   15- and 14-class rows at several primes, including the irredundancy test
   (each class removable or not, by brute force).
2. gatecheck.c cascade with k = 15 equals a brute force over all 2^15 lifts
   (sieve.Level(15, p, l).is_proper, i.e. Def. 2.1 with the gcd clause) for
   levels 2 and 4, on random level-one improper rows and on (1..15).
3. (1..15) has improper fibres 1, 2, 4, 0 at levels 2, 4, 8, 16 for p = 269,
   367, 509, 659 (as in results/tight_orbit_k15.jsonl, from liftfree.c).
Run: python3 -m unittest -v test_check_gate15   (from this directory)
"""
import itertools
import os
import random
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import check_gate15 as cg  # noqa: E402
from sieve import Level  # noqa: E402

K = 15


def hexrow(r):
    return "".join("%02x" % x for x in r)


def brute_lifts(row, p, l_from, l_to, L):
    """improper lifts at level l_to of the level-l_from vector row (mod l_from p)."""
    M = l_from * p
    c = l_to // l_from
    out = []
    for js in itertools.product(range(c), repeat=len(row)):
        w = tuple(x + j * M for x, j in zip(row, js))
        if not L.is_proper(w):
            out.append(w)
    return out


class RowCheck(unittest.TestCase):
    def test_rowcheck_matches_bruteforce(self):
        rng = random.Random(1)
        for p in (67, 101, 131, 269):
            h = (p - 1) // 2
            L1 = Level(K, p, 1)
            for n in (K, K - 1):
                rows = []
                for _ in range(150):
                    r = rng.sample(range(2, h + 1), n - 1) + [1]
                    rng.shuffle(r)
                    rows.append(tuple(r))
                st, bad = cg.rowcheck(p, n, [hexrow(r) for r in rows])
                nc = sum(1 for r in rows if L1.has_witness(r))
                # irredundant: removing any class gives a witness (for covers)
                red = 0
                for r in rows:
                    if L1.has_witness(r):
                        continue
                    if any(not L1.has_witness(r[:i] + r[i + 1:]) for i in range(n)):
                        red += 1
                self.assertEqual(st["rows"], len(rows))
                self.assertEqual(st["not_cover"], nc, (p, n))
                self.assertEqual(st["gatecheck_with_witness"], nc, (p, n))
                self.assertEqual(st["redundant"], red, (p, n))
                self.assertEqual(st["not_distinct"] + st["no_class1"] + st["out_of_range"], 0)

    def test_rowcheck_flags_format(self):
        st, bad = cg.rowcheck(67, K, [hexrow((1, 1) + tuple(range(3, 16))), hexrow((2,) + tuple(range(3, 17))),
                                      hexrow((1,) + tuple(range(3, 16)) + (40,))])
        self.assertEqual(st["not_distinct"], 1)
        self.assertEqual(st["no_class1"], 1)
        self.assertEqual(st["out_of_range"], 1)


class Cascade(unittest.TestCase):
    def cascade(self, p, rows):
        out = cg.run([cg.binary("gatecheck"), "cascade", str(K), str(p)],
                     "\n".join(" ".join(map(str, r)) for r in rows) + "\n")
        return [tuple(map(int, l.split()[1:])) for l in out.splitlines()]

    def test_cascade_matches_bruteforce_levels_2_4(self):
        rng = random.Random(2)
        for p in (37, 41, 67):
            h = (p - 1) // 2
            L1, L2, L4 = Level(K, p, 1), Level(K, p, 2), Level(K, p, 4)
            rows = [tuple(range(1, K + 1))]
            while len(rows) < 4:
                r = tuple(sorted(rng.choice(range(1, h + 1)) for _ in range(K)))
                if not L1.has_witness(r):
                    rows.append(r)
            ours = self.cascade(p, rows)
            for r, c in zip(rows, ours):
                s2 = brute_lifts(r, p, 1, 2, L2)
                self.assertEqual(c[0], len(s2), (p, r))
                n4 = sum(len(brute_lifts(w, p, 2, 4, L4)) for w in s2)
                self.assertEqual(c[1], n4, (p, r))

    def test_tight_trace(self):
        for p in (269, 367, 509, 659):
            (c,) = self.cascade(p, [tuple(range(1, K + 1))])
            self.assertEqual(c, (1, 2, 4, 0, 0), p)


if __name__ == "__main__":
    unittest.main()
