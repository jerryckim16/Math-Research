"""Rank-4 classified factor J_4 and the new gate target, exact arithmetic.

Input: the census outputs of sect.c (R = 4) for every greedy-surviving
profile at n (run_census.py).  For each support size a, g_max(a) is the
largest saturated Gram determinant of an admitted section (no support-<=2
line, signed Riesz not excluded at the delta enclosure, greedy profile
consistent) with exactly a active coordinates.  A support with no admitted
section is excluded.

The interface is unchanged from relrank_n.py (coarse bound): a
counterexample whose full odd space O has rank 4 and support a satisfies
(prod v)^(2/n) <= C_4 g tau_4 / (G(n,4,a) 4 n^2 K_n); relative to the plain
bound this is the factor J = (2 r_n)^2 / (C_4 tau_4 g/G).  We replace the
coarse g <= min(max prod s, full_row_index(4,a)) by the classified g_max(a).
J(4) = max(1, J_classified, J_select(<=4)) as in relrank_n.final.
"""
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from relrank_n import J_cases, G, tau, delta_bounds, survivors  # noqa: E402
from flag_n import R_N, ln, lcm_upto, flag_constants  # noqa: E402
from classes import parse  # noqa: E402


def census_gmax(n, outdir, r=4):
    D = delta_bounds(n)
    gmax, nadm, files = {}, 0, 0
    for prof in survivors(n, r, D):
        path = os.path.join(outdir, f"n{n}_r{r}_{'_'.join(map(str, prof))}.txt")
        types, recs, p = parse(path)          # raises if missing
        assert p == prof, (path, p, prof)      # SUMMARY present: run completed
        files += 1
        for rec in recs:
            nadm += 1
            gmax[rec["a"]] = max(gmax.get(rec["a"], 0), rec["g"])
    return gmax, nadm, files


def classified(n, outdir, excluded=(1, 2, 3)):
    """excluded: ranks proved excluded elsewhere (ranks 1-3 at n = 17 by
    rank_exclusion.exclude, tested in test_bound.py)."""
    gmax, nadm, files = census_gmax(n, outdir)
    D, cases = J_cases(n)
    r = 4
    C, t = cases[r]["C_r"], tau(n, r)
    worst = max((Fr(g) / G(n, r, a) for a, g in gmax.items()), default=None)
    J4c = None if worst is None else (2 * R_N[n]) ** 2 / (C * worst * t)
    best_sel, rows = Fr(0), {}
    for rr in sorted(cases):
        cs = cases[rr]
        best_sel = max(best_sel, cs["J_select"])
        if cs["J_greedy"] is None or rr in excluded:
            rows[rr] = "excluded"
            continue
        if rr == 4:
            rows[rr] = "excluded" if J4c is None else max(Fr(1), J4c, best_sel)
        else:
            rows[rr] = max(Fr(1), cs["J_greedy"], best_sel)
    rows[n - 1] = max(Fr(1), best_sel)
    live = {k: v for k, v in rows.items() if v != "excluded"}
    arg = min(live, key=lambda k: live[k])
    Jmin = live[arg]
    K, _, _ = flag_constants(n)
    plain = n * (-ln(K) / 2 + ln(R_N[n]) - ln(n)) - ln(lcm_upto(n + 1))
    gain = n * ln(Jmin) / 2
    return {"gmax": gmax, "admitted": nadm, "files": files, "C4": C, "J4_classified": J4c,
            "J(r)": rows, "J_min": Jmin, "argmin": arg, "plain": plain, "gain": gain,
            "target": plain - gain}


if __name__ == "__main__":
    n, outdir = int(sys.argv[1]), sys.argv[2]
    res = classified(n, outdir)
    print("files", res["files"], "admitted orbit reps", res["admitted"])
    print("g_max by support:", dict(sorted(res["gmax"].items())))
    print("C_4 <=", float(res["C4"]), " J_4 classified =", res["J4_classified"], "~", float(res["J4_classified"]) if res["J4_classified"] else None)
    for r in sorted(res["J(r)"])[:6]:
        v = res["J(r)"][r]
        print("  J(%d) =" % r, v if v == "excluded" else float(v))
    print("J_min", float(res["J_min"]), "at rank", res["argmin"])
    print("plain ", res["plain"])
    print("gain  ", res["gain"])
    print("target", res["target"])
