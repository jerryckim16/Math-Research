"""Rank-5 classified factor J_5 and the gate target for LRC(17), exact.

Input: census outputs of sectj.c (R = 5, support cap AMAX) for every
greedy-surviving rank-5 profile with s_5 <= AMAX (profiles with s_5 > AMAX
have no section of support <= AMAX).  For each support a <= AMAX, g_max(a)
is the largest saturated Gram determinant of an admitted section with
exactly a active coordinates; a support with no admitted section is
excluded.  Supports a > AMAX keep the coarse bound of relrank_n.J_cases:
g <= min(max prod s over surviving profiles with s_5 <= a, full_row_index(5, a)).

Interface (unchanged, bound/relrank_n.py): a rank-5 counterexample of
support a gets J(a) = (2 r_n)^2 / (C_5 tau_5 g/G(n,5,a)); J_classified =
min_a J(a); J(5) = max(1, J_classified, J_select(<= 5)).  Other ranks as in
constrained/assemble.rank_target (rank 4 classified with g_max(6) = 133),
with the constrained Schur constants of notes/lonely-runner/constrained-shape.md
where given.

usage: python3 rank5_bound.py n OUTDIR AMAX [r=C ...]
"""
import os
import sys
from fractions import Fraction as Fr
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND = os.path.dirname(HERE)
sys.path.insert(0, BOUND)
sys.path.insert(0, os.path.join(BOUND, "rank4"))
sys.path.insert(0, os.path.join(BOUND, "constrained"))
from relrank_n import J_cases, G, tau, delta_bounds, survivors, full_row_index  # noqa: E402
from flag_n import R_N, ln, lcm_upto, flag_constants  # noqa: E402
from classes import parse  # noqa: E402
from assemble import GMAX_RANK4_N17  # noqa: E402


def census_gmax(n, outdir, amax, r=5):
    D = delta_bounds(n)
    gmax, nadm, files, profs = {}, 0, 0, []
    for prof in survivors(n, r, D):
        if prof[-1] > amax:
            continue
        profs.append(prof)
        path = os.path.join(outdir, f"n{n}_r{r}_{'_'.join(map(str, prof))}.txt")
        types, recs, p = parse(path)
        assert p == prof, (path, p, prof)          # SUMMARY present: run completed
        files += 1
        for rec in recs:
            assert rec["a"] <= amax
            nadm += 1
            gmax[rec["a"]] = max(gmax.get(rec["a"], 0), rec["g"])
    return gmax, nadm, files, profs


def J5_by_support(n, gmax, amax, C5):
    D = delta_bounds(n)
    surv = survivors(n, 5, D)
    t = tau(n, 5)
    out = {}
    for a in range(6, n + 1):
        if a <= amax:
            if a not in gmax:
                out[a] = ("excluded", None)
                continue
            g = gmax[a]
            src = "census"
        else:
            ls = [s for s in surv if s[-1] <= a]
            if not ls:
                out[a] = ("excluded", None)
                continue
            g = min(max(prod(s) for s in ls), full_row_index(5, a))
            src = "coarse"
        out[a] = (src, g, (2 * R_N[n]) ** 2 / (C5 * Fr(g) / G(n, 5, a) * t))
    return out


def target(n, outdir, amax, overrides=None, gmax4=GMAX_RANK4_N17, excluded=(1, 2, 3)):
    overrides = overrides or {}
    gmax5, nadm, files, profs = census_gmax(n, outdir, amax)
    D, cases = J_cases(n)
    rn = R_N[n]
    scale = {r: (cases[r]["C_r"] / overrides[r] if r in overrides else Fr(1)) for r in cases}
    C4 = overrides.get(4, cases[4]["C_r"])
    C5 = overrides.get(5, cases[5]["C_r"])
    J4c = (2 * rn) ** 2 / (C4 * max(Fr(g) / G(n, 4, a) for a, g in gmax4.items()) * tau(n, 4))
    by_a = J5_by_support(n, gmax5, amax, C5)
    live5 = [v[2] for v in by_a.values() if v[0] != "excluded"]
    J5c = min(live5) if live5 else None
    best_sel, rows = Fr(0), {}
    for rr in sorted(cases):
        cs = cases[rr]
        best_sel = max(best_sel, cs["J_select"] * scale[rr])
        if cs["J_greedy"] is None or rr in excluded:
            rows[rr] = "excluded"
            continue
        if rr == 4:
            rows[rr] = max(Fr(1), J4c, best_sel)
        elif rr == 5:
            rows[rr] = "excluded" if J5c is None else max(Fr(1), J5c, best_sel)
        else:
            rows[rr] = max(Fr(1), cs["J_greedy"] * scale[rr], best_sel)
    rows[n - 1] = max(Fr(1), best_sel)
    live = {k: v for k, v in rows.items() if v != "excluded"}
    arg = min(live, key=lambda k: live[k])
    K, _, _ = flag_constants(n)
    plain = n * (-ln(K) / 2 + ln(rn) - ln(n)) - ln(lcm_upto(n + 1))
    gain = n * ln(live[arg]) / 2
    return {"gmax5": gmax5, "admitted": nadm, "files": files, "profiles": len(profs),
            "J5_by_support": by_a, "J(r)": rows, "J_min": live[arg], "argmin": arg,
            "plain": plain, "gain": gain, "target": plain - gain}


if __name__ == "__main__":
    n, outdir, amax = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    ov = {}
    for a in sys.argv[4:]:
        k, v = a.split("=")
        ov[int(k)] = Fr(v)
    res = target(n, outdir, amax, ov)
    print("files", res["files"], "of", res["profiles"], "profiles; admitted records", res["admitted"])
    print("g_max by support (census):", dict(sorted(res["gmax5"].items())))
    for a, v in res["J5_by_support"].items():
        print("  a=%2d %-8s g=%s J=%s" % (a, v[0], v[1], None if v[0] == "excluded" else round(float(v[2]), 4)))
    for r in sorted(res["J(r)"])[:7]:
        v = res["J(r)"][r]
        print("  J(%d) =" % r, v if v == "excluded" else float(v))
    print("J_min", float(res["J_min"]), "at rank", res["argmin"])
    print("target", res["target"])
