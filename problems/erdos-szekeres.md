# Erdős–Szekeres convex polygon conjecture

**Area:** combinatorial geometry
**Status:** in progress (ES(6) = 17 reproduced and certified twice; ES(7) cost-probed, not resolved)
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
  (signotope encodings; ES(6) in CPU hours). Heule–Scheucher 2024 used SAT
  plus a verified encoding for the empty-hexagon number h(6) = 30.
- ProofAtlas note: a SoCG 2025 paper refutes an ordered-hypergraph
  generalisation, but the planar conjecture stays open.

- Scheucher, "A SAT attack on higher dimensional Erdős–Szekeres numbers"
  (arXiv:2105.08406). It uses chirotope/signotope encodings with DRAT
  certificates. A 2026 survey says SAT brought ES(6) verification down to
  about an hour (Marić; Scheucher).
- **Closest prior work on ES(7):** B. Dumitru, "Notes on the 33-point
  Erdős–Szekeres problem" (arXiv:2512.24061, Dec 2025). It proposes a SAT
  encoding (triple orientations plus a 4-subset reduction) for 33 points,
  but does not resolve it, and reports heavy-tailed solver behaviour. Read
  this before investing in ES(7).

- **Literature attempt, 2026-11-23 (second worker).**
  - arXiv.org is blocked by this session's network policy. WebFetch failed
    with ENOTFOUND, and curl got a CONNECT 403 from the proxy, so the full
    text of arXiv:2512.24061 was **not read**.
  - A web-search snippet of the abstract (not verified against the paper)
    says it uses:
    - triple-orientation variables;
    - a 4-set convexity criterion for excluding convex 7-gons;
    - "convex-layer anchoring" constraints.
  - The same snippet says it reports UNSAT certificates for a collection of
    *anchored subfamilies* only, with heavy-tailed runtimes dominating the
    effort.
  - Nothing more is assumed here about its encoding, sizes or timings.
  - The same search also listed arXiv:2604.20120, "Combinatorial Geometry of
    Erdős–Szekeres Type Problems: SAT/ASP Modeling and Linear Subreduction".
    It was not read, and its relevance to ES(7) is unknown.

The citations were checked against web search results only (2026-11-23), not
the full papers. Run `mathbox:literature-check` before any write-up.

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
| Cost of an optimised SAT proof of ES(7) ≤ 33: weeks to > 10⁸ CPU-years, central guess 10³–10⁶ | **heuristic** extrapolation of per-level hardness ratio from 4 walks; method within ×30 per walk on ES(6) | Approach 4 |

## Trust base for ES(6) ≤ 17

- `encode.py` is correct, meaning the soundness argument and symmetry lemma above hold. This part is not formally verified. It is supported by `test_encoding.py`.
- `lrat_check.py` is correct. It is about 80 lines, and it was tested to reject a corrupted proof.
- Upgrade path: check the same proof with cake_lpr (a verified checker), and formalise the encoding as Marić 2019 did.

## Next steps

- **ES(7) ≤ 33 needs a structural reduction before any big run.** The probe
  in Approach 4 shows that generic lookahead cubing on orientation variables
  is hopeless at fixed depth (≥ 10⁸ CPU-years). The heuristic cost of even an
  optimised solve is uncertain over about 7 orders of magnitude. Candidate
  bounded steps, cheapest first:
  1. **Measure the near-root hardness profile.** Pick 3–4 walks and solve
     the cubes at depths 8, 16, 24, 32 and 40 with a 2–4 h cap each, about
     1 core-day. This pins r near the root, which dominates the uncertainty
     in the extrapolation.
  2. **Stronger symmetry breaking and redundant clauses.** Both must be
     sound, with an argument written down.
     - The remaining symmetries after fixing point 0 are the choice of hull
       vertex and reflection; use lex-leader constraints over them, as in
       Scheucher / Heule–Scheucher.
     - Add explicit no-6-cup clauses among points 1…32. They are implied
       already, since X(0,·,·) is true and point 0 extends every cup;
       test whether stating them helps. There is no cap analogue.
     - Add monotone "≥ l" auxiliaries.
     - Re-measure on ES(6) first. The target is a large speed-up, not 20%.
  3. **Domain splitting instead of literal splitting.** Split on structural
     invariants, such as the size of the convex hull or of the first convex
     layer, or the longest cup or cap through point 1. This is close in
     spirit to Dumitru's anchoring. Each piece must be argued exhaustive.
  4. **Read arXiv:2512.24061 in full** before step 3. This needs arxiv.org to
     be allowed in the session's network settings. Also read
     Heule–Scheucher's cubing for h(6) = 30 (arXiv:2403.00737) and
     arXiv:2604.20120.
- **ES(6) trust upgrades.**
  - Check either LRAT proof with cake_lpr, a verified checker.
  - Formalise one of the two encodings, as Marić 2019 did.
  - The compact encoding's soundness argument is short (convex-under-chord
    geometry), which makes it the better formalisation target.
