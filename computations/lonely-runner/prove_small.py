"""Reproduce LRC(k) for small k with the prime-gate method, end to end.

Usage: python3 prove_small.py K [START_PRIME] [CHAIN] [JOBS]
  CHAIN: comma list of lift factors and 'p' (projection), e.g. 2,2,p,5
  JOBS:  number of worker processes (gates are independent; results are
         consumed in increasing order of p, so the output is the same).
  Set LRC_USE_C=1 to use the C level-1 engine (level1.c), or
  LRC_LEVEL1=cover for the minimal-cover generator (covergen.c).

Walks primes upward from START_PRIME, runs the sieve chain at each, keeps
the primes where the chain ends empty (so J(k,p) is empty), and stops as
soon as their product is >= B_k (exact integer test).  Prints a JSON
record of every gate, including failures.

What this proves (given the cited inputs; see problems/lonely-runner.md):
  LRC(k-1)  and  [J(k,p) empty for all p in P]  and  prod P >= B_k
  ==>  LRC(k).
The bound B_k is NOT computed here; it is the Malikiosis-Santos-Schymura
theorem as packaged in Rosenfeld's Corollary 3 (cited, not re-proved).
"""

import json
import sys
import time
from math import log

from sieve import B_bound_ok, log_B, run_gate


def primes_from(a):
    n = max(2, a)
    while True:
        if all(n % q for q in range(2, int(n ** 0.5) + 1)):
            yield n
        n += 1


DEFAULT_CHAIN = {3: [2, 2], 4: [2, 2, "p", 5], 5: [2, 3], 6: [2, 2, "p", 7],
                 7: [2, 2, 2], 8: [2, 2, 2, "p", 3, 3], 9: [2, 2, 2, "p", 5, 2], 10: [2, 2, 2, "p", 11]}


def _gate(args):
    k, p, chain = args
    ok, trace, S = run_gate(k, p, chain)
    return p, ok, trace, S


def main():
    k = int(sys.argv[1])
    start = int(sys.argv[2]) if len(sys.argv) > 2 else k + 2
    if len(sys.argv) > 3:
        chain = [x if x == "p" else int(x) for x in sys.argv[3].split(",")]
    else:
        chain = DEFAULT_CHAIN[k]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    used, record = [], []
    t0 = time.time()
    if jobs > 1:
        from multiprocessing import Pool
        pool = Pool(jobs)
        # finite list: Pool.imap consumes its input eagerly
        plist = [p for p in range(start, 3000)
                 if p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1))]
        results = pool.imap(_gate, ((k, p, chain) for p in plist))
    else:
        results = map(_gate, ((k, p, chain) for p in primes_from(start)))
    for p, ok, trace, S in results:
        record.append({"p": p, "J_empty": ok, "trace": trace,
                       "survivors": [list(s) for s in S][:5]})
        print(json.dumps(record[-1]), flush=True)
        if ok:
            used.append(p)
            if B_bound_ok(k, used):
                break
    if jobs > 1:
        pool.terminate()
    summary = {
        "k": k, "runners": k + 1, "chain": chain, "primes": used,
        "sum_log_p": round(sum(log(p) for p in used), 4),
        "log_B_k": round(log_B(k), 4),
        "prod_ge_B_k_exact": B_bound_ok(k, used),
        "seconds": round(time.time() - t0, 1),
    }
    print("SUMMARY " + json.dumps(summary))


if __name__ == "__main__":
    main()
