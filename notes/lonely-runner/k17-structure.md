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

(Further rows are added below as the small-gate runs finish.)

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
  Full enumeration again; about 5 min for $k=17$, $c=3$.
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
