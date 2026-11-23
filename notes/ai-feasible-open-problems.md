# Open problems from ProofAtlas most feasible for AI

Source: ProofAtlas "Top 500 open problems", edition of 2026-11-12
(https://www.proofatlas.ai/open-problems/, data file `top500-v35.json`).
Ranks below are ProofAtlas importance ranks, not feasibility. Status notes are
quoted from ProofAtlas; they were not checked independently here.

## How these were chosen

A problem scores well when:

1. **The statement is elementary.** It needs little theory to state or attack.
2. **A solution comes with a certificate a machine can check.** Examples are
   an explicit construction, a SAT/UNSAT certificate or a Lean proof.
3. **The frontier has moved recently.** Recent small steps show the problem is
   not stuck behind a known barrier.
4. **A partial result counts.** A settled small case or a better bound is
   publishable on its own.

These criteria reward search, SAT solving and computer-assisted proof, which
is where AI has actually landed results so far (FunSearch/AlphaEvolve
constructions, SAT-solved Ramsey-type cases, RL search in group presentations,
LLM proofs of Erdős-style problems). The headline conjectures in Tier 1 are
still hard. What makes them good targets is that each has a well-defined
partial result that is within reach.

## Tier 1: best targets (finite or checkable partial results)

| Rank | Problem | Concrete AI-sized target | Why it is feasible |
| --- | --- | --- | --- |
| 477 | Lonely Runner Conjecture | Prove the next unverified number of runners | Recent computer-assisted proofs extended the verified range by reducing each case to a finite check. The next case is mostly an algorithm and compute question. |
| 256 | Erdős–Szekeres convex polygon (ES(n) = 2^(n-2)+1) | Prove ES(7) = 33 | ES(6) = 17 was settled by computer (Szekeres–Peters 2006). The empty-hexagon result (Heule–Scheucher 2024) shows SAT encodings of planar order types scale. |
| 206 | Chromatic number of the plane | Find a 6-chromatic unit-distance graph, or a 6-colouring | ProofAtlas now records 6 ≤ χ ≤ 7 (Oct 2026 partial progress). Either answer is a finite object that a SAT solver can check, and the 5-chromatic graphs were found and shrunk by computer search. |
| 455 | Existence of EFX allocations | Settle 4 agents with additive valuations, or find a counterexample | The 3-agent case is known. Counterexample search over small instances is an LP/SMT problem, and the arguments are combinatorial. |
| 284 | Hadamard matrix conjecture | Construct a Hadamard matrix of order 668 (smallest open order) | This is a single finite construction search. Settling the whole conjecture is not in reach. |
| 98 | Exact kissing numbers, n > 4 | Close a gap, e.g. dimension 5 (40 to 44) | AlphaEvolve-style search has already improved lower bounds in some dimensions. Upper bounds come from SDP, and matching the two for a single dimension would count. |
| 383 | Andrews–Curtis conjecture | Trivialise or obstruct specific potential counterexamples (Akbulut–Kirby, Miller–Schupp families) | RL and search have already settled individual candidate presentations. A full disproof would need a new invariant, which is much harder. |
| 347 | Fewest variables for undecidable H10 over Z | Lower the current record (11 unknowns over Z) | Each improvement is an explicit, checkable polynomial construction, which suits search plus careful verification. |

## Tier 2: short statements where a proof idea could plausibly come from AI

These have no finite shortcut. They need a genuine argument, but the
statements are self-contained and the methods are elementary or
probabilistic. They are the kind of problem where LLM-assisted proofs have
recently landed (Erdős-problem style).

| Rank | Problem | Note |
| --- | --- | --- |
| 363 | Frankl union-closed sets | Gilmer's entropy method moved the bound from about 0.01 to about 0.38. ProofAtlas logs a claim of 0.38289 (Oct 2026). Reaching 1/2 needs a new idea, but the setting is elementary. |
| 375 | Erdős matching conjecture | ProofAtlas logs fixed-k and k = 4 subcase claims (Oct–Nov 2026). Good for extending case by case. |
| 319 | Černý conjecture | Bound is (n-1)^2. ProofAtlas logs a cubic-coefficient improvement claim (Nov 2026). Counterexample search for small n is cheap. |
| 482 | Reed's conjecture | ProofAtlas logs partial progress for fixed forbidden cliques (Oct 2026). |
| 488 / 411 / 500 | Total colouring, list edge colouring, Berge–Fulkerson | Graph colouring conjectures with small-case verification and active partial results. |
| 471 | Coven–Meyerowitz tiling | Finite algebraic condition with known special cases. Computation can guide the proof. |
| 359 | Turán density of K_4^(3) = 5/9 | Flag-algebra SDP bounds are close to 5/9 but do not reach it. A new certificate or a better construction is the AI-shaped route. |
| 407 | Illumination conjecture | Low-dimensional cases (n = 3 in general) are the realistic target. |
| 340 | Thomson problem | Computer-assisted optimality proofs for specific N (Schwartz did N = 5). The next N is a bounded target. |
| 260 | Sample compression, O(d) | Purely combinatorial. A clever construction or argument would settle it. |

## Avoid for now

- **Deep theory-building problems.** The Millennium problems, Langlands,
  Hodge/Tate, the standard conjectures and the minimal model program need
  large new frameworks.
- **Prime-pattern conjectures.** Twin primes, Goldbach, Hardy–Littlewood and
  Landau's problems hit the parity barrier.
- **Transcendence and irrationality** (γ, ζ(5), e and π). There is no
  plausible method on the horizon.
- **Complexity separations** (P vs NP, circuit lower bounds). Known barriers
  (relativization, natural proofs, algebrization) block most approaches.
- **Exact constants of physical models** (percolation thresholds, connective
  constant, Grothendieck constant). Many have no conjectured closed form.

## Suggested first steps in this repo

1. Pick one Tier 1 target and write its exact finite subcase in
   `problems/<name>.md` using the template.
2. Reproduce the current record computationally first (e.g. re-verify ES(6) =
   17, or the latest lonely-runner case) to validate the pipeline.
3. Look for a Lean statement in DeepMind's `formal-conjectures` repository
   before formalising from scratch. Only 2 of the 500 ProofAtlas entries link
   one.
