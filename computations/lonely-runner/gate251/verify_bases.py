"""Independent per-base re-check with k17struct/cascade_verify.c.

For each base (one per line on stdin), follow the chain 3,3,2,2 from level
one with cascade_verify (its own witness search, gcd clause and Lemma NG,
full unit-orbit canonical forms; `cv k p l c ng`, then sort -u) until the
retained set is empty, and compare the closing level with the one xcascq
reports for the same base and chain.  Prints one JSON summary line.

usage: python3 -I verify_bases.py BIN_DIR k p < bases
"""
import json
import subprocess
import sys

CHAIN = [3, 3, 2, 2]


def cv_close(cv, k, p, base):
    reps, L = [base], 1
    for c in CHAIN:
        out = subprocess.run([cv, str(k), str(p), str(L), str(c), "ng"], input="\n".join(reps) + "\n",
                             capture_output=True, text=True, check=True).stdout
        reps = sorted(set(l.strip() for l in out.splitlines() if l.strip()))
        L *= c
        if not reps:
            return L
    return None


def main():
    bindir, k, p = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    bases = [l.strip() for l in sys.stdin if l.strip()]
    if not bases:
        print(json.dumps({"n": 0, "agree": 0, "mismatch": [], "levels": {}}))
        return
    xo = subprocess.run([bindir + "/xcascq", str(k), str(p), "3,3,2,2"], input="\n".join(bases) + "\n",
                        capture_output=True, text=True, check=True).stdout.splitlines()
    xl = [json.loads(l)["empty_at"] for l in xo]
    assert len(xl) == len(bases)
    mism, levels = [], {}
    for b, x in zip(bases, xl):
        c = cv_close(bindir + "/cv", k, p, b)
        levels[str(c)] = levels.get(str(c), 0) + 1
        if c != x or c is None:
            mism.append({"base": b, "cascade_verify": c, "xcascq": x})
    print(json.dumps({"n": len(bases), "agree": len(bases) - len(mism), "mismatch": mism, "levels": levels}))
    sys.exit(1 if mism else 0)


if __name__ == "__main__":
    main()
