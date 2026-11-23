"""Prime-gate sieve for the Lonely Runner Conjecture (Rosenfeld /
Trakulthongchai / Sungkawichai-Trakulthongchai framework), in exact
integer arithmetic with Python big-int bitsets.

Definitions (Trakulthongchai, Def. 3; as restated in Sungkawichai &
Trakulthongchai, arXiv:2604.23906, Def. 2.1).  Fix k >= 2, a prime p and
l >= 1; put N = l*p and Z_{p,l} = {x in Z_N : x != 0 mod p}.  A tuple
w in Z_{p,l}^k is (k,p,l)-PROPER if
  (a) some i has gcd(l, w_1, ..., w_{i-1}, w_{i+1}, ..., w_k) > 1, or
  (b) some t in (1/N)Z has ||t w_i|| >= 1/(k+1) for all i.
I(k,p,l) = the improper tuples.  J(k,p) = the tuples of Z_{p,1}^k that are
not "eventually proper" (Def. 2.3 there).

Facts used (all elementary; proofs in problems/lonely-runner.md):
  F1  If w is improper at level clp, its reduction mod lp is improper at
      level lp.  Hence J(k,p) is contained in pi_p(S) for every S built by
      starting from I(k,p,1) and repeatedly replacing S by its improper
      lifts (lifting by c) or by its reduction mod p.  (This is the
      lifting/projection Prop. 3.1 of arXiv:2604.23906.)
  F2  Properness is invariant under permutations, coordinate negation and
      multiplication by a unit of Z_N.  So it is enough to keep one
      representative per orbit; every orbit member at level N lifts to
      level cN through a unit lift of the group element (Z_{cN}^* -> Z_N^*
      is onto).
So if the chain ends with an empty set, J(k,p) is empty.

Then (Lemma 2.2 / Cor. 2.4 there): if LRC(k-1) holds and J(k,p) is empty,
p divides u_1...u_k for every counterexample u to LRC(k).  Combined with
the Malikiosis-Santos-Schymura bound in the form of Rosenfeld's Cor. 3
(any gcd-1 counterexample has u_1...u_k < B_k = (C(k+1,2)^(k-1)/k)^k),
a set of primes P with J(k,p) empty for p in P and prod P >= B_k proves
LRC(k) (Prop. 2.6 there).
"""

import sys
import time
from math import comb, gcd, prod


def good_mask(a, N, k):
    """Bitset over m in [0, N) of times t = m/N with ||a m / N|| >= 1/(k+1)."""
    bits = 0
    for m in range(N):
        r = (a * m) % N
        if (k + 1) * min(r, N - r) >= N:
            bits |= 1 << m
    return bits


class Level:
    """Cached masks for modulus N = l*p."""

    def __init__(self, k, p, l):
        self.k, self.p, self.l, self.N = k, p, l, l * p
        self._m = {}
        self.units = [a for a in range(1, self.N) if gcd(a, self.N) == 1]

    def mask(self, a):
        a %= self.N
        m = self._m.get(a)
        if m is None:
            m = good_mask(a, self.N, self.k)
            self._m[a] = m
        return m

    def has_witness(self, w):
        acc = (1 << self.N) - 1
        for x in w:
            acc &= self.mask(x)
            if not acc:
                return False
        return True

    def gcd_condition(self, w):
        if self.l == 1:
            return False
        k = len(w)
        for i in range(k):
            g = self.l
            for j in range(k):
                if j != i:
                    g = gcd(g, w[j])
            if g > 1:
                return True
        return False

    def is_proper(self, w):
        return self.gcd_condition(w) or self.has_witness(w)

    def canon(self, w):
        """Orbit representative under units, signs and permutations."""
        N = self.N
        best = None
        for a in self.units:
            t = tuple(sorted(min((a * x) % N, N - (a * x) % N) for x in w))
            if best is None or t < best:
                best = t
        return best


def level1_improper(k, p):
    """Orbit representatives of I(k,p,1).

    Every orbit of Z_{p,1}^k contains a tuple (1, a_2, ..., a_k) with
    1 <= a_2 <= ... <= a_k <= (p-1)/2: scale by the inverse of v_1, fold
    signs, sort the rest.  DFS with an AND of good-time bitsets.  Returned
    tuples are canonicalised and de-duplicated.
    """
    L = Level(k, p, 1)
    h = (p - 1) // 2
    masks = [0] + [L.mask(a) for a in range(1, h + 1)]
    out = set()
    cnt = 0

    def dfs(prefix, start, acc):
        nonlocal cnt
        if len(prefix) == k:
            cnt += 1
            if acc == 0:
                out.add(L.canon(prefix))
            return
        for a in range(start, h + 1):
            dfs(prefix + [a], a, acc & masks[a])

    dfs([1], 1, masks[1])
    return sorted(out), cnt


def lift(S, k, p, l, c):
    """Improper lifts (orbit reps at level c*l) of the reps S at level l."""
    lo = Level(k, p, l)
    hi = Level(k, p, c * l)
    N = lo.N
    out = set()
    checked = 0
    for v in S:
        # all c^k lifts w_i = v_i + j_i N
        lifts = [[]]
        for x in v:
            lifts = [w + [x + j * N] for w in lifts for j in range(c)]
        for w in lifts:
            checked += 1
            if not hi.is_proper(w):
                out.add(hi.canon(w))
    return sorted(out), checked


def project(S, k, p):
    """Reduce reps mod p and canonicalise at level 1."""
    L = Level(k, p, 1)
    return sorted({L.canon([x % p for x in v]) for v in S})


def run_gate(k, p, chain, log=None):
    """Run the sieve chain at prime p.  chain: list of ints c (lift by c) or
    'p' (project to level 1).  Returns (J_empty, trace)."""
    t0 = time.time()
    eng = {"py": "level1_improper", "c": "level1_improper_c",
           "cover": "level1_improper_covers"}[LEVEL1_ENGINE]
    S, cnt = globals()[eng](k, p)
    trace = [("I1", 1, len(S), cnt, round(time.time() - t0, 3))]
    l = 1
    for op in chain:
        if not S:
            break
        t1 = time.time()
        if op == "p":
            S = project(S, k, p)
            l = 1
            trace.append(("proj", l, len(S), len(S), round(time.time() - t1, 3)))
        else:
            S, checked = lift(S, k, p, l, op)
            l *= op
            trace.append(("x%d" % op, l, len(S), checked, round(time.time() - t1, 3)))
        if log:
            log(trace[-1])
    return (len(S) == 0), trace, S


def B_bound_ok(k, primes):
    """Exact test of prod(primes) >= B_k = (C(k+1,2)^(k-1)/k)^k,
    i.e. prod(primes) * k^k >= C(k+1,2)^(k(k-1))."""
    return prod(primes) * k ** k >= comb(k + 1, 2) ** (k * (k - 1))


def log_B(k):
    from math import log
    return k * ((k - 1) * log(comb(k + 1, 2)) - log(k))


# ---------------------------------------------------------------------------
# Optional C engine for the level-1 step (same enumeration, same test).
# Built on demand into a temporary directory; cross-checked against the
# Python level1_improper in test_sieve.py.

import os
import subprocess
import tempfile

_LEVEL1_BIN = None


def _level1_bin():
    global _LEVEL1_BIN
    if _LEVEL1_BIN is None:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "level1.c")
        out = os.path.join(tempfile.mkdtemp(prefix="lrc_"), "level1")
        subprocess.run(["cc", "-O2", "-o", out, src], check=True)
        _LEVEL1_BIN = out
    return _LEVEL1_BIN


def level1_improper_c(k, p):
    res = subprocess.run([_level1_bin(), str(k), str(p)], check=True,
                         capture_output=True, text=True)
    L = Level(k, p, 1)
    out = {L.canon([int(x) for x in line.split()])
           for line in res.stdout.splitlines() if line.strip()}
    cnt = int(res.stderr.split()[1])
    return sorted(out), cnt


USE_C = os.environ.get("LRC_USE_C") == "1"


# ---------------------------------------------------------------------------
# Cover-based level-one generator (covergen.c).  Produces orbit
# representatives of I(k,p,1) from the minimal covers C containing class 1:
# every improper k-multiset is C + (k-|C|) arbitrary classes.  Validated
# against level1_improper / level1_improper_c in test_lonely.py.

from itertools import combinations_with_replacement as _cwr

_COVERGEN_BIN = None


def _covergen_bin():
    global _COVERGEN_BIN
    if _COVERGEN_BIN is None:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "covergen.c")
        out = os.path.join(tempfile.mkdtemp(prefix="lrc_"), "covergen")
        subprocess.run(["cc", "-O3", "-o", out, src, "-lm"], check=True)
        _COVERGEN_BIN = out
    return _COVERGEN_BIN


def minimal_covers(k, p):
    res = subprocess.run([_covergen_bin(), str(k), str(p)], check=True,
                         capture_output=True, text=True)
    covers = [tuple(int(x) for x in line.split())
              for line in res.stdout.splitlines() if line.strip()]
    nodes = int(res.stderr.split()[1])
    return covers, nodes


def level1_improper_covers(k, p, max_rows=5_000_000):
    """Orbit representatives of I(k,p,1) via minimal covers."""
    covers, nodes = minimal_covers(k, p)
    h = (p - 1) // 2
    L = Level(k, p, 1)
    out = set()
    rows = 0
    for C in covers:
        for extra in _cwr(range(1, h + 1), k - len(C)):
            rows += 1
            if rows > max_rows:
                raise RuntimeError("too many level-one rows (small covers)")
            out.add(L.canon(list(C) + list(extra)))
    return sorted(out), nodes


LEVEL1_ENGINE = os.environ.get("LRC_LEVEL1", "c" if USE_C else "py")
