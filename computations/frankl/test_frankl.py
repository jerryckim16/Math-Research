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
6. Costa-Sadhu Thm 1.2 (costa_sadhu_thm12.py): exact pieces, 1D and contact
   certificates, mpmath.iv cross-check of the 1e-8 contact margin, negative controls.
7. Jiang arXiv:2609.08291 (jiang_checks.py): scalars, bridge, coordinate map, the
   1e-8 kernel/mixture margins with negative controls, derivative formulas.
8. Costa-Sadhu Thm 1.2 analytic glue (analytic_glue.py), with negative controls.
9. Jiang analytic glue (analytic_glue_jiang.py), with negative controls.
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


def test_costa_sadhu_thm12():
    """Thm 1.2 (l0 = 1409/2000): exact pieces, 1D certificate, contact certificate,
    derivative formulas vs finite differences, an independent mpmath.iv evaluation
    of the 1e-8 contact margin, and negative controls."""
    import costa_sadhu_thm12 as t12
    t12.exact_checks(verbose=False)
    t12.one_dimensional_checks(verbose=False)
    nb, worst, Fc, Ft, lb = t12.contact_checks(verbose=False)
    assert lb.lo > 0
    # negative control 1: lowering alpha0 by 1e-8 makes F0(t_c, t_c) < 0, and our
    # enclosure resolves the sign (so the 1.1e-8 margin is genuinely resolved)
    dA = t12.IF(Fraction(1, 10**8)) * t12.M0_I
    G2 = t12.G_val(I(2 * t12.TC))
    assert (Fc - dA * G2).hi < 0
    # negative control 2: the 1D prover rejects the false W0 >= 1.62 G (true min ratio 1.6121)
    c = t12.IF(Fraction(162, 100))
    try:
        t12.cover_1d(lambda lo, hi: (t12.W0_point(lo) - c * t12.G_all(I(hi))[0]).lo, 0.125, 0.5,
                     n0=8, min_w=1e-6)
    except AssertionError:
        pass
    else:
        raise AssertionError("1D prover certified a false inequality")
    try:
        import mpmath as mp
    except ImportError:
        print("  Thm 1.2 exact/1D/contact OK (mpmath missing: cross-checks skipped)")
        return
    # independent evaluation with mpmath.iv (MPFR-style intervals, 200 bits)
    iv = mp.iv
    iv.prec = 200
    tau = iv.mpf(1985281) / 4000000
    m0 = iv.mpf(3085573725166011) / 5000000000000000
    a0 = 1 / (2 * m0) + iv.mpf(1) / 800000000
    b0 = 1 - a0
    Hi = lambda x: -x * iv.log(x) - (1 - x) * iv.log(1 - x)
    tc = iv.mpf(t12.TC)
    x = iv.exp(-tc)
    Gv = Hi(x) / x
    W0 = Hi(x * x * (1 + tau * (1 - x) ** 2)) / (x * x)
    F0 = a0 * Hi(x * x) / (x * x) - Gv / m0 + b0 * W0
    assert F0.a > 0 and abs(float(F0.a) - float((Fc / t12.M0_I).mid())) < 1e-13
    # derivative formulas vs finite differences (mpmath, 40 digits)
    mp.mp.dps = 40
    tau, m0 = mp.mpf(1985281) / 4000000, mp.mpf(3085573725166011) / 5000000000000000
    a0 = 1 / (2 * m0) + mp.mpf(1) / 800000000
    b0 = 1 - a0
    Hm = lambda x: -x * mp.log(x) - (1 - x) * mp.log(1 - x)
    gm = lambda x: x**2 * (1 + tau * (1 - x) ** 2)
    Gm = lambda u: mp.e**u * Hm(mp.e**-u)
    Gam = lambda u: mp.sqrt(Hm(gm(mp.e**-u))) * mp.e**u
    F = lambda t, d: m0 * (a0 * Gm(2 * t) + b0 * Gam(t + d) * Gam(t - d)) - (Gm(t + d) + Gm(t - d)) / 2
    Fx = lambda t, xi: F(t, t * xi)
    rnd = random.Random(7)
    for _ in range(6):
        u = rnd.choice([rnd.uniform(0.01, 3.0), rnd.uniform(3.0, 40.0)])
        g = t12.G_all(I(u))
        m = t12.Gam_all(I(u), True)
        for enc, ref in [(g[0], Gm(u)), (g[1], mp.diff(Gm, u)), (g[2], mp.diff(Gm, u, 2)),
                         (m[0], Gam(u)), (m[1], mp.diff(Gam, u)), (m[2], mp.diff(Gam, u, 2))]:
            assert enc.lo - 1e-9 <= ref <= enc.hi + 1e-9, (u, enc, ref)
        t, xi = rnd.uniform(0.01, 10.0), rnd.uniform(0.0, 15 / 17)
        a, b = t12.Fderivs_box(I(t), I(xi))
        ra = mp.diff(lambda s: Fx(s, xi), t)
        rb = mp.diff(lambda s: Fx(t, s), xi)
        assert a.lo - 1e-8 <= ra <= a.hi + 1e-8 and b.lo - 1e-8 <= rb <= b.hi + 1e-8
        assert t12.F_point(t, xi).lo - 1e-12 <= Fx(t, xi) <= t12.F_point(t, xi).hi + 1e-12
        d = xi * t * 0.5
        tt, dd, td = t12.hessian_box(I(t), I(d))
        assert abs(tt.mid() - mp.diff(F, (t, d), (2, 0))) < 1e-7
        assert abs(dd.mid() - mp.diff(F, (t, d), (0, 2))) < 1e-7
        assert abs(td.mid() - mp.diff(F, (t, d), (1, 1))) < 1e-7
    print("  Costa-Sadhu Thm 1.2: exact pieces, 1D + contact certificates, mpmath.iv contact value,"
          " derivative formulas, negative controls OK")


def test_jiang():
    """Jiang arXiv:2609.08291: scalar signs, bridge, coordinate map, the 1.4e-8
    kernel margin at (x*, x*) (+ negative control), and derivative formulas of the
    kernel gap / P / mixture against mpmath finite differences."""
    import jiang_checks as jc
    jc.scalar_checks(verbose=False)
    jc.verify_bridge(verbose=False)
    import mpmath as mp
    mp.mp.dps = 40
    xs = mp.mpf(172727) / 250000
    p = float(mp.sqrt((1 - 2 * xs**2) / (2 * xs * (1 - xs))))
    gap = jc.kernel_gap(I(p), I(p), 1, 1)
    assert 1.38e-8 < gap.lo and gap.hi < 1.39e-8          # = ln2 (1 - sigma^2) at the tangency
    old = jc.SIGi
    try:
        jc.SIGi = old * (1.0 + 2e-8)                      # negative control: gap must go negative
        assert jc.kernel_gap(I(p), I(p), 1, 1).hi < 0
    finally:
        jc.SIGi = old
    # mpmath model of the construction
    m, w0, w4 = mp.mpf(2468459) / 4000000, mp.mpf(8102221) / 10**7, mp.mpf(1897779) / 10**7
    A, B, z, sig = mp.mpf(716) / 1000, mp.mpf(721) / 1000, mp.mpf(181) / 256, mp.mpf(99999999) / 10**8
    h = lambda x: -x * mp.log(x) - (1 - x) * mp.log(1 - x)
    hp = lambda x: mp.log((1 - x) / x)
    ks = hp(xs) / (2 * h(xs))
    E = lambda x: -ks * (x - xs) - mp.mpf(7) / 10 * (x - xs) ** 2
    D = lambda x: h(x) if x <= 0.5 else (mp.log(2) if x <= z else mp.log(2) * h(x * x) / h(z * z))
    phi = lambda x: sig * mp.sqrt(D(x) * h(x) / h(xs)) * mp.e ** E(x)
    s = lambda x: mp.sqrt(h(x * x))
    psi = lambda x: phi(x) if x <= A else (s(x) if x >= B else
                                           (1 - (x - A) / (B - A)) * phi(x) + (x - A) / (B - A) * s(x))
    a = lambda x: 1 if x <= 0.5 else (mp.sqrt((1 - 2 * x * x) / (2 * x * (1 - x))) if x < 1 / mp.sqrt(2) else 0)
    r = lambda x, y: x * y + a(x) * a(y) * (min(x, y) - x * y)
    xmap = lambda q, br: _xmap(mp.mpf(q), br)
    _xmap = lambda q, br: (mp.mpf(1) / 16 + (mp.mpf(1) / 2 - mp.mpf(1) / 16) * q if br == 0 else
                          (1 / (q * q + mp.sqrt((q * q - 1) ** 2 + 1)) if br == 1 else
                           1 / mp.sqrt(2) + (mp.mpf(15) / 16 - 1 / mp.sqrt(2)) * q))
    gapm = lambda q1, q2, i, j: h(r(xmap(q1, i), xmap(q2, j))) - phi(xmap(q1, i)) * phi(xmap(q2, j))
    G = lambda u: h(mp.e**-u) * mp.e**u
    P = lambda u: psi(mp.e**-u) * mp.e**u
    F = lambda t, xi: m * w0 * G(2 * t) + m * w4 * P(t * (1 + xi)) * P(t * (1 - xi)) - (G(t * (1 + xi)) + G(t * (1 - xi))) / 2
    rnd = random.Random(11)
    for _ in range(40):
        q = rnd.uniform(0.02, 0.98)
        x, aa, _, _ = jc.coord(I(q), 1)
        assert x.lo - 1e-14 <= xmap(q, 1) <= x.hi + 1e-14 and abs(a(xmap(q, 1)) - q) < 1e-20
        i, j = rnd.choice(jc.KERNEL_PAIRS)
        q1, q2 = rnd.uniform(0.02, 0.98), rnd.uniform(0.02, 0.98)
        if i == j and abs(q1 - q2) < 0.05:
            continue
        val, dA, dB = jc.kernel_gap(I(q1), I(q2), i, j, True)
        assert val.lo - 1e-12 <= gapm(q1, q2, i, j) <= val.hi + 1e-12
        ra = mp.diff(lambda w: gapm(w, q2, i, j), q1)
        rb = mp.diff(lambda w: gapm(q1, w, i, j), q2)
        assert dA.lo - 1e-8 <= ra <= dA.hi + 1e-8 and dB.lo - 1e-8 <= rb <= dB.hi + 1e-8, (i, j, q1, q2)
        u = rnd.choice([rnd.uniform(0.01, 0.3), rnd.uniform(0.35, 0.7), rnd.uniform(0.75, 20)])
        pv, pd = jc.P_all(I(u))
        assert pv.lo - 1e-10 <= P(u) <= pv.hi + 1e-10
        assert pd.lo - 1e-8 <= mp.diff(P, u) <= pd.hi + 1e-8, (u, pd, mp.diff(P, u))
        t, xi = rnd.uniform(0.01, 10.0), rnd.uniform(0.0, 0.95)
        fv = jc.mixture_val(t, xi)
        assert fv.lo - 1e-10 <= F(t, xi) <= fv.hi + 1e-10
        Ft, Fx = jc.mixture_derivs(I(t), I(xi))
        if all(abs(w - c) > 1e-6 for w in (t * (1 + xi), t * (1 - xi))
               for c in (float(-mp.log(B)), float(-mp.log(A)), float(-mp.log(z)), float(mp.log(2)))):
            assert Ft.lo - 1e-8 <= mp.diff(lambda w: F(w, xi), t) <= Ft.hi + 1e-8
            assert Fx.lo - 1e-8 <= mp.diff(lambda w: F(t, w), xi) <= Fx.hi + 1e-8
    # the thinnest mixture point: the diagonal near x = x*, F(-log x*, 0) ~ 1.105e-8
    tc = -mp.log(xs)
    fv = jc.mixture_val(float(tc), 0.0)
    assert 1.1e-8 < fv.lo and abs(F(float(tc), 0) - fv.mid()) < 1e-13
    oldk = jc.K0
    try:
        jc.K0 = oldk - 2e-8                               # negative control for the mixture
        assert jc.mixture_val(float(tc), 0.0).hi < 0
    finally:
        jc.K0 = oldk
    print("  Jiang: 12 scalar signs, bridge, coordinate map, kernel margin 1.386e-8 and mixture margin 1.105e-8"
          " (+ negative controls),"
          " kernel/P/mixture values and derivatives vs mpmath OK")


def test_analytic_glue():
    """Costa-Sadhu Thm 1.2 analytic glue (analytic_glue.py): all claims, plus negative
    controls showing that each tool can fail (false identity, false z3 implications,
    Sturm count with roots present)."""
    import analytic_glue as ag
    import sympy as sp
    z3 = ag.z3
    res = ag.run_all(verbose=False)
    assert len(res) == len(ag.ALL) and all(r[3] == "OK" for r in res)
    x = ag.x
    # false identity: G' = S + x is rejected
    S = -sp.log(1 - x) / x
    assert not ag.zero_with_logs(-x * sp.diff(ag.Hs(x) / x, x) - S - x, {x: ag.La, 1 - x: ag.Lb})
    # Sturm: (lam-2)(lam-3)(lam+5) has two roots in (1, oo), one in (1, 5/2]
    p = (ag.lam - 2) * (ag.lam - 3) * (ag.lam + 5)
    assert ag.sturm_roots(p, 1) == 2 and ag.sturm_roots(p, 1, sp.Rational(5, 2)) == 1

    def must_fail(hyps, goal):
        try:
            ag.z3_valid(hyps, goal, None)
        except AssertionError:
            return
        raise AssertionError("z3 proved a false implication")
    Q = ag.Q
    # Case 1 with 7.11 in place of 178/25 = 7.12: the scalar (8 beta0/5) sqrt(7.11) - 1/(2 m0) < 0
    Gs_, Gu_, P_, D_ = z3.Reals("Gs Gu P D")
    F0z = Gu_ / 800000000 - D_ / (2 * Q(ag.M0)) + Q(ag.BETA0) * P_
    must_fail([Gs_ > 0, Gu_ > 0, D_ >= 0, D_ < Gs_, P_ >= 0,
               P_ * P_ >= Q(Fraction(64, 25) * Fraction(711, 100)) * Gs_ * Gs_, Gu_ < 1], F0z > 0)
    # Case 3 with log(1/2u) >= 6 log 2 only (6 beta0 log 2 < 1/(2 m0))
    U2, R_, H_, Lg_ = z3.Reals("u R H Lg")
    must_fail([Gu_ > 0, Gu_ < 1, U2 > 0, U2 <= Q(Fraction(1, 512)), R_ > 0, D_ < U2 * H_,
               H_ <= 2 * R_, P_ >= 2 * U2 * R_ * Lg_, Lg_ >= 6 * Q(ag._L2LO)], F0z > 0)
    # residual region: xi < 14/17 does NOT follow
    S_, Sg, Gs2, Gsg, G16 = z3.Reals("s sigma Gs Gsig G16")
    K = Q(ag.k2)
    hyps = [S_ > 0, Sg >= S_, Gs2 > 0, G16 >= K * Gs2, z3.Implies(Sg >= 16 * S_, Gsg >= G16),
            z3.Not(Gsg >= K * Gs2), z3.Not(z3.And(S_ >= 2, Sg >= 2)),
            z3.Not(z3.And(S_ <= Q(Fraction(1, 1024)), Sg <= Q(Fraction(1, 1024))))]
    must_fail(hyps, 17 * (Sg - S_) < 14 * (Sg + S_))
    # and dropping "not Case 3" loses the lower bound t > 2^-11
    must_fail(hyps[:-1], (S_ + Sg) / 2 > Q(Fraction(1, 2048)))
    # non-vacuity guard: inconsistent hypotheses are refused even though they imply anything
    must_fail([S_ > 1, S_ < 0], S_ == 5)
    print(f"  analytic glue: {len(res)} claims OK; negative controls (false identity, Sturm, "
          "z3 with 7.11, 6 log 2, 14/17, no Case 3, vacuity guard) behave")


def test_analytic_glue_jiang():
    """Jiang arXiv:2609.08291 analytic glue (analytic_glue_jiang.py): all claims, plus negative
    controls showing that each tool can fail (false log identities, an unlisted log factor, z3 on
    weakened hypotheses, the z3 vacuity guard, Arb and interval scalars with a changed parameter)."""
    import analytic_glue_jiang as aj
    import sympy as sp
    z3 = aj.z3
    res = aj.run_all(verbose=False)
    assert len(res) == len(aj.ALL) and all(r[3] == "OK" for r in res)
    x = aj.x
    Lp_ = sp.Symbol("L1px")
    bases = {x: aj.LX, 1 - x: aj.L1X, 1 + x: Lp_}
    pr = [(1 - x) / (1 + x), x / (1 + x), x / (1 + x)]
    H3 = -sum(pi_ * sp.log(pi_) for pi_ in pr)
    # sympy: the grouping identity with a wrong prefactor (1 + x^2) is rejected
    assert not aj.zero_logs(2 * aj.hs(x) - aj.hs(x**2) - (1 + x**2) * H3, bases)
    # sympy: the q' identity with the sign of h/(1-x) flipped is rejected
    h_ = aj.hs(x)
    hp = sp.diff(h_, x)
    lhs = h_**2 * sp.diff(x * hp / h_, x)
    assert not aj.zero_logs(lhs - (hp * (-sp.log(1 - x)) + h_ / (1 - x)), {x: aj.LX, 1 - x: aj.L1X})
    # logsub refuses a log factor that is not listed (nothing left to heuristics)
    try:
        aj.logsub(sp.log(1 + x), {x: aj.LX})
        raise RuntimeError("logsub accepted an unlisted factor")
    except AssertionError:
        pass

    def must_fail(hyps, goal):
        try:
            aj.z3_valid(hyps, goal, None)
        except AssertionError:
            return
        raise AssertionError("z3 proved a false implication")
    from fractions import Fraction as Fr
    must_fail(*aj.lower_strip_skeleton("y>=1/2", Fr(101, 100)))     # 2 C_b P0 < 1.01 is not enough
    must_fail(*aj.upper_strip_checks(Fr(101, 100)))                 # C_t C_g < 1.01 is not enough
    must_fail(*aj.small_t_skeleton(with_bracket=False))             # bracket <= 0 (e.g. T = 0.1)
    must_fail(*aj.large_t_skeleton(8))                              # t >= 8 instead of 16
    must_fail(*aj.edge_skeleton(2, with_tail=False))                # edge2 without v <= -ln B
    must_fail(*aj.passing_skeleton("mixed", with_bridge=False))     # mixed case without the bridge
    must_fail(*aj.reduction_skeleton(p_is_max=False))               # p = min p_i instead of max
    X = z3.Real("x")
    must_fail([X > 1, X < 0], X == 5)                               # vacuity guard: unsat hypotheses
    # Arb: the same scalars with a changed parameter are certified NEGATIVE
    if aj.flint is not None:
        assert aj.arb_scalars(T=Fr(1, 10))["2 m w4 (1 - ln 4T) - 1"] < 0
        assert aj.arb_scalars(large_t=8)["16 m w4 C^2 - 1/2"] < 0
        assert aj.arb_scalars(sigma=aj.jc.SIG * Fr(101, 100))["s(A) - phi(A)"] < 0
    # interval: the small-t bracket at T = 1/10 is certified negative by interval.py too
    jc = aj.jc
    br = 2.0 * jc.MW4 * (1.0 - jc.ilog(4.0 * jc.IF(Fr(1, 10)))) - 1.0
    assert br.hi < 0
    print(f"  Jiang analytic glue: {len(res)} claims OK; negative controls (2 false identities, unlisted log, "
          "z3 x7 + vacuity guard, Arb x3, interval) behave")


if __name__ == "__main__":
    tests = [test_bruteforce, test_c_enumerator, test_interval, test_boppana]
    if os.path.exists(os.path.join(HERE, "costa_sadhu_checks.py")):
        tests.append(test_lemma_R_pieces)
        try:
            import mpmath  # noqa: F401
            tests.append(test_costa_sadhu_derivatives)
        except ImportError:
            print("(mpmath missing: derivative cross-check skipped)")
    if os.path.exists(os.path.join(HERE, "costa_sadhu_thm12.py")):
        tests.append(test_costa_sadhu_thm12)
    if os.path.exists(os.path.join(HERE, "jiang_checks.py")):
        tests.append(test_jiang)
    if os.path.exists(os.path.join(HERE, "analytic_glue.py")):
        try:
            import sympy  # noqa: F401
            import z3  # noqa: F401
            tests.append(test_analytic_glue)
        except ImportError:
            print("(sympy or z3-solver missing: analytic-glue checks skipped)")
    if os.path.exists(os.path.join(HERE, "analytic_glue_jiang.py")) and test_analytic_glue in tests:
        tests.append(test_analytic_glue_jiang)
    for t in tests:
        print(t.__name__)
        t()
    print("ALL TESTS PASSED")
