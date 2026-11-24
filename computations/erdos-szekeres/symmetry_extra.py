"""Extra symmetry breaking for the signotope encodings (encode_compact.py).

Setting. Points 0..N-1 in x-order, with X(0,b,c) true for all 0<b<c
(clause family (Y)): point 0 is a hull vertex and 1..N-1 are its
counterclockwise angular order. Two choices remain free in that
normalisation: the mirror image, and which hull vertex is point 0.

(R) Reflection. Mirroring the point set and renumbering 1..N-1 so that the
    counterclockwise order around point 0 is kept maps the normalised
    assignment A to sigma(A), where
        sigma(A)(a,b,c) = A(N-c, N-b, N-a)   for 1 <= a < b < c <= N-1,
    and leaves X(0,.,.) = true (see Approach 5 in problems/erdos-szekeres.md;
    tested in test_encoding.py). We add the lex-leader constraint
        (A(v_1), ..., A(v_m))  <=_lex  (A(sigma v_1), ..., A(sigma v_m))
    (false < true) for a fixed list V = (v_1..v_m) of orientation variables:
      short: V = X(a,a+1,a+2) for a = floor((N-3)/2) down to 1, i.e. the
             consecutive triples left of the middle, read from the middle out
             (the predicate of Heule-Scheucher 2024, eq. (sbp)).
      full:  the short list followed by every other variable with a >= 1 not
             fixed by sigma (by increasing span c-a, middle out).
    Encoding (chain, e_i = "prefix 1..i equal"): for each i
        e_{i-1} -> (-A(v_i) | A(sigma v_i)),
        e_{i-1} & A(v_i) & A(sigma v_i) -> e_i,
        e_{i-1} & -A(v_i) & -A(sigma v_i) -> e_i,     with e_0 = true.
(E) Hull ear. For a hull vertex v with hull neighbours v-, v+ let ear(v) be
    the number of points strictly inside the triangle (v-, v, v+). Choosing
    point 0 as a hull vertex minimising ear(.) gives ear(0) <= ear(1) and
    ear(0) <= ear(N-1) (1 and N-1 are the hull neighbours of 0). In the
    normalisation:
      * i (1 <= i <= N-1) is a hull vertex iff X(a,i,c) for all 1<=a<i<c<=N-1;
      * ear(0) = #{ b : 1 < b < N-1, X(1,b,N-1) false };
      * ear(1) = h2 - 2 and ear(N-1) = N - 2 - h', where h2 is the hull vertex
        after 1 and h' the hull vertex before N-1 in angular order.
    Clauses (all aux variables are forced only upward, so setting them to their
    definitions satisfies everything):
      H_i  <-  AND_{a<i<c} X(a,i,c)                         (2 <= i <= N-2)
      G_t  <-  "at least t of -X(1,b,N-1)"  (sequential counter)
      H_i -> -G_{i-1}            (ear(0) <= i-2 for every hull vertex i >= 2)
      H_i -> -G_{N-1-i}          (ear(0) <= N-2-i for every hull vertex i <= N-2)
    Mirroring keeps every ear count and swaps the roles of 1 and N-1, so (R)
    and (E) can be imposed together.
"""
import itertools


def sigma(N, t):
    a, b, c = t
    assert a >= 1
    return (N - c, N - b, N - a)


def reflect_order(N, mode):
    short = []
    for a in range((N - 3) // 2, 0, -1):
        t = (a, a + 1, a + 2)
        if sigma(N, t) != t and a + 2 <= N - 1:
            short.append(t)
    if mode == "short":
        return short
    seen = set(short)
    rest = []
    for span in range(2, N - 1):
        row = [(a, b, a + span) for a in range(1, N - span) for b in range(a + 1, a + span)]
        mid = (N - span) / 2.0
        row.sort(key=lambda t: (abs(t[0] - mid), t[0], t[1]))
        for t in row:
            if t not in seen and sigma(N, t) != t:
                rest.append(t)
                seen.add(t)
    return short + rest


def ear_semantic(N, A):
    """ear(0), ear(1), ear(N-1) and hull flags computed from an orientation dict A (for tests)."""
    hull = [i for i in range(1, N) if all(A[(a, i, c)] for a in range(1, i) for c in range(i + 1, N))]
    e0 = sum(1 for b in range(2, N - 1) if not A[(1, b, N - 1)])
    h2 = min(i for i in hull if i > 1)
    hp = max(i for i in hull if i < N - 1)
    return e0, h2 - 2, N - 2 - hp, hull


def lex_ok(N, A, mode):
    for t in reflect_order(N, mode):
        x, y = A[t], A[sigma(N, t)]
        if x != y:
            return (not x) and y
    return True


def add(N, var, aux, clauses, nv, reflect=None, ear=False):
    """Append the (R) and/or (E) clauses; returns the new variable count."""
    X = lambda t: var[t]

    def new(key):
        nonlocal nv
        nv += 1
        aux[key] = nv
        return nv

    if reflect:
        V = reflect_order(N, reflect)
        prev = None  # e_0 = true
        for i, t in enumerate(V):
            x, y = X(t), X(sigma(N, t))
            pre = [] if prev is None else [-prev]
            clauses.append(pre + [-x, y])
            if i + 1 < len(V):
                e = new(('LEX', i + 1))
                clauses.append(pre + [-x, -y, e])
                clauses.append(pre + [x, y, e])
                prev = e
    if ear:
        H = {}
        for i in range(2, N - 1):
            H[i] = new(('HULL', i))
            clauses.append([-X((a, i, c)) for a in range(1, i) for c in range(i + 1, N)] + [H[i]])
        lits = [-X((1, b, N - 1)) for b in range(2, N - 1)]
        m = len(lits)
        # sequential counter, S[j][t] <- at least t of lits[0..j]
        S = {}
        for j in range(m):
            for t in range(1, j + 2):
                S[j, t] = new(('CNT', j, t))
                clauses.append([-lits[j], S[j, t]] if t == 1 else [-lits[j], -S[j - 1, t - 1], S[j, t]])
                if j > 0 and t <= j:
                    clauses.append([-S[j - 1, t], S[j, t]])
        G = lambda t: S[m - 1, t] if 1 <= t <= m else None
        for i in range(2, N - 1):
            for t in (i - 1, N - 1 - i):
                g = G(t)
                if g is not None:
                    clauses.append([-H[i], -g])
    return nv
