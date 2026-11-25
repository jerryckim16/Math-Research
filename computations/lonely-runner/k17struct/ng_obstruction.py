"""NG-surviving Lemma T elements: for which levels l can an NG cascade NOT close?

Setting (notes/lonely-runner/k17-structure.md, Lemma TN).  Fix k, a prime p with a cover
C = {c_1..c_s} of the folded times (s = tau_k(p)), f = k - s >= 2 free coordinates, and a
level l coprime to p.  For u in Z^f put (CRT)
    w_i = c_i (mod p), 0 (mod l)        (i <= s)
    w_{s+j} = 1 (mod p), u_j (mod l)     (j <= f).
w is improper at level l (Lemma T of gates.md) as soon as the gcd clause fails, i.e.
    gcd(l, u_j : j != j0) = 1 for every j0                     (robust gcd condition),
and w is NOT settled by Lemma NG at any divisor d >= 2 of l iff for every such d either
d | u_j for all j, or  sum_{j : d does not divide u_j} g_j * ceil(2d/((k+1) g_j)) >= d,
g_j = gcd(u_j, d).  Only e_j = gcd(u_j, l) matters, so we search multisets of divisors.

Usage: python3 ng_obstruction.py k f l_max [primes]   (levels l = 2^a 3^b <= l_max)
       python3 ng_obstruction.py witness k p l e_1 ... e_f   (print an explicit tuple)
Output per level: SURVIVES (with a divisor pattern e) or NG-CLOSED (no pattern exists).
"""
import itertools
import sys
from math import gcd


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def cost(k, e, d):
    """NG cost at d of free coordinates with gcd pattern e (gcd(u_j, l) = e_j)."""
    tot, E = 0, 0
    for x in e:
        g = gcd(x, d)
        if g == d:
            continue
        E += 1
        tot += g * (-(-2 * d // ((k + 1) * g)))
    return E, tot


def robust(l, e):
    for j0 in range(len(e)):
        g = l
        for j, x in enumerate(e):
            if j != j0:
                g = gcd(g, x)
        if g != 1:
            return False
    return True


def survives(k, l, e):
    for d in divisors(l)[1:]:
        E, c = cost(k, e, d)
        if E >= 1 and c < d:
            return False, d
    return True, None


def search(k, f, l):
    divs = divisors(l)
    for e in itertools.combinations_with_replacement(divs, f):
        if robust(l, e) and survives(k, l, e)[0]:
            return e
    return None


def levels(lmax, primes=(2, 3)):
    out = {1}
    for q in primes:
        new = set()
        for x in out:
            y = x
            while y <= lmax:
                new.add(y)
                y *= q
        out = new
    return sorted(x for x in out if x > 1)


def witness(k, p, l, e):
    """Explicit CRT tuple mod lp for the Lemma S cover C = all folded classes 1..(p-1)/2."""
    n = (p - 1) // 2
    s = n
    assert len(e) == k - s
    N = l * p
    def crt(a_p, a_l):
        for x in range(N):
            if x % p == a_p % p and x % l == a_l % l:
                return x
    return [crt(c, 0) for c in range(1, n + 1)] + [crt(1, x) for x in e]


if __name__ == "__main__":
    if sys.argv[1] == "witness":
        k, p, l = map(int, sys.argv[2:5])
        e = list(map(int, sys.argv[5:]))
        print(*witness(k, p, l, e))
        sys.exit()
    k, f, lmax = map(int, sys.argv[1:4])
    primes = tuple(map(int, sys.argv[4].split(","))) if len(sys.argv) > 4 else (2, 3)
    for l in levels(lmax, primes):
        e = search(k, f, l)
        print(f"k={k} f={f} l={l}: " + (f"SURVIVES e={e}" if e else "NG-CLOSED (no robust pattern survives NG)"), flush=True)
