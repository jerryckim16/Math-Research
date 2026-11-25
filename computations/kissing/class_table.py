"""Exact class-threshold table for kiss_check.c / kiss_check_np.py class mode.

Setting. Every point is x_r = (L u_r, w_c) in R^(d_b + d_h), with u_r an
integer "body" row (stored in BODY.i8), c = c(r) its class, L > 0 an integer
common to all rows, and w_c an integer vector shared by the class, whose
body norm n_c = |u_r|^2 is also fixed per class. Then exactly
    p   = x_r . x_s = L^2 t + beta,   t = u_r . u_s,  beta = w_c . w_c',
    N_c = |x_r|^2  = L^2 n_c + |w_c|^2,
and the kissing condition p <= 0 or 4 p^2 <= N_c N_c' is equivalent to
2p <= sqrt(N_c N_c'), i.e. (p and 2p integers) p <= Q := isqrt(N_c N_c') // 2.
As p is increasing in t, the pair passes iff
    t <= T(c, c') := floor((Q - beta) / L^2),
and it is an exact 60-degree contact iff 4 Q^2 = N_c N_c', Q > 0, and
t = (Q - beta) / L^2 is an integer (then C(c, c') = that t).
All of this is Python integer arithmetic. Since |t| <= B := max body norm,
T is clamped to [-B-1, B+1] and an unreachable C is written as 32767 (> B);
this changes no outcome. The checkers then only evaluate the integer t.

Input CLASSES.json: {"L": L, "classes": [{"w": [...], "body_norm": n}, ...]}.
Output TABLE.txt: "k", then k*k lines "a b T C".
Usage: python3 -I class_table.py CLASSES.json TABLE.txt
"""
import json
import math
import sys


def table(L, classes):
    assert type(L) is int and L > 0 and 1 <= len(classes) <= 256
    W = [[int(x) for x in c["w"]] for c in classes]
    nb = [int(c["body_norm"]) for c in classes]
    assert all(n >= 0 for n in nb)
    B = max(nb)
    assert B < 32767
    N = [L * L * n + sum(x * x for x in w) for n, w in zip(nb, W)]
    assert all(v > 0 for v in N)
    out = {}
    for a in range(len(classes)):
        for b in range(len(classes)):
            beta = sum(x * y for x, y in zip(W[a], W[b]))
            Q = math.isqrt(N[a] * N[b]) // 2
            T = (Q - beta) // (L * L)
            # sanity: T is the largest passing t
            for t, ok in ((T, True), (T + 1, False)):
                p = L * L * t + beta
                assert (p <= 0 or 4 * p * p <= N[a] * N[b]) == ok
            C = 32767
            if 4 * Q * Q == N[a] * N[b] and Q > 0 and (Q - beta) % (L * L) == 0:
                C = (Q - beta) // (L * L)
                assert C == T
            if not -B <= C <= B:
                C = 32767
            out[a, b] = (max(-B - 1, min(B + 1, T)), C)
    return out


def main(src, dst):
    c = json.load(open(src))
    t = table(c["L"], c["classes"])
    k = len(c["classes"])
    with open(dst, "w") as f:
        f.write(f"{k}\n")
        for (a, b), (T, C) in sorted(t.items()):
            f.write(f"{a} {b} {T} {C}\n")
    print(f"{k} classes, L = {c['L']}: table -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
