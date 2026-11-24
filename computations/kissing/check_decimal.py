"""Exact pairwise kissing check for a small configuration given as decimal text.

Input: a text file with one point per line, coordinates separated by
whitespace or commas, each a decimal literal (e.g. -0.1977552394027646 or
1.5e-05). Every literal is read EXACTLY as a rational number (fractions.Fraction
on the string), so the check is about the configuration exactly as published,
not about a floating-point approximation of it. Rows need not be unit
vectors: angles are scale-free.

Each row is scaled to integers by the least common denominator of its
entries (a positive factor, which does not change angles); then, with
p = a.b, A = |a|^2, B = |b|^2 in Python integers, the pair is fine iff
p <= 0 or 4p^2 <= AB (the criterion of kiss_check.c). Reports violations,
exact contacts (4p^2 = AB), and the largest cosine as a float together with
its exact gap below 1/2 (lower bound, as a float). O(n^2 d) big-integer
operations: meant for n up to a few thousand.

Negative controls (--control KIND I J, applied after reading, before the check):
  dup    append a copy of row I
  merge  append row I + row J (a positive combination of the two directions,
         so within 30 degrees of one of them when I, J are about 60 apart)
  nudge  replace row I by row I + 10^-6 * row J (moves I towards J)
Each must FAIL on a valid configuration (nudge: when I, J is a near-contact).

Usage: python3 -I check_decimal.py FILE D [--skip-header K] [--control KIND I J]
"""
import math
import sys
from fractions import Fraction


def read_rows(path, d, skip):
    rows = []
    with open(path) as f:
        for i, line in enumerate(f):
            if i < skip or not line.strip():
                continue
            toks = line.replace(",", " ").split()
            if len(toks) != d:
                raise SystemExit(f"line {i + 1}: {len(toks)} entries, expected {d}")
            fr = [Fraction(t) for t in toks]
            den = 1
            for x in fr:
                den = den * x.denominator // math.gcd(den, x.denominator)
            rows.append([int(x * den) for x in fr])
    return rows


def apply_control(rows, kind, i, j):
    a, b = rows[i], rows[j]
    if kind == "dup":
        rows.append(list(a))
    elif kind == "merge":
        rows.append([x + y for x, y in zip(a, b)])
    elif kind == "nudge":
        rows[i] = [10**6 * x + y for x, y in zip(a, b)]
    else:
        raise SystemExit("unknown control")


def main(path, d, skip=0, control=None):
    rows = read_rows(path, d, skip)
    if control:
        apply_control(rows, *control)
    n = len(rows)
    norms = [sum(x * x for x in r) for r in rows]
    if min(norms) <= 0:
        raise SystemExit("zero row")
    viol = contacts = seen = 0
    best = None          # (p^2, AB, i, j) of the largest cosine so far
    for i in range(n):
        a, A = rows[i], norms[i]
        for j in range(i + 1, n):
            b, B = rows[j], norms[j]
            seen += 1
            p = sum(x * y for x, y in zip(a, b))
            if p <= 0:
                continue
            lhs, rhs = 4 * p * p, A * B
            if lhs > rhs:
                viol += 1
            elif lhs == rhs:
                contacts += 1
            # cos^2 = p^2/(AB); compare exactly, keep the largest
            if best is None or p * p * best[1] > best[0] * A * B:
                best = (p * p, A * B, i, j)
    cos2 = Fraction(best[0], best[1]) if best else Fraction(0)
    cmax = math.sqrt(float(cos2))
    gap = Fraction(1, 4) - cos2
    print(f"rows={n} d={d}")
    assert seen == n * (n - 1) // 2
    print(f"pairs_checked={seen}")
    print(f"violations={viol}")
    print(f"contacts={contacts}")
    if best:
        print(f"max_cosine={cmax:.15f} at rows ({best[2]},{best[3]}); "
              f"exact 1/4 - cos^2 = {float(gap):.6e}")
    print("RESULT: PASS" if viol == 0 else "RESULT: FAIL")
    return 0 if viol == 0 else 1


if __name__ == "__main__":
    skip = 0
    if "--skip-header" in sys.argv:
        skip = int(sys.argv[sys.argv.index("--skip-header") + 1])
    control = None
    if "--control" in sys.argv:
        k = sys.argv.index("--control")
        control = (sys.argv[k + 1], int(sys.argv[k + 2]), int(sys.argv[k + 3]))
    sys.exit(main(sys.argv[1], int(sys.argv[2]), skip, control))
