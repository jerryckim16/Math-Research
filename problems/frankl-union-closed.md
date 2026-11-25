# Frankl's union-closed sets conjecture

**Area:** extremal combinatorics / information theory
**Status:** in progress. Literature pinned down from primary sources. The
one-variable inequality behind the $(3-\sqrt{5})/2$ bound is **certificate-checked**
here with self-contained interval arithmetic. **Every finite computation** in
Costa–Sadhu's proofs of $c_{\mathrm{UC}} \ge c_{L} \approx 0.3827091$ (their Thm 1.1) and of the
record $c_{\mathrm{UC}} \ge 0.3828852549667978$ (their Thm 1.2), and in Jiang's independent
proof of $c_{\mathrm{UC}} \ge 0.38288525$, is **independently re-certified**. The analytic
glue of Thm 1.2 (Lemmas 4.1, 4.4, 6.1, $W_{0}$ monotonicity, Lemma 6.2 Cases 1–3
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
exhaustively for universes of size $n \le 6$**: all 75,973,751,474 labeled
families, reproducing the known labeled counts exactly.
**Started:** 2026-11-24
**ProofAtlas:** rank 363

## Statement

A family $F$ of finite sets is *union-closed* if $A \cup B \in F$ for all $A, B \in F$.

**Conjecture (Frankl, 1979).** Every finite union-closed family $F \ne \{\emptyset\}$
($F$ nonempty) has an element $x$ with $\lvert\{A \in F : x \in A\}\rvert \ge \lvert F\rvert/2$.

Remarks.

- WLOG $\emptyset \in F$. Adding $\emptyset$ keeps $F$ union-closed, raises $\lvert F\rvert$ by one and changes
  no frequency. So the conjecture for $F \cup \{\emptyset\}$ implies it for $F$.
- Union-closed families on $[n]$ that contain $\emptyset$ are exactly the complements
  $\{[n] \setminus A : A \in F\}$ of *Moore families* (intersection-closed families
  containing $[n]$).
- Write $c_{\mathrm{UC}} := \inf_{F} \max_{x} \mathrm{freq}_{x}(F)/\lvert F\rvert$ over finite union-closed $F$ that
  contain a nonempty set. The family $\{\emptyset, \{1\}\}$ gives $c_{\mathrm{UC}} \le 1/2$, and the
  conjecture says $c_{\mathrm{UC}} = 1/2$.
- Equivalent forms exist for lattices (every finite lattice with $\ge 2$ elements
  has a join-irreducible $a$ with $\lvert[a, 1]\rvert \le \lvert L\rvert/2$) and for bipartite graphs
  (Bruhn–Charbit–Schaudt–Telle). See the survey of Bruhn–Schaudt.

## Known results

Labels: **[read]** = the arXiv LaTeX source was read for the cited
statement; **[skimmed]** = the source was searched for the cited constant
and its statement read, not the whole proof; **[abstract]** = arXiv abstract
only. Literature was checked on 2026-11-24 with the arXiv API: every title or
abstract containing "union-closed", "union closed" or "Frankl", up to
arXiv:2611.13749. OEIS could not be reached (the host was blocked), so all
counts are taken from Brinkmann–Deklerck (below).

### Lower bounds on $c_{\mathrm{UC}}$ (the entropy method)

| bound | who | status | label |
| --- | --- | --- | --- |
| 0.01 | Gilmer, arXiv:2211.09055 (Nov 2022) | proved | [abstract] |
| $(3-\sqrt{5})/2 \approx 0.381966$ | Alweiss–Huang–Sellke arXiv:2211.11731, EJC 31(3) P3.35 (2024); Chase–Lovett arXiv:2211.11689; Sawin arXiv:2211.11504; Pebody arXiv:2211.13139 (all Nov 2022) | proved. AHS use a computer check for one 1-variable inequality, which Boppana (arXiv:2301.09664, 1985 origin) proves by calculus | AHS [read]; others [abstract] |
| $\approx 0.3823455$ (exactly the optimum of Sawin's iid + max-entropy mixture, 0.382345533366703) | Sawin (strict improvement, no value); Yu arXiv:2212.00658 ($\approx 0.38234$, numerical); Cambie arXiv:2212.12500 (proof of the optimum, computer-aided) | proved (Cambie) | Cambie [skimmed], Yu [abstract] |
| $> 0.3823455$ strictly; $\approx 0.382709$ under numerically checked hypotheses | Liu, arXiv:2306.08824 (CISS 2024), conditionally-iid couplings | the strict improvement is analytic; 0.382709 is not proved | [skimmed] |
| $c_{L} = 1 - x^{*}H(x^{*})/H(x^{*2}) > 0.382709087918735$, where $x^{*}$ is the root in $(0,1)$ of $x^{4}-2x^{3}+3x^{2}-1$ | Costa–Sadhu, arXiv:2610.02295 Thm 1.1 (Oct 2026); earlier Zenodo preprint by Costa | preprint; computer-assisted (MPFR intervals, Bernstein certificate) | [read] §§1–5 |
| **$0.38288525 = 1531541/4000000$** | Jiang, arXiv:2609.08291 (8 Sep 2026) | preprint; computer-assisted (interval code in the appendix). **All finite computations re-verified here** (Approach 5); **analytic glue machine-checked** (Approach 7) | [read] §§1–8, App. A–B |
| **0.3828852549667978** | Costa–Sadhu, arXiv:2610.02295 Thm 1.2 (1 Oct 2026). **This is the ProofAtlas "Oct 2026" claim.** | preprint, not refereed; computer-assisted (Zenodo supplement). **All finite computations re-verified here** (Approach 4) | [read] §6, App. A |

Current best *claimed* constant: **0.3828852549667978** (Costa–Sadhu,
unrefereed). Every finite computation of its proof, and of Jiang's
0.38288525, is independently re-verified here. The analytic glue of both
proofs is machine-checked (sympy/z3/interval/Arb, Approaches 6–7) up to named
hand steps and a read-only probability/measure-theory layer. The best constant in a refereed journal is $(3-\sqrt{5})/2$ (AHS, EJC
2024). Cambie's 0.3823455 is in an arXiv v2 (2025); whether it was refereed
was not checked. Two independent groups give near-identical values
(0.38288525 and 0.38288525497), and both bounds sit within $10^{-8}$ of the same
proved ceiling (next section). That agreement is decent evidence that the
numerics are right, but it is not a referee check. We have since re-run every
finite computation of both proofs with our own code (Approaches 4–5), and
machine-checked their analytic glue (Approaches 6–7). That is still not a
referee check: the hand steps and the probability layer were read, and
nothing is Lean-verified.

### Barriers: what each variant of the method can give

The engine is Gilmer's. Let $A$, $B$ be two samples of a uniform member of $F$, with
some coupling. Then $A \cup B \in F$, so $H(A \cup B) \le \log\lvert F\rvert = H(A)$. Coordinatewise
chain-rule bounds turn this into a one-coordinate inequality between
probability measures on $[0,1]$. Each choice of coupling family gives its own
optimal constant:

1. **iid coupling.** The optimum is exactly **$(3-\sqrt{5})/2$**. AHS [read] prove
   $\min_{\mu:\,\text{mean }\varphi} E_{\mu\times\mu} H(xy) - E_{\mu} H(x) \ge 0$ iff $\varphi \ge (\sqrt{5}-1)/2$ (with
   $x = 1 - p$). The minimiser is two-point, $\{0, x\}$. The key fact is
   $\varphi H(x^{2}) \ge x H(x)$ on $[\varphi, 1]$. Chase–Lovett [abstract] show $(3-\sqrt{5})/2$ is
   *sharp* for "approximately union-closed" families, so no iid argument that
   only uses approximate union-closedness can beat it.
2. **Sawin's mixture of iid and max-entropy coupling.** The optimum is
   $\approx$ **0.382345533366703** (Cambie [skimmed], §"upper bound": "one cannot aim
   to prove the result with a constant better than 0.382345533366703 with the
   exact suggested approach of Sawin").
3. **Liu's conditionally-iid couplings, Example 5 with $f(x) = x(1-x)$, mixed
   with iid.** The value is $c_{L} \approx$ **0.382709087918735**. Liu found it
   numerically; Costa–Sadhu proved it.
4. **The "pointwise product" relaxation.** The iid kernel is mixed with one
   (or finitely many) conditionally-iid kernels $K$, each bounded below by
   $\psi(x)\psi(y)$. The ceiling is
   **$C^{*} = 1/2 - (1-q^{*}) \ln(1+q^{*}) / (2 \ln 2) \approx 0.3828852599667978$**, where $q^{*}$
   is the root in $(0,1)$ of $(1-q)\ln(1-q) + q \ln(1+q) = 0$ ($q^{*} \approx 0.69090774$).
   This is proved in Jiang [read], Prop. "Limitation of the pointwise method".
   The proof has two steps. The endpoint $y = 1$ forces $m\cdot w_{0} \ge 1/2$. The
   diagonal $x = y = q$, with $\psi(q)^{2} \le K(q,q) \le \ln 2$, then gives the bound.
   Costa–Sadhu §7 state the same number. Both record bounds sit within
   $5.1\cdot 10^{-9}$ of this ceiling, so **this route is exhausted**. Any further
   progress needs a different inequality: global couplings (Jiang §global,
   which gives a gain that tends to 0 with $\lvert F\rvert$), more coordinates, or
   non-entropy input.
5. **Gilmer's strengthening.** Gilmer's Conjecture 1 would have given 1/2. It
   is false (Sawin [abstract]; Ellis, arXiv:2211.12401 [abstract]).

We recomputed (mpmath, 40 digits; this is a check, not part of any proof):
$x^{*} = 0.690787593924988$, $c_{L} = 0.382709087918735030$, $q^{*} = 0.690907738725408$,
$C^{*} = 0.382885259966797797$. All agree with the papers.

### Exact verification for small cases

Notation clash: the survey writes $m$ for the universe size and $n$ for the number
of sets. Here **$n$ = universe size**.

- **$n \le 12$** (universe of at most 12 elements). Živković–Vučković, "The 12
  element case of Frankl's conjecture", preprint 2012, as cited in the
  Bruhn–Schaudt survey (Graphs Combin. 31 (2015); arXiv:1309.3297 [read], Thm
  "$m=12$"). The method uses FC-families and weights (Poonen's theorem) plus a
  computer search. Earlier steps: $n \le 11$ (Bošnjak–Marković, EJC 15 (2008)
  R88), $n \le 10$ (Marković 2007), $n \le 9$ (Lo Faro 1994), $n \le 7$ (Poonen 1992).
  We did not locate a refereed version of the $n = 12$ paper, and no claim of
  $n = 13$ was found on arXiv.
- **$\lvert F\rvert \le 50$ sets.** Lo Faro (1994), rediscovered by Roberts–Simpson
  (Australas. J. Combin. 47 (2010)): a minimal counterexample on a minimal
  universe of size $n$ has at least $4n - 1$ sets. Combined with $n \le 12$, this
  gives $\ge 4\cdot 13 - 1 = 51$ sets (survey Cor. "$n=50$" [read]). Older direct bounds:
  $\le 36$ sets (Lo Faro), $\le 40$ sets (Roberts 1992 tech. report).
- **Formalisation.**
  - Marić–Živković–Vučković: FC-families in Isabelle/HOL (CICM 2012,
    arXiv:1207.3604) and a fully verified classification of FC(6) families
    (arXiv:1902.08765), both [abstract].
  - Koutsoukou-Argyraki–Paulson: Isabelle/HOL formalisation of the
    Aaronson–Ellis–Leader special case (arXiv:2609.20876, Sep 2026) [abstract].
  - Ho (arXiv:2601.19327, Jan 2026) [abstract]: proves
    $\alpha_{k} H(x^{k}) \ge x^{k-1} H(x)$ for real $k > 1$ and **formalises the proof in Lean 4**. The
    case $k = 2$ is Boppana's inequality.
- **Structural special cases.** These cover the $\ge (2/3)2^{n}$ regime, separating
  families with $\le 2n$ sets (Maßberg, arXiv:1508.05718), lower semimodular
  lattices, subcubic graphs, and height $\le 4$ in the $\emptyset$-free form (Tian,
  arXiv:2608.25147, 2026, [abstract]).
- **Enumeration data used as ground truth.** Brinkmann–Deklerck
  (arXiv:1701.03751 [read], Tables 1–2) give these numbers of labeled
  union-closed families on $[n]$ that contain $\emptyset$ (= labeled Moore families), for
  $n = 1\dots 7$:
  - labeled: 2, 7, 61, 2480, 1385552, 75973751474, 14087648235707352472;
  - up to isomorphism: 2, 5, 19, 184, 14664, 108295846, …;
  - with universe exactly $[n]$ ("UCS"), labeled: 1, 4, 45, 2271, 1373701,
    75965474236, ….

  (These are probably OEIS A102896 / A102894. That could not be confirmed,
  because OEIS was unreachable.)

## Approaches

### 1. Reproduce the iid entropy bound rigorously (interval arithmetic)

- **Idea.** AHS reduce the constant $(3-\sqrt{5})/2$ to a one-variable inequality
  (Claim 1): $\varphi H(x^{2}) \ge x H(x)$ for $x \in [\varphi, 1]$, $\varphi = (\sqrt{5}-1)/2$. Their appendix
  checks it by floating point to within $10^{-3}$ and notes that it "can be made
  completely rigorous using interval arithmetic". We do exactly that, on all of
  $[0, 1]$ (Boppana's form).
- **Outcome:** worked. See `computations/frankl/verify_boppana.py`, which
  certifies the inequality in 0.3 s:
  - **R0, $x \in (0, 1/100]$: analytic.** $G(x) \ge x^{2}[(2\varphi-1) \log(1/x) - 1] > 0$,
    because $(2\varphi-1) \log 100 - 1 \in [0.08713, 0.08714]$.
  - **R1, $x \in [1 - 1/4096, 1)$: analytic.** Write $y = 1 - x$ and $b = 1/4096$.
    Then $G \ge y[(\varphi(2-b)-1) \log(1/y) - \varphi(2-b) \log 2 - 1]$, and the bracket is
    $\ge 0.1056$ at $y = b$. It is increasing in $\log(1/y)$.
  - **R2, $x \in [1/2, 4/5]$: tangency.** $G(\varphi) = 0$ and $G'(\varphi) = 0$ exactly, by the
    algebra below. $G'' \ge 0.0021 > 0$ on $[1/2, 4/5]$ (44 interval cells), so
    $G(x) = \int_{\varphi}^{x} (x-s) G''(s)\, ds > 0$ for $x \ne \varphi$.
  - **R3, $[1/100, 1/2] \cup [4/5, 1 - 1/4096]$: bisection.** Mean-value-form
    enclosures over 29 + 15 cells; the minimum certified lower bound is
    $2.9\cdot 10^{-5}$.

  The exact algebra at $\varphi$: $\varphi^{2} = 1 - \varphi$ gives $H(\varphi^{2}) = H(\varphi)$. Also
  $\log((1-\varphi^{2})/\varphi^{2}) = -\log \varphi =: L$ and $\log((1-\varphi)/\varphi) = \log \varphi = -L$. Hence
  $G(\varphi) = \varphi H(\varphi) - \varphi H(\varphi) = 0$. Then $G'(\varphi) = 2\varphi^{2}L - H(\varphi) + \varphi L$, and
  $H(\varphi) = \varphi L + 2\varphi^{2}L$, so $G'(\varphi) = 0$.
- **Interval arithmetic** (`interval.py`) is pure Python on IEEE doubles.
  $+$, $-$, $\times$, $\div$ and $\sqrt{\cdot}$ are rounded one ulp outward. log is computed by an atanh
  series after an exact frexp reduction, with a rigorous tail bound; $\log 2$ is
  bounded in exact rationals. It never calls libm log. Tests cross-check it
  against exact rational bounds and against mpmath.iv.
- **What this establishes.** AHS Claim 1 (hence Boppana's inequality) is
  certificate-checked. With AHS Theorems 1–2 [read], this gives
  $c_{\mathrm{UC}} \ge (3-\sqrt{5})/2$. The reduction itself is AHS's analytic argument; we read it
  but did not formalise it.

### 2. Exhaustive small-case checker

- **Idea.** Enumerate every union-closed $F \ni \emptyset$ on $[n]$ by splitting on the last
  element: $F0$ = members without $n$, $F1$ = (members with $n$) minus $n$. The
  conditions are: $F0$ union-closed with $\emptyset \in F0$; $F1$ union-closed; $F0 \vee F1 \subseteq F1$.
  - F0 runs over $S_{n-1}$-classes, weighted by orbit size.
  - F1 runs over a depth-first search of the subsets in decreasing numeric
    order. The prefix chosen so far is always closed, because $s \mid t \ge s$. So
    "may $s$ be added" is a check of a few bit operations, and each family
    appears exactly once.
  - Frequencies are popcounts.
- **Outcome:** worked. See `computations/frankl/frankl_enum.c` and
  `results/small_cases.txt`.

| $n$ | labeled families $\ni \emptyset$ (ours = literature) | with universe $[n]$ (ours = lit.) | $S_{n-1}$ classes of F0 | Frankl fails | tight (max freq $= \lvert F\rvert/2$) |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 0 | 1 |
| 2 | 7 | 4 | 2 | 0 | 4 |
| 3 | 61 | 45 | 5 | 0 | 14 |
| 4 | 2,480 | 2,271 | 19 | 0 | 51 |
| 5 | 1,385,552 | 1,373,701 | 184 | 0 | 202 |
| 6 | **75,973,751,474** | **75,965,474,236** | 14,664 | **0** | 876 |

  The $n = 6$ run used 925,328,674 representative $(F0, F1)$ pairs and took about
  3 minutes on 4 cores. For $n \le 4$, everything (counts, classes for $n \le 3$,
  tight counts) is also re-derived by naive Python brute force over all
  subfamilies (`test_frankl.py`).
- **Limit.** $n = 7$ has $1.4\cdot 10^{19}$ labeled families, about $2\cdot 10^{16}$ $(F0, F1)$
  pairs even after symmetry. Plain enumeration cannot go further. The known
  range $n \le 12$ needs FC-family pruning.

### 3. Independent re-verification of Costa–Sadhu Thm 1.1 ($c_{\mathrm{UC}} \ge c_{L} \approx 0.382709$)

- **Idea.** Costa–Sadhu's proof of the bound $c_{L}$ has four parts:
  - Liu's one-coordinate criterion (Liu, Prop. 3);
  - the positive-correlation Lemma 2.1;
  - Lemma R: $H(r(x,y))^{2} \ge H(g(x)) H(g(y))$, where $r = xy(2-x-y+xy)$ and
    $g(x) = r(x,x)$;
  - Lemma S: $2\alpha H(xy) + 2\beta\sqrt{H(g(x))H(g(y))} \ge (xH(y)+yH(x))/m^{*}$, where
    $m^{*} = 1 - c_{L}$ and $\alpha$, $\beta$ are fixed by tangency at $x = y = x^{*}$.

  Lemma R is analytic except for one exact Bernstein certificate. Lemma S has
  analytic boundary lemmas (5.3, 5.4), a Hessian check around the tangency
  $(t^{*}, 0)$, and an interval box cover of the compact remainder. Our code
  re-does every one of these finite steps, with our own cover.
- **Outcome:** worked. See `computations/frankl/costa_sadhu_checks.py` and
  `results/costa_sadhu_thm11.txt`.
  - **Exact rationals.**
    - The identity $W r_{xy} = UV + xy$, and $r_{x} = yU$, $r_{y} = xV$, $r_{xy}$, by
      formal differentiation.
    - $g(43/64) - 1/2 = 305/2^{24}$.
    - The $4\times 4$ Bernstein matrix of $WUV - (1-r)$ on $[0, 43/64]^{2}$ equals the
      published matrix entry by entry, and every entry is $> 0$.
  - **Constants** (intervals): $x^{*} \in [0.690787593924988, 0.6907875939249881]$,
    $m^{*} \in [0.61729091208126, 0.61729091208127]$,
    $\beta \in [0.1000525598628, 0.1000525598630]$, $t^{*} = -\log x^{*} \in [0.36992289186770, 0.36992289186772]$,
    $c_{0} = m^{*}\alpha \in [0.55552937614741, 0.55552937614746] > 1/2$. All lie inside the
    published enclosures. The decimal claim $c_{L} > 0.382709087918735$ holds
    with a margin of only **$3.0\cdot 10^{-17}$**, so it needs exact rational
    arithmetic: we used a bracket for $x^{*}$ of width $2^{-71}$ and atanh-series log
    bounds.
  - **Scalars of Lemmas 5.3/5.4**: $\zeta(0.002) \ge 0.0166724744112$; the
    5.4(a, b, c) values are $\ge 0.00117883769797$, 0.0355980952001 and
    0.0107176824298. Each is positive and matches the paper.
  - **Tangency.** We use our own local rectangle
    $Q_{0} = [5/16, 7/16] \times [-1/16, 1/16]$ in $(t, d)$; $F$ is even in $d$. On it $F_{tt} \ge 0.0337$, $F_{dd} \ge 0.78$ and
    $\det \ge 8.8\cdot 10^{-5}$ (703 boxes). So $F$ is convex on $Q_{0}$. The point $(t^{*}, 0)$ is
    stationary with $F = 0$ there (their Lemma 5.5, analytic), so $F \ge 0$ on $Q_{0}$.
  - **Cover.** This is our own dyadic decomposition: $t \in [1/512, 45/32]$ with
    $v = t - d \ge 2^{-15}$, and $t \in [45/32, 33/8]$ with $v \ge 3/32$. It overlaps the
    analytic regions ($t \le 0.002$; $v \le 5\cdot 10^{-5}$ for $t \le 1.4$; $v \le 0.1$ for
    $1.4 \le t \le 4.1$; $t \ge 4.1$).
    - It uses 31,944 boxes with mean-value lower bounds
      $\tilde{F}(c) - \sup\lvert \tilde{F}_{t}\rvert\Delta t - \sup\lvert \tilde{F}_{\xi}\rvert\Delta\xi$, all rigorously rounded. The minimum certified
      lower bound is $2.7\cdot 10^{-7}$.
    - Box endpoints are exact dyadics, and the clipping $\xi \le 1 - \nu/t$ is
      rounded upward.
    - It takes about 8 CPU-minutes.
  - **Test harness.** `test_frankl.py` checks the derivative formulas
    ($G'$, $G''$, $\Gamma_{5}'$, $\Gamma_{5}''$, $\tilde{F}_{t}$, $\tilde{F}_{\xi}$ and the Hessian) against 40-digit finite
    differences. The mean-value bounds rely on them.
- **What this establishes.** We re-ran every computer-assisted assertion
  that Thm 1.1 uses, with independent code (not their MPFR supplement) and a
  different cover. They come out true. We read but did not machine-check:
  - Lemma 4.1 (entropy, one variable);
  - Lemma 4.4 ($M$ decreasing);
  - the case analysis of Lemma R;
  - Lemmas 5.2–5.5;
  - the reduction (Prop. 3.1);
  - Lemma 2.1;
  - Liu's Prop. 3. This was read only as Costa–Sadhu restate it. It has
    since been read in Liu's own text and the restatement is faithful
    (Approach 6).

  We found no error. Label: **$c_{\mathrm{UC}} \ge c_{L}$ — proof read, all finite
  computations certificate-checked independently**. (Their record Thm 1.2
  is treated in Approach 4.)

### 4. Independent re-verification of Costa–Sadhu Thm 1.2 ($c_{\mathrm{UC}} \ge 0.3828852549667978$)

- **Source.** arXiv:2610.02295 v1 LaTeX, §6 (Lemmas 6.1, 6.2, Prop. 6.3,
  proof of Thm 1.2) and Appendix A (Certificates A.4–A.7) **[read]**. The
  Zenodo supplement (record 22727713) was **not** used; every check below is
  our own code.
- **Parameters** (all exact rationals): $\ell_{0} = 1409/2000$,
  $\tau_{0} = \ell_{0}^{2} = 1985281/4000000$, $m_{0} = 3085573725166011/(5\cdot 10^{15})$, $\alpha_{0} = 1/(2m_{0}) + 1/800000000$,
  $\beta_{0} = 1 - \alpha_{0}$. The theorem's decimal is exactly $1 - m_{0}$. Kernel
  $r(x,y) = xy(1 + \tau_{0}(1-x)(1-y))$ (Liu's Example 5 with $f = \ell_{0}x(1-x)$),
  $g(x) = r(x,x)$.

#### Proof map

The chain is: Liu's Prop. 3 (criterion) $\to$ Prop. 6.3 (integrate the two
pointwise inequalities; uses Lemma 2.1, positive correlation in $C_{3}(P)$) $\to$
Lemma 6.1 + Lemma 6.2. Analytic steps (A) were read; finite computations (C)
were re-done.

1. **Lemma 6.1** (tuned product): $H(r(x,y))^{2} \ge H(g(x))H(g(y))$ on $[0,1]^{2}$.
   - (A) $\Delta_{x}(y) = L(x,y) - \tfrac{1}{2}L(x,x) - \tfrac{1}{2}L(y,y)$, $L = \log H\circ r$; it suffices that
     $\partial_{y}\Delta = L_{2}(x,y) - L_{2}(y,y) > 0$ for $x < y$.
   - (C) exact: $r_{x} = y[1+\tau_{0}(1-2x)(1-y)]$, $r_{y} = x[1+\tau_{0}(1-x)(1-2y)]$,
     $r_{xy} = 1+\tau_{0}(1-2x)(1-2y)$; identity $W\cdot r_{xy} - r_{x} r_{y}/(xy) = \tau_{0}xy$;
     $g' = 2x[1+\tau_{0}(1-x)(1-2x)]$ with $(1-x)(1-2x) \ge -1/8$;
     $g(45/64) - \tfrac{1}{2} = 42978321721/2684354560000$.
   - Case $g(y) < \tfrac{1}{2}$: (C) **Certificate A.4**, exact Bernstein: the 16
     product-Bernstein coefficients of $W\cdot U\cdot V - \tau_{0}(1-r)$ on $[0, 45/64]^{2}$ are
     positive, minimum $4652778828628843621308587/8388608\cdot 10^{18}$. (A) This gives
     $r_{xy}/(r_{x} r_{y}) \le 1/r + 1/(1-r)$; with Lemma 4.1
     ($-\Lambda''/\Lambda' > 1/u + 1/(1-u)$ on $(0, \tfrac{1}{2})$, $\Lambda = \log H$) it gives $L_{12} < 0$.
   - Case $g(y) \ge \tfrac{1}{2}$: (A) $A_{x}(y) = r_{y}/r < A_{y}(y)$, and Lemma 4.4 ($M = uH'/H$ is
     strictly decreasing) gives $L_{2}(x,y) > L_{2}(y,y)$.
2. **Lemma 6.2** (second inequality): $F_{0}(s,\sigma) > 0$ for $0 < s \le \sigma$, where
   $x = e^{-s}$, $y = e^{-\sigma}$,
   $F_{0} = \alpha_{0}G(s+\sigma) - (G(s)+G(\sigma))/(2m_{0}) + \beta_{0}\sqrt{W_{0}(s)W_{0}(\sigma)}$,
   $G(u) = e^{u} H(e^{-u})$ and $W_{0}(u) = e^{2u}H(g(e^{-u}))$.
   - (A) $G$ is increasing and concave (series); $W_{0}$ is increasing (its proof
     uses $z q_{z} = 2q - 2\tau_{0}z^{3}(1-z)$ and $27\tau_{0}/256 < 1$, both re-checked exactly);
     $0 \le D := G(s)+G(\sigma)-G(s+\sigma) \le \min(G(s)-s, G(\sigma)-\sigma) < 1$.
   - (C) **Certificate A.5**: for all $v > 0$, $W_{0}(v) \ge (8/5)G(v)$ and
     $G(16v) \ge (178/25)G(v)$; three scalar margins $(8\beta_{0}/5)\sqrt{178/25} - 1/(2m_{0})$,
     $\beta_{0}W_{0}(2) - 1/(2m_{0})$ and $8\beta_{0} \log 2 - 1/(2m_{0})$ are positive.
   - (A) Case 1, $G(\sigma) \ge (178/25)G(s)$: $F_{0} \ge G(s+\sigma)/8\cdot 10^{8} + G(s)\cdot[\text{first scalar}] > 0$.
     **This is the $y \to 1$ edge** ($s \to 0$). There $F_{0} \to G(\sigma)/8\cdot 10^{8}$,
     because $m_{0}\alpha_{0} - \tfrac{1}{2} = m_{0}/8\cdot 10^{8} = 7.7\cdot 10^{-10}$. The proof never resolves that
     margin numerically: Case 1 works with the $2.9\cdot 10^{-6}$ margin.
   - (A) Case 2, $s, \sigma \ge 2$: uses $D < 1$, $W_{0}$ increasing and the second scalar.
   - (A) Case 3, $s, \sigma \le 2^{-10}$: $D < uH(\lambda)$ (via $-G''(v) < 1/v$),
     $W_{0}(w) \ge 2w \log(1/2u)$, $H(\lambda) \le 2\sqrt{\lambda(1-\lambda)}$, and the third scalar.
   - (A) What remains: $\sigma < 16s$, $s < 2$, $\sigma > 2^{-10}$. That is, in $t = (s+\sigma)/2$
     and $\xi = (\sigma-s)/(\sigma+s)$: $2^{-11} < t < 17$ and $0 \le \xi < 15/17$.
   - (C) **Certificate A.6**: $F(t,d) := F_{0}(t-d, t+d)$ has a positive definite
     Hessian on a rectangle around $(t_{c}, 0)$, $t_{c} = 0.369781418829901$. Also
     $F_{0}(t_{c},t_{c}) \approx 1.14\cdot 10^{-8}$ and $\lvert F_{t}(t_{c},0)\rvert$ is tiny; $F$ is even in $d$. So
     $F > 0$ there by the tangent-plane inequality.
   - (C) **Certificate A.7**: a finite box cover of $[2^{-11}, 17] \times [0, 15/17]$.
     Each cell either lies in the A.6 rectangle or has a positive
     mean-value lower bound.
3. **Prop. 6.3 and the theorem** (A): Lemma 6.1 + Lemma 2.1 give
   $\iint H(r)\,d\rho \ge (\int\sqrt{H\circ g}\, dP)^{2}$; integrating Lemma 6.2 against $P\otimes P$ and Liu's
   criterion with $\gamma = (1-c)/m_{0}$ give $c_{\mathrm{UC}} \ge 1 - m_{0}$. (Same as Thm 1.1.)

Not used by Thm 1.2: Certificate A.3 (the ceiling $\hat{c}$) and A.8 (§7).

#### What we re-computed (`computations/frankl/costa_sadhu_thm12.py`, `results/costa_sadhu_thm12.txt`)

- **Exact rationals.**
  - Parameters: $\tau_{0}$, $1 - m_{0} = 0.3828852549667978$ exactly, and
    $2m_{0}(1 - 1/8\cdot 10^{8}) > 1$.
  - Lemma 6.1: the derivative formulas, the identity, $g'$ and its $-1/8$ bound,
    and $g(45/64) - \tfrac{1}{2}$.
  - The $W_{0}$-monotonicity algebra, including
    $27/256 - z^{3} + z^{4} = (z - \tfrac{3}{4})^{2}(z^{2} + z/2 + 3/16)$.
  - The Case 3 identity $1 - g(z) = 1 - z^{2} - \tau_{0}z^{2}(1-z)^{2}$.
  - **A.4**: all 16 Bernstein coefficients are positive. Their minimum
    equals the published rational exactly.
- **A.5, with our own tails.** The paper's tails on $(0, 0.001]$ and $[8, \infty)$
  are "documented in the computational supplement", which we did not use.
  We wrote our own (docstring of `tails_1d`).
  - Small $v \le 2^{-12}$: $v + (v - v^{2}/2)\log(1/v) \le G(v) \le v + v \log(1/v)/(1-v)$,
    and $W_{0}(v) \ge 2v \log(1/2v)$. The two resulting brackets are monotone in $v$,
    and at $v = 2^{-12}$ they are 0.338 and 38.1.
  - Large $v \ge 8$: $G \le v + 1$, $G(16v) \ge 16v$, and
    $W_{0} \ge 2v - \tau_{0} + 1 - 2e^{-2v}$. The bracket is 2.10.
  - Middle $[2^{-12}, 8]$: endpoint evaluation, with $G' > 0$ and $(\sqrt{W_{0}})' > 0$
    certified on each cell.
    - $W_{0} \ge (8/5)G$: 451 cells, minimum lower bound $7.9\cdot 10^{-6}$. The true minimum
      ratio is 1.6121, at $v \approx 0.257$.
    - $G(16v) \ge (178/25)G$: 373 cells, minimum $2.0\cdot 10^{-4}$. The true minimum
      ratio is 7.1411, at $v \approx 0.132$.
  - The three scalars lie in $[2.89081907767\cdot 10^{-6}, 2.89081907856\cdot 10^{-6}]$,
    $[0.405361570566, 0.405361570567]$ and $[0.242130073052, 0.242130073053]$.
    Each is $\ge$ the published bound.
- **A.6, with our own rectangle** $Q_{1} = [5/16, 7/16] \times [-1/16, 1/16]$. The
  paper's rectangle is $\lvert t - t_{c}\rvert \le 1/20$, $\lvert d\rvert \le 1/20$.
  - Hessian PD on 1036 boxes: $F_{tt} \ge 0.0625$, $F_{dd} \ge 0.414$,
    $\det \ge 1.4\cdot 10^{-4}$ (for $m_{0}F_{0}$).
  - $m_{0}F_{0}(t_{c}, t_{c}) \in [7.02671277\cdot 10^{-9}, 7.02674996\cdot 10^{-9}]$, i.e.
    **$F_{0}(t_{c},t_{c}) \ge 1.13864\cdot 10^{-8}$** (paper: $\ge 1.1386421\cdot 10^{-8}$).
  - $\lvert\partial_{t}\rvert \le 4.4\cdot 10^{-14}$ there. Hence $F_{0} \ge 1.13864\cdot 10^{-8}$ on $Q_{1}$.
  - This is the **thinnest margin resolved by computation**. Our double
    enclosure has width $4\cdot 10^{-14}$. An independent mpmath.iv evaluation at
    200 bits agrees to $10^{-13}$ (`test_frankl.py`).
  - Negative control: lowering $\alpha_{0}$ by $10^{-8}$ makes the certified enclosure of
    $F_{0}(t_{c},t_{c})$ negative.
- **A.7, with our own dyadic cover.** $t$-regions $[2^{-11}, 1/8]$, $[1/8, 5/16]$,
  $[5/16, 7/16]$, $[7/16, 3/2]$, $[3/2, 4]$ and $[4, 17]$; $\xi \in [0, 15/17]$, with the
  clip at 15/17 rounded upward.

  | $t$-region | mean-value boxes | boxes in $Q_{1}$ | min lower bound of $m_{0}F_{0}$ | time |
  | --- | --- | --- | --- | --- |
  | $[2^{-11}, 1/8]$ | 1,215 | 0 | $5.3\cdot 10^{-7}$ (at $t \approx 2^{-11}$, $\xi \approx 0.52$) | 9 s |
  | $[1/8, 5/16]$ | 1,014 | 0 | $4.6\cdot 10^{-5}$ | 8 s |
  | $[5/16, 7/16]$ | 908 | 208 | $2.2\cdot 10^{-5}$ | 9 s |
  | $[7/16, 3/2]$ | 1,050 | 0 | $7.8\cdot 10^{-5}$ | 8 s |
  | $[3/2, 4]$ | 960 | 0 | 0.108 | 6 s |
  | $[4, 17]$ | 10,176 | 0 | $1.2\cdot 10^{-3}$ | 64 s |

  In total, 15,323 boxes certified positive and none unresolved. The paper
  reports 666 cells with minimum $5.2\cdot 10^{-8}$. Our cover is finer because our
  derivative enclosures are cruder.
- **Numerics needed for large $t$.** At $t$ up to 17, $e^{-2t} \approx 10^{-15}$, and the
  naive $(1-x)\log(1-x)$ loses all relative accuracy. The new module evaluates
  $G = u + (1-x)S(x)$, $G' = S(x)$, $G'' = S(x) - 1/(1-x)$, with
  $S(x) = -\log(1-x)/x$, and $H(p) = p(\log(1/p) + (1-p)S(p))$ for $p \le \tfrac{1}{4}$. For
  $x \le \tfrac{1}{4}$, $S$ is the series $\sum x^{k}/(k+1)$ with a geometric tail bound. All of
  this is checked against mpmath at 120 digits for $u$ up to 128.
- **Tests.** `test_frankl.py::test_costa_sadhu_thm12` runs the exact
  pieces, A.5 and A.6, the 200-bit mpmath.iv contact value, and the
  derivative formulas against 40-digit finite differences. It also runs two
  negative controls: the $\alpha_{0} - 10^{-8}$ contact value, and the false $W_{0} \ge 1.62 G$,
  which the 1D prover rejects.

**Label: $c_{\mathrm{UC}} \ge 0.3828852549667978$ (Costa–Sadhu Thm 1.2): all finite
computations re-verified independently (own interval code, own tails, own
local rectangle, own cover); analytic steps read, not machine-checked.**

- Read but not machine-checked *at the time of Approach 4*: Lemma 6.1's case
  analysis (with Lemmas 4.1 and 4.4), the $W_{0}$-monotonicity argument, Cases 1–3
  of Lemma 6.2 and the reduction to the compact region, Prop. 6.3, Lemma 2.1,
  and Liu's Prop. 3 (read only as Costa–Sadhu restate it). **All but the last
  three are now machine-checked in Approach 6. Liu's Prop. 3 has been read
  in Liu's own text (Approach 6).**
- We found no error. One presentational point: the tails of A.5 live only
  in the Zenodo supplement, not in the paper. We supplied our own.

### 5. Independent re-verification of Jiang's 0.38288525 (arXiv:2609.08291)

Source: arXiv v1 LaTeX, §§2–8 and Appendices A–B **[read]**. Parameters are
exact rationals: $m = 2468459/4\cdot 10^{6}$ (so $1 - m = 1531541/4\cdot 10^{6}$), $w_{0} = 0.8102221$,
$w_{4} = 0.1897779$, $A = 0.716$, $B = 0.721$, $z = 181/256$, $\sigma = 0.99999999$, and a
rational centre $x^{*} = 0.690908$. Exactly, $k_{0} = mw_{0} = 20000000347439/4\cdot 10^{13}$,
so $k_{0} - \tfrac{1}{2} = 8.69\cdot 10^{-9}$.

- **Reduction** (Prop. "Entropy reduction", analytic). The kernel is
  $K(x,y) = h(xy + a(x)a(y)(\min(x,y) - xy))$. This is Liu's Example 4, a
  shared-uniform rule, with $a = 1$ on $[0, \tfrac{1}{2}]$, $a = \sqrt{(1-2x^{2})/(2x(1-x))}$ on
  $(\tfrac{1}{2}, 1/\sqrt{2})$, and $a = 0$ above. If (K) $K \ge \psi(x)\psi(y)$ and
  (M) $2m[w_{0}h(xy) + w_{4}\psi(x)\psi(y)] \ge xh(y) + yh(x)$, then $p \ge 1 - m$. The proof
  is self-contained: it uses conditional independence given the shared
  history, not Liu's $C_{3}$ closure.
- **Profile.** $\psi$ is explicit and piecewise: $\varphi = \sigma\sqrt{D h/h(x^{*})} e^{E}$ below $A$,
  $s = \sqrt{h(x^{2})}$ above $B$, and a linear blend on $[A, B]$. Here $D$ is piecewise
  ($h$, then $\ln 2$, then a scaled $h(x^{2})$), and $E$ is quadratic.
- **Finite computations.** These are Python `decimal` at 35 digits with
  outward rounding (code in Appendix B).
  1. Twelve scalar signs, among them $E'(1) > 0$, $C_{g}C_{t} < 1$, $2C_{b}P_{0} < 1$,
     $A - s(A)C_{b} > 0$, $s(A) > \varphi(A)$, $k_{0} > \tfrac{1}{2}$, the small-$t$ bracket
     $2mw_{4}(1 - \ln 4T) - 1 > 0$ at $T = 0.001$, $e^{-2T} > B$, and $16mw_{4}C^{2} > \tfrac{1}{2}$.
  2. The **bridge** $h(Ay) \ge s(A)\varphi(y)$ on $[1/16, A]$: a 1D mean-value cover.
  3. The **kernel** $K \ge \varphi(x)\varphi(y)$ on $[1/16, 15/16]^{2}$: six parameter squares
     built from three coordinate maps. The middle map, through $t = a(x)$,
     avoids the $\sqrt{\cdot}$ singularity of $a$ at $1/\sqrt{2}$.
  4. The **mixture** $F(t,\xi) = mw_{0}G(2t) + mw_{4}P(u)P(v) - (G(u)+G(v))/2 > 0$ on
     $[0.001, 16] \times [0, 1]$: nine $t$-strips and a mean-value cover. Near $\xi = 1$
     $(v \to 0)$ it uses two analytic edge bounds instead of derivatives,
     (edge1) $F \ge (k_{0}-\tfrac{1}{2})G(2t) - \tfrac{1}{2}G(v)$, and (edge2) $F \ge (k_{0}-\tfrac{1}{2})G(2t)$ when
     $v \le -\ln B$ and $G(v) \le [2mw_{4}C\cdot G(t)]^{2}$.
- **Analytic pieces.** The ceiling (Prop. "Limitation"); geometric
  concavity $h(xy) \ge s(x)s(y)$; profile ordering $\varphi \le \psi \le s$ on $[A, 1]$; the
  lower and upper strips of (K); small $t \le 0.001$ and large $t \ge 16$ for (M).
- **Differences from Costa–Sadhu.**
  - Kernel: Liu's Example 4 instead of Example 5.
  - Lemma (K): checked by a 2D interval cover here. In Costa–Sadhu it is
    analytic plus an exact Bernstein certificate.
  - $y \to 1$ edge: Jiang's mixture function **does** touch the
    $k_{0} - \tfrac{1}{2} = 8.7\cdot 10^{-9}$ margin. It is handled by the analytic edge bounds
    inside the cover. Costa–Sadhu stay away from it via their Case 1.
  - Arithmetic: Decimal instead of MPFR.
  - Jiang also has an analytic finite-$N$ global-coupling gain, which tends
    to 0.

#### What we re-computed (`computations/frankl/jiang_checks.py`, `results/jiang.txt`)

All of this is our own code: outward-rounded doubles, with the accurate
G/H evaluation from Approach 4. It is not Jiang's Decimal program. Every
rational parameter is entered exactly.

- **Exact rationals.**
  - $w_{0} + w_{4} = 1$ and $1 - m = 1531541/4\cdot 10^{6}$.
  - $k_{0} - \tfrac{1}{2} = 347439/4\cdot 10^{13}$.
  - $1/2 < z < 1/\sqrt{2} < A$ (as $2z^{2} < 1 < 2A^{2}$), and $z^{2} + z > 1$.
- **The 12 scalar signs.** All are positive. The smallest is
  $k_{0} - \tfrac{1}{2} \in [8.685974939\cdot 10^{-9}, 8.68597505\cdot 10^{-9}]$. The next smallest are
  $s(A) - \varphi(A) \ge 1.63\cdot 10^{-3}$ and $1 - 2C_{b}P_{0} \ge 0.0271$.
- **Bridge** on $[1/16, A]$: 68 cells, minimum lower bound $4.6\cdot 10^{-6}$.
- **Kernel** on $[1/16, 15/16]^{2}$, using our own implementation of the three
  coordinate maps ($x(p) = 1/(p^{2} + \sqrt{(p^{2}-1)^{2} + 1})$, so that $a(x(p)) = p$).
  The proven range $xy \le r \le \min(x,y)$ is intersected in.

  | maps | boxes | min lower bound | time |
  | --- | --- | --- | --- |
  | (low, low) | 64 | 0.022 | 0.3 s |
  | (low, mid) | 64 | $1.0\cdot 10^{-4}$ | 0.4 s |
  | (low, high) | 64 | $3.3\cdot 10^{-3}$ | 0.4 s |
  | (mid, mid) | 897 | $1.4\cdot 10^{-10}$ (at $x \approx y \approx x^{*}$) | 10 s |
  | (mid, high) | 147 | $5.3\cdot 10^{-7}$ | 1.6 s |
  | (high, high) | 70 | $1.2\cdot 10^{-4}$ | 0.4 s |

  The true kernel gap at $(x^{*}, x^{*})$ is exactly $\ln 2\cdot(1 - \sigma^{2}) = 1.386\cdot 10^{-8}$,
  because $r(x,x) = \tfrac{1}{2}$ on $[\tfrac{1}{2}, 1/\sqrt{2}]$ and $\varphi(x^{*})^{2} = \sigma^{2} \ln 2$. Our enclosure is
  $[1.38629304\cdot 10^{-8}, 1.38629528\cdot 10^{-8}]$. Negative control: raising $\sigma$ by a
  factor $1 + 2\cdot 10^{-8}$ gives a certified negative gap there.
- **Mixture** on $[0.001, 16] \times [0, 1]$: nine $t$-strips; the edge bounds
  (edge1, edge2) are used next to $\xi = 1$.

  | $t$-strip | boxes (by edge bound) | min lower bound | time |
  | --- | --- | --- | --- |
  | $[0.001, 0.01]$ | 169 (23) | $1.3\cdot 10^{-10}$ (edge2) | 1.6 s |
  | $[0.01, 0.1]$ | 178 (21) | $8.6\cdot 10^{-10}$ (edge2) | 2.0 s |
  | $[0.1, 0.3]$ | 229 (10) | $5.0\cdot 10^{-9}$ (edge2) | 3.6 s |
  | $[0.3, 0.5]$ | 3,051 (4) | **$1.8\cdot 10^{-11}$** (mean value, $t \approx 0.3705$, $\xi \approx 4\cdot 10^{-4}$) | 57 s |
  | $[0.5, 1]$ | 359 (3) | $1.6\cdot 10^{-8}$ | 6.4 s |
  | $[1, 2]$ | 181 (4) | $2.5\cdot 10^{-8}$ | 2.8 s |
  | $[2, 4]$ | 82 (3) | $4.3\cdot 10^{-8}$ | 0.9 s |
  | $[4, 8]$ | 55 (3) | $7.8\cdot 10^{-8}$ | 0.6 s |
  | $[8, 16]$ | 53 (2) | $1.5\cdot 10^{-7}$ | 0.5 s |

  - **Two thin spots, both resolved.**
    - The diagonal near $x^{*}$: $F(-\log x^{*}, 0) \approx 1.105\cdot 10^{-8}$, reflecting
      $C^{*} - c_{0} \approx 10^{-8}$. Our point enclosures there have width $\approx 4\cdot 10^{-14}$,
      and the weakest mean-value box still clears zero by $1.8\cdot 10^{-11}$, about
      400 times the rounding width.
    - The $\xi \to 1$ edge, where the edge bounds certify $(k_{0} - \tfrac{1}{2})G(2t)$, down to
      $1.3\cdot 10^{-10}$.
  - Negative control: lowering $k_{0}$ by $2\cdot 10^{-8}$ makes the certified value at
    the diagonal point negative.
- **Tests.** `test_frankl.py::test_jiang` checks the kernel gap, its two
  partial derivatives, $P, P'$ and the mixture value and derivatives against
  40-digit mpmath models of Jiang's definitions, written separately from
  `jiang_checks.py`.

**Label: $c_{\mathrm{UC}} \ge 0.38288525$ (Jiang): all finite computations re-verified
independently (own interval code and own covers, same decomposition of the
domain); analytic steps read, not machine-checked.** *(Superseded: the
analytic steps are now machine-checked in Approach 7.)*

- Read but not machine-checked *at the time of Approach 5*: the reduction, geometric concavity, profile
  ordering, the lower/upper strips, small $t \le 0.001$, large $t \ge 16$, and the
  two edge estimates.
- We reused Jiang's *decomposition* (the strip/square split, the coordinate
  maps and the edge bounds), but none of his code.
- We found no error. Neither record bound has been refereed. The two
  constructions are genuinely different (Liu's Example 5 vs Example 4), and
  both are now checked.

### 6. Machine-checking the analytic glue of Costa–Sadhu Thm 1.2

Goal: check by machine as much as practical of the steps of Approach 4 that
were only read: Lemma 6.2 Cases 1–3 and the residual region, Lemmas 4.1 and
4.4, Lemma 6.1's case analysis, $W_{0}$ monotonicity, Prop. 6.3. Source:
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
    arithmetic (`sympy.cancel`). Every $\log(\cdot)$ atom is first replaced by an
    independent symbol, so nothing transcendental is left to sympy's
    heuristics, and an identity that holds with the logs as free symbols holds
    a fortiori.
  - **sturm.** An exact Sturm root count over $\mathbb{Q}$.
  - **z3.** The negated implication is unsat over the reals (nonlinear real
    arithmetic, exact rationals). The hypotheses fed to z3 are exactly the
    facts proved by the other checks. Since Approach 7, z3 first shows the
    hypotheses satisfiable (non-vacuity guard). All of this approach's
    calls pass it.
  - **interval.** `interval.py`.
  - **hand.** A standard analysis fact that we state but do not formalise:
    Taylor bounds with positive terms; "$f(0) = 0$ and $f' > 0 \Rightarrow f > 0$" (MVT);
    FTC/Tonelli; Jensen; weak limits; continuity at the boundary.
- **Code.** `computations/frankl/analytic_glue.py`, output in
  `results/analytic_glue.txt`: 26 claims, 15 s. Test:
  `test_frankl.py::test_analytic_glue`. It runs all claims plus negative
  controls showing each tool can fail:
  - a false log identity $(G' = S + x)$ is rejected;
  - a Sturm count with roots present is correct;
  - z3 refuses four false variants, namely Case 1 with 7.11 in place of
    178/25, Case 3 with $6 \log 2$ in place of $8 \log 2$, $\xi < 14/17$ in place of
    15/17, and the residual region without "not Case 3".

Notation as in Approach 4. In addition, $S(x) := -\log(1-x)/x$, $x = e^{-u}$.

#### $G$ facts (used by 4.4 and 6.2) — closed form instead of the paper's series

- **Statement.** $G(u) = u + (1-x)S(x)$, $G'(u) = S(x)$, $G''(u) = S(x) - 1/(1-x)$.
  On $(0, \infty)$: $G' > 1$, $G'' < 0$, $G(u) - u < 1$, $-G''(u) < 1/(e^{u}-1) < 1/u$, and
  $G(0+) = 0$.
- **Reduction.**
  - The three formulas are derivatives of $H(x)/x$ under $d/du = -x\, d/dx$
    (sympy-exact). sympy also sums $\sum x^{k}/(k(k+1)) = 1 + (1-x)\log(1-x)/x$, so
    the closed form agrees with the paper's series (Lemma 5.2).
  - $S > 1$ because $f = -\log(1-x) - x$ has $f(0) = 0$ and $f' = x/(1-x) > 0$.
  - $\psi(x) := x + (1-x)\log(1-x)$ has $\psi(0) = 0$ and $\psi' = -\log(1-x) > 0$. The
    identities $G'' = -\psi/(x(1-x))$, $G - u = 1 - \psi/x$ and
    $-G'' - x/(1-x) = 1 - S$ (sympy-exact) then give the three signs.
- **Label:** sympy-exact + hand (MVT, twice).

#### Lemma 4.1: $-\Lambda''/\Lambda' > 1/u + 1/(1-u)$ on $(0, \tfrac{1}{2})$, $\Lambda = \log H$

- **Reduction.**
  - (a) $-\Lambda''/\Lambda' - 1/u - 1/(1-u) = N/(u(1-u)\lambda H)$, where
    $N = q(1-\lambda) + u\lambda(1-u\lambda)$, $\lambda = \log((1-u)/u)$, $q = -\log(1-u)$, $H = u\lambda + q$ and
    $H' = \lambda$ (sympy-exact). The denominator is $> 0$ because $\lambda > 0$ on $(0, \tfrac{1}{2})$.
  - (b) $q \le u/(1-u)$: $f = u/(1-u) + \log(1-u)$ has $f(0) = 0$ and
    $f' = u/(1-u)^{2}$ (sympy + MVT).
  - (c) The algebra
    $(u/(1-u))(1-\lambda) + u\lambda(1-u\lambda) = (u/(1-u))(1 - u\lambda(\lambda+1) + u^{2}\lambda^{2})$ (sympy-exact). Also $u = 1/(1+e^{\lambda})$.
  - (d) $1 - \lambda^{2}/2 + \lambda^{3}/6 > 0$ on $[1, \infty)$: no root by an exact Sturm count;
    the minimum is 1/3 at $\lambda = 2$. With the Taylor bound
    $e^{\lambda} > 1 + \lambda + \lambda^{2}/2 + \lambda^{3}/6$ (hand) this gives $u\lambda(\lambda+1) < e^{-\lambda}\lambda(\lambda+1) < 1$.
  - (e) $N > 0$ in both cases, $\lambda \le 1$ and $\lambda > 1$: z3, from (b) and (d).
- **Cross-check** (not needed for the proof): $N(u)/u > 0$ on $[2^{-40}, \tfrac{1}{2}]$ by 624
  interval cells; the minimum lower bound is 0.42.
- **Label: machine-checked** (sympy-exact + Sturm + z3), with two hand steps
  (a Taylor bound and one MVT).

#### Lemma 4.4: $M = uH'/H$ is strictly decreasing on $(0, 1)$

- **Reduction.**
  - With $H$ an abstract function, $d/dv\, \log H(e^{-v}) = -M(e^{-v})$ and
    $d^{2}/dv^{2} \log H(e^{-v}) = e^{-v}M'(e^{-v})$ (sympy-exact).
  - $\log H(e^{-v}) = -v + \log G(v)$, and
    $(\log G)'' = G''/G - (G'/G)^{2} < 0$ by $G'' < 0$ and $G > 0$.
  - Hence $M' < 0$ pointwise.
- **Wording point, not a gap.** The paper says "strict concavity makes this
  quantity negative". Strict concavity alone does not give a negative second
  derivative everywhere (think of $-x^{4}$ at 0). But the paper's previous display
  already proves $(\log G)'' < 0$ pointwise, which is what is used.
- **Cross-check:** the numerator $K = (\lambda - 1/(1-u))H - u\lambda^{2}$ of $M' = K/H^{2}$ is
  $< 0$ on $[2^{-40}, 1 - 2^{-40}]$ (11,493 interval cells).
- **Label: machine-checked** (sympy-exact), with $G$ facts as above.

#### Lemma 6.1: $H(r(x,y))^{2} \ge H(g(x))H(g(y))$ — the case analysis

- **Reduction.**
  - (a) $r_{x}$, $r_{y}$, $r_{xy}$, the identity $W r_{xy} - r_{x} r_{y}/(xy) = \tau_{0}xy$, and
    $r_{xy}/(r_{x} r_{y}) = 1/r + \tau_{0}/(WUV)$, where $r_{x} = yU$ and $r_{y} = xV$
    (sympy-exact).
  - (b) On $[0,1]^{2}$: $W \ge 1$ and $U, V \ge 1 - \tau_{0} > 0$ (z3). Also
    $g' \ge 2x(1 - \tau_{0}/8)$ via $(1-x)(1-2x) + 1/8 = 2(x - \tfrac{3}{4})^{2}$, the exact value of
    $g(45/64) - \tfrac{1}{2}$, $g \ge z^{2}$, and $g(1) = 1$.
  - (c) **A.4 by a second method.** We solve the $16\times 16$ monomial linear
    system for the Bernstein coefficients, instead of using the
    degree-elevation formula of Approach 4. All 16 are $> 0$, and the minimum is
    the published rational.
  - (d) With $\Lambda$ and $H$ abstract: $\partial_{y}\Delta_{x} = L_{2}(x,y) - L_{2}(y,y)$;
    $L_{12} = \Lambda''(r)r_{x} r_{y} + \Lambda'(r)r_{xy}$; $L_{2} = (r_{y}/r)M(r)$ with
    $r_{y}/r = 1/y - \tau_{0}(1-x)/(1+\tau_{0}(1-x)(1-y))$; and
    $a \mapsto \tau_{0}a/(1+\tau_{0}a(1-y))$ has derivative $\tau_{0}/(1+\tau_{0}a(1-y))^{2} > 0$. All
    sympy-exact.
  - (e) **Case logic** (z3).
    - Case A: $P(\rho + \ell) < 0$ from $P > 0$, $\rho \le 1/r + 1/(1-r)$ and
      $\ell < -1/r - 1/(1-r)$. These hypotheses come from (a), A.4 and Lemma 4.1;
      the last applies because $0 < r(s,y) \le g(y) < \tfrac{1}{2}$.
    - Case B: $A_{x} M(r) > A_{y} M(g)$ from $0 < A_{x} < A_{y}$, $M > 0$ below $\tfrac{1}{2}$,
      $M \le 0$ above $\tfrac{1}{2}$, and $M$ decreasing.
  - Hand steps: $\Delta_{x}(x) = 0$ plus the FTC in $s$ and in $y$, and continuity at the
    boundary.
- **Label: machine-checked**, except the FTC and continuity steps.

#### $W_{0}$ is increasing

- **Reduction.**
  - With $H$ abstract, $W_{0}'(v) = (2H(q) - z q_{z} H'(q))/z^{2}$, where $q = g(z)$ and
    $z = e^{-v}$.
  - $z q_{z} = 2q - 2\tau_{0}z^{3}(1-z)$ and $H(q) - qH'(q) = -\log(1-q)$. Hence
    $z^{2}W_{0}' = -2\log(1-q) + 2\tau_{0}z^{3}(1-z)H'(q)$.
  - $H'(q) - \log(1-q) = -\log q$.

  All of these are sympy-exact. Then:
  - $z^{3}(1-z) \le 27/256$, by the exact factorisation in Approach 4, so
    $c := 2\tau_{0}z^{3}(1-z) < 2$.
  - The sign skeleton is checked by z3: with $A = -\log(1-q) > 0$,
    $H' \ge 0$ for $q \le \tfrac{1}{2}$ and $H' \ge -A$ for $q > \tfrac{1}{2}$, we get $2A + cH' > 0$.
- **Label: machine-checked.** The interval check of $(\sqrt{W_{0}})' > 0$ on
  $[2^{-12}, 8]$ in Approach 4 is an independent confirmation there.

#### Lemma 6.2: $F_{0}(s,\sigma) > 0$ for $0 < s \le \sigma$

- **(a) Reduction** (sympy-exact):
  - Divide (6.tuned-second) by $2xy$, with logs of $x, y, 1-x$, $1-y$ and $1-xy$ as
    free symbols. This gives $F_{0} = \alpha_{0}G(s+\sigma) - (G(s)+G(\sigma))/(2m_{0}) + \beta_{0}P$ with
    $P = \sqrt{W_{0}(s)W_{0}(\sigma)}$.
  - Then $F_{0} = G(u)/8\cdot 10^{8} - D/(2m_{0}) + \beta_{0}P$.
- **(b)** $D \le G(s) - s < G(s)$ and $D < 1$ (z3 skeleton). The inputs are
  $G(s+\sigma) - G(\sigma) \ge s$ (MVT with $G' > 1$) and $G(s) - s < 1$. *Our route differs
  from the paper's*, which compares series term by term. Both are valid.
- **(c) Case 1, $G(\sigma) \ge (178/25)G(s)$.** This is the $y \to 1$ ($s \to 0$) edge.
  - **Exact certificate** (sympy-exact):
    $F_{0} - [G(u)/8\cdot 10^{8} + c_{1}G(s)] = (G(s) - D)/(2m_{0}) + \beta_{0}(P - (8/5)Q)$
    $+ (8\beta_{0}/5)(Q - kG(s))$, where $Q = \sqrt{G(s)G(\sigma)}$ and $k = \sqrt{178}/5$. Each bracket
    is $\ge 0$ by (b) and A.5; the first is $> 0$.
  - **The margin $c_{1} = (8\beta_{0}/5)k - 1/(2m_{0}) > 0$ is now proved in exact rational
    arithmetic.** We show $(8\beta_{0}\sqrt{178}/25)^{2} > (1/(2m_{0}))^{2}$, and, with a rational
    lower bound for $\sqrt{178}$, $c_{1} \ge 2.89081907812\cdot 10^{-6}$ (paper: $\ge 2.8908190756\cdot 10^{-6}$).
    Before this session it was an interval enclosure.
  - z3 also proves the whole implication without square roots, using
    $P^{2} \ge (64/25)(178/25)G(s)^{2}$.
  - The $7.7\cdot 10^{-10}$ margin $m_{0}\alpha_{0} - \tfrac{1}{2} = m_{0}/8\cdot 10^{8}$ is never needed: the
    $G(u)/8\cdot 10^{8}$ term is only dropped (it is $> 0$).
- **(d) Case 2, $s, \sigma \ge 2$.**
  - Certificate: $F_{0} - [G(u)/8\cdot 10^{8} + (\beta_{0}W_{0}(2) - 1/(2m_{0}))]$
    $= (1-D)/(2m_{0}) + \beta_{0}(P - W_{0}(2))$ (sympy-exact). $P \ge W_{0}(2)$ because $W_{0}$ is
    increasing.
  - The scalar $\beta_{0}W_{0}(2) - 1/(2m_{0}) \ge 0.4053615705664$ is transcendental. It is
    interval-verified (`interval.py`), and independently by Arb at 200 bits;
    the two agree to $10^{-12}$.
  - z3 skeleton.
- **(e) Case 3, $s, \sigma \le 2^{-10}$.**
  - sympy evaluates $\int_{0}^{s}\int_{0}^{\sigma} db da/(a+b) = (s+\sigma)\log(s+\sigma) - s \log s - \sigma \log \sigma$
    $= uH(\lambda)$ (exact, logs as symbols). The mixed derivative of
    $G(a) + G(b) - G(a+b)$ is $-G''(a+b)$.
  - The rest is identities (sympy-exact): $e^{2w}(1 - g(e^{-w})) =$
    $e^{2w} - 1 - \tau_{0}(1-e^{-w})^{2}$ (an identity in $z = e^{-w}$),
    $\sqrt{s\sigma} = u\sqrt{\lambda(1-\lambda)}$, and $A + B - 1 - AB = -(1-A)(1-B)$ (for
    $H(\lambda) \le 2\sqrt{\lambda(1-\lambda)}$).
  - z3 skeletons: $e^{2w}r_{w} \ge 2w$, from $e^{2w} \ge 1 + 2w + 2w^{2}$ and
    $0 \le 1 - e^{-w} \le w$; and the final step, from $D < uH(\lambda)$, $H(\lambda) \le 2R$,
    $P \ge 2uR \log(1/2u)$ and $\log(1/2u) \ge 8 \log 2$.
  - The final certificate $F_{0} - [G(u)/8\cdot 10^{8} + 2uR(\beta_{0} \log(1/2u) - 1/(2m_{0}))] =$
    $(uH - D)/(2m_{0}) + \beta_{0}(P - 2uR \log(1/2u)) + u(2R - H)/(2m_{0})$ is sympy-exact.
  - **The scalar $8\beta_{0} \log 2 - 1/(2m_{0}) \ge 0.2421300730523$ is now proved
    exactly.** It uses the rational lower bound for $\log 2$ from the atanh
    series, which Arb confirms lies below $\log 2$.
  - Hand steps:
    - the FTC/Tonelli representation $D = -\int\int G''$. It is improper at 0, since
      $G'(v) \sim \log(1/v)$, but valid because $G$ is continuous at 0 with $G(0) = 0$
      and $G'$ is integrable there;
    - $\log t \le t - 1$;
    - $e^{t} \ge 1 + t + t^{2}/2$.

    A cross-check of $H(\lambda) \le 2\sqrt{\lambda(1-\lambda)}$ on $[1/4096, \tfrac{1}{2}]$ in 2047 interval cells
    gives a minimum gap of 0.027.
- **(f) Residual region** (z3). From $0 < s \le \sigma$, not Case 1, not Case 2, not
  Case 3, A.5 at $v = s$ ($G(16s) \ge (178/25)G(s)$) and $G$ increasing, z3 derives
  $2^{-11} < t < 17$ and $\xi < 15/17$. The bound on $\xi$ is stated as
  $17(\sigma-s) < 15(\sigma+s)$. It also derives the paper's intermediate bounds
  $2^{-14} < s < 2$ and $2^{-10} < \sigma < 32$. That region is covered by A.6 + A.7
  (Approach 4, our own rectangle and cover).
- **Label: machine-checked**, given A.5–A.7 (certificate-checked in
  Approach 4), with the hand steps listed in (b) and (e). Symmetry and
  boundary continuity are also hand steps.

#### Prop. 6.3 and the theorem

- **Checked** (exact rationals + z3): $\alpha_{0} + \beta_{0} = 1$, $0 < \alpha_{0}$, $\beta_{0} < 1$,
  $2m_{0}(1 - 1/8\cdot 10^{8}) > 1$, $1 - m_{0} = 0.3828852549667978$, and $\gamma = (1-c)/m_{0} > 1$
  for $0 < c < 1 - m_{0}$. Also the finite Jensen identity
  $\sum\lambda_{i}a_{i}^{2} - (\sum\lambda_{i}a_{i})^{2} = \sum\lambda_{i}(a_{i} - \bar{a})^{2}$, checked for $n = 3$, which is Lemma 2.1
  before the weak limit.
- **Sanity test (not a proof).** Prop. 6.3's inequality is certified by
  interval arithmetic on 200 random finitely supported $P$, with $\rho$ a finite
  mixture of $Q\otimes Q$ (so $\rho \in C_{3}(P)$), and on a point mass at $e^{-t_{c}}$.
  Negative control: raising $1/m_{0}$ by $10^{-7}$ makes the point-mass instance
  certifiably negative.
- **Liu's Prop. 3, now read in Liu's own text.** Source: arXiv:2306.08824
  LaTeX, §2 (Def. of protocol, eq. (16), Prop. 3, Def. 2, Examples 4–5,
  the definition of $C_{3}$) **[read]**. Costa–Sadhu's restatement is faithful in
  three respects:
  - Weights $w_{k} \ge 0$ sum to 1. There is a fixed $C > 1$. The condition is
    imposed for every $\mu$ with mean $\le c$, and the inf is over sets $C_{k}(\mu)$
    "large enough to contain all couplings … induced by the $k$-protocol".
  - The conclusion is "$c$ is a lower bound for the constant".
  - The only difference is the log base: Liu uses bits, Costa–Sadhu use
    nats. Both sides of (16) scale by the same factor, so nothing changes.

  Liu's proof is four lines: the chain rule as in Gilmer, plus "uniform
  maximises entropy". We read it and it is correct. It needs $H(X^{n}) > 0$, i.e.
  $\lvert F\rvert \ge 2$, which the definition of $c_{\mathrm{UC}}$ provides.

  Liu's Example 5 is the following protocol: $X = 0$ with probability
  $\bar{s} \pm f(\bar{s})$, the sign set by $U \lessgtr \tfrac{1}{2}$. Its formula $\Pi_{s,t}(0,0) = \bar{s}\bar{t} + f(\bar{s})f(\bar{t})$,
  the marginal $P(X=0) = \bar{s}$, and the specialisation to $r_{\ell}$ are sympy-exact.
  Admissibility of $f_{\ell}$ for $0 \le \ell \le 1$ is checked by z3 (claim L.ex5).
- **Read only.** Integration against $P\otimes P$ (Fubini); Lemma 2.1's weak limit;
  the reflection argument ($C_{3}$ is preserved by $x \mapsto 1-x$); Liu's argument that
  conditionally-iid protocols induce laws in $C_{3}$ ($X^{i}$, $Y^{i}$ are conditionally
  iid given $U^{i}$). These are measure theory, not computations.

#### Outcome

| step | method | status |
| --- | --- | --- |
| $G$ facts $(G' > 1, G'' < 0, G - u < 1, -G'' < 1/u)$ | sympy-exact + MVT | machine-checked (MVT by hand) |
| Lemma 4.1 | sympy-exact + Sturm + z3 (+ interval cross-check) | machine-checked (Taylor bound, MVT by hand) |
| Lemma 4.4 | sympy-exact (+ interval cross-check) | machine-checked |
| Lemma 6.1 identities, A.4 (second method), positivity | sympy-exact + z3 | machine-checked |
| Lemma 6.1 case analysis (Cases A, B) | z3 on sympy-checked inputs | machine-checked (FTC, continuity by hand) |
| $W_{0}$ increasing | sympy-exact + z3 | machine-checked |
| Lemma 6.2 reduction, $D$ bounds | sympy-exact + z3 | machine-checked (MVT by hand) |
| Lemma 6.2 Case 1 ($y \to 1$ edge) | sympy certificate + **exact** margin $c_{1} \ge 2.89\cdot 10^{-6}$ + z3 | machine-checked, given A.5 |
| Lemma 6.2 Case 2 | sympy certificate + z3 + interval + Arb | machine-checked, given A.5 |
| Lemma 6.2 Case 3 | sympy (integral, identities) + **exact** scalar + z3 | machine-checked (FTC/Tonelli, two elementary bounds by hand) |
| Lemma 6.2 residual region $\to$ A.6/A.7 | z3 | machine-checked |
| Prop. 6.3 arithmetic, $\gamma > 1$ | exact + z3 | machine-checked |
| Liu's Prop. 3 vs Costa–Sadhu's restatement; Liu's Example 5 formula | read in Liu's LaTeX; formula sympy-exact + z3 | restatement faithful; formula machine-checked |
| Prop. 6.3 measure theory, Lemma 2.1 limit, $C_{3}$ membership of induced laws | — | read only |

Also a **statement-level stress test** (claim 6.x; numerical, not a proof).
In 40-digit mpmath, Lemma 6.1 and Lemma 6.2 were evaluated at 3000 random
points each. $s$ and $\sigma$ were drawn log-uniformly in $[10^{-12}, 60]$, so every Case
region and the residual region is hit, plus near-diagonal and near-contact
points. The minima are $(H(r)^{2} - H(g(x))H(g(y)))/(x-y)^{2} \ge 9.6\cdot 10^{-6}$ and
$F_{0}/G(s+\sigma) \ge 7.85\cdot 10^{-9}$ (the latter at the contact point).

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
  - `logsub` replaces each $\log(\cdot)$ atom by an integer combination of symbols.
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
    prefactor $1 + x^{2}$ instead of $1 - x^{2}$, and $h^{2}q'$ with the sign of $h/(1-x)$
    flipped. `logsub` refuses an unlisted log factor.
  - z3 refuses seven weakened skeletons and one vacuous one:
    - lower strip with $2C_{b}P_{0} < 1.01$;
    - upper strip with $C_{t}C_{g} < 1.01$;
    - small $t$ with the bracket $\le 0$;
    - large $t$ with $t \ge 8$ instead of 16;
    - edge2 without $v \le -\ln B$;
    - the mixed case of (K) without the bridge;
    - the reduction with $p = \min p_{i}$ instead of max;
    - and the vacuity guard rejects unsatisfiable hypotheses.
  - Arb certifies three scalars **negative** under a changed parameter:
    $T = 1/10$ in the small-$t$ bracket, 8 in place of 16 at large $t$, and
    $\sigma$ raised by 1% in $s(A) - \varphi(A)$. interval.py also certifies the
    $T = 1/10$ bracket negative.
  - The reduction-instance test (R.x below) shows that the family
    $\{\emptyset, \{1\}\}$ violates the chain at $m = 0.55$.

#### Reduction (Prop. "Entropy reduction", §3)

- **R.1 (sympy-exact).** With $Q_{U}(x) = x + a(x)(1[U\le x] - x)$, integrating
  piecewise over $U \in [0,1]$ gives $E Q_{U}(x) = x$ and
  $E[Q_{U}(x)Q_{U}(y)] = xy + a(x)a(y)(\min(x,y) - xy) = r(x,y)$, in both orders.
  This is eq. (Qproduct).
- **R.2 (z3).** $a \in [0,1]$ gives $Q_{U} \in [0,1]$, and $xy \le r \le \min(x,y) \le 1$.
- **R.3 (sympy-exact).** Finite forms of the two averaging steps:
  - the conditional-Jensen step is the variance identity
    $\sum\lambda_{v} c_{v}^{2} - (\sum\lambda_{v} c_{v})^{2} = \sum\lambda_{v}(c_{v} - \bar{c})^{2}$;
  - integrating $xh(y) + yh(x)$ against $P \otimes P$ gives $2(E x)(E h)$.
- **R.4 (z3).** The assembly, with three coordinates. The inputs are the
  per-coordinate bounds (ind-lower), (rule4-lower) and (M) integrated; the
  chain rule; $H(Z_{0})$, $H(Z_{4}) \le \ln N = H(X) > 0$; and $p_{i} \le p$. The output is
  $p \ge 1 - m$. With $p = \min p_{i}$ the implication fails (negative control).
- **Read only.** The chain rule; "conditioning reduces entropy"; maximum
  entropy; the induction showing that each sample of the shared-uniform rule
  has the law of $X$; and conditional independence of the two prefixes given
  the shared history. These are probability, not computation. They are the
  same kind of step as Approach 6's measure-theory layer, and simpler,
  because everything here is finite.
- **R.x (numerical sanity test of that read-only layer; not a proof).** Since
  $U_{i}$ is fresh, averaging it gives a finite pair kernel at each coordinate:
  $P(00) = r(S,T)$, $P(0\cdot) = S$, $P(\cdot 0) = T$. So the exact laws of both couplings
  are finite sums.
  - These laws were computed in 30-digit mpmath for 150 random families with
    $n \le 4$ and at most 8 sets (75 arbitrary, 75 union-closed).
  - Per coordinate they satisfy $H((Z_{0})_{i}\mid\cdot) \ge E h(ST)$ and
    $H((Z_{4})_{i}\mid\cdot) \ge E K(S,T) \ge (E \psi)^{2}$.
  - Both marginals of the shared rule are uniform on $F$.
  - $w_{0}H(Z_{0}) + w_{4}H(Z_{4}) \ge (1-p)H(X)/m$. The minimum slack, over families
    with $p < 1$, is $0.037\cdot\ln N$.
  - For union-closed $F$, $H(Z_{0}), H(Z_{4}) \le \ln N$ and $p \ge 1 - m$.

#### Ceiling (Prop. "Limitation", §4; not on the proof path of the bound)

- **C.1 (sympy-exact).** The formulas for $f'$, $f''$, $f'''$; the expansion
  $f = \tfrac{1}{2}(1-q)^{2}\ln(1-q) + \tfrac{1}{2}(1-q^{2})\ln(1+q)$; $f(q^{*}) = \tfrac{1}{2}(1-q^{*})\ln(1+q^{*})$ at the
  stationary point; $f'(\tfrac{1}{2}) = \tfrac{1}{2}\ln(4/3)$; and $f''(\tfrac{1}{2}) = 2/3 - \ln 3$.
- **C.2 (z3).** The endpoint step (E): $mw_{0} \ge \tfrac{1}{2}$. The diagonal chain to (C).
  And $f' > q(1-2q)$ on $(0, \tfrac{1}{2}]$ from the two log bounds (hand).

#### Profiles (§5): definitions, Lemma "geometric", profile order, passing to (K)

- **P.1 (exact + sympy + z3).** The parameter order
  $1/16 < \tfrac{1}{2} < z < 1/\sqrt{2} < A < B < 15/16$, plus $z^{2} + z > 1$ and $2U^{2} > 1$.
  Continuity of $a$ at $\tfrac{1}{2}$ and $1/\sqrt{2}$, $0 \le a \le 1$, continuity of $D$ at $\tfrac{1}{2}$ and $z$,
  and $\theta(A) = 0$, $\theta(B) = 1$. Also $E'' = -7/5$, so $E'(1) > 0$ gives $E' > 0$ on
  $[0,1]$ (z3). That $E$ is then increasing is a hand step (MVT).
- **G.1–G.3, Lemma "geometric" (sympy-exact + z3).**
  - The identities $h - xh' = \ell$ and $h^{2}q' = h'\ell - h/(1-x) =$
    $h'(\ell - x/(1-x)) - \ell/(1-x)$, with logs as symbols.
  - $\ell < x/(1-x)$ (MVT), and the sign skeleton for $x \ge \tfrac{1}{2}$ and $x < \tfrac{1}{2}$ (z3).
  - With $h$ abstract: $f(t) = \ln h(e^{t})$ has $f' = q(e^{t})$ and $f'' = e^{t}q'(e^{t})$, and
    $d/dx\, \ln(h(xy)/s(x)) = (q(xy) - q(x^{2}))/x$.
  - Hand: concavity at the midpoint.
  - Cross-check: $h^{2}q' < 0$ on $[2^{-10}, 1 - 2^{-30}]$ by 303 interval cells.
- **O.1–O.2, (profile-order) (sympy-exact + z3).**
  - $(\varphi/s)^{2} = \sigma^{2}\ln 2\cdot h(x)e^{2E}/(h(z^{2})h^{*})$ on $[z, 1]$.
  - $(\ln \varphi/s)' = h'/(2h) + E'$, and its derivative is
    $(h''h - h'^{2})/(2h^{2}) - 7/5 < 0$.
  - Then the convex-combination skeleton $\varphi \le \psi \le s$.
  - Hand: "$L(A) < 0$, $L'(A) < 0$, $L'' < 0 \Rightarrow L < 0$ on $[A, 1)$" (MVT twice).
  - The two scalars are checked by interval and Arb.
- **T.1, passing to (K) (z3).** All three cases, $x, y \le A$; $x, y \ge A$; and
  $x \ge A \ge y$. Inputs: (original-K), Lemma "geometric" (both parts),
  (profile-order) and (bridge), with $a = 0$ on $[A, 1]$ because $2A^{2} > 1$.

#### Kernel strips, coordinate maps, bridge (§6)

- **S.1 (sympy-exact).** The AND inequality $h(x^{2}) \le 2h(x)$ is a **grouping
  identity**:
  $2h(x) - h(x^{2}) = (1-x^{2})\cdot H_{3}((1-x)/(1+x), x/(1+x), x/(1+x))$,
  with logs of $x, 1-x, 1+x$ as symbols, which is $\ge 0$. For concavity-scaling,
  $g(c) = h(cx) - ch(x)$ has $g(0) = g(1) = 0$ and $g'' = -x/(c(1-cx)) < 0$.
  Hand: entropy $\ge 0$; a concave function with zero ends is $\ge 0$.
- **S.2.** (lower-profile), (P0) and (linear-profile).
  - $(\ln \varphi/x)' = D'/(2D) + h'/(2h) + E' - 1/x$, with $D$ abstract (sympy).
  - On $[z, 1/\sqrt{2}]$, $D'/(2D) = xh'(x^{2})/h(x^{2}) \le h'(z^{2})/h(z^{2})$, from
    $(h'/h)' < 0$ and $2z^{2} < 1$.
  - The derivative is then $< 0$ on all three pieces, given the scalar
    $1 - E'(\tfrac{1}{2}) - h'(z^{2})/h(z^{2}) > 0$ (z3).
  - Then $\varphi \le C_{b} h$ on $[0, L]$, $\varphi \le P_{0}$ on $[0, \tfrac{1}{2}]$, and $\varphi(y) \le 2P_{0}y$ on
    $[\tfrac{1}{2}, 1]$ (z3).
- **S.3, lower strip (sympy + z3).** If $y \le \tfrac{1}{2}$ then $r = x$. If $y \ge \tfrac{1}{2}$ then
  $r = xk$ with $k = y + a(y)(1-y) \in [y, 1]$. Both cases close with
  $2C_{b}P_{0} < 1$.
- **S.4, upper strip (z3).**
  - $\varphi(x) \le C_{t}x$, in squared form, from $h(x) \le h(U)$, $h(x^{2}) \le h(U^{2})$,
    $E \le E(1)$ and $x \ge U$.
  - $D/h \le 2\ln 2/h(z^{2})$ on all three pieces, using $h(z^{2}) \le \ln 2$,
    $h(z^{2}) \le 2h(z)$ and $h(y^{2}) \le 2h(y)$.
  - Then $\varphi(y) \le C_{g} h(y)$, and the chain closes with $C_{t}C_{g} < 1$.
- **S.5, middle coordinate map (sympy-exact + z3).**
  - $x(t) = 1/(t^{2} + R)$ solves $x^{2} + t^{2}x(1-x) = \tfrac{1}{2}$. This is reduced modulo
    $R^{2} = (t^{2}-1)^{2} + 1$, so $a(x(t)) = t$.
  - $x(0) = 1/\sqrt{2}$ and $x(1) = \tfrac{1}{2}$, and the derivative formula
    (coordinate-derivative) holds.
  - Every positive root for $t \in [0,1]$ lies in $[\tfrac{1}{2}, 1/\sqrt{2}]$, and $\lvert x'\rvert \le 4$.
  - Hand: IVT, so the three maps cover $[1/16, 15/16]$.
- **S.6 (z3).** The bridge on $[0, L]$ reduces to the scalar $A - s(A)C_{b} > 0$.
  The proven kernel range $1/256 \le r \le 15/16$ on the compact square is the
  intersection used by our cover.

#### Mixture (§7)

- **M.1 (sympy-exact + z3).**
  - The change of variables is $u = t(1+\xi) = -\ln x$ and $v = -\ln y$.
  - $0 < x \le y$, $xy < 1 \Rightarrow t > 0$ and $\xi \in [0, 1]$.
  - (M)/(2xy) is exactly $F$, with $h$ and $\psi$ abstract.
  - Both sides of (M) vanish at $xy = 0$ and at $x = y = 1$.
- **M.2 (sympy-exact).** $G = u - (e^{u}-1)\ln(1-e^{-u})$. The series for $G, G'$
  and $G''$ are summed by sympy, and $\sum 1/(j(j+1)) = 1$. $G' > 0$, $G'' < 0$, $G \ge u$
  and $-G'' \le 1/(e^{u}-1) \le 1/u$. This reuses Approach 6's G.1–G.2; $e^{u} \ge 1 + u$
  is a hand step.
- **M.3, (Gsmall).** $J = G + u \ln u$ has $J'' = G'' + 1/u \ge 0$ (z3), and
  $\lim J(u)/u = 1$ (sympy limit). Hand: chord slopes of a convex function.
  Cross-check: $G(u) \ge u(1 - \ln u)$ on $[2^{-8}, 64]$ by 604 interval cells.
- **M.4, (Gdeficit).**
  - The identity $G(u)+G(v)-G(u+v) = [J(u)+J(v)-J(u+v)] + (u+v)h(u/(u+v))$
    is sympy-exact, and the bracket is $\le 0$ (z3, from chord slopes).
  - $(\sqrt{p} + \sqrt{1-p})^{2} = 1 + 2\sqrt{p(1-p)}$, and $(u+v)\cdot 2\sqrt{p(1-p)} = 2\sqrt{uv}$.
  - Hand: Jensen, and $\ln(1+r) \le r$.
- **M.5, (Ptail) and $P \ge CG$.**
  - $P^{2} = G(2u)$ where $\psi = s$ (sympy).
  - $D \ge h$: $x \ge z \Rightarrow 1 - x \le x^{2} \le x$ (z3, from $z^{2} + z > 1$). Hand: $h$ on
    $[1-x, x]$ is $\ge h(x)$ (concavity and symmetry), and $h \le \ln 2$.
  - Then $\varphi \ge Ch$ and $P \ge CG$ (z3).
- **M.6, small $t \le 1/1000$ (z3 + exact).**
  - The skeleton gives $F \ge (k_{0} - \tfrac{1}{2})G(2t)$.
  - **Both scalars are now exact:**
    - $e^{-1/500} \ge 1 - 1/500 > 0.721$ (hand: $e^{-x} \ge 1 - x$);
    - $e < 2.72$ (Taylor tail, hand; Arb confirms), so $2.72^{4} < 250$ and
      $\ln 250 > 4$. Hence $2mw_{4}(1 + \ln 250) - 1 > 10mw_{4} - 1 > 0$.
- **M.7, large $t \ge 16$ (z3).** The skeleton closes with the scalar
  $16mw_{4}C^{2} > \tfrac{1}{2}$ (interval and Arb), and fails with 8 in place of 16.
- **M.8, edge bounds (z3).**
  - (edge1) holds, and so does (edge2) under $v \le -\ln B$ and
    $G(v) \le [2mw_{4}CG(t)]^{2}$. Without $v \le -\ln B$, edge2 fails.
  - The box form follows by monotonicity of $G$ (App. A, "Bounds for an
    entire edge box").
  - The claim also asserts that the edge tests in
    `jiang_checks.verify_mixture_strip` use exactly these quantities
    ($v_{\max}$, $-\ln B$ rounded down, $G(t_{-})$, $G(2t_{-})$).
- **M.9, App. A derivative formulas (sympy-exact, abstract functions).**
  - $\varphi'$ (phiprime); $s'$; $\psi'$ on $[A, B]$; $P' = \psi(x)/x - \psi'(x)$.
  - $P$ and $P'$ on the two closed-form pieces that `jiang_checks.P_all` uses.
  - $F_{t}$ and $F_{\xi}$ (eq. Ft, Fxi).
  - $r_{\alpha}$ and $r_{\beta}$ in both orders, and $\Delta_{\alpha}$, $\Delta_{\beta}$.

  Earlier, `test_jiang` had checked these only numerically against mpmath.

#### Scalars and stress test

- **SC.** All 12 scalar signs were re-evaluated in Arb at 200 bits,
  independently of `interval.py`. All are positive, and each Arb ball
  overlaps the interval.py enclosure. The smallest are:
  - $k_{0} - \tfrac{1}{2} = 8.685975\cdot 10^{-9}$ (exact rational);
  - $s(A) - \varphi(A) = 1.63498\cdot 10^{-3}$;
  - $1 - 2C_{b}P_{0} = 0.02714$;
  - $1 - C_{g}C_{t} = 0.06286$.
- **x (numerical, not a proof).** (K) and (M) were evaluated in 40-digit
  mpmath at 2000 random points each. Extra points sit near $(x^{*}, x^{*})$,
  $y \to 1$, $x \to 0$ and every breakpoint. The minima are $K - \psi\psi \ge 1.1\cdot 10^{-11}$
  (near $x \to 0$, where both sides are tiny) and (M)-gap/$(xy) \ge 2.2\cdot 10^{-8}$.

#### Outcome

| step | method | status |
| --- | --- | --- |
| Reduction: $E_{U} Q = x$, $E\, QQ = r$, $Q \in [0,1]$, $r$ range | sympy-exact + z3 | machine-checked |
| Reduction: variance step, integration of (M), assembly to $p \ge 1-m$ | sympy-exact (finite form) + z3 | machine-checked |
| Reduction: chain rule, conditioning, max entropy, law of the shared-uniform samples, conditional independence | exact finite laws on 150 random families (numerical sanity test) | read only; instances consistent |
| Ceiling (not used by the bound): $f'$, $f''$, $f'''$, $f(q^{*})$, (E), (C) | sympy-exact + z3 | machine-checked (two log bounds by hand) |
| Definitions: order of parameters, continuity of $a$, $D$, $\psi$; $E' > 0$ | exact + sympy + z3 (+ interval/Arb) | machine-checked (MVT by hand) |
| Lemma "geometric" (both parts) | sympy-exact + z3 (+ interval cross-check) | machine-checked (MVT, midpoint concavity by hand) |
| (profile-order) | sympy-exact + z3 + interval/Arb scalars | machine-checked (MVT twice by hand) |
| Passing from (original-K) to (K) | z3 | machine-checked |
| (and), (concavity-scaling) | sympy-exact (grouping identity; $g''$) | machine-checked (entropy $\ge 0$, concave-with-zero-ends by hand) |
| (lower-profile), (P0), (linear-profile) | sympy-exact + z3 + interval/Arb scalar | machine-checked (MVT by hand) |
| Lower strip, upper strip of (original-K) | sympy + z3 + interval/Arb scalars | machine-checked |
| Middle coordinate map, coverage of the square | sympy-exact + z3 | machine-checked (IVT by hand) |
| Bridge on $[0, 1/16]$; kernel range for the cover | z3 + interval/Arb scalar | machine-checked |
| Change of variables, (M)/$(2xy) = F$, boundary $xy = 0$ | sympy-exact + z3 | machine-checked |
| $G$ facts, (Gsmall), (Gdeficit) | sympy-exact + z3 (+ interval cross-checks) | machine-checked (Jensen, chord slopes, $e^{u} \ge 1+u$ by hand) |
| (Ptail), $D \ge h$, $P \ge CG$ | sympy + z3 + exact | machine-checked ($h \ge h(x)$ on $[1-x, x]$ by hand) |
| Small $t \le 0.001$ | z3 + **exact** scalars | machine-checked ($e^{-x} \ge 1-x$, Taylor tail of $e$ by hand) |
| Large $t \ge 16$ | z3 + interval/Arb scalar | machine-checked |
| (edge1), (edge2), box form, match with our cover code | z3 + source inspection | machine-checked |
| App. A derivative formulas | sympy-exact | machine-checked |
| 12 scalar signs | interval (Approach 5) + **Arb** (new) | two independent evaluations |
| Mean-value acceptance test for piecewise-$C^{1}$ functions, hull at joins | — | hand (MVT along axis-parallel segments) |

**No gap or error found in Jiang's argument.** Every step listed above was
reproduced exactly as stated in the paper. One cosmetic point: (strip-checks)
lists both $C_{b}P_{0} < \tfrac{1}{2}$ and $2C_{b}P_{0} < 1$, which are the same condition.

Nothing was Lean-verified.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| $\varphi H(x^{2}) \ge x H(x)$ on $[0,1]$, $\varphi = (\sqrt{5}-1)/2$, equality only at 0, $\varphi$, 1 (AHS Claim 1, Boppana) | certificate-checked (own outward-rounded interval arithmetic + analytic end/tangency lemmas) | `computations/frankl/verify_boppana.py` |
| $c_{\mathrm{UC}} \ge (3-\sqrt{5})/2$ | proved (AHS) given the line above; the reduction is AHS's, read and not formalised | AHS arXiv:2211.11731 |
| Frankl holds for every union-closed family on a universe of $\le 6$ elements | computationally checked (exhaustive, $n \le 6$) — already known up to 12 | `computations/frankl/frankl_enum.c`, `results/small_cases.txt` |
| Labeled counts 2, 7, 61, 2480, 1385552, 75973751474 (and the universe-$[n]$ counts) | computed; they equal Brinkmann–Deklerck | same |
| Costa–Sadhu Lemma S (2D inequality at Liu's parameter), Lemma R's Bernstein certificate, all constants | certificate-checked independently (own interval code, own cover) | `computations/frankl/costa_sadhu_checks.py`, `results/costa_sadhu_thm11.txt` |
| $c_{\mathrm{UC}} \ge c_{L} = 0.3827090879187350$… | proved in Costa–Sadhu (preprint); analytic steps read here, all computations re-certified here | same + arXiv:2610.02295 |
| Costa–Sadhu Lemma 6.1 Bernstein certificate (A.4), 1D inequalities (A.5), contact convexity (A.6, $F_{0} \ge 1.1386\cdot 10^{-8}$), compact cover (A.7) at $\ell_{0} = 1409/2000$ | certificate-checked independently (own interval code, own tails, own rectangle, own cover of 15,323 boxes) | `computations/frankl/costa_sadhu_thm12.py`, `results/costa_sadhu_thm12.txt` |
| Costa–Sadhu Thm 1.2 analytic glue: Lemmas 4.1, 4.4, 6.1 (case analysis), $W_{0}$ increasing, Lemma 6.2 Cases 1–3 + residual region, Prop. 6.3 arithmetic; Case 1 margin $c_{1} \ge 2.89\cdot 10^{-6}$ and Case 3 scalar now exact | machine-checked (sympy-exact + Sturm + z3 + interval/Arb), up to listed standard hand steps (MVT, FTC/Tonelli, Taylor bounds, continuity); not Lean | `computations/frankl/analytic_glue.py`, `results/analytic_glue.txt` |
| $c_{\mathrm{UC}} \ge 0.3828852549667978$ (Costa–Sadhu Thm 1.2) | proved in Costa–Sadhu (preprint); all computations re-certified here; analytic glue machine-checked here except the measure-theoretic integration (Prop. 6.3, Lemma 2.1) and Liu's Prop. 3 (read in Liu's own text; restatement faithful) | same + arXiv:2610.02295 |
| Jiang's 12 scalar signs, bridge, kernel (K) on $[1/16,15/16]^{2}$, mixture (M) on $[0.001,16]\times[0,1]$ | certificate-checked independently (own interval code; 1,306 kernel + 4,357 mixture boxes) | `computations/frankl/jiang_checks.py`, `results/jiang.txt` |
| Jiang analytic glue: reduction (finite forms + assembly), ceiling, Lemma "geometric", profile order, passing to (K), (and), strips, coordinate maps, bridge tail, change of variables, $G$ facts, (Gsmall), (Gdeficit), (Ptail), small $t$ (scalars now exact), large $t$, edge bounds, App. A derivative formulas; 12 scalars re-evaluated in Arb | machine-checked (sympy-exact + z3 with non-vacuity guard + interval/Arb), up to named hand steps (MVT, IVT, Jensen, concavity, Taylor bounds); probability layer read only (sanity-tested on exact finite laws of 150 random families); not Lean | `computations/frankl/analytic_glue_jiang.py`, `results/analytic_glue_jiang.txt` |
| $c_{\mathrm{UC}} \ge 0.38288525$ (Jiang) | proved in Jiang (preprint); all computations re-certified here; analytic glue machine-checked here except the probability layer of the reduction (read only) | same + arXiv:2609.08291 |

## Failed or closed routes (do not retry blindly)

- **Pushing the pointwise entropy inequality past 0.38288526.** This is
  impossible: there is a proved ceiling $C^{*}$ (Jiang Prop. "Limitation"; Costa–Sadhu
  §7). Mixing in more product kernels $\psi_{j}(x)\psi_{j}(y)$ does not help either (same
  endpoint plus diagonal argument).
- **Gilmer's Conjecture 1** (it would give 1/2) is false (Sawin; Ellis).
- **iid-only arguments** cannot beat $(3-\sqrt{5})/2$, even in principle. That bound
  is sharp for approximately union-closed families (Chase–Lovett).
- **Plain enumeration** stops at $n = 6$. $n = 7$ means about $2\cdot 10^{16}$
  representative pairs.
- Optional item not done: a numerical survey of a "conjectured better"
  inequality. Every published variant with a closed-form optimum is already
  pinned by the ceilings above, so a grid test would be redundant.

## Next steps

Realistic for the next session (bounded, about 3 hours):

1. **Finish the analytic glue.** For Costa–Sadhu Thm 1.2 only the
   measure-theoretic layer is left (Prop. 6.3's integration, Lemma 2.1's weak
   limit, and Liu's argument that the induced laws lie in $C_{3}$). Liu's
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
   - So formalising Gilmer + AHS, i.e. $c_{\mathrm{UC}} \ge (3-\sqrt{5})/2$ in Lean, is a concrete
     and *genuinely new* artefact. First check that nobody has done it (search
     Zulip/GitHub).
   - It is a multi-session project; the first step is a Lean statement plus
     the two-point reduction (AHS Lemmas 2.1–3.1).

Genuinely new, but not realistic in one session:

3. **$n = 13$.**
   - It needs FC-family pruning (Poonen weights, as in Živković–Vučković).
   - A useful intermediate step is $n = 7$ by Poonen-style pruning, as a
     pipeline test. Then, step by step, $n = 8$.
4. **Beating 0.38289.**
   - This needs an entropy inequality that is *not* pointwise in one
     coordinate. Candidates: kernels with no product lower bound, block
     (several-coordinate) chain rules, or Jiang's global coupling made uniform
     in $\lvert F\rvert$.
   - No concrete candidate has been identified yet. Any claim here must come
     with a checkable certificate.
