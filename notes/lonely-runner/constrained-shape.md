# Lonely runner: shape bounds restricted to counterexample shapes (bound track, $n=17$)

Scope: the shape constants of the $n=17$ gate target (18 runners, LRC(17)). Both the flag shape factor $R_{17}$ (`bound.md` §3) and the Schur shape constants $C_r$ of the relation-rank bound (`bound.md` §5, `bound-rank4.md`) are suprema over *all* sorted shapes. A counterexample's shape must also violate every elementary "lonely" condition. Here those conditions are proved in a sharp form, and the suprema are re-proved over the restricted region.

Background: `literature.md` §2.5 item 7 (a float search at $n=15$).

Labels follow `README.md`: **proved**, **machine-checked (exact)**, **heuristic**, **failed**.

Code: `computations/lonely-runner/bound/constrained/`.
- `constrained_shape.py`: sweep lemmas, the 1-D bounds, and the branch-and-bound.
- `assemble.py`: the targets.
- `test_constrained.py`: tests, including the negative controls.

## 0. Summary

| item | old | new | label |
| --- | --- | --- | --- |
| flag shape radius $r_{17}$ | $951/2000$ (all shapes) | $\mathbf{433/1000}$ on counterexample shapes | **proved** (§3–4), given LRC(16) |
| Schur constant $C_5$ (binding rank) | $3.0098$ | $\mathbf{2.855}$ | **proved** (§3–4), given LRC(16) |
| Schur constants $C_4$, $C_6$ | $2.3710$, $3.8377$ | $2.243$, $3.652$ | **proved** (§3–4), given LRC(16); not needed for the target |
| **relation-rank target** (binding) | $647.534682$ | $\mathbf{647.085815}$ ($-0.4489$) | **proved**, same inputs as `bound-rank4.md` plus §2 |
| plain flag target / Lemma H + M target | $670.28173$ / $667.92857$ | $668.69003$ / $666.33687$ ($-1.5917$) | proved; not binding |
| gate set and level-one cost (`k17/gate_set.py`, heuristic cost) | 101 gates, 313–1021, about $6.8\cdot10^7$ CPU-h | **unchanged** | heuristic cost model |

**Why the gain is small.** The radius $r_n$ cancels from the relation-rank target, because each $J_r$ is proportional to $(2r_n)^2$. So the large flag gain (about 1.6 nats) does not reach the binding target. Only the $C_r$ do, and they fall by about 5%. The optimum needs just one small coordinate, $u_{17}\approx0.023$, and one coordinate raised, $u_2\approx0.38$. That is a cheap way to violate every elementary condition (§5).

## 1. Setting

- $n\ge5$, and $v\in\mathbb Z_{>0}^n$ is a counterexample to LRC($n$): no real $\tau$ has $\lVert\tau v_i\rVert\ge\theta:=\tfrac1{n+1}$ for all $i$.
- Assume LRC($m$) for $m<n$. Then the $v_i$ are pairwise distinct: with a repeated speed there are at most $n-1$ distinct speeds, and LRC for them gives a time at distance at least $\tfrac1n>\theta$.
- The shape is $u=v/\max v$, sorted $1=u_1>u_2>\dots>u_n>0$. Write $s=u_2$, $t=u_3$, $m=u_n$, $b=2\theta$ and $g=1-2\theta$.
- Loneliness is scale invariant, since $\tau\mapsto\tau/\max v$ maps witnesses to witnesses. So "$u$ is lonely" is well defined, and a counterexample shape is not lonely.

## 2. Sweep lemmas: elementary conditions a counterexample shape violates (proved)

The set $\{y:\lVert y\rVert\ge\theta\}=\bigcup_k[k+\theta,k+1-\theta]$ consists of closed good arcs of length $g$, separated by open gaps of length $b$.

**Lemma S (sweep).** Let $J=[\alpha,\beta]$ and $x>0$, and put $L=x(\beta-\alpha)$.
1. If $L\ge b$, then some $\tau\in J$ has $\lVert\tau x\rVert\ge\theta$.
2. If $L\ge b$, then $J$ contains a closed interval of length at least $P(L)/x$ on which $\lVert\tau x\rVert\ge\theta$ throughout, where
$$P(L)=\min\bigl(g,\tfrac12(L-b)\bigr).$$

*Proof.* Put $W=xJ$, a closed interval of length $L$.
- If $W$ contains a whole good arc, the claim holds with length $g\ge P(L)$.
- Otherwise $W$ meets at most one gap: between two gaps that both meet $W$ there is a whole good arc inside $W$. So $W$ is one gap piece (open, of length at most $b$) together with at most two closed good pieces at its ends. Their lengths add up to at least $L-b$, so one of them has length at least $(L-b)/2$.
- For (1): a closed interval of length at least $b$ is not contained in an open gap of length $b$. ∎

Each of the following conditions implies that $u$ is lonely, so a counterexample shape violates all of them.

| | condition | witness argument | relation to the literature |
| --- | --- | --- | --- |
| C1 | $m\ge\tfrac1n$ | $\tau=\theta/m$: $\theta\le\tau u_i\le\tau\le n\theta=1-\theta$ | the classical $v_{\max}\le n\,v_{\min}$ |
| L1 | $s\le\tfrac1n$ | LRC($n-1$) gives $\tau_0$ with $\lVert\tau_0u_i\rVert\ge\tfrac1n$ for $i\ge2$. The window $\lvert\tau-\tau_0\rvert\le(\tfrac1n-\theta)/s$ keeps $i\ge2$ at least $\theta$ from the integers. Its length is $2/(n(n+1)s)\ge b$; apply S(1) to $u_1=1$. | $v_n\ge n\,v_{n-1}$ (uses LRC($n-1$)) |
| C2 | $\ell_2:=\frac{1-\theta}{s}-\frac\theta m\ge b$ | On $I_2=[\theta/m,(1-\theta)/s]$ every $u_i$, $i\ge2$, satisfies $\theta\le\tau u_i\le1-\theta$. Apply S(1) to $u_1=1$. | sharp form of Beck–Hoşten–Schymura, arXiv:1606.01783v4 (*Integers* 19 (2019) A29), Thm `mainProjection` (a) |
| C3 | $\ell_3:=\frac{1-\theta}{t}-\frac\theta m\ge0$ and $P(s\ell_3)/s\ge b$ | On $I_3=[\theta/m,(1-\theta)/t]$ every $u_i$, $i\ge3$, is good. S(2) for $u_2$ gives a subinterval of length at least $P(s\ell_3)/s$ where $u_2$ is good too. Apply S(1) to $u_1=1$. | implies Bhardwaj–Narayanan–Venkataraman, arXiv:2211.08749v3, Thm 1, which implies BHS (b) |

*Comparison with the published forms* (source TeX read: arXiv e-prints 1606.01783v4 and 2211.08749v3; speeds $n_1\ge\dots\ge n_k$, $k=n$):
- **BHS (a)**: $n_2\le(k-2)n_k$ gives loneliness. In shape terms, C2 reads $n/s-1/m\ge2$, i.e. $s\le nm/(1+2m)$. Since $m<1/n$, this contains BHS (a) ($s\le(n-2)m$) and is strictly larger. BHS's proof replaces $u_1=1$ by $u_1\ge u_2$.
- **BNV Thm 1** ($k\ge4$): $n_2(k/n_3-1/n_k)\ge k+1$ gives loneliness. In shape terms this is $s\ell_3\ge1$. Then $P(s\ell_3)\ge g/2$, and $g/(2s)\ge b$ holds for $n\ge5$. So C3 contains BNV Thm 1.
- **BHS (b)**: $n_3\le(k-2)n_k$ and $n_2\ge kn_3$. These give $s\ell_3\ge2k/(k+1)\ge1$, so BHS (b) is contained in BNV Thm 1 and in C3.

Our proofs are self-contained, so the cited theorems are not inputs.

**Tests.** An exact loneliness oracle for integer speeds checks every good-set endpoint $(k\pm\theta)/v_i$.
- It confirms every C1, C2 and C3 certificate on 1,500 random 17-speed vectors.
- The tight instance $(1,\dots,17)$ ($\mathrm{ML}=\tfrac1{18}$ exactly) is the negative control. At a threshold slightly above $\tfrac1{18}$ the oracle rejects it, the true lemmas do not certify it, and a deliberately broken C2 (window $b$ replaced by $0$) does certify it, which the oracle refutes.

**Region.** Let $F$ be the set of $(s,t,m)$ with $1\ge s\ge t\ge m>0$ violating C1, L1, C2 and C3. Every counterexample has $(u_2,u_3,u_n)\in F$.

## 3. The restricted suprema: method (proved)

**Functionals** (`bound/flag_n.py`, `bound/relrank_n.py`). With $q=1+2u-u^2$, $w=u^2/q$ and $a=q/u^{2/n}$:
- $R_n(u)^2=n^2/H(u)$, where $H=\bigl(\sum_iw(u_i)\bigr)\prod_ia(u_i)$.
- $\Phi_r(u)=4n^2(\prod u)^{2/n}/\bigl((\sum u^2)\prod_{i\ge r+2}q(u_i)\bigr)$.

**Where they enter.**
- The flag bound uses $R_n(u)<r_n$ at the counterexample's own shape (Allikvere, arXiv:2609.02604v2, Lemma 3.7).
- The relation-rank bound uses Allikvere's Lemma `schur-shape` ("Sixteen lonely runners", Zenodo 10.5281/zenodo.23304361, `main_geometry.tex`; source read, SHA-256 of `proof_sources.zip` equal to the record's): $(2R)^2\det(AQA^T)/\det(AA^T)\le\Phi_r(u)$ *at the counterexample's normalized speeds*, sorted as above, with $C_r\ge\Phi_r(u)$.

So both may be replaced by suprema over $\{u:(u_2,u_3,u_n)\in F\}$, which we write $R^F_n$ and $C^F_r$.

**$\lambda$-separation.** For $A>0$, $\ln A=\min_{\lambda>0}(\lambda A-1-\ln\lambda)$, attained at $\lambda=1/A$.
- $\Phi_r$: $A=\sum u^2\in[1,n]$, so $\lambda\in[1/n,1]$ and
$$\ln\Phi_r(u)=\max_\lambda\Bigl[\ln4n^2+1+\ln\lambda-\lambda+\sum_{i=2}^{r+1}h_1(u_i)+\sum_{i\ge r+2}h_2(u_i)\Bigr],$$
with $h_1=\tfrac2n\ln x-\lambda x^2$ and $h_2=h_1-\ln q$.
- $R_n$: $A=\sum w\in(\tfrac12,\tfrac n2]$, so $\lambda\in[2/n,2]$ and
$$\ln H(u)=\min_\lambda\Bigl[-1-\ln\lambda+\sum_i\big(\lambda w(u_i)+\ln q(u_i)-\tfrac2n\ln u_i\big)\Bigr].$$

**Relaxation.** Every coordinate other than $1,s,t,m$ is replaced by its one-variable optimum.
- For $\Phi_r$: the top-group coordinates are taken over $(0,t]$ and the low-group ones over $(0,1]$.
- For $R_n$: all of them are taken over $(0,1]$.

Dropping the order constraints only enlarges the domain. What remains is a 4-dimensional problem in $(\lambda,s,t,m)$.

**One-variable optima** (`M1`, `M2`, `Mg`).
- $h_1$ is concave, and its maximum is in closed form.
- Put $x_c=35007/250000$, so $x_c^2<1/(3n)$. On $(0,x_c]$:
  - $h_2''\le-2/(nx^2)+6<0$, since $(2q+q'^2)/q^2\le6$;
  - $g_\lambda''\ge-6+2/(nx^2)>0$, using $w''q^3=2(1+3x^2+2x^3)>0$ (exact identity, tested).
- So one tangent line at a float-located stationary point bounds each optimum rigorously on $(0,x_c]$. On $[x_c,1]$ the bound uses monotone cell bounds.

**Branch-and-bound** (`branch_and_bound`).
- *Boxes.* The domain of $(\lambda,s,t,m)$ is split into boxes by bisection.
- *Excluding a box.* A box is closed if one of C1, L1, C2, C3 holds at its worst corner, which is then a certificate for the whole box. The worst corners follow from monotonicity: $\ell_2$ decreases in $s$ and increases in $m$; $\ell_3$ decreases in $t$ and increases in $m$; and $P(s\ell_3)/s=\min(g/s,(\ell_3-b/s)/2)$.
- *Closing a box by the bound.* Otherwise each separable term is bounded at its worst corner ($w$, $q$ and $\ln$ are increasing on $[0,1]$), and the box is closed if the sum beats the target.
- *Rigour.* Logarithms are enclosed with `mpmath` interval arithmetic and rounded outward to $2^{-80}$. All other arithmetic is exact `Fraction`s. A box that fails both tests is split along its widest scaled side.

## 4. Results at $n=17$

| claim | float sup (heuristic) | boxes | label |
| --- | --- | --- | --- |
| $R^F_{17}<433/1000$ | $0.43280$ | 2,153,673 (169 s) | **proved** |
| $C^F_5\le2855/1000$ | $2.85392$ | 13,538,511 (946 s); $C^F_5\le286/100$ takes 1,542,375 | **proved** |
| $C^F_4\le2243/1000$ | $2.24177$ | 7,551,687 (517 s) | **proved** |
| $C^F_6\le3652/1000$ | $3.65013$ | 11,286,767 (817 s) | **proved** |

Every box was closed; the smallest closing margin in $\ln$ is about $10^{-11}$–$10^{-10}$, above the $2^{-80}$ rounding. Times are on one core of this container.

**Targets** (`assemble.py`, exact; logarithms to 50 digits).
- *Relation-rank assembly.* The regression with no overrides reproduces $647.534682$. With $C_5\to2855/1000$, $J_5$ rises from $14.52865$ to $15.31650$. That is still below $J_4=16.38535$, so rank 5 still binds, and the target becomes
$$670.281725-\tfrac{17}2\ln J_5=\mathbf{647.085815}.$$
- *$C_4$ and $C_6$.* Proving them changes nothing in the target, since $J_4$ and $J_6$ do not bind. They show that the cap from rank 4 now sits at $J_4=16.385\cdot2.37103/2.243=17.32$.
- *Flag targets.* These move by $17\ln(433/1000\cdot2000/951)=-1.5917$, to $668.69003$ (plain) and $666.33687$ (Lemma H + M). Neither binds.

**Gate set.** `k17/gate_set.py 17 647.085815` returns the same 101 gates (313–1021, $\sum\ln p=649.139$) as at $647.534682$. Removing any gate would need a target below about $642.2$ (dropping $1021$). So the level-one cost estimate, about $6.8\cdot10^7$ CPU-h with the current generator (heuristic cost model, `gates.md` §6), is unchanged.

**Label.** Proved, given LRC($m$) for $m\le16$ (needed for L1 and for distinct speeds) and the analytic inputs of `bound.md` §5 and `bound-rank4.md`. The finite inputs are exact.

## 5. Heuristic exploration and routes that did not help (kept)

Float searches (Nelder–Mead and Powell, 16–24 starts; heuristic) at $n=17$:

| constraints | $R_{17}$ | $\Phi_4$ | $\Phi_5$ | $\Phi_6$ |
| --- | --- | --- | --- | --- |
| none | $0.47544$ | $2.37103$ | $3.00979$ | $3.83761$ |
| C1, L1, BHS (a), BNV Thm 1 (published forms) | $0.43788$ | $2.25667$ | $2.87181$ | $3.67201$ |
| C1, L1, C2, C3 (sharp forms) | $0.43280$ | $2.24177$ | $2.85392$ | $3.65013$ |
| plus chains of every length and $\mathrm{LRC}(n-k)$ windows, $k\le4$ | $0.43219$ | $2.24176$ | $2.85387$ | — |

- **Longer sweep chains** carry the C3 argument down to $u_j$ for $j\ge4$. **$\mathrm{LRC}(n-k)$ windows** generalise L1 to the top $k$ runners. Both are valid lemmas of the same kind. At the optimum only C2 and C3 are active (and C4 for $R$), and the extra gain is below $0.002$ in $\Phi_5$. They are not used in the proofs.
- **$n=15$.** The same searches give $R_{15}$: $0.48796$ unconstrained, $0.44819$ with the published conditions, and $0.42938$ with the chains. The survey reported $0.4473$ for the published conditions. Ours is a little higher, presumably from local optimisation (heuristic either way).
- **Shape of the optimum.** In every case the optimum is clustered. It has a top group near $0.30$, a low group near $0.068$, and the two coordinates the constraints force: one tiny $u_n$ and a raised $u_2$. Elementary conditions involve only a few extreme coordinates, so they cannot touch the clusters.
- **A route that could do more (idea, not tried).** Certify loneliness on whole cells of shape space, using a finite good-set computation with $\tau$ up to some $T$. A cluster of near-equal speeds acts like one runner for small $\tau$, so clustered shapes are lonely with margin. The obstacle is dimension: the certificate depends on the occupancy pattern of the cells, and the number of patterns is exponential. This is recorded as a possible lever, not a result.
