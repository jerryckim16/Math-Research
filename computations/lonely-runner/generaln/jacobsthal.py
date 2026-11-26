"""Jacobsthal function g(s) and the explicit range of Theorem 1 (general-n.md).

g(s) = least g such that every g consecutive integers contain one coprime
to s (g(1) = 1).  g(s) depends only on rad(s).  G(x) = max_{1<=s<=x} g(s).

Exact values: g(r) for every squarefree r <= X, by marking the residues
0..r-1 that share a prime with r and taking the longest cyclic run of
marked residues (plus one).

Bound used beyond X (Lemma J of general-n.md, proved there by
inclusion-exclusion):  g(s) <= ceil((2^w - 1) * s/phi(s)),  w = omega(s),
and s/phi(s) <= prod_{i<=w} p_i/(p_i - 1) (first w primes).

Theorem 1 (general-n.md): if v_n <= (3/2)(n+1) - G((n+1)/2) then the
n speeds are lonely.  `n0_for_alpha(a, b)` returns the least n0 such that
floor(a n / b) <= (3/2)(n+1) - G((n+1)/2) holds for every n >= n0
(exact integer arithmetic; the tail is handled by the bound).
"""
from fractions import Fraction
import sys


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(N + 1) if s[i]]


def prime_factors(n, ps):
    out = []
    for p in ps:
        if p * p > n:
            break
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        out.append(n)
    return out


def g_exact(r, pf):
    """Jacobsthal g of squarefree r with prime factors pf (exact)."""
    if r == 1:
        return 1
    mark = bytearray(r)
    for p in pf:
        mark[0::p] = b"\x01" * len(mark[0::p])
    doubled = bytes(mark) + bytes(mark)
    run = max(len(x) for x in doubled.split(b"\x00"))
    return run + 1


def G_table(X):
    """G[x] = max_{s<=x} g(s) for 0 <= x <= X (G[0] = 0)."""
    ps = primes_upto(X + 1)
    g = [0] * (X + 1)
    cache = {}
    for s in range(1, X + 1):
        pf = prime_factors(s, ps)
        r = 1
        for p in pf:
            r *= p
        if r not in cache:
            cache[r] = g_exact(r, pf)
        g[s] = cache[r]
    G = [0] * (X + 1)
    for s in range(1, X + 1):
        G[s] = max(G[s - 1], g[s])
    return G, g


def tail_bound(k, ps):
    """Upper bound for g(s) when omega(s) <= k: ceil((2^k - 1) prod p/(p-1))."""
    prod = Fraction(1)
    for p in ps[:k]:
        prod *= Fraction(p, p - 1)
    v = (2 ** k - 1) * prod
    return -((-v.numerator) // v.denominator)


def n0_for_alpha(a, b, X=5000):
    """Least n0 with floor(a n/b) <= 3(n+1)/2 - G((n+1)/2) for all n >= n0.

    For x = (n+1)/2 <= X the exact table is used; for x > X we use
    G(x) <= max(G(X), tail_bound(k)) where k = max omega(s) for s <= x,
    and check the inequality on each block [p_k#, p_{k+1}#) of x at its
    worst point (smallest n in the block), which suffices because the
    right side minus the left side is nondecreasing in n once G is fixed
    (it grows like (3/2 - a/b) n with a/b < 3/2)."""
    assert Fraction(a, b) < Fraction(3, 2)
    G, _ = G_table(X)
    ps = primes_upto(1000)

    def ok(n, Gval):
        return 2 * ((a * n) // b) <= 3 * (n + 1) - 2 * Gval

    bad_last = None
    for n in range(1, 2 * X + 1):
        x = (n + 1) // 2  # G((n+1)/2) = G(floor((n+1)/2))
        if not ok(n, G[x]):
            bad_last = n
    # tail: x > X, i.e. n >= 2X
    k = 0
    prim = 1
    while prim * ps[k] <= X:
        prim *= ps[k]
        k += 1
    # now omega(s) <= k for s <= X; blocks
    lo_x = X + 1
    while True:
        nxt = prim * ps[k]  # smallest s with omega = k+1
        Gb = max(G[X], tail_bound(k, ps))
        n_lo = 2 * lo_x - 1
        # need ok for all n with x in [lo_x, nxt-1]; monotone -> check n_lo
        # unfloored (stronger) form, valid for every n >= n_lo in the block
        if not (2 * a * n_lo <= b * (3 * (n_lo + 1) - 2 * Gb)):
            return None  # bound too weak; increase X
        if k >= 40:
            break
        lo_x = nxt
        prim = nxt
        k += 1
    # k > 40: tail_bound(k) <= 4^k <= p_k#/10^9 <= x/10^9, so the
    # inequality holds trivially there (see general-n.md, Lemma J remark).
    return 1 if bad_last is None else bad_last + 1


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    X = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    G, g = G_table(min(X, 200))
    print("G(x) jumps for x<=200:", [(x, G[x]) for x in range(1, 201) if G[x] != G[x - 1]])
    print("alpha = %d/%d: n0 =" % (a, b), n0_for_alpha(a, b, X))
