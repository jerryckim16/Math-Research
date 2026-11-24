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
"""
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
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
