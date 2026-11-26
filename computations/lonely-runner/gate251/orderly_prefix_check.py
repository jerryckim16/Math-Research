"""Sampled check of the orderly-root rule at a large prime (gate251), in
independent Python.

covergen with LRC_ORDERLY=1 explores the same tree as with LRC_ORDERLY=0
(same child order, same exclusions of earlier siblings), minus the subtrees
cut by Lemma B.1 and the leaves rejected by the canonical test.  So within a
root branch the orderly output is exactly the subsequence of the
non-orderly output made of the canonical covers, in the same order.

Canonical (Toner, Lemma B.1, as implemented in covergen.c): with the root
candidate list R = (r_0, r_1, ...) and rho(S) = least i with r_i in S, a cover
T (which contains class 1) is canonical iff (rho(T), sorted T) is
lexicographically <= (rho(s^-1 T), sorted s^-1 T) for every s in T
(classes folded to 1..(p-1)/2).

This script recomputes the test from scratch on a prefix of the non-orderly
output of one root branch and compares the canonical subsequence with the
prefix of the orderly output of the same branch.

usage: python3 -I orderly_prefix_check.py p "r_0 r_1 ..." NONORDERLY_PREFIX ORDERLY_FILE
"""
import sys


def main():
    p = int(sys.argv[1])
    R = [int(x) for x in sys.argv[2].split()]
    idx = {c: i for i, c in enumerate(R)}
    fold = lambda x: min(x % p, p - x % p)
    inv = lambda s: pow(s, p - 2, p)
    rho = lambda S: min((idx[c] for c in S if c in idx), default=10 ** 9)

    def canonical(T):
        S = tuple(sorted(T))
        me = (rho(S), S)
        for s in S:
            si = inv(s)
            U = tuple(sorted(fold(t * si) for t in S))
            if (rho(U), U) < me:
                return False
        return True

    non = [tuple(map(int, l.split())) for l in open(sys.argv[3]) if l.strip() and l.endswith("\n")]
    filt = [T for T in non if canonical(T)]
    orde = [tuple(map(int, l.split())) for l in open(sys.argv[4]) if l.strip() and l.endswith("\n")]
    m = min(len(filt), len(orde))
    ok = filt[:m] == orde[:m] and m == len(filt)
    print(f"non-orderly prefix {len(non)} covers, canonical {len(filt)}, orderly prefix {len(orde)}; "
          f"{'EQUAL' if ok else 'MISMATCH'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
