"""Track the tight orbit (1..k) through a lift chain at given primes.

Usage: python3 tight_chain.py k "c1 c2 ..." p1 [p2 ...]   (env NG=1: apply Lemma NG)
At each step: liftfree.c witness-free lifts by c, then orbit_filter.c (gcd clause,
optional NG, unit-orbit canonical form), dedupe.  Prints per-prime JSON traces.
Only this one level-one orbit is examined: these are not gate checks.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
B = tempfile.mkdtemp(prefix="tc_")
subprocess.run(["cc", "-O3", "-o", f"{B}/lf", os.path.join(HERE, "..", "liftfree.c")], check=True)
subprocess.run(["cc", "-O3", "-o", f"{B}/of", os.path.join(HERE, "orbit_filter.c")], check=True)

k = int(sys.argv[1])
chain = list(map(int, sys.argv[2].split()))
ng = ["ng"] if os.environ.get("NG") else []
for p in map(int, sys.argv[3:]):
    reps, l, tr = [tuple(range(1, k + 1))], 1, []
    for c in chain:
        if not reps:
            break
        inp = "".join(" ".join(map(str, r)) + "\n" for r in reps)
        lf = subprocess.run([f"{B}/lf", str(k), str(l * p), str(c)], input=inp, capture_output=True, text=True, check=True)
        l *= c
        of = subprocess.run([f"{B}/of", str(k), str(p), str(l), "idx"] + ng, input=lf.stdout, capture_output=True, text=True, check=True)
        reps = sorted({tuple(map(int, x.split())) for x in of.stdout.splitlines() if x.strip()})
        wf = int(lf.stderr.split("witness_free")[1].split()[0])
        tr.append([l, wf, len(reps)])
    print(json.dumps({"k": k, "p": p, "chain": chain, "trace_level_wf_orbits": tr,
                      "dies_by": tr[-1][0] if not reps else None, "survivors": reps[:3]}), flush=True)
