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
| [Lonely Runner](problems/lonely-runner.md) | in progress — LRC(3..9) reproduced; all 71 published LRC(14) gate certificates re-checked; LRC(13) re-check under way |
| [EFX allocations](problems/efx-allocations.md) | parked — EFX existence for 4 additive agents and 8 goods reproduced, certificate-checked by two SMT solvers (Z3, cvc5); 9 goods projected at 10³–10⁴ CPU-hours |
| [Frankl union-closed sets](problems/frankl-union-closed.md) | parked — the finite computations and analytic glue behind the 0.38289 record were re-verified; the measure-theoretic layer is not |
| [Chromatic number of the plane](problems/chromatic-number-plane.md) | χ ≥ 6 Lean-verified (OpenAI's formal proof re-run here from source and kernel-replayed with `leanchecker`, including a from-scratch replay of all 787k constants); χ ≥ 5 re-proved with our own LRAT certificate; open between 6 and 7 |
| [Andrews–Curtis (length-14 frontier)](problems/andrews-curtis.md) | in progress — Theorems 1–4 of Carreras (arXiv:2607.23611, unrefereed) **Lean-verified**: our Lean 4 checker replays the author's certificates, kernel-checked by `decide +kernel` against our own definition of AC moves; Theorems 3–4 re-found by our own search; the paper's Theorem 6 exhaustions (caps 25–27) reproduced exactly; new: cap-28/29/30 exhaustions (47.5M, 88.6M, 351.4M states) with no common forward-reachable state, so directed d_GS ≥ 30 for P1, P2 vs AK(3); found that the GS graph is directed, so these (and Theorem 6) bound only directed paths — a possible gap in the paper; new: exact predecessor enumeration (checked exhaustively) and an undirected search find no undirected GS path below energy 31, so Theorem 6's bounds hold undirected too and the gap is closed; AK(3) open |
| [Kissing numbers (2026 lower bounds, dims 11, 12, 25–39, 43)](problems/kissing-numbers.md) | in progress — independent exact pairwise checks of unrefereed 2026 claims, validated first on D4, D5, E8 and Leech; **certificate-checked** (all pairs, exact), 29 configurations, no violation found: Qiushi Engine (arXiv:2609.35051) dims 25, 27, 32–39, 43 and Lin (arXiv:2611.03682) dims 32–35, 37–39, rebuilt from pinned data with our own code (ℚ(√2,√3) coordinates through an exact field checker); **new:** the 2026 claims on arXiv were surveyed: data, sizes, and what each would take to check. A. Kravatskiy's repository records in dims 25–33 (197,586 … 370,528 points, up to 6.9·10¹⁰ pairs each; 25D, 29D, 32D, 33D rebuilt from his witness/trade files, two implementations for the integer parts; 32D/33D shown to be Lin's configurations with a few thousand points exchanged) are checked, as are τ₁₁ ≥ 604 (EinsteinArena, arXiv:2606.10402, rebuilt from the paper; 19,704 contacts, matching the Station paper's count) and τ₁₂ ≥ 841 (arXiv:2606.18984, the published decimals read exactly; margin 1/4 − cos² = 6.2·10⁻⁸). These checks prove the bounds, not that they are current records: by a third-party copy of Cohn's table (17 Nov 2026; reported, not checked) most of the 2026 arXiv claims, including all the Qiushi and Lin values checked here, are already exceeded. Kamenetsky's 49–61 (≈5·10⁷ points) are too large for brute force; a structure-aware check is outlined |
