# Erdős–Szekeres convex polygon conjecture

**Area:** combinatorial geometry
**Status:** in progress (ES(6) = 17 reproduced and certified; ES(7) not yet attempted)
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
  - Old encoding: 201 s, which is about 20% slower. Only a modest gain.
- **Certificate.** The LRAT proof (471 MB, 1,319,776 lemmas) was checked by
  `lrat_check.py` in 55 s. It reports VERIFIED. The CNF sha256 is
  `682629f2…a252e81e3`. This gives a second, independent certificate for
  ES(6) ≤ 17, through a different encoding.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| Encoding gives ES(4) = 5 and ES(5) = 9 | SAT/UNSAT; sanity check only | `encode.py` |
| ES(5) ≤ 9 | LRAT proof checked by `lrat_check.py` | `encode.py 9 5` |
| ES(6) > 16: explicit 16-point set, no convex hexagon | exhaustive exact check of all 8008 6-subsets | `construct.py 6` |
| ES(7) > 32: explicit 32-point set, no convex heptagon | exhaustive exact check of all 7-subsets | `construct.py 7` |
| ES(6) ≤ 17 | LRAT proof (302 MB, 1,288,188 lemmas) checked by `lrat_check.py`; CaDiCaL 1.7.3, 191 s on 1 core; CNF sha256 `587ae401…0902ad2` | `reproduce.sh` |
| **ES(6) = 17** | combination of the two rows above, plus the encoding soundness argument | |
| Encoding faithful on real point sets | 300 random sets agree with brute force; symmetry-break transform preserves all orientations on 200 random sets | `test_encoding.py` |

## Trust base for ES(6) ≤ 17

- `encode.py` is correct, meaning the soundness argument and symmetry lemma above hold. This part is not formally verified. It is supported by `test_encoding.py`.
- `lrat_check.py` is correct. It is about 80 lines, and it was tested to reject a corrupted proof.
- Upgrade path: check the same proof with cake_lpr (a verified checker), and formalise the encoding as Marić 2019 did.

## Next steps

- Scale estimate for ES(7) ≤ 33:
  - The naive encoding has C(33,7)·32 ≈ 1.4·10⁸ clauses, so the forbidden
    pattern needs auxiliary cup/cap variables (Scheucher-style).
  - It also needs much stronger symmetry breaking and cube-and-conquer.
  - Expect this to be orders of magnitude beyond ES(6), probably a
    cluster-scale computation rather than a single-session one.
- Literature check: confirm whether ES(7) has been attacked by SAT already,
  and what the best published partial results are.
