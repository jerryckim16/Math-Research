# Lonely Runner Conjecture

**Area:** Diophantine approximation / combinatorics
**Status:** in progress. Done so far:
- The prime-gate framework is reproduced end to end for 4–10 runners, conditional on one cited bound (B_k).
- Four of Allikvere's 15-runner gate certificates are spot-checked.
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

### 7. Independent re-check of Allikvere's certificates, widened (step 3)

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

**LRC(14) results:** see the table in `results/lrc14_gates/SUMMARY.md` (generated by `summarize_step3.py`). Per-gate JSON files are in `results/lrc14_gates/`.

- **"J(14,p) = ∅" gates (decomposition type, τ(p) ≥ 13):** **47 of the 52 checked in full: every prime from 263 to 569.** All pass, with no mismatches.

  - Totals: 4,683,759 stored rows re-tested, cascade per orbit, the persistent orbit is exactly (1..14) at every gate, and 47 kill records are identical.
  - Not checked: 239, 251, 257, 271 and 277. These are the largest decomposition archives; the batch was cut off by two container restarts and the step budget.
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
  - **p = 233:** a full run was started but stopped by a container restart (memory). It was not redone.
- **No discrepancy with any certificate was found.** Two apparent issues turned out to be artefacts of our own scripts:
  - p = 263: 1021 against 1023 level-2 lifts. The certificate counts with multiplicity over rows; per-row counts agree exactly.
  - The k = 13 SHA-256 lookup: duplicate kill-file copies under `cloud_gates/` with LF line endings were matched against the wrong manifest. With paths resolved relative to each manifest, every file matches.

**Level-one completeness (p = 89, a near-gcd gate).**

- Method: `covergen.c` enumerated all 1,689,912 minimal covers containing class 1 (8.5·10⁶ search nodes), expanded them to 10,174,414 multisets, and `canon.c` reduced them to orbits. This is **without** Allikvere's private-time pruning.
  - The pruning (his Lemma 4.1) has a short proof in the paper, but we did not implement it. The unpruned search is exhaustive by the argument in `covergen.c`'s header and fits the budget at p = 89.
- Result: **687,016 orbits, equal to the orbit set of the certificate's 966,696 stored rows** (110,720 irredundant + 19,454 km1 covers × 44 extensions). There are no orbits on only one side.
- Not done:
  - A completeness run at p = 179 was started and lost in the container restart.
  - No completeness check was made at any "J empty" gate. The smallest, p = 239, needs about 4.6·10¹⁰ nodes for our unpruned generator, roughly 4 core-hours.

**LRC(13) archive** (Zenodo 10.5281/zenodo.22066772, `fourteen_lonely_runners_package.zip`).

- The zip's MD5 matches Zenodo's (9b65648956…); Zenodo publishes only MD5 for this record.
- **The archive does not store the level-one rows for k = 13** (only generator logs). So rows, cascade and completeness cannot be re-checked from it.
- Checked instead, at **19 gate primes** (83, 139, 167, 181, 191, 211, 223, 239, 263, 307, 401, 449, 503, 563, 601, 701, 797, 853, 877):
  - Each kill file's SHA-256 against its gate's `MANIFEST_SHA256.json` (all match).
  - Our recomputation of the terminal level-14 step for both persistent orbits, (1..13) and (1..11, 13, 24):
    - the improper level-2 members (1–8 per orbit);
    - for each member, all witness-free lifts by 7 (liftfree.c, M = 2p, c = 7) and the gcd clause at l = 14.
- **All match the certificates:** exactly one witness-free lift per member, and 0 improper after the gcd clause. At p = 83 even the search-node count (17,753,408) coincides with the record.
- Not checked: the other 92 of the 111 primes; the binary cascade; the level-one family.

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
| LRC(14) certificates: independent re-check of 47 of 71 gates in full (every "J empty" gate from 263 to 569) plus near-gcd gate 89 (sampled: 3,000 rows and 3,000 of 186,365 kills; level-one completeness in full) and near-gcd gate 179 (see Approach 7); all pass | independent re-computation of the certificates' claims; level-one completeness only at p = 89 | `results/lrc14_gates/`, Approach 7 |
| LRC(13) certificates: terminal level-14 kill of both persistent orbits re-computed at 19 of 111 gate primes; kill-file SHA-256s match manifests | independent re-computation (cascade and level one not checkable: rows not archived) | `results/lrc13_kills.jsonl` |
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
5. **Finish the LRC(14) replay.**
   - Run the five large decomposition gates (239, 251, 257, 271, 277) and the remaining near-gcd gates. Thirteen of the near-gcd archives are 0.1–1.6 GB, so their kills need about 0.5 s per orbit (p = 181 has 8.2M orbits).
   - Run a completeness check at one decomposition gate (p = 239 needs about 4 core-hours unpruned, or less with the private-time pruning).
   - This would turn the spot check into a full independent replay.
6. **LRC(10) (11 runners)** was not reproduced, to stay within the budget. Our chain would need an ×11 lift of the tight orbit (11¹⁰ lifts) or Sungkawichai–Trakulthongchai's Prop. 1.2. `liftfree.c` with branch and bound should make the ×11 lift cheap; try it first.
7. **Independent replay of 15 runners.** With the faster generator from step 2, rerun a handful of small k = 14 gates in full, including level-one completeness. This would upgrade the spot check.
8. **Do not** present any of this as a proof until every gate has stored, re-checkable output and the bound is proved.
