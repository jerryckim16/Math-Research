"""Direct bounded check: every n-tuple of distinct positive integers
1 <= v_1 < ... < v_n <= N with gcd 1 has a time t with all
||v_i t|| >= 1/(n+1) (exact search, lonely.find_witness).  Also lists the
tuples with ML(v) = 1/(n+1) exactly ("tight").

This is evidence of the type "computed up to N", not a proof.
Usage: python3 exhaustive.py n N
"""
import sys
import time
from fractions import Fraction
from itertools import combinations
from math import gcd
from functools import reduce

from lonely import find_witness


def main():
    n, N = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    checked, tight, bad = 0, [], []
    for v in combinations(range(1, N + 1), n):
        if reduce(gcd, v) != 1:
            continue
        checked += 1
        ok, t = find_witness(v)
        if not ok:
            bad.append(v)
            continue
        # tight iff no witness for any delta > 1/(n+1); by the left-endpoint
        # argument it suffices to test whether the interior of the good set
        # is empty, which we detect with a slightly larger rational delta
        # below every gap: ML(v) is of the form a/(v_i+v_j), so
        # ML > 1/(n+1) implies ML >= 1/(n+1) + 1/((n+1)*2*N).
        ok2, _ = find_witness(v, Fraction(1, n + 1) + Fraction(1, (n + 1) * 2 * N))
        if not ok2:
            tight.append(v)
    print(f"n={n} N={N} primitive tuples checked={checked} "
          f"counterexamples={len(bad)} tight={tight} seconds={time.time()-t0:.1f}")
    if bad:
        print("COUNTEREXAMPLES", bad)
        sys.exit(1)


if __name__ == "__main__":
    main()
