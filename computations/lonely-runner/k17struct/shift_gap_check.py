"""Third, exact-rational check of len(y,r) (shift_gap_exact.c / shift_gap_sort.c).

For y in Z_c^k (any y, no normalisation) and r != 0, G(y,r) = {t in R/Z : ||i t + y_i r/c|| >= 1/(k+1)}.
Computes the longest closed arc of G(y,r) with Python Fractions: all open bad arcs are cut at 0
into pieces inside [0,1), merged, and the circular complement is measured.
Also tests the two proved reductions on every sampled y:
  len(y + j(1..k), r) = len(y, r)   and   len(y, c-r) = len(-y, r)... (= len(y,r) via t -> -t).
Usage: python3 shift_gap_check.py k c nsample seed [sgs_binary]
With sgs_binary, the sampled y (normalised to y_1 = 0) and the given argmins are piped to
`sgs k c eval` and the integer lengths (units 1/D) are compared exactly.
"""
import random
import subprocess
import sys
from fractions import Fraction as F
from math import lcm


def length(k, c, y, r):
    pieces = []
    zero_covered = False
    for i in range(1, k + 1):
        s = F(y[i - 1] * r % c, c)
        for n in range(i):
            lo = ((n - s) - F(1, k + 1)) / i
            hi = ((n - s) + F(1, k + 1)) / i
            lo, hi = lo - (lo // 1), hi - (lo // 1)
            if hi <= 1:
                pieces.append((lo, hi))
            else:
                pieces.append((lo, F(1)))
                pieces.append((F(0), hi - 1))
                zero_covered = True
    pieces.sort()
    # merge open arcs; an open arc ending at x and one starting at x leave the point x good
    merged = []
    for lo, hi in pieces:
        if merged and lo < merged[-1][1]:
            if hi > merged[-1][1]:
                merged[-1][1] = hi
        else:
            merged.append([lo, hi])
    if not merged:
        return F(1)
    best = None
    for a in range(len(merged)):
        end = merged[a][1]
        nxt = merged[a + 1][0] if a + 1 < len(merged) else merged[0][0] + 1
        gap = nxt - end
        if a + 1 == len(merged) and zero_covered:
            continue  # the seam at 0 lies inside an open arc: not a good point
        if gap >= 0 and (best is None or gap > best):
            best = gap
    return best if best is not None else F(-1)


def main():
    k, c, ns, seed = map(int, sys.argv[1:5])
    sgs = sys.argv[5] if len(sys.argv) > 5 else None
    D = c * (k + 1) * lcm(*range(1, k + 1))
    rng = random.Random(seed)
    ys = []
    for _ in range(ns):
        y = [0] + [rng.randrange(c) for _ in range(k - 1)]
        if any(y):
            ys.append(y)
    extra = [line.split() for line in sys.stdin.read().splitlines() if line.strip()]
    ys += [list(map(int, e)) for e in extra]
    vals = []
    for y in ys:
        row = []
        for r in range(1, c):
            v = length(k, c, y, r)
            # reductions
            for j in range(1, c):
                yj = [(y[i] + j * (i + 1)) % c for i in range(k)]
                assert length(k, c, yj, r) == v, ("translation", y, j, r)
            ym = [(-x) % c for x in y]
            assert length(k, c, ym, (c - r) % c) == v, ("reflection", y, r)
            row.append(v)
        vals.append(row)
    print(f"k={k} c={c}: {len(ys)} vectors, translation and reflection identities hold")
    mn = min(max(r) for r in vals)
    print(f"min over these of max_r len = {mn} = 1/{1/mn if mn > 0 else 'inf'}")
    if sgs:
        inp = "".join(" ".join(map(str, y)) + "\n" for y in ys)
        out = subprocess.run([sgs, str(k), str(c), "eval"], input=inp, capture_output=True, text=True, check=True).stdout
        bad = 0
        for y, row, line in zip(ys, vals, out.splitlines()):
            got = list(map(int, line.split()))
            want = [int(v * D) if v >= 0 else -1 for v in row]
            assert all((v * D).denominator == 1 for v in row if v >= 0)
            if got != want:
                bad += 1
                print("MISMATCH", y, got, want)
        print(f"compared with {sgs} eval: {len(ys)} vectors, {bad} mismatches")


if __name__ == "__main__":
    main()
