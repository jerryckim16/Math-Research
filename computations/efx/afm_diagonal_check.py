"""Re-check the two "diagonal" exhibits of Alkassar-Fouz-Mehlhorn
(arXiv:2608.08590v1, Sec. 'Why it is hard'): four identical rows vA, vB.
Claimed: vA has 1680 EFX_0 allocations, each giving good 0 a bundle of size
exactly 1; vB has 5544, each giving good 0 a bundle of size exactly 2.
Pure-Python enumeration of all 4^9 allocations (independent of efxcore.c)."""
import collections
import efx

vA = [9200, 120, 100, 99, 98, 97, 96, 95, 95]
vB = [1200, 1110, 1099, 1099, 1099, 1099, 1098, 1098, 1098]
for name, row in (("vA", vA), ("vB", vB)):
    allocs = efx.brute([row] * 4, want_all=True)
    sizes = collections.Counter(sum(1 for g in range(9) if a[g] == a[0]) for a in allocs)
    print(name, "EFX allocations:", len(allocs), "size of good 0's bundle:", dict(sizes))
