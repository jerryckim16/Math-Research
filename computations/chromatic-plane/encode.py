"""CNF encoding of "graph G is k-colourable", with clique symmetry breaking.

Variables: x(v, c) = v*k + c + 1 for vertex v in [0, n) and colour c in [0, k).
Clauses:
  (1) at least one colour per vertex:   x(v,0) v ... v x(v,k-1)
  (2) edge constraint, per edge uv and colour c:  -x(u,c) v -x(v,c)
  (3) symmetry breaking: for a clique (q_0, ..., q_{m-1}) of G with m <= k,
      unit clauses x(q_i, i).

Soundness (G properly k-colourable  =>  CNF satisfiable):
  Let col : V -> [0,k) be a proper colouring. The clique vertices receive
  pairwise distinct colours (they are pairwise adjacent), so there is a
  permutation pi of [0,k) with pi(col(q_i)) = i for all i < m (extend the
  injective partial map i |-> col(q_i) inverse to a bijection). pi o col is
  again proper. Set x(v,c) true iff c = pi(col(v)). Then (1) holds, (2) holds
  because adjacent vertices get distinct colours, and (3) holds by choice of
  pi. No at-most-one clauses are used, so nothing else must be satisfied.
Hence UNSAT  =>  G is not k-colourable. (The converse direction is not
needed; a satisfying assignment still yields a colouring by picking any true
colour per vertex.)

Usage: python3 encode.py is a library; see run_pipeline.py.
"""


def var(v, c, k):
    return v * k + c + 1


def colouring_cnf(n, edges, k, clique=()):
    if len(clique) > k:
        raise ValueError("clique larger than k: trivially non-colourable")
    clauses = []
    for v in range(n):
        clauses.append([var(v, c, k) for c in range(k)])
    for u, v in edges:
        if u == v:
            raise ValueError("loop")
        for c in range(k):
            clauses.append([-var(u, c, k), -var(v, c, k)])
    for i, q in enumerate(clique):
        clauses.append([var(q, i, k)])
    return n * k, clauses


def is_clique(edges, clique):
    es = {frozenset(e) for e in edges}
    return all(frozenset((a, b)) in es
               for i, a in enumerate(clique) for b in clique[i + 1:])


def write_dimacs(path, nvars, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")


def decode(model, n, k):
    """model: set of true literals. Returns a colour per vertex."""
    col = []
    for v in range(n):
        cs = [c for c in range(k) if var(v, c, k) in model]
        col.append(cs[0])
    return col


def is_proper(edges, col):
    return all(col[u] != col[v] for u, v in edges)
