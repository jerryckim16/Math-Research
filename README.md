# Math Research

A workspace for attacking problems in mathematics — open conjectures, competition-style problems, and anything in between — with proofs checked as rigorously as possible.

**Progress site:** https://jerryckim16.github.io/Math-Research/ (rebuilt on every merge to `main` by `.github/workflows/pages.yml` from `site/build.py`).

## Layout

| Folder | What goes there |
| --- | --- |
| `problems/` | One file per problem: statement, status, approaches tried, results |
| `lean/` | Lean 4 formalizations of verified results |
| `computations/` | Scripts and data supporting numerical or exhaustive checks |
| `notes/` | Literature notes, sketches, and failed routes worth remembering |
| `site/` | Generator for the progress website |

## Working rules

1. **State the claim exactly** before trying to prove it.
2. **Label evidence honestly**: *proved*, *Lean-verified*, *computationally checked up to N*, *heuristic*, or *conjectured*. A bounded computation is never a proof.
3. **Keep failed routes.** Write down why an approach broke so it isn't retried blindly.
4. **Cite sources** for any external theorem used, with its exact hypotheses.

## Adding a problem

Copy `problems/TEMPLATE.md` to `problems/<short-name>.md` and fill it in.

## Status

| Problem | Status |
| --- | --- |
| [Erdős–Szekeres (ES(7) = 33?)](problems/erdos-szekeres.md) | parked — ES(6) = 17 reproduced with a checked LRAT proof; ES(7) estimated at ≥ 375 CPU-years with current encodings, so it needs a structural idea |
| [Lonely Runner](problems/lonely-runner.md) | in progress (current focus: 18 runners, the first unclaimed case) — LRC(3)–LRC(10) reproduced; Allikvere's 15-runner certificates re-checked; 16 and 17 runners are claimed on Zenodo (unrefereed); **all 59 of Allikvere's 16-runner gate certificates re-checked with our own code, no discrepancy** (level-one completeness still unchecked); proved 18-runner gate target lowered from 670.28 to 647.53; tight orbit at 18 runners dies at level 18 for all p ≥ 353 (proved); the full 18-runner computation is estimated far beyond one machine |
| [EFX allocations](problems/efx-allocations.md) | parked — EFX existence for 4 additive agents and 8 goods reproduced, certificate-checked by two SMT solvers (Z3, cvc5); 9 goods projected at 10³–10⁴ CPU-hours |
| [Frankl union-closed sets](problems/frankl-union-closed.md) | parked — the finite computations and analytic glue behind the 0.38289 record were re-verified; the measure-theoretic layer is not |
| [Chromatic number of the plane](problems/chromatic-number-plane.md) | χ ≥ 6 Lean-verified (OpenAI's formal proof re-run here from source and kernel-replayed with `leanchecker`, including a from-scratch replay of all 787k constants); χ ≥ 5 re-proved with our own LRAT certificate; open between 6 and 7 |
| [Andrews–Curtis (length-14 frontier)](problems/andrews-curtis.md) | in progress — Theorems 1–4 of Carreras (arXiv:2607.23611, unrefereed) **Lean-verified**: our Lean 4 checker replays the author's certificates, kernel-checked by `decide +kernel` against our own definition of AC moves; Theorems 3–4 re-found by our own search; the paper's Theorem 6 exhaustions (caps 25–27) reproduced exactly; new: cap-28/29/30 exhaustions (47.5M, 88.6M, 351.4M states) with no common forward-reachable state, so directed d_GS ≥ 30 for P1, P2 vs AK(3); found that the GS graph is directed, so these (and Theorem 6) bound only directed paths — a possible gap in the paper; new: exact predecessor enumeration (checked exhaustively) and an undirected search find no undirected GS path below energy 31, so Theorem 6's bounds hold undirected too and the gap is closed; AK(3) open |
| [Kissing numbers (2026 lower bounds, dims 11, 12, 19, 25–43)](problems/kissing-numbers.md) | in progress — independent exact pairwise checks of unrefereed 2026 claims, validated first on D4, D5, E8 and Leech; **certificate-checked** (all pairs, exact), 36 configurations, no violation found: Qiushi Engine (arXiv:2609.35051) dims 25, 27, 32–39, 43 and Lin (arXiv:2611.03682) dims 32–35, 37–39, rebuilt from pinned data with our own code (ℚ(√2,√3) coordinates through an exact field checker); **new:** the 2026 claims on arXiv were surveyed: data, sizes, and what each would take to check. A. Kravatskiy's repository records in dims 25–33 (197,586 … 370,528 points, up to 6.9·10¹⁰ pairs each; 25D, 29D, 32D, 33D rebuilt from his witness/trade files, two implementations for the integer parts; 32D/33D shown to be Lin's configurations with a few thousand points exchanged) are checked, as are τ₁₁ ≥ 604 (EinsteinArena, arXiv:2606.10402, rebuilt from the paper; 19,704 contacts, matching the Station paper's count) and τ₁₂ ≥ 841 (arXiv:2606.18984, the published decimals read exactly; margin 1/4 − cos² = 6.2·10⁻⁸), and Ho's τ₁₉ ≥ 11,948 (arXiv:2603.10425). **New:** Kravatskiy's 34–39D records (391,004; 415,360; 506,628; 544,666; 652,076; 783,468), each stored as a chain of edits on parent certificates, rebuilt by our own code. Our 34D rebuild reproduces his final certificate hash, and our 39D rebuild reproduces his layer counts exactly. All pairs pass (7.6·10¹⁰–3.1·10¹¹ per dimension). The 36D points lie in K₁₂³ and are checked under the Gram form; the 39D rational heads are checked through an exact class-threshold decomposition; negative controls with a wrong chain stage or parent fail. For all six, a second implementation (numpy, plus the field checker's interval mode for the 37D √2 rows) agrees exactly. **New:** Kravatskiy's 40–43D records (1,126,365; 1,460,066; 1,991,475; 2,921,073) are rebuilt with our own shell enumerator from his affine-shell data (rank-40 P₄₈ complements with rational heads; every published family population reproduced). All pairs pass (6.3·10¹¹–4.3·10¹² per dimension; 43D in 72 min of C on 4 cores), checked exactly in a new combined class + Gram mode of our C checker; 40D, 41D and 42D also by a second (numpy) implementation, which agrees exactly, while 43D has one implementation so far; wrong-centre, wrong-parent, wrong-order and wrong-scale controls are rejected. **New:** Kravatskiy's 45D record (7,655,056) is rebuilt by our own code, with all 2,187 family weights reproduced by full shell enumeration (the author's are inherited). Its pairwise check is **partial**: 9 of 16 parts (56.3% of the pairs), no violations so far, with about 2–3 h of C remaining (7 parts of 19–23 min); parked 2026-11-25, with the resume steps in the problem file. These checks prove the bounds, not that they are current records: by a third-party copy of Cohn's table (17 Nov 2026; reported, not checked) most of the 2026 arXiv claims, including all the Qiushi and Lin values checked here, are already exceeded. Kamenetsky's 49–61 (≈5·10⁷ points) are too large for brute force; a structure-aware check is outlined |
