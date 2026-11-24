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
| `run_tree.py` | Resumable driver: all argmax branches with a time limit, timeouts split into cubes and finer layers (`cegar_branches.refine`); every finished region is appended and flushed at once. Options of `cegar_branches.py`: `--arith 2` (Z3 `smt.arith.solver=2`), `--lemma-m` (AFM Lemma M items 2–3), `--c0` (Lemma C0′), `--multi K`, `--seed-points P`. |
| `pack_certs.py` | Packs a driver output into a gzipped certificate file (allocations as digit strings). |
| `box_runs.py` | CEGAR in small ℓ∞ boxes around the hardest profiles found by annealing (local exhaustive search). |
| `rules_m10.py` | Failed route: AFM's Lemma L1 rule and "tops + round robin" at m = 10. |
| `summarize.py` | Aggregates `data/*.jsonl` into the coverage numbers and scans for counterexample flags. |
| `data/` | JSONL logs of every run reported in the problem file. `speedups_n4.jsonl`: the speed-up measurements (problem file, Approach 4a). `m8_tree_certs.jsonl.gz`: the m = 8 refinement-tree records (unsat certificates and timeouts); `m8_run_summary.txt`: its coverage and verification status; `m8_cvc5_verdicts.txt`: cvc5 verdicts per record (sha256 of the record → verdict; pass a fresh `--log` file to re-verify from scratch rather than reuse them); `cegar_m10_distinct_sample.jsonl`: four m = 10 distinct-favourites regions. |

Reproduce: `python3 test_efx.py`, then the commands listed in the problem
file's Results table. Requirements: gcc, Python 3, `pip install z3-solver`
(tested with 5.4.1), and `pip install cvc5` for `recheck_cvc5.py`.
