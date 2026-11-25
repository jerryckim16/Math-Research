# Lonely Runner: exact checker and prime-gate sieve

Companion to [`problems/lonely-runner.md`](../../problems/lonely-runner.md).
Everything is exact integer or `Fraction` arithmetic. There is no floating point in any decision.

| file | what it does |
| --- | --- |
| `lonely.py` | Single-tuple checker. `find_witness(v, delta)` decides whether some real t has all `‖v_i t‖ ≥ delta`. It returns either a rational witness or a checkable certificate that none exists, using a complete search over the left endpoints of the good intervals; the proof is in the module docstring. `max_loneliness(v)` computes `ML(v) = max_t min_i ‖v_i t‖` exactly. The maximum is attained at some `t = a/(v_i+v_j)`; the proof is also in the docstring. |
| `sieve.py` | The prime-gate sieve: the sets I(k,p,l), lifting, projection, orbit canonicalisation and the exact test `prod P ≥ B_k`. The definitions follow arXiv:2604.23906, §2–3. |
| `level1.c` | Optional C engine for the level-1 step. It does the same enumeration and the same test as `sieve.level1_improper`, but about 100× faster. It is cross-checked in the tests. |
| `covergen.c` | Step 2: level-one generator by minimal covers. The completeness proof is in its header. Also has a cost-estimation mode: Knuth random probes plus a capped timed DFS. Step 6: `LRC_PRUNE` (private-time pruning). Step 7: `LRC_IRR` (sharper gain bound = 2, redundancy cuts = 1; same output). Step 11: `LRC_TWOBRANCH=1`, Allikvere's two-branch split (|C| = k and |C| ≤ k−1 searched separately). Same output and no node reduction, so it is not recommended. The Knuth probe now applies the `LRC_PRUNE` q-cut. Step 12: `LRC_ORDER=1` orders children by descending gain and adds the child-gain cutoff, and `LRC_IRR` bit 4 is an incremental redundancy cut. Both keep the same output and are about 2.7× faster at (14,251). Recommended: `LRC_PRUNE=2 LRC_IRR=2 LRC_ORDER=1`, or `LRC_IRR=6` at small p. |
| `liftfree.c` | Step 2: all witness-free lifts of given tuples from level M to level cM, by branch and bound over the lift digits. Tuples are read from stdin. Step 7: `sieve.lift_c` uses it for every lift with c^k > 65,536 (unless `LRC_LIFT=py`), e.g. the ×11 lift for LRC(10). |
| `check_allikvere.py` | Step 2: independent spot check of Allikvere's LRC(14) gate certificates. The Zenodo archives are read as data and never executed. |
| `flag_bound.py` | Step 2: exact re-derivation of Allikvere's flag-bound constants for n = 13 and 14, extended to n = 15. Its one-variable shape value for n = 15 is a float estimate; the proof is in `shape_lemma.py`. |
| `flag_theorem_check.py` | Step 10: exact machine checks for the general-n parts of Allikvere's Theorem 3.8. Lemma 3.1 inclusion: the vertex identity and exact samples. Lemma 3.2 covolume: an exact Hermite basis of P Z^n and Gram determinants. Lemma 3.6 product minimization: brute-force vertex enumeration for d ≤ 7, and all block points at n = 13–15. Also the n = 15 log bound to 40 digits. Written verification: problem file, Approach 11. Tests: `test_flag_theorem.py`. |
| `shape_lemma.py` | Step 9: Allikvere's shape Lemma 3.7 run for general n, with every identity and inequality checked in exact rational arithmetic. Re-proves R_13 < 101/200 and R_14 < 1/2 and proves R_15 < 49/100 (written proof: problem file, Approach 10). Tests: `test_shape_lemma.py`. |
| `tight_orbit_k15.py` | Step 2: binary cascade of (1..15) at the candidate gate primes for 16 runners. |
| `cost_estimate.py` | Step 2: measured-basis cost estimate for LRC(15). |
| `gatecheck.c` | Step 3: per-row binary cascade (levels 2–32) and per-orbit level-15 kill for LRC(14) gates. The kill does level-3/5 witness-free lifts, CRT, the level-15 grid, the gcd clause and the near-gcd Lemma 3.12. |
| `canon.c` | Step 3: unit-orbit canonical forms of level-one multisets, with dedup (`rows`, `expand`) or per line (`each`). |
| `check_gate_full.py` | Step 3: full re-check of one LRC(14) gate archive (or a seeded random sample): SHA-256, stored rows improper, cascade per orbit, persistent orbits, every kill record. Step 8: optional `KILL_SAMPLE` (0 = skip the kill) for a full cascade with a sampled or separate kill. |
| `run_lrc14_batch.sh` | Step 3: batch driver writing `results/lrc14_gates/gate_<p>.json`. |
| `completeness_check.py` | Step 3: level-one completeness. It regenerates I(14,p,1) with `covergen.c` (no private-time pruning) and compares orbit sets with the certificate's stored rows. |
| `check_lrc13_kills.py` | Step 3: LRC(13) archive. It checks the kill files' SHA-256 against the gate manifests and recomputes the level-14 kill of the two persistent orbits. |
| `coverage_table.py` | Step 4: per-gate coverage table for all 71 LRC(14) gates → `results/lrc14_gates/COVERAGE.md`. |
| `check_gate_stream.py`, `run_big_gates.sh` | Step 5: streaming re-check for large archives (up to 1.6 GB). Every stored row is tested in C (`gatecheck hexrows`); cascade and kill run on seeded reservoir samples. Archives are downloaded, checked and deleted one at a time. |
| `prove_small.py` | End-to-end reproduction of LRC(k) for small k. It walks primes upwards, runs the sieve chain at each one, and stops once the product of the successful gate primes reaches B_k. |
| `exhaustive.py` | Direct bounded check over all primitive tuples with max speed ≤ N. It also lists the tight tuples, i.e. those with ML = 1/(n+1). |
| `test_lonely.py` | Tests (21). See the list below. |
| `results/` | Raw logs of the runs reported in the problem file. Every gate is listed, including the failed ones. |

## Reproduce

```
python3 -m unittest -v test_lonely        # ~30 s
python3 prove_small.py 3                  # LRC(3): instant
python3 prove_small.py 4
python3 prove_small.py 5
python3 prove_small.py 6                  # ~50 s, pure Python
LRC_USE_C=1 python3 prove_small.py 7      # ~30 s
LRC_USE_C=1 python3 prove_small.py 8 47 2,2,2,p,3,3 4   # 4 processes, see results/lrc_k8.jsonl
LRC_LEVEL1=cover python3 prove_small.py 9 137 2,2,2,p,5,2 4   # LRC(9), cover generator
LRC_LEVEL1=cover python3 prove_small.py 10 127 2,2,2,p,11 4  # LRC(10), x11 lift via liftfree.c
python3 flag_bound.py
python3 shape_lemma.py
python3 flag_theorem_check.py
python3 tight_orbit_k15.py              # ~1 min
# Allikvere spot check (download from Zenodo 10.5281/zenodo.22667683 first):
python3 check_allikvere.py SHA256SUMS.txt evidence_401_s0.tgz evidence_397_s0.tgz ...
python3 cost_estimate.py path/to/inputs/gates.json   # from fifteen_runners_manuscript_source.zip
python3 exhaustive.py 4 60
```

## What the tests check

- The checker:
  - `ML(1..n) = 1/(n+1)` for n ≤ 10, and the Goddyn–Wong tight tuple (1,3,4,7) has ML = 1/5.
  - `find_witness` agrees with `max_loneliness` on 300 random tuples, at thresholds just above and just below ML.
  - ML is attained at the reported t and dominates a 600-point grid.
  - No-witness certificates pass the independent checker, and tampered certificates are rejected.
- The sieve:
  - The orbit sets from `level1_improper` and `lift` equal a brute force over all of Z_{p,l}^k straight from the definition, with no symmetry reduction and no bitsets. This was checked for several (k, p, l), including a two-step lift.
  - The tight tuple (1..k) survives exactly until (k+1) | l (Remark 3.2 of arXiv:2604.23906).
  - A witness m/N for w transfers to random integer tuples u ≡ w (mod N).
  - The C engine agrees with the Python engine.
  - The B_k arithmetic matches the value `log B_13 < 670.3498` quoted in the abstract of arXiv:2609.02604.

- Step 12: `LRC_ORDER=1` and `LRC_IRR` bits 4/6 print exactly the plain minimal covers on 5 (k,p) pairs × 2 prune levels × 4 settings, and also under sharding (`test_covergen_order_same_minimal_covers`).
- Step 11: `LRC_TWOBRANCH=1` prints exactly the single-tree minimal covers on 5 (k,p) pairs × 3 cut settings (`test_covergen_twobranch_same_minimal_covers`).
- Step 10 (`test_flag_theorem.py`): the inclusion, covolume and product-minimization checks at random and actual instances. Negative controls: a fatter ellipsoid leaves D, a wrong F fails the covolume, and with c_{i+1}/c_i < 4/3 a geometric block beats ∏c. Also the n = 14 log bound matches the paper.
- Step 9 (`test_shape_lemma.py`): `shape_lemma.py` reproduces the paper's Lemma 3.7 objects for n = 13 and 14 (interior polynomials, cubics, intervals) and its bounds. All n = 15 checks pass. Negative controls: targets above the true minimum fail. A float search over the 15-dimensional domain never goes below the target. An optional sympy check covers the identities with the real exponent u^(2/n).
- Step 6: `covergen.c` with `LRC_PRUNE=1` (Lemma 4.1) and `=2` (max-private normalisation) gives the same orbit sets as unpruned on 5 (k,p) pairs, including (14,89).
- Step 7: `covergen.c` with `LRC_IRR` = 1, 2, 3 prints exactly the same minimal covers as plain on 6 (k,p) pairs (also sharded), and `LRC_PRUNE=2` + `LRC_IRR=2` keeps the (14,89) orbit set. `sieve.lift_c` (liftfree.c) equals `sieve.lift` at levels 1 and 2.
- Step 4: `covergen.c` sharding (`LRC_NSHARDS`/`LRC_SHARD`) gives exactly the unsharded output.
- Step 2:
  - The cover generator equals the naive enumerator on a sample of (k, p). 125 pairs were checked during development.
  - `liftfree.c` plus the gcd clause equals the Python `lift`.
  - The flag constants equal Allikvere's published values.

## Trust base for the LRC(k) reproductions

1. **B_k.** The Malikiosis–Santos–Schymura theorem, in the form of Rosenfeld's Corollary 3: a gcd-1 counterexample to LRC(k) has `u_1⋯u_k < B_k = (C(k+1,2)^(k-1)/k)^k`, provided LRC(k−1) holds. It is cited and not re-proved here.
2. **The elementary lemmas** F1, F2, the divisibility lemma, and "J empty ⇒ I(k,p,l) empty for some l". Proofs are written out in the problem file.
3. **Correctness of `sieve.py` / `level1.c`.** Supported by the brute-force tests above. Not formally verified.
4. **LRC(2).** Classical (3 runners).
