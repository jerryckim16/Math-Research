# Existence of EFX allocations (additive goods)

**Area:** discrete fair division / combinatorics
**Status:** in progress. Literature pinned down; exact checker, adversarial
search and a Z3 CEGAR certifier built in `computations/efx/`; no
counterexample found. The first case with no located proof claim is
**4 additive agents, 10 goods**.
**Started:** 2026-11-24
**ProofAtlas:** rank 455 ("Settle 4 agents with additive valuations, or find a counterexample")

## Statement

Agents i = 1..n have additive valuations v_i over a set M of m indivisible
goods, v_i(S) = Σ_{g∈S} v_i(g), with v_i(g) ∈ ℝ_{≥0}. A (complete) allocation
X = (X_1, …, X_n) is a partition of M (empty bundles allowed). X is **EFX**
if for all i ≠ j and every g ∈ X_j,

  v_i(X_i) ≥ v_i(X_j \ {g}).

**Question.** Does every instance (every n, m, and nonnegative additive v)
admit a complete EFX allocation?

Remarks on the definition.

- This is the zero-tolerant form, often written EFX₀: the condition is
  required also for goods g with v_i(g) = 0. The weaker form only quantifies
  over g with v_i(g) > 0. The two *existence* questions coincide: perturb
  v_i(g_j) by ε^j, so all bundle values become distinct, and let ε → 0. This
  argument is stated in Chaudhury–Garg–Mehlhorn and recalled in footnote 1 of
  AFM 2026 (both cited below).
- Equivalently v_i(X_i) ≥ v_i(X_j) − min_{g∈X_j} v_i(g) for every nonempty X_j.
- **Openness.** For fixed (n, m), the set of profiles v that admit an EFX
  allocation is a finite union of closed polyhedral cones (one for each
  allocation). So the set of counterexamples is open. If a counterexample
  exists, then one with positive integer values exists, and so does a whole
  open ball of them. This is why random and integer search is meaningful at
  all, and why a "boundary" score of exactly 0 is not a counterexample.
- EFX is invariant under positive rescaling of each v_i separately, and under
  relabelling goods or agents.

**Next open target (as of 2026-11-24):** n = 4 additive agents, m = 10 goods.
The cases m ≤ 9 are claimed by a computer-assisted preprint (AFM 2026, below)
that is not yet refereed. AFM say only that their method "applies unchanged
to larger m and n, at increased computational cost". Wang (arXiv:2608.30203,
abstract) states that "unrestricted four-agent, ten-good all-good EFX₀
remains unresolved". Without AFM, the first case without a proof is m = 8
(Mahara covers m ≤ n+3 = 7; this is re-certified below).

## Known results

Labels: **[read]** = primary text read (arXiv LaTeX source); **[abstract]** =
arXiv abstract (via the arXiv API) or the citing text of a [read] paper only.
Literature checked 2026-11-24 (arXiv listing of all titles containing "EFX"
up to 2611.21387; web search). epoch.ai's "Existence of EFX allocations"
open-problem page was found by search but could not be fetched (host blocked).

### Positive results (complete EFX exists)

| setting | source | label |
| --- | --- | --- |
| n = 2, any monotone valuations; any n with identical monotone valuations | Plaut–Roughgarden, SIAM J. Discrete Math. 34(2) (2020) | [abstract] (as cited in AFM) |
| n = 3 additive | Chaudhury–Garg–Mehlhorn, EC 2020 / JACM 71 (2024), arXiv:2002.05119 | [abstract] |
| n = 3: one agent MMS-feasible (includes additive, nice-cancelable), the other two arbitrary monotone | Akrami–Alon–Chaudhury–Garg–Mehlhorn–Mehta, EC 2023 / Oper. Res. (2024), arXiv:2205.07638 | [abstract] |
| n = 3 nice-cancelable; extensions of earlier additive results | Berger–Cohen–Feldman–Fiat, AAAI 2022, arXiv:2102.10654 | [abstract] |
| n = 3, any monotone valuations, m ≤ 7 (tight: m = 8 fails for submodular) | Akrami–Mackenzie–Mayorov–Mehlhorn–Srinivas–Suzuki–Weidenbach, "EFX Need Not Exist", arXiv:2604.18216v4 | [abstract] |
| any n, **m ≤ n + 3**, general monotone valuations; any n with two general valuation types | Mahara, Math. Oper. Res. 49(2) (2023), arXiv:2107.09901 | [abstract] |
| any n, two additive types | Mahara, arXiv:2008.08798 | [abstract] |
| any n, at most three distinct additive valuations | Prakash HV–Ghosal–Nimbhorkar–Varma, arXiv:2410.13580 | [abstract] |
| all but two agents identical (additive) | Ghosal et al., arXiv:2301.10632 | [abstract] |
| binary marginals (general) | Bu–Song–Yu, arXiv:2308.05503 | [abstract] |
| bi-valued additive (via max Nash welfare) | Amanatidis et al., arXiv:2001.09838 | [abstract] |
| personalised bi-valued additive | Byrka–Malinka–Ponitka, arXiv:2507.14957 | [abstract] |
| graphical (simple graph) valuations | Christodoulou–Fiat–Koutsoupias–Sgouritsa, EC 2023 (as cited in arXiv:2606.18665) | [abstract] |
| multigraph valuations, cancelable | Afshinmehr–Ashuri–Mahmoudkhan–Mehlhorn–Shahrezaei, arXiv:2606.18665 | [abstract] |
| **n = 4 additive, m ≤ 9** (computer-assisted, QF_LRA certificates; m = 8 also by an earlier run) | Alkassar–Fouz–Mehlhorn, "Complete EFX Allocations Exist for Four Additive Agents and Up to Nine Goods", arXiv:2608.08590v1 (Aug 2026), "AFM 2026" below | **[read]** |

### Relaxations proved for n = 4 additive

- EFX with at most one unallocated good (n = 4); at most n − 2 unallocated
  for general n. Both hold for nice-cancelable valuations (Berger et al., above) [abstract].
- EFX with charity: at most n − 1 goods unallocated and nobody envies the
  pool (Chaudhury–Kavitha–Mehlhorn–Sgouritsa, SIAM J. Comput. 50(4) (2021),
  arXiv:1907.04596) [abstract].
- EF2X exists for 4 agents, even for cancelable valuations (Ashuri–Gkatzelis–Sgouritsa,
  arXiv:2412.00254) [abstract]. Its abstract says EFX for four additive agents "remains open".

### Negative results (nearby classes)

- **Submodular / subadditive goods:** there is no EFX allocation for 3 agents
  and 8 goods with weighted-coverage (hence submodular) valuations. It extends
  to all n ≥ 3, m ≥ n + 5. For subadditive valuations, α-EFX fails for
  α > 2^{-1/6} (Akrami et al. arXiv:2604.18216 "EFX Need Not Exist";
  Mackenzie–Suzuki arXiv:2605.06451) [abstract]. A first version was found
  by SAT/SMT, the first use of SAT for EFX according to the abstract.
- **Chores:** superadditive costs, 3 agents and 6 chores, no EFX
  (Christoforidis–Santorinaios arXiv:2406.10752). **Additive** (tri-valued)
  chores, every n ≥ 4, no EFX (He–Tao arXiv:2606.08872). Both [abstract].
  Additive chores with 3 agents and m ≤ 8 always have EFX (Zhang
  arXiv:2609.10585, Z3 + cvc5 QF_LRA, the same method as AFM) [abstract].
- **EFX + Pareto optimality:** incompatible with zero values
  (Plaut–Roughgarden), and with strictly positive additive values
  (Mahabadi–Ramakrishnan–Tarnawski arXiv:2610.29201) [abstract].
- Graph orientations: EFX *orientations* need not exist (Christodoulou et al.;
  see arXiv:2409.03594, 2410.17002) [abstract].

### The AFM 2026 m ≤ 9 proof (read in full, 2026-11-24)

- **Theorem.** 4 additive agents, m ≤ 9, real nonnegative values: a complete
  EFX₀ allocation exists. The case m = 8 follows by padding (a zero good)
  and was also done by an earlier independent run.
- **Method.**
  - Normalise rows to sum 1 and sort agent 0's values.
  - Branch on the argmax goods (b₁ ≤ b₂ ≤ b₃) of agents 1–3: 165 branches for m = 9.
  - Hand Lemma L1 settles the 56 branches with distinct nonzero b_i: three
    agents each take their top good plus a favourite remaining good, and one
    agent takes its top good plus the last two goods. We checked this proof;
    it is correct for m = 9, and it does **not** extend verbatim to m = 10
    (the leftover bundle then has 4 goods).
  - The other 109 branches are split into cubes by second favourites
    (36,152 canonical cubes), then into deeper rank layers.
  - Each leaf region R carries a finite allocation list S(R), with a Z3 QF_LRA
    certificate that R ∧ ⋀_{A∈S(R)} "A is not EFX" is unsat.
  - Further ingredients: Lemma C0 (canonical choice of the sorted agent on the
    common-top branch) and Lemma M (clause reduction, re-proved per clause).
- **Scale.** 122,553 certificates, 141,878,161 per-clause checks, about one
  week on five 48-vCPU machines (≈ 4·10⁴ vCPU-hours). Single solver (Z3
  4.16.0); no proof objects; the independent verifier's solve pass is
  "packaged as resumable", not executed. Not refereed. AI-assisted (disclosed).
- **Hardness anatomy.** All difficulty sits on the "diagonal": a common top
  good and near-identical valuations. Two exhibits vA, vB (identical rows)
  have 1,680 and 5,544 EFX allocations out of 4⁹. In every EFX allocation of
  vA the top good is alone; in every one of vB it is paired.
  **Re-checked here exactly** (`computations/efx/afm_diagonal_check.py`, pure-Python 4⁹
  enumeration): counts 1680 and 5544, bundle sizes {1: 1680} and {2: 5544}. ✓
- **Our assessment.** The architecture is sound in principle; it is the same
  QF_LRA formulation as `computations/efx/cegar.py`. Correctness rests on the
  enumeration of regions and on Z3. We did not re-run their corpus (the
  archive is on Google Drive and was not downloaded). Label: *claimed,
  computer-assisted preprint*.

### Computational searches in the literature

- Brânzei, arXiv:2510.05429: simulated annealing over allocations. It found
  EFX in "thousands" of random instances, up to hundreds of agents and
  thousands of goods [abstract]. This is a search for allocations, not an
  adversarial search over valuations.
- Akrami et al. arXiv:2604.18216: SAT/SMT encoding over monotone valuations
  (n = 3, m ≤ 7 positive; m = 8 counterexample) [abstract].
- AFM arXiv:2608.08590: QF_LRA region certificates, n = 4, m ≤ 9. Zero
  counterexample candidates in either campaign [read].
- Neoh–Teh arXiv:2504.03951: the minimum number of EFX allocations when m
  slightly exceeds n [abstract].
- Wang arXiv:2608.30203: "maximum-anchor" EFX₀ certificates, including a
  22-dimensional open cone on a fixed 4×10 support face. It explicitly says
  "unrestricted four-agent, ten-good all-good EFX₀ remains unresolved" [abstract].

## Approaches

### 1. Exact checker (`computations/efx/efxcore.c`, `efx.py`)

- **Idea.** An allocation is an *unordered* set partition into ≤ n blocks plus
  an assignment of blocks to agents. Enumerate the partitions (restricted
  growth strings; Σ_{k≤4} S(m,k) = 2,795 / 11,051 / 43,947 / 175,275 / 700,075
  for m = 8…12). For each partition, agent i may take block k iff
  v_i(B_k) ≥ max_{k'≠k} r_i(B_{k'}). Then test the 4! assignments. Arithmetic
  is exact int64, with r_i(S) precomputed for all 2^m subsets.
- **Speed (n = 4).** Existence with early exit takes ≈ 0.1 ms (m = 8),
  0.2 ms (m = 10) and 0.7 ms (m = 12). A full count of EFX allocations takes
  1 / 15 / 230 ms.
- **Validation (`test_efx.py`, all pass).**
  - Against the independent pure-Python n^m brute force on 400 random
    instances (n ≤ 4, m ≤ 7, zeros and ties): existence and the **exact
    number** of EFX allocations both agree.
  - Every returned witness is re-checked by `verify`, written straight from
    the definition.
  - Known theorems on random instances: n = 2, n = 3, identical rows, and
    n = 4 with m ≤ 7.
  - AFM's exhibits vA, vB reproduce 1680 / 5544.
- **Outcome:** works.

### 2. Random search over valuations (`search.py random`)

- **Idea.** Draw instances from ten families and decide each one exactly:
  uniform; sparse (half zeros); heavy-tailed; near-identical; common top good;
  bi-valued; lexicographic (powers of 2); graphical (each good valued by ≤ 2
  agents); two near-types; and AFM's "diagonal" (shared top good, the rest
  nearly equal, noise ±1…±20).
- **Outcome.** No instance without an EFX allocation; coverage table below.
  This is evidence only. Random points rarely hit small regions, although the
  set of counterexamples, if non-empty, is open (see Statement).

### 3. Annealing on valuations (`search.py climb`)

- **Objectives.**
  - "score": maximise, over allocations X, min_i (v_i(X_i) − max_{j≠i} r_i(X_j)) / v_i(M).
    The instance is a counterexample iff the score is < 0, and the score is
    continuous in v.
  - "count": the number of EFX allocations.
- **Moves.** Additive, relative, reset, swap, and copy-from-another-agent.
- **Outcome.**
  - Score climbs drive the score to 0 at m = 9, where a boundary is reached
    (exactly tight instances), and to about 0.002 at m = 10. They never go
    below 0.
  - Count climbs at m = 10 found instances with only 220 EFX allocations out
    of 4¹⁰ = 1,048,576 (0.021 %; AFM report ≈ 0.14 % at a typical diagonal
    point for m = 9). Those instances still had large slack (0.147), so few
    EFX allocations does not mean nearly infeasible.
- **Why it is weak.** Annealing in a 40-dimensional space with a max–min
  objective stalls on plateaus. The CEGAR boxes of Approach 5 are the
  stronger local test.

### 4. CEGAR certifier over valuation regions (`cegar.py`, `cegar_branches.py`, `recheck_cvc5.py`)

- **Formulation.** The formula is R(v) ∧ ⋀_A Φ_A(v), with Φ_A = ⋁_{i≠j, g∈A_j}
  v_i(A_i) < v_i(A_j) − v_i(g), solved in QF_LRA (exact rationals). The loop:
  1. Z3 proposes v.
  2. The exact checker finds an EFX allocation A at v, or reports a
     counterexample.
  3. Add Φ_A and repeat.
- **Region.** R is: rows normalised to sum 1, agent 0 sorted, and argmax
  branches b₁ ≤ b₂ ≤ b₃ for agents 1–3. Optional deeper value chains give
  AFM-style cubes and tri-subs. These cover the space up to symmetry, by the
  same lemmas as AFM's Normalization, Sorted agent 0 and Argmax branching;
  the proofs are immediate.
- **Clause reduction.** Drop the remove-g disjunct when the region implies
  v_i(g) ≥ v_i(h) for some h in the same target. This is a subset of AFM
  Lemma M.
- **Checks on every unsat answer.**
  1. `recheck` re-solves from scratch in Z3 with the *full, unreduced*
     clauses.
  2. `recheck_cvc5.py` is an independent encoding, sharing no code with
     `cegar.py`, solved by cvc5. It also checks that the regions cover all
     branches.
  3. Negative control: dropping the last stored allocation makes the
     formula sat.
- **Outcome.**
  - Reproduces the known small cases **including n = 4, m = 7** (Mahara's
    m ≤ n+3 at n = 4).
  - The whole space at once fails (n = 4, m = 7: 1,863 iterations, timeout at
    1,400 s). Branching is essential.
  - At m = 8 the diagonal needs at least the cube level and more; see Results.
  - At m = 10, even the "distinct favourites" branch (1,2,3) did not close in
    500 s (245 allocations).

### 5. Local exhaustive boxes around the hardest points (`box_runs.py`)

- **Idea.** Take the m = 10 profiles with the smallest score found by
  annealing (score 0.002–0.005). Run CEGAR in the ℓ∞ box of radius δ around
  the normalised profile, with no symmetry reduction.
- **Outcome.** unsat for δ = 0.005, 0.01 and 0.02 around 4 of the 6 points,
  and for δ ≤ 0.01 around a fifth. Every δ = 0.05 box timed out at 240 s,
  and one point timed out already at δ = 0.005. So none of the near-tight
  points found by search has a counterexample within ℓ∞ distance 0.02
  (normalised; Z3 single solve). Entries are ≈ 0.1 on average, so this is a
  20 % relative neighbourhood.

### 6. Failed route: extending AFM's hand Lemma L1 to m = 10

- AFM's L1 covers the case where the four agents' favourite goods are
  distinct. Three agents take their top good plus a favourite remaining good;
  the fourth takes its top good plus the leftovers.
- Re-tested here: no failure on 20,000 random m = 9 instances (we also
  checked the proof).
- At m = 10 it fails on 18.9 % of random instances with distinct strict
  favourites (5,676 / 30,000, values in 0…1000). The leftover bundle has 4
  goods, so removing one leaves 3.
- On near-identical instances (base 500–1000, noise ±30) it fails on
  **30,000 / 30,000**.
- Adding "tops, then round robin" in all 24 orders covers all 30,000 uniform
  instances. But on near-identical instances with distinct tops, both rule
  families fail together on 28,807 / 30,000 (96 %).
- **So the distinct-favourites part of m = 10 is not easy.** It needs a new
  lemma or computation. Script: `computations/efx/rules_m10.py` (about 9 min).

## Results

All runs: n = 4 additive agents unless stated otherwise. 4 cores. Some
CEGAR timings were taken with 5–6 processes on 4 cores, so they are up to
≈ 1.5× pessimistic.

| Claim | Evidence level | Where |
| --- | --- | --- |
| C checker = brute force (existence and exact counts) on 400 random tiny instances; all witnesses verify | computed (tests) | `test_efx.py` |
| AFM exhibits: vA has 1,680 EFX₀ allocations, all with good 0 alone; vB has 5,544, all with good 0 paired | computed exactly (two independent enumerators) | `afm_diagonal_check.py` |
| n = 4, **m ≤ 7**: every instance has an EFX₀ allocation (re-derives Mahara's m ≤ n+3 at n = 4) | **certificate-checked**: 84/84 branches unsat in Z3 (491 s, 7,297 allocations, max 340 per branch). Every branch re-solved unsat with full clauses in Z3 **and** with an independent encoding in cvc5; coverage of all 84 branches checked; negative control sat | `data/cegar_branches_n4_m7.jsonl`, `data/recheck_cvc5_n4_m7.txt` |
| n = 3, m ≤ 7 additive (special case of Chaudhury–Garg–Mehlhorn) | certificate-checked (Z3, full-clause recheck): 28/28 branches, 319 s | `data/cegar_branches_n3_m7.jsonl` |
| (n, m) = (2, 6), (2, 8), (3, 5), (3, 6), (4, 5), (4, 6), whole space without branching | certificate-checked (Z3, plus full-clause recheck) | `data/cegar_small_whole_space.jsonl` |
| Random search, m = 10: 11.40 M instances with B = 1000 (10 families, about 1 M each, 2.39 M diagonal), plus 10.89 M with values in {0,…,3} (many ties): all have EFX | computed (exhaustive check per instance) | `data/random_m10_*.jsonl` |
| Random search, m = 11: 1.30 M; m = 12: 0.38 M (B = 1000): all have EFX | computed | `data/random_m11_*`, `random_m12_*` |
| Random search, m = 9: 10.42 M instances (B = 1000, 10 families, about 1.04 M each incl. diagonal): all have EFX. This corroborates AFM's m = 9 claim; zero counterexample candidates | computed | `data/random_m9_s91.jsonl` |
| Annealing: 129 runs (m = 9), 49 + 138 runs (m = 10): no score < 0 | computed (heuristic search) | `data/climb_*.jsonl` |
| Adversarial CEGAR, m = 10, cube b = (0,0,0), s = (1,1,1) (AFM's hardest type): 453 Z3 models, each avoiding all previously found EFX allocations; every one had an EFX allocation (min 304 of them) | computed; region **not** closed (timeout 1,200 s) | `data/cegar_adv_m10_cube011.jsonl` |
| No counterexample within ℓ∞ distance 0.02 (normalised) of 4 of the 6 hardest m = 10 points found | Z3 unsat per box, single solve | `data/box_m10.jsonl` |
| m = 8 cost probe (see below) | measured | `data/cegar_*_n4_m8*.jsonl` |

**No counterexample candidate arose in any run** (`summarize.py` scans all
logs for the `COUNTEREXAMPLE_CANDIDATE` flag; count 0).

### m = 8 cost probe (naive pipeline, Z3 5.4.1, single thread)

- **Argmax branches.** A random sample of 12 of the 120 branches:
  - 9 unsat in 0–140 s;
  - 3 hit the 240 s timeout: (0,3,3), (0,2,2) and (6,6,6).
  - (0,0,0) and (0,0,1) also time out at 700 s.
- **Cubes of branch (0,0,0).** There are 84. The first 6 tried:
  - 3 unsat in 159–200 s;
  - 3 timeouts at 240 s, including (0,1)³.
- **Tri-subs of cube (0,1)³.** There are 56. The first 27 finished in 23 min with 2 workers:
  - 26 unsat in 42–175 s (median 66 s), all re-solved unsat with full clauses;
  - 1 timeout at 180 s, the fully symmetric tri-sub (0,1,2)³, which would
    need a 4th level.
- **Reading.** As at m = 7, the hard regions are those where agents share
  their top goods (b₁ = b₂ = b₃, or b's equal to 0). At m = 8 they need at
  least one more refinement level than at m = 7. This matches AFM's report
  that "each additional pinned rank reduced per-region cost by orders of
  magnitude".
- **Extrapolation (heuristic).**
  - At about 2–5 CPU-minutes per closed region, after refining hard regions
    to depth 3–4, a full m = 8 reproduction looks like **10³–10⁴ regions ⇒
    roughly 50–500 CPU-hours** with this naive pipeline.
  - AFM's m = 9 run, with Lemma M, C0, seeding and promotion, took about
    4·10⁴ vCPU-hours.
  - m = 10 adds a factor of ≈ 4 in allocations (4¹⁰ vs 4⁹), C(12,3) = 220 vs
    165 branches, and AFM's hand lemma no longer applies (Approach 6). A
    plausible m = 10 cost is **10⁵–10⁶ vCPU-hours**. This is an
    order-of-magnitude guess, not a measurement, and it is far outside a
    single-session budget.

## Next steps

1. **(Recommended next bounded step) Independent reproduction of n = 4,
   m = 8.** AFM's m = 8 and m = 9 are single-solver and unrefereed, so this
   has independent value. It also calibrates the m = 10 cost.
   - Run `cegar_branches.py` over all 120 branches with a 300 s budget, then
     `--cubes` on the timeouts, then `--refine` on cube timeouts. This
     escalation is not automated yet; it needs a driver of ≈ 30 lines on top
     of `cegar_branches.py`.
   - Verify with `recheck_cvc5.py`, extended to check coverage at every
     refinement level.
   - Budget: 50–500 CPU-h. Do it in chunks of ≤ 25 min, resumable (results
     are appended and finished regions are skipped).
   - Before that, port AFM's Lemma C0 (choice of the sorted agent on the
     common-top branch) and seeding. Each gives a constant factor.
2. **m = 10, distinct-favourites subclass.** These are the 84 branches with
   b₁, b₂, b₃ distinct and nonzero, plus agent 0's top good 0.
   - This is the part AFM settled by hand at m = 9. It is now open, and
     Approach 6 shows that simple rules fail on near-identical instances.
   - Measure first: run 5 of these branches at m = 10 with `--cubes` and
     600 s per cube.
   - If cubes close in minutes, this subclass is 84 × 9³ ≈ 6·10⁴ cubes, about
     10³–10⁴ CPU-h. Otherwise look for a hand lemma, e.g. a generalisation of
     AFM's appendix rainbow-matching lemmas A4 to 6 leftover goods.
3. **Speed-ups to try first** (each cheap to test on the m = 7 corpus, where
   the baseline is 491 s):
   - Lemma M's dominance deletions for agents 1–3;
   - several EFX allocations added per model (top-k by slack);
   - seeding from random samples in the region;
   - solver options `smt.arith.solver=2` (used by AFM) and cvc5 as the
     primary solver;
   - an MILP with a big-M bound, since valuations are normalised to [0,1]
     (`highspy` is installed). This is incomplete only through the margin.
4. **Counterexample side.** Keep `search.py` running in the background at
   m = 10–12 with the diagonal family. Also run box-CEGAR at larger δ with
   longer budgets around the count-minimising instances.
   - A counterexample, if one exists, sits in an open region, so a box run
     that returns sat would find it exactly.
   - Any hit must go through `search.confirm` (fast, full and brute) and be
     announced loudly.
