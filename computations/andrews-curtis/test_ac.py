"""Tests for the independent Andrews-Curtis certificate checker and search.

Run: python3 test_ac.py     (a few seconds; compiles ac_search.cpp with g++)
"""
import json
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ac_check as A  # noqa: E402
import ac_path  # noqa: E402

CERTS = os.path.join(HERE, "certs")


def rand_word(rng, n):
    return A.reduce([rng.choice(A.GENS) for _ in range(n)])


def test_basics():
    assert A.reduce((1, -1, 2, 2, -2, 1)) == (2, 1)
    assert A.inv((1, 2, -1)) == (1, -2, -1)
    assert A.word("x^-1 y^2 x y^-3") == (-1, 2, 2, 1, -2, -2, -2)
    assert A.apply(((1, 2, 2), (2,)), ["cycle", 0, 1]) == ((2, 2, 1), (2,))
    assert A.apply(((1, 2), (2,)), ["conj", 0, -1]) == ((2, 1), (2,))
    assert A.apply(((1, 2), (-2, 1)), ["mul", 0, 1, 1]) == ((1, 1), (-2, 1))
    for bad in (["mul", 0, 0, 1], ["mul", 0, 1, 2], ["conj", 0, 3], ["frob", 0], ["invert", 2]):
        try:
            A.apply(((1,), (2,)), bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted {bad}")


def test_swap_and_bridge():
    rng = random.Random(1)
    for _ in range(300):
        a, b = rand_word(rng, rng.randint(1, 9)), rand_word(rng, rng.randint(1, 9))
        if not a or not b:
            continue
        assert A.replay((a, b), A.swap_moves((a, b)))[0] == (b, a)
    for _ in range(300):
        a = A.reduce(rand_word(rng, 8))
        b = A.reduce(rand_word(rng, 7))
        if not (a and b and A.is_cyclically_reduced(a) and A.is_cyclically_reduced(b)):
            continue
        k1, k2 = rng.randrange(len(a)), rng.randrange(len(b))
        t = (A.inv(b[k2:] + b[:k2]), a[k1:] + a[:k1])     # swapped, rotated, one inverted
        br = A.bridge((a, b), t)
        assert br is not None and A.replay((a, b), br)[0] == t
    # not in the orbit
    assert A.bridge(((1, 2), (2,)), ((1, 1), (2,))) is None


def test_abelianization_invariant():
    rng = random.Random(2)
    for _ in range(200):
        s = (rand_word(rng, 6), rand_word(rng, 6))
        d0 = abs(A.abelian_det(s))
        for _ in range(20):
            op = rng.choice(["invert", "mul", "conj", "cycle"])
            i = rng.randrange(2)
            mv = {"invert": ["invert", i], "mul": ["mul", i, 1 - i, rng.choice((1, -1))],
                  "conj": ["conj", i, rng.choice(A.GENS)], "cycle": ["cycle", i, rng.randrange(7)]}[op]
            s = A.apply(s, mv)
            assert abs(A.abelian_det(s)) == d0


def test_named_presentations():
    assert sum(map(len, A.AK(3))) == 13 and sum(map(len, A.AK(2))) == 11
    for w in ("y x^2 y", "y^-1 x^2 y^-1"):
        assert sum(map(len, A.MS(3, w))) == 14
    # the paper's P1 is MS(2, x^-2 y^-1 x^2 y) up to rotation
    assert A.bridge(A.P1_CLASSICAL, A.MS(2, "x^-2 y^-1 x^2 y")) is not None
    # Shehper et al. print the MS(3) cases as x = y^{+-1} x^2 y^{+-1}; their released
    # data has MS(3, y x y x^-1) and MS(3, x^-1 y^-1 x y^-1).  These agree up to
    # rotation + inversion, with the signs crossed:
    assert A.bridge(A.MS(3, "y^-1 x^2 y^-1"), A.MS(3, "y x y x^-1")) is not None
    assert A.bridge(A.MS(3, "y x^2 y"), A.MS(3, "x^-1 y^-1 x y^-1")) is not None
    assert A.bridge(A.MS(3, "y x^2 y"), A.MS(3, "y x y x^-1")) is None


def _certs():
    return {f: A.load(os.path.join(CERTS, f)) for _, (_, _, f) in A.THEOREMS.items()}


def test_theorems_1_to_4():
    certs = _certs()
    expect = {"cert_sym_equiv_orphan1.json": (36, 58, 27, 17),
              "cert_idx0_equiv_mirror.json": (85, 155, 33, 21),
              "bottleneck_ak_f3_cert.json": (66, 101, 24, 15),
              "cert_ms3_yx2y_equiv_ak3.json": (71, 106, 22, 15),
              "cert_ms3_yinvx2yinv_equiv_ak3.json": (13, 22, 23, 14)}
    for name, (Pa, Pb, f) in A.THEOREMS.items():
        ok, info = A.check_cert(certs[f])
        assert ok, (name, info)
        assert (info["packaged"], info["classical"], info["peak_total"], info["peak_single"]) == expect[f]
        A.prove_named(Pa, Pb, certs[f])


def test_our_certificates():
    """Certificates found by our own search (ac_search + ac_path)."""
    ours = os.path.join(HERE, "certs_ours")
    cases = {"ms3_yx2y_to_ak3.json": (A.MS(3, "y x^2 y"), A.AK(3)),
             "ms3_yinvx2yinv_to_ak3.json": (A.MS(3, "y^-1 x^2 y^-1"), A.AK(3)),
             "ak2_trivial.json": (A.AK(2), ((1,), (2,)))}
    for f, (Pa, Pb) in cases.items():
        d = A.load(os.path.join(ours, f))
        assert A.check_cert(d)[0], f
        A.prove_named(Pa, Pb, d)


def test_tampered_certificates_rejected():
    rng = random.Random(3)
    certs = _certs()
    for f, d in certs.items():
        for trial in range(25):
            e = json.loads(json.dumps(d))
            k = rng.randrange(len(e["moves"]))
            mv = e["moves"][k]
            if mv[0] == "mul":
                mv[3] = -mv[3]
            elif mv[0] == "conj":
                mv[2] = -mv[2]
            elif mv[0] == "cycle":
                mv[2] += 1
            else:
                e["moves"][k] = ["conj", mv[1], 1]
            ok, _ = A.check_cert(e)
            assert not ok, (f, k, mv)
        # same moves, wrong target
        e = json.loads(json.dumps(d))
        e["target"][1] = list(A.reduce(e["target"][1] + [1, 1]))
        e.pop("reached", None)
        assert not A.check_cert(e)[0]
    # a valid certificate attached to the wrong named presentation
    try:
        A.prove_named(A.MS(3, "y x^2 y"), A.AK(3), certs["cert_ms3_yinvx2yinv_equiv_ak3.json"])
    except AssertionError:
        pass
    else:
        raise AssertionError("wrong endpoints accepted")


def test_search_pipeline():
    tmp = tempfile.mkdtemp()
    exe = os.path.join(tmp, "ac_search")
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", exe, os.path.join(HERE, "ac_search.cpp")], check=True)
    # AK(2) is AC-trivial (Miasnikov); our search must find and certify it
    out = os.path.join(tmp, "ak2.out")
    with open(out, "w") as f:
        subprocess.run([exe, "14", "xxYYY/xyxYXY", "+", "x/y"], stdout=f, check=True)
    assert ac_path.main(out, "xxYYY/xyxYXY", "x/y", os.path.join(tmp, "ak2.json")) == 0
    # AK(3) and the trivial presentation are not joined below total length 14
    r = subprocess.run([exe, "14", "--junction", "xxxYYYY/xyxYXY", "+", "x/y"], capture_output=True, text=True)
    assert "EXHAUSTED" in r.stdout
    # a corrupted path is rejected by the expansion step
    lines = open(out).read().split("\n")
    i = lines.index("PATH") + 2
    lines[i] = "XXyyy|XYXYXY"
    bad = os.path.join(tmp, "bad.out")
    open(bad, "w").write("\n".join(lines))
    try:
        ac_path.main(bad, "xxYYY/xyxYXY", "x/y", os.path.join(tmp, "bad.json"))
    except AssertionError:
        pass
    else:
        raise AssertionError("corrupted path accepted")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all tests passed")
