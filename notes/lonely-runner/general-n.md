# General-$n$ results: dense windows, a referee check of Bonfioli, and the range $v_n \le 1.47\,n$

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Track notes from the general-$n$ agent ("route 2", 2026-11-26). Companion code:
`computations/lonely-runner/generaln/`. Labels follow the repository README:
*proved* (complete written proof here), *computed* (exact integer arithmetic,
our own tested code, not formally verified), *heuristic* (floating point or
sampling).

## 0. Summary

| result | label |
| --- | --- |
| Bonfioli's Theorem D (dense window when $2m+1$ is prime) is correct as written; it is Lemma B below plus a pigeonhole count | proved (refereed here, §2) |
| **Theorem 1.** For every $n \ge 1$: if $v_n \le 2n + 2 - E(n)$, where $E(n) = \max_{1 \le j \le (n+1)/2} (j + g(j))$ and $g$ is Jacobsthal's function, then $\mathrm{ML}(V) \ge 1/(n+1)$. A simpler sufficient condition is $v_n \le \tfrac32(n+1) - G\bigl(\tfrac{n+1}2\bigr)$, with $G(x) = \max_{s \le x} g(s)$ | proved (§3) |
| **Corollary 1.** For every $n \ge 1$: if $v_n \le 147n/100$, then $\mathrm{ML}(V) \ge 1/(n+1)$ | proved for $n \ge 85$ (Theorem 1 with an exact table of $g$); computed for $n \le 84$ |
| Corollary 1 with $29n/20$, resp. $7n/5$, in place of $147n/100$ | proved for $n \ge 61$, resp. $n \ge 12$; computed below that |
| Dense window $\mathrm{DW}(m)$: every set of at most $m$ positive integers in $[1,2m]$ has $\mathrm{ML} \ge 1/(m+1)$ | computed for $2 \le m \le 51$ (all $m$, prime or composite $2m+1$); a second, independent program agrees for $m \le 13$ |
| Every set of $n$ positive integers in $[1, \lfloor 19n/10 \rfloor]$ is lonely | computed for $n \le 67$ |
| Primality cannot be removed using only times with denominator $\le 2m+2$: for every composite $2m+1$ with $15 \le 2m+1 \le 75$ some $m$-set in $[1,2m]$ meets every bad set of those times | computed |
| The full window $[1,2n]$ for all $n$ | **not achieved**; see §5 for the routes that failed |

Theorem 1 is the main new result. The best range valid for every $n$ that we
found in the literature is Tao's $v_n < 1.2n$. Bohman–Peng and Pomerance reach
$2n - c(\log n)^2$, but only for $n$ sufficiently large, with constants that are
not explicit (§4). Theorem 1 is explicit for every $n$, and gives
$\tfrac32 n - O((\log n)^2)$ asymptotically (typically $\tfrac32 n - O(1)$, since only $j$ near $(n+1)/2$ matter in $E(n)$). That is weaker than Bohman–Peng
for large $n$, so the novelty is explicitness, not the asymptotic range.

## 1. Setting and two basic lemmas

$V = \{v_1 < \dots < v_n\}$ are positive integers and $M = v_n$. A real $t$ is
a *witness* if $\lVert v t\rVert \ge 1/(n+1)$ for all $v \in V$. $V$ is
*lonely* if a witness exists, i.e. $\mathrm{ML}(V) \ge 1/(n+1)$. Integers not in
$V$ are *non-speeds*; every integer above $M$ is a non-speed.

**Lemma A** (divisibility; Tao, arXiv:1701.02048v4, Lemma 5.1(i)). If some
$q \in [2, n+1]$ divides no element of $V$, then $t = 1/q$ is a witness.

*Proof.* $\lVert v/q\rVert \ge 1/q \ge 1/(n+1)$ when $q \nmid v$. $\blacksquare$

**Lemma B** (coprime pair of non-speeds). Let $s, t$ be positive non-speeds
with $\gcd(s,t) = 1$ and $M < s + t \le 2n+2$. Put $N = s + t$ and let $c$ be
the inverse of $s$ modulo $N$. Then $c/N$ is a witness.

*Proof.* $\gcd(s, N) = \gcd(s, t) = 1$, so $c$ exists and is a unit mod $N$.
Take $v \in V$. Since $1 \le v \le M < N$, we have $vc \not\equiv 0$. Also
$vc \equiv \pm 1$ iff $v \equiv \pm s \pmod N$, iff $v \in \{s, N - s\} = \{s, t\}$,
because $1 \le v < N$; but $s, t$ are non-speeds. So $vc \bmod N \in [2, N-2]$,
and $\lVert vc/N\rVert \ge 2/N \ge 2/(2n+2) = 1/(n+1)$. $\blacksquare$

The device is that of Bohman and Peng (arXiv:2109.09860v1, §3, the time
$q/(s+t)$). They use only $s + t \le 2n$, to get a strict inequality. For
the non-strict statement, $N = 2n+1$ and $N = 2n+2$ are also allowed. Bonfioli's
prime case uses exactly these two moduli, and they enlarge the range of Theorem 1
by allowing $N$ up to $2n+2$.

## 2. Referee check of Bonfioli's dense-window Theorem D

**Source.** V. Bonfioli, Zenodo record 24189338, version 1.6.0 (published
2026-11-13), archive `ElVec1o/lonely-runner-covering-v1.6.0.zip`, MD5
`52d5a6be65052f006c061e974793f7e1` (our download matches the record's checksum).
We read `paper/dense-window/main.tex`, "Instances of the lonely runner conjecture
for integer speeds in $[1,2m]$", dated 9 November 2026, §1–3 and the composite-case
summary. It is unrefereed, a single-author preprint, and it discloses AI
assistance. We ran no code from the archive.

**Statement (Theorem 3 there, "Theorem D").** Let $m \ge 2$ with $2m+1$ prime,
and $v_1, \dots, v_m$ integers in $[1,2m]$ (repetitions allowed). Then
$\mathrm{ML}(v) \ge 1/(m+1)$.

**The proof, step by step.** Here $n = m$.

- *P1* (his Lemma 2). If $1 \notin V$, then $t = 1/(2m+2)$ works:
  $2 \le v \le 2m$ gives $\lVert v/(2m+2)\rVert \ge 2/(2m+2)$. **Correct.**
  In our terms this is Lemma B with $(s,t) = (1, 2m+1)$.
- *P2* (Lemma 1). If some $q \in [2, m+1]$ divides no speed, then $1/q$ works. **Correct**; this is Lemma A.
- *P3* (Lemma 3, forced pair). Otherwise $m+1 \in V$, the only multiple of
  $m+1$ in $[1,2m]$. Also $m \in [2, m+1]$ (this uses $m \ge 2$), so $m \in V$
  or $2m \in V$. Either $m + (m+1)$ or $1 + 2m$ is a pair of distinct speeds
  with sum $2m+1$. **Correct.**
- *P4* (Lemma 4). Let $N = 2m+1$ be prime. The $m$ classes $\{s, N-s\}$,
  $1 \le s \le m$, partition $[1,2m]$. The at most $m$ distinct speeds include
  two in the same class, so they meet at most $m-1$ classes. If $\{s, N-s\}$ is
  missed, then $c = s^{-1} \bmod N$ gives residues $vc \notin \{0, \pm 1\}$, and
  $\lVert vc/N\rVert \ge 2/N > 1/(m+1)$. **Correct.** In our terms the missed
  class is a pair of non-speeds $s, N - s$ with $\gcd(s, N-s) = \gcd(s,N) = 1$,
  and $N = 2m+1 > M$, so this is Lemma B.

**Where primality is used.** Only in P4, and only through "every class
$\{s, N-s\}$ consists of units". For composite $N$ the missed class may consist of
non-units. The manuscript says so itself and gives the example
$m = 7$, $V = \{1,2,4,5,6,7,8\}$. We re-checked it: $\mathrm{ML}(V) = 2/13$, and no
$c/15$ is a witness (`test_generaln.py::test_bonfioli_composite_example`).

**Verdict.** Theorem D and its written proof are correct, for multisets too.
The proof is short and elementary; the manuscript itself calls it "a routine
consequence of known ingredients".

**Minor points found.**

- The "Primality" paragraph says there are "32, 544, 368 such sets" for
  $m = 7, 10, 12$, where "such" reads as "sets with a pair summing to $N$ and no
  witness $c/N$". With that reading we count 384 and 15360 for $m = 7, 10$. The
  numbers 32 and 544 are the counts of *case-3* sets (1 present, every
  $q \le m+1$ dividing a speed) without a witness $c/N$, as in the manuscript's
  own table. Ours agree with those (`bonfioli_counts.py`; $m = 12$ not re-run).
  So it is a wording slip, not an error in the mathematics.
- The composite cases $m \le 126$ rest on Lean certificates that we did not
  rebuild or read. Our own exhaustive computation (§3.3) independently confirms
  the dense-window statement for all $m \le 51$, composite or prime.

**Is Theorem D new?** We found no earlier statement of the dense window for an
infinite family of $m$ (§4), and the manuscript says the same. It answers Tao's
"speeds at most $2n$" question for $n$ with $2n+1$ prime, given the trivial checks
above.

## 3. Theorem 1: the range $v_n \le 2n + 2 - E(n) \approx \tfrac32 n$

**Jacobsthal's function.** $g(s)$ is the least $g$ such that every $g$
consecutive integers contain one coprime to $s$; $g(1) = 1$. It depends only on
the radical of $s$. Put $G(x) = \max_{1 \le s \le x} g(s)$. Exact values (computed): $G(x) = 1, 2, 4, 6, 10, 14$ on the ranges
$[1,2)$, $[2,6)$, $[6,30)$, $[30,210)$, $[210,2310)$ and $[2310, 2400]$; the jumps are at the primorials in this range.

**Lemma J.** Let $s \ge 2$ with $\omega(s) = w$ distinct prime factors, and let
$h \ge (2^w - 1)\, s/\varphi(s)$. Then every $h$ consecutive integers contain one
coprime to $s$. Hence $g(s) \le \lceil (2^w - 1)\, s/\varphi(s)\rceil$, and
$s/\varphi(s) \le \prod_{i \le w} p_i/(p_i - 1)$, where $p_i$ is the $i$-th prime.

*Proof.* Let $r$ be the radical of $s$. In a block of $h$ consecutive integers
the number of multiples of $d$ is $h/d + \theta_d$ with $\lvert\theta_d\rvert < 1$,
and $\theta_1 = 0$. By inclusion–exclusion the number of elements coprime to $s$ is

$$\sum_{d \mid r} \mu(d) \Bigl(\frac hd + \theta_d\Bigr) = h\,\frac{\varphi(s)}{s} + \sum_{d \mid r,\, d > 1} \mu(d)\,\theta_d > h\,\frac{\varphi(s)}{s} - (2^w - 1) \ge 0.$$

The inequality is strict because $w \ge 1$ and each of the $2^w - 1$ terms is
less than 1 in absolute value. So the count is a positive integer. The bound on
$s/\varphi(s) = \prod_{p \mid s} p/(p-1)$ holds because $p/(p-1)$ decreases in $p$. $\blacksquare$

(Sharper classical bounds exist, e.g. Iwaniec's $g(s) \ll (\log s)^2$, but they
are not needed.)

**Theorem 1.** Let $n \ge 1$ and let $V$ be $n$ distinct positive integers with
maximum $M$. Put

$$E(n) = \max_{1 \le j \le (n+1)/2} \bigl(j + g(j)\bigr).$$

If $M \le 2n + 2 - E(n)$, then $V$ is lonely: $\mathrm{ML}(V) \ge 1/(n+1)$.

Since $j + g(j) \le \lfloor (n+1)/2 \rfloor + G((n+1)/2)$ for $j \le (n+1)/2$,
the hypothesis holds whenever

$$M \le \tfrac32 (n+1) - G\Bigl(\frac{n+1}{2}\Bigr).$$

*Proof.* Suppose $V$ has no witness. Write $x = \lfloor (n+1)/2 \rfloor$, so
$x \ge n/2$, and note $E(n) \ge x + g(x) \ge x + 1$, so $M \le 2n + 1 - x$.

1. If $M \le n$, then $V = [1,n]$ and $t = 1/(n+1)$ is a witness. So $M \ge n+1$.
2. **Large $j$.** Let $M/2 < j \le n+1$. Then $j \ge 2$, and the only multiple of
   $j$ in $[1,M]$ is $j$. By Lemma A, $j \in V$.
3. **Middle $j$.** Let $(n+1)/2 < j \le M/2$, so $j \ge x + 1$. Then
   $3j \ge 3x + 3 > 2n + 1 - x \ge M$, because $4x \ge 2n > 2n - 2$. So the
   multiples of $j$ in $[1,M]$ are $j$ and $2j$, and by Lemma A, $j \in V$ or
   $2j \in V$. Note that $2j > n+1$.
4. **Small $j$.** Let $1 \le j \le (n+1)/2$, and suppose $j \notin V$. The interval
   $(M + j,\, 2n+2]$ contains $2n + 2 - M - j \ge E(n) - j \ge g(j)$
   consecutive integers. So it contains an $N$ with $\gcd(N, j) = 1$. Then
   $t = N - j > M$ is a non-speed, $\gcd(j, t) = \gcd(j, N) = 1$, and
   $M < N \le 2n+2$. By Lemma B, $V$ has a witness, a contradiction. So $j \in V$.
5. **Counting.** Define $f$ on $[1, n+1]$ by $f(j) = j$ in steps 2 and 4 and in
   step 3 when $j \in V$, and $f(j) = 2j$ in step 3 when $j \notin V$. Then
   $f(j) \in V$ for every $j$. The values $f(j) \le n+1$ are the $j$ themselves,
   and the values above $n+1$ are distinct even numbers $2j$. So $f$ is
   injective, and $\lvert V\rvert \ge n+1$, a contradiction. $\blacksquare$

The steps cover $[1, n+1]$: step 4 covers $[1, (n+1)/2]$, step 3 covers
$((n+1)/2, M/2]$, and step 2 covers $(M/2, n+1]$.

*Credit.* The skeleton is Tao's proof of his Prop. 1.5 (the injection
$j \mapsto j$ or $2j$). The new input is step 4: Tao forces small $j$ into $V$ with
his Lemma 5.1(ii), which forces $j \in V$ only when $2(n+1-j) \ge \max V$; that is what limits his range to $1.2n$. We use
instead the Bohman–Peng pair time (Lemma B) with $N$ up to $2n+2$, controlled by
Jacobsthal's function.

$E(n)$ is usually $x + 2$ to $x + 6$: only $j$ close to $x$ matter, because
$g(j) \le G(x)$ is small. For example the largest admissible $M$ is
$15, 28, 74, 148, 298, 1498$ for $n = 10, 20, 50, 100, 200, 1000$, against
$14, 27, 72, 145, 295, 1491$ from the simple form.

**Machine check of the case split** (computed). `theorem1.py` follows steps 1–4
constructively. For every $n \le 15$ and every $n$-set with maximum at most
$2n + 2 - E(n)$, it produces the witness its case gives. Each witness is
re-verified with the independent exact routine `lonely.check_witness`: 224,521
sets, with no failure and no set reaching the impossible step 5. As a negative
control, beyond the range ($n = 12$, $M \ge 2n-2$) the case split does fail on
some lonely set (`test_theorem1_fails_beyond_range`).

### 3.1 Corollary 1: $v_n \le 147n/100$ for every $n$

**Corollary 1.** For every $n \ge 1$, every set of $n$ positive integers with
$v_n \le 147n/100$ is lonely.

*Proof for $n \ge 85$ (proved).* We need $\lfloor 147n/100 \rfloor \le 2n + 2 - E(n)$.

- For $n \le 20000$ this is checked number by number with the exact table of
  $g(s)$, $s \le 10000$. The last failure is at $n = 84$.
- For $n > 20000$ we check the simple form instead,
  $2 \cdot 147 n \le 100\,\bigl(3(n+1) - 2G\bigr)$, which implies the condition.
  We use $G(x) \le \max\bigl(G(10^4),\, B(k)\bigr)$ for $x < p_{k+1}\#$, where
  $p_k\#$ is the $k$-th primorial and
  $B(k) = \lceil (2^k - 1) \prod_{i \le k} p_i/(p_i-1) \rceil$
  (Lemma J; $\omega(s) \le k$ when $s < p_{k+1}\#$). On each block
  $p_k\# \le x < p_{k+1}\#$ the inequality is linear in $n$ with slope
  $3 - 2.94 > 0$, so it suffices to check it at the block's smallest $n$. This
  is done exactly for every block up to $k = 40$.
- For $k > 40$ we have $B(k) \le 4^k$ and $p_k\# \ge 10^{9} \cdot 4^k$. The
  simple form reads $0.06\, n + 3 \ge 2G$, and for $n \ge 2p_k\# - 1$ we get
  $0.06\, n + 3 \ge 0.12\, p_k\# \ge 2 \cdot 4^k \ge 2B(k)$.

`jacobsthal.py 147 100 10000` returns $n_0 = 85$ for this form. $\blacksquare$

*Small $n$ (computed).* For $n \le 84$, `dwsolve` decides exhaustively that every
$n$-subset of $[1, \lfloor 147n/100\rfloor]$ has a witness at $1/(n+1)$:
`results/window_147_100.txt`, 84 of 84 values of $n$. The same was run for
$\lfloor 29n/20 \rfloor$ with $n \le 80$ (`results/window_29_20.txt`), where the
proved part starts at $n = 61$. With $7n/5$ it starts at $n = 12$.

So "$v_n \le 1.47\,n$ implies lonely" holds for every $n$: proved for $n \ge 85$
and computed for $n \le 84$. For $n \le 12$ the full LRC is classical or
refereed in any case.

**Corollary 2** (shape of a dense-window counterexample; proved). Suppose
$V \subseteq [1, 2n]$, $\lvert V\rvert = n$, has no witness, and let $M = \max V$. Then:

- $2n+1$ is composite (Theorem D), and $M > 2n + 2 - E(n)$ (Theorem 1);
- every $j \in (M/2, n+1]$ lies in $V$ (step 2, which does not use the bound on $M$);
- every $j \le n+1$ with $j + g(j) \le 2n + 2 - M$ lies in $V$ (step 4); in particular $1 \in V$;
- the non-speeds in $[1, n+1]$ number $1 + \lvert V \cap (n+1, M]\rvert$, and they all lie in $(2n + 2 - M - G(M/2),\, M/2]$.

For large $n$ the Bohman–Peng and Pomerance theorem adds $M > 2n - c(\log n)^2$.

### 3.2 Why the argument stops at $3/2$

The injection breaks if a small $j \le (n+1)/2$ is a non-speed. Its only certain
replacement is a multiple $2j \le n+1$, which is already the image of $2j$. Step 4
excludes such $j$ only while $(M+j, 2n+2]$ is long enough to contain an integer coprime
to $j$. For $j$ near $(n+1)/2$ that interval has length about $\tfrac32(n+1) - M$. Going
past $3/2$ needs a Hall-type matching between low non-speeds and high speeds; that
is the coprime-mapping theorem of Bohman–Peng and Pomerance, which is not explicit (§4).

### 3.3 Computations

**Solver** (`dwsolve.c`, exact integers). The bad set of a time $a/q$ is
$B(a/q) = \{x \in [1,H] : K \min(xa \bmod q,\, q - xa \bmod q) < q\}$, with
$K = m+1$ and $H = 2m$ by default. A set has no witness among a family of times
iff it meets every bad set.

- The program enumerates the hitting sets of size $\le m$ of the inclusion-minimal
  bad sets of all $a/q$ with $q \le Q$. It branches on the smallest unhit set and
  forbids earlier siblings; completeness is argued in the file header.
- Each hitting set found is given a *complete* witness test: the left-endpoint
  search of `../lonely.py`. If the test finds a witness $t$, then $B(t)$ joins the family and the search
  continues. If not, the set is printed as a counterexample.
- If the search ends with no counterexample, the statement is decided for that $m$.

Results (all computed, exact):

- **Full dense window**, $2 \le m \le 51$, $Q = 4m$: no counterexample
  (`results/dw_full_m2_47.txt` and `results/dw_full_m48_plus.txt`). The time
  roughly doubles every two steps; $m = 47, \dots, 51$ took 510, 217, 956, 484 and
  609 s; $m = 52$ did not finish within 2400 s. This independently confirms Bonfioli's statement for $m \le 51$,
  including the 25 composite values of $2m+1$ in that range.
- **Restricted windows:** $[1, \lfloor 147n/100\rfloor]$ for $n \le 84$, $[1, \lfloor 29n/20\rfloor]$ for $n \le 80$, and
  $[1, \lfloor 19n/10 \rfloor]$ for $n \le 67$: no counterexample (`results/window_*.txt`).
- **Negative controls** (`test_generaln.py`): at the threshold $1/m$ the solver
  finds a counterexample for every $m \le 8$, and `lonely.find_witness`
  independently confirms it. In a window wider than $[1,2m]$ at threshold $1/m$ it also
  fails, as it must.
- **Completeness of the search** (`test_fixed_mode_complete_vs_bruteforce`). For
  $(m, Q) = (7, 16), (10, 22), (12, 26)$ the $m$-supersets of the reported hitting
  sets are exactly the $m$-sets that a brute force over all $m$-subsets finds to
  hit every bad set.
- **Second implementation** (`dw_bruteforce.py`, pure Python, no shared code with
  `dwsolve.c`). It checks every $m$-subset of $[1,2m]$ separately, and every
  witness it uses is re-verified by `lonely.check_witness`. It agrees for
  $m \le 13$ (`results/dw_bruteforce_m1_13.txt`; columns: $m$, number of $m$-sets, number that needed the complete search, counterexample). For $m = 13$ that is 10,400,600 sets.

## 4. Literature searched (2026-11-26)

- **arXiv.** API queries `all:"lonely runner"` and `all:lonely AND all:runners`
  (46 records, 2007–2026), `all:lonely AND all:Jacobsthal` (none) and
  `abs:"lonely runner" AND abs:coprime` (two: Bohman–Peng, Pomerance). All titles were scanned.
- **Read in source:**
  - Tao, arXiv:1701.02048v4, §5: Prop. 1.5, $v_i \le 1.2n$, for every $n$, by an injection $j \mapsto j$ or $2j$, and Lemma 5.1.
  - Bohman–Peng, arXiv:2109.09860v1, Thm 1.2 and §3: loose instances for $n < v_n \le 2n - \exp(C(\log\log n)^2)$, "for sufficiently large $n$".
  - Pomerance, arXiv:2111.07157v1: $2n - c'(\log n)^2$, again for sufficiently large $n$ and an unspecified constant.
  - The Perarnau–Serra survey, arXiv:2409.20160v3, §4 and the "Linearly bounded speeds" subsection, and Problem 6.
  - Pandey (via the survey, Cor. "ap"): dense subsets of progressions, and the remark that $v_n \le 2n-3$ remains open only when $v_1 = 1$.
  - Zhang, arXiv:2608.13599v3, and Bhardwaj–Narayanan–Venkataraman, arXiv:2211.08749v3, for any explicit linear range. They state none.
- **Zenodo.** Queries `"lonely runner" AND dense`, `AND Tao`, `AND coprime`,
  `AND "bounded speeds"`, `AND Jacobsthal`. The only dense-window record is Bonfioli 24189338.
- **Outcome.** We found no explicit range $v_n \le \alpha n$ with $\alpha > 1.2$
  valid for every $n$, and no general-$n$ dense-window result other than
  Bonfioli's prime case. This does not show that none exists. The Mathematika
  version of Bohman–Peng was not read.

## 5. Failed routes (kept)

1. **A different single modulus.** For a fixed $N \in (M, 2n+2]$, Lemma B with the class count gives
   only $\lvert V \cap (\mathbb Z/N)^*\rvert \ge \varphi(N)/2$. For $N = 2m+1$
   composite, $\varphi(N)/2 < m$, and the speeds that are non-units mod $N$ are
   unconstrained, so no contradiction arises.
   A prime $p = 2m+1-2j < 2m+1$ has $p \le 2m$, so $p$ itself may be a speed and
   then blocks every time $c/p$. Otherwise the speeds must meet $m-j$ classes with $m$
   elements, and nothing forces $j+1$ collisions.
2. **All denominators up to $2m+2$** (computed). With all times of denominator
   $\le 2m+2$, the solver finds $m$-sets meeting every bad set for **every**
   composite $2m+1$ with $15 \le 2m+1 \le 75$; only $m = 4$ ($2m+1 = 9$) closes.
   The least $Q$ that closes, $Q_{\min}$, sits at $2m + c$ with $c$ ranging over
   $5, 8, 5, 6, 8, 7, 9, 12, 8, 10, 12, 15, 12$ for
   $m = 7, 10, 12, 13, 16, 17, 19, 22, 24, 25, 27, 28, 31$. The offset is not
   bounded in this range, so no fixed finite family of denominators near $2m$ removes primality.
3. **Tao's perturbed times.** Adding $d/j + 1/(2j(m+1))$ (Tao's Lemma 5.1(ii) with $k=2$)
   to the denominators $\le 2m+2$ still leaves transversals for every composite $2m+1$
   in $[15, 57]$ (computed, `explore/taofam.py`).
4. **Fractional blocking** (heuristic: floating-point LP, HiGHS). The fractional
   transversal number of the bad sets with denominators $\le 4m$ is exactly $m+1$
   whenever $2m+1$ is prime ($m \le 30$). For composite $2m+1$ it is $\le m$ in many cases:
   $m = 10, 16, 24, 27$ give exactly $m$, and $m = 17, 19, 22, 25, 28$ give less than $m$.
   So an averaging argument over denominators cannot replace integrality. This matches
   Bonfioli's remark that the fractional bound is $m$ at $2m+1 = 21, 33, 49$, and his
   use of fractional certificates exactly at $m = 4, 7, 12, 13$, where we find a value above $m$.
   Script `explore/lp.py`; all data for routes 2–4 are in `results/failed_routes_data.txt`.
5. **Pairs plus divisibility for the whole range below $2n$** (computed). Using only
   Lemma A and Lemma B, every $n$-set with $\max \le 2n-3$ is handled for $n \le 26$.
   This fails at $n = 28$ ($M = 53$) and $n = 32$ ($M = 61$), both $2n-3$.
   For every $n \le 34$ with $2n+1$ prime the family closes all $M \le 2n$,
   as Theorem D predicts; among composite $2n+1$ only $n = 4$ closes. So
   Lemmas A and B alone cannot give the window $[1, 2n-3]$ for every $n$,
   however the counting is done. The slack this family needs seems to grow
   slowly with $n$, which fits the Jacobsthal-type obstruction discussed by
   Bohman–Peng and Pomerance; that is an observation on $n \le 34$, not a proof. Data: `results/pairs_div_family.txt`
   (`explore/bpfam.py`).
6. **Induction on the number of speeds above $n+1$.** If $h$ speeds lie above
   $n+1$, then $h+1$ non-speeds lie in $[1,n+1]$, all in $(2n+2-M-G, M/2]$ by steps 2 and 4 of Theorem 1. Each low
   non-speed $j$ forces all integers coprime to $j$ in a window of length
   $2n+2-M$ to be speeds. This gives counting constraints, but at $M$ near $2n$
   the window has length 2 and the constraints are void. Not pursued further.

## 6. Reproduce

```
cd computations/lonely-runner/generaln
python3 -m pytest -q test_generaln.py          # 12 tests, about 20 s
python3 theorem1.py 15                         # case split of Theorem 1, n <= 15
python3 jacobsthal.py 147 100 10000             # n0 = 85 (E form) for Corollary 1
python3 jacobsthal.py 29 20 5000               # n0 = 61 (E form)
python3 jacobsthal.py 7 5 2000                 # n0 = 12 (E form)
sh run_windows.sh /tmp/dwbuild                 # restricted windows (about 3 min)
gcc -O2 -o /tmp/dwbuild/dwsolve dwsolve.c
for m in $(seq 2 51); do /tmp/dwbuild/dwsolve $m $((4*m)) | tail -1; done   # full window, about 70 min
python3 bonfioli_counts.py 7 10                # the 32 / 544 counts of §2
python3 dw_bruteforce.py 13                    # second implementation, m <= 13
```

All runs above used one core.
