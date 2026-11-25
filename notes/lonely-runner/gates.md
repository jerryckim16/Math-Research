# Gate selection for LRC(15) and LRC(17): admissibility (tau), cost per prime, pilot

Track notes (gates agent, 2026-11-25). Companion to `problems/lonely-runner.md`
(Approaches 7–13 and "Next steps: plan for LRC(15)"). Code:
`computations/lonely-runner/k15/`. The coordinator integrates these notes into
the problem file; this note does not edit it.

Labels: **proved**, **computed** (exact computation, tested code, not formally
verified), **certificate data** (numbers read from Allikvere's archives, not
recomputed), **heuristic** (Knuth estimates and extrapolations).

## 1. Admissibility: the covering number tau_k(p)

**Definition.** Fix k and a prime p > k+1, with h = (p−1)/2. Folded speed class v
*covers* folded time a when (k+1)·d_p(av) < p; this is the relation used in
`covergen.c`. Each class covers m = ⌊(p−1)/(k+1)⌋ times. Define
**tau_k(p)** as the least number of classes that together cover all h times.
A k-multiset lies in I(k,p,1) exactly when its support covers every time.

**Lemma T (proved here).** If tau_k(p) ≤ k−2, then for every level l with
gcd(l, p) = 1, I(k,p,l) ≠ ∅. In particular J(k,p) ≠ ∅ cannot be avoided at a
level coprime to p, so the gate cannot be closed as "J empty" through the binary
or 3-adic cascades.

*Proof.* Let C = {c_1, …, c_s} be a cover with s ≤ k−2. Put N = lp. By CRT,
choose w_i ≡ c_i (mod p) and w_i ≡ 0 (mod l) for i ≤ s, and choose
w_j ≡ 1 (mod p) and w_j ≡ 1 (mod l) for the remaining k−s ≥ 2 coordinates.
No coordinate is divisible by p.

- **No witness.** Let t = m/N.
  - If p ∤ m, then w_i t ≡ (w_i/l)·m/p (mod 1), and w_i/l ≡ c_i l^{−1} (mod p).
  - Multiplication by the unit l^{−1} maps covers to covers, so some i ≤ s has
    (k+1)·d_p(m c_i l^{−1}) < p, that is, ‖w_i t‖ < 1/(k+1).
  - If p | m, then t ∈ (1/l)Z and w_1 t ∈ Z.
- **The gcd clause fails.** For every i, the coordinates other than i include a
  w_j ≡ 1 (mod l), so gcd(l, w_j : j ≠ i) = 1.

So w ∈ I(k,p,l), and w lies above v = (c_1, …, c_s, 1, …, 1). ∎

- **The boundary case tau = k−1.** The same construction with one free coordinate
  is proper by the gcd clause: drop the free coordinate, and the rest are all
  divisible by l. This is why the threshold is k−1.
- **Agreement with Allikvere.** His "J(14,p) = ∅" gates are exactly the τ ≥ 13
  ones, and his near-gcd gates are the τ ≤ 12 ones. At k = 15 every one of his 59
  campaign gates records the precondition "covers on ≤ 13 classes = 0". So
  **tau_k(p) ≥ k−1 is the J-empty admissibility condition.**
- **Gates with smaller tau.** These can still give divisibility, but only through
  a near-gcd argument (Lemma S below).

**Tool:** `k15/tau.c` (`tau k p smax`). It is an exhaustive DFS for a cover
containing class 1 with at most s classes, using:

- unit normalisation;
- branching on the most-constrained time, with exclusion of earlier siblings;
- a top-gain sum bound;
- with TAU_CUTS (the default), the Lemma 4.1 q-cut and an empty-private cut,
  both valid for minimal covers.

A found cover proves tau ≤ s. Exhausting the search proves tau > s.

- **Validation** (`k15/test_gate15.py::test_tau`): it equals a brute force over
  all subsets at (5,29), (5,31), (6,37), (7,41), (7,43), with and without the cuts.
- **k = 14 reproduction:** tau_14 = 12, 11, 13, 12, 13, 13 at p = 89, 131, 239,
  241, 251, 257. These match his near-gcd / J-empty split.

### k = 15 screen (computed)

Exact results for "is there a cover on at most 13 classes?":

| p | result |
| --- | --- |
| 17–23, 37–233, 241, 251, 257, 263 | a cover on ≤ 13 classes exists, so tau_15 ≤ 13 and the gate is near-gcd only |
| 29 | tau_15 = 14 (m = 1, h = 14) |
| 31 | tau_15 = 15 |
| **239** | **tau_15 ≥ 14, proved by exhaustive search (60 s)** |

- **Consequence for the old plan.** The pre-Allikvere 79-gate plan (all primes
  251–743, problem file Next steps 3) silently assumed J-empty gates. It is
  **not admissible as stated**: 251, 257 and 263 (at least) have tau_15 = 13.
- **Consistency with Allikvere.** This matches his "Sixteen lonely runners"
  (Zenodo 10.5281/zenodo.23304361; certificate data):
  - 251 and 257 appear only in his weighted-shift divisibility audit, and 263 in a
    divisibility "provenance" record;
  - 239 is one of his five J-empty preliminary gates (239, 271, 283, 293, 307);
  - his campaign starts at 269.

## 2. Lemma S (shift lemma for improper lifts; proved here)

Assume LRC(m) for all m < k. Let N = lp and let d ≥ 2 with d | N. Let
w ∈ Z_N^k, and put:

- E = {i : d ∤ w_i};
- g_i = gcd(w_i, d) for i ∈ E;
- b_i = g_i · ⌈2d / ((k+1) g_i)⌉.

If E ≠ ∅ and Σ_{i∈E} b_i < d, then every integer tuple u ≡ w (mod N) with all
u_i ≠ 0 is lonely, i.e. some t has ‖u_i t‖ ≥ 1/(k+1) for all i.

The hypothesis E ≠ ∅ is automatic in our use. If w is improper at level l and
d | l, then |E| ≥ 2: with |E| ≤ 1 the gcd clause would hold, giving
gcd(l, w_j : j ≠ i) ≥ d for the exceptional index i, or for any i when E = ∅.

*Proof.* Since d | N, we have d | u_i ⟺ d | w_i and gcd(u_i, d) = g_i.

1. **The base time.** By LRC(k−|E|) for (u_j)_{j∉E} (repeats allowed; trivial if
   that set is empty) there is t_0 with ‖u_j t_0‖ ≥ 1/(k−|E|+1) ≥ 1/(k+1) for
   j ∉ E. Since |E| ≥ 1, only LRC(m) with m < k is used.
2. **Shifting.** For r ∈ Z_d put t = t_0 + r/d. For j ∉ E, u_j t ≡ u_j t_0 (mod 1).
3. **Counting bad shifts.** For i ∈ E, u_i r/d runs over the coset of
   (g_i/d)Z, and each point is hit by g_i values of r.
   - An open arc of length 2/(k+1) contains at most ⌈(2/(k+1))/(g_i/d)⌉ points
     of a (g_i/d)-spaced progression, since the points inside form a run of
     consecutive terms.
   - So at most b_i values of r give ‖u_i t‖ < 1/(k+1).
4. **Conclusion.** Since Σ b_i < d, some r is good for every i ∈ E. ∎

- **Relation to Allikvere's Lemma 3.12.** For g_i = 1 this is his few-exception
  shift, with m_d = ⌈2d/(k+1)⌉ and e·m_d < d (the k = 14 version with
  d ∈ {3, 5} is in `gatecheck.c`).
- **Divisibility (Lemma 2.2(ii) form).** Every improper w with some d | l passing
  Lemma S has only lonely integer preimages. If, for some level l, every member
  of I(k,p,l) passes Lemma S for some d | l, then p | u_1⋯u_k for every
  counterexample u. The proof is Lemma D's.
  - The symmetry reduction is safe. Lemma S's hypothesis is invariant under units
    a of Z_N, signs and permutations: d | aw_i ⟺ d | w_i and gcd(a w_i, d) = g_i.
  - Integer rescaling by an odd a′ ≡ a (mod p) preserves loneliness.
  - It also preserves the gcd(u) = 1 step of Lemma D's (a)-branch, since
    gcd(a′, l) = 1.
- **Tests** (`k15/test_gate15.py::test_shift_lemma_sound_on_samples`): for
  shift-killed improper level-8 lifts at k = 7 (p = 17, 19, 23), random integer
  preimages are all lonely according to the exact checker `lonely.find_witness`.

## 3. Pilot tools for k = 15 (computed, tested)

`k15/gate15.c` (`gate15 k p LMAX`) does three things:

- it checks that each level-one row is witness-free;
- it runs the binary cascade S_{2l} = improper lifts of S_l (j_i ∈ {0,1}, with the
  gcd clause at each level) up to LMAX ∈ {16, 32};
- it tests every member at levels ≥ 4 with Lemma S for d ∈ {4, 8, 16, 32}, d | l.

For k = 15 the kill level 16 = 2⁴ is reached by the cascade itself.

Validation and measurements:

- **Brute force** (`test_cascade_matches_bruteforce_k7`): for k = 7 (k+1 = 8 a power
  of 2) at p = 17, 19, 23, 29, 31 and every level-one orbit, the per-row counts
  n_2, n_4, n_8 and the shift-unkilled counts f_4, f_8 equal a brute force over
  all 2^k lifts from Def. 2.1 (`sieve.Level.is_proper`).
- **Tight orbit:** (1..15) mod 251 gives n_2, n_4, n_8, n_16 = 1, 2, 4, 0, the
  same as `tight_orbit_k15.py`.
- **Speed:** 0.18 ms per level-one orbit at p = 239, measured on 20,000 orbits
  of a partial shard.

## 4. Pilot gate p = 239 for k = 15: stopped, not closed

Choice and run:

- 239 is the cheapest tau_15 ≥ 14 prime at or above 37 (Knuth estimate 2.57·10¹⁰
  nodes, about 4 CPU-h). Primes p ≤ 31 were left to the structure agent.
- Run: `covergen 15 239` with `LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1` in 16 shards,
  3 workers, scratch `lr-gates/p239/`.
- **Stopped after about 8 min wall, 0 of 16 shards finished, about 1.0M partial
  covers**, when the coordinator retargeted the track to k = 17. The projected
  completion was 1.5–2 h wall on the shared machine (load 9–12).
- The run is restartable: rmdir the `claim_*` directories, then run `worker.sh`
  three times. The partial covers are not a result.

Planned comparison (not done), against his out15_239 tree in
`gates_239_271_283_293_307_audit.zip`, whose SHA-256 matches SHA256SUMS:

- his 9,552,452 irredundant rows, plus 8,272 km1 covers × 119 extensions;
- cascade: 35,819 survivor rows, dying by level 16;
- 0 persistent orbits.

## 5. Allikvere's k = 15 campaign as data (certificate data)

Downloaded to scratch `lr-gates/dl/`, kept for the certificate agent:

- all 59 `evidence15_<p>_s0.tgz` files;
- the five-prime audit zip.

Every SHA-256 equals `SHA256SUMS.txt`, whose MD5 equals the Zenodo record's.
The 59 `SUMMARY.json` files were read as data
(`k15/allikvere_k15_summaries.json`). In every one:

- the status is GATE_CLOSED;
- the claim type is "J(K,p) empty";
- the precondition reports 0 covers on ≤ 13 classes;
- there are 0 persistent orbits.

His recorded CPU is 49,255 CPU-h in total (generation plus precondition).

**Re-check cost (heuristic).** Our k = 15 Knuth tree (`k15/knuth_k15.txt`) is 1.13–1.34×
his recorded irredundant node counts at all 59 gates (median 1.20). Level-one
completeness at all 59 gates with our generator would take about **8.1·10⁴ CPU-h**
at 1.8·10⁶ nodes/s. The cheapest of his gates are:

| gate | CPU-h |
| --- | --- |
| 239 (preliminary) | about 4 |
| 269 | about 12 |
| 281 | about 20 |

## 6. LRC(17) (18 runners)

(filled in below)
