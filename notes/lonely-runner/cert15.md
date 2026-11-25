# Re-check of Allikvere's LRC(15) gate certificates (16 runners)

**Source.** J. Allikvere, *Sixteen lonely runners*, Zenodo doi:10.5281/zenodo.23304361 (created 2026-10-11, one version, unrefereed). We read the README, `SHA256SUMS.txt` and the manuscript source (`paper.tex`, §§2, 4–7) as data.

**Scope of this note.** It covers the 59 gate primes of his set $\mathcal P$: all primes $269 \le p \le 659$ except $271, 277, 283, 293, 307$. Out of scope:

- the bound $\log \prod v_i < 459.084$, which is audited separately;
- the 16 preliminary primes $\mathcal Q_0$;
- level-one completeness.

What is open is listed at the end.

**Method.** Every check below uses our own code, written from the definitions:

- `computations/lonely-runner/cert15/rowcheck15.c` and `check_gate15.py`;
- `gatecheck.c` and `canon.c` in `computations/lonely-runner/`.

None of the author's programs were run, including `verify_article.py`, `verify_campaign_gate.py` and the audit kits. The archives were extracted with Python `tarfile` (`filter="data"`) into fresh directories and read as data. We used 1 core throughout.

## 1. What each gate certificate claims

Fix $k = 15$ and a prime $p$. Put $h = (p-1)/2$ and $d_p(x) = \min(r, p-r)$, where $r \equiv x \pmod p$ and $0 \le r < p$. A vector $w \in \mathbb Z_{lp}^{15}$ with $p \nmid w_i$ is *$(15,p,l)$-proper* if

- (a) $\gcd(l, w_1, \dots, \widehat{w_i}, \dots, w_{15}) > 1$ for some $i$, or
- (b) some $t \in \frac{1}{lp}\mathbb Z$ has $\lVert t w_i \rVert \ge \frac1{16}$ for all $i$.

This is Sungkawichai–Trakulthongchai, arXiv:2604.23906, Def. 2.1, restated in his §2. $I(15,p,l)$ is the set of improper vectors, and $J(15,p)$ is the set of level-one vectors that are not eventually proper.

**Claim of each gate certificate** (his Prop. "gates", §5). For every $p \in \mathcal P$, every level-one unit orbit has an empty improper fibre by level 16. Hence $J(15,p) = \varnothing$. Via his Lemma "gate"(i) (= arXiv:2609.02604, Lemma 2.2(i)), every primitive counterexample with distinct coordinates then has $p \mid v_1 \cdots v_{15}$.

The claim rests on two parts.

1. **Level-one completeness** (his Prop. "tau"). The improper set $I(15,p,1)$ is, up to units, permutations and signs, the union of:
   - the stored irredundant 15-class covers;
   - the stored 14-class covers, each extended by every class $x \in \{1, \dots, h\}$.

   This rests on an exhaustive search certifying $\tau(p) \ge 14$, i.e. no cover by $\le 13$ classes, followed by the two-branch minimal-cover search with private-time quotas (his Lemma "quota").
2. **Binary cascade.** For each stored row $r$, put $S_1 = \{r\}$ and let $S_{2l}$ be the improper lifts $w_i + j_i\, lp$, $j_i \in \{0, 1\}$, of the members of $S_l$. Then $S_{16} = \varnothing$.

The archive records the rows of part 1 and the outcome of part 2. Part 1's search, about $10^{12}$–$10^{13}$ nodes per gate, is recorded only as logs.

**Why part 2, with part 1, gives $J(15,p) = \varnothing$** (checked here, elementary).

- If $w$ is proper at level $l$, every lift $w'$ to level $2l$ is proper.
  - A witness $t \in \frac{1}{lp}\mathbb Z$ lies in $\frac{1}{2lp}\mathbb Z$. Also $w' \equiv w \pmod{lp}$ gives $\lVert t w'_i \rVert = \lVert t w_i \rVert$.
  - Since $l \mid lp$, we have $\gcd(l, w'_j) = \gcd(l, w_j)$, so $\gcd(2l, \dots) > 1$ whenever $\gcd(l, \dots) > 1$.
- Hence $S_{16}$ is exactly the set of elements of $I(15,p,16)$ that reduce to $r$.
- Improperness is invariant under units, permutations and signs (ST, Prop. 5.1), and level-one improper vectors are the covers (eq. (cover) of the manuscript; our `rowcheck15.c` header).
- So $S_{16} = \varnothing$ for one representative of every orbit gives $I(15,p,16) = \varnothing$. Hence $J(15,p) = \varnothing$ (ST, Lemma 2.4).

## 2. Archive format

The format was read from the archives and agrees with his `SUMMARY.json` fields. Each `evidence15_<p>_s0.tgz` holds the following.

| member | content |
| --- | --- |
| `out15_<p>/rows_ir/ir_<r>_<s>.txt` | irredundant 15-class covers, 2 hex digits per class, one per line; root job $r$, sub-job $s$ |
| `out15_<p>/rows_km1/km1_<r>.txt` | rooted 14-class covers (hex) |
| `out15_<p>/rows_km1/dedup_<i>.txt` | the deduplicated 14-class covers, one or more per file |
| `out15_<p>/filt/ir_<r>_<s>.out`, `ext_<i>.out` | one line `SURVIVOR base: v_1 … v_15 l2=… [tight=…] l4=… l8=… l16=…` for every input row with an improper level-2 lift; `ext_<i>` holds the covers of `dedup_<i>`, each extended by every class $x = 1..h$ |
| `filt/*.stats` | rows and survivors per input file |
| `SUMMARY.json` | counts (base family, cascade totals, persistent orbits = 0), status `GATE_CLOSED` |
| `MANIFEST_SHA256.json` | SHA-256 of every file, plus three entries `../bgk15`, `../cascade_k15`, `../tight_lift_16` naming executables that are not shipped |
| `kills/` | empty at all 59 gates |
| top level | run logs, `SOURCES15_SHA256.txt`; laptop runs ($p \le 503$) also have `BUILD_SHA256.txt`, `lscpu.txt` |

**Comparison with the LRC(14) archives** (Zenodo 10.5281/zenodo.22667683, which `check_gate_full.py` handles):

- The layout is the same: `rows_ir`, `rows_km1`, `filt`, `kills`, `SUMMARY.json`, and the same `SURVIVOR` line format.
- The differences:
  - the directory is `out15_<p>`;
  - deduplicated covers are stored explicitly as `dedup_<i>.txt`, so each `ext_<i>` cascade file corresponds to one stored file of covers;
  - the cascade stops at level 16, which for $k = 15$ is the kill level $k+1 = 16$ itself.
- There is no terminal level-15 kill: `kills/` and `level_kills` are empty and the persistent-orbit count is 0.
- So the LRC(14) check D (level-3/5 CRT kill and few-exception shift lemma) has no counterpart. The level-16 emptiness of the binary cascade replaces it.

## 3. Checks (per gate, every stored row, no sampling)

`check_gate15.py` runs the following checks.

- **A. Integrity.**
  - The archive SHA-256 equals his `SHA256SUMS.txt`. That file has CRLF line endings; its MD5 matches the Zenodo metadata.
  - Every file entry of the internal `MANIFEST_SHA256.json` matches.
  - The three executable entries are compared with the archive's `BUILD_SHA256.txt` and recorded only.
- **B. Stored rows**, tested on every irredundant row and every rooted and dedup 14-class cover:
  - classes lie in $1..h$, are distinct, and include class 1;
  - the row is witness-free at level 1, by two implementations:
    - `rowcheck15.c`: covering test $16\, d_p(a v) < p$ for every folded time $a$;
    - `gatecheck.c hexrows`: every $t = m/p$ directly;
  - the row is irredundant: every class has a private time.

  Further checks on the 14-class covers and on the counts:
  - The 14-class covers are tested with the $k = 15$ threshold. So every extension $c + x$ is in $I(15,p,1)$.
  - Every 14-class cover is irredundant, as $\tau(p) \ge 14$ requires.
  - The dedup covers represent exactly the unit orbits of the rooted covers (`canon.c`), one cover per orbit.
  - A `dedup_<i>.txt` file may hold several covers: one at most gates, but 2 at $p = 317$ and 3–4 at $p = 331$.
  - **Bug in our own checker, now fixed; not a problem with his data.** The first version of `check_gate15.py` assumed one cover per dedup file and extended only the first.
    - At $p = 313$ and $p = 317$ it therefore reported a cascade mismatch: one survivor line of the certificate absent from our run, and totals off by one.
    - The fixed script extends every cover in the file. Both gates were re-run with it, and the reported records are the re-runs.
    - The 51 gates run before the fix were unaffected: the old script flagged any file with more than one cover, and none of them was flagged. All 59 records reported below come from the final script; the 51 were re-run with it.
  - All counts equal `SUMMARY.json`.
- **C. Cascade**, by `gatecheck.c cascade` with $k = 15$, on every irredundant row and every extension row (dedup cover $+\,x$, $x = 1..h$).
  - Per input file, the multiset of $(\text{row}, \lvert S_2\rvert, \lvert S_4\rvert, \lvert S_8\rvert, \lvert S_{16}\rvert, \lvert S_{32}\rvert)$ over rows with $S_2 \ne \varnothing$ equals the certificate's `.out` file. Rows and survivors equal the `.stats` file. The set of `filt` files equals the set of stored input files.
  - The totals `survivor_rows`, `died_l<l>`, `level2_improper_lifts_total` and `level2_survivor_rows_ir/ext` equal `SUMMARY.json`.
  - **$S_{16} = \varnothing$ for every row.**
  - The rows whose fibre first empties at level 16 are exactly the unit orbit of $(1, \dots, 15)$, with trace $1, 2, 4, 0$, as stated in his §4.
  - There are no persistent orbits and no kill files.

**Tests** (`cert15/test_check_gate15.py`, 4 tests, all pass):

- `rowcheck15` and `gatecheck hexrows` agree with a brute force from Def. 2.1 at level 1 (`sieve.Level(15,p,1)`). This covers cover/non-cover status and irredundancy, on 1,200 random rows at $p = 67, 101, 131, 269$ with $n = 15, 14$.
- `gatecheck cascade` with $k = 15$ agrees with a brute force over all $2^{15}$ lifts of every fibre member (witness on the level-$l$ grid, or the gcd clause). The inputs are $(1..15)$ at $p = 269$ (levels 2, 4, 8) and four stored rows of the $p = 367$ archive (levels 2, 4).
- $(1..15)$ has trace $1, 2, 4, 0, 0$ at $p = 269, 367, 509, 659$, the same as `results/tight_orbit_k15.jsonl` (from `liftfree.c`).

**Negative controls** (tampered copies of the $p = 463$ archive). Each was rejected by a content check, not only by the archive hash:

- one $l_8$ count altered;
- one irredundant row deleted;
- the `tight=YES` survivor line deleted;
- $l_{16} = 0$ changed to 2;
- a row replaced by a non-cover.

A first draft of the cascade test, on random rows at $p = 37$, blew up: fibres are huge at such small primes. It was replaced by the tests above.

**Cost.** Build `gatecheck.c` with `-march=native`. Without it, `__builtin_popcountll` compiles to a software routine and the cascade is about 5× slower (0.83 against 0.17 ms per row at $p = 367$; identical output on 20,000 rows).

## 4. Results

RESULTS_PLACEHOLDER

## 5. Provenance observations (not mathematical discrepancies)

These do not affect our check, which trusts none of his executables.

- In all 59 archives, `SOURCES15_SHA256.txt` gives `bgk15` as `497576c02da1…`.
- In the 35 laptop archives ($269 \le p \le 503$), `BUILD_SHA256.txt` and the `../bgk15` manifest entry give `285606ceab54…`.
  - So two different executable hashes are recorded under one name. The same holds for `cascade_k15` and `tight_lift_16`.
  - Each of those `BUILD_SHA256.txt` files says `P=503`. The build record appears to be one shared build, copied into every laptop archive.
- The fleet archives ($509 \le p \le 659$) have no `BUILD_SHA256.txt`.
- `SUMMARY.json`'s claim string still says "binary cascade to level 32 plus level-16 composite kill". This is template text; the recorded run stops at 16 and has no kill.

## 6. What remains unchecked

- **Level-one completeness at all 59 gates.** This is the substantive gap. It includes the covering-number precondition $\tau(p) \ge 14$. His logs record that precondition only as "covers on $\le 13$ classes = 0", with node counts; the search itself is not stored.
  - At the larger gates the stored family is tiny. At $p = 607$ the only stored row is $(1..15)$. Sixteen gates (509, 541, 569, 571, 587, 599, 601, 607, 617, 619, 631, 641, 643, 647, 653, 659) store at most 10 rows, and every gate $p \ge 509$ stores at most 60.
  - So there the certificate's content is almost entirely the completeness of a search of about $10^{13}$ nodes, which we have not reproduced. Our cascade check is necessary but nearly trivial there.
  - Reproducing it needs a $k = 15$ generator run. At about $10^5$ CPU-h for the whole campaign (`problems/lonely-runner.md`, Next steps 3, heuristic), that is far beyond this session. The gates agent is running completeness at one gate.
- **The preliminary primes $\mathcal Q_0$** (16 primes: 29, 31, 191, 211, 223, 233, 239, 241, 251, 257, 263, 271, 277, 283, 293, 307). They are in separate packages:
  - `gates_239_271_283_293_307_audit.zip`, 292 MB;
  - the weighted-shift package;
  - `gate_211_audit.zip`;
  - `gate_263_provenance.zip`;
  - `gates_29_31_records.zip`.

  Nine of them rely on the weighted shift lemma with $d = 4$ and Lemma "gate"(ii). None was checked here.
- **The bound** $\log \prod v_i < 459.084$ and the requirement $\sum_{p \in \mathcal P} \log p > 361.44573307$ (Cor. "mass"). These are audited by the bound agent. We only recomputed the prime sum (§4).
- **Cited inputs:**
  - the retention and invariance facts (ST, Lemma 2.4 and Prop. 5.1);
  - his Lemma "gate"(i);
  - LRC(m) for $m \le 14$.

  These are taken as stated, apart from the elementary argument in §1.
- **Our code is tested, not formally verified.**
