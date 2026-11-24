# Andrews–Curtis conjecture (rank-2, length-14 frontier)

**Area:** combinatorial group theory / low-dimensional topology
**Status:** in progress. We are checking an unrefereed, computer-assisted claim independently: J. Carreras, arXiv:2607.23611v1 (July 2026). Done so far:
- Theorems 1–4 (four AC-equivalences among the six hard length-14 Miller–Schupp presentations and AK(3)) are **Lean-verified**: a checker written in plain Lean 4 replays the author's certificates, and the Lean kernel checks the run (`decide +kernel`) against our own definition of AC moves (§4 below). Before that they were certificate-checked by our Python checker.
- Our own search **re-finds** Theorems 3–4 independently, and our checker accepts the resulting certificates.
- **Theorem 6** (computer-assisted) is re-derived with our own implementation:
  - the exact bottleneck 19;
  - all exhaustive state counts at energy caps 25, 26 and 27, matching the paper exactly, including the 13,504,944 states behind the "≥ 27" lower bounds.
- **New, beyond the paper:** the cap-28, cap-29 and cap-30 exhaustions finish, with 47,544,780, 88,628,824 and **351,388,696** states and no meeting.
  - So no state below energy 30 is forward-reachable from two of AK(3), P1, P2. This is the paper's criterion, pushed from cap 27 to cap 30. In the directed reading it gives d_GS ≥ 30 for each pair, in both directions.
  - Caps 28–29 were run by two implementations, which agree exactly. Cap 30 was run by one (`ac_search_par.cpp`).
  - **Caveat found here: the GS graph is directed** (§3, "Directedness"). "No meeting" therefore gives the bound only for *directed* paths (and for paths S → X ← T). It does not give the bound for paths that may use edges backwards. The paper's d_GS does not say which reading it means. So we no longer write "d_GS ≥ c" without the word "directed".
  - All of this is graph-relative and not an AC-distance bound.
- **New: the undirected reading (§5).** We enumerate predecessors in the GS graph exactly. The derivation is in `ac_graph.py`, and the edge sets are checked exhaustively in both directions. We then searched the graph with edges usable both ways.
  - There is **no undirected GS path below energy 30** between any two of AK(3), P1, P2. This is computed, exhaustive and relative to the graph. It matches the directed cap-30 result, so the undirected reading now goes as far as the directed one.
  - So **Theorem 6's lower bounds (d_GS ≥ 27) hold in the undirected reading too**, and the possible gap is closed at the paper's own level.
  - The bottleneck 19 for P3, P4 vs AK(3) also holds undirected.
- AK(3) and the conjecture itself remain open.

**Started:** 2026-11-24
**ProofAtlas:** rank 383, "open_with_solved_subcases". Its AC research workspace lists the Carreras preprint (2026-07-26) and says: "ProofAtlas did not replay its certificates or independently check its exhaustive-search claims."

## Statement

A *balanced presentation* ⟨x₁,…,x_n | r₁,…,r_n⟩ of the trivial group is *AC-trivializable* if it can be turned into ⟨x₁,…,x_n | x₁,…,x_n⟩ by a finite sequence of *AC moves*:
- r_i ← r_i⁻¹;
- r_i ← r_i r_j^{±1} (j ≠ i);
- r_i ← w r_i w⁻¹ for a word w.

Two presentations are *AC-equivalent* if such moves turn one into the other. The moves are invertible, so this is an equivalence relation.

**Conjecture (Andrews–Curtis 1965).** Every balanced presentation of the trivial group is AC-trivializable.

This is the classical (unstabilized) version. The *stable* version also allows adding a generator x_{n+1} together with the relator x_{n+1}. It is weaker and not considered here.

**Notation** (as in Carreras and in Shehper et al.):
- AK(n) = ⟨x, y | xⁿ = yⁿ⁺¹, xyx = yxy⟩. AK(3) has total relator length 13.
- MS(n, w) = ⟨x, y | x⁻¹yⁿx = yⁿ⁺¹, x = w⟩, with relators (x⁻¹yⁿxy⁻⁽ⁿ⁺¹⁾, x⁻¹w). Here w has exponent sum 0 in x.

## The claim being checked (Carreras, arXiv:2607.23611v1, 26 Jul 2026)

**Source.**
- J. Carreras, "Machine-checkable equivalence certificates at the length-14 Andrews–Curtis frontier", arXiv:2607.23611v1. We read the full PDF (10 pp., sha256 `cc8ff285…dcd8`).
- Artifact: github.com/joe-carr-data/ac-certificates, tag v1.0; Zenodo DOI 10.5281/zenodo.21499081 (record 21499081, v1.0, `ac-certificates-v1.0.zip`, md5 `c1109300a3281b0edeef32acc2c1ae1b`, as stated by Zenodo and re-computed here).
- The arXiv ancillary files are byte-identical to the Zenodo copies of the five theorem certificates.
- The author states that the work was done "in a human-directed collaboration with AI systems". The paper is not refereed.

**Background claims it builds on** (cited, not checked here):
- Every two-generator balanced presentation of the trivial group of total length ≤ 12 is AC-trivializable (Miasnikov–Myasnikov, arXiv:math/0304305).
- At length 13, every such presentation is AC-trivializable or AC-equivalent to AK(3) (Havas–Ramsay, IJAC 13 (2003)).
- Shehper et al. (arXiv:2408.15332v2, p. 10) find six length-14 Miller–Schupp presentations that their greedy search does not solve.
  - They state that four of them are AC-equivalent to AK(3), with no published move sequences.
  - Two are "holdouts".

**The six presentations**, in Carreras' naming (P1 also equals Johnson's ⟨x, y | x⁻¹y²x = y³, y⁻¹x²y = x³⟩ up to rotation):

| # | presentation | Shehper et al. | Carreras |
| --- | --- | --- | --- |
| P1 | MS(2, x⁻²y⁻¹x²y) | "AC-equiv. to AK(3)" | ~ P6 (Thm 1) |
| P2 | MS(2, x⁻²y⁻¹x²y⁻¹) | "AC-equiv. to AK(3)" | ~ P5 (Thm 2) |
| P3 | MS(3, yx²y) | "AC-equiv. to AK(3)" | ~ AK(3) (Thm 3) |
| P4 | MS(3, y⁻¹x²y⁻¹) | "AC-equiv. to AK(3)" | ~ AK(3) (Thm 4) |
| P5 | MS(2, yx²yx⁻²) | holdout | ~ P2 (Thm 2) |
| P6 | MS(2, yx²y⁻¹x⁻²) | holdout | ~ P1 (Thm 1) |

**Exact claims checked here.**
- *Theorems 1–4.* P1 ~AC P6; P5 ~AC P2; P3 ~AC AK(3); P4 ~AC AK(3).
  - Each comes with a JSON certificate of elementary moves.
  - The paper reports these counts: moves (classical count) and peak total / single relator length:

    | Theorem | moves (classical) | peak total / single |
    | --- | --- | --- |
    | 1 | 36 (58) | 27 / 17 |
    | 2 | 85 (155) | 33 / 21 |
    | 3 | 66 (101) | 24 / 15 |
    | 3, second certificate | 71 (106) | 22 / 15 |
    | 4 | 13 (22) | 23 / 14 |

- *Theorem 6* (computer-assisted; relative to the search engine). The paper works in the "canonical GS-substitution graph":
  - vertices are pairs of cyclically reduced relators, taken up to swap, inversion and rotation;
  - edges are products r_i ← rot(r_i)·rot(r_j)^{±1} with a cancelling junction, then cyclically reduced;
  - a vertex's energy is its total length; d_GS is the minimax (bottleneck) energy of a path.
  - The paper's definition, quoted exactly (§5, p. 6): "For a path γ, define its bottleneck B(γ) = max_{P∈γ} E(P); for states S, T define d_GS(S, T) = min_{γ : S⇝T} B(γ)." It also says: "edges are their substitution moves (cyclically aligned products with a cancelling junction)". The search is "bidirectional multi-source bottleneck-Dijkstra". The proof of the lower bounds says that the cap-26 search "exhausted 6,212,968 canonical states without any cross-source intersection, excluding every GS path of bottleneck ≤ 25".
  - The paper does not say whether the graph is directed or whether a path may use an edge backwards. **The graph is in fact directed** (see §3). The search only follows edges forward, from each source.

  The claims:
  - d_GS(MS(3, yx²y), AK(3)) = 19.
  - d_GS(P1, AK(3)), d_GS(P2, AK(3)) and d_GS(P1, P2) are all ≥ 27.
  - Exclusive cap 25: 1,532,732 / 135,892 / 168,304 states are settled from AK(3) / P1 / P2.
  - Exclusive cap 26: 6,212,968 states, with no meeting.
  - Exclusive cap 27: 13,504,944 states, with no meeting.
  - The author stresses that these are statements about this graph only, not about AC distance.

**Possible gap in Theorem 6 (found here).**
- A forward-only search with no cross-source intersection below cap c shows exactly this: no state of energy < c is forward-reachable from two different sources.
- This excludes every directed path S⇝T, in either direction, with bottleneck < c. Each source is in the table, so reaching it from another source is an intersection. It also excludes paths of the form S → X ← T.
- It does **not** exclude zig-zag paths such as S → X ← Y → Z ← T, which use edges backwards. Every edge is still a valid AC-equivalence, so such a path would still give a certificate.
- So Theorem 6's lower bounds hold if d_GS uses directed paths ("γ : S⇝T"). If d_GS allows edges to be used backwards, the cited search does not prove them. The paper does not settle which reading is meant.
- For the upper bound d_GS(P3, AK(3)) ≤ 19, both readings are fine here: our passive-source runs find directed paths P3 ⇝ AK(3) and AK(3) ⇝ P3, each with bottleneck 19, and likewise for P4.
- **Gap closed at the paper's level (§5).** An undirected search enumerates predecessors exactly. It finds no GS path between two of AK(3), P1, P2, using edges in either direction, with all energies below 30. So the paper's lower bounds d_GS ≥ 27 hold in the undirected reading as well, and in fact d_GS ≥ 30 in that reading.

  The exact value 19 for P3/P4 vs AK(3) also holds undirected.

Not checked: the §6 analysis of the Two-Hump classification table, the 214-pair σ-merge programme, and the AC-19 membership audit. These need third-party files that the artifact does not redistribute.

## Known results

- AK(2) is AC-trivial (Miasnikov, "Genetic algorithms and the Andrews–Curtis conjecture", IJAC 1999; cited as [Mia03] by Shehper et al.). Re-found here as a pipeline check.
- Length ≤ 12 and length 13 in rank 2: see above (Miasnikov–Myasnikov; Havas–Ramsay).
- Panteleev–Ushakov (arXiv:1609.00325): every automorphism of F₂ is AC-realized on AK(n). [cited by Carreras, not read]
- Borovik–Lubotzky–Myasnikov (arXiv:1103.1295): finite quotients cannot obstruct AC-equivalence beyond abelianization. [cited by Carreras, not read]
- Two-Hump (Fagan et al., arXiv:2606.21611, ICML 2026) released AC-19, a set of more than 140,000 solved presentations. [not read]

## Approaches

### 1. Independent replay of the author's certificates (worked)

- **Our checker.** `ac_check.py` was written from the move definitions in §2 of the paper, *without* reading or importing the author's `ac_verify.py`.
  - Moves are checked as exact free-group operations: invert, mul (i ≠ j, e = ±1), conj by one generator, and cycle.
  - Cycle by k replaces r = uv by u⁻¹(uv)u = vu, so it is a conjugation. A rotation of a word that is not cyclically reduced is still a conjugation, hence still sound.
- **Endpoints.** Certificates end at a recorded state `reached` inside the {swap, invert, rotate} orbit of `target`.
  - We do not rely on the orbit argument. `bridge()` writes out explicit elementary moves to the exact target: rotation, inversion, and the 6-move swap (a,b) → (ab,b) → (ab,b⁻¹) → (ab,b⁻¹ab) → (ab,a) → (aba⁻¹,a) → (b,a).
  - `prove_named()` does the same from and to the presentations *built from their definitions*: MS(n,w), AK(n), and Johnson's P1.
  - The final check is always the same: one explicit move list, replayed from presentation A, gives exactly presentation B.
- **Result (`python3 ac_check.py --theorems certs`, 0.03 s).**
  - All 5 certificates pass.
  - Packaged moves, classical moves and peak lengths match the paper's table *exactly*: 36 (58), 27/17; 85 (155), 33/21; 66 (101), 24/15; 71 (106), 22/15; 13 (22), 23/14. Our cycle semantics also reproduce the recorded `reached` states exactly.
  - Explicit chains between the named presentations have 40, 87, 103, 108 and 34 moves.
  - The abelianization determinant is ±1 for all of them, a sanity check only.
- **Provenance of the replayed files.**
  - `computations/andrews-curtis/certs/` holds the **author's** certificate files, copied unchanged and replayed by **our** checker.
  - Source: the arXiv ancillary files of 2607.23611v1 (`https://arxiv.org/src/2607.23611v1/anc/certs/…`), byte-identical to `certs/` in Zenodo record 21499081 (v1.0).

  | file (author's) | sha256 | theorem |
  | --- | --- | --- |
  | `cert_sym_equiv_orphan1.json` | `b8ead47e6f40801cfe5dc92d5e8e7374389438035e513a72094ae1e0b3fbbc0f` | 1 |
  | `cert_idx0_equiv_mirror.json` | `6f55a391077991fd41bcae8ea9fd655a6f1406ae6d09b6e9c2b50a0060fcdd86` | 2 |
  | `bottleneck_ak_f3_cert.json` | `8f16b97aa59057885589e1fc8aa187af26bf709a156af31ee890888a35042648` | 3 |
  | `cert_ms3_yx2y_equiv_ak3.json` | `9cfeff76a1ec2e81bf6a66eb8b16954683fdd5aade3bdc42283726a9a4c7d697` | 3 (second) |
  | `cert_ms3_yinvx2yinv_equiv_ak3.json` | `20d9fd3db1847a7e1502cf3a3fa037042669e2b6b8de899660da99136aeb69b4` | 4 |

  - The sha256 prefixes printed in the paper's table agree with these.
  - `computations/andrews-curtis/certs_ours/` holds certificates **generated here** by `ac_search` + `ac_path`:
    - `ms3_yx2y_to_ak3.json` (sha256 `76e35e72…797b`);
    - `ms3_yinvx2yinv_to_ak3.json` (`8dbd1728…d76d`);
    - `ak2_trivial.json` (`fe142ee4…e3e5`).
    - These were found by a search other than the author's, so they do not depend on the author's files.
- **Tests** (`test_ac.py`):
  - the swap macro and the orbit bridge on random words;
  - |det| of the abelianized exponent matrix is invariant under random move sequences;
  - 125 single-move corruptions of the five certificates are all rejected;
  - a wrong target and wrong named endpoints are rejected.
- No code from the author's artifact was executed here: not `ac_verify.py`, `selftest_ac.py`, `ak_bottleneck.py` or `bn.cpp`. One attempt to run `ac_verify.py` as a cross-check was refused by the session's permission policy and was not pursued. All checks above use our own code only.
- The four Two-Hump trivialization certificates in the artifact (`cert_u066`, `cert_twohump_u066`, `cert_u102`, `cert_twohump_u102`) also replay to ⟨x, y | x, y⟩ under our checker. This was a side check; it is not a claim of the paper's theorems.

### 2. Are P3 and P4 the presentations Shehper et al. meant? (checked; one pitfall)

- Shehper et al. (v2, p. 11, checked on the rendered page) print the MS(3) cases as ⟨x, y | x⁻¹y³x = y⁴, x = y^{±1}x²y^{±1}⟩. Carreras takes P3, P4 from that text.
- **Pitfall.** Here w = y^{±1}x²y^{±1} has x-exponent sum 2, so taken literally it is not a Miller–Schupp word.
  - The released benchmark data has every w with x-exponent sum 0 (1,190/1,190 entries). That data is `ac_solver/search/miller_schupp/data/*.txt` at github.com/shehper/AC-Solver `main`, fetched via raw.githubusercontent.com. Its `all_presentations.txt` is byte-identical to the copy in Carreras' artifact.
  - Its six unsolved length-14 entries (all presentations minus greedy-solved; 1,190 − 533 = 657 unsolved) are the four MS(2) cases above, plus MS(3, yxyx⁻¹) and MS(3, x⁻¹y⁻¹xy⁻¹).
  - We first read this as a mismatch. **It is not one.** x⁻¹y⁻¹x²y⁻¹ is the inverse of a rotation of x⁻¹yxyx⁻¹: both say x² = yxy. Likewise x⁻¹yx²y matches x⁻¹y⁻¹xy⁻¹ (both say x² = y⁻¹xy⁻¹).
  - So P4 ≡ MS(3, yxyx⁻¹) and P3 ≡ MS(3, x⁻¹y⁻¹xy⁻¹) up to rotation and inversion, with the ± signs crossed. This is checked in `test_named_presentations`.
- **Conclusion.** Theorems 3–4 do concern the two MS(3) presentations of the released benchmark. The "first public certificates" wording is the author's; we did not audit novelty.

### 3. Our own search: rediscovery, Theorem 6, and its extension to caps 28–29 (worked)

- **Search.** `ac_search.cpp` was written here.
  - It does a multi-source minimax search over pairs of cyclically reduced words, taken up to swap, inversion and rotation.
  - Edges: r_i ← cyclic_reduce(rot(r_i)·rot(r_j)^{±1}). With `--junction`, only products whose junction cancels are used. This is our reading of the GS-substitution graph.
  - States are settled in nondecreasing bottleneck. A state of total length ≥ cap is never entered.
- **Path expansion.** `ac_path.py` turns a path of canonical states into elementary moves: rotations, a possible inversion, one mul, conjugations to cyclically reduce, and a final orbit bridge. `ac_check` then checks the result. So nothing in the search has to be trusted for positive claims.
- **Pipeline check.** AK(2) → ⟨x, y | x, y⟩ found at bottleneck 13; the 34-move certificate passes. As a negative control, AK(3) and the trivial presentation do not meet below total length 14.
- **Rediscovery of Theorems 3–4.**
  - P3 → AK(3) and P4 → AK(3) are each found in under 1 s.
  - They expand to certificates of 149 and 45 elementary moves (peak total 29 and 33). `ac_check` accepts both, and they are saved in `certs_ours/`.
  - These are certificates generated by us and independent of the author's.
- **Bottleneck 19 (Theorem 6).** In our graph:
  - cap 19 is exhausted with no meeting, for both P3–AK(3) and P4–AK(3);
  - cap 20 meets.
  - With the passive-source option of `ac_search_compact` (one source expanded, the other only a target), there is a **directed** path P3 ⇝ AK(3) of bottleneck 19, and also AK(3) ⇝ P3, P4 ⇝ AK(3) and AK(3) ⇝ P4. Cap 19 is exhausted in each direction with no path.
  - So the minimax energy is exactly **19** for both pairs, in the directed reading and in both directions. The paper states 19 for P3. The upper bound 19 also holds in the undirected reading. The lower bound holds there as well, by the undirected search of §5 (exhausted below 19).
- **Cap-25 counts (Theorem 6).** Sources {AK(3)}, {P1}, {P2}, exclusive cap 25: 1,836,928 states settled, **1,532,732 / 135,892 / 168,304** per source, no meeting. This took 83 s and about 0.4 GB.
  - These are *exactly* the paper's numbers.
  - The match is good evidence that our graph is the same as the paper's GS graph. Equal counts from two independent implementations are evidence, not a proof that the graphs coincide.
- **Cap 26 (Theorem 6).** Same three sources, exclusive cap 26: **6,212,968** states settled, no meeting. This took 5 min 26 s on one core.
  - Per source: 5,431,780 (AK(3)), **356,836** (P1), **424,352** (P2).
  - The total matches the paper's 6,212,968. The P1 and P2 numbers match the paper's "energy ≤ 25" figures in §5 exactly.
  - So no state of energy < 26 is forward-reachable from two of AK(3), P1, P2. In particular, no directed path in this graph joining two of them, in either direction, has bottleneck < 26.
- **Cap 27 (Theorem 6).** Exclusive cap 27: **13,504,944** states settled, no meeting. This took 834 s wall on one core at 3.01 GB peak RSS.
  - Per source: 10,118,636 (AK(3)), **851,836** (P1), **2,534,472** (P2).
  - The total and the P1/P2 counts all equal the paper's numbers.
  - So no state of energy < 27 is forward-reachable from two of the sources. This is the lower-bound half of Theorem 6, re-derived here exactly as the paper's procedure states it. It gives d_GS ≥ 27 in the directed reading, both directions. The undirected reading is settled separately in §5, also at ≥ 27.
  - The paper's cap-28 run hit its 40M-state budget and was inconclusive.
- **Cap 28 (beyond the paper).** Exclusive cap 28 from {AK(3)}, {P1}, {P2}, run with `ac_search_compact.cpp`.
  - That engine explores the same graph using about 30 B per state instead of about 220 B: packed 2-bit words, an append-only state array, and an open-addressing index.
  - Its per-level and per-source counts equal those of `ac_search.cpp`: cap 25 in full; cap 21 in `test_ac.py`; and in this run, levels ≤ 26 again give exactly 6,212,968 and 13,504,944.
  - **Result: 47,544,780 states settled, no meeting.** It took 1,050 s on one core at 1.67 GB peak RSS.
  - Per source: 36,700,896 (AK(3)), 2,323,596 (P1), 8,520,288 (P2).
  - So **no state of energy < 28 is forward-reachable from two of AK(3), P1, P2.** Hence directed d_GS ≥ 28 for each pair, in both directions.
  - This extends the paper's Theorem 6. The paper's cap-28 run stopped at its 40M budget while processing barrier 27, with partial counts 1,987,856 (P1) and 5,640,276 (P2), below our full counts as they must be.
- **Cap 29 (beyond the paper).** Same engine and sources, exclusive cap 29.
  - **Result: 88,628,824 states settled, no meeting.** It took 2,028 s on one core at 3.05 GB peak RSS.
  - Per source: 68,481,208 (AK(3)), 5,374,816 (P1), 14,772,800 (P2).
  - So **no state of energy < 29 is forward-reachable from two of AK(3), P1, P2.** Hence directed d_GS ≥ 29 for each pair, in both directions.
  - In the same run, the levels below 28 again gave exactly the cap-28 counts (47,544,780; 36,700,896 / 2,323,596 / 8,520,288).
- **Passive-source runs (directed reachability from one source only).** `ac_search_compact ... P --passive AK3 Q` expands only P. It reports a meeting if P's forward sublevel set contains AK(3) or Q.
  - Validation: at exclusive caps 25 and 29, P1 alone settles 135,892 and 5,374,816 states, and P2 alone settles 168,304 and 14,772,800. These are exactly the per-source counts of the multi-source runs, as they must be when there is no meeting.
  - **Cap 30, P1 alone:** 17,796,820 states settled, and the set contains neither AK(3) nor P2. This took 496 s on one core at 0.96 GB peak RSS.
  - So there is no directed path P1 ⇝ AK(3) and no directed path P1 ⇝ P2 with all energies < 30. On its own this says nothing about paths *into* P1, or about V-shaped or zig-zag paths. The multi-source run below covers the V-shaped paths.
- **Cap 30 (beyond the paper).** Same sources and exclusive cap 30, run with `ac_search_par.cpp`.
  - That engine explores the same graph with different data structures. Each state is one 64-bit hash-table entry: a 56-bit mixed-radix key plus level, group and settled bits. There are no parent pointers and no queue. The levels are processed in order by 4 threads.
  - Its move generation and canonicalisation code is copied from `ac_search_compact.cpp`, so it is a *second implementation* (different data structures and parallelism), not an independent one.
  - Validation: at cap 25 it gives 1,532,732 / 135,892 / 168,304. At cap 27 it gives 13,504,944 (10,118,636 / 851,836 / 2,534,472), in 93 s.
  - Inside the cap-30 run, the cumulative counts after levels 26, 27 and 28 are exactly the cap-27, cap-28 and cap-29 totals and per-source counts above. The "seen" counts after levels 25 and 26 (107,663,712 and 189,133,772) are identical to those of the compact engine's cap-30 attempt.
  - **Result: 351,388,696 states settled, no meeting.** It took 3,210 s wall (4 threads) at 4.73 GB peak RSS, with a 600M-slot table.
  - Per source: 284,176,652 (AK(3)), 17,796,820 (P1), 49,415,224 (P2). The P1 count equals the P1-only passive run exactly, as it must.
  - So **no state of energy < 30 is forward-reachable from two of AK(3), P1, P2.** Hence directed d_GS ≥ 30 for each pair, in both directions. The same bound, d_GS ≥ 30, holds in the undirected reading (§5).
  - Before this, a cap-30 attempt with `ac_search_compact` hit its 190M-state budget at level 27 (peak 5.6 GB). That engine stores every state seen below the cap, and the planning estimate of 165M states was far too low.
- Caveat for caps 28–30.
  - Caps 28 and 29 now have two implementations that agree exactly: `ac_search_compact`, and `ac_search_par` (inside its cap-30 run).
  - Cap 30 has one. `ac_search.cpp`, which was written separately, needs about 10 GB at cap 28 and was not run there.
  - All engines match the paper exactly at caps 25–27. The graph-relative scope noted below applies in full.
- **The full graph** (all rotations, not only cancelling junctions) is barely larger but about 20× slower in our implementation.
  - Cap 21: 41,306 states against 40,078 with `--junction`. Cap 23: 285,760 against 274,430. No meeting in either.
  - It was not pushed further.
- **Directedness (found here).** The junction GS graph is not symmetric.
  - Example: from S = (x⁻³y⁴xyxy⁻¹x⁻¹y⁻¹, x⁻¹y⁻¹x⁻¹yxy) (canonical words `XXXyyyyxyxYXY` | `XYXyxy`, energy 19), multiplying the first relator by the inverse of the second cancels all of it and gives AK(3) = (`XXXyyyy` | `XYXyxy`).
  - The reverse product, AK(3)'s x⁻³y⁴ times a rotation of xyxy⁻¹x⁻¹y⁻¹ (or of its inverse), only gives back S through a product with a non-cancelling junction. That edge is not in the graph.
  - A brute-force check (a scratch script, not kept in the repo) took every state of energy < 20 forward-reachable from AK(3), P1 or P2: 20,236 states, the same count as the engines. It found that **168 of the 79,752 edges among them have no reverse edge**. Below energy 18 there were none among 3,446 edges.
  - Consequences:
    - (a) Every search here and in the paper is forward-only. "No meeting below cap c" means *no state of energy < c is forward-reachable from two different sources*.
    - (b) That excludes all directed paths between the sources, in both directions, and all paths of the form S → X ← T.
    - (c) It does not exclude zig-zag paths that use some edges backwards. Every edge is an AC-equivalence, so those would also give AC certificates.
  - Deciding the undirected question needs predecessor enumeration in this graph. It is done in §5.
- **Scope.** As the author says, Theorem 6 is a statement about this graph. It is not an AC-distance bound and not evidence of AC-inequivalence.

### 4. Lean-verified certificate checking (worked)

The files are in `computations/andrews-curtis/lean/`. They use plain Lean 4 core v4.34.1, with no Mathlib.

**Definitions** (`AC/Defs.lean`). These fix what is claimed.
- A word is a `List L`, with letters `x, X = x⁻¹, y, Y = y⁻¹`.
- `FreeEq` is the equivalence relation generated by deleting a cancelling pair anywhere: `p ++ a :: a⁻¹ :: q ~ p ++ q`. Words up to `FreeEq` are the elements of F(x, y).
- A presentation `Pres` is a pair of words (r₀, r₁).
- `ACStep` has exactly the moves of the Statement above, for i = 0, 1:
  - r_i ← r_i⁻¹;
  - r_i ← r_i r_j^{±1} (j ≠ i);
  - r_i ← w r_i w⁻¹ for any word w;
  - replacing r_i by a freely equal word.
- `ACEquiv` is the reflexive–transitive closure of `ACStep`. It is proved symmetric (`ACEquiv.symm`): each move is undone by moves.
- Every `ACStep` is a genuine AC move on the group elements, or the identity on them. So `ACEquiv P Q` implies that P and Q are AC-equivalent in the classical sense.
- **Rotation and swap are not primitive.**
  - The checker's `cycle` move (r = uv ↦ vu) is literally `conj` by u⁻¹ followed by a free step.
  - The relator swap is never used as a primitive. `gen_lean.py` expands every orbit step into ordinary moves, using the 6-move swap of §1, so each chain ends at the exact target words.
- The named presentations are written from their definitions:
  - `MS n w = (x⁻¹yⁿxy⁻⁽ⁿ⁺¹⁾, x⁻¹w)`;
  - `AK n = (xⁿy⁻⁽ⁿ⁺¹⁾, xyxy⁻¹x⁻¹y⁻¹)`;
  - `johnsonP1 = (x⁻¹y²xy⁻³, y⁻¹x²yx⁻³)`.
  - `AC/Audit.lean` checks by `rfl` that these are the explicit words below.

**Checker and soundness** (`AC/Checker.lean`).
- `check p ms q : Bool` replays the JSON move types (`invert`, `mul`, `conj`, `cycle`) with free reduction `red` (stack reduction), then compares the result with q.
- `check_sound : check p ms q = true → ACEquiv p q` is proved. Its key lemma is `freeEq_red : FreeEq w (red w)`.

**Certificates** (`AC/Certs.lean`, generated by `gen_lean.py` from the JSON files).
- For each claim the file contains:
  - the certificate moves, verbatim;
  - `_replay`: the JSON `initial` goes to the JSON `reached`;
  - `_check`: `check A (pre ++ cert ++ post) B = true`, where A and B are the Lean-defined presentations and pre/post are the explicit bridge moves;
  - the theorem `ACEquiv A B`.
- Each `_check` and `_replay` is proved by `decide +kernel`, so the Lean kernel evaluates the replay. `native_decide` is not used.
- The theorems, in explicit words (`AC/Audit.lean`):
  - `carreras_thm1 : ACEquiv ([X,y,y,x,Y,Y,Y], [Y,x,x,y,X,X,X]) ([X,y,y,x,Y,Y,Y], [X,y,x,x,Y,X,X])`. This is Johnson's P1 ~ P6.
  - `carreras_thm1_MS`: the same with P1 = MS(2, x⁻²y⁻¹x²y) = ([X,y,y,x,Y,Y,Y], [X,X,X,Y,x,x,y]).
  - `carreras_thm2 : ACEquiv ([X,y,y,x,Y,Y,Y], [X,y,x,x,y,X,X]) ([X,y,y,x,Y,Y,Y], [X,X,X,Y,x,x,Y])`. This is P5 ~ P2.
  - `carreras_thm3 : ACEquiv ([X,y,y,y,x,Y,Y,Y,Y], [X,y,x,x,y]) ([x,x,x,Y,Y,Y,Y], [x,y,x,Y,X,Y])`. This is P3 ~ AK(3).
  - `carreras_thm4 : ACEquiv ([X,y,y,y,x,Y,Y,Y,Y], [X,Y,x,x,Y]) ([x,x,x,Y,Y,Y,Y], [x,y,x,Y,X,Y])`. This is P4 ~ AK(3).
  - `ak2_trivial : ACEquiv ([x,x,Y,Y,Y], [x,y,x,Y,X,Y]) ([x], [y])`.
  - Also `thm3b` (the second Thm-3 certificate), and `ours_thm3`, `ours_thm4` (our own search's certificates). All three are in the MS/AK form.
- The explicit chains have 40, 87, 103, 108, 34 moves (author's certificates), 149 and 45 moves (ours), 34 moves (AK(2)), and 1 move (P1 in MS form to Johnson's form).
- **Trust base:** the Lean 4.34.1 kernel (and its `decide +kernel` evaluation of `check`), plus the definitions in `AC/Defs.lean`.
- `#print axioms` gives `[propext]` for every theorem: no `sorryAx` and no `Lean.ofReduceBool`.
- `leanchecker` re-checks the compiled modules: AC.Certs in 3.1 s. `leanchecker --fresh AC.Audit` replays everything from scratch, Init included, in 65 s.
- **Cost:** `build.sh` takes about 6 s in total. Generating and kernel-checking all certificates takes 4.5 s, at under 1 GB.
- **Negative controls.**
  - In `AC/Certs.lean`, the kernel evaluates `check` to `false` for: three single-move corruptions of the Theorem 4 chain; the right chain with the wrong target AK(2); and the right chain from the wrong source P3.
  - `test/BadCert.lean` claims `= true` for a corrupted chain. `build.sh` requires it to fail, and it does ("decide proved that the proposition … is false").
- **Pitfall.** A corrupted chain can blow up word lengths exponentially, because products double the length. Replaying the Theorem 3 chain from P4 reaches 650k letters. With a raised `maxRecDepth`, the kernel then ran out of memory. With the default it stops at "deep recursion". So `gen_lean.py` does not raise `maxRecDepth`, and it uses the Theorem 4 chain from P3 (at most 307 letters) as the wrong-source control.

### 5. The undirected GS graph: exact predecessors and undirected search (worked)

**Predecessors** (`ac_graph.py`; the same enumeration is `preds_of` in the C++ engines).
- An edge S = {u, v} → T = {p, v} keeps v and replaces u by p ~ cyclic_reduce(A·B). Here A is a rotation of u and B a rotation of v^{±1}, and last(A) cancels first(B).
- In the cyclic word A·B, every cancelling pair joins a letter of A to a letter of B. The only exception comes after one of the two words is consumed completely: then the leftover arc can cancel with itself.
- Write M for a rotation of p^{±1} and Z for the consumed part. Then u is exactly one of:
  - (I) **f M f⁻¹ Z**, with Z a rotation of v^{±1}, f any word, and the whole cyclic word reduced. Here B is consumed, and u's own arc may then cancel; that arc is f.
  - (II) **M₁ Z**, where M = M₁M₂ with M₁, M₂ nonempty, M₂ Z⁻¹ is a rotation of v^{±1}, Z is nonempty, and M₁ Z is cyclically reduced. Here both words leave an arc.
  - (III) **Z**, where g M g⁻¹ Z⁻¹ is a rotation of v^{±1}, Z is nonempty, and Z is cyclically reduced. Here A is consumed.
- Conversely, each shape gives an edge by an explicit choice of A and B (for example A = f M f⁻¹ Z and B = Z⁻¹ in shape (I)).
- The forward move rotates only u's canonical orientation. The three shapes are closed under inverting u, so this restriction never matters. Dropping the orientation test changes nothing in the exhaustive check below.
- Length bounds: |u| = 2|f| + |p| + |v| in (I), |p| + |v| − 2|M₂| in (II), and |v| − |p| − 2|g| in (III). So the enumeration below a cap is finite.

**Validation** (`test_ac.py`).
- *Exhaustive on all states.* For **every** state of energy ≤ 12, pred() equals the inverted forward map: 0 mismatches. The test suite runs energy ≤ 9, which is 4,244 states and 9,301 edges; ≤ 12 was run once by hand.
  - As mutation checks, dropping shape (I)'s f, shape (II) or shape (III) gives 128, 1,673 and 768 mismatches at energy ≤ 9. So each shape is needed.
- *Both directions below energy 20.*
  - The forward closure of {AK(3), P1, P2} again gives 20,236 states, 79,752 edges and 168 one-way edges.
  - The **undirected** closure has 20,656 states. Its forward-edge set and its predecessor-edge set are **identical**: 80,172 edges, 588 of them one-way.
  - The C++ engines (`ac_search_par --undirected` and `ac_search_compact --undirected`) settle exactly these 20,656 states, 20,024 / 399 / 233 per source. The two engines also agree at caps 22 and 23.
- *Controls in undirected mode.*
  - P3 and P4 vs AK(3): exhausted below 19, and a meeting at bottleneck 19. The paths expand to certificates that `ac_check` accepts. So d_GS = 19 holds in the undirected reading too.
  - AK(2) vs ⟨x, y | x, y⟩: a meeting at bottleneck 13, with an accepted certificate.
  - AK(3) vs the trivial presentation: no meeting below 14.
  - A path through the one-way edge S → AK(3) of "Directedness", used backwards, expands to an accepted certificate. `ac_path.py` classifies every path edge against the graph and expands a backward edge by inverting the forward step move by move. A pair of states that is not an edge is rejected.

**Undirected search: no meeting below cap c.** Sources {AK(3)}, {P1}, {P2}; edges usable in both directions; exclusive cap c; `ac_search_par --undirected`, 4 threads. The settled sets are then the connected components of the sources in the undirected graph on states of energy < c.

| cap c | states settled (AK(3) / P1 / P2) | directed count, for comparison | wall time | result |
| --- | --- | --- | --- | --- |
| 20 | 20,656 (20,024 / 399 / 233) | 20,236 | < 1 s | no meeting |
| 24 | 1,033,896 (891,748 / 63,220 / 78,928) | — | 20 s | no meeting |
| 25 | 1,913,268 (1,596,072 / 141,740 / 175,456) | 1,836,928 | 34 s | no meeting |
| 26 | 6,373,628 (5,562,224 / 371,140 / 440,264) | 6,212,968 | 142 s | no meeting |
| 27 | 13,873,120 (10,340,996 / 877,892 / 2,654,232) | 13,504,944 | 284 s, 1.1 GB | no meeting |

- **Single-source components (for caps ≥ 28).** The graph is undirected here, so the settled set of a source is its connected component in the sublevel graph.
  - If P1's component below c contains neither AK(3) nor P2, and P2's component contains not AK(3), then no two of the three sources are joined below c.
  - So it is enough to expand P1 and P2 alone, with the other sources passive (`ac_search_par c --undirected P1 --passive AK3 P2`, and likewise for P2). The much larger AK(3) component never has to be built.
  - Validation at cap 27: the passive runs settle 877,892 (P1) and 2,654,232 (P2) states, equal to the per-source counts of the multi-source run.

  | cap c | P1 component (directed count) | P2 component (directed count) | contains another source? |
  | --- | --- | --- | --- |
  | 27 | 877,892 (851,836), 22 s | 2,654,232 (2,534,472), 53 s | no |
  | 28 | 2,376,948 (2,323,596), 48 s | 8,780,944 (8,520,288), 178 s | no |
  | 29 | 5,493,468 (5,374,816), 154 s | 15,211,400 (14,772,800), 321 s | no |
  | 30 | 18,141,004 (17,796,820), 409 s, 0.4 GB | 50,655,984 (49,415,224), 1,180 s, 0.8 GB | no |

  Times are wall-clock on 4 threads. Each "directed count" is the per-source count of the forward search at the same cap (§3).

- Hence there is **no undirected GS path below energy 30** joining two of AK(3), P1, P2. This is computed, exhaustive, one implementation (two engines sharing the predecessor code) and relative to the graph.
- Each undirected sublevel set is only 3–4% larger than the directed one, but a state costs about 3× more to expand. A multi-source cap-30 run would need about 360M states and over 2 h on 4 threads; the single-source runs avoid this.
- **Scope.** This is a statement about the GS graph, not about AC distance. A zig-zag path in the graph would still have given an AC certificate. No such path exists below 30.
- **Pitfall (found and fixed here; no reported result affected).** `ac_search_par` stored a state as a 56-bit key: (letters in mixed radix) × 512 + a code for the two lengths.
  - At total length 30 that overflows: 16·3²⁸·512 ≈ 2^57.4. So the engine was exact only for caps ≤ 30. At total length ≤ 29 the largest key is 6.2·10¹⁶ < 2⁵⁶.
  - Every run reported above, directed and undirected, used cap ≤ 30. A first undirected cap-31 attempt was stopped and discarded.
  - The key is now an exact ranking: an offset for the two lengths plus the mixed radix. It fits in 56 bits up to total length 31, and the engine refuses CAP > 32.
  - `test_ac.py` checks the encode/decode round trip at all total lengths ≤ 31. The rebuilt engine reproduces the directed cap-25 count (1,836,928) and the undirected cap-26 count (6,373,628) exactly.

**Observation, local only: one-way edges near the sources.** Computed with scratch scripts that are not kept in the repo.
- Take the undirected closure of {AK(3), P1, P2} below energy 20. Each of its 588 one-way junction edges S → T has a reverse T → S that is a single product step r_i ← cyclic_reduce(rot(r_i^{±1})·rot(r_j^{±1})) *without* the junction condition. So, near the sources, the directedness comes from the junction condition alone.
- This is **not** true in general.
  - Among all states of energy ≤ 12 with both relators nonempty, 41,284 of the 127,167 one-way junction edges have no single-product-step reverse.
  - The smallest example is (x⁻¹, x⁻¹y⁻¹xy) → (x⁻¹, x⁻¹). The reverse needs a conjugation before any product.
- So this observation explains nothing beyond the states it was checked on, and it is not used anywhere above.

## Blocked / failed routes

- **Černý conjecture (rank 319) as a target.** The cubic-coefficient claim (Hexagon preprint 2611.00172v1, reset threshold ≤ (8242/49923)n³ + O(n²)) is hosted only on hexagonmath.org. That host is refused by the proxy (CONNECT 403; WebFetch ENOTFOUND). The ID 2611.00172 on arXiv is an unrelated paper.
- **Erdős matching (rank 375).** The k = 4 claim is also a Hexagon preprint (2610.00607v1, blocked). arXiv:2610.16203 (fixed k, large s) is an analytic proof via a tail-probability inequality, with no computer-assisted part to replay.
- **Hadamard order 668 (rank 284)** and **Turán K₄^(3) (rank 359)** have no recent claim recorded by ProofAtlas.
- **GitHub API for shehper/AC-Solver.** Not enabled for this session. The data files were read through raw.githubusercontent.com instead.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| P1 ~AC MS(2, yx²y⁻¹x⁻²) (Carreras Thm 1), for P1 both in Johnson's form and as MS(2, x⁻²y⁻¹x²y) | **Lean-verified** (kernel-checked by `decide +kernel`; trust: Lean 4.34.1 kernel and our definitions of AC moves in `AC/Defs.lean`); also certificate-checked by `ac_check.py` | `lean/AC/Audit.lean` (`carreras_thm1`, `carreras_thm1_MS`); `ac_check.py --theorems certs` |
| MS(2, yx²yx⁻²) ~AC MS(2, x⁻²y⁻¹x²y⁻¹) (Thm 2) | **Lean-verified** (as above) | `carreras_thm2` |
| MS(3, yx²y) ~AC AK(3) (Thm 3) | **Lean-verified** for all 3 certificates (2 by the author, 1 found by our own search) | `carreras_thm3`, `thm3b`, `ours_thm3` |
| MS(3, y⁻¹x²y⁻¹) ~AC AK(3) (Thm 4) | **Lean-verified** for both certificates (the author's, and 1 found by our own search) | `carreras_thm4`, `ours_thm4` |
| P3 and P4 are the benchmark's MS(3, x⁻¹y⁻¹xy⁻¹) and MS(3, yxyx⁻¹) up to rotation and inversion | checked (exact word comparison against AC-Solver's released data) | `test_ac.py` |
| AK(2) is AC-trivial (known) | **Lean-verified** (certificate from our search) | `ak2_trivial`; `certs_ours/ak2_trivial.json` |
| d_GS(P3, AK(3)) = d_GS(P4, AK(3)) = 19 (Thm 6, first part), in the directed reading (both directions) and in the undirected reading | computed (exhaustive below cap 19, directed and undirected; paths of bottleneck 19 found and certificate-checked; relative to the graph) | `reproduce.sh`; `test_ac.py` |
| Exact predecessor enumeration in the GS graph (shapes I–III, §5) | checked exhaustively: equals the inverted forward map on all states of energy ≤ 12; forward and predecessor edge sets identical (80,172 edges) on the undirected closure below 20 | `ac_graph.py`; `test_ac.py` |
| **New:** no undirected GS path below energy 27 between two of AK(3), P1, P2 (cap 27: 13,873,120 states, 10,340,996 / 877,892 / 2,654,232; cap 26: 6,373,628). Theorem 6's lower bounds d_GS ≥ 27 therefore hold in the undirected reading too, which closes the possible gap | computed (exhaustive; one implementation; relative to the graph) | `ac_search_par.cpp --undirected`; `AC_HEAVY=1 reproduce.sh` |
| **New:** no undirected GS path below energy 30 between two of AK(3), P1, P2. The undirected components below 30 of P1 (18,141,004 states) and P2 (50,655,984 states) contain no other source. So d_GS ≥ 30 in the undirected reading too, the same level as the directed cap-30 run | computed (exhaustive; single-source components, validated against the multi-source run at cap 27; one implementation; relative to the graph) | `ac_search_par.cpp --undirected ... --passive`; `AC_HEAVY=1 reproduce.sh` |
| Sublevel counts at exclusive cap 25: 1,532,732 / 135,892 / 168,304, no meeting | computed; reproduces the paper's numbers exactly | `reproduce.sh` |
| Sublevel count at exclusive cap 26: 6,212,968 (5,431,780 / 356,836 / 424,352), no meeting: no state of energy < 26 forward-reachable from two sources (the paper's criterion; implies directed d_GS ≥ 26 for each pair) | computed; reproduces the paper's numbers exactly | `AC_HEAVY=1 reproduce.sh` |
| Sublevel count at exclusive cap 27: 13,504,944 (10,118,636 / 851,836 / 2,534,472), no meeting: no state of energy < 27 forward-reachable from two sources (Thm 6's criterion; implies directed d_GS ≥ 27; the undirected reading of Thm 6 is not established, a possible gap in the paper) | computed (exhaustive, our implementation; relative to the graph); reproduces the paper's numbers exactly | same |
| **New:** sublevel count at exclusive cap 28: 47,544,780 (36,700,896 / 2,323,596 / 8,520,288), no meeting: no state of energy < 28 forward-reachable from two sources (implies directed d_GS ≥ 28) | computed (exhaustive; two implementations agree exactly; relative to the graph) | `ac_search_compact.cpp`, `ac_search_par.cpp` |
| **New:** sublevel count at exclusive cap 29: 88,628,824 (68,481,208 / 5,374,816 / 14,772,800), no meeting: no state of energy < 29 forward-reachable from two sources (implies directed d_GS ≥ 29) | computed (exhaustive; two implementations agree exactly; relative to the graph) | same |
| **New:** sublevel count at exclusive cap 30: 351,388,696 (284,176,652 / 17,796,820 / 49,415,224), no meeting: no state of energy < 30 forward-reachable from two of AK(3), P1, P2 (implies directed d_GS ≥ 30 for each pair, both directions; undirected: see the undirected row) | computed (exhaustive; one implementation, a second implementation of the compact engine's graph with different data structures, matching it exactly at caps 25–29; relative to the graph) | `ac_search_par.cpp`; `AC_HEAVY=1 reproduce.sh` |
| AK(3) AC-trivial? Andrews–Curtis conjecture | open | — |

## Next steps

- **Undirected cap 31** (in progress, via single-source P1/P2 components, §5): extend "no undirected GS path below 30". P1 is about 70M states; P2 may be about 200M states and more than 1 h. A meeting would come with a path from `ac_search_compact --undirected` (parents kept), which `ac_path.py` expands and `gen_lean.py --extra` Lean-verifies.
- **Next concrete step:** a bounded attack on the open edges, P1 or P2 → AK(3), the two remaining uncertified claims of Shehper et al.
  - Cap 30 is done (no meeting, §3).
  - Cap 31 with `ac_search_par`: growth from cap 29 to cap 30 was ×3.96 in states, so cap 31 might need about 1.4 billion states, about 12 GB of table at 8 B per slot and 90% load, and several hours. It is out of reach on this machine. (It also needed the key fix of §5. The single-source runs of §5 avoid the AK(3) component, and they work for the directed search too, with `--passive`.)
  - A meeting would need parent recovery: rerun `ac_search_compact --passive` from each side toward the meeting state. Then `ac_path.py` expands the path, and `gen_lean.py --extra` Lean-verifies it.
  - Alternatively, try the non-junction edges, which our search supports and the paper's graph excludes.
- Done: the Lean port (§4).
- Done (§5): the undirected-graph version of the Theorem 6 bounds, at ≥ 30.
