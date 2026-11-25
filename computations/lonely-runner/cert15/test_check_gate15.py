"""Tests for the LRC(15) certificate checker (check_gate15.py).

1. rowcheck15.c (covering formulation) equals a brute force from Def. 2.1 at
   level 1 (sieve.Level(15, p, 1).has_witness, every t = m/p) on random
   15- and 14-class rows at several primes, including the irredundancy test
   (each class removable or not, by brute force).
2. gatecheck.c cascade with k = 15 equals a brute force over all 2^15 lifts
   of every fibre member (sieve.Level(15, p, l): Def. 2.1, witness on the
   level-l grid or the gcd clause) for (1..15) at p = 269 (levels 2, 4, 8)
   and four stored rows at p = 367 (levels 2, 4).
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


def hex_tuple(s):
    return tuple(int(s[i:i + 2], 16) for i in range(0, len(s), 2))


def brute_lifts(row, p, l_from, l_to, L):
    """improper lifts at level l_to of the level-l_from vector row (mod l_from p)."""
    M = l_from * p
    c = l_to // l_from
    out = []
    for js in itertools.product(range(c), repeat=len(row)):
        w = tuple(x + j * M for x, j in zip(row, js))
        if not L.has_witness(w) and not L.gcd_condition(w):
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

    def test_cascade_matches_bruteforce(self):
        # Inputs: (1..15) at p = 269 (levels 2, 4, 8 by brute force) and four
        # stored rows of the p = 367 archive, two with an improper level-2 lift
        # and two without (levels 2, 4).  The archive rows serve only as test
        # inputs: the comparison is gatecheck.c against brute force.
        cases = [(269, tuple(range(1, K + 1)), 3),
                 (367, (1, 9, 13, 15, 22, 29, 68, 83, 84, 133, 139, 144, 159, 160, 162), 2),
                 (367, (1, 4, 5, 11, 13, 14, 57, 81, 83, 86, 96, 153, 157, 179, 43), 2),
                 (367, hex_tuple("01030a2127383a565f60617e8a9bb3"), 2),
                 (367, hex_tuple("0102142737383a4d5f60617e868a9b"), 2)]
        for p, r, depth in cases:
            self.assertFalse(Level(K, p, 1).has_witness(r))
            (c,) = self.cascade(p, [r])
            S = [r]
            for e in range(1, depth + 1):
                L = Level(K, p, 1 << e)
                S = [w for v in S for w in brute_lifts(v, p, 1 << (e - 1), 1 << e, L)]
                self.assertEqual(c[e - 1], len(S), (p, r, 1 << e))

    def test_tight_trace(self):
        for p in (269, 367, 509, 659):
            (c,) = self.cascade(p, [tuple(range(1, K + 1))])
            self.assertEqual(c, (1, 2, 4, 0, 0), p)


if __name__ == "__main__":
    unittest.main()
