"""Constructive form of Theorem 1 of notes/lonely-runner/general-n.md.

Theorem 1.  Let V be a set of n positive integers with max M and
    M <= 2n + 2 - E(n),   E(n) = max_{1<=j<=(n+1)/2} (j + g(j)),
g Jacobsthal's function.  (This implies the form with
M <= (3/2)(n+1) - G((n+1)/2), G(x) = max_{s<=x} g(s).)  Then some t has
||v t|| >= 1/(n+1) for all v in V.

`proof_witness(V)` follows the proof: it returns the witness the proof
produces (a Fraction) together with the step that produced it, or None if
the proof's case split does not apply (which the theorem says cannot
happen in the stated range).  Every returned witness is re-checked with
the independent routine lonely.check_witness (exact Fractions).

Steps (see the note):
  'small'   M <= n: V = [n], t = 1/(n+1)
  'div'     some j in (M/2, n+1], or some j in ((n+1)/2, M/2] with
            j, 2j not in V: t = 1/j (Lemma A)
  'pair'    some j <= (n+1)/2 not in V: N in (M+j, 2n+2] coprime to j,
            t = c/N with c = j^{-1} mod N (Lemma B)
"""
import os
import sys
from fractions import Fraction
from math import gcd
from itertools import combinations

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lonely import check_witness  # noqa: E402
from jacobsthal import G_table, E_values  # noqa: E402


def proof_witness(V):
    V = sorted(set(V))
    n = len(V)
    S = set(V)
    M = V[-1]
    if M <= n:
        return Fraction(1, n + 1), "small"
    for j in range(1, (n + 1) // 2 + 1):          # j <= (n+1)/2
        if j not in S:
            for N in range(M + j + 1, 2 * n + 3):
                if gcd(N, j) == 1:
                    c = pow(j, -1, N) if N > 1 else 0
                    return Fraction(c, N), "pair"
            return None, "pair-failed"
    for j in range((n + 1) // 2 + 1, n + 2):      # (n+1)/2 < j <= n+1
        if 2 * j > M and j not in S:
            return Fraction(1, j), "div"
        if 2 * j <= M and j not in S and 2 * j not in S and 3 * j > M:
            return Fraction(1, j), "div"
    return None, "no-case"


def bound_simple(n, G):
    """floor(3(n+1)/2 - G((n+1)/2)), the simple form of Theorem 1."""
    return (3 * (n + 1) - 2 * G[(n + 1) // 2]) // 2


def bound(n, E):
    """Largest M allowed by Theorem 1 (sharp form): 2n + 2 - E(n)."""
    return 2 * n + 2 - E[n]


def check_range(nmax):
    """All n-subsets V with max V <= bound(n), for 1 <= n <= nmax."""
    G, g = G_table(max(10, nmax))
    E = E_values(nmax, g)
    total = 0
    stats = {}
    for n in range(1, nmax + 1):
        assert bound(n, E) >= bound_simple(n, G)
        B = bound(n, E)
        for V in combinations(range(1, B + 1), n):
            t, how = proof_witness(V)
            if t is None or not check_witness(V, t):
                raise AssertionError((n, V, how))
            stats[how] = stats.get(how, 0) + 1
            total += 1
    return total, stats


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    G, g = G_table(200)
    E = E_values(nmax, g)
    for n in range(1, nmax + 1):
        print(n, "bound M <=", bound(n, E), "(simple form:", bound_simple(n, G), ")")
    print(check_range(nmax))
