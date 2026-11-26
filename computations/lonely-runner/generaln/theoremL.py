"""Table for Theorem L of notes/lonely-runner/general-n-explicit.md.

For each block of n, [na, nb] with nb = 2*na - 1 (na = 2^i), put
N = 2*nb + 2 and find the least m such that Lemma H's hypothesis holds for
both (m, N) and (m+1, N) (exact check, explicit_core.check_H).  Lemma H is
monotone in N (smaller N is easier), so (m, N) covers every n in the block.
Theorem L then gives, for every n in the block with n >= 2 m^2 + 2:
    every set of n positive integers with v_n <= 2n - (4m + 4) is lonely.

Output: one line per block
    i na nb m F=4m+4 sqrt_ok(n>=2m^2+2 for n=na) j gstar
and a final line naming the first block where no m was found below the
search cap (the explicit argument stops there; see the note, section 6).

Usage: python3 theoremL.py IMIN IMAX
"""
import sys
from math import isqrt

from explicit_core import check_H, per_element


def both(m, N):
    return check_H(m, N)[0] and check_H(m + 1, N)[0]


def least_m(N, cap):
    hi = 4
    while not both(hi, N):
        hi *= 2
        if hi > cap:
            return None
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if both(mid, N):
            hi = mid
        else:
            lo = mid
    assert both(hi, N)
    return hi


def main():
    imin, imax = int(sys.argv[1]), int(sys.argv[2])
    for i in range(imin, imax + 1):
        na, nb = 2 ** i, 2 ** (i + 1) - 1
        N = 2 * nb + 2
        m = least_m(N, cap=N)
        if m is None:
            print("STOP i=%d na=%d: no m <= N satisfies Lemma H" % (i, na))
            return
        j, g, _ = per_element(m, N)
        print(i, na, nb, m, 4 * m + 4, int(na >= 2 * m * m + 2), j, "%.4f" % float(g), flush=True)


if __name__ == "__main__":
    main()
