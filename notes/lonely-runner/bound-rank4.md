# Lonely runner: rank-4 complete-section classification at $n=17$ (bound track)


Scope: the relation-rank bound of `bound.md` §5 for LRC(17) (18 runners), with the coarse rank-4 determinant bound replaced by a complete classification of the admissible rank-4 odd relation spaces. The method follows Allikvere, "Sixteen lonely runners" (Zenodo 10.5281/zenodo.23304361), §"rank-four classification" and App. B. Everything here is our own code. None of his code was run; his `proof_sources.zip` was read as data only.

Code is in `computations/lonely-runner/bound/rank4/`, and the tests are in `computations/lonely-runner/bound/test_bound.py` (the `rank4` block).

Labels follow `README.md`.

## 0. Summary

| item | value | label |
| --- | --- | --- |
| rank-4 sections admitted at $n=17$ (49 greedy profiles) | 34 row-sign orbit representatives (272 multiplicity vectors), 5 classes, all of support $a=6$ | computed (exact), complete enumeration |
| classified determinant | $g\le133$, attained at $a=6$; every support $a\ne6$ admits no section | computed (exact) |
| $J_4$ (classified) | $16.38535$ (coarse value: $3.48680$) | proved, given the inputs of `bound.md` §5 |
| $\min_r J(r)$ | $J_5=14.52865$ (coarse rank 5); rank 4 is no longer the bottleneck | proved (same inputs) |
| **new $n=17$ target** | $670.281725-\tfrac{17}{2}\ln J_5=\mathbf{647.534682}$ ($-12.1307$ against $659.665353$) | **proved**, given LRC($m$) for $m\le16$ and the general lemmas as read in `bound.md` §4–5 |
| validation at $n=15$ | the $g\ge168$ classes equal Allikvere's 16 classes (profiles, Grams, and the classes themselves); rank-3 table reproduced exactly | machine-checked against his data |

## 1. The finite problem

Let $v$ be a primitive counterexample to LRC(17). Its speeds are positive and pairwise distinct, because LRC(16) holds.

- Let $O$ be the span of its odd ternary relations, and assume $\dim O=4$. Ranks $1$–$3$ are excluded in `bound.md` §5.
- Choose odd relations greedily by increasing support, keeping each one that is independent of those already chosen. This gives a basis $h_1,\dots,h_4$ with supports $s_1\le\dots\le s_4$.
- Let $H$ be the $4\times17$ matrix with these rows.

Up to column signs, which preserve every support, $H$ is a multiplicity vector $m$ over the $40$ projective nonzero types of $\{-1,0,1\}^4$, plus zero columns. Its row supports are exactly $s$, and $\sum m\le17$.

The complete ternary section is
$$\mathcal T(O)=\{\lambda\in\mathbb Q^4\setminus0:\ \lambda\cdot c\in\{-1,0,1\}\ \text{for every present type }c\}/\pm.$$
The support of $\lambda$ is $\sum_{c:\lambda\cdot c\ne0}m_c$. Every member of $\mathcal T(O)$ is a relation of $v$.

**Necessary conditions**, each valid for the actual $H$ of a counterexample:

1. **Rank.** The present types span $\mathbb Q^4$.
2. **No short line.** There is no line of support $1$ (that would force $v_l=0$) or $2$ (that would force $v_i=v_j$).
3. **Signed Riesz** (`bound.md` §5, Lemma `signed-relations` for general $n$):
$$S_O(\delta)=\sum_{\text{odd}}\frac{\delta+s}{2^{s-1}}-\sum_{\text{even}}\frac{\delta+s}{2^{s-1}}>\delta,\qquad \delta=\delta_{17}=\frac1{1-\cos(\pi/9)}-9\in\Bigl(\tfrac{3790859}{500000},\tfrac{7581719}{1000000}\Bigr).$$
   - $S_O(\delta)-\delta$ is affine in $\delta$.
   - A section is *excluded* only if this quantity is $<0$ at both endpoints.
4. **Greedy consistency.** The greedy support sequence of the odd lines of $\mathcal T(O)$ equals $s$.
   - Greedy selection on a matroid gives a well-defined sequence of supports.
   - The actual space appears under its own greedy profile.

A rank-4 counterexample with support $a=\lvert\operatorname{supp}O\rvert$ and saturated Gram determinant $g=\det(HH^T)/\iota^2$ satisfies all four conditions. Here $\iota$ is the gcd of the $4\times4$ minors.

The profile $s$ must also survive the greedy bound, since the positive odd weight is at least $S_O>\delta$. Exactly $49$ profiles survive at $n=17$ (`relrank_n.survivors`). Without symmetry reduction there are $1.36\cdot10^8$ multiplicity vectors in all (counted by a DP in scratch).

## 2. The enumerator (`rank4/sect.c`)

**Global candidate set.** Each section element is $\lambda=M^{-1}x$, where $M$ is an invertible set of $4$ present types and $x$ is ternary.

- So it lies in the finite set $\Lambda$ of all $M^{-1}x$, taken over all $4$-subsets of the $40$ types. $\lvert\Lambda\rvert=68260$ up to sign.
- For each $\lambda\in\Lambda$ we precompute the masks of types on which it is ternary and on which it is nonzero.

**Search.** A DFS over the types assigns the multiplicities $m_c$.

- When a type becomes present, every $\lambda$ that is not ternary on it is dropped, and the partial supports grow.
- At a leaf, the surviving list is exactly $\mathcal T(O)$.
- Conditions 1–4 are tested with integer arithmetic. The Riesz test multiplies through by $2^{n-1}\cdot10^6$ and uses 128-bit integers.

**Rigorous pruning.** Along the DFS, lines only disappear and supports only grow. In a greedy-consistent section every odd line has support $\ge s_1$. So
$$S_O\le\sum_{\lambda\ \text{surviving}}w\bigl(\text{odd ceiling of }\max(s_1,\text{partial support})\bigr).$$
If this bound minus $\delta$ is $<0$ at both endpoints, the subtree is cut.

**Symmetry.** The quotient is by the row-sign group $\{\pm1\}^4/\pm1$, of order $8$. It maps each type to one with the same support pattern.

- Types are ordered in pattern blocks.
- The lexicographically least representative of each orbit is selected block by block.
- The orbit size $8/\lvert\mathrm{Stab}\rvert$ is recorded. Orbit-weighted counts reproduce the raw counts exactly (§3).
- The section, $a$, $g$ and the greedy profile are invariant under the action, because the row space is unchanged.

Admitted records (`ADM` lines) carry $a$, $g$, $\iota$, the raw determinant, $(A,B)$ with $2^{n-1}S_O=A\delta+B$, the orbit size and $m$.

**Independent checks** (`rank4/crosscheck.py`, `rank4/pyenum.py`): pure Python with exact `Fraction`s, sharing no code with `sect.c`.

- *Every admitted record.* The section is rebuilt by Cramer solves from one invertible set of present columns (`rank_exclusion.section`). The rank, the short-line test, Riesz, the greedy sequence, $a$, $\iota$ (gcd of *all* maximal minors) and $g$ are recomputed and compared.
- *Full enumeration of one profile.* For $(3,3,3,3)$ at $n=17$, the full Python enumeration (no pruning, no symmetry, 34,702 vectors) admits exactly the $224$ vectors of the orbit-expanded C output.

## 3. Validation

**Rank 3, $n=15$.** This uses `sect.c` with $R=3$, no greedy filter and no pruning, which is the domain of Allikvere's table.

- All nine multiplicity counts ($354,545,561,561,554,449,112,1353,4378$) are reproduced.
- All nine exact maxima are reproduced: $(5\delta+14)/8,\dots,(7\delta+27)/16$.
- Orbit-weighted counts equal the raw counts.
- Test: `test_sect_rank3_reproduces_allikvere_table`.

**Rank 4, $n=15$: high Gram.** Allikvere reports 72 sections with $g\ge168$, forming 16 classes under row signs and profile-preserving row permutations. His file `lrc15/N15_RANK4_SHAPE_CLASSES_CHECK.json` has SHA-256 `e9a2c7d1…dcd56`, equal to the pin in his `rank4_complete/CHECK.json`.

- Our census gives exactly 16 classes with $g\ge168$.
- One is $(3,3,3,7)$ with $g=168$. Fifteen are $(3,3,5,5)$ with $g\in\{169,171,174,174,181,186,187,189,195,196,201,210,216,225,225\}$.
- Supports are $6$, $7$ and $8$.
- Mapping his 16 matrices into our canonical class keys gives *the same 16 classes*. Test: `test_sect_n15_high_gram_classes_match_allikvere`.
- His "72" counts records after a partial quotient in his census, so it is not comparable to our raw counts: we have 336 multiplicity vectors with $g\ge168$.

**Rank 4, $n=15$: support seven.** The Grams $>43$ of our admitted support-7 sections are exactly the values in his support-seven table:
$$\{52,69,76,80,82,84,108,111,112,118,126,135,136,148,166,171,186,187,189,201,216\}.$$
His table comes from a separate two-triple reduction. The value $148$ occurs in two classes, matching his "two spaces". Test: `test_sect_n15_support7_grams_match_allikvere_table`.

The full $n=15$ census is in §5.

## 4. Result at $n=17$

The census covers all 49 profiles, in about 3 min of one core.

| profile | admitted orbit reps (raw vectors) | classes: $(g,a)$ |
| --- | --- | --- |
| $(3,3,3,3)$ | 28 (224) | $(48,6)$, $(48,6)$, $(55,6)$ |
| $(3,3,5,5)$ | 6 (48) | $(133,6)$, $(133,6)$ |
| other 47 profiles | 0 | — |

The two $(48,6)$ classes, and likewise the two $(133,6)$ classes, have identical line-support multisets. They may coincide under a basis change; we did not quotient further.

A representative of the worst class ($g=133$) has row-sign orbit size 8:
$$H=\begin{pmatrix}0&0&0&1&1&1\\1&0&0&0&1&-1\\-1&0&1&-1&1&-1\\0&1&-1&1&-1&-1\end{pmatrix}.$$
Its section has line supports $3,3,5,5,5$. Then $2^{16}S_O=45056\,\delta+159744$, so $S_O-\delta=0.0682$ at $\delta_{\rm lo}$, a narrow pass.

**Completeness checks at $n=17$.**
- *Pruning.* The same census rerun with pruning switched off (`NOPRUNE=1`) gives byte-identical admitted records for all 49 profiles.
- *Domain.* The no-pruning run's orbit-weighted leaf count is $135{,}937{,}974$. An independent exact DP count of all multiplicity vectors over the 49 profiles gives the same $135{,}937{,}974$. So the symmetry quotient covers the domain exactly.
- *Python enumeration.* The independent Python enumeration of $(3,3,3,3)$ agrees, as in §2.

**Bound** (`rank4/rank4_bound.py`, exact). The interface is unchanged from `relrank_n.py`. It uses
- $C_4\le2.37103$, from weighted AM–GM with interval arithmetic;
- $\tau_4=310063/1771470000$;
- the prefix gain $G(17,4,6)=1$.

So
$$J_4=\frac{(2r_{17})^2}{C_4\,\tau_4\,g_{\max}(6)}=\frac{4436628636852420383322038641424921035605540864}{270768051825261085847149708495982494648966925}\approx16.38535.$$
Supports $a\ne6$ admit no rank-4 section at all.

The coarse value was $J_4=3.48680$, which used $g\le5^4=625$ at $a=6$. So the classification cuts $g$ at the worst support from $625$ to $133$. With ranks $1$–$3$ excluded,
$$\min_rJ(r)=J(5)=14.52865\ (\text{coarse}),\qquad J(4)=16.385,\ J(6)=48.47,$$
$$\text{target}=670.281725-\tfrac{17}{2}\ln J_5=670.281725-22.747043=\mathbf{647.534682}.$$

**Label.** Proved, given LRC($m$) for $m\le16$ and the analytic inputs of `bound.md` §5. Those inputs are Allikvere's general lemmas, re-derived for general $n$ and checked by reading. The finite input is the complete census, which is exact and independently re-checked as in §2.

The heuristic estimate in `bound.md` §5 was "rank 4 excluded gives about $647.5$". We get the same number without excluding rank 4, because the classified $J_4$ already exceeds $J_5$.

**Negative controls** (`test_rank4_negative_controls`):
1. Feeding the coarse $g_{\max}(6)=625$ into the same script gives back $J_4=3.4868$, with rank 4 binding.
2. With the smaller $n=15$ value of $\delta$, the $(3,3,5,5)$ census at $n=17$ admits sections with $g>133$. So the Riesz test is load-bearing.
3. A record with $g$ altered by $1$ is rejected by the independent checker.

## 5. Full rank-4 census at $n=15$ (validation)

The census covers all 45 profiles, in about 3 min. Every admitted record passes the independent checker.

- **Size.** 326 orbit representatives (2,403 multiplicity vectors) in 71 row-sign/permutation classes. Anything is admitted only in the profiles $(3,3,3,3)$, $(3,3,3,5)$, $(3,3,3,7)$ and $(3,3,5,5)$.
- **$g_{\max}$ by support.** $a=5$: $100$; $a=6$: $225$; $a=7$: $216$; $a=8$: $225$; $a=9$: $135$. Supports $a\ge10$ admit nothing.
- **His claims, confirmed.** We confirm Allikvere's
  - $g\le225$;
  - the sections with $g\ge168$ have support at most $8$;
  - $a\ge9\Rightarrow g\le167$ (ours gives $\le135$).
- **Profile domain.** His high-Gram census was restricted to the 43 profiles with $\prod s_j\ge168$. Ours covers all 45.
- **Bound.** In our interface, which has no metric or quarter-point refinements, the classified $n=15$ factor is $J_4=10.276$, worst at $a=6$ with $g=225$. Then $\min_rJ(r)=J_4$ and the target is $465.765$.
  - This compares with $473.427$ (coarse) and Allikvere's $445.596$.
  - His additional gain is the metric work of `proof_rank4_geometry.tex`, which we did not redo.

## 6. What is still open, and the next levers

- **Rank 5 is now the bottleneck** ($J_5=14.53$, coarse).
  - Classifying rank 5 alone can gain at most $\tfrac{17}2\ln(16.385/14.529)=1.02$ before rank 4 binds again.
  - To go further, the rank-4 support-6 cases (5 classes, $g\le133$) need a metric argument, as in Allikvere's "support-five/six metric argument" ($W_{\rm eff}\le1223/50$ at $n=15$), or an exclusion.
  - After both, $J_6=48.47$ allows up to $\tfrac{17}2\ln48.47=33.0$ in total, a target near $637.3$.
  - The four support-6 rank-4 spaces are very special. Six speeds carry four independent relations, so they span a rank-2 group. This may allow a direct argument.
- **Rank-5 census: not attempted** (time).
  - There are $121$ column types and $198$ surviving profiles.
  - The global candidate set built from all $5$-subsets ($2\cdot10^8$) is too large to build naively. It should instead be generated per leaf, or from bases inside the present set.
  - The sign quotient is $16$.
- The classes were not quotiented beyond row signs and row permutations, which is harmless for the bound.

## 7. Reproduction, and routes that did not work

**Reproduction.** Run these from `computations/lonely-runner/bound/rank4/`:

- `gcc -O2 -DR=4 -o sect4 sect.c`
- `python3 run_census.py 17 4 OUT ./sect4 2`: one process per profile, under `nice`. All profiles together take about 3 min.
- `python3 rank4_bound.py 17 OUT`
- `python3 -m pytest test_bound.py` from `bound/`: 18 tests, about 5 min. The tests compile `sect.c` and rerun the full $n=17$ census.

**Implementation notes (kept so they are not retried).**

- *Python is too slow for the full census.* The exact-`Fraction` enumerator `pyenum.py` takes 257 s for the 34,702 vectors of $(3,3,3,3)$ alone. It is used only as a cross-check.
- *A naive C version was also slow.* The first C version took about $20\,\mu$s per leaf: it had no symmetry quotient and kept a per-node candidate list. The cost was in filtering the large candidate lists near the root. Three changes did not help: avoiding `malloc`, lazily stored supports, and precomputed feasibility tables.
- *What did help.* The row-sign quotient gave a factor of about $5$ in time.
- *The Riesz upper-bound prune is weak near the root.* Most of the $68260$ global candidates are still alive there. It cuts subtrees only once fewer than about $50$ candidates remain. It is still the main pruning for the large profiles, for example $5.4\cdot10^7$ cuts on $(5,7,7,7)$ at $n=15$.
- *Rank 5 needs a different candidate generator.* Building the global candidate set from all $5$-subsets of the $121$ types means $2\cdot10^8$ subsets times $3^5$, which is too many. A per-leaf Cramer section, as in `pyenum.py`, together with the 16-element sign quotient is the obvious next design.
