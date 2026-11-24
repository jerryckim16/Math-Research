"""End-to-end certificate pipeline for "unit-distance graph G is not k-colourable".

  1. build G with exact coordinates (graphs.py), find edges, confirm each
     edge EXACTLY (|p-q|^2 = 1 in Q(sqrt3, sqrt5, sqrt11));
  2. independent second exact pass over the final edge list;
  3. encode k-colourability (encode.py) with a unit triangle fixed to
     colours 0,1,2 (soundness argued in encode.py);
  4. solve with CaDiCaL --lrat; on UNSAT check the LRAT proof with our own
     checker (computations/erdos-szekeres/lrat_check.py); on SAT decode and
     verify the colouring.

Usage: python3 run_pipeline.py {moser|v31|v151|v1939|heule} K WORKDIR [--keep-proof]
Prints a one-line JSON summary at the end.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import importlib.util  # noqa: E402

import graphs  # noqa: E402
import encode  # noqa: E402

# Reuse the repository's own LRAT checker (loaded by path: the
# erdos-szekeres directory also has a module named encode).
_spec = importlib.util.spec_from_file_location(
    "lrat_check", os.path.join(HERE, "..", "erdos-szekeres", "lrat_check.py"))
lrat_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lrat_check)


def build(name):
    if name == "moser":
        return graphs.moser_spindle()
    v31 = graphs.heule_v31()
    if name == "v31":
        return v31
    v151 = graphs.heule_v151(v31)
    if name == "v151":
        return v151
    v1939 = graphs.heule_v1939(v31, v151)
    if name == "v1939":
        return v1939
    if name == "heule":
        return graphs.heule_g(v1939)
    raise ValueError(name)


def origin_index(points):
    for i, p in enumerate(points):
        if p == graphs.unit(0):
            return i
    return 0


def run(name, k, work, keep_proof=False, solver_args=()):
    os.makedirs(work, exist_ok=True)
    t0 = time.time()
    pts = build(name)
    edges, cand, rej = graphs.unit_edges(pts)
    assert rej == 0, "float candidates rejected by exact test"
    assert graphs.verify_edges_exact(pts, edges)
    t_build = time.time() - t0
    tri = graphs.find_triangle(pts, edges, anchor=origin_index(pts))
    clique = tri[:min(3, k)] if tri else ()
    assert encode.is_clique(edges, clique)
    nv, cls = encode.colouring_cnf(len(pts), edges, k, clique)
    cnf = os.path.join(work, f"{name}_k{k}.cnf")
    encode.write_dimacs(cnf, nv, cls)
    sha = hashlib.sha256(open(cnf, "rb").read()).hexdigest()
    proof = os.path.join(work, f"{name}_k{k}.lrat")
    t1 = time.time()
    r = subprocess.run(["cadical", "-q", *solver_args, "--lrat=true", "--binary=false",
                        cnf, proof], capture_output=True, text=True)
    t_solve = time.time() - t1
    out = {"graph": name, "k": k, "vertices": len(pts), "edges": len(edges),
           "float_candidates": cand, "exact_rejected": rej, "clique": list(clique),
           "cnf_vars": nv, "cnf_clauses": len(cls), "cnf_sha256": sha,
           "build_s": round(t_build, 2), "solve_s": round(t_solve, 2)}
    if r.returncode == 20:
        out["result"] = "UNSAT"
        out["proof_bytes"] = os.path.getsize(proof)
        t2 = time.time()
        out["lrat_lemmas"] = lrat_check.check(cnf, proof)
        out["lrat_check_s"] = round(time.time() - t2, 2)
        out["lrat"] = "VERIFIED"
    elif r.returncode == 10:
        out["result"] = "SAT"
        model = set()
        for line in r.stdout.splitlines():
            if line.startswith("v "):
                model.update(int(t) for t in line.split()[1:] if t != "0")
        col = encode.decode(model, len(pts), k)
        assert encode.is_proper(edges, col)
        out["colouring_checked"] = True
    else:
        raise RuntimeError(f"cadical exit {r.returncode}: {r.stderr[:500]}")
    if not keep_proof and os.path.exists(proof):
        os.remove(proof)
    return out


if __name__ == "__main__":
    name, k, work = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    res = run(name, k, work, keep_proof="--keep-proof" in sys.argv)
    print(json.dumps(res))
