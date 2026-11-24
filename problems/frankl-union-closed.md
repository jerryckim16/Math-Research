# Frankl's union-closed sets conjecture

**Area:** extremal combinatorics / information theory
**Status:** in progress. Literature pinned down from primary sources. The
one-variable inequality behind the (3−√5)/2 bound is **certificate-checked**
here with self-contained interval arithmetic. **Every finite computation** in
Costa–Sadhu's proofs of c_UC ≥ c_L ≈ 0.3827091 (their Thm 1.1) and of the
record c_UC ≥ 0.3828852549667978 (their Thm 1.2), and in Jiang's independent
proof of c_UC ≥ 0.38288525, is **independently re-certified**. The analytic
glue of Thm 1.2 (Lemmas 4.1, 4.4, 6.1, W₀ monotonicity, Lemma 6.2 Cases 1–3
and the residual region) is now **machine-checked** with sympy (exact) + z3 +
interval arithmetic, up to listed standard hand steps (Approach 6; no Lean:
the Mathlib cache is unreachable from here). Its measure-theoretic part
(Prop. 6.3's integration, Lemma 2.1's limit, Liu's Prop. 3) is read only.
Liu's Prop. 3 has now been read in Liu's own text. Jiang's analytic glue
(reduction, Lemma "geometric", profile order, kernel strips, coordinate maps,
small-t/large-t tails, edge bounds, App. A derivative formulas) is likewise
**machine-checked** (Approach 7), up to named hand steps; only its
probability layer (chain rule, conditioning, conditional independence) is
read only. No gap was found in either proof. The conjecture is **checked
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
| **0.38288525 = 1531541/4000000** | Jiang, arXiv:2609.08291 (8 Sep 2026) | preprint; computer-assisted (interval code in the appendix). **All finite computations re-verified here** (Approach 5); **analytic glue machine-checked** (Approach 7) | [read] §§1–8, App. A–B |
| **0.3828852549667978** | Costa–Sadhu, arXiv:2610.02295 Thm 1.2 (1 Oct 2026). **This is the ProofAtlas "Oct 2026" claim.** | preprint, not refereed; computer-assisted (Zenodo supplement). **All finite computations re-verified here** (Approach 4) | [read] §6, App. A |

Current best *claimed* constant: **0.3828852549667978** (Costa–Sadhu,
unrefereed). Every finite computation of its proof, and of Jiang's
0.38288525, is independently re-verified here. The analytic glue of both
proofs is machine-checked (sympy/z3/interval/Arb, Approaches 6–7) up to named
hand steps and a read-only probability/measure-theory layer. The best constant in a refereed journal is (3−√5)/2 (AHS, EJC
2024). Cambie's 0.3823455 is in an arXiv v2 (2025); whether it was refereed
was not checked. Two independent groups give near-identical values
(0.38288525 and 0.38288525497), and both bounds sit within 10⁻⁸ of the same
proved ceiling (next section). That agreement is decent evidence that the
numerics are right, but it is not a referee check. We have since re-run every
finite computation of both proofs with our own code (Approaches 4–5), and
machine-checked their analytic glue (Approaches 6–7). That is still not a
referee check: the hand steps and the probability layer were read, and
nothing is Lean-verified.

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
  - Liu's Prop. 3. This was read only as Costa–Sadhu restate it. It has
    since been read in Liu's own text and the restatement is faithful
    (Approach 6).

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

- Read but not machine-checked *at the time of Approach 4*: Lemma 6.1's case
  analysis (with Lemmas 4.1 and 4.4), the W₀-monotonicity argument, Cases 1–3
  of Lemma 6.2 and the reduction to the compact region, Prop. 6.3, Lemma 2.1,
  and Liu's Prop. 3 (read only as Costa–Sadhu restate it). **All but the last
  three are now machine-checked in Approach 6. Liu's Prop. 3 has been read
  in Liu's own text (Approach 6).**
- We found no error. One presentational point: the tails of A.5 live only
  in the Zenodo supplement, not in the paper. We supplied our own.

### 5. Independent re-verification of Jiang's 0.38288525 (arXiv:2609.08291)

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

#### What we re-computed (`computations/frankl/jiang_checks.py`, `results/jiang.txt`)

All of this is our own code: outward-rounded doubles, with the accurate
G/H evaluation from Approach 4. It is not Jiang's Decimal program. Every
rational parameter is entered exactly.

- **Exact rationals.**
  - w₀ + w₄ = 1 and 1 − m = 1531541/4·10⁶.
  - k₀ − ½ = 347439/4·10¹³.
  - 1/2 < z < 1/√2 < A (as 2z² < 1 < 2A²), and z² + z > 1.
- **The 12 scalar signs.** All are positive. The smallest is
  k₀ − ½ ∈ [8.685974939·10⁻⁹, 8.68597505·10⁻⁹]. The next smallest are
  s(A) − φ(A) ≥ 1.63·10⁻³ and 1 − 2C_bP₀ ≥ 0.0271.
- **Bridge** on [1/16, A]: 68 cells, minimum lower bound 4.6·10⁻⁶.
- **Kernel** on [1/16, 15/16]², using our own implementation of the three
  coordinate maps (x(p) = 1/(p² + √((p²−1)² + 1)), so that a(x(p)) = p).
  The proven range xy ≤ r ≤ min(x,y) is intersected in.

  | maps | boxes | min lower bound | time |
  | --- | --- | --- | --- |
  | (low, low) | 64 | 0.022 | 0.3 s |
  | (low, mid) | 64 | 1.0·10⁻⁴ | 0.4 s |
  | (low, high) | 64 | 3.3·10⁻³ | 0.4 s |
  | (mid, mid) | 897 | 1.4·10⁻¹⁰ (at x ≈ y ≈ x*) | 10 s |
  | (mid, high) | 147 | 5.3·10⁻⁷ | 1.6 s |
  | (high, high) | 70 | 1.2·10⁻⁴ | 0.4 s |

  The true kernel gap at (x*, x*) is exactly ln 2·(1 − σ²) = 1.386·10⁻⁸,
  because r(x,x) = ½ on [½, 1/√2] and φ(x*)² = σ² ln 2. Our enclosure is
  [1.38629304·10⁻⁸, 1.38629528·10⁻⁸]. Negative control: raising σ by a
  factor 1 + 2·10⁻⁸ gives a certified negative gap there.
- **Mixture** on [0.001, 16] × [0, 1]: nine t-strips; the edge bounds
  (edge1, edge2) are used next to ξ = 1.

  | t-strip | boxes (by edge bound) | min lower bound | time |
  | --- | --- | --- | --- |
  | [0.001, 0.01] | 169 (23) | 1.3·10⁻¹⁰ (edge2) | 1.6 s |
  | [0.01, 0.1] | 178 (21) | 8.6·10⁻¹⁰ (edge2) | 2.0 s |
  | [0.1, 0.3] | 229 (10) | 5.0·10⁻⁹ (edge2) | 3.6 s |
  | [0.3, 0.5] | 3,051 (4) | **1.8·10⁻¹¹** (mean value, t ≈ 0.3705, ξ ≈ 4·10⁻⁴) | 57 s |
  | [0.5, 1] | 359 (3) | 1.6·10⁻⁸ | 6.4 s |
  | [1, 2] | 181 (4) | 2.5·10⁻⁸ | 2.8 s |
  | [2, 4] | 82 (3) | 4.3·10⁻⁸ | 0.9 s |
  | [4, 8] | 55 (3) | 7.8·10⁻⁸ | 0.6 s |
  | [8, 16] | 53 (2) | 1.5·10⁻⁷ | 0.5 s |

  - **Two thin spots, both resolved.**
    - The diagonal near x*: F(−log x*, 0) ≈ 1.105·10⁻⁸, reflecting
      C* − c₀ ≈ 10⁻⁸. Our point enclosures there have width ≈ 4·10⁻¹⁴,
      and the weakest mean-value box still clears zero by 1.8·10⁻¹¹, about
      400 times the rounding width.
    - The ξ → 1 edge, where the edge bounds certify (k₀ − ½)G(2t), down to
      1.3·10⁻¹⁰.
  - Negative control: lowering k₀ by 2·10⁻⁸ makes the certified value at
    the diagonal point negative.
- **Tests.** `test_frankl.py::test_jiang` checks the kernel gap, its two
  partial derivatives, P, P′ and the mixture value and derivatives against
  40-digit mpmath models of Jiang's definitions, written separately from
  `jiang_checks.py`.

**Label: c_UC ≥ 0.38288525 (Jiang): all finite computations re-verified
independently (own interval code and own covers, same decomposition of the
domain); analytic steps read, not machine-checked.** *(Superseded: the
analytic steps are now machine-checked in Approach 7.)*

- Read but not machine-checked *at the time of Approach 5*: the reduction, geometric concavity, profile
  ordering, the lower/upper strips, small t ≤ 0.001, large t ≥ 16, and the
  two edge estimates.
- We reused Jiang's *decomposition* (the strip/square split, the coordinate
  maps and the edge bounds), but none of his code.
- We found no error. Neither record bound has been refereed. The two
  constructions are genuinely different (Liu's Example 5 vs Example 4), and
  both are now checked.

### 6. Machine-checking the analytic glue of Costa–Sadhu Thm 1.2

Goal: check by machine as much as practical of the steps of Approach 4 that
were only read: Lemma 6.2 Cases 1–3 and the residual region, Lemmas 4.1 and
4.4, Lemma 6.1's case analysis, W₀ monotonicity, Prop. 6.3. Source:
arXiv:2610.02295 v1 LaTeX, §§2, 4, 6 **[read]**.

- **Tooling.**
  - **Lean: not available here.** The elan installer downloads, but
    `elan toolchain install` fails: the proxy refuses `releases.lean-lang.org`
    (HTTP 403 on CONNECT). GitHub release assets are reachable, so a bare Lean
    binary could be fetched by hand. But both Mathlib cache hosts
    (`lakecache.blob.core.windows.net`, `cache.lean-lang.org`) are refused too,
    and building Mathlib from source takes hours. We stopped there (about 5
    minutes spent) and did not retry.
  - **Used instead:**
    - sympy 1.14 for exact identities, derivatives and Sturm sequences;
    - the z3 SMT solver for the case-analysis skeletons;
    - python-flint/Arb (200-bit balls) as a second evaluation of the one
      transcendental scalar;
    - our own `interval.py`.

    The first three are pip-installed (`pip install sympy z3-solver
    python-flint`). The sympy install downgraded mpmath from 1.4.1 to 1.3.0,
    and the existing tests still pass.
- **Labels used below.**
  - **sympy-exact.** The identity reduces to 0 in exact rational-function
    arithmetic (`sympy.cancel`). Every log(·) atom is first replaced by an
    independent symbol, so nothing transcendental is left to sympy's
    heuristics, and an identity that holds with the logs as free symbols holds
    a fortiori.
  - **sturm.** An exact Sturm root count over Q.
  - **z3.** The negated implication is unsat over the reals (nonlinear real
    arithmetic, exact rationals). The hypotheses fed to z3 are exactly the
    facts proved by the other checks. Since Approach 7, z3 first shows the
    hypotheses satisfiable (non-vacuity guard). All of this approach's
    calls pass it.
  - **interval.** `interval.py`.
  - **hand.** A standard analysis fact that we state but do not formalise:
    Taylor bounds with positive terms; "f(0) = 0 and f′ > 0 ⇒ f > 0" (MVT);
    FTC/Tonelli; Jensen; weak limits; continuity at the boundary.
- **Code.** `computations/frankl/analytic_glue.py`, output in
  `results/analytic_glue.txt`: 26 claims, 15 s. Test:
  `test_frankl.py::test_analytic_glue`. It runs all claims plus negative
  controls showing each tool can fail:
  - a false log identity (G′ = S + x) is rejected;
  - a Sturm count with roots present is correct;
  - z3 refuses four false variants, namely Case 1 with 7.11 in place of
    178/25, Case 3 with 6 log 2 in place of 8 log 2, ξ < 14/17 in place of
    15/17, and the residual region without "not Case 3".

Notation as in Approach 4. In addition, S(x) := −log(1−x)/x, x = e^{−u}.

#### G facts (used by 4.4 and 6.2) — closed form instead of the paper's series

- **Statement.** G(u) = u + (1−x)S(x), G′(u) = S(x), G″(u) = S(x) − 1/(1−x).
  On (0, ∞): G′ > 1, G″ < 0, G(u) − u < 1, −G″(u) < 1/(e^u−1) < 1/u, and
  G(0+) = 0.
- **Reduction.**
  - The three formulas are derivatives of H(x)/x under d/du = −x d/dx
    (sympy-exact). sympy also sums Σx^k/(k(k+1)) = 1 + (1−x)log(1−x)/x, so
    the closed form agrees with the paper's series (Lemma 5.2).
  - S > 1 because f = −log(1−x) − x has f(0) = 0 and f′ = x/(1−x) > 0.
  - ψ(x) := x + (1−x)log(1−x) has ψ(0) = 0 and ψ′ = −log(1−x) > 0. The
    identities G″ = −ψ/(x(1−x)), G − u = 1 − ψ/x and
    −G″ − x/(1−x) = 1 − S (sympy-exact) then give the three signs.
- **Label:** sympy-exact + hand (MVT, twice).

#### Lemma 4.1: −Λ″/Λ′ > 1/u + 1/(1−u) on (0, ½), Λ = log H

- **Reduction.**
  - (a) −Λ″/Λ′ − 1/u − 1/(1−u) = N/(u(1−u)λH), where
    N = q(1−λ) + uλ(1−uλ), λ = log((1−u)/u), q = −log(1−u), H = uλ + q and
    H′ = λ (sympy-exact). The denominator is > 0 because λ > 0 on (0, ½).
  - (b) q ≤ u/(1−u): f = u/(1−u) + log(1−u) has f(0) = 0 and
    f′ = u/(1−u)² (sympy + MVT).
  - (c) The algebra (u/(1−u))(1−λ) + uλ(1−uλ) =
    (u/(1−u))(1 − uλ(λ+1) + u²λ²) (sympy-exact). Also u = 1/(1+e^λ).
  - (d) 1 − λ²/2 + λ³/6 > 0 on [1, ∞): no root by an exact Sturm count;
    the minimum is 1/3 at λ = 2. With the Taylor bound
    e^λ > 1 + λ + λ²/2 + λ³/6 (hand) this gives uλ(λ+1) < e^{−λ}λ(λ+1) < 1.
  - (e) N > 0 in both cases, λ ≤ 1 and λ > 1: z3, from (b) and (d).
- **Cross-check** (not needed for the proof): N(u)/u > 0 on [2⁻⁴⁰, ½] by 624
  interval cells; the minimum lower bound is 0.42.
- **Label: machine-checked** (sympy-exact + Sturm + z3), with two hand steps
  (a Taylor bound and one MVT).

#### Lemma 4.4: M = uH′/H is strictly decreasing on (0, 1)

- **Reduction.**
  - With H an abstract function, d/dv log H(e^{−v}) = −M(e^{−v}) and
    d²/dv² log H(e^{−v}) = e^{−v}M′(e^{−v}) (sympy-exact).
  - log H(e^{−v}) = −v + log G(v), and
    (log G)″ = G″/G − (G′/G)² < 0 by G″ < 0 and G > 0.
  - Hence M′ < 0 pointwise.
- **Wording point, not a gap.** The paper says "strict concavity makes this
  quantity negative". Strict concavity alone does not give a negative second
  derivative everywhere (think of −x⁴ at 0). But the paper's previous display
  already proves (log G)″ < 0 pointwise, which is what is used.
- **Cross-check:** the numerator K = (λ − 1/(1−u))H − uλ² of M′ = K/H² is
  < 0 on [2⁻⁴⁰, 1 − 2⁻⁴⁰] (11,493 interval cells).
- **Label: machine-checked** (sympy-exact), with G facts as above.

#### Lemma 6.1: H(r(x,y))² ≥ H(g(x))H(g(y)) — the case analysis

- **Reduction.**
  - (a) r_x, r_y, r_xy, the identity W r_xy − r_x r_y/(xy) = τ₀xy, and
    r_xy/(r_x r_y) = 1/r + τ₀/(WUV), where r_x = yU and r_y = xV
    (sympy-exact).
  - (b) On [0,1]²: W ≥ 1 and U, V ≥ 1 − τ₀ > 0 (z3). Also
    g′ ≥ 2x(1 − τ₀/8) via (1−x)(1−2x) + 1/8 = 2(x − ¾)², the exact value of
    g(45/64) − ½, g ≥ z², and g(1) = 1.
  - (c) **A.4 by a second method.** We solve the 16×16 monomial linear
    system for the Bernstein coefficients, instead of using the
    degree-elevation formula of Approach 4. All 16 are > 0, and the minimum is
    the published rational.
  - (d) With Λ and H abstract: ∂_yΔ_x = L₂(x,y) − L₂(y,y);
    L₁₂ = Λ″(r)r_x r_y + Λ′(r)r_xy; L₂ = (r_y/r)M(r) with
    r_y/r = 1/y − τ₀(1−x)/(1+τ₀(1−x)(1−y)); and
    a ↦ τ₀a/(1+τ₀a(1−y)) has derivative τ₀/(1+τ₀a(1−y))² > 0. All
    sympy-exact.
  - (e) **Case logic** (z3).
    - Case A: P(ρ + ℓ) < 0 from P > 0, ρ ≤ 1/r + 1/(1−r) and
      ℓ < −1/r − 1/(1−r). These hypotheses come from (a), A.4 and Lemma 4.1;
      the last applies because 0 < r(s,y) ≤ g(y) < ½.
    - Case B: A_x M(r) > A_y M(g) from 0 < A_x < A_y, M > 0 below ½,
      M ≤ 0 above ½, and M decreasing.
  - Hand steps: Δ_x(x) = 0 plus the FTC in s and in y, and continuity at the
    boundary.
- **Label: machine-checked**, except the FTC and continuity steps.

#### W₀ is increasing

- **Reduction.**
  - With H abstract, W₀′(v) = (2H(q) − z q_z H′(q))/z², where q = g(z) and
    z = e^{−v}.
  - z q_z = 2q − 2τ₀z³(1−z) and H(q) − qH′(q) = −log(1−q). Hence
    z²W₀′ = −2log(1−q) + 2τ₀z³(1−z)H′(q).
  - H′(q) − log(1−q) = −log q.

  All of these are sympy-exact. Then:
  - z³(1−z) ≤ 27/256, by the exact factorisation in Approach 4, so
    c := 2τ₀z³(1−z) < 2.
  - The sign skeleton is checked by z3: with A = −log(1−q) > 0,
    H′ ≥ 0 for q ≤ ½ and H′ ≥ −A for q > ½, we get 2A + cH′ > 0.
- **Label: machine-checked.** The interval check of (√W₀)′ > 0 on
  [2⁻¹², 8] in Approach 4 is an independent confirmation there.

#### Lemma 6.2: F₀(s,σ) > 0 for 0 < s ≤ σ

- **(a) Reduction** (sympy-exact):
  - Divide (6.tuned-second) by 2xy, with logs of x, y, 1−x, 1−y and 1−xy as
    free symbols. This gives F₀ = α₀G(s+σ) − (G(s)+G(σ))/(2m₀) + β₀P with
    P = √(W₀(s)W₀(σ)).
  - Then F₀ = G(u)/8·10⁸ − D/(2m₀) + β₀P.
- **(b)** D ≤ G(s) − s < G(s) and D < 1 (z3 skeleton). The inputs are
  G(s+σ) − G(σ) ≥ s (MVT with G′ > 1) and G(s) − s < 1. *Our route differs
  from the paper's*, which compares series term by term. Both are valid.
- **(c) Case 1, G(σ) ≥ (178/25)G(s).** This is the y → 1 (s → 0) edge.
  - **Exact certificate** (sympy-exact):
    F₀ − [G(u)/8·10⁸ + c₁G(s)] = (G(s) − D)/(2m₀) + β₀(P − (8/5)Q)
    + (8β₀/5)(Q − kG(s)), where Q = √(G(s)G(σ)) and k = √178/5. Each bracket
    is ≥ 0 by (b) and A.5; the first is > 0.
  - **The margin c₁ = (8β₀/5)k − 1/(2m₀) > 0 is now proved in exact rational
    arithmetic.** We show (8β₀√178/25)² > (1/(2m₀))², and, with a rational
    lower bound for √178, c₁ ≥ 2.89081907812·10⁻⁶ (paper: ≥ 2.8908190756·10⁻⁶).
    Before this session it was an interval enclosure.
  - z3 also proves the whole implication without square roots, using
    P² ≥ (64/25)(178/25)G(s)².
  - The 7.7·10⁻¹⁰ margin m₀α₀ − ½ = m₀/8·10⁸ is never needed: the
    G(u)/8·10⁸ term is only dropped (it is > 0).
- **(d) Case 2, s, σ ≥ 2.**
  - Certificate: F₀ − [G(u)/8·10⁸ + (β₀W₀(2) − 1/(2m₀))]
    = (1−D)/(2m₀) + β₀(P − W₀(2)) (sympy-exact). P ≥ W₀(2) because W₀ is
    increasing.
  - The scalar β₀W₀(2) − 1/(2m₀) ≥ 0.4053615705664 is transcendental. It is
    interval-verified (`interval.py`), and independently by Arb at 200 bits;
    the two agree to 10⁻¹².
  - z3 skeleton.
- **(e) Case 3, s, σ ≤ 2⁻¹⁰.**
  - sympy evaluates ∫₀^s∫₀^σ db da/(a+b) = (s+σ)log(s+σ) − s log s − σ log σ
    = uH(λ) (exact, logs as symbols). The mixed derivative of
    G(a) + G(b) − G(a+b) is −G″(a+b).
  - The rest is identities (sympy-exact): e^{2w}(1 − g(e^{−w})) =
    e^{2w} − 1 − τ₀(1−e^{−w})² (an identity in z = e^{−w}),
    √(sσ) = u√(λ(1−λ)), and A + B − 1 − AB = −(1−A)(1−B) (for
    H(λ) ≤ 2√(λ(1−λ))).
  - z3 skeletons: e^{2w}r_w ≥ 2w, from e^{2w} ≥ 1 + 2w + 2w² and
    0 ≤ 1 − e^{−w} ≤ w; and the final step, from D < uH(λ), H(λ) ≤ 2R,
    P ≥ 2uR log(1/2u) and log(1/2u) ≥ 8 log 2.
  - The final certificate F₀ − [G(u)/8·10⁸ + 2uR(β₀ log(1/2u) − 1/(2m₀))] =
    (uH − D)/(2m₀) + β₀(P − 2uR log(1/2u)) + u(2R − H)/(2m₀) is sympy-exact.
  - **The scalar 8β₀ log 2 − 1/(2m₀) ≥ 0.2421300730523 is now proved
    exactly.** It uses the rational lower bound for log 2 from the atanh
    series, which Arb confirms lies below log 2.
  - Hand steps:
    - the FTC/Tonelli representation D = −∫∫G″. It is improper at 0, since
      G′(v) ~ log(1/v), but valid because G is continuous at 0 with G(0) = 0
      and G′ is integrable there;
    - log t ≤ t − 1;
    - e^t ≥ 1 + t + t²/2.

    A cross-check of H(λ) ≤ 2√(λ(1−λ)) on [1/4096, ½] in 2047 interval cells
    gives a minimum gap of 0.027.
- **(f) Residual region** (z3). From 0 < s ≤ σ, not Case 1, not Case 2, not
  Case 3, A.5 at v = s (G(16s) ≥ (178/25)G(s)) and G increasing, z3 derives
  2⁻¹¹ < t < 17 and ξ < 15/17. The bound on ξ is stated as
  17(σ−s) < 15(σ+s). It also derives the paper's intermediate bounds
  2⁻¹⁴ < s < 2 and 2⁻¹⁰ < σ < 32. That region is covered by A.6 + A.7
  (Approach 4, our own rectangle and cover).
- **Label: machine-checked**, given A.5–A.7 (certificate-checked in
  Approach 4), with the hand steps listed in (b) and (e). Symmetry and
  boundary continuity are also hand steps.

#### Prop. 6.3 and the theorem

- **Checked** (exact rationals + z3): α₀ + β₀ = 1, 0 < α₀, β₀ < 1,
  2m₀(1 − 1/8·10⁸) > 1, 1 − m₀ = 0.3828852549667978, and γ = (1−c)/m₀ > 1
  for 0 < c < 1 − m₀. Also the finite Jensen identity
  Σλᵢaᵢ² − (Σλᵢaᵢ)² = Σλᵢ(aᵢ − ā)², checked for n = 3, which is Lemma 2.1
  before the weak limit.
- **Sanity test (not a proof).** Prop. 6.3's inequality is certified by
  interval arithmetic on 200 random finitely supported P, with ρ a finite
  mixture of Q⊗Q (so ρ ∈ C₃(P)), and on a point mass at e^{−t_c}.
  Negative control: raising 1/m₀ by 10⁻⁷ makes the point-mass instance
  certifiably negative.
- **Liu's Prop. 3, now read in Liu's own text.** Source: arXiv:2306.08824
  LaTeX, §2 (Def. of protocol, eq. (16), Prop. 3, Def. 2, Examples 4–5,
  the definition of C₃) **[read]**. Costa–Sadhu's restatement is faithful in
  three respects:
  - Weights w_k ≥ 0 sum to 1. There is a fixed C > 1. The condition is
    imposed for every μ with mean ≤ c, and the inf is over sets C_k(μ)
    "large enough to contain all couplings … induced by the k-protocol".
  - The conclusion is "c is a lower bound for the constant".
  - The only difference is the log base: Liu uses bits, Costa–Sadhu use
    nats. Both sides of (16) scale by the same factor, so nothing changes.

  Liu's proof is four lines: the chain rule as in Gilmer, plus "uniform
  maximises entropy". We read it and it is correct. It needs H(Xⁿ) > 0, i.e.
  |F| ≥ 2, which the definition of c_UC provides.

  Liu's Example 5 is the following protocol: X = 0 with probability
  s̄ ± f(s̄), the sign set by U ≶ ½. Its formula Π_{s,t}(0,0) = s̄t̄ + f(s̄)f(t̄),
  the marginal P(X=0) = s̄, and the specialisation to r_ℓ are sympy-exact.
  Admissibility of f_ℓ for 0 ≤ ℓ ≤ 1 is checked by z3 (claim L.ex5).
- **Read only.** Integration against P⊗P (Fubini); Lemma 2.1's weak limit;
  the reflection argument (C₃ is preserved by x ↦ 1−x); Liu's argument that
  conditionally-iid protocols induce laws in C₃ (X^i, Y^i are conditionally
  iid given U^i). These are measure theory, not computations.

#### Outcome

| step | method | status |
| --- | --- | --- |
| G facts (G′ > 1, G″ < 0, G − u < 1, −G″ < 1/u) | sympy-exact + MVT | machine-checked (MVT by hand) |
| Lemma 4.1 | sympy-exact + Sturm + z3 (+ interval cross-check) | machine-checked (Taylor bound, MVT by hand) |
| Lemma 4.4 | sympy-exact (+ interval cross-check) | machine-checked |
| Lemma 6.1 identities, A.4 (second method), positivity | sympy-exact + z3 | machine-checked |
| Lemma 6.1 case analysis (Cases A, B) | z3 on sympy-checked inputs | machine-checked (FTC, continuity by hand) |
| W₀ increasing | sympy-exact + z3 | machine-checked |
| Lemma 6.2 reduction, D bounds | sympy-exact + z3 | machine-checked (MVT by hand) |
| Lemma 6.2 Case 1 (y → 1 edge) | sympy certificate + **exact** margin c₁ ≥ 2.89·10⁻⁶ + z3 | machine-checked, given A.5 |
| Lemma 6.2 Case 2 | sympy certificate + z3 + interval + Arb | machine-checked, given A.5 |
| Lemma 6.2 Case 3 | sympy (integral, identities) + **exact** scalar + z3 | machine-checked (FTC/Tonelli, two elementary bounds by hand) |
| Lemma 6.2 residual region → A.6/A.7 | z3 | machine-checked |
| Prop. 6.3 arithmetic, γ > 1 | exact + z3 | machine-checked |
| Liu's Prop. 3 vs Costa–Sadhu's restatement; Liu's Example 5 formula | read in Liu's LaTeX; formula sympy-exact + z3 | restatement faithful; formula machine-checked |
| Prop. 6.3 measure theory, Lemma 2.1 limit, C₃ membership of induced laws | — | read only |

Also a **statement-level stress test** (claim 6.x; numerical, not a proof).
In 40-digit mpmath, Lemma 6.1 and Lemma 6.2 were evaluated at 3000 random
points each. s and σ were drawn log-uniformly in [10⁻¹², 60], so every Case
region and the residual region is hit, plus near-diagonal and near-contact
points. The minima are (H(r)² − H(g(x))H(g(y)))/(x−y)² ≥ 9.6·10⁻⁶ and
F₀/G(s+σ) ≥ 7.85·10⁻⁹ (the latter at the contact point).

**No gap or error found.** The only finding is the harmless wording point in
Lemma 4.4. Nothing was Lean-verified.

### 7. Machine-checking the analytic glue of Jiang's 0.38288525

Goal: give the analytic steps of Approach 5, which were read only, the same
treatment as Approach 6. That means every step that the finite computations in
`jiang_checks.py` rely on, or that turns them into the theorem. Source:
arXiv:2609.08291 v1 LaTeX (`frankl_038288525_proof.tex`), §§2–7 and App. A
**[read]**. Equation names below are the paper's `\label`s.

- **Tooling and labels.** As in Approach 6: **sympy-exact**, **z3**,
  **interval**, **Arb**, **exact** (Fraction arithmetic), **hand (named)**,
  and **read only**. Two things are new.
  - `logsub` replaces each log(·) atom by an integer combination of symbols.
    It factors the argument over a *listed* set of bases, and a log of a
    rational constant becomes a combination of log-of-prime symbols. It
    refuses any unlisted factor, so nothing transcendental is left to sympy.
  - Every z3 call first checks that its hypotheses are **satisfiable**
    (z3 returns a model). So no skeleton is proved vacuously from
    inconsistent hypotheses. The guard now lives in
    `analytic_glue.z3_valid`, so Approach 6's 16 z3 calls get it too. All
    16 have satisfiable hypotheses, and all 26 claims still pass.

  Sturm sequences were not needed: no polynomial sign condition comes up.
- **Code.** `computations/frankl/analytic_glue_jiang.py`, output in
  `results/analytic_glue_jiang.txt`: 31 claims, 5 s. Test:
  `test_frankl.py::test_analytic_glue_jiang`. The test runs all claims plus
  negative controls:
  - sympy rejects two false identities: the AND-grouping identity with
    prefactor 1 + x² instead of 1 − x², and h²q′ with the sign of h/(1−x)
    flipped. `logsub` refuses an unlisted log factor.
  - z3 refuses seven weakened skeletons and one vacuous one:
    - lower strip with 2C_bP₀ < 1.01;
    - upper strip with C_tC_g < 1.01;
    - small t with the bracket ≤ 0;
    - large t with t ≥ 8 instead of 16;
    - edge2 without v ≤ −ln B;
    - the mixed case of (K) without the bridge;
    - the reduction with p = min pᵢ instead of max;
    - and the vacuity guard rejects unsatisfiable hypotheses.
  - Arb certifies three scalars **negative** under a changed parameter:
    T = 1/10 in the small-t bracket, 8 in place of 16 at large t, and
    σ raised by 1% in s(A) − φ(A). interval.py also certifies the
    T = 1/10 bracket negative.
  - The reduction-instance test (R.x below) shows that the family
    {∅, {1}} violates the chain at m = 0.55.

#### Reduction (Prop. "Entropy reduction", §3)

- **R.1 (sympy-exact).** With Q_U(x) = x + a(x)(1[U≤x] − x), integrating
  piecewise over U ∈ [0,1] gives E Q_U(x) = x and
  E[Q_U(x)Q_U(y)] = xy + a(x)a(y)(min(x,y) − xy) = r(x,y), in both orders.
  This is eq. (Qproduct).
- **R.2 (z3).** a ∈ [0,1] gives Q_U ∈ [0,1], and xy ≤ r ≤ min(x,y) ≤ 1.
- **R.3 (sympy-exact).** Finite forms of the two averaging steps:
  - the conditional-Jensen step is the variance identity
    Σλ_v c_v² − (Σλ_v c_v)² = Σλ_v(c_v − c̄)²;
  - integrating xh(y) + yh(x) against P ⊗ P gives 2(E x)(E h).
- **R.4 (z3).** The assembly, with three coordinates. The inputs are the
  per-coordinate bounds (ind-lower), (rule4-lower) and (M) integrated; the
  chain rule; H(Z₀), H(Z₄) ≤ ln N = H(X) > 0; and pᵢ ≤ p. The output is
  p ≥ 1 − m. With p = min pᵢ the implication fails (negative control).
- **Read only.** The chain rule; "conditioning reduces entropy"; maximum
  entropy; the induction showing that each sample of the shared-uniform rule
  has the law of X; and conditional independence of the two prefixes given
  the shared history. These are probability, not computation. They are the
  same kind of step as Approach 6's measure-theory layer, and simpler,
  because everything here is finite.
- **R.x (numerical sanity test of that read-only layer; not a proof).** Since
  U_i is fresh, averaging it gives a finite pair kernel at each coordinate:
  P(00) = r(S,T), P(0·) = S, P(·0) = T. So the exact laws of both couplings
  are finite sums.
  - These laws were computed in 30-digit mpmath for 150 random families with
    n ≤ 4 and at most 8 sets (75 arbitrary, 75 union-closed).
  - Per coordinate they satisfy H((Z₀)ᵢ|·) ≥ E h(ST) and
    H((Z₄)ᵢ|·) ≥ E K(S,T) ≥ (E ψ)².
  - Both marginals of the shared rule are uniform on F.
  - w₀H(Z₀) + w₄H(Z₄) ≥ (1−p)H(X)/m. The minimum slack, over families
    with p < 1, is 0.037·ln N.
  - For union-closed F, H(Z₀), H(Z₄) ≤ ln N and p ≥ 1 − m.

#### Ceiling (Prop. "Limitation", §4; not on the proof path of the bound)

- **C.1 (sympy-exact).** The formulas for f′, f″, f‴; the expansion
  f = ½(1−q)²ln(1−q) + ½(1−q²)ln(1+q); f(q*) = ½(1−q*)ln(1+q*) at the
  stationary point; f′(½) = ½ln(4/3); and f″(½) = 2/3 − ln 3.
- **C.2 (z3).** The endpoint step (E): mw₀ ≥ ½. The diagonal chain to (C).
  And f′ > q(1−2q) on (0, ½] from the two log bounds (hand).

#### Profiles (§5): definitions, Lemma "geometric", profile order, passing to (K)

- **P.1 (exact + sympy + z3).** The parameter order
  1/16 < ½ < z < 1/√2 < A < B < 15/16, plus z² + z > 1 and 2U² > 1.
  Continuity of a at ½ and 1/√2, 0 ≤ a ≤ 1, continuity of D at ½ and z,
  and θ(A) = 0, θ(B) = 1. Also E″ = −7/5, so E′(1) > 0 gives E′ > 0 on
  [0,1] (z3). That E is then increasing is a hand step (MVT).
- **G.1–G.3, Lemma "geometric" (sympy-exact + z3).**
  - The identities h − xh′ = ℓ and h²q′ = h′ℓ − h/(1−x) =
    h′(ℓ − x/(1−x)) − ℓ/(1−x), with logs as symbols.
  - ℓ < x/(1−x) (MVT), and the sign skeleton for x ≥ ½ and x < ½ (z3).
  - With h abstract: f(t) = ln h(eᵗ) has f′ = q(eᵗ) and f″ = eᵗq′(eᵗ), and
    d/dx ln(h(xy)/s(x)) = (q(xy) − q(x²))/x.
  - Hand: concavity at the midpoint.
  - Cross-check: h²q′ < 0 on [2⁻¹⁰, 1 − 2⁻³⁰] by 303 interval cells.
- **O.1–O.2, (profile-order) (sympy-exact + z3).**
  - (φ/s)² = σ²ln2·h(x)e^{2E}/(h(z²)h*) on [z, 1].
  - (ln φ/s)′ = h′/(2h) + E′, and its derivative is
    (h″h − h′²)/(2h²) − 7/5 < 0.
  - Then the convex-combination skeleton φ ≤ ψ ≤ s.
  - Hand: "L(A) < 0, L′(A) < 0, L″ < 0 ⇒ L < 0 on [A, 1)" (MVT twice).
  - The two scalars are checked by interval and Arb.
- **T.1, passing to (K) (z3).** All three cases, x, y ≤ A; x, y ≥ A; and
  x ≥ A ≥ y. Inputs: (original-K), Lemma "geometric" (both parts),
  (profile-order) and (bridge), with a = 0 on [A, 1] because 2A² > 1.

#### Kernel strips, coordinate maps, bridge (§6)

- **S.1 (sympy-exact).** The AND inequality h(x²) ≤ 2h(x) is a **grouping
  identity**:
  2h(x) − h(x²) = (1−x²)·H₃((1−x)/(1+x), x/(1+x), x/(1+x)),
  with logs of x, 1−x, 1+x as symbols, which is ≥ 0. For concavity-scaling,
  g(c) = h(cx) − ch(x) has g(0) = g(1) = 0 and g″ = −x/(c(1−cx)) < 0.
  Hand: entropy ≥ 0; a concave function with zero ends is ≥ 0.
- **S.2.** (lower-profile), (P0) and (linear-profile).
  - (ln φ/x)′ = D′/(2D) + h′/(2h) + E′ − 1/x, with D abstract (sympy).
  - On [z, 1/√2], D′/(2D) = xh′(x²)/h(x²) ≤ h′(z²)/h(z²), from
    (h′/h)′ < 0 and 2z² < 1.
  - The derivative is then < 0 on all three pieces, given the scalar
    1 − E′(½) − h′(z²)/h(z²) > 0 (z3).
  - Then φ ≤ C_b h on [0, L], φ ≤ P₀ on [0, ½], and φ(y) ≤ 2P₀y on
    [½, 1] (z3).
- **S.3, lower strip (sympy + z3).** If y ≤ ½ then r = x. If y ≥ ½ then
  r = xk with k = y + a(y)(1−y) ∈ [y, 1]. Both cases close with
  2C_bP₀ < 1.
- **S.4, upper strip (z3).**
  - φ(x) ≤ C_tx, in squared form, from h(x) ≤ h(U), h(x²) ≤ h(U²),
    E ≤ E(1) and x ≥ U.
  - D/h ≤ 2ln2/h(z²) on all three pieces, using h(z²) ≤ ln 2,
    h(z²) ≤ 2h(z) and h(y²) ≤ 2h(y).
  - Then φ(y) ≤ C_g h(y), and the chain closes with C_tC_g < 1.
- **S.5, middle coordinate map (sympy-exact + z3).**
  - x(t) = 1/(t² + R) solves x² + t²x(1−x) = ½. This is reduced modulo
    R² = (t²−1)² + 1, so a(x(t)) = t.
  - x(0) = 1/√2 and x(1) = ½, and the derivative formula
    (coordinate-derivative) holds.
  - Every positive root for t ∈ [0,1] lies in [½, 1/√2], and |x′| ≤ 4.
  - Hand: IVT, so the three maps cover [1/16, 15/16].
- **S.6 (z3).** The bridge on [0, L] reduces to the scalar A − s(A)C_b > 0.
  The proven kernel range 1/256 ≤ r ≤ 15/16 on the compact square is the
  intersection used by our cover.

#### Mixture (§7)

- **M.1 (sympy-exact + z3).**
  - The change of variables is u = t(1+ξ) = −ln x and v = −ln y.
  - 0 < x ≤ y, xy < 1 ⇒ t > 0 and ξ ∈ [0, 1].
  - (M)/(2xy) is exactly F, with h and ψ abstract.
  - Both sides of (M) vanish at xy = 0 and at x = y = 1.
- **M.2 (sympy-exact).** G = u − (eᵘ−1)ln(1−e^{−u}). The series for G, G′
  and G″ are summed by sympy, and Σ1/(j(j+1)) = 1. G′ > 0, G″ < 0, G ≥ u
  and −G″ ≤ 1/(eᵘ−1) ≤ 1/u. This reuses Approach 6's G.1–G.2; e^u ≥ 1 + u
  is a hand step.
- **M.3, (Gsmall).** J = G + u ln u has J″ = G″ + 1/u ≥ 0 (z3), and
  lim J(u)/u = 1 (sympy limit). Hand: chord slopes of a convex function.
  Cross-check: G(u) ≥ u(1 − ln u) on [2⁻⁸, 64] by 604 interval cells.
- **M.4, (Gdeficit).**
  - The identity G(u)+G(v)−G(u+v) = [J(u)+J(v)−J(u+v)] + (u+v)h(u/(u+v))
    is sympy-exact, and the bracket is ≤ 0 (z3, from chord slopes).
  - (√p + √(1−p))² = 1 + 2√(p(1−p)), and (u+v)·2√(p(1−p)) = 2√(uv).
  - Hand: Jensen, and ln(1+r) ≤ r.
- **M.5, (Ptail) and P ≥ CG.**
  - P² = G(2u) where ψ = s (sympy).
  - D ≥ h: x ≥ z ⇒ 1 − x ≤ x² ≤ x (z3, from z² + z > 1). Hand: h on
    [1−x, x] is ≥ h(x) (concavity and symmetry), and h ≤ ln 2.
  - Then φ ≥ Ch and P ≥ CG (z3).
- **M.6, small t ≤ 1/1000 (z3 + exact).**
  - The skeleton gives F ≥ (k₀ − ½)G(2t).
  - **Both scalars are now exact:**
    - e^{−1/500} ≥ 1 − 1/500 > 0.721 (hand: e^{−x} ≥ 1 − x);
    - e < 2.72 (Taylor tail, hand; Arb confirms), so 2.72⁴ < 250 and
      ln 250 > 4. Hence 2mw₄(1 + ln 250) − 1 > 10mw₄ − 1 > 0.
- **M.7, large t ≥ 16 (z3).** The skeleton closes with the scalar
  16mw₄C² > ½ (interval and Arb), and fails with 8 in place of 16.
- **M.8, edge bounds (z3).**
  - (edge1) holds, and so does (edge2) under v ≤ −ln B and
    G(v) ≤ [2mw₄CG(t)]². Without v ≤ −ln B, edge2 fails.
  - The box form follows by monotonicity of G (App. A, "Bounds for an
    entire edge box").
  - The claim also asserts that the edge tests in
    `jiang_checks.verify_mixture_strip` use exactly these quantities
    (v_max, −ln B rounded down, G(t₋), G(2t₋)).
- **M.9, App. A derivative formulas (sympy-exact, abstract functions).**
  - φ′ (phiprime); s′; ψ′ on [A, B]; P′ = ψ(x)/x − ψ′(x).
  - P and P′ on the two closed-form pieces that `jiang_checks.P_all` uses.
  - F_t and F_ξ (eq. Ft, Fxi).
  - r_α and r_β in both orders, and Δ_α, Δ_β.

  Earlier, `test_jiang` had checked these only numerically against mpmath.

#### Scalars and stress test

- **SC.** All 12 scalar signs were re-evaluated in Arb at 200 bits,
  independently of `interval.py`. All are positive, and each Arb ball
  overlaps the interval.py enclosure. The smallest are:
  - k₀ − ½ = 8.685975·10⁻⁹ (exact rational);
  - s(A) − φ(A) = 1.63498·10⁻³;
  - 1 − 2C_bP₀ = 0.02714;
  - 1 − C_gC_t = 0.06286.
- **x (numerical, not a proof).** (K) and (M) were evaluated in 40-digit
  mpmath at 2000 random points each. Extra points sit near (x*, x*),
  y → 1, x → 0 and every breakpoint. The minima are K − ψψ ≥ 1.1·10⁻¹¹
  (near x → 0, where both sides are tiny) and (M)-gap/(xy) ≥ 2.2·10⁻⁸.

#### Outcome

| step | method | status |
| --- | --- | --- |
| Reduction: E_U Q = x, E QQ = r, Q ∈ [0,1], r range | sympy-exact + z3 | machine-checked |
| Reduction: variance step, integration of (M), assembly to p ≥ 1−m | sympy-exact (finite form) + z3 | machine-checked |
| Reduction: chain rule, conditioning, max entropy, law of the shared-uniform samples, conditional independence | exact finite laws on 150 random families (numerical sanity test) | read only; instances consistent |
| Ceiling (not used by the bound): f′, f″, f‴, f(q*), (E), (C) | sympy-exact + z3 | machine-checked (two log bounds by hand) |
| Definitions: order of parameters, continuity of a, D, ψ; E′ > 0 | exact + sympy + z3 (+ interval/Arb) | machine-checked (MVT by hand) |
| Lemma "geometric" (both parts) | sympy-exact + z3 (+ interval cross-check) | machine-checked (MVT, midpoint concavity by hand) |
| (profile-order) | sympy-exact + z3 + interval/Arb scalars | machine-checked (MVT twice by hand) |
| Passing from (original-K) to (K) | z3 | machine-checked |
| (and), (concavity-scaling) | sympy-exact (grouping identity; g″) | machine-checked (entropy ≥ 0, concave-with-zero-ends by hand) |
| (lower-profile), (P0), (linear-profile) | sympy-exact + z3 + interval/Arb scalar | machine-checked (MVT by hand) |
| Lower strip, upper strip of (original-K) | sympy + z3 + interval/Arb scalars | machine-checked |
| Middle coordinate map, coverage of the square | sympy-exact + z3 | machine-checked (IVT by hand) |
| Bridge on [0, 1/16]; kernel range for the cover | z3 + interval/Arb scalar | machine-checked |
| Change of variables, (M)/(2xy) = F, boundary xy = 0 | sympy-exact + z3 | machine-checked |
| G facts, (Gsmall), (Gdeficit) | sympy-exact + z3 (+ interval cross-checks) | machine-checked (Jensen, chord slopes, e^u ≥ 1+u by hand) |
| (Ptail), D ≥ h, P ≥ CG | sympy + z3 + exact | machine-checked (h ≥ h(x) on [1−x, x] by hand) |
| Small t ≤ 0.001 | z3 + **exact** scalars | machine-checked (e^{−x} ≥ 1−x, Taylor tail of e by hand) |
| Large t ≥ 16 | z3 + interval/Arb scalar | machine-checked |
| (edge1), (edge2), box form, match with our cover code | z3 + source inspection | machine-checked |
| App. A derivative formulas | sympy-exact | machine-checked |
| 12 scalar signs | interval (Approach 5) + **Arb** (new) | two independent evaluations |
| Mean-value acceptance test for piecewise-C¹ functions, hull at joins | — | hand (MVT along axis-parallel segments) |

**No gap or error found in Jiang's argument.** Every step listed above was
reproduced exactly as stated in the paper. One cosmetic point: (strip-checks)
lists both C_bP₀ < ½ and 2C_bP₀ < 1, which are the same condition.

Nothing was Lean-verified.

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
| Costa–Sadhu Thm 1.2 analytic glue: Lemmas 4.1, 4.4, 6.1 (case analysis), W₀ increasing, Lemma 6.2 Cases 1–3 + residual region, Prop. 6.3 arithmetic; Case 1 margin c₁ ≥ 2.89·10⁻⁶ and Case 3 scalar now exact | machine-checked (sympy-exact + Sturm + z3 + interval/Arb), up to listed standard hand steps (MVT, FTC/Tonelli, Taylor bounds, continuity); not Lean | `computations/frankl/analytic_glue.py`, `results/analytic_glue.txt` |
| c_UC ≥ 0.3828852549667978 (Costa–Sadhu Thm 1.2) | proved in Costa–Sadhu (preprint); all computations re-certified here; analytic glue machine-checked here except the measure-theoretic integration (Prop. 6.3, Lemma 2.1) and Liu's Prop. 3 (read in Liu's own text; restatement faithful) | same + arXiv:2610.02295 |
| Jiang's 12 scalar signs, bridge, kernel (K) on [1/16,15/16]², mixture (M) on [0.001,16]×[0,1] | certificate-checked independently (own interval code; 1,306 kernel + 4,357 mixture boxes) | `computations/frankl/jiang_checks.py`, `results/jiang.txt` |
| Jiang analytic glue: reduction (finite forms + assembly), ceiling, Lemma "geometric", profile order, passing to (K), (and), strips, coordinate maps, bridge tail, change of variables, G facts, (Gsmall), (Gdeficit), (Ptail), small t (scalars now exact), large t, edge bounds, App. A derivative formulas; 12 scalars re-evaluated in Arb | machine-checked (sympy-exact + z3 with non-vacuity guard + interval/Arb), up to named hand steps (MVT, IVT, Jensen, concavity, Taylor bounds); probability layer read only (sanity-tested on exact finite laws of 150 random families); not Lean | `computations/frankl/analytic_glue_jiang.py`, `results/analytic_glue_jiang.txt` |
| c_UC ≥ 0.38288525 (Jiang) | proved in Jiang (preprint); all computations re-certified here; analytic glue machine-checked here except the probability layer of the reduction (read only) | same + arXiv:2609.08291 |

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

1. **Finish the analytic glue.** For Costa–Sadhu Thm 1.2 only the
   measure-theoretic layer is left (Prop. 6.3's integration, Lemma 2.1's weak
   limit, and Liu's argument that the induced laws lie in C₃). Liu's
   Prop. 3 itself has been read in Liu's own text and the restatement is
   faithful (Approach 6). Jiang's analytic glue is done (Approach 7); for it
   only the probability layer of the reduction is left (chain rule,
   conditioning, the induction for the shared-uniform rule, conditional
   independence given the shared history). Next:
   - write the shared probability layer of both reductions (Gilmer chain
     rule + Liu/Jiang couplings) as one short, explicit finite-probability
     argument. That is the natural first Lean target once Mathlib is
     reachable.

   Optionally, ask for the Zenodo supplement (record 22727713) and diff its
   covers against ours. For Lean, a session with access to the Mathlib cache
   is needed (`lakecache.blob.core.windows.net` or `cache.lean-lang.org`);
   from here both are blocked.
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
