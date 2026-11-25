# Small primes as gates: the shift lemma, τ_k(p), and an audit of Allikvere's preliminary primes

Track notes from the small-primes agent (2026-11-25). Companion code: `computations/lonely-runner/smallp/`.
Labels follow the repository README: *proved*, *computed* (exact, our code), *certificate-checked*, *heuristic*.

Notation follows `problems/lonely-runner.md`:

- k speeds, threshold 1/(k+1), prime p > k+1, level l with p ∤ l;
- the folded classes 1..h, with h = (p−1)/2;
- class v covers time a iff (k+1)·d_p(av) < p;
- τ_k(p) is the least number of classes covering all h times (Allikvere's covering number);
- Lemma 2.2(ii) is the prime-divisibility criterion of arXiv:2609.02604v2. It is restated, restricted to primitive vectors, as Lemma 2.1 of the sixteen-runner manuscript.

Sources read:

- J. Allikvere, arXiv:2609.02604v2. LaTeX source from arxiv.org/e-print, §§2 and 4, Lemma 3.12 (`lem:neargcd`).
- J. Allikvere, "Sixteen lonely runners", Zenodo 10.5281/zenodo.23304361 (Oct 2026, unrefereed): the manuscript source `paper.tex` and `appendices.tex`, and the data file `gates_weighted_shift_audit.zip` (MD5 443abc5398d9627aad9e415876afcffb, equal to Zenodo's).
- None of his programs was run. His files were read as data only.

## 1. τ ≤ k − 2 forces J(k,p) ≠ ∅ (proved)

**Lemma N.** Let p > k+1 be prime and suppose some set C of s ≤ k − 2 classes covers all folded times. Then J(k,p) ≠ ∅.

*Proof.*

1. Fix a level l with p ∤ l. Let w ∈ Z_{lp}^k have:
   - w_i ≡ c_i (mod p) and w_i ≡ 0 (mod l) for the first s coordinates (c_i ∈ C, by CRT);
   - w_i ≡ 1 (mod l) and w_i ≢ 0 (mod p) for the remaining k − s ≥ 2 coordinates.
2. Take a time t = m/(lp), 0 < m < lp. For i ≤ s write w_i = l·w_i′. Then t·w_i = m·w_i′/p, and w_i′ ≡ l^{−1}c_i (mod p), so ‖t w_i‖ = ‖a c_i/p‖ with a ≡ m·l^{−1} (mod p).
   - If p ∤ m, then a ≢ 0 and C covers a: some i has (k+1)d_p(a c_i) < p, so ‖t w_i‖ < 1/(k+1).
   - If p | m, then t w_i ∈ Z, so ‖t w_i‖ = 0.

   So w has no witness at level l.
3. The gcd clause fails: for every i, at least one of the ≥ 2 coordinates ≡ 1 (mod l) remains, so gcd(l, w_j : j ≠ i) = 1.
4. So w is improper. Its reduction mod p is the same level-one vector u for every l, so u has an improper lift at every level and u ∈ J(k,p). ∎

**Consequence.** J(k,p) = ∅ needs τ_k(p) ≥ k − 1. This is exactly the dividing line in Allikvere's LRC(14) table: "J empty" gates have τ ≥ 13, while gates with τ ≤ 12 use Lemma 3.12. It is also the line in his LRC(15) Prop. "Previously verified primes": the divisibility-only primes are those with τ_15 ≤ 13. Every prime with τ_k(p) ≤ k − 2 can only be a *divisibility* gate, through Lemma 2.2(ii) and a shift lemma.

The vectors constructed in Lemma N are exactly the near-gcd shape: k − e coordinates divisible by every prime of l, and e = k − s ≥ 2 exceptions.

## 2. The weighted shift lemma (proved; = Allikvere's Lemma "A weighted shift")

**Lemma S.** Let k ≥ 3 and assume LRC(m) for all m ≤ k − 2. Let u ∈ (Z∖{0})^k and d ≥ 2. Put

- E = {i : d ∤ u_i};
- g_i = gcd(u_i, d) for i ∈ E;
- c(g) = g·⌈2d/((k+1)g)⌉.

If |E| ≥ 2 and Σ_{i∈E} c(g_i) < d, then some real t has ‖t u_i‖ ≥ 1/(k+1) for all i.

*Proof.*

1. **The block D.** D = [k] ∖ E has at most k − 2 coordinates, taking m ≤ k − 2 distinct values (up to sign). LRC(m) gives t_0 with ‖t_0 u_j‖ ≥ 1/(m+1) ≥ 1/(k−1) > 1/(k+1) for j ∈ D. If D = ∅, take any t_0.
2. **The shifts.** For q = 0, …, d−1, put t_q = t_0 + q/d. For j ∈ D, d | u_j, so t_q u_j ≡ t_0 u_j (mod 1).
3. **One exception.** Fix i ∈ E with g = g_i. Then q·u_i/d ≡ q·(u_i/g)/(d/g), and u_i/g is a unit mod d/g. So as q runs over Z_d, t_q u_i runs over the (d/g)-point coset t_0 u_i + (g/d)Z (mod 1), each point exactly g times.
4. **Forbidden shifts.** The bad set {y : ‖y‖ < 1/(k+1)} is an open arc of length 2/(k+1). An open arc of length L·(spacing) holds at most ⌈L⌉ points of a coset of that spacing. Here L = 2(d/g)/(k+1), so exception i forbids at most g·⌈2d/((k+1)g)⌉ = c(g) values of q.
5. **Conclusion.** Σ c(g_i) < d, so some q is forbidden by no exception, and t_q is a witness. ∎

**Notes on Lemma S.**

- **Prime d.** For d prime, g_i = 1 and c = ⌈2d/(k+1)⌉. This is Allikvere's Lemma 3.12 (arXiv:2609.02604v2) for k = 14, d ∈ {3, 5}.
- **k = 15.** c(g) = g⌈d/(8g)⌉, which is verbatim the sixteen-runner Lemma "A weighted shift". Its hypothesis there is LRC(m), m ≤ 13 = k − 2, as here. Independently found here (checkpoint 1) and then located in his manuscript.
- **Use in Lemma 2.2(ii).** If d | l, then E and the g_i depend only on u mod lp. So the conclusion holds on the whole residue class, which is what Lemma 2.2(ii) needs.
- **Extended properness is inherited by lifts.** Call a lift *extended-proper* at level l if it has a witness, or satisfies the gcd clause, or satisfies Lemma S for some d | l. All three conditions persist to multiples of the level: the class mod (cl)p sits inside the class mod lp. So the cascade may discard extended-proper lifts at *every* level. If the retained set is empty at level L, every lift at level L is proper or lies in a class covered by Lemma S, so Lemma 2.2(ii) applies at level L.
- **Units and signs.** Allikvere's unit reduction (Remark 2.3: b ≡ a^{−1} mod p, b ≡ 1 mod l) fixes residues mod l, hence E and the g_i. Sign changes of coordinates do not change E, the g_i, or loneliness. So one orbit representative suffices.
- **Machine check** (`smallp/shift_lemma_check.py`, exact Fractions):
  - the arc count max_x #{j : ‖x + j/n‖ < 1/16} = ⌈2n/16⌉ for every n ≤ 256 (step 4, with equality);
  - the multiplicity statement of step 3 for all d ≤ 128 and all u mod d;
  - a negative control: floor in place of ceiling fails.

**Which d help (k = 15, c(g) = g⌈d/(8g)⌉).**

| d | allowed exceptions (sum of c < d) |
| --- | --- |
| 2 | none beyond the gcd clause (e ≤ 1) |
| 3 | e = 2 |
| 4 | odd costs 1, 2 mod 4 costs 2: up to 3 odd exceptions |
| 5 | e ≤ 4 |
| 7 | e ≤ 6 |
| 8 | odd 1, 2 mod 4 costs 2, 4 mod 8 costs 4: up to **7** odd exceptions |
| 16 | odd or 2 mod 4 cost 2, 4 mod 8 costs 4, 8 mod 16 costs 8: up to 7 |
| 32 | valuations 0–2 cost 4: up to 7 |

The limit is e < (k+1)/2 = 8. For k = 15 the powers d = 8, 16, 32 reach it, and they divide the binary levels 8, 16, 32 themselves, so **no odd lift is needed**. Allikvere's certificates use only d = 4 (at most 3 odd exceptions) and then an exact level-8 test of the residual lifts.

## 3. Covering numbers (computed)

`smallp/mincover.c` (exact): an exhaustive DFS for a cover by ≤ s classes containing class 1. This loses nothing by unit symmetry.

- It branches on the uncovered time with the fewest allowed coverers, excluding earlier siblings.
- It cuts when the s − |L| largest gains sum to less than |U|.
- τ is the least s for which a cover is found; the cover found is re-verified.
- "None" for s − 1 is exhaustive by the branching argument (covergen.c header). This is not an external certificate.
- Cross-checked against a SAT formulation (`smallp/tau.py`, pysat/CaDiCaL) at k = 14, p = 83–113: same values.

**k = 14** (consistency with arXiv:2609.02604v2, Table "primes used for LRC(14)"):

| p | 83 | 89 | 97 | 101 | 103 | 107 | 109 | 113 | 127 | 131 | 137 | 139 | 149 | 151 | 157–233 | 239 | 241 | 251 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| τ_14 | 12 | 12 | 10 | 11 | 10 | 11 | 10 | 11 | 11 | 11 | 11 | 12 | 12 | 11 | 12 (each) | 13 | 12 | 13 |

- His near-gcd block (τ ≤ 12) and J-empty block (τ ≥ 13) agree with these values at every listed prime we computed, 89–251.
- He also used 131 (τ = 11).
- p ≥ 257 timed out at 120 s per prime and was not computed.

**k = 15:**

| p | 37 | 41 | 43 | 47 | 53 | 59 | 61 | 67 | 71 | 73 | 79 | 83 | 89 | 97 | 101 | 103 | 107 | 109 | 113 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| τ_15 | 9 | 10 | 12 | 12 | 11 | 12 | 12 | 10 | 11 | 12 | 11 | 12 | 12 | 10 | 11 | 10 | 11 | 10 | 11 |

| p | 127 | 131 | 137 | 139 | 149 | 151 | 157 | 163 | 167 | 173 | 179 | 181 | 191 | 193 | 197 | 199 | 211 | 223 | 227 | 229 | 233 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| τ_15 | 12 | 11 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 13 | 13 | 12 | 12 | 12 | 13 | 13 | 12 | 12 | 13 |

- By Lemma N, every prime 37–233 has J(15,p) ≠ ∅, because τ_15 ≤ 13 = k − 2.
- Hence each of them is at best a divisibility gate. This agrees with Allikvere: 191, 211, 223, 233 are divisibility-only in his Prop. "Previously verified primes".
- τ_15(p) ≥ ⌈h/m⌉ ≥ 8 always, where m = ⌊(p−1)/16⌋ is the number of times each class covers. So the Lemma N vectors have at most 7 exceptions, and these are always killed by Lemma S with d = 8 or 16.
- **Not computed:** τ_15 at 239–307. His J-empty claims there need τ_15 ≥ 14 by Lemma N. That run was paused for the retarget.

## 4. Audit of the k = 15 preliminary primes (certificate-checked, partial)

His Prop. "Previously verified primes" uses the following preliminary primes:

- **Divisibility-only:** 191, 211, 223, 233, 241, 251, 257, 263, 277.
  - Seven of them (191, 223, 233, 241, 251, 257, 277) by the "weighted shift d = 4 + exact level-8 test" composition, recorded in `small_prime_pilot_20260910`.
  - 211 and 263 by separate compositions, not examined here.
- **J-empty:** 239, 271, 283, 293, 307.
- **29 and 31:** these belong to the structure agent.

**Composition (checked by reading).** For each level-one orbit r:

- either the plain binary cascade empties by level 32 (eventually proper);
- or r is "persistent", and at level 8 every lift is proper or covered by Lemma S.

The level-8 step works as follows. A level-8 lift reduces to a level-4 lift.

- If the level-4 lift is proper, so is the level-8 lift.
- If it is closed by Lemma S with d = 4, so is every level-8 lift, since 4 | 8.
- Otherwise it is "residual", and all of its level-8 lifts must have a grid witness.

This is a valid instance of Lemma 2.2(ii) at level 8.

**p = 191: what we re-derived with our own code.**

1. **Covers on ≤ 13 classes.** Our exhaustive enumeration (`mincover.c` enum mode) finds 260 minimal covers containing class 1, all of size 13, forming **20 unit orbits**.
   - His precondition file `km1low_191.txt` has 260 rows: 14-multisets, i.e. a 13-cover with one class doubled. Their supports form the **same 20 orbits**.
   - So τ_15(191) = 13, and his "260" is confirmed.
2. **Terminal step for all 90,248 persistent orbits** (`terminal15.py`; his representatives read from `SUMMARY.json`). Every quantity is recomputed from Def. 2.1 with `liftfree.c` and our own gcd and Lemma S tests:

   | quantity | ours | his `terminal_191.out` |
   | --- | --- | --- |
   | bases | 90,248 | 90,248 |
   | level-2 improper lifts | 132,675 | 132,675 |
   | level-4 witness-free lifts | 471,470 | 471,470 |
   | closed by Lemma S, d = 4 | 470,880 | 470,880 |
   | residual | 590 | 590 |
   | witness-free level-8 lifts of residuals | 0 | 0 |

   - Also: every representative is witness-free at level 1, i.e. in I(15,191,1).
   - Our variant, with Lemma S at d ∈ {4, 8} and the gcd clause on the level-8 lifts, also leaves 0.
   - **Exact agreement.**

3. **p = 251 and 223:** the same terminal re-derivation was started. The results are in the addendum below if it finished.

**Not checked here.** These are the expensive parts:

- level-one completeness at these primes: his irredundant branch has 12.1M rows at 191;
- that every non-persistent row dies in the plain cascade: 16.3M rows, about 14 CPU-h of his cascade at 191;
- the gates 211, 263, 239, 271, 283, 293, 307.

So at p = 191 the audit covers the precondition and the whole terminal step, but not generation or the bulk cascade.

## 5. Lemma S at d = 8, 16, 32 kills the "p = 149 regime" fibres (heuristic, 2 samples)

His pilot abandoned p = 149 and fourteen other τ ≤ 12 primes. His record: every sampled row persistent, with fibres growing 4–8× per level, about 35 CPU-years for the cascade.

- His sample bases (`pilot149_evidence.tgz`, `t3.out`) are the 12-class cover {1,2,3,11,13,25,28,48,59,61,63,67} at p = 149 (checked: it covers all 74 times), plus classes 1, 1, x.
- `smallp/cascade15x.py`:
  - The **plain** cascade reproduces his fibre sizes exactly: x = 1 gives 24 / 344 / 1888 / 8576 at levels 2/4/8/16; x = 4 gives 21 / 204 / 816 / 6336.
  - With **Lemma S for d ∈ {4, 8, 16, 32, 64}, d | l, applied at every level**, the fibres are 24 / 288 / 768 / **0** (x = 1, empty at level 16) and 21 / 156 / **0** (x = 4, empty at level 8).
  - With d = 4 alone they kept growing; that run was stopped after 2 min.
- This is two bases only, so it is **heuristic**. But it shows that the d = 8/16 form of the shift lemma removes the mechanism that made the τ ≤ 12 primes infeasible. Those primes would then be limited by level-one generation cost, not by cascade blow-up.
- **Not yet done:** a random sample of level-one rows at p = 139–199 through the extended cascade.

## 6. Failed or abandoned routes (kept)

- **Lemma 3.12 with d = 2 at k = 15** gives nothing: c = ⌈4/16⌉ = 1, so e < 2, which is the gcd clause. The odd-level route (l = 16·3 with d = 3, or 16·5 with d = 5), which mimics Allikvere's level-15 kill, was considered. It is dominated by d = 8/16, which need no odd lift.
- **SAT for τ** (`tau.py`) is correct but slow on the UNSAT side above p ≈ 113. The DFS in `mincover.c` is much faster.

## Next (retargeted to k = 17, 18 runners)

See the k = 17 section once it is written: Lemma S for k = 17 has c(g) = g⌈d/(9g)⌉, and the tight tuple forces 18 | l.
