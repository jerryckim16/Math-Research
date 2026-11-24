"""Full independent re-check of one LRC(14) gate certificate (Allikvere,
Zenodo 10.5281/zenodo.22667683), apart from level-one completeness (see
completeness_check.py for that).

Usage: python3 check_gate_full.py SHA256SUMS.txt evidence_<p>_s0.tgz [JOBS [SAMPLE [KILL_SAMPLE]]]
  SAMPLE (optional): re-check the cascade only on SAMPLE random rows and the
  kill only on SAMPLE random orbits (seeded); the persistent-orbit set
  comparison is then skipped.  Without SAMPLE (or SAMPLE = 0) every row/orbit
  is checked.
  KILL_SAMPLE (optional, step 8): sample size for the kill alone, so that the
  cascade (and the persistent-orbit set equality) can run in full while the
  kill is sampled.  KILL_SAMPLE = 0 skips the kill in this record
  ("kill_skipped": true); the kill is then covered by another record.
Archives are read as data only (never executed).

Checks, with our own code (gatecheck.c, canon.c, sieve.Level):
  A. archive SHA-256 = published SHA256SUMS.txt entry;
  B. every stored level-one row (rows_ir, and rows_km1 covers extended by
     every class 1..(p-1)/2) is witness-free at level 1;
  C. per-row binary cascade to level 32 (gatecheck cascade): for every row
     listed in filt/*.out the counts l2, l4, l8, l16, l32 equal ours; every
     row not listed has no improper level-2 lift; the rows that persist to
     level 32 form exactly the certificate's persistent orbits (canonical
     forms, canon.c) = the orbits of kills/kill_orbit*.txt;
  D. per-orbit level-15 kill (gatecheck kill): wf3, wf5, CRT candidates,
     wf15, improper_after_gcd, improper_after_neargcd equal the record, and
     improper_after_neargcd = 0 (and improper_after_gcd = 0 when the claim is
     J(14,p) empty).
Any mismatch is reported row by row (first 20) and makes "pass" false.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sieve import Level  # noqa: E402

K = 14
_BIN = {}


def binary(name):
    if name not in _BIN:
        out = os.path.join(tempfile.mkdtemp(prefix="lrc_"), name)
        subprocess.run(["cc", "-O3", "-o", out, os.path.join(HERE, name + ".c"), "-lm"], check=True)
        _BIN[name] = out
    return _BIN[name]


def run_parallel(args, lines, jobs):
    """Run a filter binary on chunks of input lines in parallel; outputs are
    'idx ...' lines with idx local to the chunk; return list of int lists in
    input order."""
    chunks = [lines[i::jobs] for i in range(jobs)]
    procs = []
    for ch in chunks:
        f = tempfile.TemporaryFile("w+")
        f.write("\n".join(ch) + "\n")
        f.seek(0)
        procs.append(subprocess.Popen(args, stdin=f, stdout=subprocess.PIPE, text=True))
    outs = [pr.communicate()[0] for pr in procs]
    res = [None] * len(lines)
    for j, out in enumerate(outs):
        for line in out.splitlines():
            xs = list(map(int, line.split()))
            res[xs[0] * jobs + j] = xs[1:]
    assert all(r is not None for r in res)
    return res


def decode(path, n):
    out = []
    for line in open(path):
        s = line.strip()
        if s:
            w = len(s) // n
            assert w * n == len(s) and w in (2, 4), (path, len(s))
            out.append(tuple(int(s[i:i + w], 16) for i in range(0, len(s), w)))
    return out


def canon_each(k, p, rows):
    res = subprocess.run([binary("canon"), str(k), str(p), "each"],
                         input="\n".join(" ".join(map(str, r)) for r in rows) + "\n",
                         capture_output=True, text=True, check=True)
    return [tuple(map(int, l.split())) for l in res.stdout.splitlines()]


def canon_set(k, p, rows):
    res = subprocess.run([binary("canon"), str(k), str(p), "rows"],
                         input="\n".join(" ".join(map(str, r)) for r in rows) + "\n",
                         capture_output=True, text=True, check=True)
    return {tuple(map(int, l.split())) for l in res.stdout.splitlines()}


def check(tgz, sums, jobs=4, sample=None, kill_sample=None):
    import random
    rng = random.Random(20261123)
    t0 = time.time()
    rep = {"archive": os.path.basename(tgz), "mismatches": []}
    rep["sha256_ok"] = sums.get(os.path.basename(tgz)) == hashlib.sha256(open(tgz, "rb").read()).hexdigest()
    tmp = tempfile.mkdtemp(prefix="lrc_ev_")
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp, filter="data")
    (sub,) = [d for d in os.listdir(tmp) if d.startswith("out_")]
    root = os.path.join(tmp, sub)
    summ = json.load(open(os.path.join(root, "SUMMARY.json")))
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    assert k == K
    h = (p - 1) // 2
    rep.update(p=p, status=summ["status"], claim_type=summ["claim_type"],
               variant=summ["precondition"]["variant"])
    # B. rows
    rows = []
    for fn in sorted(os.listdir(os.path.join(root, "rows_ir"))):
        if fn.endswith(".txt"):
            rows += decode(os.path.join(root, "rows_ir", fn), k)
    km1 = []
    d = os.path.join(root, "rows_km1")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".txt"):
                km1 += decode(os.path.join(d, fn), k - 1)
    km1 = sorted(set(km1))
    ext = [c + (x,) for c in km1 for x in range(1, h + 1)]
    L1 = Level(k, p, 1)
    bad = [r for r in rows if L1.has_witness(r)]
    ext_imp = [r for r in ext if not L1.has_witness(r)]
    rep.update(rows_ir=len(rows), km1_covers=len(km1), ext_rows=len(ext), ext_rows_improper=len(ext_imp),
               ir_rows_with_witness=len(bad),
               claimed=dict(ir_rows=summ["base_family"].get("irredundant_rows"),
                            km1_covers=summ["base_family"].get("km1_covers_dedup"),
                            ext_rows=summ["base_family"].get("km1_extension_rows")))
    if bad:
        rep["mismatches"].append({"what": "ir row with a level-1 witness", "rows": bad[:20]})
    # C. cascade, per row
    allrows = rows + ext_imp
    sample = sample or None
    if kill_sample is None:
        kill_sample = sample
    rep["sample"] = sample
    rep["kill_sample"] = kill_sample
    if sample:
        allrows = rng.sample(allrows, min(sample, len(allrows)))
    lines = [" ".join(map(str, r)) for r in allrows]
    cas = run_parallel([binary("gatecheck"), "cascade", str(k), str(p)], lines, jobs)
    # Compare per unit orbit: the improper-lift counts of a row are invariant
    # under units, permutations and signs (F2), so every stored row of an
    # orbit must carry the same counts.  The certificate stores only some
    # km1 extension rows (deduplicated), so raw rows cannot be matched 1:1.
    ourcanon = canon_each(k, p, allrows)
    ours = {}
    for cform, c in zip(ourcanon, cas):
        c = tuple(c)
        if cform in ours and ours[cform] != c:
            rep["mismatches"].append({"what": "our counts differ within one orbit (bug)", "orbit": cform})
        ours[cform] = c
    tbases, tcounts = [], []
    for fn in sorted(os.listdir(os.path.join(root, "filt"))):
        if fn.endswith(".out"):
            for line in open(os.path.join(root, "filt", fn)):
                m = re.match(r"SURVIVOR base: ([\d ]+?) (l2=.*)$", line.strip())
                if m:
                    kv = dict(x.split("=") for x in m.group(2).split() if "=" in x)
                    tbases.append(tuple(map(int, m.group(1).split())))
                    tcounts.append(tuple(int(kv.get("l%d" % (1 << e), 0)) for e in range(1, 6)))
    theirs = {}
    for cform, c in zip(canon_each(k, p, tbases), tcounts):
        if cform in theirs and theirs[cform] != c:
            rep["mismatches"].append({"what": "certificate counts differ within one orbit", "orbit": cform})
        theirs[cform] = c
    our_surv = {o: c for o, c in ours.items() if c[0] > 0}
    if sample:
        theirs = {o: c for o, c in theirs.items() if o in ours}
    rep["cascade_orbits_checked"] = len(ours)
    rep["cascade_survivor_orbits_ours"] = len(our_surv)
    rep["cascade_survivor_orbits_cert"] = len(theirs)
    diff_counts = [(o, theirs[o], our_surv[o]) for o in set(theirs) & set(our_surv) if theirs[o] != our_surv[o]]
    only_cert = sorted(set(theirs) - set(our_surv))
    only_ours = sorted(set(our_surv) - set(theirs))
    rep["cascade_orbits_count_mismatch"] = len(diff_counts)
    rep["cascade_survivor_orbits_only_in_certificate"] = len(only_cert)
    rep["cascade_survivor_orbits_only_ours"] = len(only_ours)
    if diff_counts:
        rep["mismatches"].append({"what": "cascade counts differ", "orbits": diff_counts[:20]})
    if only_cert:
        rep["mismatches"].append({"what": "certificate survivor orbit has no improper level-2 lift in our run "
                                  "(or is not among the stored rows we re-ran)", "orbits": only_cert[:20]})
    if only_ours:
        rep["mismatches"].append({"what": "our survivor orbit absent from certificate survivors", "orbits": only_ours[:20]})
    pers_rows = [r for r, c in zip(allrows, cas) if c[4] > 0]
    pers = canon_set(k, p, pers_rows) if pers_rows else set()
    kills = []
    kd = os.path.join(root, "kills")
    for fn in sorted(os.listdir(kd)):
        txt = open(os.path.join(kd, fn)).read()
        m = re.search(r"base: ([\d ]+)\n", txt)
        nums = dict(re.findall(r"(\w+)=(\d+)", txt))
        kills.append((tuple(map(int, m.group(1).split())), nums))
    kill_orbits = canon_set(k, p, [b for b, _ in kills]) if kills else set()
    rep["persistent_orbits_ours"] = len(pers)
    rep["persistent_orbits_cert"] = len(kill_orbits)
    if sample:
        # every sampled persistent row must lie in a certificate orbit
        rep["persistent_orbits_equal"] = "sampled: ours subset of cert = %s" % pers.issubset(kill_orbits)
        if not pers.issubset(kill_orbits):
            rep["mismatches"].append({"what": "sampled persistent row not among cert orbits",
                                      "rows": sorted(pers - kill_orbits)[:20]})
    else:
        rep["persistent_orbits_equal"] = pers == kill_orbits
    if not sample and pers != kill_orbits:
        rep["mismatches"].append({"what": "persistent orbit sets differ",
                                  "only_ours": sorted(pers - kill_orbits)[:20],
                                  "only_cert": sorted(kill_orbits - pers)[:20]})
    # D. kills
    rep["kill_files"] = len(kills)
    if kill_sample == 0:
        kills = []
        rep["kill_skipped"] = True
    elif kill_sample:
        kills = rng.sample(kills, min(kill_sample, len(kills)))
    kl = run_parallel([binary("gatecheck"), "kill", str(k), str(p)],
                      [" ".join(map(str, b)) for b, _ in kills], jobs) if kills else []
    keys = ["witness_free_level_3", "witness_free_level_5", "crt_candidates",
            "witness_free_level_15", "improper_after_gcd", "improper_after_neargcd"]
    kmis = []
    tot = collections.Counter()
    for (b, nums), mine in zip(kills, kl):
        cert = [int(nums.get(x, -1)) for x in keys]
        for x, y in zip(keys, mine):
            tot[x] += y
        if cert != mine:
            kmis.append({"base": b, "cert": cert, "ours": mine})
    rep["kill_orbits"] = len(kills)
    rep["kill_mismatches"] = len(kmis)
    rep["kill_totals_ours"] = dict(tot)
    if kmis:
        rep["mismatches"].append({"what": "kill record differs", "orbits": kmis[:20]})
    if tot["improper_after_neargcd"] != 0:
        rep["mismatches"].append({"what": "improper level-15 lift survives near-gcd lemma"})
    if summ["claim_type"].startswith("J(K,p) empty") and tot["improper_after_gcd"] != 0:
        rep["mismatches"].append({"what": "J-empty claim but gcd clause leaves improper lifts"})
    rep["pass"] = rep["sha256_ok"] and not rep["mismatches"]
    rep["seconds"] = round(time.time() - t0, 1)
    return rep


def main():
    sums = {}
    for line in open(sys.argv[1]):
        a = line.split()
        if len(a) == 2:
            sums[os.path.basename(a[1])] = a[0]
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    sample = int(sys.argv[4]) if len(sys.argv) > 4 else None
    kill_sample = int(sys.argv[5]) if len(sys.argv) > 5 else None
    print(json.dumps(check(sys.argv[2], sums, jobs, sample, kill_sample)), flush=True)


if __name__ == "__main__":
    main()
