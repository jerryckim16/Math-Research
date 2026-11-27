# Lonely Runner: structural lemmas and small gates (structure track)

*Best read on the [progress site](https://jerryckim16.github.io/Math-Research/notes/lonely-runner/structure.html), where all the math is typeset. GitHub's own preview does not render the math in long files.*

> **Correction (2026-11-25, k17-structure track).** In Lemma R, $\Lambda(k,c)$ must be defined as $\min_y \max_{r\ne 0}$ of the longest arc of $G(y,r)$. It is not the longest arc of the union over $r$, because the coset that must be hit depends on $r$. The code always computed the max over $r$, and for $c = 2$ the two definitions coincide, so no result on this page changes. The corrected statement and proof are Lemma R′ in `k17-structure.md`.

Working notes of the "structure" track (2026-11-25). Notation follows
`problems/lonely-runner.md`:

- LRC($k$) is the conjecture for $k$ speeds, i.e. $k+1$ runners.
- $I(k,p,l)$ is the set of improper tuples and $J(k,p)$ the set of tuples
  that are not eventually proper, in the prime-gate framework
  (Sungkawichai–Trakulthongchai, Def. 2.1).
- F1, F2, Lemma D and Lemma E are as written out in the problem file.
- $\lVert x\rVert$ is the distance to the nearest integer, and $d_N(x)$ the
  folded residue of $x$ mod $N$.

Code is in `computations/lonely-runner/structure/`; outputs are in its
`results/` folder.

**Allikvere's prior work.** Several items below re-derive results already
in J. Allikvere, "Sixteen lonely runners" (Zenodo
10.5281/zenodo.23304361, Oct 2026, unrefereed): Lemma S with the same orbit
counts, the $p = 29$ and $p = 31$ gates for LRC(15), and the weighted shift.
They are **independent re-derivations**. We first derived Lemma S and ran
$p = 31$, and only then read his files (`gates_29_31_records.zip`,
`N15_SMALL_PRIME_SHIFT_GATE_SEARCH.md`, manuscript source), as data only.
The archives' SHA-256 sums match his `SHA256SUMS.txt`.

## Summary

| # | Statement | Label |
| --- | --- | --- |
| 1 | Lemma S: for a prime $k+2\le p\le 2k+1$, $I(k,p,1)$ is exactly the multisets whose $\pm$ classes cover every class; orbit count by Burnside | **proved**; checked against `covergen.c` and `level1.c` at 26 pairs $(k,p)$ |
| 2 | $J(15,31)=\varnothing$ by binary level 16, so $31 \mid v_1\cdots v_{15}$ for every counterexample to LRC(15) | **certificate-checked computation**, two independent implementations, given LRC(14); re-derivation of Allikvere's gate |
| 3 | $p=29$ for $k=15$: level 2 matches Allikvere exactly; our run reached level 4 only. $p = 23, 19, 17$ not run | partial; stopped when the target moved to $k=17$ |
| 4 | Lemma NG (weighted shift) | **proved**; the same as Allikvere's Lemma "weighted shift" |
| 5 | With NG, the small-gate binary cascade leaves exactly the known tight instances ($4\le k\le 8$) | computed observation (heuristic pattern) |
| 6 | Lemma R (rigidity of the tight orbit) and Cor. R: for $k = 15$, the tight orbit dies at binary level 16 for **every** prime $p\ge 293$ | **proved**, with one exact finite computation (`shift_gap.c`) |
| 7 | $k=17$: Lemma S orbit counts at $p = 19, 23, 29, 31$; the tight orbit $(1..17)$ dies at level 18 under the chain $\times2\times3\times3$ | counts **proved**; kill **computed** at 8 primes in 307–907; Cor. R covers the $\times 2$ step for $p\ge 423$ |
| 8 | Beck–Everett relation theorem | cited preprint; **proof verified by reading**; tested; **no pruning** |
| 9 | Alon–Bucić–Davies matrix theorem | cited preprint; **implies nothing for LRC($k$)** |

---

## 1. Lemma S: cover radius $\pm1$ at small primes

**Lemma S.** Let $k\ge 2$, and let $p$ be a prime with $k+2\le p\le 2k+1$.
Put $n=(p-1)/2$. For $v\in(\mathbb Z_p\setminus 0)^k$ the following are
equivalent:

1. $v\in I(k,p,1)$, i.e. no $t\in\frac1p\mathbb Z$ has
   $\lVert tv_i\rVert\ge\frac1{k+1}$ for all $i$;
2. for every $a\in\mathbb Z_p\setminus0$ some $i$ has $av_i\equiv\pm1\pmod p$;
3. the classes $\{\pm v_i\}$ cover all $n$ classes of $\mathbb Z_p^*/\{\pm1\}$.

This forces $k\ge n$. For $p=2k+1$ prime, $I(k,p,1)$ is exactly the unit
orbit of $(1,2,\dots,k)$.

*Proof.* The gcd clause is void at level 1, and $t=0$ is never a witness.
For $a\ne0$, let $d=d_p(av_i)\in\{1,\dots,n\}$. Then
$\lVert av_i/p\rVert=d/p$, and this is $\ge \frac1{k+1}$ iff $(k+1)d\ge p$.

- If $d\ge2$, then $(k+1)d\ge 2k+2>p$, so the inequality holds.
- If $d=1$, then $k+1<p$, so it fails.

So $a/p$ is a witness iff no $i$ has $av_i\equiv\pm1$; this is (1)⇔(2).
Condition (2) says that every class $\pm a$ equals some $\pm v_i^{-1}$.
Inversion is a bijection of $\mathbb Z_p^*/\{\pm1\}$, which gives (3). For
$p=2k+1$ we have $n=k$, so the $\pm v_i$ are $k$ distinct classes that
exhaust all of them. ∎

**Corollary (orbit count).** The group $G=\mathbb Z_p^*/\{\pm1\}$ is cyclic
of order $n$. A member of $I(k,p,1)$ is "each class once" plus a multiset of
$k-n$ extra classes, and units act on it by translating the extras. So the
unit orbits of $I(k,p,1)$ correspond to the $G$-orbits of $(k-n)$-multisets
on $G$, and Burnside gives their number:

$$\#\text{orbits}=\frac1n\sum_{d\mid\gcd(n,\,k-n)}\varphi(d)\binom{n/d+(k-n)/d-1}{(k-n)/d}\qquad(k>n),$$

and 1 if $k=n$.

| $k$ | $p$ | $n$ | unit orbits |
| --- | --- | --- | --- |
| 15 | 17, 19, 23, 29, 31 | 8, 9, 11, 14, 15 | 429, 335, 91, 1, 1 |
| 17 | 19, 23, 29, 31 | 9, 11, 14, 15 | 1430, 728, 40, 8 |

**Checks** (`test_small_gates.py`; output in
`results/lemma_s_validation.txt`):

- For all 26 pairs with $3\le k\le12$ and prime $k+2\le p\le 2k+1$, the
  orbit set from Lemma S equals the orbit sets from `covergen.c` (minimal
  covers plus extensions) and from the naive `level1.c`.
- Its size equals the Burnside count.
- At $k=15$ and $k=17$ the enumerated sets have the Burnside sizes (the
  $k = 17$ counts by `small_gates.level_one`).
- Allikvere's §3 of `N15_SMALL_PRIME_SHIFT_GATE_SEARCH.md` has the same
  $k=15$ table.

For $p>2k+2$ the cover radius is at least $\pm2$, and level one is a genuine
covering problem; Lemma S does not apply.

---

## 2. The gate $p=31$ for LRC(15)

**Claim.** $I(15,31,16)=\varnothing$, hence $J(15,31)=\varnothing$.

**Consequence.** Assume LRC(14). Lemma D then gives
$31\mid v_1\cdots v_{15}$ for every primitive counterexample $v$ to LRC(15).

**Method.**

1. By Lemma S, level one is the single orbit of $(1,\dots,15)$.
2. Binary cascade: lift each unit-orbit representative by 2, i.e. take the
   full fibre $w_i=b_i+j_i\,lp$ with $j_i\in\{0,1\}$.
3. Keep the lifts with no witness on the grid $\frac1{2lp}\mathbb Z$, then
   drop those proper by the gcd clause at level $2l$.
4. Canonicalise under units of $\mathbb Z_{2lp}$, signs and permutations
   (F2).

Why the orbit reduction is sound:

- Every unit of $\mathbb Z_{lp}$ lifts to a unit of $\mathbb Z_{2lp}$, and
  improperness projects (F1). So every element of $I(15,31,2l)$ lies in the
  orbit of an improper lift of a representative.
- A canonical form is an element of its input's orbit, so deduplication
  never loses an orbit.

| level $l$ | witness-free lifts | gcd-proper | improper unit orbits |
| --- | --- | --- | --- |
| 1 | — | — | 1 |
| 2 | 2,747 | 1 | 186 |
| 4 | 86,926 | 0 | 42,541 |
| 8 | 55,778 | 0 | 27,881 |
| 16 | **0** of $27{,}881\cdot2^{15}\approx9.1\cdot10^8$ | 0 | **0** |

**Independent agreement.**

- (A) `small_gates.py`: `liftfree.c` plus the gcd clause and canonical form
  in Python.
- (B) `cascade_verify.c`: a plain DFS over the whole fibre, with no cut, and
  its own witness bitsets, gcd clause and canonical form.
- (C) `cascade.sh`: `liftfree.c` plus `orbit_filter.c`.
- All three give the same witness-free counts and identical orbit sets at
  levels 2, 4 and 8, and 0 at level 16. Run times: (A) 53 s, (B) about
  2 min, (C) 44 s, on one core.
- Record: `results/gate_k15_p31.json`.

**Gate conditions** are those of any gate:

- $p>k+1=16$;
- $31\nmid 720720=\operatorname{lcm}(2..16)=2^4 3^2\,5\,7\,11\,13$, so
  $\operatorname{lcm}(2..16)\prod_{\text{gates}}p$ still divides
  $\prod v_i$;
- only grid witnesses and the plain gcd clause are used (no near-gcd lemma,
  no level-15 kill).

It adds $\ln31=3.434$.

**Label.** Certificate-checked computation (two implementations), given
LRC(14).

**Comparison.** Allikvere's `p31_gate_independent_replay.json` gives
$\ell_2=2746$ ($=2747-1$) and $\ell_{16}=0$. His $\ell_4,\ell_8$ count
lifts with multiplicity and are not comparable with our orbit counts. Both
computations die at level 16. He uses Lemma S and this certificate in his
Proposition "previously verified primes" (his set $\mathcal Q_0$ contains 29
and 31).

## 3. $p=29$ (and 23, 19, 17) for LRC(15): partial

- **Level 2 matches Allikvere exactly.** We get 5,257 witness-free lifts, 3
  gcd-proper (so 5,254 left) and 3,636 unit orbits. His $p = 29$ note has
  5,254 children and 3,636 swap orbits.
- **Level 4:** 3,538,878 witness-free lifts and 1,446,910 orbits
  (`results/gate_k15_p29_partial.jsonl`).
- **Not finished.** The level-8 step was stopped when the target moved to
  $k=17$.
- **His record** (`N15_P29_SINGLE_ORBIT_GATE.md`): the cascade dies at level
  32, with weighted $\ell_{16}=38{,}112$ and $\ell_{32}=0$.
- **Not run:** $p=23,19,17$, which he does not close. If they closed they
  would add $\ln17+\ln19+\ln23=8.91$ to his margin of 0.916. Their level-4
  families are expected to be at least as large as at $p=29$. With NG
  (§4–5), the cascade should shrink to the tight-type survivors.

---

## 4. Lemma NG (weighted shift)

**Lemma NG.** Let $k\ge2$ and assume LRC($m$) for all $m<k$. Let
$u\in\mathbb Z_{>0}^k$ and $d\ge2$. Put $E=\{i:d\nmid u_i\}$ and
$g_i=\gcd(u_i,d)$, and suppose $1\le\lvert E\rvert<k$. If

$$\sum_{i\in E} g_i\left\lceil\frac{2d}{(k+1)g_i}\right\rceil<d,$$

then some $t$ has $\lVert tu_i\rVert\ge\frac1{k+1}$ for all $i$.

*Proof.*

1. **A starting time.** The speeds outside $E$ take
   $m\le k-\lvert E\rvert\le k-1$ distinct values. LRC($m$) gives $t_0$
   with $\lVert u_jt_0\rVert\ge\frac1{m+1}>\frac1{k+1}$ for $j\notin E$.
2. **Shifts.** For $r\in\mathbb Z_d$ put $t_r=t_0+r/d$. For $j\notin E$,
   $d\mid u_j$, so $u_jt_r\equiv u_jt_0\pmod 1$.
3. **Bad shifts.** For $i\in E$, $u_it_r \bmod 1$ visits the $d/g_i$ points
   of a coset of $\frac{g_i}{d}\mathbb Z$, each $g_i$ times. An open arc of
   length $L$ contains at most $\lceil L/s\rceil$ points of spacing $s$
   (if $c$ fit, then $(c-1)s<L$). With $L = 2/(k+1)$, speed $i$ forbids at
   most $g_i\lceil 2d/((k+1)g_i)\rceil$ shifts.
4. **Conclusion.** Fewer than $d$ shifts are forbidden in all, so some
   $t_r$ works. ∎

- **Source.** For $k=15$ this is Allikvere's Lemma "weighted shift"
  ("Sixteen lonely runners"; cost $g\lceil d/(8g)\rceil$,
  $\lvert E\rvert\ge2$). It generalises the few-exception shift Lemma 3.12
  of arXiv:2609.02604v2. The proof here was written independently.
- **Use in a cascade.** If $d\mid l$, then $E$ and the $g_i$ are constant on
  a residue class mod $lp$. Such a class can be dropped through gate
  criterion (ii), and its lifts satisfy NG with the same $d$.
- **Implementation:** `orbit_filter.c` with flag `ng`; `CASCADE_NG=1` in
  `cascade.sh` and `cascade_chain.sh`.

## 5. What survives a small-gate cascade (computed pattern)

**Worked case: $k=7$, $p=11$.**

- The plain binary cascade does not close. Improper orbit counts at levels
  $2,\dots,256$ are 35, 252, 142, 34, 42, 82, 162, 322.
- The level-64 survivors are dyadic near-gcd families, e.g.
  $(1,x,64,128,192,256,320)\bmod 704$, with five coordinates
  $\equiv 0 \pmod{64}$.
- With NG the cascade closes at level 32: 35, 246, 130, 12, 0 orbits. NG
  settles 12 lifts at level 4 ($d=4$, $\lvert E\rvert=2$, cost $2<4$).

**Survey** of all Lemma S pairs with $3\le k\le8$, binary + NG cascade to
level 64. The survivors are exactly the known primitive tight instances with
$p\nmid\prod$, as literal integer tuples:

| pairs $(k,p)$ | survivors at level 64 |
| --- | --- |
| $(4,7)$ | $(1,2,3,4)$ |
| $(5,7)$, $(5,11)$ | $(1,2,3,4,5)$ and $(1,3,4,5,9)$ |
| $(6,11)$, $(6,13)$ | $(1..6)$ |
| $(8,11)$, $(8,13)$, $(8,17)$ | $(1..8)$ |
| $(3,5)$, $(3,7)$, $(7,11)$, $(7,13)$ | none: $k+1$ is a power of 2 |

At $(5,7)$ the plain cascade leaves 52 orbits, NG leaves 2. This is a
computed pattern, not a theorem.

**Lemma T1 (proved).** Let $p>k+1\ge4$ be prime and $l\ge1$. The class of
$(1,\dots,k)$ mod $lp$ is improper iff $(k+1)\nmid l$.

*Proof.* The integer tuple is lonely exactly at $t=s/(k+1)$ with
$\gcd(s,k+1)=1$. Such a time lies in $\frac1{lp}\mathbb Z$ iff
$(k+1)\mid l$. For the gcd clause, deleting one entry still leaves two
consecutive integers, so the gcd is 1. Witness transfer finishes the proof. ∎

NG never settles this class at a dyadic $d$, as long as $k+1$ is not a power
of 2. This was checked for all $k\le39$ and $d=2^a\le2^{11}$ (the one-line
check is reproduced in §7). So for $k=16$ and $k=17$ every gate chain must
pass through a level divisible by 17, respectively 18.

---

## 6. Rigidity of the tight orbit (any $k$; the structural kill)

Fix $k$, a prime $p>k$, a level $l$, and put $M=lp$. Let $b=(1,\dots,k)$,
viewed mod $M$; its entries are $<M$. Every lift of $b$ by a factor $c$ is

$$w=b+My \pmod{cM},\qquad y\in\mathbb Z_c^k.$$

Call $y$ **trivial** if $y\equiv j\,(1,\dots,k)\pmod c$ for some $j$. Then
$w\equiv(1+jM)\,b\pmod{cM}$.

**Reduction (proved).** For $t=m/(cM)$ with $m\equiv r\pmod c$,

$$t\,w_i\equiv i\,t+\frac{y_i r}{c}\pmod 1,\qquad t\in \frac{r}{cM}+\frac1M\mathbb Z .$$

This holds because $tw_i = im/(cM)+y_im/c$. So $w$ has a witness iff some
$r\in\mathbb Z_c$ and some $t$ in the coset $\frac{r}{cM}+\frac1M\mathbb Z$
lie in

$$\mathcal G(y,r)=\Big\{t\in\mathbb R:\ \Big\lVert it+\frac{y_ir}{c}\Big\rVert\ge\frac1{k+1}\ \ \forall i\Big\}.$$

**Lemma R (rigidity).** Let $\Lambda(k,c)$ be the minimum, over nontrivial
$y$, of the length of the longest closed interval in
$\bigcup_{r\ne0}\mathcal G(y,r)$. If $M\ge 1/\Lambda(k,c)$, then:

1. every nontrivial lift $w$ has a witness;
2. every trivial lift with $q=\gcd(1+jM,c)>1$ is proper by the gcd clause;
3. every other trivial lift lies in the unit orbit of the integer tuple $b$
   mod $cM$.

*Proof.*

1. A closed interval of length $\ge 1/M$ contains a point of every translate
   of $\frac1M\mathbb Z$; then apply the Reduction.
2. Since $1+jM\equiv1$ mod $l$ and mod $p$, $q$ divides $c$ and every
   $w_i=(1+jM)i$. So $\gcd(cl,\,w_j:j\ne i)\ge q>1$.
3. Otherwise $1+jM$ is a unit mod $cM$. ∎

**Corollary R.** Let $c_1,c_2,\dots$ be a lift chain, with
$L_j=c_1\cdots c_j$. Suppose $L_{j-1}p\ge1/\Lambda(k,c_j)$ at every step.
Then:

- at each level $L_j$ with $(k+1)\nmid L_j$, the improper part of the tight
  orbit is exactly one unit orbit, that of the integer tuple $(1..k)$
  (Lemma R and Lemma T1);
- at the first $L_j$ with $(k+1)\mid L_j$ it is empty: nontrivial lifts and
  gcd-type trivial lifts are proper by Lemma R, and the integer orbit has the
  witness $u^{-1}/(k+1)$.

**The finite input.** `shift_gap.c` evaluates
$\min_i\lVert it+y_ir/c\rVert$ exactly in integers at $t=m/G$. A run of $n$
consecutive good grid points certifies a closed good interval of length
$\ge(n-1)/G$. Since $c\mid G$, it is enough to treat $y$ normalised to
$y_1=0$: replacing $y$ by $y+j(1..k)$ translates $\mathcal G$ by $jr/c$.
Results (`results/shift_gap.txt`):

| $k$ | $c$ | $G$ | nontrivial $y$ | $\Lambda(k,c)\ge$ | so $M\ge$ suffices | $\max_t\min$ over worst $y$ $\ge$ |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 2 | 3360 | 63 | $40/3360=1/84$ | 84 | $1/7$ |
| 15 | 2 | 13440 | 16,383 | $46/13440=1/292.2$ | 293 | $1/15$ |
| 17 | 2 | 12240 | 65,535 | $29/12240=1/422.1$ | 423 | $1/17$ |

**Consequences.**

- **$k=15$ (proved, with the exact finite check).** For every prime
  $p\ge293$, the tight orbit $(1..15)$ has exactly one improper unit orbit
  (the integer tuple) at levels 2, 4 and 8, and none at level 16.
  - The step at level $l$ needs $lp\ge293$, so all steps are covered once
    $p\ge293$.
  - This explains Approach 6 of the problem file (counts 1, 2, 4, 0 lifts at
    all 79 primes 251–743), and extends it to **all** primes $\ge 293$.
  - With Approach 6's direct computation for 251–293, it holds for every
    prime $p\ge251$.
- **$k=17$.**
  - Chain $\times2\times3\times3$ (level 18). Corollary R covers the
    $\times2$ step for $p\ge423$.
  - $\Lambda(17,3)$ is **not** computed: there are $3^{16}\approx4.3\cdot10^7$
    normalised $y$, beyond this session's budget.
  - Direct computation (`tight_chain.py`, `results/tight_orbit_k17_chain2332_large.jsonl`):
    at $p=307,401,409,499,601,701,797,907$ the trace is 2 witness-free lifts
    and 1 orbit at level 2, 3 lifts and 1 orbit at level 6, and **0 at level
    18**. This is exactly the rigid pattern of Corollary R.
  - At small $p$ the pattern breaks (`results/tight_orbit_k17_chain2332_small.jsonl`,
    plain cascade without NG). The tight orbit still dies at level 18 at
    101, 103 and 107, but not by level 36 at 109 and 113.
- **Small primes for $k=17$.**
  - Level one at $p=31$ has 8 orbits, and the binary + NG cascade gives
    75,530 orbits at level 2; level 4 and beyond were not run. These gates
    need the $\times3\times3$ steps as well (Lemma T1).
  - Expected cost: at least the $k=15$, $p=29$ run (1.4M orbits at level 4).

---

## 7. Literature checked for structural consequences

**Beck–Everett, "Lonely Runner Relations"**, arXiv:2609.06259v3 (24 Nov
2026; preprint; read from the arXiv LaTeX source).

- **Thm 2** (= Thm 1(a)). Let $k\ge2$, $n\in\mathbb Z_{>0}^k$, and suppose
  no $t$ has $\lVert tn_j\rVert>\frac1{k+1}$ for all $j$ (every
  counterexample and every tight instance). Then some $m\in\mathbb Z^k$ has
  $m\cdot n=0$, $\sum m_j$ odd, and
  $$\lVert m\rVert_2\le\frac{2(k+1)}{\sqrt{k-1}},\qquad \lVert m\rVert_1\le 2k+3 .$$
  - The paper states distinct entries, but the proof does not use them.
  - The proof gives the general form: if $\operatorname{lon}(n)\le\delta<\frac12$,
    then $\lVert m\rVert_2^2\le (k-1)/(\frac12-\delta)^2$.
  - For $k=15$: $\lVert m\rVert_2^2\le 73$ and $\lVert m\rVert_1\le33$.
- **Proof check (by reading, line by line).**
  - The window lemma: $\sum_r a_r=1$ and $\sum_r r^2a_r=\frac1{4h^2}$, by
    Parseval for $\psi_h$ and $\psi_h'$.
  - Vanishing Fourier coefficients give $s_q$, with $\sum_q s_q=\frac12$.
  - $\sum_c w(c)\lVert Pc\rVert^2=\frac{k-1}{4h^2}$, so some $q$ has
    $X_q\le\frac{k-1}{2h^2}$. Then
    $\lVert x-y\rVert^2\le2(\lVert Px\rVert^2+\lVert Py\rVert^2)\le\frac{k-1}{h^2}$.
  - Parity rounding.
  - We found no gap. Thm 1(b) needs the flatness constant
    $\operatorname{flt}(k)$, which is unknown for $k=15$.
  - **Label:** cited preprint; proof verified by reading.
- **Tests** (`beck_everett_check.py`, `results/beck_everett_check.txt`;
  all pass):
  - every recorded tight instance has a harmful relation with
    $\lVert m\rVert_2^2=3$ (an $a+b=c$ relation);
  - exhaustive test of the general-$\delta$ form, 2,674 positive cases:
    $k=3$ (entries $\le24$, $\delta=\frac14,\frac13,\frac25$) and $k=4$
    (entries $\le14$, $\delta=\frac15,\frac14,\frac13$).
- **No pruning.**
  - Modulo $N=lp$ the relation becomes a congruence. There are
    $(3^{15}+1)/2\approx7.2\cdot10^6$ harmful $m\in\{-1,0,1\}^{15}$, against
    $N\le 11{,}888$.
  - In 200 random $v\in\mathbb Z_{16p}^{15}$, some harmful
    $m\in\{-1,0,1\}^{15}$ has $m\cdot v\equiv0\pmod N$, with at least 468
    completing half-vectors each.
  - So the level-one family, the cascade and the kill are not reduced. On
    the LRC(14) data the theorem is consistent, trivially: the persistent
    orbit $(1..14)$ has $2x_1-x_2=0$.
- **Failed route (kept): feeding a relation into the flag bound as a dual
  vector.** It gives $t_d\ge\lVert b_d^*\rVert_2^2/2\ge1/146$, against the
  forced $c_d\approx0.47$, so it adds nothing. Allikvere's "Sixteen lonely
  runners" gets 497.03 → 459.08 from relations by a different route (a rank
  analysis of odd ternary relations); not re-checked here.

**Alon–Bucić–Davies**, arXiv:2609.36220v1 (preprint; read from the arXiv
LaTeX source).

- **Theorem.** If $a_1,\dots,a_n\in\mathbb R^k$ have full spark, then
  $\sup_x\min_i\lVert a_i\cdot x-b_i\rVert\ge\frac{k}{2n}$ for every shift
  $b$. This settles Schoenberg's view-obstruction conjecture and the
  Henze–Malikiosis bound $\mu\le d/m$.
- **No consequence for LRC.**
  - At $k=1$ it is the trivial shifted bound $\frac1{2n}$.
  - It holds uniformly in the shifts, and the shifted LRC is false from
    $n=5$ (Blanco–Criado–Santos, arXiv:2603.24784). So no statement of this
    form can give $\frac1{n+1}$.

**The dyadic NG check of §5:** for $k\le39$ with $k+1$ not a power of 2,
and $d=2^a\le2^{11}$, the integer tuple $(1..k)$ violates the NG inequality
or has $\lvert E\rvert\in\{0,k\}$. This was checked by a direct Python
one-liner (in the session log; easy to re-run).

## 8. Failed routes and open leads

- **Beck–Everett pruning:** vacuous mod $N$ (§7).
- **Dual vector in the flag bound:** too weak (§7).
- **Binary cascade without NG at small $p$:** can leave dyadic near-gcd
  families (§5).
- **Direct $\times18$ lift of $(1..17)$ from level 1 with `liftfree.c`:**
  its branch and bound did not finish in about 5 min at $p = 401$.
  Abandoned; the chain $\times2\times3\times3$ takes 6 s.
- **Open leads:**
  1. Compute $\Lambda(17,3)$ (a C job over $3^{16}$ vectors, or a smarter
     search). It would prove that the $k=17$ tight orbit dies at level 18 for
     all large $p$.
  2. A proof of the §5 pattern: the binary + NG cascade converges to the
     tight instances.
  3. Finish $p=29$ and run $23,19,17$ for $k=15$ with NG.
  4. The $k=17$ small gates $19,23,29,31$, with chain
     $\times2\times3\times3$ and NG.
  5. A hand proof of $I(15,31,16)=\varnothing$.
