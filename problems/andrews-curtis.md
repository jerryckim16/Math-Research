# Andrews–Curtis conjecture (rank-2, length-14 frontier)

**Area:** combinatorial group theory / low-dimensional topology
**Status:** in progress. We are checking an unrefereed, computer-assisted claim independently: J. Carreras, arXiv:2607.23611v1 (July 2026). Done so far:
- Theorems 1–4 (four AC-equivalences among the six hard length-14 Miller–Schupp presentations and AK(3)) are **certificate-checked**. Our own checker replays the author's move certificates.
- Our own search **re-finds** Theorems 3–4 independently, and our checker accepts the resulting certificates.
- **Theorem 6** (computer-assisted) is re-derived with our own implementation:
  - the exact bottleneck 19;
  - all exhaustive state counts at energy caps 25, 26 and 27, matching the paper exactly, including the 13,504,944 states behind the "≥ 27" lower bounds.
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

  The claims:
  - d_GS(MS(3, yx²y), AK(3)) = 19.
  - d_GS(P1, AK(3)), d_GS(P2, AK(3)) and d_GS(P1, P2) are all ≥ 27.
  - Exclusive cap 25: 1,532,732 / 135,892 / 168,304 states are settled from AK(3) / P1 / P2.
  - Exclusive cap 26: 6,212,968 states, with no meeting.
  - Exclusive cap 27: 13,504,944 states, with no meeting.
  - The author stresses that these are statements about this graph only, not about AC distance.

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
- The four Two-Hump trivialization certificates in the artifact (`cert_u066`, `cert_twohump_u066`, `cert_u102`, `cert_twohump_u102`) also replay to ⟨x, y | x, y⟩ under our checker. This was a side check; it is not a claim of the paper's theorems.

### 2. Are P3 and P4 the presentations Shehper et al. meant? (checked; one pitfall)

- Shehper et al. (v2, p. 11, checked on the rendered page) print the MS(3) cases as ⟨x, y | x⁻¹y³x = y⁴, x = y^{±1}x²y^{±1}⟩. Carreras takes P3, P4 from that text.
- **Pitfall.** Here w = y^{±1}x²y^{±1} has x-exponent sum 2, so taken literally it is not a Miller–Schupp word.
  - The released benchmark data has every w with x-exponent sum 0 (1,190/1,190 entries). That data is `ac_solver/search/miller_schupp/data/*.txt` at github.com/shehper/AC-Solver `main`, fetched via raw.githubusercontent.com. Its `all_presentations.txt` is byte-identical to the copy in Carreras' artifact.
  - Its six unsolved length-14 entries (all presentations minus greedy-solved; 1,190 − 533 = 657 unsolved) are the four MS(2) cases above, plus MS(3, yxyx⁻¹) and MS(3, x⁻¹y⁻¹xy⁻¹).
  - We first read this as a mismatch. **It is not one.** x⁻¹y⁻¹x²y⁻¹ is the inverse of a rotation of x⁻¹yxyx⁻¹: both say x² = yxy. Likewise x⁻¹yx²y matches x⁻¹y⁻¹xy⁻¹ (both say x² = y⁻¹xy⁻¹).
  - So P4 ≡ MS(3, yxyx⁻¹) and P3 ≡ MS(3, x⁻¹y⁻¹xy⁻¹) up to rotation and inversion, with the ± signs crossed. This is checked in `test_named_presentations`.
- **Conclusion.** Theorems 3–4 do concern the two MS(3) presentations of the released benchmark. The "first public certificates" wording is the author's; we did not audit novelty.

### 3. Our own search: rediscovery and Theorem 6 (worked so far)

- **Search.** `ac_search.cpp` was written here.
  - It does a multi-source minimax search over pairs of cyclically reduced words, taken up to swap, inversion and rotation.
  - Edges: r_i ← cyclic_reduce(rot(r_i)·rot(r_j)^{±1}). With `--junction`, only products whose junction cancels are used. This is our reading of the GS-substitution graph.
  - States are settled in nondecreasing bottleneck. A state of total length ≥ cap is never entered.
- **Path expansion.** `ac_path.py` turns a path of canonical states into elementary moves: rotations, a possible inversion, one mul, conjugations to cyclically reduce, and a final orbit bridge. `ac_check` then checks the result. So nothing in the search has to be trusted for positive claims.
- **Pipeline check.** AK(2) → ⟨x, y | x, y⟩ found at bottleneck 13; the 34-move certificate passes. AK(3) and the trivial presentation do not meet below total length 14, consistent with Havas–Ramsay.
- **Rediscovery of Theorems 3–4.**
  - P3 → AK(3) and P4 → AK(3) are each found in under 1 s.
  - They expand to certificates of 149 and 45 elementary moves (peak total 29 and 33). `ac_check` accepts both, and they are saved in `certs_ours/`.
  - These are certificates generated by us and independent of the author's.
- **Bottleneck 19 (Theorem 6).** In our graph:
  - cap 19 is exhausted with no meeting, for both P3–AK(3) and P4–AK(3);
  - cap 20 meets.
  - So the minimax energy is exactly **19** for both pairs. The paper states 19 for P3.
- **Cap-25 counts (Theorem 6).** Sources {AK(3)}, {P1}, {P2}, exclusive cap 25: 1,836,928 states settled, **1,532,732 / 135,892 / 168,304** per source, no meeting. This took 83 s and about 0.4 GB.
  - These are *exactly* the paper's numbers.
  - The match is good evidence that our graph is the same as the paper's GS graph. Equal counts from two independent implementations are evidence, not a proof that the graphs coincide.
- **Cap 26 (Theorem 6).** Same three sources, exclusive cap 26: **6,212,968** states settled, no meeting. This took 5 min 26 s on one core.
  - Per source: 5,431,780 (AK(3)), **356,836** (P1), **424,352** (P2).
  - The total matches the paper's 6,212,968. The P1 and P2 numbers match the paper's "energy ≤ 25" figures in §5 exactly.
  - So every path in this graph joining any two of AK(3), P1, P2 has bottleneck ≥ 26.
- **Cap 27 (Theorem 6).** Exclusive cap 27: **13,504,944** states settled, no meeting. This took 834 s wall on one core at 3.01 GB peak RSS.
  - Per source: 10,118,636 (AK(3)), **851,836** (P1), **2,534,472** (P2).
  - The total and the P1/P2 counts all equal the paper's numbers.
  - So d_GS(P1, AK(3)), d_GS(P2, AK(3)) and d_GS(P1, P2) are all **≥ 27**, which is the lower-bound half of Theorem 6, re-derived here.
  - The paper's cap-28 run hit its 40M-state budget and was inconclusive.
- **Cap 28 (beyond the paper; running).**
  - `ac_search_compact.cpp` explores the same graph using about 30 B per state instead of about 220 B: packed 2-bit words, an append-only state array, and an open-addressing index.
  - Its per-level and per-source counts equal those of `ac_search.cpp`: cap 25 in full, cap 21 in `test_ac.py`.
  - Run: exclusive cap 28 from {AK(3)}, {P1}, {P2}, budget 95M states (about 2.9 GB).
  - Possible outcomes:
    - a meeting at bottleneck 27, which would give a new explicit certificate for one of Shehper et al.'s uncertified claims;
    - exhaustion with no meeting, which would give d_GS ≥ 28;
    - budget exhausted, which would be inconclusive, as in the paper.
- **The full graph** (all rotations, not only cancelling junctions) is barely larger but about 20× slower in our implementation.
  - Cap 21: 41,306 states against 40,078 with `--junction`. Cap 23: 285,760 against 274,430. No meeting in either.
  - It was not pushed further.
- **Scope.** As the author says, Theorem 6 is a statement about this graph. It is not an AC-distance bound and not evidence of AC-inequivalence.

## Blocked / failed routes

- **Černý conjecture (rank 319) as a target.** The cubic-coefficient claim (Hexagon preprint 2611.00172v1, reset threshold ≤ (8242/49923)n³ + O(n²)) is hosted only on hexagonmath.org. That host is refused by the proxy (CONNECT 403; WebFetch ENOTFOUND). The ID 2611.00172 on arXiv is an unrelated paper.
- **Erdős matching (rank 375).** The k = 4 claim is also a Hexagon preprint (2610.00607v1, blocked). arXiv:2610.16203 (fixed k, large s) is an analytic proof via a tail-probability inequality, with no computer-assisted part to replay.
- **Hadamard order 668 (rank 284)** and **Turán K₄^(3) (rank 359)** have no recent claim recorded by ProofAtlas.
- **GitHub API for shehper/AC-Solver.** Not enabled for this session. The data files were read through raw.githubusercontent.com instead.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| P1 ~AC MS(2, yx²y⁻¹x⁻²) (Carreras Thm 1) | certificate-checked (author's certificate, our independent checker; explicit chain from the defined presentations) | `ac_check.py --theorems certs` |
| MS(2, yx²yx⁻²) ~AC MS(2, x⁻²y⁻¹x²y⁻¹) (Thm 2) | certificate-checked (as above) | same |
| MS(3, yx²y) ~AC AK(3) (Thm 3) | certificate-checked: 2 author certificates, plus 1 certificate found by our own search | same; `certs_ours/ms3_yx2y_to_ak3.json` |
| MS(3, y⁻¹x²y⁻¹) ~AC AK(3) (Thm 4) | certificate-checked: author's certificate, plus 1 found by our own search | same; `certs_ours/ms3_yinvx2yinv_to_ak3.json` |
| P3 and P4 are the benchmark's MS(3, x⁻¹y⁻¹xy⁻¹) and MS(3, yxyx⁻¹) up to rotation and inversion | checked (exact word comparison against AC-Solver's released data) | `test_ac.py` |
| AK(2) is AC-trivial (known) | certificate-checked (our search and our checker) | `certs_ours/ak2_trivial.json` |
| d_GS(P3, AK(3)) = d_GS(P4, AK(3)) = 19 (Thm 6, first part) | computed (exhaustive below cap 19, our implementation; relative to the graph) | `reproduce.sh` |
| Sublevel counts at exclusive cap 25: 1,532,732 / 135,892 / 168,304, no meeting | computed; reproduces the paper's numbers exactly | `reproduce.sh` |
| Sublevel count at exclusive cap 26: 6,212,968 (5,431,780 / 356,836 / 424,352), no meeting, so d_GS(P1, AK(3)), d_GS(P2, AK(3)), d_GS(P1, P2) ≥ 26 | computed; reproduces the paper's numbers exactly | `AC_HEAVY=1 reproduce.sh` |
| Sublevel count at exclusive cap 27: 13,504,944 (10,118,636 / 851,836 / 2,534,472), no meeting, so d_GS(P1, AK(3)), d_GS(P2, AK(3)), d_GS(P1, P2) ≥ 27 (Thm 6) | computed (exhaustive, our implementation; relative to the graph); reproduces the paper's numbers exactly | same |
| AK(3) AC-trivial? Andrews–Curtis conjecture | open | — |

## Next steps

- **Next concrete step:** a bounded attack on the open edges, P1 or P2 → AK(3), the two remaining uncertified claims of Shehper et al.
  - Push our minimax search to cap 28–29 within a memory budget.
  - Alternatively, try the non-junction edges, which our search supports and the paper's graph excludes.
- Formal check: port `ac_check` to Lean (word reduction plus move replay by `decide`) to turn the certificate checks into Lean-verified statements.
