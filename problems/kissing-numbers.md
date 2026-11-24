# Kissing numbers: 2026 lower bounds in dimensions 11, 12, 25–39 and 43

**Area:** discrete geometry / spherical codes
**Status:** in progress. We are checking recent, unrefereed, computer-assisted lower-bound claims independently, by an exact pairwise check of every point pair:
- S. Yang et al. ("Qiushi Engine", an autonomous multi-agent AI system), arXiv:2609.35051v1 (28 Sep 2026): new bounds in 19 dimensions. Scope here: dims 32–39 and 43 (all done), from the authors' complete integer exports. Their own release notes say the exports were **not** checked pair by pair. Also dims 25 and 27 (done), which have no complete export: we rebuilt them from the repository data with our own code.
- Q. Lin, arXiv:2611.03682v1 (22 Oct 2026): larger bounds in dims 32–35 and 37–39. Scope here: all seven configurations, rebuilt from his certificate files with our own builder and checked pair by pair (all seven done).
- Added 2026-11-24 (§Survey, §Approaches 3–4): A. Kravatskiy's public repository `alexlegeartis/KissingNumbers` (not a paper), whose published exact data give the largest values we found in dims 25–31 (seven configurations: five complete coordinate files, 25D rebuilt from an exact witness, 29D from a parent file plus a trade; all done); Bianchi et al., arXiv:2606.10402v2, τ₁₁ ≥ 604 (rebuilt from the paper's appendix, done); Takhanov–Assylbekov–Yun, arXiv:2606.18984v2, τ₁₂ ≥ 841 (the published decimal coordinates, read exactly, done).

Results so far: see §Results. No violation was found in any of the 27 configurations checked (Qiushi 25, 27, 32–39 and 43; Lin 32–35 and 37–39; Kravatskiy 25–31; 11D 604; 12D 841). The exact kissing numbers in these dimensions remain open; these are lower bounds only.

**What our checks do and do not show.** Each check shows that a configuration is a valid kissing configuration of the stated size, so the stated lower bound holds. It does not show that the bound is the current record. Many of the 2026 arXiv claims, including Qiushi's 25D, 27D and 43D values and all of Qiushi's and Lin's 32–39D values, are already exceeded according to a third-party copy of Cohn's table (§Survey; reported, not checked).

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

## Survey: the other 2026 lower-bound claims (done 2026-11-24)

**Search scope.** arXiv API queries `ti:kissing` and `abs:kissing`, sorted by date, read on 2026-11-24 (all entries from 2026), plus the references of the papers found. Every arXiv source below was read in its TeX source (`arxiv.org/e-print/<id>`). Repositories were inspected with `git clone --depth 1 --filter=blob:none` at the commits named; data files were fetched from `raw.githubusercontent.com` at those commits and pinned by sha256. The note "25–55" in `notes/ai-feasible-open-problems.md` is Qiushi's paper (its 19 dimensions lie in 25–55); "32–39" is Lin's.

Pair counts are N(N−1)/2. Our C checker runs at about 7–10·10⁸ pairs/s on 4 cores, so up to about 10¹² pairs fit in an hour here.

| Paper (arXiv, version, date) | Claims: n, τ_n ≥ (previous value, per the paper's own table) | Complete data published? (exact URL, version) | Full pairwise check here? | Status in the 17 Nov 2026 snapshot of Cohn's table (third-party copy, reported) |
|---|---|---|---|---|
| B. S. Ho, 2603.10425v3 (v1 11 Mar 2026; v3 23 Oct 2026, "revised following referee comments") | 19: 11,948 (Cohn–Li 11,692) | Yes. `github.com/boonsuan/kissing` @ 55225e51f8465c9c4ddd95ac037de3dc617bb0e0, `data/dimension19_11948.txt` (sha256 c2ea852b…7615; 684 + 9,984 integer rows and 1,280 rows ±√(8/19)). The author's own script checks all pairs exactly | Yes: 7.1·10⁷ pairs (seconds). Not run: lower priority (the author checks every pair exactly; superseded) | 19: 12,460 (reference [13] of the table, not identified here). Superseded |
| F. Bianchi, Y. Kwon, A. Pappu, J. Zou ("EinsteinArena"), 2606.10402v2 (v1 9 Jun; v2 26 Aug 2026) | 11: 604 (AlphaEvolve 593) | Construction written out in Appendix "Kissing number construction (n = 604)", except which 8 triples form each of the 3 layers. Coordinates on einsteinarena.com (proxy refuses the host); `github.com/vinid/einstein-arena` not inspected | Yes: 182,106 pairs. **Done** (§Approaches 4) | 11: 604. Current |
| S. Chung, W. Du, W. J. Wesley ("Station"), 2608.23691v2 (v2 14 Sep 2026) | 11: 604, three non-isometric configurations (Construction 1 = EinsteinArena's) | `dualverse-ai.github.io/station_data_v2` (proxy refuses the host); `github.com/dualverse-ai/station` @ f2603c817694145610b4a1057eeee7fb6f31d516 has notebooks and reports, not parsed here | Yes (604 points). Constructions 2 and 3 not checked | 11: 604. Current |
| R. Takhanov, Z. Assylbekov, S. Yun, 2606.18984v2 (v2 22 Jun 2026) | 12: 841 (840) | Yes. `github.com/k-nic/841_in_12D` @ eba37f0368f62828780d1f9d90315b367d2a612f, `gram841_coordinates.txt` (841 × 12 decimals, sha256 995264fe…76a9). Found numerically; the paper reports only a numerical maximum inner product 0.499999937751 | Yes: 353,220 pairs. **Done** (§Approaches 4) | 12: 841. Current |
| R. Takhanov, S. Yun, 2609.21591v2 (v2 23 Sep 2026) | 25: 197,058; 26: 198,552; 27: 200,046; 28: 204,522; 29: 209,497; 30: 220,442; 31: 238,354 (PackingStar: 197,056; 198,550; 200,044; 204,520; 209,496; 220,440; 238,350) | Only float64 coordinates. `github.com/k-nic/Leech_lifting` @ 12a06bc252f865ae7dcaf746c53774c4a827275b: one `.npy` per dimension, plus the rotations (Q, R, G) and saved optimiser runs. In 26–31 a block (or its extra coordinates) is rotated by a float matrix, which the paper takes to mean its orthogonal polar factor, so the exact points are not in the files. The 25D construction (lifting height ½, poles ±e₂₅) is exact in ℚ(√3). The authors certify the changed pair classes with interval bounds, not every pair | Pair counts are 1.9–2.8·10¹⁰ (25: 1.94·10¹⁰; 31: 2.84·10¹⁰), which fits. But an exact check of the float files cannot decide the contacts (about 10⁻¹⁶ rounding on the exact 1/2 contacts); it would need the structure (Next steps). Not run | All seven superseded: 25–31 are 197,586; 201,188; 209,884; 222,120; 231,814; 248,212; 251,420. Qiushi's 25 and 27 are also larger |
| I. Dorofeev, X. Sun, C. Wang, 2607.20359v4 (v4 29 Aug 2026) | Kissing numbers of packings: 40: 1,092,000; 41: 1,324,472; 42: 1,792,386; 45: 7,379,838 (previous 1,064,368; 1,170,384; 1,541,292; 6,702,080). Also computes the 1982 Conway–Sloane cross-sections, e.g. 47: 23,766,960 | Lattice bases in closed form; code at `github.com/wcgbg/sphere-packing` (not inspected). These are lattice shells, so a check means computing a lattice's minimal vectors, not checking pairs | 10⁶–10⁷ points: 6·10¹¹ (40D) to 2.7·10¹³ (45D) pairs. Not run | 40–46 superseded. 47: 23,766,960, equal to this paper's value (the table's reference [3], not identified here) |
| D. Kamenetsky, 2611.01906v1 (1 Nov 2026) | 49–61: 52,430,388 … 60,057,914 (Qiushi 52,430,156 … 53,301,140 in 49–55; Kravatskiy's repository 54,085,392 … 59,898,694 in 56–61) | Generators only. `github.com/dimkadimon/KissingNumbers` @ 191165545b39fdc3099e6e0a46b9b5743410dc1b (tag v7 = 2e3beef2): the class patch and the t automorphisms A_i of P₄₈p, with an exact structural verifier. No coordinate list | No: 5.2–6.0·10⁷ points, 1.4–1.8·10¹⁵ pairs (Next steps) | Cohn's table stops at 48. Kravatskiy's README lists larger values in all of 49–61 (e.g. 61: 120,324,786), reported, not checked |
| C. Ma et al. ("PackingStar"), 2511.13391v5 (first posted 17 Nov 2025; v5 22 Sep 2026) | 25–31 and others (the starting points of Takhanov–Yun) | Not inspected | — | Superseded in 25–31 |

**Third-party record table.** cohn.mit.edu is refused by the proxy here (CONNECT 403, re-tried 2026-11-24), so we could not read Cohn's table. The record values above come from a copy in A. Kravatskiy's repository `github.com/alexlegeartis/KissingNumbers`, commit 907f9b1f4c5f8bb4196ea03775f60cc260189789 (2026-11-23), file `common/cohn_20261117.json` (sha256 c895fba1…23d5). It records an HTTP fetch of `https://cohn.mit.edu/kissing-numbers/` on 2026-11-17 15:22 UTC (html sha256 1f54cedd…4ecb) and the table's lower bounds for dims 1–48. It says that the table credits that repository in dims 18 and 25–46. Its 32–39 values are 352,992; 370,408; 390,992; 415,334; 501,822; 505,638; 611,638; 769,852, and 43 is 2,919,803, so every Qiushi and Lin value we checked is exceeded there. **Reported, not checked.** The file belongs to an interested party (the holder of most of the listed records), the snapshot predates later updates, and we have not seen the table itself. The repository's README (same commit) lists still larger values in several dimensions (e.g. 26: 201,204; 28: 223,528; 30: 248,506; 31: 251,524).

## Known results

- τ₁…τ₄ = 2, 6, 12, 24 (τ₄: Musin, Ann. Math. 2008); τ₈ = 240, τ₂₄ = 196560 (Odlyzko–Sloane 1979; Levenshtein 1979). All other n are open.
- Edel–Rains–Sloane, *On kissing numbers in dimensions 32 to 128*, Electron. J. Combin. 5 (1998) R22: the three-layer construction both sources use in dims 32–37 and 39.
- Other 2026 lower-bound papers (Ho 19D; EinsteinArena and Station 11D; Takhanov–Assylbekov–Yun 12D; Takhanov–Yun 25–31; Dorofeev–Sun–Wang 40–47; Kamenetsky 49–61) and A. Kravatskiy's repository: see §Survey.

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

### 3. Kravatskiy's repository records in dims 25–31 (worked)

- **Why.** These are the largest values we found in 25–31: the snapshot values in 25, 26 and 27, and newer values in 28–31 (§Survey). Their exact data is published, and only their author has checked them so far. Each package states that its author's own checker (one implementation; the 25D package says "not a claim of two independently implemented checkers") covered every unordered pair. Our check is independent. The repository is not a paper and is unrefereed.
- **Data.** `alexlegeartis/KissingNumbers` @ 907f9b1f4c5f8bb4196ea03775f60cc260189789. `fetch_kravatskiy.py` fetches and pins by sha256 the following:
  - complete coordinate files for 26, 27, 28, 30 and 31: `.npz`, sha256 aafeba2a…d8c3, 3eb58e11…2d59, 3556adb1…d5d2, 3f875bd8…a4b7, 8d8b36e5…acb5;
  - for 25, the exact witness `certificate25.json` (5270afec…1299);
  - for 29, the 232,154-point parent file (5daac8c4…bd4) and `trade.npz` (d85b5cdf…f9cd).

  No repository code is run. `.npz` files are read with numpy's `.npy` reader (allow_pickle=False), and keys, dtypes, shapes and the claimed counts are asserted.
  - 26–28, 30, 31 (`load_kravatskiy.py`): int16 numerators over the common denominator 2, entries in [−8, 8], squared norm 128. In 26D, 32 of the 201,188 rows are (R + √3 S)/2 with S ≠ 0. Our loader checks that their squared norms have no √3 part and sends them to `kiss_check_field.py`. The other rows are integral.
  - 29 (`build_kravatskiy29.py`): the parent rows minus the 11 listed indices, plus the 14 listed rays scaled to squared norm 128 (factors 2, 4, 8). The sha256 of our int16 array equals the `final_little_endian_int16_sha256` in the package manifest (80aa09bd…ecf), so our rebuild is byte-identical to the author's final code.
  - 25 (`build_kravatskiy25.py`): rebuilt with our own Leech shell (`known.py`). The conventions are taken from the package's PROOF.md and its checker `verify_general.py`, read but not run.
    - Each of 926 recorded owner pairs u, u + v (both asserted to be in our shell, with u·v = −24) is deleted. It is replaced by three points ((2u + v)/2 + cos θ · v/2, 2√3 sin θ) at three base phases rotated by rational half-tangents.
    - 247 rational points and 147 further deleted shell vectors (`local_owners`) complete the set: 196,560 − (2·926 + 147) + 2,778 + 247 = 197,586.
    - The circle points lie in ℚ(√2, √3)²⁵, with coefficients of about 40 digits. If we had misread a convention, the rebuilt set would fail our checks; it could not make an invalid set pass, because we check the rebuilt points themselves.
- **Checks.** `kiss_check.c` checks all pairs of integral rows. For 26–31, `kiss_check_np.py` repeats this as a second implementation. For 25D and 26D, `kiss_check_field.py` checks every pair that involves a non-integral row, in both modes. Our pair totals equal the author's stated counts: 25D 4,573,800 exceptional pairs; 26D 20,238,205,078; 27D 22,025,541,786; 29D 26,948,320,246.
- **Dimension.** Every configuration has exactly n columns, so it lies in ℝⁿ.

### 4. Dims 11 and 12: the 604- and 841-point records (worked)

- **11D, τ₁₁ ≥ 604 (EinsteinArena, arXiv:2606.10402v2).** `build_einstein11.py` builds the configuration from the appendix text alone (the hosts with the authors' coordinates are refused here). The backbone has 496 points: ±2eᵢ (i < 8) and all signs on 30 four-point supports. There are 96 points ±e_a ± e_b ± √2 u_j for the pairs (a,b) ∈ {(0,6), (1,4), (2,5), (3,7)}, and 12 points √2(±u_i ± u_j), where u₁, u₂, u₃ = (2,1,2)/3, (2,−2,−1)/3, (1,2,−2)/3 sit in coordinates 8–10.
  - The appendix does not say which 8 of the 32 "transversal" triples make up each of the three layers. The kissing condition forces two things: triples in the same layer meet in at most one element, and no triple appears in two layers. The builder takes the lexicographically first valid choice (printed in its output). With it, the full configuration passes, so the bound holds for this completion of the appendix's construction.
  - Scaled by 3, the backbone is integral and the other 108 points lie in ℤ[√2]¹¹. `kiss_check.c` checks backbone × backbone, and `kiss_check_field.py` (both modes) checks everything else.
  - The contact count is 17,088 + 2,616 = **19,704**. This equals the count the Station paper (arXiv:2608.23691v2, §S1) gives for its Construction 1, which it identifies with EinsteinArena's. Our backbone alone has 17,088 contacts, the size of the "active set" the EinsteinArena paper reports for the basin of its first valid (594-point) solution; the paper says that the backbone is shared by its 594–600 constructions. So our completion appears to be the published configuration up to isometry (the contact count is an isometry invariant; this is evidence, not proof, of isometry).
  - Negative controls: `--variant repeat` (layer 9 reuses a triple of layer 8) fails with 96 violations, and `--variant pairmix` (8 extra points ±e₀ ± e₁ ± √2u₁ on the non-pair (0,1)) fails with 80 violations.
- **12D, τ₁₂ ≥ 841 (Takhanov–Assylbekov–Yun, arXiv:2606.18984v2).** The configuration was found by numerical optimisation, and the paper gives only a floating-point maximum inner product. `check_decimal.py` reads every decimal literal of the published `gram841_coordinates.txt` **exactly** as a rational number, scales each row to integers (the rows are not exactly unit vectors, which does not matter because angles are scale-free) and decides 4p² ≤ AB in Python integers for all 353,220 pairs. So the published 841 points themselves, taken as exact rationals, form a kissing configuration.
  - Largest cosine 0.499999937751432 (pair 413, 756); exact 1/4 − cos² = 6.22·10⁻⁸. There are no contacts.
  - Negative controls: duplicating a row (1 violation), appending row 413 + row 756 (45 violations), and moving row 413 towards row 756 by 10⁻⁶ (8 violations; cosine 0.5000037) all fail. The last shows that the check resolves the 6·10⁻⁸ margin.
  - Kravatskiy's repository also contains an audit of this file (`research/dim12_paper_audit_20261104/decimal841_certificate.json`). We did not read it, so ours is not the only exact check of this file.

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
| **Kravatskiy 25D: 197,586 points, τ₂₅ ≥ 197,586** (rebuilt by `build_kravatskiy25.py` from the pinned witness, with our own Leech shell). All 19,520,014,905 pairs pass. Retained shell (194,561 integer rows): 18,926,894,080 pairs, 0 violations, 443,172,539 contacts (`kiss_check.c`). Circle and rational points (3,025 rows in ℚ(√2,√3)): 593,120,825 pairs (588,547,025 with the shell, 4,573,800 among themselves), 0 violations, 769,352 exact contacts (`kiss_check_field.py`, float mode; interval mode: see the next row) | certificate-checked (exact, all pairs; rebuilt from pinned data by our own code) | `build_kravatskiy25.py` + `kiss_check.c` + `kiss_check_field.py` |
| **Kravatskiy 26D: 201,188 points, τ₂₆ ≥ 201,188**. All 20,238,205,078 pairs pass. Integer rows (201,156): 20,231,767,590 pairs, max 64/64 at norm 128, 441,778,112 contacts (C and numpy agree). √3 rows (32): 6,437,488 pairs, 0 violations, 48 exact contacts (both field modes) | certificate-checked (exact, all pairs) | `load_kravatskiy.py` + `kiss_check.c` / `kiss_check_np.py` + `kiss_check_field.py` |
| **Kravatskiy 27D: 209,884 points, τ₂₇ ≥ 209,884** (all rational). 22,025,541,786 pairs, 0 violations, max 64/64, 424,899,912 contacts (C and numpy agree) | certificate-checked | `load_kravatskiy.py` + `kiss_check.c` / `kiss_check_np.py` |
| **Kravatskiy 28D: 223,528**. 24,982,271,628 pairs, 0 violations, max 64/64, 406,261,728 contacts (C and numpy agree) | certificate-checked | same |
| **Kravatskiy 29D: 232,157** (rebuilt by `build_kravatskiy29.py`; byte-identical to the author's final code by the manifest's sha256). 26,948,320,246 pairs, 0 violations, max 64/64, 395,980,180 contacts (C and numpy agree) | certificate-checked | `build_kravatskiy29.py` + `kiss_check.c` / `kiss_check_np.py` |
| **Kravatskiy 30D: 248,506**. 30,877,491,765 pairs, 0 violations, max 64/64, 381,224,162 contacts (C and numpy agree) | certificate-checked | `load_kravatskiy.py` + `kiss_check.c` / `kiss_check_np.py` |
| **Kravatskiy 31D: 251,524**. 31,632,035,526 pairs, 0 violations, max 64/64, 375,810,468 contacts (C and numpy agree) | certificate-checked | same |
| Negative controls for Kravatskiy's data, each rejected. 27D and 31D with row 0 replaced by a copy of row 1: 1 violation each. With row 0 replaced by row 0 + a contact partner: 798 and 624 violations. 26D with a √3 row duplicated: 1 violation; with one √3 row conjugated (R − √3S)/2: 1 violation. 25D keeping one deleted owner in the shell: 3 violations; with a rational point duplicated: 1 violation | computed (exact) | `perturb.py`, `load_kravatskiy.py --variant`, `build_kravatskiy25.py --variant` |
| **11D: 604 points, τ₁₁ ≥ 604** (EinsteinArena construction, rebuilt from arXiv:2606.10402v2's appendix by `build_einstein11.py`, with the layer triples completed as in §Approaches 4). All 182,106 pairs pass. Backbone (496 integer rows): 122,760 pairs, max 18/18 at norm 36, 17,088 contacts. ℤ[√2] rows (108): 59,346 pairs, 0 violations, 2,616 exact contacts (both field modes). Total 19,704 contacts, equal to the Station paper's count for its Construction 1 (= EinsteinArena's) | certificate-checked (exact, all pairs; built by our own code from the paper's text, with our own choice of layer triples) | `build_einstein11.py` + `kiss_check.c` + `kiss_check_field.py` |
| 11D negative controls: a triple reused across two layers gives 96 violations; 8 extra points on the non-pair (0,1) give 80 violations | computed (exact) | `build_einstein11.py --variant` |
| **12D: 841 points, τ₁₂ ≥ 841** (Takhanov–Assylbekov–Yun, arXiv:2606.18984v2; the published decimal coordinates read as exact rationals). All 353,220 pairs pass in exact integer arithmetic. Largest cosine 0.499999937751432; 1/4 − cos² = 6.22·10⁻⁸; no contacts | certificate-checked (exact, all pairs) | `check_decimal.py` |
| 12D negative controls: a duplicated row (1 violation), row 413 + row 756 appended (45), and row 413 moved towards row 756 by 10⁻⁶ (8; cosine 0.5000037) are all rejected | computed (exact) | `check_decimal.py --control` |

Our pair counts match the counts in Lin's README: 6.85·10¹⁰, 7.64·10¹⁰, 8.62·10¹⁰, 1.25·10¹¹ and 2.96·10¹¹ for 33, 34, 35, 37 and 39D, and 1.83·10¹¹ for 38D.

Costs (wall time on 4 cores, `kiss_check.c`):
- Qiushi: 32D 64 s, 33D 89 s, 34D 99 s, 35D 91 s, 36D 145 s, 37D 132 s, 38D norm-48 rows 402 s, 39D 353 s.
- Lin: 32D 125 s, 33D 139 s, 34D 154 s, 35D 174 s, 37D 246 s, 38D norm-48 rows 426 s, 39D 680 s. Lin's dense layer has no zero coordinates, so our zero-skipping does not help.
- 38D huge-row pairs: 186 s and 191 s on one core (`check_mixed.py`).
- 25D/27D: build 13 s for both. Bulk `kiss_check.c` 26 s / 33 s, `kiss_check_np.py` 178 s (4 processes) / 86 s (2 processes). `kiss_check_field.py` float mode 14 s / 51 s, interval mode 206 s / 449 s (2 processes, run alongside other jobs).
- Kravatskiy 25–31 (2026-11-24, `kiss_check.c`, 4 cores, partly alongside other jobs): 26D 19 s, 27D 20 s, 28D 24 s, 29D 76 s, 30D 30 s, 31D 31 s. 25D: build 1 s, retained shell about 20 s, `kiss_check_field.py` float mode 27 s (4 processes). Second implementation `kiss_check_np.py` (4 processes): 48 s, 50 s, 71 s, 187 s, 203 s for 26, 27, 28, 30, 31.
- 11D and 12D: under 1 s each.
- Survey: about 15 min (arXiv API, TeX sources, shallow clones).
- Peak RAM < 1 GB.

## Next steps

- Done 2026-11-24: Qiushi 25D and 27D rebuilt and checked (above). Our check is of the configuration as built from the pinned data and the paper's text. It does not confirm that the 197,579 and 201,566 inputs are the cited earlier records; we did not open the KissingNumbers repository.
- Optional cross-check: export the authors' numerical 25D array with their `export.py` in a sandbox, and compare it with ours up to row order and scaling. Not done, because it means running downloaded code.
- Qiushi 45D (7,380,090 points, 2.7·10¹³ pairs): about 9 h at the measured 43D rate (8.2·10⁸ pairs/s on 4 cores). That is feasible as a long background job, and using antipodality would halve it.
- **Kamenetsky, dims 49–61 (arXiv:2611.01906v1), and Qiushi's 49–55: not run, too large for brute force.** There are 5.24–6.01·10⁷ points per dimension and 1.4–1.8·10¹⁵ pairs, about 20–26 days at our C rate. Kravatskiy's README already lists larger values in all of 49–61 (reported, not checked). A structure-aware exact check needs the following, all small except (a):
  - (a) The premise that the minimal shell of P₄₈p has norm 6 and 52,416,000 vectors. Either cite extremality (the theta series of an extremal even unimodular 48-dimensional lattice is determined) together with Nebe's/Conway–Sloane's proof that P₄₈p is extremal, or enumerate the shell from the published Gram matrix. A Fincke–Pohst enumeration of 2.6·10⁷ lines in dimension 48 is a long but feasible job.
  - (b) The class: 7,193 lines with cGcᵀ = 6 and |cGc′ᵀ| ≤ 2, which is 2.6·10⁷ pairs (seconds).
  - (c) A_iGA_iᵀ = G for the t ≤ 577 integer automorphisms (seconds).
  - (d) S = |⋃ C₀A_i| by exact de-duplication of at most 4.15·10⁶ sign-canonical rows (seconds).
  - (e) The tails (k ≤ 13, at most 1,154 points) and their t antipodal pairs.
  - (f) The lift (Yang et al., Thm 2.5). Its proof is a short inner-product case split: shell × shell ≤ 3 (by (a)); bulk × lift ≤ (√3/2)(1/2); lift × lift in one block ≤ ¾·⅓ + ¼ = ½; in different blocks ≤ ¾·½ + ¼·½ = ½; tail × lift ≤ ½. We would write it out and check it.

  Data to pin: `dimkadimon/KissingNumbers` @ 191165545b39fdc3099e6e0a46b9b5743410dc1b (`data/class_patch.json`, the automorphism files and `results/verified.json`) and the 7,077-line class from Qiushi's repository.
- **Takhanov–Yun 25–31 (arXiv:2609.21591v2): not run.** They are superseded in all seven dimensions, and only float64 coordinates are published. An exact check would have to rebuild the exact configuration: our Leech shell; S_i and T_i recovered from the float rows; the auxiliary blocks K, K′. It would then bound the rotated cross pairs B × QM, using ‖polar(Q̂) − Q̂‖ ≤ ‖Q̂ᵀQ̂ − I‖ and the 1.7·10⁻⁸ margin. Their 25D (h = ½, poles ±e₂₅) is exact in ℚ(√3) and could be rebuilt cheaply.
- **Ho 19D (arXiv:2603.10425v3): not run.** It is cheap (7·10⁷ pairs) but superseded (12,460 in the snapshot), and the author's script already checks every pair exactly. With rows scaled by positive factors, the file is integral: ±2 / ±1 rows of norm 8 and ±1 sign rows of norm 19. So `kiss_check.c` applies directly once a parser is written.
- **Station Constructions 2 and 3 (11D, 604) and Dorofeev–Sun–Wang (40–47): not run.** The Station data host is refused here. DSW's values are lattice-shell counts and are superseded in 40–46.
- **Kravatskiy's 32–46D values: the next target.** They are current per the snapshot or newer, e.g. 32: 352,992; 38: 652,076 (README). Their packages are compact witnesses in package-specific formats (`witness.json`, `certificate.json`, replacement/trade files), not plain coordinate lists. Each needs a rebuilder like `build_kravatskiy25.py`. Sizes 3.5·10⁵–1.3·10⁷ points; 32–39 are 6·10¹⁰–3·10¹¹ pairs each (minutes).
