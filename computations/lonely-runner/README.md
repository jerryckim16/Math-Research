# Lonely Runner: exact checker and prime-gate sieve

Companion to [`problems/lonely-runner.md`](../../problems/lonely-runner.md).
Everything is exact integer or `Fraction` arithmetic. There is no floating point in any decision.

| file | what it does |
| --- | --- |
| `lonely.py` | Single-tuple checker. `find_witness(v, delta)` decides whether some real t has all `‖v_i t‖ ≥ delta`. It returns either a rational witness or a checkable certificate that none exists, using a complete search over the left endpoints of the good intervals; the proof is in the module docstring. `max_loneliness(v)` computes `ML(v) = max_t min_i ‖v_i t‖` exactly. The maximum is attained at some `t = a/(v_i+v_j)`; the proof is also in the docstring. |
| `sieve.py` | The prime-gate sieve: the sets I(k,p,l), lifting, projection, orbit canonicalisation and the exact test `prod P ≥ B_k`. The definitions follow arXiv:2604.23906, §2–3. |
| `level1.c` | Optional C engine for the level-1 step. It does the same enumeration and the same test as `sieve.level1_improper`, but about 100× faster. It is cross-checked in the tests. |
| `covergen.c` | Step 2: level-one generator by minimal covers. The completeness proof is in its header. Also has a cost-estimation mode: Knuth random probes plus a capped timed DFS. |
| `liftfree.c` | Step 2: all witness-free lifts of given tuples from level M to level cM, by branch and bound over the lift digits. Tuples are read from stdin. |
| `check_allikvere.py` | Step 2: independent spot check of Allikvere's LRC(14) gate certificates. The Zenodo archives are read as data and never executed. |
| `flag_bound.py` | Step 2: exact re-derivation of Allikvere's flag-bound constants for n = 13 and 14, extended to n = 15. The n = 15 shape factor is heuristic. |
| `tight_orbit_k15.py` | Step 2: binary cascade of (1..15) at the candidate gate primes for 16 runners. |
| `cost_estimate.py` | Step 2: measured-basis cost estimate for LRC(15). |
| `prove_small.py` | End-to-end reproduction of LRC(k) for small k. It walks primes upwards, runs the sieve chain at each one, and stops once the product of the successful gate primes reaches B_k. |
| `exhaustive.py` | Direct bounded check over all primitive tuples with max speed ≤ N. It also lists the tight tuples, i.e. those with ML = 1/(n+1). |
| `test_lonely.py` | Tests (17). See the list below. |
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
python3 flag_bound.py
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

- Step 2:
  - The cover generator equals the naive enumerator on a sample of (k, p). 125 pairs were checked during development.
  - `liftfree.c` plus the gcd clause equals the Python `lift`.
  - The flag constants equal Allikvere's published values.

## Trust base for the LRC(k) reproductions

1. **B_k.** The Malikiosis–Santos–Schymura theorem, in the form of Rosenfeld's Corollary 3: a gcd-1 counterexample to LRC(k) has `u_1⋯u_k < B_k = (C(k+1,2)^(k-1)/k)^k`, provided LRC(k−1) holds. It is cited and not re-proved here.
2. **The elementary lemmas** F1, F2, the divisibility lemma, and "J empty ⇒ I(k,p,l) empty for some l". Proofs are written out in the problem file.
3. **Correctness of `sieve.py` / `level1.c`.** Supported by the brute-force tests above. Not formally verified.
4. **LRC(2).** Classical (3 runners).
