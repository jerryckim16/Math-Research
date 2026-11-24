"""Independent replay of Andrews-Curtis (AC) move certificates.

Written here from the move definitions in Carreras, arXiv:2607.23611v1, Sec. 2,
WITHOUT reading or importing the author's verifier (ac_verify.py).

Words in the free group F(x, y) are tuples of nonzero ints: 1 = x, 2 = y,
-1 = x^-1, -2 = y^-1.  A state is a pair (r1, r2) of freely reduced words.

Elementary moves (each is a classical AC move, or a composite of them):
  ["invert", i]       r_i <- r_i^-1
  ["mul", i, j, e]    r_i <- r_i r_j^e      (i != j, e = +-1)
  ["conj", i, g]      r_i <- g r_i g^-1     (g a generator or inverse)
  ["cycle", i, k]     r_i <- u^-1 r_i u where u = first (k mod |r_i|) letters
                      of r_i; i.e. r = uv -> vu (a conjugation)
All results are freely reduced.  Every move is invertible by AC moves, so a
sequence P -> Q proves P ~AC Q in both directions.

Equivalence certificates end at a state `reached` that should be a member of
the orbit of `target` under swap / invert / rotate.  Instead of trusting an
orbit argument, `bridge()` writes out explicit elementary moves (rotation =
conjugation, inversion, and the 6-move swap) that take `reached` EXACTLY to
`target`, and `prove_named()` does the same from/to presentations built here
from their textbook definitions.  The final check is always: replaying one
explicit move list from presentation A gives exactly presentation B.

Usage: python3 ac_check.py CERT.json [...]      (replay + report)
       python3 ac_check.py --theorems CERTDIR   (Theorems 1-4 of 2607.23611)
"""
import json
import sys

GENS = (1, -1, 2, -2)


def reduce(w):
    out = []
    for a in w:
        if a not in GENS:
            raise ValueError(f"bad letter {a!r}")
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inv(w):
    return tuple(-a for a in reversed(w))


def word(s):
    """Parse 'x^-1 y^2 x y^-3' style strings (spaces between factors)."""
    letters = {"x": 1, "y": 2}
    out = []
    for tok in s.split():
        base, _, exp = tok.partition("^")
        e = int(exp) if exp else 1
        g = letters[base]
        out.extend([g if e > 0 else -g] * abs(e))
    return reduce(out)


def apply(state, mv):
    r = list(state)
    op = mv[0]
    if len(mv) < 2 or mv[1] not in (0, 1) or isinstance(mv[1], bool):
        raise ValueError(f"bad relator index {mv}")
    if op == "invert":
        (i,) = mv[1:]
        r[i] = inv(r[i])
    elif op == "mul":
        i, j, e = mv[1:]
        if i == j or e not in (1, -1):
            raise ValueError(f"illegal mul {mv}")
        r[i] = reduce(r[i] + (r[j] if e == 1 else inv(r[j])))
    elif op == "conj":
        i, g = mv[1:]
        if g not in GENS:
            raise ValueError(f"illegal conj {mv}")
        r[i] = reduce((g,) + r[i] + (-g,))
    elif op == "cycle":
        i, k = mv[1:]
        if not isinstance(k, int) or isinstance(k, bool):
            raise ValueError(f"illegal cycle {mv}")
        n = len(r[i])
        u = r[i][: (k % n)] if n else ()
        r[i] = reduce(inv(u) + r[i] + u)
    else:
        raise ValueError(f"unknown move {mv}")
    return tuple(r)


def replay(state, moves):
    """Replay moves; return (final_state, stats)."""
    state = tuple(reduce(w) for w in state)
    packaged = classical = 0
    peak_total = sum(map(len, state))
    peak_single = max(map(len, state))
    for mv in moves:
        if mv[0] == "cycle":
            n = len(state[mv[1]])
            k = mv[2] % n if n else 0
            classical += min(k, n - k)
        else:
            classical += 1
        packaged += 1
        state = apply(state, mv)
        peak_total = max(peak_total, sum(map(len, state)))
        peak_single = max(peak_single, max(map(len, state)))
    return state, dict(packaged=packaged, classical=classical,
                       peak_total=peak_total, peak_single=peak_single)


# --- explicit bridges inside the swap/invert/rotate orbit -------------------

def conj_word_moves(i, u):
    """Moves conjugating r_i by the word u (r_i <- u r_i u^-1)."""
    return [["conj", i, g] for g in reversed(u)]


def swap_moves(state):
    """Explicit AC moves taking (a, b) to (b, a):
    (a,b) -> (ab,b) -> (ab,b^-1) -> (ab, b^-1 ab) -> conj by b: (ab, ab b^-1)=(ab,a)
          -> (ab a^-1, a) -> conj by a^-1: (b, a)."""
    a, b = state
    mv = [["mul", 0, 1, 1], ["invert", 1], ["mul", 1, 0, 1]]
    mv += conj_word_moves(1, b)           # b (b^-1 a b) b^-1 = a
    mv += [["mul", 0, 1, -1]]             # (a b a^-1, a)
    mv += conj_word_moves(0, inv(a))      # a^-1 (a b a^-1) a = b
    return mv


def match_relator(r, t):
    """Moves on relator slot taking word r to word t by inversion and/or
    rotation (conjugation), or None.  Both must be cyclically reduced."""
    for flip in (False, True):
        w = inv(r) if flip else r
        n = len(w)
        if n != len(t):
            continue
        for k in range(max(n, 1)):
            if w[k:] + w[:k] == t:
                return flip, k
    return None


def bridge(state, target):
    """Explicit move list taking `state` exactly to `target`, using only
    rotations, inversions and the swap; None if `target` is not in the orbit."""
    target = tuple(reduce(w) for w in target)
    for do_swap in (False, True):
        mv = swap_moves(state) if do_swap else []
        s = replay(state, mv)[0]
        ok = True
        for i in (0, 1):
            m = match_relator(s[i], target[i])
            if m is None:
                ok = False
                break
            flip, k = m
            if flip:
                mv.append(["invert", i])
            if k:
                mv.append(["cycle", i, k])
        if ok:
            s2 = replay(state, mv)[0]
            if s2 == target:
                return mv
    return None


def is_cyclically_reduced(w):
    return len(w) < 2 or w[0] != -w[-1]


# --- named presentations, built from their definitions -----------------------

def MS(n, w):
    """Miller-Schupp MS(n, w) = <x, y | x^-1 y^n x = y^(n+1), x = w>,
    as relators (x^-1 y^n x y^-(n+1), x^-1 w).  [Shehper et al. arXiv:2408.15332
    Sec. 1; Carreras 2607.23611 Sec. 1]"""
    return (reduce((-1,) + (2,) * n + (1,) + (-2,) * (n + 1)),
            reduce((-1,) + tuple(word(w))))


def AK(n):
    """Akbulut-Kirby AK(n) = <x, y | x^n = y^(n+1), xyx = yxy>."""
    return (reduce((1,) * n + (-2,) * (n + 1)), word("x y x y^-1 x^-1 y^-1"))


P1_CLASSICAL = (word("x^-1 y^2 x y^-3"), word("y^-1 x^2 y x^-3"))  # Johnson 1980

THEOREMS = {
    # name: (presentation A, presentation B, certificate file)
    "Thm1: P1 ~ MS(2, y x^2 y^-1 x^-2)":
        (P1_CLASSICAL, MS(2, "y x^2 y^-1 x^-2"), "cert_sym_equiv_orphan1.json"),
    "Thm2: MS(2, y x^2 y x^-2) ~ MS(2, x^-2 y^-1 x^2 y^-1)":
        (MS(2, "y x^2 y x^-2"), MS(2, "x^-2 y^-1 x^2 y^-1"), "cert_idx0_equiv_mirror.json"),
    "Thm3: MS(3, y x^2 y) ~ AK(3)":
        (MS(3, "y x^2 y"), AK(3), "bottleneck_ak_f3_cert.json"),
    "Thm3': MS(3, y x^2 y) ~ AK(3) (second certificate)":
        (MS(3, "y x^2 y"), AK(3), "cert_ms3_yx2y_equiv_ak3.json"),
    "Thm4: MS(3, y^-1 x^2 y^-1) ~ AK(3)":
        (MS(3, "y^-1 x^2 y^-1"), AK(3), "cert_ms3_yinvx2yinv_equiv_ak3.json"),
}


def load(path):
    with open(path) as f:
        d = json.load(f)
    for key in ("initial", "moves"):
        if key not in d:
            raise ValueError(f"missing {key}")
    for key in ("initial", "target", "reached"):
        if key in d:
            if len(d[key]) != 2:
                raise ValueError(f"{key} is not a pair")
            for w in d[key]:
                if tuple(w) != reduce(w):
                    raise ValueError(f"{key} word not freely reduced")
    return d


def check_cert(d):
    """Replay a certificate.  Returns (ok, info).  For equivalence claims the
    full explicit chain initial -> reached -> target is replayed."""
    init = tuple(tuple(w) for w in d["initial"])
    final, st = replay(init, d["moves"])
    info = dict(st)
    if "reached" in d and final != tuple(tuple(w) for w in d["reached"]):
        return False, dict(info, error="terminal state != recorded 'reached'")
    claim = d.get("claim", "AC_equivalence")
    if claim == "AC_equivalence":
        target = tuple(tuple(w) for w in d["target"])
    else:  # trivialization: target is the trivial presentation up to orbit
        target = ((1,), (2,))
    br = bridge(final, target)
    if br is None:
        return False, dict(info, error="terminal state not in orbit of target")
    full = list(d["moves"]) + br
    if replay(init, full)[0] != target:
        return False, dict(info, error="explicit chain does not reach target")
    info["bridge_moves"] = len(br)
    info["full_chain"] = full
    return True, info


def prove_named(A, B, d):
    """Explicit chain A -> cert.initial -> ... -> cert.target -> B, where
    the cert may run A->B or B->A.  Returns the chain length or raises."""
    ok, info = check_cert(d)
    if not ok:
        raise AssertionError(info["error"])
    init = tuple(tuple(w) for w in d["initial"])
    tgt = tuple(tuple(w) for w in d["target"])
    for src, dst in ((A, B), (B, A)):
        b0 = bridge(src, init)
        b1 = bridge(tgt, dst)
        if b0 is not None and b1 is not None:
            chain = b0 + info["full_chain"] + b1
            assert replay(src, chain)[0] == dst
            return len(chain), (src is A)
    raise AssertionError("certificate endpoints are not the named presentations")


def abelian_det(P):
    """Determinant of the 2x2 exponent-sum matrix (must be +-1 for a
    presentation of the trivial group)."""
    m = [[sum(1 if a == g else -1 if a == -g else 0 for a in r) for g in (1, 2)]
         for r in P]
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def main(argv):
    if argv and argv[0] == "--theorems":
        import os
        cdir = argv[1]
        allok = True
        for name, (A, B, f) in THEOREMS.items():
            d = load(os.path.join(cdir, f))
            ok, info = check_cert(d)
            n, fwd = prove_named(A, B, d) if ok else (None, None)
            print(f"{'OK  ' if ok else 'FAIL'} {name}: {f}: {info['packaged']} moves "
                  f"({info['classical']} classical), peak total/single "
                  f"{info['peak_total']}/{info['peak_single']}, bridge "
                  f"{info.get('bridge_moves')}, explicit chain {n} moves "
                  f"({'A->B' if fwd else 'B->A'}); det A={abelian_det(A)} B={abelian_det(B)}"
                  f"; lengths A={sum(map(len, A))} B={sum(map(len, B))}")
            allok &= ok
        print("ALL OK" if allok else "SOME FAILED")
        return 0 if allok else 1
    rc = 0
    for p in argv:
        ok, info = check_cert(load(p))
        info.pop("full_chain", None)
        print(("OK  " if ok else "FAIL"), p, info)
        rc |= (not ok)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
