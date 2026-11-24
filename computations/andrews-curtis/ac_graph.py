"""Reference (slow, Python) implementation of the junction GS-substitution graph
searched by ac_search*.cpp: forward edges, and exact PREDECESSOR enumeration.

Letters are codes X=0, Y=1, x=2, y=3 (the C++ engines' order); inverse = c ^ 2.
A state is an unordered pair of cyclic words, each up to rotation and
inversion; it is stored as a sorted pair of canonical words, where the
canonical word of w is the lexicographically least rotation of w or w^-1
(this is exactly the order of `pack`/`canon` in the C++ engines, and fixes the
"canonical orientation" that the forward move uses).

Forward edge (as in ac_search_compact.cpp): for each slot i, a = canonical word
of r_i, b0 = canonical word of the other relator; for e = +-1, b = b0^e; for
every rotation A of a and B of b whose junction cancels (last(A) = first(B)^-1):
r_i <- cyclic_reduce(A B).  Only the canonical orientation of r_i is rotated,
so the graph is directed (see problems/andrews-curtis.md, "Directedness").

Predecessors.  An edge S = {u, v} -> T = {p, v} keeps v and replaces u by
p ~ cyclic_reduce(A B), A a rotation of u (canonical orientation), B a rotation
of v^{+-1}, junction cancelling.  In the cyclic word A.B every cancelling pair
joins a letter of A and a letter of B, except after one of the two words has
been consumed completely.  Writing M for a rotation of p^{+-1} and Z for the
consumed part, this gives exactly three shapes (pred() docstring); conversely
each shape yields an edge by an explicit choice of A and B, provided the
cyclic word written down for u is u's canonical orientation.  test_ac.py checks
pred() against the inverted forward map on every state of small energy.

Usage: python3 ac_graph.py STATE CAP     e.g.  xxxYYYY/xyxYXY 16
"""
import sys

LET = "XYxy"


def parse(s):
    return tuple(LET.index(c) for c in s)


def show(w):
    return "".join(LET[c] for c in w)


def inv(w):
    return tuple(c ^ 2 for c in reversed(w))


def freered(w):
    out = []
    for c in w:
        if out and out[-1] == c ^ 2:
            out.pop()
        else:
            out.append(c)
    return tuple(out)


def cycred(w):
    w = freered(w)
    i, j = 0, len(w)
    while j - i >= 2 and w[i] == w[j - 1] ^ 2:
        i += 1
        j -= 1
    return w[i:j]


def rots(w):
    return [w[k:] + w[:k] for k in range(len(w))] or [w]


def canon(w):
    """Least rotation of w or w^-1 (w cyclically reduced)."""
    return min(rots(w) + rots(inv(w)))


def is_canonical_orientation(w):
    """True iff some rotation of w (not of w^-1) is canon(w)."""
    return min(rots(w)) == canon(w)


def key(u, v):
    return tuple(sorted((canon(u), canon(v))))


def energy(state):
    return len(state[0]) + len(state[1])


def cyc_reduced(w):
    return len(w) < 2 or w[0] != w[-1] ^ 2


def reduced(w):
    return all(w[k + 1] != w[k] ^ 2 for k in range(len(w) - 1))


def forward(state, cap):
    """Successors of `state` (a key) with energy < cap; multiset collapsed."""
    out = set()
    for i in (0, 1):
        a, b0 = state[i], state[1 - i]
        for b in (b0, inv(b0)):
            if not a or not b:
                continue
            for A in rots(a):
                for B in rots(b):
                    if B[0] != A[-1] ^ 2:
                        continue
                    nw = cycred(A + B)
                    if len(nw) + len(b0) >= cap or len(nw) > 29:
                        continue
                    out.add(key(nw, b0))
    return out


def pred(state, cap):
    """All S with an edge S -> state and energy(S) < cap.

    For the kept relator v (either word of `state`, nonempty) and the new
    relator p (the other word), u ranges over the cyclic words
      (I)   f M f^-1 Z    M rotation of p^{+-1}, Z rotation of v^{+-1},
                          f any word; the whole cyclic word reduced
                          (B = Z^-1 consumed; then u's own arc may cancel, f);
      (II)  M1 Z          M = M1 M2 a rotation of p^{+-1}, M1, M2 nonempty,
                          M2 Z^-1 a rotation of v^{+-1}, Z nonempty; cyclic
                          word M1 Z reduced (both words leave an arc);
      (III) Z             g M g^-1 Z^-1 a rotation of v^{+-1}, Z nonempty,
                          Z cyclically reduced (A = Z consumed);
    and S = {u, v} is a predecessor iff, in addition, the cyclic word written
    is u's canonical orientation (the forward move rotates only that one).
    """
    out = set()
    for i in (0, 1):
        p, v = state[i], state[1 - i]
        if not v:
            continue
        nv = len(v)
        Ms = set(rots(p)) | set(rots(inv(p)))
        Vs = set(rots(v)) | set(rots(inv(v)))

        cand = set()
        add = cand.add

        # (I): f M f^-1 Z, |u| = 2|f| + |p| + |v|
        fmax = (cap - 1 - len(p) - 2 * nv) // 2
        for M in Ms:
            for Z in Vs:
                stack = [()]
                while stack:
                    f = stack.pop()
                    core = f + M + inv(f)
                    if not reduced(core):
                        continue              # growing f outward cannot repair this
                    u = core + Z
                    if reduced(u) and cyc_reduced(u):
                        add(u)
                    if len(f) < fmax and M:   # (f f^-1 is never reduced)
                        stack.extend((c,) + f for c in range(4))
        # (II): M1 Z with M = M1 M2, rotation of v^{+-1} = M2 Z^-1
        for M in Ms:
            for j in range(1, len(M)):
                M1, M2 = M[:j], M[j:]
                for V in Vs:
                    if len(V) > len(M2) and V[:len(M2)] == M2:
                        add(M1 + inv(V[len(M2):]))
        # (III): rotation of v^{+-1} = g M g^-1 Z^-1
        for V in Vs:
            for gl in range(0, nv):
                for M in Ms:
                    m = len(M)
                    if 2 * gl + m >= nv:
                        continue
                    if V[gl:gl + m] != M or V[gl + m:2 * gl + m] != inv(V[:gl]):
                        continue
                    add(inv(V[2 * gl + m:]))
        cv = canon(v)
        for u in cand:
            if (u and len(u) + nv < cap and len(u) <= 29 and cyc_reduced(u) and reduced(u)
                    and is_canonical_orientation(u)):
                out.add(tuple(sorted((canon(u), cv))))
    return out


if __name__ == "__main__":
    s = sys.argv[1].split("/")
    st = key(cycred(parse(s[0])), cycred(parse(s[1])))
    cap = int(sys.argv[2])
    print("forward:", sorted("|".join(map(show, t)) for t in forward(st, cap)))
    print("pred:   ", sorted("|".join(map(show, t)) for t in pred(st, cap)))
