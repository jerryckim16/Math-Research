# Chromatic number of the plane (Hadwiger–Nelson problem)

**Area:** combinatorial geometry
**Status:** in progress. Done so far:
- χ ≥ 5 is reproduced end to end with our own pipeline: exact unit edges, our own CNF, and an LRAT proof checked by our own checker.
- The claimed χ ≥ 6 (OpenAI preprint, Sept 2026) is located and mapped. It is an analytic proof with no finite graph. Its one finite certificate (Lemma 8.9) is re-checked exactly here. Its Lean formalization has not yet been re-run here, because the Mathlib cache host is blocked.

**Started:** 2026-11-24
**ProofAtlas:** rank 206, "open". Its 2026-10-07 note: the OpenAI release "narrows the answer to six or seven … proofs not independently audited … Lean artifacts not executed".

## Statement

Let χ(R²) be the least k such that there is a function c : R² → {1, …, k}
with c(x) ≠ c(y) whenever |x − y| = 1. Colour classes are arbitrary
(no measurability), and we work in ZFC.

**Problem.** Determine χ(R²).

- By the de Bruijn–Erdős compactness theorem (ZFC), χ(R²) ≥ k iff some *finite* unit-distance graph has chromatic number ≥ k.
- So a lower bound k can be certified by a finite graph, even when the proof does not exhibit one.

## Known results

- **4 ≤ χ ≤ 7.** The lower bound is the Moser spindle (Moser–Moser 1961). The upper bound is Isbell's hexagonal 7-colouring. [classical]
- **χ ≥ 5.** A. de Grey, arXiv:1804.02385 (1,581-vertex graph). Also Exoo–Ismailescu, arXiv:1805.00157.
- **Smaller 5-chromatic graphs.**
  - M. Heule, arXiv:1805.12181 (553 vertices) and arXiv:1907.00929 (529/510).
  - J. Parts, arXiv:2010.12665: 509 vertices, 2,442 edges. This is still the smallest according to MathWorld (seen via search snippet only).
  - Parts' and Heule's minimal graphs list vertices only on the Polymath16 wiki (asone.ai), which is blocked here; see "Blocked".
- **Measurable version.** χ_m ≥ 5 (Falconer 1981). [cited in the OpenAI preprint; not read]
- **Claimed: χ ≥ 6** (OpenAI, "The Euclidean plane is not five-colorable", September 23, 2026). Details below.

## The χ ≥ 6 claim: source pinned down (2026-11-24)

**Source.**
- ProofAtlas `top500-v35.json`, record `problem.chromatic-number-of-the-plane-hadwiger-nelson-problem`.
- Its status source is `github.com/openai/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, file `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf` (family 158).
- Author: "OpenAI"; the repository README says the work was produced by an internal model.
- Fetched via raw.githubusercontent.com. 60 pages, sha256 `607c2601b5ae655c7c116272840e260f71f637aacf611453186e0a1c65111d36`.
- The file is byte-identical on `main` as of 2026-11-24.
- **[read]**: §§1, 2.1–2.2, 3.3, 4 (start and §4.2), 5.4, 6.2 (Lemma 6.4), 8 in full. The rest was skimmed.

**Exact claims.**
- *Theorem 1.1.* There is no proper 5-colouring of R², with arbitrary colour classes. Hence 6 ≤ χ ≤ 7.
- *Theorem 1.3 (transfer, every k, ZFC).* A proper k-colouring of R² exists iff a *weak measurable k-colouring* exists. That is a Lebesgue-measurable c with Σ_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0 for all R.
- *Theorem 1.4.* No weak measurable 5-colouring exists.
- A measurable proper colouring is weak, so Theorem 1.4 alone would also give **χ_m ≥ 6**. That is a claim beyond Falconer's χ_m ≥ 5.

**What kind of proof.** It is **analytic, not a finite certificate.**
- *Transfer (⇒), §§2–4.*
  - Average a proper colouring over the algebraic plane E = Q̄∩R(i) and its algebraic rotations K.
  - Prove a rigidity theorem (Thm 2.3): every K-invariant probability on the character group of E that gives the continuous characters measure 0 is Haar.
  - This uses Furstenberg–Zimmer compact towers, an invariant-mean line average, and a radial difference inequality.
  - Then project onto the continuous factor.
- *Transfer (⇐), §4.2.* Density points plus de Bruijn–Erdős.
- *Theorem 1.4, §§5–8.*
  - Angular "palettes" of at most 2 labels; cyclic centres form a locally finite set.
  - Disk-average smoothing and a planar cover obstruction extract a label cycle of length 3, 4 or 5, with common exclusion continua.
  - Length 5 is excluded by six-position angular words, length 4 by a parity argument, and length 3 by a Moser-spindle placement (Lemma 8.9, a "rational certificate").

**No finite 6-chromatic unit-distance graph is given.**
- Corollary 1.5 says such a graph exists, by compactness, but calls it "existential".
- So the SAT route in the task (exact edges, then non-5-colourability by LRAT) **cannot be applied to the claim as published**.

**Lean formalization.**
- The catalogue `lean/formalization.yaml` lists `OAI.EuclideanFiveColor.no_proper_five_coloring` in `OAI/Geometry/PlaneColoring/Five.lean`.
- Its comparator config `lean/ComparatorChallenges/EuclideanFiveColor.json` permits only the axioms `propext`, `Quot.sound` and `Classical.choice`.
- The challenge statement, read by us, is:
  ```lean
  def ProperColoring (colorCount : ℕ) (coloring : ℂ → Fin colorCount) : Prop :=
    ∀ point otherPoint : ℂ, ‖point - otherPoint‖ = 1 → coloring point ≠ coloring otherPoint
  theorem no_proper_five_coloring : ¬ ∃ coloring : ℂ → Fin 5, ProperColoring 5 coloring
  ```
  This is exactly Theorem 1.1, with ℂ ≅ R² and the complex norm equal to the Euclidean distance.
- We fetched the transitive OAI imports of `Five.lean`: 70 modules, 30,336 lines, depending only on Mathlib.
  - The pins are Lean `v4.34.1` and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`.
  - `grep` finds no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern` or `unsafe`.
- All 70 Lean files on `main` (2026-11-24) are byte-identical to those at the pinned commit `adc7f12`. The concatenation in `LC_ALL=C sort` path order has sha256 `171452cc…a14e4b`. The toolchain and Mathlib revision are the same at both.
- The Lean proof is organised differently from the paper: Borel transfer, then a mesh / graph-map argument.
- **Map of the Lean sources against the paper** (from imports and statement names; not compiled):

  | Lean directory | Modules / lines | Paper part |
  | --- | --- | --- |
  | `OAI/MeasureTheory/CompactFactors` | 14 / 7,728 | §§2.3–3.2: compact towers, relative centres, conditional limits, Lemma 2.7 |
  | `OAI/Analysis/PlaneSpectrum` | 19 / 8,466 | §§2.1–2.2, 3.3–3.4: characters, invariant mean, wild laws, Haar rigidity (Thm 2.3) |
  | `OAI/Geometry/PlaneColoring` | 37 / 14,142 | §4 (`BorelTransfer.proper_to_borel_weak`, Thm 1.3 ⇒) and §§5–8 (`Palettes`, `Transitions`, `CyclicCore`, `DiskAverages`, `ContinuumLimits`, `FourTransport`, `FiveSupport`, `Moser`, `Mesh`, …) |

  - `Five.lean` combines `proper_to_borel_weak` (proper ⇒ Borel weak colouring) with `no_measurable_weak_five_coloring`.
  - The final step goes through `FullApprox` and a planar-cover lemma (`graph_map_small_mesh_impossible`), not literally through the paper's §8 case split.
  - The converse transfer (§4.2) is not needed for Theorem 1.1, and it is not on the path to `Five.lean`.
  - Lean's `WeakColoring` is "AE-measurable, and c(p) ≠ c(p + e^{iθ}) for (volume × Haar)-a.e. (p, θ)". This is equivalent to Definition 1.2.
  - `Moser.lean` uses the same placement as (8.6), *with* the parentheses: `moserRotation*(moserPoint i+(-290+149*I)/250)`. This matches our corrected reading.
- **We have not compiled it.** See Approach 3.

## Approaches

### 1. Pipeline validation: χ ≥ 5 with our own certificate (worked)

- **Graph.** Heule's explicit construction, arXiv:1805.12181 §4.1, read from the LaTeX source.
  - θ_i is the rotation by arccos((2i−1)/(2i)).
  - V31 = {0} ∪ {θ₁^j θ₃^k (1,0) : j = 0..5, k ∈ {−1, −½, 0, ½, 1}}. This is de Grey's five 7-wheels.
  - V151 = (V31 ⊕ V31) ∩ {|p| ≤ 1}, and V1939 = V31 ⊕ V151.
  - G = V1939 ∪ θ₄(V1939). Heule reports χ(G) = 5.
  - We do not use the published minimal 509/553-vertex graphs, because their data host is blocked.
- **Exact coordinates.** All points lie in Q(√3, √5, √11). `qfield.py` uses exact rational coefficients on the basis {√m : m | 165 squarefree}, which is Q-linearly independent (Besicovitch).
- **Edges.** A float grid search proposes candidates, and every edge is then confirmed exactly (|p−q|² = 1 in the field).
  - Missing edges could only weaken the claim, never make it unsound.
  - 0 float candidates failed the exact test.
  - A second, independent exact pass re-checks the final list.
- **Counts reproduce Heule.** |V31| = 31 with 60 edges, |V151| = 151 with 510 edges, |V1939| = 1939. G has **3,877 vertices and 26,814 edges** (2·1939 − 1, sharing the origin).
- **Encoding** (`encode.py`).
  - Variables x(v,c). Clauses: at least one colour per vertex, and ¬x(u,c) ∨ ¬x(v,c) per edge and colour.
  - No at-most-one clauses.
  - Symmetry breaking: a unit triangle (0, (1,0), (½, √3/2)) is fixed to colours 0, 1, 2.
- **Soundness.**
  - A proper colouring gives distinct colours on the clique, so a colour permutation maps them to 0, 1, 2. The permuted colouring satisfies every clause.
  - Hence UNSAT ⇒ not k-colourable.
  - `test_chromatic_plane.py` checks equisatisfiability with brute force on 150 random small graphs.
- **Result: certificate-checked χ(G) ≥ 5, i.e. χ(R²) ≥ 5.**
  - CNF: 15,508 variables, 111,136 clauses, sha256 `f012031c…992f`.
  - CaDiCaL 1.7.3 UNSAT in 13.4 s.
  - LRAT proof: 57.0 MB, 145,301 lemmas. Checked by our `lrat_check.py` in 6.4 s, then deleted.
- **Sanity checks.**
  - Moser spindle: 3-colouring UNSAT (LRAT-checked), 4-colouring SAT.
  - V1939 is 4-colourable (colouring decoded and checked).
  - G is 5-colourable (found in 126 s, decoded and checked).
  - A tampered LRAT proof is rejected.

### 2. Exact re-check of the finite parts of the χ ≥ 6 paper (worked; partial coverage)

`cert_section8.py` checks the following, all passing.
- **(A) Moser graph (8.5).** 0, A = (√3+i)/2, B = (√3−i)/2, T = √3, and u·{A, B, T} with u = (5+i√11)/6.
  - |u| = 1, and all 11 edges have length exactly 1.
  - Not 3-colourable (exhaustive over 3⁷).
- **(B) Placement (8.6).** z_g = ((35+12i)/37)·(g + (−290+149i)/250).
  - The multiplier has modulus 1, and all placed edges stay exactly unit.
  - *Pitfall:* `pdftotext` drops the large parentheses. The misread formula ((35+12i)/37)·g + (−290+149i)/250 puts 3 of the 7 vertices outside the region.
  - We first got that "failure". It was traced to the misreading by comparing against Table 1, and the formula was confirmed on the rendered page 57.
  - The test suite keeps this as a has-teeth check.
- **(C) Lemma 8.9.** For each of the 7 placed vertices, 0 < l < 4 and P = υ²(3ξ²−υ²)² < P′ = l³(1−l/4)(l−1)², where l = |z|².
  - Each quantity is computed exactly as an element of Q(√3, √11).
  - Signs are decided by rigorous rational enclosures of √3, √11 and √33 (width 10⁻⁴⁰).
  - The smallest margin is P′−P ≈ 6.97·10⁻⁴, at z_B.
- **(D) The paper's own Tables 1–2.** Centres are within h = 0.00011 of the exact coordinates, and the chain P < P₊ < P′₋ < P′ holds. Every row re-checked with Fractions.
- **(E) Identities** (sympy).
  - Lemma 8.8: sin²3φ = υ²(3ξ²−υ²)²/l³; sin 3δ = sin δ(4cos²δ−1) = √(1−l/4)(l−1) when cos δ = r/2; sin3(φ−δ)·sin3(φ+δ) = sin²3φ − sin²3δ; e^{i(φ−δ)} + e^{i(φ+δ)} = 2cos δ·e^{iφ}.
  - Lemma 8.6: F = r² − 2r cos θ, with ∂_θF(1, π/3) = √3.
  - Lemma 6.4: cos γ = 5/6 and |1 − e^{iγ}|² = 1/3 for γ = 2 arcsin(1/(2√3)).
- **(F) Prop. 8.2 (five-cycle), brute force.**
  - Every sign vector with I, O ≠ ∅ is one + run and one − run, of lengths {2, 3}.
  - No six-position palette word exists, even allowing arbitrary independent sign vectors at the three non-antipodal positions. That is a superset of the paper's configurations.
- **(G) Hexagonal 7-colouring.** 2r < 1 and (√21 − 2)r > 1 for r = 2/5.
- **(H) §§2–3 algebra** (sympy and Fractions).
  - Identity (3.14): |A − Bu²|² = (A−B)² + 4AB(Im u)² = |−L + (A−B)u + Lu²|², with L = √(AB) and |u| = 1.
  - The unit decomposition x = k + k′ in Lemma 2.7, with k = x/2 + i√(1−x²/4).
  - The explicit numerics in Lemma 2.7: 18τ²/s² = 0.0018 at s = 100τ, and the Jensen step 0.95² − 0.1 > 1/4.

What this does **not** cover:
- The analytic core: Theorem 2.3 rigidity, the transfer Theorem 1.3, palettes (§5), local finiteness (§6), continuum extraction (§7), and the four-cycle parity argument (§8.3).
- These are tens of pages of ergodic theory and measure-theoretic topology.
- They were not audited, and a 3-hour budget is not enough for an audit.

### 3. Re-run the published Lean proof (in progress: from-source Mathlib build)

- **Plan.** Build `OAI.Geometry.PlaneColoring.Five` at the pinned Lean and Mathlib versions, then `#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring`. The comparator setup also checks that the theorem matches the challenge statement.
- **Blocked.** The Mathlib build cache host `lakecache.blob.core.windows.net` is refused by the network proxy (CONNECT 403), so `lake exe cache get` cannot run. Building Mathlib from source is the fallback (cost below).
- **Reachable:**
  - the Lean toolchain release (github.com/leanprover/lean4 releases);
  - the Mathlib git repository;
  - raw.githubusercontent.com, for the OAI sources.
- **Toolchain, obtained through allowed hosts.**
  - `elan toolchain install` failed: its manifest/self-update lookup got a 403.
  - The release tarball `lean-4.34.1-linux.tar.zst` (580 MB) downloaded directly from github.com releases (via release-assets.githubusercontent.com).
  - It was unpacked with the PyPI `zstandard` module (no `zstd` binary here) and linked with `elan toolchain link`.
  - Mathlib `d13f23b` was fetched with `git fetch --depth 1` (152 MB). Lake cloned the Mathlib dependencies from GitHub.
  - Everything lives in the scratchpad, outside the repository.
- **Size.** The OAI files `import Mathlib`, so the whole library is needed: 8,530 Mathlib modules (2,336,169 lines), plus about 300 modules from dependencies.
- **Measured cost** (4 cores, 15 GB). Slice 1, 23 min wall:
  - 2,287 Mathlib modules (532,515 lines), 72 min user CPU, about 3.3 cores busy;
  - 105 lines per CPU-second, from the per-module times Lake reports.
  - Extrapolated: about 6 CPU-hours for Mathlib, so about 2 h wall here.
  - Throughput falls in the analysis-heavy layers, so this is a lower estimate.
  - After slice 2 (47 min wall in total): 3,820 modules, 997,769 lines (43 % of Mathlib by lines), 155 min user CPU, 94.6 lines per CPU-second, no errors. Updated extrapolation: about 7 CPU-hours for Mathlib.
- **Source hygiene.** The 70 OAI files contain no `set_option` at all, and no `macro`, `syntax`, `elab_rules`, `initialize`, `run_cmd` or `#eval`. Nothing in them can switch off kernel checking.
  - The 30k-line OAI development comes on top.
- **Scripted:** `computations/chromatic-plane/lean_recheck/lean_recheck.sh` (text only; no build outputs are kept in the repository).
- **Lean-specific check prepared:** `lean_recheck/Check.lean`. It restates the theorem from scratch, with no OAI definitions:
  ```lean
  theorem plane_not_five_colourable :
      ¬ ∃ c : ℂ → Fin 5, ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y :=
    OAI.EuclideanFiveColor.no_proper_five_coloring
  #print axioms CNPRecheck.plane_not_five_colourable
  ```

### 4. Find a finite 6-chromatic unit-distance graph (not attempted)

- Theorem 1.1 plus compactness implies one exists, but the proof is non-constructive.
- No candidate is published, and none is known to the literature we read.
- Out of scope for this step.

## Blocked / failed routes

- **GitHub access to `openai/math`.**
  - `gh api` was refused: the repository is not enabled for this session.
  - `add_repo` was denied by the permission classifier.
  - The web tree page github.com/openai/math/tree/… returned 403.
  - Public files were read instead via raw.githubusercontent.com, so directory listings were done by following imports.
- **Polymath16 wiki (asone.ai).** Blocked by the proxy (CONNECT 403). The Parts 509-vertex and Heule 553-vertex vertex lists are not available. We used Heule's explicit construction instead.
- **Mathlib cache (lakecache.blob.core.windows.net).** Blocked by the proxy (CONNECT 403).

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| χ(R²) ≥ 4 (Moser spindle) | certificate-checked (exact edges; LRAT, our checker) | `run_pipeline.py moser 3` |
| χ(R²) ≥ 5 (Heule's G, 3,877 vertices, 26,814 edges) | certificate-checked (exact edges; LRAT, 145,301 lemmas, our checker) | `run_pipeline.py heule 4` |
| χ(R²) ≤ 7 | proved (classical); inequalities re-checked | `cert_section8.py` (G) |
| OpenAI Lemma 8.9 (Moser placement lies in region (8.4)) | checked exactly (algebraic arithmetic plus rigorous intervals) | `cert_section8.py` (A–D) |
| OpenAI Prop. 8.2 finite combinatorics | computed (exhaustive, superset of cases) | `cert_section8.py` (F) |
| **χ(R²) ≥ 6 (OpenAI, Thm 1.1)** | **claimed; not verified here.** Unrefereed preprint; Lean proof published but not re-run here; the analytic core is not audited; no finite certificate exists to check | — |

## Next steps

- Lean re-check: get `lakecache.blob.core.windows.net` allowed, or budget a from-source Mathlib build; then compile `Five.lean` and print its axioms.
- If the Lean check passes, audit the Lean *statement chain*: that `ProperColoring` and the `ComparatorChallenges` statement are what `Five.lean` proves, and that no local `instance` or `notation` changes the meaning of ℂ, `‖·‖` or `Fin 5`.
- Optional: an adversarial read of §§2–4, the transfer, where the claim is most surprising.
