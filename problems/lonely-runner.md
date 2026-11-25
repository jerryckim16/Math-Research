# Lonely Runner Conjecture

**Area:** Diophantine approximation / combinatorics
**Status:** in progress. Done so far:
- The prime-gate framework is reproduced end to end for LRC(3)–LRC(10) (4–11 runners), conditional on one cited bound (B_k). LRC(10) uses an explicit ×11 lift, independent of Sungkawichai–Trakulthongchai's Prop. corlarge (step 7).
- All 71 of Allikvere's 15-runner (LRC(14)) gate certificates are independently re-checked, with no discrepancy found. Stored rows were checked in full at every gate; the cascade and kill in full at 54 gates and sampled at 17, with the cascade alone also in full at near-gcd gate 223; level-one completeness at 3 gates. See "Independent re-check summary". His 14-runner terminal kills are re-checked at all 111 of his gate primes.
- The n = 15 shape lemma R_15 < 49/100 is proved (Approach 10; every inequality machine-checked exactly). The general-n parts of Allikvere's Theorem 3.8 are independently verified (Approach 11), so the 16-runner gate target 483.239 is proved here, given LRC(m) for m ≤ 14.
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
    - **The shape lemma R_15 < 49/100 is now proved here** (Approach 10, step 9; machine-checked by `shape_lemma.py`). The general-n parts of Theorem 3.8 are verified in Approach 11 (step 10), so the target 483.239 is proved here, given LRC(m) for m ≤ 14.
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

### 2. Prime-gate sieve, reproduced end to end for 4–11 runners (done)

- **Steps 1–2:**
  - The level-one step uses a naive bitset DFS (k ≤ 8) or the minimal-cover generator (k = 9, 10). For k = 10 the ×11 lift uses `liftfree.c`.
  - Lifting and projection chains are as in arXiv:2604.23906.
  - The exact test ∏p ≥ B_k uses the MSS/Rosenfeld B_k. We do not use the flag bound or the forced divisor in our reproductions.
- **Cross-check against the papers' gate sets:**
  - **k = 6:** our failing primes (11, 17, 23, 29) are exactly the gaps in Rosenfeld's set {13, 19, 31, …}.
  - **k = 7:** our first passing prime (31) equals Rosenfeld's.
  - **k = 8:** our passing set from 47 is all 39 primes from 47 to 241, **identical to Trakulthongchai's S_8**.
  - **k = 9:** every prime from 137 to 401 passed, **identical to Trakulthongchai's S_9**.
  - **k = 10:** every prime from 127 to 467 passed (61 primes), **identical to Sungkawichai–Trakulthongchai's P_10**. They reach it via Prop. corlarge; we reach it via an explicit ×11 lift (Next steps 6).
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
- The flag-bound shape Lemma 3.7. We did re-check K_n and the log constants. (Later re-checked, step 9: Approach 10.)

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
- Level-one completeness was checked at p = 89, 239 and 251.
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
  - **p = 179, full (step 8):** every row and every persistent orbit, 4 processes, 8,864 s (`results/lrc14_gates/gate_179_full.json`).
  - **p = 223, full cascade only (step 8):** every stored row and every improper extension row (1,886,974 + 328,893). The results matched: 2,160,276 unit orbits, survivor orbits 62,638 = 62,638 (none only on one side, 0 count mismatches), and persistent-orbit sets equal (48,071 = 48,071). 4 processes, 8,999 s (`results/lrc14_gates/gate_223_fullcascade.json`). The kill at 223 is still the 3,000-orbit sample.
  - **p = 233, full cascade only (step 8):** every stored row and every improper extension row (5,767,782 + 782,536). The results matched: 6,517,315 unit orbits, survivor orbits 70,223 = 70,223 (none only on one side, 0 count mismatches), and persistent-orbit sets equal (13,457 = 13,457). 4 processes, 3,634 s (`results/lrc14_gates/gate_233_fullcascade.json`).
  - **p = 233, full (step 8):** every row and every persistent orbit, cascade and kill together. The cascade figures repeat the run above exactly. All 13,457 kill records are reproduced, with 0 mismatches; totals: CRT 4,528,173, wf15 3,674,453, improper after gcd 1,056,768, improper after near-gcd shift 0. 4 processes, 10,703 s (`results/lrc14_gates/gate_233_full.json`).
    - Cascade: all 2,676,385 orbits of stored rows (irredundant rows plus improper km1 extensions) re-run; 70,089 survivor orbits on both sides, 0 count mismatches.
    - Persistent orbits: our set equals the certificate's, 8,011 = 8,011.
    - Kills: all 8,011 records match. Totals: 2,920,345 CRT candidates, 2,284,817 witness-free at level 15, 659,328 left by the gcd clause, **0 after the near-gcd lemma**.
    - p = 179 is the first near-gcd gate re-checked in full (apart from level-one completeness).
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
  - At the time of this step-3 run, the pruning (his Lemma 4.1) was not yet implemented here (it is now: Approach 8). The unpruned search is exhaustive by the argument in `covergen.c`'s header and fits the budget at p = 89.
- Result: **687,016 orbits, equal to the orbit set of the certificate's 966,696 stored rows** (110,720 irredundant + 19,454 km1 covers × 44 extensions). There are no orbits on only one side.
- **p = 239 ("J empty" gate, step 4).**
  - Generation: unpruned `covergen.c`, sharded over 3 cores with `LRC_NSHARDS=3`. Sharding is tested to give exactly the unsharded output. It took 4.75·10¹⁰ search nodes and about 88 min wall time, producing 18,810,658 minimal covers. Those expand to 20,093,082 multisets.
  - Result: **1,441,284 orbits, exactly equal to the orbit set of the certificate's 1,442,327 stored rows** (1,342,843 irredundant + 99,484 extension rows). No orbit appears on only one side.
- **p = 251 ("J empty" gate, step 6).**
  - Generation: `covergen.c` **with `LRC_PRUNE=2`** (Lemma 4.1 plus max-private normalisation; Approach 8), sharded over 3 cores. It took 8.93·10¹⁰ search nodes and about 4 h 55 min wall time (the shards were uneven: 1 h 46 min, 1 h 47 min, 4 h 55 min), producing 3,876,360 covers. Those expand to 4,143,952 multisets.
  - Result: **2,404,346 orbits, exactly equal to the orbit set of the certificate's 2,405,962 stored rows.** No orbit appears on only one side.
  - Because this run is pruned, its completeness rests on the Lemma 4.1 / normalisation proof transcribed in Approach 8 (and its tests) as well as the minimal-cover argument. The p = 89 and 239 runs are unpruned and rely on the minimal-cover argument alone.
- Not done: completeness at the other 68 gates (a p = 179 run was lost in a step-3 restart).

**LRC(13) archive** (Zenodo 10.5281/zenodo.22066772, `fourteen_lonely_runners_package.zip`).

- The zip's MD5 matches Zenodo's (9b65648956…); Zenodo publishes only MD5 for this record.
- **The archive does not store the level-one rows for k = 13** (only generator logs). So rows, cascade and completeness cannot be re-checked from it.
- Checked instead, at **all 111 gate primes** (83 to 877; the list is in `results/lrc13_kills.jsonl` and equals the set of `certificates_p<p>` directories in the archive). This includes p = 199, whose kill records are the root-level files `kill_tight_final.txt` and `kill_gw_final.txt` referenced by `certificates_p199/SUMMARY.json`:
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

### 9. Sharper bounds in the minimal-cover search (step 7)

Goal: a faster level-one generator, as the precondition for completeness at more gates. `covergen.c` with `LRC_IRR` (a bitmask; the output is unchanged by construction):

- **Bit 2, sharper gain bound.** At a node with r = k − |L| classes still to choose, the r largest gains |cov(c) ∩ U| over allowed classes c must sum to at least |U|. The plain bound uses r · max gain. Any completion adds at most r classes, and each covers at most its gain of the uncovered times, so the cut removes only nodes with no cover below.
- **Bit 1, redundancy cuts.**
  - If a chosen class has no private time relative to the other chosen classes, the node is cut: private sets only shrink as classes are added, so no minimal cover lies below.
  - An allowed class c that covers all private times P_v of some chosen class v is forbidden in the subtree, because v would be redundant in any cover containing c.
  - By the symmetry of d_p(av) in a and v, the coverers of a time a are exactly cov(a). So these classes are found as the intersection of cov(a) over a ∈ P_v.
- **Validation** (`test_covergen_irr_same_minimal_covers`). For (k, p) = (5,41), (7,61), (8,101), (9,137), (10,127), (14,89), `LRC_IRR` = 1, 2 and 3 print **exactly the same set of minimal covers** as the plain search, also under 3-way sharding. Combined with `LRC_PRUNE=2`, the (14, 89) orbit set is unchanged: 687,016 orbits (`test_covergen_pruning_preserves_orbits`).
- **Measured** (`results/knuth_irr_k14.txt`; Knuth estimates are heuristic):
  - Ablation at p = 251: the sharper gain bound gives nearly all of the node saving (8.70·10¹⁰ → 4.55·10¹⁰) at about 90% of the node rate.
  - The redundancy cuts remove few extra nodes and more than halve the node rate, so `LRC_IRR=2` is the recommended setting.
  - A greedy packing bound (times with disjoint coverer sets) gave nothing and was dropped (failed route, kept).
  - Exact count at (14, 113): 268M plain vs 111M nodes with both bits, giving the same 43,763,271 minimal covers.
  - With `LRC_IRR=2`, the tree has 1.90× fewer nodes at p = 251 and 1.83× fewer at p = 257, for a net speed-up of about 1.7×.
  - So completeness at p = 257 would still take about 12 core-hours (at least about 4 h of wall time on 3 cores). It was not run.
- **Still short of Allikvere's tree** (about 14× smaller than our plain search, Approach 4). The remaining gap is not explained by the bounds tried here.

### 10. Shape lemma R_15 < 49/100 (step 9)

**Claim.** On the positive simplex in R^15, R_15 < 49/100. Here R_n is the shape factor of Allikvere's flag bound (arXiv:2609.02604v2, eq. (F)):

- F_n(x)² = ∏ q_i · Σ x_i²/q_i and R_n(x) = n (∏ x_i)^{1/n} / F_n(x);
- q_i = 1 + 2u_i − u_i², with u_i = x_i / max_j x_j.

**Status: proved here.** The argument is the paper's proof of Lemma 3.7 carried over to n = 15, written out below. Every identity and numeric inequality in it is checked in exact rational arithmetic by `computations/lonely-runner/shape_lemma.py` (tests: `test_shape_lemma.py`). The same script, run with n = 13 and n = 14, reproduces the paper's polynomials, cubics, intervals and the bounds R_13 < 101/200 and R_14 < 1/2 (regression tests). So Lemma 3.7 itself is now re-checked as well.

The (unreviewed) munim lonely-runner-16 repository states the same bound. We did not use its text; our derivation agrees with it.

**Notation.** For u ∈ (0,1] put:

- q(u) = 1 + 2u − u²;
- a(u) = q(u)/u^{2/15};
- w(u) = u²/q(u);
- H(u) = (Σ_i w(u_i)) · ∏_i a(u_i);
- D(u) = 14u² − 13u + 1.

The common scale cancels, so R_15(x)² = 225/H(u). Hence R_15 < 49/100 ⟺ H(u) > T := (1500/49)² = 937.1095… on the domain Ω = {u ∈ (0,1]^15 : max_i u_i = 1}.

The smaller root of D is α = (13 − √113)/28. Since D(0.0846) > 0 > D(0.0847) and D decreases on [0, 13/28], α ∈ (0.0846, 0.0847).

**Step 0: H attains its minimum on Ω.**

- Σ w ≥ w(1) = 1/2, and a > 8/5 (Step 2). So H ≥ ½ (8/5)^14 a(u_i) for every i.
- Also a(u) ≥ u^{−2/15} because q ≥ 1.
- So on {H ≤ M} every u_i ≥ δ(M) > 0. This sublevel set is a closed subset of [δ,1]^15, hence compact, and the continuous H attains its minimum on it.

**Step 1: all coordinates below 1 share one value.**

Fix a minimizer and a coordinate u = u_i < 1. Some other coordinate equals 1, so u can vary in (0,1) inside Ω. Put C = Σ_{j≠i} w(u_j).

- Bounds on C: w > 0 on (0,1], so C > 0. Also ½ − w = (1 + 3u)(1 − u)/(2q) ≥ 0, so w ≤ ½ and C ≤ 7.
- Up to a positive factor, H is φ(u) = a(u)(C + w(u)) = u^{−2/15}(Cq + u²).
- The derivative satisfies (15/2) u^{1+2/15} φ'(u) = −β(u), with β(u) = C·D(u) − 14u². This holds because (15/2)u(Cq' + 2u) − (Cq + u²) = −C·D + 14u², a polynomial identity in u for each C.

Shape of β: β(0) = C > 0 and β(α) = −14α² < 0.

- If C ≤ 1: β is concave (leading coefficient 14(C − 1) ≤ 0; linear if C = 1) with β(0) > 0. So it has exactly one positive root, and β < 0 beyond it.
- If C > 1: β is convex and β(1) = 2C − 14 ≤ 0, so its second root is ≥ 1.

In both cases β has exactly one root u₀ in (0,1), with u₀ < α. Then φ decreases on (0,u₀) and increases on (u₀,1), so the minimizer has u = u₀ ∈ (0, α).

Putting all these coordinates on one scale:

- On (0, α), D > 0, so β(u) = 0 ⟺ C = 14u²/D.
- Since 14q + D = 15(1 + u), this gives A := C + w(u) = Σ_k w(u_k) = 15u²(1 + u)/(D q).
- So every coordinate below 1 satisfies L(u) := q D/(15 u²(1 + u)) = 1/A, with the same A for all of them.
- L'(u) = −2P(u)/(15u³(1 + u)²), where P(u) = 7u⁵ + 14u⁴ − 27u³ − 11u² − 4u + 1.
- On (0, α) ⊂ (0, 0.0847): P(u) > 1 − 4(0.0847) − 11(0.0847)² − 27(0.0847)³ = 0.5658… > 0.

So L is strictly decreasing on (0, α), and all coordinates below 1 are equal, to some t ∈ (0, α).

**Step 2: a(u) > 8/5 on (0,1].**

- a'/a = (15u q' − 2q)/(15u q), and 15u q' − 2q = −2D(u).
- So a decreases on (0, α), increases between the roots of D, and decreases on the rest of (0,1]. D(1) = 2 > 0, so both roots lie below 1.
- Hence min a = min(a(α), a(1) = 2).
- a(α) > q(0.0846)/0.0847^{2/15}, because q increases and u^{−2/15} decreases. This is > 8/5 ⟺ q(0.0846)^15 > (8/5)^15 · 0.0847², an exact rational inequality that holds (a(α) ≈ 1.6152).

**Step 3: two or more coordinates equal to 1.** If k ≥ 2 coordinates equal 1:

- Σ w ≥ k/2 and ∏ a ≥ 2^k (8/5)^{15−k}.
- The bound (k/2) 2^k (8/5)^{15−k} increases with k (ratio (k+1)/k · 5/4 > 1).
- So H ≥ 4 (8/5)^13 = 1801.4… > T.

**Step 4: exactly one coordinate equal to 1.** By Step 1 the other fourteen equal some t ∈ (0, α), and

H₁(t) = (½ + 14t²/q) · 2 · (q/t^{2/15})^14 = (1 + 2t + 27t²) q(t)^13 / t^{28/15},

using q + 28t² = 1 + 2t + 27t².

- Its log-derivative times 15t(1 + 2t + 27t²)q(t) equals 28(1 − t)·K(t), with K(t) = 378t³ + 25t² + 10t − 1 (polynomial identity).
- On (0,1) the factor 15t(1 + 2t + 27t²)q(t) is positive, so the sign of the log-derivative is the sign of K.
- K is increasing on t > 0, with K(0.07247) < 0 < K(0.07248). So H₁ decreases up to the root t₀ ∈ (0.07247, 0.07248) and increases after it, and H₁ ≥ H₁(t₀) on (0,1).
- Bound at t₀: 1 + 2t + 27t² and q increase, and t^{−28/15} decreases. So H₁(t₀) ≥ (1 + 2·0.07247 + 27·0.07247²) q(0.07247)^13 / 0.07248^{28/15} = 944.71…
- This exceeds T ⟺ (1 + 2·0.07247 + 27·0.07247²)^15 q(0.07247)^195 > T^15 · 0.07248^28, an exact rational inequality that holds. (H₁(t₀) itself is ≈ 944.96.)

Ω has at least one coordinate equal to 1, so Steps 3 and 4 cover every case. Therefore H > T on Ω, and R_15 < 49/100. ∎

**Margins and negative controls (tests):**

- The proof has about 0.8% of room in Step 4 (944.7 against 937.1).
- A target above the true minimum (T = 946, or r_15 = 0.487) correctly fails the Step 4 check.
- A float coordinate-descent search over Ω never goes below T, and finds the minimum ≈ 944.96 on the one-variable family. This search is a sanity check only, not part of the proof.

**Consequence.** Allikvere's Theorem 3.8 is stated and proved for general n. For n = 15 its ratio hypothesis holds: min c_{i+1}/c_i = 3751/2349 > 4/3, exact (`flag_bound.py`). Its other hypothesis is LRC(m) for all m < 15, i.e. up to 15 runners, which is Allikvere's certificate-based result re-checked in Approach 7.

With r_15 = 49/100 the theorem gives, for a primitive counterexample with 15 speeds, ln(v_1⋯v_15) < 15 ln(A_15 · (49/100)/15) = 496.727. With the forced divisor lcm(2..16) = 720720, the prime-gate target is 483.239.

At step 9 the general-n parts of Theorem 3.8 were only read, so the target was then labelled conditional on the cited theorem. They are verified in Approach 11 (step 10), which removes that condition.

### 11. Independent check of the general-n flag bound, Theorem 3.8 (step 10)

**Goal.** Verify the general-n parts of Allikvere's Theorem 3.8 (arXiv:2609.02604v2, §3, read from the v2 TeX source), so that the 16-runner target 483.239 no longer rests on the cited theorem. These are Lemmas 3.1, 3.2, 3.3, 3.5 and 3.6, Proposition 3.4 and the assembly.

**Result.** Every step checks out, and no gap or error was found. Where a step has a finite or numeric component, it is machine-checked in exact rational arithmetic (`computations/lonely-runner/flag_theorem_check.py`, tests `test_flag_theorem.py`, 13 tests including negative controls). The purely logical steps (Lemma 3.3, Proposition 3.4, Lemma 3.5) were checked line by line by reading. They have no finite component to machine-check.

The only inputs not re-proved here are:

- **Standard facts:** the existence of Korkine–Zolotarev bases; the Minkowski–Weyl decomposition of a pointed polyhedron; Schur-concavity of Σ log; Babai's nearest-plane rounding; elementary lattice duality.
- **Lower cases of the conjecture:** LRC(m) for m ≤ 14.

**Setting.** Here n ≥ 2 and v ∈ Z^n_{>0} is primitive. "Counterexample" means every real t has some i with ‖t v_i‖ < 1/(n+1). We use the following objects:

- S = Σ v_i, x = v/S, u = v/max v, and q_i = 1 + 2u_i − u_i² ∈ (1,2];
- H = v^⊥ and P, the orthogonal projection onto H;
- Λ = P Z^n, of rank d = n − 1;
- D = P[−1,1]^n and E = P Q^{1/2} B_2^n;
- ‖·‖_E, the norm on H whose unit ball is E.

**Lattice facts (used in Lemma 3.2).**

- **Covolume of Z^n ∩ H is ‖v‖.** The layers {z ∈ Z^n : ⟨v,z⟩ = k} of Z^n parallel to H are at spacing 1/‖v‖ (⟨v, Z^n⟩ = gcd(v) Z = Z), and det Z^n = 1.
- **Λ is the dual of Z^n ∩ H.** Extend a basis y_1, …, y_{n−1} of the primitive sublattice Z^n ∩ H to a basis of Z^n, and take its dual basis y_k^* (in Z^n). Then the P y_i^* (i < n) are the dual basis of Z^n ∩ H inside H, and P y_n^* = 0.
- **Hence det Λ = 1/‖v‖.** This is machine-checked exactly: an exact Hermite-form basis of P Z^n, at random primitive v for n = 3–6 (`check_covolume`).

**Lemma 3.1 (Inclusion, E ⊆ D): verified.** Both bodies are convex and closed in H, so E ⊆ D iff h_E ≤ h_D on H.

- **Support functions.** For y ∈ H, h_D(y) = sup_{x∈[−1,1]^n} ⟨Py, x⟩ = Σ |y_i|, and h_E(y) = sup_{|b|≤1} ⟨Q^{1/2}y, b⟩ = (Σ q_i y_i²)^{1/2}.
- **Reduction to vertices.** By homogeneity it suffices that Σ q_i y_i² ≤ 1 on the polytope {y ∈ H : Σ|y_i| ≤ 1}. The left side is convex, so it suffices at the vertices.
- **The vertices.** The vertices of a hyperplane section of a polytope are its intersections with edges, together with any polytope vertices lying in the hyperplane. No ±e_i lies in H (v_i ≠ 0). Edges between same-sign vertices miss H (v > 0). The segment from e_i to −e_j meets H at y = (v_j e_i − v_i e_j)/(v_i + v_j).
- **The check at a vertex.** There Σ q y² ≤ 1 ⟺ (q_i − 1)v_j² + (q_j − 1)v_i² ≤ 2 v_i v_j. With q − 1 = u(2 − u) and v = M u, the difference of the two sides equals −2M² u_i u_j (1 − u_i)(1 − u_j) ≤ 0.

Machine checks:

- the identity, exactly, at 200 random rational points;
- every vertex point, exactly, for random v with n = 3–7;
- h_E(y)² ≤ h_D(y)² at random rational y ∈ H, a sample check of the conclusion;
- negative control: with q replaced by 1 + 2u, the inclusion fails, as it must.

**Lemma 3.2 (Covolume, covol_E(Λ) = 1/(S F_n(x))): verified.**

- **The E norm.** By definition, ‖y‖_E = min{|z| : P Q^{1/2} z = y}. Writing Q^{1/2} z = y + λv and minimizing over λ gives ‖y‖_E² = yᵀ M y, with M = Q^{−1} − Q^{−1}v vᵀQ^{−1}/(vᵀQ^{−1}v).
- **The paper's computation.** It uses the Gram matrix (UᵀQU)^{−1} and the Schur-complement identity det(UᵀQU) = det Q · ṽᵀQ^{−1}ṽ. It agrees with this formula, and it gives covol_E² = det Λ² / det(UᵀQU) = 1/(∏q_i · Σ v_i²/q_i) = 1/(S² F_n(x)²).
- **Machine check.** At 20 random primitive v (n = 3–6), the Gram determinant of an exact Z-basis of Λ in the form M equals 1/(S² F_n²) exactly. It is computed directly from the definition of E, independently of the paper's U-coordinates. Negative control: a wrong F fails.

**Lemma 3.3 (Separated points on rational subspaces; Giri–Kravitz Lemma 3.3): verified by reading.**

*Statement.* Let 1 ≤ q ≤ n and assume LRC(m) for m ≤ n+1−q. Then every rational q-dimensional V ⊆ R^n with no identically vanishing coordinate contains s with ‖s_i‖ ≥ 1/(n+2−q) for all i.

*Base case, q = 1.* V = R a with a primitive and all a_i ≠ 0. The |a_i| take m ≤ n distinct values, so LRC(m) gives t with ‖t a_i‖ ≥ 1/(m+1) ≥ 1/(n+1).

*Induction step, q ≥ 2.* The restrictions a_k of the coordinate functionals to V are nonzero and span V*, so not all are proportional.

- Take a non-proportional pair (i, j) minimizing the angle between their lines, and fix the sign so that ⟨a_i, a_j⟩ ≥ 0.
- h = a_i + a_j lies strictly inside that angle. So, by minimality, no a_k is proportional to h: such an a_k would form a pair with a_i at a smaller angle.
- V' = V ∩ {y_i + y_j = 0} is rational of dimension q − 1. a_k vanishes on V' iff a_k ∈ R h, so no coordinate vanishes on V'.
- Deleting coordinate j is injective on V' (y_j = −y_i). The image V'' is rational and has no vanishing coordinate.
- Induction applies in R^{n−1} with q − 1. It needs LRC(m) for m ≤ n+1−q, the same range, and gives distance 1/((n−1)+2−(q−1)) = 1/(n+2−q).

Each step was checked, including the edge cases: the sign flip leaves ‖·‖ unchanged, and the pair minimizing the angle exists because there are finitely many pairs.

**Proposition 3.4 (Prefix inequalities, t_1 + … + t_r > B_r = (2r/((n+1)(n+1−r)))²): verified by reading.** Take any basis b_1, …, b_d of Λ, its E-Gram–Schmidt vectors b_i^*, and t_i = ‖b_i^*‖_E². Choose z_i ∈ Z^n with P z_i = b_i, and let V = span(v, z_1, …, z_r).

1. **V is admissible for Lemma 3.3.** It has dimension r + 1 (apply P to a linear relation) and is rational. No coordinate vanishes on it (v > 0).
2. **A separated point.** Lemma 3.3 with q = r + 1 needs LRC(m) for m ≤ n − r ≤ n − 1. It gives s = a v + Σ a_i z_i with ‖s_k‖ ≥ 1/(n+1−r).
3. **Rounding.** Nearest-plane rounding gives integers k_i with e = Σ(a_i − k_i) b_i = Σ θ_i b_i^*, |θ_i| ≤ ½. So ε = ‖e‖_E ≤ ½ (t_1 + … + t_r)^{1/2}.
4. **From E to D.** By Lemma 3.1, e ∈ εE ⊆ εD, so e = P y with |y_k| ≤ ε.
5. **A time t.** Σ(a_i − k_i) z_i − y lies in ker P = R v. Hence s − Σ k_i z_i − y = t v for some t, and ‖t v_k‖ ≥ ‖s_k‖ − |y_k| ≥ 1/(n+1−r) − ε.
6. **Conclusion.** If ε ≤ 1/(n+1−r) − 1/(n+1) = r/((n+1)(n+1−r)), then t is a witness, which is impossible. So 4ε² > B_r, and t_1 + … + t_r ≥ 4ε² > B_r.

Every step was checked, including the strict inequality and the LRC range.

**Lemma 3.5 (KZ, t_{i+1} ≥ ¾ t_i): verified by reading (standard).**

- In a KZ basis, b_i^* is a shortest nonzero vector of the projected lattice π_i(Λ).
- π_i(b_{i+1}) = b_{i+1}^* + μ b_i^* with |μ| ≤ ½ is nonzero in π_i(Λ).
- So t_i ≤ t_{i+1} + t_i/4. KZ bases exist for every lattice (Korkine–Zolotarev 1873; Lagarias–Lenstra–Schnorr 1990), in any Euclidean norm.

**Lemma 3.6 (Product minimization, ∏ t_i ≥ ∏ c_i = K_n under c_{i+1}/c_i > 4/3): verified.**

1. **Change of variables.** Put z_i = t_i/ρ^{i−1}. The constraints become z_1 ≤ … ≤ z_d and Σ_{i≤r} w_i z_i ≥ B_r. They define a polyhedron Π in the open positive orthant (z_1 ≥ B_1 > 0).
2. **Reduction to vertices.** Π's recession cone is {0 ≤ z_1 ≤ … ≤ z_d}: the r = 1 constraint forces dz_1 ≥ 0. So Π is pointed and is the convex hull of its vertices plus that cone. f = Σ log(w_i z_i) is concave and nondecreasing, so f ≥ its minimum over the vertices.
3. **Structure of a vertex.** At a vertex, the β maximal blocks of equal z use d − β monotonicity constraints, so at least β prefix constraints are active.
   - None is active strictly inside a block (a, b]. Activity at r with feasibility at a gives ζ ≤ (weighted mean of c_i/w_i over a < i ≤ r) ≤ c_r/w_r. Here c_i > 0 by induction, and c_i/w_i strictly increases because (c_{i+1}/c_i)/ρ > 1/ρ² > 1. Activity at r with feasibility at r + 1 gives ζ ≥ c_{r+1}/w_{r+1} > c_r/w_r. These contradict each other.
   - So all β block ends are active, and on each block t is geometric with ratio ρ and the same sum as c over the block.
4. **Comparison within a block.** Ratio comparison shows that c↓ majorizes the geometric g (both decreasing, with equal totals). Schur-concavity of Σ log then gives ∏_block c ≤ ∏_block t.
5. **The minimum is attained.** t = c is feasible.

Machine checks, exact, with the actual B_r of each n:

- **(a) Brute-force vertex enumeration, d ≤ 7.** All d-subsets of the 2d − 1 constraints are solved and filtered for feasibility. There are exactly 2^{d−1} vertices, each the block point of a composition of d, as the lemma's structure claim says, and each has ∏ t ≥ K_n.
- **(b) Block points, n = 13, 14, 15.** All 2^{d−1} block points (8,192 at n = 15) are feasible and have ∏ t ≥ K_n, with equality only at t = c. K_14 equals the paper's value.
- **(c) Random feasible points (float).** All have ∏ t ≥ K_n.
- **Negative control.** For prefix constants with c_{i+1}/c_i < 4/3, a single geometric block is feasible and has a smaller product, so the hypothesis is needed.

**Assembly (Theorem 3.8): verified.** Take a KZ basis in the E norm.

- Proposition 3.4 and Lemma 3.5 give the hypotheses of Lemma 3.6, so covol_E(Λ)² = ∏ t_i ≥ K_n.
- Lemma 3.2 then gives S F_n(x) ≤ A_n = K_n^{−1/2}.
- With R_n < r_n: n (∏ v_i)^{1/n} = n S (∏ x_i)^{1/n} = S F_n R_n < r_n A_n.
- For n = 15, the ratio minimum is 3751/2349 > 4/3 (exact) and r_15 = 49/100 (Approach 10). Hence ln(v_1⋯v_15) < 496.72677196, and the prime-gate target after ln 720720 is 483.23876597. Both are computed to 40 digits; n = 14 reproduces the paper's 414.77936455669981.

**Consequence.** For a primitive counterexample with 15 speeds (16 runners), assuming LRC(m) for m ≤ 14: v_1⋯v_15 < e^{496.7268}. The 16-runner gate target 483.239 is therefore **proved here**, modulo:

- **LRC(13) and LRC(14)**, the 14- and 15-runner cases. These are Allikvere's certificate-based results: LRC(14) is re-checked in Approach 7, fully at 54 of 71 gates, with level-one completeness at 3; LRC(13) is re-checked only through its terminal kills. LRC(m) for m ≤ 12 comes from the literature.
- **The standard facts listed above.**
- **The forced divisor** (Rosenfeld Lemma 4), which is elementary (see "The finite reduction").

It no longer depends on citing Theorem 3.8.

## Independent re-check summary

Scope: J. Allikvere's computer-assisted proofs of LRC(13) and LRC(14), i.e. 14 and 15 runners (arXiv:2609.02604v2). Certificates: Zenodo 10.5281/zenodo.22066772 and 10.5281/zenodo.22667683. All checks use our own code (C and Python, in `computations/lonely-runner/`), written from the definitions in the paper and in arXiv:2604.23906. The archives were read as data only; none of the author's programs were executed.

**What an outside reader can rely on (LRC(14), 71 gate primes):**

- **Archive integrity: all 71 gates.** Each archive's SHA-256 equals the published `SHA256SUMS.txt` entry. 58 archives were kept; 13 were checked on download and then deleted.
- **Stored level-one rows: all 71 gates, every row.** Every stored irredundant row is witness-free at level 1, i.e. lies in I(14,p,1). Every stored km1 multiset is a cover. That is 495,538,971 stored irredundant rows in total.
- **Binary cascade, levels 2–32.** In full at all 52 "J(14,p) = ∅" gates and at the near-gcd gates p = 179, 223 and 233 (step 8). At the other 16 near-gcd gates, on seeded uniform samples of stored rows (compared both ways) and of extension-survivor lines: 3,000 at p = 89, 163, 173; 500 at the 13 large archives. There were 0 mismatches.
- **Level-15 kill records.** In full at the 52 "J empty" gates (one persistent orbit, (1..14), each) and at p = 179 (all 8,011 orbits) and p = 233 (all 13,457 orbits). At the other near-gcd gates, on seeded samples of the same sizes. Every record checked is reproduced exactly: level-3/5 witness-free lifts, CRT candidates, level-15 grid, gcd clause, and the few-exception shift Lemma 3.12. Improper after Lemma 3.12 is 0 everywhere, and improper after the gcd clause is 0 at the "J empty" gates. At the stream-checked gates, the number of kill files equals the certificate's persistent-orbit count.
- **Level-one completeness at 3 gates.** At p = 89 (near-gcd), p = 239 and p = 251 ("J empty"), an independent minimal-cover enumeration reproduces exactly the certificate's set of level-one orbits: 687,016, 1,441,284 and 2,404,346 orbits. The runs at 89 and 239 are unpruned; the run at 251 uses our implementation of the private-time pruning (Approach 8).
- **Constants.** The flag-bound constants K_14, A_14, the log bound 414.779365 and the target 401.984506 were re-derived exactly. The 71 gates' Σ ln p = 408.8233 exceeds the target, recomputed from the gate list.
- **LRC(13).** At all 111 gate primes, the terminal level-14 kill of both persistent orbits was recomputed and matches, and the kill files' SHA-256 match the gate manifests.
- **No discrepancy with any certificate was found.**

**What remains unverified here:**

- **Level-one completeness at the other 68 LRC(14) gates.** That every orbit of I(14,p,1) is represented among the stored rows is checked only at p = 89, 239 and 251. At all other gates it rests on Allikvere's generator and its completeness proposition (his Prop. 4.2 with the private-time Lemma 4.1). We implemented Lemma 4.1 (Approach 8) but have run it to completeness only at p = 251.
- **The sampled parts at the 19 near-gcd gates.** The unsampled cascade rows and kill records there were not re-computed.
- **The analytic inputs.** The finite-checking bound (Malikiosis–Santos–Schymura, via Rosenfeld's Cor. 3) was not re-proved. Allikvere's flag bound (Thm 3.8) is now independently verified: the shape Lemma 3.7 is re-checked for n = 13 and 14 and extended to n = 15 (Approach 10), and its general-n Lemmas 3.1–3.6 and assembly are checked in Approach 11, resting only on standard facts (KZ bases, Minkowski–Weyl, Schur-concavity). Not re-proved, beyond reading their proofs, are the prime-divisibility Lemma 2.2(ii) and the few-exception shift Lemma 3.12. The lower cases LRC(m), m ≤ 12, are taken from the literature.
- **LRC(13).** The archive does not contain the k = 13 level-one rows, so the rows, cascade and completeness cannot be re-checked from it.
- **Our own code is not formally verified.** It is tested against brute force on small cases (18 tests) and against the certificates' own numbers.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| `find_witness` is a complete decision procedure; ML(v) is attained at some a/(v_i+v_j) | proved (short proofs in docstring) | `lonely.py` |
| ML(1, …, n) = 1/(n+1) exactly, n ≤ 10; ML(1,3,4,7) = 1/5 | computed exactly | `test_lonely.py` |
| Every primitive tuple with max speed ≤ N has a witness at 1/(n+1): (n, N) = (3, 150), (4, 60), (5, 32), (6, 22), (7, 18) | computed up to N | `results/exhaustive.txt` |
| Tight primitive tuples in those ranges: (1,2,3); (1,2,3,4), (1,3,4,7); (1,…,5), (1,3,4,5,9); (1,…,6); (1,…,7), (1,2,3,4,5,7,12), (1,4,5,6,7,11,13) | computed up to N | `results/exhaustive.txt` |
| Sieve, naive level one, cover generator and `liftfree.c` agree with each other and with brute force from the definitions | tested (21 tests; 125 (k,p) pairs for the generator) | `test_lonely.py` |
| LRC(3) … LRC(8) (4–9 runners); gate sets in `results/lrc_k*.jsonl`; the k = 8 set equals Trakulthongchai's S_8 | certificate-checked computation **+ cited B_k** | `results/lrc_k3..8.jsonl` |
| LRC(9) (10 runners): all 47 primes 137…401 pass (identical to Trakulthongchai's S_9), Σ ln p = 259.94 > 254.30; cover generator, chain ×2×2×2, proj, ×5×2; 1,313 s wall on 4 processes | certificate-checked computation **+ cited B_k** | `results/lrc_k9.jsonl` |
| LRC(10) (11 runners): all 61 primes 127…467 pass (identical to Sungkawichai–Trakulthongchai's P_10), Σ ln p = 342.72 > ln B_10 = 337.63 (exact test `prod_ge_B_k_exact`); cover generator, chain ×2×2×2, proj, ×11 (`liftfree.c`); in every gate only (1..10) survives the ×2 lifts and the ×11 lift kills it; 13,924 s wall (about 13.8 core-hours, almost all level one) on 4 processes. Depends on cited B_10, LRC(9) and tested-not-verified code; does **not** use Prop. corlarge (Next steps 6) | certificate-checked computation **+ cited B_k** | `results/lrc_k10.jsonl` |
| Allikvere constants: K_13, K_14, ratio minima, ln bounds 341.031991 and 414.779365, target 401.984506 | exact rational re-derivation | `flag_bound.py` |
| n = 15 flag constants: K_15, ratio min 3751/2349 > 4/3 | exact | `flag_bound.py` |
| n = 15 shape lemma R_15 < 49/100 (min of H ≈ 944.96 > (1500/49)²), hence ln(v_1⋯v_15) < 496.727 and gate target 483.239 | shape lemma **proved** (written proof, every inequality exact-checked); the general-n Thm 3.8 is **verified** (Approach 11; Lemmas 3.1, 3.2, 3.6 machine-checked exactly, 3.3–3.5 by reading), so the target is **proved given LRC(m), m ≤ 14** and standard facts | Approaches 10–11, `shape_lemma.py`, `flag_theorem_check.py`, tests |
| 4 of 71 LRC(14) gate certificates (p = 263, 311, 397, 401): rows improper, cascade and kill reproduced | independent re-computation of the certificate's claims **except level-one completeness** | `check_allikvere.py`, `results/allikvere_spotcheck.jsonl` |
| LRC(14) certificates: independent re-check of 71/71 gates. All 52 "J empty" gates and near-gcd gates 179 and 233 in full; cascade also in full at 223. Near-gcd gates 89, 163, 173, 223 (sample 3,000) and 131, 149, 157, 167, 181, 191, 193, 197, 199, 211, 227, 229, 241 (sample 500): all rows, plus seeded samples of the cascade and kill. Level-one completeness at p = 89, 239 and 251. No discrepancy found. | independent re-computation of the certificates' claims; cascade sampled at 16 and kill at 17 of the 19 near-gcd gates; completeness at 3 gates only | `results/lrc14_gates/COVERAGE.md`, Approach 7 |
| LRC(13) certificates: terminal level-14 kill of both persistent orbits re-computed at all 111 gate primes; kill-file SHA-256s match manifests | independent re-computation (cascade and level one not checkable: rows not archived) | `results/lrc13_kills.jsonl` |
| (1..15) dies at level 16 at all 79 primes 251–743 | computed exactly (one orbit only) | `results/tight_orbit_k15.jsonl` |
| Cost of LRC(15) level one + kill with Allikvere-class code: about 1.75·10⁵ CPU-h (about 20 CPU-years) for 79 gates 251–743 under the flag target 483.24 (proved, Approaches 10–11); about 8.7·10⁶ CPU-h under the proved B_15 | **heuristic extrapolation from measurements** | `cost_estimate.py`, `results/knuth_covergen_k14_k15.txt` |

"Certificate-checked computation + cited B_k" means the following. The chain LRC(2) ⇒ … ⇒ LRC(9) is a proof *if* three things hold:

- the MSS bound in Rosenfeld's Corollary 3 form,
- the elementary lemmas above,
- the correctness of our code.

Our code is tested against brute force, but not formally verified. These reproduce *known* cases only. Nothing new is claimed.

## Next steps: plan for LRC(15) (16 runners)

1. **Bound.**
   - Done (steps 9–10): R_15 < 49/100 is proved (Approach 10), and the general-n parts of Theorem 3.8 are independently verified (Approach 11). So the 16-runner gate target 483.239 is proved, given LRC(m) for m ≤ 14.
   - Without Theorem 3.8, the only target from MSS is ln B_15 − ln 720720 = 951.26. That needs about 147 gates up to 1223, which is roughly 50× the cost below.
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
   - full cascade and kill at near-gcd gates 163 and 173. These are **beyond this session's budget** (re-timed costs below) and are not being run;
   - the 13 near-gcd archives over 60 MB (0.1–1.6 GB; p = 181 has 8.2M orbits);
   - full rather than sampled cascade and kill at near-gcd gates 89 and 223 (the kill only at 223). p = 179 and p = 233 are done in full, and the full cascade at p = 223 is done (step 8). The full cascade at 89 is beyond budget and is not being run. The full kills at 223 and 89 are beyond budget and not run. p = 233 is now done in full, cascade and kill (`gate_233_full.json`; 10,703 s on 4 processes, about 11.9 core-hours).
   - Measured cost (step 8, single core): the kill takes 1.4–2.2 s per orbit and the cascade about 1 ms per row. Full kills would cost about 8.3 core-hours at 233 (13,457 orbits), 28.8 at 223 (48,071), 53.7 at 173 (96,840), 63.9 at 163 (107,244) and 70.5 at 89 (186,365). The earlier "about 0.5 s per orbit" was wall time per orbit on 4 processes. Full cascades (without kills) were first estimated at 0.5–3 core-hours per gate. That estimate timed only stored (ir) rows. The cascade input is the ir rows followed by the improper extension rows (km1 cover × x), and an extension row costs 30–80 times as much as an ir row. Re-timed on the fixed `check_gate_full.py` (step 8, 2026-11-25; 2,000 ir rows and 60 extension rows per gate, single core, seeded), the projected full-cascade costs in core-hours are:
    - 233: 0.7 (ir) + 5.9 (782,536 ext);
    - 223: 0.2 + 8.9 (328,893 ext);
    - 163: 0.8 + 14.3 (3,722,274 ext);
    - 173: 0.9 + 32.7 (2,901,296 ext);
    - 89: 0.05 + 32.7 (855,976 ext; 0.14 s per ext row).
    - Check against a finished run: p = 223 took 8,999 s on 4 processes, about 10.0 core-hours, close to the sampled 9.1. A mid-run projection from the live read rate (about 25 core-hours) was misleading, because the expensive extension rows are clustered in the input.
    - Two attempts have been lost so far. The first p = 89 attempt (2026-11-24) ran serialised by a pipe bug, fixed in #61, and was stopped. The first p = 223 run was killed by a container restart.
    - Status: the p = 223 full cascade is done (pass, above). The p = 233 full cascade is done (pass, 3,634 s on 4 processes, about 4.0 core-hours, below the sampled 6.6). Gates 89, 163 and 173 are beyond budget (about 33, 15 and 34 core-hours for the cascade alone) and are not being run; they stay sampled.
   - level-one completeness at more gates. Unpruned, p = 239 took about 4.4 core-hours; with `LRC_PRUNE=2`, p = 251 took about 8.4 core-hours (8.93·10¹⁰ nodes). The pruning gives only a modest node saving at these primes (Approach 8), so cost grows quickly with p. The next "J empty" gate, p = 257, is estimated (Knuth probes calibrated on the 239 and 251 runs, `results/knuth_completeness_257.txt`; heuristic) at 2.16·10¹¹ nodes, about 20 core-hours. It was not run. A faster generator is the precondition for many more completeness gates. Approach 9's sharper gain bound gives about 1.7×, which brings p = 257 to about 12 core-hours; that is still not enough.
6. **LRC(10) (11 runners): done (step 7), with the label in the Results table.** Chain ×2 ×2 ×2, projection, ×11, with the ×11 lift done by `liftfree.c` (`sieve.lift_c`, tested equal to the Python `lift`). All 61 gates 127…467 pass and ∏p ≥ B_10 holds exactly; see `results/lrc_k10.jsonl` and the SUMMARY line. Failed gates: none in this range (the run started at 127, P_10's first prime; we did not test p < 127). This differs from Sungkawichai–Trakulthongchai, who avoid the ×11 lift via their Prop. (corlarge, p > k² + k). Their P_10 is all 61 primes from 127 to 467 (Σ ln p > 342 > ln B_10 ≈ 337.63; read in the arXiv:2604.23906v2 source, Table 2).
   - **Dependencies of our LRC(10) chain.** It is the same trust base as for LRC(3)–LRC(9) (see "Certificate-checked computation + cited B_k"):
     - the cited bound B_10 = (C(11,2)⁹/10)^10, i.e. Malikiosis–Santos–Schymura in the form of Rosenfeld's Cor. 3;
     - LRC(9) (Trakulthongchai; also reproduced here);
     - the elementary lemmas F1, F2 and the prime-divisibility Lemma 2.2 / Cor. 2.4 of arXiv:2604.23906, with proofs written out above;
     - the correctness of `covergen.c`, `sieve.py` and `liftfree.c`, which are tested but not formally verified.
   - **Independence.** The chain does **not** use Sungkawichai–Trakulthongchai's Prop. corlarge, nor the footnoted inclusion for p ∈ {103, 107, 109}. The tight orbit (1..10) is killed by an explicit ×11 lift. It also uses no flag bound and no forced divisor lcm(2..11).
7. **Independent replay of 15 runners.** With the faster generator from step 2, rerun a handful of small k = 14 gates in full, including level-one completeness. This would upgrade the spot check.
8. **Do not** present any of this as a proof until every gate has stored, re-checkable output and the bound is proved.
