"""Independent spot check of Allikvere's LRC(14) gate certificates
(Zenodo 10.5281/zenodo.22667683, arXiv:2609.02604v2).

Usage: python3 check_allikvere.py SHA256SUMS.txt EVIDENCE.tgz [...]
(Archives are untrusted data: they are only read, never executed.)

For each gate archive (k = 14, prime p) this checks, with our own code:
  0. the archive's SHA-256 matches the published SHA256SUMS.txt;
  1. every retained level-one row (rows_ir/*.txt; rows_km1/*.txt extended
     by every class, as in the paper's km1 branch) has NO witness
     t in (1/p)Z, i.e. lies in I(14,p,1)   [soundness of the rows];
  2. the binary cascade: lifting all rows by 2 up to level 32 with our
     liftfree.c + gcd clause gives the same number of improper level-2
     lifts as the certificate, and the surviving orbits at level 32
     equal the certificate's persistent orbits (canonical form);
     Also, for every level-2 survivor row listed in filt/*.out
     ("SURVIVOR base: ... l2=N"), our count of improper level-2 lifts of
     that row equals N (the certificate's total counts with multiplicity
     over rows, so it can exceed our count of distinct lifts);
  3. the level-15 kill of each persistent orbit: witness-free lifts at
     levels 3 and 5 (liftfree.c), CRT combination, witness test on the
     level-15 grid, gcd clause (and the near-gcd Lemma 3.12 if needed):
     no improper lift remains.
NOT checked: completeness of the level-one rows (that every orbit of
I(14,p,1) is represented).  That needs re-running a level-one generator
for k = 14 at p, which is beyond this step's budget.
"""
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sieve import Level  # noqa: E402

K = 14
HERE = os.path.dirname(os.path.abspath(__file__))
_LF = None


def liftfree_bin():
    global _LF
    if _LF is None:
        out = os.path.join(tempfile.mkdtemp(prefix="lrc_"), "liftfree")
        subprocess.run(["cc", "-O3", "-o", out, os.path.join(HERE, "liftfree.c")], check=True)
        _LF = out
    return _LF


def witness_free_lifts(k, M, c, tuples):
    """Return {input index: [lifts]} of witness-free lifts to level c*M."""
    inp = "\n".join(" ".join(map(str, t)) for t in tuples) + "\n"
    res = subprocess.run([liftfree_bin(), str(k), str(M), str(c)], input=inp,
                         capture_output=True, text=True, check=True)
    out = {}
    for line in res.stdout.splitlines():
        xs = list(map(int, line.split()))
        out.setdefault(xs[0], []).append(tuple(xs[1:]))
    return out


def gcd_clause(w, l):
    if l == 1:
        return False
    for i in range(len(w)):
        g = l
        for j, x in enumerate(w):
            if j != i:
                g = gcd(g, x)
        if g > 1:
            return True
    return False


def neargcd_ok(w, k=K):
    """Lemma 3.12 (few-exception shift) of arXiv:2609.02604v2 for d in {3,5}."""
    for d in (3, 5):
        e = sum(1 for x in w if x % d)
        md = -(-2 * d // (k + 1))
        if 2 <= e and e * md < d:
            return True
    return False


def decode_rows(path, k):
    rows = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            width = len(s) // k
            if width * k != len(s) or width not in (2, 4):
                raise ValueError("unexpected row width %d in %s" % (len(s), path))
            rows.append(tuple(int(s[i:i + width], 16) for i in range(0, len(s), width)))
    return rows


def check_gate(tgz, sums):
    report = {"archive": os.path.basename(tgz)}
    h = hashlib.sha256(open(tgz, "rb").read()).hexdigest()
    report["sha256_ok"] = sums.get(os.path.basename(tgz)) == h
    tmp = tempfile.mkdtemp(prefix="lrc_ev_")
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp, filter="data")
    (sub,) = [d for d in os.listdir(tmp) if d.startswith("out_")]
    root = os.path.join(tmp, sub)
    summ = json.load(open(os.path.join(root, "SUMMARY.json")))
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    assert k == K
    report.update(p=p, status=summ["status"], claim_type=summ["claim_type"])
    hcl = (p - 1) // 2
    # 1. rows
    rows = []
    for fn in sorted(os.listdir(os.path.join(root, "rows_ir"))):
        if fn.endswith(".txt"):
            rows += decode_rows(os.path.join(root, "rows_ir", fn), k)
    km1 = []
    if os.path.isdir(os.path.join(root, "rows_km1")):
        for fn in sorted(os.listdir(os.path.join(root, "rows_km1"))):
            if fn.endswith(".txt"):
                km1 += decode_rows(os.path.join(root, "rows_km1", fn), k - 1)
    ext = [tuple(sorted(c + (x,))) for c in km1 for x in range(1, hcl + 1)]
    L1 = Level(k, p, 1)
    bad = [r for r in rows + ext if L1.has_witness(r)]
    report["rows_ir"] = len(rows)
    report["km1_covers"] = len(km1)
    report["km1_extension_rows"] = len(ext)
    report["rows_with_witness"] = len(bad)
    report["claimed_ir_rows"] = summ["base_family"].get("irredundant_rows")
    report["claimed_km1_extension_rows"] = summ["base_family"].get("km1_extension_rows")
    # the extension rows with a witness are dropped (they are proper); the
    # irredundant rows must all be improper
    ext_improper = [r for r in ext if not L1.has_witness(r)]
    report["km1_extension_rows_improper"] = len(ext_improper)
    # 2. cascade (we lift all improper rows; duplicates are harmless)
    cur = sorted(set(r for r in rows if not L1.has_witness(r)) | set(ext_improper))
    l = 1
    trace = []
    while cur and l < 32:
        wf = witness_free_lifts(k, l * p, 2, cur)
        l *= 2
        nxt = sorted({w for ws in wf.values() for w in ws if not gcd_clause(w, l)})
        trace.append((l, len(nxt)))
        cur = nxt
    report["cascade_trace"] = trace
    import re
    bases, l2 = [], []
    for fn in sorted(os.listdir(os.path.join(root, "filt"))):
        if fn.endswith(".out"):
            for line in open(os.path.join(root, "filt", fn)):
                m = re.match(r"SURVIVOR base: ([\d ]+) l2=(\d+)", line)
                if m:
                    bases.append(tuple(map(int, m.group(1).split())))
                    l2.append(int(m.group(2)))
    wf2 = witness_free_lifts(k, p, 2, bases) if bases else {}
    ours2 = [len([w for w in wf2.get(i, []) if not gcd_clause(w, 2)]) for i in range(len(bases))]
    report["level2_survivor_rows_listed"] = len(bases)
    report["level2_per_row_mismatches"] = sum(1 for a, b in zip(l2, ours2) if a != b)
    report["level2_improper_with_multiplicity_ours"] = sum(ours2)
    report["claimed_level2_improper"] = summ["cascade"].get("level2_improper_lifts_total")
    pers = sorted({L1.canon([x % p for x in w]) for w in cur})
    claimed = sorted(L1.canon([int(x) for x in s.split()])
                     for s in summ["persistent_orbits"]["representatives"])
    report["persistent_orbits_ours"] = [list(x) for x in pers]
    report["persistent_match"] = pers == claimed
    # 3. level-15 kill of each persistent orbit (representative as stated)
    kills = []
    for s in summ["persistent_orbits"]["representatives"]:
        base = tuple(int(x) for x in s.split())
        w3 = witness_free_lifts(k, p, 3, [base]).get(0, [])
        w5 = witness_free_lifts(k, p, 5, [base]).get(0, [])
        L15 = Level(k, p, 15)
        cand = []
        for a in w3:
            for b in w5:
                x = []
                for ai, bi in zip(a, b):
                    sol = [ai + 3 * p * j for j in range(5) if (ai + 3 * p * j - bi) % (5 * p) == 0]
                    assert len(sol) == 1
                    x.append(sol[0])
                cand.append(tuple(x))
        wf15 = [w for w in cand if not L15.has_witness(w)]
        after_gcd = [w for w in wf15 if not gcd_clause(w, 15)]
        after_near = [w for w in after_gcd if not neargcd_ok(w)]
        kills.append({"orbit": s, "wf3": len(w3), "wf5": len(w5), "crt": len(cand),
                      "wf15": len(wf15), "improper_after_gcd": len(after_gcd),
                      "improper_after_neargcd": len(after_near)})
    report["kills_ours"] = kills
    report["kills_claimed"] = [{x: d[x] for x in ("witness_free_level_3", "witness_free_level_5",
                                                  "crt_candidates", "witness_free", "improper_after_gcd",
                                                  "improper_after_neargcd")} for d in summ["level_kills"]]
    return report


def main():
    sums = {}
    for line in open(sys.argv[1]):
        parts = line.split()
        if len(parts) == 2:
            sums[os.path.basename(parts[1])] = parts[0]
    for tgz in sys.argv[2:]:
        t0 = time.time()
        r = check_gate(tgz, sums)
        r["seconds"] = round(time.time() - t0, 1)
        print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
