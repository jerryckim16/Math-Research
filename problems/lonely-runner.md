# Lonely Runner Conjecture

**Area:** Diophantine approximation / combinatorics
**Status:** in progress. Done so far:
- **New general-$n$ result (2026-11-26).** Every set of $n$ distinct positive speeds with largest speed $v_n \le 2n+2-E(n)$ is lonely, where $E(n) = \max_{j \le (n+1)/2}(j + g(j))$ and $g$ is Jacobsthal's function; this is about $\tfrac32 n$. Hence every set with $v_n \le 1.47\,n$ is lonely, for every $n$ (proved for $n \ge 85$, computed below). The best range valid for every $n$ that we found in the literature is Tao's $1.2\,n$. Proved, reviewed by the coordinator; see `notes/lonely-runner/general-n.md`.
- The prime-gate framework is reproduced end to end for $\mathrm{LRC}(3)$–$\mathrm{LRC}(10)$ (4–11 runners), conditional on one cited bound ($B_k$). $\mathrm{LRC}(10)$ uses an explicit $\times 11$ lift, independent of Sungkawichai–Trakulthongchai's Prop. corlarge (step 7).
- All 71 of Allikvere's 15-runner ($\mathrm{LRC}(14)$) gate certificates are independently re-checked, with no discrepancy found. Stored rows were checked in full at every gate; the cascade and kill in full at 54 gates and sampled at 17, with the cascade alone also in full at near-gcd gate 223; level-one completeness at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$). See "Independent re-check summary". His 14-runner terminal kills are re-checked at all 111 of his gate primes.
- **Allikvere's 16-runner ($\mathrm{LRC}(15)$) gate certificates: all 59 re-checked (2026-11-25), with no discrepancy.** Every stored row, the binary cascade to level 16, every SUMMARY total and the archive hashes were checked with our own code (`notes/lonely-runner/cert15.md`). **Level-one completeness is checked at 9 of the 59 gates ($p = 269, 281, 311, 313, 317, 331, 347, 349, 367$, each equal to the certificate; Approach 15)**; at the other gates, and especially at the large gates where the stored families are tiny, the claim rests mainly on his search. The completeness campaign was paused on 2026-11-26 by the owner's decision, to focus on original work (Approach 15).
- The $n = 15$ shape lemma $R_{15} < 49/100$ is proved (Approach 10; every inequality machine-checked exactly). The general-$n$ parts of Allikvere's Theorem 3.8 are independently verified (Approach 11), so the 16-runner gate target 483.239 is proved here, given $\mathrm{LRC}(m)$ for $m \le 14$.
- The cost of 16 runners with our code is estimated from measurements. **16 and 17 runners turn out to be already claimed** (Zenodo, Oct 2026; see the correction under Statement). The first unclaimed case is 18 runners.

**Started:** 2026-11-23 (literature upgraded to primary texts the same day, step 2)
**ProofAtlas:** rank 477

## Statement

Write $\lVert x\rVert$ for the distance from $x$ to the nearest integer.

**Conjecture (Wills 1967; Cusick 1973).** Let $n \ge 1$ and let $v_1, \ldots, v_n$ be
positive integers. Then there is a real $t$ with

$$\lVert v_i t\rVert \ge \frac{1}{n+1} \quad \text{for all } i = 1, \ldots, n.$$

- **Interpretation.** There are $n+1$ runners on a circular track of length 1, with one runner at rest. At some time $t$ every moving runner is at distance at least $1/(n+1)$ from the runner at rest.
- **Original form.** Runners have distinct real speeds and *each* runner is lonely at some time. That form reduces to positive integer speeds with one runner at rest: Wills 1968, Bohman–Holzman–Kleitman 2001 and Henze–Malikiosis, as recalled in the introductions of arXiv:2509.14111 and arXiv:2511.22427.
- **Repeated speeds are harmless.** With $k' < n$ distinct values, $1/(k'+1) > 1/(n+1)$.

Following the recent literature, write **$\mathrm{LRC}(k)$** for the statement with
$k = n$ speeds. $\mathrm{LRC}(k)$ is "the conjecture for $k+1$ runners".

The bound $1/(n+1)$ cannot be improved. Speeds $(1, 2, \ldots, n)$ attain it exactly
(re-checked below for $n \le 10$).

**Correction (2026-11-25, literature survey): 16 and 17 runners are already claimed.** See `notes/lonely-runner/literature.md`.

- $\mathrm{LRC}(15)$ (16 runners) is claimed by J. Allikvere, *Sixteen lonely runners*, Zenodo doi:10.5281/zenodo.23304361 (2026-10-11). It is a computer-assisted proof, not on arXiv and not refereed. It uses a new relation-rank bound $\log \prod v < 459.084$, the forced divisor 720720, 16 preliminary primes and 59 gate primes 269–659, with a margin of 0.916.
- $\mathrm{LRC}(16)$ (17 runners) is claimed by W. Toner, Zenodo doi:10.5281/zenodo.23552885 (2026-10-22), conditional on $\mathrm{LRC}(15)$. It is not refereed.
- **First case without a located claim: $\mathrm{LRC}(17)$, i.e. 18 runners.** Every 17-tuple of positive integers has a $t$ with all $\lVert v_i t\rVert \ge 1/18$.
- Our own $\mathrm{LRC}(15)$ work below (Approaches 10–13, the shape lemma and the flag-bound check) was done before these claims were found. It is an independent re-derivation of parts of Allikvere's approach, not a new result.
- Earlier text in this file calls $\mathrm{LRC}(15)$ the "next open case". Read that as "next case without an independently checked proof".
- The first case without a peer-reviewed proof is 11 runners.

## Known results

Labels:

- **[read]**: we read the primary text, from its arXiv LaTeX source unless stated otherwise.
- **[abstract]**: seen only via abstracts, search snippets or secondary pages.

Literature checked on 2026-11-23. In step 2, arxiv.org and zenodo.org became reachable and the four main computer-assisted papers were read.

| runners | $k$ | result | source | how checked |
| --- | --- | --- | --- | --- |
| 2, 3 | 1, 2 | trivial | classical | |
| 4 | 3 | proved | Betke–Wills 1972; Cusick 1974 | cited in the [read] introductions below |
| 5 | 4 | proved (computer-assisted) | Cusick–Pomerance 1984; simpler proof Bienia et al. 1998 | as above |
| 6 | 5 | proved | Bohman–Holzman–Kleitman 2001; simpler proof Renault 2004 | as above |
| 7 | 6 | proved | Barajas–Serra, *Electron. J. Combin.* 15 (2008) R48, arXiv:0710.4495 | [abstract] |
| 8 | 7 | proved (computer-assisted) | M. Rosenfeld, "The lonely runner conjecture holds for eight runners", arXiv:2509.14111 (v1 17 Sep 2025, v2), *Math. Comp.* (2026), doi:10.1090/mcom/4243 | **[read]** (journal reference as cited in arXiv:2609.02604) |
| 9 | 8 | proved (computer-assisted) | T. Trakulthongchai, "Nine and ten lonely runners", arXiv:2511.22427 (v1 27 Nov 2025, v2), *Electron. J. Combin.* 33(2) (2026) P2.46, doi:10.37236/14972; independently M. Rosenfeld, "The lonely runner conjecture holds for nine runners", arXiv:2512.01912 (v1 1 Dec 2025, v2; preprint) | **[read]** both |
| 10 | 9 | proved (computer-assisted) | Trakulthongchai, same paper | **[read]** |
| 11, 12, 13 | 10–12 | claimed (computer-assisted preprint) | T. Sungkawichai, T. Trakulthongchai, "Eleven, twelve, and thirteen lonely runners", arXiv:2604.23906 (Apr 2026, v2); code github.com/vzsky/lonely-runners | **[read]** (LaTeX source in the code repository) |
| 14 | 13 | claimed (computer-assisted preprint), two proofs | J. Allikvere, "Fourteen and fifteen lonely runners", arXiv:2609.02604 (v1 2 Sep 2026, "Fourteen lonely runners"; v2 24 Sep 2026). Certificates: Zenodo 10.5281/zenodo.22066772 | **[read]** v2 |
| 15 | 14 | claimed (computer-assisted preprint) | Allikvere, same v2. Certificates: Zenodo 10.5281/zenodo.22667683. 2,137 CPU-hours | **[read]**; 4 of 71 gate certificates spot-checked (below) |
| 16 | 15 | claimed (computer-assisted, Zenodo preprint) | J. Allikvere, *Sixteen lonely runners*, Zenodo 10.5281/zenodo.23304361 (2026-10-11) | metadata and manuscript source read (`notes/lonely-runner/literature.md`); all 59 gate certificates re-checked (rows, cascade, totals; `notes/lonely-runner/cert15.md`); level-one completeness independently checked at $p = 269, 281, 311, 313, 317, 331, 347, 349, 367$ (Approach 15) |
| 17 | 16 | claimed, conditional on 16 runners (Zenodo preprint) | W. Toner, *Seventeen lonely runners, assuming sixteen*, Zenodo 10.5281/zenodo.23552885 (2026-10-22) | metadata and PDF read; not re-checked |
| 18 | 17 | **open** (no located claim, 2026-11-25) | — | |

Details from the primary texts:

- **Rosenfeld, 8 runners ($k = 7$).**
  - Gate primes $S = \{31, 37, \ldots, 163\}$, i.e. all 27 primes from 31 to 163.
  - Bound: $\prod \le \bigl(\binom{8}{2}^{6}/7\bigr)^{7} < 7.4\cdot 10^{54}$ (Corollary 3).
  - Forced divisor: $\operatorname{lcm}(2,\ldots,8)$ (his Lemma 4).
  - His level is $l = k+1$ directly, i.e. times in $(1/((k+1)p))\mathbb{Z}$.
  - Table 1 there also does 4–7 runners:
    - $k = 3$: $\{7, 11, 13\}$
    - $k = 4$: $\{17, \ldots, 37\}$
    - $k = 5$: $\{23, \ldots, 71\}$
    - $k = 6$: $\{13, 19, 31, \ldots, 103\}$
- **Trakulthongchai, 9 and 10 runners.**
  - $S_8$ = all 39 primes from 47 to 241 ($\prod > 10^{82}$; $C_8 < 10^{80}$).
  - $S_9$ = all 47 primes from 137 to 401 ($\prod > 10^{112}$; $C_9 < 10^{111}$).
  - For $k = 8$, every $p$ with $11 \le p \le 43$ failed (non-empty $I(8,9,p)$).
  - Run times: 15 min ($k = 8$) and under 23 h ($k = 9$) on a 14-core M3 Max.
- **Rosenfeld, 9 runners (arXiv:2512.01912).** Proves $\mathrm{LRC}(8)$ independently, using a sharpened gcd lemma for $k = 8$ and prime powers (64, 81, 25, 121, 169, …) as moduli.
- **Sungkawichai–Trakulthongchai, 11–13 runners.** Gate tables and the polynomial Prop. 1.2 are as summarised in step 1. They report $k = 10$ in 45 min on a 10-core M4.
- **Allikvere, 14 and 15 runners.**
  - $\mathrm{LRC}(13)$, first proof: MSS bound $\ln B_{13} < 670.34974$, with 111 gate primes, $\sum \ln p = 681.5292$.
  - $\mathrm{LRC}(13)$, second proof: his flag bound (below), $\ln < 341.031991$, with 61 primes, $\sum = 353.7726$.
  - $\mathrm{LRC}(14)$:
    - Flag bound $\ln(v_1\cdots v_{14}) < 414.779365$.
    - Minus $\ln \operatorname{lcm}(2,\ldots,15) = \ln 360360 = 12.79485$, giving a target of 401.984506.
    - 71 gates (89, 131–241 selected, and every prime 239–569), $\sum \ln p = 408.8233$.
    - 19 gates ($\tau(p) \le 12$) also use the "few-exception shift" Lemma 3.12 through Lemma 2.2(ii). Those gates prove divisibility, not $J(14,p) = \emptyset$.
  - Total 2,137 CPU-hours. Our sum of the generation and kill CPU in `gates.json` is 2,028.6 h; the cascade wall time is not included.
  - He states: "The full computation has not been independently reimplemented or formally verified."

### Results for general n

- The trivial bound is $1/(2n)$.
- Tao (2018) proved $1/(2n) + c\cdot \log n/(n^2(\log\log n)^2)$.
- Bedert (arXiv:2511.16636, 2025) proved $1/(2n) + 1/n^{5/3+o(1)}$. Cited in the [read] intro of arXiv:2604.23906.
- Hu–Jing, "Near optimal gap in the lonely runner conjecture", arXiv:2610.23790 (Oct 2026), reportedly proves $(1+c)/(2n)$. [abstract]: seen via MathWorld only, not read.
- None of these settles any finite case.
- **Bounded speeds.** Tao (2018, Prop. 1.5): lonely if $v_n \le 1.2\,n$, for every $n$. Bohman–Peng and Pomerance: lonely if $n < v_n \le 2n - c(\log n)^2$, for sufficiently large $n$ (constants not explicit). Bonfioli (Zenodo 24189338, unrefereed): every $n$-set in $[1,2n]$ is lonely when $2n+1$ is prime (refereed here, correct). **Ours** (2026-11-26, proved): lonely if $v_n \le 2n+2-E(n) \approx \tfrac32 n$, hence if $v_n \le 1.47\,n$, for every $n$. Computed: every $n$-set in $[1,2n]$ is lonely for $n \le 51$. Details in `notes/lonely-runner/general-n.md`.

### The finite reduction (exact hypotheses, from the read texts)

- **MSS Theorem A** (Malikiosis–Santos–Schymura, *Forum Math. Sigma* 13 (2025) e164, arXiv:2411.06903), quoted as stated in arXiv:2509.14111:
  - *If LRC holds for $k$ [speeds], it holds for $k+1$ for every tuple with $\gcd(v) = 1$ and $\sum_{S\subseteq[k]} \gcd(\{v_i : i\in S\}) > \binom{k+1}{2}^{k-1}$.*
  - We have not read the MSS paper itself. Note that arXiv:2509.14111 indexes by $k$ with $k+1$ runners; Allikvere restates it as $\sum v_i < \binom{n+1}{2}^{n-1}$ for $n$ speeds.
- **Rosenfeld's Corollary 3** (by AM–GM). A gcd-1 counterexample to $\mathrm{LRC}(k)$, with $\mathrm{LRC}(k-1)$ assumed, has

  $$u_1\cdots u_k < B_k := \left(\binom{k+1}{2}^{k-1}\Big/k\right)^{k}.$$

  Values of $\ln B_k$:

  | $k$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | $\ln B_k$ | 7.45 | 22.09 | 46.11 | 80.59 | 126.33 | 184.04 | 254.3 | 337.6 | 434.5 | 545.3 | 670.35 | 810.07 | 964.75 |

- **Forced divisor** (Rosenfeld, Lemma 4; restated with proof as Allikvere's Lemma 3.9, `lem:divisor`, arXiv:2609.02604v2 §3.7). For a counterexample $u$ to $\mathrm{LRC}(k)$, $\operatorname{lcm}(2, \ldots, k+1) \mid u_1\cdots u_k$.
  - *Proof (checked here).* For $2 \le d \le k+1$, if $d$ divides no $u_i$, then at $t = 1/d$ every $\lVert u_i/d\rVert$ is a nonzero multiple of $1/d$, hence at least $1/d \ge 1/(k+1)$, and $t$ is a witness. So every such $d$ divides some $u_i$.
  - For each prime $r \le k+1$, the largest power $q_r \le k+1$ of $r$ therefore divides $\prod u_i$. The $q_r$ are pairwise coprime with product $\operatorname{lcm}(2, \ldots, k+1)$.
  - In a gate target the gate primes $p > k+1$ are coprime to this lcm, so $\operatorname{lcm}\cdot \prod p$ divides $\prod u_i$. This is how $\ln 720720$ enters the 16-runner target 483.239.
- **Allikvere's flag bound** (arXiv:2609.02604v2, Thm 3.8; due to Allikvere, building on Giri–Kravitz's projected lattice).
  - Setting: assume $\mathrm{LRC}(m)$ for all $m < n$, and let $v$ be a primitive positive counterexample to $\mathrm{LRC}(n)$.
  - Constants: $B_r = \bigl(2r/((n+1)(n+1-r))\bigr)^2$, $c_i = B_i - B_{i-1}$, and $K_n = \prod_{i<n} c_i$. The hypothesis is $c_{i+1}/c_i > 4/3$.
  - Conclusion: $v_1\cdots v_n < (A_n r_n/n)^n$ with $A_n = K_n^{-1/2}$, whenever the "shape factor" satisfies $R_n < r_n$ on the simplex.
  - He proves $r_{13} = 101/200$ and $r_{14} = 1/2$ (Lemma 3.7). That gives $\ln$ bounds 341.031991 ($n = 13$) and 414.779365 ($n = 14$).
  - **We re-derived $K_{13}$, $K_{14}$, the ratio minima 1175/688 and 847/513, and both log bounds exactly** (`flag_bound.py`, tested).
  - **$n = 15$ (our computation; not in the paper):**
    - The ratio minimum is $3751/2349 > 4/3$, exactly.
    - The paper's one-variable shape family gives $\min R_{15} \approx 0.48796$ numerically.
    - If a shape lemma $r_{15} = 49/100$ were proved, then $\ln(v_1\cdots v_{15}) < 496.727$, and the gate target after $\ln \operatorname{lcm}(2,\ldots,16) = \ln 720720$ would be 483.239. This agrees with the figure in the (unreviewed) munim lonely-runner-16 repository.
    - **The shape lemma $R_{15} < 49/100$ is now proved here** (Approach 10, step 9; machine-checked by `shape_lemma.py`). The general-$n$ parts of Theorem 3.8 are verified in Approach 11 (step 10), so the target 483.239 is proved here, given $\mathrm{LRC}(m)$ for $m \le 14$.
- **Prime gates (Sungkawichai–Trakulthongchai, Def. 2.1).** Fix $k \ge 2$, a prime $p$ and $l \ge 1$. Put $N = lp$ and $\mathbb{Z}_{p,l} = \{x \in \mathbb{Z}_N : p \nmid x\}$. Then $w \in \mathbb{Z}_{p,l}^k$ is *$(k,p,l)$-proper* if either
  - (a) $\gcd(l, w_1, \ldots, \widehat{w}_i, \ldots, w_k) > 1$ for some $i$, or
  - (b) some $t \in (1/N)\mathbb{Z}$ has $\lVert t w_i\rVert \ge 1/(k+1)$ for all $i$.

  $I(k,p,l)$ is the set of improper tuples. $J(k,p)$ is the set of $v \in \mathbb{Z}_{p,1}^k$ that are not eventually proper.
- **Lemma D** (Trakulthongchai, Lemma 5; Allikvere, Lemma 2.2(i)). Let $k \ge 3$, assume $\mathrm{LRC}(k-1)$, and suppose $J(k,p) = \emptyset$. Then $p \mid u_1\cdots u_k$ for every counterexample $u$.
  - Allikvere's Lemma 2.2(ii) relaxes this: improper lifts are allowed if every integer tuple in their residue class is lonely.
- **Lemma E** (Sungkawichai–Trakulthongchai, Lemma 2.4). $J(k,p) = \emptyset$ iff $I(k,p,l) = \emptyset$ for some $l$.
- **Proposition V** (Sungkawichai–Trakulthongchai, Prop. 2.6). Assume $\mathrm{LRC}(k-1)$ and $J(k,p) = \emptyset$ for all $p \in P$. If $\prod_P p \ge B_k$, then $\mathrm{LRC}(k)$ holds. With the forced divisor or the flag bound, the target changes accordingly.
- **Tight tuples force $l$.** $(1, \ldots, k)$ is lonely exactly at $t = s/(k+1)$ with $\gcd(s, k+1) = 1$. So for $p > k+1$, $I(k,p,l) = \emptyset$ requires $(k+1) \mid l$.

Other relevant work:

- Blanco–Criado–Santos, arXiv:2603.24784, give counterexamples to the *shifted* LRC from $n = 5$. This does not affect the unshifted conjecture. Allikvere says their reformulation gives the same bound as MSS.
- Giri–Kravitz, *Math. Proc. Cambridge* 180 (2026), arXiv:2304.01462, prove a weaker finite-checking bound.
- Goddyn–Wong 2006 study tight tuples.
- Zhang, arXiv:2608.13599, studies tight one-entry modifications. [abstract]

## Elementary lemmas used by our reproduction (proofs)

**Witness transfer.** If $u \equiv w \pmod N$ and $t = m/N$, then $u_i t - w_i t \in \mathbb{Z}$, so $\lVert u_i t\rVert = \lVert w_i t\rVert$.

**Lemma D (proof).** Take a counterexample $u$. We may assume $\gcd(u) = 1$ (replace $t$ by $t\cdot g$). Suppose that $p \nmid u_i$ for every $i$, and let $w = u \bmod lp \in \mathbb{Z}_{p,l}^k$. Since $I(k,p,l) = \emptyset$, $w$ is proper.

- If (b) holds, witness transfer makes $u$ lonely, which is a contradiction.
- If (a) holds, let $d = \gcd(l, w_j : j \ne i) > 1$.
  - Then $d \mid u_j$ for $j \ne i$, since $d \mid l \mid N$.
  - Because $\gcd(u) = 1$, $\gcd(d, u_i) = 1$.
  - $\mathrm{LRC}(k-1)$, applied to $(u_j)_{j\ne i}$ (repeats allowed), gives $t_0$ with $\lVert u_j t_0\rVert \ge 1/k$ for $j \ne i$.
  - The times $t_0 + r/d$ leave every $u_j t_0$ unchanged mod 1, and move $u_i t_0$ through a full coset $x + (1/d)\mathbb{Z}$.
  - One of these points has $\lVert\cdot\rVert \ge 1/2 - 1/(2d) \ge 1/4 \ge 1/(k+1)$, using $k \ge 3$.
  - So $u$ is lonely, which is again a contradiction. ∎

This is the same argument as Rosenfeld's Lemma 5 in arXiv:2509.14111 and Allikvere's Lemma 2.2.

**F1 (improperness projects).** Let $w$ be improper at level $clp$, and let $w' = w \bmod lp$. A witness for $w'$ would be a witness for $w$, and a gcd divisor $d \mid l$ for $w'$ divides $cl$ and the corresponding $w_j$. So $w'$ is improper. Consequently, lifting and projecting chains keep a preimage of every $v \in J(k,p)$ (Prop. 3.1 of arXiv:2604.23906). If the final stage is empty, $J(k,p) = \emptyset$.

**F2 (symmetry).** Properness is invariant under permutations, sign changes, and units of $\mathbb{Z}_N$. $\mathbb{Z}_{cN}^* \to \mathbb{Z}_N^*$ is onto, so one orbit representative suffices. At level 1, every orbit contains $(1, a_2 \le \cdots \le a_k)$ with $1 \le a_i \le (p-1)/2$.

**Lemma E (proof of $\Rightarrow$).** Let $l = \operatorname{lcm}$ over $v$ of a level $l_v$ at which $v$ has no improper lift. Properness transfers up to level $lp$. ∎

**Minimal-cover generation** (`covergen.c`; our proof, same idea as Allikvere §4.1).

- The $k$-multiset $M$ lies in $I(k,p,1)$ iff its folded classes *cover* every folded time class $1, \ldots, (p-1)/2$, where $v$ covers $a$ iff $(k+1)\cdot d_p(av) < p$.
- Any such $M$ is $C + (k-\lvert C\rvert)$ arbitrary classes, where $C \subseteq \operatorname{supp} M$ is a minimal cover ($\lvert C\rvert \le k$).
- Units map covers to covers, so every orbit has a representative with $1 \in C$.
- The DFS adds class 1 first, then repeatedly branches on the uncovered time with fewest allowed coverers, excluding earlier siblings. It cuts a node only when $(k - \lvert L\rvert) \cdot \text{max-gain} < \#\text{uncovered}$.
  - This reaches every minimal cover containing 1 exactly once: follow, at each node, the first candidate that lies in $C$. The leaf is a cover inside $C$, hence equal to $C$.
- We do **not** implement Allikvere's private-time normalisation (his Lemma 4.1). Our tree is therefore larger, about $14\times$ at $k = 14$, $p = 401$.

## Approaches

### 1. Exact checker for one tuple (done, step 1)

`lonely.py` provides:

- a complete search over left endpoints of the good intervals, with no-witness certificates;
- exact $\mathrm{ML}(v)$, attained at some $a/(v_i+v_j)$.

The proofs are in the docstring.

### 2. Prime-gate sieve, reproduced end to end for 4–11 runners (done)

- **Steps 1–2:**
  - The level-one step uses a naive bitset DFS ($k \le 8$) or the minimal-cover generator ($k = 9, 10$). For $k = 10$ the $\times 11$ lift uses `liftfree.c`.
  - Lifting and projection chains are as in arXiv:2604.23906.
  - The exact test $\prod p \ge B_k$ uses the MSS/Rosenfeld $B_k$. We do not use the flag bound or the forced divisor in our reproductions.
- **Cross-check against the papers' gate sets:**
  - **$k = 6$:** our failing primes (11, 17, 23, 29) are exactly the gaps in Rosenfeld's set $\{13, 19, 31, \ldots\}$.
  - **$k = 7$:** our first passing prime (31) equals Rosenfeld's.
  - **$k = 8$:** our passing set from 47 is all 39 primes from 47 to 241, **identical to Trakulthongchai's $S_8$**.
  - **$k = 9$:** every prime from 137 to 401 passed, **identical to Trakulthongchai's $S_9$**.
  - **$k = 10$:** every prime from 127 to 467 passed (61 primes), **identical to Sungkawichai–Trakulthongchai's $P_{10}$**. They reach it via Prop. corlarge; we reach it via an explicit $\times 11$ lift (Next steps 6).
- **Failed gates (kept):**
  - $k = 3$: $p = 5$.
  - $k = 6$: $p = 11, 17, 23, 29$.
  - $k = 7$: $p = 11, \ldots, 29$.
  - $k = 8$: $p = 11, 13, 17$. That run was restarted from 47, and Trakulthongchai reports 11–43 all fail.

  At small $p$ the time grid is too coarse.

### 3. Naive level-one DFS (measured, step 1): does not scale

The number of leaves is $\binom{(p-1)/2 + k - 2}{k - 1}$. That works out to about $10^{14}$ core-hours for $k = 15$. Kept for reference.

### 4. Minimal-cover generator (step 2): validated; cost measured

- **Validation.** On 125 $(k,p)$ pairs ($k = 3, \ldots, 8$, primes up to 89), its orbit set equals the naive enumerator's (`test_lonely.py` keeps a subset).
- **Speed.** At $k = 7$, $p = 173$: 0.05 s against 3.7 s for the naive enumerator.
- **Cost-estimation mode.**
  - Knuth's random-probe estimator of the tree size: 20,000 probes. Validated against exact node counts at $k = 7, 8, 9$ within 0.3%.
  - A capped timed DFS: about 2–$3\cdot 10^{6}$ nodes/s on one (shared) core.
- **Estimated tree sizes for ours:**

  | $p$ | 251 | 263 | 307 | 353 | 401 | 449 | 503 | 569 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | $N_{14}$ | 9.5e10 | 1.4e11 | 6.1e11 | 1.1e12 | 2.2e12 | 3.3e12 | 1.0e13 | 1.9e13 |
  | $N_{15}$ | 4.2e11 | 9.2e11 | 4.1e12 | 1.3e13 | 3.0e13 | 5.8e13 | 8.4e13 | 1.9e14 |

- **Comparison with Allikvere.** His tree at $k = 14$, $p = 401$ has $1.6\cdot 10^{11}$ nodes and took 44,413 CPU-s. Ours is $2.2\cdot 10^{12}$ nodes, about 300 CPU-h. So his private-time pruning is worth about $14\times$ in nodes. Our generator alone is too slow for $k = 15$; his normalisation must be added.

### 5. Spot check of Allikvere's 15-runner certificates (step 2)

`check_allikvere.py` reads the archives as data only and uses our own code throughout. It ran on four of the 71 gates: $p = 401, 397, 311, 263$. Every archive's SHA-256 matches the published `SHA256SUMS.txt`.

For each of the four gates we checked:

1. Every stored level-one row is witness-free at level 1, i.e. lies in $I(14,p,1)$. The row counts were 394, 3,072, 130,999 and 812,780.
2. Every km1 cover extended by every class is also improper.
3. **Cascade.**
   - Lifting all rows by 2 up to level 32 with our `liftfree.c` (branch-and-bound over lift digits, a separate code path) plus the gcd clause leaves exactly one orbit: $(1, \ldots, 14)$. This matches the certificate.
   - For every listed level-2 survivor row, our count of improper level-2 lifts equals the certificate's `l2`, with 0 mismatches. The totals are 3, 2, 23 and 1023.
   - At $p = 263$ our count of *distinct* lifts is 1021, because two pairs of rows share a lift. This is not a discrepancy.
4. **Level-15 kill of $(1,\ldots,14)$.**
   - Witness-free lifts: 3 at level 3 and 5 at level 5.
   - 15 CRT candidates, of which 7 are witness-free on the level-15 grid.
   - All 7 are proper by the gcd clause.
   - This is identical to the certificate at all four gates.

**Not checked:**

- *Completeness* of the level-one rows, i.e. that every orbit of $I(14,p,1)$ is represented. This needs a $k = 14$ generator run, about 12 CPU-h per gate for his code and about 300 CPU-h for ours at $p = 401$.
- The other 67 gates.
- The 19 near-gcd gates ($\tau \le 12$, $p \le 241$), which use Lemma 3.12.
- The $\mathrm{LRC}(13)$ archive (174 MB).
- The flag-bound shape Lemma 3.7. We did re-check $K_n$ and the log constants. (Later re-checked, step 9: Approach 10.)

### 6. Tight orbit for 16 runners (step 2)

`tight_orbit_k15.py` tracks the tight tuple $(1, \ldots, 15)$ at all 79 candidate gate primes $251, \ldots, 743$. At every prime it has 1, 2 and 4 improper lifts at levels 2, 4 and 8, and **none at level 16**. This is computed exactly with `liftfree.c` plus the gcd clause.

So, unlike 14 and 15 runners, the tight orbit needs no extra fibre search at these primes. This agrees with the munim repository's 10-prime pilot. Only this one orbit is examined: these are not gate checks.

### 7. Independent re-check of Allikvere's certificates (steps 3–4)

**Tools** (all ours, archives read as data only):

- `gatecheck.c`:
  - `cascade`: per-row binary cascade to level 32, directly from Def. 2.1.
  - `kill`: level-3 and level-5 witness-free lifts, CRT to level 15, level-15 grid, gcd clause, then the few-exception shift Lemma 3.12 ($d \in \{3, 5\}$, $m_d = \lceil 2d/15\rceil$).
- `canon.c`: unit-orbit canonical forms.
- `check_gate_full.py` checks, per $\mathrm{LRC}(14)$ gate:
  - **A.** The archive SHA-256 matches the published `SHA256SUMS.txt`.
  - **B.** Every stored irredundant row is witness-free at level 1.
  - **C.** The cascade counts (l2, l4, l8, l16, l32) agree **per unit orbit** with the certificate's `filt/*.out`, with the same set of survivor orbits.
    - The comparison is per orbit because the certificate deduplicates km1 extension rows, so rows cannot be matched one-to-one. Improper-lift counts are unit-invariant (F2).
    - The orbits persisting to level 32 equal the orbits of the certificate's `kills/`.
  - **D.** Every kill record (wf3, wf5, CRT candidates, wf15, improper after gcd, improper after near-gcd) equals ours. Improper after near-gcd is 0, and for "$J(14,p) = \emptyset$" claims improper after gcd is also 0.
- `completeness_check.py`: level-one completeness (below).
- `check_lrc13_kills.py`: the $\mathrm{LRC}(13)$ archive (below).

**Downloads.** 58 of the 71 $\mathrm{LRC}(14)$ archives were downloaded: every archive under 60 MB, which is all 52 "J empty" gates and 6 of the 19 near-gcd gates. All 58 SHA-256 sums match. The 13 archives over 60 MB (near-gcd gates 131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241; up to 1.6 GB) were not downloaded.

**$\mathrm{LRC}(14)$ results.** Two summary files are generated from the results:

- `results/lrc14_gates/COVERAGE.md` (from `coverage_table.py`): every one of the 71 gates, with the status of each check (archive hash, rows, cascade, kill, completeness) marked full, sampled or not checked.
- `results/lrc14_gates/SUMMARY.md` (from `summarize_step3.py`).

Per-gate JSON files are in `results/lrc14_gates/`.

**Overall verdict (step 5, checkpoint 5):** independent re-check of 71/71 $\mathrm{LRC}(14)$ gates.

- All 52 "J empty" gates were checked in full.
- 19 of the 19 near-gcd gates were checked: every stored row tested, with the cascade and kill on seeded samples (3,000, or 500 for the large archives).
- Level-one completeness was checked at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$).
- **No discrepancy was found.**
- **All 71 gates are now covered.**

- **"$J(14,p) = \emptyset$" gates (decomposition type, $\tau(p) \ge 13$): all 52 checked in full. All pass.**
  - Step 3 covered the 47 primes from 263 to 569.
  - Step 4 added 239, 251, 257, 271 and 277, one at a time with 1 process. These have 1.34M, 2.25M, 5.65M, 10.0M and 2.77M stored irredundant rows, and 2,030, 3,228, 12,208, 26,521 and 3,266 survivor orbits on both sides respectively. Each took 8–75 min.
  - At every gate, the persistent orbit is exactly $(1,\ldots,14)$ and the kill record is identical.
- **Near-gcd gates ($\tau(p) \le 12$, divisibility via Lemma 2.2(ii)):**
  - **$p = 89$, sampled:** 3,000 random rows and 3,000 random persistent orbits out of 186,365, seeded.
    - Cascade: 2,998 orbits compared, 2,671 survivor orbits on both sides, 0 count mismatches.
    - Every sampled persistent row lies in a certificate orbit.
    - Kills: all 3,000 match the records. Totals: 2,249,044 CRT candidates, 1,211,876 witness-free at level 15, 354,688 left by the gcd clause, **0 after the near-gcd lemma**.
    - Time: 2,535 s.
  - **$p = 179$:** sampled: 1,000 random rows and 1,000 random persistent orbits out of 8,011, seeded, 2 processes, 815 s.

    - All 2,133,835 stored irredundant rows are improper; this test covers every row, not a sample.
    - Cascade: 1,000 orbits compared, 25 survivor orbits on both sides, 0 count mismatches.
    - Kills: all 1,000 match. Totals: 356,114 CRT candidates, 281,826 witness-free, 81,280 left by the gcd clause, **0 after the near-gcd lemma**.
    - A first run with 3,000/3,000 was lost to a container restart.
  - **$p = 179$, full (step 8):** every row and every persistent orbit, 4 processes, 8,864 s (`results/lrc14_gates/gate_179_full.json`).
  - **$p = 223$, full cascade only (step 8):** every stored row and every improper extension row (1,886,974 + 328,893). The results matched: 2,160,276 unit orbits, survivor orbits 62,638 = 62,638 (none only on one side, 0 count mismatches), and persistent-orbit sets equal (48,071 = 48,071). 4 processes, 8,999 s (`results/lrc14_gates/gate_223_fullcascade.json`). The kill at 223 is still the 3,000-orbit sample.
  - **$p = 233$, full cascade only (step 8):** every stored row and every improper extension row (5,767,782 + 782,536). The results matched: 6,517,315 unit orbits, survivor orbits 70,223 = 70,223 (none only on one side, 0 count mismatches), and persistent-orbit sets equal (13,457 = 13,457). 4 processes, 3,634 s (`results/lrc14_gates/gate_233_fullcascade.json`).
  - **$p = 233$, full (step 8):** every row and every persistent orbit, cascade and kill together. The cascade figures repeat the run above exactly. All 13,457 kill records are reproduced, with 0 mismatches; totals: CRT 4,528,173, wf15 3,674,453, improper after gcd 1,056,768, improper after near-gcd shift 0. 4 processes, 10,703 s (`results/lrc14_gates/gate_233_full.json`).
    - Cascade: all 2,676,385 orbits of stored rows (irredundant rows plus improper km1 extensions) re-run; 70,089 survivor orbits on both sides, 0 count mismatches.
    - Persistent orbits: our set equals the certificate's, 8,011 = 8,011.
    - Kills: all 8,011 records match. Totals: 2,920,345 CRT candidates, 2,284,817 witness-free at level 15, 659,328 left by the gcd clause, **0 after the near-gcd lemma**.
    - $p = 179$ is the first near-gcd gate re-checked in full (apart from level-one completeness).
  - **$p = 233$ (step 4, redone), sampled 3,000/3,000:**
    - All 5,767,782 stored rows are improper.
    - Cascade: 46 survivor orbits among the sample on both sides.
    - Kills: all 3,000 of 13,457 match; 0 after the near-gcd lemma.
    - Time: 2,790 s.
  - **$p = 223$ (step 4), sampled 3,000/3,000:**
    - All 1,886,974 stored rows are improper.
    - Cascade: 140 survivor orbits among the sample on both sides.
    - Kills: all 3,000 of 48,071 match. Totals: 1,063,346 CRT candidates, 845,170 witness-free, 243,968 left by the gcd clause, **0 after the near-gcd lemma**.
    - Time: 2,883 s.
  - **$p = 163$ and $p = 173$ (step 5),** run with the streaming checker `check_gate_stream.py`, sample 3,000:
    - All stored rows are witness-free at level 1: 7,383,739 at $p = 163$ and 7,777,371 at $p = 173$. All km1 covers are covers.
    - Cascade: 3,000 uniformly sampled irredundant rows (99 and 74 with survivors) plus 3,000 uniformly sampled extension-survivor lines (of 726,154 and 538,767). 0 mismatches.
    - Kills: 3,000 of 107,244 and 3,000 of 96,840 match. 0 improper after the near-gcd lemma.
    - The number of kill files equals the certificate's persistent-orbit count.
    - Time: about 34 min each.
  - **Large near-gcd archives (step 5),** streaming checker, **sample 500** (500 irredundant rows, 500 extension-survivor lines, 500 kills per gate). Every stored row is tested, and every gate passes with 0 mismatches and 0 improper after the near-gcd lemma:
    - $p = 131$: 5,463,210 rows; 2,239,365 kill files; extension-survivor lines 8,725,762; 611 s.
    - $p = 149$: 4,307,522 rows; 967,875 kill files; extension-survivor lines 3,203,434; 411 s.
    - $p = 157$: 29,230,783 rows; 3,541,563 kill files; extension-survivor lines 14,912,271; 850 s.
    - $p = 167$: 32,890,555 rows; 1,599,697 kill files; extension-survivor lines 7,563,522; 562 s.
    - $p = 181$: 142,334,217 rows; 8,235,157 kill files; extension-survivor lines 38,160,231; 1605 s.
    - $p = 191$: 27,201,490 rows; 2,362,553 kill files; extension-survivor lines 7,713,522; 617 s.
    - $p = 193$: 15,203,915 rows; 973,342 kill files; extension-survivor lines 2,888,145; 502 s.
    - $p = 197$: 46,411,987 rows; 312,041 kill files; extension-survivor lines 2,092,913; 410 s.
    - $p = 199$: 25,180,487 rows; 196,288 kill files; extension-survivor lines 817,224; 367 s.
    - $p = 211$: 45,883,385 rows; 165,061 kill files; extension-survivor lines 1,079,040; 396 s.
    - $p = 227$: 28,242,035 rows; 44,974 kill files; extension-survivor lines 308,105; 353 s.
    - $p = 229$: 19,201,544 rows; 62,072 kill files; extension-survivor lines 314,785; 350 s.
    - $p = 241$: 22,356,624 rows; 14,401 kill files; extension-survivor lines 78,382; 361 s.
  - **Not checked:**
    - None: all 19 near-gcd gates are covered (sampled as stated).
- **No discrepancy with any certificate was found.** Two apparent issues turned out to be artefacts of our own scripts:
  - $p = 263$: 1021 against 1023 level-2 lifts. The certificate counts with multiplicity over rows; per-row counts agree exactly.
  - The $k = 13$ SHA-256 lookup: duplicate kill-file copies under `cloud_gates/` with LF line endings were matched against the wrong manifest. With paths resolved relative to each manifest, every file matches.

**Level-one completeness ($p = 89$, a near-gcd gate).**

- Method: `covergen.c` enumerated all 1,689,912 minimal covers containing class 1 ($8.5\cdot 10^{6}$ search nodes), expanded them to 10,174,414 multisets, and `canon.c` reduced them to orbits. This is **without** Allikvere's private-time pruning.
  - At the time of this step-3 run, the pruning (his Lemma 4.1) was not yet implemented here (it is now: Approach 8). The unpruned search is exhaustive by the argument in `covergen.c`'s header and fits the budget at $p = 89$.
- Result: **687,016 orbits, equal to the orbit set of the certificate's 966,696 stored rows** (110,720 irredundant + 19,454 km1 covers $\times$ 44 extensions). There are no orbits on only one side.
- **$p = 239$ ("J empty" gate, step 4).**
  - Generation: unpruned `covergen.c`, sharded over 3 cores with `LRC_NSHARDS=3`. Sharding is tested to give exactly the unsharded output. It took $4.75\cdot 10^{10}$ search nodes and about 88 min wall time, producing 18,810,658 minimal covers. Those expand to 20,093,082 multisets.
  - Result: **1,441,284 orbits, exactly equal to the orbit set of the certificate's 1,442,327 stored rows** (1,342,843 irredundant + 99,484 extension rows). No orbit appears on only one side.
- **$p = 251$ ("J empty" gate, step 6).**
  - Generation: `covergen.c` **with `LRC_PRUNE=2`** (Lemma 4.1 plus max-private normalisation; Approach 8), sharded over 3 cores. It took $8.93\cdot 10^{10}$ search nodes and about 4 h 55 min wall time (the shards were uneven: 1 h 46 min, 1 h 47 min, 4 h 55 min), producing 3,876,360 covers. Those expand to 4,143,952 multisets.
  - Result: **2,404,346 orbits, exactly equal to the orbit set of the certificate's 2,405,962 stored rows.** No orbit appears on only one side.
  - Because this run is pruned, its completeness rests on the Lemma 4.1 / normalisation proof transcribed in Approach 8 (and its tests) as well as the minimal-cover argument. The $p = 89$ and 239 runs are unpruned and rely on the minimal-cover argument alone.
- **$p = 251$ again (step 13)**, with the faster generator (`LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, Approach 13): the same 3,876,360 covers and 2,404,346 orbits, equal to the certificate. $1.35\cdot 10^{10}$ nodes, 7,505 CPU-s, 33 min wall on 4 cores (`results/lrc14_gates/regen_251_order.json`).
- **Step 14: more "J empty" gates with the faster generator** (`LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, 16 shards on 4 cores, `results/lrc14_gates/completeness_<p>.json`). Gates were chosen cheapest first by Knuth estimates (`results/knuth_completeness_step14.txt`).
  - $p = 269$: **197,957 orbits, equal to the certificate** (none only on one side); 318,113 covers; $1.22\cdot 10^{10}$ nodes; 8,433 CPU-s; 36 min wall.
  - $p = 263$: **849,135 orbits, equal to the certificate** (none only on one side); 1,376,334 covers; $1.91\cdot 10^{10}$ nodes; 12,517 CPU-s; 56 min wall.
  - $p = 283$: **480,781 orbits, equal to the certificate** (none only on one side); 741,139 covers; $2.17\cdot 10^{10}$ nodes; 18,665 CPU-s; 82 min wall (run with another job sharing the cores).
  - $p = 281$ (step 17, orderly generator `LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1`, 32 depth-2 shards): **496,107 orbits, equal to the certificate** (none only on one side); 486,408 covers; $4.69\cdot 10^{9}$ nodes; 1,903 CPU-s; 8 min wall.
- Not done: completeness at the other 64 gates (a $p = 179$ run was lost in a step-3 restart).

**$\mathrm{LRC}(13)$ archive** (Zenodo 10.5281/zenodo.22066772, `fourteen_lonely_runners_package.zip`).

- The zip's MD5 matches Zenodo's (9b65648956…); Zenodo publishes only MD5 for this record.
- **The archive does not store the level-one rows for $k = 13$** (only generator logs). So rows, cascade and completeness cannot be re-checked from it.
- Checked instead, at **all 111 gate primes** (83 to 877; the list is in `results/lrc13_kills.jsonl` and equals the set of `certificates_p<p>` directories in the archive). This includes $p = 199$, whose kill records are the root-level files `kill_tight_final.txt` and `kill_gw_final.txt` referenced by `certificates_p199/SUMMARY.json`:
  - Each kill file's SHA-256 against its gate's `MANIFEST_SHA256.json` (all match).
  - Our recomputation of the terminal level-14 step for both persistent orbits, $(1,\ldots,13)$ and $(1,\ldots,11, 13, 24)$:
    - the improper level-2 members (1–8 per orbit);
    - for each member, all witness-free lifts by 7 (liftfree.c, $M = 2p$, $c = 7$) and the gcd clause at $l = 14$.
- **All match the certificates:** exactly one witness-free lift per member, and 0 improper after the gcd clause. At $p = 83$ even the search-node count (17,753,408) coincides with the record.
- Not checked: the other 92 of the 111 primes; the binary cascade; the level-one family.

### 8. Private-time pruning for the level-one generator (step 6)

**Notation.** Fix $k$ and a prime $p$. Put $n = (p-1)/2$ (folded time classes $1, \ldots, n$) and folded speed classes $1, \ldots, n$. Class $v$ *covers* time $a$ iff $(k+1)\cdot d_p(av) < p$. For a set $C$ of classes and $v \in C$, the *private times* of $v$ in $C$ are the times covered by $v$ and by no other class of $C$; write $\mathrm{priv}_C(v)$ for their number.

**Fact.** Every class covers exactly $m = \lfloor (p-1)/(k+1)\rfloor$ times.

- As $a$ runs over $1, \ldots, n$, the folded residue $d_p(av)$ runs over $1, \ldots, n$ bijectively, because $v$ is a unit and folding identifies $\pm$.
- $(k+1)x < p \Leftrightarrow x \le m$, since $(k+1) \nmid p$.

**Lemma 4.1 (Allikvere, arXiv:2609.02604v2; our transcription).** Let $C$ be a cover of all $n$ times by $s$ distinct classes. Some class of $C$ has at least $q_s := \lceil \max(0, 2n - s\cdot m)/s\rceil$ private times.

*Proof.* Let $n_j$ be the number of times covered by exactly $j$ classes of $C$.

1. Counting incidences: $s\cdot m = \sum_j j\cdot n_j \ge n_1 + 2(n - n_1)$.
2. So $n_1 \ge 2n - s\cdot m$.
3. The $n_1$ singly-covered times are private to their class, and there are $s$ classes, so by pigeonhole one class has at least $\lceil n_1/s\rceil \ge q_s$ of them. ∎

**Normalisation.**

- Multiplying by a unit $u$ maps covers to covers: $v$ covers $a$ iff $uv$ covers $u^{-1}a$. So it maps private times of $v$ to private times of $uv$ bijectively.
- Hence every unit orbit of minimal covers contains a representative $C \ni 1$ in which class 1 has the **largest** number of private times. Choose $v$ with maximal $\mathrm{priv}_C(v)$ and scale by $v^{-1}$.
- Then in particular $\mathrm{priv}_C(1) \ge q_{\lvert C\rvert}$.
- Every improper $k$-multiset is $C$ + extras for a minimal cover $C$ (see `covergen.c`), so restricting to these representatives keeps at least one representative of every orbit of $I(k,p,1)$.

**Search cuts** (`covergen.c`, environment `LRC_PRUNE`):

- **`LRC_PRUNE=1` (Lemma 4.1).**
  - Leaf filter: $\mathrm{priv}_C(1) \ge q_{\lvert C\rvert}$.
  - Node cut: class 1's private set only shrinks when classes are added, and $q_s$ is non-increasing in $s$ ($\lvert C\rvert \le k$). So a node whose current $\mathrm{priv}(1) < q_k$ has no passing leaf below it, and a child that would bring $\mathrm{priv}(1)$ below $q_k$ is skipped. Its class is still excluded for later siblings, exactly as in the unpruned search.
- **`LRC_PRUNE=2` (max-private normalisation, Allikvere §4.1).**
  - Leaf filter: $\mathrm{priv}_C(1) \ge \mathrm{priv}_C(v)$ for every $v \in C$.
  - Node cut ("locked" times): a private time of a chosen class $v$ that **no still-allowed class covers** remains private to $v$ in every completion (allowed sets only shrink below a node). Since $\mathrm{priv}(1)$ only shrinks, the node is cut if $\lvert\mathrm{locked}(v)\rvert > \mathrm{priv}(1)$ for some $v$.
  - Forbidding: an allowed class $c$ with $\mathrm{priv}(1) - \lvert P_1 \cap \mathrm{cov}(c)\rvert < \max_v \lvert\mathrm{locked}(v)\rvert$ is removed from the allowed set. Here $P_1$ is class 1's current private set. Adding $c$ would leave class 1 below some class's locked count forever, and forbidding classes only enlarges locked sets. The gain bound is then re-applied.
- These rules only remove search nodes with no admissible leaf below them, and leaves that are not the normalised representative. The orbit set is unchanged.

**Validation** (`test_lonely.py`, `test_covergen_pruning_preserves_orbits`). For $(k,p) = (5,41), (7,61), (8,101), (9,137), (14,89)$, levels 0, 1 and 2 give identical orbit sets, and at $(14,89)$ that set has the certificate's 687,016 orbits. At $(14,113)$ only the node counts were measured: the orbit-set comparison (expanding 43.8M unpruned covers) did not finish within its time limit, so it is not claimed.

**Measured speed-up** (single core):

| $(k, p)$ | nodes, levels 0 / 1 / 2 | minimal covers output | time |
| --- | --- | --- | --- |
| $(14, 89)$ | 8.49M / 4.74M / 4.73M | 1.69M / 0.98M / 0.26M | 3.3 / 1.9 / 1.8 s |
| $(14, 113)$ | 268M / 240M / 235M | 43.8M / 43.1M / 6.6M | 88 / 87 / 70 s |

- The node savings shrink as $p$ grows. $q_k$ is only 2 at $p = 239$. The locked-time rule also rarely fires, because nearly every time stays reachable until deep in the tree.
- The large gain is in output: 5–$7\times$ fewer covers to expand and canonicalise.
- **Failed route (kept):** these rules do **not** reproduce Allikvere's roughly $14\times$ smaller tree (Approach 4). His engine also uses a two-branch search (irredundant $k$-class covers and extensions of smaller covers) with irredundance-aware bounds, which we have not implemented.

### 9. Sharper bounds in the minimal-cover search (step 7)

Goal: a faster level-one generator, as the precondition for completeness at more gates. `covergen.c` with `LRC_IRR` (a bitmask; the output is unchanged by construction):

- **Bit 2, sharper gain bound.** At a node with $r = k - \lvert L\rvert$ classes still to choose, the $r$ largest gains $\lvert\mathrm{cov}(c) \cap U\rvert$ over allowed classes $c$ must sum to at least $\lvert U\rvert$. The plain bound uses $r\cdot$ max gain. Any completion adds at most $r$ classes, and each covers at most its gain of the uncovered times, so the cut removes only nodes with no cover below.
- **Bit 1, redundancy cuts.**
  - If a chosen class has no private time relative to the other chosen classes, the node is cut: private sets only shrink as classes are added, so no minimal cover lies below.
  - An allowed class $c$ that covers all private times $P_v$ of some chosen class $v$ is forbidden in the subtree, because $v$ would be redundant in any cover containing $c$.
  - By the symmetry of $d_p(av)$ in $a$ and $v$, the coverers of a time $a$ are exactly $\mathrm{cov}(a)$. So these classes are found as the intersection of $\mathrm{cov}(a)$ over $a \in P_v$.
- **Validation** (`test_covergen_irr_same_minimal_covers`). For $(k, p) = (5,41), (7,61), (8,101), (9,137), (10,127), (14,89)$, `LRC_IRR` = 1, 2 and 3 print **exactly the same set of minimal covers** as the plain search, also under 3-way sharding. Combined with `LRC_PRUNE=2`, the $(14, 89)$ orbit set is unchanged: 687,016 orbits (`test_covergen_pruning_preserves_orbits`).
- **Measured** (`results/knuth_irr_k14.txt`; Knuth estimates are heuristic):
  - Ablation at $p = 251$: the sharper gain bound gives nearly all of the node saving ($8.70\cdot 10^{10} \to 4.55\cdot 10^{10}$) at about 90% of the node rate.
  - The redundancy cuts remove few extra nodes and more than halve the node rate, so `LRC_IRR=2` is the recommended setting.
  - A greedy packing bound (times with disjoint coverer sets) gave nothing and was dropped (failed route, kept).
  - Exact count at $(14, 113)$: 268M plain vs 111M nodes with both bits, giving the same 43,763,271 minimal covers.
  - With `LRC_IRR=2`, the tree has $1.90\times$ fewer nodes at $p = 251$ and $1.83\times$ fewer at $p = 257$, for a net speed-up of about $1.7\times$.
  - So completeness at $p = 257$ would still take about 12 core-hours (at least about 4 h of wall time on 3 cores). It was not run.
- **Still short of Allikvere's tree** (about $14\times$ smaller than our plain search, Approach 4). The remaining gap is not explained by the bounds tried here.

### 10. Shape lemma $R_{15} < 49/100$ (step 9)

**Claim.** On the positive simplex in $\mathbb{R}^{15}$, $R_{15} < 49/100$. Here $R_n$ is the shape factor of Allikvere's flag bound (arXiv:2609.02604v2, eq. (F)):

- $F_n(x)^2 = \prod q_i \cdot \sum x_i^2/q_i$ and $R_n(x) = n (\prod x_i)^{1/n} / F_n(x)$;
- $q_i = 1 + 2u_i - u_i^2$, with $u_i = x_i / \max_j x_j$.

**Status: proved here.** The argument is the paper's proof of Lemma 3.7 carried over to $n = 15$, written out below. Every identity and numeric inequality in it is checked in exact rational arithmetic by `computations/lonely-runner/shape_lemma.py` (tests: `test_shape_lemma.py`). The same script, run with $n = 13$ and $n = 14$, reproduces the paper's polynomials, cubics, intervals and the bounds $R_{13} < 101/200$ and $R_{14} < 1/2$ (regression tests). So Lemma 3.7 itself is now re-checked as well.

The (unreviewed) munim lonely-runner-16 repository states the same bound. We did not use its text; our derivation agrees with it.

**Notation.** For $u \in (0,1]$ put:

- $q(u) = 1 + 2u - u^2$;
- $a(u) = q(u)/u^{2/15}$;
- $w(u) = u^2/q(u)$;
- $H(u) = (\sum_i w(u_i)) \cdot \prod_i a(u_i)$;
- $D(u) = 14u^2 - 13u + 1$.

The common scale cancels, so $R_{15}(x)^2 = 225/H(u)$. Hence $R_{15} < 49/100 \iff H(u) > T := (1500/49)^2 = 937.1095\ldots$ on the domain $\Omega = \{u \in (0,1]^{15} : \max_i u_i = 1\}$.

The smaller root of $D$ is $\alpha = (13 - \sqrt{113})/28$. Since $D(0.0846) > 0 > D(0.0847)$ and $D$ decreases on $[0, 13/28]$, $\alpha \in (0.0846, 0.0847)$.

**Step 0: $H$ attains its minimum on $\Omega$.**

- $\sum w \ge w(1) = 1/2$, and $a > 8/5$ (Step 2). So $H \ge \tfrac{1}{2} (8/5)^{14} a(u_i)$ for every $i$.
- Also $a(u) \ge u^{-2/15}$ because $q \ge 1$.
- So on $\{H \le M\}$ every $u_i \ge \delta(M) > 0$. This sublevel set is a closed subset of $[\delta,1]^{15}$, hence compact, and the continuous $H$ attains its minimum on it.

**Step 1: all coordinates below 1 share one value.**

Fix a minimizer and a coordinate $u = u_i < 1$. Some other coordinate equals 1, so $u$ can vary in $(0,1)$ inside $\Omega$. Put $C = \sum_{j\ne i} w(u_j)$.

- Bounds on $C$: $w > 0$ on $(0,1]$, so $C > 0$. Also $\tfrac{1}{2} - w = (1 + 3u)(1 - u)/(2q) \ge 0$, so $w \le \tfrac{1}{2}$ and $C \le 7$.
- Up to a positive factor, $H$ is $\varphi(u) = a(u)(C + w(u)) = u^{-2/15}(Cq + u^2)$.
- The derivative satisfies $(15/2) u^{1+2/15} \varphi'(u) = -\beta(u)$, with $\beta(u) = C\cdot D(u) - 14u^2$. This holds because $(15/2)u(Cq' + 2u) - (Cq + u^2) = -C\cdot D + 14u^2$, a polynomial identity in $u$ for each $C$.

Shape of $\beta$: $\beta(0) = C > 0$ and $\beta(\alpha) = -14\alpha^2 < 0$.

- If $C \le 1$: $\beta$ is concave (leading coefficient $14(C - 1) \le 0$; linear if $C = 1$) with $\beta(0) > 0$. So it has exactly one positive root, and $\beta < 0$ beyond it.
- If $C > 1$: $\beta$ is convex and $\beta(1) = 2C - 14 \le 0$, so its second root is $\ge 1$.

In both cases $\beta$ has exactly one root $u_0$ in $(0,1)$, with $u_0 < \alpha$. Then $\varphi$ decreases on $(0,u_0)$ and increases on $(u_0,1)$, so the minimizer has $u = u_0 \in (0, \alpha)$.

Putting all these coordinates on one scale:

- On $(0, \alpha)$, $D > 0$, so $\beta(u) = 0 \iff C = 14u^2/D$.
- Since $14q + D = 15(1 + u)$, this gives $A := C + w(u) = \sum_k w(u_k) = 15u^2(1 + u)/(D q)$.
- So every coordinate below 1 satisfies $L(u) := q D/(15 u^2(1 + u)) = 1/A$, with the same $A$ for all of them.
- $L'(u) = -2P(u)/(15u^3(1 + u)^2)$, where $P(u) = 7u^5 + 14u^4 - 27u^3 - 11u^2 - 4u + 1$.
- On $(0, \alpha) \subset (0, 0.0847)$: $P(u) > 1 - 4(0.0847) - 11(0.0847)^2 - 27(0.0847)^3 = 0.5658\ldots > 0$.

So $L$ is strictly decreasing on $(0, \alpha)$, and all coordinates below 1 are equal, to some $t \in (0, \alpha)$.

**Step 2: $a(u) > 8/5$ on $(0,1]$.**

- $a'/a = (15u q' - 2q)/(15u q)$, and $15u q' - 2q = -2D(u)$.
- So $a$ decreases on $(0, \alpha)$, increases between the roots of $D$, and decreases on the rest of $(0,1]$. $D(1) = 2 > 0$, so both roots lie below 1.
- Hence $\min a = \min(a(\alpha), a(1) = 2)$.
- $a(\alpha) > q(0.0846)/0.0847^{2/15}$, because $q$ increases and $u^{-2/15}$ decreases. This is $> 8/5 \iff q(0.0846)^{15} > (8/5)^{15} \cdot 0.0847^2$, an exact rational inequality that holds ($a(\alpha) \approx 1.6152$).

**Step 3: two or more coordinates equal to 1.** If $k \ge 2$ coordinates equal 1:

- $\sum w \ge k/2$ and $\prod a \ge 2^k (8/5)^{15-k}$.
- The bound $(k/2)\, 2^k (8/5)^{15-k}$ increases with $k$ (ratio $(k+1)/k \cdot 5/4 > 1$).
- So $H \ge 4 (8/5)^{13} = 1801.4\ldots > T$.

**Step 4: exactly one coordinate equal to 1.** By Step 1 the other fourteen equal some $t \in (0, \alpha)$, and

$$H_1(t) = \left(\tfrac{1}{2} + \frac{14t^2}{q}\right) \cdot 2 \cdot \left(\frac{q}{t^{2/15}}\right)^{14} = \frac{(1 + 2t + 27t^2)\, q(t)^{13}}{t^{28/15}},$$

using $q + 28t^2 = 1 + 2t + 27t^2$.

- Its log-derivative times $15t(1 + 2t + 27t^2)q(t)$ equals $28(1 - t)\cdot K(t)$, with $K(t) = 378t^3 + 25t^2 + 10t - 1$ (polynomial identity).
- On $(0,1)$ the factor $15t(1 + 2t + 27t^2)q(t)$ is positive, so the sign of the log-derivative is the sign of $K$.
- $K$ is increasing on $t > 0$, with $K(0.07247) < 0 < K(0.07248)$. So $H_1$ decreases up to the root $t_0 \in (0.07247, 0.07248)$ and increases after it, and $H_1 \ge H_1(t_0)$ on $(0,1)$.
- Bound at $t_0$: $1 + 2t + 27t^2$ and $q$ increase, and $t^{-28/15}$ decreases. So $H_1(t_0) \ge (1 + 2\cdot 0.07247 + 27\cdot 0.07247^2)\, q(0.07247)^{13} / 0.07248^{28/15} = 944.71\ldots$
- This exceeds $T \iff (1 + 2\cdot 0.07247 + 27\cdot 0.07247^2)^{15}\, q(0.07247)^{195} > T^{15} \cdot 0.07248^{28}$, an exact rational inequality that holds. ($H_1(t_0)$ itself is $\approx 944.96$.)

$\Omega$ has at least one coordinate equal to 1, so Steps 3 and 4 cover every case. Therefore $H > T$ on $\Omega$, and $R_{15} < 49/100$. ∎

**Margins and negative controls (tests):**

- The proof has about 0.8% of room in Step 4 (944.7 against 937.1).
- A target above the true minimum ($T = 946$, or $r_{15} = 0.487$) correctly fails the Step 4 check.
- A float coordinate-descent search over $\Omega$ never goes below $T$, and finds the minimum $\approx 944.96$ on the one-variable family. This search is a sanity check only, not part of the proof.

**Consequence.** Allikvere's Theorem 3.8 is stated and proved for general $n$. For $n = 15$ its ratio hypothesis holds: $\min c_{i+1}/c_i = 3751/2349 > 4/3$, exact (`flag_bound.py`). Its other hypothesis is $\mathrm{LRC}(m)$ for all $m < 15$, i.e. up to 15 runners, which is Allikvere's certificate-based result re-checked in Approach 7.

With $r_{15} = 49/100$ the theorem gives, for a primitive counterexample with 15 speeds, $\ln(v_1\cdots v_{15}) < 15 \ln(A_{15} \cdot (49/100)/15) = 496.727$. With the forced divisor $\operatorname{lcm}(2,\ldots,16) = 720720$, the prime-gate target is 483.239.

At step 9 the general-$n$ parts of Theorem 3.8 were only read, so the target was then labelled conditional on the cited theorem. They are verified in Approach 11 (step 10), which removes that condition.

### 11. Independent check of the general-n flag bound, Theorem 3.8 (step 10)

**Goal.** Verify the general-$n$ parts of Allikvere's Theorem 3.8 (arXiv:2609.02604v2, §3, read from the v2 TeX source), so that the 16-runner target 483.239 no longer rests on the cited theorem. These are Lemmas 3.1, 3.2, 3.3, 3.5 and 3.6, Proposition 3.4 and the assembly.

**Result.** Every step checks out, and no gap or error was found. Where a step has a finite or numeric component, it is machine-checked in exact rational arithmetic (`computations/lonely-runner/flag_theorem_check.py`, tests `test_flag_theorem.py`, 13 tests including negative controls). The purely logical steps (Lemma 3.3, Proposition 3.4, Lemma 3.5) were checked line by line by reading. They have no finite component to machine-check.

The only inputs not re-proved here are:

- **Standard facts:** the existence of Korkine–Zolotarev bases; the Minkowski–Weyl decomposition of a pointed polyhedron; Schur-concavity of $\sum \log$; Babai's nearest-plane rounding; elementary lattice duality.
- **Lower cases of the conjecture:** $\mathrm{LRC}(m)$ for $m \le 14$.

**Setting.** Here $n \ge 2$ and $v \in \mathbb{Z}^n_{>0}$ is primitive. "Counterexample" means every real $t$ has some $i$ with $\lVert t v_i\rVert < 1/(n+1)$. We use the following objects:

- $S = \sum v_i$, $x = v/S$, $u = v/\max v$, and $q_i = 1 + 2u_i - u_i^2 \in (1,2]$;
- $H = v^\perp$ and $P$, the orthogonal projection onto $H$;
- $\Lambda = P \mathbb{Z}^n$, of rank $d = n - 1$;
- $D = P[-1,1]^n$ and $E = P Q^{1/2} B_2^n$;
- $\lVert\cdot\rVert_E$, the norm on $H$ whose unit ball is $E$.

**Lattice facts (used in Lemma 3.2).**

- **Covolume of $\mathbb{Z}^n \cap H$ is $\lVert v\rVert$.** The layers $\{z \in \mathbb{Z}^n : \langle v,z\rangle = k\}$ of $\mathbb{Z}^n$ parallel to $H$ are at spacing $1/\lVert v\rVert$ ($\langle v, \mathbb{Z}^n\rangle = \gcd(v)\, \mathbb{Z} = \mathbb{Z}$), and $\det \mathbb{Z}^n = 1$.
- **$\Lambda$ is the dual of $\mathbb{Z}^n \cap H$.** Extend a basis $y_1, \ldots, y_{n-1}$ of the primitive sublattice $\mathbb{Z}^n \cap H$ to a basis of $\mathbb{Z}^n$, and take its dual basis $y_k^*$ (in $\mathbb{Z}^n$). Then the $P y_i^*$ ($i < n$) are the dual basis of $\mathbb{Z}^n \cap H$ inside $H$, and $P y_n^* = 0$.
- **Hence $\det \Lambda = 1/\lVert v\rVert$.** This is machine-checked exactly: an exact Hermite-form basis of $P \mathbb{Z}^n$, at random primitive $v$ for $n = 3$–$6$ (`check_covolume`).

**Lemma 3.1 (Inclusion, $E \subseteq D$): verified.** Both bodies are convex and closed in $H$, so $E \subseteq D$ iff $h_E \le h_D$ on $H$.

- **Support functions.** For $y \in H$, $h_D(y) = \sup_{x\in[-1,1]^n} \langle Py, x\rangle = \sum \lvert y_i\rvert$, and $h_E(y) = \sup_{\lvert b\rvert\le 1} \langle Q^{1/2}y, b\rangle = (\sum q_i y_i^2)^{1/2}$.
- **Reduction to vertices.** By homogeneity it suffices that $\sum q_i y_i^2 \le 1$ on the polytope $\{y \in H : \sum\lvert y_i\rvert \le 1\}$. The left side is convex, so it suffices at the vertices.
- **The vertices.** The vertices of a hyperplane section of a polytope are its intersections with edges, together with any polytope vertices lying in the hyperplane. No $\pm e_i$ lies in $H$ ($v_i \ne 0$). Edges between same-sign vertices miss $H$ ($v > 0$). The segment from $e_i$ to $-e_j$ meets $H$ at $y = (v_j e_i - v_i e_j)/(v_i + v_j)$.
- **The check at a vertex.** There $\sum q y^2 \le 1 \iff (q_i - 1)v_j^2 + (q_j - 1)v_i^2 \le 2 v_i v_j$. With $q - 1 = u(2 - u)$ and $v = M u$, the difference of the two sides equals $-2M^2 u_i u_j (1 - u_i)(1 - u_j) \le 0$.

Machine checks:

- the identity, exactly, at 200 random rational points;
- every vertex point, exactly, for random $v$ with $n = 3$–$7$;
- $h_E(y)^2 \le h_D(y)^2$ at random rational $y \in H$, a sample check of the conclusion;
- negative control: with $q$ replaced by $1 + 2u$, the inclusion fails, as it must.

**Lemma 3.2 (Covolume, $\mathrm{covol}_E(\Lambda) = 1/(S F_n(x))$): verified.**

- **The $E$ norm.** By definition, $\lVert y\rVert_E = \min\{\lvert z\rvert : P Q^{1/2} z = y\}$. Writing $Q^{1/2} z = y + \lambda v$ and minimizing over $\lambda$ gives $\lVert y\rVert_E^2 = y^{\top} M y$, with $M = Q^{-1} - Q^{-1}v v^{\top}Q^{-1}/(v^{\top}Q^{-1}v)$.
- **The paper's computation.** It uses the Gram matrix $(U^{\top}QU)^{-1}$ and the Schur-complement identity $\det(U^{\top}QU) = \det Q \cdot \tilde v^{\top}Q^{-1}\tilde v$. It agrees with this formula, and it gives $\mathrm{covol}_E^2 = \det \Lambda^2 / \det(U^{\top}QU) = 1/(\prod q_i \cdot \sum v_i^2/q_i) = 1/(S^2 F_n(x)^2)$.
- **Machine check.** At 20 random primitive $v$ ($n = 3$–$6$), the Gram determinant of an exact $\mathbb{Z}$-basis of $\Lambda$ in the form $M$ equals $1/(S^2 F_n^2)$ exactly. It is computed directly from the definition of $E$, independently of the paper's $U$-coordinates. Negative control: a wrong $F$ fails.

**Lemma 3.3 (Separated points on rational subspaces; Giri–Kravitz Lemma 3.3): verified by reading.**

*Statement.* Let $1 \le q \le n$ and assume $\mathrm{LRC}(m)$ for $m \le n+1-q$. Then every rational $q$-dimensional $V \subseteq \mathbb{R}^n$ with no identically vanishing coordinate contains $s$ with $\lVert s_i\rVert \ge 1/(n+2-q)$ for all $i$.

*Base case, $q = 1$.* $V = \mathbb{R} a$ with $a$ primitive and all $a_i \ne 0$. The $\lvert a_i\rvert$ take $m \le n$ distinct values, so $\mathrm{LRC}(m)$ gives $t$ with $\lVert t a_i\rVert \ge 1/(m+1) \ge 1/(n+1)$.

*Induction step, $q \ge 2$.* The restrictions $a_k$ of the coordinate functionals to $V$ are nonzero and span $V^*$, so not all are proportional.

- Take a non-proportional pair $(i, j)$ minimizing the angle between their lines, and fix the sign so that $\langle a_i, a_j\rangle \ge 0$.
- $h = a_i + a_j$ lies strictly inside that angle. So, by minimality, no $a_k$ is proportional to $h$: such an $a_k$ would form a pair with $a_i$ at a smaller angle.
- $V' = V \cap \{y_i + y_j = 0\}$ is rational of dimension $q - 1$. $a_k$ vanishes on $V'$ iff $a_k \in \mathbb{R} h$, so no coordinate vanishes on $V'$.
- Deleting coordinate $j$ is injective on $V'$ ($y_j = -y_i$). The image $V''$ is rational and has no vanishing coordinate.
- Induction applies in $\mathbb{R}^{n-1}$ with $q - 1$. It needs $\mathrm{LRC}(m)$ for $m \le n+1-q$, the same range, and gives distance $1/((n-1)+2-(q-1)) = 1/(n+2-q)$.

Each step was checked, including the edge cases: the sign flip leaves $\lVert\cdot\rVert$ unchanged, and the pair minimizing the angle exists because there are finitely many pairs.

**Proposition 3.4 (Prefix inequalities, $t_1 + \cdots + t_r > B_r = \bigl(2r/((n+1)(n+1-r))\bigr)^2$): verified by reading.** Take any basis $b_1, \ldots, b_d$ of $\Lambda$, its $E$-Gram–Schmidt vectors $b_i^*$, and $t_i = \lVert b_i^*\rVert_E^2$. Choose $z_i \in \mathbb{Z}^n$ with $P z_i = b_i$, and let $V = \mathrm{span}(v, z_1, \ldots, z_r)$.

1. **$V$ is admissible for Lemma 3.3.** It has dimension $r + 1$ (apply $P$ to a linear relation) and is rational. No coordinate vanishes on it ($v > 0$).
2. **A separated point.** Lemma 3.3 with $q = r + 1$ needs $\mathrm{LRC}(m)$ for $m \le n - r \le n - 1$. It gives $s = a v + \sum a_i z_i$ with $\lVert s_k\rVert \ge 1/(n+1-r)$.
3. **Rounding.** Nearest-plane rounding gives integers $k_i$ with $e = \sum(a_i - k_i) b_i = \sum \theta_i b_i^*$, $\lvert\theta_i\rvert \le \tfrac{1}{2}$. So $\varepsilon = \lVert e\rVert_E \le \tfrac{1}{2} (t_1 + \cdots + t_r)^{1/2}$.
4. **From $E$ to $D$.** By Lemma 3.1, $e \in \varepsilon E \subseteq \varepsilon D$, so $e = P y$ with $\lvert y_k\rvert \le \varepsilon$.
5. **A time $t$.** $\sum(a_i - k_i) z_i - y$ lies in $\ker P = \mathbb{R} v$. Hence $s - \sum k_i z_i - y = t v$ for some $t$, and $\lVert t v_k\rVert \ge \lVert s_k\rVert - \lvert y_k\rvert \ge 1/(n+1-r) - \varepsilon$.
6. **Conclusion.** If $\varepsilon \le 1/(n+1-r) - 1/(n+1) = r/((n+1)(n+1-r))$, then $t$ is a witness, which is impossible. So $4\varepsilon^2 > B_r$, and $t_1 + \cdots + t_r \ge 4\varepsilon^2 > B_r$.

Every step was checked, including the strict inequality and the LRC range.

**Lemma 3.5 (KZ, $t_{i+1} \ge \tfrac{3}{4} t_i$): verified by reading (standard).**

- In a KZ basis, $b_i^*$ is a shortest nonzero vector of the projected lattice $\pi_i(\Lambda)$.
- $\pi_i(b_{i+1}) = b_{i+1}^* + \mu b_i^*$ with $\lvert\mu\rvert \le \tfrac{1}{2}$ is nonzero in $\pi_i(\Lambda)$.
- So $t_i \le t_{i+1} + t_i/4$. KZ bases exist for every lattice (Korkine–Zolotarev 1873; Lagarias–Lenstra–Schnorr 1990), in any Euclidean norm.

**Lemma 3.6 (Product minimization, $\prod t_i \ge \prod c_i = K_n$ under $c_{i+1}/c_i > 4/3$): verified.**

1. **Change of variables.** Put $z_i = t_i/\rho^{i-1}$. The constraints become $z_1 \le \cdots \le z_d$ and $\sum_{i\le r} w_i z_i \ge B_r$. They define a polyhedron $\Pi$ in the open positive orthant ($z_1 \ge B_1 > 0$).
2. **Reduction to vertices.** $\Pi$'s recession cone is $\{0 \le z_1 \le \cdots \le z_d\}$: the $r = 1$ constraint forces $dz_1 \ge 0$. So $\Pi$ is pointed and is the convex hull of its vertices plus that cone. $f = \sum \log(w_i z_i)$ is concave and nondecreasing, so $f \ge$ its minimum over the vertices.
3. **Structure of a vertex.** At a vertex, the $\beta$ maximal blocks of equal $z$ use $d - \beta$ monotonicity constraints, so at least $\beta$ prefix constraints are active.
   - None is active strictly inside a block $(a, b]$. Activity at $r$ with feasibility at $a$ gives $\zeta \le$ (weighted mean of $c_i/w_i$ over $a < i \le r$) $\le c_r/w_r$. Here $c_i > 0$ by induction, and $c_i/w_i$ strictly increases because $(c_{i+1}/c_i)/\rho > 1/\rho^2 > 1$. Activity at $r$ with feasibility at $r + 1$ gives $\zeta \ge c_{r+1}/w_{r+1} > c_r/w_r$. These contradict each other.
   - So all $\beta$ block ends are active, and on each block $t$ is geometric with ratio $\rho$ and the same sum as $c$ over the block.
4. **Comparison within a block.** Ratio comparison shows that $c^{\downarrow}$ majorizes the geometric $g$ (both decreasing, with equal totals). Schur-concavity of $\sum \log$ then gives $\prod_{\text{block}} c \le \prod_{\text{block}} t$.
5. **The minimum is attained.** $t = c$ is feasible.

Machine checks, exact, with the actual $B_r$ of each $n$:

- **(a) Brute-force vertex enumeration, $d \le 7$.** All $d$-subsets of the $2d - 1$ constraints are solved and filtered for feasibility. There are exactly $2^{d-1}$ vertices, each the block point of a composition of $d$, as the lemma's structure claim says, and each has $\prod t \ge K_n$.
- **(b) Block points, $n = 13, 14, 15$.** All $2^{d-1}$ block points (8,192 at $n = 15$) are feasible and have $\prod t \ge K_n$, with equality only at $t = c$. $K_{14}$ equals the paper's value.
- **(c) Random feasible points (float).** All have $\prod t \ge K_n$.
- **Negative control.** For prefix constants with $c_{i+1}/c_i < 4/3$, a single geometric block is feasible and has a smaller product, so the hypothesis is needed.

**Assembly (Theorem 3.8): verified.** Take a KZ basis in the $E$ norm.

- Proposition 3.4 and Lemma 3.5 give the hypotheses of Lemma 3.6, so $\mathrm{covol}_E(\Lambda)^2 = \prod t_i \ge K_n$.
- Lemma 3.2 then gives $S F_n(x) \le A_n = K_n^{-1/2}$.
- With $R_n < r_n$: $n (\prod v_i)^{1/n} = n S (\prod x_i)^{1/n} = S F_n R_n < r_n A_n$.
- For $n = 15$, the ratio minimum is $3751/2349 > 4/3$ (exact) and $r_{15} = 49/100$ (Approach 10). Hence $\ln(v_1\cdots v_{15}) < 496.72677196$, and the prime-gate target after $\ln 720720$ is 483.23876597. Both are computed to 40 digits; $n = 14$ reproduces the paper's 414.77936455669981.

**Consequence.** For a primitive counterexample with 15 speeds (16 runners), assuming $\mathrm{LRC}(m)$ for $m \le 14$: $v_1\cdots v_{15} < e^{496.7268}$. The 16-runner gate target 483.239 is therefore **proved here**, modulo:

- **$\mathrm{LRC}(13)$ and $\mathrm{LRC}(14)$**, the 14- and 15-runner cases. These are Allikvere's certificate-based results: $\mathrm{LRC}(14)$ is re-checked in Approach 7, fully at 54 of 71 gates, with level-one completeness at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$); $\mathrm{LRC}(13)$ is re-checked only through its terminal kills. $\mathrm{LRC}(m)$ for $m \le 12$ comes from the literature.
- **The standard facts listed above.**
- **The forced divisor** (Rosenfeld Lemma 4), which is elementary (see "The finite reduction").

It no longer depends on citing Theorem 3.8.

### 12. Two-branch level-one search (step 11): implemented, validated, no node reduction (failed route, kept)

**Goal.** Allikvere's level-one engine (arXiv:2609.02604v2 §4.1, "A complete two-branch covering search") splits the improper $k$-multisets into two kinds and searches them separately:

1. irredundant covers on exactly $k$ distinct classes, satisfying the $q_k$ private-time bound;
2. covers on at most $k - 1$ classes, normalized to contain class 1 once and satisfying $q_{k-1}$, followed by all one-class extensions.

The aim was to test whether this split explains his much smaller tree (Approaches 4, 8 and 9).

**Implementation** (`covergen.c`, environment `LRC_TWOBRANCH=1`). The minimal covers $C \ni 1$ with $\lvert C\rvert \le k$ are searched in two trees.

- **Branch 1, $\lvert C\rvert = k$.** Depth limit $k$, and leaves with $\lvert L\rvert < k$ are not printed. A new cut $\lvert U\rvert \ge k - \lvert L\rvert$ applies: each class of $C$ not yet chosen has a private time, which lies in $U$ and is distinct from the others' private times.
- **Branch 2, $\lvert C\rvert \le k - 1$.** The depth limit, the gain bound and (with `LRC_PRUNE`) the private-time node cut all use $k - 1$, so the node cut is $q_{k-1} \ge q_k$.

Every cut removes only nodes with no admissible leaf below them, so the union of the two outputs is the single-tree output. The Knuth probe now applies the $q$-cut when `LRC_PRUNE` is set, and the same cuts in each branch, so the estimates compare like with like.

**Validation.** The sorted minimal-cover output is identical to the single tree in 36 configurations:

- $(k, p) = (5,41), (7,61), (8,101), (9,137), (10,127), (14,89)$;
- `LRC_PRUNE` = 0/1/2 and `LRC_IRR` = 0/2.

`test_lonely.py`, `test_covergen_twobranch_same_minimal_covers`, keeps 15 of these.

**Measured** (`results/knuth_twobranch_k14.txt`):

| $(k, p)$, cuts | single tree | branch 1 + branch 2 | change |
| --- | --- | --- | --- |
| $(14, 89)$, PRUNE=2 IRR=2, exact | 4,629,123 | 4,544,404 + 732,536 | +14% |
| $(14, 113)$, PRUNE=2 IRR=2, exact | 229,333,830 (64.5 s) | 227,304,940 + 18,585,560 (67.8 s) | +7% |
| $(14, 251)$, PRUNE=1 IRR=2, Knuth | $4.71\cdot 10^{10}$ | $4.71\cdot 10^{10} + 1.60\cdot 10^{9}$ | +3.4% |
| $(14, 401)$, PRUNE=1 IRR=2, Knuth | $7.36\cdot 10^{11}$ | $7.36\cdot 10^{11} + 1.45\cdot 10^{10}$ | +2.0% |

**Conclusion.** Branch 1 is the single tree to within 1%: the exactly-$k$ cut almost never fires. Branch 2 is pure overhead. So in our engine the two-branch split gives **no node reduction**, and it is **not** the source of Allikvere's advantage. The mode is kept for reference; it is not recommended.

**What his records do show** (`gates.json` in the Zenodo manuscript source; his node counts may be defined differently from ours):

- **At $p = 89$**, his irredundant branch used 517,527 nodes and output 110,720 rows. Our branch 1 used 4,544,404 nodes ($8.8\times$ more) and output 238,039 covers ($2.15\times$ more).
- **Rows per gate.** At $p = 401$ his irredundant branch output only 394 rows from $1.6\cdot 10^{11}$ nodes. A separate exhaustive "precondition" search ($1.07\cdot 10^{8}$ nodes) certified that no cover uses at most 12 classes there.
- **Where the gap probably lies.** His normalization in the irredundant branch is stronger than our max-private one ("taking a lexicographic minimum … removes duplicates"), and it may also prune. His decomposition into 513 jobs may matter too.
- **CPU time.** He took 2,475 s at $p = 251$, against about 30,240 s for our `LRC_PRUNE=2` run, or about 18,000 s with `LRC_IRR=2`. That is a gap of about $7\times$.

These leads are not explored further here (Next steps 2).

### 13. Closing the generator gap: child ordering and incremental redundancy cut (step 12)

**Source of the ideas.** Allikvere's generator source (`basegen_v66_lf.cpp`) and `CODE_GUIDE.md` are in the $\mathrm{LRC}(13)$ Zenodo record (10.5281/zenodo.22066772). They were **read as text; the program was not compiled or run.**

The v2 paper's §4.1 ("lexicographic minimum among the normalizations") turned out to be an **output** filter: one row per unit orbit, which is why he has $2.15\times$ fewer rows. It cannot shrink the tree. The $\tau$ precondition only affects the small second branch. The node savings come instead from search rules listed in his change log (v6.3–v6.6). Two were reimplemented here from that description, in our own code:

1. **`LRC_ORDER=1`: child order and child-gain cutoff.**
   - The children of the chosen time (allowed classes covering it) are tried in order of descending gain $\lvert\mathrm{cov}(c) \cap U\rvert$, ties by ascending class, instead of ascending class. Exclusion of earlier siblings is unchanged, and the header's completeness and uniqueness argument works for any fixed child order, so the printed set is unchanged.
   - Excluding high-gain classes early makes the gain bound bite much sooner in later siblings.
   - Cutoff: a child $c$ is dead if $g_c + \mathrm{bsum} < \lvert U\rvert$, where bsum is the sum of the $(\mathrm{left} - 1)$ largest gains over the allowed classes (gains only shrink below the node). Later siblings have $g \le g_c$, so the loop stops.
   - The gains are computed once per node and feed the sharper gain bound, the cutoff and the order.
2. **`LRC_IRR` bit 4: incremental redundancy cut.** Per depth we keep the set of times covered at least twice and each chosen class's private set.
   - Adding a class removes the newly doubly-covered times from every earlier private set. If one becomes empty, no minimal cover lies below, so the child is skipped. Its class is still excluded for later siblings.
   - This is the same cut as bit 1 part (i), at $O(\lvert L\rvert)$ instead of $O(\lvert L\rvert^2)$ mask work, and applied before the child node is created.

**Validation.** The set of minimal covers, with classes sorted per line, is identical to the plain search on:

- $(5,41), (7,61), (8,101), (9,137), (10,127), (14,89)$;
- `LRC_PRUNE` 0/1/2, `LRC_IRR` 0/2/4/6, `LRC_ORDER` 0/1, also with `LRC_TWOBRANCH=1`.

The test is `test_lonely.py`, `test_covergen_order_same_minimal_covers`, which also covers 3-way sharding. Since the output sets are equal, the orbit sets are equal.

**Measured** (`results/knuth_order_k14.txt`; Knuth estimates are heuristic):

| $k = 14$ | before (PRUNE=2, IRR=2) | ORDER=1 | ORDER=1 + IRR bit 4 |
| --- | --- | --- | --- |
| $p = 89$, exact nodes | 4,629,123 | 2,661,496 | 2,084,920 |
| $p = 113$, exact nodes / time | 229.3M / 58.0 s | 108.5M / 34.2 s | **83.3M / 31.6 s** |
| $p = 251$, Knuth nodes (PRUNE=1) / nodes per s | $4.71\cdot 10^{10}$ / $3.9\cdot 10^{6}$ | **$1.34\cdot 10^{10}$ / $3.0\cdot 10^{6}$** | $1.34\cdot 10^{10}$ / $2.6\cdot 10^{6}$ |

**Results:**

- **Child ordering: worked.** It gives 1.7–$3.5\times$ fewer nodes and a $1.8\times$ ($p = 113$) to about $2.7\times$ ($p = 251$) net speed-up. At $k = 8$–$10$ the node saving is 2.4–$3.5\times$.
- **Bit 4: worked at small $p$ only.** It saves 22% of nodes at $p = 89$ and 23% at $p = 113$, but nothing at $p = 251$, where it only slows each node. Use `LRC_IRR=6` for small gates and `LRC_IRR=2` for large ones.
- **The two-branch split** (Approach 12) still adds about 7% on top.

**Remaining gap.** At step 12 the $k = 14$ level one at $p = 251$ was projected at about $1.34\cdot 10^{10} / 3.0\cdot 10^{6} \approx 4{,}500$ CPU-s (`LRC_PRUNE=1`, single process), which would be a gap of about $1.8\times$.

**Exact confirmation at $p = 251$ (step 13).** `LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, in 16 shards on 4 cores (`results/lrc14_gates/regen_251_order.json`):

- **Same output as step 6.** Exactly **3,876,360 covers**, which expand to 4,143,952 multisets and give **2,404,346 orbits**. That is equal to the certificate's orbit set, with none only on one side, as in step 6.
- **Nodes.** $1.3515\cdot 10^{10}$, against $8.93\cdot 10^{10}$ with `LRC_PRUNE=2` alone ($6.6\times$ fewer).
- **Time.** **7,505 CPU-s**, against about 30,500 at step 6 ($4.1\times$ faster), and 32 min 50 s wall time.
- **The real gap is $2.9\times$, not $1.8\times$.** Allikvere's two branches at $p = 251$ took 2,475 + 104 = 2,579 CPU-s, on another machine. The step-12 projection used `LRC_PRUNE=1` and an unloaded node rate. The real run used `LRC_PRUNE=2`, with its locked-time rule, and had 4 processes sharing 4 cores, giving $1.8\cdot 10^{6}$ nodes/s.
- **At $p = 401$** (Knuth, `LRC_PRUNE=1`): $1.845\cdot 10^{11}$ nodes, about $1.0\cdot 10^{5}$ CPU-s at that rate, against his 45,577. That is about $2.2\times$.

- At $p = 89$ our tree still has $4\times$ more nodes than his irredundant branch: 2.08M for both branches against 517k. His node counter may be defined differently.
- Not yet tried from his change log:
  - the exact finish of the last two slots (intersect the coverer sets over the uncovered times);
  - the mandatory-point gain bounds for the last 2–3 slots;
  - the shrinking top-$k$ gain multiset for the cutoff;
  - bit-parallel or AVX-512 popcount kernels.
- These are constant-factor or late-depth improvements.

### 14. More generator speed: exact finish, fixed width, job split, orderly-root rule (steps 15–16)

**Sources.** The first three changes come from the change log of Allikvere's generator (`basegen_v66_lf.cpp`; read as text, not run). The fourth is from Toner, "Seventeen lonely runners, assuming sixteen" (Zenodo 10.5281/zenodo.23552885, Appendix B, Lemma B.1; read as text; his code was not run). All four are reimplemented in our `covergen.c`.

1. **Exact two-slot finish (`LRC_FINISH=1`).** With two classes left, after the first child $c_1$ the possible last classes are exactly the allowed $c_2$ in $\bigcap_{t \in U \setminus \mathrm{cov}(c_1)} \mathrm{cov}(t)$. These are enumerated directly. The leaf filters subsume every cut that is skipped, so the output is unchanged.
2. **Compile-time width (`-DWFIX=n`).** The bitsets have exactly $n$ words instead of 32, so struct copies shrink and loops unroll. The output is unchanged.
3. **Depth-1 job split (`LRC_SHARD_DEPTH=2`).** Depth-2 subtrees are dealt out by a global counter. All shards walk depths 0–1 identically, so the union over shards is the unsharded output.
4. **Orderly-root rule (`LRC_ORDERLY=1`).**
   - *Definitions.* The root's branching time and its candidate list $R=(r_0,r_1,\dots)$, in the child order used, are fixed. For a cover $S \ni 1$ let $\rho(S)=\min\{i : r_i \in S\}$; the search finds $S$ in the subtree of $r_{\rho(S)}$. Call $S$ canonical if $(\rho(S),\mathrm{sorted}(S))$ is lexicographically least among the pairs for $s^{-1}S$ (folded), $s \in S$.
   - *Uniqueness.* Each unit orbit has exactly one canonical cover.
   - *The cut.* At a node in the subtree of $r_\rho$ with selection $T$, if some $s^{-1}T$ ($s \in T$) contains $r_i$ with $i<\rho$, then every completion $S$ has $\rho(s^{-1}S) \le i < \rho(S)$. So $S$ is not canonical and the node is cut. We checked this argument.
   - *Restriction.* The class-1 private-time quota is not unit-invariant, so the rule requires `LRC_PRUNE=0`.
   - *Expansion.* One cover per orbit suffices for the multiset expansion, because $u(C+E)=uC+uE$.
   - *Cost per node.* A precomputed $(h+1)^2$ table of $\mathrm{fold}(a\,b^{-1})$ makes the test a few lookups.

**Validation.**

- Items 1–3 print the same minimal covers as the plain search (`test_covergen_finish_wfix_sharddepth`).
- Item 4, at $(k,p)=(7,61),(8,101),(9,137),(10,127),(14,89)$: exactly one cover per unit orbit of the plain minimal covers (for example 1,689,912 → 121,569 at $(14,89)$), and the expanded multiset orbit sets equal the plain search's (`test_covergen_orderly_root`).

**Measured** (`results/speed_step15.txt`, `results/speed_step16_orderly.txt`; Knuth figures are heuristic):

| $(k,p)$ | previous best (`LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`) | new |
| --- | --- | --- |
| $(14,113)$, full run | 42–49 s (shared cores) | 19–21 s with `LRC_FINISH` + `WFIX` (≈2.3×) |
| $(14,251)$, a fixed $1/64$ slice | 275 s | 172 s with `LRC_FINISH` + `WFIX` (1.60×) |
| $(14,157)$, full run, light load | 344.6 s (with `LRC_FINISH` + `WFIX`) | **100.9 s with `LRC_ORDERLY`** (3.4×) |
| $(14,251)$, $(14,401)$, Knuth nodes | $1.43\times10^{10}$, $1.99\times10^{11}$ | $2.55\times10^{9}$, $2.92\times10^{10}$ with `LRC_ORDERLY` (5.6×, 6.8×) |
| $(17,307)$, $(17,401)$, $(17,503)$, Knuth nodes | $1.11\times10^{13}$, $6.72\times10^{13}$, $1.20\times10^{14}$ | $1.87\times10^{12}$, $9.97\times10^{12}$, $1.83\times10^{13}$ (5.9×, 6.7×, 6.5×) |

**Results:**

- The orderly rule is the largest single gain so far.
- At $(14,113)$ it is only 1.45× faster, because the canonicity test costs relatively more at small $p$.
- For $k=17$ the tree ratio $N_{17}/N_{15}$ (`results/knuth_k15_k17.txt`, before the orderly rule) is about 22–26 at $p=307$–$503$, 42–44 at $p=601$–$701$, and 96 at $p=797$.

**Exact check at a real gate (step 16).** The full orderly run at $p=251$ used `LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1`, built with `-DWFIX=2`, in 32 depth-2 shards (`results/lrc14_gates/regen_251_orderly.json`).

- **Output.** 2,253,938 covers, one per orbit. They expand to exactly the certificate's 2,405,962 rows and give **2,404,346 orbits, equal to the certificate**, with none only on one side.
- **Cost.** $2.51\times10^{9}$ nodes, **841 CPU-s**, 3.6 min wall time on 4 cores. Earlier settings took 7,505 CPU-s (step 13) and about 30,500 (step 6); Allikvere's engine took 2,579 CPU-s on another machine.
- **Dependencies.** This completeness check rests on the minimal-cover argument and Lemma B.1. It does not use Lemma 4.1.

**Not tried yet:**

- the mandatory-point bounds for the last 2–3 slots, measured marginal at step 12;
- AVX-512 popcount kernels;

### 15. Independent level-one completeness at Allikvere's 16-runner gates (step 17)

**Goal.** Allikvere's $\mathrm{LRC}(15)$ claim (*Sixteen lonely runners*, Zenodo 10.5281/zenodo.23304361) certifies $J(15,p)=\varnothing$ at 59 primes $269 \le p \le 659$. The certificates store the level-one rows, so the cascade can be replayed; all 59 have been (`notes/lonely-runner/cert15.md`). What no replay of the certificate checks is **completeness**: that the stored rows represent every unit orbit of $I(15,p,1)$. We check it by generating $I(15,p,1)$ ourselves and comparing orbit sets.

**Method.**

- **Archive.** `evidence15_<p>_s0.tgz` is downloaded from Zenodo and its SHA-256 compared with the record's `SHA256SUMS.txt` (the file has CRLF line endings, which are stripped). The archive is parsed only by our own code; none of his programs are run.
- **Ours.** `covergen.c` at $k=15$ with `LRC_PRUNE=0 LRC_ORDERLY=1 LRC_IRR=2 LRC_ORDER=1 LRC_FINISH=1` (orderly-root rule, Approach 14), built with `-DWFIX`, in 32 depth-2 shards on 4 cores. The covers are expanded to 15-multisets and reduced to unit-orbit canonical forms by `canon.c`.
- **Theirs.** `rows_ir/*.txt` plus `rows_km1/*.txt`, each $14$-class cover extended by every class, reduced the same way (`completeness_check.py`, which now accepts the `out15_<p>` layout).
- **Pass.** The two orbit sets are equal.
- **Dependencies.** Completeness rests on the minimal-cover argument in `covergen.c` and Toner's Lemma B.1 (proof checked, Approach 14).

**Results** (`results/lrc15_gates/completeness_<p>.json`):

| $p$ | orbits (ours = his) | only on one side | our covers → rows | his rows (ir + km1 ext) | nodes | our CPU-s | his generation CPU-s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 269 | **6,589,665 = 6,589,665** | 0 / 0 | 6,153,299 → 6,596,721 | 6,149,965 + 446,756 = 6,596,721 | $1.41\times10^{10}$ | 5,160 (22 min wall) | 26,741 |
| 281 | **3,823,848 = 3,823,848** | 0 / 0 | 3,653,814 → 3,825,618 | 3,652,578 + 173,040 = 3,825,618 | $2.20\times10^{10}$ | 9,883 (41 min wall) | 49,672 |
| 311 | **2,811,345 = 2,811,345** | 0 / 0 | 2,727,679 → 2,811,763 | 2,727,133 + 84,630 = 2,811,763 | $5.27\times10^{10}$ | 20,875 (resumed after 2 container restarts) | 133,383 |
| 313 | **884,238 = 884,238** | 0 / 0 | 867,851 → 884,281 | 867,745 + 16,536 = 884,281 | $4.24\times10^{10}$ | 17,563 (75 min wall) | 128,618 |
| 317 | **430,529 = 430,529** | 0 / 0 | 419,992 → 431,139 | 419,921 + 11,218 = 431,139 | $3.55\times10^{10}$ | 14,964 (64 min wall) | 90,460 |
| 331 | **1,133,553 = 1,133,553** | 0 / 0 | 1,108,193 → 1,133,613 | 1,108,038 + 25,575 = 1,133,613 | $6.77\times10^{10}$ | 27,876 (128 shards; see JSON) | 153,904 |
| 347 | **237,421 = 237,421** | 0 / 0 | 236,390 → 237,422 | 236,384 + 1,038 = 237,422 | $8.15\times10^{10}$ | 37,163 (3 range tasks + compare task) | 237,081 |
| 349 | **147,994 = 147,994** | 0 / 0 | 146,957 → 147,995 | 146,951 + 1,044 = 147,995 | $7.59\times10^{10}$ | 33,557 (142 min wall) | 218,661 |
| 367 | **108,134 = 108,134** | 0 / 0 | 105,593 → 108,141 | 105,579 + 2,562 = 108,141 | $9.36\times10^{10}$ | 45,911 (3 range tasks + compare task; 197 min wall) | 224,826 |

**Restarts.** The container was reclaimed twice during $p = 311$. The run resumed from its finished shards (`run_gate15.sh` skips shards listed in `times.txt`; unfinished shards rerun from scratch). Before each resume, every kept shard's cover file was checked to have exactly as many lines as `minimal_covers` in its log. The details are in the JSON. From $p = 347$ on, each gate runs as several harness-tracked tasks, one per shard range (`LO`/`HI`, generation only, each well under the 2 h task limit), plus a separate check-and-compare task. Since step 17's last fix, a shard counts as finished only if `covergen` exits 0, and the runner aborts before the comparison unless every shard's line count equals its `minimal_covers` (`run_gate15.sh`). That check was done by hand for $p = 349$, which started on the earlier script.

**Status.** At $p = 269, 281, 311, 313, 317, 331, 347, 349, 367$ the $\mathrm{LRC}(15)$ gates' level-one families are **independently verified complete**. From $p = 317$ on, the orbit sets are compared on disk (`LRC_COMPARE_FILES=1`: `sort -u` and `comm`; validated at $(14,89)$ against the in-memory mode, including a negative control). **Paused (2026-11-26).** The campaign was paused at 9 of 59 gates by the owner's decision, to focus on original work. The $p = 383$ run was stopped partway (31 of 128 shards generated); its partial data is not used and was not committed. The other 50 gates are unchecked for level-one completeness. `run_gate15.sh` can resume the campaign: it downloads and hash-checks each archive, runs shard ranges, and refuses to compare until every shard passes the line-count check. The remaining gates are ordered cheapest first by orderly Knuth estimates (`results/lrc15_gates/knuth_orderly_k15.txt`; heuristic): $p = 281$ about $2.1\times10^{10}$ nodes, up to $p = 641$ about $6.8\times10^{12}$.

## Independent re-check summary

Scope: J. Allikvere's computer-assisted proofs of $\mathrm{LRC}(13)$ and $\mathrm{LRC}(14)$, i.e. 14 and 15 runners (arXiv:2609.02604v2). Certificates: Zenodo 10.5281/zenodo.22066772 and 10.5281/zenodo.22667683. All checks use our own code (C and Python, in `computations/lonely-runner/`), written from the definitions in the paper and in arXiv:2604.23906. The archives were read as data only; none of the author's programs were executed.

**What an outside reader can rely on ($\mathrm{LRC}(14)$, 71 gate primes):**

- **Archive integrity: all 71 gates.** Each archive's SHA-256 equals the published `SHA256SUMS.txt` entry. 58 archives were kept; 13 were checked on download and then deleted.
- **Stored level-one rows: all 71 gates, every row.** Every stored irredundant row is witness-free at level 1, i.e. lies in $I(14,p,1)$. Every stored km1 multiset is a cover. That is 495,538,971 stored irredundant rows in total.
- **Binary cascade, levels 2–32.** In full at all 52 "$J(14,p) = \emptyset$" gates and at the near-gcd gates $p = 179$, 223 and 233 (step 8). At the other 16 near-gcd gates, on seeded uniform samples of stored rows (compared both ways) and of extension-survivor lines: 3,000 at $p = 89, 163, 173$; 500 at the 13 large archives. There were 0 mismatches.
- **Level-15 kill records.** In full at the 52 "J empty" gates (one persistent orbit, $(1,\ldots,14)$, each) and at $p = 179$ (all 8,011 orbits) and $p = 233$ (all 13,457 orbits). At the other near-gcd gates, on seeded samples of the same sizes. Every record checked is reproduced exactly: level-3/5 witness-free lifts, CRT candidates, level-15 grid, gcd clause, and the few-exception shift Lemma 3.12. Improper after Lemma 3.12 is 0 everywhere, and improper after the gcd clause is 0 at the "J empty" gates. At the stream-checked gates, the number of kill files equals the certificate's persistent-orbit count.
- **Level-one completeness at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$).** At $p = 89$ (near-gcd), $p = 239, 251, 263, 269, 281$ and 283 ("J empty"; 263, 269 and 283 in step 14, 281 in step 17), an independent minimal-cover enumeration reproduces exactly the certificate's set of level-one orbits: 687,016, 1,441,284, 2,404,346, 849,135, 197,957, 496,107 and 480,781 orbits. The run at 281 uses the orderly-root rule (Approach 14) instead of the private-time pruning. The runs at 89 and 239 are unpruned; the run at 251 uses our implementation of the private-time pruning (Approach 8).
- **Constants.** The flag-bound constants $K_{14}$, $A_{14}$, the log bound 414.779365 and the target 401.984506 were re-derived exactly. The 71 gates' $\sum \ln p = 408.8233$ exceeds the target, recomputed from the gate list.
- **$\mathrm{LRC}(13)$.** At all 111 gate primes, the terminal level-14 kill of both persistent orbits was recomputed and matches, and the kill files' SHA-256 match the gate manifests.
- **No discrepancy with any certificate was found.**

**What remains unverified here:**

- **Level-one completeness at the other 64 $\mathrm{LRC}(14)$ gates.** That every orbit of $I(14,p,1)$ is represented among the stored rows is checked only at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$). At all other gates it rests on Allikvere's generator and its completeness proposition (his Prop. 4.2 with the private-time Lemma 4.1). We implemented Lemma 4.1 (Approach 8) and have run it to completeness at $p = 251$, 263, 269 and 283 (step 14).
- **The sampled parts at the 19 near-gcd gates.** The unsampled cascade rows and kill records there were not re-computed.
- **The analytic inputs.** The finite-checking bound (Malikiosis–Santos–Schymura, via Rosenfeld's Cor. 3) was not re-proved. Allikvere's flag bound (Thm 3.8) is now independently verified: the shape Lemma 3.7 is re-checked for $n = 13$ and 14 and extended to $n = 15$ (Approach 10), and its general-$n$ Lemmas 3.1–3.6 and assembly are checked in Approach 11, resting only on standard facts (KZ bases, Minkowski–Weyl, Schur-concavity). Not re-proved, beyond reading their proofs, are the prime-divisibility Lemma 2.2(ii) and the few-exception shift Lemma 3.12. The lower cases $\mathrm{LRC}(m)$, $m \le 12$, are taken from the literature.
- **$\mathrm{LRC}(13)$.** The archive does not contain the $k = 13$ level-one rows, so the rows, cascade and completeness cannot be re-checked from it.
- **Our own code is not formally verified.** It is tested against brute force on small cases (18 tests) and against the certificates' own numbers.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| `find_witness` is a complete decision procedure; $\mathrm{ML}(v)$ is attained at some $a/(v_i+v_j)$ | proved (short proofs in docstring) | `lonely.py` |
| $\mathrm{ML}(1, \ldots, n) = 1/(n+1)$ exactly, $n \le 10$; $\mathrm{ML}(1,3,4,7) = 1/5$ | computed exactly | `test_lonely.py` |
| Every primitive tuple with max speed $\le N$ has a witness at $1/(n+1)$: $(n, N) = (3, 150), (4, 60), (5, 32), (6, 22), (7, 18)$ | computed up to $N$ | `results/exhaustive.txt` |
| Tight primitive tuples in those ranges: $(1,2,3)$; $(1,2,3,4)$, $(1,3,4,7)$; $(1,\ldots,5)$, $(1,3,4,5,9)$; $(1,\ldots,6)$; $(1,\ldots,7)$, $(1,2,3,4,5,7,12)$, $(1,4,5,6,7,11,13)$ | computed up to $N$ | `results/exhaustive.txt` |
| Sieve, naive level one, cover generator and `liftfree.c` agree with each other and with brute force from the definitions | tested (21 tests; 125 $(k,p)$ pairs for the generator) | `test_lonely.py` |
| $\mathrm{LRC}(3), \ldots, \mathrm{LRC}(8)$ (4–9 runners); gate sets in `results/lrc_k*.jsonl`; the $k = 8$ set equals Trakulthongchai's $S_8$ | certificate-checked computation **+ cited $B_k$** | `results/lrc_k3..8.jsonl` |
| $\mathrm{LRC}(9)$ (10 runners): all 47 primes $137, \ldots, 401$ pass (identical to Trakulthongchai's $S_9$), $\sum \ln p = 259.94 > 254.30$; cover generator, chain $\times 2\times 2\times 2$, proj, $\times 5\times 2$; 1,313 s wall on 4 processes | certificate-checked computation **+ cited $B_k$** | `results/lrc_k9.jsonl` |
| $\mathrm{LRC}(10)$ (11 runners): all 61 primes $127, \ldots, 467$ pass (identical to Sungkawichai–Trakulthongchai's $P_{10}$), $\sum \ln p = 342.72 > \ln B_{10} = 337.63$ (exact test `prod_ge_B_k_exact`); cover generator, chain $\times 2\times 2\times 2$, proj, $\times 11$ (`liftfree.c`); in every gate only $(1,\ldots,10)$ survives the $\times 2$ lifts and the $\times 11$ lift kills it; 13,924 s wall (about 13.8 core-hours, almost all level one) on 4 processes. Depends on cited $B_{10}$, $\mathrm{LRC}(9)$ and tested-not-verified code; does **not** use Prop. corlarge (Next steps 6) | certificate-checked computation **+ cited $B_k$** | `results/lrc_k10.jsonl` |
| Allikvere constants: $K_{13}$, $K_{14}$, ratio minima, $\ln$ bounds 341.031991 and 414.779365, target 401.984506 | exact rational re-derivation | `flag_bound.py` |
| $n = 15$ flag constants: $K_{15}$, ratio min $3751/2349 > 4/3$ | exact | `flag_bound.py` |
| $n = 15$ shape lemma $R_{15} < 49/100$ (min of $H \approx 944.96 > (1500/49)^2$), hence $\ln(v_1\cdots v_{15}) < 496.727$ and gate target 483.239 | shape lemma **proved** (written proof, every inequality exact-checked); the general-$n$ Thm 3.8 is **verified** (Approach 11; Lemmas 3.1, 3.2, 3.6 machine-checked exactly, 3.3–3.5 by reading), so the target is **proved given $\mathrm{LRC}(m)$, $m \le 14$** and standard facts | Approaches 10–11, `shape_lemma.py`, `flag_theorem_check.py`, tests |
| 4 of 71 $\mathrm{LRC}(14)$ gate certificates ($p = 263, 311, 397, 401$): rows improper, cascade and kill reproduced | independent re-computation of the certificate's claims **except level-one completeness** | `check_allikvere.py`, `results/allikvere_spotcheck.jsonl` |
| $\mathrm{LRC}(14)$ certificates: independent re-check of 71/71 gates. All 52 "J empty" gates and near-gcd gates 179 and 233 in full; cascade also in full at 223. Near-gcd gates 89, 163, 173, 223 (sample 3,000) and 131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241 (sample 500): all rows, plus seeded samples of the cascade and kill. Level-one completeness at 7 gates ($p = 89, 239, 251, 263, 269, 281, 283$). No discrepancy found. | independent re-computation of the certificates' claims; cascade sampled at 16 and kill at 17 of the 19 near-gcd gates; completeness at 6 gates only | `results/lrc14_gates/COVERAGE.md`, Approach 7 |
| $\mathrm{LRC}(13)$ certificates: terminal level-14 kill of both persistent orbits re-computed at all 111 gate primes; kill-file SHA-256s match manifests | independent re-computation (cascade and level one not checkable: rows not archived) | `results/lrc13_kills.jsonl` |
| $(1,\ldots,15)$ dies at level 16 at all 79 primes 251–743 | computed exactly (one orbit only) | `results/tight_orbit_k15.jsonl` |
| Child ordering + cutoff (`LRC_ORDER=1`) and incremental redundancy cut (`LRC_IRR` bit 4): same minimal covers as the plain search; $k = 14$ nodes $2.75\times$ fewer at $p = 113$ (58 s → 31.6 s), $3.5\times$ fewer at $p = 251$ (Knuth). Exact sharded run at $p = 251$ (step 13): $1.35\cdot 10^{10}$ nodes, 7,505 CPU-s ($4.1\times$ faster than step 6), same 3,876,360 covers and 2,404,346 orbits as the certificate | validated computation; **worked** (Knuth figures heuristic) | Approach 13, `results/knuth_order_k14.txt`, `results/lrc14_gates/regen_251_order.json` |
| $\mathrm{LRC}(15)$ (Allikvere, 16 runners): level-one completeness at gates $p = 269, 281, 311, 313, 317, 331, 347, 349, 367$ (6,589,665, 3,823,848, 2,811,345, 884,238, 430,529, 1,133,553, 237,421, 147,994 and 108,134 orbits), each equal to the certificate (step 17) | independent re-computation; **9 of 59 gates** (campaign paused 2026-11-26) | Approach 15, `results/lrc15_gates/` |
| Two-branch level-one search (`LRC_TWOBRANCH=1`): same minimal covers as the single tree in 36 configurations; node change at $k = 14$ is +14% ($p = 89$), +7% ($p = 113$), +3.4% ($p = 251$), +2.0% ($p = 401$) | validated computation; **failed route** (no speed-up) | Approach 12, `results/knuth_twobranch_k14.txt` |
| Cost of $\mathrm{LRC}(15)$ level one + kill with Allikvere-class code: about $1.75\cdot 10^{5}$ CPU-h (about 20 CPU-years) for 79 gates 251–743 under the flag target 483.24 (proved, Approaches 10–11); about $2.0\cdot 10^{5}$ CPU-h for level one with our generator (step 13; $9.5\cdot 10^{5}$ at step 11); about $8.7\cdot 10^{6}$ CPU-h under the proved $B_{15}$ | **heuristic extrapolation from measurements** | `cost_estimate.py`, `results/knuth_covergen_k14_k15.txt` |

"Certificate-checked computation + cited $B_k$" means the following. The chain $\mathrm{LRC}(2) \Rightarrow \cdots \Rightarrow \mathrm{LRC}(9)$ is a proof *if* three things hold:

- the MSS bound in Rosenfeld's Corollary 3 form,
- the elementary lemmas above,
- the correctness of our code.

Our code is tested against brute force, but not formally verified. These reproduce *known* cases only. Nothing new is claimed.

## $\mathrm{LRC}(17)$ (18 runners): progress toward the first unclaimed case

Started 2026-11-25. This is the current focus. The results below were reviewed by the coordinator, with key steps re-derived and the checks re-run. Details are in the linked notes. Pages under `notes/lonely-runner/` that are marked **Draft** are not yet reviewed.

**Gate target.** Write $\ln(v_1\cdots v_{17}) < \text{bound}$. Any counterexample with 17 speeds needs gate primes with $\sum \ln p$ above the target, which is the bound minus $\ln \operatorname{lcm}(2,\ldots,18) = \ln 12252240$.

| target | how | label | source |
| --- | --- | --- | --- |
| $670.28173$ | flag bound at $n = 17$; shape lemma $R_{17} < 951/2000$ | proved, given $\mathrm{LRC}(m)$ for $m \le 16$; exact arithmetic | `notes/lonely-runner/bound.md`, `bound/flag_n.py` |
| $667.92857$ | plus Lemma H (hyperplane prefix) and Lemma M | proved, same assumptions | `bound.md`, `bound/hyperplane.py` |
| $659.66535$ | coarse relation-rank bound; ranks 1–3 excluded by our own enumeration | proved, given also Allikvere's general lemmas as re-derived and **checked by reading** | `bound.md`, `bound/relrank_n.py`, `bound/rank_exclusion.py` |
| $647.534682$ | complete rank-4 census at $n = 17$: 34 admitted orbit representatives, $J_4 = 16.385$, so rank 5 binds ($J_5 = 14.529$) | proved, same assumptions; the census is complete and exact (byte-identical with pruning off; DP leaf count matches; independent Fraction re-check). At $n = 15$ the same code reproduces Allikvere's rank-3 and rank-4 tables. | `notes/lonely-runner/bound-rank4.md`, `bound/rank4/` |
| $647.085815$ | shape constants restricted to counterexample shapes: sweep lemmas (sharp BHS (a); a chain containing BNV Thm 1) and an exact branch-and-bound give $C_5 \le 2.855$ (was $3.0098$). $J_5 = 15.317$, rank 5 still binds. The flag radius improves to $R_{17} < 433/1000$, but $r_n$ cancels from this target. The gate set is unchanged (101 gates). | proved, same assumptions; exact rationals with interval-arithmetic logarithms; reviewed and re-run by the coordinator | `notes/lonely-runner/constrained-shape.md`, `bound/constrained/` |
| $646.040584$ | complete rank-5 section census at $n = 17$ for supports $a \le 9$ (48 profiles; $g_{\max} = 905, 963, 960, 1021$ at $a = 6$–$9$), so $J_5 = 30.28$ and rank 4 binds again ($J_4 = 17.32$). The gate set is unchanged. Dropping a gate needs about $642.2$, i.e. rank 4 improved by $1.57\times$. | proved, same assumptions; census exact and complete for $a \le 9$, with $a \ge 10$ coarse; **draft, not yet reviewed** | `notes/lonely-runner/bound-rank5.md`, `bound/rank5/` |

`bound/test_bound.py` has 18 tests, including negative controls; all pass, and they rerun the full census. These targets assume $\mathrm{LRC}(15)$ and $\mathrm{LRC}(16)$, which are claimed (Zenodo) but **unrefereed**.

**Structural lemmas** (`notes/lonely-runner/structure.md`):

- **Lemma S (proved).** For a prime $k+2 \le p \le 2k+1$, a tuple is improper at level one iff its $\pm$ classes cover all $(p-1)/2$ classes. This gives tiny level-one sets at the smallest primes; for $k = 17$ the orbit counts are 1430, 728, 40, 8 at $p = 19, 23, 29, 31$. Allikvere has the same lemma for $k = 15$; ours was derived before we read it.
- **Lemma T1 (proved).** For $p > k+1$, the class of $(1,\ldots,k)$ is improper at level $l$ iff $(k+1) \nmid l$. So $k = 17$ gates need a level divisible by $18$, i.e. lifts by 3 as well as 2.
- **$J(15,31) = \emptyset$** (certificate-checked, two independent implementations, re-run by the coordinator). This is an independent re-derivation of one of Allikvere's 16-runner preliminary primes, not a new gate.

**The tight orbit at $k = 17$** (`notes/lonely-runner/k17-structure.md`):

- **Theorem K (proved).** For every prime $p \ge 353$, the tight orbit $(1,\ldots,17)$ dies at level 18 along the lift chain $\times 3\times 2\times 3$; along $\times 2\times 3\times 3$ the same holds for $p \ge 421$.
- The proof uses Lemma R′ and the exact constants $\Lambda(17,3) = 1/352$ and $\Lambda(17,2) = 4/1683$. These were computed by two independent exact algorithms with a Fraction spot check; the coordinator re-ran the exact code and got $\Lambda(17,3) = 1/352$.
- **The smallest primes do not work.** The four Lemma S gates $p = 19, 23, 29, 31$ for $k = 17$ blow up under the cascade with NG; for example, $p = 31$ goes from 8 orbits at level 1 to $1.8\cdot 10^{7}$ at level 4. This is recorded as a failed route.
- **Lemma TN (proved)** gives lower bounds on the level at which a cascade with NG could close at small-$\tau$ primes.

**Mid-range primes as divisibility gates** (`notes/lonely-runner/midprimes17.md`; the proved parts were reviewed by the coordinator on 2026-11-26, the sampling results are heuristic):

- **Proved.**
  - *Lemma TF.* A "Lemma T family" (coordinates $\equiv 0$ mod the level whose classes cover, plus $f$ free coordinates) is extended-improper iff its free residues form a Lemma TN pattern. So such families die at level 18 when $f \le 5$.
  - *Corollary TN′* (given the exact Lemma TN search, which an independent enumeration reproduces). Every extended-improper tuple at level 18 has at least 6 coordinates not divisible by 18, for every base and every prime.
  - Also proved: Lemma $\mathrm{R}_b$ (Lemma R′ for any base tuple), and per-base closing levels are allowed.
- **Computed.** $\tau_{17} = 15$ at 251, 263, 269 and 277, and $\tau_{17} = 14$ at 271 and 281, all by exhaustive search. The tight orbit closes at level 18 along $3,3,2$ at every prime $97 \le p \le 311$.
- **Heuristic (sampling; no gate is closed).**
  - All 203,500 uniformly sampled level-one orbits close under the extended cascade (Lemma S at every $d \mid l$), at all 42 near-gcd primes $83 \le p \le 379$ with $\tau_{17}(p) \ge 12$. They close by level 18 (36 for 79 bases at 97, 127 and 131), and fibres stay small: below 5,000 orbits, except for three bases at 97, 127 and 131 (at most 46,080).
  - The samples do not close at 113 ($\tau_{17} = 11$, as Lemma TN predicts) or at 73.
  - Admitting these primes cuts the gate-set estimate at target 647.53 from $6.8\cdot 10^{7}$ to about $1\cdot 10^{7}$ CPU-h, still far beyond one machine.

**Cost (heuristic; draft page `notes/lonely-runner/gates.md`).**

- At target $659.67$, "J empty" gates alone need about 103 primes $313$–$1021$, with level one costing about $7.6\cdot 10^{7}$ CPU-h. Port Toner's orderly-root rule and this falls by a further factor of about 5–6.
- If the small and medium primes could also be closed, the estimate is about $4.6\cdot 10^{6}$ CPU-h.
- **Either way this is far beyond a single 4-core machine.**
- No prime below 258 can be a J-empty $k = 17$ gate. This follows from the exact $\tau_{17}$ table and Lemma N (`small-primes.md`, draft).

## Next steps: plan for LRC(15) (16 runners)

1. **Bound.**
   - Done (steps 9–10): $R_{15} < 49/100$ is proved (Approach 10), and the general-$n$ parts of Theorem 3.8 are independently verified (Approach 11). So the 16-runner gate target 483.239 is proved, given $\mathrm{LRC}(m)$ for $m \le 14$.
   - Without Theorem 3.8, the only target from MSS is $\ln B_{15} - \ln 720720 = 951.26$. That needs about 147 gates up to 1223, which is roughly $50\times$ the cost below.
2. **Generator.**
   - Done: his Lemma 4.1 normalisation (Approach 8), sharper bounds (Approach 9), and the two-branch search (step 11, Approach 12). The two-branch split is validated but gives **no** node reduction (+2–14%).
   - Step 12 (Approach 13): descending-gain child order with the child-gain cutoff (`LRC_ORDER=1`) and an incremental redundancy cut (`LRC_IRR` bit 4), taken from his generator's change log. Same output. Measured on an exact sharded run at $p = 251$ (step 13): $4.1\times$ faster than step 6, with the same 3,876,360 covers and 2,404,346 orbits. The real CPU gap to his engine at $p = 251$ is now $2.9\times$ (was about $7\times$), and about $2.2\times$ projected at $p = 401$.
   - Next leads:
     - the lexicographic-minimum rule is an output filter (one row per orbit), not a node saving;
     - from his change log, not yet tried: the exact two-slot finish, the mandatory-point bounds for the last 2–3 slots, and bit-parallel popcount kernels;
     - his precondition search certifying $\tau(p) \ge k - 1$ (affects only the small second branch);
     - the decomposition into jobs (done in step 15 as `LRC_SHARD_DEPTH=2`).
   - Steps 15–16 (Approach 14): exact two-slot finish, compile-time width, depth-1 job split, and Toner's orderly-root rule. The orderly rule is 3.4× faster at $(k,p)=(14,157)$ and cuts the $k=17$ tree 6–7× (Knuth).
   - Validate any change against the current generator, and then against his archived $k = 14$ rows at $p = 397$ and 401. Those are small gates: about 13 and 16 CPU-h for his code.
3. **Cost.**
   - Model: Allikvere's per-gate $k = 14$ CPU time, times our measured $k = 15$ / $k = 14$ tree-size ratio. The ratio grows from 4.4 at $p = 251$ to 10–18 at $p = 353$–$569$, fitted $\propto p^{1.0}$. His cost is fitted $\propto p^{6.07}$.
   - Result: **about $1.75\cdot 10^{5}$ CPU-hours for 79 gates $251, \ldots, 743$** under the flag target 483.239, which is now proved (Approaches 10–11). Of that, gates above 569 are extrapolated, and the top gates dominate. This is a **heuristic** extrapolation; the number is unchanged from step 2 because the target value is the same, and only its status changed (step 11).
   - Second model (`cost_estimate.py`; **heuristic**): **our** generator, level one only, for the same 79 gates.
     - Step 11 (`LRC_PRUNE=1`, `LRC_IRR=2`): about $9.5\cdot 10^{5}$ CPU-hours.
     - **Step 13 (`LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`): about $1.96\cdot 10^{5}$ CPU-hours (about 22 CPU-years).** That is comparable to the first model, which also includes the kill.
     - Inputs: our plain $k = 15$ tree $N_{15}(p) \propto p^{7.25}$ (Knuth); the $k = 14$ cut fraction (0.1425 at $p = 251$ from the exact run, 0.0837 at $p = 401$ from Knuth), fitted $\propto p^{-1.14}$ and assumed to carry over to $k = 15$ and up to $p = 743$; and the measured $1.8\cdot 10^{6}$ nodes/s.
     - The extrapolation of the cut fraction is the weakest input.
   - This is a **cluster-scale** project (for example 1,000 cores for about a week). It does not fit in a single session.
   - Uncertainties:
     - The ratio is noisy (single estimates per prime).
     - Small-$\tau$ gates may need the near-gcd treatment.
     - Better gate choices (including some $p < 251$) could change the total by small factors.
4. **The tight orbit is not a bottleneck.** $(1,\ldots,15)$ dies by level 16 at every candidate prime (Approach 6). The remaining unknown per gate is the level-one family and whether any other orbit persists.
5. **Finish the $\mathrm{LRC}(14)$ replay.** What remains:
   - full cascade and kill at near-gcd gates 163 and 173. These are **beyond this session's budget** (re-timed costs below) and are not being run;
   - the 13 near-gcd archives over 60 MB (0.1–1.6 GB; $p = 181$ has 8.2M orbits);
   - full rather than sampled cascade and kill at near-gcd gates 89 and 223 (the kill only at 223). $p = 179$ and $p = 233$ are done in full, and the full cascade at $p = 223$ is done (step 8). The full cascade at 89 is beyond budget and is not being run. The full kills at 223 and 89 are beyond budget and not run. $p = 233$ is now done in full, cascade and kill (`gate_233_full.json`; 10,703 s on 4 processes, about 11.9 core-hours).
   - Measured cost (step 8, single core): the kill takes 1.4–2.2 s per orbit and the cascade about 1 ms per row. Full kills would cost about 8.3 core-hours at 233 (13,457 orbits), 28.8 at 223 (48,071), 53.7 at 173 (96,840), 63.9 at 163 (107,244) and 70.5 at 89 (186,365). The earlier "about 0.5 s per orbit" was wall time per orbit on 4 processes. Full cascades (without kills) were first estimated at 0.5–3 core-hours per gate. That estimate timed only stored (ir) rows. The cascade input is the ir rows followed by the improper extension rows (km1 cover $\times\, x$), and an extension row costs 30–80 times as much as an ir row. Re-timed on the fixed `check_gate_full.py` (step 8, 2026-11-25; 2,000 ir rows and 60 extension rows per gate, single core, seeded), the projected full-cascade costs in core-hours are:
    - 233: 0.7 (ir) + 5.9 (782,536 ext);
    - 223: 0.2 + 8.9 (328,893 ext);
    - 163: 0.8 + 14.3 (3,722,274 ext);
    - 173: 0.9 + 32.7 (2,901,296 ext);
    - 89: 0.05 + 32.7 (855,976 ext; 0.14 s per ext row).
    - Check against a finished run: $p = 223$ took 8,999 s on 4 processes, about 10.0 core-hours, close to the sampled 9.1. A mid-run projection from the live read rate (about 25 core-hours) was misleading, because the expensive extension rows are clustered in the input.
    - Two attempts have been lost so far. The first $p = 89$ attempt (2026-11-24) ran serialised by a pipe bug, fixed in #61, and was stopped. The first $p = 223$ run was killed by a container restart.
    - Status: the $p = 223$ full cascade is done (pass, above). The $p = 233$ full cascade is done (pass, 3,634 s on 4 processes, about 4.0 core-hours, below the sampled 6.6). Gates 89, 163 and 173 are beyond budget (about 33, 15 and 34 core-hours for the cascade alone) and are not being run; they stay sampled.
   - level-one completeness at more gates. Unpruned, $p = 239$ took about 4.4 core-hours; with `LRC_PRUNE=2`, $p = 251$ took about 8.4 core-hours ($8.93\cdot 10^{10}$ nodes). The pruning gives only a modest node saving at these primes (Approach 8), so cost grows quickly with $p$. The next "J empty" gate, $p = 257$, is estimated (Knuth probes calibrated on the 239 and 251 runs, `results/knuth_completeness_257.txt`; heuristic) at $2.16\cdot 10^{11}$ nodes, about 20 core-hours. It was not run. A faster generator is the precondition for many more completeness gates. Approach 9's sharper gain bound gives about $1.7\times$, which brings $p = 257$ to about 12 core-hours; that is still not enough.
6. **$\mathrm{LRC}(10)$ (11 runners): done (step 7), with the label in the Results table.** Chain $\times 2 \times 2 \times 2$, projection, $\times 11$, with the $\times 11$ lift done by `liftfree.c` (`sieve.lift_c`, tested equal to the Python `lift`). All 61 gates $127, \ldots, 467$ pass and $\prod p \ge B_{10}$ holds exactly; see `results/lrc_k10.jsonl` and the SUMMARY line. Failed gates: none in this range (the run started at 127, $P_{10}$'s first prime; we did not test $p < 127$). This differs from Sungkawichai–Trakulthongchai, who avoid the $\times 11$ lift via their Prop. (corlarge, $p > k^2 + k$). Their $P_{10}$ is all 61 primes from 127 to 467 ($\sum \ln p > 342 > \ln B_{10} \approx 337.63$; read in the arXiv:2604.23906v2 source, Table 2).
   - **Dependencies of our $\mathrm{LRC}(10)$ chain.** It is the same trust base as for $\mathrm{LRC}(3)$–$\mathrm{LRC}(9)$ (see "Certificate-checked computation + cited $B_k$"):
     - the cited bound $B_{10} = \bigl(\binom{11}{2}^{9}/10\bigr)^{10}$, i.e. Malikiosis–Santos–Schymura in the form of Rosenfeld's Cor. 3;
     - $\mathrm{LRC}(9)$ (Trakulthongchai; also reproduced here);
     - the elementary lemmas F1, F2 and the prime-divisibility Lemma 2.2 / Cor. 2.4 of arXiv:2604.23906, with proofs written out above;
     - the correctness of `covergen.c`, `sieve.py` and `liftfree.c`, which are tested but not formally verified.
   - **Independence.** The chain does **not** use Sungkawichai–Trakulthongchai's Prop. corlarge, nor the footnoted inclusion for $p \in \{103, 107, 109\}$. The tight orbit $(1,\ldots,10)$ is killed by an explicit $\times 11$ lift. It also uses no flag bound and no forced divisor $\operatorname{lcm}(2,\ldots,11)$.
7. **Independent replay of 15 runners.** With the faster generator from step 2, rerun a handful of small $k = 14$ gates in full, including level-one completeness. This would upgrade the spot check.
8. **Do not** present any of this as a proof until every gate has stored, re-checkable output and the bound is proved.
