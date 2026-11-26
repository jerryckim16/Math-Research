# Explicit ranges below $2n$: a matching criterion, an explicit Hall lemma, and $v_n \le 1.93n$ up to $10^{47}$

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Track notes (general-$n$ explicit agent, 2026-11-26). Continues
[general-n.md](general-n.md) (Theorem 1, Corollary 1: $v_n \le 1.47n$ for every
$n$). Companion code: `computations/lonely-runner/generaln/` (`matchcrit.c`,
`check_matching.py`, `explicit_core.py`, `theoremL.py`, `test_explicit.py`).
Labels as in the README: *proved* (complete written proof here), *computed*
(exact integer arithmetic, our own tested code, not formally verified),
*heuristic*.

Notation as in general-n.md: $V$ is a set of $n$ distinct positive integers,
$M = v_n = \max V$, and $V$ is *lonely* if some $t$ has $\lVert vt\rVert \ge 1/(n+1)$
for all $v \in V$. Lemma A (divisibility) and Lemma B (coprime pair of non-speeds
with $M < s+t \le 2n+2$) are used as stated there.

## 0. Summary

| result | label |
| --- | --- |
| **Novelty.** Bohman–Peng and Pomerance contain no explicit $n_0$ and no explicit constant for the lonely-runner application. No later paper we found states an explicit range beyond Tao's $1.2n$ valid for every $n$ (§1). One step in the proof of Bohman–Peng's Lemma 2.3 (arXiv v1) is not justified as written (§1.3); we do not use that lemma | literature check, bounded (§1) |
| **Lemma C** (matching criterion). If a bipartite graph $G(n,M)$, defined from $n$ and $M$ only, has a matching saturating $[1, \lfloor M/2\rfloor]$, then every $n$-set with maximum $M$ is lonely. It is monotone in $M$ | proved (§2) |
| $M^*(n)$, the largest $M$ for which Lemma C applies, for every $n \le 12000$: $2n - M^*(n) \le 12$ throughout, and $M^*(n) = 2n$ exactly when $2n+1$ is prime or $n = 4$ | computed (§3) |
| Every $n$-set with $v_n \le 2n - 14$ is lonely, for every $n$ with $12001 \le n \le 28560$ | computed (§3) |
| **Lemma H** (explicit Hall condition for two progressions) and **Lemma G** (block geometry) | proved (§4, §5) |
| **Theorem L.** For every $n$ with $2^{19} \le n < 2^{157}$: $v_n \le 2n - n^{0.6}$ implies lonely; for $2^{26} \le n < 2^{157}$ even $v_n \le 2n - \sqrt n$ | proved, with an exact finite check of Lemma H's numeric hypothesis per block (§6) |
| **Corollary L.** For every $n < 2^{157}$ (about $1.8 \cdot 10^{47}$): $v_n \le 1.93n$ implies lonely. With $1.95n$ the same holds except that $n \in \{58, 59, 60, 94, 124\}$ are not covered | computed for $n \le 28560$, proved for $28560 \le n < 2^{157}$ |
| A range $\alpha n$ with $\alpha > 1.47$ valid for **every** $n$ | **not achieved**: the explicit argument here stops somewhere near $n \approx e^{300}$ (§7); the block table was computed only to $2^{157}$ |

So the answer to "can Theorem 1 be made significantly stronger?" is: yes in a
huge but bounded range ($1.93n$, and $2n - n^{0.6}$, for every $n$ below
$1.8 \cdot 10^{47}$), not yet for all $n$.

## 1. Literature searched (2026-11-26)

### 1.1 Bohman–Peng

- **Read in full:** arXiv:2109.09860, the only arXiv version (v1, 20 Sep 2021),
  LaTeX source. Published as T. Bohman, F. Peng, *Coprime mappings and lonely
  runners*, Mathematika (2022), DOI 10.1112/mtk.12131 (the DOI comes from a
  web-search result). The publisher site `londmathsoc.onlinelibrary.wiley.com`
  and `api.crossref.org` are blocked from this session, so **the published
  version was not read**, and its volume and pages are unconfirmed.
- Theorem 1.2: "there exists a constant $\mathcal C$ such that for sufficiently large
  $n$, if $n < v_n \le 2n - \exp(\mathcal C (\log\log n)^2)$", the instance is loose.
  The proof (§3) needs Theorem 2.1 for intervals of length $2m$ in $[2n]$ with
  $m \ge \lceil\exp(\mathcal C_0(\log\log 2n)^2)\rceil$, and that rests on Fact 2.5
  (Erdős's Jacobsthal bound $c_1\omega^{c_2}$, constants not given).
- **Explicit content found:** Remark 2.6 gives explicit sufficient conditions
  for Lemmas 2.3 and 2.4 (for Lemma 2.3: $M = (m/5)^{1/\log_2(2r)} > \log n$ and
  $\log n/(M\log M) < 1/9$; for Lemma 2.4: $m^{1/3} \ge 16$ and
  $\log n/(M \log M) < 1/45$). §4 proves the Larsen et al. conjecture (adjacent
  intervals) explicitly for all $k \ge 4$; there $m \ge (n-2)/6$ is linear in $n$, which is
  of no use for the lonely runner. There is **no explicit $n_0$ and no explicit
  $\mathcal C$** for Theorem 1.2, because Fact 2.5 is used with unspecified constants.

### 1.2 Pomerance

- **Read in full:** arXiv:2111.07157, the only arXiv version (v1, 13 Nov 2021),
  LaTeX source (`coprime11_12.tex`). A web search shows a journal-formatted PDF
  on the author's site with the header "INTEGERS: 21 (2021)" and a revised file
  `coprime11_12rev.pdf`. The host `math.dartmouth.edu` is blocked from this
  session, so **neither was read**.
- Theorem 1 and Proposition 2: constants $c, c_1, \dots, c_5$ are not given; the
  input from Iwaniec (Jacobsthal bound) is used with an unspecified constant, and
  several steps say "for $m$ sufficiently large". The lonely-runner remark gives
  $v_n \le 2n - c'(\log n)^2$ with $c'$ unspecified. **No explicit constant or $n_0$.**

### 1.3 A gap in Bohman–Peng, Lemma 2.3 (arXiv v1)

In the case "$p \in P_k$, $p > M$" the proof claims
$\lvert J_k \cap p\mathbb Z\rvert < \lvert J_k\rvert/p + 1$ "by (2.6)". But (2.6) is
stated for an arithmetic progression, and $J_k = J \setminus (p_1\mathbb Z \cup \dots \cup p_k \mathbb Z)$ is
not one. The inequality can fail: if $m/p$ is slightly above $1$, $J$ can contain
two multiples of $p$, neither divisible by any $p_i$, while
$\lvert J_k \rvert/p + 1 \approx (m/p)\prod(1 - 1/p_i) + 1 < 2$. The step is
repairable, since $\lvert J_k\cap p\mathbb Z\rvert \le \lvert J \cap p\mathbb Z\rvert \le m/p+1$ and
$\Phi \ge 2m/(k+2)$, at the cost of a factor of about $(k+2)/2$ in the
large-prime term, so the asymptotic theorem is unaffected. We did not check whether the
published version changed this. Nothing below uses Bohman–Peng's lemmas.

### 1.4 Later work

- arXiv full-text search `"lonely runner"` (45 records, newest 2610.23790), all
  titles scanned. The abstracts were scanned for "2n", "1.2", "Tao", "coprime",
  "linear", "bounded speeds", "sufficiently large". None states an explicit linear
  range. The recent ones are about small $k$ (2509.14111, 2511.22427, 2512.01912,
  2604.23906, 2609.02604), gaps (2511.16636, 2610.23790), spectra, shifted
  versions, and tight instances (2608.13599).
- arXiv `"coprime matching"`, `"coprime mapping(s)"`: besides the two papers, only
  2610.37512 (coprime matchings of divisor sets; not about intervals or runners).
- `export.arxiv.org` and Semantic Scholar are blocked, so a citation-graph
  search of the two papers was not possible. The arXiv listing and web search
  are the only sources used.
- **Outcome.** We found no explicit range $v_n \le \alpha n$ with $\alpha > 1.2$ valid for
  every $n$, other than our own Corollary 1 ($1.47n$), and no explicit form of the
  Bohman–Peng or Pomerance range. This is a bounded search, not a proof that none exists.

## 2. Lemma C: a matching criterion that depends only on $(n, M)$

**Definition.** For $n \ge 1$ and $n+1 \le M \le 2n$ put $A = \lfloor M/2 \rfloor$.
$G(n,M)$ is the bipartite graph with left side $[1, A]$, right side $[n+2, 2n+2]$,
and edges

- (a) $s \sim t$ when $\gcd(s,t) = 1$ and $M < s + t \le 2n+2$;
- (b) $s \sim 2s$ when $s \ge 2$, $3s > M$ and $2s \ge n+2$.

**Lemma C.** If $G(n,M)$ has a matching $\tau$ that saturates $[1,A]$, then every
set $V$ of $n$ distinct positive integers with $\max V = M$ is lonely.

*Proof.* Suppose $V$ has no witness. Let $x = \max([1,n+1] \setminus V)$; it exists
because $\lvert V \cap [1,n+1]\rvert \le n$.

1. If $x > M/2$: since $M \ge n+1 \ge 2$ we have $x \ge 2$, and the only multiple
   of $x$ in $[1, M]$ is $x \notin V$. By Lemma A ($x \le n+1$), $1/x$ is a
   witness. So $x \le A$, that is, $[A+1, n+1] \subseteq V$.
2. Let $s \in [1,A] \setminus V$ and $t = \tau(s)$. If the edge is of type (a)
   and $t \notin V$, then $s, t$ are coprime non-speeds with $M < s+t \le 2n+2$,
   and Lemma B gives a witness. If it is of type (b) and $2s \notin V$, then
   $s \le A \le n$, $s \ge 2$, and the multiples of $s$ in $[1,M]$ are $s$ and $2s$
   (as $3s > M$); none is in $V$, so Lemma A gives the witness $1/s$. So $\tau(s) \in V$.
3. Define $f$ on $[1, n+1]$ by $f(j) = j$ if $j \in V$ and $f(j) = \tau(j)$ otherwise
   (then $j \le A$ by step 1). By step 2, $f$ maps into $V$. Values at most $n+1$
   are fixed points, values at least $n+2$ are distinct values of the injective $\tau$.
   So $f$ is injective and $\lvert V\rvert \ge n+1$, a contradiction. $\blacksquare$

**Lemma C' (monotone).** If $G(n,M)$ has a matching saturating $[1, \lfloor M/2\rfloor]$,
so does $G(n, M')$ for every $n+1 \le M' \le M$. Hence every $n$-set with
$n < v_n \le M$ is lonely, and sets with $v_n \le n$ are $[1,n]$, which is lonely.

*Proof.* Restrict the matching to $[1, \lfloor M'/2 \rfloor]$. An edge of type (a)
for $M$ is one for $M'$ ($M' < M < s+t$), and so is an edge of type (b)
($3s > M > M'$). $\blacksquare$

*Relation to Theorem 1.* Theorem 1 of general-n.md is the special case where
small $j$ are matched to $t > M$ (forced non-speeds) and middle $j$ to $2j$.
Lemma C allows $t \le M$, which is what the coprime-matching method of
Bohman–Peng and Pomerance needs; Lemma C states it as one finite matching problem
per $(n, M)$, independent of $V$.

## 3. Computations with Lemma C (computed)

**Program.** `matchcrit.c` builds $G(n,M)$ with exact gcds and finds a maximum
matching by Hopcroft–Karp. `matchcrit cert n M` prints the matching.
`check_matching.py`, which shares no code with it, re-verifies a certificate
(every $s \le \lfloor M/2\rfloor$ matched, images distinct in $[n+2,2n+2]$, every
pair an edge of type (a) or (b)). Tests (`test_explicit.py`, 9 tests):

- the certificates for $M^*(n)$, $n \le 250$, and for $n = 2252, 12000, 30011$ are
  re-verified;
- the criterion fails at $M^*(n)+1$ whenever $M^*(n) < 2n$;
- negative controls: a certificate with a non-coprime pair, or with a repeated image, is rejected;
- for $n \le 8$ every $n$-subset of $[1, M^*(n)]$ is confirmed lonely by the
  exact witness search `lonely.find_witness`. This is only a sanity check, since the conjecture is known for these $n$.

**Results.**

- *Exact $M^*(n)$ for $1 \le n \le 12000$* (`results/matchcrit_scan_1_12000.txt`;
  columns $n$, $M^*(n)$, $f^*(n) = 2n - M^*(n)$). The values of $f^*$ are $0$ (2669
  times), $2$ (2265), $3$ (once, $n = 17$), $4$ (1911), $5$ (twice), $6$ (2449),
  $8$ (1906), $10$ (737) and $12$ (60). Records: $f^* = 2, 3, 4, 6, 8, 10, 12$ first at
  $n = 7, 17, 25, 94, 124, 1153, 2252$. By Lemma C', **every $n$-set with
  $v_n \le 2n - f^*(n)$ is lonely, for every $n \le 12000$**. In particular $v_n \le 2n-12$
  suffices for every $n \le 12000$. That is far beyond Theorem 1 ($\approx 1.5n$) and the dense-window
  computations of general-n.md ($[1, 1.9n]$ for $n \le 67$).
- $f^*(n) = 0$, i.e. the full window $[1,2n]$, holds exactly for the $n \le 12000$ with
  $2n+1$ prime and for $n = 4$. So on the window $[1,2n]$ the criterion
  reproduces Bonfioli's prime case and nothing more: it does not settle any
  composite $2n+1$ beyond $9$.
- *Fixed deficiency 14*, $M = 2n - 14$, for every $12001 \le n \le 28560$: no failure
  (`results/matchcrit_fixed14_12001_28560.txt`). Partial runs beyond that found
  the first failures of $F = 14$ near $n \approx 5.9 \cdot 10^4$ (e.g. $n = 58967$,
  deficit 3), so $f^*(n) > 14$ occurs there (`results/matchcrit_fixed14_partial.txt`).
  $f^*$ grows, slowly.

All runs used at most 3 cores; the exact scan to $12000$ took a few minutes on one core.

## 4. Lemma H: an explicit Hall condition for two progressions

Two integers are *2-coprime* if they have no common odd prime factor.

**Lemma H.** Let $I, J \subseteq [1, N]$ be arithmetic progressions of $m \ge 2$ terms
with common difference $2$. Let $p_1 = 3, p_2 = 5, \dots$ be the odd primes, let $j$
be the largest index with $p_1 \cdots p_j \le N$, and put
$\gamma^* = \prod_{i \le j}(1 - 1/p_i)$, $x = m\gamma^* - (2^j - 1)$ and
$k_0 = \lfloor x \rfloor + 1$. Let $\ell$ be the largest integer with $m^\ell \le N$, and for odd
primes $p < m$ let $a_p = \lceil m/p \rceil$. Suppose every integer $k$ with
$k_0 < k \le (m+1)/2$ lies in an interval $[k_1, k_2]$ with

$$\sum_{p < m \text{ odd prime}} \min(k_1, a_p)\,\min(m+1-k_2, a_p) + \ell k_1 < k_1 (m+1-k_2). \qquad (\mathrm{LAM})$$

Then there is a bijection $I \to J$ under which matched numbers are 2-coprime.

*Proof.* By Hall's theorem it suffices to show: whenever $S \subseteq I$,
$T \subseteq J$ and $\lvert S\rvert + \lvert T\rvert = m+1$, some $s \in S$ and $t \in T$ are 2-coprime.
(If Hall's condition failed for some $S$, then $T = J \setminus N(S)$ would violate this.)
Both sets are nonempty. The hypothesis depends only on $(m, N)$, so we may
swap the roles of $I$ and $J$ and assume $k := \lvert S \rvert \le \lvert T\rvert$, so
$k \le (m+1)/2$ and $\lvert J \setminus T\rvert = k - 1$.

*Case $k \le k_0$ (one element suffices).* Take any $s \in S$, let $\rho$ be the product of
its distinct odd prime factors and $w = \omega(\rho)$. The terms of $J$ are
$b, b+2, \dots, b+2(m-1)$, and for odd $d$ the multiples of $d$ among them are every
$d$-th term, so their number is $m/d + \theta_d$ with $\lvert\theta_d\rvert < 1$, and $\theta_1 = 0$.
By inclusion–exclusion (as in Lemma J of general-n.md) the number $c(s)$ of terms
coprime to $\rho$ satisfies $c(s) > m\varphi(\rho)/\rho - (2^w - 1)$. Since $\rho \le s \le N$, we
have $w \le j$, and $\varphi(\rho)/\rho \ge \gamma^*$ (replace the prime factors of $\rho$ by the $w$
smallest odd primes; this lowers the product and does not raise $\varphi(\rho)/\rho$). So
$c(s) > x$, hence $c(s) \ge \lfloor x\rfloor + 1 = k_0 \ge k$. These $c(s)$ terms are
2-coprime to $s$ and cannot all lie in $J \setminus T$, which has $k - 1$ elements.

*Case $k > k_0$ (counting).* For an odd prime $p$ write $S_p = S \cap p\mathbb Z$, $T_p = T \cap p\mathbb Z$.
A pair in $S \times T$ that is not 2-coprime lies in some $S_p \times T_p$, so it suffices that
$\sum_p \lvert S_p\rvert \lvert T_p\rvert < k(m+1-k)$. For $p < m$: $I$ and $J$ contain at most $a_p$
multiples of $p$, so $\lvert S_p\rvert \lvert T_p\rvert \le \min(k, a_p)\min(m+1-k, a_p)$. For $p \ge m$:
multiples of $p$ in $J$ are $2p$ apart while $J$ spans $2(m-1)$, so $\lvert T_p\rvert \le 1$;
and each $s \le N$ has at most $\ell$ distinct prime factors $p \ge m$, so
$\sum_{p \ge m}\lvert S_p\rvert \le k\ell$. Dividing by $k(m+1-k)$, it suffices that

$$\sum_{p<m} \min\Bigl(1, \frac{a_p}{k}\Bigr)\min\Bigl(1, \frac{a_p}{m+1-k}\Bigr) + \frac{\ell}{m+1-k} < 1.$$

For $k_1 \le k \le k_2$ the left side is at most the left side of (LAM) divided by
$k_1(m+1-k_2)$, because $\min(1, a/k) \le \min(k_1,a)/k_1$ and
$\min(1, a/(m+1-k)) \le \min(m+1-k_2, a)/(m+1-k_2)$. $\blacksquare$

**Monotonicity in $N$.** For fixed $m$, the hypothesis for $N$ implies it for every
$N' \le N$: $j$ and $\ell$ do not increase, and $\gamma^*$ does not decrease, so $x$
does not decrease (it changes from $m\gamma^*_N - 2^{j}+1$ to $m\gamma^*_{N'} - 2^{j'}+1$ with $j' \le j$).

**Checker** (`explicit_core.py`, exact integers and fractions). `check_H(m, N)`
computes $j, \gamma^*, k_0, \ell$ and covers $(k_0, (m+1)/2]$ by intervals satisfying
(LAM); `verify_pieces` re-checks a cover. For $m > 20011$ the primes $20011 < p < m$
are not summed one by one: their terms are replaced by the upper bound
$\sum_{\text{odd } n \in (P_0, m)} (m/n+1)^2 \le m^2/(2P_0) + m\ln(m/P_0) + m/2$ with
$P_0 = 20011$ (each term $\min(k_1,a_p)\min(u,a_p) \le a_p^2 \le (m/p+1)^2$; for odd $n > P_0$,
$1/n^2 \le \frac12\int_{n-2}^n x^{-2}dx$ and $1/n \le \frac12\int_{n-2}^n x^{-1}dx$; and
$\ln y \le 0.6932 \cdot (\text{bit length of } \lceil y\rceil)$). Tests: random progression pairs
($m \le 40$, $N \le 1200$) on which the hypothesis holds always have a 2-coprime
perfect matching (brute force); negative control: $I = \{105, 107\}$, $J = \{63, 65\}$
has none ($105$ meets every element of $J$), and `check_H(2, 107)` is false.

Least $m$ for which the hypothesis holds (computed): $m = 14, 33, 83, 179, 397, 840$ for
$N = 10^2, \dots, 10^7$; $m = 3737$ at $10^{10}$; $1.38 \cdot 10^7$ at $10^{30}$; $5.4 \cdot 10^{14}$ at
$10^{80}$. The $2^j$ term dominates, so $m$ grows like $N^{O(1/\log\log N)}$: faster than any
power of $\log N$, slower than any power of $N$.

## 5. Lemma G: from coprime matchings of blocks to Lemma C

Write $D = 2n + 2 - M$, $A = \lfloor M/2\rfloor$, and say that the condition $H(m)$ holds if
Lemma H's hypothesis holds for $(m, 2n+2)$. Splitting an interval of length $2m$
into its even and odd elements gives two progressions of $m$ terms with
difference 2, and a 2-coprime matching between an even and an odd number is a
coprime matching. So $H(m)$ gives a coprime bijection between any two intervals
of length $2m$ in $[1, 2n+2]$ (even part to odd part, odd part to even part).

**Lemma G.** Let $n+1 \le M \le 2n$.

- (U) If $H(m)$ holds and $D \ge 8m - 2$, then $G(n,M)$ has a matching saturating $[1,A]$.
- (T) If $H(m)$ and $H(m+1)$ hold, $D \ge 4m + 6$ and $n \ge 2m^2 + 2$, the same conclusion holds.

*Proof.* Choose block lengths $\lambda_1, \dots, \lambda_q$, with sum $A' \ge A$, and a constant $C$. Put
$I_i = [\lambda_1 + \dots + \lambda_{i-1} + 1,\ \lambda_1 + \dots + \lambda_i]$ and let $J_i$ be the interval of length $\lambda_i$
with $\max J_i = C - \min I_i$. Then the $J_i$ tile $[C - A', C - 1]$ and are pairwise disjoint.
For $s \in I_i$ and $t \in J_i$ we have $C - \lambda_i + 1 \le s + t \le C + \lambda_i - 1$. If
(i) $C + \lambda_{\max} - 1 \le 2n+2$, (ii) $C - \lambda_{\max} + 1 \ge M+1$ and (iii) $C - A' \ge n+2$,
then the coprime bijections $I_i \to J_i$ combine into an injective map
$[1, A'] \to [n+2, 2n+2]$ along edges of type (a). Its restriction to $[1, A]$ is the matching.

- (U): all $\lambda_i = 2m$, $q = \lceil A/(2m)\rceil$, so $A' \le A + 2m - 1$, and $C = 2n + 3 - 2m$.
  (i) holds with equality. (ii) is $D \ge 4m - 1$. (iii) is $A' \le n + 1 - 2m$, which
  follows from $A \le n + 1 - D/2$ and $D \ge 8m - 2$.
- (T): $\lambda_i \in \{2m, 2m+2\}$ and $C = 2n + 1 - 2m$. With $q$ parts every even number in
  $[2mq, (2m+2)q]$ is a sum of $q$ parts; for $q \ge m-1$ consecutive ranges meet, so every
  even $A' \ge 2m(m-1)$ is attainable. (i) holds with equality, and (ii) is
  $D \ge 4m+3$. (iii) needs an even $A'$ in $[\max(A, 2m(m-1)),\ n - 1 - 2m]$. That interval
  contains two consecutive integers because $n - 1 - 2m - A \ge D/2 - 2m - 2 \ge 1$ and
  $n - 1 - 2m - 2m(m-1) \ge 1$. $\blacksquare$

Test: for $(n, m) = (1023, 80), (4000, 83), (20000, 179)$ the construction (U), with brute-force
block matchings, produces a matching of $G(n, 2n+4-8m)$ that `check_matching.py` accepts.

## 6. Theorem L

**Theorem L.** Let $n \ge 1$, $N = 2n+2$, and let $V$ be a set of $n$ positive integers.

- If Lemma H's hypothesis holds for $(m, N)$ and $v_n \le 2n + 4 - 8m$, then $V$ is lonely.
- If it holds for $(m, N)$ and $(m+1, N)$, $n \ge 2m^2 + 2$ and $v_n \le 2n - 4m - 4$, then $V$ is lonely.

*Proof.* If $v_n \le n$, then $V = [1,n]$. Otherwise apply Lemma G with $M = v_n$
($D \ge 8m-2$, resp. $D \ge 4m+6$), then Lemma C. $\blacksquare$

**The table** (`theoremL.py`, `results/theoremL_table.txt`; proved, given the exact
finite check). For the block $2^i \le n < 2^{i+1}$, $6 \le i \le 156$, put $N_i = 2^{i+2}$
(this is $2n + 2$ at the block's top). The script finds the least $m_i$ with Lemma H's hypothesis
for $(m_i, N_i)$ and $(m_i + 1, N_i)$, checked exactly. By monotonicity in $N$ the hypothesis then holds for
every $n$ in the block. A few rows:

| block $i$ | $m_i$ | $4m_i + 4$ |
| --- | --- | --- |
| 16 ($n \ge 65536$) | 397 | 1592 |
| 19 | 397 | 1592 |
| 24 | 843 | 3376 |
| 40 | 16944 | 67780 |
| 80 | 3149633 | 12598536 |
| 120 | 259549184 | 1038196740 |
| 156 | 10026400898 | 40105603596 |

Consequences, each checked block by block from the table (on a block the bound
$4m_i + 4$ is constant and $n \ge 2^i$):

- **$2n - n^{0.6}$.** For $2^{19} \le n < 2^{157}$, $n \ge 2m_i^2 + 2$ holds and $4m_i + 4 \le n^{0.6}$ (the largest
  ratio $(4m_i+4)/2^{0.6i}$ is $0.59$, at $i = 19$). So **$v_n \le 2n - n^{0.6}$ implies lonely**.
- **$2n - \sqrt n$.** For $2^{26} \le n < 2^{157}$ the ratio $(4m_i+4)/2^{i/2}$ is at most $0.87$ (at $i = 26$; it is $1.22$ at $i = 25$).
- **$1.93n$ and $1.95n$.** Use the first part of Theorem L, whose condition $v_n \le 2n + 4 - 8m$
  follows from $v_n \le 1.95n$ once $0.05n \ge 8m - 4$. With $m = 179$ (Lemma H holds for
  $(179, 131072)$, hence for every $N \le 131072$) this covers $28560 \le n < 65536$; with
  $m = 397$ it covers $65536 \le n < 2^{21}$; and for every later block $8m_i - 4 \le 0.05 \cdot 2^i$
  (checked from the table). The same holds a fortiori with $1.93n$.
- **Small $n$.** For $12001 \le n \le 28560$, §3 gives $v_n \le 2n - 14$, which contains $v_n \le 1.93n$.
  For $n \le 12000$, the scan file has $M^*(n) \ge \lfloor 1.93n \rfloor$ except at
  $n = 7, 10, 12, 13, 17, 25, 28, 32, 38$, and $M^*(n) \ge \lfloor 1.95n \rfloor$ except at 19 values of $n$, the largest
  $58, 59, 60, 94, 124$. Every $n \le 51$ is covered by the full dense-window computation of
  general-n.md ($\mathrm{DW}(m)$ for $m \le 51$, computed), which contains $[1, \lfloor\alpha n\rfloor]$ for any $\alpha \le 2$.
  That leaves $n = 58, 59, 60, 94, 124$ for $1.95n$ (see the end of §3 for the attempt to close them).

**Corollary L.** For every $n < 2^{157}$, every set of $n$ positive integers with
$v_n \le 1.93n$ is lonely. (Computed for $n \le 28560$; proved for $28560 \le n < 2^{157}$.)
The same with $1.95n$ holds for every $n < 2^{157}$ other than $58, 59, 60, 94, 124$.

The upper limit $2^{157}$ is where we stopped the table (time box), not where the
argument stops; see §7.

## 7. Where the explicit argument stops, and failed routes

1. **The limit of Lemma H.** The one-element case needs $k_0 \approx m\gamma^*$, and
   $\gamma^* = \prod_{p \le p_j}(1 - 1/p) \approx 1.12/\log p_j \approx 1.12/\log\log N$ tends to $0$. The counting case
   (LAM), with the trivial bounds $\lvert S_p\rvert \le \min(k, a_p)$, $\lvert T_p\rvert \le \min(\lvert T\rvert, a_p)$, needs
   $\sum_{p} \min(1, 1/(\sigma p)) \cdot 1/((1-\sigma)p) < 1$ with $\sigma = k/m$. That is $0.986$ at $\sigma = 0.2$ and
   above $1$ at $\sigma = 1/6$, so it cannot reach below $\sigma \approx 0.19$ (heuristic computation,
   floating point). Lemma H therefore fails, for every $m$, once $\gamma^* < 0.19$ or so,
   which happens for $p_j$ of a few hundred, i.e. $N$ around $e^{300}$ (heuristic: from $\gamma^* \approx 1.12/\log p_j$). At $i = 156$ the table has $\gamma^* = 0.2295$.
   Between $2^{157}$ and the true limit the table could be extended mechanically. Beyond the limit one needs the
   "zooming" step of Bohman–Peng (Lemma 2.3: pass to $S \cap p\mathbb Z$, $T \setminus p\mathbb Z$ when $S$
   is concentrated on multiples of $p$), with the repair of §1.3 and explicit
   error terms. We did not carry this out. **This is the missing piece for a statement valid for every $n$.**
2. **Moment method for the one-element bound (failed: too weak).** A first version of Lemma H
   handled all $k$ through the distribution of $\gamma_z(i) = \prod_{p \mid i,\, 2 < p \le z}(1-1/p)$, using
   Markov's inequality on $\sum_{i \in I}\gamma_z(i)^{-a}$ (multiplicative, with explicit constant
   $\prod_{2<p\le z}(1 + ((p/(p-1))^a - 1)/p)$), and handled primes above $z$ by a union bound. The
   union bound costs $m\ell/(z+1)$ per element, and inclusion–exclusion costs $2^{\pi(z)}$. It needed
   $m \ge 0.077N$ at $N = 10^6$, against $m \ge 397$ for Lemma H. Discarded.
3. **Jacobsthal-only bounds.** Bounding each $c(s)$ by $\lfloor m/g(\rho)\rfloor$ covers only
   $\lvert S\rvert \le m/g$; every explicit bound on $g$ that we know is far too large for this to meet the counting case.
   Not used.
4. **Pomerance's route made explicit (not attempted in full).** Its steps "$\omega(n) \le 2\log n$",
   "$n/\varphi(n) \le 3\log\omega(n)$ (from Rosser–Schoenfeld)" are explicit, but the Iwaniec input
   ($\ge \omega^2$ coprime integers in every interval of length $c_1 (s/\varphi(s))\omega^2\log\omega$) has no
   explicit $c_1$ that we can cite. Without it the $(\log n)^2$ range is out of reach here, and what remains
   is the averaging argument, which is essentially Lemma H's counting case.
5. **Lemma C does not give the dense window.** $f^*(n) = 0$ only for prime $2n+1$ (and $n = 4$),
   for $n \le 12000$. The Hall-type criterion loses exactly where Bonfioli's pigeonhole on
   classes modulo a prime wins.

## 8. Reproduce

```
cd computations/lonely-runner/generaln
python3 -m pytest -q test_explicit.py                 # 9 tests, about 1 min
gcc -O2 -o /tmp/mc matchcrit.c
/tmp/mc scan 1 12000 > /tmp/scan.txt                  # a few minutes
/tmp/mc fixed 14 12001 28560                          # about 8 min
/tmp/mc cert 2252 4492 | python3 check_matching.py    # independent re-check
python3 theoremL.py 6 156                             # Theorem L table, under 1 h
```

All runs used at most 3 cores.
