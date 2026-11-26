"""Summary of the larger closure samples of run_big.sh (heuristic).
Usage: python3 bigsummary.py P1 P2 ...   prints per prime: samples, closed at level 2, closing
levels of the rest under 3,3,2,2, number not closed; then the totals."""
import json
import os
import sys

import rio

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "results")


def main():
    tot = bad_tot = 0
    print("| $p$ | samples | closed at 2 | rest closed at 3 / 9 / 18 / 36 | not closed |")
    print("| --- | --- | --- | --- | --- |")
    for p in map(int, sys.argv[1:]):
        a2 = [json.loads(l) for l in rio.opn(os.path.join(R, f"big2_p{p}.jsonl"))]
        f3 = os.path.join(R, f"big3322_p{p}.jsonl")
        a3 = {tuple(r["base"]): r for r in map(json.loads, rio.opn(f3))} if rio.exists(f3) else {}
        lv, bad = {}, 0
        for r in a2:
            if r["empty_at"]:
                continue
            x = a3.get(tuple(r["base"]))
            if not x or not x["empty_at"]:
                bad += 1
            else:
                lv[x["empty_at"]] = lv.get(x["empty_at"], 0) + 1
        c2 = sum(1 for r in a2 if r["empty_at"])
        tot += len(a2)
        bad_tot += bad
        print(f"| {p} | {len(a2)} | {c2} | {lv.get(3, 0)} / {lv.get(9, 0)} / {lv.get(18, 0)} / {lv.get(36, 0)} | {bad} |")
    print(f"\ntotal samples {tot}, not closed {bad_tot}")


if __name__ == "__main__":
    main()
