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
| `recheck_cvc5.py` | Independent re-check of stored certificates: its own encoding, full clauses, cvc5, and a coverage check of all branches. |
| `box_runs.py` | CEGAR in small ℓ∞ boxes around the hardest profiles found by annealing (local exhaustive search). |
| `rules_m10.py` | Failed route: AFM's Lemma L1 rule and "tops + round robin" at m = 10. |
| `summarize.py` | Aggregates `data/*.jsonl` into the coverage numbers and scans for counterexample flags. |
| `data/` | JSONL logs of every run reported in the problem file. |

Reproduce: `python3 test_efx.py`, then the commands listed in the problem
file's Results table. Requirements: gcc, Python 3, `pip install z3-solver`
(tested with 5.4.1), and `pip install cvc5` for `recheck_cvc5.py`.
