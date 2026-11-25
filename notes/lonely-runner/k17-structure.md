# LRC(17) with cheap primes: tight-orbit rigidity and the Lemma S gates


Working notes of the "k17-structure" track (2026-11-25). They continue
`notes/lonely-runner/structure.md` (Lemma S, Lemma NG, Lemma T1, Lemma R,
Corollary R), whose notation is used throughout:

- LRC($k$) is the conjecture for $k$ speeds ($k+1$ runners); the target here
  is $k=17$.
- $I(k,p,l)$ is the set of improper tuples mod $lp$, and $J(k,p)$ the set of
  tuples that are not eventually proper.
- $\lVert x\rVert$ is the distance to the nearest integer, and
  $\iota=(1,2,\dots,k)$.

Code: `computations/lonely-runner/k17struct/` (outputs in its `results/`;
scratch logs under the session scratchpad, not kept).

## Summary

| # | Statement | Label |
| --- | --- | --- |
| 1 | $\Lambda(17,3)=1/352$ and $\Lambda(17,2)=4/1683=1/420.75$ exactly; also $\Lambda(7,2)=1/84$, $\Lambda(7,3)=1/96$, $\Lambda(15,2)=1/288$, $\Lambda(15,3)=1/264$ | **exact finite computation**, two independent algorithms plus an exact-rational spot check |
| 2 | For every prime $p\ge353$, the improper lifts of the tight orbit $(1..17)$ along $\times3\times2\times3$ are one unit orbit at levels 3 and 6 and **none at level 18**; along $\times2\times3\times3$ the same holds for $p\ge421$ | **proved** (Lemma R′ + Lemma T1 + item 1) |
| 3 | Lemma R as written in `structure.md` needs "$\max_{r\ne0}$ of the longest arc of $\mathcal G(y,r)$", not "the longest arc of $\bigcup_{r\ne0}\mathcal G(y,r)$" | correction (proved); the code always used the max over $r$, and for $c=2$ the two agree |
| 4 | The $k=17$ Lemma S gates $p=31,29,23,19$ do **not** close in budget. With NG the cascade grows: at $p=31$, $8\to75{,}530\to18{,}145{,}635$ orbits (levels 1, 2, 4), or $8\to6{,}344{,}186$ at level 3 with $\times3$ first; level 2 has $421{,}686$, $605{,}189$ and $1{,}697{,}639$ orbits at $p=29,23,19$ | **computed**; level-2 orbit sets identical under two independent codes; **no gate claimed** |
| 5 | Lemma TN: Lemma T elements that NG never settles. For $k=17$ they show that no witness + gcd + NG cascade over levels $2^a3^b$ can close at $p=23$ below level 54, or at $p=19$ below level 486 (both divisible by 18) | lemma **proved**; the level tables are an **exact finite search**, with sample tuples re-checked by `cascade_verify.c` |
| 6 | Why the $k\le8$ pattern (only tight instances survive) fails at small $\tau$: the Lemma TN elements are non-tight survivors at every obstructed level. The width at $p=31$ (where TN obstructs only level 2) is not explained; its level-2 survivors are not near-gcd shaped | proved (the first part); computed observation and open (the second) |

---

## 1. The shifted-Dirichlet gap, exactly

### 1.1 Definitions and the corrected Lemma R

Fix $k$, a lift factor $c\ge2$, $y\in\mathbb Z_c^k$ and $r\in\mathbb Z_c$, and
put

$$\mathcal G(y,r)=\Big\{t\in\mathbb R/\mathbb Z:\ \Big\lVert it+\frac{y_ir}{c}\Big\rVert\ge\frac1{k+1}\ \ \forall i\Big\}.$$

It is closed. Let $\ell(y,r)$ be the length of its longest closed arc ($0$ if
it is a finite set, $-\infty$ if empty). Call $y$ trivial if
$y\equiv j\iota\pmod c$ for some $j$, and define

$$\Lambda(k,c)=\min_{y\ \text{nontrivial}}\ \max_{r\ne0}\ \ell(y,r).$$

**Lemma R′ (corrected form of Lemma R).** Let $p>k$ be prime, $l\ge1$,
$M=lp$, $b=\iota\bmod M$. If $M\ge1/\Lambda(k,c)$, then every lift
$w=b+My\pmod{cM}$ of $b$ by $c$ is (i) proper with a grid witness if $y$ is
nontrivial, (ii) proper by the gcd clause if $y=j\iota$ with
$\gcd(1+jM,c)>1$, and (iii) otherwise a unit multiple of $b$ mod $cM$.

*Proof.* The Reduction of `structure.md` §6 says: $w$ has a witness iff for
some $r\in\mathbb Z_c$ the set $\mathcal G(y,r)$ meets the coset
$\frac r{cM}+\frac1M\mathbb Z$. The coset depends on $r$. So what is needed is
one $r\ne0$ for which $\mathcal G(y,r)$ *itself* contains a closed arc of
length $\ge1/M$; such an arc meets every translate of $\frac1M\mathbb Z$. By
definition of $\Lambda$ this holds for every nontrivial $y$. Parts (ii) and
(iii) are unchanged from Lemma R. ∎

The statement in `structure.md` takes the longest arc of the *union* over
$r\ne0$. An arc of the union made of pieces of $\mathcal G(y,1)$ and
$\mathcal G(y,2)$ need not meet the right coset, so that form is not what the
proof gives. For $c=2$ the union has one term and the two forms coincide, so
nothing proved there changes; `shift_gap.c` already takes the max over $r$.

### 1.2 Reductions used by the computation (proved)

1. **Translation.** $\mathcal G(y+j\iota,r)=\mathcal G(y,r)-\frac{jr}{c}$,
   since $i(t+\frac{jr}c)+\frac{y_ir}c = it+\frac{(y_i+ji)r}{c}$. So we may
   take $y_1=0$, and then $y$ is trivial iff $y=0$. This leaves $c^{k-1}-1$
   vectors.
2. **Reflection.** For integer $y_i$, $\frac{y_i(c-r)}c\equiv-\frac{y_ir}c$,
   so $\mathcal G(y,c-r)=-\mathcal G(y,r)$ and $\ell(y,c-r)=\ell(y,r)$. For
   $c=3$ this makes $r=1$ alone sufficient. The codes still compute both
   $r=1,2$, and their per-$r$ minima agree, as a consistency check.
3. **Exactness.** The bad set of speed $i$ is the union of the open arcs
   $$\Big(\frac{n-y_ir/c-1/(k+1)}{i},\ \frac{n-y_ir/c+1/(k+1)}{i}\Big),\qquad n\in\mathbb Z .$$
   Every endpoint has denominator dividing $c(k+1)i$, hence dividing
   $D=c(k+1)\operatorname{lcm}(1,\dots,k)$. So $\mathcal G(y,r)$ is a finite
   union of closed arcs with endpoints in $\frac1D\mathbb Z$, and $\ell$ is
   computed exactly in integers. For $k=17$, $c=3$: $D=661{,}620{,}960$.
4. **No wrap.** With $y_1=0$, speed 1 removes $(-\frac1{k+1},\frac1{k+1})$, so
   $\mathcal G\subset[\frac1{k+1},\frac k{k+1}]$.

### 1.3 Codes and checks

- **(A) `shift_gap_exact.c`.** DFS over $y_2,\dots,y_k$; the good set is a
  sorted list of disjoint closed integer intervals, and each speed subtracts
  its open arcs exactly. $c^{k-1}-1$ leaves; $k=17$, $c=3$ takes 32 s.
- **(B) `shift_gap_sort.c`.** A different algorithm: for each $y$ and $r$ it
  lists all $1+\dots+k$ bad arcs, sorts them by left end and sweeps.
  Full enumeration again; a few minutes for $k=17$, $c=3$.
- **(C) `shift_gap_check.py`.** Python `Fraction`s, no normalisation of $y$:
  random samples (400 at $(7,3)$, 200 at $(17,2)$ and $(17,3)$) plus the
  argmins. It checks the translation and reflection identities on every
  sample and compares $\ell(y,r)$ with (B)'s `eval` mode exactly:
  0 mismatches (`results/shift_gap_check.txt`).
- **Validation against the grid bounds** of `structure.md` (which are lower
  bounds): exact $\Lambda(15,2)=1/288\ge1/292.2$ and
  $\Lambda(17,2)=1/420.75\ge1/422.1$, each within the grid error $2/G$;
  $\Lambda(7,2)=1/84$ equals the grid value. (A) and (B) agree on every value
  and on the argmin sets.

### 1.4 Results (`results/shift_gap_exact.txt`)

| $k$ | $c$ | nontrivial $y$ ($y_1=0$) | $\Lambda(k,c)$ | argmins ($y_1=0$) | $1/\Lambda$ |
| --- | --- | --- | --- | --- | --- |
| 7 | 2 | 63 | $1/84$ | 2 | 84 |
| 7 | 3 | 728 | $1/96$ | 2 | 96 |
| 15 | 2 | 16,383 | $1/288$ | 2 | 288 |
| 15 | 3 | 4,782,968 | $1/264$ | 2: $\pm e_{14}$ | 264 |
| 17 | 2 | 65,535 | $4/1683$ | 2 | 420.75 |
| 17 | 3 | 43,046,720 | $1/352$ | 2: $\pm e_8$ | 352 |

At $k=17$, $c=3$ only 4 of the $4.3\cdot10^7$ vectors have $1/\max_r\ell\ge300$;
all others are below 300.

### 1.5 The tight-orbit kill for $k=17$ at large $p$ (proved)

**Theorem K.** Let $p\ge353$ be prime. Along the lift chain $\times3,\times2,\times3$
(levels $3,6,18$), the improper lifts of the level-one unit orbit of
$(1,\dots,17)$ are exactly the unit orbit of the integer tuple $(1..17)$ at
levels 3 and 6, and there are **none at level 18**. Along
$\times2,\times3,\times3$ the same holds for every prime $p\ge421$.

*Proof.* Corollary R (with Lemma R′ in place of Lemma R) needs
$L_{j-1}p\ge1/\Lambda(17,c_j)$ at each step.

- Chain $3,2,3$: the conditions are $p\ge352$, $3p\ge420.75$ and $6p\ge352$,
  all implied by $p\ge353$.
- Chain $2,3,3$: they are $p\ge420.75$, $2p\ge352$ and $6p\ge352$, all implied
  by $p\ge421$ (and 421 is prime).

Lemma T1 ($18\nmid3,6$, and $18\mid18$) gives the level-by-level conclusion.
Every unit of $\mathbb Z_{lp}$ lifts to a unit of $\mathbb Z_{clp}$, so it is
enough to lift the integer representative. ∎

**Label:** proved, resting on the exact finite computation of item 1 (two
independent implementations).

**Direct check** (`results/tight_orbit_k17_check_P0.jsonl`, `tight_chain.py`):
at $p=353,359,421$ with $\times3\times2\times3$ the trace (witness-free lifts,
orbits) is $(3,1),(2,1),(0,0)$, and at $p=421$ with $\times2\times3\times3$ it is
$(2,1),(3,1),(0,0)$. This is exactly the pattern of Lemma R′: at a $\times3$ step
with $3\nmid M$, one of the three trivial lifts is gcd-proper; at a $\times2$
step with $M$ odd, one of the two.

**Scope.** This is a statement about one level-one orbit. A $J$-empty gate at
$p\ge353$ must still kill the rest of the level-one family; Theorem K only
shows that the tight orbit, which survives every level not divisible by 18
(Lemma T1), never needs special treatment there. The range $p<353$ is covered
by direct computation, done by the small-primes track for $37\le p\le300$
(not duplicated here) and in `structure.md` for 307–907.

---

## 2. The Lemma S gates $p=31,29,23,19$ for $k=17$ (computed; no gate closes)

**Setting.** For $k=17$ these are the primes with $k+2\le p\le 2k+1$. Lemma S
gives level one exactly: $n=(p-1)/2=15,14,11,9$ classes, and $8$, $40$, $728$,
$1430$ unit orbits (Burnside; reproduced by `small_gates.level_one`). Each step
keeps the witness-free lifts on the grid $\frac1{lp}\mathbb Z$, drops lifts
that are proper by the gcd clause, drops lifts settled by Lemma NG at a
divisor of the new level, and reduces to unit orbits (`cascade.sh`,
`cascade_chain.sh` with `CASCADE_NG=1`, i.e. `liftfree.c | orbit_filter.c ng`).

| $p$ | chain | level | witness-free lifts | gcd-proper | NG-settled | improper unit orbits | CPU |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | $\times2$ | 2 | 161,764 | 39 | 0 | 75,530 | 2 s |
| 31 | $\times2\times2$ | 4 | 54,319,056 | 0 | 32 | **18,145,635** | 22 min |
| 31 | $\times3$ | 3 | 35,660,518 | 70 | 124 | **6,344,186** | 17 min |
| 29 | $\times2$ | 2 | 1,260,662 | 265 | 0 | 421,686 | 14 s |
| 23 | $\times2$ | 2 | 8,538,286 | 8,099 | 0 | 605,189 | 79 s |
| 19 | $\times2$ | 2 | 49,878,016 | 19,305 | 0 | 1,697,639 | 6.4 min |

Records: `results/gate_k17_p31_binary_ng_partial.jsonl`,
`results/gate_k17_p31_chain323_partial.jsonl`,
`results/gate_k17_level2_p29_23_19.jsonl`.

- **Independent check.** At all four primes the level-2 orbit sets produced
  by `liftfree.c | orbit_filter.c` and by `k17struct/cascade_verify.c` are
  identical, file for file (`results/gate_k17_level2_verify.txt`, with SHA-256
  prefixes). The verifier is a generalisation of `structure/cascade_verify.c`
  to any lift factor $c$. It has its own gcd clause, its own NG test and its
  own canonical form, it processes coordinates in reverse order, and it uses
  a different sound cut. The cut drops a branch only when some still-open
  witness time is good for every choice of every remaining coordinate.
  The level-3 and level-4 sets were not re-checked.
- **Comparison.** For $k=15$, $p=31$ the cascade ran $1\to186\to42{,}541\to27{,}881\to0$.
  For $k=17$, $p=31$ it is $8\to75{,}530\to18{,}145{,}635$, a factor of 240 at
  the second step. A level-8 step over $1.8\cdot10^7$ representatives, each
  with a $2^{17}$ fibre on a grid twice as fine, would take on the order of
  $10^2$ CPU-h or more by the observed rate. That is far beyond this track's
  budget, so the runs were stopped as instructed.
- **Lifting by 3 first is worse.** The grid $\frac1{3p}\mathbb Z$ is coarse,
  so 8 level-one orbits give $6.3\cdot10^6$ orbits at level 3.
- **Gate conditions (for the record; no gate is claimed).** A closing gate
  would need $p>18$, which holds for all four primes, and
  $p\nmid\operatorname{lcm}(2..17)=12{,}252{,}240$, which also holds. It would
  use Lemma NG and so LRC($m$) for $m\le16$, and it would close at a level
  divisible by 18 (Lemma T1). By §3, a level that small cannot work at
  $p=19$ or $p=23$.

**Label:** computed partial cascades; no gate condition is met, and nothing
is added to $\sum\ln p$.

---

## 3. Lemma TN: Lemma T elements that NG never settles

Lemma T (`gates.md` §1; Lemma N of `small-primes.md`) builds, from a cover of
size $s\le k-2$, an element of $I(k,p,l)$ for every level $l$ with $p\nmid l$.
The task here is to decide when Lemma NG settles it.

**Lemma TN.** Let $p>k+1$ be prime. Let $C=\{c_1,\dots,c_s\}$ be a set of
folded classes that covers every folded time, i.e. every $a\in\mathbb Z_p^*$
has some $i$ with $(k+1)\,d_p(ac_i)<p$. Put $f=k-s\ge2$. Let $l\ge2$ with
$p\nmid l$, and let $e_1,\dots,e_f$ be divisors of $l$ such that:

- **(R)** $\gcd(l,\ e_j: j\ne j_0)=1$ for every $j_0$;
- **(N)** for every divisor $d\ge2$ of $l$ with $E_d=\{j: d\nmid e_j\}\ne\varnothing$,
  $$\sum_{j\in E_d} g_j\left\lceil\frac{2d}{(k+1)g_j}\right\rceil\ \ge\ d,\qquad g_j=\gcd(e_j,d).$$

Define $w\in\mathbb Z_{lp}^k$ by CRT:

- $w_i\equiv c_i\pmod p$ and $w_i\equiv0\pmod l$ for $i\le s$;
- $w_{s+j}\equiv1\pmod p$ and $w_{s+j}\equiv e_j\pmod l$ for $j\le f$.

Then $w$ is improper at level $l$, and Lemma NG at no divisor $d\ge2$ of $l$
settles it. The same holds for $w\bmod l'p$, for every $l'\mid l$, with the
pattern $\gcd(e_j,l')$. Hence the witness + gcd + NG cascade at $p$ is
**nonempty at level $l$, along every lift chain that reaches $l$**.

*Proof.*

1. **No witness.** This is the argument of Lemma T, and it uses only the
   first $s$ coordinates. Let $t=m/(lp)$.
   - If $p\nmid m$: $w_i=lw_i'$ with $w_i'\equiv c_il^{-1}$, so
     $\lVert tw_i\rVert=\lVert ac_i/p\rVert$ with $a\equiv ml^{-1}\not\equiv0$.
     $C$ covers $a$.
   - If $p\mid m$: $tw_1\in\mathbb Z$.
2. **The gcd clause fails.** Deleting a cover coordinate leaves
   $\gcd(l,\text{all }e_j)=1$. Deleting the free coordinate $j_0$ leaves
   $\gcd(l,e_j:j\ne j_0)=1$ by (R).
3. **NG fails.** Let $d\ge2$ divide $l$.
   - The cover coordinates are $\equiv0\pmod l$, hence divisible by $d$.
   - A free coordinate satisfies $\gcd(w_{s+j},d)=\gcd(e_j,d)$, because
     $d\mid l$.
   - So the NG set $E$ equals $E_d$, and the NG sum equals the left side of
     (N).
   - If $E_d=\varnothing$, NG does not apply, since it needs $\lvert E\rvert\ge1$.
     Otherwise (N) says that the NG inequality fails. The version with
     $\lvert E\rvert\ge2$, as in `small-primes.md`, is weaker and fails as
     well.
4. **Projection.** (R) and (N) pass to $l'\mid l$ with $e_j'=\gcd(e_j,l')$:
   - the gcds in (R) only shrink;
   - (N) at $d\mid l'$ is the same condition, since $\gcd(e_j',d)=\gcd(e_j,d)$.
5. **The cascade is nonempty.** The NG test at $d$ depends only on the
   residue mod $d$. So the cascade at level $L$ is exactly $I(k,p,L)$ minus
   the classes settled by NG at some divisor of $L$, up to unit orbits. This
   follows by induction along the chain, using F1 and the fact that every
   unit lifts. ∎

**Monotonicity (proved).**

- If $l$ admits no pattern, neither does any multiple of $l$, by step 4.
- A pattern for $f$ gives one for $f+1$: append $e=1$, which keeps (R) and
  only increases the sums in (N).

**Search** (`ng_obstruction.py`). Only the pattern $e_j=\gcd(u_j,l)$
matters, so the search runs over multisets of $f$ divisors of $l$:

- **Exhaustive DFS.** A branch is cut only when some chosen coordinate already
  forces $E_d\ne\varnothing$ and even maximal costs for the remaining
  coordinates cannot reach $d$. Such a branch is NG-settled at $d$ throughout.
- **Divisor inheritance.** A level is tested only if every $l/q$ admits a
  pattern; otherwise it is closed by monotonicity.
- **Checks.**
  - Explicit CRT tuples were built from patterns at $(p,l)=(31,2)$, $(29,4)$,
    $(23,36)$, $(23,48)$, $(19,144)$, $(19,576)$ and $(19,768)$. Each is
    confirmed improper and not NG-settled by `cascade_verify.c` with $c=1$
    (`results/ng_obstruction_witness_check.txt`).
  - Two closed cases, $(31,4)$ and $(29,6)$ with the unit pattern, are
    confirmed NG-settled.
  - It is consistent with the $k\le8$ data of `structure.md` §5. For
    $(k,f)=(7,2)$, $(8,3)$ and $(5,2)$, on binary levels $\le64$, patterns
    exist only at levels 2, $\le4$ and $\le4$, while those cascades end with
    only tight survivors.

**Results for $k=17$, levels $l=2^a3^b\le3000$** (`results/ng_obstruction_f*.txt`).
Here $f=17-\tau_{17}(p)$, with $\tau$ from `small-primes.md` §3 for $p\ge37$,
and $\tau=n$ for the Lemma S primes.

| $f$ | primes with this $f$ | maximal levels with a pattern | minimal closed levels | least closed multiple of 18 |
| --- | --- | --- | --- | --- |
| 2 | 31 | 2 | 3, 4 | 18 |
| 3 | 29; $\tau=14$: 71, 173, 179, 197, 211, 223–241, 257 | 3, 4 | 6, 8, 9 | 18 |
| 4 | $\tau=13$: 53, 83, 89, 103, 137, 157, 163, 167, 181, 191, 193, 199 | 6, 8 | 9, 12, 16 | 18 |
| 5 | $\tau=12$: 43, 47, 59, 61, 67, 73, 97, 101, 107, 127, 131, 139, 149, 151 | 9, 16, 24 | 18, 27, 32, 48 | 18 |
| 6 | 23; $\tau=11$: 79, 113 | 32, 36, 48 | 27, 64, 72, 96 | **54** |
| 7 | $\tau=10$: 41, 109 | 64, 108, 144, 192 | 81, 128, 216, 288 | **162** |
| 8 | 19; $\tau=9$: 37 | 324, 432, 576, 768 | 243, 512, 648, 864, 1152 | **486** |

"Maximal levels with a pattern" lists the maximal elements, under
divisibility, of the set of levels at which a Lemma TN pattern exists; that
set is closed under taking divisors. For the Lemma S primes, $f=k-n$; for
$p\ge37$, $f=17-\tau_{17}(p)$. The $\tau$ values ("223–241" means every prime
in that range) are taken from `small-primes.md` §3 and were not recomputed
here.

**Consequences (proved, given the exact search).** A witness + gcd + NG
cascade can be empty at level $L$ only if two things hold:

- $18\mid L$. By Lemma T1 the class of $(1..17)$ is improper whenever
  $18\nmid L$, and NG settles it at no $d=2^a3^b\le10^5$: $\lvert E\rvert=k$,
  or the NG sum is at least $d$. This was checked directly by a one-line
  Python loop.
- No Lemma TN pattern exists at $L$.

Hence:

- **$p=19$ and $p=37$ ($f=8$).** No witness + gcd + NG cascade over levels
  $2^a3^b$ is empty at any level dividing 576, 768, 432, 324, 256 or 162. Its
  first possible closing level divisible by 18 is 486, i.e. modulus
  $486\cdot19=9234$.
- **$p=23$, $79$, $113$ ($f=6$).** The first possible closing level divisible
  by 18 is 54, because 18 and 36 are obstructed.
- **$p=41$, $109$ ($f=7$).** It is 162.
- **$f\le5$.** Lemma TN gives nothing beyond what Lemma T1 already forces
  (level 18).
- **$p=31$.** Lemma TN obstructs only level 2, yet the cascade has
  $1.8\cdot10^7$ orbits at level 4. The growth there comes from other
  improper classes, not identified here.
  - The level-2 survivors are **not** of near-gcd shape. The number of even
    coordinates is a unit-orbit invariant ($N=62$ is even and units are odd).
    Across the 75,530 orbits it ranges over 1–15 and peaks at 6–7; only 36
    orbits have 15 even coordinates (`results/gate_k17_p31_level2_parity.txt`).
  - So the width is generic, a coarse-grid effect: at $N=62$ a witness needs
    $d_{62}(mw_i)\ge4$ for all 17 coordinates. Removing near-gcd families
    with a shift lemma is unlikely to cure it (heuristic).

**What this says about the $k\le8$ pattern** (`structure.md` §5: with NG,
only the tight instances survive). That pattern cannot hold at low levels
whenever $\tau_k(p)$ is small. The Lemma TN elements are improper,
NG-unsettled and non-tight at every obstructed level: their coordinates are
$\equiv0\pmod l$ in $s$ places, and unit multiples preserve that. For the
$k\le8$ Lemma S pairs, Lemma TN obstructs only levels $\le4$, which is
consistent with convergence by level 64. A proof that the cascade converges
to the tight instances would need, at the least, the level to exceed every
Lemma TN level. For $k=17$ that is far up at $p=19,23,37,41,79,109,113$.

---

## 4. Failed routes and open leads

- **The Lemma S gates of $k=17$ with the current pipeline.** They grow to
  $10^6$–$10^7$ orbits by level 2–4 (§2). Stopped, as instructed. Do not
  re-run them without a new reduction.
- **Lifting by 3 early.** At $p=31$ it is worse than binary first
  ($6.3\cdot10^6$ orbits at level 3, against $7.6\cdot10^4$ at level 2).
- **Open leads:**
  1. Identify the improper classes behind the $p=31$ growth (8 orbits →
     $1.8\cdot10^7$ at level 4). A Lemma TN-type family with near-gcd
     structure mod 2 or 4, rather than mod $l$, is the natural suspect. If
     such a family can be described in closed form, NG (or a stronger shift
     lemma) could be tested on it symbolically instead of by enumeration.
  2. A rigidity lemma like Lemma R′ for a general base tuple $b$ (the
     computation is the same with speed $b_i$ in place of $i$). This would
     handle any small family of tight-type survivors at a high binary level
     with the $\times3\times3$ steps for free, once $lp\ge1/\Lambda_b(3)$.
  3. Extend the Lemma TN search to levels with prime factors 5 and 7. The
     NG divisors $d=5,7,10,\dots$ might close the obstructed families at
     lower cost than powers of 3.
  4. A stronger shift lemma than NG: Allikvere's Lemma 2.2(ii) allows any
     argument that every integer tuple in a class is lonely. The Lemma TN
     elements are the first test cases for one.

## 5. Reproduction

All runs used one core under `nice -n 10`, from `computations/lonely-runner/k17struct/`:

- $\Lambda$: `cc -O3 -o sge shift_gap_exact.c && ./sge 17 3` (32 s);
  `cc -O3 -o sgs shift_gap_sort.c && ./sgs 17 3 | tail -3`;
  `printf '0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0\n' | python3 shift_gap_check.py 17 3 200 3 ./sgs`.
- Tight orbit at $P_0$: `python3 tight_chain.py 17 "3 2 3" 353 359 421`.
- Cascades: `CASCADE_NG=1 bash cascade.sh 17 p 4 OUT`, then
  `./cv 17 p 1 2 ng < OUT/L1.txt | LC_ALL=C sort -u | cmp - OUT/L2.txt`
  (`cv` = `cascade_verify.c`).
- Lemma TN: `python3 ng_obstruction.py 17 f 3000` for $f=2..8$;
  `python3 ng_obstruction.py witness 17 p l e_1 ... e_f | ./cv 17 p l 1 ng`.
