"""Orderly-rule check at k = 17 (and any k): the set of unit-orbit canonical
forms of the covers from an LRC_ORDERLY=1 run must equal the set of distinct
canonical forms of the covers from an LRC_ORDERLY=0 run (all minimal covers
containing class 1), and the orderly run must contain no two covers in the
same orbit.  Canonical form of a cover S: min over units a in 1..(p-1)/2 of
sorted(fold(a s)), fold(x) = min(x mod p, p - x mod p).

usage: python3 orbit_check.py p ORDERLY_FILE FULL_FILE
"""
import sys


def canon(S, p):
    h = (p - 1) // 2
    best = None
    for a in range(1, h + 1):
        t = tuple(sorted(min(a * s % p, p - a * s % p) for s in S))
        if best is None or t < best:
            best = t
    return best


def main():
    p = int(sys.argv[1])
    orderly = [tuple(map(int, l.split())) for l in open(sys.argv[2]) if l.strip()]
    co = [canon(S, p) for S in orderly]
    so = set(co)
    full = set(canon(tuple(map(int, l.split())), p) for l in open(sys.argv[3]) if l.strip())
    print("orderly covers", len(orderly), "distinct orbits among them", len(so), "full-run orbits", len(full))
    ok = len(so) == len(orderly) and so == full
    print("ORBIT SETS EQUAL, one cover per orbit" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
