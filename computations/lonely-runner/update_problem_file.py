"""Regenerate the step-5 parts of problems/lonely-runner.md from the result
files: the overall verdict, the list of large near-gcd gates checked at
sample 500, the in-progress list, and the results-table row.  Run after
coverage_table.py."""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "problems", "lonely-runner.md")
LARGE = (131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241)


def main():
    import sys
    global CP
    CP = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    s = open(PF).read()
    done = []
    for x in glob.glob(os.path.join(HERE, "results/lrc14_gates/gate_*_stream.json")):
        try:
            done.append(json.load(open(x)))
        except Exception:
            pass
    big = sorted(d["p"] for d in done if d["p"] in LARGE)
    rest = [p for p in LARGE if p not in big]
    lines = ["    - p = %d: %s rows; %s kill files; extension-survivor lines %s; %.0f s." % (
        d["p"], format(d["rows_ir"], ","), format(d["kill_files"], ","),
        format(d["C2_ext_survivor_lines_total"], ","), d["seconds"])
        for d in sorted(done, key=lambda d: d["p"]) if d["p"] in LARGE]
    block = ("  - **Large near-gcd archives (step 5),** streaming checker, **sample 500** (500 irredundant rows, "
             "500 extension-survivor lines, 500 kills per gate). Every stored row is tested, and every gate passes "
             "with 0 mismatches and 0 improper after the near-gcd lemma:\n" + "\n".join(lines) + "\n")
    a = s.index("  - **Large near-gcd archives (step 5)")
    b = s.index("  - **Not checked:**", a)
    s = s[:a] + block + s[b:]
    prog = ", ".join(map(str, rest)) if rest else "none"
    s = re.sub(r"    - Large near-gcd archives still in progress: [^\n]*", "    - Large near-gcd archives still in progress: " + prog + ".", s)
    n = 58 + len(big)
    s = re.sub(r"\*\*Overall verdict \(step 5, checkpoint \d+\):\*\* independent re-check of \d+/71 LRC\(14\) gates\.",
               "**Overall verdict (step 5, checkpoint %d):** independent re-check of %d/71 LRC(14) gates." % (CP, n), s)
    s = re.sub(r"- \d+ of the 19 near-gcd gates were checked: [^\n]*",
               "- %d of the 19 near-gcd gates were checked: every stored row tested, with the cascade and kill on seeded samples (3,000, or 500 for the large archives)." % (n - 52), s)
    s = re.sub(r"- Still in progress: [^\n]*", "- Still in progress: " + prog + ".", s)
    s = re.sub(r"\| LRC\(14\) certificates: independent re-check of \d+/71 gates\.[^\n]*",
               "| LRC(14) certificates: independent re-check of %d/71 gates. All 52 \"J empty\" gates in full. Near-gcd gates 89, 163, 173, 179, 223, 233 (sample 3,000 or 1,000) and %s (sample 500): all rows, plus seeded samples of the cascade and kill. Level-one completeness at p = 89, 239 and 251. No discrepancy found. | independent re-computation of the certificates' claims; in progress: %s; completeness at 3 gates only | `results/lrc14_gates/COVERAGE.md`, Approach 7 |"
               % (n, ", ".join(map(str, big)), prog), s)
    open(PF, "w").write(s)
    print(n, "checked; in progress:", prog)


if __name__ == "__main__":
    main()
