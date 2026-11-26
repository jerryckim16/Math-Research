"""Gate targets for LRC(17) with constrained shape constants (exact).

Relation-rank target: the assembly of bound/rank4/rank4_bound.classified
(rank-4 classified factor with g_max(6) = 133, G(17,4,6) = 1; ranks 1-3
excluded; coarse ranks >= 5 from bound/relrank_n.J_cases), with the Schur
shape constants C_r replaced by proved constrained values where given.
Each J for rank r is proportional to 1/C_r, so an override C_r -> C'_r
multiplies J_greedy(r), J_select(r) (and J_4 classified) by C_r / C'_r.
The radius r_n cancels from this target.

Flag targets: plain flag (bound/flag_n.py) and Lemma H + M
(bound/hyperplane.py) with the proved shape radius r_n replaced by a
proved constrained radius r'_n: the target moves by n ln(r'_n / r_n).
"""
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
BOUND = os.path.dirname(HERE)
sys.path.insert(0, BOUND)
from relrank_n import J_cases, G, tau  # noqa: E402
from flag_n import R_N, ln, lcm_upto, flag_constants  # noqa: E402

GMAX_RANK4_N17 = {6: 133}        # notes/lonely-runner/bound-rank4.md, section 4 (census, tested in test_bound.py)


def rank_target(n=17, overrides=None, gmax=GMAX_RANK4_N17, excluded=(1, 2, 3)):
    overrides = overrides or {}
    D, cases = J_cases(n)
    rn = R_N[n]
    scale = {r: (cases[r]["C_r"] / overrides[r] if r in overrides else Fr(1)) for r in cases}
    r = 4
    C4 = overrides.get(4, cases[4]["C_r"])
    worst = max(Fr(g) / G(n, r, a) for a, g in gmax.items())
    J4c = (2 * rn) ** 2 / (C4 * worst * tau(n, r))
    best_sel, rows = Fr(0), {}
    for rr in sorted(cases):
        cs = cases[rr]
        best_sel = max(best_sel, cs["J_select"] * scale[rr])
        if cs["J_greedy"] is None or rr in excluded:
            rows[rr] = "excluded"
            continue
        if rr == 4:
            rows[rr] = max(Fr(1), J4c, best_sel)
        else:
            rows[rr] = max(Fr(1), cs["J_greedy"] * scale[rr], best_sel)
    rows[n - 1] = max(Fr(1), best_sel)
    live = {k: v for k, v in rows.items() if v != "excluded"}
    arg = min(live, key=lambda k: live[k])
    Jmin = live[arg]
    K, _, _ = flag_constants(n)
    plain = n * (-ln(K) / 2 + ln(rn) - ln(n)) - ln(lcm_upto(n + 1))
    gain = n * ln(Jmin) / 2
    return {"J(r)": rows, "J_min": Jmin, "argmin": arg, "J4_classified": J4c,
            "C_used": {k: overrides.get(k, cases[k]["C_r"]) for k in cases},
            "plain": plain, "gain": gain, "target": plain - gain}


def flag_targets(n=17, r_new=None):
    """Plain flag and Lemma H + M targets (hyperplane.targets) at r_n and at
    r_new; both are n(-ln K/2 + ln r - ln n) - ln lcm(2..n+1)."""
    import hyperplane
    old = hyperplane.targets(n)
    out = {"plain": old["plain target"], "lemmaHM": old["new target"]}
    if r_new is not None:
        new = hyperplane.targets(n, r_new)
        out.update(plain_new=new["plain target"], lemmaHM_new=new["new target"],
                   shift=new["plain target"] - old["plain target"])
    return out


if __name__ == "__main__":
    base = rank_target()
    print("regression target", base["target"], "J_min", float(base["J_min"]), "rank", base["argmin"])
    if len(sys.argv) > 1:
        ov = {}
        for a in sys.argv[1:]:
            k, v = a.split("=")
            ov[int(k)] = Fr(v)
        res = rank_target(overrides=ov)
        for r in sorted(res["J(r)"])[:7]:
            v = res["J(r)"][r]
            print("  J(%d) =" % r, v if v == "excluded" else float(v))
        print("new target", res["target"], "J_min", float(res["J_min"]), "rank", res["argmin"], "gain vs base", base["target"] - res["target"])
