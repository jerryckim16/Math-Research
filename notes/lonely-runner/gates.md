# Gate selection for LRC(15) and LRC(17): admissibility ($\tau$), cost per prime, pilot

*Best read on the [progress site](https://jerryckim16.github.io/Math-Research/notes/lonely-runner/gates.html), where all the math is typeset. GitHub's own preview does not render the math in long files.*

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Track notes (gates agent, 2026-11-25). Companion to `problems/lonely-runner.md`
(Approaches 7–13 and "Next steps: plan for LRC(15)"). Code:
`computations/lonely-runner/k15/` and `computations/lonely-runner/k17/`. The
coordinator integrates these notes into the problem file; this note does not
edit it.

Labels: **proved**, **computed** (exact computation, tested code, not formally
verified), **certificate data** (numbers read from Allikvere's archives, not
recomputed), **heuristic** (Knuth estimates and extrapolations).

## 1. Admissibility: the covering number $\tau_k(p)$

**Definition.** Fix $k$ and a prime $p > k+1$, and put $h = (p-1)/2$.

- A folded speed class $v$ *covers* a folded time $a$ when $(k+1)\,d_p(av) < p$.
  This is the relation used in `covergen.c`.
- Each class covers $m = \lfloor (p-1)/(k+1) \rfloor$ times.
- $\tau_k(p)$ is the least number of classes that together cover all $h$ times.
- A $k$-multiset lies in $I(k,p,1)$ exactly when its support covers every time.

**Lemma T (proved here).** If $\tau_k(p) \le k-2$, then $I(k,p,l) \ne \emptyset$
for every level $l$ with $\gcd(l,p) = 1$. So the gate cannot be closed as
"$J(k,p) = \emptyset$" by any cascade whose levels are coprime to $p$: binary,
3-adic, and so on.

*Proof.* Let $C = \{c_1, \dots, c_s\}$ be a cover with $s \le k-2$, and put
$N = lp$. By CRT, choose

$$w_i \equiv c_i \pmod p,\quad w_i \equiv 0 \pmod l \quad (i \le s), \qquad w_j \equiv 1 \pmod p,\quad w_j \equiv 1 \pmod l \quad (j > s).$$

There are $k - s \ge 2$ coordinates of the second kind, and no coordinate is
divisible by $p$.

- **No witness.** Take $t = m'/N$.
  - If $p \nmid m'$, then $w_i t \equiv (w_i/l)\,m'/p \pmod 1$, with
    $w_i/l \equiv c_i l^{-1} \pmod p$.
  - Multiplication by the unit $l^{-1}$ maps covers to covers. So some $i \le s$
    has $(k+1)\,d_p(m' c_i l^{-1}) < p$, i.e. $\lVert w_i t \rVert < 1/(k+1)$.
  - If $p \mid m'$, then $t \in \tfrac1l\mathbb Z$ and $w_1 t \in \mathbb Z$.
- **The gcd clause fails.** For every $i$, the coordinates other than $i$
  include some $w_j \equiv 1 \pmod l$. So $\gcd(l, w_j : j \ne i) = 1$.

Hence $w \in I(k,p,l)$, and $w$ lies above $(c_1, \dots, c_s, 1, \dots, 1)$. $\blacksquare$

The boundary case $\tau = k-1$ behaves differently. There the same construction
has only one free coordinate. Dropping it leaves coordinates all divisible by
$l$, so the tuple is proper by the gcd clause.

**This is the $J$-empty admissibility condition.** Two pieces of evidence:

- Allikvere's "$J(14,p) = \emptyset$" gates are exactly the $\tau_{14} \ge 13$
  ones, and his near-gcd gates the $\tau_{14} \le 12$ ones.
- At $k = 15$, each of his 59 campaign gates records the precondition "covers on
  $\le 13$ classes $= 0$".

So $\tau_k(p) \ge k-1$ is necessary for a $J$-empty gate. Gates with smaller
$\tau$ can still give divisibility, but only through a near-gcd argument
(Lemma S, §2).

**Tool:** `k15/tau.c`, run as `tau k p smax` (optionally with `TAU_FROM`). It is
an exhaustive DFS for a cover that contains class 1 and has at most $s$ classes.

- **Search rules.** Unit normalisation; branching on the most-constrained time,
  with exclusion of earlier siblings; and a bound requiring the top
  $(s - \lvert L\rvert)$ gains to sum to at least $\lvert U\rvert$.
- **Extra cuts (on by default).** The Lemma 4.1 $q$-cut and an empty-private-set
  cut. Both are valid for minimal covers, and a least cover is minimal.
- **Reading the output.** A cover found proves $\tau \le s$. An exhausted search
  proves $\tau > s$.
- **Validation** (`k15/test_gate15.py::test_tau`). It equals a brute force over
  all subsets at $(k,p) = (5,29), (5,31), (6,37), (7,41), (7,43)$, with and
  without the cuts.
- **Reproduction of Allikvere's $k = 14$ split.** We get $\tau_{14} = 12, 11, 13, 12, 13, 13$
  at $p = 89, 131, 239, 241, 251, 257$.

### $k = 15$ screen (computed)

Each entry answers "is there a cover on at most 13 classes?":

| $p$ | result |
| --- | --- |
| 17–23, 37–233, 241, 251, 257, 263 | a cover on $\le 13$ classes is found, so $\tau_{15} \le 13$: near-gcd only |
| 29, 31 | $\tau_{15} = 14, 15$ (here $m = 1$, so $\tau = h$) |
| **239** | $\tau_{15} \ge 14$, **proved** (exhaustive, 60 s) |

**The pre-Allikvere 79-gate plan is not admissible as stated.** That plan (all
primes 251–743; problem file, Next steps 3) assumed $J$-empty gates throughout,
but $\tau_{15} = 13$ at 251, 257 and 263.

This agrees with Allikvere's "Sixteen lonely runners" (Zenodo
10.5281/zenodo.23304361; certificate data):

- 251 and 257 appear only in his weighted-shift divisibility audit;
- 263 appears in a divisibility "provenance" record;
- 239 is one of his five $J$-empty preliminary gates (239, 271, 283, 293, 307);
- his campaign starts at 269.

## 2. Lemma S, a shift lemma for improper lifts (proved here)

Assume LRC($m$) for all $m < k$. Let $N = lp$, $d \ge 2$ with $d \mid N$, and
$w \in \mathbb Z_N^k$. Put

$$E = \{i : d \nmid w_i\}, \qquad g_i = \gcd(w_i, d), \qquad b_i = g_i \left\lceil \frac{2d}{(k+1)\,g_i} \right\rceil .$$

**Statement.** If $E \ne \emptyset$ and $\sum_{i \in E} b_i < d$, then every
integer tuple $u \equiv w \pmod N$ with all $u_i \ne 0$ is lonely: some $t$ has
$\lVert u_i t \rVert \ge 1/(k+1)$ for all $i$.

**When $E \ne \emptyset$ holds automatically.** Suppose $w$ is improper at level
$l$ and $d \mid l$. If $\lvert E\rvert \le 1$, the gcd clause would hold, since
removing the exceptional index (or any index, if $E = \emptyset$) leaves
$\gcd \ge d$. So $\lvert E\rvert \ge 2$.

*Proof.* Since $d \mid N$, we have $d \mid u_i \iff d \mid w_i$ and
$\gcd(u_i, d) = g_i$.

1. **A base time.** By LRC($k - \lvert E\rvert$) for $(u_j)_{j \notin E}$
   (repeats allowed; trivial if the set is empty), there is $t_0$ with
   $\lVert u_j t_0 \rVert \ge 1/(k - \lvert E\rvert + 1) \ge 1/(k+1)$ for
   $j \notin E$. Only LRC($m$) with $m < k$ is used.
2. **Shifted times.** For $r \in \mathbb Z_d$ put $t = t_0 + r/d$. For
   $j \notin E$ we have $u_j t \equiv u_j t_0 \pmod 1$.
3. **Counting bad shifts.** For $i \in E$, the values $u_i r/d$ run over a coset
   of $(g_i/d)\mathbb Z$, and each point is hit by $g_i$ values of $r$. An open
   arc of length $2/(k+1)$ contains a run of consecutive progression points, at
   most $\lceil (2/(k+1))/(g_i/d) \rceil$ of them. So at most $b_i$ values of $r$
   give $\lVert u_i t \rVert < 1/(k+1)$.
4. **Conclusion.** Since $\sum b_i < d$, some $r$ is good for every $i \in E$. $\blacksquare$

**Relation to Allikvere's Lemma 3.12.** For $g_i = 1$, Lemma S is his
few-exception shift, with $m_d = \lceil 2d/(k+1) \rceil$ and $e\,m_d < d$. The
$k = 14$ version, with $d \in \{3,5\}$, is in `gatecheck.c`.

**Divisibility (Lemma 2.2(ii) form).** Suppose that for some level $l$ every
member of $I(k,p,l)$ passes Lemma S for some $d \mid l$. Then
$p \mid u_1 \cdots u_k$ for every counterexample $u$. The proof is Lemma D's,
with Lemma S covering the improper residues. Three points keep the symmetry
reduction valid:

- Lemma S's hypothesis is invariant under units $a$ of $\mathbb Z_N$, under signs
  and under permutations, because $d \mid a w_i \iff d \mid w_i$ and
  $\gcd(a w_i, d) = g_i$.
- Rescaling by an integer $a' \equiv a \pmod p$ with $\gcd(a', l) = 1$ preserves
  loneliness.
- It also preserves the $\gcd(u) = 1$ step in Lemma D's (a)-branch.

**Test** (`test_shift_lemma_sound_on_samples`). At $k = 7$, for shift-killed
improper level-8 lifts at $p = 17, 19, 23$, random integer preimages are all
lonely according to the exact checker `lonely.find_witness`.

## 3. The $k = 15$ cascade and kill tool (computed, tested)

`k15/gate15.c`, run as `gate15 k p LMAX`, does three things:

- it checks that each level-one row is witness-free;
- it runs the binary cascade, where $S_{2l}$ is the set of improper lifts of
  $S_l$ (digits $j_i \in \{0,1\}$, gcd clause at each level), up to
  $\mathrm{LMAX} \in \{16, 32\}$;
- it tests every member at levels $\ge 4$ with Lemma S for $d \in \{4,8,16,32\}$,
  $d \mid l$.

For $k = 15$ the kill level $16 = 2^4$ is reached by the cascade itself.

- **Validation** (`test_cascade_matches_bruteforce_k7`). At $k = 7$ ($k+1 = 8$),
  $p = 17, 19, 23, 29, 31$, for every level-one orbit: the per-row counts
  $n_2, n_4, n_8$ and the shift-unkilled counts $f_4, f_8$ equal a brute force
  over all $2^k$ lifts from Def. 2.1 (`sieve.Level.is_proper`).
- **The tight orbit.** $(1..15) \bmod 251$ gives $n_2, n_4, n_8, n_{16} = 1, 2, 4, 0$,
  as in `tight_orbit_k15.py`.
- **Speed.** 0.18 ms per level-one orbit at $p = 239$, measured on 20,000 orbits
  of a partial shard.

## 4. Pilot gate $p = 239$, $k = 15$: stopped, not closed

**Why 239.** It is the cheapest $\tau_{15} \ge 14$ prime with $p \ge 37$. Its
Knuth estimate is $2.57\cdot 10^{10}$ nodes, about 4 CPU-h. Primes $\le 31$
were left to the structure agent. After Allikvere's claim surfaced, it turned
out to be one of his preliminary $J$-empty gates.

**Run.** `covergen 15 239` with `LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, 16 shards,
3 workers, scratch `lr-gates/p239/`.

**Stopped** after about 8 min wall, with 0 of 16 shards finished and about
$1.0\cdot 10^6$ partial covers, when the coordinator retargeted the track to
$k = 17$.

- The projected run was 1.5–2 h wall on the shared machine (load 9–12).
- It is restartable: remove the `claim_*` directories, then start `worker.sh`
  three times.
- The partial covers are not a result.

**Comparison target (not done).** His `out15_239` tree in
`gates_239_271_283_293_307_audit.zip` (SHA-256 matches `SHA256SUMS.txt`):

- 9,552,452 irredundant rows;
- 8,272 km1 covers $\times$ 119 extensions;
- a cascade with 35,819 survivor rows, all dead by level 16, and 0 persistent
  orbits.

## 5. Allikvere's $k = 15$ campaign as data (certificate data)

**Downloads.** All 59 `evidence15_<p>_s0.tgz` and the five-prime audit zip are in
scratch `lr-gates/dl/`, kept for the certificate agent. Every SHA-256 equals
`SHA256SUMS.txt`, whose MD5 equals the Zenodo record's.

**The 59 summaries.** The `SUMMARY.json` files were read as data
(`k15/allikvere_k15_summaries.json`). Every one has:

- status GATE_CLOSED;
- claim type "J(K,p) empty";
- the precondition "0 covers on $\le 13$ classes";
- 0 persistent orbits.

His recorded CPU totals 49,255 CPU-h (generation plus precondition).

**Re-check cost (heuristic).** Our $k = 15$ Knuth tree (`k15/knuth_k15.txt`) is
$1.13$–$1.34\times$ his recorded irredundant node counts at the 59 gates (median
1.20). Level-one completeness at all 59 gates with our generator would take about
$8.1\cdot 10^4$ CPU-h, at $1.8\cdot 10^6$ nodes/s. The cheapest of his gates:

| gate | CPU-h |
| --- | --- |
| 239 (preliminary) | about 4 |
| 269 | about 12 |
| 281 | about 20 |

## 6. LRC(17) (18 runners): admissibility, cost, gate set

**Target.** The rank-4 agent gives $\sum_{p\in P}\ln p > 647.534682$. It
classifies rank 4 at $n = 17$, which pushes the binding rank to 5, with
$(17/2)\ln J_5 = 22.747$. Its label is proved, given the inputs in the bound
notes, §5.

The target was revised several times during this session:

| target | source |
| --- | --- |
| 670.28173 | plain flag bound, with the shape lemma $R_{17} < 0.4755$ machine-checked |
| 667.92857 | hyperplane lemma |
| 659.66535 | coarse relation-rank bound |
| **647.534682** | **rank-4 classification (current)** |

The tables below are computed at the current target, at the current target
minus 10, and at 659.66535.

Every target includes $-\ln \operatorname{lcm}(2..18) = -\ln 12252240 = -16.321$,
so the gate primes must satisfy $p > 18$.

### 6.1 Admissibility screen $\tau_{17}(p) \ge 16$ (computed)

Each prime was screened with `TAU_FROM=15 tau 17 p 15`, 60 s per prime, which
asks "is there a cover on at most 15 classes?". Data: `k17/tau_k17.txt`.

- **A cover on $\le 15$ classes was found (exact),** so $\tau_{17}(p) \le 15$
  and, by Lemma T, the prime is near-gcd only:
  - every prime $19 \le p \le 311$;
  - $p = 331$ and $379$.
- **The small-primes agent's exact values**
  (`computations/lonely-runner/smallp/results/tau17.txt`; exhaustive DFS)
  agree. Every prime 37–257 has $\tau_{17} \in [9, 14]$. For example
  $\tau_{17}(71) = 14$, $\tau_{17}(173) = 14$, $\tau_{17}(257) = 14$.
- **No small cover within 60 s:** every other prime $313 \le p \le 1103$ (120 primes, also 1583 and 1597). These are *candidates* only.
  Proving $\tau_{17}(p) \ge 16$ means exhausting the 15-class search. That took
  60 s for $\tau_{15}(239) \ge 14$, and Allikvere's $k = 15$ precondition took
  8 h at $p = 659$, so for $k = 17$ it is far beyond this session. A full
  level-one run would settle it anyway, since `covergen` prints every minimal
  cover with $\le k$ classes.

### 6.2 Cost per prime (heuristic)

**Data.** Knuth estimates of our tree at $k = 17$ (`LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`,
20,000 probes) for all 244 primes 19–1597 (`k17/knuth_k17.txt`). They agree within
a few percent with the cloud session's independent probes (`LRC_PRUNE=1`):

| $p$ | 307 | 401 | 503 | 601 | 701 | 797 |
| --- | --- | --- | --- | --- | --- | --- |
| $N_{17}$ (ours) | $1.12\cdot10^{13}$ | $6.52\cdot10^{13}$ | $1.24\cdot10^{14}$ | $7.65\cdot10^{14}$ | $1.29\cdot10^{15}$ | $6.60\cdot10^{15}$ |
| $N_{17}/N_{15}$ | 25 | 27 | 22 | 47 | 40 | 101 |

**Fit.** Over the candidate range $313 \le p \le 1597$,

$$N_{17}(p) \approx 2.9\cdot 10^{-4}\, p^{6.62} \quad (\text{scatter} \times 1.3).$$

The exponent is $6.90$ over 313–797, $6.11$ over 797–1597, and $7.41$ over
151–311.

**Rate.** Cost is $N_{17}/(1.8\cdot10^{6}\ \text{nodes/s})$, level one only. The
rate is from the exact $k = 14$, $p = 251$ run; the cloud session measures
$2$–$3\cdot10^6$ per core. The tau precondition, cascade and kill are not
included; at $k = 15$ they were a small fraction of Allikvere's total.

| band | primes | $\sum \ln p$ | CPU-h per gate (median) | band total, CPU-h |
| --- | --- | --- | --- | --- |
| 19–150 | 28 | 118.5 | $7\cdot10^{-4}$ | 12 |
| 151–311 | 29 | 156.8 | $1.0\cdot10^{2}$ | $8.2\cdot10^{3}$ |
| 313–401 | 15 | 88.2 | $2.7\cdot10^{3}$ | $6.9\cdot10^{4}$ |
| 409–503 | 17 | 104.0 | $1.9\cdot10^{4}$ | $3.3\cdot10^{5}$ |
| 509–601 | 14 | 88.6 | $8.0\cdot10^{4}$ | $1.2\cdot10^{6}$ |
| 607–701 | 16 | 103.6 | $1.9\cdot10^{5}$ | $3.1\cdot10^{6}$ |
| 709–797 | 13 | 86.1 | $5.8\cdot10^{5}$ | $7.6\cdot10^{6}$ |
| 809–907 | 16 | 107.9 | $1.3\cdot10^{6}$ | $2.2\cdot10^{7}$ |
| 911–1021 | 17 | 116.9 | $3.2\cdot10^{6}$ | $5.8\cdot10^{7}$ |
| 1031–1201 | 25 | 175.3 | $6.6\cdot10^{6}$ | $1.9\cdot10^{8}$ |

### 6.3 Cheapest admissible gate set (heuristic)

**Method.** `k17/gate_set.py` sorts the admissible primes by
$\text{cost}/\ln p$ and takes them until $\sum \ln p$ exceeds the target. This
order solves the fractional knapsack "minimise cost subject to
$\sum \ln p \ge T$" exactly, so the greedy set is optimal up to its last prime.
"Admissible" means not shown to have $\tau_{17} \le 15$.

**$J$-empty route.** Gates are the $\tau$-candidates $\ge 313$. All of them are
undetermined, not proved admissible.

| target | gates | primes | $\sum\ln p$ | level-one CPU-h, current generator | with `LRC_ORDERLY=1` and the step-15 build ($\div 5$–$6$) |
| --- | --- | --- | --- | --- | --- |
| **647.534682** | **101** | 313–1021 | 649.14 | $6.8\cdot10^{7}$ (7,700 CPU-years) | $1.1$–$1.4\cdot10^{7}$ (1,300–1,500 CPU-years) |
| 637.534682 (−10) | 100 | 313–1021 | 642.26 | $6.4\cdot10^{7}$ | $1.1$–$1.3\cdot10^{7}$ |
| 659.66535 | 103 | 313–1021 | 662.97 | $7.6\cdot10^{7}$ | $1.3$–$1.5\cdot10^{7}$ |

**Optimistic route.** This assumes every near-gcd prime closes, which is **not**
established; see below.

| target | gates | primes | level-one CPU-h | $\div 5$–$6$ |
| --- | --- | --- | --- | --- |
| 647.534682 | 118 | 19–719 | $4.4\cdot10^{6}$ | $0.73$–$0.87\cdot10^{6}$ |
| 637.534682 | 116 | 19–701 | $3.8\cdot10^{6}$ | $0.64$–$0.77\cdot10^{6}$ |

The gate list at 647.534682 ($J$-empty route) is every candidate prime from 313
to 983, plus 1021; `python3 k17/gate_set.py 17 647.534682` prints it.

About the $\div 5$–$6$ factor (heuristic):

- It comes from the cloud session. It ported Toner's orderly-root rule
  (`LRC_ORDERLY=1`, validated to give equal orbit sets).
- Its Knuth node reductions at $k = 17$ are 5.9×, 6.7× and 6.5× at $p = 307$,
  401 and 503. Time gains have tracked about half of the node gains.
- The step-15 build gives another 1.6×.
- The factor is measured at three primes only and is assumed to hold up to
  about 1021.

**Reading.**

- The $J$-empty route needs about 100 gates from 313 to about 1020, at roughly
  $10^{4}$ CPU-years. The top band, 900–1021, is about 75% of the cost.
- **The lever is the near-gcd primes.** The 57 primes 19–311 give
  $\sum \ln p \approx 275$ for about $8\cdot10^{3}$ CPU-h of level one.
  - If they could all be closed by divisibility (Lemma S with a 3-adic kill), the
    optimistic set to 647.53 would be 118 gates 19–719 at about
    $4.4\cdot10^{6}$ CPU-h, about 15× cheaper.
  - Against that, the small-primes agent found at $p = 71$ (381,083 level-one
    orbits) that the cascade blows up even with the shift lemma. So the
    smallest primes, $p \approx 4k$, almost certainly fail.
  - Which of 150–311 close is the open question. Their cascades, not their level
    one, will dominate.
- **No $J$-empty $k = 17$ gate is feasible here.** The cheapest candidate, 313,
  is about $2.7\cdot10^{3}$ CPU-h. Only near-gcd primes $\lesssim 150$ have level
  one under about 1 CPU-h. They need the $\times 3$/$\times 9$ kill: the structure
  agent showed that the class of $(1..17)$ stays improper at every dyadic level,
  because $18$ is not a power of $2$. That tool was deliberately not built here,
  to avoid duplication (coordinator).

### 6.4 Failed or limited routes (kept)

- **The $k = 15$ pilot at 239 was stopped** before any shard finished (§4).
- **The 60 s $\tau$ screen proves nothing at the candidate primes.** It is an
  upper-bound screen only.
- **`covergen.c`'s Knuth probe ignores the `LRC_PRUNE=2` locked-time rule.**
  The estimates therefore describe a slightly larger tree. At $k = 14$,
  $p = 251$, this made no measurable difference ($1.34$ vs $1.35\cdot10^{10}$).

## 7. Files

- `computations/lonely-runner/k15/tau.c`: the covering number $\tau_k(p)$
  (exhaustive, with screening mode `TAU_FROM`).
- `computations/lonely-runner/k15/gate15.c`: the binary cascade, the kill and the
  Lemma S test, for $k+1$ a power of 2.
- `computations/lonely-runner/k15/test_gate15.py`: 3 tests (brute-force cascade
  at $k = 7$, soundness of Lemma S on samples, $\tau$ against brute force). All
  pass.
- `computations/lonely-runner/k15/knuth_k15.txt`: $k = 15$ Knuth table, primes
  17–797.
- `computations/lonely-runner/k15/allikvere_k15_summaries.json`: his 59
  `SUMMARY.json` files, as data.
- `computations/lonely-runner/k17/knuth_k17.txt` and `tau_k17.txt`: $k = 17$
  Knuth table (19–1597) and $\tau$ screen (19–1103).
- `computations/lonely-runner/k17/gate_set.py`: gate selection.

**Suggested `covergen.c` change, not made.** Let the Knuth probe also apply the
`LRC_PRUNE=2` locked-time rule, so that the estimates describe exactly the tree
that is run.
