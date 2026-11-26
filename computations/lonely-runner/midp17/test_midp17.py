"""Tests for midp17: xcasc.c against an independent reference cascade, the
level-one samplers against exact counts, and negative controls.

Reference cascade: smallp/xcascade.py (witness-free lifts by liftfree.c, gcd
clause and Lemma S in Python) keeping exact tuples, compared orbit by orbit
after reduction to a full unit-orbit canonical form (all units of Z_{lp},
sorted folded residues), as in k17struct/cascade_verify.c.
Run: python3 -m pytest -q computations/lonely-runner/midp17/test_midp17.py
"""
import itertools
import json
import os
import subprocess
import sys
from math import comb, gcd

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "smallp"))
import xcascade as X  # noqa: E402


def build(name, extra=()):
    exe = os.path.join(HERE, name + ("_broken" if extra else ""))
    subprocess.run(["cc", "-O2", *extra, "-o", exe, os.path.join(HERE, name + ".c"), "-lm"], check=True)
    return exe


@pytest.fixture(scope="module")
def xc():
    return build("xcasc")


def canon_full(w, N):
    best = None
    for u in range(1, N):
        if gcd(u, N) == 1:
            t = sorted(min(u * x % N, N - u * x % N) for x in w)
            if best is None or t < best:
                best = t
    return tuple(best)


def reference_levels(k, p, base, chain):
    """exact retained sets along the chain, as sets of full-canonical orbits"""
    cur, l, out = [tuple(base)], 1, []
    for c in chain:
        ws = X.wf_lifts(k, l * p, c, cur)
        l *= c
        ds = X.divisors(l)
        nxt = set()
        for lst in ws:
            for w in lst:
                if X.gcd_clause(w, l) or any(X.shift_ok(w, d, k) for d in ds):
                    continue
                nxt.add(w)
        cur = sorted(nxt)
        out.append((l, {canon_full(w, l * p) for w in cur}))
        if not cur:
            break
    return out


def xcasc_levels(exe, k, p, base, chain):
    out, lev = [], 1
    for c in chain:
        lev *= c
        r = subprocess.run([exe, str(k), str(p), ",".join(map(str, chain)), "10000000", str(lev)],
                           input=" ".join(map(str, base)) + "\n", capture_output=True, text=True, check=True)
        orb = set()
        info = None
        for line in r.stdout.splitlines():
            if line.startswith("S "):
                xs = list(map(int, line.split()[3:]))
                orb.add(canon_full(xs, lev * p))
            else:
                info = json.loads(line)
        out.append((lev, orb))
        if not orb:
            break
    return out, info


def level_one_bases(k, p, n, seed):
    """a few improper level-one multisets (support covers all folded times)"""
    import random
    rnd = random.Random(seed)
    h = (p - 1) // 2
    cov = {v: {a for a in range(1, h + 1) if (k + 1) * min(a * v % p, p - a * v % p) < p} for v in range(1, h + 1)}
    res = []
    while len(res) < n:
        b = sorted(rnd.randint(1, h) for _ in range(k))
        if set().union(*(cov[v] for v in set(b))) == set(range(1, h + 1)):
            res.append(b)
    return res


CASES = [(7, 29, (2, 2, 2)), (7, 31, (2, 3)), (8, 37, (3, 3)), (5, 17, (2, 3, 2))]


@pytest.mark.parametrize("k,p,chain", CASES)
def test_xcasc_matches_reference(xc, k, p, chain):
    for b in level_one_bases(k, p, 4, seed=p):
        ref = reference_levels(k, p, b, chain)
        got, info = xcasc_levels(xc, k, p, b, chain)
        assert [l for l, _ in got] == [l for l, _ in ref]
        for (l1, s1), (l2, s2) in zip(got, ref):
            assert s1 == s2, (k, p, b, l1)
        assert info["lvl1_witness"] == 0


def test_tight_k17_matches_smallp_record(xc):
    """tight tuple (1..17): level-2 count and death at level 18 as in smallp/results/tight17.jsonl"""
    recs = [json.loads(l) for l in open(os.path.join(HERE, "..", "smallp", "results", "tight17.jsonl"))]
    for rec in recs[:3]:
        p = rec["p"]
        r = subprocess.run([xc, "17", str(p), "2,3,3,2"], input=" ".join(map(str, range(1, 18))) + "\n",
                           capture_output=True, text=True, check=True)
        info = json.loads(r.stdout)
        assert info["trace"][0][1] == rec["trace"][0][1]       # level 2: no orbit reduction (distinct b, Z_2^* = 1)
        assert info["empty_at"] == rec["empty_at"] == 18


def test_negative_control_broken_shift_lemma_detected(xc):
    """with floor in place of ceiling the (unsound) cascade differs from the reference somewhere"""
    bad = build("xcasc", ("-DBROKEN_NG",))
    differs = False
    for k, p, chain in CASES:
        for b in level_one_bases(k, p, 4, seed=p):
            if xcasc_levels(bad, k, p, b, chain)[0] != reference_levels(k, p, b, chain):
                differs = True
                break
        if differs:
            break
    assert differs


def test_negative_control_level_one_witness_flagged(xc):
    r = subprocess.run([xc, "7", "29", "2"], input="1 1 1 1 1 1 1\n", capture_output=True, text=True, check=True)
    assert json.loads(r.stdout)["lvl1_witness"] == 1


def exact_level_one_count(k, p):
    """brute force over all k-multisets"""
    h = (p - 1) // 2
    cov = [0] * (h + 1)
    for v in range(1, h + 1):
        for a in range(1, h + 1):
            if (k + 1) * min(a * v % p, p - a * v % p) < p:
                cov[v] |= 1 << (a - 1)
    full = (1 << h) - 1
    n = 0
    for m in itertools.combinations_with_replacement(range(1, h + 1), k):
        acc = 0
        for v in m:
            acc |= cov[v]
        n += acc == full
    return n


def test_samplers_count_small_case():
    """ladder MCMC and rejection estimates agree with the exact count at k = 7, p = 29"""
    exact = exact_level_one_count(7, 29)
    mc = build("mcmc1")
    r = subprocess.run([mc, "7", "29", "5", "20000", "200"], capture_output=True, text=True, check=True)
    est = float([l for l in r.stdout.splitlines() if "est_multisets" in l][0].split()[2])
    assert abs(est / exact - 1) < 0.08
    sm = build("sample1")
    r = subprocess.run([sm, "7", "29", "count", "2000000", "3"], capture_output=True, text=True, check=True)
    est2 = float(r.stdout.splitlines()[-1].split()[2])
    assert abs(est2 / exact - 1) < 0.02
    # weights: sum_j C(k-1, j-1) A_j with exact A_j
    assert exact == sum(comb(6, j - 1) * a for j, a in exact_aj(7, 29).items())


def exact_aj(k, p):
    h = (p - 1) // 2
    cov = [0] * (h + 1)
    for v in range(1, h + 1):
        for a in range(1, h + 1):
            if (k + 1) * min(a * v % p, p - a * v % p) < p:
                cov[v] |= 1 << (a - 1)
    full = (1 << h) - 1
    res = {}
    for j in range(1, k + 1):
        n = 0
        for S in itertools.combinations(range(1, h + 1), j):
            acc = 0
            for v in S:
                acc |= cov[v]
            n += acc == full
        res[j] = n
    return res


def test_negative_control_sampler_check():
    sm = build("sample1")
    r = subprocess.run([sm, "7", "29", "check"], input="1 1 1 1 1 1 1\n1 2 3 4 5 6 7\n", capture_output=True, text=True, check=True)
    assert r.stdout.split()[0] == "0"


K17_BASES = [  # two sampled p = 151 bases (results/mcmc_p151_s1.txt); the first carries a Lemma T family
    (151, [6, 10, 14, 20, 26, 34, 34, 36, 43, 44, 45, 46, 48, 49, 62, 66, 75]),
    (151, [2, 19, 23, 24, 32, 39, 40, 47, 50, 56, 59, 60, 61, 62, 63, 65, 68]),
]


@pytest.mark.parametrize("p,b", K17_BASES)
@pytest.mark.parametrize("chain", [(2,), (3,)])
def test_xcasc_matches_reference_k17(xc, p, b, chain):
    ref = reference_levels(17, p, b, chain)
    got, _ = xcasc_levels(xc, 17, p, b, chain)
    assert got == ref and len(ref[0][1]) > 0


def test_lemma_tf_family_at_level6(xc):
    """level-6 retained set of the first base: 2,144 orbits, 2,120 of Lemma T type (zero coordinates
    cover), the other 24 with 11 zero coordinates (a defect family); regression values of section 4.1"""
    sys.path.insert(0, HERE)
    import classify
    p, b = K17_BASES[0]
    r = subprocess.run([xc, "17", str(p), "2,3", "1000000", "6"], input=" ".join(map(str, b)) + "\n",
                       capture_output=True, text=True, check=True)
    rows = [list(map(int, l.split()[3:])) for l in r.stdout.splitlines() if l.startswith("S ")]
    assert len(rows) == 2144
    tt = defect = 0
    for w in rows:
        z = [min(x % p, p - x % p) for x in w if x % 6 == 0]
        assert 11 <= len(z) <= 17 - 4      # Corollary TN': at least f_min(6) = 4 non-multiples of 6
        if classify.covers(17, p, z):
            tt += 1
        else:
            defect += 1
            assert len(z) == 11
    assert (tt, defect) == (2120, 24)
