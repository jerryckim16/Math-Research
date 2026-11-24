# Lonely Runner Conjecture

**Area:** Diophantine approximation / combinatorics
**Status:** in progress. Done so far:
- The prime-gate framework is reproduced end to end for LRC(3)–LRC(9) (4–10 runners), conditional on one cited bound (B_k).
- All 71 of Allikvere's 15-runner (LRC(14)) gate certificates are independently re-checked, with no discrepancy found. Stored rows were checked in full at every gate; the cascade and kill in full at 52 gates and sampled at 19; level-one completeness at 2 gates. See "Independent re-check summary". His 14-runner terminal kills are re-checked at 66 of 111 gates (in progress).
- The cost of the next open case (16 runners) is estimated from measurements.

**Started:** 2026-11-23 (literature upgraded to primary texts the same day, step 2)
**ProofAtlas:** rank 477

## Statement

Write ‖x‖ for the distance from x to the nearest integer.

**Conjecture (Wills 1967; Cusick 1973).** Let n ≥ 1 and let v_1, …, v_n be
positive integers. Then there is a real t with

  ‖v_i t‖ ≥ 1/(n+1) for all i = 1, …, n.

- **Interpretation.** There are n+1 runners on a circular track of length 1, with one runner at rest. At some time t every moving runner is at distance at least 1/(n+1) from the runner at rest.
- **Original form.** Runners have distinct real speeds and *each* runner is lonely at some time. That form reduces to positive integer speeds with one runner at rest: Wills 1968, Bohman–Holzman–Kleitman 2001 and Henze–Malikiosis, as recalled in the introductions of arXiv:2509.14111 and arXiv:2511.22427.
- **Repeated speeds are harmless.** With k' < n distinct values, 1/(k'+1) > 1/(n+1).

Following the recent literature, write **LRC(k)** for the statement with
k = n speeds. LRC(k) is "the conjecture for k+1 runners".

The bound 1/(n+1) cannot be improved. Speeds (1, 2, …, n) attain it exactly
(re-checked below for n ≤ 10).

**Next open case: LRC(15), i.e. 16 runners.** Every 15-tuple of positive
integers has a t with all ‖v_i t‖ ≥ 1/16.

- This assumes Allikvere's computer-assisted preprint for 14 and 15 runners is correct. It has not been independently re-implemented in full; see the spot check below.
- Without that preprint, the first case without a located claim is still 16 runners.
- The first case without a peer-reviewed proof is 11 runners.

## Known results

Labels:

- **[read]**: we read the primary text, from its arXiv LaTeX source unless stated otherwise.
- **[abstract]**: seen only via abstracts, search snippets or secondary pages.

Literature checked on 2026-11-23. In step 2, arxiv.org and zenodo.org became reachable and the four main computer-assisted papers were read.

| runners | k | result | source | how checked |
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
| 16 | 15 | **open** | — | |

Details from the primary texts:

- **Rosenfeld, 8 runners (k = 7).**
  - Gate primes S = {31, 37, …, 163}, i.e. all 27 primes from 31 to 163.
  - Bound: ∏ ≤ (C(8,2)⁶/7)⁷ < 7.4·10⁵⁴ (Corollary 3).
  - Forced divisor: lcm(2..8) (his Lemma 4).
  - His level is l = k+1 directly, i.e. times in (1/((k+1)p))Z.
  - Table 1 there also does 4–7 runners:
    - k = 3: {7, 11, 13}
    - k = 4: {17, …, 37}
    - k = 5: {23, …, 71}
    - k = 6: {13, 19, 31, …, 103}
- **Trakulthongchai, 9 and 10 runners.**
  - S_8 = all 39 primes from 47 to 241 (∏ > 10⁸²; C_8 < 10⁸⁰).
  - S_9 = all 47 primes from 137 to 401 (∏ > 10¹¹²; C_9 < 10¹¹¹).
  - For k = 8, every p with 11 ≤ p ≤ 43 failed (non-empty I(8,9,p)).
  - Run times: 15 min (k = 8) and under 23 h (k = 9) on a 14-core M3 Max.
- **Rosenfeld, 9 runners (arXiv:2512.01912).** Proves LRC(8) independently, using a sharpened gcd lemma for k = 8 and prime powers (64, 81, 25, 121, 169, …) as moduli.
- **Sungkawichai–Trakulthongchai, 11–13 runners.** Gate tables and the polynomial Prop. 1.2 are as summarised in step 1. They report k = 10 in 45 min on a 10-core M4.
- **Allikvere, 14 and 15 runners.**
  - LRC(13), first proof: MSS bound ln B_13 < 670.34974, with 111 gate primes, Σ ln p = 681.5292.
  - LRC(13), second proof: his flag bound (below), ln < 341.031991, with 61 primes, Σ = 353.7726.
  - LRC(14):
    - Flag bound ln(v_1⋯v_14) < 414.779365.
    - Minus ln lcm(2..15) = ln 360360 = 12.79485, giving a target of 401.984506.
    - 71 gates (89, 131–241 selected, and every prime 239–569), Σ ln p = 408.8233.
    - 19 gates (τ(p) ≤ 12) also use the "few-exception shift" Lemma 3.12 through Lemma 2.2(ii). Those gates prove divisibility, not J(14,p) = ∅.
  - Total 2,137 CPU-hours. Our sum of the generation and kill CPU in `gates.json` is 2,028.6 h; the cascade wall time is not included.
  - He states: "The full computation has not been independently reimplemented or formally verified."

### Results for general n

- The trivial bound is 1/(2n).
- Tao (2018) proved 1/(2n) + c·log n/(n²(log log n)²).
- Bedert (arXiv:2511.16636, 2025) proved 1/(2n) + 1/n^{5/3+o(1)}. Cited in the [read] intro of arXiv:2604.23906.
- Hu–Jing, "Near optimal gap in the lonely runner conjecture", arXiv:2610.23790 (Oct 2026), reportedly proves (1+c)/(2n). [abstract]: seen via MathWorld only, not read.
- None of these settles any finite case.

### The finite reduction (exact hypotheses, from the read texts)

- **MSS Theorem A** (Malikiosis–Santos–Schymura, *Forum Math. Sigma* 13 (2025) e164, arXiv:2411.06903), quoted as stated in arXiv:2509.14111:
  - *If LRC holds for k [speeds], it holds for k+1 for every tuple with gcd(v) = 1 and Σ_{S⊆[k]} gcd({v_i : i∈S}) > C(k+1,2)^{k−1}.*
  - We have not read the MSS paper itself. Note that arXiv:2509.14111 indexes by k with k+1 runners; Allikvere restates it as Σv_i < C(n+1,2)^{n−1} for n speeds.
- **Rosenfeld's Corollary 3** (by AM–GM). A gcd-1 counterexample to LRC(k), with LRC(k−1) assumed, has

  u_1⋯u_k < B_k := (C(k+1,2)^{k−1}/k)^k.

  Values of ln B_k:

  | k | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | ln B_k | 7.45 | 22.09 | 46.11 | 80.59 | 126.33 | 184.04 | 254.3 | 337.6 | 434.5 | 545.3 | 670.35 | 810.07 | 964.75 |

- **Forced divisor** (Rosenfeld, Lemma 4). For a counterexample, lcm(2, …, k+1) | u_1⋯u_k. Proof: t = 1/d is a witness unless d divides some u_i.
- **Allikvere's flag bound** (arXiv:2609.02604v2, Thm 3.8; due to Allikvere, building on Giri–Kravitz's projected lattice).
  - Setting: assume LRC(m) for all m < n, and let v be a primitive positive counterexample to LRC(n).
  - Constants: B_r = (2r/((n+1)(n+1−r)))², c_i = B_i − B_{i−1}, and K_n = ∏_{i<n} c_i. The hypothesis is c_{i+1}/c_i > 4/3.
  - Conclusion: v_1⋯v_n < (A_n r_n/n)^n with A_n = K_n^{−1/2}, whenever the "shape factor" satisfies R_n < r_n on the simplex.
  - He proves r_13 = 101/200 and r_14 = 1/2 (Lemma 3.7). That gives ln bounds 341.031991 (n = 13) and 414.779365 (n = 14).
  - **We re-derived K_13, K_14, the ratio minima 1175/688 and 847/513, and both log bounds exactly** (`flag_bound.py`, tested).
  - **n = 15 (our computation; not in the paper):**
    - The ratio minimum is 3751/2349 > 4/3, exactly.
    - The paper's one-variable shape family gives min R_15 ≈ 0.48796 numerically.
    - If a shape lemma r_15 = 49/100 were proved, then ln(v_1⋯v_15) < 496.727, and the gate target after ln lcm(2..16) = ln 720720 would be 483.239. This agrees with the figure in the (unreviewed) munim lonely-runner-16 repository.
    - **The shape lemma for n = 15 is unproved here.** This target is heuristic until it is.
- **Prime gates (Sungkawichai–Trakulthongchai, Def. 2.1).** Fix k ≥ 2, a prime p and l ≥ 1. Put N = lp and Z_{p,l} = {x ∈ Z_N : p ∤ x}. Then w ∈ Z_{p,l}^k is *(k,p,l)-proper* if either
  - (a) gcd(l, w_1, …, ŵ_i, …, w_k) > 1 for some i, or
  - (b) some t ∈ (1/N)Z has ‖t w_i‖ ≥ 1/(k+1) for all i.

  I(k,p,l) is the set of improper tuples. J(k,p) is the set of v ∈ Z_{p,1}^k that are not eventually proper.
- **Lemma D** (Trakulthongchai, Lemma 5; Allikvere, Lemma 2.2(i)). Let k ≥ 3, assume LRC(k−1), and suppose J(k,p) = ∅. Then p | u_1⋯u_k for every counterexample u.
  - Allikvere's Lemma 2.2(ii) relaxes this: improper lifts are allowed if every integer tuple in their residue class is lonely.
- **Lemma E** (Sungkawichai–Trakulthongchai, Lemma 2.4). J(k,p) = ∅ iff I(k,p,l) = ∅ for some l.
- **Proposition V** (Sungkawichai–Trakulthongchai, Prop. 2.6). Assume LRC(k−1) and J(k,p) = ∅ for all p ∈ P. If ∏_P p ≥ B_k, then LRC(k) holds. With the forced divisor or the flag bound, the target changes accordingly.
- **Tight tuples force l.** (1, …, k) is lonely exactly at t = s/(k+1) with gcd(s, k+1) = 1. So for p > k+1, I(k,p,l) = ∅ requires (k+1) | l.

Other relevant work:

- Blanco–Criado–Santos, arXiv:2603.24784, give counterexamples to the *shifted* LRC from n = 5. This does not affect the unshifted conjecture. Allikvere says their reformulation gives the same bound as MSS.
- Giri–Kravitz, *Math. Proc. Cambridge* 180 (2026), arXiv:2304.01462, prove a weaker finite-checking bound.
- Goddyn–Wong 2006 study tight tuples.
- Zhang, arXiv:2608.13599, studies tight one-entry modifications. [abstract]

## Elementary lemmas used by our reproduction (proofs)

**Witness transfer.** If u ≡ w (mod N) and t = m/N, then u_i t − w_i t ∈ Z, so ‖u_i t‖ = ‖w_i t‖.

**Lemma D (proof).** Take a counterexample u. We may assume gcd(u) = 1 (replace t by t·g). Suppose that p ∤ u_i for every i, and let w = u mod lp ∈ Z_{p,l}^k. Since I(k,p,l) = ∅, w is proper.

- If (b) holds, witness transfer makes u lonely, which is a contradiction.
- If (a) holds, let d = gcd(l, w_j : j ≠ i) > 1.
  - Then d | u_j for j ≠ i, since d | l | N.
  - Because gcd(u) = 1, gcd(d, u_i) = 1.
  - LRC(k−1), applied to (u_j)_{j≠i} (repeats allowed), gives t_0 with ‖u_j t_0‖ ≥ 1/k for j ≠ i.
  - The times t_0 + r/d leave every u_j t_0 unchanged mod 1, and move u_i t_0 through a full coset x + (1/d)Z.
  - One of these points has ‖·‖ ≥ 1/2 − 1/(2d) ≥ 1/4 ≥ 1/(k+1), using k ≥ 3.
  - So u is lonely, which is again a contradiction. ∎

This is the same argument as Rosenfeld's Lemma 5 in arXiv:2509.14111 and Allikvere's Lemma 2.2.

**F1 (improperness projects).** Let w be improper at level clp, and let w′ = w mod lp. A witness for w′ would be a witness for w, and a gcd divisor d | l for w′ divides cl and the corresponding w_j. So w′ is improper. Consequently, lifting and projecting chains keep a preimage of every v ∈ J(k,p) (Prop. 3.1 of arXiv:2604.23906). If the final stage is empty, J(k,p) = ∅.

**F2 (symmetry).** Properness is invariant under permutations, sign changes, and units of Z_N. Z_{cN}^* → Z_N^* is onto, so one orbit representative suffices. At level 1, every orbit contains (1, a_2 ≤ … ≤ a_k) with 1 ≤ a_i ≤ (p−1)/2.

**Lemma E (proof of ⇒).** Let l = lcm over v of a level l_v at which v has no improper lift. Properness transfers up to level lp. ∎

**Minimal-cover generation** (`covergen.c`; our proof, same idea as Allikvere §4.1).

- The k-multiset M lies in I(k,p,1) iff its folded classes *cover* every folded time class 1..(p−1)/2, where v covers a iff (k+1)·d_p(av) < p.
- Any such M is C + (k−|C|) arbitrary classes, where C ⊆ supp M is a minimal cover (|C| ≤ k).
- Units map covers to covers, so every orbit has a representative with 1 ∈ C.
- The DFS adds class 1 first, then repeatedly branches on the uncovered time with fewest allowed coverers, excluding earlier siblings. It cuts a node only when (k − |L|) · max-gain < #uncovered.
  - This reaches every minimal cover containing 1 exactly once: follow, at each node, the first candidate that lies in C. The leaf is a cover inside C, hence equal to C.
- We do **not** implement Allikvere's private-time normalisation (his Lemma 4.1). Our tree is therefore larger, about 14× at k = 14, p = 401.

## Approaches

### 1. Exact checker for one tuple (done, step 1)

`lonely.py` provides:

- a complete search over left endpoints of the good intervals, with no-witness certificates;
- exact ML(v), attained at some a/(v_i+v_j).

The proofs are in the docstring.

### 2. Prime-gate sieve, reproduced end to end for 4–10 runners (done)

- **Steps 1–2:**
  - The level-one step uses a naive bitset DFS (k ≤ 8) or the minimal-cover generator (k = 9).
  - Lifting and projection chains are as in arXiv:2604.23906.
  - The exact test ∏p ≥ B_k uses the MSS/Rosenfeld B_k. We do not use the flag bound or the forced divisor in our reproductions.
- **Cross-check against the papers' gate sets:**
  - **k = 6:** our failing primes (11, 17, 23, 29) are exactly the gaps in Rosenfeld's set {13, 19, 31, …}.
  - **k = 7:** our first passing prime (31) equals Rosenfeld's.
  - **k = 8:** our passing set from 47 is all 39 primes from 47 to 241, **identical to Trakulthongchai's S_8**.
  - **k = 9:** every prime from 137 to 401 passed, **identical to Trakulthongchai's S_9**.
- **Failed gates (kept):**
  - k = 3: p = 5.
  - k = 6: p = 11, 17, 23, 29.
  - k = 7: p = 11, …, 29.
  - k = 8: p = 11, 13, 17. That run was restarted from 47, and Trakulthongchai reports 11–43 all fail.

  At small p the time grid is too coarse.

### 3. Naive level-one DFS (measured, step 1): does not scale

The number of leaves is C((p−1)/2 + k − 2, k − 1). That works out to about 10¹⁴ core-hours for k = 15. Kept for reference.

### 4. Minimal-cover generator (step 2): validated; cost measured

- **Validation.** On 125 (k,p) pairs (k = 3…8, primes up to 89), its orbit set equals the naive enumerator's (`test_lonely.py` keeps a subset).
- **Speed.** At k = 7, p = 173: 0.05 s against 3.7 s for the naive enumerator.
- **Cost-estimation mode.**
  - Knuth's random-probe estimator of the tree size: 20,000 probes. Validated against exact node counts at k = 7, 8, 9 within 0.3%.
  - A capped timed DFS: about 2–3·10⁶ nodes/s on one (shared) core.
- **Estimated tree sizes for ours:**

  | p | 251 | 263 | 307 | 353 | 401 | 449 | 503 | 569 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | N_14 | 9.5e10 | 1.4e11 | 6.1e11 | 1.1e12 | 2.2e12 | 3.3e12 | 1.0e13 | 1.9e13 |
  | N_15 | 4.2e11 | 9.2e11 | 4.1e12 | 1.3e13 | 3.0e13 | 5.8e13 | 8.4e13 | 1.9e14 |

- **Comparison with Allikvere.** His tree at k = 14, p = 401 has 1.6·10¹¹ nodes and took 44,413 CPU-s. Ours is 2.2·10¹² nodes, about 300 CPU-h. So his private-time pruning is worth about 14× in nodes. Our generator alone is too slow for k = 15; his normalisation must be added.

### 5. Spot check of Allikvere's 15-runner certificates (step 2)

`check_allikvere.py` reads the archives as data only and uses our own code throughout. It ran on four of the 71 gates: p = 401, 397, 311, 263. Every archive's SHA-256 matches the published `SHA256SUMS.txt`.

For each of the four gates we checked:

1. Every stored level-one row is witness-free at level 1, i.e. lies in I(14,p,1). The row counts were 394, 3,072, 130,999 and 812,780.
2. Every km1 cover extended by every class is also improper.
3. **Cascade.**
   - Lifting all rows by 2 up to level 32 with our `liftfree.c` (branch-and-bound over lift digits, a separate code path) plus the gcd clause leaves exactly one orbit: (1, …, 14). This matches the certificate.
   - For every listed level-2 survivor row, our count of improper level-2 lifts equals the certificate's `l2`, with 0 mismatches. The totals are 3, 2, 23 and 1023.
   - At p = 263 our count of *distinct* lifts is 1021, because two pairs of rows share a lift. This is not a discrepancy.
4. **Level-15 kill of (1..14).**
   - Witness-free lifts: 3 at level 3 and 5 at level 5.
   - 15 CRT candidates, of which 7 are witness-free on the level-15 grid.
   - All 7 are proper by the gcd clause.
   - This is identical to the certificate at all four gates.

**Not checked:**

- *Completeness* of the level-one rows, i.e. that every orbit of I(14,p,1) is represented. This needs a k = 14 generator run, about 12 CPU-h per gate for his code and about 300 CPU-h for ours at p = 401.
- The other 67 gates.
- The 19 near-gcd gates (τ ≤ 12, p ≤ 241), which use Lemma 3.12.
- The LRC(13) archive (174 MB).
- The flag-bound shape Lemma 3.7. We did re-check K_n and the log constants.

### 6. Tight orbit for 16 runners (step 2)

`tight_orbit_k15.py` tracks the tight tuple (1, …, 15) at all 79 candidate gate primes 251…743. At every prime it has 1, 2 and 4 improper lifts at levels 2, 4 and 8, and **none at level 16**. This is computed exactly with `liftfree.c` plus the gcd clause.

So, unlike 14 and 15 runners, the tight orbit needs no extra fibre search at these primes. This agrees with the munim repository's 10-prime pilot. Only this one orbit is examined: these are not gate checks.

### 7. Independent re-check of Allikvere's certificates (steps 3–4)

**Tools** (all ours, archives read as data only):

- `gatecheck.c`:
  - `cascade`: per-row binary cascade to level 32, directly from Def. 2.1.
  - `kill`: level-3 and level-5 witness-free lifts, CRT to level 15, level-15 grid, gcd clause, then the few-exception shift Lemma 3.12 (d ∈ {3, 5}, m_d = ⌈2d/15⌉).
- `canon.c`: unit-orbit canonical forms.
- `check_gate_full.py` checks, per LRC(14) gate:
  - **A.** The archive SHA-256 matches the published `SHA256SUMS.txt`.
  - **B.** Every stored irredundant row is witness-free at level 1.
  - **C.** The cascade counts (l2, l4, l8, l16, l32) agree **per unit orbit** with the certificate's `filt/*.out`, with the same set of survivor orbits.
    - The comparison is per orbit because the certificate deduplicates km1 extension rows, so rows cannot be matched one-to-one. Improper-lift counts are unit-invariant (F2).
    - The orbits persisting to level 32 equal the orbits of the certificate's `kills/`.
  - **D.** Every kill record (wf3, wf5, CRT candidates, wf15, improper after gcd, improper after near-gcd) equals ours. Improper after near-gcd is 0, and for "J(14,p) = ∅" claims improper after gcd is also 0.
- `completeness_check.py`: level-one completeness (below).
- `check_lrc13_kills.py`: the LRC(13) archive (below).

**Downloads.** 58 of the 71 LRC(14) archives were downloaded: every archive under 60 MB, which is all 52 "J empty" gates and 6 of the 19 near-gcd gates. All 58 SHA-256 sums match. The 13 archives over 60 MB (near-gcd gates 131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241; up to 1.6 GB) were not downloaded.

**LRC(14) results.** Two summary files are generated from the results:

- `results/lrc14_gates/COVERAGE.md` (from `coverage_table.py`): every one of the 71 gates, with the status of each check (archive hash, rows, cascade, kill, completeness) marked full, sampled or not checked.
- `results/lrc14_gates/SUMMARY.md` (from `summarize_step3.py`).

Per-gate JSON files are in `results/lrc14_gates/`.

**Overall verdict (step 5, checkpoint 5):** independent re-check of 71/71 LRC(14) gates.

- All 52 "J empty" gates were checked in full.
- 19 of the 19 near-gcd gates were checked: every stored row tested, with the cascade and kill on seeded samples (3,000, or 500 for the large archives).
- Level-one completeness was checked at p = 89 and p = 239.
- **No discrepancy was found.**
- **All 71 gates are now covered.**

- **"J(14,p) = ∅" gates (decomposition type, τ(p) ≥ 13): all 52 checked in full. All pass.**
  - Step 3 covered the 47 primes from 263 to 569.
  - Step 4 added 239, 251, 257, 271 and 277, one at a time with 1 process. These have 1.34M, 2.25M, 5.65M, 10.0M and 2.77M stored irredundant rows, and 2,030, 3,228, 12,208, 26,521 and 3,266 survivor orbits on both sides respectively. Each took 8–75 min.
  - At every gate, the persistent orbit is exactly (1..14) and the kill record is identical.
- **Near-gcd gates (τ(p) ≤ 12, divisibility via Lemma 2.2(ii)):**
  - **p = 89, sampled:** 3,000 random rows and 3,000 random persistent orbits out of 186,365, seeded.
    - Cascade: 2,998 orbits compared, 2,671 survivor orbits on both sides, 0 count mismatches.
    - Every sampled persistent row lies in a certificate orbit.
    - Kills: all 3,000 match the records. Totals: 2,249,044 CRT candidates, 1,211,876 witness-free at level 15, 354,688 left by the gcd clause, **0 after the near-gcd lemma**.
    - Time: 2,535 s.
  - **p = 179:** sampled: 1,000 random rows and 1,000 random persistent orbits out of 8,011, seeded, 2 processes, 815 s.

    - All 2,133,835 stored irredundant rows are improper; this test covers every row, not a sample.
    - Cascade: 1,000 orbits compared, 25 survivor orbits on both sides, 0 count mismatches.
    - Kills: all 1,000 match. Totals: 356,114 CRT candidates, 281,826 witness-free, 81,280 left by the gcd clause, **0 after the near-gcd lemma**.
    - A first run with 3,000/3,000 was lost to a container restart.
  - **p = 233 (step 4, redone), sampled 3,000/3,000:**
    - All 5,767,782 stored rows are improper.
    - Cascade: 46 survivor orbits among the sample on both sides.
    - Kills: all 3,000 of 13,457 match; 0 after the near-gcd lemma.
    - Time: 2,790 s.
  - **p = 223 (step 4), sampled 3,000/3,000:**
    - All 1,886,974 stored rows are improper.
    - Cascade: 140 survivor orbits among the sample on both sides.
    - Kills: all 3,000 of 48,071 match. Totals: 1,063,346 CRT candidates, 845,170 witness-free, 243,968 left by the gcd clause, **0 after the near-gcd lemma**.
    - Time: 2,883 s.
  - **p = 163 and p = 173 (step 5),** run with the streaming checker `check_gate_stream.py`, sample 3,000:
    - All stored rows are witness-free at level 1: 7,383,739 at p = 163 and 7,777,371 at p = 173. All km1 covers are covers.
    - Cascade: 3,000 uniformly sampled irredundant rows (99 and 74 with survivors) plus 3,000 uniformly sampled extension-survivor lines (of 726,154 and 538,767). 0 mismatches.
    - Kills: 3,000 of 107,244 and 3,000 of 96,840 match. 0 improper after the near-gcd lemma.
    - The number of kill files equals the certificate's persistent-orbit count.
    - Time: about 34 min each.
  - **Large near-gcd archives (step 5),** streaming checker, **sample 500** (500 irredundant rows, 500 extension-survivor lines, 500 kills per gate). Every stored row is tested, and every gate passes with 0 mismatches and 0 improper after the near-gcd lemma:
    - p = 131: 5,463,210 rows; 2,239,365 kill files; extension-survivor lines 8,725,762; 611 s.
    - p = 149: 4,307,522 rows; 967,875 kill files; extension-survivor lines 3,203,434; 411 s.
    - p = 157: 29,230,783 rows; 3,541,563 kill files; extension-survivor lines 14,912,271; 850 s.
    - p = 167: 32,890,555 rows; 1,599,697 kill files; extension-survivor lines 7,563,522; 562 s.
    - p = 181: 142,334,217 rows; 8,235,157 kill files; extension-survivor lines 38,160,231; 1605 s.
    - p = 191: 27,201,490 rows; 2,362,553 kill files; extension-survivor lines 7,713,522; 617 s.
    - p = 193: 15,203,915 rows; 973,342 kill files; extension-survivor lines 2,888,145; 502 s.
    - p = 197: 46,411,987 rows; 312,041 kill files; extension-survivor lines 2,092,913; 410 s.
    - p = 199: 25,180,487 rows; 196,288 kill files; extension-survivor lines 817,224; 367 s.
    - p = 211: 45,883,385 rows; 165,061 kill files; extension-survivor lines 1,079,040; 396 s.
    - p = 227: 28,242,035 rows; 44,974 kill files; extension-survivor lines 308,105; 353 s.
    - p = 229: 19,201,544 rows; 62,072 kill files; extension-survivor lines 314,785; 350 s.
    - p = 241: 22,356,624 rows; 14,401 kill files; extension-survivor lines 78,382; 361 s.
  - **Not checked:**
    - None: all 19 near-gcd gates are covered (sampled as stated).
- **No discrepancy with any certificate was found.** Two apparent issues turned out to be artefacts of our own scripts:
  - p = 263: 1021 against 1023 level-2 lifts. The certificate counts with multiplicity over rows; per-row counts agree exactly.
  - The k = 13 SHA-256 lookup: duplicate kill-file copies under `cloud_gates/` with LF line endings were matched against the wrong manifest. With paths resolved relative to each manifest, every file matches.

**Level-one completeness (p = 89, a near-gcd gate).**

- Method: `covergen.c` enumerated all 1,689,912 minimal covers containing class 1 (8.5·10⁶ search nodes), expanded them to 10,174,414 multisets, and `canon.c` reduced them to orbits. This is **without** Allikvere's private-time pruning.
  - The pruning (his Lemma 4.1) has a short proof in the paper, but we did not implement it. The unpruned search is exhaustive by the argument in `covergen.c`'s header and fits the budget at p = 89.
- Result: **687,016 orbits, equal to the orbit set of the certificate's 966,696 stored rows** (110,720 irredundant + 19,454 km1 covers × 44 extensions). There are no orbits on only one side.
- **p = 239 ("J empty" gate, step 4).**
  - Generation: unpruned `covergen.c`, sharded over 3 cores with `LRC_NSHARDS=3`. Sharding is tested to give exactly the unsharded output. It took 4.75·10¹⁰ search nodes and about 88 min wall time, producing 18,810,658 minimal covers. Those expand to 20,093,082 multisets.
  - Result: **1,441,284 orbits, exactly equal to the orbit set of the certificate's 1,442,327 stored rows** (1,342,843 irredundant + 99,484 extension rows). No orbit appears on only one side.
- **Pruning: none.** We did not implement Allikvere's Lemma 4.1 private-time normalisation. Both completeness runs are unpruned, so they rely only on the minimal-cover argument in `covergen.c`.
- Not done: completeness at any other gate (a p = 179 run was lost in a step-3 restart).

**LRC(13) archive** (Zenodo 10.5281/zenodo.22066772, `fourteen_lonely_runners_package.zip`).

- The zip's MD5 matches Zenodo's (9b65648956…); Zenodo publishes only MD5 for this record.
- **The archive does not store the level-one rows for k = 13** (only generator logs). So rows, cascade and completeness cannot be re-checked from it.
- Checked instead, at **66 of 111 gate primes** so far (the list is in `results/lrc13_kills.jsonl`; more are running). This includes p = 199, whose kill records are the root-level files `kill_tight_final.txt` and `kill_gw_final.txt` referenced by `certificates_p199/SUMMARY.json`:
  - Each kill file's SHA-256 against its gate's `MANIFEST_SHA256.json` (all match).
  - Our recomputation of the terminal level-14 step for both persistent orbits, (1..13) and (1..11, 13, 24):
    - the improper level-2 members (1–8 per orbit);
    - for each member, all witness-free lifts by 7 (liftfree.c, M = 2p, c = 7) and the gcd clause at l = 14.
- **All match the certificates:** exactly one witness-free lift per member, and 0 improper after the gcd clause. At p = 83 even the search-node count (17,753,408) coincides with the record.
- Not checked: the other 92 of the 111 primes; the binary cascade; the level-one family.

### 8. Private-time pruning for the level-one generator (step 6)

**Notation.** Fix k and a prime p. Put n = (p−1)/2 (folded time classes 1..n) and folded speed classes 1..n. Class v *covers* time a iff (k+1)·d_p(av) < p. For a set C of classes and v ∈ C, the *private times* of v in C are the times covered by v and by no other class of C; write priv_C(v) for their number.

**Fact.** Every class covers exactly m = ⌊(p−1)/(k+1)⌋ times.

- As a runs over 1..n, the folded residue d_p(av) runs over 1..n bijectively, because v is a unit and folding identifies ±.
- (k+1)x < p ⇔ x ≤ m, since (k+1) ∤ p.

**Lemma 4.1 (Allikvere, arXiv:2609.02604v2; our transcription).** Let C be a cover of all n times by s distinct classes. Some class of C has at least q_s := ⌈max(0, 2n − s·m)/s⌉ private times.

*Proof.* Let n_j be the number of times covered by exactly j classes of C.

1. Counting incidences: s·m = Σ_j j·n_j ≥ n_1 + 2(n − n_1).
2. So n_1 ≥ 2n − s·m.
3. The n_1 singly-covered times are private to their class, and there are s classes, so by pigeonhole one class has at least ⌈n_1/s⌉ ≥ q_s of them. ∎

**Normalisation.**

- Multiplying by a unit u maps covers to covers: v covers a iff uv covers u⁻¹a. So it maps private times of v to private times of uv bijectively.
- Hence every unit orbit of minimal covers contains a representative C ∋ 1 in which class 1 has the **largest** number of private times. Choose v with maximal priv_C(v) and scale by v⁻¹.
- Then in particular priv_C(1) ≥ q_|C|.
- Every improper k-multiset is C + extras for a minimal cover C (see `covergen.c`), so restricting to these representatives keeps at least one representative of every orbit of I(k,p,1).

**Search cuts** (`covergen.c`, environment `LRC_PRUNE`):

- **`LRC_PRUNE=1` (Lemma 4.1).**
  - Leaf filter: priv_C(1) ≥ q_|C|.
  - Node cut: class 1's private set only shrinks when classes are added, and q_s is non-increasing in s (|C| ≤ k). So a node whose current priv(1) < q_k has no passing leaf below it, and a child that would bring priv(1) below q_k is skipped. Its class is still excluded for later siblings, exactly as in the unpruned search.
- **`LRC_PRUNE=2` (max-private normalisation, Allikvere §4.1).**
  - Leaf filter: priv_C(1) ≥ priv_C(v) for every v ∈ C.
  - Node cut ("locked" times): a private time of a chosen class v that **no still-allowed class covers** remains private to v in every completion (allowed sets only shrink below a node). Since priv(1) only shrinks, the node is cut if |locked(v)| > priv(1) for some v.
  - Forbidding: an allowed class c with priv(1) − |P₁ ∩ cov(c)| < max_v |locked(v)| is removed from the allowed set. Here P₁ is class 1's current private set. Adding c would leave class 1 below some class's locked count forever, and forbidding classes only enlarges locked sets. The gain bound is then re-applied.
- These rules only remove search nodes with no admissible leaf below them, and leaves that are not the normalised representative. The orbit set is unchanged.

**Validation** (`test_lonely.py`, `test_covergen_pruning_preserves_orbits`). For (k,p) = (5,41), (7,61), (8,101), (9,137), (14,89), levels 0, 1 and 2 give identical orbit sets, and at (14,89) that set has the certificate's 687,016 orbits. At (14,113) only the node counts were measured: the orbit-set comparison (expanding 43.8M unpruned covers) did not finish within its time limit, so it is not claimed.

**Measured speed-up** (single core):

| (k, p) | nodes, levels 0 / 1 / 2 | minimal covers output | time |
| --- | --- | --- | --- |
| (14, 89) | 8.49M / 4.74M / 4.73M | 1.69M / 0.98M / 0.26M | 3.3 / 1.9 / 1.8 s |
| (14, 113) | 268M / 240M / 235M | 43.8M / 43.1M / 6.6M | 88 / 87 / 70 s |

- The node savings shrink as p grows. q_k is only 2 at p = 239. The locked-time rule also rarely fires, because nearly every time stays reachable until deep in the tree.
- The large gain is in output: 5–7× fewer covers to expand and canonicalise.
- **Failed route (kept):** these rules do **not** reproduce Allikvere's roughly 14× smaller tree (Approach 4). His engine also uses a two-branch search (irredundant k-class covers and extensions of smaller covers) with irredundance-aware bounds, which we have not implemented.

## Independent re-check summary

Scope: J. Allikvere's computer-assisted proofs of LRC(13) and LRC(14), i.e. 14 and 15 runners (arXiv:2609.02604v2). Certificates: Zenodo 10.5281/zenodo.22066772 and 10.5281/zenodo.22667683. All checks use our own code (C and Python, in `computations/lonely-runner/`), written from the definitions in the paper and in arXiv:2604.23906. The archives were read as data only; none of the author's programs were executed.

**What an outside reader can rely on (LRC(14), 71 gate primes):**

- **Archive integrity: all 71 gates.** Each archive's SHA-256 equals the published `SHA256SUMS.txt` entry. 58 archives were kept; 13 were checked on download and then deleted.
- **Stored level-one rows: all 71 gates, every row.** Every stored irredundant row is witness-free at level 1, i.e. lies in I(14,p,1). Every stored km1 multiset is a cover. That is 495,538,971 stored irredundant rows in total.
- **Binary cascade, levels 2–32.** In full at all 52 "J(14,p) = ∅" gates. At the 19 near-gcd gates, on seeded uniform samples of stored rows (compared both ways) and of extension-survivor lines: 3,000 at p = 89, 163, 173, 223, 233; 1,000 at p = 179; 500 at the 13 large archives. There were 0 mismatches.
- **Level-15 kill records.** In full at the 52 "J empty" gates (one persistent orbit, (1..14), each). At the near-gcd gates, on seeded samples of the same sizes. Every record checked is reproduced exactly: level-3/5 witness-free lifts, CRT candidates, level-15 grid, gcd clause, and the few-exception shift Lemma 3.12. Improper after Lemma 3.12 is 0 everywhere, and improper after the gcd clause is 0 at the "J empty" gates. At the stream-checked gates, the number of kill files equals the certificate's persistent-orbit count.
- **Level-one completeness at 2 gates.** At p = 89 (near-gcd) and p = 239 ("J empty"), an independent, unpruned minimal-cover enumeration reproduces exactly the certificate's set of level-one orbits: 687,016 and 1,441,284 orbits.
- **Constants.** The flag-bound constants K_14, A_14, the log bound 414.779365 and the target 401.984506 were re-derived exactly. The 71 gates' Σ ln p = 408.8233 exceeds the target, recomputed from the gate list.
- **LRC(13).** At 66 of 111 gate primes (in progress), the terminal level-14 kill of both persistent orbits was recomputed and matches, and the kill files' SHA-256 match the gate manifests.
- **No discrepancy with any certificate was found.**

**What remains unverified here:**

- **Level-one completeness at the other 69 LRC(14) gates.** That every orbit of I(14,p,1) is represented among the stored rows is checked only at p = 89 and 239. At all other gates it rests on Allikvere's generator and its completeness proposition (his Prop. 4.2 with the private-time Lemma 4.1), which we did not implement.
- **The sampled parts at the 19 near-gcd gates.** The unsampled cascade rows and kill records there were not re-computed.
- **The analytic inputs.** The finite-checking bound (Malikiosis–Santos–Schymura, via Rosenfeld's Cor. 3) and Allikvere's flag bound (Thm 3.8) were not re-proved; in particular the shape Lemma 3.7 was not re-checked. Nor were the lattice lemmas behind it, the prime-divisibility Lemma 2.2(ii), or the few-exception shift Lemma 3.12, beyond reading their proofs. The lower cases LRC(m), m ≤ 12, are taken from the literature.
- **LRC(13).** The archive does not contain the k = 13 level-one rows, so the rows, cascade and completeness cannot be re-checked from it. Only 66 of 111 terminal kills were recomputed.
- **Our own code is not formally verified.** It is tested against brute force on small cases (18 tests) and against the certificates' own numbers.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| `find_witness` is a complete decision procedure; ML(v) is attained at some a/(v_i+v_j) | proved (short proofs in docstring) | `lonely.py` |
| ML(1, …, n) = 1/(n+1) exactly, n ≤ 10; ML(1,3,4,7) = 1/5 | computed exactly | `test_lonely.py` |
| Every primitive tuple with max speed ≤ N has a witness at 1/(n+1): (n, N) = (3, 150), (4, 60), (5, 32), (6, 22), (7, 18) | computed up to N | `results/exhaustive.txt` |
| Tight primitive tuples in those ranges: (1,2,3); (1,2,3,4), (1,3,4,7); (1,…,5), (1,3,4,5,9); (1,…,6); (1,…,7), (1,2,3,4,5,7,12), (1,4,5,6,7,11,13) | computed up to N | `results/exhaustive.txt` |
| Sieve, naive level one, cover generator and `liftfree.c` agree with each other and with brute force from the definitions | tested (17 tests; 125 (k,p) pairs for the generator) | `test_lonely.py` |
| LRC(3) … LRC(8) (4–9 runners); gate sets in `results/lrc_k*.jsonl`; the k = 8 set equals Trakulthongchai's S_8 | certificate-checked computation **+ cited B_k** | `results/lrc_k3..8.jsonl` |
| LRC(9) (10 runners): all 47 primes 137…401 pass (identical to Trakulthongchai's S_9), Σ ln p = 259.94 > 254.30; cover generator, chain ×2×2×2, proj, ×5×2; 1,313 s wall on 4 processes | certificate-checked computation **+ cited B_k** | `results/lrc_k9.jsonl` |
| Allikvere constants: K_13, K_14, ratio minima, ln bounds 341.031991 and 414.779365, target 401.984506 | exact rational re-derivation | `flag_bound.py` |
| n = 15 flag constants: K_15, ratio min 3751/2349 > 4/3 | exact | `flag_bound.py` |
| n = 15 shape factor ≈ 0.48796, hence target 483.24 | **heuristic** (no shape lemma) | `flag_bound.py` |
| 4 of 71 LRC(14) gate certificates (p = 263, 311, 397, 401): rows improper, cascade and kill reproduced | independent re-computation of the certificate's claims **except level-one completeness** | `check_allikvere.py`, `results/allikvere_spotcheck.jsonl` |
| LRC(14) certificates: independent re-check of 71/71 gates. All 52 "J empty" gates in full. Near-gcd gates 89, 163, 173, 179, 223, 233 (sample 3,000 or 1,000) and 131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241 (sample 500): all rows, plus seeded samples of the cascade and kill. Level-one completeness at p = 89 and p = 239. No discrepancy found. | independent re-computation of the certificates' claims; cascade/kill sampled at the 19 near-gcd gates; completeness at 2 gates only | `results/lrc14_gates/COVERAGE.md`, Approach 7 |
| LRC(13) certificates: terminal level-14 kill of both persistent orbits re-computed at 66 of 111 gate primes (in progress); kill-file SHA-256s match manifests | independent re-computation (cascade and level one not checkable: rows not archived) | `results/lrc13_kills.jsonl` |
| (1..15) dies at level 16 at all 79 primes 251–743 | computed exactly (one orbit only) | `results/tight_orbit_k15.jsonl` |
| Cost of LRC(15) level one + kill with Allikvere-class code: about 1.75·10⁵ CPU-h (about 20 CPU-years) for 79 gates 251–743 under the heuristic flag target; about 8.7·10⁶ CPU-h under the proved B_15 | **heuristic extrapolation from measurements** | `cost_estimate.py`, `results/knuth_covergen_k14_k15.txt` |

"Certificate-checked computation + cited B_k" means the following. The chain LRC(2) ⇒ … ⇒ LRC(9) is a proof *if* three things hold:

- the MSS bound in Rosenfeld's Corollary 3 form,
- the elementary lemmas above,
- the correctness of our code.

Our code is tested against brute force, but not formally verified. These reproduce *known* cases only. Nothing new is claimed.

## Next steps: plan for LRC(15) (16 runners)

1. **Bound.**
   - Prove a shape lemma R_15 < 49/100, following Allikvere's Lemma 3.7. The one-variable reduction and the "two or more coordinates equal to one" case must be redone for n = 15.
   - Until then, the only proved target is ln B_15 − ln 720720 = 951.26. That needs about 147 gates up to 1223, which is roughly 50× the cost below.
2. **Generator.** Add Allikvere's private-time normalisation (his Lemma 4.1 and the two-branch search) to `covergen.c`. Validate it against the current generator for k ≤ 9, and then against his archived k = 14 rows at p = 397 and 401. Those are small gates: about 13 and 16 CPU-h for his code.
3. **Cost.**
   - Model: Allikvere's per-gate k = 14 CPU time, times our measured k = 15 / k = 14 tree-size ratio. The ratio grows from 4.4 at p = 251 to 10–18 at p = 353–569, fitted ∝ p^1.0. His cost is fitted ∝ p^6.07.
   - Result: **about 1.75·10⁵ CPU-hours for 79 gates 251…743**, assuming the flag target. Of that, gates above 569 are extrapolated, and the top gates dominate.
   - This is a **cluster-scale** project (for example 1,000 cores for about a week). It does not fit in a single session.
   - Uncertainties:
     - The ratio is noisy (single estimates per prime).
     - Small-τ gates may need the near-gcd treatment.
     - Better gate choices (including some p < 251) could change the total by small factors.
4. **The tight orbit is not a bottleneck.** (1..15) dies by level 16 at every candidate prime (Approach 6). The remaining unknown per gate is the level-one family and whether any other orbit persists.
5. **Finish the LRC(14) replay.** What remains:
   - near-gcd gates 163 and 173;
   - the 13 near-gcd archives over 60 MB (0.1–1.6 GB; kills about 0.5 s per orbit, and p = 181 has 8.2M orbits);
   - full rather than sampled cascade and kill at the 4 sampled near-gcd gates;
   - level-one completeness at more gates. With the private-time pruning implemented and tested, this would be much cheaper; unpruned, p = 239 took about 4.4 core-hours.
6. **LRC(10) (11 runners)** was not reproduced, to stay within the budget. Our chain would need an ×11 lift of the tight orbit (11¹⁰ lifts) or Sungkawichai–Trakulthongchai's Prop. 1.2. `liftfree.c` with branch and bound should make the ×11 lift cheap; try it first.
7. **Independent replay of 15 runners.** With the faster generator from step 2, rerun a handful of small k = 14 gates in full, including level-one completeness. This would upgrade the spot check.
8. **Do not** present any of this as a proof until every gate has stored, re-checkable output and the bound is proved.
