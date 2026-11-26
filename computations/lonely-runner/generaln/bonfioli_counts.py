"""Re-count two numbers quoted in Bonfioli's dense-window manuscript
(Zenodo 24189338 v1.6.0, paper/dense-window/main.tex, Section 3, paragraphs
"Primality" and the unnumbered case table), for composite N = 2m+1.

  A(m) = #{V subset [1,2m], |V| <= m : V contains a, b with a + b = N,
           and no c in 1..N-1 makes c/N a witness at threshold 1/(m+1)}
  C(m) = #{V : 1 in V, every q in [2, m+1] divides an element of V
           ("case 3"), and no c/N witness}
The manuscript gives 32, 544, 368 for m = 7, 10, 12 (both readings).
Usage: python3 bonfioli_counts.py 7 10
"""
import sys
from itertools import combinations


def counts(m):
    N = 2 * m + 1
    K = m + 1
    good_c = {}  # x -> bitmask of c with x*c mod N not bad
    for x in range(1, 2 * m + 1):
        mask = 0
        for c in range(1, N):
            r = x * c % N
            if K * min(r, N - r) >= N:
                mask |= 1 << c
        good_c[x] = mask
    full = sum(1 << c for c in range(1, N))
    A = C = 0
    for k in range(1, m + 1):
        for V in combinations(range(1, 2 * m + 1), k):
            S = set(V)
            mask = full
            for x in V:
                mask &= good_c[x]
            if mask:
                continue  # some c/N is a witness
            if any(N - x in S for x in V):
                A += 1
            if 1 in S and all(any(x % q == 0 for x in V) for q in range(2, m + 2)):
                C += 1
    return A, C


if __name__ == "__main__":
    for m in map(int, sys.argv[1:]):
        print(m, 2 * m + 1, "pair-sets without c/N witness, case-3 sets without c/N witness:", counts(m), flush=True)
