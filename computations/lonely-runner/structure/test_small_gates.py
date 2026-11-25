"""Validation of Lemma S (level one at k+2 <= p <= 2k+1) against the project's
independent level-one engines, plus the Burnside orbit-count formula.

For every k in 3..12 and prime p with k+2 <= p <= 2k+1:
  * small_gates.level_one(k,p)   (Lemma S: multisets containing every class)
  * sieve.level1_improper_covers  (covergen.c minimal covers + extensions)
  * sieve.level1_improper_c       (naive level1.c DFS; only when cheap)
must give the same set of canonical orbit representatives, and its size must
equal the Burnside count (1/n) sum_{d | gcd(n, k-n)} phi(d) C(n/d + (k-n)/d - 1, (k-n)/d).
Run: python3 test_small_gates.py
"""
import os
import sys
from math import comb, gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import sieve  # noqa: E402
import small_gates as sg  # noqa: E402


def phi(d):
    return sum(1 for x in range(1, d + 1) if gcd(x, d) == 1)


def burnside(n, e):
    g = gcd(n, e) if e else n
    return sum(phi(d) * comb(n // d + e // d - 1, e // d)
               for d in range(1, g + 1) if g % d == 0 and n % d == 0 and e % d == 0) // n


def isprime(p):
    return p > 1 and all(p % q for q in range(2, int(p ** .5) + 1))


def main():
    ok = True
    for k in range(3, 13):
        for p in range(k + 2, 2 * k + 2):
            if not isprime(p):
                continue
            n = (p - 1) // 2
            a = sg.level_one(k, p)
            b, _ = sieve.level1_improper_covers(k, p)
            L = sieve.Level(k, p, 1)
            a_c = sorted({L.canon(list(t)) for t in a})   # same canonical form as sieve
            same = a_c == b
            line = f"k={k} p={p}: lemma {len(a)} covergen {len(b)} burnside {burnside(n, k - n)}"
            same &= len(a) == burnside(n, k - n)
            if comb(n + k - 2, k - 1) <= 2_000_000:
                c, _ = sieve.level1_improper_c(k, p)
                same &= c == b
                line += f" naive {len(c)}"
            print(line, "OK" if same else "MISMATCH")
            ok &= same
    # k = 15 orbit counts
    for p in (17, 19, 23, 29, 31):
        n = (p - 1) // 2
        print(f"k=15 p={p}: lemma {len(sg.level_one(15, p))} burnside {burnside(n, 15 - n)}")
        ok &= len(sg.level_one(15, p)) == burnside(n, 15 - n)
    print("ALL OK" if ok else "FAIL")


if __name__ == "__main__":
    main()
