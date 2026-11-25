"""Tests for the kissing-configuration checkers.

Run: python3 test_kissing.py BUILD_DIR   (BUILD_DIR holds the compiled
kiss_check binary; scratch files are written there too).

1. Known configurations pass with the known contact counts (24-cell, D5, E8).
2. Negative controls fail: an added short vector, a perturbed coordinate,
   a duplicated row, a scaled copy of a row.
3. Three implementations (C int16, numpy float32 GEMM, pure-Python big
   integers) agree exactly on violation and contact counts on random
   integer configurations with mixed norms, passing and failing.
4. check_mixed.py: rows rescaled by ~1e15 keep their angles (pass), and a
   scaled copy of an existing row is caught (fail).
5. kiss_check_field.py (both modes): E8 with rows multiplied by sqrt2, sqrt3,
   sqrt6 and by 7e18 passes with 6720 contacts in all; the 12 rotated
   cuboctahedron tails of the 27D construction (entries in Z[sqrt2]) pass
   with 24 contacts; adding a bad irrational row fails. Contact counts are
   compared with a pure-Python exact reference.
6. check_decimal.py: E8 written as decimal text, every row scaled by a
   different exact decimal factor (some in e-notation), passes with 6720
   contacts; moving one row by 1e-15 towards a contact partner fails.
   build_einstein11.py: the 604-point 11D configuration passes with
   17088 + 2616 = 19704 contacts; both negative variants fail.
7. Class mode of kiss_check.c and kiss_check_np.py (thresholds from
   class_table.py): (a) on random mixed-norm sets with one class per norm
   (L = 1, no head part) it agrees exactly with norm mode and with the
   brute-force reference; (b) on random split sets x = (L u, w_c) with
   large integer head vectors w_c (L = 10^6) both implementations agree
   with a pure-Python big-integer check of the assembled vectors, passing
   and failing; (c) E8 split as (body 7 coords, head = last coordinate)
   passes with 6720 contacts; lowering one table entry by 1, or adding a
   duplicate row, makes it fail.
9. Partner (Gram) mode: D5 and E8, and E8 with a duplicated or perturbed
   row, written in a random unimodular basis (coordinates C = X U^-1, Gram
   G = U U^T, partner rows C G): C and numpy agree with norm mode on X.
10. Affine class mode (40-43D, build_kravatskiy4043.py): class and partner
   modes combined, with uint16 labels (more than 256 classes). Points
   (x, z_c/D_c) with body metric G/3, G = 3 U U^T in a random basis, and
   300 classes of random rational heads: the C checker (whole, and as
   --part K 3 pieces whose pair counts add up to C(n,2)) and numpy agree
   exactly with a pure-Python Fraction check of the inner products, passing
   and failing; E8 spread over 300 zero-head classes passes with 6720
   contacts; enum_affine.c reproduces a brute-force affine shell count.
8. Chain rebuild (small, synthetic, in the format of build_kravatskiy34.py):
   a toy parent certificate plus a witness is edited by the same `edit`
   function; the stars, root deletions and counts come out as computed by
   hand, and applying the octad switch to a support that does not match
   the parent is rejected.
"""

import itertools
import json
import os
import random
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import known  # noqa: E402

BUILD = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
CBIN = os.path.join(BUILD, "kiss_check")


def brute(rows):
    """Reference: pure Python integers."""
    viol = cont = 0
    n = len(rows)
    nr = [sum(x * x for x in r) for r in rows]
    for i in range(n):
        for j in range(i + 1, n):
            p = sum(x * y for x, y in zip(rows[i], rows[j]))
            if p > 0:
                if 4 * p * p > nr[i] * nr[j]:
                    viol += 1
                elif 4 * p * p == nr[i] * nr[j]:
                    cont += 1
    return viol, cont


def parse(out):
    v = int(re.search(r"^violations (\d+)", out, re.M).group(1))
    c = int(re.search(r"^contacts_60deg (\d+)", out, re.M).group(1))
    res = re.search(r"^RESULT (\w+)", out, re.M).group(1)
    return v, c, res


def run_c(rows, d, tag):
    path = os.path.join(BUILD, f"t_{tag}.i8")
    known.write_i8(rows, path)
    out = subprocess.run([CBIN, path, str(d)], capture_output=True, text=True).stdout
    return parse(out)


def run_np(rows, d, tag):
    path = os.path.join(BUILD, f"t_{tag}.i8")
    known.write_i8(rows, path)
    out = subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_np.py"), path, str(d),
                          "--workers", "1", "--tile", "7"], capture_output=True, text=True).stdout
    return parse(out)


def check(name, rows, d, expect_pass, expect_contacts=None):
    b = brute(rows)
    c = run_c(rows, d, name)
    p = run_np(rows, d, name)
    assert c[:2] == b and p[:2] == b, (name, b, c, p)
    assert (c[2] == "PASS") == expect_pass and (p[2] == "PASS") == expect_pass, (name, c, p)
    if expect_contacts is not None:
        assert b[1] == expect_contacts, (name, b)
    print(f"ok  {name:28s} violations={b[0]:<6d} contacts={b[1]:<6d} {'PASS' if expect_pass else 'FAIL (expected)'}")


def main():
    D4, D5, E8 = known.roots_D(4), known.roots_D(5), known.roots_E8_scaled()
    check("D4 (24-cell)", D4, 4, True, 24 * 8 // 2)
    check("D5", D5, 5, True, 40 * 12 // 2)
    check("E8", E8, 8, True, 240 * 56 // 2)
    # negative controls
    check("D4 + (1,0,0,0)", D4 + [(1, 0, 0, 0)], 4, False)
    e = list(E8)
    e[0] = tuple(list(e[0][:2]) + [1] + list(e[0][3:]))  # (2,2,0,..) -> (2,2,1,0,..)
    assert e[0] != E8[0]
    check("E8 perturbed coordinate", e, 8, False)
    check("E8 duplicated row", E8 + [E8[17]], 8, False)
    check("D5 scaled copy of a row", D5 + [tuple(2 * x for x in D5[3])], 5, False)
    # random cross-checks with mixed norms
    rng = random.Random(20261124)
    for t in range(40):
        d = rng.randint(3, 7)
        rows = []
        while len(rows) < rng.randint(10, 60):
            v = tuple(rng.randint(-3, 3) for _ in range(d))
            if any(v):
                rows.append(v)
        b = brute(rows)
        check(f"random#{t} d={d} n={len(rows)}", rows, d, b[0] == 0)
    # greedy random kissing sets (pass) with mixed norms
    for t in range(10):
        d = rng.randint(3, 6)
        rows = []
        for _ in range(3000):
            v = tuple(rng.randint(-2, 2) for _ in range(d))
            nv = sum(x * x for x in v)
            if any(v) and all(
                    (q := sum(x * y for x, y in zip(v, r))) <= 0 or 4 * q * q <= nv * sum(x * x for x in r)
                    for r in rows):
                rows.append(v)
        check(f"greedy#{t} d={d} n={len(rows)}", rows, d, True)

    # check_mixed.py: huge rescaled rows keep their angles
    K = 10**15 + 37
    rows = [list(r) for r in E8]
    big = [tuple(K * x for x in rows[i]) for i in range(5)]
    good = [tuple(r) for r in rows[5:]] + big
    for tag, data, ok in (("mixed pass", good, True), ("mixed fail", good + [tuple(K * x for x in rows[9])], False)):
        path = os.path.join(BUILD, "t_mixed.i64")
        small_path = os.path.join(BUILD, "t_mixed_small.i8")
        np.array(data, dtype="<i8").tofile(path)
        out = subprocess.run([sys.executable, os.path.join(HERE, "check_mixed.py"), path, "8",
                              "--write-small", small_path], capture_output=True, text=True).stdout
        res = re.search(r"RESULT\(big pairs\) (\w+)", out).group(1)
        small = subprocess.run([CBIN, small_path, "8"], capture_output=True, text=True).stdout
        sres = parse(small)[2]
        allpass = res == "PASS" and sres == "PASS"
        bv = brute([tuple(x) for x in data])
        assert allpass == ok == (bv[0] == 0), (tag, out, small)
        print(f"ok  check_mixed {tag:16s} big-pairs {res}, small-pairs {sres}")
    field_tests(E8)
    decimal_tests(E8)
    einstein11_tests()
    class_tests(E8)
    chain_tests()
    partner_tests(D5, E8)
    affine_tests(E8)
    print("ALL TESTS PASSED")


def field_tests(E8):
    import json
    sys.path.insert(0, HERE)
    import kiss_check_field as kf

    def run(bulk, field, d, tag):
        bp, fp = os.path.join(BUILD, f"f_{tag}.i8"), os.path.join(BUILD, f"f_{tag}.json")
        known.write_i8(bulk, bp)
        json.dump({"d": d, "rows": field}, open(fp, "w"))
        outs = []
        for mode in ("float", "interval"):
            out = subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_field.py"), bp, fp,
                                  "--mode", mode, "--workers", "2"], capture_output=True, text=True).stdout
            outs.append(parse(out))
        assert outs[0] == outs[1], (tag, outs)
        # exact reference over field pairs only
        z = [0] * d
        allrows = [[list(b), z, z, z] for b in bulk] + field
        nb = len(bulk)
        nrm = [kf.pair_coeffs(r, r)[0] for r in allrows]
        v = c = 0
        for i in range(nb, len(allrows)):
            for j in range(i):
                r = kf.exact_nested(kf.pair_coeffs(allrows[i], allrows[j]), nrm[i], nrm[j])
                v += r > 0
                c += r == 0
        assert outs[0][:2] == (v, c), (tag, outs, v, c)
        return outs[0]

    z8 = [0] * 8
    bulk = E8[:120]
    field = []
    for t, r in enumerate(E8[120:]):
        r = list(r)
        k = t % 4
        if k == 0:
            field.append([[x * (7 * 10**18 + 1) for x in r], z8, z8, z8])
        else:
            comp = [z8, z8, z8, z8]
            comp[k] = r
            field.append(comp)
    v, c, res = run(bulk, field, 8, "e8")
    bb = brute(bulk)
    assert res == "PASS" and bb == (0, 6720 - c), (v, c, bb)
    print(f"ok  field E8 (sqrt2, sqrt3, sqrt6, 7e18 multiples)  field contacts={c} + bulk {bb[1]} = 6720")
    bad = field + [[[2, 2, 1, 0, 0, 0, 0, 0], z8, z8, z8], [z8, [2, 2, 0, 0, 0, 0, 0, 1], z8, z8]]
    v, c, res = run(bulk, bad, 8, "e8bad")
    assert res == "FAIL" and v > 0
    print(f"ok  field E8 + two bad rows                  violations={v} FAIL (expected)")
    V = sorted({(a, b, 0) for a in (1, -1) for b in (1, -1)} | {(a, 0, b) for a in (1, -1) for b in (1, -1)}
               | {(0, a, b) for a in (1, -1) for b in (1, -1)})
    tails = [[[0, 0, 4 * w[2], 0], [2 * (w[0] - w[1]), 2 * (w[0] + w[1]), 0, 0], [0] * 4, [0] * 4] for w in V]
    v, c, res = run([(0, 0, 0, 1)], tails, 4, "tails")
    assert res == "PASS" and c == 24, (v, c)
    print(f"ok  field 27D pure tails (cuboctahedron)       contacts={c} PASS")
    v, c, res = run([(0, 0, 0, 1)], tails + [[[0, 0, 1, 0], [0] * 4, [0] * 4, [0] * 4]], 4, "tailsbad")
    assert res == "FAIL" and v == 4, (v, c)
    print(f"ok  field tails + (0,0,1)                     violations={v} FAIL (expected)")


def run_out(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout


def decimal_tests(E8):
    from decimal import Decimal
    rng = random.Random(7)
    path = os.path.join(BUILD, "t_e8.txt")

    def write(rows):
        with open(path, "w") as f:
            for r in rows:
                f.write(" ".join(r) + "\n")

    rows = []
    for k, r in enumerate(E8):
        c = Decimal(rng.randint(1, 10**6)) / Decimal(10**rng.randint(0, 9))
        if k % 3 == 0:   # exact e-notation: (value * 10^5) followed by e-5
            rows.append([format((Decimal(x) * c).scaleb(5), "f") + "e-5" for x in r])
        else:
            rows.append([str(Decimal(x) * c) for x in r])
    write(rows)
    code, out = run_out([sys.executable, os.path.join(HERE, "check_decimal.py"), path, "8"])
    con = int(re.search(r"contacts=(\d+)", out).group(1))
    assert code == 0 and "RESULT: PASS" in out and con == 6720, out
    print(f"ok  check_decimal E8 (rescaled decimal rows)    contacts={con} PASS")
    # nudge row 0 by 1e-15 of a contact partner
    a = E8[0]
    j = next(i for i, b in enumerate(E8) if 2 * sum(x * y for x, y in zip(a, b)) == sum(x * x for x in a))
    bad = [[str(Decimal(x)) for x in r] for r in E8]
    bad[0] = [str(Decimal(x) + Decimal(y) * Decimal("1e-15")) for x, y in zip(a, E8[j])]
    write(bad)
    code, out = run_out([sys.executable, os.path.join(HERE, "check_decimal.py"), path, "8"])
    assert code == 1 and "RESULT: FAIL" in out, out
    print("ok  check_decimal E8 row nudged by 1e-15        FAIL (expected)")


def einstein11_tests():
    pre = os.path.join(BUILD, "t_e11")
    for variant, ok in ((None, True), ("repeat", False), ("pairmix", False)):
        args = [sys.executable, "-I", os.path.join(HERE, "build_einstein11.py"), pre]
        if variant:
            args += ["--variant", variant]
        subprocess.run(args, check=True, capture_output=True)
        c_out = subprocess.run([CBIN, pre + ".i8", "11"], capture_output=True, text=True).stdout
        bv, bc, bres = parse(c_out)
        f_out = subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_field.py"), pre + ".i8",
                                pre + "_field.json", "--mode", "float", "--workers", "1"],
                               capture_output=True, text=True).stdout
        fv = int(re.search(r"violations (\d+)", f_out).group(1))
        fc = int(re.search(r"contacts_60deg (\d+)", f_out).group(1))
        if ok:
            assert bres == "PASS" and fv == 0 and (bc, fc) == (17088, 2616), (bc, fc, c_out, f_out)
            print(f"ok  11D EinsteinArena 604                       contacts={bc}+{fc} PASS")
        else:
            assert bv + fv > 0, (variant, c_out, f_out)
            print(f"ok  11D variant {variant:8s}                      violations={bv + fv} FAIL (expected)")


def run_class(body, labels, classes, L, d, tag, table_edit=None):
    """Write body/labels/classes, build the table, run C and numpy class mode."""
    import class_table
    pre = os.path.join(BUILD, f"t_cls_{tag}")
    np.array(body, dtype=np.int8).reshape(-1, d).tofile(pre + ".i8")
    np.array(labels, dtype=np.uint8).tofile(pre + ".u8")
    json.dump({"L": L, "classes": classes}, open(pre + ".json", "w"))
    class_table.main(pre + ".json", pre + ".tab")
    if table_edit:
        lines = open(pre + ".tab").read().split("\n")
        lines = [table_edit(ln) for ln in lines]
        open(pre + ".tab", "w").write("\n".join(lines))
    c = parse(subprocess.run([CBIN, pre + ".i8", str(d), pre + ".u8", pre + ".tab"],
                             capture_output=True, text=True).stdout)
    p = parse(subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_np.py"), pre + ".i8", str(d),
                              "--workers", "1", "--tile", "7", "--classes", pre + ".u8", pre + ".tab"],
                             capture_output=True, text=True).stdout)
    return c, p


def class_tests(E8):
    rng = random.Random(20261125)
    # (a) one class per norm, L = 1, no head: must equal norm mode
    for t in range(15):
        d = rng.randint(3, 6)
        rows = [v for v in (tuple(rng.randint(-3, 3) for _ in range(d)) for _ in range(rng.randint(10, 50))) if any(v)]
        norms = sorted({sum(x * x for x in r) for r in rows})
        lab = [norms.index(sum(x * x for x in r)) for r in rows]
        cl = [{"w": [], "body_norm": n} for n in norms]
        c, p = run_class(rows, lab, cl, 1, d, f"a{t}")
        b = brute(rows)
        nm = run_c(rows, d, f"cls_a{t}")
        assert c[:2] == p[:2] == b == nm[:2], (t, c, p, b, nm)
    print("ok  class mode = norm mode on 15 random sets (C, numpy, brute force)")
    # (b) split vectors (L u, w_c) with big heads, against big-integer brute force
    L = 10**6
    pool = {}
    for v in itertools.product(range(-2, 3), repeat=5):
        if any(v):
            pool.setdefault(sum(x * x for x in v), []).append(v)
    seen = [0, 0]
    for t in range(12):
        k = rng.randint(2, 5)
        cl, heads = [], []
        for _ in range(k):
            n = rng.choice([4, 8, 12, 16])
            w = [rng.choice([0, L]) * rng.randint(-2, 2) + rng.randint(-3 * L, 3 * L) * rng.randint(0, 1)
                 for _ in range(2)]
            cl.append({"w": w, "body_norm": n})
            heads.append(w)
        body, lab, full = [], [], []
        greedy = t % 2 == 0  # even t: keep only rows compatible with all earlier rows
        for _ in range(rng.randint(15, 40) * (20 if greedy else 1)):
            c_ = rng.randrange(k)
            u = rng.choice(pool[cl[c_]["body_norm"]])
            x = tuple(L * v for v in u) + tuple(heads[c_])
            if greedy and brute(full + [x])[0]:
                continue
            body.append(u)
            lab.append(c_)
            full.append(x)
        b = brute(full)
        c, p = run_class(body, lab, cl, L, 5, f"b{t}")
        assert c[:2] == p[:2] == b, (t, c, p, b)
        seen[b[0] == 0] += 1
    assert min(seen) > 0, seen
    print(f"ok  class mode on 12 random split sets, L = 10^6 ({seen[1]} pass, {seen[0]} fail): C = numpy = big-integer brute force")
    # (c) E8 split as body (first 7 coordinates) + head (last coordinate), L = 3
    body = [r[:7] for r in E8]
    keys = sorted({(r[7], sum(x * x for x in r[:7])) for r in E8})
    lab = [keys.index((r[7], sum(x * x for x in r[:7]))) for r in E8]
    cl = [{"w": [3 * h], "body_norm": n} for h, n in keys]
    c, p = run_class(body, lab, cl, 3, 7, "e8")
    assert c == p == (0, 6720, "PASS"), (c, p)

    def lower(ln):  # lower the threshold of the first class pair that has contacts
        f = ln.split()
        if len(f) == 4 and f[3] != "32767" and not lower.done:
            lower.done = True
            return f"{f[0]} {f[1]} {int(f[2]) - 1} {f[3]}"
        return ln
    lower.done = False
    c2, p2 = run_class(body, lab, cl, 3, 7, "e8low", lower)
    c3, p3 = run_class(body + [body[5]], lab + [lab[5]], cl, 3, 7, "e8dup")
    assert c2[2] == p2[2] == "FAIL" and c2[0] == p2[0] > 0 and c3[:2] == p3[:2] and c3[0] > 0, (c2, p2, c3, p3)
    print(f"ok  class mode E8 split: PASS 6720 contacts; lowered table entry FAIL ({c2[0]}); duplicate row FAIL ({c3[0]})")


def chain_tests():
    import build_kravatskiy34 as b34
    D = b34.D
    parent = {"full_even_supports": [0xFF, 0xFF00], "stars": [], "removed_root_lines": [],
              "heavy_numerators_over_85": [], "counts": {"dense": 0, "middle": 256, "stars": 0, "roots": 2 * D * (D - 1)},
              "points": 0}
    wit = {"octads": [[1, list(range(8, 16)), list(range(16, 24))]], "stars": [[[30, 31, 32, 33, 29], 0]]}
    c = b34.edit(parent, wit)
    assert c["full_even_supports"] == [0xFF, 0xFF0000]
    assert len(c["stars"]) == 16 and all(v[30] in (4, -4) for v in c["stars"])
    # star centre 30, leaves 31, 32, 33, 29: the 4 lines (30, leaf, +-1) are
    # blocked in both signs, i.e. 8 lines, 16 roots
    assert len(c["removed_root_lines"]) == 8 and c["counts"]["roots"] == 2 * D * (D - 1) - 16
    assert c["points"] == 256 + 16 + 2 * D * (D - 1) - 16
    bad = {"octads": [[1, list(range(16, 24)), list(range(8, 16))]], "stars": wit["stars"]}
    try:
        b34.edit(parent, bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("mismatched switch accepted")
    print("ok  chain rebuild (toy 34D-format parent + witness): stars, root deletions, counts; bad switch rejected")


def partner_tests(D5, E8):
    rng = random.Random(20261126)
    e = list(E8)
    e[3] = tuple(list(e[3][:4]) + [e[3][4] + 1] + list(e[3][5:]))
    for name, rows, d in (("D5", D5, 5), ("E8", E8, 8), ("E8 dup", E8 + [E8[9]], 8), ("E8 perturbed", e, 8)):
        X = np.array(rows, dtype=np.int64)
        U = np.eye(d, dtype=np.int64)
        for _ in range(3 * d):  # random elementary operations, |entries| kept small
            i, j = rng.sample(range(d), 2)
            V = U.copy()
            V[i] += rng.choice((-1, 1)) * V[j]
            if np.abs(V).max() <= 2:
                U = V
        Ui = np.round(np.linalg.inv(U)).astype(np.int64)
        assert (U @ Ui == np.eye(d, dtype=np.int64)).all()
        C = X @ Ui
        G = U @ U.T
        assert (C @ G @ C.T == X @ X.T).all() and np.abs(C).max() <= 127 and np.abs(C @ G).max() <= 127
        pre = os.path.join(BUILD, "t_partner")
        C.astype(np.int8).tofile(pre + "_x.i8")
        (C @ G).astype(np.int8).tofile(pre + "_xg.i8")
        c = parse(subprocess.run([CBIN, pre + "_x.i8", str(d), "--partner", pre + "_xg.i8"],
                                 capture_output=True, text=True).stdout)
        p = parse(subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_np.py"), pre + "_x.i8", str(d),
                                  "--workers", "1", "--tile", "7", "--partner", pre + "_xg.i8"],
                                 capture_output=True, text=True).stdout)
        ref = run_c(rows, d, "partner_ref")
        assert c == p == ref and (ref[2] == "PASS") == (name in ("D5", "E8")), (name, c, p, ref)
        print(f"ok  partner mode {name:12s} (basis change, |U| <= 2): {c}")



def affine_tests(E8):
    """Section 10: class + partner modes with > 256 classes (40-43D format)."""
    from fractions import Fraction
    import build_kravatskiy4043 as b43
    rng = random.Random(20261125)
    ebin = os.path.join(BUILD, "enum_affine")
    subprocess.run(["gcc", "-O3", "-fopenmp", os.path.join(HERE, "enum_affine.c"), "-o", ebin, "-lm"], check=True)

    def basis(d):
        U = np.eye(d, dtype=np.int64)
        for _ in range(3 * d):
            i, j = rng.sample(range(d), 2)
            V = U.copy()
            V[i] += rng.choice((-1, 1)) * V[j]
            if np.abs(V).max() <= 2:
                U = V
        return U

    # enum_affine against brute force: x == c (mod 3), x G x^T == n
    d = 4
    U = basis(d)
    G = U @ U.T
    c = [1, 0, 2, 1]
    for n in (6, 9, 14):
        inp, out = os.path.join(BUILD, "t_enum.in"), os.path.join(BUILD, "t_enum.i8")
        with open(inp, "w") as f:
            f.write(f"{d} {n}\n" + "\n".join(" ".join(map(str, r)) for r in G) + "\n" + " ".join(map(str, c)) + "\n")
        cnt = int(subprocess.run([ebin, inp, out], capture_output=True, text=True, check=True).stdout.split()[0])
        R = range(-12, 13)
        ref = sum(1 for x in itertools.product(R, repeat=d)
                  if all((x[k] - c[k]) % 3 == 0 for k in range(d)) and int(np.array(x) @ G @ np.array(x)) == n)
        assert cnt == ref, (n, cnt, ref)
    print(f"ok  enum_affine affine shell counts equal brute force (norms 6, 9, 14)")

    def run(X, G, classes, lab, tag):
        """X int rows, G Gram (body metric G/3), classes (r, D, z), lab labels."""
        pre = os.path.join(BUILD, f"t_aff_{tag}")
        X = np.array(X, dtype=np.int64)
        assert all(int(x @ G @ x) == 3 * classes[l][0] for x, l in zip(X, lab))
        assert np.abs(X).max() <= 127 and np.abs(X @ G).max() <= 127
        X.astype(np.int8).tofile(pre + "_x.i8")
        (X @ G).astype(np.int8).tofile(pre + "_xg.i8")
        np.array(lab).astype("<u2").tofile(pre + ".lab")
        tab = b43.table(classes)
        with open(pre + ".tab", "w") as f:
            f.write(f"{len(classes)}\n")
            for (a, b), (T, C) in sorted(tab.items()):
                f.write(f"{a} {b} {T} {C}\n")
        dd = str(X.shape[1])
        args = [pre + "_x.i8", dd, pre + ".lab", pre + ".tab", "--partner", pre + "_xg.i8"]
        c = parse(subprocess.run([CBIN] + args, capture_output=True, text=True).stdout)
        parts, ppairs = [0, 0], 0
        for k in range(3):
            o = subprocess.run([CBIN] + args + ["--part", str(k), "3"], capture_output=True, text=True).stdout
            q = parse(o)
            parts[0] += q[0]
            parts[1] += q[1]
            ppairs += int(re.search(r"pairs_in_part (\d+)", o).group(1))
        n = len(X)
        assert ppairs == n * (n - 1) // 2 and tuple(parts) == c[:2], (ppairs, parts, c)
        p = parse(subprocess.run([sys.executable, os.path.join(HERE, "kiss_check_np.py"), pre + "_x.i8", dd,
                                  "--workers", "1", "--tile", "13", "--classes", pre + ".lab", pre + ".tab",
                                  "--partner", pre + "_xg.i8"], capture_output=True, text=True).stdout)
        # Fraction reference: v = (x, z/D), <v, v'> = x G y / 3 + z.w / (D E)
        V, C2 = 0, 0
        for i in range(n):
            for j in range(i + 1, n):
                (ra, Da, za), (rb, Db, zb) = classes[lab[i]], classes[lab[j]]
                ip = Fraction(int(X[i] @ G @ X[j]), 3) + Fraction(sum(u * v for u, v in zip(za, zb)), Da * Db)
                A = ra + Fraction(sum(u * u for u in za), Da * Da)
                B = rb + Fraction(sum(u * u for u in zb), Db * Db)
                V += ip > 0 and 4 * ip * ip > A * B
                C2 += ip > 0 and 4 * ip * ip == A * B
        assert c[:2] == p[:2] == (V, C2), (tag, c, p, V, C2)
        return c

    seen = {True: 0, False: 0}
    for t in range(6):
        d = 5
        U = basis(d)
        G = 3 * (U @ U.T)
        k = 300
        D = rng.choice((1, 7, 10**6 + 3))
        classes, X, lab = [], [], []
        for _ in range(k):
            x = [rng.randint(-2, 2) for _ in range(d)]
            while np.abs(np.array(x) @ G).max() > 127 or int(np.array(x) @ G @ np.array(x)) > 54:
                x = [rng.randint(-1, 1) for _ in range(d)]
            if not any(x) and rng.random() < 0.5:
                r = 0
            else:
                x = x if any(x) else [1] + [0] * (d - 1)
                r = int(np.array(x) @ G @ np.array(x)) // 3
            z = [rng.randint(-3 * D, 3 * D) for _ in range(2)]
            if r == 0 and not any(z):
                z = [D, 0]
            classes.append((r, D, z))
            X.append(x)
            lab.append(len(classes) - 1)
            if r and rng.random() < 0.3:  # a second body of the same class (same norm: -x)
                X.append([-v for v in x])
                lab.append(len(classes) - 1)
        if t % 2:  # keep a greedy valid subset (by the Fraction test), so the set passes
            keep = []
            for i in range(len(X)):
                ok = True
                for j in keep:
                    (ra, Da, za), (rb, Db, zb) = classes[lab[i]], classes[lab[j]]
                    ip = Fraction(int(np.array(X[i]) @ G @ np.array(X[j])), 3) + Fraction(
                        sum(u * v for u, v in zip(za, zb)), Da * Db)
                    A = ra + Fraction(sum(u * u for u in za), Da * Da)
                    B = rb + Fraction(sum(u * u for u in zb), Db * Db)
                    if ip > 0 and 4 * ip * ip > A * B:
                        ok = False
                        break
                if ok:
                    keep.append(i)
            X, lab = [X[i] for i in keep], [lab[i] for i in keep]
        c = run(X, G, classes, lab, f"r{t}")
        seen[c[2] == "PASS"] += 1
        assert (c[2] == "PASS") == (t % 2 == 1), (t, c)
    # E8 over 300 zero-head classes, with D varying: passes with 6720 contacts
    G = 3 * np.eye(8, dtype=np.int64)
    rows = [list(r) for r in E8]
    classes = [(8, rng.choice((1, 5, 10**9)), [0, 0]) for _ in range(300)]
    lab = [rng.randrange(300) for _ in rows]
    c = run(rows, G, classes, lab, "e8")
    assert c == (0, 6720, "PASS"), c
    c2 = run(rows + [rows[4]], G, classes, lab + [lab[4]], "e8dup")
    assert c2[2] == "FAIL"
    print(f"ok  affine class+partner mode, 300 classes (uint16 labels): {seen[False]} random sets fail, "
          f"{seen[True]} pass, C (whole and 3 parts) = numpy = Fraction reference; E8 PASS 6720, duplicate FAIL")


if __name__ == "__main__":
    main()
