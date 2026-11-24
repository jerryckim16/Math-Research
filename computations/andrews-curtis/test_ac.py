"""Tests for the independent Andrews-Curtis certificate checker and search.

Run: python3 test_ac.py     (about 2 minutes; compiles the C++ engines with g++;
     most of the time is the Python edge-set check below energy 20)
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
import ac_graph as G  # noqa: E402
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
    # the compact engine explores the same graph: identical per-level counts
    exe2 = os.path.join(tmp, "ac_compact")
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", exe2, os.path.join(HERE, "ac_search_compact.cpp")], check=True)
    srcs = ["xxxYYYY/xyxYXY", "+", "XyyxYYY/XXXYxxy", "+", "XyyxYYY/XXXYxxY"]
    r1 = subprocess.run([exe, "21", "--junction"] + srcs, capture_output=True, text=True).stdout
    r2 = subprocess.run([exe2, "21", "--maxstates", "200000"] + srcs, capture_output=True, text=True).stdout
    lv = lambda r: [l.split("per source:")[1] for l in r.splitlines() if l.startswith("level")]
    assert lv(r1) == lv(r2) and lv(r1)[-1].split() == ["38612", "945", "521"], (lv(r1)[-1:], lv(r2)[-1:])
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


# --- the GS graph in both directions (ac_graph.py; --undirected engines) ----

AK3, P1, P2 = "xxxYYYY/xyxYXY", "XyyxYYY/XXXYxxy", "XyyxYYY/XXXYxxY"
P3, P4 = "XyyyxYYYY/Xyxxy", "XyyyxYYYY/XYxxY"


def _gkey(s):
    a, b = s.split("/")
    return G.key(G.cycred(G.parse(a)), G.cycred(G.parse(b)))


def test_predecessors_exhaustive():
    """pred() equals the inverted forward map on EVERY state of energy <= 9
    (and, run by hand, <= 12: 0 mismatches)."""
    import itertools
    E = 9
    words = {()}
    for n in range(1, E):
        for t in itertools.product(range(4), repeat=n):
            if G.reduced(t) and G.cyc_reduced(t):
                words.add(G.canon(t))
    states = {tuple(sorted((a, b))) for a in words for b in words if (a or b) and len(a) + len(b) <= E}
    into = {s: set() for s in states}
    for s in states:
        for t in G.forward(s, E + 1):
            into[t].add(s)
    assert len(states) == 4244 and sum(map(len, into.values())) == 9301
    for s in states:
        assert G.pred(s, E + 1) == into[s], s


def test_edge_sets_below_20():
    """The closure of {AK(3), P1, P2} below energy 20: forward edges as in the
    problem file (20,236 states, 79,752 edges, 168 one-way); in the undirected
    closure the forward edges and the predecessor edges are the same set."""
    def closure(undirected):
        seen = {_gkey(x) for x in (AK3, P1, P2)}
        st, F, P = list(seen), {}, {}
        while st:
            s = st.pop()
            F[s] = G.forward(s, 20)
            nb = set(F[s])
            if undirected:
                P[s] = G.pred(s, 20)
                nb |= P[s]
            for n in nb - seen:
                seen.add(n)
                st.append(n)
        return seen, F, P
    seen, F, _ = closure(False)
    E1 = {(a, b) for a in F for b in F[a]}
    assert (len(seen), len(E1), sum((b, a) not in E1 for a, b in E1)) == (20236, 79752, 168)
    seen, F, P = closure(True)
    E1 = {(a, b) for a in F for b in F[a]}
    E2 = {(a, b) for b in P for a in P[b]}
    assert E1 == E2
    assert (len(seen), len(E1), sum((b, a) not in E1 for a, b in E1)) == (20656, 80172, 588)


def test_inverse_moves():
    rng = random.Random(4)
    for _ in range(200):
        s = (rand_word(rng, 7), rand_word(rng, 6))
        mv = [rng.choice([["invert", rng.randrange(2)], ["mul", 0, 1, rng.choice((1, -1))],
                          ["mul", 1, 0, rng.choice((1, -1))], ["conj", rng.randrange(2), rng.choice(A.GENS)],
                          ["cycle", rng.randrange(2), rng.randrange(9)]]) for _ in range(12)]
        t = A.replay(s, mv)[0]
        assert A.replay(t, ac_path.inverse_moves(s, mv))[0] == s


def test_undirected_search():
    tmp = tempfile.mkdtemp()
    par, comp = os.path.join(tmp, "par"), os.path.join(tmp, "comp")
    subprocess.run(["g++", "-O2", "-std=c++17", "-pthread", "-o", par, os.path.join(HERE, "ac_search_par.cpp")], check=True)
    subprocess.run(["g++", "-O2", "-std=c++17", "-o", comp, os.path.join(HERE, "ac_search_compact.cpp")], check=True)
    run = lambda *a: subprocess.run(list(a), capture_output=True, text=True).stdout
    srcs = [AK3, "+", P1, "+", P2]
    # both engines, cap 20: the per-source components (Python: 20,656 states in all)
    r = run(par, "20", "--slots", "1000000", "--undirected", *srcs)
    assert "per group: 20024 399 233 0" in r and "EXHAUSTED" in r, r
    r = run(comp, "20", "--maxstates", "100000", "--undirected", *srcs)
    assert "per source: 20024 399 233" in r and "EXHAUSTED" in r, r
    # directed mode unchanged
    assert "per group: 38612 945 521 0" in run(par, "21", "--slots", "1000000", *srcs)
    # positive controls: P3, P4 ~ AK(3) at undirected bottleneck exactly 19
    for p in (P3, P4):
        assert "EXHAUSTED" in run(comp, "19", "--maxstates", "100000", "--undirected", p, "+", AK3)
        out = os.path.join(tmp, "p.out")
        open(out, "w").write(run(comp, "20", "--maxstates", "1000000", "--undirected", p, "+", AK3))
        assert ac_path.main(out, p, AK3, os.path.join(tmp, "p.json")) == 0
    # AK(2) ~ trivial is found undirected too; AK(3), trivial not joined below 14
    out = os.path.join(tmp, "ak2.out")
    open(out, "w").write(run(comp, "14", "--undirected", "xxYYY/xyxYXY", "+", "x/y"))
    assert ac_path.main(out, "xxYYY/xyxYXY", "x/y", os.path.join(tmp, "ak2.json")) == 0
    assert "EXHAUSTED" in run(comp, "14", "--undirected", AK3, "+", "x/y")
    # a path that needs a backward edge: S -> AK(3) is one-way (problem file, "Directedness")
    S = "XXXyyyyxyxYXY/XYXyxy"
    assert _gkey(AK3) in G.forward(_gkey(S), 100) and _gkey(S) not in G.forward(_gkey(AK3), 100)
    r = run(comp, "20", "--undirected", AK3, "--passive", S)
    assert "MEET at level 13" in r, r      # directed, AK(3) first reaches S at level 19
    out = os.path.join(tmp, "back.out")
    open(out, "w").write(r)
    assert ac_path.main(out, AK3, S, os.path.join(tmp, "back.json")) == 0
    d = A.load(os.path.join(tmp, "back.json"))
    assert A.check_cert(d)[0] and tuple(map(tuple, d["initial"])) == A.replay(A.AK(3), [])[0]
    # a pair of states that is not an edge is rejected by the expansion
    assert _gkey(P3) not in G.forward(_gkey(AK3), 100) and _gkey(AK3) not in G.forward(_gkey(P3), 100)
    open(out, "w").write("PATH\nXXXyyyy|XYXyxy\nXyyyxYYYY|Xyxxy\nEND\n")
    try:
        ac_path.main(out, AK3, P3, os.path.join(tmp, "bad.json"))
    except AssertionError as e:
        assert "not an edge" in str(e), e
    else:
        raise AssertionError("non-edge accepted")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all tests passed")
