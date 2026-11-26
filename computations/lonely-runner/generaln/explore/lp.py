import sys
from math import gcd
import numpy as np
from scipy.optimize import linprog


def bad(m, a, q):
    K = m + 1
    return frozenset(x for x in range(1, 2 * m + 1) if K * min(x * a % q, q - x * a % q) < q)


def family(m, Q):
    S = set()
    for q in range(2, Q + 1):
        for a in range(1, q // 2 + 1):
            if gcd(a, q) == 1:
                S.add(bad(m, a, q))
    S = list(S)
    S.sort(key=len)
    return [B for B in S if not any(C < B for C in S)]


def tau(m, F):
    n = 2 * m
    A = np.zeros((len(F), n))
    for i, B in enumerate(F):
        for x in B:
            A[i, x - 1] = 1
    r = linprog(np.ones(n), A_ub=-A, b_ub=-np.ones(len(F)), bounds=(0, None), method='highs')
    return r.fun, r.x


if __name__ == "__main__":
    for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        Q = int(eval(sys.argv[3]))
        F = family(m, Q)
        N = 2 * m + 1
        t, z = tau(m, F)
        pr = "prime" if all(N % d for d in range(2, int(N ** .5) + 1)) else "comp"
        print(m, N, pr, len(F), round(t, 4), round(t - m, 4), flush=True)
