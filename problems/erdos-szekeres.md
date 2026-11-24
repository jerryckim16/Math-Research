# Erdős–Szekeres convex polygon conjecture

**Area:** combinatorial geometry
**Status:** in progress (ES(6) = 17 reproduced and certified three times; ES(7) open, cost-probed at about 10³ CPU-years, which is out of reach here)
**Started:** 2026-11-23
**ProofAtlas:** rank 256, "open with solved subcases"

## Statement

For n ≥ 3, let ES(n) be the least N such that every set of N points in the
plane in general position (no three collinear) contains n points in convex
position.

**Conjecture (Erdős–Szekeres 1935).** ES(n) = 2^(n-2) + 1 for every n ≥ 3.

**Next open case:** ES(7) = 33. That is, every 33 points in general position
contain a convex heptagon. The matching 32-point lower bound is known and is
re-verified below.

## Known results

- ES(n) ≥ 2^(n-2) + 1 for all n. This is an explicit construction (Erdős–Szekeres 1961).
- ES(4) = 5 (Klein), ES(5) = 9 (Kalbfleisch–Kalbfleisch–Stanton 1970;
  Bonnice 1974), ES(6) = 17 (Szekeres–Peters 2006, computer-assisted, about
  1500 CPU hours by their report).
- ES(n) ≤ 2^(n + O(√(n log n))) (Suk 2017; refined by Holmsen–Mojarrad–Pach–Tardos).
- SAT approaches: Marić 2019 (formally verified ES(6) encoding) and Scheucher
  (signotope/chirotope encodings; ES(6) in about 10 CPU-min per
  arXiv:2105.08406). Heule–Scheucher 2024 proved the empty-hexagon number
  h(6) = 30 by SAT. Their base ("trusted") encoding is not formally verified;
  the optimised encoding is linked to it by checked proof steps, and the
  LRAT proofs were checked by cakeLPR (see the literature section).
- ProofAtlas note: a SoCG 2025 paper refutes an ordered-hypergraph
  generalisation, but the planar conjecture stays open.

- Closer SAT literature (Dumitru on ES(7); Heule–Scheucher; Scheucher;
  Koshelev–Koshka) is summarised in the next section. It was read from the
  arXiv sources on 2026-11-23 and replaces the earlier snippet-only notes.
  Balko–Valtr (SoCG 2017) has still not been read.

## Literature on SAT attacks (read 2026-11-23)

Sources were fetched from arxiv.org (abstract page plus the LaTeX source via
`arxiv.org/e-print/<id>`) and read in full unless marked otherwise. Numbers
below are as reported by the authors, not re-measured here.

- **B. Dumitru, "Notes on the 33-point Erdős–Szekeres problem",
  arXiv:2512.24061v1 (Dec 2025). [read]** The only paper found that attacks
  ES(7) ≤ 33 directly.
  - *Encoding.* 5,456 triple-orientation variables, but points are labelled
    by convex layers in cyclic order, not in x-order, so there are no
    signotope axioms. Instead it uses a *reduced, explicitly relaxed* subset
    of Knuth's 5-point CC axiom (9,493,440 clauses). Each 4-set gets 14
    selector variables for its "realizable" cyclic sign patterns (71 clauses
    per 4-set); each 7-set gets one 280-literal clause saying "some 4-subset
    is non-convex" (4,272,048 clauses). Total 578,336 variables and
    16,670,808 clauses, about 23× our compact formula. The 4-pattern
    classification in the paper was not checked here.
  - *Symmetry breaking / splitting.* "Convex-layer anchoring": a template
    fixes the layer sizes h = (h₀, h₁, …) and adds unit clauses for
    within-layer convexity and nesting; a manual "sub-cube" vector w fixes a
    wedge at an anchor vertex of each layer.
  - *Results.* Kissat UNSAT, single thread, for 13 selected templates/sub-cubes,
    2.5·10³ s to 2.28·10⁶ s each (up to about 26 days). Within the 5⁶ template
    the sub-cubes range over three orders of magnitude.
  - *What it does not give.* No claim that the templates cover all 33-point
    configurations, no exhaustiveness argument for the splits, no total cost
    estimate, and no proof checking is described. **ES(7) is not resolved
    there, and its data cannot be turned into a cost estimate** (the number
    of templates needed, and their mix, is unknown).
- **M. J. H. Heule and M. Scheucher, "Happy Ending: An Empty Hexagon in Every
  Set of 30 Points", arXiv:2403.00737 (TACAS 2024). [read]** h(6) = 30; also
  every 24 points contain a 6-hole or a 7-gon.
  - *Encoding.* x-sorted orientation variables; 4 signotope clauses per
    4-tuple (a subset of our 8); unit clauses o₁ₐᵦ (point 1 extremal, others
    counterclockwise around it; justified by Scheucher's Lemma 1, the same
    lemma as ours). Gon/hole detection from k−2 consecutive orientation
    literals, compressed to O(n⁴) clauses with auxiliaries u⁴, u⁵, v⁴. For
    k-gons this is "simply remove the 3-hole literals", which is essentially
    our compact cup/cap encoding.
  - *Reflection symmetry.* Lex-leader predicate (their eq. sbp) on the
    consecutive triples o_{a,a+1,a+2}, read from the middle outwards, under
    o_{a,b,c} ↦ o_{n−c+2,n−b+2,n−a+2}. On g(6) ≤ 17 it cut 623,540
    conflicts / 42.0 s to 316,785 / 17.4 s.
  - *Hull-vertex choice.* Explicitly **not** broken ("complicated … left it
    on the table"; they expect at least a factor 3).
  - *Partitioning.* Static split on the consecutive triples o_{a,a+1,a+2} in a
    centred window of length ℓ, skipping patterns that unit propagation kills
    at once (for 6-gons: three consecutive true or four consecutive false),
    plus a further split on o_{b,b+2,b+4} at every alternating +−+ pattern.
    Each assignment roughly halves cube time. On "6-hole or 7-gon at 24
    points", the total is 231–606 CPU-h for ℓ = 7…21 (optimum ℓ = 15),
    against about 1,000 CPU-h estimated monolithic. The march lookahead
    splitter (-d 13) was "very poor": at least 18 cubes over 10⁵ s and about
    10× the monolithic estimate. **This matches our Approach 4 failure.**
  - *Solver.* CaDiCaL 1.9.3 with `--sat --reducetarget=10 --forcephase
    --phase=0`. g(6) ≤ 17 with 1,108 cubes (ℓ = 12) as iCNF: 8.53 s.
  - *Scale.* h(6) ≤ 30: 312,418 cubes, about 17,300 CPU-h (≈ 2 CPU-years),
    LRAT checked concurrently by cakeLPR, 180 TB of proofs. The trusted
    encoding with off-the-shelf partitioning was first estimated at about
    1,000 CPU-years, so encoding plus partitioning gained about 500×.
  - *On 33 points.* The published text says nothing about g(7). A passage
    commented out in the arXiv source (not part of the paper) says they were
    "optimistic that we can determine … g(7) on a computing cluster with some
    further engineering", and that Balko–Valtr found 7-gon-free
    configurations on 33 elements "in a more general setting". This is
    recorded only as context. Balko–Valtr (SoCG 2017) was not read.
- **M. Scheucher, "A SAT attack on higher dimensional Erdős–Szekeres
  numbers", arXiv:2105.08406v2. [read]** Acyclic-chirotope SAT model with
  DRAT certificates. It gives g⁽³⁾(7) = 13, g⁽⁴⁾(8) ≤ 13, g⁽⁵⁾(9) ≤ 13 and
  hole bounds, with single-instance runs of 2–19 CPU-days. Planar
  g(6) ≤ 17 takes about 10 CPU-min (668 MB DRAT). Nothing on g(7).
- **V. Koshelev and A. Koshka, "Combinatorial Geometry of Erdős–Szekeres Type
  Problems: SAT/ASP Modeling and Linear Subreduction", arXiv:2604.20120
  (Apr 2026). [read, skimmed outside §§3–4 and the results tables]**
  Coloured and empty-polygon variants with signotope SAT/ASP models (same
  L_{0bc} = true normalisation), plus an SMT method for finding
  realisations. No ES(7) computation. **Not relevant to the ES(7) attack.**

Literature conclusion: no published work resolves ES(7). The closest
working method for problems of this size is Heule–Scheucher's: a compact
encoding, a reflection lex-leader, a static split on consecutive triples,
and tuned CaDiCaL. Its largest success (h(6) = 30) took about 2 CPU-years.
Dumitru's per-template times (up to 2.3·10⁶ s each, encoding 23× larger)
are consistent with ES(7) being much harder than h(6) = 30.

## Approach 1: signotope SAT encoding (reproduce ES(6) = 17)

- **Encoding** (`computations/erdos-szekeres/encode.py`): there is one
  variable per triple a<b<c of x-sorted points, recording its orientation.
  - Felsner–Weil signotope axioms: each 4-tuple's orientation sequence changes
    sign at most once.
  - Each k-subset gets one clause per split of its inner points into an upper
    cap and a lower cup.
  - Symmetry breaking: X(0,b,c) = true.
- **Soundness (point set ⇒ satisfying assignment):**
  - Any x-sorted point set in general position gives a signotope.
  - A convex k-gon, read in x-order, has an upper chain that is a cap and a
    lower chain that is a cup, which is exactly a forbidden pattern.
  - So UNSAT for N points implies ES(k) ≤ N. The converse fails, because
    signotopes need not be realisable. That only matters for SAT answers,
    which is why the lower bound uses explicit coordinates instead.
- **Symmetry-breaking lemma.** WLOG X(0,b,c) holds for all 0<b<c. Proof
  sketch:
  1. Let p₀ be a hull vertex. The other points lie in an open cone at p₀ of
     angle < π. Apply an affine map so p₀ = 0 and the others have x > 0.
  2. The projective map ψ(x,y) = (y/x, −1/x) is a projective transformation.
     Its homogeneous matrix [[0,1,0],[0,0,−1],[1,0,0]] has det −1, and every
     point has positive weight x. So ψ flips all orientations among the other
     points uniformly. Reflect in y to restore them.
  3. After that, x-order equals angular order around p₀.
  4. Put a new p₀′ at (−M, M²) with M large. Then orient(p₀′,b,c) =
     M²(x_c − x_b) + O(M) > 0 for x_b < x_c, which matches the original
     orientation of (p₀,b,c) for b before c counterclockwise.
  5. All triple orientations agree with the original set, so every subset
     keeps its convex-position status, and p₀′ is leftmost.
- **Certificate:** CaDiCaL LRAT proof, checked by our own LRAT checker
  (`lrat_check.py`). The checker was tested to reject a tampered proof.

## Approach 2: explicit lower-bound sets

`computations/erdos-szekeres/construct.py` builds the classical
Erdős–Szekeres sets with exact integer coordinates. It then checks every
n-subset exhaustively, using the fact that a set in general position is in
convex position iff all of its 4-subsets are.

## Approach 3: compact cup/cap encoding (`encode_compact.py`)

- **Encoding.** Same orientation variables (same numbering), the same
  Felsner–Weil clauses and the same symmetry breaking X(0,b,c) as
  `encode.py`. The forbidden pattern uses auxiliary variables instead of one
  clause per k-subset and split:
  - U[l](a,c,d) means "there is an l-cup with first point a and last two
    points c,d" (3 ≤ l ≤ k). C[l](a,c,d) is the same for caps.
  - EU[l](a,d) and EC[l](a,d) mean "there is an l-cup (l-cap) from a to d".
  - Clauses: X(a,c,d) → U[3](a,c,d); U[l](a,b,c) ∧ X(b,c,d) → U[l+1](a,c,d);
    U[l](a,c,d) → EU[l](a,d); the same for caps with ¬X.
  - Prohibitions: ¬U[k], ¬C[k] (no k-cup or k-cap), and
    ¬EU[l](a,d) ∨ ¬EC[k+2−l](a,d) for 3 ≤ l ≤ k−1.
  - Size is O(N⁴k). For N = 17, k = 6 it is 6,936 variables and 40,648
    clauses (old encoding: 680 variables, 217,176 clauses).
- **Soundness** (full argument in the docstring). Set every auxiliary
  variable to the truth value of its definition on a real point set. All
  implications then hold. An l-cup and an m-cap from a to d with
  l + m = k + 2 lie strictly below and above the chord ad, so they are
  disjoint. Their union is the vertex set of the convex region between a
  convex and a concave function, which is a convex k-gon. So a set with no
  convex k-gon satisfies every prohibition, and UNSAT ⇒ ES(k) ≤ N. The two
  encodings are equisatisfiable. This uses the signotope fact that all
  triples of a cup are positive, which follows from the 4-point axiom by
  induction.
- **Validation.**
  - SAT/UNSAT agrees with `encode.py` on (k,N) = (4,4) SAT, (4,5) UNSAT,
    (5,8) SAT, (5,9) UNSAT, (6,16) SAT and (6,17) UNSAT.
  - `test_encoding.py` now checks 400 random instances: 160 with a convex
    k-gon and 240 without, for k = 4…7.
    - With auxiliaries set to their definitions, every definitional clause
      holds, and the prohibitions hold iff brute force finds no k-gon.
    - With orientations fixed as assumptions, CaDiCaL finds the formula SAT
      iff there is no k-gon. So the formula forbids every k-gon.
  - The explicit ES sets for n = 5, 6, 7 (8, 16 and 32 points) satisfy the
    full compact formula.
  - **Gap found in the old test.** The original random check in
    `test_encoding.py` (300 sets) was one-sided: all 300 random sets contained
    a k-gon. The k-gon-free side was only exercised by the two ES sets. The
    new balanced generator, which adds random subsets of the ES sets,
    re-checks `encode.py` as well, and it passes.
- **N = 17, k = 6 timings.** Both runs used CaDiCaL 1.7.3 on one core, on the
  same machine and at the same time as other jobs.
  - Compact encoding: UNSAT in 161 s, or 170 s with LRAT output.
  - Old encoding: 201 s. The compact encoding is about 20% faster, a modest gain.
- **Certificate.** The LRAT proof (471 MB, 1,319,776 lemmas) was checked by
  `lrat_check.py` in 55 s. It reports VERIFIED. The CNF sha256 is
  `682629f2…a252e81e3`. This gives a second, independent certificate for
  ES(6) ≤ 17, through a different encoding.

## Approach 4: cost probe for ES(7) ≤ 33 (compact encoding, cube-and-conquer sampling)

**Goal.** Estimate the cost of a SAT proof of ES(7) ≤ 33. This is an estimate
only. Nothing here is a certificate, and ES(7) remains open.

- **Formula.** `encode_compact.py 33 7`:
  - 64,240 variables: 5,456 orientation and 58,784 auxiliary.
  - 722,800 clauses, 13.4 MB.
  - sha256 `2a98487f…6178e0e`.
  - The naive encoding would need about 1.4·10⁸ clauses.
- **Direct solve.** CaDiCaL 1.7.3 with `-t 1500` on one core got no answer
  after 1,480 s of process time (1.78·10⁶ conflicts). Summary in
  `es7_probe_data/direct_33_7_summary.txt`.
- **Cube-and-conquer probe** (`cube_sample.py`, `cube_estimate.py`).
  - **Splitting.** A march-style lookahead over the orientation variables
    uses glucose unit propagation. It scores each variable by
    (1 + new orientation literals under v)·(1 + new under ¬v), and adds
    failed literals to the cube. In practice the first decisions are the
    triples X(1,3,·), i.e. the local sequence of point 1.
  - **Probes.** Random root-to-leaf walks, using Knuth's estimator
    E[weight·time] = total conquer time.
  - **Leaves.** Each leaf cube is solved by CaDiCaL (CLI, cube as unit
    clauses) under a time cap. The measured time includes about 0.3 s of
    process start-up and parsing at N = 33.
  - **`--nested`.** Solves the prefixes of the same walk at several depths,
    giving a hardness-versus-depth profile.
- **Calibration on ES(6) (N = 17), where the truth is known.**
  - Solving all 63 leaves at depth 6 takes 170 s in total (max 38.7 s, 23% of
    the total), compared with 161 s for the monolithic solve.
  - From 24 probes, the Knuth estimates at depths 2, 4 and 6 are 2.3, 2.0 and
    1.7 min (bootstrap 5–95% ranges about 0.8–3.7 min). They are correct to
    within the range.
  - At depths 8–20 the estimates drift up, to 4 min and then 71 min. Two
    causes: per-cube overhead times many leaves, and one heavy probe carrying
    50–87% of the sum. **Fixed-depth estimates are only trustworthy near the
    cost-optimal depth.**
- **N = 33 results.** All raw records are in `es7_probe_data/`.

  | depth | probes | outcome | Knuth total (CPU-years) |
  | --- | --- | --- | --- |
  | 10 | 2 | 2 timeouts at 300 s | ≥ 0.01 (lower bound) |
  | 20 / 30 / 45 | 3 each | all timeouts at 120 s | ≥ 4 / ≥ 4·10³ / ≥ 1.3·10⁸ |
  | 44 | 4 | 4 timeouts at 400 s | ≥ 2.2·10⁸ |
  | 52 | 8 | 2 refuted by lookahead above depth 48; 4 timeouts; 2 solved (255 s, 326 s) | ≥ 3.5·10¹⁰ |
  | 60 | 11 | 3 refuted; 7 solved in 0.26–95 s; 1 timeout at 400 s | ≈ 1.9·10¹² (bootstrap 3·10¹¹–4·10¹²), a lower bound because of the timeout |

  No probe ever found a lookahead refutation above depth about 45. The cube
  tree is a full binary tree down there, so the leaf count is 2^d.
- **Hardness profile along a walk.** Let r be the factor by which cube time
  drops per extra decision. Measured on the four walks that solved at two
  depths:
  - r = 1.66 (depths 58→60), 1.18 (56→60), 1.45 (52→60), and ≥ 2.3 (52→60;
    the depth-60 time is at the overhead floor).
  - Where r < 2, adding depth costs more in total than it saves.
  - **Conclusion (empirical, this splitting rule):** fixed-depth
    cube-and-conquer with this lookahead costs at least 10⁸ CPU-years at any
    depth from 44 to 60. It is not a viable route.
- **Extrapolated cost of an optimal-depth or monolithic solve.** This is
  heuristic and low-confidence. The extrapolation is T(0) ≈ T(d)·r^d along
  each walk.
  - **Test at k = 6.** Six N = 17 walks, using r from depths 4→8, give
    6 s to 946 s against the true 161 s, with a median of 137 s. That is
    within a factor of about 30 per walk, and the median is right.
  - **At k = 7.** The four walks give about 2 weeks (r = 1.18), about 2,500
    years (r = 1.45), about 5·10⁷ years (r = 1.66), and an unbounded value
    (r ≥ 2.3), all in CPU time.
  - **Honest range.** From weeks to more than 10⁸ CPU-years, with a central
    guess of 10³–10⁶ CPU-years. The extrapolation runs over 50–60 levels from
    4 walks, so an error of ±0.2 in r moves the answer by about 10⁴. The
    near-root profile is unmeasured: every cube shallower than depth 44 timed
    out. At k = 6, r near the root was about 2, larger than deeper down. If
    the same holds at k = 7, the central guess is too high.
  - **Heavy tails.** These are visible in every table above:
    - single probes carry 50–87% of the Knuth sums;
    - cube times on one level span 0.3 s to more than 400 s;
    - which walks get refuted varies from one seed to the next.
    With 4–11 probes per depth, the bootstrap ranges understate the
    uncertainty, and they cannot see tail mass that no probe hit.
- **What failed, and why.**
  - Plain unit-propagation lookahead on orientation variables gives
    essentially no refutations before depth about 50. The cube tree is
    therefore about 2^d at every useful depth, so the fixed-depth Knuth
    totals are astronomical.
  - The compact encoding helps formula size enormously, by a factor of about
    200 versus naive at N = 33. It helps solve time only modestly, by about
    20% at N = 17.
  - Sampler bug, fixed mid-run: the first version dropped walks that ended
    in refutation. Those records (`nested33.jsonl`) show two of four walks
    missing at depths 48 and above. They are counted as zero-cost leaves in
    the table above.
  - One 30-minute batch was lost when it hit a background time limit, because
    results were only written at the end. The sampler now writes each cube
    as it finishes.

## Approach 5: stronger symmetry breaking and solver settings (`symmetry_extra.py`)

**Goal.** A large, certified speed-up on ES(6) ≤ 17 before spending anything on
ES(7). Flags `--reflect short|full` and `--ear` of `encode_compact.py` add the
clauses. Without the flags the CNF is byte-identical to before (sha256
`682629f2…a252e81e3`, re-checked).

- **(R) Reflection lex-leader.** Let σ(a,b,c) = (N−c, N−b, N−a) on triples
  with 1 ≤ a < b < c ≤ N−1. Add the lex-leader constraint
  (A(v₁),…,A(v_m)) ≤_lex (A(σv₁),…,A(σv_m)), with false < true, using the
  usual chain of "prefix equal" auxiliaries e_i (3 clauses per position).
  - `short`: V = X(a,a+1,a+2) for a = ⌊(N−3)/2⌋ down to 1. This is
    Heule–Scheucher's predicate, transcribed to our labels.
  - `full`: the short list, then every other triple with a ≥ 1 not fixed by
    σ.
- **(E) Hull-ear rule (partial break of the choice of point 0).** For a hull
  vertex v with hull neighbours v⁻, v⁺, let ear(v) be the number of points
  strictly inside the triangle v⁻vv⁺. Require ear(0) ≤ ear(1) and
  ear(0) ≤ ear(N−1). In the normalisation:
  - i is a hull vertex iff X(a,i,c) holds for all 1 ≤ a < i < c;
  - ear(0) = #{b : ¬X(1,b,N−1)};
  - ear(1) = h₂ − 2 and ear(N−1) = N − 2 − h′, where h₂ and h′ are the
    hull vertices after 1 and before N−1.
  It is encoded with hull indicators, a sequential counter, and the clauses
  H_i → ¬G_{i−1} and H_i → ¬G_{N−1−i}. All auxiliaries are forced upward
  only.

**Soundness (proved).**

- *Lemma R.* Let P be in general position, p₀ a hull vertex, and A the
  normalised assignment: labels 1…N−1 in counterclockwise order around p₀,
  A(a,b,c) = [orient(p_a,p_b,p_c) > 0]. Let P′ be the mirror image
  (x,y) ↦ (−x,y), with the same p₀. Then P′'s normalised assignment is
  A′ = σ(A).
  - *Proof.* Mirroring reverses every orientation and the angular order
    around p₀, so old label i ≥ 1 becomes N−i.
  - For new labels a < b < c the old labels are N−a > N−b > N−c. Hence
    A′(a,b,c) = [orient(p_{N−a},p_{N−b},p_{N−c}) < 0]
    = [orient(p_{N−c},p_{N−b},p_{N−a}) > 0] = A(N−c,N−b,N−a). The middle
    step swaps the first and last arguments, an odd permutation.
  - X(0,·,·) stays true because the new labels are again counterclockwise
    around p₀. ∎
- *Theorem.* If some N-point set in general position has no convex k-gon,
  then `encode_compact.py N k --reflect (short|full) [--ear]` is
  satisfiable. So UNSAT still implies ES(k) ≤ N.
  - *Proof.* Take such a P and let p₀ be a hull vertex minimising ear(·).
    Then ear(0) ≤ ear(1) and ear(0) ≤ ear(N−1) in the normalisation.
  - P′ has the same convex subsets (an affine map) and the same ear counts,
    with the roles of 1 and N−1 swapped. So (E) holds for both A and σ(A).
  - By the symmetry lemma of Approach 1 (Scheucher's Lemma 1), both A and
    σ(A) are realised by x-sorted sets with no convex k-gon. So both satisfy
    (S), (B), (R), (E), (F) and (Y), with the auxiliaries set to their
    definitions (Approach 3).
  - σ is an involution, so the lex-smaller B ∈ {A, σ(A)} on V satisfies
    B ≤_lex σ(B). Setting e_i := [B and σB agree on v₁…v_i] satisfies the
    chain clauses, and the counters and hull indicators set to their
    definitions satisfy (E). ∎
  - Without --ear, any hull vertex can serve as p₀.
- *Not used:* a lex-leader over all hull vertices. The relabelling then
  depends on the assignment, so it is not a variable permutation. This is
  the symmetry Heule–Scheucher also left unbroken.

**Tests** (`test_encoding.py`, item 4). 150 trials gave 128 point sets
with N ≥ 6: random sets and subsets of the explicit ES sets, N = 6…14,
k = 5…7, 87 of them without a convex k-gon. That is 1,302 normalisations in
all. All checks pass. Each check is run for
every hull vertex as point 0 and for both mirror images.
- The exact transform of the lemma produces the angular labelling in
  x-order.
- The mirrored set's assignment equals σ(A).
- The ear counts read off the formula's definitions equal the geometric
  counts.
- The (R)+(E) clauses with orientations fixed are SAT iff the semantic
  predicate holds (CaDiCaL via pysat).
- Every set has at least one normalisation satisfying the predicate.
- The full compact formula with `--reflect full --ear` is SAT for some
  normalisation iff brute force finds no convex k-gon.
- The test is not vacuous: the predicate excludes 776 of the 1,302
  normalisations (short list) and 867 (full list).

**N = 17, k = 6 timings.** CaDiCaL 1.7.3, single runs, one core each,
4 jobs in parallel on the 4-core machine. "HS opts" means `--sat
--reducetarget=10 --forcephase --phase=0`; "phase=1" is the same with
`--phase=1`.

| formula | solver options | process time (s) | conflicts |
| --- | --- | --- | --- |
| compact (baseline, Approach 3) | default | 162.3 | 1,173,226 |
| + ear | default | 196.3 | 1,305,545 |
| + reflect short | default | 78.2 | 610,570 |
| + reflect full | default | 72.5 (seed 2: 74.1) | 581,282 |
| + reflect short + ear / full + ear | default | 77.9 / 76.8 | 627,100 / 611,253 |
| compact | HS opts | 116.8 | 810,109 |
| + reflect short | HS opts | 43.4 | 385,442 |
| + reflect full | HS opts | 42.1 | 349,979 |
| + reflect full | phase=1 | 35.0 | 310,169 |
| **+ reflect short** | **phase=1** | **35.7** (38.1 with LRAT output) | **359,436** |
| + reflect short, 987 iCNF cubes (ℓ = 12 middle window) | HS opts | 24.4 | 220,298 |

- **Speed-up: 162 s → 36 s, a factor of 4.5** (reflection about 2.1×, solver
  options about 2.2×). Conflicts fall by 3.3×. Heule–Scheucher report a
  similar factor of 2 from reflection.
- The ear rule does not help: it is about 20% slower alone and neutral with
  reflection. It stays implemented and tested, but is not used.
- **Certificate.** `encode_compact.py 17 6 --reflect short` (6,942 variables,
  40,667 clauses, sha256 `e81aee68…5a2dba`). CaDiCaL with
  `--sat --reducetarget=10 --forcephase --phase=1 --lrat=true
  --binary=false`: UNSAT in 38.1 s. The LRAT proof (139 MB, 478,525 lemmas)
  was checked by `lrat_check.py` in 13.6 s and reports VERIFIED. This is a
  third certificate for ES(6) ≤ 17, now trusting the reflection lemma as
  well. The proof file was deleted after checking.

## Approach 6: near-root hardness with the strongest encoding (static split)

**Goal.** Measure how hard cubes are near the root, which was the dominant
uncertainty in Approach 4. Use the strongest setting from Approach 5 and
Heule–Scheucher's split instead of the lookahead. **This is an estimate,
not a certificate.**

- **Setting.**
  - Formula: `encode_compact.py 33 7 --reflect short`, with 64,254
    variables, 722,843 clauses and sha256 `6796f2ea…5251b4f3`.
  - Leaf solver: CaDiCaL 1.7.3 with `--sat --reducetarget=10 --forcephase
    --phase=1`, one core per cube and up to 4 cubes in parallel on the
    4-core machine. Times are wall-clock times of the CLI, including about
    0.3 s of parsing.
  - Split: `cube_sample.py --order static`. It branches on X(a,a+1,a+2)
    from the middle outwards (30 variables), then on X(b,b+2,b+4).
    Variables already fixed by unit propagation are skipped, and children
    refuted by unit propagation are dropped.
  - Walks are random, and the Knuth weight is the product of the number of
    children. The same seed and probe index give the same walk at every
    depth, so the depths are nested prefixes of one walk.
  - Raw records: `es7_probe_data/static33_*.jsonl`. Summary:
    `walk_profile.py es7_probe_data/static33_*.jsonl`.
- **Calibration at k = 6 (N = 17, the same setting, where the truth is
  known).**
  - Monolithic solve: 35.7 s.
  - Enumerating every leaf of the static tree gives 29.0 s at depth 2
    (4 leaves, max 19.0 s) and 29.3 s at depth 4 (16 leaves, max 10.3 s).
    So with this split the **total is roughly depth-independent near the
    root**: r ≈ the branching factor ≈ 2. This matches Heule–Scheucher.
  - Six random probes gave Knuth estimates of only 5.6–9.3 s at depths 2–8,
    an underestimate by 3–5×. They missed the one heavy leaf, which carries
    65% of the depth-2 total. **Few-probe Knuth sums here are biased low by
    heavy tails.**
  - Records: `es7_probe_data/static17_*.jsonl`.
- **N = 33 measurements.** 10 walks (seeds 11 and 12, probes 0–5), 22 cubes
  in total. The ≥ entries are timeouts at the stated cap.

  | walk | depth 16 | depth 24 | depth 32 | r(24→32) |
  | --- | --- | --- | --- | --- |
  | s11p0 | ≥ 1440 s | 516 s | 0.7 s | 2.28 |
  | s11p1 | ≥ 1440 s | 460 s | 9.2 s | 1.63 |
  | s11p2 | – | ≥ 1380 s | ≥ 1440 s | – |
  | s11p3 | – | ≥ 1380 s | 20.2 s | ≥ 1.70 |
  | s12p0 | – | ≥ 1380 s | 72.5 s | ≥ 1.45 |
  | s12p1 | – | ≥ 1380 s | 98.3 s | ≥ 1.39 |
  | s12p2 | – | 428 s | 1.6 s | 2.01 |
  | s12p3 | – | ≥ 1000 s | ≥ 500 s | – |
  | s12p4 | – | ≥ 1000 s | ≥ 500 s | – |
  | s12p5 | – | ≥ 1000 s | 2.5 s | ≥ 2.12 |

  - **Depth 8 was not run.** Both depth-16 cubes already exceeded the
    1,440 s cap, so a depth-8 run under the same cap could only return
    "≥ 1,440 s". The compute went to more depth-24 walks instead.
  - **Lost runs.** A container restart killed the first depth-16 attempt,
    one depth-24 cube and four depth-32 cubes; all of them were re-run.
    Before that, one depth-24 cube was killed by a wall-clock limit after
    about 1,040 s; it was re-run as s11p3 above. Only results written to
    disk are reported.
  - **Knuth totals** (CPU time on this machine; lower bounds wherever a cube
    timed out):

    | depth | probes | timeouts | Knuth total (CPU-years) |
    | --- | --- | --- | --- |
    | 16 | 2 | 2 | ≥ 1.5 (uninformative) |
    | 24 | 10 | 7 | ≥ 375 (bootstrap ≥ 270 to ≥ 490) |
    | 32 | 10 | 3 | ≥ 3.1·10⁴ (one probe carries 63%) |

    Leaf counts are about 2²³–2²⁴ at depth 24 and 2³⁰–2³² at depth 32;
    unit propagation prunes almost nothing this shallow.
  - **Per-decision hardness r(24→32):** measured 1.63, 2.01 and 2.28 on the
    three walks solved at both depths, and ≥ 1.39 to ≥ 2.12 on four more.
    Near the root, only r(16→24) ≥ 1.14 is known (both depth-16 cubes timed
    out).
- **Comparison with Approach 4** (lookahead split, no reflection, default
  CaDiCaL).
  - There, every cube shallower than depth 44 timed out, and fixed-depth
    totals were ≥ 10⁸ CPU-years.
  - Here, depth-32 cubes often take seconds, and the depth-24 total is
    ≥ 375 CPU-years.
  - The static split is the main gain, by a factor of 10⁵ or more in the
    fixed-depth bound. The encoding and solver changes add about 4.5×, as
    measured at N = 17.
- **Updated estimate (heuristic; all CPU time on one core of this machine).**
  1. *Cube-and-conquer at depth 24, measured:* at least 375 CPU-years.
     - Seven of ten cubes are censored at 1,000–1,440 s, so the true
       total is larger.
     - If a censored cube costs 3–10× its cap (the depth-32 times span
       three orders of magnitude), the total is about 10³–4·10³ CPU-years.
  2. *Monolithic or optimal-depth cost, extrapolated as t(24)·r²⁴ along
     the three fully measured walks:* about 1.8, 260 and 6,400 CPU-years
     (r = 1.63, 2.01 and 2.28).
     - The N = 17 calibration says the total is flat near the root
       (r ≈ 2). That picks the middle of this range and agrees with item 1.
     - The 1.8-year value needs r to stay at 1.6 all the way to the root,
       which the k = 6 data contradict. Even then it is one sequential
       solve of years.
  3. **Best estimate: 10^2.5–10^4 CPU-years, central about 10³.** This
     replaces "weeks to > 10⁸" from Approach 4. The heavy tails remain:
     30% of depth-32 cubes and 70% of depth-24 cubes hit the cap. Tail mass
     that no probe hit is not covered. Confidence is low to moderate: the
     lower bound of 375 CPU-years is solid for this split and solver; the
     upper end is not.
  4. *Reference point:* h(6) = 30 cost Heule–Scheucher about 2 CPU-years
     with the same kind of encoding, split and solver. ES(7) ≤ 33 is
     **2–4 orders of magnitude harder**, before counting proof production
     and checking. For h(6) = 30 these produced 180 TB of LRAT.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| Encoding gives ES(4) = 5 and ES(5) = 9 | SAT/UNSAT; sanity check only | `encode.py` |
| ES(5) ≤ 9 | LRAT proof checked by `lrat_check.py` | `encode.py 9 5` |
| ES(6) > 16: explicit 16-point set, no convex hexagon | exhaustive exact check of all 8008 6-subsets | `construct.py 6` |
| ES(7) > 32: explicit 32-point set, no convex heptagon | exhaustive exact check of all 7-subsets | `construct.py 7` |
| ES(6) ≤ 17 | LRAT proof (302 MB, 1,288,188 lemmas) checked by `lrat_check.py`; CaDiCaL 1.7.3, 191 s on 1 core; CNF sha256 `587ae401…0902ad2` | `reproduce.sh` |
| **ES(6) = 17** | combination of the two rows above, plus the encoding soundness argument | |
| Encoding faithful on real point sets | 300 random sets agree with brute force (all 300 contained a k-gon, so this check was one-sided; now complemented by the balanced check below); symmetry-break transform preserves all orientations on 200 random sets | `test_encoding.py` |
| Compact cup/cap encoding equisatisfiable with `encode.py` on (k,N) ∈ {(4,4),(4,5),(5,8),(5,9),(6,16),(6,17)} | SAT/UNSAT agreement, CaDiCaL 1.7.3 | `encode_compact.py` |
| Compact encoding faithful on real point sets | 400 random instances (160 with k-gon, 240 without, k = 4…7) agree with brute force, both by aux-truth assignment and by SAT with fixed orientations; ES sets n = 5, 6, 7 satisfy it; soundness argument in docstring | `test_encoding.py` |
| ES(6) ≤ 17 (second, independent certificate) | compact encoding UNSAT in 161 s (old encoding 201 s, same machine); LRAT proof (471 MB, 1,319,776 lemmas) checked by `lrat_check.py`; CNF sha256 `682629f2…a252e81e3` | `COMPACT=1 reproduce.sh` |
| ES(7) ≤ 33 | **open**. N = 33 compact formula (64,240 vars, 722,800 clauses) not solved: direct CaDiCaL 1,480 s gave no answer | `es7_probe_data/` |
| Fixed-depth lookahead cube-and-conquer for ES(7) ≤ 33 costs ≥ 10⁸ CPU-years at depths 44–60 | empirical sample estimate (Knuth probes, 2–11 per depth, timeouts counted as lower bounds); heavy-tailed | `cube_sample.py`, `cube_estimate.py` |
| *(superseded by the two rows below)* Cost of an optimised SAT proof of ES(7) ≤ 33: weeks to > 10⁸ CPU-years, central guess 10³–10⁶ | **heuristic** extrapolation of per-level hardness ratio from 4 walks; method within ×30 per walk on ES(6) | Approach 4 |
| Reflection lex-leader (and hull-ear rule) sound | proof (Lemma R + theorem, Approach 5); tested on 128 point sets / 1,302 normalisations against brute force | `symmetry_extra.py`, `test_encoding.py` |
| ES(6) ≤ 17 (third certificate, compact + reflection SB) | UNSAT in 35.7 s (38.1 s with LRAT) vs 162 s baseline; LRAT proof (139 MB, 478,525 lemmas) checked by `lrat_check.py` in 13.6 s; CNF sha256 `e81aee68…5a2dba` | `REFLECT=1 reproduce.sh` |
| Static-split cube-and-conquer for ES(7) ≤ 33 at depth 24 costs ≥ 375 CPU-years | empirical Knuth estimate, 10 walks, 7 of 10 cubes censored (lower bound); heavy-tailed | Approach 6, `es7_probe_data/static33_*` |
| Cost of a SAT proof of ES(7) ≤ 33 with the best current setting: 10^2.5–10^4 CPU-years, central ~10³ | **heuristic**; Knuth lower bound plus r-extrapolation on 3 walks; near-root r taken from the k = 6 calibration | Approach 6 |

## Trust base for ES(6) ≤ 17

- `encode.py` is correct, meaning the soundness argument and symmetry lemma above hold. This part is not formally verified. It is supported by `test_encoding.py`.
- `lrat_check.py` is correct. It is about 80 lines, and it was tested to reject a corrupted proof.
- The third certificate (Approach 5) also trusts Lemma R, the reflection lemma, which is proved above and tested in `test_encoding.py`.
- Upgrade path: check the same proof with cake_lpr (a verified checker), and formalise the encoding as Marić 2019 did.

## Next steps

- **Go/no-go for ES(7) (2026-11-24): NO-GO for further compute in this
  project.**
  - With the strongest setting found (compact encoding, reflection
    lex-leader, Heule–Scheucher static split, tuned CaDiCaL), a SAT proof
    of ES(7) ≤ 33 costs **at least 375 CPU-years** at depth 24. This is a
    measured lower bound.
  - The best estimate is about 10³ CPU-years, with a range of
    10^2.5–10^4 (Approach 6). That is 2–4 orders of magnitude more than
    h(6) = 30 (about 2 CPU-years on a 1,000-instance cluster), and
    centuries on this project's 4 cores.
  - The earlier gap of "weeks to 10⁸" is closed from both sides. The
    pessimistic end is gone (the static split beats the lookahead by
    ≥ 10⁵). The optimistic end ("weeks") needs r ≈ 1.6 up to the root,
    which the k = 6 calibration contradicts.
  - **Do not run more ES(7) cubes here.**
- **What would change the verdict.** ES(7) needs a structural idea from the
  literature or new mathematics before more compute, cheapest first:
  1. *Break the hull-vertex symmetry.* Heule–Scheucher left it unbroken and
     expect at least 3×. The local ear rule tried here gave nothing
     (Approach 5). A full break must handle an assignment-dependent
     relabelling.
  2. *A structural case split with an exhaustiveness proof.* For example
     the hull size (at most 6 for a 7-gon-free set) or the convex-layer
     sizes, as in Dumitru's templates. His published template times
     (10³–2·10⁶ s each) suggest it is not cheap either.
  3. *Encoding work.* Further domain-consistent clauses, and
     Heule–Scheucher's extra split on X(b,b+2,b+4) at alternating
     patterns, which cut their worst cubes from days to under an hour.
     Re-measure on ES(6) first; the bar is a 10× gain.
  - Only if these bring the estimate near 10 CPU-years is a cluster
    campaign worth planning. It should start with a pilot of about 100
    unbiased depth-20–24 cubes, uncapped or with caps ≥ 4 h, to pin the
    censored tail (roughly 1–2 core-months).
- **Literature still unread:** Balko–Valtr (SoCG 2017), "A SAT attack on
  the Erdős–Szekeres conjecture". A commented-out remark in the
  Heule–Scheucher arXiv source says it found 7-gon-free configurations on
  33 elements in a more general setting; this has not been checked. Read it
  before any structural work, since it may limit what a purely
  combinatorial argument can do.
- **ES(6) trust upgrades.**
  - Check any of the three LRAT proofs with cake_lpr, a verified checker.
  - Formalise one of the two encodings, as Marić 2019 did.
  - The compact encoding's soundness argument is short (convex-under-chord
    geometry), which makes it the better formalisation target.
