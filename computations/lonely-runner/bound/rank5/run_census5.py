"""Driver: run sectj (R = 5) over every greedy-surviving rank-5 profile with
s_5 <= AMAX at n, JOBS processes in parallel under nice.  Outputs go to
OUTDIR/n{n}_r5_{profile}.txt (written as .part, renamed when complete; a
completed file is skipped on rerun).  Extra environment (e.g. NOPRUNE=1) is
passed through to the binary.

usage: python3 run_census5.py n OUTDIR BINARY AMAX [JOBS] [REJ]
"""
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "rank4"))
from relrank_n import delta_bounds, survivors  # noqa: E402
from run_census import endpoints, QD  # noqa: E402


def run_one(args):
    n, outdir, binary, amax, rej, prof, plo, phi = args
    tag = "_".join(map(str, prof))
    out = os.path.join(outdir, f"n{n}_r5_{tag}.txt")
    if os.path.exists(out) and "SUMMARY" in open(out).read():
        return f"skip {tag}"
    t0 = time.time()
    with open(out + ".part", "w") as f:
        subprocess.run(["nice", "-n", "10", binary, str(n), str(plo), str(phi), str(QD), str(rej), str(amax)]
                       + [str(x) for x in prof], stdout=f, stderr=subprocess.DEVNULL, check=True)
    os.replace(out + ".part", out)
    summ = [l for l in open(out) if l.startswith("SUMMARY")][0].strip()
    return f"{time.time() - t0:8.1f}s {summ}"


def main():
    n, outdir, binary, amax = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
    jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    rej = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    lo, hi = endpoints(n)
    os.makedirs(outdir, exist_ok=True)
    profs = [p for p in survivors(n, 5, delta_bounds(n)) if p[-1] <= amax]
    # heaviest first (larger supports run longest)
    profs.sort(key=lambda p: -sum(p))
    tasks = [(n, outdir, binary, amax, rej, p, lo.numerator, hi.numerator) for p in profs]
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for line in ex.map(run_one, tasks):
            print(line, flush=True)
    print("DONE", len(profs), "profiles", flush=True)


if __name__ == "__main__":
    main()
