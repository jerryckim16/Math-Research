"""Tests for the chromatic-number-of-the-plane computations.

Run: python3 test_chromatic_plane.py          (about 10 s)
     CNP_HEAVY=1 python3 test_chromatic_plane.py   (adds the 3877-vertex
     chi >= 5 certificate: about 30 s and a 57 MB temporary LRAT proof)
"""
import itertools
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import qfield as Q  # noqa: E402
import graphs  # noqa: E402
import encode  # noqa: E402
import run_pipeline  # noqa: E402
import cert_section8 as C8  # noqa: E402


def test_field():
    s3, s5, s11 = Q.root(3), Q.root(5), Q.root(11)
    assert Q.mul(s3, s3) == Q.const(3)
    assert Q.mul(s3, s5) == Q.root(15)
    assert Q.mul(Q.root(15), Q.root(33)) == Q.root(55, 3)
    assert Q.mul(Q.root(165), Q.root(165)) == Q.const(165)
    for r in (graphs.THETA1, graphs.THETA3, graphs.THETA3_HALF, graphs.THETA4):
        assert Q.is_rotation(r)
    assert Q.compose(graphs.THETA3_HALF, graphs.THETA3_HALF) == graphs.THETA3
    assert graphs.rot_power(graphs.THETA1, 6) == graphs.IDENTITY
    x = Q.add(Q.root(3, F(1, 7)), Q.root(55, F(-2, 3)))
    assert abs(Q.approx(Q.mul(x, x)) - Q.approx(x) ** 2) < 1e-12


def test_counts_match_heule():
    v31 = graphs.heule_v31()
    e31, _, rej = graphs.unit_edges(v31)
    assert (len(v31), len(e31), rej) == (31, 60, 0)
    v151 = graphs.heule_v151(v31)
    e151, _, rej = graphs.unit_edges(v151)
    assert (len(v151), len(e151), rej) == (151, 510, 0)
    assert len(graphs.heule_v1939(v31, v151)) == 1939


def test_exact_edge_check_has_teeth():
    pts = graphs.moser_spindle()
    edges, _, _ = graphs.unit_edges(pts)
    assert len(pts) == 7 and len(edges) == 11
    assert graphs.verify_edges_exact(pts, edges)
    # a pair at distance sqrt3 is not accepted
    nonedge = [(i, j) for i, j in itertools.combinations(range(7), 2)
               if (i, j) not in edges][0]
    assert not graphs.verify_edges_exact(pts, [nonedge])
    # perturbing one coordinate by 1e-30 breaks exact unit length
    p = list(pts)
    i, j = edges[0]
    p[i] = (Q.add(p[i][0], Q.const(F(1, 10 ** 30))), p[i][1])
    assert not graphs.verify_edges_exact(p, [(i, j)])


def _brute_colourable(n, edges, k):
    for col in itertools.product(range(k), repeat=n):
        if all(col[a] != col[b] for a, b in edges):
            return True
    return False


def _cadical_sat(nv, cls):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "f.cnf")
        encode.write_dimacs(path, nv, cls)
        r = subprocess.run(["cadical", "-q", "-n", path], capture_output=True)
        assert r.returncode in (10, 20)
        return r.returncode == 10


def test_encoding_with_symmetry_breaking_is_equisatisfiable():
    rng = random.Random(1)
    for trial in range(150):
        n = rng.randint(3, 8)
        k = rng.randint(2, 4)
        es = [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5]
        # pick a clique greedily for symmetry breaking (size <= k)
        adj = {v: set() for v in range(n)}
        for a, b in es:
            adj[a].add(b); adj[b].add(a)
        clique = []
        for v in rng.sample(range(n), n):
            if len(clique) < k and all(v in adj[c] for c in clique):
                clique.append(v)
        assert encode.is_clique(es, clique)
        nv, cls = encode.colouring_cnf(n, es, k, clique)
        assert _cadical_sat(nv, cls) == _brute_colourable(n, es, k), (n, k, es, clique)


def test_moser_pipeline_and_tamper():
    with tempfile.TemporaryDirectory() as d:
        r3 = run_pipeline.run("moser", 3, d, keep_proof=True)
        assert r3["result"] == "UNSAT" and r3["lrat"] == "VERIFIED"
        cnf = os.path.join(d, "moser_k3.cnf")
        proof = os.path.join(d, "moser_k3.lrat")
        lines = open(proof).read().splitlines()
        # tamper: drop the first hint of the first addition step
        for t, line in enumerate(lines):
            toks = line.split()
            if toks[1] != "d":
                z = toks.index("0", 1)
                if len(toks) > z + 2:
                    del toks[z + 1]
                    lines[t] = " ".join(toks)
                    break
        bad = os.path.join(d, "bad.lrat")
        open(bad, "w").write("\n".join(lines) + "\n")
        try:
            run_pipeline.lrat_check.check(cnf, bad)
            raise AssertionError("tampered proof accepted")
        except ValueError:
            pass
        r4 = run_pipeline.run("moser", 4, d)
        assert r4["result"] == "SAT" and r4["colouring_checked"]


def test_section8_certificate():
    assert C8.main()


def test_section8_certificate_has_teeth():
    names, pts, edges, u = C8.moser_graph()
    # A different translation (the text-extraction misreading g*rot + shift)
    # puts several vertices outside region (8.4); the check must notice.
    bad = [Q.padd(C8.cmul(C8.ROT, p), C8.SHIFT) for p in pts]
    fails = 0
    for z in bad:
        l, fml, P, P2 = C8.region_quantities(z)
        if C8.sign(Q.sub(P2, P)) != 1:
            fails += 1
    assert fails == 3
    # the table check rejects a centre moved by 2h
    z = C8.place(pts[0])
    _, _, P, P2 = C8.region_quantities(z)
    saved = C8.TABLE1["0"]
    C8.TABLE1["0"] = ("-1.2908", saved[1], saved[2], saved[3])
    try:
        assert not C8.check_tables("0", z, P, P2)
    finally:
        C8.TABLE1["0"] = saved


def test_heule_chi_ge_5_heavy():
    if os.environ.get("CNP_HEAVY") != "1":
        print("  (skipped; set CNP_HEAVY=1)")
        return
    with tempfile.TemporaryDirectory() as d:
        r = run_pipeline.run("heule", 4, d)
        print("  ", r)
        assert (r["vertices"], r["edges"]) == (3877, 26814)
        assert r["result"] == "UNSAT" and r["lrat"] == "VERIFIED"
        assert r["cnf_sha256"] == "f012031c250da4ee59928d7e8833321c6bbf633b90cdb548abcb0164baed992f"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            print(name)
            fn()
    print("all tests passed")
