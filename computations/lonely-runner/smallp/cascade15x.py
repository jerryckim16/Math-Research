"""Binary cascade for k = 15 with the weighted shift lemma applied at every
level ("extended properness"), our code only (liftfree.c from the repo).

Extended-proper at level l: a witness on (1/(lp))Z, or the gcd clause, or
the weighted shift lemma (Allikvere, 'Sixteen lonely runners', Lemma 'A
weighted shift'; our notes/lonely-runner/small-primes.md, Lemma S) for some
d | l with d in DSET.  Extended properness is inherited by every lift (a
witness / a gcd divisor of l persists at multiples of l, and the residue
class mod (cl)p of a lift is contained in the class mod lp), so the retained
sets F'_l(r) satisfy F'_{2l}(r) = {lifts of F'_l(r)} minus extended-proper
ones, and F'_L(r) empty means r meets Lemma 2.2(ii) at level L.
Usage: python3 cascade15x.py p LMAX DSET < bases     (DSET e.g. 4,8,16,32 or
'none'; each base line: 15 residues mod p).  Prints per base the sizes
|F'_2|, |F'_4|, ... and, for comparison, plain sizes when DSET=none.
"""
import json
import sys
import terminal15 as T


def main():
    p, lmax = int(sys.argv[1]), int(sys.argv[2])
    D = [] if sys.argv[3] == "none" else [int(x) for x in sys.argv[3].split(",")]
    T.LF = T.liftfree_bin()
    bases = [tuple(int(x) for x in l.split()) for l in sys.stdin if l.strip()]
    for b in bases:
        cur, l, tr = [b], 1, []
        while cur and l < lmax:
            ws = T.wf_lifts(l * p, 2, cur)
            l *= 2
            nxt = []
            for lst in ws:
                for w in lst:
                    if T.gcd_clause(w, l):
                        continue
                    if any(l % d == 0 and T.shift_ok(w, d) for d in D):
                        continue
                    nxt.append(w)
            cur = sorted(set(nxt))
            tr.append(len(cur))
        print(json.dumps({"base": b, "D": D, "sizes": tr, "empty_at": l if not cur else None}), flush=True)


if __name__ == "__main__":
    main()
