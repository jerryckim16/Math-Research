"""Independent checker for matchcrit certificates (Lemma C of
notes/lonely-runner/general-n-explicit.md).  Shares no code with matchcrit.c.

A certificate for (n, M), n+1 <= M <= 2n, lists pairs "s t" for every
s in [1, floor(M/2)].  It is valid iff
  * the t are distinct and lie in [n+2, 2n+2];
  * each pair is an edge: gcd(s,t) = 1 and M < s+t <= 2n+2, or
    t = 2s with s >= 2 and 3s > M.
Usage: matchcrit cert n M | python3 check_matching.py
"""
import sys
from math import gcd


def valid_edge(n, M, s, t):
    if gcd(s, t) == 1 and M < s + t <= 2 * n + 2:
        return True
    return t == 2 * s and s >= 2 and 3 * s > M


def check_certificate(n, M, pairs):
    """pairs: dict s -> t.  Returns (ok, reason)."""
    if not (n + 1 <= M <= 2 * n):
        return False, "M out of range"
    A = M // 2
    seen = set()
    for s in range(1, A + 1):
        if s not in pairs:
            return False, "s=%d unmatched" % s
        t = pairs[s]
        if not (n + 2 <= t <= 2 * n + 2):
            return False, "t=%d out of range" % t
        if t in seen:
            return False, "t=%d used twice" % t
        seen.add(t)
        if not valid_edge(n, M, s, t):
            return False, "(%d,%d) is not an edge" % (s, t)
    return True, "ok"


def parse(text):
    n = M = None
    pairs = {}
    for line in text.splitlines():
        if line.startswith("#"):
            for tok in line[1:].split():
                k, v = tok.split("=")
                if k == "n":
                    n = int(v)
                elif k == "M":
                    M = int(v)
            continue
        if line.strip():
            s, t = map(int, line.split())
            if t >= 0:
                pairs[s] = t
    return n, M, pairs


if __name__ == "__main__":
    n, M, pairs = parse(sys.stdin.read())
    ok, why = check_certificate(n, M, pairs)
    print(n, M, "VALID" if ok else "INVALID: " + why)
    sys.exit(0 if ok else 1)
