# Kissing numbers: 2026 lower bounds in dimensions 25, 27 and 32–39

**Area:** discrete geometry / spherical codes
**Status:** in progress. We are checking two recent, unrefereed, computer-assisted lower-bound claims independently, by an exact pairwise check of every point pair:
- S. Yang et al. ("Qiushi Engine", an autonomous multi-agent AI system), arXiv:2609.35051v1 (28 Sep 2026): new bounds in 19 dimensions. Scope here: dims 32–39 and 43 (all done), from the authors' complete integer exports. Their own release notes say the exports were **not** checked pair by pair. Also dims 25 and 27 (done), which have no complete export: we rebuilt them from the repository data with our own code.
- Q. Lin, arXiv:2611.03682v1 (22 Oct 2026): larger bounds in dims 32–35 and 37–39. Scope here: all seven configurations, rebuilt from his certificate files with our own builder and checked pair by pair (all seven done).

Results so far: see §Results. No violation was found in any of the 18 configurations checked (Qiushi 25, 27, 32–39 and 43; Lin 32–35 and 37–39). The exact kissing numbers in these dimensions remain open; these are lower bounds only.

**Started:** 2026-11-24
**ProofAtlas:** rank 98, "Exact Kissing Numbers in Higher Dimensions", `open_with_solved_subcases` (Top-500 edition 2026-11-12). Its status note (reviewed 12 Nov 2026) cites only Salmon's arXiv:2610.21263 (asymptotics of the Delsarte bound) and the open 40 ≤ τ₅ ≤ 44 gap, and says: "no local proof audit, certificate replay, Lean execution or refereeing confirmation." Its only kissing workspace, "Five-dimensional kissing number" (status checked 26 Aug 2026), cites Cohn–Rajagopal (2026) and Szöllősi (2023). Neither page mentions arXiv:2609.35051 or arXiv:2611.03682, so ProofAtlas has not checked either claim.

## Why this problem (choice made 2026-11-24)

Candidates from `notes/ai-feasible-open-problems.md` that were surveyed:
- **Kissing numbers (rank 98) — chosen.** arXiv lists at least six 2026 lower-bound papers (dims 19, 25–31, 25–55, 32–39, 49–61). Two of them publish complete data we can fetch: Qiushi's full integer exports (GitHub release assets) and Lin's certificates (Zenodo). A kissing configuration is a finite certificate, and with integer coordinates the check is exact integer arithmetic. The claims are recent (Sep–Oct 2026) and unrefereed. Qiushi's claim comes from an AI system, and its authors say the exports were not checked pair by pair. ProofAtlas has not checked either claim (above).
- Hadamard 668 (rank 284): arXiv:2610.27175v2 (Egan–Kotsireas–London–Ó Catháin, Oct 2026) reports that Alpöge, Voinov and Reynolds-Haertle announced Hadamard matrices at all twelve open orders below 2000 in Aug 2026, and that the survey verifies them. So the shortlist target "order 668" is out of date. The ProofAtlas Hadamard workspace (checked 14 Aug 2026) does not record this. Not pursued here.
- Turán K₄⁽³⁾ (rank 359): arXiv:2609.27495v2 (Jeong–Park–Im–Lee–Yang, Sep 2026) claims π(K₄⁽³⁾) ≤ 0.557789 with a Lean 4 proof. A possible later target (replay the Lean proof). No ProofAtlas workspace.
- H10 fewest unknowns (rank 347): no ProofAtlas workspace and no recent claim found in this pass.
- Thomson (rank 340): the ProofAtlas workspace is a proof programme for N = 7. There is no external computer-assisted claim with data to check.

## Statement

The kissing number τ_n is the largest number of non-overlapping unit balls in ℝⁿ that touch a central unit ball. Equivalently, it is the largest N for which there are nonzero vectors x₁,…,x_N ∈ ℝⁿ with pairwise angles ≥ 60°, i.e. ⟨x_i,x_j⟩ ≤ ½|x_i||x_j| for i ≠ j.

**Exact criterion used here.** For integer vectors a, b, put p = a·b, A = |a|², B = |b|². The angle is ≥ 60° iff

  p ≤ 0 or 4p² ≤ AB,

which for integer p means p ≤ T(A,B) := isqrt(⌊AB/4⌋). A repeated point (or a positive multiple) has 4p² = 4AB > AB, so passing the check also certifies that the N directions are distinct. A configuration of integer rows that passes the check for every pair, and whose rows lie in an n-dimensional subspace, proves τ_n ≥ N.

## The claims being checked

**Source 1: Qiushi Engine.** S. Yang, R. Zhao, J. Wu, et al. (16 authors), *Large-Scale Autonomous Discovery of Kissing Number Constructions*, arXiv:2609.35051v1 (28 Sep 2026), unrefereed. Data: GitHub `Oxelra-AI/Qiushi-Engine-Kissing-Number-Research` (HEAD 39911e4b38c01c4631e06b12a3e0b23a84e403f8, 2026-10-24), release `configuration-vectors-2026-10-12`. Its `constructions/VECTORS.md` and the release JSON (`"full_pairwise_inner_products_checked": false`) say the exports were checked for "exact source membership, norms, uniqueness and complete layer counts", **not pair by pair**.

Claims checked (`research/results.md` of the repository; abstract of the paper):

| n | claimed τ_n ≥ | export file (sha256 of the .gz) | rows × columns |
|---:|---:|---|---|
| 32 | 347,584 | `configuration32.i8.gz` f30dfb6f…4616f7 | 347,584 × 32, int8 |
| 33 | 363,968 | `configuration33.i8.gz` 40a6ce91…7dc0 | 363,968 × 33 |
| 34 | 384,196 | `configuration34.i8.gz` e3e8500d…8ecd | 384,196 × 34 |
| 35 | 409,676 | `configuration35.i8.gz` 8dc1a68c…dc12 | 409,676 × 35 |
| 36 | 484,760 | `configuration36.i8.gz` 7f15909a…065d | 484,760 × 36 |
| 37 | 498,024 | `configuration37.i8.gz` 97cd948a…3d25 | 498,024 × 37 |
| 38 | 591,900 | `configuration38.i64.gz` 0117193c…3eca | 591,900 × 52, int64, rank 38 |
| 39 | 763,668 | `configuration39.i8.gz` 02591a7a…b60e | 763,668 × 39 |

Full hashes are pinned in `computations/kissing/fetch_qiushi.py`. They equal the sha256 values in the authors' release JSON (the 38D JSON lists none). The 38D export embeds ℝ³⁸ = ℝ²⁴ ⊕ ℝ¹⁴ isometrically into ℝ⁵² as (x, y/√2, y/√2), which keeps the 1932 "rotated axis" rows integral at the cost of entries up to 3.7·10¹⁷.

**Dims 25 and 27** (checked here, §Approaches 2). They have no complete export, so the configurations are defined by repository data plus the paper's construction text. We fetch the six data files from the repository at commit 39911e4b and pin them by sha256 in `fetch_qiushi.py --with-25-27`. These hashes equal those in the authors' `constructions/d25/verification.json` and `constructions/d27/verification.json`. The files are `d25/baseline-heads.json` (b6b1dff1…15d6), `d25/repair-points.json` (daeabf4a…3677) and `d27/data/heads27_{Y,side,layer2_u,layer2_line}.npy` (e137a6e3…4bd1, b0e1457e…9fb2, 7d7a4bcd…ca2, f7b01851…7fb95). The previous records, taken from the paper's own Table 1 and **not re-derived here**, are 197,579 for d = 25 (credited there to A. Kravatskiy's KissingNumbers repository, revision cf14c5e) and 201,566 for d = 27 (credited to B. Lindow, KissingNumbers pull request no. 1, revision 277c2970). Each claim is +1.

| n | claimed τ_n ≥ | previous (paper's Table 1) | construction (paper §motion, §"two-layer configuration") |
|---:|---:|---:|---|
| 25 | 197,580 | 197,579 | 197579 − 552 − 2 + 552 + 2 + 1: move the 552 retained shell points w with w·g = 24 to (r + a n, b), add Q = (√3 n, −1), replace two caps by 2k/√1007176 and 2ℓ/√10209 |
| 27 | 201,567 | 201,566 | 196560 − 2090 − 311 + 3·2258 + 2·311 + 12: first-layer caps (y/3, 4v/√3), second-layer caps (√3u/2, ±√8 e_ℓ), 12 pure tails (0, 4Rv) |

Not checked here: dim 45 (a 7.4M-point export exists; see Next steps). The 43D export (release `section-vectors-2026-10-11`, 2,553,792 × 48 int8, raw sha256 101491f3…bf4bd, which equals the authors' `section43-verification.json`, also marked `pairwise_inner_products_checked: false`) is checked here too and 49–55 (≈5.2·10⁷ points each; brute force is out of reach).

**Source 2: Lin.** Q. Lin, *New lower bounds for kissing numbers in dimensions 32–35 and 37–39*, arXiv:2611.03682v1 (22 Oct 2026), unrefereed. Data: Zenodo 10.5281/zenodo.23552484 (dim 32, v1.1.0, archive sha256 683fc500…ab659) and 10.5281/zenodo.23554809 (dims 33–39, v1.0.0, archive sha256 1a1368fe…f21f5). The per-file sha256s are pinned in `computations/kissing/fetch_lin.py`. Construction: Edel–Rains–Sloane three layers (dense code layer, ±2 on weight-8 supports, ±4e_i ± 4e_j) with new constant-weight codes A(n,8,8). In dim 38 it is Kravatskiy's 591,612-point configuration plus 6,855 antipodal pairs of norm-48 Leech vectors on the empty equator.

| n | claimed τ_n ≥ | construction |
|---:|---:|---|
| 32 | 352,320 | 131072 + 128·1713 + 1984 |
| 33 | 370,240 | 131072 + 128·1852 + 2112 |
| 34 | 390,980 | 131072 + 128·2013 + 2244 |
| 35 | 415,308 | 131072 + 128·2202 + 2380 |
| 37 | 499,816 | 131072 + 128·2860 + 2664 |
| 38 | 605,322 | 591612 + 2·6855 |
| 39 | 768,916 | 327680 + 128·3424 + 2964 |

Lin also lists Qiushi's 32, 35, 37, 38, 39 values as the previous records. For 33 and 34 he names larger previous values (364,736 and 384,836, credited to "Pliny the Liberator" codes), which supersede Qiushi's 33 and 34 values. We could not open Cohn's table (cohn.mit.edu is blocked here) to confirm the current records.

## Known results

- τ₁…τ₄ = 2, 6, 12, 24 (τ₄: Musin, Ann. Math. 2008); τ₈ = 240, τ₂₄ = 196560 (Odlyzko–Sloane 1979; Levenshtein 1979). All other n are open.
- Edel–Rains–Sloane, *On kissing numbers in dimensions 32 to 128*, Electron. J. Combin. 5 (1998) R22: the three-layer construction both sources use in dims 32–37 and 39.
- Lower bounds in dims 25–31 were also improved in 2026 (Takhanov–Yun, arXiv:2609.21591v2), and dims 49–61 too (Kamenetsky, arXiv:2611.01906v1, data on GitHub). Neither is checked here.

## Approaches

### 1. Exact pairwise check of complete configurations (worked)

- **Idea:** check the criterion above for every pair, in exact integer arithmetic, with two independent implementations. Validate on known configurations and on deliberately broken ones first.
- **Implementation** (`computations/kissing/`):
  - `kiss_check.c` (C, OpenMP). Rows are int8; dot products are accumulated in int16. This is exact because every squared norm is ≤ 32767: by Cauchy–Schwarz, each partial sum is at most Σ|a_k b_k| ≤ |a||b| ≤ max(A,B). The program checks this precondition. It reports violations, the maximum excess p − T, the number of exact 60° contacts, and the largest p per pair of norm classes.
  - `kiss_check_np.py` (numpy, float32 GEMM). It is exact because every partial sum is an integer of absolute value < 2²⁴ (same Cauchy–Schwarz bound), and any flagged pair is recomputed in int64.
  - `check_mixed.py` handles the 38D int64 exports. Pairs of small rows go to `kiss_check.c` (written out as int8). Huge-row × small-row pairs are computed exactly by splitting each entry as hi·2³¹ + lo in int64, then recombining in Python integers wherever a float64 screen (margin 10⁻⁶ in cosine) cannot decide. Huge × huge pairs use exact Python-integer dot products. It also checks the dimension: columns 38–51 equal columns 24–37 in every row, so the rows span ≤ 38 dimensions, and the rank modulo 2⁶¹−1 of a 3,205-row sample is 38.
  - `build_lin.py` rebuilds Lin's configurations from his certificate files with our own parser. It assumes nothing about their validity and only checks the claimed counts.
    For 38D the base (Kravatskiy's 591,612 points) is taken from the Qiushi export, not rebuilt from the base data Lin ships. The check of the assembled set is unconditional: it proves τ₃₈ ≥ 605,322. That this set is exactly Lin's construction rests on two things. First, Lin's seven `certificates/d38/base-data/` files are byte-identical (sha256) to `constructions/d38/base-data/` in the Qiushi repository; we checked this. Second, the Qiushi export is built from that data; we did not re-derive it.
- **Validation:**
  - D₄ (24, 96 contacts), D₅ (40, 240 contacts), E₈ (240, 6720 = 240·56/2 contacts) and the Leech minimal vectors (196,560, 452,088,000 = 196560·4600/2 contacts; built from our own Golay code, whose weight enumerator is checked) all pass in both implementations, with exactly the classical contact numbers.
  - Negative controls fail: an added short vector, one perturbed coordinate in E₈, a duplicated row, and a scaled copy of a row.
  - On 50 random integer sets with mixed norms (40 failing, 10 passing), C, numpy and a pure-Python big-integer reference agree exactly on violation and contact counts.
  - check_mixed: E₈ with five rows rescaled by 10¹⁵+37 passes, and adding a rescaled copy of an existing row fails.
  - On real data, Qiushi's 32D file with row 0 duplicated, or replaced by the sum of itself and a 60° neighbour, must fail (`perturb.py`).
- **Outcome:** see §Results.

### 2. Qiushi 25D and 27D: rebuild from repository data, exact check over Q(√2, √3) (worked)

- **Rebuild** (`build_qiushi2527.py`, our own code). It follows the paper's construction text and reads only the six pinned data files; none of the authors' code is run. The Leech shell is our own (`known.py`, the same Golay generator polynomial as the authors'; a coordinate-convention mismatch would show up as owners missing from the shell). The builder re-derives and asserts the structural facts the counts depend on.
  - 25D: all 1,016 head owners lie in our shell and are distinct. The layer {w : w·g = 24} has exactly 552 points, and it equals {u + g : u·g = −24}, whose members u are all owners.
  - 27D: each first-layer head has at most one shell vector with y·z > 48, giving 2,090 distinct owners. The 311 second-layer owners lie in the shell and are disjoint from the 2,090.
  - The point counts come out as 197,580 and 201,567, equal to the claims.
- **Coordinates are not integral.** 25D needs √2, √3, √6 (the moved block and Q's plane) and 44 rational heads with denominators up to about 3.5·10¹⁸. 27D needs √2 and √3. Each point is therefore stored, up to a positive factor (which does not change angles), as x = C₀ + C₁√2 + C₂√3 + C₃√6 with integer vectors C_k. The configuration splits into two parts:
  - a pure-integer "bulk" (int8, norm ≤ 32767): 25D has 194,992 unmoved shell rows plus P₀ ∝ (−g, 0), the poles, Q ∝ (g, −4) and R₋ ∝ ℓ, 194,997 rows in all; 27D has the 194,159 remaining shell rows;
  - "field" rows: 2,583 in 25D and 7,408 in 27D.
- **Checks.**
  - Bulk × bulk pairs go through the existing `kiss_check.c` and `kiss_check_np.py`.
  - Every pair involving a field row goes through the new `kiss_check_field.py`. It computes every squared norm exactly and requires it to be a positive integer. It has two independent decision modes:
    - *float*: a float64 cosine screen with margin 10⁻⁹, with a rigorous rounding bound below 10⁻¹¹ (conditioning checked per row). Undecided pairs get an exact sign of a + b√2 + c√3 + d√6 by repeated squaring in Python integers.
    - *interval*: exact integer P₀…P₃ via float64 GEMM on 24-bit limbs, exact because every partial sum is below 2⁵³ (checked). Then come integer interval bounds at scale 2¹², refinement up to 2¹⁰²⁴, and an exact equality test for contacts.
  - The checker asserts that it covered exactly n_T·n_S + C(n_T, 2) pairs, so bulk and field pairs together are all pairs.
- **Validation** (`test_kissing.py` §5).
  - E₈ with rows multiplied by √2, √3, √6 or 7·10¹⁸+1 passes with 6720 contacts in total.
  - The 12 rotated cuboctahedron tails of the 27D construction pass with 24 contacts.
  - Bad rows are caught.
  - Both modes agree with a pure-Python exact reference.

## Results

| Claim | Evidence level | Where |
|---|---|---|
| Pipeline: D₄, D₅, E₈, Leech pass with the classical contact counts; negative controls fail; three implementations agree on random sets | computed (exact) | `test_kissing.py`, `reproduce.sh` §1–2 |
| **Qiushi 32D: 347,584 points, τ₃₂ ≥ 347,584**: all 60,407,144,736 pairs satisfy the criterion; max inner product 16 = threshold at norm 32; 358,430,976 contacts | certificate-checked (exact, all pairs) | `kiss_check.c` on the pinned export |
| **Qiushi 33D: 363,968**: 0 violations, max 16/16, 368,310,912 contacts | certificate-checked | same |
| **Qiushi 34D: 384,196**: 0 violations, max 16/16, 380,481,792 contacts | certificate-checked | same |
| **Qiushi 35D: 409,676**: 0 violations, max 16/16, 315,579,800 contacts | certificate-checked | same |
| **Qiushi 36D: 484,760**: 0 violations, max 16/16, 404,388,832 contacts | certificate-checked | same |
| **Qiushi 37D: 498,024**: 0 violations, max 16/16, 392,397,168 contacts | certificate-checked | same |
| **Qiushi 38D: 591,900 points, τ₃₈ ≥ 591,900**. All 175,172,509,050 pairs pass: 174,030,825,528 pairs among the 589,968 norm-48 rows (max inner product 24 = threshold, 379,694,006 contacts), 1,139,818,176 axis × other pairs (max cosine 0.49184, no contacts) and 1,865,346 axis × axis pairs (159,264 contacts). The rows lie in a 38-dim subspace: the tail copy is exact (columns 38–51 = 24–37), and the rank mod 2⁶¹−1 of a 3,205-row sample is 38 | certificate-checked | `check_mixed.py` + `kiss_check.c` |
| **Qiushi 39D: 763,668 points, τ₃₉ ≥ 763,668**. All 291,594,025,278 pairs pass. Two norm classes (39: 327,680 rows; 32: 435,988 rows); max inner products 19/19 (39·39), 16/17 (39·32), 16/16 (32·32); 325,490,632 contacts | certificate-checked | `kiss_check.c` |
| **Lin 32D: 352,320 points, τ₃₂ ≥ 352,320** (rebuilt by `build_lin.py`). All 62,064,515,040 pairs pass, max 16/16, 366,910,976 contacts | certificate-checked | `kiss_check.c` |
| **Lin 33D: 370,240**. 68,538,643,680 pairs, 0 violations, max 16/16, 374,626,176 contacts | certificate-checked | same |
| **Lin 34D: 390,980**. 76,432,484,710 pairs, 0 violations, max 16/16, 383,763,968 contacts | certificate-checked | same |
| **Lin 35D: 415,308**. 86,240,159,778 pairs, 0 violations, max 16/16, 395,664,280 contacts | certificate-checked | same |
| **Lin 37D: 499,816**. 124,907,767,020 pairs, 0 violations, max 16/16, 398,495,856 contacts | certificate-checked | same |
| **Lin 38D: 605,322 points, τ₃₈ ≥ 605,322**: the first 591,612 rows of the Qiushi 38D export (Kravatskiy's base) plus ±6,855 equatorial vectors. All 183,207,059,181 pairs pass: 182,039,444,355 among the 603,390 norm-48 rows (max 24/24, 403,492,534 contacts), 1,165,749,480 axis × other pairs (max cosine 0.49184) and 1,865,346 axis × axis pairs (159,264 contacts). Rank 38 as above. Lin's 6,855 vectors are in the export's Leech frame: their inner products with all 196,560 cap heads lie in 8ℤ with absolute value ≤ 24 | certificate-checked | `check_mixed.py` + `kiss_check.c` |
| **Lin 39D: 768,916 points, τ₃₉ ≥ 768,916**. All 295,615,523,070 pairs pass. Norm classes 39 (327,680 rows) and 32 (441,236 rows); max inner products 19/19, 16/17, 16/16; 323,661,000 contacts | certificate-checked | `kiss_check.c` |
| **Qiushi 43D: 2,553,792 points, τ₄₃ ≥ 2,553,792**. All 3,260,925,512,736 pairs pass. Squared norm 576 throughout; max inner product 288 = threshold; 4,467,331,098 contacts. The rows (48 integer columns) span exactly 43 dimensions: the rank mod 2⁶¹−1 of a sample is 43, and 5 exact integer kernel vectors are orthogonal to every row | certificate-checked | `span_check.py` + `kiss_check.c` (3,971 s, 4 cores) |
| Second implementation: `kiss_check_np.py` (float32 GEMM, a different code path) agrees exactly with the C checker on two full files. Qiushi 32D: 0 violations, max 16/16, the same 358,430,976 contacts (134 s, 4 processes). Lin 32D: 0 violations, max 16/16, the same 366,910,976 contacts (278 s, 3 processes, run alongside the 43D job) | certificate-checked (second implementation) | `kiss_check_np.py` |
| **Qiushi 25D: 197,580 points, τ₂₅ ≥ 197,580** (rebuilt by `build_qiushi2527.py`). All 19,518,829,410 pairs pass. Bulk (194,997 integer rows): 19,011,817,506 pairs, 0 violations, 445,096,391 contacts, with `kiss_check.c` and `kiss_check_np.py` agreeing exactly. Field (2,583 rows in Q(√2,√3), including 86 rational caps with about 19-digit entries and R₊): 507,011,904 pairs, 0 violations, 978,414 exact contacts, identical in both modes of `kiss_check_field.py` | certificate-checked (exact, all pairs; built from pinned data by our own code) | `build_qiushi2527.py` + `kiss_check.c` / `kiss_check_np.py` + `kiss_check_field.py` |
| **Qiushi 27D: 201,567 points, τ₂₇ ≥ 201,567** (rebuilt). All 20,314,526,961 pairs pass. Bulk (194,159 shell rows): 18,848,761,561 pairs, 0 violations, 441,324,134 contacts (C and numpy agree). Field (6,774 first-layer caps, 622 second-layer caps, 12 pure tails): 1,465,765,400 pairs, 0 violations, 2,815,546 exact contacts, identical in both modes | certificate-checked (exact, all pairs) | same |
| Negative controls for 25D/27D, each rejected (float mode). `q25_extra`, adding (√3 n, +1), the mirror of Q: 553 violations. `q25_norepair`, keeping the two old caps instead of R₊ and R₋ (so the repair is needed): 9 violations. `q27_owner`, putting back the equatorial point of one second-layer owner: 2 violations. `q27_label`, moving owner 0 onto the line of owner 107 (u·u′ = 16): 8 violations | computed (exact) | `build_qiushi2527.py --variant` + `kiss_check_field.py` |
| Real-data negative controls: Qiushi 32D with row 0 replaced by a copy of row 1 is rejected (1 violation, pair (0,1), max inner product 32). With row 0 replaced by row 0 + row 1 (a 60° neighbour) it is rejected with 1,047 violations | computed (exact) | `perturb.py` + `kiss_check.c` |

Our pair counts match the counts in Lin's README: 6.85·10¹⁰, 7.64·10¹⁰, 8.62·10¹⁰, 1.25·10¹¹ and 2.96·10¹¹ for 33, 34, 35, 37 and 39D, and 1.83·10¹¹ for 38D.

Costs (wall time on 4 cores, `kiss_check.c`):
- Qiushi: 32D 64 s, 33D 89 s, 34D 99 s, 35D 91 s, 36D 145 s, 37D 132 s, 38D norm-48 rows 402 s, 39D 353 s.
- Lin: 32D 125 s, 33D 139 s, 34D 154 s, 35D 174 s, 37D 246 s, 38D norm-48 rows 426 s, 39D 680 s. Lin's dense layer has no zero coordinates, so our zero-skipping does not help.
- 38D huge-row pairs: 186 s and 191 s on one core (`check_mixed.py`).
- 25D/27D: build 13 s for both. Bulk `kiss_check.c` 26 s / 33 s, `kiss_check_np.py` 178 s (4 processes) / 86 s (2 processes). `kiss_check_field.py` float mode 14 s / 51 s, interval mode 206 s / 449 s (2 processes, run alongside other jobs).
- Peak RAM < 1 GB.

## Next steps

- Done 2026-11-24: Qiushi 25D and 27D rebuilt and checked (above). Our check is of the configuration as built from the pinned data and the paper's text. It does not confirm that the 197,579 and 201,566 inputs are the cited earlier records; we did not open the KissingNumbers repository.
- Optional cross-check: export the authors' numerical 25D array with their `export.py` in a sandbox, and compare it with ours up to row order and scaling. Not done, because it means running downloaded code.
- Qiushi 45D (7,380,090 points, 2.7·10¹³ pairs): about 9 h at the measured 43D rate (8.2·10⁸ pairs/s on 4 cores). That is feasible as a long background job, and using antipodality would halve it.
- Kamenetsky's dims 49–61 (arXiv:2611.01906v1) and Qiushi's 49–55: ≈5.2·10⁷ points each. An exact check needs the structure (the P₄₈p shell is a lattice shell, so only the lifted layers need pairwise work).
