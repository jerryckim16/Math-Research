"""Tests for computations/frankl.   Run:  python3 test_frankl.py

1. Brute force (pure Python) over all families of subsets of [n], n <= 4:
   union-closed families containing the empty set are counted and checked for
   Frankl's property; counts must match the literature (Brinkmann-Deklerck,
   arXiv:1701.03751, Tables 1-2) and the C enumerator frankl_enum.c.
2. The C enumerator reproduces the labeled counts for n <= 5 (n = 6 is in
   results/small_cases.txt; rerun with run_small_cases.sh).
3. Interval arithmetic: log/exp enclosures against exact rational bounds.
4. The rigorous verification of phi*H(x^2) >= x*H(x) succeeds, and the same
   prover FAILS on a false variant (negative control).
5. Costa-Sadhu Lemma R pieces (exact rational checks) and constants.
"""
from __future__ import annotations

import itertools
import os
import random
import re
import shutil
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from interval import I, ilog, iexp, H  # noqa: E402

# literature values (Brinkmann-Deklerck Table 2 "labeled Moore families" and
# Table 1 "labeled UCS" = union-closed, containing {} and with universe [n])
LABELED = {1: 2, 2: 7, 3: 61, 4: 2480, 5: 1385552, 6: 75973751474}
LABELED_FULL = {1: 1, 2: 4, 3: 45, 4: 2271, 5: 1373701, 6: 75965474236}
CLASSES = {0: 1, 1: 2, 2: 5, 3: 19, 4: 184, 5: 14664}  # Moore families up to iso


def brute(n):
    """All union-closed F subset of 2^[n] with {} in F; returns stats."""
    sets = list(range(1, 1 << n))
    total = full = tight = fails = 0
    for bits in range(1 << len(sets)):
        F = [0] + [sets[i] for i in range(len(sets)) if bits >> i & 1]
        Fs = set(F)
        if any((a | b) not in Fs for a in F for b in F):
            continue
        total += 1
        U = 0
        for a in F:
            U |= a
        if U == (1 << n) - 1:
            full += 1
        if len(F) >= 2:
            best = max(sum(1 for a in F if a >> j & 1) for j in range(n))
            if 2 * best < len(F):
                fails += 1
            elif 2 * best == len(F):
                tight += 1
    return total, full, tight, fails


def canon_classes(n):
    """Number of union-closed families with {} on [n] up to S_n (brute)."""
    sets = list(range(1, 1 << n))
    fams = []
    for bits in range(1 << len(sets)):
        F = frozenset([0] + [sets[i] for i in range(len(sets)) if bits >> i & 1])
        if all((a | b) in F for a in F for b in F):
            fams.append(F)
    perms = list(itertools.permutations(range(n)))

    def img(F, p):
        return frozenset(sum(1 << p[j] for j in range(n) if s >> j & 1) for s in F)

    seen = set()
    classes = 0
    for F in fams:
        if F in seen:
            continue
        classes += 1
        for p in perms:
            seen.add(img(F, p))
    return classes


def test_bruteforce():
    for n in range(1, 5):
        total, full, tight, fails = brute(n)
        assert total == LABELED[n], (n, total)
        assert full == LABELED_FULL[n], (n, full)
        assert fails == 0
        print(f"  brute n={n}: {total} families ({full} with universe [n]), tight={tight}, counterexamples=0")
    for n in range(0, 4):
        c = canon_classes(n) if n > 0 else 1
        assert c == CLASSES[n], (n, c)
    print("  brute isomorphism classes n<=3 match 1,2,5,19")


def test_c_enumerator():
    if shutil.which("gcc") is None:
        print("  (gcc not found: C enumerator test skipped)")
        return
    exe = os.path.join(HERE, "frankl_enum_test")
    subprocess.run(["gcc", "-O2", "-o", exe, os.path.join(HERE, "frankl_enum.c")], check=True)
    brute_tight = {n: brute(n)[2] for n in range(1, 5)}
    for n in range(1, 6):
        r = subprocess.run([exe, str(n)], capture_output=True, text=True, check=True)
        d = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", r.stdout)}
        assert d["labeled_total"] == LABELED[n], (n, d)
        assert d["labeled_fulluniverse"] == LABELED_FULL[n], (n, d)
        assert d["base_classes"] == CLASSES[n - 1], (n, d)
        assert d["counterexamples"] == 0
        if n in brute_tight:
            assert d["tight"] == brute_tight[n], (n, d["tight"], brute_tight[n])
        print(f"  C n={n}: {d['labeled_total']} labeled, {d['base_classes']} base classes, OK")
    os.remove(exe)
    # n = 6 stored result
    path = os.path.join(HERE, "results", "small_cases.txt")
    t = {}
    for line in open(path):
        if line.startswith("n=6 part="):
            for k, v in re.findall(r"(\w+)=(\d+)", line):
                if k in ("labeled_total", "labeled_fulluniverse", "counterexamples"):
                    t[k] = t.get(k, 0) + int(v)
    assert t == {"labeled_total": LABELED[6], "labeled_fulluniverse": LABELED_FULL[6], "counterexamples": 0}, t
    print("  stored n=6 run: totals match 75973751474 / 75965474236, no counterexample")


def _log_frac_bounds(q: Fraction, N=60):
    """Exact rational bounds for log q, q in [1/2, 2], via atanh series."""
    z = (q - 1) / (q + 1)
    s = sum(z ** (2 * j + 1) / (2 * j + 1) for j in range(N)) * 2
    tail = 2 * abs(z) ** (2 * N + 1) / ((2 * N + 1) * (1 - z * z))
    return s - tail, s + tail


def test_interval():
    rnd = random.Random(1)
    for _ in range(300):
        x = rnd.uniform(0.5, 2.0)
        lo, hi = _log_frac_bounds(Fraction(x))
        L = ilog(I(x))
        assert Fraction(L.lo) <= lo and hi <= Fraction(L.hi), (x, L)
        assert L.width() < 1e-14
    # exp vs log consistency (both rigorous => intervals must overlap)
    for _ in range(300):
        x = rnd.uniform(-20, 20)
        E = iexp(I(x))
        L = ilog(E)
        assert L.lo <= x <= L.hi
    try:
        import mpmath  # optional cross-check
        iv = mpmath.iv
        iv.prec = 120
        for _ in range(200):
            x = rnd.uniform(1e-6, 1 - 1e-6)
            Hx = H(I(x))
            ref = iv.mpf(x)
            ref = -ref * iv.log(ref) - (1 - ref) * iv.log(1 - ref)
            assert Hx.lo <= float(ref.a) and float(ref.b) <= Hx.hi
        print("  interval log/exp/H: exact-rational and mpmath.iv cross-checks OK")
    except ImportError:
        print("  interval log/exp: exact-rational cross-check OK (mpmath not installed)")


def test_boppana():
    import verify_boppana as vb
    vb.run(verbose=False)
    # negative control: (phi - 1e-3) H(x^2) >= x H(x) is FALSE near x = phi
    shifted = vb.PHI - 1e-3

    def bad(lo, hi):
        X = I(lo, hi)
        return shifted * H(X.sq()) - X * H(X)
    try:
        vb.prove_positive(bad, 0.55, 0.7, min_width=1e-9)
    except AssertionError:
        pass
    else:
        raise AssertionError("prover certified a false inequality")
    # H(phi^2) = H(phi) since phi^2 = 1 - phi  (equality case)
    p = vb.PHI
    assert abs(H(p.sq()).mid() - H(p).mid()) < 1e-14
    print("  Boppana/AHS inequality certified; negative control rejected")


def test_lemma_R_pieces():
    import costa_sadhu_checks as cs
    cs.exact_checks(verbose=False)
    print("  Costa-Sadhu exact rational pieces (Bernstein certificate, identities) OK")


def test_costa_sadhu_derivatives():
    """The mean-value / Hessian bounds are only sound if the derivative
    formulas are right: compare with central finite differences (mpmath)."""
    import mpmath as mp
    import costa_sadhu_checks as cs
    mp.mp.dps = 40
    cs.setup()
    ms, al, be = (mp.mpf(cs.K[k].mid()) for k in ("ms", "alpha", "beta"))
    Hm = lambda x: -x * mp.log(x) - (1 - x) * mp.log(1 - x)
    gm = lambda x: x**2 * (1 + (1 - x) ** 2)
    Gm = lambda u: mp.e**u * Hm(mp.e**-u)
    Gam = lambda u: mp.sqrt(Hm(gm(mp.e**-u))) * mp.e**u
    F = lambda t, d: ms * (al * Gm(2 * t) + be * Gam(t + d) * Gam(t - d)) - (Gm(t + d) + Gm(t - d)) / 2
    Ft = lambda t, xi: F(t, t * xi)
    rnd = random.Random(5)
    for _ in range(6):
        u = rnd.uniform(0.05, 3.0)
        U = I(u)
        g0, g1, g2 = cs.G_all(U)
        m0, m1, m2 = cs.Gam_all(U, True)
        for enc, ref in [(g0, Gm(u)), (g1, mp.diff(Gm, u)), (g2, mp.diff(Gm, u, 2)),
                         (m0, Gam(u)), (m1, mp.diff(Gam, u)), (m2, mp.diff(Gam, u, 2))]:
            assert enc.lo - 1e-9 <= ref <= enc.hi + 1e-9, (u, enc, ref)
        t, xi = rnd.uniform(0.1, 2.0), rnd.uniform(0.0, 0.9)
        a, b = cs.Fderivs_box(I(t), I(xi))
        ra = mp.diff(lambda s: Ft(s, xi), t)
        rb = mp.diff(lambda s: Ft(t, s), xi)
        assert a.lo - 1e-8 <= ra <= a.hi + 1e-8 and b.lo - 1e-8 <= rb <= b.hi + 1e-8
        d = xi * t * 0.5
        tt, dd, td = cs.hessian_box(I(t), I(d))
        assert abs(tt.mid() - mp.diff(F, (t, d), (2, 0))) < 1e-7
        assert abs(dd.mid() - mp.diff(F, (t, d), (0, 2))) < 1e-7
        assert abs(td.mid() - mp.diff(F, (t, d), (1, 1))) < 1e-7
    # F vanishes at the tangency (t*, 0)
    assert abs(cs.F_point(cs.K["ts"].mid(), 0.0).mid()) < 1e-12
    print("  Costa-Sadhu derivative formulas agree with finite differences; F(t*,0)=0")


if __name__ == "__main__":
    tests = [test_bruteforce, test_c_enumerator, test_interval, test_boppana]
    if os.path.exists(os.path.join(HERE, "costa_sadhu_checks.py")):
        tests.append(test_lemma_R_pieces)
        try:
            import mpmath  # noqa: F401
            tests.append(test_costa_sadhu_derivatives)
        except ImportError:
            print("(mpmath missing: derivative cross-check skipped)")
    for t in tests:
        print(t.__name__)
        t()
    print("ALL TESTS PASSED")
