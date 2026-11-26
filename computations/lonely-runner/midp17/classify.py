"""Classify retained tuples at a level L (heuristic statistics, exact tests).

A retained tuple w (mod Lp) is of LEMMA T TYPE if the classes b_i = w_i mod p
(folded) of the coordinates with L | w_i already cover every folded level-one
time.  Then w is witness-free at level L for any values of the other
coordinates (Lemma T of notes/lonely-runner/gates.md); its fate is decided by
the gcd clause and Lemma S alone, i.e. by the Lemma TN pattern of the other
coordinates (notes/lonely-runner/k17-structure.md section 3).

Usage: python3 classify.py k p L < xcasc dump ("S idx L w_1..w_k" lines)
Prints, per base index: #retained, #Lemma T type, and the distribution of
f = k - #{i : L | w_i}; then totals.
"""
import sys
from collections import Counter, defaultdict


def covers(k, p, classes):
    h = (p - 1) // 2
    need = set(range(1, h + 1))
    for v in set(classes):
        for a in list(need):
            if (k + 1) * min(a * v % p, p - a * v % p) < p:
                need.discard(a)
    return not need


def main():
    k, p, L = map(int, sys.argv[1:4])
    per = defaultdict(lambda: [0, 0, Counter()])
    for line in sys.stdin:
        if not line.startswith("S "):
            continue
        xs = [0] + list(map(int, line.split()[1:]))
        idx, lev, w = xs[1], xs[2], xs[3:]
        if lev != L:
            continue
        z = [min(x % p, p - x % p) for x in w if x % L == 0]
        rec = per[idx]
        rec[0] += 1
        if z and covers(k, p, z):
            rec[1] += 1
        rec[2][k - len(z)] += 1
    tot = sum(r[0] for r in per.values())
    tt = sum(r[1] for r in per.values())
    fs = Counter()
    for r in per.values():
        fs.update(r[2])
    for i in sorted(per):
        r = per[i]
        print(f"base {i}: retained {r[0]}, Lemma T type {r[1]}, f-distribution {dict(sorted(r[2].items()))}")
    print(f"TOTAL bases {len(per)}, retained {tot}, Lemma T type {tt} ({100.0 * tt / max(tot, 1):.2f}%), "
          f"f-distribution {dict(sorted(fs.items()))}")


if __name__ == "__main__":
    main()
