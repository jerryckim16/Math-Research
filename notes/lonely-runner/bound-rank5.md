# Lonely runner: rank-5 section census at $n=17$ and the cap on the bound track

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Scope: the relation-rank bound for LRC(17) (18 runners) after `bound-rank4.md` and `constrained-shape.md`. There, rank 5 binds with $J_5=15.317$. Here, the admissible rank-5 odd relation spaces of small support are classified completely, in the same way `bound-rank4.md` does rank 4. The note also records the cap that limits what the bound track alone can do.

Code: `computations/lonely-runner/bound/rank5/`. Tests: `test_rank5.py`. Labels follow `README.md`.

## 0. Summary

| item | value | label |
| --- | --- | --- |
| binding supports at rank 5 | only $a\le9$ matter. For $a\ge10$ the coarse $J_5(a)\ge30.28$ already exceeds every other cap (§1). | proved (exact) |
| census, $a\le9$ | 48 greedy profiles; 20,669 admitted orbit representatives in 10 profiles; $g_{\max}(a)=905,963,960,1021$ for $a=6,7,8,9$ | computed (exact), complete enumeration, checks in §3 |
| $J_5$ | $30.28$, now set by the coarse bound at $a=10$ (was $15.317$) | proved, same inputs as `bound-rank4.md` and `constrained-shape.md` |
| **new $n=17$ target** | rank 4 binds again ($J_4=17.321$): $670.281725-\tfrac{17}2\ln J_4=\mathbf{646.040584}$ ($-1.0452$ against $647.085815$) | **proved**, same assumptions |
| gate set (`k17/gate_set.py`) | unchanged: 101 gates, 313–1021 | heuristic cost model |
| **cap** | dropping a gate needs a target $\le642.2$, i.e. $J\ge27.21$ at every rank. Rank 4 is at $17.32$ and must improve by $1.57\times$. No rank-5 or rank-$\ge6$ work can help until it does. | proved (arithmetic) |

**Conclusion.** The bound track cannot remove a gate without a new idea that raises rank 4 by a factor of $1.57$. The rank-4 support-6 classes ($g\le133$, 5 classes, `bound-rank4.md` §4) need a metric argument or an exclusion. Rank 5 is now well clear of that threshold, except through the coarse bound at $a=10$ ($J=30.28>27.21$).

## 1. Caps and binding supports

Write $J(r)$ for the factor of rank $r$ in the relation-rank bound (`bound/relrank_n.py`). The target is $670.281725-\tfrac{17}2\ln\min_rJ(r)$. With the constrained Schur constants $C_4\le2.243$, $C_5\le2.855$ and $C_6\le3.652$ (`constrained-shape.md`):

| rank | $J$ before this note | note |
| --- | --- | --- |
| 4 | $17.321$ | classified, $g_{\max}(6)=133$ |
| 5 | $15.317$ | coarse, binding at $a=8$ |
| 6 | $50.931$ | coarse |
| $\ge7$ | $\ge215.9$ | coarse |

- **A rank-5 census alone** can lower the target only to the rank-4 cap: $(17/2)\ln(17.321/15.317)=1.045$, giving $646.04$.
- **Dropping a gate.** The 101 gates have $\sum\ln p=649.139$, and the cheapest removal is $1021$, which needs a target below $649.139-\ln1021=642.21$. That means $J\ge e^{(670.281725-642.21)/8.5}=27.21$ at every rank.

**Coarse $J_5(a)$ by support** (`rank5_bound.J5_by_support`, $C_5=2.855$):

| $a$ | 6 | 7 | 8 | 9 | 10 | 11 | 12 | $\ge13$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| coarse $g$ | 3125 | 4375 | 16807 | 21609 | 21609 | 21609 | 21609 | $\le44217$ |
| $J_5(a)$ | 30.65 | 21.89 | **15.32** | 19.15 | 30.28 | 46.77 | 70.95 | $\ge106.98$ |

Since the support $a$ equals $\sum m$, the number of nonzero columns, classifying $a\le9$ caps the multiplicity vectors at 9 columns. That collapses the domain.

**Domain sizes** (`count_domain.c`: exact DP over the 31 support patterns; a pattern with $j$ rows holds $2^{j-1}$ projective types):
- rank 4, all supports (validation): $135{,}937{,}974$, equal to `bound-rank4.md` §4;
- rank 5, all supports: $4.70\cdot10^{14}$ (198 profiles);
- rank 5, $a\le9$: $8.28\cdot10^{10}$ (48 profiles);
- rank 5, $a\le8$: $6.58\cdot10^{9}$.

## 2. The enumerator

`bound/rank4/sect.c` builds one global candidate list from every $R$-subset of the types. At $R=5$ that is $\binom{121}5\approx1.9\cdot10^8$ subsets, too many.

**`sectn.c`** (reference; generic $R$; support cap `AMAX`):
- Candidates are generated at the DFS node where the present types first reach rank $R$. With $c_1,\dots,c_R$ the first rank-raising types (the rows of $M$), every section element satisfies $M\lambda=x$ with $x$ ternary. So the section lies among the $(3^R-1)/2$ vectors $\operatorname{adj}(M)x/\det M$.
- These candidates are filtered by every present type and carried down the DFS, as in `sect.c`.
- The tests, the symmetry quotient (row signs, order $2^{R-1}$), the Riesz pruning and the output format are those of `sect.c`.

**`sectj.c`** (production) gives the same output, faster:
- *Jump DFS.* It jumps directly to the next nonzero type and applies the skipped block-end symmetry checks while scanning. Leaves are visited in the same order.
- *Generation.* The adjugate comes from one fraction-free Gauss–Jordan pass (Montante). The candidates are not reduced, because every later test is invariant under $(y,D)\mapsto(cy,cD)$. Only non-basis present types are re-checked.
- *Speed.* 14–22 µs per leaf against 115 µs for `sectn.c` (profiled).

## 3. Validation

| check | result |
| --- | --- |
| $R=4$, $n=17$: `sectn` and `sectj` against `rank4/sect.c` with pruning off | byte-identical output (all records and counters) on the profiles tested; with pruning on, identical ADM records (`test_rank5.py`) |
| $R=5$: `sectj` against `sectn` | identical ADM records on (3,3,3,3,3), (3,3,3,3,5) and (3,3,3,5,5) at $a\le9$ |
| $R=5$ domain | orbit-weighted leaf counts equal the DP counts exactly: (3,3,3,3,3) at $a\le6$ and $a\le9$; (3,3,3,3,5) and (3,3,3,5,5) at $a\le9$; with `NOSYM` the raw leaf count equals the DP count |
| pruning off, slice of the $n=17$ census: (3,7,7,9,9), (3,3,5,5,9), (5,5,7,9,9) and (3,3,5,5,7), chosen for heavy pruning and admitted records | ADM records byte-identical; orbit-weighted leaves equal the DP counts ($43{,}415{,}328$; $38{,}388{,}080$; $175{,}750{,}176$; $322{,}848{,}332$) |
| independent Python re-check of every admitted record (`rank4/crosscheck.py`, generic in $r$: Cramer-solved sections, Fraction minors) | all $20{,}669$ records pass (rank, no short line, Riesz, greedy sequence, $a$, $g$, index, $A$, $B$) |
| independent Python full enumeration (`pyenum5.py`; no pruning, no symmetry) against `sectj` with `NOSYM`, (3,3,3,3,3) at $a\le6$ | **not completed** (capped). Its domain generator reproduces the DP count $915{,}024$ at $a\le5$, and `admitted()` reproduces C records it was given. But the full $a\le6$ run (2.9 M vectors, 7,680 C records) did not finish in 2 h, and an unbalanced slice timed out. So Python-side completeness is not checked. Completeness rests on the C-vs-C checks above (`sectn`/`sectj`, `sect.c` at $R=4$) and on the DP domain counts. Every admitted record is still re-checked in Python. |
| $n=15$ against Allikvere's rank-5 bounds (`proof_rank5.tex`, Lemma `rank5-classification`; source read as data) | consistent: our census at $n=15$, $a\le8$ (21 profiles, 1,979 CPU-s, 196,892 admitted records) gives exact maxima within every bound he states on $g$ itself; see the table below |
| negative control: the $n=15$ $\delta$ enclosure used at $n=17$ changes the admitted set | passes (`test_rank5.py`) |

**$n=15$ comparison** ($a\le8$; his bounds are upper bounds, ours exact maxima):

| his statement | his bound | ours |
| --- | --- | --- |
| 33333, 33335, 33337 ($a\le7$; Hadamard) | $g\le243,405,567$ | $168,360,384$ |
| 33355 ($a\le7$) | $g\le648$ | $630$ |
| 33357 ($a\le7$, in the proof text) | $g\le873$ | $783$ |
| 55557 ($a\le7$) | excluded | none admitted |
| support $a=8$ | $g\le1800$ | $1530$ |

His rows for 33555, 35555 and 55555 bound $g/\gamma$, not $g$, and his own case analysis there treats $g>760$ (19,296 admissible cases for 33555). So our larger $g$ in those profiles ($1035$, $1106$ and $819$ at $a=7$) are not in conflict. Profile 35557 has no admitted section at $a\le8$ in our census.

## 4. Result at $n=17$

The census covers all 48 greedy-surviving profiles with $s_5\le9$, in 16,674 CPU-s. Records are admitted in 10 profiles only:

| profile | admitted orbit reps |
| --- | --- |
| (3,3,3,3,3) | 4,670 |
| (3,3,3,3,5) | 4,704 |
| (3,3,3,5,5) | 3,570 |
| (3,3,5,5,5) | 4,359 |
| (3,3,3,3,7) | 2,088 |
| (3,3,5,5,7) | 534 |
| (3,5,5,5,5) | 528 |
| (3,3,3,3,9) | 168 |
| (3,3,5,5,9) | 36 |
| (3,3,3,5,7) | 12 |

The other 38 profiles admit nothing.

| $a$ | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- |
| $g_{\max}(a)$ (census) | 905 | 963 | 960 | 1021 |
| coarse $g$ | 3125 | 4375 | 16807 | 21609 |
| $J_5(a)$ | 105.83 | 99.46 | 268.15 | 405.31 |

With $J_5(a)$ for $a\ge10$ kept coarse, $J(5)=\max(1,\min_aJ_5(a),J_{\rm select})=30.28$ (at $a=10$). Then $\min_rJ(r)=J(4)=17.3206$, and
$$\text{target}=670.281725-\tfrac{17}2\ln17.3206=\mathbf{646.040584}.$$
`k17/gate_set.py 17 646.040584` returns the same 101 gates.

**Label.** Proved, given LRC($m$) for $m\le16$ and the analytic inputs of `bound.md` §5 (Allikvere's general lemmas, re-derived and checked by reading), `bound-rank4.md` and `constrained-shape.md`. The finite input is the complete census, which is exact.

## 5. Notes, partial data and routes not taken

- The partial sample from the feasibility stage, shard 0 of 100 per profile, gave $g$ up to $456$ at $a=8$. That was partial; the complete value is $960$.
- No row-permutation quotient beyond row signs was applied. That is harmless for $g_{\max}$.
- **The next lever is rank 4**, which needs $1.57\times$. Allikvere's rank-4 metric work (`proof_rank4_geometry.tex`, $W_{\rm eff}\le1223/50$ at $n=15$) is the model. At $n=17$ the five support-6 classes are very special: six speeds carry four independent relations, so they span a rank-2 group (`bound-rank4.md` §6). That may allow a direct exclusion.
- **Raising rank 5 past $30.28$** needs $a=10$ classified. The domain for $a\le10$ is larger (not counted here), and it is not needed until rank 4 exceeds $30.28$.
