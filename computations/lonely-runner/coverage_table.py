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
chk = {}
for f in glob.glob(os.path.join(R, "lrc14_gates", "gate_*.json")):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    old = chk.get(d["p"])
    if old is None or (old.get("sample") and not d.get("sample")):
        chk[d["p"]] = d
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
    d = chk.get(p)
    if d:
        n_any += 1
        mode = "sampled (%d)" % d["sample"] if d.get("sample") else "full"
        if not d.get("sample"):
            n_full += 1
        rws = "full"
        cas = kil = mode
        verdict = "PASS" if d["pass"] else "**FAIL**"
    else:
        rws = cas = kil = "not checked"
        verdict = "—"
    c = comp.get(p)
    cs = ("full (%d orbits, equal)" % c["orbits_ours"] if c["equal"] else "**differs**") if c else "not checked"
    rows.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (p, typ, hs, rws, cas, kil, cs, verdict))
print("| p | type | archive SHA-256 | rows improper | cascade | kill | level-one completeness | result |")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")
print("\n".join(rows))
ok = all(d["pass"] for d in chk.values()) and all(c["equal"] for c in comp.values())
print()
print("**Verdict:** independent re-check of %d/71 LRC(14) gates (%d in full, %d sampled); "
      "level-one completeness at p = %s; %s." % (
          n_any, n_full, n_any - n_full, ", ".join(map(str, sorted(comp))) or "none",
          "no discrepancy found" if ok else "DISCREPANCY FOUND"))
