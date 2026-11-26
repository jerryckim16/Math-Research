"""Second, independent check of the dense window DW(m) for small m.

Pure Python; shares no code with dwsolve.c.  For every m-subset V of
[1, 2m] it looks for a witness at threshold 1/(m+1): first among a fixed list
of rational times (every witness found is re-verified with
lonely.check_witness), then, if none of those works, with the complete
left-endpoint search lonely.find_witness.  Sets of size < m need no check
(they are subsets of m-sets, and removing speeds keeps a witness).
Usage: python3 dw_bruteforce.py MMAX
"""
import os
import sys
from fractions import Fraction
from itertools import combinations
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lonely import find_witness, check_witness  # noqa: E402


def check_m(m):
    K = m + 1
    times = [(a, q) for q in range(2, 4 * m + 1) for a in range(1, q // 2 + 1) if gcd(a, q) == 1]
    good = []  # good[i] = bitmask over speeds x in [1,2m] that are fine at times[i]
    for a, q in times:
        mask = 0
        for x in range(1, 2 * m + 1):
            r = x * a % q
            if K * min(r, q - r) >= q:
                mask |= 1 << x
        good.append(mask)
    n_sets = n_full = 0
    for V in combinations(range(1, 2 * m + 1), m):
        n_sets += 1
        vm = 0
        for x in V:
            vm |= 1 << x
        for i, g in enumerate(good):
            if g & vm == vm:
                t = Fraction(*times[i])
                assert check_witness(V, t, Fraction(1, K))
                break
        else:
            n_full += 1
            ok, t = find_witness(V, Fraction(1, K))
            if not ok:
                return n_sets, n_full, V
            assert check_witness(V, t, Fraction(1, K))
    return n_sets, n_full, None


if __name__ == "__main__":
    for m in range(1, int(sys.argv[1]) + 1):
        print(m, *check_m(m), flush=True)
