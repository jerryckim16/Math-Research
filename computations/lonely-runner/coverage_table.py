"""Per-gate coverage table for the independent re-check of Allikvere's
LRC(14) certificates (71 gates).  Inputs: results/allikvere_gates_lrc14.json
(the certificate's own gate list, gates.json from the Zenodo record),
results/lrc14_sha256_check.txt (sha256sum -c output), results/lrc14_gates/*.json.
Output: markdown on stdout."""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "results")
gates = json.load(open(os.path.join(R, "allikvere_gates_lrc14.json")))
sha = {}
for line in open(os.path.join(R, "lrc14_sha256_check.txt")):
    if ":" in line:
        name, st = line.rsplit(":", 1)
        sha[name.strip()] = st.strip()
chk = {}   # p -> list of records (step 8: several records per gate are merged)
for f in glob.glob(os.path.join(R, "lrc14_gates", "gate_*.json")):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    chk.setdefault(d["p"], []).append(d)


def coverage(d):
    """(cascade_full, cascade_text, kills_checked, kills_total, kill_text) for one record."""
    if d.get("mode") == "stream":
        full_cas = d["C1_ir_rows_sampled"] >= d["rows_ir"] and d["C2_ext_lines_sampled"] >= d["C2_ext_survivor_lines_total"]
        cas = "full" if full_cas else "sampled (%d ir rows + %d ext survivor lines)" % (d["C1_ir_rows_sampled"], d["C2_ext_lines_sampled"])
        return full_cas, cas, d["D_kills_sampled"], d["kill_files"]
    full_cas = not d.get("sample")
    cas = "full" if full_cas else "sampled (%d)" % d["sample"]
    total = d.get("kill_files", d.get("persistent_orbits_cert"))
    if d.get("kill_skipped"):
        return full_cas, cas, 0, total
    if "kill_files" not in d and d.get("sample"):
        total = None   # older sampled records did not store the kill-file count
    return full_cas, cas, d["kill_orbits"], total


comp = {}
for f in glob.glob(os.path.join(R, "lrc14_gates", "completeness_*.json")):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    comp[d["p"]] = d
rows = []
n_any = n_full = 0
for p in sorted(int(x) for x in gates):
    g = gates[str(p)]
    typ = "J empty" if g["variant"].startswith("decomposition") else "near-gcd"
    h = sha.get("evidence_%d_s0.tgz" % p)
    hs = "OK" if h == "OK" else ("FAIL" if h else "not downloaded")
    ds = chk.get(p, [])
    if ds:
        n_any += 1
        covs = [coverage(d) for d in ds]
        best_cas = max(covs, key=lambda c: (c[0], 0))
        best_kill = max(covs, key=lambda c: c[2])
        totals = [c[3] for c in covs if c[3]]
        ktot = max(totals) if totals else None
        rws = "full (%d rows)" % ds[0]["rows_ir"] if any(d.get("mode") == "stream" for d in ds) else "full"
        cas = best_cas[1]
        if ktot is not None and best_kill[2] >= ktot:
            kil = "full (%d)" % ktot if any(d.get("mode") == "stream" or d.get("kill_files") for d in ds) else "full"
        elif ktot is not None:
            kil = "sampled (%d of %d)" % (best_kill[2], ktot)
        else:
            kil = "sampled (%d)" % best_kill[2]
        full_kill = ktot is not None and best_kill[2] >= ktot
        if best_cas[0] and full_kill:
            n_full += 1
        verdict = "PASS" if all(d["pass"] for d in ds) else "**FAIL**"
    else:
        rws = cas = kil = "not checked"
        verdict = "—"
    c = comp.get(p)
    cs = ("full (%d orbits, equal)" % c["orbits_ours"] if c["equal"] else "**differs**") if c else "not checked"
    rows.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (p, typ, hs, rws, cas, kil, cs, verdict))
print("| p | type | archive SHA-256 | rows improper | cascade | kill | level-one completeness | result |")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")
print("\n".join(rows))
ok = all(d["pass"] for ds in chk.values() for d in ds) and all(c["equal"] for c in comp.values())
print()
print("**Verdict:** independent re-check of %d/71 LRC(14) gates (%d in full, %d sampled); "
      "level-one completeness at p = %s; %s." % (
          n_any, n_full, n_any - n_full, ", ".join(map(str, sorted(comp))) or "none",
          "no discrepancy found" if ok else "DISCREPANCY FOUND"))
