# Mid-range primes as divisibility gates for LRC(17): sampled cascades, Lemma T families, cost

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Track notes of the mid-range-primes agent (2026-11-26). They continue
`small-primes.md` (§2 Lemma S, §3 $\tau_{17}$, §6–7), `k17-structure.md`
(Lemma R′, Lemma TN, §4 open leads) and `gates.md` (§6, the cost table).
Code and data: `computations/lonely-runner/midp17/`.

Labels follow the README: **proved**, **computed** (exact computation with
tested code), **heuristic** (sampling, extrapolation). No gate is claimed
closed here: every closure statement below is about a random sample of
level-one orbits.

## Summary

| # | Statement | Label |
| --- | --- | --- |
| 1 | An exact uniform sampler and counter for the level-one set $I(17,p,1)$, at any $p$: a Metropolis chain on multisets with a ladder of nested covering constraints. It agrees with exact counts at $k=7$ and with an independent rejection sampler at $p=151,173,193$ | computed (validated); the counts are estimates with error bars |
| 2 | $I(17,p,1)$ is large: $10^{7}$–$10^{11}$ unit orbits, e.g. $1.3\cdot10^{7}$ at 89, $2.3\cdot10^{10}$ at 151, $6.2\cdot10^{8}$ at 251. Most of it has support of size 16 or 17, not "small cover plus free classes" | heuristic (relative error about 5%) |
| 3 | **All 175,500 sampled level-one orbits close** under the extended cascade (grid witness, gcd clause, Lemma S at every $d\mid l$) at the 41 primes $83\le p\le379$ with $\tau_{17}(p)\ge12$. They close by level 18, or 36 for 10 bases at 127 and 131; for $\tau_{17}\ge13$ almost always by level 9. Fibres stay small: at most 4,348 retained orbits per base at any level. The samples do not close at $p=113$ ($\tau_{17}=11$, as Lemma TN predicts) or at $p=73$ (coarse grid) | heuristic for the gates (sampling; **no gate is closed**); the closure of each sampled orbit is an exact computation |
| 4 | Lemma TF: a Lemma T family (coordinates $\equiv0$ mod the level whose classes cover, plus $f$ free coordinates) is retained iff its free residues form a Lemma TN pattern. So such families die at the first level with no pattern, e.g. level 18 for $f\le5$ | **proved** |
| 5 | Corollary TN′: every retained tuple at level $l$ has at least $f_{\min}(l)$ coordinates not divisible by $l$; $f_{\min}(18)=6$. Lemma TD: if the zero set does not cover, the free coordinates must block all shifts at each uncovered time. `defect.c` cross-checks the Lemma TN table and counts the blockable patterns | **proved** (given the exact Lemma TN search); the counts are computed |
| 6 | The last survivors in the samples are Lemma T families (89–99% at the $\tau=12$ primes, level 9) and *defect* families whose zero set misses 1–3 times (all of them at 127 and 131, level 18) | computed on samples |
| 7 | The tight orbit $(1..17)$ closes at level 18 along $3,3,2$ at all 39 primes $97\le p\le311$ | computed (exact) |
| 8 | Cost: cascade $10^{2}$–$2.5\cdot10^{5}$ CPU-h per mid-range gate, plus level one. Gate set at target 647.53 with 41 mid-range primes: about $9.9\cdot10^{6}$ CPU-h, against $6.8\cdot10^{7}$ for J-empty gates alone (same model) | heuristic |
| 9 | Lemma B (per-base symmetry), Lemma $\mathrm{R}_b$ (Lemma R′ for any base tuple; open lead 2), Remark L (closing levels may differ from base to base) | **proved** |
| 10 | No stronger shift lemma (open lead 4): the averaging, coset and grid variants fail, for the reasons given in §6. Neither rejection nor importance sampling scales | failed routes |

---

## 1. Setting

Fix $k=17$ and a prime $p>18$, and put $h=(p-1)/2$. Folded classes and
folded times are $1,\dots,h$. Class $v$ covers time $a$ iff
$(k+1)\,d_p(av)<p$. A level-one *base* is a sorted $17$-multiset of classes
whose support covers every time; these are the elements of $I(17,p,1)$, up to
the unit action.

A level-$l$ tuple $w\in\mathbb Z_{lp}^{17}$ over a base $b$ has
$w_i\equiv b_i\pmod p$. It is **extended-proper** if

- (a) it has a witness on the grid $\frac1{lp}\mathbb Z$: some $n$ with
  $(k+1)\,d_{lp}(nw_i)\ge lp$ for all $i$; or
- (b) the gcd clause holds: $\gcd(l,w_j:j\ne i)>1$ for some $i$; or
- (c) Lemma S (= Lemma NG, `small-primes.md` §2) holds at some divisor
  $d\ge2$ of $l$: with $E=\{i:d\nmid w_i\}$ and $g_i=\gcd(w_i,d)$,
  $\lvert E\rvert\ge2$ and $\sum_{i\in E}g_i\lceil 2d/(18g_i)\rceil<d$.

Each of (a)–(c) persists to every lift. The **retained set** of $b$ at level
$L$ is the set of extended-improper lifts of $b$ to level $L$. It does not
depend on the chain of lift factors used to reach $L$, only on $L$: the chain
only organises the enumeration (Lemma TN, step 5 of its proof). The base
**closes at level $L$** if its retained set there is empty. Lemma S needs
LRC($m$) for $m\le15$, i.e. Allikvere's unrefereed 16-runner claim; so does
everything below that uses (c).

**Remark L (proved; per-base levels).** Suppose every base $b$ closes at
some level $L_b$, with $p\nmid L_b$. Then $p$ divides $u_1\cdots u_{17}$ for
every counterexample $u$.

*Proof.* This is Lemma E of the problem file, with extended properness in
place of properness.

1. **One common level.** There are finitely many bases. Put
   $L=\operatorname{lcm}_bL_b$, so that $p\nmid L$.
2. **Every lift is extended-proper.** Let $w$ be any level-$L$ tuple over a
   base $b$. Its projection to level $L_b$ is extended-proper, because the
   retained set of $b$ there is empty. Each of (a)–(c) persists to lifts, so
   $w$ is extended-proper.
3. **Every level-$L$ class is covered.** By F2 (units of $\mathbb Z_{Lp}$,
   signs, permutations), every tuple in $(\mathbb Z_{Lp}\setminus p\mathbb Z_{Lp})^{17}$
   is equivalent to one whose reduction mod $p$ is a sorted folded orbit
   representative. If that representative has a level-one witness, so does
   the tuple. Otherwise it is a base. These symmetries preserve (a)–(c):
   for (c), $\gcd(vw_i,d)=\gcd(w_i,d)$ for units $v$.
4. **Conclusion.** Apply Lemma 2.2(ii) of arXiv:2609.02604v2 in the form of
   `gates.md` §2, with Lemma S covering the classes settled by (c). ∎

So the level may differ from orbit to orbit, and so may the chain. §5 uses
this: a base is first lifted by 2, and only if that fails is it lifted
along $3,3,2,2$ from level one.

## 2. Tools

### 2.1 Level-one sampling (computed, validated)

The full level-one set is too large to enumerate here: $10^{9}$–$10^{11}$ orbits per prime
(§3), and `covergen.c` trees of $10^{10}$–$10^{12}$ nodes (`k17/knuth_k17.txt`).
So the bases are sampled.

- **Rejection** (`sample1.c`). A $17$-multiset with support $S$, $\lvert S\rvert=j$,
  corresponds to a composition of 17 into $j$ parts. So
  $$\#I(17,p,1)=\sum_j\binom{16}{j-1}A_j,$$
  where $A_j$ is the number of covering $j$-subsets of $\{1,\dots,h\}$.
  Drawing uniform $j$-sets estimates each $A_j$. A uniform covering $j$-set
  (by rejection) together with a uniform composition is an exactly uniform
  multiset. This works up to $p\approx193$; at $p\ge211$ no covering
  17-set appeared in $3\cdot10^8$ draws.
- **Ladder chain** (`mcmc1.c`, used for all results). This is a Metropolis
  chain on ordered 17-tuples. A move replaces one or two uniformly chosen
  positions by uniform classes; the proposal is symmetric.
  - The target weight is $\prod_c n_c!$ ($n_c$ the multiplicity of class
    $c$). This is the uniform distribution on multisets, because a multiset
    has $17!/\prod_c n_c!$ orderings.
  - Times are added in random order, three at a time. Stage $s$ samples the
    multisets that cover the first $3s$ times and estimates the fraction
    $r_s$ that also cover the next three.
  - Then $\#I(17,p,1)=\binom{h+16}{17}\prod_s r_s$, and the final stage
    samples $I(17,p,1)$. Unit orbits number $\#I/h$ up to stabilisers,
    which are rare.
- **Validation.**
  - $k=7$, $p=29$: the exact count by brute force over all multisets is
    checked in the test. The ladder gives $630.2$ (binomial error $2\%$);
    rejection gives $632.9$ ($0.25\%$).
  - $k=17$, $p=151$: ladder $1.63$ and $1.55\cdot10^{12}$ (two seeds,
    $3\%$ each); rejection $1.61\cdot10^{12}$ ($1.35\%$).
  - $p=173$: ladder $4.37$, $4.32\cdot10^{11}$; rejection
    $4.07\cdot10^{11}\pm7\%$.
  - $p=193$: ladder $7.6$, $8.0\cdot10^{11}$; rejection
    $8.4\cdot10^{11}\pm13\%$.
  - The support-size distribution of the final ladder samples at $p=151$
    is $j=14,15,16,17$: $0.7, 7.8, 35.5, 55.9\%$ (seed 1) and
    $0.6, 6.6, 37.0, 55.7\%$ (seed 2). The exact rejection weights give
    $0.5, 7.0, 36.8, 55.6\%$.
- **Not exact.** The ladder's error bars ignore autocorrelation. Thinning is
  20,000 steps (acceptance about 0.35), and independent seeds agree within
  the stated errors. A sequential-importance sampler was also tried and
  failed (§6).

### 2.2 The extended cascade `xcasc.c` (computed, tested)

For one base at a time, `xcasc k p CHAIN` keeps the retained set level by
level. Each lift is enumerated by a branch-and-bound DFS over the digits
$j_i\in\{0,\dots,c-1\}$ of $w_i+j_i\,lp$, using two sound cuts:

- a time that is good for every digit of every remaining coordinate (the cut
  of `k17struct/cascade_verify.c`);
- the counting bound of `liftfree.c`.

Lifts are then filtered by (b) and (c) and reduced by the symmetries of
Lemma B.

**Lemma B (proved).** Let $b$ be a base, $w$ a level-$l$ tuple over $b$, $v$ a
unit of $\mathbb Z_l$, and $v^*\in\mathbb Z_{lp}$ the unit with $v^*\equiv1$
(mod $p$) and $v^*\equiv v$ (mod $l$). Then:

1. $v^*w$ lies over $b$, and $w$, $v^*w$ are extended-proper together.
2. The lifts of $v^*w$ by $c$ are the $V$-multiples of the lifts of $w$,
   for a unit $V$ of $\mathbb Z_{clp}$ with $V\equiv1$ (mod $p$).
3. The same holds for a permutation of coordinates with equal $b_i$.

*Proof.*

- **Witnesses.** $n\mapsto v^*n$ permutes the grid, and
  $\lVert v^*w_i\,n/(lp)\rVert=\lVert w_i\,(v^*n)/(lp)\rVert$.
- **gcd clause and Lemma S.** $\gcd(l,vw_j)=\gcd(l,w_j)$, and
  $\gcd(vw_i,d)=\gcd(w_i,d)$ for $d\mid l$.
- **Lifts.** A unit of $\mathbb Z_l$ lifts to a unit of $\mathbb Z_{cl}$, so
  by CRT there is a unit $V$ of $\mathbb Z_{clp}$ with $V\equiv1$ (mod $p$)
  and $V\equiv v^*$ (mod $lp$). Multiplication by $V$ maps the fibre of $w$
  onto the fibre of $v^*w$.
- **Permutations.** They act on every condition coordinatewise. ∎

So a retained tuple is stored by $e=w\bmod l$ in canonical form: the
lexicographic minimum over $v\in\mathbb Z_l^*$ of $ve$, sorted inside each
block of equal $b_i$. Inside the DFS, equal coordinates are lifted with
non-decreasing digits.

**Tests** (`midp17/test_midp17.py`, 9 tests, all pass):

- At $(k,p,\text{chain})=(7,29,2\cdot2\cdot2)$, $(7,31,2\cdot3)$,
  $(8,37,3\cdot3)$ and $(5,17,2\cdot3\cdot2)$, each on 4 random bases, the
  retained sets at every level equal, orbit for orbit, those of an
  independent reference. The reference is `smallp/xcascade.py`, with
  witness-free lifts from `liftfree.c` and the gcd clause and Lemma S in
  Python, reduced to full unit-orbit canonical forms as in
  `cascade_verify.c`.
- At $k=17$, $p=97,101,103$, the tight tuple $(1..17)$ gives the level-2
  counts 143, 52, 56 and closure at level 18, as in
  `smallp/results/tight17.jsonl`.
- **Negative controls.**
  - A build with floor in place of the ceiling in Lemma S (unsound) is
    detected by the comparison.
  - A base with a level-one witness is flagged.
  - The level-one checker rejects a non-covering multiset.

## 3. Measurements (heuristic)

### 3.1 Six primes, 4,000 sampled orbits each, chain $2,3,3,2$

The primes 151, 173, 193, 211, 229 and 251 cover $\tau_{17}=12,14,13,14,14$
and the undetermined 251. They have the cheapest level one in their
$\tau$-classes in the band (Knuth table), and they are spread across 150–250.
Two independent ladder runs give 2,000 samples each. Results:
`results/casc_p<p>.jsonl` and `results/summary_2332.txt`.

| $p$ | orbits | closed at 2 / 6 / 18 | mean retained at 2 / 6 | max retained at 6 | s/base (95%) |
| --- | --- | --- | --- | --- | --- |
| 151 | $2.1\cdot10^{10}$ | 399 / 2941 / 660 | 8.2 / 39.1 | 2388 | 0.145 (0.124–0.168) |
| 173 | $5.1\cdot10^{9}$ | 1935 / 2056 / 9 | 1.5 / 0.02 | 20 | 0.0033 |
| 193 | $8.1\cdot10^{9}$ | 2402 / 1587 / 11 | 0.93 / 0.22 | 160 | 0.0024 |
| 211 | $1.5\cdot10^{9}$ | 3481 / 519 / 0 | 0.19 / 0 | 0 | 0.00039 |
| 229 | $1.0\cdot10^{10}$ | 3407 / 593 / 0 | 0.21 / 0 | 0 | 0.00032 |
| 251 | $6.6\cdot10^{8}$ | 3868 / 132 / 0 | 0.04 / 0 | 0 | 0.000033 |

**All 24,000 bases close by level 18; none needed level 36.**

**Fibre growth.** There is no blow-up.

- At $p=151$, the retained set grows from 1 to 8 (mean) at level 2 and to
  39 at level 6, then drops to 0 at level 18.
- At $p\ge173$ the mean is at most 1.5 orbits at level 2.

Compare $p=31$, where 8 orbits became $1.8\cdot10^{7}$ by level 4
(`k17-structure.md` §2).

### 3.2 All 31 primes $139\le p\le311$ with $\tau_{17}\le15$, 600 orbits each, chain $3,3,2,2$

Results: `results/sweep_*.jsonl`. The table is `results/sweep_table.md`,
generated by `summarize.py`.

- The last two columns of that table are the cascade CPU-h, i.e. orbits
  times the mean seconds per base of the cheaper strategy, with a bootstrap
  95% interval widened by twice the orbit-count error, and the level-one
  CPU-h ($N_{17}/1.8\cdot10^{6}$ per s, as in `gates.md`).
- "2, then 3,3,2,2" is the two-stage strategy of `run_adaptive.sh`: lift by
  2; if anything is retained, restart from level one along $3,3,2,2$
  (Remark L).

| $p$ | $\tau_{17}$ | orbits | closed at 3 / 9 / 18 | s/base, 3,3,2,2 | s/base, 2 then 3,3,2,2 | cascade CPU-h (95%) | level one CPU-h |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 139 | 12 | 1.52e+09 | 459 / 139 / 2 | 1.78e-02 | 1.85e-02 | 7.5e+03 (5.7e+03–1e+04) | 0.7 |
| 149 | 12 | 2.66e+10 | 362 / 231 / 7 | 2.53e-02 | 2.29e-02 | 1.7e+05 (1.3e+05–2.1e+05) | 7.8 |
| 151 | 12 | 2.29e+10 | 347 / 235 / 18 | 3.95e-02 | 4.02e-02 | 2.5e+05 (1.9e+05–3.4e+05) | 7 |
| 157 | 13 | 6.56e+09 | 471 / 129 / 0 | 1.33e-02 | 1.12e-02 | 2e+04 (1.6e+04–2.6e+04) | 3.3 |
| 163 | 13 | 4.44e+10 | 512 / 88 / 0 | 8.11e-03 | 6.65e-03 | 8.2e+04 (6.5e+04–1e+05) | 27 |
| 167 | 13 | 1.90e+10 | 541 / 59 / 0 | 5.15e-03 | 3.74e-03 | 2e+04 (1.6e+04–2.5e+04) | 24 |
| 173 | 14 | 5.23e+09 | 569 / 31 / 0 | 5.49e-03 | 3.57e-03 | 5.2e+03 (3.7e+03–7e+03) | 8.6 |
| 179 | 14 | 7.11e+08 | 597 / 3 / 0 | 3.62e-03 | 1.16e-03 | 2.3e+02 (1.7e+02–3.1e+02) | 4.2 |
| 181 | 13 | 7.38e+10 | 548 / 52 / 0 | 6.59e-03 | 4.48e-03 | 9.2e+04 (6.9e+04–1.2e+05) | 84 |
| 191 | 13 | 1.12e+10 | 572 / 28 / 0 | 3.74e-03 | 1.69e-03 | 5.3e+03 (3.9e+03–6.9e+03) | 24 |
| 193 | 13 | 7.78e+09 | 582 / 18 / 0 | 4.20e-03 | 1.92e-03 | 4.2e+03 (3.2e+03–5.3e+03) | 21 |
| 197 | 14 | 1.86e+09 | 596 / 4 / 0 | 3.59e-03 | 6.67e-04 | 3.5e+02 (2.4e+02–4.8e+02) | 14 |
| 199 | 13 | 2.96e+10 | 573 / 27 / 0 | 4.34e-03 | 2.17e-03 | 1.8e+04 (1.4e+04–2.3e+04) | 1e+02 |
| 211 | 14 | 1.45e+09 | 598 / 2 / 0 | 3.48e-03 | 6.03e-04 | 2.4e+02 (1.6e+02–3.4e+02) | 21 |
| 223 | 14 | 2.75e+10 | 596 / 4 / 0 | 3.34e-03 | 6.00e-04 | 4.6e+03 (3.3e+03–6.2e+03) | 1.4e+02 |
| 227 | 14 | 1.51e+10 | 596 / 4 / 0 | 3.57e-03 | 6.18e-04 | 2.6e+03 (1.9e+03–3.4e+03) | 1.2e+02 |
| 229 | 14 | 8.84e+09 | 599 / 1 / 0 | 2.73e-03 | 3.89e-04 | 9.6e+02 (6.8e+02–1.3e+03) | 1e+02 |
| 233 | 14 | 5.79e+09 | 597 / 3 / 0 | 2.03e-03 | 3.29e-04 | 5.3e+02 (3.6e+02–7.2e+02) | 68 |
| 239 | 14 | 1.15e+10 | 598 / 2 / 0 | 2.09e-03 | 2.27e-04 | 7.3e+02 (4.5e+02–1.1e+03) | 2.3e+02 |
| 241 | 14 | 1.31e+10 | 596 / 4 / 0 | 2.73e-03 | 5.46e-04 | 2e+03 (1.3e+03–2.8e+03) | 2.2e+02 |
| 251 | ≤ 15 | 6.19e+08 | 600 / 0 / 0 | 2.06e-03 | 6.40e-05 | 11 (4.9–21) | 78 |
| 257 | 14 | 8.89e+09 | 599 / 1 / 0 | 2.16e-03 | 1.40e-04 | 3.5e+02 (1.9e+02–5.5e+02) | 3.7e+02 |
| 263 | ≤ 15 | 3.48e+09 | 600 / 0 / 0 | 1.99e-03 | 1.57e-04 | 1.5e+02 (86–2.4e+02) | 2.7e+02 |
| 269 | ≤ 15 | 3.61e+08 | 600 / 0 / 0 | 2.19e-03 | 7.86e-05 | 7.9 (4.1–13) | 1.5e+02 |
| 271 | ≤ 15 | 1.33e+10 | 600 / 0 / 0 | 2.81e-03 | 1.65e-04 | 6.1e+02 (3e+02–1e+03) | 8.1e+02 |
| 277 | ≤ 15 | 3.56e+09 | 600 / 0 / 0 | 2.34e-03 | 3.95e-05 | 39 (14–76) | 5.1e+02 |
| 281 | ≤ 15 | 6.50e+08 | 600 / 0 / 0 | 1.74e-03 | 1.29e-05 | 2.3 (0.22–5.6) | 4.2e+02 |
| 283 | ≤ 15 | 1.10e+09 | 600 / 0 / 0 | 2.20e-03 | 2.96e-05 | 9 (3.6–17) | 3.9e+02 |
| 293 | ≤ 15 | 2.81e+09 | 600 / 0 / 0 | 1.66e-03 | 1.91e-05 | 15 (3.5–34) | 1e+03 |
| 307 | ≤ 15 | 2.19e+09 | 600 / 0 / 0 | 2.20e-03 | 1.51e-05 | 9.2 (3.2–18) | 1.7e+03 |
| 311 | ≤ 15 | 1.06e+09 | 600 / 0 / 0 | 1.58e-03 | 2.09e-05 | 6.2 (1.5–14) | 1.2e+03 |

- **Closure.** 18,600 of 18,600 sampled orbits close. Add the 24,000 of
  §3.1 for 42,600 in all, with no base capped and no base open.
- **What this does not show.** Zero failures in 600 samples bounds the
  failing fraction of a prime's orbits by about $5\cdot10^{-3}$ at 95%
  ("rule of three"). With 4,000 samples the bound is $7.5\cdot10^{-4}$. A
  gate needs every one of $10^{9}$–$10^{11}$ orbits. Rare structured
  families are invisible to sampling; §4 treats the ones known.
- **Chain choice** (heavy bases at $p=151$, `results/chain151_*.jsonl`).
  - On the 120 bases that needed level 18 under $2,3,3,2$, the chains
    $2,3,3$, $3,2,3$ and $3,3,2$ took 0.83, 0.79 and 0.19 s per base. The
    retained sets at level 6 are identical, as they must be.
  - On 573 random bases at $p=151$, $3,3,2,2$ took 0.051 s per base,
    against 0.174 s for $2,3,3,2$ on the same bases.
  - At $p\ge197$, lifting by 2 first is 5 to 100 times cheaper, because
    most bases already close at level 2. Hence the two-stage strategy.

### 3.3 Below 139, the near-gcd primes 331 and 379, the J-empty primes 313 and 401, and two structured families

**Primes 73–137, 300 sampled orbits each** (100 at 73, 83 and 89; chain
$3,3,2,2$; same files and columns as §3.2):

| $p$ | $\tau_{17}$ | orbits | closed at 3 / 9 / 18 / 36 | open | s/base | cascade CPU-h (95%) |
| --- | --- | --- | --- | --- | --- | --- |
| 73 | 12 | 4.21e+08 | 0 / 4 / 27 / 40 | **29** | 7.9 | — |
| 83 | 13 | 6.82e+07 | 8 / 78 / 14 / 0 | 0 | 0.27 | 5.1e+03 (3.6e+03–6.9e+03) |
| 89 | 13 | 1.31e+07 | 13 / 87 / 0 / 0 | 0 | 0.081 | 2.9e+02 (2.2e+02–3.8e+02) |
| 97 | 12 | 5.38e+08 | 5 / 274 / 21 / 0 | 0 | 0.32 | 4.8e+04 (3.8e+04–6.1e+04) |
| 101 | 12 | 2.28e+08 | 73 / 215 / 12 / 0 | 0 | 0.11 | 6.8e+03 (4.9e+03–9.1e+03) |
| 103 | 13 | 1.29e+08 | 55 / 235 / 10 / 0 | 0 | 0.10 | 3.6e+03 (2.7e+03–4.7e+03) |
| 107 | 12 | 5.18e+07 | 137 / 140 / 23 / 0 | 0 | 0.085 | 1.2e+03 (8.4e+02–1.7e+03) |
| 113 | **11** | 6.90e+09 | 41 / 212 / 34 / 8 | **5** | 0.17 | — |
| 127 | 12 | 2.30e+10 | 65 / 188 / 39 / 8 | 0 | 0.16 | 1e+06 (7.5e+05–1.4e+06) |
| 131 | 12 | 1.08e+10 | 108 / 169 / 21 / 2 | 0 | 0.072 | 2.2e+05 (1.6e+05–2.8e+05) |
| 137 | 13 | 3.33e+09 | 197 / 103 / 0 / 0 | 0 | 0.016 | 1.5e+04 (1.1e+04–1.9e+04) |

- **$p=113$ fails, as Lemma TN predicts.** There $\tau_{17}=11$, so $f=6$,
  and Lemma TN obstructs levels 18 and 36. The first level divisible by 18
  at which a cascade can be empty is 54 (`k17-structure.md` §3).
  - Of the 5 open bases, 4 hit the retained-set cap ($2\cdot10^{5}$ orbits)
    at level 18 or 36.
  - The fifth still had 4 retained orbits at level 36, the end of the chain.
  - So the boundary of the mid-range route is $\tau_{17}\ge12$, i.e.
    $f\le5$, and not a bound on $p$.
- **$p=73$ fails although $\tau_{17}=12$.** 29 of 100 bases are still
  open at level 36, most of them at the node cap; this is the coarse-grid
  blow-up of `small-primes.md` §6 ($p\approx4k$, $m=4$). Primes below 83
  were not tried further.
- **The other nine primes** have $\tau_{17}\ge12$, and all their samples
  close: 83, 89, 97–107, 127, 131 and 137. At 127 and 131, ten bases need
  level 36. Their level-18 survivors are not Lemma T families (§4.1).
- **The near-gcd primes 331 and 379**, which the $\tau$ screen of
  `gates.md` §6.1 puts at $\tau_{17}\le15$, were measured with 300 orbits
  each. All close at level 2 or 3. The cascade costs about 2 and 1 CPU-h,
  against $2.3\cdot10^{3}$ and $9.5\cdot10^{3}$ CPU-h of level one.
- **J-empty primes, measured the same way** (two-stage strategy, 300 orbits):
  - 313: $4.3\cdot10^{8}$ orbits; every sample closes at level 2 or 3;
    cascade about 2 CPU-h, against $1.2\cdot10^{3}$ CPU-h of level one.
  - 401: $2.0\cdot10^{7}$ orbits; cascade negligible.

  So leaving the cascade out of the J-empty cost (as `gates.md` does) is
  justified there.

**The tight orbit** $(1,\dots,17)$ (`results/tight_3322.jsonl`; computed,
exact, one orbit per prime). At every prime $97\le p\le311$ in the tables
above, its retained sets along $3,3,2$ are:

- for $p\ge137$: 1, 1 and 0 orbits at levels 3, 9 and 18;
- below 137: up to 162 orbits at level 3, then 1 at level 9 and 0 at level 18.

So it closes at level 18 at every one of these primes. This is the pattern
that Theorem K proves for $p\ge353$ along $\times3\times2\times3$.

**Lemma T families, worst cases** (`results/tnbases_*.txt`,
`results/tncasc_*.jsonl`; computed, exact per base). For 20 random minimal
covers $C$ of size $\tau_{17}(p)$ at $p=139,149,151,157,173$ (only 4 exist
at 139), two bases were formed:

- $C$ plus $f$ further copies of class 1;
- $C$ plus $f$ random classes.

All 168 bases close:

- at level 18 when $\tau_{17}=12$, with up to 2,880 retained orbits on the
  way;
- at level 9 when $\tau_{17}=14$;
- at level 9 when $\tau_{17}=13$, except for 3 of the 40 bases at 157, which
  needed level 18.

### 3.4 A larger sample: 5,000 fresh orbits at each of 26 primes (two-stage strategy)

These are new ladder samples (seed 4), lifted by 2 first and then, if
anything is retained, along $3,3,2,2$ from level one (`run_big.sh`,
`bigsummary.py`, `results/big_table.md`).

| $p$ | samples | closed at 2 | rest closed at 3 / 9 / 18 / 36 | not closed |
| --- | --- | --- | --- | --- |
| 157 | 5000 | 1117 | 2798 / 1084 / 1 / 0 | 0 |
| 173 | 5000 | 2309 | 2459 / 232 / 0 / 0 | 0 |
| 179 | 5000 | 3846 | 1128 / 26 / 0 / 0 | 0 |
| 191 | 5000 | 2805 | 1978 / 217 / 0 / 0 | 0 |
| 193 | 5000 | 2995 | 1781 / 224 / 0 / 0 | 0 |
| 197 | 5000 | 4117 | 860 / 23 / 0 / 0 | 0 |
| 211 | 5000 | 4356 | 624 / 20 / 0 / 0 | 0 |
| 223 | 5000 | 3908 | 1048 / 44 / 0 / 0 | 0 |
| 227 | 5000 | 3930 | 1044 / 26 / 0 / 0 | 0 |
| 229 | 5000 | 4224 | 760 / 16 / 0 / 0 | 0 |
| 233 | 5000 | 4203 | 774 / 23 / 0 / 0 | 0 |
| 239 | 5000 | 4518 | 478 / 4 / 0 / 0 | 0 |
| 241 | 5000 | 4197 | 786 / 17 / 0 / 0 | 0 |
| 251 | 5000 | 4830 | 170 / 0 / 0 / 0 | 0 |
| 257 | 5000 | 4706 | 291 / 3 / 0 / 0 | 0 |
| 263 | 5000 | 4664 | 336 / 0 / 0 / 0 | 0 |
| 269 | 5000 | 4863 | 137 / 0 / 0 / 0 | 0 |
| 271 | 5000 | 4761 | 237 / 2 / 0 / 0 | 0 |
| 277 | 5000 | 4871 | 129 / 0 / 0 / 0 | 0 |
| 281 | 5000 | 4948 | 52 / 0 / 0 / 0 | 0 |
| 283 | 5000 | 4887 | 113 / 0 / 0 / 0 | 0 |
| 293 | 5000 | 4945 | 55 / 0 / 0 / 0 | 0 |
| 307 | 5000 | 4931 | 69 / 0 / 0 / 0 | 0 |
| 311 | 5000 | 4947 | 53 / 0 / 0 / 0 | 0 |
| 331 | 5000 | 4969 | 31 / 0 / 0 / 0 | 0 |
| 379 | 5000 | 4991 | 9 / 0 / 0 / 0 | 0 |

- **All 130,000 close.**
- With 5,000 samples and no failure, the failing fraction at each prime is
  below $6\cdot10^{-4}$ at 95% (rule of three).
- The level-9 closures at 257 ($\tau_{17}=14$) and at 271 (2 of 5,000)
  qualify the prediction of §4. At 251, 263, 269 and 277–379 every sample
  closes by level 3, consistent with $\tau_{17}=15$ there. At 271 the two
  level-9 bases suggest $\tau_{17}(271)\le14$, or a defect family (not
  checked).
- At 157 ($\tau_{17}=13$), one base needed level 18. Lemma T families with
  $f=4$ are gone at level 9, so this was a defect family.

**Totals.** At the 41 primes $83\le p\le379$ with $\tau_{17}\ge12$:

- 175,500 sampled level-one orbits (§3.1–3.4), every one closed;
- plus the tight orbit at 39 primes, and the 168 constructed Lemma T bases.

At 73 ($\tau_{17}=12$, small $p$) and at 113 ($\tau_{17}=11$), samples do
not close.

## 4. Structure of the survivors: Lemma T families

**Lemma TF (proved).** Let $b$ be a base and $Z\subseteq[17]$ a set of
coordinates whose classes $\{b_i:i\in Z\}$ cover every folded time. Put
$F=[17]\setminus Z$ and $f=\lvert F\rvert$. Let $l\ge2$ with $p\nmid l$, and
let $w$ be a level-$l$ tuple over $b$ with $w_i\equiv0\pmod l$ for all
$i\in Z$. Then:

1. $w$ has no witness at level $l$.
2. $w$ is retained, i.e. extended-improper, iff $f\ge2$ and the residues
   $e_j=w_j\bmod l$ ($j\in F$) satisfy conditions (R) and (N) of Lemma TN
   (`k17-structure.md` §3).
3. In particular, if level $l$ admits no Lemma TN pattern for $f$, every
   such $w$ is extended-proper.

*Proof.*

1. **No witness.** Take a time $n/(lp)$.
   - If $p\nmid n$: for $i\in Z$, write $w_i=lw_i'$. Then
     $\lVert w_in/(lp)\rVert=\lVert b_ia/p\rVert$ with $a\equiv nl^{-1}\not\equiv0$
     (mod $p$), and the classes of $Z$ cover $a$.
   - If $p\mid n$: $w_in/(lp)\in\mathbb Z$ for $i\in Z$.

   This is Lemma T of `gates.md`.
2. **The gcd clause.**
   - If $f\le1$, deleting the free coordinate (or any coordinate) leaves
     only multiples of $l$, so the gcd clause holds.
   - Let $f\ge2$. Deleting $i\in Z$ leaves $\gcd(l,e_F)$; deleting $j_0\in F$
     leaves $\gcd(l,e_j:j\ne j_0)$. So the clause holds iff some
     $\gcd(l,e_j:j\ne j_0)>1$, because $\gcd(l,e_F)$ divides each of these.
     That is, iff (R) fails.
3. **Lemma S at $d\mid l$.**
   - The coordinates in $Z$ are divisible by $d$, and $\gcd(w_j,d)=\gcd(e_j,d)$
     for $j\in F$. So $E=E_d$, and the Lemma S sum is the left side of (N).
   - Lemma S settles $w$ iff $\lvert E_d\rvert\ge2$ and the sum is $<d$.
   - If $\lvert E_d\rvert=1$, then all coordinates but one are divisible by
     $d$, and the gcd clause holds.
   - Hence, given (R), $w$ is unsettled at every $d$ iff (N) holds at every $d$. ∎

**Consequence (proved, given the exact Lemma TN search of `k17-structure.md` §3).**
A Lemma T family with $f$ free coordinates is extended-proper at every level
of the following kind (levels of the form $2^a3^b\le3000$, the range of that
search):

| $f$ | levels with no Lemma TN pattern | so the family is gone at |
| --- | --- | --- |
| $\le2$ | every level not dividing 2 | level 3 |
| 3 | every level not dividing 3 or 4 | levels 6, 9 |
| 4 | every level not dividing 6 or 8 | level 9 |
| 5 | every level not dividing 9, 16 or 24 | level 18 |

Along the chain $3,3,2,2$ (levels 3, 9, 18, 36), the families with
$f=17-s$, for a cover of size $s$ inside the base, are therefore gone at:

| cover size $s$ | gone at level |
| --- | --- |
| $\ge15$ | 3 |
| 13–14 | 9 |
| 12 | 18 |

Every cover inside a base has at least $\tau_{17}(p)$ classes, so
$f\le17-\tau_{17}(p)$ for every Lemma T family at $p$. The table therefore
gives the last level of the chain at which any Lemma T family can survive at
$p$. It does not bound the other retained tuples.

**Observation (computed on the samples).** With $f=17-\tau_{17}(p)$, the
closing levels of §3.2 follow this table for almost every base:

- the $\tau_{17}=12$ primes have bases that need level 18;
- the $\tau_{17}=13,14$ primes close by level 9;
- at 251, 263, 269 and 277–311, which the 60 s screen puts at
  $\tau_{17}\le15$ and whose exact $\tau_{17}$ is not known, every sample
  closes at level 3. That is what $f\le2$ predicts, and it suggests
  $\tau_{17}=15$ there (not proved).

The exceptions are bases carrying *defect* families (§4.1, §4.3), which
need one level more than the table:

- at 127 and 131, 10 of 600 bases need level 36;
- at 157, 1 of 5,000 needs level 18;
- at 271, 2 of 5,000 need level 9.

**Classification of the retained tuples** (`classify.py`, results in
`results/classify_*.txt`).

- **The example base.** The $p=151$ base
  $(6,10,14,20,26,34,34,36,43,44,45,46,48,49,62,66,75)$ keeps 2,144 orbits
  at level 6.
  - 2,120 of them are of Lemma T type: they include the 12 coordinates at
    classes $6,14,20,26,34,43,44,45,46,48,62,75$, which form a 12-cover,
    as multiples of 6. The other five coordinates (classes $10,34,36,49,66$)
    take the patterns allowed by (R) and (N); some of these patterns are
    themselves $\equiv0\pmod6$ in one more place.
  - The remaining 24 have only 11 coordinates $\equiv0\pmod6$, which do not
    cover. They are a defect family (below).

  So 98.9% of this retained set is one Lemma T family with $f\le5$. The
  regression test `test_lemma_tf_family_at_level6` pins these numbers.
- **Sample-wide statistics.** These are in the table below (§4.1).

### 4.1 Fraction of Lemma T type among retained tuples (computed on samples)

For each prime, the bases of §3.2–3.3 that needed the most levels were
re-run to their last nonempty level $L$. Each retained tuple there was then
tested: do the coordinates $\equiv0\pmod L$ cover by themselves?
(`run_classify.sh`, `results/classify_p<p>_L<L>.txt`.) Here $f$ is the
number of coordinates $\not\equiv0\pmod L$.

| $p$ | $\tau_{17}$ | bases | level $L$ | retained tuples | of Lemma T type | $f$ (count) |
| --- | --- | --- | --- | --- | --- | --- |
| 97 | 12 | 21 | 9 | 1,614 | 1,440 (89%) | 5 (1511), 6 (16), 7 (87) |
| 149 | 12 | 7 | 9 | 1,466 | 1,440 (98%) | 5 (1464), 6 (2) |
| 151 | 12 | 18 | 9 | 8,992 | 8,928 (99%) | 5 (8992) |
| 127 | 12 | 8 | 18 | 847 | **0** | 6 (815), 7 (32) |
| 131 | 12 | 2 | 18 | 464 | **0** | 6 (464) |
| 157 | 13 | 129 | 3 | 746 | 451 (60%) | 3 (541), 4 (170), 5 (28), 6 (6), 7 (1) |
| 173 | 14 | 31 | 3 | 136 | 103 (76%) | 3 (126), 4 (10) |
| 199 | 13 | 27 | 3 | 96 | 67 (70%) | 3 (86), 4 (10) |
| 239 | 14 | 2 | 3 | 5 | 4 (80%) | 3 (5) |

- **At the $\tau_{17}=12$ primes, level 9.** The retained tuples are almost
  all Lemma T families with $f=5$. At $p=151$ the 18 bases carry 0, 792,
  1,440, 1,584 or 2,880 of them each.
  - 1,440 is exactly the number of Lemma TN patterns for $f=5$ at level 9
    modulo units: three free residues prime to 3 and two $\equiv\pm3\pmod9$,
    checked by enumeration.
  - Multiples of it come from bases containing several 12-covers, or a
    repeated class.
  - The other 11 bases keep only 4–8 tuples each, all of them defect
    families (below) with $f=5$.
  - Lemma TF and the Lemma TN table explain why the Lemma T families all
    die at level 18.
- **At 127 and 131, level 18: Lemma T families with a defect.** No retained
  tuple is of Lemma T type. Instead, 11 (or 10) coordinates are
  $\equiv0\pmod{18}$, and their classes cover every folded time except one
  (or three). The 6 or 7 free coordinates must then block all 18 shifts at
  that one time.
  - At $p=127$, all 847 tuples have this shape: 814 leave one time
    uncovered, 32 leave three, and 1 leaves two.
  - For example, the zero classes miss only the time 48, and the free
    coordinates are $(7,6)$, $(25,5)$, $(45,12)$, $(48,2)$, $(55,15)$ and
    $(63,8)$, written as (class, residue mod 18).
  - These families are not covered by Lemma TF, and they need one more
    level, 36.
  - The obvious generalisation is a *defect* version of Lemma TF, with zero
    set $Z$ covering all but a set $U$ of times. The proof of Lemma TF shows
    that such a tuple is witness-free iff the free coordinates block every
    grid time whose level-one part lies in $U$. That is a finite condition
    on the free coordinates' phases $ab_j/p$ ($a\in U$) and residues.
- **At the $\tau_{17}\in\{13,14\}$ primes, level 3.** 60–80% of the last
  survivors are Lemma T families with $f=3$ or 4. The rest are again
  near-cover families with $f=3$–7.

**Reading (heuristic).** The cascade's last survivors are covers or near
covers with the rest free, i.e. the Lemma T families and their
low-defect relatives. Generic bases die at level 2 or 3. This is the
mid-range analogue of the $k\le8$ pattern of `structure.md` §5 (only tight
instances survive), with Lemma T families in place of tight instances.

### 4.2 Lemma $\mathrm{R}_b$: Lemma R′ for an arbitrary base tuple (open lead 2)

**Lemma $\mathrm{R}_b$ (proved).** Let $k\ge1$, let $b\in(\mathbb Z\setminus\{0\})^k$ be
an integer tuple, let $M\ge1$ and $c\ge2$, and let $y\in\mathbb Z^k$. For
$r\in\mathbb Z_c$ put
$$\mathcal G_b(y,r)=\Big\{t\in\mathbb R/\mathbb Z:\ \Big\lVert b_it+\frac{y_ir}{c}\Big\rVert\ge\frac1{k+1}\ \ \forall i\Big\}.$$
If for some $r$ the set $\mathcal G_b(y,r)$ contains a closed arc of length at
least $1/M$, then $w=b+My$ has a witness on the grid $\frac1{cM}\mathbb Z$.
So $w$ is proper at level $cM/p$ whenever $M=lp$.

*Proof.*

1. **The grid point.** Let $n\equiv r\pmod c$ and $t=n/(cM)$. Then
   $$w_it=\frac{b_in}{cM}+\frac{y_in}{c}\equiv b_it+\frac{y_ir}{c}\pmod1,$$
   since $y_i(n-r)/c\in\mathbb Z$. So $t$ is a witness iff $t\in\mathcal G_b(y,r)$.
2. **The coset.** As $n$ runs over the integers $\equiv r\pmod c$, $t$ runs over
   the coset $\frac r{cM}+\frac1M\mathbb Z$.
3. **Conclusion.** A closed arc of length $\ge1/M$ meets every coset of
   $\frac1M\mathbb Z$. ∎

**Notes on Lemma $\mathrm{R}_b$.**

- **Special case.** For $b=\iota=(1,\dots,k)$ this is Lemma R′ of
  `k17-structure.md` §1.1.
- **The translation identity** $\mathcal G_b(y+jb,r)=\mathcal G_b(y,r)-jr/c$
  holds verbatim: $b_i(t+jr/c)+y_ir/c=b_it+(y_i+jb_i)r/c$. So the trivial
  lifts are $y\equiv jb$, giving $w=(1+jM)b$, and
  $$\Lambda_b(c)=\min_{y\not\equiv jb}\ \max_r\ \ell(y,r)$$
  plays the role of $\Lambda(k,c)$. If $M\ge1/\Lambda_b(c)$, every nontrivial
  lift of $b$ by $c$ is proper.
- **Scope (why it does not help the mid-range gates).** The arcs of
  $\mathcal G_b$ have length about $1/((k+1)\max_i\lvert b_i\rvert)$. So
  $\Lambda_b(c)\ge1/M$ is only possible when the integer representative of
  the base is small compared with $M/(k+1)$.
  - For a level-one base mod $p$, the entries are as large as $p/2$. The
    condition then needs $l\gtrsim9$ before it can bite.
  - By then (§3) the generic bases are already closed, and the Lemma T
    families are handled by Lemma TF.
  - Lemma $\mathrm{R}_b$ is the right tool for *tight-type* survivors, which are
    integer tuples with small entries (Theorem K is the case $b=\iota$). None
    other than the tight orbit was seen here.

### 4.3 Every retained tuple has many non-multiples of the level (Corollary TN′, Lemma TD)

For a level-$l$ tuple $w$, put $F_l(w)=\{i:l\nmid w_i\}$ and
$Z_l(w)=[17]\setminus F_l(w)$.

**Corollary TN′ (proved, given the exact Lemma TN search; cross-checked
below).** If $w$ is retained at level $l$, then the residues
$(w_j\bmod l)_{j\in F_l(w)}$ satisfy (R) and (N) of Lemma TN. Hence
$\lvert F_l(w)\rvert\ge f_{\min}(l)$, the least $f$ for which level $l$ admits a
Lemma TN pattern. For example:

| $l$ | 2 | 3 | 4 | 6 | 8 | 9 | 12 | 16 | 18 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $f_{\min}(l)$ | 2 | 3 | 3 | 4 | 4 | 5 | 5 | 5 | **6** |

So a retained tuple at level 18 has at most 11 coordinates divisible by 18,
whatever the base and the prime. At a prime with $\tau_{17}(p)\ge12$ those
coordinates cannot cover, so no retained tuple at level 18 is a Lemma T
family there.

*Proof.* The proof of Lemma TF, steps 2–3, never used that $Z$ covers:

- the coordinates of $Z_l(w)$ are $\equiv0\pmod l$, so they do not affect
  (R) and do not enter $E_d$ for any $d\mid l$;
- "not gcd-proper" is (R), and "not settled by Lemma S at any $d\mid l$" is
  (N), as shown there. ∎

**Lemma TD (proved).** Let $w$ be a level-$l$ tuple over the base $b$, and
let $a\in\mathbb Z_p^*$ be a level-one time that no class of $Z_l(w)$ covers.
If $w$ is witness-free at level $l$, then for every $s\in\mathbb Z_l$ some
$j\in F_l(w)$ has
$$\Big\lVert\frac{ab_j}{p}+\frac{se_j}{l}\Big\rVert<\frac1{18},\qquad e_j=w_j\bmod l .$$

*Proof.*

1. **Coordinates of grid times.** Write $1/(lp)\equiv\alpha/p+\beta/l\pmod1$
   with $\alpha=l^{-1}\bmod p$ and $\beta=p^{-1}\bmod l$. Then
   $$\frac{w_in}{lp}\equiv\frac{(\alpha n)b_i}{p}+\frac{(\beta n)e_i}{l}\pmod1,$$
   and $n\mapsto(\alpha n\bmod p,\ \beta n\bmod l)$ is a bijection
   $\mathbb Z_{lp}\to\mathbb Z_p\times\mathbb Z_l$ (CRT).
2. **The time $(a,s)$.** At the grid time corresponding to $(a,s)$:
   - a coordinate $i\in Z_l(w)$ sits at $ab_i/p$, which is not within
     $1/18$ of $\mathbb Z$, because $b_i$ does not cover $a$;
   - so the time is a witness unless some $j\in F_l(w)$ is within $1/18$
     of $\mathbb Z$. ∎

**The finite test behind Lemma TD.** Replace the phases $ab_j/p$ by arbitrary
reals $\varphi_j$, and call a pattern $e$ *blockable* if some $\varphi$
makes $\bigcup_j B_j=\mathbb Z_l$, where
$$B_j=\{s:\lVert\varphi_j+se_j/l\rVert<1/18\}.$$
Then a retained tuple whose zero set does not cover has a blockable,
(R)+(N) pattern on $F_l(w)$.

The code `defect.c` decides blockability exactly:

- $B_j$ is the preimage of the points of $(g_j/l)\mathbb Z$, $g_j=\gcd(e_j,l)$,
  that lie in an open arc of length $1/9$;
- enlarging a $B_j$ only helps, so it suffices to try the maximal runs of
  $\lceil l/(9g_j)\rceil$ consecutive points, with every start;
- a DFS covers the least uncovered $s$.

Results (`results/defect_k17.txt`). The columns count multisets of nonzero
residues mod $l$:

| $l$ | $f$ | multisets | (R)+(N) | (R)+(N)+blockable |
| --- | --- | --- | --- | --- |
| 9 | 5 | 792 | 168 | 168 |
| 12 | 5 | 3,003 | 1,138 | 578 |
| 16 | 6 | 38,760 | 7,866 | 4,974 |
| 18 | 5 | 20,349 | 0 | 0 |
| 18 | 6 | 74,613 | 8,827 | 7,099 |
| 18 | 7 | 245,157 | 98,420 | 65,568 |

- **Cross-check of Lemma TN.** At every level of the $f_{\min}$ table, the
  first $f$ with a nonzero (R)+(N) count equals $f_{\min}(l)$ from Lemma TN.
  The two searches are independent: `ng_obstruction.py` searches gcd
  patterns, while `defect.c` enumerates all residue multisets.
- **What blockability adds.** It removes up to half of the patterns at some
  levels, but never all of them where (R)+(N) has any.
- **Consequence.** So Lemma TD does not by itself raise $f_{\min}$, and the
  defect families of §4.1 ($f=6$ at level 18) are consistent with it. A
  b-independent closure proof would need the phases to be tied together
  across the several uncovered times $a$, through $\varphi_j=ab_j/p$. That
  is the next refinement, not attempted here.

## 5. Cost and the gate set (heuristic)

**Cost of a mid-range gate.** The cost is level one, plus orbit expansion,
plus the cascade on every orbit.

- **Level one** is $N_{17}(p)/1.8\cdot10^{6}$ s by the cost model of
  `gates.md`: 0.7–1,700 CPU-h over 139–311.
- **Orbit expansion and deduplication.** Covers to orbits, about
  $10^{9}$–$10^{11}$ orbits, at an assumed $5\,\mu\mathrm{s}$ each: $1$–$100$ CPU-h.
  The duplicates (a multiset contains several minimal covers) need an
  external sort or a canonical-cover rule. Neither is implemented.
- **Cascade:** the table of §3.2. It dominates at the $\tau_{17}=12$ and 13
  primes and is negligible from about 251 on.

**Gate set** (`gate_scenario.py`, `results/gate_scenario.txt`). The pool is:

- the J-empty candidates $\ge313$, at level-one cost as in `k17/gate_set.py`;
- the 41 near-gcd primes whose samples all closed (83, 89, 97–107, 131–311
  except 113, 331 and 379; 127 was measured but is too expensive), at the
  cost above. They are admitted *because every sampled orbit closed*, which
  is not a proof.

The greedy selection by cost / $\ln p$ gives:

| target | plan | gates | largest prime | CPU-h |
| --- | --- | --- | --- | --- |
| 647.534682 | J-empty only (`gates.md` §6.3) | 101 | 1021 | $6.8\cdot10^{7}$ |
| 647.534682 | with the mid-range primes | 110 (41 mid-range) | 787 | $9.9\cdot10^{6}$, of which $1.0\cdot10^{6}$ mid-range |
| 659.66535 | with the mid-range primes | 112 | 809 | $1.1\cdot10^{7}$ |
| 637.534682 | with the mid-range primes | 109 | 773 | $9.3\cdot10^{6}$ |

- **The saving.** Admitting the mid-range primes removes every J-empty gate
  above 787. That is a factor of about 7 at the current target.
- **With the orderly-root rule and the step-15 build** ($\div5$–$6$ on level
  one, `gates.md` §6.3, J-empty part only), the total would be about
  $2.5$–$3\cdot10^{6}$ CPU-h.
  - The mid-range part, about $10^{6}$ CPU-h, would then be a third or more
    of it.
  - It is concentrated at the $\tau_{17}=12$ primes 97, 131, 149 and 151 and
    at the large orbit counts of 163 and 181.
  - A faster lift for Lemma T families (§7) would remove most of it.
- **Still far beyond one machine.** The cheapest single mid-range gates
  (251, 269, 179, 211, 89) cost 90–290 CPU-h each by this model.

## 6. Failed routes (kept)

- **Rejection sampling at $p\ge211$.** No covering 17-set appeared in
  $3\cdot10^{8}$ draws at 211 and 251. The covering fraction falls roughly
  like $e^{-cp}$. Replaced by the ladder chain.
- **Sequential importance sampling** (`sis1.c`). This is a Knuth-type probe of
  the tree of sorted multisets, with feasibility cuts. Of 20,000 probes at
  $p=151$, 122 reached a leaf, and the effective sample size was 1.6. The
  cuts are far too weak to keep probes alive. Abandoned.
- **Chain $2,3,3,2$ at $\tau_{17}=12$.** The $\times3$ step from level 6 to 18
  must lift the whole level-6 Lemma T family. That family has up to 2,388
  orbits, each with a $3^{17}$ fibre, and the step costs up to 15 s per base.
  The chain $3,3,2$ (or $3,3,2,2$) is $3$–$4\times$ cheaper, because most of
  the family already dies at level 9 and the last step is $\times2$.
- **A stronger shift lemma (open lead 4).** Three variants were examined.
  - *Averaging over the base time.* Lemma S bounds, for each exception, the
    number of bad shifts $q/d$ by the worst case $c(g)$. The average over
    $t$ is $2d/18$, smaller for $d\le8$. An averaging argument would need
    the set $G_D$ of good base times for the block $D$ to be equidistributed
    with respect to the exceptions' bad sets.
    - $G_D$ is only known to be non-empty (LRC($\lvert D\rvert$)).
    - Its pieces have length about $1/\max_{j\in D}u_j$, the same scale as
      the exceptions' bad arcs, so no scale separation is available. The
      correlation can be total, e.g. $u_i=2u_j$.
    - So no averaged bound follows. Using the slack
      $1/(\lvert D\rvert+1)-1/18$ only gives intervals of length about
      $1/(144\max_D u_j)$, again on the same scale.
  - *Shifts restricted to a coset* $r+H$ of a subgroup $H<\mathbb Z_d$. The
    block $D$ stays fixed only if $d\mid u_j$, as before. A coordinate with
    $\gcd(u_i,d)=d/2$ costs $d/2$ over all of $\mathbb Z_d$, but in the coset
    of odd shifts it costs 0 or the whole coset, and the worst case is the
    whole coset. So the coset version is never better than Lemma S.
  - *The grid analogue.* Replace the real $t_0$ by $t_0=a/p$, a level-one time.
    This gives Lemma G below. It is exactly complementary to Lemma S, so it
    settles nothing new.

  **Lemma G (proved).** Let $w$ be a level-$l$ tuple and $d\mid l$. Put
  $Z_d=\{i:d\mid w_i\}$ and $E_d$ for its complement. If
  $\sum_{i\in E_d}c_d(\gcd(w_i,d))<d$ and the classes of $Z_d$ do not cover
  every folded time, then $w$ has a grid witness.

  *Proof.*
  - Let $a$ be uncovered by $Z_d$, and put $t_\sigma=a'/p+\sigma/d\in\frac1{lp}\mathbb Z$,
    with $a'$ the corresponding level-one time.
  - For $i\in Z_d$, $\lVert w_it_\sigma\rVert=\lVert w_ia'/p\rVert\ge\frac1{18}$.
  - For $i\in E_d$, as in step 4 of Lemma S, at most $c_d(g_i)$ values of
    $\sigma$ are bad.
  - Since fewer than $d$ values are bad in all, some $t_\sigma$ is a
    witness. ∎

  So a retained tuple satisfies $\sum_{E_d}c_d\ge d$ at every $d\mid l$
  whether or not $Z_d$ covers. That is the definition of being unsettled,
  so Lemma G adds no new test. It does explain the dichotomy that the data
  show: either $Z_d$ covers (a Lemma T family, decided by Lemma TF), or the
  grid itself does the work.
- **Proving closure of the non-Lemma-T survivors** (open lead 1, in its
  mid-range form). The Lemma T families are decided in closed form by
  Lemma TF. What remains are tuples whose zero set does not cover.
  - For these, witness-freeness depends on the positions $ab_i/p$, i.e. on
    $b$ itself.
  - One instance was worked out by hand: a level-9 Lemma T family with
    $f=5$, lifted by 2. The pattern then has exactly three coordinates prime
    to 3 and two with $\gcd=3$.
  - For the odd shifts at a time not blocked by the zero set, the five free
    coordinates block at most $1+1+1+3+3=9$ of the 9 odd shifts. That is
    exactly the number needed, so the capacity count does not close the
    case; only an exact tiling would.
  - No general argument was found.

## 7. Next steps

1. **Faster lift of Lemma T families.** At a $\tau=12$ prime, the retained
   set of a base at level 6 or 9 is essentially one family: a fixed cover
   part and up to about $3\cdot10^{3}$ patterns on the $f$ free coordinates.
   A DFS that lifts the shared cover part once (a trie over the parents) and
   then branches into each pattern should cut the $\tau=12$ cost by a large
   factor.
2. **Exact gate checks at the cheapest mid-range primes:**
   - 89: $1.3\cdot10^{7}$ orbits, seconds of level one, about 290 CPU-h of
     cascade (100 samples only);
   - 269: $3.6\cdot10^{8}$ orbits, about 150 CPU-h of level one, about 8 CPU-h
     of cascade;
   - 179: $7.1\cdot10^{8}$ orbits, about 4 CPU-h of level one, about 230 CPU-h
     of cascade.

   Each needs the level-one orbit set without duplicates, which requires a
   canonical-cover rule or an external sort of $10^{7}$–$10^{9}$ rows. It
   also needs an independent second implementation of the cascade (for
   example `k17struct/cascade_verify.c` with the shift lemma) before a gate
   could be claimed.
3. **Tie the phases together.** Lemma TD uses one uncovered time at a time.
   A defect family must block every uncovered time $a$ with the same
   residues $e_j$ and phases $ab_j/p$. A finite search over $(U, e)$ with
   phases tied this way might show that defect families with $f\le7$ die at
   level 36 for every base.
4. **Prove $\tau_{17}=15$ at 251, 263, 269 and 277–311** (the prediction of
   §4), and decide $\tau_{17}$ at the undetermined primes, including 271.
5. **Primes 59–79 and 331–379.** Only 73 (fails) and 331, 379 (close,
   300 samples) were tried. 79 has $\tau_{17}=11$ and is excluded by Lemma
   TN.

## 8. Files and reproduction

Files in `computations/lonely-runner/midp17/`:

| file | what it does |
| --- | --- |
| `mcmc1.c` | ladder chain: count of $I(k,p,1)$ and uniform samples (§2.1) |
| `sample1.c` | rejection counts and samples; `check` mode tests coverage |
| `sis1.c` | the failed importance sampler (§6) |
| `xcasc.c` | per-base extended cascade (§2.2); `DUMP_LEVEL` prints a retained set |
| `run_casc.py` | parallel driver and per-prime summary with bootstrap |
| `summarize.py`, `bigsummary.py`, `gate_scenario.py` | the tables of §3 and §5 |
| `classify.py` | Lemma T type test of retained tuples (§4.1) |
| `defect.c` | (R)+(N)+blockable pattern counts (§4.3) |
| `rio.py` | reads results stored plain or gzipped |
| `test_midp17.py` | 14 tests, including the negative controls |
| `results/` | the per-base cascade records as gzipped JSONL (each record holds its base); the ladder logs `*mcmc_p*.txt` with the sample lines removed, since they are regenerated from the seeds and the bases are in the JSONL; and the tables `sweep_table.md`, `big_table.md`, `gate_scenario.txt`, `classify_*.txt`, `defect_k17.txt` and `summary_2332.txt` |

Commands, from `computations/lonely-runner/midp17/` (every run used at most
3 processes, under `nice -n 10`):

```
cc -O3 -march=native -o mcmc1 mcmc1.c -lm
cc -O3 -march=native -o sample1 sample1.c -lm
cc -O3 -march=native -o xcasc xcasc.c
cc -O2 -o defect defect.c
JMIN=12 ./sample1 17 151 count 300000000 1          # rejection counts (results/count_p*.txt)
bash run_mcmc.sh 151 173 193 211 229 251            # ladder counts + 2 x 2000 samples
bash run_all.sh 151 173 193 211 229 251             # chain 2,3,3,2 (section 3.1)
bash run_chains.sh                                  # chain comparison at 151
bash run_sweep.sh 139 149 151 157 ... 311           # section 3.2 (chain 3,3,2,2, 600 samples)
NS=300 bash run_sweep.sh 97 101 103 107 113 127 131 137 313 401 331 379
NS=100 NODECAP=200000000 bash run_sweep.sh 83 89 73
bash run_adaptive.sh 139 ... 311 ; NS=300 bash run_adaptive.sh 97 ... 401   # two-stage strategy
N=5000 JOBS=2 bash run_big.sh 157 173 ... 379       # section 3.4
python3 bigsummary.py 157 173 ... 379 > results/big_table.md
python3 summarize.py > results/sweep_table.md
python3 gate_scenario.py 647.534682
bash run_classify.sh                                # section 4.1
seq 1 17 | tr '\n' ' ' | ./xcasc 17 151 3,3,2,2   # tight orbit (results/tight_3322.jsonl)
./xcasc 17 151 3,3,2,2 400000 < results/tnbases_151.txt   # Lemma T worst cases
./defect 17 18 7                                    # section 4.3
python3 -m pytest -q test_midp17.py
```

The samplers are deterministic given their seeds, so the sample files can be
regenerated. Wall time on this machine (4 cores, 3 used): 1–3 min per prime
and seed for a ladder run, a few minutes per prime for the cascades, about
15 min for the 31-prime sweep, and about 10 min for §3.4.
