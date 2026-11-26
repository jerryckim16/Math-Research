"""Per-shard consistency checks and JSON record for run_gate251.sh.

usage: python3 -I shard_check.py WORKDIR/pP SHARD SECONDS
Writes shard_<i>.json and exits 0 only if every check passes:
  covergen minimal_covers == covers read by expand; expand bad == 0;
  bases expanded == bases entering stage 1 (x2); stage-1 open == stage-2 bases;
  no base open after stage 2 (3,3,2,2), none capped, no level-one witness;
  re-check with cascade_verify.c: no level-2 survivor for the sampled bases
  closed at 2 (batch); for the sampled bases open after x2 and for every base
  closing at level >= 9, the per-base chain 3,3,2,2 closes at the same level
  as xcascq (verify_bases.py).
"""
import json
import os
import re
import sys


def kv(path, tag):
    txt = open(path).read()
    line = [l for l in txt.splitlines() if l.startswith(tag)]
    if not line:
        raise ValueError(f"{path}: no {tag} line")
    return line[-1]


def xcsum(path):
    l = kv(path, "XCSUM")
    f = l.split()
    d = {f[i]: int(f[i + 1]) for i in range(1, 9, 2)}
    hist = {}
    if "hist" in f:
        for t in f[f.index("hist") + 1:]:
            a, b = t.split(":")
            hist[int(a)] = int(b)
    d["hist"] = hist
    return d


def main():
    D, i, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    P = lambda name: os.path.join(D, name)
    cg = open(P(f"cg{i}.err")).read()
    m = re.findall(r"minimal_covers (\d+)", cg)
    nodes = re.findall(r"^nodes (\d+)", cg, re.M)
    ex = kv(P(f"ex{i}.err"), "EXPAND").split()
    exd = {ex[j]: int(ex[j + 1]) for j in range(1, len(ex) - 1, 2)}
    x1, x2 = xcsum(P(f"x1_{i}.err")), xcsum(P(f"x2_{i}.err"))
    cv2 = int(open(P(f"cv2_{i}.n")).read().split()[0])
    vb = json.load(open(P(f"vb_{i}.json")))
    nlog = sum(1 for _ in open(P(f"log{i}.json"))) if os.path.exists(P(f"log{i}.json")) else 0
    open2 = sum(1 for l in open(P(f"open2_{i}.txt")) if l.strip())
    hist = dict(x1["hist"])
    for a, b in x2["hist"].items():
        hist[a] = hist.get(a, 0) + b
    checks = {
        "covergen_finished": bool(m) and bool(nodes),
        "covers": bool(m) and int(m[-1]) == exd["covers"],
        "expand_no_bad_lines": exd["bad"] == 0,
        "bases_into_stage1": exd["bases"] == x1["bases"],
        "stage1_open_into_stage2": x1["open"] == x2["bases"],
        "none_open": x2["open"] == 0 and open2 == 0,
        "none_capped": x1["capped"] == 0 and x2["capped"] == 0,
        "no_level1_witness": x1["lvl1_witness"] == 0 and x2["lvl1_witness"] == 0,
        "histogram_total": sum(hist.values()) == exd["bases"],
        "recheck_level2_empty": cv2 == 0,
        "recheck_per_base_agree": vb["agree"] == vb["n"] and not vb["mismatch"],
    }
    rec = {"shard": i, "seconds": secs, "nodes": int(nodes[-1]) if nodes else None,
           "minimal_covers": int(m[-1]) if m else None, "bases": exd["bases"],
           "sampled_1pct": exd["sampled"], "closed_hist": {str(a): b for a, b in sorted(hist.items())},
           "stage2_bases": x2["bases"], "logged_ge9_or_open": nlog,
           "recheck": {"level2_batch_survivors": cv2, "per_base": vb["n"], "per_base_levels": vb["levels"]}, "checks": checks,
           "ok": all(checks.values())}
    json.dump(rec, open(P(f"shard_{i}.json"), "w"))
    if not rec["ok"]:
        print("SHARD", i, "FAILED", [k for k, v in checks.items() if not v], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
