# Frankl's union-closed sets conjecture

**Area:** extremal combinatorics / information theory
**Status:** in progress. Literature pinned down from primary sources. The
one-variable inequality behind the (3−√5)/2 bound is **certificate-checked**
here with self-contained interval arithmetic. The conjecture is **checked
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
| **0.3828852549667978** | Costa–Sadhu, arXiv:2610.02295 Thm 1.2 (1 Oct 2026). **This is the ProofAtlas "Oct 2026" claim.** | preprint, not refereed; computer-assisted (Zenodo supplement) | [read] statement and §6 opening |

Current best *claimed* constant: **0.3828852549667978** (Costa–Sadhu,
unrefereed). The best constant in a refereed journal is (3−√5)/2 (AHS, EJC
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

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| φ H(x²) ≥ x H(x) on [0,1], φ = (√5−1)/2, equality only at 0, φ, 1 (AHS Claim 1, Boppana) | certificate-checked (own outward-rounded interval arithmetic + analytic end/tangency lemmas) | `computations/frankl/verify_boppana.py` |
| c_UC ≥ (3−√5)/2 | proved (AHS) given the line above; the reduction is AHS's, read and not formalised | AHS arXiv:2211.11731 |
| Frankl holds for every union-closed family on a universe of ≤ 6 elements | computationally checked (exhaustive, n ≤ 6) — already known up to 12 | `computations/frankl/frankl_enum.c`, `results/small_cases.txt` |
| Labeled counts 2, 7, 61, 2480, 1385552, 75973751474 (and the universe-[n] counts) | computed; they equal Brinkmann–Deklerck | same |

## Next steps

- (see the end of the file; updated at each checkpoint)
