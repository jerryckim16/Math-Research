# Lonely Runner Conjecture

**Area:** Diophantine approximation / combinatorics
**Status:** in progress. The prime-gate framework is reproduced for 4–9 runners, conditional on one cited bound (B_k); the next open case is 16 runners.
**Started:** 2026-11-23
**ProofAtlas:** rank 477

## Statement

Write ‖x‖ for the distance from x to the nearest integer.

**Conjecture (Wills 1967; Cusick 1973).** Let n ≥ 1 and let v_1, …, v_n be
positive integers. Then there is a real t with

  ‖v_i t‖ ≥ 1/(n+1) for all i = 1, …, n.

Interpretation: there are n+1 runners on a circular track of length 1, with
one runner at rest. At some time t every moving runner is at distance at
least 1/(n+1) from the runner at rest. In the conjecture's original form,
runners have distinct real speeds and *each* runner is lonely at some time.
That form reduces to positive integer speeds with one runner at rest
(Bohman–Holzman–Kleitman; Henze–Malikiosis; cited from the introduction of
arXiv:2604.23906). Repeated speeds are harmless: if there are k' < n distinct
values, then 1/(k'+1) > 1/(n+1).

Following the recent literature, write **LRC(k)** for the statement with
k = n speeds. LRC(k) is "the conjecture for k+1 runners".

The bound 1/(n+1) cannot be improved. Speeds (1, 2, …, n) attain it exactly
(re-checked below for n ≤ 10).

**Next open case (as far as located): LRC(15), i.e. 16 runners**: every
15-tuple of positive integers has a t with all ‖v_i t‖ ≥ 1/16. This is
conditional on the 14- and 15-runner preprint of Allikvere being correct.
If that preprint is not accepted, the first case without a located claim is
still 16 runners. The first case that is not peer-reviewed is 11 runners
(see the table).

## Known results

Sources marked **[read]** were read in full-text source form. Those marked
**[abstract]** were seen only via abstracts, search snippets or secondary
pages, because arxiv.org, combinatorics.org and zenodo.org are blocked by
this session's network policy. Literature checked on 2026-11-23.

| runners | k | result | source | how checked |
| --- | --- | --- | --- | --- |
| 2, 3 | 1, 2 | trivial | classical | |
| 4 | 3 | proved | Betke–Wills 1972; Cusick 1974 | cited in [read] intro of arXiv:2604.23906 |
| 5 | 4 | proved (computer-assisted) | Cusick–Pomerance 1984; simpler proof Bienia et al. 1998 | as above |
| 6 | 5 | proved | Bohman–Holzman–Kleitman 2001; simpler proof Renault 2004 | as above |
| 7 | 6 | proved | Barajas–Serra, *Electron. J. Combin.* 15 (2008) R48, arXiv:0710.4495 | [abstract] |
| 8 | 7 | proved (computer-assisted) | M. Rosenfeld, arXiv:2509.14111 (Sep 2025), reportedly *Math. Comp.* 2026 | [abstract]; method [read] via arXiv:2604.23906 |
| 9 | 8 | proved (computer-assisted) | T. Trakulthongchai, arXiv:2511.22427, *Electron. J. Combin.* 33(2) (2026) #P2.46; independently M. Rosenfeld, arXiv:2512.01912 | [abstract] |
| 10 | 9 | proved (computer-assisted) | Trakulthongchai, same paper | [abstract] |
| 11, 12, 13 | 10–12 | claimed (computer-assisted preprint) | T. Sungkawichai, T. Trakulthongchai, "Eleven, twelve, and thirteen lonely runners", arXiv:2604.23906 (Apr 2026); code at github.com/vzsky/lonely-runners | **[read]**: LaTeX source `article/article.tex` on the repo's `latest` branch |
| 14 | 13 | claimed (computer-assisted preprint) | J. Allikvere, arXiv:2609.02604 (2 Sep 2026), v1 "Fourteen lonely runners" | [abstract]: "certifies 111 prime gates with Σ log p > 681.5292, exceeding … log B_13 < 670.3498" |
| 15 | 14 | claimed (preprint v2, retitled "Fourteen and fifteen lonely runners") | Allikvere, same arXiv number; about 2,140 CPU-hours reportedly; certificates on Zenodo (10.5281/zenodo.22667683) | [abstract] / secondary only: search snippets and the README of github.com/munimtechnologies/lonely-runner-16 (an AI-made repository, unreviewed) |
| 16 | 15 | **open** | — | |

### Results for general n

- The trivial bound is 1/(2n).
- Tao (2018) proved 1/(2n) + c·log n/(n²(log log n)²).
- Bedert (arXiv:2511.16636, 2025) proved 1/(2n) + 1/n^{5/3+o(1)} [cited in the read intro].
- Hu–Jing, "Near optimal gap in the lonely runner conjecture", arXiv:2610.23790 (Oct 2026), reportedly proves (1+c)/(2n) for an absolute c > 0. [Seen via MathWorld only; not read.]
- None of these settles any finite case.

### The finite reduction (exact hypotheses)

These items are taken from the [read] source arXiv:2604.23906, §2.

- **Reduction to bounded speeds.**
  - Tao (2018) showed that speeds of size n^{O(n²)} suffice.
  - Malikiosis–Santos–Schymura, "Linearly-exponential checking is enough for the Lonely Runner Conjecture and some of its variants", *Forum Math. Sigma* 13 (2025) e164, arXiv:2411.06903, Thm 1.1.
  - Rosenfeld's **Corollary 3** packages that result as follows. *Let k ≥ 3. If LRC(k−1) holds, then every counterexample u to LRC(k) with gcd(u) = 1 satisfies*

    u_1⋯u_k < B_k := ( C(k+1,2)^{k−1} / k )^k.

  - Values: ln B_k = 7.45, 22.09, 46.11, 80.59, 126.33, 184.0, 254.3, 337.6, 434.5, 545.3, 670.3, 810.1, 964.8 for k = 3, …, 15.
  - Allikvere replaces B_k by a smaller "flag bound" from Korkine–Zolotarev inequalities. Per secondary sources, ln ≈ 415 for k = 14 and ≈ 496.7 for k = 15, the latter derived in the munim repository and not by Allikvere. Not verified here.
- **Prime gates.** Fix k ≥ 2, a prime p and l ≥ 1. Put N = lp and Z_{p,l} = {x ∈ Z_N : p ∤ x}. Call w ∈ Z_{p,l}^k *(k,p,l)-proper* if
  - (a) gcd(l, w_1, …, ŵ_i, …, w_k) > 1 for some i, or
  - (b) some t ∈ (1/N)Z has ‖t w_i‖ ≥ 1/(k+1) for all i.

  I(k,p,l) is the set of improper tuples. J(k,p) is the set of v ∈ Z_{p,1}^k that lie in π(I(k,p,l)) for every l ("not eventually proper").
- **Lemma D** (Trakulthongchai, Lemma 5). Let k ≥ 3. If LRC(k−1) holds and I(k,p,l) = ∅ for some l, then p | u_1⋯u_k for every counterexample u to LRC(k).
- **Lemma E** (arXiv:2604.23906, Lemma 2.4). J(k,p) = ∅ iff I(k,p,l) = ∅ for some l.
- **Proposition V** (arXiv:2604.23906, Prop. 2.6). Let k ≥ 3, assume LRC(k−1), and let P be a set of primes with J(k,p) = ∅ for every p ∈ P. If ∏_{p∈P} p ≥ B_k, then LRC(k) holds.
- **Tight tuples force l.** By Remark 3.2 there, (1, …, k) is lonely exactly at t = s/(k+1) with gcd(s, k+1) = 1. So for p > k+1, I(k,p,l) = ∅ requires (k+1) | l.
- **Sungkawichai–Trakulthongchai, Prop. 1.2.** Suppose k+1 and p are odd primes with p > k² + k. Then every gcd-1 tuple u with u_i ≡ i (mod p) has the LR property.
- **Primes used there:**
  - k = 10: 61 primes from 127 to 467 (Σ ln p > 342 against ln B_10 < 338).
  - k = 11: 76 primes from 23 to 577.
  - k = 12: 92 primes from 167 to 733.
- **Cost model.** Their heuristic time model is ∝ p^{(k+1)/2}/(k·2^k). They report k = 10 in 45 min on a 10-core M4, and estimate "15 years on our original machine" for LRC(13) with their algorithm. Allikvere's different level-one generator is what made 14 and 15 runners feasible.

Other relevant work, [abstract] only:

- Blanco–Criado–Santos, arXiv:2603.24784, give counterexamples to the *shifted* LRC from n = 5. This does not affect the unshifted conjecture.
- Goddyn–Wong (2006) studied tight tuples.
- Zhang, arXiv:2608.13599, studied tight one-entry modifications of [n−1].

## Elementary lemmas used by our reproduction (proofs)

**Witness transfer.** If u ≡ w (mod N) and t = m/N, then u_i t − w_i t ∈ Z, so ‖u_i t‖ = ‖w_i t‖.

**Lemma D (proof).** Take a counterexample u. We may assume gcd(u) = 1 (replace t by t·g). Suppose that p ∤ u_i for every i, and let w = u mod lp ∈ Z_{p,l}^k. Since I(k,p,l) = ∅, w is proper.

- If (b) holds, witness transfer makes u lonely, which is a contradiction.
- If (a) holds, let d = gcd(l, w_j : j ≠ i) > 1.
  - Then d | u_j for j ≠ i, since d | l | N.
  - Because gcd(u) = 1, gcd(d, u_i) = 1.
  - LRC(k−1), applied to (u_j)_{j≠i} (repeats allowed, see the statement), gives t_0 with ‖u_j t_0‖ ≥ 1/k for j ≠ i.
  - The times t_0 + r/d (r = 0, …, d−1) leave every u_j t_0 unchanged mod 1, and move u_i t_0 through a full coset x + (1/d)Z.
  - One of these points is within 1/(2d) of 1/2, so its ‖·‖ is ≥ 1/2 − 1/(2d) ≥ 1/4 ≥ 1/(k+1), using k ≥ 3.
  - Since 1/k > 1/(k+1), this t is a witness for u, which is again a contradiction. ∎

**F1 (improperness projects).** Let w be improper at level clp, and let w′ = w mod lp.

- If w′ had a witness t ∈ (1/lp)Z, then t ∈ (1/clp)Z would be a witness for w.
- If w′ satisfied (a) via d | l, then d | cl, and d divides the corresponding w_j because w ≡ w′ (mod lp) and d | lp.

So w′ is improper. Consequently, start from S_1 = I(k,p,1) and repeatedly apply "replace S by all its improper lifts by c" or "reduce S mod p". Every v ∈ J(k,p) keeps a preimage in every stage. If the final stage is empty, J(k,p) = ∅. (This is Prop. 3.1 of arXiv:2604.23906.)

**F2 (symmetry).** Properness is invariant under permutations, sign changes of coordinates, and multiplication by a unit a of Z_N. Use the witness t·a^{−1}, and note that gcd(l, a·x) = gcd(l, x).

- Z_{cN}^* → Z_N^* is onto, so lifts of one orbit representative cover the lifts of the whole orbit.
- At level 1, every orbit contains a tuple (1, a_2 ≤ … ≤ a_k) with 1 ≤ a_i ≤ (p−1)/2.

**Lemma E (proof of ⇒).** Pick, for each v ∈ Z_{p,1}^k, an l_v at which v has no improper lift. Let l = lcm(l_v). Any w ∈ Z_{p,l}^k reduces to a proper tuple at level l_v·p over v, and that properness transfers up to level lp (witness or gcd, as in F1). ∎

## Approaches

### 1. Exact checker for one tuple (done)

- **Idea:** decide "∃t: ‖v_i t‖ ≥ δ ∀i" exactly.
  - Each good set G_{v_i} is a finite union (mod 1) of closed intervals [(m+δ)/v_i, (m+1−δ)/v_i].
  - If ∩G_{v_i} is nonempty, it contains a left endpoint. (Take s = max of the left endpoints of the intervals containing a point.)
  - So it suffices to search the Σv_i left endpoints. A failed search yields a certificate: one failing index per endpoint.
  - ML(v) = max_t min_i ‖v_i t‖ is attained at some t = a/(v_i+v_j), with i = j allowed. (At a maximum, an increasing active piece meets a decreasing one, or a peak is active.)
  - Proofs are in the docstring of `computations/lonely-runner/lonely.py`.
- **Outcome:** worked.

### 2. Prime-gate sieve, reproduced end to end for 4–9 runners (done)

- **Idea:**
  - Compute I(k,p,1) by a DFS over the orbit representatives, ANDing bitsets of good times m/p.
  - Lift by 2, 3, … and project as in arXiv:2604.23906 until the set is empty.
  - Then collect gate primes until ∏p ≥ B_k (an exact integer comparison).
- **Outcome:** worked for k = 3, …, 8. See Results. This uses no Prop. 1.2 and no polynomial method. For prime k+1 the chain simply lifts by k+1, e.g. ×7 for k = 6.
- **Failed gates (kept):**
  - p = 5 fails for k = 3.
  - p = 11, 17, 23, 29 fail for k = 6.
  - p ≤ 29 fail for k = 7.
  - p ∈ {11, 13, 17} fail for k = 8 with chain ×2×2×2, proj, ×3×3.

  At small p the tuple space is too coarse. The surviving tuples are recorded in `results/*.jsonl`.

### 3. Naive level-one DFS for larger k (measured: does not scale)

- Our C level-one engine visits C((p−1)/2 + k − 2, k − 1) leaves at about 1.8·10⁸ leaves/s/core. Measured examples: k = 8, p = 151: 3.5·10⁹ leaves in 19.5 s; k = 7, p = 173: 6.7·10⁸ leaves in 3.7 s.
- Projected level-one cost with B_k and the smallest feasible gate set (core-hours):

  | k | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | core-hours | 0.44 | 63 | 8.6·10⁴ | 2·10⁷ | 5·10⁹ | 2·10¹² | 7·10¹⁴ | 2.6·10¹⁷ |

- For k = 15 with the (unverified) flag-bound target Σ ln p > 483.2, it is still about 1.7·10¹⁴ core-hours over 79 primes from 251 to 743.
- **Why it fails:** the enumeration is p^{k−1}. The published methods avoid enumerating Z_p^k:
  - Rosenfeld's and Sungkawichai–Trakulthongchai's pruned DFS: k = 8 in 2 s.
  - Allikvere's generator of the "level-one improper family" by covers of folded times: reportedly about p⁶.
- Lesson: the next case needs that generator, not more cores.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| `find_witness` is a complete decision procedure; ML(v) is attained at some a/(v_i+v_j) | proved (short proofs in docstring) | `lonely.py` |
| ML(1, …, n) = 1/(n+1) exactly, n ≤ 10; ML(1,3,4,7) = 1/5 | computed exactly | `test_lonely.py` |
| Every primitive tuple with max speed ≤ N has a witness at 1/(n+1): (n, N) = (3, 150), (4, 60), (5, 32), (6, 22), (7, 18) | computed up to N | `exhaustive.py`, `results/exhaustive.txt` |
| Tight primitive tuples in those ranges: n=3: (1,2,3); n=4: (1,2,3,4), (1,3,4,7); n=5: (1,…,5), (1,3,4,5,9); n=6: (1,…,6); n=7: (1,…,7), (1,2,3,4,5,7,12), (1,4,5,6,7,11,13) | computed up to N | `results/exhaustive.txt` |
| Sieve code agrees with brute force from the definition of I(k,p,l) on small (k,p,l) | tested | `test_lonely.py` |
| LRC(3): J(3,p) = ∅ for p ∈ {7, 11, 13, 17}; ∏p = 17017 ≥ B_3 = 1728 | certificate-checked computation **+ cited B_k** | `results/lrc_k3.jsonl` |
| LRC(4): 8 gate primes 13…41, Σ ln p = 25.60 > 22.09 | same | `results/lrc_k4.jsonl` |
| LRC(5): 13 gate primes 23…73, Σ ln p = 49.79 > 46.11 | same | `results/lrc_k5.jsonl` |
| LRC(6) (7 runners): 21 gate primes 13…109, Σ ln p = 85.26 > 80.59; 48 s pure Python | same | `results/lrc_k6.jsonl` |
| LRC(7) (8 runners, Rosenfeld's case): 29 gate primes 31…173, Σ ln p = 130.78 > 126.33; 30 s with C level one | same | `results/lrc_k7.jsonl` |
| LRC(8) (9 runners) | see `results/lrc_k8.jsonl` (status in the PR description) | |

"Certificate-checked computation + cited B_k" means the following. The chain LRC(2) ⇒ LRC(3) ⇒ … ⇒ LRC(8) is a proof *if* three things hold:

- the Malikiosis–Santos–Schymura bound in Rosenfeld's Corollary 3 form,
- the elementary lemmas above,
- the correctness of `sieve.py`.

The last is tested against brute force but not formally verified. These reproduce *known* cases only. Nothing new is claimed.

## Next steps: plan for LRC(15) (16 runners)

1. **Get the primary sources.** arxiv.org, zenodo.org and combinatorics.org must be allowed in the environment (currently blocked). Then:
   - read Allikvere arXiv:2609.02604 v2, in particular the flag bound (Lemma 3.3, Prop. 3.4), the level-one generator, and the level-14/15 fibre searches;
   - read Rosenfeld's Cor. 3 and MSS Thm 1.1 to re-confirm B_k from the primary text.
2. **Re-implement Allikvere's level-one generator** independently. Cross-check it against our brute-force sieve for k ≤ 8, and against the published gate tables for k = 13, 14. An independent replay of 14 and 15 runners is itself valuable: per its README, the munim repository has only partially re-checked them.
3. **Bound.**
   - With B_15 (cited, safe): Σ ln p ≥ 964.8, which needs about 149 primes from 241 to 1229.
   - With Allikvere's flag bound carried to k = 15: Σ ln p ≥ 496.7, or 483.2 after the forced divisor lcm(2..16) = 720720. That needs about 79 primes from 251 to about 743. This is per the munim repository; we must re-derive it before relying on it.
4. **Size of the search and cost.** Level-one generation is the bottleneck. Two data points:
   - Allikvere reportedly spent about 2,140 CPU-hours on 15 runners, dominated by 19 small primes (p = 181 alone about 140 CPU-hours).
   - Level-one cost reportedly grows about p⁶.

   Extrapolating from 71 gates up to p = 569 to about 80 gates up to p ≈ 800 at k = 15 gives (800/569)⁶ ≈ 7.7 per gate at the top end, plus the extra dimension. Order of magnitude: 10⁴–10⁵ CPU-hours. That is cluster scale, not a single session. This is a heuristic estimate: the k = 15 generator cost is unmeasured, and step 2 must measure it at p = 251 before any commitment.
5. **Structural simplification for 16 runners.** k+1 = 16 = 2⁴, so binary lifts reach the tight witness 1/16 directly. The munim repository reports, at 10 pilot primes, that the tight orbit (1..15) dies by level 16 (computed, unreviewed). If that holds at every gate prime, the per-prime fibre searches that 14/15 runners needed disappear. Re-check with `sieve.py` at small levels.
6. **Do not** present any of this as a proof until every gate has a stored certificate (the improper sets at each stage) and the bound has been re-derived from primary text.
