"""Level-one completeness for one LRC(14) gate: regenerate the orbits of
I(14,p,1) independently and compare with the certificate's stored rows.

Usage: python3 completeness_check.py evidence_<p>_s0.tgz [COVERS_FILE]
  COVERS_FILE: optional, precomputed covergen.c output (e.g. the
  concatenation of a sharded run, LRC_NSHARDS/LRC_SHARD); otherwise
  covergen.c is run here.

Ours:   covergen.c (all minimal covers containing class 1; completeness
        proof in its header), expanded to every k-multiset C + extras and
        reduced to unit-orbit canonical forms by canon.c.  This is WITHOUT
        Allikvere's private-time pruning, so it enumerates I(14,p,1)
        exhaustively by the argument in covergen.c alone.
Theirs: rows_ir/*.txt and rows_km1/*.txt (each km1 multiset extended by
        every class), reduced to canonical forms the same way.
Pass:   the two orbit sets are equal.  (Theirs must also be a subset of
        ours, since every stored row is improper.)
"""
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_gate_full import binary, decode  # noqa: E402


def main():
    tgz = sys.argv[1]
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="lrc_ev_")
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp, filter="data")
    (sub,) = [d for d in os.listdir(tmp) if d.startswith("out_")]
    root = os.path.join(tmp, sub)
    summ = json.load(open(os.path.join(root, "SUMMARY.json")))
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    h = (p - 1) // 2
    # ours
    t1 = time.time()
    if len(sys.argv) > 2:
        class _C:
            stderr = "precomputed covers: %s" % sys.argv[2]
        cov = _C()
        with open(sys.argv[2]) as fin:
            ours_p = subprocess.run([binary("canon"), str(k), str(p), "expand"], stdin=fin,
                                    capture_output=True, text=True, check=True)
    else:
        cov = subprocess.run([binary("covergen"), str(k), str(p)], capture_output=True, text=True, check=True)
        ours_p = subprocess.run([binary("canon"), str(k), str(p), "expand"], input=cov.stdout,
                                capture_output=True, text=True, check=True)
    ours = {tuple(map(int, l.split())) for l in ours_p.stdout.splitlines()}
    t_ours = time.time() - t1
    # theirs
    rows = []
    for fn in sorted(os.listdir(os.path.join(root, "rows_ir"))):
        if fn.endswith(".txt"):
            rows += decode(os.path.join(root, "rows_ir", fn), k)
    km1 = set()
    d = os.path.join(root, "rows_km1")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".txt"):
                km1 |= set(decode(os.path.join(d, fn), k - 1))
    lines = [" ".join(map(str, r)) for r in rows] + \
            [" ".join(map(str, c + (x,))) for c in sorted(km1) for x in range(1, h + 1)]
    th = subprocess.run([binary("canon"), str(k), str(p), "rows"], input="\n".join(lines) + "\n",
                        capture_output=True, text=True, check=True)
    theirs = {tuple(map(int, l.split())) for l in th.stdout.splitlines()}
    # rows we formed from km1 covers that are not improper are dropped by
    # neither side's definition: a km1 multiset is a cover, so every
    # extension is improper; report anyway.
    rep = {"p": p, "k": k, "covergen_stderr": cov.stderr.strip(), "canon_ours": ours_p.stderr.strip(),
           "canon_theirs": th.stderr.strip(), "orbits_ours": len(ours), "orbits_cert": len(theirs),
           "only_ours": len(ours - theirs), "only_cert": len(theirs - ours),
           "examples_only_ours": sorted(ours - theirs)[:10], "examples_only_cert": sorted(theirs - ours)[:10],
           "equal": ours == theirs, "seconds_ours_generation": round(t_ours, 1),
           "seconds_total": round(time.time() - t0, 1),
           "pruning": "none (covergen.c minimal covers; Allikvere's private-time normalisation NOT used)"}
    print(json.dumps(rep), flush=True)


if __name__ == "__main__":
    main()
