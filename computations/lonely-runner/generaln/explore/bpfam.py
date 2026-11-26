"""Which max speeds M are handled by divisibility + Bohman-Peng pair witnesses alone?
For n speeds with max exactly M (M in V, V in [1,M]), family:
  D_q = multiples of q in [1,M], 2<=q<=n+1
  P_{N,s} = {s, N-s} cap [1,M], M < N <= 2n+2, gcd(s,N)=1, 1<=s<=N/2
V (|V|<=n, M in V) must hit all.  Report transversals."""
import sys
from math import gcd
sys.setrecursionlimit(10000)


def fam(n, M, extra=()):
    F = set()
    for q in range(2, n + 2):
        F.add(frozenset(range(q, M + 1, q)))
    for N in range(M + 1, 2 * n + 3):
        for s in range(1, N // 2 + 1):
            if gcd(s, N) == 1:
                F.add(frozenset(x for x in (s, N - s) if x <= M))
    for B in extra:
        F.add(frozenset(B))
    F = [B for B in F]
    F.sort(key=len)
    return [B for B in F if not any(C < B for C in F)]


def transversals(F, n, M, cap=5):
    out = []

    def dfs(T, forb):
        if len(out) >= cap:
            return
        best = None
        for B in F:
            if B & T:
                continue
            avail = B - forb
            if best is None or len(avail) < len(best):
                best = avail
                if len(avail) <= 1:
                    break
        if best is None:
            out.append(sorted(T))
            return
        if len(T) == n:
            return
        f = set(forb)
        for x in sorted(best):
            dfs(T | {x}, frozenset(f))
            f.add(x)
    if any(len(B) == 0 for B in F):
        return out
    dfs(frozenset([M]), frozenset())
    return out


if __name__ == "__main__":
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        bad = []
        for M in range(n + 1, 2 * n + 1):
            T = transversals(fam(n, M), n, M, cap=1)
            if T:
                bad.append(M)
        first = bad[0] if bad else None
        print(n, "first M with transversal:", first, "ratio", None if first is None else round(first / n, 3), "4n/3=", round(4 * n / 3, 2), "bad Ms:", bad[:12], flush=True)
