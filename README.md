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
| [Andrews–Curtis (length-14 frontier)](problems/andrews-curtis.md) | in progress — the Theorems 1–4 certificates of Carreras (arXiv:2607.23611, unrefereed) replayed by our own checker; Theorems 3–4 re-found by our own search; the paper's Theorem 6 exhaustions (caps 25–27, up to 13.5M states) reproduced exactly; AK(3) open |
