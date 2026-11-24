# Existence of EFX allocations (additive goods)

**Area:** discrete fair division / combinatorics
**Status:** in progress. Literature pinned down; exact checker, adversarial
search and a Z3 CEGAR certifier built in `computations/efx/`; no
counterexample found. n = 4, m = 8 independently reproduced **modulo Z3**
(cvc5 second check 722/979 regions so far). The first case with no located
proof claim is **4 additive agents, 10 goods**.
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
(Mahara covers m ≤ n+3 = 7; this is re-certified below). Our own m = 8 run
(Results) closes every region in Z3 with a complete coverage tree, but the
cvc5 second check is not finished, so we do not yet call m = 8 reproduced
without qualification.

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

### 4a. Speed-ups for the CEGAR certifier (second session, 2026-11-24)

Each option was added to `cegar.py` (off by default, so the old corpus is
reproducible) and measured on the **whole m = 7 corpus** (84 branches, 4
workers, 300 s timeout, Z3 5.4.1; time = CEGAR seconds summed over branches,
excluding the re-checks). Every run closed 84/84 branches, and every branch
re-solved unsat with full clauses. Raw summaries: `data/speedups_n4.jsonl`.

| configuration | CEGAR s | Z3 calls | allocations | slowest branch |
| --- | --- | --- | --- | --- |
| baseline (re-measured; 491 s in the first session, with 5–6 processes) | 347 | 7,174 | 7,090 | 45.3 s |
| + Lemma M items 2–3 (`--lemma-m`) | 247 | 6,669 | 6,585 | 32.8 s |
| + Lemma C0′ (`--c0`) | 581 | 7,333 | 7,249 | 64.4 s |
| + `smt.arith.solver=2` (`--arith 2`) | 106 | 6,573 | 6,489 | 11.4 s |
| + 8 extra points per model (`--multi 8`) | 367 | 6,208 | 6,782 | 42.1 s |
| + 300 seed points (`--seed-points 300`) | 331 | 5,860 | 6,524 | 44.8 s |
| **arith 2 + Lemma M** (used for m = 8) | **77** | 6,811 | 6,727 | 8.9 s |
| arith 2 + Lemma M + seed 300 | 89 | 5,642 | 6,306 | 10.0 s |
| arith 2 + Lemma M + C0′ | 133 | 6,647 | 6,563 | 18.9 s |
| arith 2 + Lemma M + multi 8 | 94 | 5,981 | 6,399 | 9.8 s |

The same comparison on four hard m = 8 regions (300 s each; the old naive
pipeline is from the first session's probe, 240 s timeout):

| m = 8 region | old pipeline | arith 2 + M | arith 2 + M + C0′ |
| --- | --- | --- | --- |
| branch (0,3,3) | timeout (240 s) | unsat, 168 s | unsat, 258 s |
| branch (6,6,6) | timeout (240 s) | timeout (300 s) | timeout (300 s) |
| cube (0,1),(0,1),(0,4) | unsat, 188 s | unsat, 13.7 s | unsat, 18.1 s |
| cube (0,1)³ | timeout (240 s); 1 of its tri-subs also timed out | **unsat, 220 s** | unsat, 222 s |

What helped and what did not:

- **`smt.arith.solver=2` (the solver AFM used): 3.3×.** The single largest
  gain. It is only a Z3 option; certificates are unchanged in form.
- **Lemma M items 2–3: 1.4× alone, and still 1.4× on top of arith 2**
  (106 → 77 s). The clause is shorter; the certificate (the allocation
  list) has the same meaning, and both re-checks use full clauses.
- **Seeding and extra points per model: no gain** (−15 to −20 % Z3 calls,
  but each call is slower with more clauses). The added points
  (convex combinations of the Z3 model with random region points, uniform
  and near-diagonal) were mostly already covered: the uncovered set is a
  union of thin slivers along the boundaries of the allocations' cones, and
  random points rarely hit it. Kept in the code (`--multi`, `--seed-points`),
  not used.
- **Lemma C0′ (agent sorting by top-two sum): a slow-down** (1.7× at m = 7,
  1.0–1.5× at m = 8). It adds 3(m−1) inequalities per region and did not
  reduce the number of Z3 calls, even on the diagonal branch (0,0,0)
  (358 vs 355 at m = 7). AFM say C0 "does not reduce the number of cubes";
  at our depths it does not pay. Kept (proof and test below), not used.
- **MILP / LP back-end: not tried.** With ≈ 10 literals per allocation and
  ≈ 10³ allocations the big-M relaxation is very weak, and the final unsat
  proof would still need an exact solver. The Z3 gain above made it a low
  priority.

**Lemma M items 2–3 (as implemented in `cegar.reduced_disjuncts`).** Fix an
envier i and the known order of i's goods (agent 0: the full sort; agent
i ≥ 1: its chain p₀ ≥ p₁ ≥ … ≥ p_k ≥ every other good). Write T ⪯ U if there is
an injective φ: T → U with v_i(x) ≤ v_i(φ(x)) known for all x; then
v_i(T) ≤ v_i(U) on the region, since v ≥ 0. (2) If the trimmed target T =
A_j∖g satisfies T ⪯ T′ = A_k∖h for another disjunct that is still present,
the disjunct own < v_i(T) implies own < v_i(T′) and is deleted. Deletions
are sequential, so every deleted disjunct implies one that is kept in the
end. (3) If T ⪯ A_i (the own bundle), the disjunct is false on the region and
is deleted. So on the region the reduced clause is equivalent to the full one.
This matches AFM Lemma M. Brute-force test `test_lemma_m_equivalence`:
reduced, old and full clauses have the same truth value at 600 exact points
with many ties × 15 allocations. The certificates do not depend on it: both
re-checks use full clauses.

**Lemma C0′ (global form of AFM's Lemma C0).** Let T(w) be the sum of the two
largest entries of a row w. Every instance is EFX-equivalent to one in which,
in addition to the usual normalisations (rows sum to 1, agent 0 sorted,
argmax branch b₁ ≤ b₂ ≤ b₃, deeper chains sorted among agents with equal
chains), **agent 0 has the largest normalised top-two sum**:
v₀(0) + v₀(1) ≥ v_i(x) + v_i(y) for all i ≥ 1 and all goods x ≠ y.

*Proof.*
1. Normalise each row; replace an all-zero row by any positive row. The
   zero agent has no EFX constraint, so an EFX allocation of the new
   instance is EFX for the old one.
2. Pick an agent a* maximising T and rename it agent 0. Relabel the goods
   so that its row is non-increasing. Then T(v₀) = v₀(0) + v₀(1).
3. Choose argmax goods and sort agents 1..3 (and deeper chains within
   classes of equal chains) exactly as without C0′.

None of these steps changes the multiset of values of a row, so T(v_i) is
unchanged and stays ≤ T(v₀). Renaming agents or goods and scaling rows are
EFX-preserving bijections.

The constraint is invariant under permuting agents 1..3, so the
symmetry-sorted splits ("equal chains, non-decreasing next goods") stay
sound with it. It is a single fixed set intersected with every region, so a
whole run must use it everywhere or nowhere: this is the AFM "exclusivity
hazard". `recheck_cvc5.py --tree` refuses records that disagree on the
flag.

Encoding: `cegar.py` uses the chain to shorten the constraint (pair
(p₀, p₁) if the chain has length ≥ 2, else (p₀, g) for all g). The cvc5
re-check writes all pairs x < y independently.

Brute-force test `test_c0_canonicalisation` (300 random instances with ties,
zeros and near-identical rows):
- the map of the proof lands in the C0′-constrained branch **and** cube
  region, as encoded by `cegar.region`;
- the exact number of EFX allocations is preserved;
- negative control: making a strictly non-maximal agent agent 0 violates
  the region, while the same point satisfies the region without C0′.

**Refinement driver (`run_tree.py`).** It runs all argmax branches with a
time limit. Each timeout is split with `cegar_branches.refine`: every agent's
next favourite, and among agents with identical chains the new goods are
non-decreasing. Branch → cube → tri-sub → … . Every finished region is
appended to the output file and flushed immediately; on restart, closed
regions are skipped and timed-out ones are expanded, so a restart loses only
the ≤ 4 regions in flight. `recheck_cvc5.py --tree` re-derives coverage
independently, through any number of levels: a node is covered if it has a
cvc5-verified unsat record, or if all its children are covered under either
the symmetric all-agents rule or a single-agent rule.

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
| m = 8 cost probe, naive pipeline (see below) | measured | `data/cegar_*_n4_m8*.jsonl` |
| CEGAR speed-ups on the full m = 7 corpus: Z3 `smt.arith.solver=2` + AFM Lemma M items 2–3 give 347 → 77 CPU-s (4.5×); C0′, seeding and extra points do not help (Approach 4a) | measured; every run 84/84 unsat with full-clause re-solve | `data/speedups_n4.jsonl` |
| Lemma C0′ (agent 0 has the largest top-two sum) is a sound extra normalisation | proved (Approach 4a) + brute-force test of the canonicalisation map | `test_efx.py::test_c0_canonicalisation` |
| m = 10 distinct-favourites sample (arith 2 + Lemma M, 300 s): branches (1,2,3) and (2,5,8) time out (263 / 299 Z3 calls); cube (1,0),(2,0),(3,0) times out; cube (1,4),(2,4),(3,4) unsat in 136 s, but its full-clause Z3 re-solve hit the 300 s limit (`unknown`), so it is **not** counted as closed | measured; nothing closed | `data/cegar_m10_distinct_sample.jsonl` |
| **n = 4, m = 8**: every instance has an EFX₀ allocation (independent reproduction of the m = 8 case of AFM 2026, the first case beyond Mahara's m ≤ n+3) | **certificate-checked in Z3; second-solver (cvc5) re-check partial**. Coverage 120/120 argmax branches: 111 closed at branch level, the 9 diagonal branches (0,0,0), (0,0,1), (k,k,k) for k = 1…7 closed through **all** their cubes (868 cubes, none needed a deeper layer). 979 unsat certificates, 167,112 allocations (max 1,364 per region). Each was re-solved from scratch in Z3 with full clauses: 979/979 unsat. Tree coverage re-derived by the independent code in `recheck_cvc5.py --tree`: complete. cvc5 (independent encoding, full clauses, QF_LRA logic): **722/979 records unsat, 0 not unsat, 257 pending** (all records with ≤ 222 allocations are done; the pending ones have 223–1,364). With only the cvc5-verified records the tree covers 50/120 branches. So m = 8 is **reproduced modulo Z3**; the second-solver check is incomplete | `data/m8_tree_certs.jsonl.gz`, `data/m8_cvc5_verdicts.txt`, `data/m8_run_summary.txt` |

**No counterexample candidate arose in any run** (`summarize.py` scans all
logs for the `COUNTEREXAMPLE_CANDIDATE` flag; count 0).

### m = 8 run (second session; `run_tree.py --arith 2 --lemma-m`, 4 workers, 300 s per region)

- **Coverage.** All 120 branches ran with 300 s. 111 closed (mean 24 s,
  max 229 s). The 9 that timed out are exactly the shared-top ones:
  (0,0,0), (0,0,1) and (k,k,k) for k = 1…7. All their cubes were then run:
  84 each for (0,0,0) and (k,k,k), and 196 for (0,0,1). **All 868 cubes
  closed** (median 0.9 s, mean 4.8 s, max 218 s), so no tri-sub layer was
  needed. With the old pipeline, cube (0,1)³ had needed tri-subs, and one of
  them timed out.
- **Cost (measured).**
  - CEGAR time 9,532 CPU-s (2.6 CPU-h). Of this, 2,700 s went to the 9
    branch-level timeouts, which could be skipped by sending shared-top
    branches straight to cubes.
  - Wall time 78 min on 4 workers, in four resumable chunks of ≤ 24 min.
    That is 5.2 CPU-h including the Z3 full-clause re-solves.
  - cvc5 re-check: 23 min × 4 workers verified the 722 smallest records
    (67,526 allocations). cvc5 is much slower than Z3 on large records.
    In an aborted first attempt (default logic, largest-first order),
    none of the four roots (0,0,2)–(0,0,5) (680–816 allocations) finished
    in 11 min. The QF_LRA logic is 3.1× faster (10.5 s vs 32.8 s on a
    111-allocation cube). The pending 257 records (99,586 allocations) are
    therefore **several CPU-hours at least; not measured**.
  - The first session's projection of 50–500 CPU-h for m = 8 is superseded:
    the gain came from `smt.arith.solver=2` plus Lemma M (Approach 4a).
- **Not used:** C0′, seeding, extra points. All shared-top cubes closed at
  the cube level.
- **No counterexample candidate** was flagged (0 occurrences of the flag in
  the run log). Every Z3 model had an EFX allocation, confirmed by the exact
  C checker and `efx.verify`.

### m = 8 cost probe (first session; naive pipeline, Z3 5.4.1, single thread)

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

1. **(Recommended next bounded step) Finish the second-solver check of
   m = 8.** The run itself is complete: 979 regions closed, a full-clause
   Z3 re-solve for each, and a complete coverage tree. cvc5 has verified 722
   of the 979 regions. The 257 pending records are the large ones (61
   branch-level records, 196 cubes; 223–1,364 allocations each).
   - Cheapest route: re-close the 61 pending **branch-level** regions at the
     cube level in Z3 with `run_tree.py`. Cubes take a median of 0.9 s, and
     cube certificates are small, so cvc5 is fast on them. Then run cvc5
     on all small records. `recheck_cvc5.py --tree` accepts either cover of
     a branch. The 196 large cubes (all on shared-top branches) can be
     split once more the same way if cvc5 stays slow on them.
   - Run `recheck_cvc5.py data/m8_tree_certs.jsonl.gz <new files> --tree
     --workers=4 --log=VERDICTS` in ≤ 25 min chunks. The log makes it
     resumable.
   - Only when the tree is covered by cvc5-verified records should the
     Results row say "m = 8 reproduced (two solvers)".
2. **m = 9 reproduction (AFM's main claim).** At m = 8 the whole run took
   2.6 CPU-h of CEGAR plus a Z3 re-solve (5.2 CPU-h wall-clock on 4 cores).
   From m = 7 to m = 8 the CEGAR cost grew by ≈ 90–120× (77 s → 6,800 s of
   successful regions).
   - A **heuristic** extrapolation by the same factor gives ≈ 200–300
     CPU-h for m = 9, i.e. a few days on 4 cores. It is feasible in
     chunks, but it is a multi-session job.
   - Send shared-top branches straight to cubes. At m = 8, the 9
     branch-level timeouts were 28 % of the CEGAR time.
3. **m = 10, distinct-favourites subclass** (84 branches; AFM's hand lemma
   L1 fails here, Approach 6). The sample is above: two branches and one cube
   timed out at 300 s; one cube closed in 136 s.
   - If cubes typically need 100–300 s, the 84 × 9³ = 61,236 cubes cost
     ≈ 2,000–5,000 CPU-h. That is from **one** closed sample, so it is an
     order-of-magnitude guess.
   - Measure 20 random cubes with a 1,200 s limit before committing. In
     parallel, look for a hand lemma, e.g. a generalisation of AFM's
     appendix rainbow-matching lemmas A4 to 6 leftover goods.
4. **Speed-ups still untried:**
   - per-region Z3 random seeds, or a portfolio of seeds;
   - cvc5 as the primary solver (it is slower as a checker here, so this
     is unlikely to help);
   - an MILP back-end (judged weak; see Approach 4a);
   - AFM's "promotion" (merging closed children into one certificate),
     which only compresses the corpus.
   Seeding, extra points per model and C0′ were tried and did not help.
5. **Counterexample side.** Keep `search.py` running in the background at
   m = 10–12 with the diagonal family. Also run box-CEGAR at larger δ with
   longer budgets around the count-minimising instances.
   - A counterexample, if one exists, sits in an open region, so a box run
     that returns sat would find it exactly.
   - Any hit must go through `search.confirm` (fast, full and brute) and be
     announced loudly.
