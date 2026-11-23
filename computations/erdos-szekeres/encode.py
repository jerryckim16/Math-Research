"""SAT encoding: N points in general position with no k points in convex position.

Points are labelled 0..N-1 in increasing x-order. Variable X(a,b,c), a<b<c, is
true iff the triple (p_a, p_b, p_c) is positively oriented (counterclockwise).

Constraints
  1. Signotope axioms (Felsner-Weil): for a<b<c<d the sequence
     X(abc), X(abd), X(acd), X(bcd) changes sign at most once.
     Every x-sorted point set in general position satisfies these.
  2. No convex k-gon: for every k-subset i_1<...<i_k and every split of the
     k-2 inner points into an upper chain U and a lower chain L, forbid
     "U is a cap (consecutive triples negative) and L is a cup (consecutive
     triples positive)". A convex k-gon in x-order is exactly such a pattern.
  3. Symmetry breaking (optional, --sym): X(0,b,c) true for all 0<b<c.
     Justification in problems/erdos-szekeres.md (point 0 is a hull vertex
     moved by a projective map; the order type is unchanged).

Soundness direction: a real N-point set with no convex k-gon yields a
satisfying assignment. Hence UNSAT implies ES(k) <= N.
"""
import argparse
import itertools


def build(N, k, sym=True):
    var = {}
    for t in itertools.combinations(range(N), 3):
        var[t] = len(var) + 1
    X = lambda a, b, c: var[(a, b, c)]
    clauses = []
    # 1. signotope axioms
    for a, b, c, d in itertools.combinations(range(N), 4):
        s = [X(a, b, c), X(a, b, d), X(a, c, d), X(b, c, d)]
        for i, j, l in itertools.combinations(range(4), 3):
            clauses.append([-s[i], s[j], -s[l]])  # forbid + - +
            clauses.append([s[i], -s[j], s[l]])   # forbid - + -
    # 2. no convex k-gon
    for S in itertools.combinations(range(N), k):
        first, last, inner = S[0], S[-1], S[1:-1]
        for mask in range(1 << (k - 2)):
            up = [first] + [p for i, p in enumerate(inner) if mask >> i & 1] + [last]
            lo = [first] + [p for i, p in enumerate(inner) if not mask >> i & 1] + [last]
            cl = []
            for i in range(len(up) - 2):
                cl.append(X(up[i], up[i + 1], up[i + 2]))      # cap needs negative; negate -> positive literal
            for i in range(len(lo) - 2):
                cl.append(-X(lo[i], lo[i + 1], lo[i + 2]))     # cup needs positive; negate -> negative literal
            clauses.append(cl)
    # 3. symmetry breaking
    if sym:
        for b, c in itertools.combinations(range(1, N), 2):
            clauses.append([X(0, b, c)])
    return var, clauses


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("out")
    ap.add_argument("--nosym", action="store_true")
    a = ap.parse_args()
    var, clauses = build(a.N, a.k, sym=not a.nosym)
    with open(a.out, "w") as f:
        f.write(f"p cnf {len(var)} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print(f"N={a.N} k={a.k} vars={len(var)} clauses={len(clauses)}")


if __name__ == "__main__":
    main()
