# Frankl's union-closed sets conjecture

**Area:** extremal combinatorics / information theory
**Status:** in progress. Literature pinned down from primary sources. The
one-variable inequality behind the (3−√5)/2 bound is **certificate-checked**
here with self-contained interval arithmetic. **Every finite computation** in
Costa–Sadhu's proofs of c_UC ≥ c_L ≈ 0.3827091 (their Thm 1.1) and of the
record c_UC ≥ 0.3828852549667978 (their Thm 1.2) is **independently
re-certified** (analytic steps read, not machine-checked). The conjecture is **checked
exhaustively for universes of size n ≤ 6**: all 75,973,751,474 labeled
families, reproducing the known labeled counts exactly.
**Started:** 2026-11-24
**ProofAtlas:** rank 363

## Statement

A family F of finite sets is *union-closed* if A ∪ B ∈ F for all A, B ∈ F.

**Conjecture (Frankl, 1979).** Every finite union-closed family F ≠ {∅}
(F nonempty) has an element x with |{A ∈ F : x ∈ A}| ≥ |F|/2.

Remarks.

- WLOG ∅ ∈ F. Adding ∅ keeps F union-closed, raises |F| by one and changes
  no frequency. So the conjecture for F ∪ {∅} implies it for F.
- Union-closed families on [n] that contain ∅ are exactly the complements
  {[n] \ A : A ∈ F} of *Moore families* (intersection-closed families
  containing [n]).
- Write c_UC := inf_F max_x freq_x(F)/|F| over finite union-closed F that
  contain a nonempty set. The family {∅, {1}} gives c_UC ≤ 1/2, and the
  conjecture says c_UC = 1/2.
- Equivalent forms exist for lattices (every finite lattice with ≥ 2 elements
  has a join-irreducible a with |[a, 1]| ≤ |L|/2) and for bipartite graphs
  (Bruhn–Charbit–Schaudt–Telle). See the survey of Bruhn–Schaudt.

## Known results

Labels: **[read]** = the arXiv LaTeX source was read for the cited
statement; **[skimmed]** = the source was searched for the cited constant
and its statement read, not the whole proof; **[abstract]** = arXiv abstract
only. Literature was checked on 2026-11-24 with the arXiv API: every title or
abstract containing "union-closed", "union closed" or "Frankl", up to
arXiv:2611.13749. OEIS could not be reached (the host was blocked), so all
counts are taken from Brinkmann–Deklerck (below).

### Lower bounds on c_UC (the entropy method)

| bound | who | status | label |
| --- | --- | --- | --- |
| 0.01 | Gilmer, arXiv:2211.09055 (Nov 2022) | proved | [abstract] |
| (3−√5)/2 ≈ 0.381966 | Alweiss–Huang–Sellke arXiv:2211.11731, EJC 31(3) P3.35 (2024); Chase–Lovett arXiv:2211.11689; Sawin arXiv:2211.11504; Pebody arXiv:2211.13139 (all Nov 2022) | proved. AHS use a computer check for one 1-variable inequality, which Boppana (arXiv:2301.09664, 1985 origin) proves by calculus | AHS [read]; others [abstract] |
| ≈ 0.3823455 (exactly the optimum of Sawin's iid + max-entropy mixture, 0.382345533366703) | Sawin (strict improvement, no value); Yu arXiv:2212.00658 (≈ 0.38234, numerical); Cambie arXiv:2212.12500 (proof of the optimum, computer-aided) | proved (Cambie) | Cambie [skimmed], Yu [abstract] |
| > 0.3823455 strictly; ≈ 0.382709 under numerically checked hypotheses | Liu, arXiv:2306.08824 (CISS 2024), conditionally-iid couplings | the strict improvement is analytic; 0.382709 is not proved | [skimmed] |
| c_L = 1 − x*H(x*)/H(x*²) > 0.382709087918735, where x* is the root in (0,1) of x⁴−2x³+3x²−1 | Costa–Sadhu, arXiv:2610.02295 Thm 1.1 (Oct 2026); earlier Zenodo preprint by Costa | preprint; computer-assisted (MPFR intervals, Bernstein certificate) | [read] §§1–5 |
| **0.38288525 = 1531541/4000000** | Jiang, arXiv:2609.08291 (8 Sep 2026) | preprint; computer-assisted (interval code in the appendix) | [read] intro, §ceiling |
| **0.3828852549667978** | Costa–Sadhu, arXiv:2610.02295 Thm 1.2 (1 Oct 2026). **This is the ProofAtlas "Oct 2026" claim.** | preprint, not refereed; computer-assisted (Zenodo supplement). **All finite computations re-verified here** (Approach 4) | [read] §6, App. A |

Current best *claimed* constant: **0.3828852549667978** (Costa–Sadhu,
unrefereed; every finite computation of its proof independently re-verified
here, analytic steps read). The best constant in a refereed journal is (3−√5)/2 (AHS, EJC
2024). Cambie's 0.3823455 is in an arXiv v2 (2025); whether it was refereed
was not checked. Two independent groups give near-identical values
(0.38288525 and 0.38288525497), and both bounds sit within 10⁻⁸ of the same
proved ceiling (next section). That agreement is decent evidence that the
numerics are right, but it is not a referee check.

### Barriers: what each variant of the method can give

The engine is Gilmer's. Let A, B be two samples of a uniform member of F, with
some coupling. Then A ∪ B ∈ F, so H(A ∪ B) ≤ log|F| = H(A). Coordinatewise
chain-rule bounds turn this into a one-coordinate inequality between
probability measures on [0,1]. Each choice of coupling family gives its own
optimal constant:

1. **iid coupling.** The optimum is exactly **(3−√5)/2**. AHS [read] prove
   min_{μ: mean φ} E_{μ×μ} H(xy) − E_μ H(x) ≥ 0 iff φ ≥ (√5−1)/2 (with
   x = 1 − p). The minimiser is two-point, {0, x}. The key fact is
   φ H(x²) ≥ x H(x) on [φ, 1]. Chase–Lovett [abstract] show (3−√5)/2 is
   *sharp* for "approximately union-closed" families, so no iid argument that
   only uses approximate union-closedness can beat it.
2. **Sawin's mixture of iid and max-entropy coupling.** The optimum is
   ≈ **0.382345533366703** (Cambie [skimmed], §"upper bound": "one cannot aim
   to prove the result with a constant better than 0.382345533366703 with the
   exact suggested approach of Sawin").
3. **Liu's conditionally-iid couplings, Example 5 with f(x) = x(1−x), mixed
   with iid.** The value is c_L ≈ **0.382709087918735**. Liu found it
   numerically; Costa–Sadhu proved it.
4. **The "pointwise product" relaxation.** The iid kernel is mixed with one
   (or finitely many) conditionally-iid kernels K, each bounded below by
   ψ(x)ψ(y). The ceiling is
   **C\* = 1/2 − (1−q\*) ln(1+q\*) / (2 ln 2) ≈ 0.3828852599667978**, where q\*
   is the root in (0,1) of (1−q)ln(1−q) + q ln(1+q) = 0 (q\* ≈ 0.69090774).
   This is proved in Jiang [read], Prop. "Limitation of the pointwise method".
   The proof has two steps. The endpoint y = 1 forces m·w₀ ≥ 1/2. The
   diagonal x = y = q, with ψ(q)² ≤ K(q,q) ≤ ln 2, then gives the bound.
   Costa–Sadhu §7 state the same number. Both record bounds sit within
   5.1·10⁻⁹ of this ceiling, so **this route is exhausted**. Any further
   progress needs a different inequality: global couplings (Jiang §global,
   which gives a gain that tends to 0 with |F|), more coordinates, or
   non-entropy input.
5. **Gilmer's strengthening.** Gilmer's Conjecture 1 would have given 1/2. It
   is false (Sawin [abstract]; Ellis, arXiv:2211.12401 [abstract]).

We recomputed (mpmath, 40 digits; this is a check, not part of any proof):
x* = 0.690787593924988, c_L = 0.382709087918735030, q* = 0.690907738725408,
C* = 0.382885259966797797. All agree with the papers.

### Exact verification for small cases

Notation clash: the survey writes m for the universe size and n for the number
of sets. Here **n = universe size**.

- **n ≤ 12** (universe of at most 12 elements). Živković–Vučković, "The 12
  element case of Frankl's conjecture", preprint 2012, as cited in the
  Bruhn–Schaudt survey (Graphs Combin. 31 (2015); arXiv:1309.3297 [read], Thm
  "m=12"). The method uses FC-families and weights (Poonen's theorem) plus a
  computer search. Earlier steps: n ≤ 11 (Bošnjak–Marković, EJC 15 (2008)
  R88), n ≤ 10 (Marković 2007), n ≤ 9 (Lo Faro 1994), n ≤ 7 (Poonen 1992).
  We did not locate a refereed version of the n = 12 paper, and no claim of
  n = 13 was found on arXiv.
- **|F| ≤ 50 sets.** Lo Faro (1994), rediscovered by Roberts–Simpson
  (Australas. J. Combin. 47 (2010)): a minimal counterexample on a minimal
  universe of size n has at least 4n − 1 sets. Combined with n ≤ 12, this
  gives ≥ 4·13 − 1 = 51 sets (survey Cor. "n=50" [read]). Older direct bounds:
  ≤ 36 sets (Lo Faro), ≤ 40 sets (Roberts 1992 tech. report).
- **Formalisation.**
  - Marić–Živković–Vučković: FC-families in Isabelle/HOL (CICM 2012,
    arXiv:1207.3604) and a fully verified classification of FC(6) families
    (arXiv:1902.08765), both [abstract].
  - Koutsoukou-Argyraki–Paulson: Isabelle/HOL formalisation of the
    Aaronson–Ellis–Leader special case (arXiv:2609.20876, Sep 2026) [abstract].
  - Ho (arXiv:2601.19327, Jan 2026) [abstract]: proves α_k H(x^k) ≥
    x^{k−1} H(x) for real k > 1 and **formalises the proof in Lean 4**. The
    case k = 2 is Boppana's inequality.
- **Structural special cases.** These cover the ≥ (2/3)2^n regime, separating
  families with ≤ 2n sets (Maßberg, arXiv:1508.05718), lower semimodular
  lattices, subcubic graphs, and height ≤ 4 in the ∅-free form (Tian,
  arXiv:2608.25147, 2026, [abstract]).
- **Enumeration data used as ground truth.** Brinkmann–Deklerck
  (arXiv:1701.03751 [read], Tables 1–2) give these numbers of labeled
  union-closed families on [n] that contain ∅ (= labeled Moore families), for
  n = 1..7:
  - labeled: 2, 7, 61, 2480, 1385552, 75973751474, 14087648235707352472;
  - up to isomorphism: 2, 5, 19, 184, 14664, 108295846, …;
  - with universe exactly [n] ("UCS"), labeled: 1, 4, 45, 2271, 1373701,
    75965474236, ….

  (These are probably OEIS A102896 / A102894. That could not be confirmed,
  because OEIS was unreachable.)

## Approaches

### 1. Reproduce the iid entropy bound rigorously (interval arithmetic)

- **Idea.** AHS reduce the constant (3−√5)/2 to a one-variable inequality
  (Claim 1): φ H(x²) ≥ x H(x) for x ∈ [φ, 1], φ = (√5−1)/2. Their appendix
  checks it by floating point to within 10⁻³ and notes that it "can be made
  completely rigorous using interval arithmetic". We do exactly that, on all of
  [0, 1] (Boppana's form).
- **Outcome:** worked. See `computations/frankl/verify_boppana.py`, which
  certifies the inequality in 0.3 s:
  - **R0, x ∈ (0, 1/100]: analytic.** G(x) ≥ x²[(2φ−1) log(1/x) − 1] > 0,
    because (2φ−1) log 100 − 1 ∈ [0.08713, 0.08714].
  - **R1, x ∈ [1 − 1/4096, 1): analytic.** Write y = 1 − x and b = 1/4096.
    Then G ≥ y[(φ(2−b)−1) log(1/y) − φ(2−b) log 2 − 1], and the bracket is
    ≥ 0.1056 at y = b. It is increasing in log(1/y).
  - **R2, x ∈ [1/2, 4/5]: tangency.** G(φ) = 0 and G'(φ) = 0 exactly, by the
    algebra below. G'' ≥ 0.0021 > 0 on [1/2, 4/5] (44 interval cells), so
    G(x) = ∫_φ^x (x−s) G''(s) ds > 0 for x ≠ φ.
  - **R3, [1/100, 1/2] ∪ [4/5, 1 − 1/4096]: bisection.** Mean-value-form
    enclosures over 29 + 15 cells; the minimum certified lower bound is
    2.9·10⁻⁵.

  The exact algebra at φ: φ² = 1 − φ gives H(φ²) = H(φ). Also
  log((1−φ²)/φ²) = −log φ =: L and log((1−φ)/φ) = log φ = −L. Hence
  G(φ) = φH(φ) − φH(φ) = 0. Then G'(φ) = 2φ²L − H(φ) + φL, and
  H(φ) = φL + 2φ²L, so G'(φ) = 0.
- **Interval arithmetic** (`interval.py`) is pure Python on IEEE doubles.
  +, −, ×, ÷ and √ are rounded one ulp outward. log is computed by an atanh
  series after an exact frexp reduction, with a rigorous tail bound; log 2 is
  bounded in exact rationals. It never calls libm log. Tests cross-check it
  against exact rational bounds and against mpmath.iv.
- **What this establishes.** AHS Claim 1 (hence Boppana's inequality) is
  certificate-checked. With AHS Theorems 1–2 [read], this gives
  c_UC ≥ (3−√5)/2. The reduction itself is AHS's analytic argument; we read it
  but did not formalise it.

### 2. Exhaustive small-case checker

- **Idea.** Enumerate every union-closed F ∋ ∅ on [n] by splitting on the last
  element: F0 = members without n, F1 = (members with n) minus n. The
  conditions are: F0 union-closed with ∅ ∈ F0; F1 union-closed; F0 ∨ F1 ⊆ F1.
  - F0 runs over S_{n−1}-classes, weighted by orbit size.
  - F1 runs over a depth-first search of the subsets in decreasing numeric
    order. The prefix chosen so far is always closed, because s | t ≥ s. So
    "may s be added" is a check of a few bit operations, and each family
    appears exactly once.
  - Frequencies are popcounts.
- **Outcome:** worked. See `computations/frankl/frankl_enum.c` and
  `results/small_cases.txt`.

| n | labeled families ∋ ∅ (ours = literature) | with universe [n] (ours = lit.) | S_{n−1} classes of F0 | Frankl fails | tight (max freq = \|F\|/2) |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 0 | 1 |
| 2 | 7 | 4 | 2 | 0 | 4 |
| 3 | 61 | 45 | 5 | 0 | 14 |
| 4 | 2,480 | 2,271 | 19 | 0 | 51 |
| 5 | 1,385,552 | 1,373,701 | 184 | 0 | 202 |
| 6 | **75,973,751,474** | **75,965,474,236** | 14,664 | **0** | 876 |

  The n = 6 run used 925,328,674 representative (F0, F1) pairs and took about
  3 minutes on 4 cores. For n ≤ 4, everything (counts, classes for n ≤ 3,
  tight counts) is also re-derived by naive Python brute force over all
  subfamilies (`test_frankl.py`).
- **Limit.** n = 7 has 1.4·10¹⁹ labeled families, about 2·10¹⁶ (F0, F1)
  pairs even after symmetry. Plain enumeration cannot go further. The known
  range n ≤ 12 needs FC-family pruning.

### 3. Independent re-verification of Costa–Sadhu Thm 1.1 (c_UC ≥ c_L ≈ 0.382709)

- **Idea.** Costa–Sadhu's proof of the bound c_L has four parts:
  - Liu's one-coordinate criterion (Liu, Prop. 3);
  - the positive-correlation Lemma 2.1;
  - Lemma R: H(r(x,y))² ≥ H(g(x)) H(g(y)), where r = xy(2−x−y+xy) and
    g(x) = r(x,x);
  - Lemma S: 2αH(xy) + 2β√(H(g(x))H(g(y))) ≥ (xH(y)+yH(x))/m*, where
    m* = 1 − c_L and α, β are fixed by tangency at x = y = x*.

  Lemma R is analytic except for one exact Bernstein certificate. Lemma S has
  analytic boundary lemmas (5.3, 5.4), a Hessian check around the tangency
  (t*, 0), and an interval box cover of the compact remainder. Our code
  re-does every one of these finite steps, with our own cover.
- **Outcome:** worked. See `computations/frankl/costa_sadhu_checks.py` and
  `results/costa_sadhu_thm11.txt`.
  - **Exact rationals.**
    - The identity W r_xy = UV + xy, and r_x = yU, r_y = xV, r_xy, by
      formal differentiation.
    - g(43/64) − 1/2 = 305/2²⁴.
    - The 4×4 Bernstein matrix of WUV − (1−r) on [0, 43/64]² equals the
      published matrix entry by entry, and every entry is > 0.
  - **Constants** (intervals): x* ∈ [0.690787593924988, 0.6907875939249881],
    m* ∈ [0.61729091208126, 0.61729091208127], β ∈ [0.1000525598628,
    0.1000525598630], t* = −log x* ∈ [0.36992289186770, 0.36992289186772],
    c₀ = m*α ∈ [0.55552937614741, 0.55552937614746] > 1/2. All lie inside the
    published enclosures. The decimal claim c_L > 0.382709087918735 holds
    with a margin of only **3.0·10⁻¹⁷**, so it needs exact rational
    arithmetic: we used a bracket for x* of width 2⁻⁷¹ and atanh-series log
    bounds.
  - **Scalars of Lemmas 5.3/5.4**: ζ(0.002) ≥ 0.0166724744112; the
    5.4(a, b, c) values are ≥ 0.00117883769797, 0.0355980952001 and
    0.0107176824298. Each is positive and matches the paper.
  - **Tangency.** We use our own local rectangle Q₀ = [5/16, 7/16] × [−1/16,
    1/16] in (t, d); F is even in d. On it F_tt ≥ 0.0337, F_dd ≥ 0.78 and
    det ≥ 8.8·10⁻⁵ (703 boxes). So F is convex on Q₀. The point (t*, 0) is
    stationary with F = 0 there (their Lemma 5.5, analytic), so F ≥ 0 on Q₀.
  - **Cover.** This is our own dyadic decomposition: t ∈ [1/512, 45/32] with
    v = t − d ≥ 2⁻¹⁵, and t ∈ [45/32, 33/8] with v ≥ 3/32. It overlaps the
    analytic regions (t ≤ 0.002; v ≤ 5·10⁻⁵ for t ≤ 1.4; v ≤ 0.1 for
    1.4 ≤ t ≤ 4.1; t ≥ 4.1).
    - It uses 31,944 boxes with mean-value lower bounds F̃(c) −
      sup|F̃_t|Δt − sup|F̃_ξ|Δξ, all rigorously rounded. The minimum certified
      lower bound is 2.7·10⁻⁷.
    - Box endpoints are exact dyadics, and the clipping ξ ≤ 1 − ν/t is
      rounded upward.
    - It takes about 8 CPU-minutes.
  - **Test harness.** `test_frankl.py` checks the derivative formulas
    (G', G'', Γ₅', Γ₅'', F̃_t, F̃_ξ and the Hessian) against 40-digit finite
    differences. The mean-value bounds rely on them.
- **What this establishes.** We re-ran every computer-assisted assertion
  that Thm 1.1 uses, with independent code (not their MPFR supplement) and a
  different cover. They come out true. We read but did not machine-check:
  - Lemma 4.1 (entropy, one variable);
  - Lemma 4.4 (M decreasing);
  - the case analysis of Lemma R;
  - Lemmas 5.2–5.5;
  - the reduction (Prop. 3.1);
  - Lemma 2.1;
  - Liu's Prop. 3. This was read only as Costa–Sadhu restate it.

  We found no error. Label: **c_UC ≥ c_L — proof read, all finite
  computations certificate-checked independently**. (Their record Thm 1.2
  is treated in Approach 4.)

### 4. Independent re-verification of Costa–Sadhu Thm 1.2 (c_UC ≥ 0.3828852549667978)

- **Source.** arXiv:2610.02295 v1 LaTeX, §6 (Lemmas 6.1, 6.2, Prop. 6.3,
  proof of Thm 1.2) and Appendix A (Certificates A.4–A.7) **[read]**. The
  Zenodo supplement (record 22727713) was **not** used; every check below is
  our own code.
- **Parameters** (all exact rationals): ℓ₀ = 1409/2000, τ₀ = ℓ₀² =
  1985281/4000000, m₀ = 3085573725166011/(5·10¹⁵), α₀ = 1/(2m₀) + 1/800000000,
  β₀ = 1 − α₀. The theorem's decimal is exactly 1 − m₀. Kernel
  r(x,y) = xy(1 + τ₀(1−x)(1−y)) (Liu's Example 5 with f = ℓ₀x(1−x)),
  g(x) = r(x,x).

#### Proof map

The chain is: Liu's Prop. 3 (criterion) → Prop. 6.3 (integrate the two
pointwise inequalities; uses Lemma 2.1, positive correlation in C₃(P)) →
Lemma 6.1 + Lemma 6.2. Analytic steps (A) were read; finite computations (C)
were re-done.

1. **Lemma 6.1** (tuned product): H(r(x,y))² ≥ H(g(x))H(g(y)) on [0,1]².
   - (A) Δ_x(y) = L(x,y) − ½L(x,x) − ½L(y,y), L = log H∘r; it suffices that
     ∂_yΔ = L₂(x,y) − L₂(y,y) > 0 for x < y.
   - (C) exact: r_x = y[1+τ₀(1−2x)(1−y)], r_y = x[1+τ₀(1−x)(1−2y)],
     r_xy = 1+τ₀(1−2x)(1−2y); identity W·r_xy − r_x r_y/(xy) = τ₀xy;
     g′ = 2x[1+τ₀(1−x)(1−2x)] with (1−x)(1−2x) ≥ −1/8;
     g(45/64) − ½ = 42978321721/2684354560000.
   - Case g(y) < ½: (C) **Certificate A.4**, exact Bernstein: the 16
     product-Bernstein coefficients of W·U·V − τ₀(1−r) on [0, 45/64]² are
     positive, minimum 4652778828628843621308587/8388608·10¹⁸. (A) This gives
     r_xy/(r_x r_y) ≤ 1/r + 1/(1−r); with Lemma 4.1
     (−Λ″/Λ′ > 1/u + 1/(1−u) on (0, ½), Λ = log H) it gives L₁₂ < 0.
   - Case g(y) ≥ ½: (A) A_x(y) = r_y/r < A_y(y), and Lemma 4.4 (M = uH′/H is
     strictly decreasing) gives L₂(x,y) > L₂(y,y).
2. **Lemma 6.2** (second inequality): F₀(s,σ) > 0 for 0 < s ≤ σ, where
   x = e^−s, y = e^−σ,
   F₀ = α₀G(s+σ) − (G(s)+G(σ))/(2m₀) + β₀√(W₀(s)W₀(σ)),
   G(u) = e^u H(e^−u) and W₀(u) = e^{2u}H(g(e^−u)).
   - (A) G is increasing and concave (series); W₀ is increasing (its proof
     uses z q_z = 2q − 2τ₀z³(1−z) and 27τ₀/256 < 1, both re-checked exactly);
     0 ≤ D := G(s)+G(σ)−G(s+σ) ≤ min(G(s)−s, G(σ)−σ) < 1.
   - (C) **Certificate A.5**: for all v > 0, W₀(v) ≥ (8/5)G(v) and
     G(16v) ≥ (178/25)G(v); three scalar margins (8β₀/5)√(178/25) − 1/(2m₀),
     β₀W₀(2) − 1/(2m₀) and 8β₀ log 2 − 1/(2m₀) are positive.
   - (A) Case 1, G(σ) ≥ (178/25)G(s): F₀ ≥ G(s+σ)/8·10⁸ + G(s)·[first
     scalar] > 0. **This is the y → 1 edge** (s → 0). There F₀ → G(σ)/8·10⁸,
     because m₀α₀ − ½ = m₀/8·10⁸ = 7.7·10⁻¹⁰. The proof never resolves that
     margin numerically: Case 1 works with the 2.9·10⁻⁶ margin.
   - (A) Case 2, s, σ ≥ 2: uses D < 1, W₀ increasing and the second scalar.
   - (A) Case 3, s, σ ≤ 2⁻¹⁰: D < uH(λ) (via −G″(v) < 1/v),
     W₀(w) ≥ 2w log(1/2u), H(λ) ≤ 2√(λ(1−λ)), and the third scalar.
   - (A) What remains: σ < 16s, s < 2, σ > 2⁻¹⁰. That is, in t = (s+σ)/2
     and ξ = (σ−s)/(σ+s): 2⁻¹¹ < t < 17 and 0 ≤ ξ < 15/17.
   - (C) **Certificate A.6**: F(t,d) := F₀(t−d, t+d) has a positive definite
     Hessian on a rectangle around (t_c, 0), t_c = 0.369781418829901. Also
     F₀(t_c,t_c) ≈ 1.14·10⁻⁸ and |F_t(t_c,0)| is tiny; F is even in d. So
     F > 0 there by the tangent-plane inequality.
   - (C) **Certificate A.7**: a finite box cover of [2⁻¹¹, 17] × [0, 15/17].
     Each cell either lies in the A.6 rectangle or has a positive
     mean-value lower bound.
3. **Prop. 6.3 and the theorem** (A): Lemma 6.1 + Lemma 2.1 give
   ∬H(r)dρ ≥ (∫√(H∘g) dP)²; integrating Lemma 6.2 against P⊗P and Liu's
   criterion with γ = (1−c)/m₀ give c_UC ≥ 1 − m₀. (Same as Thm 1.1.)

Not used by Thm 1.2: Certificate A.3 (the ceiling ĉ) and A.8 (§7).

#### What we re-computed (`computations/frankl/costa_sadhu_thm12.py`, `results/costa_sadhu_thm12.txt`)

- **Exact rationals.**
  - Parameters: τ₀, 1 − m₀ = 0.3828852549667978 exactly, and
    2m₀(1 − 1/8·10⁸) > 1.
  - Lemma 6.1: the derivative formulas, the identity, g′ and its −1/8 bound,
    and g(45/64) − ½.
  - The W₀-monotonicity algebra, including 27/256 − z³ + z⁴ =
    (z − ¾)²(z² + z/2 + 3/16).
  - The Case 3 identity 1 − g(z) = 1 − z² − τ₀z²(1−z)².
  - **A.4**: all 16 Bernstein coefficients are positive. Their minimum
    equals the published rational exactly.
- **A.5, with our own tails.** The paper's tails on (0, 0.001] and [8, ∞)
  are "documented in the computational supplement", which we did not use.
  We wrote our own (docstring of `tails_1d`).
  - Small v ≤ 2⁻¹²: v + (v − v²/2)log(1/v) ≤ G(v) ≤ v + v log(1/v)/(1−v),
    and W₀(v) ≥ 2v log(1/2v). The two resulting brackets are monotone in v,
    and at v = 2⁻¹² they are 0.338 and 38.1.
  - Large v ≥ 8: G ≤ v + 1, G(16v) ≥ 16v, and
    W₀ ≥ 2v − τ₀ + 1 − 2e^{−2v}. The bracket is 2.10.
  - Middle [2⁻¹², 8]: endpoint evaluation, with G′ > 0 and (√W₀)′ > 0
    certified on each cell.
    - W₀ ≥ (8/5)G: 451 cells, minimum lower bound 7.9·10⁻⁶. The true minimum
      ratio is 1.6121, at v ≈ 0.257.
    - G(16v) ≥ (178/25)G: 373 cells, minimum 2.0·10⁻⁴. The true minimum
      ratio is 7.1411, at v ≈ 0.132.
  - The three scalars lie in [2.89081907767·10⁻⁶, 2.89081907856·10⁻⁶],
    [0.405361570566, 0.405361570567] and [0.242130073052, 0.242130073053].
    Each is ≥ the published bound.
- **A.6, with our own rectangle** Q₁ = [5/16, 7/16] × [−1/16, 1/16]. The
  paper's rectangle is |t − t_c| ≤ 1/20, |d| ≤ 1/20.
  - Hessian PD on 1036 boxes: F_tt ≥ 0.0625, F_dd ≥ 0.414,
    det ≥ 1.4·10⁻⁴ (for m₀F₀).
  - m₀F₀(t_c, t_c) ∈ [7.02671277·10⁻⁹, 7.02674996·10⁻⁹], i.e.
    **F₀(t_c,t_c) ≥ 1.13864·10⁻⁸** (paper: ≥ 1.1386421·10⁻⁸).
  - |∂_t| ≤ 4.4·10⁻¹⁴ there. Hence F₀ ≥ 1.13864·10⁻⁸ on Q₁.
  - This is the **thinnest margin resolved by computation**. Our double
    enclosure has width 4·10⁻¹⁴. An independent mpmath.iv evaluation at
    200 bits agrees to 10⁻¹³ (`test_frankl.py`).
  - Negative control: lowering α₀ by 10⁻⁸ makes the certified enclosure of
    F₀(t_c,t_c) negative.
- **A.7, with our own dyadic cover.** t-regions [2⁻¹¹, 1/8], [1/8, 5/16],
  [5/16, 7/16], [7/16, 3/2], [3/2, 4] and [4, 17]; ξ ∈ [0, 15/17], with the
  clip at 15/17 rounded upward.

  | t-region | mean-value boxes | boxes in Q₁ | min lower bound of m₀F₀ | time |
  | --- | --- | --- | --- | --- |
  | [2⁻¹¹, 1/8] | 1,215 | 0 | 5.3·10⁻⁷ (at t ≈ 2⁻¹¹, ξ ≈ 0.52) | 9 s |
  | [1/8, 5/16] | 1,014 | 0 | 4.6·10⁻⁵ | 8 s |
  | [5/16, 7/16] | 908 | 208 | 2.2·10⁻⁵ | 9 s |
  | [7/16, 3/2] | 1,050 | 0 | 7.8·10⁻⁵ | 8 s |
  | [3/2, 4] | 960 | 0 | 0.108 | 6 s |
  | [4, 17] | 10,176 | 0 | 1.2·10⁻³ | 64 s |

  In total, 15,323 boxes certified positive and none unresolved. The paper
  reports 666 cells with minimum 5.2·10⁻⁸. Our cover is finer because our
  derivative enclosures are cruder.
- **Numerics needed for large t.** At t up to 17, e^{−2t} ≈ 10⁻¹⁵, and the
  naive (1−x)log(1−x) loses all relative accuracy. The new module evaluates
  G = u + (1−x)S(x), G′ = S(x), G″ = S(x) − 1/(1−x), with
  S(x) = −log(1−x)/x, and H(p) = p(log(1/p) + (1−p)S(p)) for p ≤ ¼. For
  x ≤ ¼, S is the series Σx^k/(k+1) with a geometric tail bound. All of
  this is checked against mpmath at 120 digits for u up to 128.
- **Tests.** `test_frankl.py::test_costa_sadhu_thm12` runs the exact
  pieces, A.5 and A.6, the 200-bit mpmath.iv contact value, and the
  derivative formulas against 40-digit finite differences. It also runs two
  negative controls: the α₀ − 10⁻⁸ contact value, and the false W₀ ≥ 1.62 G,
  which the 1D prover rejects.

**Label: c_UC ≥ 0.3828852549667978 (Costa–Sadhu Thm 1.2): all finite
computations re-verified independently (own interval code, own tails, own
local rectangle, own cover); analytic steps read, not machine-checked.**

- Read but not machine-checked: Lemma 6.1's case analysis (with Lemmas 4.1
  and 4.4), the W₀-monotonicity argument, Cases 1–3 of Lemma 6.2 and the
  reduction to the compact region, Prop. 6.3, Lemma 2.1, and Liu's Prop. 3
  (read only as Costa–Sadhu restate it).
- We found no error. One presentational point: the tails of A.5 live only
  in the Zenodo supplement, not in the paper. We supplied our own.

### 5. Jiang's 0.38288525 (arXiv:2609.08291): proof map, not yet re-verified

Source: arXiv v1 LaTeX, §§2–8 and Appendices A–B **[read]**. Parameters are
exact rationals: m = 2468459/4·10⁶ (so 1 − m = 1531541/4·10⁶), w₀ = 0.8102221,
w₄ = 0.1897779, A = 0.716, B = 0.721, z = 181/256, σ = 0.99999999, and a
rational centre x* = 0.690908. Exactly, k₀ = mw₀ = 20000000347439/4·10¹³,
so k₀ − ½ = 8.69·10⁻⁹.

- **Reduction** (Prop. "Entropy reduction", analytic). The kernel is
  K(x,y) = h(xy + a(x)a(y)(min(x,y) − xy)). This is Liu's Example 4, a
  shared-uniform rule, with a = 1 on [0, ½], a = √((1−2x²)/(2x(1−x))) on
  (½, 1/√2), and a = 0 above. If (K) K ≥ ψ(x)ψ(y) and
  (M) 2m[w₀h(xy) + w₄ψ(x)ψ(y)] ≥ xh(y) + yh(x), then p ≥ 1 − m. The proof
  is self-contained: it uses conditional independence given the shared
  history, not Liu's C₃ closure.
- **Profile.** ψ is explicit and piecewise: φ = σ√(D h/h(x*)) e^{E} below A,
  s = √h(x²) above B, and a linear blend on [A, B]. Here D is piecewise
  (h, then ln 2, then a scaled h(x²)), and E is quadratic.
- **Finite computations.** These are Python `decimal` at 35 digits with
  outward rounding (code in Appendix B).
  1. Twelve scalar signs, among them E′(1) > 0, C_gC_t < 1, 2C_bP₀ < 1,
     A − s(A)C_b > 0, s(A) > φ(A), k₀ > ½, the small-t bracket
     2mw₄(1 − ln 4T) − 1 > 0 at T = 0.001, e^{−2T} > B, and 16mw₄C² > ½.
  2. The **bridge** h(Ay) ≥ s(A)φ(y) on [1/16, A]: a 1D mean-value cover.
  3. The **kernel** K ≥ φ(x)φ(y) on [1/16, 15/16]²: six parameter squares
     built from three coordinate maps. The middle map, through t = a(x),
     avoids the √ singularity of a at 1/√2.
  4. The **mixture** F(t,ξ) = mw₀G(2t) + mw₄P(u)P(v) − (G(u)+G(v))/2 > 0 on
     [0.001, 16] × [0, 1]: nine t-strips and a mean-value cover. Near ξ = 1
     (v → 0) it uses two analytic edge bounds instead of derivatives,
     (edge1) F ≥ (k₀−½)G(2t) − ½G(v), and (edge2) F ≥ (k₀−½)G(2t) when
     v ≤ −ln B and G(v) ≤ [2mw₄C·G(t)]².
- **Analytic pieces.** The ceiling (Prop. "Limitation"); geometric
  concavity h(xy) ≥ s(x)s(y); profile ordering φ ≤ ψ ≤ s on [A, 1]; the
  lower and upper strips of (K); small t ≤ 0.001 and large t ≥ 16 for (M).
- **Differences from Costa–Sadhu.**
  - Kernel: Liu's Example 4 instead of Example 5.
  - Lemma (K): checked by a 2D interval cover here. In Costa–Sadhu it is
    analytic plus an exact Bernstein certificate.
  - y → 1 edge: Jiang's mixture function **does** touch the
    k₀ − ½ = 8.7·10⁻⁹ margin. It is handled by the analytic edge bounds
    inside the cover. Costa–Sadhu stay away from it via their Case 1.
  - Arithmetic: Decimal instead of MPFR.
  - Jiang also has an analytic finite-N global-coupling gain, which tends
    to 0.

Status: **map only.** None of Jiang's finite computations has been re-run
or re-implemented here yet.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| φ H(x²) ≥ x H(x) on [0,1], φ = (√5−1)/2, equality only at 0, φ, 1 (AHS Claim 1, Boppana) | certificate-checked (own outward-rounded interval arithmetic + analytic end/tangency lemmas) | `computations/frankl/verify_boppana.py` |
| c_UC ≥ (3−√5)/2 | proved (AHS) given the line above; the reduction is AHS's, read and not formalised | AHS arXiv:2211.11731 |
| Frankl holds for every union-closed family on a universe of ≤ 6 elements | computationally checked (exhaustive, n ≤ 6) — already known up to 12 | `computations/frankl/frankl_enum.c`, `results/small_cases.txt` |
| Labeled counts 2, 7, 61, 2480, 1385552, 75973751474 (and the universe-[n] counts) | computed; they equal Brinkmann–Deklerck | same |
| Costa–Sadhu Lemma S (2D inequality at Liu's parameter), Lemma R's Bernstein certificate, all constants | certificate-checked independently (own interval code, own cover) | `computations/frankl/costa_sadhu_checks.py`, `results/costa_sadhu_thm11.txt` |
| c_UC ≥ c_L = 0.3827090879187350… | proved in Costa–Sadhu (preprint); analytic steps read here, all computations re-certified here | same + arXiv:2610.02295 |
| Costa–Sadhu Lemma 6.1 Bernstein certificate (A.4), 1D inequalities (A.5), contact convexity (A.6, F₀ ≥ 1.1386·10⁻⁸), compact cover (A.7) at ℓ₀ = 1409/2000 | certificate-checked independently (own interval code, own tails, own rectangle, own cover of 15,323 boxes) | `computations/frankl/costa_sadhu_thm12.py`, `results/costa_sadhu_thm12.txt` |
| c_UC ≥ 0.3828852549667978 (Costa–Sadhu Thm 1.2) | proved in Costa–Sadhu (preprint); analytic steps read here, all computations re-certified here | same + arXiv:2610.02295 |
| c_UC ≥ 0.38288525 (Jiang) | claimed, computer-assisted preprint; **not** re-verified here | arXiv:2609.08291 |

## Failed or closed routes (do not retry blindly)

- **Pushing the pointwise entropy inequality past 0.38288526.** This is
  impossible: there is a proved ceiling C* (Jiang Prop. "Limitation"; Costa–Sadhu
  §7). Mixing in more product kernels ψ_j(x)ψ_j(y) does not help either (same
  endpoint plus diagonal argument).
- **Gilmer's Conjecture 1** (it would give 1/2) is false (Sawin; Ellis).
- **iid-only arguments** cannot beat (3−√5)/2, even in principle. That bound
  is sharp for approximately union-closed families (Chase–Lovett).
- **Plain enumeration** stops at n = 6. n = 7 means about 2·10¹⁶
  representative pairs.
- Optional item not done: a numerical survey of a "conjectured better"
  inequality. Every published variant with a closed-form optimum is already
  pinned by the ceilings above, so a grid test would be redundant.

## Next steps

Realistic for the next session (bounded, about 3 hours):

1. **Re-verify Jiang's independent 0.38288525 (arXiv:2609.08291).** Costa–Sadhu
   Thm 1.2 is done (Approach 4). Jiang's construction is different (map:
   Approach 5), so this would check a second, independent record proof. Its
   thin spot is the ξ → 1 edge, where mw₀ − 1/2 = 8.7·10⁻⁹ and an analytic
   edge bound is used inside the cover. Start with the 12 scalar signs and the
   1D bridge, then the mixture cover, then the 6-square kernel cover.
2. **Lean.**
   - Ho (arXiv:2601.19327) already formalised Boppana's inequality in Lean 4.
   - Mathlib-adjacent projects (PFR) have Shannon entropy.
   - So formalising Gilmer + AHS, i.e. c_UC ≥ (3−√5)/2 in Lean, is a concrete
     and *genuinely new* artefact. First check that nobody has done it (search
     Zulip/GitHub).
   - It is a multi-session project; the first step is a Lean statement plus
     the two-point reduction (AHS Lemmas 2.1–3.1).

Genuinely new, but not realistic in one session:

3. **n = 13.**
   - It needs FC-family pruning (Poonen weights, as in Živković–Vučković).
   - A useful intermediate step is n = 7 by Poonen-style pruning, as a
     pipeline test. Then, step by step, n = 8.
4. **Beating 0.38289.**
   - This needs an entropy inequality that is *not* pointwise in one
     coordinate. Candidates: kernels with no product lower bound, block
     (several-coordinate) chain rules, or Jiang's global coupling made uniform
     in |F|.
   - No concrete candidate has been identified yet. Any claim here must come
     with a checkable certificate.
