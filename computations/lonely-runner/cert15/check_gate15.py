"""Independent re-check of one LRC(15) (16-runner) gate certificate of
J. Allikvere, "Sixteen lonely runners", Zenodo 10.5281/zenodo.23304361
(archives evidence15_<p>_s0.tgz), apart from level-one completeness.

Usage: python3 -I check_gate15.py SHA256SUMS.txt evidence15_<p>_s0.tgz WORKDIR
  WORKDIR must be a fresh empty directory; the archive is extracted there
  (tarfile, filter="data") and read as data only.  None of the author's
  programs are executed.  Prints one JSON record.

Archive format (read from the archives themselves; see notes/lonely-runner/cert15.md):
  out15_<p>/rows_ir/ir_<r>_<s>.txt   irredundant 15-class covers (hex, 2 digits/class)
  out15_<p>/rows_km1/km1_<r>.txt     rooted 14-class covers (hex)
  out15_<p>/rows_km1/dedup_<i>.txt   the deduplicated 14-class covers (one or more per file)
  out15_<p>/filt/ir_<r>_<s>.{out,stats}, ext_<i>.{out,stats}
      cascade of each input file: "SURVIVOR base: v_1..v_15 l2=.. [tight=..] l4=.. l8=.. l16=.."
      for every row with an improper level-2 lift; stats "rows=R survivors=S".
      For ext_<i>, the rows are the covers of dedup_<i> extended by every class x = 1..(p-1)/2.
  out15_<p>/SUMMARY.json, MANIFEST_SHA256.json, kills/ (empty for J-empty gates).

Checks, with our own code (rowcheck15.c in this directory; gatecheck.c and
canon.c in the parent directory):
  A. archive SHA-256 = published SHA256SUMS.txt entry; every entry of the
     internal MANIFEST_SHA256.json matches the extracted file.
  B. every stored irredundant row: classes in 1..h, distinct, contain 1,
     witness-free at level 1 (two implementations: rowcheck15 covering test,
     gatecheck hexrows direct time test), irredundant; every rooted and
     dedup 14-class cover: the same (a 14-cover is witness-free at level 1
     with the k = 15 threshold, so all its extensions are too); the dedup
     covers represent exactly the unit orbits of the rooted covers (canon.c);
     counts equal SUMMARY.json.
  C. binary cascade (gatecheck cascade, k = 15) of every irredundant row and
     every extension row (dedup cover + x, x = 1..h): per input file, the
     multiset of (row, l2, l4, l8, l16) over rows with l2 > 0 equals the
     certificate's filt/*.out, the per-file rows/survivors equal filt/*.stats,
     the SUMMARY cascade totals (survivor_rows, died_l<l>,
     level2_improper_lifts_total, level2_survivor_rows_ir/ext) equal ours;
     every fiber is empty by level 16 (so J(15,p) is empty given
     completeness); the rows first empty at 16 are exactly the orbit of
     (1..15); no persistent orbit and no kill record.
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
PARENT = os.path.dirname(HERE)
K = 15
_BIN = {}


def binary(name):
    if name not in _BIN:
        src = os.path.join(HERE, name + ".c")
        if not os.path.exists(src):
            src = os.path.join(PARENT, name + ".c")
        out = os.path.join(tempfile.mkdtemp(prefix="c15_"), name)
        # -march=native: hardware popcount (about 5x faster; same output, checked on 20,000 rows at p = 367)
        subprocess.run(["cc", "-O3", "-march=native", "-o", out, src, "-lm"], check=True)
        _BIN[name] = out
    return _BIN[name]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def decode_lines(path):
    return [s.strip() for s in open(path) if s.strip()]


def hex_to_tuple(s, n):
    w = len(s) // n
    assert w * n == len(s) and w in (2, 4), (len(s), n)
    return tuple(int(s[i:i + w], 16) for i in range(0, len(s), w))


def run(args, text):
    r = subprocess.run(args, input=text, capture_output=True, text=True, check=True)
    return r.stdout


def run_file(args, inpath):
    with open(inpath) as fi:
        r = subprocess.run(args, stdin=fi, capture_output=True, text=True, check=True)
    return r.stdout


def rowcheck(p, n, hexrows=None, path=None):
    if path is None:
        path = os.path.join(tempfile.mkdtemp(prefix="c15r_"), "rows.hex")
        with open(path, "w") as o:
            o.write("\n".join(hexrows) + "\n")
    out = run_file([binary("rowcheck15"), str(K), str(p), str(n)], path)
    last = out.strip().splitlines()[-1].split()
    stats = {last[i]: int(last[i + 1]) for i in range(0, len(last), 2)}
    bad = [l for l in out.splitlines() if l.startswith("BAD")]
    out2 = run_file([binary("gatecheck"), "hexrows", str(K), str(p), str(n)], path)
    m = re.search(r"rows (\d+) with_witness (\d+)", out2)
    stats["gatecheck_rows"] = int(m.group(1))
    stats["gatecheck_with_witness"] = int(m.group(2))
    return stats, bad


def canon_set(k, p, rows):
    out = run([binary("canon"), str(k), str(p), "rows"], "\n".join(" ".join(map(str, r)) for r in rows) + "\n")
    return {tuple(map(int, l.split())) for l in out.splitlines()}


def canon_each(k, p, rows):
    out = run([binary("canon"), str(k), str(p), "each"], "\n".join(" ".join(map(str, r)) for r in rows) + "\n")
    return [tuple(map(int, l.split())) for l in out.splitlines()]


def parse_out(path):
    res = []
    for line in open(path):
        m = re.match(r"SURVIVOR base: ([\d ]+?) (l2=.*)$", line.strip())
        if not m:
            if line.strip():
                raise ValueError("unparsed line in %s: %r" % (path, line))
            continue
        kv = dict(x.split("=") for x in m.group(2).split() if "=" in x)
        base = tuple(map(int, m.group(1).split()))
        res.append((base, tuple(int(kv.get("l%d" % (1 << e), 0)) for e in range(1, 6)), kv.get("tight")))
    return res


def parse_stats(path):
    m = re.search(r"TOTAL rows=(\d+) survivors=(\d+)", open(path).read())
    return int(m.group(1)), int(m.group(2))


def fkey(fn):
    return tuple(int(x) for x in re.findall(r"\d+", fn))


def check(tgz, sums, work):
    t0 = time.time()
    rep = {"archive": os.path.basename(tgz), "mismatches": []}
    mis = rep["mismatches"]
    rep["sha256"] = sha256_file(tgz)
    rep["sha256_ok"] = sums.get(os.path.basename(tgz)) == rep["sha256"]
    if not rep["sha256_ok"]:
        mis.append({"what": "archive SHA-256 differs from SHA256SUMS.txt"})
    assert os.path.isdir(work) and not os.listdir(work), "WORKDIR must be a fresh empty directory"
    with tarfile.open(tgz) as tf:
        tf.extractall(work, filter="data")
    (sub,) = [d for d in os.listdir(work) if d.startswith("out15_")]
    root = os.path.join(work, sub)
    summ = json.load(open(os.path.join(root, "SUMMARY.json")))
    k, p = summ["gate"]["k"], summ["gate"]["p"]
    assert k == K and sub == "out15_%d" % p and rep["archive"] == "evidence15_%d_s0.tgz" % p
    h = (p - 1) // 2
    bf = summ["base_family"]
    rep.update(p=p, status=summ["status"], claim_type=summ["claim_type"],
               precondition_claimed=summ["precondition"], timing_claimed=summ.get("timing"))
    if summ["status"] != "GATE_CLOSED":
        mis.append({"what": "status is not GATE_CLOSED", "status": summ["status"]})
    # A'. internal manifest
    man = json.load(open(os.path.join(root, "MANIFEST_SHA256.json")))
    # entries "../<exe>" name the author's executables, which are not shipped;
    # their hashes are compared with the archive's BUILD_SHA256.txt instead.
    exe = {f: hsh for f, hsh in man.items() if f.startswith("../")}
    bad_man = [f for f, hsh in man.items() if f not in exe and
               (not os.path.isfile(os.path.join(root, f)) or sha256_file(os.path.join(root, f)) != hsh)]
    build = {}
    bp = os.path.join(work, "BUILD_SHA256.txt")
    if os.path.isfile(bp):
        for line in open(bp):
            a = line.split()
            if len(a) == 2 and re.fullmatch(r"[0-9a-f]{64}", a[0]):
                build[a[1]] = a[0]
    rep["manifest_executables"] = {f: hsh[:16] for f, hsh in exe.items()}
    rep["manifest_executables_equal_BUILD_SHA256"] = all(build.get(f[3:]) == hsh for f, hsh in exe.items())
    rep["manifest_entries"] = len(man)
    rep["manifest_mismatch"] = len(bad_man)
    if bad_man:
        mis.append({"what": "internal manifest mismatch", "files": bad_man[:20]})
    # B. rows
    irdir = os.path.join(root, "rows_ir")
    irfiles = sorted([f for f in os.listdir(irdir) if f.endswith(".txt")], key=fkey)
    scratch = tempfile.mkdtemp(prefix="c15w_")
    irhex = os.path.join(scratch, "ir.hex")
    casin = os.path.join(scratch, "cascade.in")
    file_ranges = []          # (cascade-file-name, number of rows), in input order
    with open(irhex, "w") as oh, open(casin, "w") as oc:
        for f in irfiles:
            nrow = 0
            for s_ in open(os.path.join(irdir, f)):
                s_ = s_.strip()
                if not s_:
                    continue
                oh.write(s_ + "\n")
                oc.write(" ".join(map(str, hex_to_tuple(s_, K))) + "\n")
                nrow += 1
            file_ranges.append(("ir_" + f[3:-4], nrow))
    st, bad = rowcheck(p, K, path=irhex)
    rep["ir_rows"] = st["rows"]
    rep["ir_rowcheck"] = st
    if bad:
        mis.append({"what": "ir row fails a level-one check", "rows": bad[:20]})
    if any(st[x] for x in ("bad_format", "out_of_range", "not_distinct", "no_class1", "not_cover", "redundant",
                           "gatecheck_with_witness")) or st["gatecheck_rows"] != st["rows"]:
        mis.append({"what": "ir row checks failed", "stats": st})
    if st["rows"] != bf["irredundant_rows"]:
        mis.append({"what": "irredundant row count differs from SUMMARY", "ours": st["rows"],
                    "cert": bf["irredundant_rows"]})
    kdir = os.path.join(root, "rows_km1")
    rooted, dedup = [], []
    dedup_files = []
    if os.path.isdir(kdir):
        for f in sorted(os.listdir(kdir), key=fkey):
            if f.startswith("km1_") and f.endswith(".txt"):
                rooted += decode_lines(os.path.join(kdir, f))
            elif f.startswith("dedup_") and f.endswith(".txt"):
                dl = decode_lines(os.path.join(kdir, f))
                dedup_files.append((f, dl))
                dedup += dl
    rep["km1_rooted"] = len(rooted)
    rep["km1_dedup"] = len(dedup)
    for name, rows_ in (("rooted", rooted), ("dedup", dedup)):
        if rows_:
            st2, bad2 = rowcheck(p, K - 1, rows_)
            rep["km1_%s_rowcheck" % name] = st2
            if bad2 or any(st2[x] for x in ("bad_format", "out_of_range", "not_distinct", "no_class1",
                                             "not_cover", "redundant", "gatecheck_with_witness")):
                mis.append({"what": "km1 %s cover fails a level-one check" % name, "stats": st2, "rows": bad2[:20]})
    if len(rooted) != bf["km1_rooted_covers"] or len(dedup) != bf["km1_covers_dedup"]:
        mis.append({"what": "km1 counts differ from SUMMARY", "ours": [len(rooted), len(dedup)],
                    "cert": [bf["km1_rooted_covers"], bf["km1_covers_dedup"]]})
    rep["dedup_files"] = len(dedup_files)
    rep["dedup_covers_per_file"] = sorted(collections.Counter(len(dl) for _, dl in dedup_files).items())
    if any(len(dl) == 0 for _, dl in dedup_files):
        mis.append({"what": "an empty dedup file"})
    rt = [hex_to_tuple(s, K - 1) for s in rooted]
    dt = [hex_to_tuple(s, K - 1) for s in dedup]
    if rt or dt:
        orr, ord_ = canon_set(K - 1, p, rt), canon_set(K - 1, p, dt)
        rep["km1_rooted_orbits"] = len(orr)
        rep["km1_dedup_orbits_equal_rooted_orbits"] = orr == ord_ and len(ord_) == len(dt)
        if not rep["km1_dedup_orbits_equal_rooted_orbits"]:
            mis.append({"what": "dedup covers do not represent exactly the rooted cover orbits",
                        "rooted_orbits": len(orr), "dedup_orbits": len(ord_), "dedup": len(dt)})
    if bf["extensions_per_cover"] != h or bf["km1_extension_rows"] != len(dt) * h:
        mis.append({"what": "extension count differs", "cert": [bf["extensions_per_cover"], bf["km1_extension_rows"]],
                    "ours": [h, len(dt) * h]})
    # C. cascade: every ir row and every extension row, one process
    with open(casin, "a") as oc:
        for f, dl in dedup_files:      # every cover of dedup_<i> (one or more), each extended by x = 1..h
            for cl in dl:
                c = hex_to_tuple(cl, K - 1)
                for x in range(1, h + 1):
                    oc.write(" ".join(map(str, c + (x,))) + "\n")
            file_ranges.append(("ext_" + f[6:-4], h * len(dl)))
    tc = time.time()
    casout = os.path.join(scratch, "cascade.out")
    with open(casin) as fi, open(casout, "w") as fo:
        subprocess.run([binary("gatecheck"), "cascade", str(K), str(p)], stdin=fi, stdout=fo, check=True)
    rep["cascade_seconds"] = round(time.time() - tc, 1)
    # walk input and output in lockstep; keep only rows with an improper level-2 lift
    ours_by_file = collections.defaultdict(collections.Counter)
    rows_by_file = collections.Counter()
    surv = []
    ntot = 0
    with open(casin) as fi, open(casout) as fo:
        for fn, nrow in file_ranges:
            rows_by_file[fn] += nrow
            for _ in range(nrow):
                r = tuple(map(int, fi.readline().split()))
                xs = list(map(int, fo.readline().split()))
                assert xs and xs[0] == ntot and len(r) == K
                ntot += 1
                c = tuple(xs[1:])
                if c[0] > 0:
                    ours_by_file[fn][(r, c)] += 1
                    surv.append((fn, r, c))
        assert fi.readline() == "" and fo.readline() == ""
    rep["cascade_rows"] = ntot
    import shutil
    shutil.rmtree(scratch)
    fdir = os.path.join(root, "filt")
    cert_files = sorted({f[:-4] for f in os.listdir(fdir) if f.endswith(".out")}, key=fkey)
    stats_files = sorted({f[:-6] for f in os.listdir(fdir) if f.endswith(".stats")}, key=fkey)
    expected = sorted(rows_by_file, key=fkey)
    rep["filt_files"] = len(cert_files)
    if cert_files != stats_files or set(cert_files) != set(expected):
        mis.append({"what": "filt file set differs from the stored input files",
                    "only_filt": sorted(set(cert_files) - set(expected))[:20],
                    "only_inputs": sorted(set(expected) - set(cert_files))[:20]})
    tight_seen = []
    file_mis = []
    for fn in cert_files:
        cert = collections.Counter()
        for base, cnt, tight in parse_out(os.path.join(fdir, fn + ".out")):
            cert[(base, cnt)] += 1
            if tight == "YES":
                tight_seen.append(base)
        r_, s_ = parse_stats(os.path.join(fdir, fn + ".stats"))
        if cert != ours_by_file.get(fn, collections.Counter()) or r_ != rows_by_file.get(fn, -1) \
                or s_ != sum(ours_by_file.get(fn, {}).values()):
            file_mis.append({"file": fn, "cert_rows": r_, "ours_rows": rows_by_file.get(fn),
                             "cert_surv": s_, "ours_surv": sum(ours_by_file.get(fn, {}).values()),
                             "only_cert": [list(x) for x in (cert - ours_by_file.get(fn, collections.Counter()))][:5],
                             "only_ours": [list(x) for x in (ours_by_file.get(fn, collections.Counter()) - cert)][:5]})
    rep["filt_files_mismatch"] = len(file_mis)
    if file_mis:
        mis.append({"what": "cascade output differs", "files": file_mis[:20]})
    # totals
    died = collections.Counter()
    for _, _, c in surv:
        e = next((i for i in range(5) if c[i] == 0), None)
        died["died_l%d" % (2 << e) if e is not None else "persist_l32"] += 1
    ours_tot = {"survivor_rows": len(surv), "level2_improper_lifts_total": sum(c[0] for _, _, c in surv)}
    ours_tot.update(died)
    rep["cascade_totals_ours"] = ours_tot
    if ours_tot != summ["cascade"]:
        mis.append({"what": "cascade totals differ from SUMMARY", "ours": ours_tot, "cert": summ["cascade"]})
    s_ir = sum(1 for fn, _, _ in surv if fn.startswith("ir_"))
    s_ext = len(surv) - s_ir
    rep["level2_survivor_rows_ir_ext_ours"] = [s_ir, s_ext]
    if [s_ir, s_ext] != [bf["level2_survivor_rows_ir"], bf["level2_survivor_rows_ext"]]:
        mis.append({"what": "level-2 survivor split differs", "ours": [s_ir, s_ext],
                    "cert": [bf["level2_survivor_rows_ir"], bf["level2_survivor_rows_ext"]]})
    # every fiber empty by level 16
    nonempty16 = [(r, c) for _, r, c in surv if c[3] > 0]
    rep["fibers_nonempty_at_16"] = len(nonempty16)
    if nonempty16:
        mis.append({"what": "improper level-16 lifts exist", "rows": nonempty16[:20]})
    last16 = [(r, c) for _, r, c in surv if c[2] > 0 and c[3] == 0]
    tight = tuple(range(1, K + 1))
    last16_orbits = set(canon_each(K, p, [r for r, _ in last16])) if last16 else set()
    rep["rows_first_empty_at_16"] = len(last16)
    rep["rows_first_empty_at_16_trace"] = sorted({c[:4] for _, c in last16})
    rep["rows_first_empty_at_16_only_tight_orbit"] = last16_orbits == {tight}
    if last16_orbits != {tight}:
        mis.append({"what": "rows first empty at level 16 are not exactly the tight orbit",
                    "orbits": sorted(last16_orbits)[:20]})
    rep["tight_marked_rows"] = len(tight_seen)
    if [tuple(sorted(b)) for b in tight_seen] != [tight] * len(tight_seen) or len(tight_seen) != 1:
        mis.append({"what": "tight=YES marks unexpected", "rows": tight_seen[:20]})
    po = summ["persistent_orbits"]["count"]
    kd = os.path.join(root, "kills")
    nk = len(os.listdir(kd)) if os.path.isdir(kd) else 0
    rep["persistent_orbits_cert"] = po
    rep["kill_files"] = nk
    if po != 0 or nk != 0 or summ.get("level_kills"):
        mis.append({"what": "certificate has persistent orbits or kill records", "count": po, "kill_files": nk})
    rep["pass"] = not mis
    rep["seconds"] = round(time.time() - t0, 1)
    return rep


def main():
    sums = {}
    for line in open(sys.argv[1]):
        a = line.split()
        if len(a) == 2:
            sums[os.path.basename(a[1])] = a[0]
    print(json.dumps(check(sys.argv[2], sums, sys.argv[3])), flush=True)


if __name__ == "__main__":
    main()
