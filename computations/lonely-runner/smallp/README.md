# smallp: small primes as gates (shift lemma, covering numbers, audit)

Write-up: [`notes/lonely-runner/small-primes.md`](../../../notes/lonely-runner/small-primes.md).
All decisions use exact integer or Fraction arithmetic.

| file | what it does |
| --- | --- |
| `mincover.c` | Covering number tau_k(p), by exhaustive DFS. `mincover k p` prints `p tau nodes cover`; `mincover k p enum s` lists every minimal cover with class 1 and at most s classes. |
| `tau.py` | The same tau_k(p) via SAT (pysat/CaDiCaL), used as a cross-check at k = 14, p = 83–113. |
| `shift_lemma_check.py` | Exact checks of the finite steps of the weighted shift lemma (arc count, shift multiplicity), plus a negative control. |
| `terminal15.py` | Independent re-derivation of Allikvere's k = 15 terminal step (weighted shift with d = 4, then the level-8 test) from his persistent orbits in `SUMMARY.json`, which is read as data. |
| `cascade15x.py`, `xcascade.py` | Binary or general-chain cascade with extended properness: witness, gcd clause, or the shift lemma at every d \| l. `xcascade.py k tight PMIN PMAX CHAIN` runs the tight tuple. |
| `xbatch.py` | Batch version of the extended cascade for many orbits. |
| `results/` | `tau14.txt`, `tau15.txt`, `tau17.txt`, `terminal_k15_allikvere.jsonl` (p = 191, 223, 251; exact agreement with his records), `covers13_k15_p191.txt`, `tight17.jsonl`. |

Two caveats on `results/`:

- `tau14.txt`: the rows for p = 83–109 come from `tau.py` (format "p tau"), the rest from `mincover.c`.
- A missing prime in `tau17.txt` means the search hit its 120 s timeout.

Run:

```
cc -O2 -o mincover mincover.c && ./mincover 17 173
python3 shift_lemma_check.py
python3 terminal15.py path/to/out15_191/SUMMARY.json      # ~15 min, 1 core
python3 xcascade.py 17 tight 97 113 2,3,3,2
```
