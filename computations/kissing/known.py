"""Known kissing configurations as integer row matrices, for validation.

D4 roots (24 in R^4), D5 roots (40 in R^5), E8 roots (240 in R^8, scaled by 2),
and the minimal vectors of the Leech lattice (196560 in R^24, scaled by
sqrt(8)). Each function returns a list of integer tuples. Self-checks of the
Golay code (size and weight enumerator) are in golay_code().
"""
import itertools


def roots_D(n):
    """All (+-1, +-1, 0, ..., 0) permutations: 2n(n-1) vectors, norm 2."""
    out = []
    for i, j in itertools.combinations(range(n), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [0] * n
                v[i], v[j] = si, sj
                out.append(tuple(v))
    return out


def roots_E8_scaled():
    """E8 roots times 2: D8 roots times 2 (112) and (+-1)^8 with an even
    number of minus signs (128). Squared norm 8."""
    out = [tuple(2 * x for x in v) for v in roots_D(8)]
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            out.append(signs)
    return out


def golay_code():
    """Extended binary Golay code [24,12,8] as a list of 4096 0/1 tuples,
    from the cyclic [23,12,7] code with generator
    g(x) = x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1, plus a parity bit."""
    g = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]  # coefficients of x^0..x^11
    basis = []
    for s in range(12):
        v = [0] * 23
        for i, c in enumerate(g):
            v[i + s] = c
        basis.append(v + [sum(v) % 2])
    words = set()
    for coeffs in itertools.product((0, 1), repeat=12):
        w = [0] * 24
        for c, b in zip(coeffs, basis):
            if c:
                w = [(x + y) % 2 for x, y in zip(w, b)]
        words.add(tuple(w))
    words = sorted(words)
    wd = {}
    for w in words:
        wd[sum(w)] = wd.get(sum(w), 0) + 1
    assert len(words) == 4096, len(words)
    assert wd == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}, wd
    return words


def leech_min_scaled():
    """The 196560 minimal vectors of the Leech lattice, scaled by sqrt(8)
    (squared norm 32), in the standard Golay-code coordinates
    (Conway-Sloane, SPLAG ch. 4, sec. 11)."""
    code = golay_code()
    octads = [w for w in code if sum(w) == 8]
    out = []
    # shape (+-2^8, 0^16): support an octad, even number of minus signs
    for w in octads:
        supp = [i for i in range(24) if w[i]]
        for signs in itertools.product((1, -1), repeat=8):
            if signs.count(-1) % 2 == 0:
                v = [0] * 24
                for i, s in zip(supp, signs):
                    v[i] = 2 * s
                out.append(tuple(v))
    # shape (-+3, +-1^23): (1^24) - 4 e_i, with signs flipped on a codeword
    for w in code:
        for i in range(24):
            base = [1] * 24
            base[i] = -3
            v = tuple(-x if w[k] else x for k, x in enumerate(base))
            out.append(v)
    # shape (+-4, +-4, 0^22)
    for i, j in itertools.combinations(range(24), 2):
        for si in (4, -4):
            for sj in (4, -4):
                v = [0] * 24
                v[i], v[j] = si, sj
                out.append(tuple(v))
    assert len(out) == 196560 and len(set(out)) == 196560
    return out


CONFIGS = {
    "D4": (4, lambda: roots_D(4), 24),
    "D5": (5, lambda: roots_D(5), 40),
    "E8": (8, roots_E8_scaled, 240),
    "Leech": (24, leech_min_scaled, 196560),
}


def write_i8(rows, path):
    import array
    a = array.array("b", [x for r in rows for x in r])
    with open(path, "wb") as f:
        a.tofile(f)


if __name__ == "__main__":
    import sys
    name, path = sys.argv[1], sys.argv[2]
    d, fn, n = CONFIGS[name]
    rows = fn()
    assert len(rows) == n and all(len(r) == d for r in rows)
    write_i8(rows, path)
    print(name, d, len(rows), path)
