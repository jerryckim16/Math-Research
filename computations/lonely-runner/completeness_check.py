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


def compare_files(k, p, h, root, covers_path, t0):
    """Disk-based comparison (LRC_COMPARE_FILES=1, step 17): the same orbit
    sets as main(), but canonical forms are written to files and compared
    with LC_ALL=C sort -u and comm, so memory does not grow with the orbit
    count.  Report fields are the same as main()'s."""
    tmpd = tempfile.mkdtemp(prefix="lrc_cmp_")
    ours_f, theirs_f, rows_f = (os.path.join(tmpd, n) for n in ("ours", "theirs", "rows"))
    t1 = time.time()
    with open(covers_path) as fin, open(ours_f + ".raw", "w") as fo:
        ours_p = subprocess.run([binary("canon"), str(k), str(p), "expand"], stdin=fin, stdout=fo,
                                stderr=subprocess.PIPE, text=True, check=True)
    t_ours = time.time() - t1
    with open(rows_f, "w") as fo:
        for fn in sorted(os.listdir(os.path.join(root, "rows_ir"))):
            if fn.endswith(".txt"):
                for r in decode(os.path.join(root, "rows_ir", fn), k):
                    fo.write(" ".join(map(str, r)) + "\n")
        km1 = set()
        d = os.path.join(root, "rows_km1")
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".txt"):
                    km1 |= set(decode(os.path.join(d, fn), k - 1))
        for c in sorted(km1):
            for x in range(1, h + 1):
                fo.write(" ".join(map(str, c + (x,))) + "\n")
    with open(rows_f) as fin, open(theirs_f + ".raw", "w") as fo:
        th = subprocess.run([binary("canon"), str(k), str(p), "rows"], stdin=fin, stdout=fo,
                            stderr=subprocess.PIPE, text=True, check=True)
    env = dict(os.environ, LC_ALL="C")
    for f in (ours_f, theirs_f):
        subprocess.run(["sort", "-u", "-S", "1G", "-T", tmpd, "-o", f, f + ".raw"], env=env, check=True)
        os.remove(f + ".raw")
    os.remove(rows_f)
    count = lambda f: int(subprocess.run(["wc", "-l", f], capture_output=True, text=True).stdout.split()[0])
    def comm(flag):
        out = subprocess.run(["comm", flag, ours_f, theirs_f], capture_output=True, text=True, env=env).stdout.splitlines()
        return len(out), [tuple(map(int, l.split())) for l in out[:10]]
    n_ours, n_theirs = count(ours_f), count(theirs_f)
    only_ours, ex_o = comm("-23")
    only_cert, ex_c = comm("-13")
    rep = {"p": p, "k": k, "covergen_stderr": "precomputed covers: %s" % covers_path, "canon_ours": ours_p.stderr.strip(),
           "canon_theirs": th.stderr.strip(), "orbits_ours": n_ours, "orbits_cert": n_theirs,
           "only_ours": only_ours, "only_cert": only_cert, "examples_only_ours": ex_o, "examples_only_cert": ex_c,
           "equal": only_ours == 0 and only_cert == 0 and n_ours == n_theirs,
           "seconds_ours_generation": round(t_ours, 1), "seconds_total": round(time.time() - t0, 1),
           "comparison": "files (LC_ALL=C sort -u, comm)",
           "pruning": "see covergen_stderr"}
    for f in (ours_f, theirs_f):
        os.remove(f)
    print(json.dumps(rep), flush=True)


def main():
    tgz = sys.argv[1]
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="lrc_ev_")
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp, filter="data")
    (sub,) = [d for d in os.listdir(tmp) if d.startswith("out") and os.path.isdir(os.path.join(tmp, d))]   # out_<p> (k = 14) or out15_<p> (k = 15)
    root = os.path.join(tmp, sub)
    summ = json.load(open(os.path.join(root, "SUMMARY.json")))
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    h = (p - 1) // 2
    if os.environ.get("LRC_COMPARE_FILES") == "1" and len(sys.argv) > 2:
        return compare_files(k, p, h, root, sys.argv[2], t0)
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
