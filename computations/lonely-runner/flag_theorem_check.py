"""Machine checks for the general-n parts of Allikvere's flag bound
(arXiv:2609.02604v2, Section 3: Lemma 3.1 Inclusion, Lemma 3.2 Covolume,
Lemma 3.6 Product minimization, and the assembly in Theorem 3.8; Lemma 3.3,
Proposition 3.4 and Lemma 3.5 have no finite component and are checked by
reading).  The written
verification is in problems/lonely-runner.md, Approach 11.

What is checked here (all exact rational arithmetic unless marked float):

  inclusion   The algebraic reduction at the vertices of {y in H : |y|_1 <= 1}
              is a polynomial identity; and h_E(y)^2 = sum q_i y_i^2 <=
              (sum |y_i|)^2 = h_D(y)^2 at random rational y in H (sample check
              of the conclusion, not a proof).
  covolume    For random primitive v (n = 3..6): an exact Z-basis of
              Lambda = P Z^n (Hermite form), its Euclidean Gram determinant
              equals 1/|v|^2, and its Gram determinant in the E inner product
              equals 1/(S F_n(x))^2.  The E inner product on H is computed
              from its definition (E is the unit ball; gauge of P Q^(1/2) B):
              <y,y'>_E = y^T M y', M = Q^-1 - Q^-1 v v^T Q^-1 / (v^T Q^-1 v).
  minimize    The product-minimization lemma for the actual constants B_r of
              each n: (a) brute-force vertex enumeration of the polyhedron
              Pi (all d-subsets of the 2d-1 constraints) for d <= 7, checking
              every vertex is a 'block' point and has prod t >= prod c;
              (b) for d = 12, 13, 14 (n = 13, 14, 15) all 2^(d-1) block
              points are feasible and have prod t >= prod c, equality only
              at t = c; (c, float) random feasible points.
  assembly    ln bound for n = 15, r = 49/100 to 30 digits (Decimal).
"""
import random
from decimal import Decimal, getcontext
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd


# ------------------------------------------------------------ linear algebra
def det(M):
    M = [list(map(Fr, r)) for r in M]
    n, d = len(M), Fr(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fr(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return d


def solve(A, b):
    """Exact solve A x = b (square, nonsingular) or None."""
    n = len(A)
    M = [list(map(Fr, A[i])) + [Fr(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * x for a, x in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def int_row_basis(rows):
    """Z-basis (echelon form) of the Z-span of integer row vectors."""
    rows = [list(r) for r in rows if any(r)]
    basis = []
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = [r for r in rows if r[c] != 0]
        rest = [r for r in rows if r[c] == 0]
        while len(piv) > 1:
            piv.sort(key=lambda r: abs(r[c]))
            a = piv[0]
            new = [a]
            for r in piv[1:]:
                q = r[c] // a[c]
                r2 = [x - q * y for x, y in zip(r, a)]
                if not any(r2):
                    continue
                if r2[c] != 0:
                    new.append(r2)
                else:
                    rest.append(r2)
            piv = new
        if piv:
            basis.append(piv[0])
        rows = rest
    return basis


# ------------------------------------------------------------------ setting
def setting(v):
    """S, x, u, q for a positive integer vector v (paper's notation)."""
    S = sum(v)
    M = max(v)
    x = [Fr(a, S) for a in v]
    u = [Fr(a, M) for a in v]
    q = [1 + 2 * a - a * a for a in u]
    return S, x, u, q


def F2(v):
    S, x, u, q = setting(v)
    p = Fr(1)
    for a in q:
        p *= a
    return p * sum(a * a / b for a, b in zip(x, q))


# ---------------------------------------------------------------- inclusion
def check_inclusion_identity(trials=200, seed=1):
    """(q_i-1) v_j^2 + (q_j-1) v_i^2 - 2 v_i v_j = -2 M^2 u_i u_j (1-u_i)(1-u_j)
    with q-1 = u(2-u), v = M u, at random rationals (a polynomial identity of
    degree <= 4 in (u_i, u_j); 200 random points)."""
    rng = random.Random(seed)
    for _ in range(trials):
        M = Fr(rng.randint(1, 50))
        ui, uj = Fr(rng.randint(1, 99), 100), Fr(rng.randint(1, 99), 100)
        vi, vj = M * ui, M * uj
        qi, qj = 1 + 2 * ui - ui * ui, 1 + 2 * uj - uj * uj
        lhs = (qi - 1) * vj ** 2 + (qj - 1) * vi ** 2 - 2 * vi * vj
        if lhs != -2 * M * M * ui * uj * (1 - ui) * (1 - uj):
            return False
    return True


def check_inclusion_vertices(v):
    """At every edge point y = (v_j e_i - v_i e_j)/(v_i + v_j) (i != j) of the
    cross-polytope meeting H: y in H, |y|_1 = 1 and sum q y^2 <= 1."""
    S, x, u, q = setting(v)
    n = len(v)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            y = [Fr(0)] * n
            y[i], y[j] = Fr(v[j], v[i] + v[j]), Fr(-v[i], v[i] + v[j])
            if sum(a * b for a, b in zip(v, y)) != 0 or sum(abs(a) for a in y) != 1:
                return False
            if sum(qq * a * a for qq, a in zip(q, y)) > 1:
                return False
    return True


def check_inclusion_samples(v, trials=200, seed=2):
    """Exact: random rational y in H satisfy sum q y^2 <= (sum |y|)^2."""
    S, x, u, q = setting(v)
    n = len(v)
    rng = random.Random(seed)
    nv = sum(a * a for a in v)
    for _ in range(trials):
        z = [Fr(rng.randint(-100, 100)) for _ in range(n)]
        pz = sum(a * b for a, b in zip(v, z))
        y = [a - Fr(pz, nv) * b for a, b in zip(z, v)]   # P z
        if sum(qq * a * a for qq, a in zip(q, y)) > sum(abs(a) for a in y) ** 2:
            return False
    return True


# ---------------------------------------------------------------- covolume
def lattice_basis(v):
    """Exact Z-basis of Lambda = P Z^n (rank n-1): Lambda = (1/N) L with
    N = |v|^2 and L = Z-span{N e_i - v_i v}."""
    n, N = len(v), sum(a * a for a in v)
    rows = [[N * (i == k) - v[i] * v[k] for k in range(n)] for i in range(n)]
    B = int_row_basis(rows)
    assert len(B) == n - 1
    return [[Fr(a, N) for a in r] for r in B]


def E_form(v):
    """Matrix M with ||y||_E^2 = y^T M y on H (gauge of E = P Q^(1/2) B_2^n):
    min |z|^2 over Q^(1/2) z = y + lambda v."""
    S, x, u, q = setting(v)
    n = len(v)
    qi = [1 / a for a in q]
    s = sum(qi[k] * v[k] * v[k] for k in range(n))
    return [[(qi[i] if i == j else 0) - qi[i] * v[i] * qi[j] * v[j] / s for j in range(n)] for i in range(n)]


def check_covolume(v):
    B = lattice_basis(v)
    n = len(v)
    G_euc = [[sum(a * b for a, b in zip(r, s)) for s in B] for r in B]
    M = E_form(v)
    G_E = [[sum(r[i] * M[i][j] * s[j] for i in range(n) for j in range(n)) for s in B] for r in B]
    S = sum(v)
    ok_euc = det(G_euc) == Fr(1, sum(a * a for a in v))
    ok_E = det(G_E) == 1 / (S * S * F2(v))
    return ok_euc and ok_E


def random_primitive(n, rng, hi=40):
    while True:
        v = sorted(rng.sample(range(1, hi), n))
        g = 0
        for a in v:
            g = gcd(g, a)
        if g == 1:
            return v


# ---------------------------------------------------------- minimization
def prefix_B(n):
    return [Fr(0)] + [Fr(2 * r, (n + 1) * (n + 1 - r)) ** 2 for r in range(1, n)]


RHO = Fr(3, 4)


def constraints(n):
    """Pi in z-coordinates (z_i = t_i / rho^(i-1)), d = n-1: rows (a, b) for
    a.z >= b.  Monotonicity z_{i+1} - z_i >= 0 (d-1 rows), prefixes
    sum_{i<=r} w_i z_i >= B_r (d rows)."""
    d = n - 1
    B = prefix_B(n)
    w = [RHO ** i for i in range(d)]
    rows = []
    for i in range(d - 1):
        a = [Fr(0)] * d
        a[i], a[i + 1] = Fr(-1), Fr(1)
        rows.append((a, Fr(0), ("mono", i)))
    for r in range(1, d + 1):
        rows.append(([w[i] if i < r else Fr(0) for i in range(d)], B[r], ("prefix", r)))
    return rows, w


def block_point(n, ends):
    """t for blocks ending at 'ends' (sorted, last = d): on block (a,b], t_i =
    w_i zeta with sum = B_b - B_a."""
    d = n - 1
    B = prefix_B(n)
    w = [RHO ** i for i in range(d)]
    z = [None] * d
    a = 0
    for b in ends:
        zeta = (B[b] - B[a]) / sum(w[a:b])
        for i in range(a, b):
            z[i] = zeta
        a = b
    return [w[i] * z[i] for i in range(d)], z


def prodc(n):
    B = prefix_B(n)
    p = Fr(1)
    for i in range(1, n):
        p *= B[i] - B[i - 1]
    return p


def feasible_t(n, t):
    d = n - 1
    B = prefix_B(n)
    if any(x <= 0 for x in t):
        return False
    if any(t[i + 1] < RHO * t[i] for i in range(d - 1)):
        return False
    s = Fr(0)
    for r in range(1, d + 1):
        s += t[r - 1]
        if s < B[r]:
            return False
    return True


def prod(xs):
    p = Fr(1)
    for x in xs:
        p *= x
    return p


def check_block_points(n):
    """All 2^(d-1) block points: feasible, prod t >= prod c, equality only
    for all-singleton blocks (t = c)."""
    d = n - 1
    K = prodc(n)
    for mask in range(2 ** (d - 1)):
        ends = [i + 1 for i in range(d - 1) if mask >> i & 1] + [d]
        t, _ = block_point(n, ends)
        if not feasible_t(n, t):
            return False, ends
        P = prod(t)
        if P < K or (P == K and len(ends) != d):
            return False, ends
    return True, None


def check_vertices_bruteforce(n):
    """d <= 7: every vertex of Pi (d linearly independent active constraints,
    feasible) is a block point with all block ends active and prod >= prod c."""
    d = n - 1
    rows, w = constraints(n)
    K = prodc(n)
    seen = set()
    for S in combinations(range(len(rows)), d):
        A = [rows[k][0] for k in S]
        b = [rows[k][1] for k in S]
        if det(A) == 0:
            continue
        z = solve(A, b)
        if any(sum(a * x for a, x in zip(r[0], z)) < r[1] for r in rows):
            continue
        key = tuple(z)
        if key in seen:
            continue
        seen.add(key)
        t = [w[i] * z[i] for i in range(d)]
        if prod(t) < K:
            return False, z
        # block structure: blocks = maximal runs of equal z; all ends active
        ends = [i + 1 for i in range(d - 1) if z[i] != z[i + 1]] + [d]
        t2, _ = block_point(n, ends)
        if t2 != t:
            return False, z
    return True, len(seen)


def check_random_feasible(n, trials=2000, seed=3):
    """Float sanity: random t with t_{i+1} >= rho t_i, scaled up until all
    prefix constraints hold; prod t >= prod c."""
    rng = random.Random(seed)
    d = n - 1
    B = [float(b) for b in prefix_B(n)]
    K = float(prodc(n))
    for _ in range(trials):
        t = [rng.uniform(0.5, 2)]
        for i in range(d - 1):
            t.append(t[-1] * rng.uniform(0.75, 2))
        s, lam = 0.0, 0.0
        for r in range(1, d + 1):
            s += t[r - 1]
            lam = max(lam, B[r] / s)
        t = [x * lam for x in t]
        p = 1.0
        for x in t:
            p *= x
        if p < K * (1 - 1e-9):
            return False
    return True


# ------------------------------------------------------------------ assembly
def log_bound_decimal(n, r, digits=40):
    getcontext().prec = digits
    K = prodc(n)
    lnK = Decimal(K.numerator).ln() - Decimal(K.denominator).ln()
    return n * (-lnK / 2 + Decimal(r.numerator).ln() - Decimal(r.denominator).ln() - Decimal(n).ln())


def ln_lcm(m):
    from math import lcm
    L = 1
    for i in range(2, m + 1):
        L = lcm(L, i)
    return Decimal(L).ln()


if __name__ == "__main__":
    rng = random.Random(0)
    print("inclusion identity:", check_inclusion_identity())
    vs = [random_primitive(n, rng) for n in (3, 4, 5, 6) for _ in range(5)]
    print("inclusion vertices:", all(check_inclusion_vertices(v) for v in vs))
    print("inclusion samples :", all(check_inclusion_samples(v) for v in vs))
    print("covolume          :", all(check_covolume(v) for v in vs))
    for n in range(3, 9):
        print(f"minimize n={n}: vertices brute force {check_vertices_bruteforce(n)}")
    for n in (13, 14, 15):
        print(f"minimize n={n}: block points {check_block_points(n)}, random feasible {check_random_feasible(n)}")
    lb = log_bound_decimal(15, Fr(49, 100))
    print("n=15 ln bound:", lb, " target:", lb - ln_lcm(16))
