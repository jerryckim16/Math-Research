"""Build the 604-point kissing configuration in R^11 from the text of
Bianchi-Kwon-Pappu-Zou, "Harnessing the Collective Intelligence of AI Agents
in the Wild for New Discoveries" (EinsteinArena), arXiv:2606.10402v2,
Appendix "Kissing number construction (n = 604)". Our own code; no data or
code of the authors is used (einsteinarena.com and the Station data site are
refused by the proxy here).

Construction (coordinates 0..10):
  backbone B: +-2 e_i (i = 0..7), and all 16 sign patterns on each of 30
    supports of size 4:
      6 supports P_i u P_j (0 <= i < j <= 3), P0=(0,6) P1=(1,4) P2=(2,5) P3=(3,7);
      3 layers k = 8, 9, 10 of 8 supports T u {k}, T a triple meeting each
      pair P_i at most once.
  E1: +-e_a +- e_b +- sqrt2 u_j, (a,b) one of the P_i, j = 1,2,3   (96 points)
  E2: sqrt2 (+-u_i +- u_j), i < j                                  (12 points)
  with u1 = (2,1,2)/3, u2 = (2,-2,-1)/3, u3 = (1,2,-2)/3 in coordinates 8,9,10.

The appendix does not say WHICH 8 triples form each layer. The kissing
condition forces (norm-4 vectors with entries +-1): two supports in the same
layer share at most 2 coordinates, so their triples meet in at most one
element; supports in different layers must not have the same triple. We pick
the lexicographically first valid choice by backtracking (any valid choice
gives a 604-point configuration if the rest of the construction is right,
which the exact all-pairs check then decides). The choice is printed.

Scaling: every point is multiplied by 3 (angles unchanged), so the backbone
is integral (bulk, int8) and E1, E2 are C0 + C1 sqrt2 with integer C0, C1
(kiss_check_field.py format [C0, C1, 0, 0]).

Negative controls (--variant, each must FAIL the check):
  repeat   layer 9 reuses the first triple of layer 8 (same triple in two
           layers: the supports share 3 coordinates)
  pairmix  E1 additionally uses the non-pair (a,b) = (0,1) with u_1
           (8 extra points)

Usage: python3 -I build_einstein11.py OUTPREFIX [--variant repeat|pairmix]
Writes OUTPREFIX.i8 (496 x 11 int8) and OUTPREFIX_field.json (108 rows).
"""
import itertools
import json
import sys

import numpy as np

PAIRS = [(0, 6), (1, 4), (2, 5), (3, 7)]
U = [(2, 1, 2), (2, -2, -1), (1, 2, -2)]          # 3 * u_j


def transversal_triples():
    out = []
    for ps in itertools.combinations(range(4), 3):
        for pick in itertools.product((0, 1), repeat=3):
            out.append(tuple(sorted(PAIRS[p][s] for p, s in zip(ps, pick))))
    return sorted(out)                                 # 32 triples


def choose_layers():
    tri = transversal_triples()
    layers = [[], [], []]
    used = set()

    def ok(layer, t):
        return all(len(set(t) & set(s)) <= 1 for s in layer)

    def rec(li):
        if li == 3:
            return True
        if len(layers[li]) == 8:
            return rec(li + 1)
        start = tri.index(layers[li][-1]) + 1 if layers[li] else 0
        for t in tri[start:]:
            if t not in used and ok(layers[li], t):
                layers[li].append(t)
                used.add(t)
                if rec(li):
                    return True
                layers[li].pop()
                used.discard(t)
        return False

    if not rec(0):
        raise SystemExit("no valid choice of layers")
    return layers


def build(variant=None):
    layers = choose_layers()
    if variant == "repeat":
        layers[1][0] = layers[0][0]
    supports = [PAIRS[i] + PAIRS[j] for i, j in itertools.combinations(range(4), 2)]
    for k, layer in zip((8, 9, 10), layers):
        supports += [t + (k,) for t in layer]
    assert len(supports) == 30 and len(set(map(frozenset, supports))) == 30
    bulk = []
    for i in range(8):
        for s in (2, -2):
            v = [0] * 11
            v[i] = 3 * s
            bulk.append(v)
    for sup in supports:
        for signs in itertools.product((1, -1), repeat=4):
            v = [0] * 11
            for c, s in zip(sup, signs):
                v[c] = 3 * s
            bulk.append(v)
    field = []
    e1 = [(ab, j) for ab in PAIRS for j in range(3)]
    if variant == "pairmix":
        e1.append(((0, 1), 0))
    for (a, b), j in e1:
        for sa, sb, su in itertools.product((1, -1), repeat=3):
            c0 = [0] * 11
            c1 = [0] * 11
            c0[a], c0[b] = 3 * sa, 3 * sb
            for t in range(3):
                c1[8 + t] = su * U[j][t]
            field.append([c0, c1, [0] * 11, [0] * 11])
    for i, j in itertools.combinations(range(3), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            c1 = [0] * 11
            for t in range(3):
                c1[8 + t] = si * U[i][t] + sj * U[j][t]
            field.append([[0] * 11, c1, [0] * 11, [0] * 11])
    assert variant or (len(bulk) == 496 and len(field) == 108)
    return layers, np.array(bulk, dtype=np.int8), field


def main(prefix, variant=None):
    layers, bulk, field = build(variant)
    for k, layer in zip((8, 9, 10), layers):
        print(f"layer {k}: {layer}")
    bulk.tofile(prefix + ".i8")
    with open(prefix + "_field.json", "w") as f:
        json.dump({"d": 11, "rows": field}, f)
    print(f"bulk {bulk.shape[0]} rows -> {prefix}.i8; field {len(field)} rows "
          f"-> {prefix}_field.json; total {bulk.shape[0] + len(field)}")


if __name__ == "__main__":
    v = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else None
    main(sys.argv[1], v)
