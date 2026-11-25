# Lonely Runner: structural lemmas and small gates (structure track)

Working notes of the "structure" track (2026-11-25). Notation follows
`problems/lonely-runner.md`: LRC(k) is the conjecture for k speeds, i.e.
k+1 runners; I(k,p,l) and J(k,p) are the improper and not-eventually-proper
sets of the prime-gate framework (Sungkawichai–Trakulthongchai, Def. 2.1);
F1, F2, Lemma D and Lemma E are as written out in the problem file.

Code is in `computations/lonely-runner/structure/`. Results are in
`computations/lonely-runner/structure/results/`.

**Summary.**

| # | Statement | Label |
| --- | --- | --- |
| 1 | Lemma S: for a prime k+2 ≤ p ≤ 2k+1, I(k,p,1) is exactly the multisets whose ± classes cover every class; orbit count by Burnside | **proved**; brute-force check against `covergen.c` and `level1.c` at 26 (k,p) pairs |
| 2 | J(15,31) = ∅ by binary level 16, so 31 \| v_1⋯v_15 for every counterexample to LRC(15) | **certificate-checked computation** (two independent implementations), given LRC(14) |
| 3 | J(15,29): see §3 | see §3 |
| 4 | Lemma NG (weighted shift) | **proved**; same as Allikvere's "weighted shift" lemma (Zenodo 10.5281/zenodo.23304361) |
| 5 | Mechanism: at small p the binary cascade's persistent families are dyadic near-gcd families, which NG removes (k = 7, p = 11) | computed; one worked case |
| 6 | Beck–Everett relation theorem | cited preprint; **proof verified by reading**; tested; **gives no pruning** |
| 7 | Alon–Bucić–Davies matrix theorem | cited preprint; **implies nothing for LRC(k)** (argument in §6) |

These are **independent re-derivations**, not new results, where Allikvere's
"Sixteen lonely runners" (Zenodo 10.5281/zenodo.23304361, Oct 2026,
unrefereed) already has them: Lemma S with the same orbit counts, the p = 29
and p = 31 gates, and the weighted shift. We read his note
`N15_SMALL_PRIME_SHIFT_GATE_SEARCH.md`, his p = 29 note and the manuscript
source as data only, after our own derivation and run at p = 31. Comparison
in §3.

---

## 1. Lemma S (cover radius ±1 at small primes)

**Lemma S.** Let k ≥ 2, and let p be a prime with k+2 ≤ p ≤ 2k+1. Put
n = (p−1)/2. For v ∈ (Z_p \ 0)^k the following are equivalent:

1. v ∈ I(k,p,1), i.e. no t ∈ (1/p)Z has ‖t v_i‖ ≥ 1/(k+1) for all i;
2. for every a ∈ Z_p \ 0 some i has a·v_i ≡ ±1 (mod p);
3. the classes {±v_i} cover all n classes of Z_p^*/{±1}.

In particular k ≥ n is forced. For p = 2k+1 prime, I(k,p,1) is exactly the
unit orbit of (1, 2, …, k).

*Proof.* The gcd clause is void at level 1. The time t = 0 is never a
witness. For a ≠ 0, put d = d_p(a v_i) ∈ {1, …, n}, so that
‖a v_i/p‖ = d/p, which is ≥ 1/(k+1) iff (k+1)d ≥ p.

- If d ≥ 2, then (k+1)d ≥ 2k+2 > p.
- If d = 1, then (k+1)d = k+1 < p.

So t = a/p is a witness iff no i has d_p(a v_i) = 1, i.e. a·v_i ≢ ±1 for all
i. That proves (1)⇔(2). Next, (2) says that every class ±a is of the form
±v_i^{-1}. Inversion is a bijection on Z_p^*/{±1}, so this is (3). For
p = 2k+1 we have n = k, so the k classes ±v_i are all distinct and exhaust
Z_p^*/{±1}. Multiplying by a unit and permuting gives (1, …, k). ∎

**Corollary (orbit count).** The cyclic group G = Z_p^*/{±1}, of order n,
acts on I(k,p,1) by multiplication. Permutations and signs are already
absorbed by working with multisets of classes. A member of I(k,p,1) is
"every class once" plus a multiset of k − n extra classes, and the action on
it is the translation action of G on the extras. So the unit orbits of
I(k,p,1) are the G-orbits of (k−n)-multisets on G. By Burnside, their number
is

  (1/n) Σ_{d | gcd(n, k−n)} φ(d) · C(n/d + (k−n)/d − 1, (k−n)/d)

(for k = n the count is 1).

| k = 15, p | 17 | 19 | 23 | 29 | 31 |
| --- | --- | --- | --- | --- | --- |
| n | 8 | 9 | 11 | 14 | 15 |
| sorted rows C(14, n−1) | 3,432 | 3,003 | 1,001 | 14 | 1 |
| unit orbits | 429 | 335 | 91 | 1 | 1 |

**Checks** (`test_small_gates.py`):

- For every k = 3…12 and every prime k+2 ≤ p ≤ 2k+1 (26 pairs), the orbit
  set from Lemma S equals the orbit set from the project's `covergen.c`
  (minimal covers plus extensions) and from the naive `level1.c` DFS.
- Its size equals the Burnside count.
- At k = 15 the Lemma S sets have the Burnside sizes above.

Allikvere's `N15_SMALL_PRIME_SHIFT_GATE_SEARCH.md` §3 has the same
classification and the same table (429, 335, 91, 1, 1), derived the same
way. Ours was derived independently and before reading his.

**Why this matters.** Only for p ≤ 2k+1 is the level-one family this small.
At p = 37 > 2k+2 the cover radius is ±2, and level one is a genuine
covering problem.

---

## 2. Gate p = 31 for LRC(15): J(15,31) = ∅ by level 16

**Claim.** J(15,31) = ∅. More precisely, I(15,31,16) = ∅.

**Consequence.** Assume LRC(14). Lemma D (Allikvere, "Sixteen lonely
runners", Lemma gate (i)) then gives 31 | v_1⋯v_15 for every primitive
counterexample v to LRC(15).

**Computation.**

1. By Lemma S, I(15,31,1) is the single orbit of (1, …, 15).
2. Binary cascade: at each level l, lift every orbit representative by 2
   (the full fibre w_i = b_i + j_i·lp, j_i ∈ {0,1}). Keep the lifts with no
   witness on the (1/(2lp))Z grid, then drop those proper by the gcd clause
   at level 2l.
3. Reduce the survivors to unit orbits of Z_{2lp} under permutations, signs
   and units (F2).

The reduction is sound because every unit of Z_{lp} lifts to a unit of
Z_{2lp}, and improperness projects (F1). So every member of I(15,31,2l) is
in the orbit of an improper lift of a representative at level l. The
canonical form is an element of the input's orbit, so deduplication can
never lose an orbit.

| level l | witness-free lifts | proper by gcd clause | improper unit orbits |
| --- | --- | --- | --- |
| 1 | — | — | 1 |
| 2 | 2,747 | 1 | 186 |
| 4 | 86,926 | 0 | 42,541 |
| 8 | 55,778 | 0 | 27,881 |
| 16 | **0** (of 27,881 · 2^15 = 9.14·10⁸ lifts) | 0 | **0** |

**Two independent implementations agree at every level.**

- Implementation A, `small_gates.py`: `liftfree.c` (branch and bound) plus
  the gcd clause and canonical form in Python.
- Implementation B, `cascade_verify.c`, new: a plain DFS over the full fibre
  (2^15 lifts per representative, no cut), with its own witness bitsets, gcd
  clause and canonical form in C.
- They give the same witness-free counts and identical orbit sets at levels
  2, 4 and 8, and 0 lifts at level 16.
- A third run, `cascade.sh` (`liftfree.c` plus the new C `orbit_filter.c`),
  also gives identical orbit sets.
- Times: A 53 s; B about 2 min; one core.

**Gate conditions.** These are the same as at every gate:

- Gate primes must be primes > k+1 = 16, so that Z_{p,1}, Lemma D and the
  time grid make sense.
- 31 is coprime to the forced divisor lcm(2..16) = 720720 = 2⁴·3²·5·7·11·13,
  so lcm(2..16)·∏(gate primes) still divides ∏v_i.
- Only properness of type (b) (a grid witness) and the plain gcd clause (a)
  are used. There is no near-gcd lemma and no level-15 kill.
- 31 adds ln 31 = 3.434 to Σ ln p.

**Label.** Certificate-checked computation (two implementations), given
LRC(14). As for every gate, LRC(14) is Allikvere's computer-assisted
result, re-checked in this project (problem file, Approach 7).

**Comparison with Allikvere.** His p = 31 record
(`gates_29_31_records.zip`: `p31_gate_independent_replay.json`) runs the
same row (1..15) through his retained cascade and gives l2 = 2746 and
l16 = 0. His l2 counts improper lifts after the gcd/deletion screen; our
figure is 2,747 − 1 = 2,746, which matches. His l4 = 1,276,122 and
l8 = 1,672,732 count lifts with multiplicity, without orbit reduction, so
they are not comparable with our orbit counts. Both computations die at
level 16. Our run uses a full unit-orbit reduction at every level (his
uses only the stabiliser of the row).

---

## 3. Gate p = 29, and the new small primes 17, 19, 23

(See the results files; filled in below as runs finish.)

PLACEHOLDER-29

---

## 4. Lemma NG (dyadic and general weighted shift)

**Lemma NG.** Let k ≥ 2 and assume LRC(m) for all m < k. Let
u ∈ Z_{>0}^k and d ≥ 2. Put E = {i : d ∤ u_i}, e = |E| and
g_i = gcd(u_i, d). If 1 ≤ e < k and

  Σ_{i∈E} g_i · ⌈2d / ((k+1) g_i)⌉ < d,

then some t has ‖t u_i‖ ≥ 1/(k+1) for all i. (Here e < k could be relaxed:
if E is everything, take t_0 arbitrary.)

*Proof.*

1. **A starting time.** The k − e speeds outside E take m ≤ k − e ≤ k − 1
   distinct values. LRC(m) gives t_0 with ‖u_j t_0‖ ≥ 1/(m+1) > 1/(k+1)
   for j ∉ E.
2. **Shifts.** For r ∈ Z_d put t_r = t_0 + r/d. For j ∉ E, d | u_j, so
   u_j t_r ≡ u_j t_0 (mod 1).
3. **Bad shifts for i ∈ E.** As r runs over Z_d, u_i r mod d runs over the
   multiples of g_i, each g_i times. So u_i t_r mod 1 visits the d/g_i points
   of a coset x + (g_i/d)Z, each g_i times. The bad set
   {y : ‖y‖ < 1/(k+1)} is an open arc of length 2/(k+1). An open arc of
   length L contains at most ⌈L/s⌉ points of spacing s: if c points fit,
   then (c−1)s < L. So at most g_i·⌈2d/((k+1)g_i)⌉ shifts are bad for i.
4. **Conclusion.** The union of the bad sets has fewer than d elements, so
   some r is good for every i ∈ E, and t_r is the required time. ∎

- **Source.** This is Allikvere's "weighted shift" lemma ("Sixteen lonely
  runners", Lemma weighted, k = 15, |E| ≥ 2, cost g⌈d/(8g)⌉). It is also
  the general form of the few-exception shift Lemma 3.12 of
  arXiv:2609.02604v2, which our `gatecheck.c` implements for d ∈ {3,5} and
  g_i = 1. Our proof was written independently and is the same argument.
- **Use in a cascade.** If d | l, then E and the g_i are constant on a
  residue class mod lp. So a class satisfying NG contains only lonely
  integer tuples, and it can be dropped through gate criterion (ii). The
  same d keeps working for all its lifts.
- **Implementation.** `orbit_filter.c` with flag `ng`; `cascade.sh` with
  `CASCADE_NG=1`. Divisors d | l are tried.

---

## 5. Why small gates leave persistent families, and what kills them

**Worked case: k = 7, p = 11.** This is a Lemma S prime, since
9 ≤ 11 ≤ 15. Level one has 3 orbits.

- **The plain binary cascade (witness + gcd) does not close.** The improper
  orbit counts at levels 2, 4, …, 256 are 35, 252, 142, 34, 42, 82, 162, 322.
  They grow without bound.
- **The survivors at level 64** look like (1, x, 64, 128, 192, 256, 320) mod
  704: five coordinates ≡ 0 (mod 64), and two odd ones. These are dyadic
  near-gcd families. In the 2-adic limit, five speeds are "divisible by an
  arbitrarily high power of 2", and the binary grid cannot see the shift
  argument.
- **With Lemma NG** (d | l), 12 lifts are settled at level 4 (d = 4, e = 2,
  cost 2 < 4), and the cascade closes: 35, 246, 130, 12, 0 orbits at levels
  2–32. So J(7,11) is not empty, but every u ∈ Z_{11,1}^7 is settled by level
  32 in the sense of gate criterion (ii).
- **At k = 7, p = 13** (= 2k − 1; one orbit) the plain cascade already
  closes at level 16.

**The tight-orbit obstruction (general k).** Suppose k+1 is not a power of 2
and p > k+1. Then (1..k) is improper at every level 2^j: its only lonely
times are s/(k+1) with gcd(s, k+1) = 1, and these are not in
(1/(2^j p))Z. NG cannot settle it either:

- for d = 2 the cost is e ≥ 2 = d;
- for d = 4 the cost is at least e ≥ 3k/4 − 1 ≥ 4 once k ≥ 7;
- for d = 2^a > k, E is everything.

(Correction to the bullets above: the d = 4 bound is loose, and the
cleanest statement is computational. For every k ≤ 39 with k+1 not a power
of 2, and every d = 2^a ≤ 2^11, the NG condition fails for the integer tuple
(1..k); checked directly, see the one-liner in `small_gates.py`'s
companion test. The gcd clause fails too, because the tuple contains 1 and
3.) So the class of (1..k) mod 2^j·p is improper and unsettled at every
level 2^j. For such k (k = 16: k+1 = 17; k = 17: k+1 = 18) a small gate
therefore always needs a lift by the odd part of k+1. This is the role of the level-15 kill for
k = 14. For k = 15 (16 = 2⁴) the binary cascade alone can close a gate,
which is why p = 31 is so cheap.

A survey of all Lemma S primes for k = 3…11 is in
`results/small_survey.txt` (see §7).

---

## 6. Literature checked for structural consequences

**Beck–Everett, "Lonely Runner Relations"**, arXiv:2609.06259v3 (24 Nov
2026, preprint; read from the arXiv LaTeX source).

- **Thm 2** (= Thm 1(a)). Let k ≥ 2 and n ∈ Z_{>0}^k, and suppose no t has
  ‖t n_j‖ > 1/(k+1) for all j. This covers every counterexample and every
  tight instance. Then there is m ∈ Z^k with m·n = 0 and Σ m_j odd (a
  "harmful" relation), with ‖m‖₂ ≤ 2(k+1)/√(k−1) and ‖m‖₁ ≤ 2k+3.
  - The paper states distinct entries, but the proof does not use them.
  - The proof gives the general form: if lon(n) ≤ δ < 1/2, then
    ‖m‖₂² ≤ (k−1)/(1/2 − δ)².
  - For k = 15: ‖m‖₂² ≤ 73 and ‖m‖₁ ≤ 33.
- **Proof check (by reading, line by line).**
  - Lemma cosine: Σ a_r = 1 and Σ r² a_r = 1/(4h²), both by Parseval for ψ
    and ψ′.
  - Product expansion; vanishing Fourier coefficients give s_q = Σ_{E_q} w
    = Σ_{O_q} w, and Σ_q s_q = 1/2.
  - Σ_c w(c)‖Pc‖² = (k−1)/(4h²). So some q has X_q ≤ (k−1)/(2h²), and then
    ‖x − y‖² ≤ 2(‖Px‖² + ‖Py‖²) ≤ (k−1)/h².
  - Parity rounding: ‖m‖₁ ≡ Σ m (mod 2) is odd and < 2k+5.
  - We found no gap. **Label:** cited, preprint; proof verified by reading.
  - Thm 1(b) depends on the flatness constant flt(k), which is not known
    explicitly for k = 15, so it is unusable here.
- **Tests** (`beck_everett_check.py`, all pass):
  - every tight instance recorded in `results/exhaustive.txt` has a harmful
    relation of ‖m‖₂² = 3 (an a + b = c relation);
  - exhaustive test of the general-δ form, with 2,674 positive cases: k = 3
    (all tuples with entries ≤ 24, δ = 1/4, 1/3, 2/5) and k = 4 (entries
    ≤ 14, δ = 1/5, 1/4, 1/3).
- **Does it prune the gate computation? No.**
  - The relation is an identity over Z. Modulo N = lp it is a congruence.
    There are (3^15 + 1)/2 ≈ 7.2·10⁶ harmful m ∈ {−1,0,1}^15, against
    N ≤ 16·743 = 11,888.
  - In 200 random v ∈ Z_{16p}^15 (p = 251…743), some harmful
    m ∈ {−1,0,1}^15 has m·v ≡ 0 (mod N), with at least 468 completing
    half-vectors each.
  - So every residue tuple satisfies an admissible relation, and level one,
    the cascade and the kill are not reduced.
  - On the stored LRC(14) data the theorem is consistent, but only
    trivially: the persistent orbit (1..14) has 2x₁ − x₂ = 0.
- **Failed route (kept): feeding the relation into the flag bound.** A
  relation m is a dual vector: Λ = PZ^n lies in layers ⟨m,·⟩ ∈ Z at spacing
  1/‖m‖₂. Choosing the last basis vector of Λ across those layers gives
  t_d = ‖b_d^*‖_E² ≥ ‖b_d^*‖₂²/2 ≥ 1/(2·73) ≈ 0.0068. The prefix
  constraint already forces c_d ≈ 0.47, so this adds nothing. (Allikvere's
  "Sixteen lonely runners" does get a real improvement from relations, from
  497.03 to 459.08, by a different route: a rank case analysis of odd
  ternary relations, i.e. a section lattice. Not re-checked here.)

**Alon–Bucić–Davies**, arXiv:2609.36220v1 (preprint; read from the arXiv
LaTeX source, Thm affine-avoidance and Thm zonotope-covering).

- **Theorem.** If a_1, …, a_n ∈ R^k have full spark (any k of them are
  linearly independent), then for every shift b ∈ R^n,
  sup_x min_i ‖a_i·x − b_i‖ ≥ k/(2n). Consequences: Schoenberg's
  view-obstruction conjecture, and the Henze–Malikiosis covering-radius
  bound μ ≤ d/m.
- **No consequence for LRC(15).**
  - For k = 1 (LRC's setting), the bound is the trivial shifted bound
    1/(2n).
  - More basically, the statement holds uniformly over all shifts b. The
    shifted LRC is false from n = 5 (Blanco–Criado–Santos,
    arXiv:2603.24784), so no shift-uniform statement can give 1/(n+1) for
    LRC.
  - Henze–Malikiosis's d/m = (n−1)/n is larger than the LRC-equivalent
    radius (n−1)/(n+1).

---

## 7. Failed routes and open leads

- **Beck–Everett pruning:** vacuous mod N (§6).
- **Dual short vector into the flag bound:** too weak (§6).
- **Binary cascade alone at small p:** can leave dyadic near-gcd families
  (k = 7, p = 11, §5). Use NG.
- **Open: a hand proof that I(15,31,16) = ∅.**
  - At level 16 the times s/16 force some coordinate ≡ 0 (mod 16), and the
    times a/31 force the classes to be a permutation of ±(1..15). The mixed
    times (α, β) ∈ Z_16 × Z_31 do the rest.
  - No short human argument was found; the computation is the proof.
