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
| n = 2, any monotone valuations; any n with identical monotone valuations | Plaut–Roughgarden, SIAM J. Discrete Math. 34(2) (2020) | cited in [read] AFM; [abstract]-level |
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
  arXiv:1907.04596) [abstract-level, cited in AFM].
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

RESULTS_PLACEHOLDER
