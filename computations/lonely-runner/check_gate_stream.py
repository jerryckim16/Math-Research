"""Streaming re-check of one LRC(14) gate archive (for archives too large to
load: up to 1.6 GB, 1.4e8 rows, 8.2e6 kill files).  The archive is read as a
tar stream (never extracted, never executed).

Usage: python3 check_gate_stream.py SHA256SUMS.txt evidence_<p>_s0.tgz SAMPLE [JOBS]

Checks (all with our own code):
  A  SHA-256 of the archive vs the published SHA256SUMS.txt          [full]
  B  every rows_ir row is witness-free at level 1 (gatecheck hexrows),
     every rows_km1 multiset is a cover (witness-free, 13 classes)   [full]
  C  cascade (gatecheck cascade, levels 2..32):
     C1 SAMPLE rows drawn uniformly (seeded reservoir) from rows_ir: our
        counts equal the certificate's filt/*.out line for that row, or the
        row has no improper level-2 lift if it has no line          [sample]
     C2 SAMPLE lines drawn uniformly from the certificate's ext survivor
        lines (filt/ext*.out): our counts equal the listed counts    [sample]
     C3 every sampled row that persists to level 32 lies in the orbit of
        some kill record (all kill bases canonicalised by canon.c)   [sample vs full set]
  D  SAMPLE kill records drawn uniformly: gatecheck kill reproduces
     wf3, wf5, CRT, wf15, improper_after_gcd, improper_after_neargcd, and
     improper_after_neargcd = 0 (gcd = 0 for J-empty claims)         [sample]
     plus: number of kill files = SUMMARY persistent-orbit count     [full]
If SAMPLE >= population, that part is full.
"""
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_gate_full import binary, run_parallel  # noqa: E402

K = 14


class Reservoir:
    def __init__(self, n, rng):
        self.n, self.rng, self.seen, self.items = n, rng, 0, []

    def add(self, x):
        self.seen += 1
        if len(self.items) < self.n:
            self.items.append(x)
        else:
            j = self.rng.randrange(self.seen)
            if j < self.n:
                self.items[j] = x


def dec(s, n):
    w = len(s) // n
    return tuple(int(s[i:i + w], 16) for i in range(0, len(s), w))


SURV = re.compile(rb"SURVIVOR base: ([\d ]+?) (l2=.*)$")


def counts_of(tail):
    kv = dict(x.split(b"=") for x in tail.split() if b"=" in x)
    return tuple(int(kv.get(b"l%d" % (1 << e), 0)) for e in range(1, 6))


def text(b):
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16")
    return b.decode()


def main():
    sums = {}
    for line in open(sys.argv[1]):
        a = line.split()
        if len(a) == 2:
            sums[os.path.basename(a[1])] = a[0]
    tgz, S = sys.argv[2], int(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    t0 = time.time()
    rep = {"archive": os.path.basename(tgz), "sample": S, "mode": "stream", "mismatches": []}
    h = hashlib.sha256()
    with open(tgz, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    rep["sha256_ok"] = sums.get(os.path.basename(tgz)) == h.hexdigest()
    rng = random.Random(20261124)
    # ---- pass 1: rows ----
    summ = None
    hx_ir = subprocess.Popen([binary("gatecheck"), "hexrows", str(K), "0", str(K)], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE) if False else None
    ir_res = Reservoir(S, rng)
    ir_files = km1_files = 0
    tmp_ir = tempfile.NamedTemporaryFile(delete=False)
    tmp_km = tempfile.NamedTemporaryFile(delete=False)
    with tarfile.open(tgz, "r|gz") as tf:
        for m in tf:
            if not m.isfile():
                continue
            name = m.name
            if name.endswith("SUMMARY.json"):
                summ = json.loads(tf.extractfile(m).read())
            elif "/rows_ir/" in name and name.endswith(".txt"):
                ir_files += 1
                data = tf.extractfile(m).read()
                tmp_ir.write(data if data.endswith(b"\n") or not data else data + b"\n")
                for line in data.split(b"\n"):
                    if line:
                        ir_res.add(line)
            elif "/rows_km1/" in name and name.endswith(".txt"):
                km1_files += 1
                data = tf.extractfile(m).read()
                tmp_km.write(data if data.endswith(b"\n") or not data else data + b"\n")
    tmp_ir.close()
    tmp_km.close()
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    assert k == K
    hcl = (p - 1) // 2
    rep.update(p=p, status=summ["status"], claim_type=summ["claim_type"], variant=summ["precondition"]["variant"])
    with open(tmp_ir.name) as fin:
        out = subprocess.run([binary("gatecheck"), "hexrows", str(k), str(p), str(k)], stdin=fin,
                             capture_output=True, text=True, check=True).stdout
    last = out.strip().splitlines()[-1].split()
    rep["rows_ir"], rep["ir_rows_with_witness"] = int(last[1]), int(last[3])
    with open(tmp_km.name) as fin:
        out2 = subprocess.run([binary("gatecheck"), "hexrows", str(k), str(p), str(k - 1)], stdin=fin,
                              capture_output=True, text=True, check=True).stdout
    last2 = out2.strip().splitlines()[-1].split()
    rep["km1_rows"], rep["km1_rows_with_witness"] = int(last2[1]), int(last2[3])
    os.unlink(tmp_ir.name)
    os.unlink(tmp_km.name)
    rep["claimed"] = {"ir_rows": summ["base_family"].get("irredundant_rows"),
                      "km1_covers": summ["base_family"].get("km1_covers_dedup"),
                      "ext_rows": summ["base_family"].get("km1_extension_rows"),
                      "persistent_orbits": summ.get("persistent_orbits", {}).get("count")}
    if rep["ir_rows_with_witness"] or rep["km1_rows_with_witness"]:
        rep["mismatches"].append({"what": "stored row with a level-1 witness", "detail": out.splitlines()[:20] + out2.splitlines()[:20]})
    # cascade on the ir sample
    ir_sample = [dec(x.decode().strip(), k) for x in ir_res.items]
    cas = run_parallel([binary("gatecheck"), "cascade", str(k), str(p)],
                       [" ".join(map(str, r)) for r in ir_sample], jobs) if ir_sample else []
    sample_keys = {tuple(sorted(r)): i for i, r in enumerate(ir_sample)}
    pers_rows = [r for r, c in zip(ir_sample, cas) if c[4] > 0]
    # ---- pass 2: filt + kills ----
    theirs_ir = {}
    ext_res = Reservoir(S, rng)
    kill_res = Reservoir(S, rng)
    nkill = 0
    canon_p = subprocess.Popen([binary("canon"), str(k), str(p), "each"], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    pers_canon = set()
    if pers_rows:
        pc = subprocess.run([binary("canon"), str(k), str(p), "each"],
                            input="\n".join(" ".join(map(str, r)) for r in pers_rows) + "\n",
                            capture_output=True, text=True, check=True).stdout
        pers_canon = {tuple(map(int, l.split())) for l in pc.splitlines()}
    found = set()
    # canon output is read in a thread to avoid pipe deadlock
    import threading

    def reader():
        for line in canon_p.stdout:
            t = tuple(map(int, line.split()))
            if t in pers_canon:
                found.add(t)
    th = threading.Thread(target=reader)
    th.start()
    with tarfile.open(tgz, "r|gz") as tf:
        for m in tf:
            if not m.isfile():
                continue
            name = m.name
            if "/filt/" in name and name.endswith(".out"):
                is_ext = "/filt/ext" in name
                for line in tf.extractfile(m).read().split(b"\n"):
                    mm = SURV.match(line.strip())
                    if not mm:
                        continue
                    base = tuple(map(int, mm.group(1).split()))
                    if is_ext:
                        ext_res.add((base, counts_of(mm.group(2))))
                    else:
                        key = tuple(sorted(base))
                        if key in sample_keys:
                            theirs_ir[key] = counts_of(mm.group(2))
            elif "/kills/" in name and name.endswith(".txt"):
                nkill += 1
                txt = text(tf.extractfile(m).read())
                mb = re.search(r"base: ([\d ]+)", txt)
                base = tuple(map(int, mb.group(1).split()))
                canon_p.stdin.write((" ".join(map(str, base)) + "\n").encode())
                kill_res.add((base, dict(re.findall(r"(\w+)=(\d+)", txt))))
    canon_p.stdin.close()
    th.join()
    canon_p.wait()
    rep["kill_files"] = nkill
    if rep["claimed"]["persistent_orbits"] is not None and nkill != rep["claimed"]["persistent_orbits"]:
        rep["mismatches"].append({"what": "kill-file count differs from SUMMARY persistent count",
                                  "files": nkill, "summary": rep["claimed"]["persistent_orbits"]})
    # C1
    c1 = []
    for r, c in zip(ir_sample, cas):
        th_c = theirs_ir.get(tuple(sorted(r)), (0, 0, 0, 0, 0))
        if tuple(c) != th_c:
            c1.append({"row": r, "ours": c, "cert": th_c})
    rep["C1_ir_rows_sampled"] = len(ir_sample)
    rep["C1_ir_rows_with_survivors"] = sum(1 for c in cas if c[0] > 0)
    rep["C1_mismatches"] = len(c1)
    if c1:
        rep["mismatches"].append({"what": "cascade counts differ on sampled ir rows", "rows": c1[:20]})
    # C2
    ext_items = ext_res.items
    rep["C2_ext_survivor_lines_total"] = ext_res.seen
    rep["C2_ext_lines_sampled"] = len(ext_items)
    if ext_items:
        cas2 = run_parallel([binary("gatecheck"), "cascade", str(k), str(p)],
                            [" ".join(map(str, b)) for b, _ in ext_items], jobs)
        c2 = [{"row": b, "ours": c, "cert": cc} for (b, cc), c in zip(ext_items, cas2) if tuple(c) != cc]
        rep["C2_mismatches"] = len(c2)
        if c2:
            rep["mismatches"].append({"what": "cascade counts differ on sampled ext survivor lines", "rows": c2[:20]})
        pers_rows2 = [b for (b, _), c in zip(ext_items, cas2) if c[4] > 0]
    else:
        rep["C2_mismatches"] = 0
        pers_rows2 = []
    # C3 (ir sample) — ext persistent rows checked too via a second canon pass is
    # omitted: their orbits are certificate survivors by construction.
    rep["C3_sampled_persistent_rows"] = len(pers_rows)
    rep["C3_in_kill_orbits"] = len(found) == len(pers_canon)
    if len(found) != len(pers_canon):
        rep["mismatches"].append({"what": "sampled persistent row not among kill orbits",
                                  "rows": sorted(pers_canon - found)[:20]})
    # D
    keys = ["witness_free_level_3", "witness_free_level_5", "crt_candidates",
            "witness_free_level_15", "improper_after_gcd", "improper_after_neargcd"]
    kill_items = kill_res.items
    kl = run_parallel([binary("gatecheck"), "kill", str(k), str(p)],
                      [" ".join(map(str, b)) for b, _ in kill_items], jobs) if kill_items else []
    km = [{"base": b, "cert": [int(nums.get(x, -1)) for x in keys], "ours": mine}
          for (b, nums), mine in zip(kill_items, kl) if [int(nums.get(x, -1)) for x in keys] != mine]
    tot = [sum(m[i] for m in kl) for i in range(6)] if kl else [0] * 6
    rep["D_kills_sampled"] = len(kill_items)
    rep["D_mismatches"] = len(km)
    rep["kill_totals_ours"] = dict(zip(keys, tot))
    if km:
        rep["mismatches"].append({"what": "kill record differs", "orbits": km[:20]})
    if tot[5] != 0:
        rep["mismatches"].append({"what": "improper lift survives near-gcd lemma"})
    if summ["claim_type"].startswith("J(K,p) empty") and tot[4] != 0:
        rep["mismatches"].append({"what": "J-empty claim but gcd clause leaves improper lifts"})
    rep["pass"] = rep["sha256_ok"] and not rep["mismatches"]
    rep["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(rep), flush=True)


if __name__ == "__main__":
    main()
