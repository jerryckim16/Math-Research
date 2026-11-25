# Existence of EFX allocations (additive goods)

**Area:** discrete fair division / combinatorics
**Status:** in progress. Literature pinned down; exact checker, adversarial
search and a Z3 CEGAR certifier built in `computations/efx/`; no
counterexample found. $n = 4$, $m = 8$ independently reproduced,
**certificate-checked by two solvers** (Z3 and cvc5, 979/979 regions each). The first case with no located
proof claim is **4 additive agents, 10 goods**.
**Started:** 2026-11-24
**ProofAtlas:** rank 455 ("Settle 4 agents with additive valuations, or find a counterexample")

## Statement

Agents $i = 1\dots n$ have additive valuations $v_{i}$ over a set $M$ of $m$ indivisible
goods, $v_{i}(S) = \sum_{g\in S} v_{i}(g)$, with $v_{i}(g) \in \mathbb{R}_{\ge 0}$. A (complete) allocation
$X = (X_{1}, \dots, X_{n})$ is a partition of $M$ (empty bundles allowed). $X$ is **EFX**
if for all $i \ne j$ and every $g \in X_{j}$,

$$v_{i}(X_{i}) \ge v_{i}(X_{j} \setminus \{g\}).$$

**Question.** Does every instance (every $n$, $m$, and nonnegative additive $v$)
admit a complete EFX allocation?

Remarks on the definition.

- This is the zero-tolerant form, often written $\mathrm{EFX}_{0}$: the condition is
  required also for goods $g$ with $v_{i}(g) = 0$. The weaker form only quantifies
  over $g$ with $v_{i}(g) > 0$. The two *existence* questions coincide: perturb
  $v_{i}(g_{j})$ by $\varepsilon^{j}$, so all bundle values become distinct, and let $\varepsilon \to 0$. This
  argument is stated in Chaudhury–Garg–Mehlhorn and recalled in footnote 1 of
  AFM 2026 (both cited below).
- Equivalently $v_{i}(X_{i}) \ge v_{i}(X_{j}) - \min_{g\in X_{j}} v_{i}(g)$ for every nonempty $X_{j}$.
- **Openness.** For fixed $(n, m)$, the set of profiles $v$ that admit an EFX
  allocation is a finite union of closed polyhedral cones (one for each
  allocation). So the set of counterexamples is open. If a counterexample
  exists, then one with positive integer values exists, and so does a whole
  open ball of them. This is why random and integer search is meaningful at
  all, and why a "boundary" score of exactly 0 is not a counterexample.
- EFX is invariant under positive rescaling of each $v_{i}$ separately, and under
  relabelling goods or agents.

**Next open target (as of 2026-11-24):** $n = 4$ additive agents, $m = 10$ goods.
The cases $m \le 9$ are claimed by a computer-assisted preprint (AFM 2026, below)
that is not yet refereed. AFM say only that their method "applies unchanged
to larger $m$ and $n$, at increased computational cost". Wang (arXiv:2608.30203,
abstract) states that "unrestricted four-agent, ten-good all-good $\mathrm{EFX}_{0}$
remains unresolved". Without AFM, the first case without a proof is $m = 8$
(Mahara covers $m \le n+3 = 7$; this is re-certified below). Our own $m = 8$ run
(Results) closes every region in Z3 with a complete coverage tree, but the
cvc5 second check is not finished, so we do not yet call $m = 8$ reproduced
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
| $n = 2$, any monotone valuations; any $n$ with identical monotone valuations | Plaut–Roughgarden, SIAM J. Discrete Math. 34(2) (2020) | [abstract] (as cited in AFM) |
| $n = 3$ additive | Chaudhury–Garg–Mehlhorn, EC 2020 / JACM 71 (2024), arXiv:2002.05119 | [abstract] |
| $n = 3$: one agent MMS-feasible (includes additive, nice-cancelable), the other two arbitrary monotone | Akrami–Alon–Chaudhury–Garg–Mehlhorn–Mehta, EC 2023 / Oper. Res. (2024), arXiv:2205.07638 | [abstract] |
| $n = 3$ nice-cancelable; extensions of earlier additive results | Berger–Cohen–Feldman–Fiat, AAAI 2022, arXiv:2102.10654 | [abstract] |
| $n = 3$, any monotone valuations, $m \le 7$ (tight: $m = 8$ fails for submodular) | Akrami–Mackenzie–Mayorov–Mehlhorn–Srinivas–Suzuki–Weidenbach, "EFX Need Not Exist", arXiv:2604.18216v4 | [abstract] |
| any $n$, **$m \le n + 3$**, general monotone valuations; any $n$ with two general valuation types | Mahara, Math. Oper. Res. 49(2) (2023), arXiv:2107.09901 | [abstract] |
| any $n$, two additive types | Mahara, arXiv:2008.08798 | [abstract] |
| any $n$, at most three distinct additive valuations | Prakash HV–Ghosal–Nimbhorkar–Varma, arXiv:2410.13580 | [abstract] |
| all but two agents identical (additive) | Ghosal et al., arXiv:2301.10632 | [abstract] |
| binary marginals (general) | Bu–Song–Yu, arXiv:2308.05503 | [abstract] |
| bi-valued additive (via max Nash welfare) | Amanatidis et al., arXiv:2001.09838 | [abstract] |
| personalised bi-valued additive | Byrka–Malinka–Ponitka, arXiv:2507.14957 | [abstract] |
| graphical (simple graph) valuations | Christodoulou–Fiat–Koutsoupias–Sgouritsa, EC 2023 (as cited in arXiv:2606.18665) | [abstract] |
| multigraph valuations, cancelable | Afshinmehr–Ashuri–Mahmoudkhan–Mehlhorn–Shahrezaei, arXiv:2606.18665 | [abstract] |
| **$n = 4$ additive, $m \le 9$** (computer-assisted, QF_LRA certificates; $m = 8$ also by an earlier run) | Alkassar–Fouz–Mehlhorn, "Complete EFX Allocations Exist for Four Additive Agents and Up to Nine Goods", arXiv:2608.08590v1 (Aug 2026), "AFM 2026" below | **[read]** |

### Relaxations proved for $n = 4$ additive

- EFX with at most one unallocated good $(n = 4)$; at most $n - 2$ unallocated
  for general $n$. Both hold for nice-cancelable valuations (Berger et al., above) [abstract].
- EFX with charity: at most $n - 1$ goods unallocated and nobody envies the
  pool (Chaudhury–Kavitha–Mehlhorn–Sgouritsa, SIAM J. Comput. 50(4) (2021),
  arXiv:1907.04596) [abstract].
- EF2X exists for 4 agents, even for cancelable valuations (Ashuri–Gkatzelis–Sgouritsa,
  arXiv:2412.00254) [abstract]. Its abstract says EFX for four additive agents "remains open".

### Negative results (nearby classes)

- **Submodular / subadditive goods:** there is no EFX allocation for 3 agents
  and 8 goods with weighted-coverage (hence submodular) valuations. It extends
  to all $n \ge 3$, $m \ge n + 5$. For subadditive valuations, $\alpha$-EFX fails for
  $\alpha > 2^{-1/6}$ (Akrami et al. arXiv:2604.18216 "EFX Need Not Exist";
  Mackenzie–Suzuki arXiv:2605.06451) [abstract]. A first version was found
  by SAT/SMT, the first use of SAT for EFX according to the abstract.
- **Chores:** superadditive costs, 3 agents and 6 chores, no EFX
  (Christoforidis–Santorinaios arXiv:2406.10752). **Additive** (tri-valued)
  chores, every $n \ge 4$, no EFX (He–Tao arXiv:2606.08872). Both [abstract].
  Additive chores with 3 agents and $m \le 8$ always have EFX (Zhang
  arXiv:2609.10585, Z3 + cvc5 QF_LRA, the same method as AFM) [abstract].
- **EFX + Pareto optimality:** incompatible with zero values
  (Plaut–Roughgarden), and with strictly positive additive values
  (Mahabadi–Ramakrishnan–Tarnawski arXiv:2610.29201) [abstract].
- Graph orientations: EFX *orientations* need not exist (Christodoulou et al.;
  see arXiv:2409.03594, 2410.17002) [abstract].

### The AFM 2026 $m \le 9$ proof (read in full, 2026-11-24)

- **Theorem.** 4 additive agents, $m \le 9$, real nonnegative values: a complete
  $\mathrm{EFX}_{0}$ allocation exists. The case $m = 8$ follows by padding (a zero good)
  and was also done by an earlier independent run.
- **Method.**
  - Normalise rows to sum 1 and sort agent 0's values.
  - Branch on the argmax goods $(b_{1} \le b_{2} \le b_{3})$ of agents 1–3: 165 branches for $m = 9$.
  - Hand Lemma L1 settles the 56 branches with distinct nonzero $b_{i}$: three
    agents each take their top good plus a favourite remaining good, and one
    agent takes its top good plus the last two goods. We checked this proof;
    it is correct for $m = 9$, and it does **not** extend verbatim to $m = 10$
    (the leftover bundle then has 4 goods).
  - The other 109 branches are split into cubes by second favourites
    (36,152 canonical cubes), then into deeper rank layers.
  - Each leaf region $R$ carries a finite allocation list $S(R)$, with a Z3 QF_LRA
    certificate that $R \wedge \bigwedge_{A\in S(R)}$ "$A$ is not EFX" is unsat.
  - Further ingredients: Lemma C0 (canonical choice of the sorted agent on the
    common-top branch) and Lemma M (clause reduction, re-proved per clause).
- **Scale.** 122,553 certificates, 141,878,161 per-clause checks, about one
  week on five 48-vCPU machines ($\approx 4\cdot 10^{4}$ vCPU-hours). Single solver (Z3
  4.16.0); no proof objects; the independent verifier's solve pass is
  "packaged as resumable", not executed. Not refereed. AI-assisted (disclosed).
- **Hardness anatomy.** All difficulty sits on the "diagonal": a common top
  good and near-identical valuations. Two exhibits vA, vB (identical rows)
  have 1,680 and 5,544 EFX allocations out of $4^{9}$. In every EFX allocation of
  vA the top good is alone; in every one of vB it is paired.
  **Re-checked here exactly** (`computations/efx/afm_diagonal_check.py`, pure-Python $4^{9}$
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
  ($n = 3$, $m \le 7$ positive; $m = 8$ counterexample) [abstract].
- AFM arXiv:2608.08590: QF_LRA region certificates, $n = 4$, $m \le 9$. Zero
  counterexample candidates in either campaign [read].
- Neoh–Teh arXiv:2504.03951: the minimum number of EFX allocations when $m$
  slightly exceeds $n$ [abstract].
- Wang arXiv:2608.30203: "maximum-anchor" $\mathrm{EFX}_{0}$ certificates, including a
  22-dimensional open cone on a fixed $4\times 10$ support face. It explicitly says
  "unrestricted four-agent, ten-good all-good $\mathrm{EFX}_{0}$ remains unresolved" [abstract].

## Approaches

### 1. Exact checker (`computations/efx/efxcore.c`, `efx.py`)

- **Idea.** An allocation is an *unordered* set partition into $\le n$ blocks plus
  an assignment of blocks to agents. Enumerate the partitions (restricted
  growth strings; $\sum_{k\le 4} S(m,k) = 2{,}795 / 11{,}051 / 43{,}947 / 175{,}275 / 700{,}075$
  for $m = 8\dots 12$). For each partition, agent $i$ may take block $k$ iff
  $v_{i}(B_{k}) \ge \max_{k'\ne k} r_{i}(B_{k'})$. Then test the 4! assignments. Arithmetic
  is exact int64, with $r_{i}(S)$ precomputed for all $2^{m}$ subsets.
- **Speed $(n = 4)$.** Existence with early exit takes $\approx 0.1$ ms $(m = 8)$,
  0.2 ms $(m = 10)$ and 0.7 ms $(m = 12)$. A full count of EFX allocations takes
  1 / 15 / 230 ms.
- **Validation (`test_efx.py`, all pass).**
  - Against the independent pure-Python $n^{m}$ brute force on 400 random
    instances ($n \le 4$, $m \le 7$, zeros and ties): existence and the **exact
    number** of EFX allocations both agree.
  - Every returned witness is re-checked by `verify`, written straight from
    the definition.
  - Known theorems on random instances: $n = 2$, $n = 3$, identical rows, and
    $n = 4$ with $m \le 7$.
  - AFM's exhibits vA, vB reproduce 1680 / 5544.
- **Outcome:** works.

### 2. Random search over valuations (`search.py random`)

- **Idea.** Draw instances from ten families and decide each one exactly:
  uniform; sparse (half zeros); heavy-tailed; near-identical; common top good;
  bi-valued; lexicographic (powers of 2); graphical (each good valued by $\le 2$
  agents); two near-types; and AFM's "diagonal" (shared top good, the rest
  nearly equal, noise $\pm 1\dots\pm 20$).
- **Outcome.** No instance without an EFX allocation; coverage table below.
  This is evidence only. Random points rarely hit small regions, although the
  set of counterexamples, if non-empty, is open (see Statement).

### 3. Annealing on valuations (`search.py climb`)

- **Objectives.**
  - "score": maximise, over allocations $X$, $\min_{i} (v_{i}(X_{i}) - \max_{j\ne i} r_{i}(X_{j})) / v_{i}(M)$.
    The instance is a counterexample iff the score is $< 0$, and the score is
    continuous in $v$.
  - "count": the number of EFX allocations.
- **Moves.** Additive, relative, reset, swap, and copy-from-another-agent.
- **Outcome.**
  - Score climbs drive the score to 0 at $m = 9$, where a boundary is reached
    (exactly tight instances), and to about 0.002 at $m = 10$. They never go
    below 0.
  - Count climbs at $m = 10$ found instances with only 220 EFX allocations out
    of $4^{10} = 1{,}048{,}576$ (0.021 %; AFM report $\approx 0.14 \%$ at a typical diagonal
    point for $m = 9$). Those instances still had large slack (0.147), so few
    EFX allocations does not mean nearly infeasible.
- **Why it is weak.** Annealing in a 40-dimensional space with a max–min
  objective stalls on plateaus. The CEGAR boxes of Approach 5 are the
  stronger local test.

### 4. CEGAR certifier over valuation regions (`cegar.py`, `cegar_branches.py`, `recheck_cvc5.py`)

- **Formulation.** The formula is $R(v) \wedge \bigwedge_{A} \Phi_{A}(v)$, with $\Phi_{A} = \bigvee_{i\ne j, g\in A_{j}} v_{i}(A_{i}) < v_{i}(A_{j}) - v_{i}(g)$,
  solved in QF_LRA (exact rationals). The loop:
  1. Z3 proposes $v$.
  2. The exact checker finds an EFX allocation $A$ at $v$, or reports a
     counterexample.
  3. Add $\Phi_{A}$ and repeat.
- **Region.** $R$ is: rows normalised to sum 1, agent 0 sorted, and argmax
  branches $b_{1} \le b_{2} \le b_{3}$ for agents 1–3. Optional deeper value chains give
  AFM-style cubes and tri-subs. These cover the space up to symmetry, by the
  same lemmas as AFM's Normalization, Sorted agent 0 and Argmax branching;
  the proofs are immediate.
- **Clause reduction.** Drop the remove-$g$ disjunct when the region implies
  $v_{i}(g) \ge v_{i}(h)$ for some $h$ in the same target. This is a subset of AFM
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
  - Reproduces the known small cases **including $n = 4$, $m = 7$** (Mahara's
    $m \le n+3$ at $n = 4$).
  - The whole space at once fails ($n = 4$, $m = 7$: 1,863 iterations, timeout at
    1,400 s). Branching is essential.
  - At $m = 8$ the diagonal needs at least the cube level and more; see Results.
  - At $m = 10$, even the "distinct favourites" branch (1,2,3) did not close in
    500 s (245 allocations).

### 4a. Speed-ups for the CEGAR certifier (second session, 2026-11-24)

Each option was added to `cegar.py` (off by default, so the old corpus is
reproducible) and measured on the **whole $m = 7$ corpus** (84 branches, 4
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
| **arith 2 + Lemma M** (used for $m = 8$) | **77** | 6,811 | 6,727 | 8.9 s |
| arith 2 + Lemma M + seed 300 | 89 | 5,642 | 6,306 | 10.0 s |
| arith 2 + Lemma M + C0′ | 133 | 6,647 | 6,563 | 18.9 s |
| arith 2 + Lemma M + multi 8 | 94 | 5,981 | 6,399 | 9.8 s |

The same comparison on four hard $m = 8$ regions (300 s each; the old naive
pipeline is from the first session's probe, 240 s timeout):

| $m = 8$ region | old pipeline | arith 2 + M | arith 2 + M + C0′ |
| --- | --- | --- | --- |
| branch (0,3,3) | timeout (240 s) | unsat, 168 s | unsat, 258 s |
| branch (6,6,6) | timeout (240 s) | timeout (300 s) | timeout (300 s) |
| cube (0,1),(0,1),(0,4) | unsat, 188 s | unsat, 13.7 s | unsat, 18.1 s |
| cube $(0,1)^{3}$ | timeout (240 s); 1 of its tri-subs also timed out | **unsat, 220 s** | unsat, 222 s |

What helped and what did not:

- **`smt.arith.solver=2` (the solver AFM used): $3.3\times$.** The single largest
  gain. It is only a Z3 option; certificates are unchanged in form.
- **Lemma M items 2–3: $1.4\times$ alone, and still $1.4\times$ on top of arith 2**
  (106 s $\to$ 77 s). The clause is shorter; the certificate (the allocation
  list) has the same meaning, and both re-checks use full clauses.
- **Seeding and extra points per model: no gain** ($-15$ to $-20$ % Z3 calls,
  but each call is slower with more clauses). The added points
  (convex combinations of the Z3 model with random region points, uniform
  and near-diagonal) were mostly already covered: the uncovered set is a
  union of thin slivers along the boundaries of the allocations' cones, and
  random points rarely hit it. Kept in the code (`--multi`, `--seed-points`),
  not used.
- **Lemma C0′ (agent sorting by top-two sum): a slow-down** ($1.7\times$ at $m = 7$,
  1.0–$1.5\times$ at $m = 8$). It adds $3(m-1)$ inequalities per region and did not
  reduce the number of Z3 calls, even on the diagonal branch (0,0,0)
  (358 vs 355 at $m = 7$). AFM say C0 "does not reduce the number of cubes";
  at our depths it does not pay. Kept (proof and test below), not used.
- **MILP / LP back-end: not tried.** With $\approx 10$ literals per allocation and
  $\approx 10^{3}$ allocations the big-$M$ relaxation is very weak, and the final unsat
  proof would still need an exact solver. The Z3 gain above made it a low
  priority.

**Lemma M items 2–3 (as implemented in `cegar.reduced_disjuncts`).** Fix an
envier $i$ and the known order of $i$'s goods (agent 0: the full sort; agent
$i \ge 1$: its chain $p_{0} \ge p_{1} \ge \dots \ge p_{k} \ge$ every other good). Write $T \preceq U$ if there is
an injective $\varphi : T \to U$ with $v_{i}(x) \le v_{i}(\varphi(x))$ known for all $x$; then
$v_{i}(T) \le v_{i}(U)$ on the region, since $v \ge 0$. (2) If the trimmed target
$T = A_{j}\setminus g$ satisfies $T \preceq T' = A_{k}\setminus h$ for another disjunct that is still present,
the disjunct $\text{own} < v_{i}(T)$ implies $\text{own} < v_{i}(T')$ and is deleted. Deletions
are sequential, so every deleted disjunct implies one that is kept in the
end. (3) If $T \preceq A_{i}$ (the own bundle), the disjunct is false on the region and
is deleted. So on the region the reduced clause is equivalent to the full one.
This matches AFM Lemma M. Brute-force test `test_lemma_m_equivalence`:
reduced, old and full clauses have the same truth value at 600 exact points
with many ties $\times 15$ allocations. The certificates do not depend on it: both
re-checks use full clauses.

**Lemma C0′ (global form of AFM's Lemma C0).** Let $T(w)$ be the sum of the two
largest entries of a row $w$. Every instance is EFX-equivalent to one in which,
in addition to the usual normalisations (rows sum to 1, agent 0 sorted,
argmax branch $b_{1} \le b_{2} \le b_{3}$, deeper chains sorted among agents with equal
chains), **agent 0 has the largest normalised top-two sum**:
$v_{0}(0) + v_{0}(1) \ge v_{i}(x) + v_{i}(y)$ for all $i \ge 1$ and all goods $x \ne y$.

*Proof.*
1. Normalise each row; replace an all-zero row by any positive row. The
   zero agent has no EFX constraint, so an EFX allocation of the new
   instance is EFX for the old one.
2. Pick an agent $a^{*}$ maximising $T$ and rename it agent 0. Relabel the goods
   so that its row is non-increasing. Then $T(v_{0}) = v_{0}(0) + v_{0}(1)$.
3. Choose argmax goods and sort agents 1..3 (and deeper chains within
   classes of equal chains) exactly as without C0′.

None of these steps changes the multiset of values of a row, so $T(v_{i})$ is
unchanged and stays $\le T(v_{0})$. Renaming agents or goods and scaling rows are
EFX-preserving bijections.

The constraint is invariant under permuting agents 1..3, so the
symmetry-sorted splits ("equal chains, non-decreasing next goods") stay
sound with it. It is a single fixed set intersected with every region, so a
whole run must use it everywhere or nowhere: this is the AFM "exclusivity
hazard". `recheck_cvc5.py --tree` refuses records that disagree on the
flag.

Encoding: `cegar.py` uses the chain to shorten the constraint (pair
$(p_{0}, p_{1})$ if the chain has length $\ge 2$, else $(p_{0}, g)$ for all $g$). The cvc5
re-check writes all pairs $x < y$ independently.

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
non-decreasing. Branch $\to$ cube $\to$ tri-sub $\to$ … . Every finished region is
appended to the output file and flushed immediately; on restart, closed
regions are skipped and timed-out ones are expanded, so a restart loses only
the $\le 4$ regions in flight. `recheck_cvc5.py --tree` re-derives coverage
independently, through any number of levels: a node is covered if it has a
cvc5-verified unsat record, or if all its children are covered under either
the symmetric all-agents rule or a single-agent rule.

### 5. Local exhaustive boxes around the hardest points (`box_runs.py`)

- **Idea.** Take the $m = 10$ profiles with the smallest score found by
  annealing (score 0.002–0.005). Run CEGAR in the $\ell_{\infty}$ box of radius $\delta$ around
  the normalised profile, with no symmetry reduction.
- **Outcome.** unsat for $\delta = 0.005$, 0.01 and 0.02 around 4 of the 6 points,
  and for $\delta \le 0.01$ around a fifth. Every $\delta = 0.05$ box timed out at 240 s,
  and one point timed out already at $\delta = 0.005$. So none of the near-tight
  points found by search has a counterexample within $\ell_{\infty}$ distance 0.02
  (normalised; Z3 single solve). Entries are $\approx 0.1$ on average, so this is a
  20 % relative neighbourhood.

### 6. Failed route: extending AFM's hand Lemma L1 to $m = 10$

- AFM's L1 covers the case where the four agents' favourite goods are
  distinct. Three agents take their top good plus a favourite remaining good;
  the fourth takes its top good plus the leftovers.
- Re-tested here: no failure on 20,000 random $m = 9$ instances (we also
  checked the proof).
- At $m = 10$ it fails on 18.9 % of random instances with distinct strict
  favourites (5,676 / 30,000, values in 0…1000). The leftover bundle has 4
  goods, so removing one leaves 3.
- On near-identical instances (base 500–1000, noise $\pm 30$) it fails on
  **30,000 / 30,000**.
- Adding "tops, then round robin" in all 24 orders covers all 30,000 uniform
  instances. But on near-identical instances with distinct tops, both rule
  families fail together on 28,807 / 30,000 (96 %).
- **So the distinct-favourites part of $m = 10$ is not easy.** It needs a new
  lemma or computation. Script: `computations/efx/rules_m10.py` (about 9 min).

## Results

All runs: $n = 4$ additive agents unless stated otherwise. 4 cores. Some
CEGAR timings were taken with 5–6 processes on 4 cores, so they are up to
$\approx 1.5\times$ pessimistic.

| Claim | Evidence level | Where |
| --- | --- | --- |
| C checker = brute force (existence and exact counts) on 400 random tiny instances; all witnesses verify | computed (tests) | `test_efx.py` |
| AFM exhibits: vA has 1,680 $\mathrm{EFX}_{0}$ allocations, all with good 0 alone; vB has 5,544, all with good 0 paired | computed exactly (two independent enumerators) | `afm_diagonal_check.py` |
| $n = 4$, **$m \le 7$**: every instance has an $\mathrm{EFX}_{0}$ allocation (re-derives Mahara's $m \le n+3$ at $n = 4$) | **certificate-checked**: 84/84 branches unsat in Z3 (491 s, 7,297 allocations, max 340 per branch). Every branch re-solved unsat with full clauses in Z3 **and** with an independent encoding in cvc5; coverage of all 84 branches checked; negative control sat | `data/cegar_branches_n4_m7.jsonl`, `data/recheck_cvc5_n4_m7.txt` |
| $n = 3$, $m \le 7$ additive (special case of Chaudhury–Garg–Mehlhorn) | certificate-checked (Z3, full-clause recheck): 28/28 branches, 319 s | `data/cegar_branches_n3_m7.jsonl` |
| $(n, m) = (2, 6)$, (2, 8), (3, 5), (3, 6), (4, 5), (4, 6), whole space without branching | certificate-checked (Z3, plus full-clause recheck) | `data/cegar_small_whole_space.jsonl` |
| Random search, $m = 10$: 11.40 M instances with $B = 1000$ (10 families, about 1 M each, 2.39 M diagonal), plus 10.89 M with values in $\{0,\dots,3\}$ (many ties): all have EFX | computed (exhaustive check per instance) | `data/random_m10_*.jsonl` |
| Random search, $m = 11$: 1.30 M; $m = 12$: 0.38 M ($B = 1000$): all have EFX | computed | `data/random_m11_*`, `random_m12_*` |
| Random search, $m = 9$: 10.42 M instances ($B = 1000$, 10 families, about 1.04 M each incl. diagonal): all have EFX. This corroborates AFM's $m = 9$ claim; zero counterexample candidates | computed | `data/random_m9_s91.jsonl` |
| Annealing: 129 runs $(m = 9)$, 49 + 138 runs $(m = 10)$: no score $< 0$ | computed (heuristic search) | `data/climb_*.jsonl` |
| Adversarial CEGAR, $m = 10$, cube $b = (0,0,0)$, $s = (1,1,1)$ (AFM's hardest type): 453 Z3 models, each avoiding all previously found EFX allocations; every one had an EFX allocation (min 304 of them) | computed; region **not** closed (timeout 1,200 s) | `data/cegar_adv_m10_cube011.jsonl` |
| No counterexample within $\ell_{\infty}$ distance 0.02 (normalised) of 4 of the 6 hardest $m = 10$ points found | Z3 unsat per box, single solve | `data/box_m10.jsonl` |
| $m = 8$ cost probe, naive pipeline (see below) | measured | `data/cegar_*_n4_m8*.jsonl` |
| CEGAR speed-ups on the full $m = 7$ corpus: Z3 `smt.arith.solver=2` + AFM Lemma M items 2–3 give 347 $\to$ 77 CPU-s ($4.5\times$); C0′, seeding and extra points do not help (Approach 4a) | measured; every run 84/84 unsat with full-clause re-solve | `data/speedups_n4.jsonl` |
| Lemma C0′ (agent 0 has the largest top-two sum) is a sound extra normalisation | proved (Approach 4a) + brute-force test of the canonicalisation map | `test_efx.py::test_c0_canonicalisation` |
| $m = 10$ distinct-favourites sample (arith 2 + Lemma M, 300 s): branches (1,2,3) and (2,5,8) time out (263 / 299 Z3 calls); cube (1,0),(2,0),(3,0) times out; cube (1,4),(2,4),(3,4) unsat in 136 s, but its full-clause Z3 re-solve hit the 300 s limit (`unknown`), so it is **not** counted as closed | measured; nothing closed | `data/cegar_m10_distinct_sample.jsonl` |
| $m = 9$ cost sample (arith 2 + Lemma M): 26/26 one-shared-pair cubes closed (median 11 s); 2/2 two-pair cubes closed; 8/9 three-shared-top cubes closed (26–623 s), 1 timeout at 1,200 s whose 6 sampled tri-subs (of 196) closed; cvc5 $\approx 3.8\cdot 10^{-3} a^{2}$ s. Projected two-solver cost $\approx 3\cdot 10^{3}$–$6\cdot 10^{3}$ CPU-h at the lower end (timeouts counted at their limit), $\approx 1.6$–$3.7\cdot 10^{4}$ CPU-h (Knuth): not feasible here | measured (43 regions, all closed regions unsat in Z3 full-clause re-solve; 13 cvc5 checks unsat); projection heuristic | `data/m9_probe_n4.jsonl`, `data/m9_cvc5_times.jsonl` |
| **$n = 4$, $m = 8$: EFX always exists** — every instance has an $\mathrm{EFX}_{0}$ allocation. This is an independent reproduction of AFM's $m = 8$, the first case beyond Mahara's $m \le n+3$ | **certificate-checked by two solvers (Z3, cvc5)**. Coverage: 120/120 argmax branches. 111 closed at branch level; the 9 diagonal branches (0,0,0), (0,0,1) and $(k,k,k)$ for $k = 1\dots 7$ closed through **all** their cubes (868 cubes; none needed a deeper layer). 979 unsat certificates, 167,112 allocations (max 1,364 per region). Every leaf is unsat in both solvers: (i) Z3 from-scratch re-solve with full clauses, 979/979; (ii) cvc5 with the independent encoding of `recheck_cvc5.py` (full clauses, QF_LRA logic), 979/979, 0 not unsat. Tree coverage was re-derived by `recheck_cvc5.py --tree` from the cvc5-verified leaves only: 120/120 branches, none uncovered. Modulo the soundness of the two solvers and of the symmetry reductions (Approach 4); no proof objects. SHA-256 below the table | `data/m8_tree_certs.jsonl.gz`, `data/m8_cvc5_verdicts.txt`, `data/m8_run_summary.txt` |

**No counterexample candidate arose in any run** (`summarize.py` scans all
logs for the `COUNTEREXAMPLE_CANDIDATE` flag; count 0).

**$m = 8$ certificate files (SHA-256).**
- `computations/efx/data/m8_tree_certs.jsonl.gz`
  `c528e05b19ce5a52fb65b7a26c0051775e41766469122454aabb3c6cf35762f5`.
  988 records: 979 unsat certificates and 9 branch-level timeouts.
  Written by `pack_certs.py` in the second session. It is unchanged
  here: no certificate was added or replaced.
- `computations/efx/data/m8_cvc5_verdicts.txt`
  `6f496f1f20893ef01f8b2937014db96e8bd036a86e14354bafecd65ef2242195`.
  979 lines, one cvc5 verdict per record, keyed by the SHA-256 of
  ($n$, $m$, branch, c0, allocations).
- Re-verify from scratch with `python3 recheck_cvc5.py
  data/m8_tree_certs.jsonl.gz --tree --workers=4 --log=FRESH.txt`
  ($\approx 9$–10 CPU-h). With the stored log, the same command only re-derives
  coverage.

### $m = 8$ run (second session; `run_tree.py --arith 2 --lemma-m`, 4 workers, 300 s per region)

- **Coverage.** All 120 branches ran with 300 s. 111 closed (mean 24 s,
  max 229 s). The 9 that timed out are exactly the shared-top ones:
  (0,0,0), (0,0,1) and $(k,k,k)$ for $k = 1\dots 7$. All their cubes were then run:
  84 each for (0,0,0) and $(k,k,k)$, and 196 for (0,0,1). **All 868 cubes
  closed** (median 0.9 s, mean 4.8 s, max 218 s), so no tri-sub layer was
  needed. With the old pipeline, cube $(0,1)^{3}$ had needed tri-subs, and one of
  them timed out.
- **Cost (measured).**
  - CEGAR time 9,532 CPU-s (2.6 CPU-h). Of this, 2,700 s went to the 9
    branch-level timeouts, which could be skipped by sending shared-top
    branches straight to cubes.
  - Wall time 78 min on 4 workers, in four resumable chunks of $\le 24$ min.
    That is 5.2 CPU-h including the Z3 full-clause re-solves.
  - cvc5 re-check: 23 min $\times$ 4 workers verified the 722 smallest records
    (67,526 allocations). cvc5 is much slower than Z3 on large records.
    In an aborted first attempt (default logic, largest-first order),
    none of the four roots (0,0,2)–(0,0,5) (680–816 allocations) finished
    in 11 min. The QF_LRA logic is $3.1\times$ faster (10.5 s vs 32.8 s on a
    111-allocation cube). The pending 257 records (99,586 allocations) are
    therefore **several CPU-hours at least; not measured**.
  - **Third session: cvc5 completion (done, 2026-11-24).** All 257
    pending records were run directly with `recheck_cvc5.py --log`
    (smallest first; the log is now written as each verdict arrives).
    It took six chunks of $\le 24$ min, 3–4 workers, 05:47–08:00 UTC, about
    7.8 CPU-h including work lost in flight at chunk ends. The largest
    record (cube $(0,1)^{3}$, 1,364 allocations) ran alone in one chunk in
    $< 24$ min. Result: **979/979 unsat, 0 not unsat; cvc5-only tree
    coverage 120/120.** cvc5 time per record is close to quadratic in
    the number of allocations $a$: measured 35–53 s at $a = 223$–274, 77 s
    at $a = 334$, 361 s at $a = 666$ ($\approx 7.8\cdot 10^{-4} a^{2}$ s; the fit
    overestimated the later chunks by $\approx 1.3\times$). Three cheaper routes
    were tried first and **failed**:
    1. *Re-closing a branch at cube level* (`run_tree.py --split-roots`,
       new option). Branch (2,2,6): 125 of its 196 cubes closed in Z3 in
       42 s, all full-clause unsat, but the cubes still carry 8–183
       allocations each (median 34, total 5,820). So the CEGAR allocation
       count does not fall in proportion to the region. Predicted cvc5
       time for those 125 cubes alone is 350–580 s, against 53 s measured
       for the single branch certificate (274 allocations). Splitting
       makes the cvc5 check $\approx 10\times$ *more* expensive, so it was stopped.
       (Data: `data/m8_probe_cubes_226.jsonl.gz`, not part of the cover.)
    2. *Shrinking certificates by a Z3 unsat core* (assumption literal
       per allocation, full clauses, `smt.core.minimize`). Branch (2,2,6):
       $274 \to 154$ allocations in 64 s, a fixed point in the next round.
       That saves $\approx 35$ s of cvc5 for 64 s of Z3. Branch (0,0,7)
       (666 allocations): no core within 1,200 s. Not used.
    3. *cvc5 options* on a 223-allocation cube (42.3 s baseline):
       `simplification=none` 40.9 s, `decision=internal` 41.0 s,
       `unate-lemmas=all` 42.7 s, `use-soi` 94.7 s, `arith-prop=none`
       $> 120$ s. No gain; the default QF_LRA settings are kept.
  - The first session's projection of 50–500 CPU-h for $m = 8$ is superseded:
    the gain came from `smt.arith.solver=2` plus Lemma M (Approach 4a).
- **Not used:** C0′, seeding, extra points. All shared-top cubes closed at
  the cube level.
- **No counterexample candidate** was flagged (0 occurrences of the flag in
  the run log). Every Z3 model had an EFX allocation, confirmed by the exact
  C checker and `efx.verify`.

### $m = 9$ cost sample (fourth session; arith 2 + Lemma M, Z3 5.4.1, cvc5 1.4.2)

**Question.** Is an independent two-solver (Z3 + cvc5) reproduction of AFM's
$m = 9$ feasible here ($\approx 30$ CPU-h)? **Answer: no, by two to three orders of
magnitude** (estimate below). No full run was started.

**Design.** The 165 argmax branches of $m = 9$ fall into strata by how many of
the four agents share a top good (agent 0's top is good 0):

| stratum | branches | cubes | treatment |
| --- | --- | --- | --- |
| L1: $b_{i}$ distinct, nonzero | 56 | (28,672) | AFM hand Lemma L1 (proof checked here); no computation |
| S2: exactly one shared pair | 84 | 30,464 | computed |
| S22: two shared pairs, $(0,b,b)$ | 8 | 2,304 | computed |
| S3: three share, $(0,0,b)$ or $(k,k,k)$ | 16 | 3,264 | computed |
| S4: (0,0,0) | 1 | 120 | computed |

The 109 computed branches have 36,152 canonical cubes (`cegar_branches.refine`),
exactly AFM's count. At $m = 9$ every computed branch goes straight to cubes
(the probes (2,2,6) and (0,1,6) of the third session time out at branch
level). A random sample of cubes (fixed seeds) was run with a 1,200 s limit;
for the one cube that timed out, a random sample of its tri-subs (next layer)
was run with a 600 s limit. Script `probe_regions.py`; records (with
allocations, Z3 re-solve time and wall time) in `data/m9_probe_n4.jsonl`;
cvc5 timings in `data/m9_cvc5_times.jsonl`. 1–7 processes on 4 cores
(mostly 4; up to 7 for $\approx 10$ min), so single timings can be up to $\approx 1.5\times$
pessimistic: two cubes accidentally run twice took 7.5/12.3 s and 90/118 s.

**Measurements (43 distinct regions: 37 cubes + 6 tri-subs; 42 closed).**

- **S2, 26 cubes** of branches (2,2,6), (0,1,6) (10 each), (4,4,5), (1,1,6)
  (3 each): **26/26 closed at cube level.** CEGAR 1–327 s (median 11 s,
  mean 65 s; 6 of 26 above 100 s), 53–669 allocations (median 152). Z3
  full-clause re-solve 5–373 s, in total $1.25\times$ the CEGAR time. Three of
  the (2,2,6) cubes also exist at $m = 8$, where they took 0.1 s with 17–47
  allocations: at $m = 9$ they cost $\approx 100$–$400\times$ more and need 3–$8\times$ more
  allocations.
- **S22, 2 cubes of (0,3,3):** closed in 192 s and 296 s (359, 505
  allocations).
- **S3, 9 cubes:** (0,0,7): 26 s, 65 s (209, 280 allocations); (1,1,1):
  217 s, 425 s, 623 s (416, 651, 1,032 allocations); (7,7,7): 207 s, 217 s,
  599 s (452–665 allocations) and **one timeout at 1,200 s**, cube
  (7,0),(7,5),(7,5), with 1,359 allocations found.
- **Tri-subs of that cube: 6 of its 196, all closed**, 22–464 s (mean
  211 s), 256–815 allocations (mean 488), Z3 re-solve 60–554 s.
- **cvc5 at $m = 9$ (13 records, $a = 90$–539, all unsat):** 23 s at $a = 91$,
  80–100 s at $a \approx 150$, 343 s at $a = 383$, 804 s at $a = 539$, 1,351 s at
  $a = 455$ (under the heaviest load). Least-squares $t \approx 3.8\cdot 10^{-3} a^{2}$ s,
  **$4.9\times$ the $m = 8$ rule** $7.8\cdot 10^{-4} a^{2}$ (per-record ratio 2.3–$6.8\cdot 10^{-3}$, the
  high end under load). Checks at $a = 492$, 546 and 665 were stopped without a verdict after
  869–1,240 s (lower bounds in the timing file).
- **Soundness side:** every closed region re-solved unsat in Z3 with full
  clauses; every finished cvc5 verdict unsat; no counterexample candidate,
  no solver disagreement.

**Estimate (`estimate_tree.py`; CPU-hours; one core = one Z3/cvc5 process).**
Per stratum: (number of cubes) $\times$ (mean cost of a sampled cube). S4 is
assumed to cost like S3 (no S4 sample; 120 cubes, small weight).
Reproduce: `python3 estimate_tree.py data/m9_probe_n4.jsonl
--map=S2=226,016,445,116 --map=S3=777,111,007 --map=S22=033
--map=S4=777,111,007 --cvc5-times=data/m9_cvc5_times.jsonl [--no-knuth]`.

| scenario | CEGAR | Z3 re-solve | cvc5 ($m = 8$ rule / $m = 9$ fit) | total |
| --- | --- | --- | --- | --- |
| lower end: the timed-out cube counted at 1,200 s, nothing below it | $1.1\cdot 10^{3}$ | $1.1\cdot 10^{3}$ | $0.8\cdot 10^{3} / 3.8\cdot 10^{3}$ | **$2.9\cdot 10^{3}$ – $5.9\cdot 10^{3}$** |
| Knuth: the timed-out cube = 1,200 s + 196 $\times$ (mean of its 6 sampled tri-subs) | $5.4\cdot 10^{3}$ | $5.8\cdot 10^{3}$ | $5.3\cdot 10^{3} / 2.6\cdot 10^{4}$ | **$1.6\cdot 10^{4}$ – $3.7\cdot 10^{4}$** |

- These are sample-mean projections, not bounds. The lower-end row only
  drops what is known to be missing (the subtree of the timed-out cube).
- At the lower end, S2 dominates (CEGAR 547, Z3 683, cvc5 460 CPU-h:
  $\approx$ 65 s + 81 s + 54 s per cube over 30,464 cubes). Even CEGAR alone,
  $\approx 1.1\cdot 10^{3}$ CPU-h, is $\approx 35\times$ the 30 CPU-h budget.
- In the Knuth estimate the diagonal stratum S3 dominates: one timed-out
  cube in nine, each costing $\approx 196 \times 211$ s $\approx 11$ CPU-h of CEGAR, plus as much
  again for each re-check. With 1 timeout in 9 the timeout rate is
  uncertain (binomial 95 % interval $\approx 0.3$–48 %), so the S3 term could be
  $\approx 4\times$ larger, or much smaller (down to the lower-end row). Deeper layers (timed-out
  tri-subs) would add to it; none was seen in 6.
- The Knuth figure agrees in order of magnitude with AFM's $\approx 4\cdot 10^{4}$ vCPU-h
  for their $m = 9$ corpus (122,553 certificates; their 141,878,161
  per-clause checks suggest $\approx 1{,}160$ allocations per certificate, if a
  check is one allocation of one certificate).
- **Assumptions:** the sampled branches represent their strata (4 random
  S2 branches; 3 S3 branches; one S22 branch); S22 rests on 2 cubes, S4 on
  none; Z3 re-solve time as measured; cvc5 time $c\cdot a^{2}$ (measured at
  $a \le 539$; larger certificates may be worse); timings on this machine
  with $\le 1.5\times$ load inflation; no speed-up beyond arith 2 + Lemma M.

**Speed ideas tried (cheap, failed or small).**

1. *cvc5 on Lemma-M-reduced clauses* instead of full clauses ($m = 8$
   records with known times, then one $m = 9$ record):

   | record | a | full | reduced (Lemma M) |
   | --- | --- | --- | --- |
   | $m = 8$ cube (0,1),(0,4),(1,5) | 223 | 47.7 s | 10.7 s |
   | $m = 8$ branch (2,2,6) | 274 | 63.4 s | 23.2 s |
   | $m = 8$ branch (0,0,7) | 666 | 361 s (third session) | 182 s |
   | $m = 8$ cube $(0,1)^{3}$ | 1,364 | $\approx 1{,}450$ s (rule; "$< 24$ min") | 241 s |
   | $m = 9$ cube (0,2),(1,4),(6,5) | 91 | 23–25 s | 4.3 s |

   A 2–$6\times$ gain on the cvc5 pass. But the cvc5 verdict then depends on Lemma
   M (proved, brute-force tested) and, as tried, on `cegar.reduced_disjuncts`,
   shared code. An independent re-implementation would be needed. It
   does not change the verdict: with ideas 1 and 2 together the lower
   end is still $> 1.2\cdot 10^{3}$ CPU-h (CEGAR alone is $1.1\cdot 10^{3}$).
2. *Dropping the Z3 from-scratch re-solve* (keeping CEGAR's own Z3 verdict
   plus the cvc5 full-clause check as the two solvers) saves $\approx 1/3$. This is
   a policy choice, not a speed-up, and also not enough.
3. *Single-agent split instead of cubes* for a timed-out diagonal region
   (extend only agent 3's chain: 7 children instead of 84–196; covered by
   the `"k"` rule of `recheck_cvc5.py --tree`). Tested at $m = 8$ on branches
   (6,6,6) and (3,3,3), whose 84 cubes each took 316 s and 359 s of CEGAR
   in total. Of the 7 children, 6 took 64–85 s (resp. 47–84 s), and the
   child whose new good is 0 timed out at 300 s in both. So $\ge 760$ s and
   $\ge 690$ s: **$\ge 1.9$–$2.4\times$ worse**, with fewer but bigger certificates
   (455–627 allocations each). Not pursued.
   Data: `data/m8_single_agent_split.jsonl`.
4. Not tried: Yices as the second solver. Installing it was not permitted
   in this session.

### $m = 8$ cost probe (first session; naive pipeline, Z3 5.4.1, single thread)

- **Argmax branches.** A random sample of 12 of the 120 branches:
  - 9 unsat in 0–140 s;
  - 3 hit the 240 s timeout: (0,3,3), (0,2,2) and (6,6,6).
  - (0,0,0) and (0,0,1) also time out at 700 s.
- **Cubes of branch (0,0,0).** There are 84. The first 6 tried:
  - 3 unsat in 159–200 s;
  - 3 timeouts at 240 s, including $(0,1)^{3}$.
- **Tri-subs of cube $(0,1)^{3}$.** There are 56. The first 27 finished in 23 min with 2 workers:
  - 26 unsat in 42–175 s (median 66 s), all re-solved unsat with full clauses;
  - 1 timeout at 180 s, the fully symmetric tri-sub $(0,1,2)^{3}$, which would
    need a 4th level.
- **Reading.** As at $m = 7$, the hard regions are those where agents share
  their top goods ($b_{1} = b_{2} = b_{3}$, or $b$'s equal to 0). At $m = 8$ they need at
  least one more refinement level than at $m = 7$. This matches AFM's report
  that "each additional pinned rank reduced per-region cost by orders of
  magnitude".
- **Extrapolation (heuristic).**
  - At about 2–5 CPU-minutes per closed region, after refining hard regions
    to depth 3–4, a full $m = 8$ reproduction looks like **$10^{3}$–$10^{4}$ regions $\Rightarrow$
    roughly 50–500 CPU-hours** with this naive pipeline.
  - AFM's $m = 9$ run, with Lemma M, C0, seeding and promotion, took about
    $4\cdot 10^{4}$ vCPU-hours.
  - $m = 10$ adds a factor of $\approx 4$ in allocations ($4^{10}$ vs $4^{9}$), $C(12,3) = 220$ vs
    165 branches, and AFM's hand lemma no longer applies (Approach 6). A
    plausible $m = 10$ cost is **$10^{5}$–$10^{6}$ vCPU-hours**. This is an
    order-of-magnitude guess, not a measurement, and it is far outside a
    single-session budget.

## Next steps

1. **Done (third session): second-solver check of $m = 8$.** All 979
   certificates are unsat in cvc5, and coverage is complete from
   cvc5-verified leaves alone (Results). The planned route of re-closing
   large regions at cube level was measured and abandoned: cubes keep
   most of the allocations, and cvc5 cost is quadratic in them ($m = 8$ run
   subsection). Possible extras, not needed for the label: a third
   solver, or proof objects (e.g. cvc5 proofs checked by an external
   checker).
2. **$m = 9$ two-solver reproduction (AFM's main claim): NO-GO here
   (fourth session, measured).** The cost sample (Results, "$m = 9$ cost
   sample") puts a full Z3 + cvc5 run at **$\approx 3\cdot 10^{3}$–$6\cdot 10^{3}$ CPU-h at the lower
   end (timeouts counted only at their limit) and $\approx 1.6$–$3.7\cdot 10^{4}$ CPU-h by
   Knuth extrapolation** (sample-based projections, not bounds). That is 100–$1{,}000\times$
   the $\approx 30$ CPU-h a few sessions on 4 cores can give. Even CEGAR alone
   projects to $\approx 1.1\cdot 10^{3}$ CPU-h. No full run was started. What would make it feasible:
   - **compute:** ~$10^{3}$ cores for a few hours to two days (AFM used $\approx 4\cdot 10^{4}$
     vCPU-h); the run is embarrassingly parallel per cube, and
     `run_tree.py` is resumable;
   - **a cheaper second check:** cvc5 at $m = 9$ costs $\approx 3.8\cdot 10^{-3} a^{2}$ s, and
     the diagonal certificates have 450–1,400 allocations. Checking
     Lemma-M-reduced clauses is 2–$6\times$ faster (with an independent
     re-implementation of Lemma M). A faster QF_LRA checker (e.g. Yices) or
     proof objects (Farkas certificates checked exactly) were not tried;
   - **new hand lemmas:** the one-shared-pair stratum S2 is 84 % of the
     36,152 cubes ($\approx 2\cdot 10^{3}$ CPU-h with re-checks). The diagonal S3 is the
     Knuth-dominant term, so a structural lemma for the common-top
     diagonal would pay most.
   - **A bounded step that fits:** close **one** S2 branch completely at
     $m = 9$ with both solvers, e.g. (2,2,6): 288 cubes, $\approx 10$–30 CPU-h by
     this sample. It would give ground truth for one stratum member and
     calibrate the estimate. It is not a proof of anything beyond that
     branch.

   Earlier notes (second and third sessions), kept for the record: At $m = 8$ the whole run took
   2.6 CPU-h of CEGAR plus a Z3 re-solve (5.2 CPU-h wall-clock on 4 cores).
   From $m = 7$ to $m = 8$ the CEGAR cost grew by $\approx 90$–$120\times$ (77 s $\to$ 6,800 s of
   successful regions).
   - A **heuristic** extrapolation by the same factor gives $\approx 200$–300
     CPU-h for $m = 9$, i.e. a few days on 4 cores. It is feasible in
     chunks, but it is a multi-session job.
   - Send shared-top branches straight to cubes. At $m = 8$, the 9
     branch-level timeouts were 28 % of the CEGAR time.
   - **$m = 9$ measurements (third session; arith 2 + Lemma M, 1 worker,
     `data/m9_probe_n4.jsonl`).**
     - Branch (2,2,6): **timeout at 600 s** (909 Z3 calls, 908
       allocations found). At $m = 8$ the same branch closed in 20 s with
       274 allocations.
     - Its first cube (2,0),(2,0),(6,0): **timeout at 300 s** (769
       calls). At $m = 8$: 4.6 s, 184 allocations.
     - Branch (0,1,6): **timeout at 600 s** (753 calls). At $m = 8$: 8 s,
       254 allocations.
     So per region $m = 9$ costs **at least 30–$75\times$** $m = 8$. Even the
     easy-at-$m = 8$ types (two agents share a top good; distinct tops
     including good 0) no longer close at branch or cube level within
     300–600 s. They will need a deeper
     layer, which multiplies the region count (cubes per branch $7^{3} \to 8^{3}$).
     The 200–300 CPU-h extrapolation above is therefore a **lower-end
     guess**, likely too low; AFM spent $\approx 4\cdot 10^{4}$ vCPU-h. A real projection
     needs a sample of cube and tri-sub costs at $m = 9$ with longer
     limits (e.g. 20 random cubes of (2,2,6) and (0,1,6), 1,200 s each;
     about 2 h on 4 cores). Do that before committing to a full run.
     *(Done in the fourth session. Most one-shared-pair cubes in fact
     close at cube level, in 1–327 s; the cube (2,0),(2,0),(6,0) above is a
     slow one.)* Also,
     cvc5 re-checking is quadratic in the allocation count, so $m = 9$
     certificates of $\gtrsim 800$ allocations would cost $\gtrsim 8$ min each in cvc5.
3. **$m = 10$, distinct-favourites subclass** (84 branches; AFM's hand lemma
   L1 fails here, Approach 6). The sample is above: two branches and one cube
   timed out at 300 s; one cube closed in 136 s.
   - If cubes typically need 100–300 s, the $84 \times 9^{3} = 61{,}236$ cubes cost
     $\approx 2{,}000$–5,000 CPU-h. That is from **one** closed sample, so it is an
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
   $m = 10$–12 with the diagonal family. Also run box-CEGAR at larger $\delta$ with
   longer budgets around the count-minimising instances.
   - A counterexample, if one exists, sits in an open region, so a box run
     that returns sat would find it exactly.
   - Any hit must go through `search.confirm` (fast, full and brute) and be
     announced loudly.
