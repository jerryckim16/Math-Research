"""Compact SAT encoding: N points in general position with no convex k-gon.

Same orientation variables, signotope axioms and symmetry breaking as
encode.py (variable X(a,b,c), a<b<c, numbered identically, 1..C(N,3)). The
forbidden pattern is expressed with auxiliary cup/cap variables instead of one
clause per k-subset and split, so the size is O(N^4 k) instead of
O(C(N,k) 2^(k-2)).

Definitions (points labelled 0..N-1 in increasing x-order)
  An l-cup (l >= 3) is i_1 < ... < i_l with X(i_j, i_{j+1}, i_{j+2}) true for
  all j; an l-cap has all these triples false. A 2-cup/2-cap is any pair.

Auxiliary variables, for 3 <= l <= k and a < c < d
  U[l](a,c,d): "there is an l-cup with first point a and last two points c,d"
  C[l](a,c,d): the same for caps.
  and for 3 <= l <= k-1, a < d
  EU[l](a,d): "there is an l-cup from a to d" (first point a, last point d)
  EC[l](a,d): the same for caps.

Clauses (all are implications "pattern => aux", plus the prohibitions)
  (S)  signotope axioms, exactly as encode.py.
  (B)  X(a,c,d) -> U[3](a,c,d);      -X(a,c,d) -> C[3](a,c,d).
  (R)  U[l](a,b,c) & X(b,c,d) -> U[l+1](a,c,d)       for 3 <= l < k,
       C[l](a,b,c) & -X(b,c,d) -> C[l+1](a,c,d).
  (E)  U[l](a,c,d) -> EU[l](a,d);  C[l](a,c,d) -> EC[l](a,d)   (3 <= l <= k-1).
  (F)  -U[k](a,c,d), -C[k](a,c,d)                        (no k-cup, no k-cap);
       -EU[l](a,d) | -EC[k+2-l](a,d) for 3 <= l <= k-1  (no l-cup and
       (k+2-l)-cap sharing both end points).
  (Y)  X(0,b,c) for 0<b<c (unless --nosym), as in encode.py.

Soundness (every x-sorted real point set with no convex k-gon satisfies the
formula, hence UNSAT => ES(k) <= N)
  Take a set P in general position with distinct x-coordinates (rotate
  slightly if needed), label it in x-order, set X to the true orientations and
  every auxiliary variable to the truth value of its defining statement.
  * (S) holds for every such P (Felsner-Weil; see encode.py), and (Y) can be
    assumed WLOG by the symmetry lemma in problems/erdos-szekeres.md.
  * (B), (R), (E) hold because each just appends one point to a chain whose
    defining triples are all positive (resp. negative), or forgets data.
  * (F): a k-cup or a k-cap is k points in convex position. For the second
    family, suppose P has an l-cup a=u_1<...<u_l=d and an m-cap
    a=v_1<...<v_m=d with l+m = k+2, l,m >= 3. The cup is the vertex sequence
    of the graph of a strictly convex piecewise-linear function f on
    [x_a, x_d], and the cap of a strictly concave g, with f = g at x_a and
    x_d. So f < (chord ad) < g in the open interval: interior cup points lie
    strictly below line ad, interior cap points strictly above, the two chains
    share only a and d, and together they have l+m-2 = k points. The region
    {x_a <= x <= x_d, f(x) <= y <= g(x)} is convex, and every one of the k
    points is a vertex of it (strict convexity/concavity at interior
    vertices; a and d are the unique points with extreme x). So the k points
    are in convex position, contradicting the assumption.
  Hence the true assignment satisfies every clause.

Relation to encode.py: a convex k-gon in x-order is exactly a cap (upper
chain) and a cup (lower chain) from its leftmost to its rightmost point, with
lengths summing to k+2. encode.py forbids each such pattern by one clause; here
(F) forbids the same patterns through the auxiliaries (lengths 2 and k are the
pure k-cup / k-cap clauses). Conversely, any assignment satisfying encode.py's
formula extends to this one (set each aux to its defining statement; under (S) an
l-cup has all C(l,3) triples positive, by induction, since for a 4-tuple a
sequence (+,?,?,+) with at most one sign change is constant, so interior points of a cup/cap from a
to d have X(a,x,d) true/false, the two chains are disjoint and (F) is exactly
encode.py's prohibition), and any
assignment satisfying this one satisfies encode.py's clauses (an encode.py
pattern forces, via (B),(R),(E), a pair of aux variables that (F) forbids).
So the two formulas are equisatisfiable; test_encoding.py and the
agreement table in problems/erdos-szekeres.md check this empirically.

Optional extra symmetry breaking (symmetry_extra.py; soundness proof in
problems/erdos-szekeres.md, Approach 5): --reflect short|full adds a
lex-leader constraint for the mirror symmetry, --ear adds the hull-ear rule
for the choice of point 0. Without these flags the output is unchanged
(byte-identical CNF).

Usage: python3 encode_compact.py N k out.cnf [--nosym] [--reflect short|full] [--ear]
"""
import argparse
import itertools


def build(N, k, sym=True, reflect=None, ear=False):
    """Return (var, aux, clauses, nvars).

    var: dict (a,b,c) -> orientation variable (same numbering as encode.py).
    aux: dict key -> variable, keys ('U'|'C', l, a, c, d) and ('EU'|'EC', l, a, d).
    """
    assert k >= 4
    var = {}
    for t in itertools.combinations(range(N), 3):
        var[t] = len(var) + 1
    nv = len(var)
    aux = {}

    def new(key):
        nonlocal nv
        nv += 1
        aux[key] = nv
        return nv

    for l in range(3, k + 1):
        for (a, c, d) in itertools.combinations(range(N), 3):
            new(('U', l, a, c, d))
            new(('C', l, a, c, d))
    for l in range(3, k):
        for (a, d) in itertools.combinations(range(N), 2):
            new(('EU', l, a, d))
            new(('EC', l, a, d))

    X = lambda a, b, c: var[(a, b, c)]
    clauses = []
    # (S) signotope axioms -- identical to encode.py
    for a, b, c, d in itertools.combinations(range(N), 4):
        s = [X(a, b, c), X(a, b, d), X(a, c, d), X(b, c, d)]
        for i, j, l in itertools.combinations(range(4), 3):
            clauses.append([-s[i], s[j], -s[l]])
            clauses.append([s[i], -s[j], s[l]])
    # (B) base
    for (a, c, d) in itertools.combinations(range(N), 3):
        clauses.append([-X(a, c, d), aux[('U', 3, a, c, d)]])
        clauses.append([X(a, c, d), aux[('C', 3, a, c, d)]])
    # (R) extension
    for l in range(3, k):
        for a, b, c, d in itertools.combinations(range(N), 4):
            clauses.append([-aux[('U', l, a, b, c)], -X(b, c, d), aux[('U', l + 1, a, c, d)]])
            clauses.append([-aux[('C', l, a, b, c)], X(b, c, d), aux[('C', l + 1, a, c, d)]])
    # (E) end-point summaries
    for l in range(3, k):
        for (a, c, d) in itertools.combinations(range(N), 3):
            clauses.append([-aux[('U', l, a, c, d)], aux[('EU', l, a, d)]])
            clauses.append([-aux[('C', l, a, c, d)], aux[('EC', l, a, d)]])
    # (F) prohibitions
    for (a, c, d) in itertools.combinations(range(N), 3):
        clauses.append([-aux[('U', k, a, c, d)]])
        clauses.append([-aux[('C', k, a, c, d)]])
    for l in range(3, k):
        m = k + 2 - l
        for (a, d) in itertools.combinations(range(N), 2):
            clauses.append([-aux[('EU', l, a, d)], -aux[('EC', m, a, d)]])
    # (Y) symmetry breaking -- identical to encode.py
    if sym:
        for b, c in itertools.combinations(range(1, N), 2):
            clauses.append([X(0, b, c)])
    if reflect or ear:
        import symmetry_extra
        assert sym, "--reflect/--ear assume the X(0,b,c) normalisation"
        nv = symmetry_extra.add(N, var, aux, clauses, nv, reflect=reflect, ear=ear)
    return var, aux, clauses, nv


def aux_truth(N, k, val):
    """Truth values of the auxiliary variables for an orientation assignment val."""
    t = {}
    for (a, c, d) in itertools.combinations(range(N), 3):
        t[('U', 3, a, c, d)] = val[(a, c, d)]
        t[('C', 3, a, c, d)] = not val[(a, c, d)]
    for l in range(4, k + 1):
        for (a, c, d) in itertools.combinations(range(N), 3):
            t[('U', l, a, c, d)] = any(t[('U', l - 1, a, b, c)] and val[(b, c, d)] for b in range(a + 1, c))
            t[('C', l, a, c, d)] = any(t[('C', l - 1, a, b, c)] and not val[(b, c, d)] for b in range(a + 1, c))
    for l in range(3, k):
        for (a, d) in itertools.combinations(range(N), 2):
            t[('EU', l, a, d)] = any(t[('U', l, a, c, d)] for c in range(a + 1, d))
            t[('EC', l, a, d)] = any(t[('C', l, a, c, d)] for c in range(a + 1, d))
    return t


def write_cnf(path, nv, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("out")
    ap.add_argument("--nosym", action="store_true")
    ap.add_argument("--reflect", choices=["short", "full"], default=None)
    ap.add_argument("--ear", action="store_true")
    a = ap.parse_args()
    var, aux, clauses, nv = build(a.N, a.k, sym=not a.nosym, reflect=a.reflect, ear=a.ear)
    write_cnf(a.out, nv, clauses)
    print(f"N={a.N} k={a.k} vars={nv} (orientation {len(var)}, aux {len(aux)}) clauses={len(clauses)}")


if __name__ == "__main__":
    main()
