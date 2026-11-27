# Lonely Runner Conjecture: literature and idea survey (25 Nov 2026)

*Best read on the [progress site](https://jerryckim16.github.io/Math-Research/notes/lonely-runner/literature.html), where all the math is typeset. GitHub's own preview does not render the math in long files.*

Scope: every result reachable on 2026-11-25 that bears on $\mathrm{LRC}(15)$ (16 runners),
the next cases, and the general conjecture. Conventions follow
`problems/lonely-runner.md`: $\mathrm{LRC}(k)$ means $k$ positive integer speeds, threshold
$1/(k+1)$, i.e. $k+1$ runners.

**Headline. $\mathrm{LRC}(15)$ is already claimed.** J. Allikvere, *Sixteen lonely
runners*, was deposited on Zenodo on 2026-10-11 (not on arXiv). W. Toner,
*Seventeen lonely runners, assuming sixteen*, followed on 2026-10-22 and claims
$\mathrm{LRC}(16)$ conditional on it. Neither is refereed, and neither has been
re-implemented independently, although Toner reports a partial replay. The
first case with no located claim is now **$\mathrm{LRC}(17)$ (18 runners)**.

Evidence labels used below:

- **refereed**: published in a refereed venue (journal reference as recorded on
  arXiv or by the citing paper);
- **preprint**: arXiv or Zenodo, not refereed;
- **claim (cert.)**: a preprint whose proof rests on a large computation with
  published certificates;
- **[src]**: we read the LaTeX source or full text;
- **[abs]**: we read the abstract or metadata only.

All downloaded material was treated as data. No code from any archive was run.

## 1. Search method and what was unreachable

Searches made on 2026-11-25:

- **arXiv API (export.arxiv.org).**
  - Full-text queries: `"lonely runner"`, `"lonely runners"`, `abs:lonely AND abs:runner`.
  - Other topics: `"view obstruction"`, `"covering radius" AND zonotope`, `"Wills conjecture"`, `loneliness AND speeds`, `sixteen AND runners`.
  - A title search for `lonely`.
  - All results were sorted by submission date. The newest relevant item is 2611.10782 (7 Nov 2026), and 2609.06259 was updated to v3 on 24 Nov 2026.
- **Zenodo API.**
  - Queries: `"lonely runner"` (71 hits, all listed), `"sixteen lonely runners"`, `"seventeen lonely runners"`, `"eighteen lonely runners"` (0 hits), `"LRC(16)"` and `"LRC(17)"` (0 hits).
  - The two key records were checked for later versions: each has a single version.
- **ProofAtlas.** Rank-477 entry on the open-problem list (status reviewed 12 Nov 2026), and the collaboration workspace `/collaboration/lonely-runner-conjecture/`. Both were fetched with curl; WebFetch's resolver refused the host.
- **GitHub.** The `munimtechnologies/lonely-runner-16` README, read through WebFetch. The `gh` API returned 403 ("GitHub access to this repository is not enabled for this session").
- **Web search.** General queries, plus the Rostock workshop page found through search results.

Unreachable hosts:

| host | what failed | consequence |
| --- | --- | --- |
| hexagonmath.org | no DNS (blocked) | unread |
| mathworld.wolfram.com | no DNS | unread (only used before for the Hu–Jing abstract; that preprint is now read on arXiv) |
| www.mathematik.uni-rostock.de | no DNS | **programme of the LRC workshop, Rostock, 6–9 Oct 2026, unread**. From search snippets, the talks include Wills (history), Goddyn (tight instances), Bedert (one-sided Fourier) and Santos (shifted counterexamples). |
| semanticscholar.org, scholar.google.com, api.openalex.org, api.crossref.org | no DNS | no citation-graph search, so the search is not exhaustive for journal-only papers |
| api.github.com for the munim repository | 403 (session permission) | README read via WebFetch only |

## 2. State of the art (as of 25 Nov 2026)

### 2.1 Finite cases

| runners | $k$ | status | source |
| --- | --- | --- | --- |
| $\le 7$ | $\le 6$ | refereed (classical; 7 runners: Barajas–Serra, EJC 15 (2008) R48) | see `problems/lonely-runner.md`. **Erratum:** H. Chen, Zenodo 10.5281/zenodo.22852990 (20 Sep 2026, technical note, [abs]), reports a gap in §6.6 of Barajas–Serra (an inference needs $\ell \le 2$ but only $\ell \le 3$ is available; the counterexample to the printed inference has $N = 343$), with a Lean 4 repair of $n \le 7$ at 10.5281/zenodo.22851977. Not checked here. |
| 8 | 7 | refereed | Rosenfeld, arXiv:2509.14111v2, *Math. Comp.* (2026) [src earlier] |
| 9, 10 | 8, 9 | refereed | Trakulthongchai, arXiv:2511.22427v2, *EJC* 33(2) (2026) P2.46; 9 also by Rosenfeld, arXiv:2512.01912v2 (preprint) [src] |
| 11–13 | 10–12 | preprint, claim (cert.) | Sungkawichai–Trakulthongchai, arXiv:2604.23906v2 (1 Sep 2026) [src] |
| 14, 15 | 13, 14 | preprint, claim (cert.) | Allikvere, arXiv:2609.02604v2 (24 Sep 2026) [src]; re-checked here (Approach 7 of the problem file). Independent audit of the $\mathrm{LRC}(13)$ part: D. M. Thornton, Zenodo 10.5281/zenodo.22974881 (26 Sep 2026) [abs]. |
| **16** | **15** | **claim (cert.), Zenodo only** | **J. Allikvere, "Sixteen lonely runners: manuscript, prime certificates, geometric proof sources, and audit code", Zenodo 10.5281/zenodo.23304361 (concept 10.5281/zenodo.23304360), created 2026-10-11, updated 2026-10-12, one version** [src: README, `paper.tex`, `main_*.tex`, `constants.tex`] |
| **17** | **16** | **claim (cert.), conditional on 16** | **W. Toner, "Seventeen Lonely Runners, Assuming Sixteen", Zenodo 10.5281/zenodo.23552885, v1, 2026-10-22** [full PDF text] |
| 18 | 17 | **open: no claim located** | — |

Neither ProofAtlas nor the munim repository knows about the 16- and 17-runner
claims:

- ProofAtlas's list still says "Open", with Hu–Jing as the latest update. Its workspace was last sourced on 14 Aug 2026 and covers only up to 13 runners.
- The munim README says no 16-runner preprint existed as of 24 Nov 2026, apparently checking arXiv only.

#### Allikvere, *Sixteen lonely runners* (claim for LRC(15))

Read from `paper.tex` and its inputs (43 pp. with appendices). Structure of the proof:

1. **Product bound.**
   - Statement: $\log \prod v_i < \mathbf{459.084}$ for a primitive counterexample with distinct coordinates.
   - Earlier bounds, for comparison: the flag bound of arXiv:2609.02604 gives 497.030 by his shape estimate (ours, with the proved $r_{15} = 49/100$, is 496.727), and MSS gives 964.753.
   - New ingredient: "odd ternary relations" $h \in \{-1,0,1\}^{15}$ with $h\cdot v = 0$ and odd support. Let $O$ be their span.
     - A **signed relation inequality** (a Riesz product as in Bedert, arXiv:2511.16636, Lemma 4.1) holds: $\sum_{h\in T(O)} (-1)^{s(h)+1} w_\delta(s(h)) > \delta$, with $w_\delta(s) = (\delta+s)/2^{s-1}$ and $\delta = 1/(1-\cos(\pi/8)) - 8 \approx 5.137$.
     - This forces $\dim O \ge 4$ (Lemma "low odd rank").
   - The relation lattice $T$ then cuts the projected lattice $\Lambda$ down to a section $\Gamma$ of rank $14 - r$. The proof has three parts:
     - Lemma "analytic section": $(\det_E \Lambda)^2 = (\det_E \Gamma)^2/\det(AQA^{\top})$.
     - The flag prefix inequalities are applied on $\Gamma$ (Giri–Kravitz Lemma 3.3 on the torus cut out by the relations).
     - A gain $\gamma$ comes from points far from the coordinate hyperplanes inside $\ker A$ ("analytic center" lemma), pooled by a weighted pool-adjacent-violators step.
   - A finite classification of the relation spaces covers ranks 4–8. It has 2,088 hash-pinned inputs, rational-cell subdivision certificates, and Schur-complement shape constants $C_r$.
   - **Rank five is binding**: $J_* = 4355451813888/29029584727 > 150$. The final bound is $\prod v \le \bigl(61/(1875\sqrt{K_{15} J_*})\bigr)^{15}$.
2. **Divisibility.**
   - Forced divisor: $720720 = \operatorname{lcm}(2,\ldots,16)$.
   - Sixteen preliminary primes $Q_0 = \{29, 31, 191, 211, 223, 233, 239, 241, 251, 257, 263, 271, 277, 283, 293, 307\}$, closed as follows:
     - $J(15,p) = \emptyset$ at 239, 271, 283, 293 and 307;
     - divisibility only, through a new **weighted shift lemma** with $d = 4$ plus exact level-8 checks, at 191, 211, 223, 233, 241, 251, 257, 263 and 277;
     - single-orbit gates at 29 (level 32) and 31 (level 16).
   - Weighted shift lemma: $E = \{i : d \nmid u_i\}$, $g_i = \gcd(u_i, d)$. If $\lvert E\rvert \ge 2$ and $\sum_{i\in E} g_i\lceil d/(8g_i)\rceil < d$, then $u$ is lonely (assuming $\mathrm{LRC}(m)$, $m \le 13$). This generalizes the few-exception shift Lemma 3.12 of arXiv:2609.02604 to composite $d$.
   - Remaining requirement: $\sum \log p > 361.44573307$.
3. **Gates.**
   - $J(15,p) = \emptyset$ for the 59 primes $269 \le p \le 659$ except $\{271, 277, 283, 293, 307\}$, with $\sum \log p = 362.36191570$ and **margin 0.91618264**.
   - At every gate $\tau(p) \ge 14$, so the search has the two-branch form.
   - At every gate every family dies by binary level 16; the tight orbit $(1,\ldots,15)$ dies exactly at 16 (for example fibres 1, 2, 4, 0 at $p = 509$). No terminal search is needed.
   - Computing time: 5.6 CPU-years.
4. **His own caveat:** "The full computation has not been independently reimplemented or formally verified."

Our arithmetic check of the deposit's figures (exact sums, `math.log`) confirms that the margin is load-bearing:

- $\sum_P \log p = 362.36192$, $\sum_{Q_0} \log p = 84.1502$ and $\log 720720 = 13.4880$, for a total of 460.0001.
- That total exceeds 459.084 by only $0.916 < \log 29$, so **every** prime of $Q_0$ is needed.
- It falls **36.73 short** of our proved flag-only bound 496.727. So the claim depends essentially on the new relation-rank bound.
- With the flag-only bound one would need about 6 more gates, at 661, 673, 677, 683, 691 and 701. A $p^7$ cost model (heuristic) puts their cost at about $0.54\times$ the 59-gate campaign, i.e. about 3 CPU-years at his rate.

#### Toner, *Seventeen lonely runners, assuming sixteen* (claim for LRC(16))

Read from the PDF text (12 pp.). Main claims:

- Bound: $\log \prod v < 6972471659/12500000 = 557.7977$. The uniform part alone gives 577.08. The rank-4 and rank-5 classifications were redone for $n = 16$; rank five (five relations of support 7) is binding.
- Forced divisor: $\operatorname{lcm}(2,\ldots,17) = 12{,}252{,}240$.
- Gates: 91 primes, namely 149–251 (17 small primes), all of 257–317 and all of 331–719. $\sum \log p = 544.29$ against a requirement of 541.48, a margin of about 2.8.
- Method:
  - Covers are enumerated on H100 GPUs (about 2,000 GPU-hours) with a **faster canonical rule** (Appendix B, "orderly root rule"), reported 3–$5\times$ faster with the same output on four complete primes.
  - The tight orbit $(1,\ldots,16)$ is killed at level 17 by Sungkawichai–Trakulthongchai Prop. 4.4, since 17 is prime; below 257 it is killed at level $17\cdot 2^j$ (Lemma C.1, Prop. C.2).
  - Families with 14-, 13- or 12-class covers plus free speeds are closed by the weighted shift with $d = 4, 8, 16$.

Toner reports three things about $\mathrm{LRC}(15)$ itself:

- Running his pipeline for $k = 15$ on 31 of Allikvere's 59 campaign primes **reproduces Allikvere's certificates field by field**. The other 28 were not run.
- The GPU enumerator matches Allikvere's CPU program byte for byte on sampled jobs.
- AI assistance (Claude) was used for most code and drafts.

This is the only partial replication of $\mathrm{LRC}(15)$ located. It re-implements Allikvere's algorithm rather than being independent of it.

**Other Zenodo items on the finite cases** ([abs], unrefereed):

- Z. Liu, 10.5281/zenodo.22650872 (7 Sep 2026): the tight class $(1,\ldots,14)$ is proper at level 15 for every $p > 210$, by 85 SAT/RUP certificates.
- R. R. Raval, 10.5281/zenodo.22647790: $J(14,29) = \emptyset$ at level 15 (DRAT).
- X. Callens, 10.5281/zenodo.23726067 (28 Oct 2026): an independent reimplementation of the $k = 10$ sieve, which finds $J(10,p) = \emptyset$ for all 61 primes of $P_{10}$.
- V. Bonfioli, 10.5281/zenodo.24359604 (19 Nov 2026): Lean 4 kernel-checked proofs of 8 and 9 runners, with no `native_decide`.
- Lean formalization of $n \le 7$: Chen (see the erratum in the table above).

### 2.2 General bounds (all n)

| bound on $\mathrm{ML}(V)$, $\lvert V\rvert = n$ | status | source |
| --- | --- | --- |
| $1/(2n)$ | classical | union bound |
| $1/(2n) + c \log n/(n^2(\log\log n)^2)$ | refereed | Tao 2018 |
| $1/(2n) + n^{-5/3-o(1)}$ | preprint | Bedert, arXiv:2511.16636v1 (20 Nov 2025) [src, §1–3] |
| **$(1+c)/(2n)$** for an absolute $c > 0$ | preprint | **Hu–Jing, arXiv:2610.23790v1 (16 Oct 2026)** [src, structure]. They use the Green–Walker large-GCD argument plus a "dilation spillover inequality". The constants are explicit but not optimized, so no finite case follows. AI assistance is disclosed. |
| finite checking $\sum v_i \le \binom{n+1}{2}^{n-1}$ | refereed | MSS, arXiv:2411.06903v2, *Forum Math. Sigma* 13 (2025) e164 [src: the count $\lvert Z\cap\mathbb{Z}^{n-1}\rvert = \sum_S v_S$ (Cor. "lrc-points") and the Minkowski first-minimum step] |
| flag bound (product) | preprint | Allikvere, arXiv:2609.02604v2 §3; verified for $n = 15$ in the problem file (Approaches 10–11) |
| relation-rank bound (product) | claim | Allikvere, Zenodo 23304361 ($n = 15$); Toner ($n = 16$) |
| $\log\lVert v\rVert_2 \le (3/4)\, n \log n + O(n \log\log n)$, and $\ge n/2 - O(n/\log n)$ independent short relations | preprint (Zenodo, Lean v2) | Y. J. Peng, "The rank of short integer relations…", 10.5281/zenodo.24372259 (19 Nov 2026) [abs]. Asymptotically this beats MSS ($\approx 2n \log n$). |
| a relation $m\cdot v = 0$ with $\lVert m\rVert_1 \le \min\bigl(2k+3, (k+1)/(k-1)\cdot \mathrm{flt}(k)\bigr)$, $\sum m_i$ odd, $\lVert m\rVert_2 \le 2(k+1)/\sqrt{k-1}$ | preprint | **Beck–Everett, arXiv:2609.06259v3 (updated 24 Nov 2026)** [src §1–2] |

The Beck–Everett relation applies to every counterexample *or tight instance*.
For $k = 15$ it gives $\lVert m\rVert_1 \le 33$ and $\lVert m\rVert_2 \le 8.55$.

### 2.3 View obstruction, zonotopes and covering radii

- **Alon–Bucić–Davies, arXiv:2609.36220v1 (28 Sep 2026), preprint** [src §1, §7].
  - Theorem: if $a_1, \ldots, a_n \in \mathbb{R}^k$ have every $k$ of them linearly independent and $b \in \mathbb{R}^n$, then $\sup_x \min_i \lVert a_i\cdot x - b_i\rVert \ge k/(2n)$.
  - Consequences: this settles **Schoenberg's 1978 view-obstruction conjecture** ($\delta_{k,n} \ge k/n$) and the **Henze–Malikiosis covering-radius conjecture**: $\mu(Z) \le d/m$ for a lattice zonotope with $m$ generators in general position in $\mathbb{R}^d$.
  - **This does not touch LRC.** For $k = 1$ it is the trivial $1/(2n)$. In the LR-zonotope form ($n$ generators in $\mathbb{R}^{n-1}$, so $d = n-1$ and $m = n$) it gives covering radius $(n-1)/n$, whereas LRC is equivalent to covering radius $\le (n-1)/(n+1)$, which is strictly stronger.
  - The proof uses an equal-leverage (Barthe/Forster-type) rescaling. It is a high-dimensional analogue of the union bound.
- **Euclidean (sphere) view obstruction.** This is a different problem: balls, not cubes.
  - Kahlon, arXiv:2610.37711v2 (30 Oct 2026), preprint [src §3–4]: $D_6 = 107/312$ and $D_7 = 73/180$.
  - Tan–Zhang, arXiv:2611.10782v1 (7 Nov 2026), preprint [abs]: $\Delta_8 = 8/17$, $\Delta_9 = 1087/1980$ and $\Delta_{10} = 7/11$, with certificates at Zenodo 24037416.
  - Method: Banaszczyk transference along a KZ flag of $v^\perp \cap \mathbb{Z}^n$ gives a finite search tree over short orthogonal integer vectors, using an "offset lower bound" and a "fiber upper bound". It is close in spirit to Allikvere's flag bound and to Giri–Kravitz.
- **Shifted LRC.**
  - It is false from $n = 5$: Blanco–Criado–Santos, arXiv:2603.24784v4 (24 Oct 2026), accepted in *Rev. Mat. Complut.*, doi 10.1007/s13163-026-00609-0. The arXiv journal-ref field says "Discrete Comput. Geom. … Nov 2026"; the metadata is inconsistent.
  - Poliakova, arXiv:2609.23952v1 (preprint): the failure grows linearly, $E_n \ge \lfloor n/287\rfloor$, and $E_n \ge 1$ for $n \ge 95$.
  - X. Callens (Zenodo, Oct–Nov 2026, [abs]) gives explicit shifted counterexamples for $18 \le n \le 38$ and at $n = 63$.
  - The shifted LRC holds for 5 runners: Alcántara–Criado–Santos, arXiv:2506.13379v1, *Exp. Math.* (2026), doi 10.1080/10586458.2026.2651085 (refereed).
- **Older formulations** (refereed, survey-level): Henze–Malikiosis, *Aequationes Math.* 91 (2017); Beck–Hoşten–Schymura, *Integers* 19 (2019) A29 [src]; Beck–Schymura, *IMRN* 2024.

### 2.4 Wills / Cusick / Goddyn–Wong lines, spectra and special cases

- **Tight instances.**
  - Zhang, arXiv:2608.13599v3 (18 Oct 2026), preprint [abs] classifies tight one-entry modifications $([n-1] \setminus \{r\}) \cup \{w\}$. They are Goddyn–Wong type or the sporadic $\{1,3,4,7\}$ and $\{1,3,4,5,9\}$. The largest speed is $M(n) < 0.60\, n \log n + 52n$, and $\limsup M(n)/(n \log n) = 1/2$.
  - Two-entry census for $8 \le n \le 140$: only the Goddyn–Wong sets.
  - Bonfioli (Zenodo 24189338) studies leave-one-out values of Goddyn–Wong vectors.
- **Spectrum below $1/n$ (Kravitz's question).** This is the structure of near-tight tuples, not LRC itself.
  - Giri–Kravitz, arXiv:2304.01462v4: the accumulation points of $S(n)$ are $S(n-1)$.
  - Jain–Kravitz, arXiv:2411.12684v2.
  - Fan–Sun, EJC (doi 10.37236/13840).
  - Cordella, arXiv:2609.03444v2 (six speeds; odd denominators).
  - Yi–Gill–Bu, arXiv:2610.40694v1 (four speeds settled). Its general-$n$ theorem, assuming LRC for $n-1$ and $n-2$, is $\mathrm{ML}(V) > 1/n - (n(n-1))^{n-2}/(2\lVert V\rVert_2)$. Turned into an LRC bound it gives $\lVert V\rVert_2 < (n+1)n\cdot\kappa_n/2 \approx e^{74.3}$ for $n = 15$, **weaker than MSS** ($\sum v < 120^{14} \approx e^{67.0}$); the authors say so.
- **Special families** (survey: Perarnau–Serra, arXiv:2409.20160v3, preprint [src §8–9]). Each of these conditions implies the tuple is lonely:
  - some $d \le n+1$ divides no speed;
  - $v_n \le n v_1$;
  - $v_{n-1} \le (n-2)v_1$, or $v_{n-2} \le (n-2)v_1$ together with $v_{n-1} \ge n v_{n-2}$ (Beck–Hoşten–Schymura, arXiv:1606.01783v4, projection theorem `thm:mainProjection` (a), (b) [src]);
  - all but the largest speed odd (BHS);
  - $v_n \ge n v_{n-1}$, given $\mathrm{LRC}(n-1)$;
  - lacunary $v_{i+1} \ge 2v_i$ (Barajas–Serra 2009);
  - arithmetic progressions and their dense subsets (Pandey; length $\le 2n-3$);
  - $v_n < 1.2n$ (Tao);
  - $n < v_n \le 2n - c(\log n)^2$ for large $n$ (Bohman–Peng, Pomerance);
  - extra conditions in Bhardwaj–Narayanan–Venkataraman, arXiv:2211.08749v3;
  - **dense windows**: $\mathrm{ML} \ge 1/(m+1)$ for $m$ distinct speeds in $[1, 2m]$. Bonfioli, Zenodo 24189338 [abs], proves this when $2m+1$ is prime and Lean-verifies it for $2 \le m \le 126$. That answers Tao's "$2n$" question in this range, if correct.
- **Mixed thresholds:** Jensen, arXiv:2605.27941v1, characterizes $\mathrm{MLPS}_2$ and gives Fourier formulas. No bearing on $\mathrm{LRC}(15)$.
- **Variants:** time-dependent velocities (Lee, arXiv:2607.16082v2) and function fields (Hu, arXiv:2608.18818v2; the Chow–Rimanić conjecture is disproved). Off-track.
- **ProofAtlas workspace:** a "rank-seven safe-box / Fourier transfer" route for the 13-speed case. It is unaudited and source-reported, and has been made moot by the $\mathrm{LRC}(13)$–$\mathrm{LRC}(15)$ claims.

### 2.5 Answers to the specific questions

1. **Has anyone claimed $\mathrm{LRC}(15)$ or more?**
   - Yes. Allikvere claims $\mathrm{LRC}(15)$, and Toner claims $\mathrm{LRC}(16)$ conditional on $\mathrm{LRC}(15)$.
   - Both are Zenodo preprints with certificates, unrefereed and not on arXiv.
   - No claim for $\mathrm{LRC}(17)$ was found.
2. **Best known general bounds.**
   - Lower bound: $(1+c)/(2n)$ (Hu–Jing, preprint). The best refereed bound is Tao's.
   - Finite checking: MSS (refereed). The sharper flag and relation-rank product bounds are specific to $n$ and are preprints.
   - Asymptotically, Peng's $(3/4)\, n \log n$ bound on $\log\lVert v\rVert$ (preprint).
3. **View obstruction / zonotopes.**
   - Schoenberg's view-obstruction conjecture and the Henze–Malikiosis general-position covering-radius conjecture are settled (Alon–Bucić–Davies, preprint). Both are union-bound-strength and do not imply anything for LRC.
   - The Euclidean view-obstruction constants are now known up to dimension 10 (preprints).
   - The shifted version is false from $n = 5$, and its failure grows linearly.
4. **Wills / Cusick / Goddyn–Wong lines.**
   - Tight one-entry modifications are classified (Zhang).
   - The four-speed spectrum is settled (Yi–Gill–Bu).
   - The six-speed spectrum has odd denominators (Cordella).
   - Beck–Everett: every counterexample or tight instance lies on one of finitely many short-relation hyperplanes.
5. **Special structures.**
   - Arithmetic progressions are done (Pandey); the dense-window case is claimed for $m \le 126$ (Bonfioli).
   - Speeds sharing a common divisor: all but one sharing a factor gives lonely (classical). All but two sharing a factor $\ge 3$ gives lonely: MSS Cor. "small-gcd" ($n \ge 7$, shifted form), and the Allikvere weighted shift in the unshifted form.

## 3. Ideas, ranked

The situation changed. $\mathrm{LRC}(15)$ is claimed, with certificates and a large new
analytic component, and only a same-algorithm partial replay exists. So the
ranking is by value to *this* project: first independent verification, then the
next open case.

1. **Independently re-check Allikvere's $\mathrm{LRC}(15)$ gate certificates.** Highest value; it reuses our tools.
   - Our `covergen.c` / `gatecheck.c` / `check_gate_full.py` stack already re-checked $\mathrm{LRC}(14)$ at 71/71 gates. Most of the 59 archives are 0.2–2 MB; the largest are 269 (33 MB), 281 (21 MB), 311 (17 MB), 337 (46 MB) and 353 (20 MB).
   - Rows, cascade and level-16 emptiness are cheap to re-check from data. Only level-one *completeness* is expensive: the 5.6 CPU-years are mostly generation, as at $k = 14$.
   - Toner's 31-prime replay uses Allikvere's algorithm. A replay with our own code is genuinely independent.
   - Also check the preliminary-prime packages ($Q_0$), which use new arguments: the weighted shift with $d = 4$, the composite-level checks, and the single-orbit gates 29 and 31.
2. **Audit the relation-rank product bound 459.084.** Highest mathematical risk.
   - It is the load-bearing new analytic step: without it the gate set is 36.7 nats short.
   - The margin over it is only 0.916 nats.
   - It is large: a Riesz-product inequality, a finite classification of odd relation spaces of ranks 4–8 with 2,088 inputs, rational-cell subdivisions, and Schur-shape constants $C_4, \ldots, C_8$.
   - Start with the uniform parts, which are proof-readable: the signed relation inequality, the section identity $(\det_E \Lambda)^2 = (\det_E \Gamma)^2/\det(AQA^{\top})$, the prefix inequalities on the section, the analytic-center gain, the pooled product lemma and the Schur-shape lemma. Then re-derive the rank-5 binding case, $J_*$ at rank 5.
   - Approach 11 of the problem file already verified the flag-bound skeleton this builds on.
3. **A relation-free route to $\mathrm{LRC}(15)$.**
   - Use our *proved* flag target and add the gates 661, 673, 677, 683, 691 and 701 ($\sum \log p$ then reaches $499.14 > 496.727$, with $Q_0$ and the 59 gates).
   - Estimated cost about 3 CPU-years at Allikvere's rate ($p^7$ model, heuristic), less with Toner's faster rule.
   - This would give an $\mathrm{LRC}(15)$ proof that avoids the 2,088-input classification. Cluster-scale, but a clean independent target.
4. **Toner's orderly-root canonical rule** (Toner, Appendix B, Lemma B.1).
   - A cover $S \ni 1$ is canonical if $(\rho(S), \text{sorted } S)$ is lexicographically least over $s^{-1}S$, $s \in S$, where $\rho$ is the index of the first root candidate in $S$. A node is cut if some $s^{-1}T$ contains an earlier root candidate.
   - Reported 3–$5\times$ faster than the lexicographic-minimum and private-time rules, with identical output on four complete primes.
   - Our generator gap to Allikvere is 2.2–$2.9\times$ (Approach 13), so this is the most concrete speed-up for idea 1.
   - It drops the private-time quota, so the proof of completeness changes; it must be validated against our current generator.
5. **Weighted shift lemma with composite $d$** (Allikvere 16; Toner Lemma C.3).
   - This makes small primes admissible as gates ($Q_0$ has 9 such primes).
   - Before finding the Zenodo record, this survey had independently proposed the $d \in \{2, 4, 8, 16\}$ generalization for $k = 15$. It is now in the literature. Implement it in `gatecheck.c` for re-checking $Q_0$.
   - Statement: $\lvert E\rvert \ge 2$ and $\sum_{i\in E} g_i\lceil d/(8g_i)\rceil < d$, assuming $\mathrm{LRC}(m)$ for $m \le 13$. Elementary; we read the proof and it is correct as stated: the open arc of length $1/8$ holds at most $\lceil d/(8g_i)\rceil$ of the $d/g_i$ grid points.
6. **For $\mathrm{LRC}(17)$ (the first open case): gate choice below 251.** Heuristic.
   - Toner's $k = 16$ gate set starts at 149. For $k = 15$, Allikvere used 191–307 as divisibility gates.
   - With the $p^7$ cost model, starting a gate list at 97 to 179 rather than 251 cuts the cost by 2–$6\times$. This is optimistic, because near-gcd gates have expensive cascades.
   - The polynomial kill of the tight orbit (Sungkawichai–Trakulthongchai Prop. 4.4) needs $k+1$ prime. For $\mathrm{LRC}(17)$, $k+1 = 18$ is composite, as at $k = 14$ ($15 = 3\cdot 5$), so a Liu-style SAT kill at level 18 (Zenodo 22650872 did level 15) or the composite weighted shift is needed.
   - The $\mathrm{LRC}(17)$ product bound would need the relation-rank classification redone for $n = 17$. Toner did $n = 16$, where rank 5 is still binding.
7. **Order constraints in the shape lemma.** Small but cheap. Heuristic float exploration: `scratchpad/lr-lit/scripts/shape_cd2.py`.
   - A counterexample must violate every elementary "lonely" condition: $v_{\max} > 15 v_{\min}$; $v_{\max} < 15 v_{\mathrm{second}}$ (given $\mathrm{LRC}(14)$); $v_{\mathrm{second}} > 13 v_{\min}$ (BHS Thm (a)); BHS (b); BNV Thm 1.
   - The unconstrained maximizer of $R_{15}$ has 14 equal coordinates at $u \approx 0.0725$. That shape meets the BHS (a) lonely condition ($v_{\mathrm{second}} \le 13 v_{\min}$), so it is not the shape of any counterexample.
   - Under these constraints, coordinate search finds $\sup R_{15} \approx 0.4473$, against 0.48796. That is a gain of about 1.3 nats in $\log \prod v$, roughly 0.2 of a top gate.
   - Not a proof (local search, floats). Whether the gain survives inside the relation-rank bound, whose Schur-shape constants $C_r$ also maximize over shapes, is untested.
8. **Prime-power divisors** (Rosenfeld, arXiv:2512.01912v2, Lemma "needOfCovering", which used 64, 81, 25, 121 and 169 for $k = 8$). Low priority.
   - Upgrading $16\to 32$, $9\to 27$, $5\to 25$, $7\to 49$, $11\to 121$ and $13\to 169$ in the forced divisor adds at most $\ln 30030 \approx 10.3$ nats.
   - Each upgrade needs a covering computation at modulus about $q\cdot c$, comparable to a gate, for 0.7–2.6 nats each.
9. **Short-relation structure as a sieve filter** (Beck–Everett; Bedert-type $\{0,\pm 1\}$ relations; Peng). Not useful mod $p$.
   - For $k = 15$ there are about $10^{13}$ candidate relations with $\lVert m\rVert_1 \le 33$, and still $3^{15}/2 \approx 7\cdot 10^{6}$ ternary ones, all far more than $p \approx 500$. Mod $p$ almost every residue class satisfies some relation, so the filter is vacuous at level one. This is a failed route, kept.
   - Their real use is inside the product bound, as Allikvere showed.
   - Check of the bare Bedert/Riesz argument at $n = 15$: on dissociated sets it gives only $\mathrm{ML} \ge \arccos(1 - 1/15)/(2\pi) \approx 0.0584 < 1/16$. So "no ternary relation implies lonely" does not follow at $n = 15$ from the crude bound. Allikvere's signed inequality is the refined form that does work.
10. **KZ-flag search trees over short relations** (Kahlon; Tan–Zhang). Low priority for LRC.
    - The sup-norm analogue (offset $\mathrm{ML}(T_U) \ge \ldots$ and fiber bounds) is the Giri–Kravitz / Yi–Gill–Bu density lemma.
    - As a search tree in dimension 14 it is far larger than the gate sieve. Interesting only for independent re-proofs of small $k$.

New routes for the full conjecture: none of the 2024–26 work gives a plausible
route.

- The analytic line (Tao → Bedert → Hu–Jing) is at $(1+c)/(2n)$, far from $1/(n+1)$.
- The zonotope line was settled only at union-bound strength (Alon–Bucić–Davies).
- The shifted analogue is false, so any proof must use the common starting point.
- The most structural general-$n$ facts are:
  - Peng's $\ge n/2 - O(n/\log n)$ independent short relations for every counterexample;
  - Beck–Everett's relation with odd coefficient sum;
  - Giri–Kravitz's reduction of near-tight tuples to lower-dimensional subtori.
- An induction that turns "many short relations" into "lies in a lower-dimensional critical subtorus" (the Yi–Gill–Bu effective Cordella reduction, but at the threshold $1/(n+1)$ instead of $1/n$) is the one idea with a visible shape. Nobody has the needed gap estimate.

## 4. Discrepancies and items to update in `problems/lonely-runner.md`

These are recommendations only; this survey did not edit that file.

- "Next open case: $\mathrm{LRC}(15)$" and the table row "16 | 15 | open" are now out of date. $\mathrm{LRC}(15)$ is claimed (Allikvere, Zenodo 23304361) and $\mathrm{LRC}(16)$ is conditionally claimed (Toner, Zenodo 23552885). The first case with no claim is $\mathrm{LRC}(17)$.
- The Hu–Jing entry can be upgraded from [abstract via MathWorld] to [read]. The arXiv v1 (16 Oct 2026) statement $\mathrm{ML}(V) > (1+c)/(2n)$ is confirmed in the source.
- His flag-only figure for $n = 15$ is 497.030, presumably with a looser shape constant; ours is 496.727 with the proved $r_{15} = 49/100$.
- The munim repository's statement "no 16-runner preprint" is wrong. Do not rely on it for status.
- Barajas–Serra (7 runners) has a reported gap with a Lean repair (Chen, Zenodo 22852990). This is not verified here; it is worth a line in "Known results".

## 5. Files

- Downloaded sources (data only) are in `/tmp/claude-0/-home-user-Math-Research/be776001-e76c-5b41-aa84-912e1d1444ca/scratchpad/lr-lit/dl/`, under `src/<arXiv id>/x/`.
- Allikvere 16 (README, SHA256SUMS, manuscript source) is in `zen/a16/` and Toner (PDF and text) in `zen/t17/`. The MD5 sums of the downloaded files match the Zenodo metadata.
- The heuristic shape scripts are `scratchpad/lr-lit/scripts/shape_cd2.py` and the gate-cost script is `scratchpad/lr-lit/scripts/gates.py`. Both use floats and are not proofs.
