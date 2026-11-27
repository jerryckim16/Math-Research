# Lonely runner: the LRC(17) gate $p=251$ (18 runners), full run

> **Draft, work in progress.** This page is written by a research agent and has not yet been reviewed by the coordinator. Treat its claims as unreviewed until this notice is removed.

Scope: the first full closure of an 18-runner gate. Every level-one base of $I(17,251,1)$ is enumerated, and the extended cascade is run on each one. Code: `computations/lonely-runner/gate251/`. Definitions follow `midprimes17.md` §1–2.

Labels follow `README.md`. The result is a **certificate-checked computation**, given the dependencies listed in §1.

## 0. Result

Run 2026-11-26 22:24 to 2026-11-27 15:09 UTC (16.8 h wall, 4 cores). **Every base closes.**

| item | value |
| --- | --- |
| shards (depth-6 `covergen` shards) | 1024 of 1024, every per-shard check passed |
| minimal-cover orbits (orderly representatives) | $482{,}629{,}287$ |
| covers by size: 15 / 16 / 17 classes | $897$ / $1{,}272{,}419$ / $481{,}355{,}971$ (none smaller: $\tau_{17}(251)=15$) |
| level-one bases processed (with repeats, see §2) | $647{,}472{,}221$ |
| closing level: 2 / 3 / 9 / 18 / 36 | $625{,}667{,}896$ / $21{,}742{,}149$ / $62{,}175$ / $1$ / $0$ |
| bases not closed by 36 | **0** |
| CPU | $228{,}100$ s $=63.4$ CPU-h; $1.049\cdot10^{11}$ `covergen` nodes (Knuth estimate $8.7\cdot10^{10}\pm8\%$) |

**Result.** Every base $b\in I(17,251,1)$ closes under the extended cascade at some level $L_b\in\{2,3,9,18\}$ (the cap was 36; no base needed it). None of these levels is divisible by $251$. By Remark L (`midprimes17.md` §1), $251$ divides $v_1\cdots v_{17}$ for every counterexample to LRC(17).

## 1. What the claim rests on

1. **Remark L and the extended cascade** (`midprimes17.md` §1–2: definitions, Lemma B, Remark L). These were proved and reviewed there.
2. **Lemma S** (`small-primes.md` §2). It needs LRC($m$) for $m\le15$. That is Allikvere's unrefereed 16-runner claim (Zenodo 10.5281/zenodo.23304361).
3. **Level-one completeness.**
   - *`covergen.c`'s search completeness* (minimal-cover enumeration), tested in `test_lonely.py`: 26 tests pass, including a new test that the union of shards equals the unsharded output.
   - *Toner's Lemma B.1* (orderly-root rule; proof checked, Approach 14). It is checked on real data at $k=17$:
     - orbit-set equality, orderly against full search, at $p=79,83,89,97,101$: $86{,}309$; $169{,}363$; $339{,}633$; $1{,}866{,}993$; $3{,}062{,}289$ orbits, all equal, with one cover per orbit;
     - at $p=251$, an independent Python re-implementation of the canonical test on four root branches. The canonical subsequence of the first $300{,}000$ non-orderly covers of branch 0 equals the orderly output in order ($125{,}554$ covers), and all $403{,}054$ orderly covers tested pass.
   - *The expansion.* Every base's support contains a minimal cover; the extra entries range over all classes with repetition; units map orbit members to each other. So expanding one cover per orbit reaches every base orbit at least once. The coordinator re-derived this argument.
   - **There is no full independent orbit count at $p=251$.** The non-orderly tree is about $6\times$ larger, and its shards do not line up with the orderly ones. §4 gives a heuristic comparison with the ladder estimate.
4. **The cascade code `xcascq.c`.** It is a copy of `midp17/xcasc.c` with a quiet output mode, and its normal-mode output is byte-identical to `xcasc` (tested). `xcasc` itself is tested in `midp17/test_midp17.py`.
   - Independent re-check with `k17struct/cascade_verify.c` (different code):
     - a 1% sample of all bases (every 100th base from the expander);
     - every base closing at level $\ge9$.
   - For the sampled bases closed at level 2, the batch check finds no level-2 survivor. For the others, the per-base chain $3,3,2,2$ closes at the same level as `xcascq`.
   - **The remaining level-2 and level-3 closures (99% of the bases) rest on `xcascq` alone.**
   - Totals: $6{,}474{,}223$ sampled bases (1%), with no level-2 survivor in the batch check. $279{,}284$ per-base re-runs (the sampled bases open after $\times2$, plus all $62{,}176$ bases closing at level $\ge9$) all agree with `xcascq` on the closing level.

## 2. Pipeline and checks

Per shard (`run_gate251.sh`):

`covergen` (`LRC_ORDERLY=1`, depth-6 shards) $\to$ `expand` (all 17-multisets containing the cover) $\to$ `xcascq` ($\times2$) $\to$ `xcascq` ($3,3,2,2$ from level one, on the bases still open)

- **Repeats.** A base containing several minimal-cover orbits is processed several times. That costs time but not soundness.
- **Retained data.** Only counts, the histogram, the open bases (none) and the bases closing at level $\ge9$ are kept.
- **Per-shard checks** (`shard_check.py`, JSON per shard):
  - covergen's `minimal_covers` equals the covers read by `expand`;
  - covers by size add up, and bases $=\sum_C\binom{h+16-|C|}{17-|C|}$;
  - the bases entering stage 1 equal the bases expanded;
  - the stage-1 open bases equal the stage-2 input;
  - nothing is open, capped, or has a level-one witness;
  - the histogram adds up to the bases;
  - the re-checks in §1.4 pass.
- **Binaries.** Shards 0–95 ran on the `covergen.c` build from before the path-flag fix (§3). Shards 96–1023 ran on the fixed build. Both are recorded in `binaries.txt`. At $k=17$, depth 6, the two builds coincide: covers have at least 15 classes, and the finish path starts only at depth 14. Old and new builds give identical covers on shards 1 and 7 (301,766 and 306,090).

## 3. Code changes

- **`covergen.c`.** `LRC_SHARD_DEPTH=D` now works for any $D\ge2$ (global count of the nodes at depth $D-1$).
  - The first version emitted the `LRC_FINISH` leaves above the cut in every shard at small $k$. The new test caught it.
  - Fix: a leaf goes to shard $r\ne0$ only if its path passed the shard filter.
  - `LRC_PRINTROOT` prints the root candidate list, for the orderly check.

## 4. Negative controls and heuristic comparisons

- **Lemma S off** (`xcascq -DNO_NG`). None of 40 production bases that close at level 9 closes by 36; with Lemma S, all 40 close at 9 (`test_gate251.py`).
- **$p=113$** ($\tau_{17}=11$). On the 300-base sample of `midp17`, 5 do not close by 36 (2 open, 3 capped), so the gate fails there, as expected. At $(7,43)$ the pipeline reports the gate as failed (test).
- **Small closing gate.** $(8,67)$ closes completely, with totals independent of the sharding (test).
- **Ladder comparison (heuristic).** Every base orbit is processed at least once, so the $647{,}472{,}221$ bases processed (with repeats) must be at least the number of base orbits. The ladder estimate of that number (`midprimes17.md` §3.2) is $6.19\cdot10^{8}$, about $\pm5\%$. The run is consistent with it. This is a necessary condition only, not a count.

**The level-18 base** is the tight orbit $(1,2,\dots,17)$: it retains 1 orbit at levels 3 and 9 and closes at 18, as at every prime $97\le p\le311$ (`midprimes17.md` §3.2). The results are in `gate251/results/`:
- `summary.json` (totals);
- `shards.jsonl` (one record per shard);
- `level_ge9_bases.jsonl.gz` (every base closing at level $\ge9$, with its trace);
- `binaries.txt`.

## 5. Reproduction

`run_gate251.sh WORKDIR 251` with `LO`/`HI` ranges (each under 2 h), then `summarize.py WORKDIR/p251`. Tests: `python3 -m pytest test_gate251.py` (5 tests, about 15 s) and `test_lonely.py` (26 tests, about 12 min).
