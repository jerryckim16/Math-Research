"""Batch extended cascade over many level-one orbit representatives (general k).
Same definitions as xcascade.py (extended properness = witness on the level
grid, gcd clause, or Lemma S for some divisor d >= 2 of the level; with
'noshift' only the first two).  One liftfree.c call per stage and chunk.
Usage: python3 xbatch.py k p CHAIN [noshift] < reps   (CHAIN e.g. 2,3,3,2)
Prints per stage: level, number of bases still open, retained lifts; at the
end the open bases (if any) and a JSON summary line.
"""
import json
import sys
import xcascade as X


def main():
    k, p = int(sys.argv[1]), int(sys.argv[2])
    chain = [int(x) for x in sys.argv[3].split(",")]
    xs = not (len(sys.argv) > 4 and sys.argv[4] == "noshift")
    reps = [tuple(int(x) for x in l.split()) for l in sys.stdin if l.strip()]
    # level-one sanity: every rep is witness-free at level 1
    bad = 0
    for r in reps:
        for m in range(1, p):
            if all((k + 1) * min(m * x % p, p - m * x % p) >= p for x in r):
                bad += 1
                break
    cur = [(i, r) for i, r in enumerate(reps)]
    l, stages = 1, []
    for c in chain:
        ds = X.divisors(l * c) if xs else []
        nxt = []
        CH = 20000
        for s in range(0, len(cur), CH):
            part = cur[s:s + CH]
            ws = X.wf_lifts(k, l * p, c, [t for _, t in part])
            for (i, _), lst in zip(part, ws):
                for w in lst:
                    if X.gcd_clause(w, l * c) or any(X.shift_ok(w, d, k) for d in ds):
                        continue
                    nxt.append((i, w))
        l *= c
        cur = sorted(set(nxt))
        openb = len({i for i, _ in cur})
        stages.append({"level": l, "open_bases": openb, "retained": len(cur)})
        print(json.dumps(stages[-1]), flush=True)
        if not cur:
            break
    openset = sorted({i for i, _ in cur})
    for i in openset[:50]:
        print("OPEN", " ".join(map(str, reps[i])))
    print(json.dumps({"k": k, "p": p, "xshift": xs, "chain": chain, "bases": len(reps),
                      "level1_with_witness": bad, "stages": stages,
                      "closed": not cur, "open_bases": len(openset)}))


if __name__ == "__main__":
    main()
