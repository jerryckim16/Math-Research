"""Summarise the step-3 re-check results into a markdown table
(results/lrc14_gates/*.json, results/lrc13_kills.jsonl)."""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in glob.glob(os.path.join(HERE, "results/lrc14_gates/gate_*.json")):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    rows.append(d)
rows.sort(key=lambda d: d["p"])
print("| p | type | mode | stored rows (ir + ext) | survivor orbits ours / cert | persistent orbits | kills checked | pass | s |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for d in rows:
    typ = "near-gcd" if d["claim_type"].startswith("divisibility") else "J empty"
    mode = "sample %d" % d["sample"] if d.get("sample") else "full"
    print("| %d | %s | %s | %d + %d | %d / %d | %s | %d | %s | %.0f |" % (
        d["p"], typ, mode, d["rows_ir"], d["ext_rows"], d["cascade_survivor_orbits_ours"],
        d["cascade_survivor_orbits_cert"], d["persistent_orbits_equal"], d["kill_orbits"],
        "PASS" if d["pass"] else "FAIL", d["seconds"]))
print()
print("LRC(14) gates checked:", len(rows), " full:", sum(1 for d in rows if not d.get("sample")),
      " all pass:", all(d["pass"] for d in rows))
k13 = [json.loads(l) for l in open(os.path.join(HERE, "results/lrc13_kills.jsonl"))]
k13 = {d["p"]: d for d in k13}
print("LRC(13) kill gates:", sorted(k13), " all pass:", all(d["pass"] for d in k13.values()))
