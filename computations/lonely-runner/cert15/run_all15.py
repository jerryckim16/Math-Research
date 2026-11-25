"""Run check_gate15.py on every LRC(15) gate archive, one at a time (1 core),
cheapest first, writing results/gate_<p>.json.  Gates that already have a
result file are skipped.  Each archive is extracted into a fresh directory,
which is deleted afterwards (the archive itself is left untouched).

Usage: python3 -I run_all15.py SHA256SUMS.txt ARCHIVE_DIR WORK_ROOT [MAX_ROWS]
  MAX_ROWS: skip gates whose SUMMARY row count (irredundant + extension
  rows) exceeds this (read from the archive's SUMMARY.json member only).
"""
import json
import os
import shutil
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


def nrows(tgz):
    with tarfile.open(tgz) as tf:
        for m in tf:
            if m.name.endswith("/SUMMARY.json") and m.name.count("/") == 1:
                b = json.load(tf.extractfile(m))["base_family"]
                return b["irredundant_rows"] + b["km1_extension_rows"]
    raise ValueError(tgz)


def main():
    sums, adir, wroot = sys.argv[1], sys.argv[2], sys.argv[3]
    maxrows = int(sys.argv[4]) if len(sys.argv) > 4 else None
    os.makedirs(RES, exist_ok=True)
    gates = []
    for fn in os.listdir(adir):
        if fn.startswith("evidence15_") and fn.endswith("_s0.tgz"):
            p = int(fn.split("_")[1])
            gates.append((nrows(os.path.join(adir, fn)), p, fn))
    for n, p, fn in sorted(gates):
        out = os.path.join(RES, "gate_%d.json" % p)
        if os.path.exists(out) or (maxrows and n > maxrows):
            continue
        work = os.path.join(wroot, "w%d" % p)
        shutil.rmtree(work, ignore_errors=True)
        os.makedirs(work)
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "check_gate15.py"), sums,
                            os.path.join(adir, fn), work], capture_output=True, text=True)
        shutil.rmtree(work, ignore_errors=True)
        if r.returncode != 0:
            print("ERROR p=%d rows=%d: %s" % (p, n, r.stderr[-2000:]), flush=True)
            continue
        rec = json.loads(r.stdout)
        with open(out, "w") as o:
            json.dump(rec, o, indent=1, sort_keys=True)
        print("p=%d rows=%d pass=%s seconds=%s mismatches=%d" % (p, n, rec["pass"], rec["seconds"],
                                                                 len(rec["mismatches"])), flush=True)


if __name__ == "__main__":
    main()
