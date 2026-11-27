# Chromatic number of the plane (Hadwiger–Nelson problem)

*Best read on the [progress site](https://jerryckim16.github.io/Math-Research/problems/chromatic-number-plane.html), where all the math is typeset. GitHub's own preview does not render the math in long files.*

**Area:** combinatorial geometry
**Status:** in progress. Done so far:
- $\chi \ge 5$ is reproduced end to end with our own pipeline: exact unit edges, our own CNF, and an LRAT proof checked by our own checker.
- The claimed $\chi \ge 6$ (OpenAI preprint, Sept 2026) is located and mapped. It is an analytic proof with no finite graph. Its one finite certificate (Lemma 8.9) is re-checked exactly here.
- **Its published Lean proof was re-run here from source.**
  - Mathlib was built from scratch, because the cache host is blocked.
  - All 70 OAI modules compile.
  - A from-scratch restatement of "no proper 5-colouring of $\mathbb{R}^{2}$" is proved by the OAI theorem and depends only on [propext, Classical.choice, Quot.sound].
  - So $\chi \ge 6$ is **Lean-verified (re-run here)**, modulo trust in the Lean 4.34.1 kernel and the faithfulness of the restated statement.
  - **Kernel replay (`leanchecker`).** The compiled `.olean` files were re-checked by the kernel, independently of the elaborator:
    - all 70 OAI modules, one at a time;
    - the whole 787,391-constant environment (core, Mathlib, OAI) from scratch with `--fresh`: exit 0, 41 min.
  - The paper's analytic argument itself was not audited by a human.
  - The SAT-style verification criteria (exact edges, LRAT-checked non-5-colourability) **do not apply and are not met**, because no finite 6-chromatic graph exists in the source. The evidence for $\chi \ge 6$ is the re-run formal proof, not a certificate.

**Started:** 2026-11-24
**ProofAtlas:** rank 206, "open". Its 2026-10-07 note: the OpenAI release "narrows the answer to six or seven … proofs not independently audited … Lean artifacts not executed".

## Statement

Let $\chi(\mathbb{R}^{2})$ be the least $k$ such that there is a function $c : \mathbb{R}^{2} \to \{1, \dots, k\}$
with $c(x) \ne c(y)$ whenever $\lvert x - y\rvert = 1$. Colour classes are arbitrary
(no measurability), and we work in ZFC.

**Problem.** Determine $\chi(\mathbb{R}^{2})$.

- By the de Bruijn–Erdős compactness theorem (ZFC), $\chi(\mathbb{R}^{2}) \ge k$ iff some *finite* unit-distance graph has chromatic number $\ge k$.
- So a lower bound $k$ can be certified by a finite graph, even when the proof does not exhibit one.

## Known results

- **$4 \le \chi \le 7$.** The lower bound is the Moser spindle (Moser–Moser 1961). The upper bound is Isbell's hexagonal 7-colouring. [classical]
- **$\chi \ge 5$.** A. de Grey, arXiv:1804.02385 (1,581-vertex graph). Also Exoo–Ismailescu, arXiv:1805.00157.
- **Smaller 5-chromatic graphs.**
  - M. Heule, arXiv:1805.12181 (553 vertices) and arXiv:1907.00929 (529/510).
  - J. Parts, arXiv:2010.12665: 509 vertices, 2,442 edges. This is still the smallest according to MathWorld (seen via search snippet only).
  - Parts' and Heule's minimal graphs list vertices only on the Polymath16 wiki (asone.ai), which is blocked here; see "Blocked".
- **Measurable version.** $\chi_{m} \ge 5$ (Falconer 1981). [cited in the OpenAI preprint; not read]
- **Claimed: $\chi \ge 6$** (OpenAI, "The Euclidean plane is not five-colorable", September 23, 2026). Details below.

## The $\chi \ge 6$ claim: source pinned down (2026-11-24)

**Source.**
- ProofAtlas `top500-v35.json`, record `problem.chromatic-number-of-the-plane-hadwiger-nelson-problem`.
- Its status source is `github.com/openai/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, file `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/paper.pdf` (family 158).
- Author: "OpenAI"; the repository README says the work was produced by an internal model.
- Fetched via raw.githubusercontent.com. 60 pages, sha256 `607c2601b5ae655c7c116272840e260f71f637aacf611453186e0a1c65111d36`.
- The file is byte-identical on `main` as of 2026-11-24.
- **[read]**: §§1, 2.1–2.2, 3.3, 4 (start and §4.2), 5.4, 6.2 (Lemma 6.4), 8 in full. The rest was skimmed.

**Exact claims.**
- *Theorem 1.1.* There is no proper 5-colouring of $\mathbb{R}^{2}$, with arbitrary colour classes. Hence $6 \le \chi \le 7$.
- *Theorem 1.3 (transfer, every $k$, ZFC).* A proper $k$-colouring of $\mathbb{R}^{2}$ exists iff a *weak measurable $k$-colouring* exists. That is a Lebesgue-measurable $c$ with $\sum_{i} \int_{B(0,R)} \int_{S^{1}} 1_{A_{i}}(x) 1_{A_{i}}(x+u)\, d\sigma(u)\, dx = 0$ for all $R$.
- *Theorem 1.4.* No weak measurable 5-colouring exists.
- A measurable proper colouring is weak, so Theorem 1.4 alone would also give **$\chi_{m} \ge 6$**. That is a claim beyond Falconer's $\chi_{m} \ge 5$.

**What kind of proof.** It is **analytic, not a finite certificate.**
- *Transfer $(\Rightarrow)$, §§2–4.*
  - Average a proper colouring over the algebraic plane $E = \overline{\mathbb{Q}}\cap\mathbb{R}(i)$ and its algebraic rotations $K$.
  - Prove a rigidity theorem (Thm 2.3): every $K$-invariant probability on the character group of $E$ that gives the continuous characters measure 0 is Haar.
  - This uses Furstenberg–Zimmer compact towers, an invariant-mean line average, and a radial difference inequality.
  - Then project onto the continuous factor.
- *Transfer $(\Leftarrow)$, §4.2.* Density points plus de Bruijn–Erdős.
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
  This is exactly Theorem 1.1, with $\mathbb{C} \cong \mathbb{R}^{2}$ and the complex norm equal to the Euclidean distance.
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
  | `OAI/Geometry/PlaneColoring` | 37 / 14,142 | §4 (`BorelTransfer.proper_to_borel_weak`, Thm 1.3 $\Rightarrow$) and §§5–8 (`Palettes`, `Transitions`, `CyclicCore`, `DiskAverages`, `ContinuumLimits`, `FourTransport`, `FiveSupport`, `Moser`, `Mesh`, …) |

  - `Five.lean` combines `proper_to_borel_weak` (proper $\Rightarrow$ Borel weak colouring) with `no_measurable_weak_five_coloring`.
  - The final step goes through `FullApprox` and a planar-cover lemma (`graph_map_small_mesh_impossible`), not literally through the paper's §8 case split.
  - The converse transfer (§4.2) is not needed for Theorem 1.1, and it is not on the path to `Five.lean`.
  - Lean's `WeakColoring` is "AE-measurable, and $c(p) \ne c(p + e^{i\theta})$ for (volume $\times$ Haar)-a.e. $(p, \theta)$". This is equivalent to Definition 1.2.
  - `Moser.lean` uses the same placement as (8.6), *with* the parentheses: `moserRotation*(moserPoint i+(-290+149*I)/250)`. This matches our corrected reading.
- **We have not compiled it.** See Approach 3.

## Approaches

### 1. Pipeline validation: $\chi \ge 5$ with our own certificate (worked)

- **Graph.** Heule's explicit construction, arXiv:1805.12181 §4.1, read from the LaTeX source.
  - $\theta_{i}$ is the rotation by $\arccos((2i-1)/(2i))$.
  - $V31 = \{0\} \cup \{\theta_{1}^{j} \theta_{3}^{k} (1,0) : j = 0\dots 5, k \in \{-1, -\tfrac{1}{2}, 0, \tfrac{1}{2}, 1\}\}$. This is de Grey's five 7-wheels.
  - $V151 = (V31 \oplus V31) \cap \{\lvert p\rvert \le 1\}$, and $V1939 = V31 \oplus V151$.
  - $G = V1939 \cup \theta_{4}(V1939)$. Heule reports $\chi(G) = 5$.
  - We do not use the published minimal 509/553-vertex graphs, because their data host is blocked.
- **Exact coordinates.** All points lie in $\mathbb{Q}(\sqrt{3}, \sqrt{5}, \sqrt{11})$. `qfield.py` uses exact rational coefficients on the basis $\{\sqrt{m} : m \mid 165 \text{ squarefree}\}$, which is $\mathbb{Q}$-linearly independent (Besicovitch).
- **Edges.** A float grid search proposes candidates, and every edge is then confirmed exactly ($\lvert p-q\rvert^{2} = 1$ in the field).
  - Missing edges could only weaken the claim, never make it unsound.
  - 0 float candidates failed the exact test.
  - A second, independent exact pass re-checks the final list.
- **Counts reproduce Heule.** $\lvert V31\rvert = 31$ with 60 edges, $\lvert V151\rvert = 151$ with 510 edges, $\lvert V1939\rvert = 1939$. $G$ has **3,877 vertices and 26,814 edges** ($2\cdot 1939 - 1$, sharing the origin).
- **Encoding** (`encode.py`).
  - Variables $x(v,c)$. Clauses: at least one colour per vertex, and $\neg x(u,c) \vee \neg x(v,c)$ per edge and colour.
  - No at-most-one clauses.
  - Symmetry breaking: a unit triangle $(0, (1,0), (\tfrac{1}{2}, \sqrt{3}/2))$ is fixed to colours 0, 1, 2.
- **Soundness.**
  - A proper colouring gives distinct colours on the clique, so a colour permutation maps them to 0, 1, 2. The permuted colouring satisfies every clause.
  - Hence UNSAT $\Rightarrow$ not $k$-colourable.
  - `test_chromatic_plane.py` checks equisatisfiability with brute force on 150 random small graphs.
- **Result: certificate-checked $\chi(G) \ge 5$, i.e. $\chi(\mathbb{R}^{2}) \ge 5$.**
  - CNF: 15,508 variables, 111,136 clauses, sha256 `f012031c…992f`.
  - CaDiCaL 1.7.3 UNSAT in 13.4 s.
  - LRAT proof: 57.0 MB, 145,301 lemmas. Checked by our `lrat_check.py` in 6.4 s, then deleted.
- **Sanity checks.**
  - Moser spindle: 3-colouring UNSAT (LRAT-checked), 4-colouring SAT.
  - V1939 is 4-colourable (colouring decoded and checked).
  - $G$ is 5-colourable (found in 126 s, decoded and checked).
  - A tampered LRAT proof is rejected.

### 2. Exact re-check of the finite parts of the $\chi \ge 6$ paper (worked; partial coverage)

`cert_section8.py` checks the following, all passing.
- **(A) Moser graph (8.5).** 0, $A = (\sqrt{3}+i)/2$, $B = (\sqrt{3}-i)/2$, $T = \sqrt{3}$, and $u\cdot\{A, B, T\}$ with $u = (5+i\sqrt{11})/6$.
  - $\lvert u\rvert = 1$, and all 11 edges have length exactly 1.
  - Not 3-colourable (exhaustive over $3^{7}$).
- **(B) Placement (8.6).** $z_{g} = ((35+12i)/37)\cdot(g + (-290+149i)/250)$.
  - The multiplier has modulus 1, and all placed edges stay exactly unit.
  - *Pitfall:* `pdftotext` drops the large parentheses. The misread formula $((35+12i)/37)\cdot g + (-290+149i)/250$ puts 3 of the 7 vertices outside the region.
  - We first got that "failure". It was traced to the misreading by comparing against Table 1, and the formula was confirmed on the rendered page 57.
  - The test suite keeps this as a has-teeth check.
- **(C) Lemma 8.9.** For each of the 7 placed vertices, $0 < l < 4$ and $P = \upsilon^{2}(3\xi^{2}-\upsilon^{2})^{2} < P' = l^{3}(1-l/4)(l-1)^{2}$, where $l = \lvert z\rvert^{2}$.
  - Each quantity is computed exactly as an element of $\mathbb{Q}(\sqrt{3}, \sqrt{11})$.
  - Signs are decided by rigorous rational enclosures of $\sqrt{3}$, $\sqrt{11}$ and $\sqrt{33}$ (width $10^{-40}$).
  - The smallest margin is $P'-P \approx 6.97\cdot 10^{-4}$, at $z_{B}$.
- **(D) The paper's own Tables 1–2.** Centres are within $h = 0.00011$ of the exact coordinates, and the chain $P < P_{+} < P'_{-} < P'$ holds. Every row re-checked with Fractions.
- **(E) Identities** (sympy).
  - Lemma 8.8: $\sin^{2}3\varphi = \upsilon^{2}(3\xi^{2}-\upsilon^{2})^{2}/l^{3}$; $\sin 3\delta = \sin \delta(4\cos^{2}\delta-1) = \sqrt{1-l/4}(l-1)$ when $\cos \delta = r/2$; $\sin 3(\varphi-\delta)\cdot\sin 3(\varphi+\delta) = \sin^{2}3\varphi - \sin^{2}3\delta$; $e^{i(\varphi-\delta)} + e^{i(\varphi+\delta)} = 2\cos \delta\cdot e^{i\varphi}$.
  - Lemma 8.6: $F = r^{2} - 2r \cos \theta$, with $\partial_{\theta}F(1, \pi/3) = \sqrt{3}$.
  - Lemma 6.4: $\cos \gamma = 5/6$ and $\lvert 1 - e^{i\gamma}\rvert^{2} = 1/3$ for $\gamma = 2 \arcsin(1/(2\sqrt{3}))$.
- **(F) Prop. 8.2 (five-cycle), brute force.**
  - Every sign vector with $I, O \ne \emptyset$ is one $+$ run and one $-$ run, of lengths $\{2, 3\}$.
  - No six-position palette word exists, even allowing arbitrary independent sign vectors at the three non-antipodal positions. That is a superset of the paper's configurations.
- **(G) Hexagonal 7-colouring.** $2r < 1$ and $(\sqrt{21} - 2)r > 1$ for $r = 2/5$.
- **(H) §§2–3 algebra** (sympy and Fractions).
  - Identity (3.14): $\lvert A - Bu^{2}\rvert^{2} = (A-B)^{2} + 4AB(\operatorname{Im} u)^{2} = \lvert-L + (A-B)u + Lu^{2}\rvert^{2}$, with $L = \sqrt{AB}$ and $\lvert u\rvert = 1$.
  - The unit decomposition $x = k + k'$ in Lemma 2.7, with $k = x/2 + i\sqrt{1-x^{2}/4}$.
  - The explicit numerics in Lemma 2.7: $18\tau^{2}/s^{2} = 0.0018$ at $s = 100\tau$, and the Jensen step $0.95^{2} - 0.1 > 1/4$.

What this does **not** cover:
- The analytic core: Theorem 2.3 rigidity, the transfer Theorem 1.3, palettes (§5), local finiteness (§6), continuum extraction (§7), and the four-cycle parity argument (§8.3).
- These are tens of pages of ergodic theory and measure-theoretic topology.
- They were not audited, and a 3-hour budget is not enough for an audit.

### 3. Re-run the published Lean proof (worked)

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
  - After slice 4 (94 min wall in total): 6,575 modules, 1,705,584 lines (73 %), about 330 min user CPU, 79.3 lines per CPU-second, no errors. Extrapolation: about 8.2 CPU-hours for all of Mathlib, about 2.5 h wall on 4 cores.
  - **Mathlib build complete** after 7 slices (14:05 UTC): `lake build Mathlib` exited 0 with no errors. That took 2 h 28 min wall and about 8.5 CPU-hours (sum of `user` times).
- **Source hygiene.**
  - The 70 OAI files contain no `set_option` at all, and no `macro`, `syntax`, `elab_rules`, `initialize`, `run_cmd` or `#eval`. Nothing in them can switch off kernel checking.
  - All 108 `instance` declarations are on OAI's own types (type synonyms such as `DiscreteE`, the character space `D`, measures and kernels), or are `Decidable` instances.
  - No instance or notation touches `Norm ℂ`, `ℂ` or `Fin 5`, so the restated statement below means what it says.
- **OAI compile (14:05–14:11 UTC).**
  - The 70 modules were compiled in dependency order with plain `lean -o` against the fresh Mathlib build (`lean_recheck/compile_oai.py`): **70/70 OK, 362 s wall, no errors, no `sorry` warnings.**
  - The compiled sources are the files with sha256 `171452cc…`, which equal the pinned commit.
- **Scripted:** `computations/chromatic-plane/lean_recheck/lean_recheck.sh` (text only; no build outputs are kept in the repository).
- **Statement and axiom check** (`lean_recheck/Check.lean`, sha256 `614d6a48…`). It restates the theorem from scratch, with no OAI definitions:
  ```lean
  theorem plane_not_five_colourable :
      ¬ ∃ c : ℂ → Fin 5, ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y :=
    OAI.EuclideanFiveColor.no_proper_five_coloring
  #print axioms CNPRecheck.plane_not_five_colourable
  ```
  - Output: `'CNPRecheck.plane_not_five_colourable' depends on axioms: [propext, Classical.choice, Quot.sound]`. The same holds for `OAI.EuclideanFiveColor.no_proper_five_coloring`.
  - The statement is exactly Theorem 1.1, with $\mathbb{C} = \mathbb{R}^{2}$ and the complex norm equal to the Euclidean distance.
  - Negative control: a `sorry`-proved theorem in the same environment reports `[sorryAx]`.
- **Trust base.** The Lean 4.34.1 kernel and elaborator (official release binary), Mathlib `d13f23b`, and our 5-line restatement.
  - The kernel replay below removes the elaborator and the `.olean` writer from the trust base for the 70 OAI modules.
  - Not done: a human audit of the paper's §§2–7.

### 3b. Kernel replay of the OAI `.olean` files with `leanchecker` (worked; full-environment replay also passed)

- **Tool.**
  - `leanchecker` ships with the Lean toolchain (`bin/leanchecker` of the official v4.34.1 release; source `src/lean/LeanChecker.lean`, by K. Morrison and S. Ullrich; it is lean4checker moved into core).
  - It loads compiled `.olean` files and re-adds every stored declaration through the kernel's `addDecl` (`Lean.Kernel.Environment.replay`).
  - So it re-checks what the files contain, independently of the elaborator, tactics and `.olean` writer that produced them. Its own docstring says it detects "environment hacking"; it is not an external verifier, since it uses the same kernel.
- **Default mode, all 70 OAI modules** (`lean_recheck/kernel_replay.sh` step 2).
  - Each module's own constants are replayed on top of its imported environment, one module per process: `LEAN_PATH=<mathlib paths>:oaicheck/build leanchecker -v <module>`.
  - **70/70 exit 0, no errors. 569 s wall in total; the slowest is `OAI.Analysis.PlaneSpectrum.Basic` at 100 s; `OAI.Geometry.PlaneColoring.Five` takes 5.5 s.**
  - The replay covers **4,273 constants, 3,553 of them theorems**. They were counted from the 70 `.olean` files with `lean_recheck/count_constants.lean`, which reads exactly the constant table `leanchecker` replays.
  - Every OAI declaration on which `no_proper_five_coloring` depends is therefore re-checked by the kernel.
  - Running all 70 at once (`leanchecker OAI`) starts one task per module, each importing Mathlib. On 15 GB RAM it was OOM-killed after 65 s, so the modules were run one at a time.
- **Controls** (`lean_recheck/controls/NegCtl/`, each compiled with `lean -o` and checked the same way).
  - *Hack:* an ill-typed `theorem NegCtl.bad : False := True.intro`, injected with `addDecl` under `debug.skipKernelTC = true` (environment hacking), plus a theorem that uses it.
    - It compiles without error, and `leanchecker` **rejects** it: `(kernel) declaration type mismatch, 'NegCtl.bad' has type True but it is expected to have type False`, exit 1.
    - This shows the tool really re-checks declarations, rather than trusting the `.olean`.
  - *Good:* the same mechanism with the kernel check on and a well-typed value. Passes.
  - *Sorry:* a `sorry` proof also passes, because `sorryAx` is an axiom, not a kernel error. So `leanchecker` does not replace the `#print axioms` check above. The two together are the evidence.
- **Fresh mode** (`leanchecker --fresh OAI.Geometry.PlaneColoring.Five`, step 4).
  - It replays the *entire* environment of `Five` into an empty kernel environment, single-threaded: Init, Std, Lean, all of Mathlib and its dependencies, and the OAI modules. That is **787,391 constants** in 10,814 modules (`env_size.lean`).
  - This also re-checks Mathlib and core rather than trusting their `.olean` files.
  - Calibration: `--fresh` on `Mathlib.Algebra.Group.Basic` (143,112 constants) took 95 s; on `Mathlib.Topology.Basic` (209,366) 142 s at 1.45 GB peak RSS.
  - The full run, 14:34–15:15 UTC: **exit 0, no errors.** It took 2,469 s wall (41 min) and 2,367 s user CPU on one core, at 8.18 GB peak RSS (most of it file-backed `.olean` mappings).
  - Linear extrapolation from the calibration predicted about 10 min. The analysis and measure-theory layers of Mathlib cost the kernel far more per constant than the early layers.
  - The memory watchdog (kill at about 10.5 GB) never fired.
- **Label.** **Kernel-replayed in full.** Every one of the 787,391 constants in the environment of `OAI.Geometry.PlaneColoring.Five` was re-checked by the Lean 4.34.1 kernel, starting from an empty environment. That covers core, Mathlib `d13f23b` with its dependencies, and the 70 OAI modules.
  - The 70 OAI modules were also replayed module by module on top of their imports.
  - What is still trusted:
    - the kernel itself, run as the same binary and code that type-checked the proof at compile time, so this is not an independent kernel such as lean4lean or nanoda;
    - `leanchecker`'s loading code;
    - the 5-line restatement in `Check.lean`.
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
- **Mathlib cache (lakecache.blob.core.windows.net).** Blocked by the proxy (CONNECT 403). Worked around by building Mathlib from source (about 8.5 CPU-hours).
- **`elan toolchain install`.** Its GitHub API/manifest lookups got a 403. Worked around by downloading the release tarball directly.

## Results

| Claim | Evidence level | Where |
| --- | --- | --- |
| $\chi(\mathbb{R}^{2}) \ge 4$ (Moser spindle) | certificate-checked (exact edges; LRAT, our checker) | `run_pipeline.py moser 3` |
| $\chi(\mathbb{R}^{2}) \ge 5$ (Heule's $G$, 3,877 vertices, 26,814 edges) | certificate-checked (exact edges; LRAT, 145,301 lemmas, our checker) | `run_pipeline.py heule 4` |
| $\chi(\mathbb{R}^{2}) \le 7$ | proved (classical); inequalities re-checked | `cert_section8.py` (G) |
| OpenAI Lemma 8.9 (Moser placement lies in region (8.4)) | checked exactly (algebraic arithmetic plus rigorous intervals) | `cert_section8.py` (A–D) |
| OpenAI Prop. 8.2 finite combinatorics | computed (exhaustive, superset of cases) | `cert_section8.py` (F) |
| **$\chi(\mathbb{R}^{2}) \ge 6$ (OpenAI, Thm 1.1)** | **Lean-verified (OpenAI's formalization, re-run here from source), and kernel-replayed with `leanchecker`**: 70/70 OAI modules in default mode (4,273 constants), plus `--fresh` replay of the whole 787,391-constant environment from scratch. Statement independently restated; axioms are only propext, Classical.choice, Quot.sound. Not refereed, the analytic text is not human-audited, and no finite certificate exists | `lean_recheck/` (`lean_recheck.sh`, `kernel_replay.sh`) |
| $\chi(\mathbb{R}^{2}) \in \{6, 7\}$ | Lean-verified lower bound (above) plus the classical upper bound | — |

## Next steps

- Replay the proof with a kernel written independently of Lean's C++ kernel, to remove trust in that kernel too.
  - Candidates: lean4lean, or nanoda via a `lean4export` file.
  - Cost not measured. The `--fresh` replay with Lean's own kernel took 41 min single-threaded.
  - The 18 GB build tree was deleted after this session, so this needs a rebuild: about 2.5 h with `lean_recheck.sh`.
- Optional: an adversarial read of §§2–4, the transfer, where the claim is most surprising.
