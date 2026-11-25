# Lonely runner: sharper product bounds for the gate target (bound track)

Scope: the analytic bound that turns "a counterexample to LRC($n$) is divisible by every gate prime" into a finite gate target. This file covers:

- $n=15$, 16 runners, the original track;
- $n=17$, 18 runners, the current main target;
- an audit of Allikvere's $459.084$ bound for $n=15$.

Labels follow `README.md`: **proved**, **machine-checked (exact)**, **heuristic**, **failed**.

Scripts are in `computations/lonely-runner/bound/` and tests are in `test_bound.py`.

## 0. Summary

| item | $n=15$ | $n=17$ | label |
| --- | --- | --- | --- |
| plain flag target $\ln(\text{bound})-\ln\operatorname{lcm}(2..n+1)$ | $483.23877$ | $670.28173$ | proved, given LRC($m$), $m<n$ (§3, `flag_n.py`) |
| shape radius used | $r_{15}=49/100$ | $r_{17}=951/2000$ | proved (§3) |
| **Lemma H** (hyperplane prefix) + **Lemma M** (block minimisation) | $481.12260$ ($-2.1162$) | $667.92857$ ($-2.3532$) | **proved** (§2, `hyperplane.py`) |
| 2-D CVP refinement of the rounding step | about $-0.12$ more | not run | heuristic (§6) |
| Allikvere's relation-rank bound | $459.084$ (his value) | not available | audit, §4: assembly, rank 3, ranks 6–8 and the general lemmas reproduced; ranks 4–5 classification **not** re-done |
| coarse relation-rank bound (his general lemmas, our code, no fine classification) | no gain while rank 2 is not excluded | in progress | §5 |

## 1. Leverage: where the target is sensitive

Write $B_r=\bigl(2r/((n+1)(n+1-r))\bigr)^2$ and $c_i=B_i-B_{i-1}$. The flag bound is $\ln\prod v_i < n\bigl(-\tfrac12\ln K_n+\ln r_n-\ln n\bigr)$ with $K_n=\prod_{i<n} c_i$.

**Shape factor (route a).** At $n=15$, the target changes by $15\ln(r/r')$. That is $0.309$ per $0.01$ of $r_{15}$ near $0.49$. The true minimum of the shape factor is $R_{15}\approx0.487960$ (from $H_{\min}\approx944.961$). So route (a) can gain at most $15\ln(0.49/0.48796)=0.0624$ (heuristic numeric minimum). That is less than $1\%$ of one top gate ($\ln 743=6.61$), so this route is not worth pursuing.

**Prefix constants (route b).** At $n=15$, $\partial(\text{target})/\partial\ln B_r$ ranges from $-4.9$ ($r=2$) to $-12.2$ ($r=14$), computed by finite differences in scratch. A $1\%$ gain in one $B_r$ is worth $0.05$–$0.12$ units, and a $1\%$ gain in all of them about $1.05$ units. This is the lever used in §2, and also by Allikvere (§4).

## 2. Lemma H (hyperplane prefix) and Lemma M (block minimisation): proved

**Setting.** This is the flag argument of Allikvere, arXiv:2609.02604v2, §3, verified in `problems/lonely-runner.md`, Approach 11.

- $n\ge3$, and $v\in\mathbb Z^n_{>0}$ is a primitive counterexample to LRC($n$): every real $\tau$ has some $i$ with $\lVert\tau v_i\rVert<1/(n+1)$.
- $u=v/\max v$, $q_l=1+2u_l-u_l^2$, $Q=\operatorname{diag}(q)$.
- $H=v^\perp$, $P$ is the orthogonal projection onto $H$, and $\Lambda=P\mathbb Z^n$ has rank $d=n-1$.
- $E=PQ^{1/2}B_2^n$, and $D=P[-1,1]^n$.
- $b_1,\dots,b_d$ is a Korkine–Zolotarev basis of $\Lambda$ in the $E$ metric. Its Gram–Schmidt vectors are $b_i^*$, with $t_i=\lVert b_i^*\rVert_E^2$.
- $z_i\in\mathbb Z^n$ are lifts with $Pz_i=b_i$.

Facts used, all verified in Approach 11:

- (F1) $E\subseteq D$ (Lemma 3.1).
- (F2) For $\alpha\in H$, the support function of $E$ is $h_E(\alpha)=\sup_{y\in E}\langle\alpha,y\rangle=\lvert Q^{1/2}\alpha\rvert$, because $\langle\alpha,PQ^{1/2}b\rangle=\langle Q^{1/2}\alpha,b\rangle$.
- (F3) Prop. 3.4 rounding. If $V_r=\operatorname{span}(v,z_1,\dots,z_r)$ contains $s$ with $\lVert s_k\rVert\ge\sigma$ for all $k$, then $\sum_{i\le r}t_i>4(\sigma-\tfrac1{n+1})^2$.
  - *Proof.* Write $s=av+\sum a_iz_i$, so $Ps=\sum_{i\le r}a_ib_i$. Nearest-plane rounding gives integers $k_i$ with $e=Ps-\sum k_ib_i$ and $\lVert e\rVert_E\le\varepsilon:=\tfrac12(\sum_{i\le r}t_i)^{1/2}$.
  - By (F1), $e=Py$ with $\lvert y_k\rvert\le\varepsilon$.
  - Then $s-\sum k_iz_i-y\in\ker P=\mathbb Rv$, say it equals $\tau v$. So $\lVert\tau v_k\rVert\ge\sigma-\varepsilon$ for all $k$.
  - If $\varepsilon\le\sigma-\tfrac1{n+1}$, then $\tau$ is a witness, which is impossible. ∎
  - With Lemma 3.3 (Giri–Kravitz) this gives $\sigma=1/(n+1-r)$ and $\sum_{i\le r}t_i>B_r$.
- (F4) $t_{i+1}\ge\tfrac34t_i$ (KZ, Lemma 3.5).

**Lemma H.** For every such counterexample,
$$\sum_{i=1}^{d-1}t_i\;>\;B'_{d-1}:=\min\Bigl(B_d-\tfrac13,\;4\bigl(\tfrac25-\tfrac1{n+1}\bigr)^2\Bigr).$$
Here $B_d=4(\tfrac12-\tfrac1{n+1})^2$.

- $n=15$: $B'_{13}=83/192$, against $B_{13}=169/576$.
- $n=17$: $B'_{15}=37/81$, against $B_{15}=25/81$. Here $4(31/90)^2=961/2025>37/81$.

*Proof.* $V:=V_{d-1}=\operatorname{span}(v,z_1,\dots,z_{d-1})$ has dimension $d=n-1$: apply $P$ to a linear relation and use the independence of the $b_i$. So $V$ is a rational hyperplane. Let $\alpha\in\mathbb Z^n$ be its primitive normal, with $\gcd(\alpha)=1$.

Then $\alpha\cdot v=0$ and $\alpha\cdot z_i=0$ for $i\le d-1$, so $\alpha\in H$. Write $L=\lVert\alpha\rVert_1$.

- $L\ne1$: $\alpha=\pm e_l$ would give $v_l=0$.
- $L$ and $\sum_l\alpha_l$ have the same parity, since $\alpha_l\equiv\lvert\alpha_l\rvert\pmod 2$.

*Case (i): $\sum\alpha_l$ even.*

- $-\tfrac12\sum\alpha_l$ is an integer. Since $\gcd(\alpha)=1$, there is $m\in\mathbb Z^n$ with $\alpha\cdot m=-\tfrac12\sum\alpha_l$.
- Then $s=\tfrac12\mathbf 1+m$ satisfies $\alpha\cdot s=0$, so $s\in V$, and $\lVert s_k\rVert=\tfrac12$ for all $k$.
- (F3) with $\sigma=\tfrac12$ gives $\sum_{i\le d-1}t_i>B_d$.

*Case (ii): $\sum\alpha_l$ odd and $L\ge5$.* This is the separation argument.

- Put $\varepsilon_l=\operatorname{sgn}(\alpha_l)/(2L)$, with $\varepsilon_l=0$ when $\alpha_l=0$. Then $\alpha\cdot\varepsilon=\sum_l\lvert\alpha_l\rvert/(2L)=\tfrac12$.
- $N_0=\tfrac12\sum\alpha_l+\tfrac12$ is an integer. Choose $m\in\mathbb Z^n$ with $\alpha\cdot m=-N_0$, which is possible since $\gcd(\alpha)=1$.
- Put $s=\tfrac12\mathbf 1+\varepsilon+m$. Then $\alpha\cdot s=\tfrac12\sum\alpha_l+\tfrac12-N_0=0$, so $s\in V$.
- $\lvert\varepsilon_l\rvert\le\tfrac1{2L}<\tfrac12$, so $\lVert s_l\rVert=\tfrac12-\lvert\varepsilon_l\rvert\ge\tfrac12-\tfrac1{2L}\ge\tfrac12-\tfrac1{10}=\tfrac25$.
- (F3) with $\sigma=\tfrac25$ gives $\sum_{i\le d-1}t_i>4(\tfrac25-\tfrac1{n+1})^2$.

*Case (iii): $L=3$.* This is the load-bearing case.

1. **$\langle\alpha,\Lambda\rangle=\mathbb Z$.** For $b=Pz\in\Lambda$, we have $\langle\alpha,Pz\rangle=\langle\alpha,z\rangle$ because $\alpha\perp v$. So $\langle\alpha,\Lambda\rangle=\alpha\cdot\mathbb Z^n=\gcd(\alpha)\mathbb Z=\mathbb Z$.
2. **$\langle\alpha,b_d\rangle=\pm1$.** Since $\langle\alpha,b_i\rangle=\alpha\cdot z_i=0$ for $i<d$, the value $\langle\alpha,b_d\rangle$ generates $\langle\alpha,\Lambda\rangle=\mathbb Z$.
3. **$b_d^*$ is the shortest point of a hyperplane.**
   - $W=\operatorname{span}(b_1,\dots,b_{d-1})=H\cap\alpha^\perp$, comparing dimensions.
   - $b_d^*$ is the $E$-orthogonal projection of $b_d$ onto the $E$-orthogonal complement of $W$. So it is the point of minimum $E$-norm in $b_d+W=\{y\in H:\langle\alpha,y\rangle=\langle\alpha,b_d\rangle=\pm1\}$.
4. **Norm duality.** For $y\in H$ with $\langle\alpha,y\rangle=1$, $1\le h_E(\alpha)\lVert y\rVert_E$. Equality is attained at $y=x/h_E(\alpha)$, where $x\in\partial E$ is a maximiser of $\langle\alpha,\cdot\rangle$. Hence
$$t_d=\lVert b_d^*\rVert_E^2=\frac1{h_E(\alpha)^2}=\frac1{\sum_l q_l\alpha_l^2}\quad\text{by (F2)}.$$
5. **Why $h_E(\alpha)^2\ge3$.**
   - Each $q_l=1+u_l(2-u_l)\ge1$, because $0<u_l\le1$.
   - Each $\alpha_l^2\ge\lvert\alpha_l\rvert$, because $\alpha_l\in\mathbb Z$.
   - So $h_E(\alpha)^2=\sum_lq_l\alpha_l^2\ge\sum_l\alpha_l^2\ge L=3$, and $t_d\le\tfrac13$.

   More generally $t_d\le1/\lVert\alpha\rVert_1$ always.
   - Concretely, $L=3$ means $\alpha$ is, up to sign and permutation, $e_i+e_j-e_k$ (so $v_k=v_i+v_j$) or $2e_i-e_j$ (so $v_j=2v_i$).
   - Here $\sum\alpha_l^2=3$ or $5$.
6. **Conclusion.** (F3) at $r=d$ with $\sigma=\tfrac12$ (case (i)'s point $\tfrac12\mathbf 1$ lies in $V_d=\mathbb R^n$) gives $\sum_{i\le d}t_i>B_d$. Hence $\sum_{i\le d-1}t_i>B_d-t_d\ge B_d-\tfrac13$.

The three cases are exhaustive: even sum; odd sum with $L\ge5$; odd sum with $L=3$. The bound in case (i), $B_d$, exceeds both entries of the minimum. ∎

*Remarks.*

- Lemma H uses no lower case of the conjecture: the points are explicit. The rest of the flag bound still needs LRC($m$) for $m<n$.
- Case (ii) is the hyperplane instance of Allikvere's support/density idea (§4).
- Case (iii), the conversion of a short relation into an *upper* bound on $t_d$, is not in his paper as far as we read it.
- His Lemma `analytic-section` uses the same duality to cut out relation sections instead.

**Lemma M (product minimisation; generalises Allikvere's Lemma 3.6).**

*Statement.*

- Let $F_0=0<F_1<\dots<F_d$ have increments $e_i=F_i-F_{i-1}$ with $e_{i+1}/e_i>\tfrac34$ for all $i$.
- Let $t\in\mathbb R^d_{>0}$ satisfy $t_{i+1}\ge\tfrac34t_i$ and $\sum_{i\le j}t_i\ge F_j$ for all $j$.
- Then $\prod t_i\ge\min_{\mathcal C}\prod_i t^{\mathcal C}_i$, where $\mathcal C$ runs over the $2^{d-1}$ compositions of $d$ into blocks.
- On a block $(a,b]$, $t^{\mathcal C}$ is geometric with ratio $\tfrac34$ and sum $F_b-F_a$.

*Proof.*

1. **Coordinates.** Put $w_i=(3/4)^{i-1}$ and $z_i=t_i/w_i$. The feasible set $\Pi$ is $\{z_1\le\dots\le z_d,\ \sum_{i\le j}w_iz_i\ge F_j\}$.
2. **Reduction to vertices.**
   - Its recession cone lies in $\mathbb R^d_{\ge0}$: the $j=1$ constraint forces $dz_1\ge0$.
   - $\Pi$ is pointed, and $\Pi=\operatorname{conv}(\text{vertices})+\text{cone}$.
   - $f=\sum\log(w_iz_i)$ is concave and nondecreasing in each $z_i$, so $\min_\Pi f$ equals the minimum over vertices.
3. **No active constraint inside a block.**
   - At a vertex, take a maximal block $(a,b]$ of equal $z=\zeta$, and suppose the constraint at $j$, with $a<j<b$, is active.
   - Subtracting the feasible constraint at $a$ gives $\zeta\le(F_j-F_a)/\sum_{a<i\le j}w_i\le\max_{a<i\le j}e_i/w_i=e_j/w_j$. This uses that $e_i/w_i$ strictly increases, since $(e_{i+1}/e_i)/(3/4)>1$.
   - Feasibility at $j+1$ gives $w_{j+1}\zeta\ge e_{j+1}$, so $\zeta\ge e_{j+1}/w_{j+1}>e_j/w_j$. This is a contradiction.
4. **Every vertex is a block point.** $\beta$ blocks need $\beta$ independent active prefix constraints, so all block ends are active. Hence every vertex is a block point.
5. **Lower bound.** The minimum over *all* block points, feasible or not, is a lower bound. ∎

*Remarks.*

- Allikvere's Lemma 3.6 additionally assumes $e_{i+1}/e_i>\tfrac43$ and then shows that the all-singleton point $t=c$ is the minimum (majorisation). Lemma M drops that hypothesis and takes the minimum by enumeration.
- His App. A.2 "pooling" is a different weakening of the same hypothesis. It is valid but cruder. At $n=15$ with $F_{13}=83/192$ it gives the same minimum here, because the pooled block $(12,14]$ is exactly the minimising block point.

**Result.** Use $F_j=B_j$ for $j\ne d-1$ and $F_{d-1}=B'_{d-1}$. The ratio hypothesis $e_{i+1}/e_i>\tfrac34$ is asserted in `hyperplane.py`, and the minimum is over all $2^{d-1}$ block points in exact rationals.

| | $n=15$ | $n=17$ |
| --- | --- | --- |
| $B'_{d-1}$ | $83/192$ | $37/81$ |
| minimising blocks | $(12,14]$ merged | $(14,16]$ merged |
| new $K'_n$ | $13739417/563178692269924866919350927360000000000$ | $6498680661001/758781616672021226517834792714378387633733632000000$ |
| new target | $481.122599$ | $667.928566$ |
| gain | $2.11617$ | $2.35316$ |

**Gates saved ($n=15$, heuristic accounting).** The 78 primes $251$–$739$ sum to $\sum\ln p=479.36$. The plain target $483.24$ needs $743$ as well.

- At $481.12$ the gate $743$ can be replaced by *any* additional gate prime $p$ with $\ln p>1.77$.
- Removing $743$ outright would need a further $1.77$.

**Label.** Proved, given LRC($m$) for $m<n$ and the standard facts of Approach 11. Every number is checked in exact rationals (logarithms to 50 digits).

## 3. Plain flag target for $n=17$ (LRC(17), 18 runners): proved

`flag_n.py` (exact):

- $K_{17}=12284840569/1891874009617192087541004654473009185161216000000$ and $\ln A_{17}=43.965010$.
- $\min c_{i+1}/c_i=948/625>4/3$, so Lemma 3.6 applies.
- **Shape lemma $R_{17}<951/2000$.** The $n$-general argument of `shape_lemma.py` (Approach 10) is re-run at $n=17$ with $T=(17\cdot2000/951)^2=1278.194$.
  - All exact checks pass: the $\varphi$-identity, the $\alpha$-interval, the critical identity, $L$ decreasing, $H_1$ form, and the $H_1$ log-derivative cubic.
  - Step 4 gives $H_1(t_0)\ge1278.448>T$, with $t_0\in(2529/40000,\,63227/1000000)$.
  - One change: the constant $a>8/5$ of Step 2 fails at $n=17$ ($a(\alpha)\approx1.55$), and $a>3/2$ is used instead. It enters only Step 0 (compactness) and Step 3, where $H\ge4(3/2)^{15}=1751.5>T$.
  - The true minimum of $R_{17}$ is $\approx0.475439$ (numeric), so $951/2000$ loses only $0.002$ of target.
- $\ln\prod v<686.602944$.
- **Forced divisor.** For $2\le d\le18$, if $d\nmid v_i$ for all $i$, then $\tau=1/d$ is a witness, because $\lVert a/d\rVert\ge1/d\ge1/18$ for $d\nmid a$ (checked for all $a$, $d$).
  - So the maximal prime powers $16, 9, 5, 7, 11, 13, 17$ each divide $\prod v$.
  - $\operatorname{lcm}(2..18)=12252240$.
- **Target $670.281725$.**

**Label.** Proved, given LRC($m$) for $m\le16$ and the general-$n$ Theorem 3.8 verified in Approach 11.

## 4. Audit of Allikvere, "Sixteen lonely runners" (Zenodo 10.5281/zenodo.23304361): partial

**Source.**

- `proof_sources.zip`: downloaded fresh; its SHA-256 `93db6a07…ab0d91` matches the record's `SHA256SUMS.txt`, and the MD5 matches the Zenodo API.
- The TeX sources were copied from the literature agent's download.
- None of the author's code was run; all checks below are our own code.
- The audit was stopped here at the coordinator's request (target changed to $n=17$).

**Structure of his bound.**

1. **Riesz inequality** (Lemma `signed-relations`). Let $O$ be the span of the odd-support ternary relations $h\in\{-1,0,1\}^{15}$ with $h\cdot v=0$. Then
$$\sum_{h\in\mathcal T(O)}(-1)^{s(h)+1}\frac{\delta+s(h)}{2^{s(h)-1}}>\delta,\qquad \delta=\frac1{1-\cos(\pi/8)}-8.$$
2. **Low ranks.** $\dim O\ge4$.
3. **Per-rank bound.** For each rank $r=\dim O$, a section bound $W(T,\gamma)$ is obtained via
   - the duality $\det_E\Lambda^2=\det_E\Gamma^2/\det(AQA^T)$;
   - support-dependent prefix gains $\gamma$;
   - a Schur shape constant $C_r$.
4. **Assembly.** The table $W_4=42$, $W_5=\tfrac{359}{100}\cdot666$, … gives $J_*=\min_r\alpha/(W_r\tau_r)$, and then
$$\ln\prod v<15\ln\frac{61}{1875\sqrt{K_{15}J_*}}.$$

**Checked here.**

| part | result | how | label |
| --- | --- | --- | --- |
| assembly: $K_{15}$, the five $J_r$, $J_*=4355451813888/29029584727$ (rank 5), $\ln$ bound $459.0839110$, $D$, requirement $361.4457331$ | all equal to the paper | `audit_assembly.py`, exact | machine-checked |
| Riesz inequality (Fourier expansion, sign of dropped even terms) | correct | re-derived by hand: $\int E-(15+\delta)\int P=-\sum_h(-\tfrac12)^{s}(s+\delta)$ | verified by reading |
| $5137/1000<\delta<2569/500$ and the quartic | correct | interval arithmetic (mpmath) | machine-checked |
| greedy support lemma ($\le3^{j-1}$ odd lines; summation by parts; $g\le\prod s_j$) | correct | read; survivors recomputed | verified by reading |
| rank-3 survivor profiles (exactly the 9 listed), rank-6 "55 lists, max $767637<4T$", rank-7 $g\le23030293$ at $(11^6,13)$, rank-4 "43 lists with $P\ge168$, max $2025$" | reproduced | `audit_relations.py` | machine-checked |
| **rank-3 exclusion**: all 9 profiles, 8,867 multiplicity vectors, per-profile $\max S_O(\delta)$ | **every count and every maximum equals his table**, e.g. $(3,3,3)$: 354 vectors, max $(5\delta+14)/8$; all $<\delta$ | `audit_rank3.py`, independent re-implementation | machine-checked |
| rank-6 auxiliary claims: the seven weight inequalities, 304 projective box vectors, counts $188,186,165,136,186$, $\lvert\mathcal L\rvert=182$ | reproduced | scratch script (same logic as `audit_relations.py`) | machine-checked |
| $\gamma$ factors: $G(6,9)=130/49$, $\gamma(r,r+3)=1+c_{m+1}/c_m$, all eight rank-7 $(g_a,G(7,a))$ pairs, rank-8 $6100/2349$, $\gamma(4,7)=2196/775$, quarter-point $\gamma=405/62$ | reproduced exactly | `audit_relations.py` (own PAV pooling, with certificate asserts) | machine-checked |
| rank 6/7/8 quotient maxima $5764801/130$, $185218112079/62500$, $442188799299/1220$; rank-4 supports $10$–$15$ values (from $g\le167$) | reproduced exactly | as above | machine-checked |
| shape constants $C'_r<D_r$ (the 240th-power integer inequalities) | true | `audit_relations.py`, exact | machine-checked |
| Schur shape lemma (Schur complement, weighted Cauchy–Schwarz, Cauchy–Binet with the $r+1$ largest $q$) | correct | read | verified by reading |
| sup of $\Phi_r$ against $C_r$ | numeric maxima $2.7489, 3.5802, 4.6908, 6.1871, 8.2231$ are below $11/4, 359/100, 47/10, 31/5, 609/50$ | Nelder–Mead/BFGS, 300 starts | heuristic sanity |
| Lemma `analytic-section` ($\Gamma=\Lambda\cap T^\perp$; covolume duality) | correct | read | verified by reading |
| prefix inequalities on the section $\Gamma$; Lemma `analytic-center` (vertices $(v_je_i-v_ie_j)/(h_iv_j+h_jv_i)$) | correct | read; vertex formula re-derived | verified by reading |
| Lemma `support-prefix` ($j\ge17-a\Rightarrow\sum_{i\le j}t_i>B_{j+1}$) and Lemma `support-clearance` (case split $e=1,2,\ge3$; fixed-coordinate enlargement; the $r=2k$, $q=k$ case) | correct | read line by line | verified by reading |
| affine density lemma (shortest vector in the affine lattice, $\lvert\delta_i\rvert\le p_i/2$; base-polytope separation; Barthe realisation; limit) | correct; the last two steps are standard facts cited (JLT25) | read | verified by reading |
| weak product lemma, PAV pooling certificate | correct | read; our PAV asserts the certificate properties | verified by reading |
| **rank-4 classification** ($g\le225$, 72 primitive sections, the support-7 table with $W_{\text{eff}}\le42$, quarter-point certificates S8, the continuous bounds for seven-coordinate classes) | **not re-done** | — | open |
| **rank-5 classification** ($g/\gamma\le666$; R5a–R5h) | **not re-done** | — | open |
| rank-2 exclusion (489,773 vectors, $I_1\le18I_0$) | not re-done (rank 3 was) | — | open |
| rank-6 support lemma and rank-6 global lemma (beyond the counts above) | read; plausible; not machine-checked | — | open |

**No error or gap was found** in anything checked.

**What is load-bearing and still unchecked.** The minimum $J_*$ is at rank 5, giving $459.0839$; rank 4 gives $459.0808$. Both rest on the large rank-4 and rank-5 classifications, about 2,000 pinned files in `proof_sources.zip`, which we did not re-implement.

Our coarse re-computation (§5) quantifies how much those classifications carry:

- With ranks $\le3$ excluded and *no* fine classification, rank 4 only gets $J_4\approx3.70$ (coarse $g\le2025$). That gives a bound near $496.67-7.5\ln3.70\approx486.9$ before divisors.
- His $J_4\approx150$ is therefore almost entirely the fine rank-4 classification.

## 5. Coarse relation-rank bound for general $n$: in progress

`relrank_n.py` re-derives Allikvere's general lemmas for general $n$. The derivations are short; we state the changes.

- **Riesz inequality.** $\delta_n=1/(1-\cos(2\pi/(n+1)))-(n+1)/2$. The same Fourier proof applies: $E(t)>(1/c+(n-1)/2)P(t)$. For $n=17$, $\delta_{17}\approx7.580$.
- **Support-prefix.** $\sum_{i\le j}t_i>B_{j+1}$ for $j\ge n+2-a$. Support-clearance needs the relation space $V_j^\perp$ to have rank $n-1-j\ge3$, which we enforce.
- **Schur lemma.** $900$ becomes $4n^2$. The shape constant $C_r$ is computed by weighted AM–GM with an optimised lower weight $\omega$; the one-variable maximum is bounded in interval arithmetic. Our $C_r$ at $n=15$ are close to the numeric suprema, e.g. $C_8\le8.2232$ against his $609/50$.
- **Interface.** $(\prod v)^{2/n}\le W\tau_r/(4n^2K_n)$. Against the plain bound with radius $r_n$, the improvement factor is $J_r=(2r_n)^2/(W_r\tau_r)$.
- **Case rule.** A counterexample whose odd space has rank $r$ gets $J(r)=\max\bigl(1,J^{\text{greedy}}_r,\max_{r'\le r}J^{\text{select}}_{r'}\bigr)$.
  - $J^{\text{select}}$ uses $r'$ selected odd relations and full-row-index $g$ bounds, with no Riesz input.
  - The gain is $\tfrac n2\ln\min_rJ(r)$.

**$n=15$ (sanity).** Ranks $\le3$ are not excluded by the greedy bound alone: rank 2 survives with $J=0.90$, rank 3 with $J=2.14$. So the coarse bound gives **no gain** (the minimum is $J=1$ at rank 2).

- With Allikvere's rank-2 and rank-3 exclusions (rank 3 re-verified in §4), the coarse minimum moves to rank 4 with $J_4=3.70$: a gain of $9.8$ units.
- Excluding rank 4 as well would give $J_5=16.4$: a gain of $21$.

**$n=17$.** Running; the next step is to exclude the low ranks with our own complete-section enumeration (the rank-3 code generalised to rank $r$ and $n$ columns).

## 6. Other routes (heuristic or failed, kept)

- **Optimal ellipsoid (John ellipsoid of $D$) instead of Allikvere's $Q$.** On the symmetric shapes $(1,t,\dots,t)$ the invariant ellipsoids are exactly the diagonal family. There, $q_1\to0$ and $q_s=(1+t)^2$ is optimal, and $H^*(1,t)=(1+t)^{28}/t^{28/15}$ has minimum $951.4$ at $t=1/14$, against $944.96$.
  - Potential gain $\approx0.05$ (heuristic; general shapes not examined). Not pursued.
- **2-D CVP in the last rounding block.** Replace $\tfrac14(t_{r-1}+t_r)$ by the exact covering radius of the Gauss-reduced projected 2-D lattice. KZ forces $\mu^2\ge1-t_r/t_{r-1}$ when $t_r<t_{r-1}$, which gives $4\mu^2=2t_{r-1}/(1+\mu)$.
  - With Lemma H at $n=15$, a numeric minimisation (SLSQP) gives $481.00$, an extra $0.12$.
  - Not proved: the constraint is nonlinear and Lemma M does not cover it.
- **Extra divisibility from small moduli ($32$, $27$, $25$, $17$, …).**
  - Mod $32$: the odd classes up to sign number $8$ and can be covered by $14$ odd speeds, so level one forces nothing.
  - Small moduli fail as gates for the same reason that primes $<89$ failed at $k=14$.
  - Not pursued (failed in principle at level one; lifts would be gate computations, not bounds).
- **Better separation in Lemma 3.3 in general.** Lemma 3.3 is tight for every $q$, for example $V=\mathbb R^{q-1}\times\mathbb R(1,2,\dots,n-q+1)$. Any gain must use $v\in V$, as Lemma H and Allikvere's support lemma do.
