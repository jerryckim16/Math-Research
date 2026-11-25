"""Tests of the Beck-Everett relation theorem (arXiv:2609.06259v3, Thm 2 = Thm 1(a)).

Statement tested (general-h form, which is what their proof shows):
  Let k >= 2, n in Z_{>0}^k, 0 < delta < 1/2.  If lon(n) <= delta, i.e. there is
  no t with ||t n_j|| > delta for all j, then there is m in Z^k with m.n = 0,
  sum(m) odd ("harmful"), and ||m||_2^2 <= (k-1)/(1/2 - delta)^2.
  For delta = 1/(k+1) this is ||m||_2 <= 2(k+1)/sqrt(k-1), hence ||m||_1 <= 2k+3.

Checks (exact integer arithmetic; ML from lonely.max_loneliness, exact):
  1. every tight instance recorded in results/exhaustive.txt has such a relation
     at delta = 1/(k+1);
  2. exhaustively, for all tuples (repeats allowed) with entries <= N, k = 3,4,5,
     and several delta: lon(n) <= delta  ==>  harmful relation within the L2 bound;
  3. residue-level vacuity: for random v in Z_N^15, N = 16p, p in 251..743, a
     harmful m in {-1,0,1}^15 (||m||_2^2 <= 15 << 73) with m.v = 0 mod N exists.
     So the theorem cannot prune the level-one family or its lifts directly.
Usage: python3 beck_everett_check.py
"""
import itertools
import os
import random
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import lonely  # noqa: E402


def harmful_vectors(k, r2max):
    """All m in Z^k, m != 0, sum odd, ||m||^2 <= r2max, first nonzero > 0."""
    R = int(r2max ** 0.5)
    out = []

    def rec(i, cur, s2):
        if i == k:
            if sum(cur) % 2 == 1:
                nz = next(x for x in cur if x)
                if nz > 0:
                    out.append(tuple(cur))
            return
        for x in range(-R, R + 1):
            if s2 + x * x <= r2max:
                cur.append(x)
                rec(i + 1, cur, s2 + x * x)
                cur.pop()
    rec(0, [], 0)
    return out


def min_harmful(n, vecs):
    best = None
    for m in vecs:
        if sum(a * b for a, b in zip(m, n)) == 0:
            s = sum(x * x for x in m)
            if best is None or s < best[0]:
                best = (s, m)
    return best


def check_tight():
    rows = []
    with open(os.path.join(os.path.dirname(HERE), "results", "exhaustive.txt")) as f:
        for line in f:
            if "tight=" in line:
                rows.append(eval(line.split("tight=")[1].split(" seconds")[0]))
    seen, ok = set(), True
    for tl in rows:
        for n in tl:
            if n in seen:
                continue
            seen.add(n)
            k = len(n)
            r2 = F(4 * (k + 1) ** 2, k - 1)
            b = min_harmful(n, harmful_vectors(k, int(r2)))
            good = b is not None
            ok &= good
            print(f"tight {n}: min harmful ||m||^2 = {b[0]} via {b[1]} (bound {float(r2):.2f})" if good
                  else f"tight {n}: NO harmful relation within bound  <-- FAIL")
    return ok


def check_exhaustive(k, N, deltas):
    ok = True
    for delta in deltas:
        r2 = (k - 1) / (F(1, 2) - delta) ** 2
        vecs = harmful_vectors(k, int(r2))
        npos = 0
        for n in itertools.combinations_with_replacement(range(1, N + 1), k):
            ml = lonely.max_loneliness(n)[0]
            if ml <= delta:
                npos += 1
                if min_harmful(n, vecs) is None:
                    ok = False
                    print(f"  FAIL k={k} delta={delta} n={n} ML={ml}")
        print(f"k={k} N={N} delta={delta}: {npos} tuples with lon <= delta, all have a harmful "
              f"relation with ||m||^2 <= {float(r2):.2f}: {ok}")
    return ok


def check_residue_vacuity(trials=200, seed=1):
    rng = random.Random(seed)
    primes = [p for p in range(251, 744) if all(p % q for q in range(2, int(p ** .5) + 1))]
    k, worst = 15, None
    for _ in range(trials):
        p = rng.choice(primes)
        N = 16 * p
        v = []
        while len(v) < k:
            x = rng.randrange(1, N)
            if x % p:
                v.append(x)
        # meet in the middle over {-1,0,1}^15 with parity of support
        A, B = v[:7], v[7:]
        left = {}
        for c in itertools.product((-1, 0, 1), repeat=7):
            s = sum(a * b for a, b in zip(c, A)) % N
            left.setdefault((s, sum(map(abs, c)) % 2), c)
        hits = 0
        for c in itertools.product((-1, 0, 1), repeat=8):
            s = (-sum(a * b for a, b in zip(c, B))) % N
            par = sum(map(abs, c)) % 2
            if (s, 1 - par) in left:
                hits += 1
        worst = hits if worst is None else min(worst, hits)
        if hits == 0:
            print(f"  residue tuple without small harmful relation: N={N} v={v}")
    print(f"residue vacuity: {trials} random v in Z_(16p)^15: min number of right halves "
          f"completing a harmful {{-1,0,1}} relation = {worst} (> 0 means vacuous)")
    return worst > 0


if __name__ == "__main__":
    a = check_tight()
    b = check_exhaustive(3, 24, [F(1, 4), F(1, 3), F(2, 5)])
    c = check_exhaustive(4, 14, [F(1, 5), F(1, 4), F(1, 3)])
    d = check_residue_vacuity()
    print("ALL OK" if (a and b and c and d) else "SOME CHECK FAILED")
