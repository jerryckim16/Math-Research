# Small primes as gates: the shift lemma, covering numbers, an audit of Allikvere's preliminary primes, and $k = 17$

Track notes from the small-primes agent (2026-11-25). Companion code: `computations/lonely-runner/smallp/`.
Labels follow the repository README: *proved*, *computed* (exact, our code), *certificate-checked*, *heuristic*.

Notation follows `problems/lonely-runner.md`:

- $k$ speeds, threshold $1/(k+1)$, a prime $p > k+1$, a level $l$ with $p \nmid l$;
- folded classes $1, \dots, h$ with $h = (p-1)/2$;
- class $v$ covers time $a$ iff $(k+1)\, d_p(av) < p$. Each class covers exactly $m = \lfloor (p-1)/(k+1) \rfloor$ times;
- $\tau_k(p)$ is the least number of classes covering all $h$ times (Allikvere's covering number);
- "Lemma 2.2(ii)" is the prime-divisibility criterion of arXiv:2609.02604v2, restated (restricted to primitive vectors) as Lemma 2.1 of the sixteen-runner manuscript.

Sources read:

- J. Allikvere, arXiv:2609.02604v2. LaTeX source from arxiv.org/e-print: §§2 and 4, Lemma 3.12 (`lem:neargcd`).
- J. Allikvere, "Sixteen lonely runners", Zenodo 10.5281/zenodo.23304361 (Oct 2026, unrefereed): manuscript source `paper.tex` and `appendices.tex`, and the data file `gates_weighted_shift_audit.zip` (MD5 443abc5398d9627aad9e415876afcffb, equal to Zenodo's).
- None of his programs was run. His files were read as data only.

## 1. Small covering number forces $J(k,p) \neq \varnothing$ (proved)

**Lemma N.** Let $p > k+1$ be prime and suppose some set $C$ of $s \le k-2$ classes covers all folded times. Then $J(k,p) \neq \varnothing$.

*Proof.*

1. Fix a level $l$ with $p \nmid l$. By CRT choose $w \in \mathbb{Z}_{lp}^k$ with:
   - $w_i \equiv c_i \pmod p$ and $w_i \equiv 0 \pmod l$ for $i \le s$, where $C = \{c_1, \dots, c_s\}$;
   - $w_i \equiv 1 \pmod l$ and $p \nmid w_i$ for the remaining $k - s \ge 2$ coordinates.
2. Let $t = n/(lp)$ with $0 < n < lp$. For $i \le s$ write $w_i = l w_i'$ with $w_i' \equiv l^{-1} c_i \pmod p$. Then $t w_i = n w_i'/p$, so
   $$\lVert t w_i \rVert = \lVert a c_i / p \rVert, \qquad a \equiv n\, l^{-1} \pmod p.$$
   - If $p \nmid n$, then $a \not\equiv 0$ and $C$ covers $a$, so some $i \le s$ has $\lVert t w_i \rVert < 1/(k+1)$.
   - If $p \mid n$, then $t w_i \in \mathbb{Z}$.

   So $w$ has no witness at level $l$.
3. The gcd clause fails: for each $i$, a coordinate $\equiv 1 \pmod l$ remains among the others, so $\gcd(l, w_j : j \ne i) = 1$.
4. So $w$ is improper at every level, and its reduction mod $p$ lies in $J(k,p)$. ∎

**Consequence.** $J(k,p) = \varnothing$ needs $\tau_k(p) \ge k-1$. This is exactly the dividing line in Allikvere's tables:

- LRC(14): the "J empty" gates have $\tau \ge 13$; the gates with $\tau \le 12$ use Lemma 3.12.
- LRC(15): the divisibility-only preliminary primes have $\tau_{15} \le 13$.

A prime with $\tau_k(p) \le k-2$ can only be a *divisibility* gate, through Lemma 2.2(ii) and a shift lemma. The vectors of Lemma N have the near-gcd shape: $k - e$ coordinates divisible by every prime of $l$, and $e = k - s \ge 2$ exceptions.

## 2. The weighted shift lemma (proved; equal to Allikvere's Lemma "A weighted shift")

**Lemma S.** Let $k \ge 3$ and assume LRC($m$) for all $m \le k-2$. Let $u \in (\mathbb{Z}\setminus\{0\})^k$ and $d \ge 2$. Put
$$E = \{ i : d \nmid u_i \}, \qquad g_i = \gcd(u_i, d), \qquad c(g) = g \left\lceil \frac{2d}{(k+1)g} \right\rceil.$$
If $\lvert E \rvert \ge 2$ and $\sum_{i \in E} c(g_i) < d$, then some real $t$ has $\lVert t u_i \rVert \ge 1/(k+1)$ for all $i$.

*Proof.*

1. **The block $D$.** Let $D = [k] \setminus E$. It has at most $k-2$ coordinates, taking $m \le k-2$ distinct absolute values. LRC($m$) gives $t_0$ with
   $$\lVert t_0 u_j \rVert \ge \frac{1}{m+1} > \frac{1}{k+1} \qquad (j \in D).$$
   If $D = \varnothing$, take any $t_0$.
2. **The shifts.** Put $t_q = t_0 + q/d$ for $0 \le q < d$. For $j \in D$, $d \mid u_j$, so $t_q u_j \equiv t_0 u_j \pmod 1$.
3. **One exception.** Fix $i \in E$ with $g = g_i$. Then $q u_i/d = q (u_i/g)/(d/g)$, and $u_i/g$ is a unit mod $d/g$. So as $q$ runs over $\mathbb{Z}_d$, $t_q u_i$ runs over the $(d/g)$-point coset $t_0 u_i + (g/d)\mathbb{Z}$, each point exactly $g$ times.
4. **Forbidden shifts.** The bad set $\{ y : \lVert y \rVert < 1/(k+1) \}$ is an open arc of length $2/(k+1)$. An open arc whose length is $L$ grid spacings holds at most $\lceil L \rceil$ points of the grid. Here $L = 2(d/g)/(k+1)$, so exception $i$ forbids at most $c(g)$ values of $q$.
5. **Conclusion.** Since $\sum c(g_i) < d$, some $q$ is forbidden by no exception, and $t_q$ is a witness. ∎

**Notes on Lemma S.**

- **Prime $d$.** Then $g_i = 1$ and this is Allikvere's Lemma 3.12 (arXiv:2609.02604v2; $k = 14$, $d \in \{3, 5\}$).
- **$k = 15$.** Here $c(g) = g \lceil d/(8g) \rceil$. This is verbatim the sixteen-runner Lemma "A weighted shift", whose hypothesis is LRC($m$), $m \le 13$. Found here independently (checkpoint 1) and then located in his manuscript.
- **Use in Lemma 2.2(ii).** If $d \mid l$, then $E$ and the $g_i$ depend only on $u \bmod lp$, so the conclusion holds on the whole residue class.
- **Extended properness is inherited by lifts.** Call a level-$l$ lift *extended-proper* if it has a grid witness, or meets the gcd clause, or meets Lemma S for some $d \mid l$. Each of the three persists to multiples of the level: the class mod $clp$ lies inside the class mod $lp$. So the cascade may discard extended-proper lifts at *every* level. An empty retained set at level $L$ gives Lemma 2.2(ii) at level $L$.
- **Units and signs.** Allikvere's Remark 2.3 uses $b \equiv a^{-1} \pmod p$ and $b \equiv 1 \pmod l$. This fixes residues mod $l$, hence $E$ and the $g_i$. Sign changes do not change $E$, the $g_i$ or loneliness. So one orbit representative suffices.
- **Machine check** (`smallp/shift_lemma_check.py`, exact Fractions):
  - the arc count $\max_x \#\{ j : \lVert x + j/n \rVert < 1/16 \} = \lceil 2n/16 \rceil$ for all $n \le 256$, with equality;
  - the multiplicity claim of step 3 for all $d \le 128$ and all $u \bmod d$;
  - a negative control: with floor in place of ceiling, the bound fails.

**Which $d$ help.** The first table is for $k = 15$, with $c(g) = g \lceil d/(8g) \rceil$:

| $d$ | costs $c(g)$ | most exceptions with $g = 1$ |
| --- | --- | --- |
| 2 | $c(1)=1$ | 1 (the gcd clause) |
| 3 | $c(1)=1$ | 2 |
| 4 | $c(1)=1,\ c(2)=2$ | 3 |
| 8 | $c(1)=1,\ c(2)=2,\ c(4)=4$ | **7** |
| 16 | $c(1)=c(2)=2,\ c(4)=4,\ c(8)=8$ | 7 |
| 32 | $c(1)=c(2)=c(4)=4,\ c(8)=8,\ c(16)=16$ | 7 |

- The limit is $e < (k+1)/2 = 8$. The powers $d = 8, 16, 32$ reach it and divide the binary levels themselves, so no odd lift is needed.
- Allikvere's certificates use only $d = 4$ (at most 3 odd exceptions), followed by an exact level-8 test of the residual lifts.

The second table is for $k = 17$, with $c(g) = g \lceil d/(9g) \rceil$, computed exactly:

| $d$ | costs $c(g)$ | most exceptions with $g = 1$ |
| --- | --- | --- |
| 3 | $c(1)=1$ | 2 |
| 4 | $c(1)=1,\ c(2)=2$ | 3 |
| 6 | $c(1)=1,\ c(2)=2,\ c(3)=3$ | 5 |
| 8 | $c(1)=1,\ c(2)=2,\ c(4)=4$ | 7 |
| 9 | $c(1)=1,\ c(3)=3$ | **8** |
| 16 | $c(1)=c(2)=2,\ c(4)=4,\ c(8)=8$ | 7 |
| 18 | $c(1)=c(2)=2,\ c(3)=3,\ c(6)=6,\ c(9)=9$ | 8 |
| 27 | $c(1)=c(3)=3,\ c(9)=9$ | 8 |
| 36 | $c(1)=4, \dots$ | 8 |

For $k = 17$ the limit is $e \le 8$, reached at $d = 9, 18, 27, 36$. It needs LRC($m$) for $m \le 15$, i.e. up to 16 runners, which is Allikvere's unrefereed claim.

## 3. Covering numbers (computed)

`smallp/mincover.c` (exact) runs an exhaustive DFS for a cover by at most $s$ classes containing class 1. This loses nothing by unit symmetry.

- It branches on the uncovered time with the fewest allowed coverers, excluding earlier siblings.
- It cuts when the $s - \lvert L \rvert$ largest gains sum to less than $\lvert U \rvert$.
- $\tau$ is the least $s$ for which a cover is found. That cover is re-verified.
- "None for $s - 1$" is exhaustive by the branching argument in the header of `covergen.c`. It is not an external certificate.
- Cross-checked against a SAT formulation (`smallp/tau.py`, pysat/CaDiCaL) at $k = 14$, $p = 83$–$113$: same values.

Results are in `smallp/results/tau14.txt`, `tau15.txt` and `tau17.txt`.

**$k = 14$** (consistency check with arXiv:2609.02604v2, Table `tab:gates14`):

| $p$ | 83 | 89 | 97 | 101 | 103 | 107 | 109 | 113 | 127 | 131 | 137 | 139 | 149 | 151 | 157–233 | 239 | 241 | 251 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\tau_{14}$ | 12 | 12 | 10 | 11 | 10 | 11 | 10 | 11 | 11 | 11 | 11 | 12 | 12 | 11 | 12 each | 13 | 12 | 13 |

- Every one of his near-gcd gates computed here has $\tau \le 12$ (all have 12, except 131 with 11).
- Every one of his J-empty gates computed here (239, 251) has $\tau = 13$.
- Primes from 257 on hit the 120 s timeout and were not computed.

**$k = 15$:**

| $p$ | 37 | 41 | 43 | 47 | 53 | 59 | 61 | 67 | 71 | 73 | 79 | 83 | 89 | 97 | 101 | 103 | 107 | 109 | 113 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\tau_{15}$ | 9 | 10 | 12 | 12 | 11 | 12 | 12 | 10 | 11 | 12 | 11 | 12 | 12 | 10 | 11 | 10 | 11 | 10 | 11 |

| $p$ | 127 | 131 | 137 | 139 | 149 | 151 | 157 | 163 | 167 | 173 | 179 | 181 | 191 | 193 | 197 | 199 | 211 | 223 | 227 | 229 | 233 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\tau_{15}$ | 12 | 11 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 13 | 13 | 12 | 12 | 12 | 13 | 13 | 12 | 12 | 13 |

- By Lemma N, every prime from 37 to 233 has $J(15,p) \neq \varnothing$, so each is at best a divisibility gate.
- This agrees with Allikvere: 191, 211, 223 and 233 are divisibility-only in his Proposition "Previously verified primes".
- $\tau_{15}(p) \ge \lceil h/m \rceil \ge 8$ always. So the vectors of Lemma N have at most 7 exceptions, and Lemma S with $d = 8$ or $16$ always closes them.
- **Not computed:** $\tau_{15}$ at 239–307. His J-empty claims there need $\tau_{15} \ge 14$.

**$k = 17$** (for the 18-runner target):

| $p$ | 37 | 41 | 43 | 47 | 53 | 59 | 61 | 67 | 71 | 73 | 79 | 83 | 89 | 97 | 101 | 103 | 107 | 109 | 113 | 127 | 131 | 137 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\tau_{17}$ | 9 | 10 | 12 | 12 | 13 | 12 | 12 | 12 | 14 | 12 | 11 | 13 | 13 | 12 | 12 | 13 | 12 | 10 | 11 | 12 | 12 | 13 |

| $p$ | 139 | 149 | 151 | 157 | 163 | 167 | 173 | 179 | 181 | 191 | 193 | 197 | 199 | 211 | 223 | 227 | 229 | 233 | 239 | 241 | 257 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\tau_{17}$ | 12 | 12 | 12 | 13 | 13 | 13 | 14 | 14 | 13 | 13 | 13 | 14 | 13 | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 14 |

- **Not determined** (120 s per prime): 251, 263, 269, 271, 277, 281, 283, 293.
- Every determined value is at most $15 = k - 2$. So by Lemma N, $J(17,p) \neq \varnothing$ for every listed prime: **none of them can be a J-empty gate for 18 runners**, and each is at best a divisibility gate via Lemma S.
- $\tau_{17}(71) = 14$ is unusually large for its size ($h = 35$, $m = 3$, so the bound $\lceil h/m \rceil$ is 12).

## 4. Audit of Allikvere's $k = 15$ preliminary primes (certificate-checked, partial)

His Proposition "Previously verified primes" lists 16 preliminary primes:

- **Divisibility-only:** 191, 211, 223, 233, 241, 251, 257, 263, 277.
  - Seven of them (191, 223, 233, 241, 251, 257, 277) use the composition "weighted shift with $d = 4$, then an exact level-8 test", recorded in `small_prime_pilot_20260910`.
  - 211 and 263 use separate compositions, not examined here.
- **J-empty:** 239, 271, 283, 293, 307.
- **29 and 31:** these belong to the structure agent.

**Composition (checked by reading).** For each level-one orbit $r$:

- either the plain binary cascade empties by level 32 (eventually proper);
- or $r$ is "persistent", and at level 8 every lift is proper or covered by Lemma S.

The level-8 step works as follows. A level-8 lift reduces to a level-4 lift.

- If the level-4 lift is proper, so is the level-8 lift.
- If the level-4 lift is closed by Lemma S with $d = 4$, so is every level-8 lift, since $4 \mid 8$.
- Otherwise the level-4 lift is "residual", and every one of its level-8 lifts must have a grid witness.

This is a valid instance of Lemma 2.2(ii) at level 8.

**Re-derived with our code** (`smallp/terminal15.py`; results in `smallp/results/terminal_k15_allikvere.jsonl`). His persistent representatives were read from `SUMMARY.json`. Every count below is recomputed from Def. 2.1 with `liftfree.c`, our gcd test and our Lemma S test:

| $p$ | bases | level-2 improper | level-4 witness-free | closed by Lemma S, $d=4$ | residual | witness-free level-8 lifts of residuals |
| --- | --- | --- | --- | --- | --- | --- |
| 191 | 90,248 | 132,675 | 471,470 | 470,880 | 590 | 0 |
| 223 | 31,080 | 41,267 | 155,082 | 155,000 | 82 | 0 |
| 251 | 15,750 | 19,861 | 76,728 | 76,728 | 0 | 0 |

- **Every entry equals his `terminal_<p>.out`.**
- Every representative lies in $I(15,p,1)$.
- Our stricter variant, which also applies the gcd clause and Lemma S with $d \in \{4, 8\}$ at level 8, also leaves 0.
- **$p = 191$, covers on at most 13 classes:**
  - Our enumeration (`mincover.c`, enum mode) finds 260 minimal covers containing class 1. All have 13 classes, and they form 20 unit orbits.
  - His `km1low_191.txt` lists 260 rows. Each is a 14-multiset (a 13-cover with one class doubled), and their supports form the same 20 orbits.
  - So $\tau_{15}(191) = 13$ (`smallp/results/covers13_k15_p191.txt`).

**Not checked here** (the expensive parts):

- level-one completeness (12.1M irredundant rows at 191);
- that every non-persistent row dies in the plain cascade (16.3M rows; about 14 CPU-h of his cascade at 191);
- the gates 211 and 263, and the J-empty gates.

## 5. Lemma S at $d = 8, 16, 32$ and the "$p = 149$ regime" (heuristic, 2 samples)

His pilot abandoned $p = 149$ and fourteen other $\tau_{15} \le 12$ primes. Its record:

- every sampled row was persistent;
- fibres grew 4–8× per level;
- the cascade was projected at about 35 CPU-years.

What we did:

- **His sample bases** (`pilot149_evidence.tgz`, `t3.out`) are the 12-class cover $\{1,2,3,11,13,25,28,48,59,61,63,67\}$ (checked: it covers all 74 times) plus the classes $1, 1, x$.
- **The plain cascade** (`smallp/cascade15x.py`, `smallp/xcascade.py`) reproduces his fibre sizes exactly: $x = 1$ gives $24, 344, 1888, 8576$ at levels $2, 4, 8, 16$, and $x = 4$ gives $21, 204, 816, 6336$.
- **With Lemma S** for $d \in \{4, 8, 16, 32, 64\}$, $d \mid l$, applied at every level, the fibres are $24, 288, 768, 0$ (empty at level 16) and $21, 156, 0$ (empty at level 8).
- **With $d = 4$ alone** they kept growing; that run was stopped after 2 min.

This is two bases only, so it is *heuristic*. But it shows that the $d = 8, 16$ form of Lemma S removes the mechanism that made the $\tau \le 12$ primes infeasible. A random sample of level-one rows at $p = 139$–$199$ through the extended cascade is still to be done.

## 6. $k = 17$ (18 runners): what was measured

- **Level structure.** $(1, \dots, 17)$ is tight, so it has no witness unless $18 \mid l$. Every gate chain must therefore contain $2 \cdot 3 \cdot 3$. We use the chain $2, 3, 3, 2$ (levels 2, 6, 18, 36). Lemma S at $d = 9$ or $18$ is available at levels 18 and 36.
- **Tight orbit** (`smallp/xcascade.py 17 tight`, Lemma S on). At $p = 101$ and $103$ it dies at level 18, with retained sizes $52, 2, 0$ and $56, 2, 0$. At $p = 101$ it dies at level 18 even without Lemma S. The run over 97–300 is in `smallp/results/tight17.jsonl`, to the extent it finished.
- **Level one at small $p$** (`covergen.c` with `LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, then `canon.c expand`):
  - $p = 37$: 39 minimal covers, giving 853,467 orbits;
  - $p = 71$: 52,786 covers (30, 935, 15,222 and 36,599 of sizes 14–17), giving 381,083 orbits.
- **Cascade at $p = 71$** (failed route, measured; `smallp/xbatch.py`). On 100 sampled orbits, with Lemma S on:
  - level 2: all 100 still open, 31,238 retained lifts;
  - level 4: 99 of 100 open, 73,888 retained lifts.

  This is the blow-up regime: at $p \approx 4k$ the time grid is far too coarse. At $p = 37$, 2,000 sampled orbits did not finish one stage in 10 min. Not pursued.
- **Consequence for gate selection** (not cost): every prime below 258 with $\tau_{17}$ computed has $\tau_{17} \le 14 \le k - 2$, so none is a J-empty gate. Whether the mid-range primes (about 150–300) close as divisibility gates under Lemma S is open. The $k = 15$ experience (Allikvere's seven primes, and §5) suggests they may, once $d = 8, 9, 16, 18$ are used at every level.

## 7. Failed or abandoned routes (kept)

- **Lemma 3.12 with $d = 2$ at $k = 15$** gives nothing: $c = \lceil 4/16 \rceil = 1$, so $e < 2$, which is the gcd clause.
- **Odd levels at $k = 15$.** The route via $l = 16 \cdot 3$ ($d = 3$) or $16 \cdot 5$ ($d = 5$), which mimics Allikvere's level-15 kill, is dominated by $d = 8, 16$, which need no odd lift.
- **SAT for $\tau$** (`tau.py`) is correct but slow on the UNSAT side above $p \approx 113$. The DFS `mincover.c` is far faster.
- **$k = 17$ at $p = 37$ and $71$**: fibre blow-up (§6).

## Next steps

1. Run the extended cascade (Lemma S at all $d \mid l$) on random level-one samples at $k = 15$, $p = 139$–$199$, and at $k = 17$, $p \approx 150$–$250$. This decides whether these primes become usable divisibility gates.
2. Compute $\tau_{15}$ at 239–307 and $\tau_{17}$ at 251–293 with a longer timeout. The first is needed to confirm Allikvere's J-empty preliminary primes against Lemma N.
3. Audit gates 211 and 263 (`gate_211_audit.zip`, 37.6 MB, not downloaded).
4. Run the terminal re-derivation at 233, 241, 257 and 277. It is cheap: 241 and 257 have about 0.5M orbits each, roughly 1 h each on one core.
