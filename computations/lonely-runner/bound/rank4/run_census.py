"""Driver: run the C section census (sect.c) over every greedy-surviving
support profile of rank r at a given n, one process per profile (each well
under 25 min), under nice.  Outputs go to OUTDIR/n{n}_r{r}_{profile}.txt.

usage: python3 run_census.py n r OUTDIR SECT_BINARY [REJ]
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from relrank_n import delta_bounds, survivors  # noqa: E402

QD = 10 ** 6


def endpoints(n):
    lo, hi = delta_bounds(n)
    assert QD % lo.denominator == 0 and QD % hi.denominator == 0
    return lo * QD, hi * QD


def main():
    n, r, outdir, binary = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    rej = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    plo, phi = endpoints(n)
    assert plo.denominator == 1 and phi.denominator == 1
    os.makedirs(outdir, exist_ok=True)
    D = delta_bounds(n)
    for prof in survivors(n, r, D):
        tag = "_".join(map(str, prof))
        out = os.path.join(outdir, f"n{n}_r{r}_{tag}.txt")
        if os.path.exists(out) and "SUMMARY" in open(out).read():
            continue
        t0 = time.time()
        with open(out + ".part", "w") as f:
            subprocess.run(["nice", "-n", "10", binary, str(n), str(plo.numerator), str(phi.numerator),
                            str(QD), str(rej)] + [str(x) for x in prof], stdout=f, check=True)
        os.replace(out + ".part", out)
        summ = [l for l in open(out) if l.startswith("SUMMARY")][0].strip()
        print(f"{time.time() - t0:8.1f}s {summ}", flush=True)


if __name__ == "__main__":
    main()
