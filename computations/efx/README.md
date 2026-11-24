# EFX allocations: exact checker, adversarial search, CEGAR certifier

See `problems/efx-allocations.md` for the statement, literature and results.

| file | what it does |
| --- | --- |
| `efxcore.c` | Exact EFX₀ existence checker in C (built automatically into `libefx.so` by `efx.py`). It enumerates set partitions into ≤ n blocks and matches agents to blocks. There are Σ_{k≤4} S(m,k) partitions (43,947 for m = 10), not 4^m allocations. Exact int64 arithmetic. |
| `efx.py` | Python wrapper with `exists`, `full` (count + max–min slack score), `score` (branch-and-bound objective). It also has two pure-Python functions that do not depend on the C code: `verify(v, alloc)` checks the definition directly, and `brute` enumerates all n^m allocations. |
| `test_efx.py` | Tests. C vs brute force (existence **and** exact counts) on 400 random tiny instances with zeros and ties. Known theorems on random instances: n = 2, n = 3, identical valuations, m ≤ n+3. Witness verification. AFM's two diagonal exhibits (counts 1680 and 5544). Run `python3 test_efx.py`. |
| `afm_diagonal_check.py` | Pure-Python re-check of AFM's exhibits vA, vB, including the bundle size of the top good. |
| `search.py` | Adversarial search for 4 agents. `random` mode draws from 10 instance families; `climb` mode does simulated annealing on valuations, minimising either the max–min slack ("score") or the number of EFX allocations ("count"). Any instance without EFX is re-verified (fast, full, brute) and logged with `COUNTEREXAMPLE_CANDIDATE`. |
| `cegar.py` | Z3 QF_LRA counterexample-guided search over a polyhedral valuation region. An `unsat` answer certifies (modulo Z3) that no counterexample exists in the region. Each `sat` model is an adversarial instance and is checked exactly. `recheck` re-solves from scratch with the full, unreduced clauses. |
| `cegar_branches.py` | Runs `cegar.py` over the argmax branches b₁ ≤ … ≤ b_{n−1}, which cover the normalised space up to symmetry. |
| `recheck_cvc5.py` | Independent re-check of stored certificates: its own encoding, full clauses, cvc5, and a coverage check of all branches (`--cover`) or of a refinement tree of any depth (`--tree`); `--workers=4` runs in parallel; reads `.jsonl` and `.jsonl.gz`. |
| `run_tree.py` | Resumable driver: all argmax branches with a time limit, timeouts split into cubes and finer layers (`cegar_branches.refine`); every finished region is appended and flushed at once. `--split-roots` starts from the cubes of the `--only` roots instead of running the roots themselves. Options of `cegar_branches.py`: `--arith 2` (Z3 `smt.arith.solver=2`), `--lemma-m` (AFM Lemma M items 2–3), `--c0` (Lemma C0′), `--multi K`, `--seed-points P`. |
| `probe_regions.py` | Cost probe: `plan` draws random children (fixed seed) of a region, `run` times them with the run_tree.py options (resumable, one flushed record per region, Z3 re-solve time and, for timeouts, the allocations found), `cvc5` times `recheck_cvc5.check_record` on the closed records. |
| `estimate_tree.py` | Stratified / Knuth-style projection of a full refinement-tree run from `probe_regions.py` records; timeouts are counted at their time limit, so the numbers are lower bounds whenever a timeout occurs. |
| `pack_certs.py` | Packs a driver output into a gzipped certificate file (allocations as digit strings). |
| `box_runs.py` | CEGAR in small ℓ∞ boxes around the hardest profiles found by annealing (local exhaustive search). |
| `rules_m10.py` | Failed route: AFM's Lemma L1 rule and "tops + round robin" at m = 10. |
| `summarize.py` | Aggregates `data/*.jsonl` into the coverage numbers and scans for counterexample flags. |
| `data/` | JSONL logs of every run reported in the problem file. `speedups_n4.jsonl`: the speed-up measurements (problem file, Approach 4a). `m8_tree_certs.jsonl.gz`: the m = 8 refinement-tree records (unsat certificates and timeouts); `m8_run_summary.txt`: its coverage and verification status; `m9_probe_n4.jsonl`: m = 9 timing probes: the first three lines are the third session's (branches (2,2,6), (0,1,6), cube (2,0),(2,0),(6,0)); the rest are the fourth session's random sample (`probe_regions.py` records with a `probe` field; allocations as digit strings); `m9_cvc5_times.jsonl`: cvc5 times on closed m = 9 sample records (three lines are lower bounds of stopped checks); `m8_single_agent_split.jsonl`: failed speed-up probe (single-agent split of m = 8 branches (6,6,6) and (3,3,3), problem file "m = 9 cost sample"); `m8_probe_cubes_226.jsonl.gz`: 125 cubes of branch (2,2,6), the failed cube re-closure probe (not part of the cover); `m8_cvc5_verdicts.txt`: cvc5 verdicts per record (sha256 of the record → verdict; pass a fresh `--log` file to re-verify from scratch rather than reuse them); `cegar_m10_distinct_sample.jsonl`: four m = 10 distinct-favourites regions. |

Reproduce: `python3 test_efx.py`, then the commands listed in the problem
file's Results table. Requirements: gcc, Python 3, `pip install z3-solver`
(tested with 5.4.1), and `pip install cvc5` for `recheck_cvc5.py`.
