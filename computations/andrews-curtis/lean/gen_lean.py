"""Generate AC/Certs.lean from the JSON move certificates.

For each claim A ~AC B the generator writes
  * `<name>_cert`   : the certificate's moves, verbatim from the JSON file;
  * `<name>_pre`    : explicit moves from the Lean presentation A (or B) to the
                      certificate's `initial` (rotations/inversions/swap);
  * `<name>_post`   : explicit moves from the certificate's terminal state to
                      the exact other endpoint;
and two kernel-checked facts:
  * `<name>_replay` : the JSON moves take the JSON `initial` exactly to the
                      JSON `reached` (a literal replay of the file);
  * `<name>_check`  : `check A (pre ++ cert ++ post) B = true` where A and B are
                      the presentations *as defined in AC/Defs.lean*
                      (MS n w, AK n, johnsonP1, trivialPres);
from which `check_sound` gives the theorem `ACEquiv A B`.

The bridges are computed with our Python checker (ac_check.bridge); nothing
the generator computes is trusted: the Lean kernel re-runs every move.

Usage: python3 gen_lean.py [OUT.lean]   (default: AC/Certs.lean next to this file)
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ACDIR = os.path.dirname(HERE)
sys.path.insert(0, ACDIR)
import ac_check as A  # noqa: E402

LET = {1: "x", -1: "X", 2: "y", -2: "Y"}


def lw(w):
    return "[" + ", ".join(LET[a] for a in w) + "]"


def lpres(p):
    return f"({lw(p[0])}, {lw(p[1])})"


def lmove(m):
    op, i = m[0], m[1]
    idx = {0: ".r0", 1: ".r1"}[i]
    if op == "invert":
        return f".invert {idx}"
    if op == "mul":
        _, i, j, e = m
        assert j == 1 - i and e in (1, -1), m
        return f".mul {idx} {'true' if e == 1 else 'false'}"
    if op == "conj":
        return f".conj {idx} {LET[m[2]]}"
    if op == "cycle":
        k = m[2]
        assert isinstance(k, int) and k >= 0, m
        return f".cycle {idx} {k}"
    raise ValueError(m)


def lmoves(ms, per_line=6):
    if not ms:
        return "[]"
    parts = [lmove(m) for m in ms]
    lines = [", ".join(parts[i:i + per_line]) for i in range(0, len(parts), per_line)]
    return "[\n    " + ",\n    ".join(lines) + "]"


def corrupt(m):
    """A single-move corruption: flip the sign of mul, invert the conjugating
    letter, shift a rotation by one, or replace an inversion by a conjugation."""
    if m[0] == "mul":
        return [m[0], m[1], m[2], -m[3]]
    if m[0] == "conj":
        return [m[0], m[1], -m[2]]
    if m[0] == "cycle":
        return [m[0], m[1], m[2] + 1]
    return ["conj", m[1], 1]


def w(s):
    return A.word(s)


# name: (Lean A, Python A, Lean B, Python B, certificate path or None, docstring)
CLAIMS = [
    ("thm1", "johnsonP1", A.P1_CLASSICAL, "MS 2 [y, x, x, Y, X, X]", A.MS(2, "y x^2 y^-1 x^-2"),
     "certs/cert_sym_equiv_orphan1.json",
     "Carreras Thm 1: Johnson's P1 ~AC MS(2, y x² y⁻¹ x⁻²) (= P6)."),
    ("thm2", "MS 2 [y, x, x, y, X, X]", A.MS(2, "y x^2 y x^-2"),
     "MS 2 [X, X, Y, x, x, Y]", A.MS(2, "x^-2 y^-1 x^2 y^-1"),
     "certs/cert_idx0_equiv_mirror.json",
     "Carreras Thm 2: MS(2, y x² y x⁻²) (= P5) ~AC MS(2, x⁻² y⁻¹ x² y⁻¹) (= P2)."),
    ("thm3", "MS 3 [y, x, x, y]", A.MS(3, "y x^2 y"), "AK 3", A.AK(3),
     "certs/bottleneck_ak_f3_cert.json",
     "Carreras Thm 3: MS(3, y x² y) (= P3) ~AC AK(3)."),
    ("thm3b", "MS 3 [y, x, x, y]", A.MS(3, "y x^2 y"), "AK 3", A.AK(3),
     "certs/cert_ms3_yx2y_equiv_ak3.json",
     "Carreras Thm 3, second certificate."),
    ("thm4", "MS 3 [Y, x, x, Y]", A.MS(3, "y^-1 x^2 y^-1"), "AK 3", A.AK(3),
     "certs/cert_ms3_yinvx2yinv_equiv_ak3.json",
     "Carreras Thm 4: MS(3, y⁻¹ x² y⁻¹) (= P4) ~AC AK(3)."),
    ("ours_thm3", "MS 3 [y, x, x, y]", A.MS(3, "y x^2 y"), "AK 3", A.AK(3),
     "certs_ours/ms3_yx2y_to_ak3.json",
     "Thm 3 again, from the certificate found by our own search."),
    ("ours_thm4", "MS 3 [Y, x, x, Y]", A.MS(3, "y^-1 x^2 y^-1"), "AK 3", A.AK(3),
     "certs_ours/ms3_yinvx2yinv_to_ak3.json",
     "Thm 4 again, from the certificate found by our own search."),
    ("ak2", "AK 2", A.AK(2), "trivialPres", ((1,), (2,)),
     "certs_ours/ak2_trivial.json",
     "AK(2) is AC-trivial (known; Miasnikov 1999), certificate from our search."),
    ("p1_ms", "MS 2 [X, X, Y, x, x, y]", A.MS(2, "x^-2 y^-1 x^2 y"), "johnsonP1", A.P1_CLASSICAL,
     None,
     "P1 = MS(2, x⁻² y⁻¹ x² y) ~AC Johnson's P1 (rotation of the second relator)."),
]

EXTRA = []  # (name, LeanA, PyA, LeanB, PyB, certpath, doc) appended by --extra


def chain_for(pyA, pyB, d):
    """(direction_is_A_to_B, pre, cert_moves, post) with pre+cert+post an
    explicit chain from A to B (or from B to A)."""
    if d is None:
        br = A.bridge(pyA, pyB)
        assert br is not None
        return True, [], [], br
    ok, info = A.check_cert(d)
    assert ok, info
    init = tuple(tuple(x) for x in d["initial"])
    tgt = tuple(tuple(x) for x in d["target"])
    final = A.replay(init, d["moves"])[0]
    for fwd, src, dst in ((True, pyA, pyB), (False, pyB, pyA)):
        b0 = A.bridge(src, init)
        b1 = A.bridge(tgt, dst)
        if b0 is not None and b1 is not None:
            b_mid = A.bridge(final, tgt)
            post = b_mid + b1
            assert A.replay(src, b0 + list(d["moves"]) + post)[0] == dst
            return fwd, b0, list(d["moves"]), post
    raise AssertionError("endpoints do not match")


def main(argv):
    out = os.path.join(HERE, "AC", "Certs.lean")
    claims = list(CLAIMS)
    i = 0
    while i < len(argv):
        if argv[i] == "--extra":
            # --extra NAME CERT  (cert must run between two of AK(3), P1, P2)
            name, cert = argv[i + 1], argv[i + 2]
            named = {
                "AK3": ("AK 3", A.AK(3)),
                "P1": ("MS 2 [X, X, Y, x, x, y]", A.MS(2, "x^-2 y^-1 x^2 y")),
                "P2": ("MS 2 [X, X, Y, x, x, Y]", A.MS(2, "x^-2 y^-1 x^2 y^-1")),
            }
            d = json.load(open(os.path.join(ACDIR, cert)))
            hit = None
            for a in named:
                for b in named:
                    if a < b or a == b:
                        continue
                    try:
                        chain_for(named[a][1], named[b][1], d)
                        hit = (a, b)
                    except AssertionError:
                        pass
            assert hit, "certificate does not join two of AK3, P1, P2"
            a, b = hit
            claims.append((name, named[a][0], named[a][1], named[b][0], named[b][1], cert,
                           f"{a} ~AC {b}, certificate from our cap-30 search."))
            i += 3
        else:
            out = argv[i]
            i += 1
    L = []
    L.append("-- GENERATED by gen_lean.py from the JSON certificates; do not edit.")
    L.append("import AC.Checker\n")
    L.append("namespace AC\nopen L\n")
    # no maxRecDepth override: a runaway evaluation stops with "deep recursion"
    summary = []
    for name, la, pa, lb, pb, cert, doc in claims:
        d = None
        if cert:
            path = os.path.join(ACDIR, cert)
            raw = open(path, "rb").read()
            sha = hashlib.sha256(raw).hexdigest()
            d = json.loads(raw)
        fwd, pre, cm, post = chain_for(pa, pb, d)
        src, dst = (la, lb) if fwd else (lb, la)
        L.append(f"/-! ### {name}: {doc}")
        if cert:
            L.append(f"Certificate `{cert}`, sha256 `{sha}`, {len(cm)} moves.")
        L.append(f"Explicit chain {'A → B' if fwd else 'B → A'}: "
                 f"{len(pre)} + {len(cm)} + {len(post)} = {len(pre) + len(cm) + len(post)} moves. -/\n")
        if cert:
            L.append(f"def {name}_cert : List Move := {lmoves(cm)}\n")
            init = tuple(tuple(x) for x in d["initial"])
            reached = tuple(tuple(x) for x in d.get("reached") or [A.replay(init, cm)[0]])
            L.append(f"/-- Literal replay of the JSON file: `initial` ↦ `reached`. -/")
            L.append(f"theorem {name}_replay :\n    check {lpres(init)}\n      {name}_cert\n"
                     f"      {lpres(reached)} = true := by\n  decide +kernel\n")
        L.append(f"def {name}_pre : List Move := {lmoves(pre)}\n")
        L.append(f"def {name}_post : List Move := {lmoves(post)}\n")
        body = f"{name}_pre ++ {name}_cert ++ {name}_post" if cert else f"{name}_pre ++ {name}_post"
        L.append(f"theorem {name}_check :\n    check ({src}) ({body}) ({dst}) = true := by\n  decide +kernel\n")
        L.append(f"/-- {doc} -/")
        L.append(f"theorem {name} : ACEquiv ({la}) ({lb}) :=")
        L.append(f"  {'' if fwd else 'ACEquiv.symm '}(check_sound {name}_check)\n")
        summary.append((name, cert, len(pre) + len(cm) + len(post)))
    # Negative controls: the kernel must evaluate `check` to `false` here.
    L.append("/-! ## Negative controls (kernel evaluates `check` to `false`) -/\n")
    d4 = json.load(open(os.path.join(ACDIR, "certs/cert_ms3_yinvx2yinv_equiv_ak3.json")))
    fwd, pre, cm, post = chain_for(A.MS(3, "y^-1 x^2 y^-1"), A.AK(3), d4)
    assert fwd
    for pos in (0, 5, 12):
        bad = [list(m) for m in cm]
        bad[pos] = corrupt(bad[pos])
        assert A.replay(A.MS(3, "y^-1 x^2 y^-1"), pre + bad + post)[0] != A.AK(3)
        L.append(f"/-- Theorem 4 certificate with move {pos} corrupted to `{bad[pos]}`. -/")
        L.append(f"theorem neg_thm4_move{pos} :\n    check (MS 3 [Y, x, x, Y]) "
                 f"(thm4_pre ++ {lmoves(bad)} ++ thm4_post) (AK 3) = false := by\n  decide +kernel\n")
    L.append("/-- Correct Theorem 4 chain, wrong target AK(2). -/")
    L.append("theorem neg_thm4_target :\n    check (MS 3 [Y, x, x, Y]) (thm4_pre ++ thm4_cert ++ thm4_post) (AK 2)"
             " = false := by\n  decide +kernel\n")
    # (Replaying the Thm 3 chain from P4 instead would be a poor control: its
    # products blow the words up to ~650k letters.  The Thm 4 chain from P3
    # stays below 310 letters.)
    L.append("/-- Correct Theorem 4 chain, wrong source MS(3, y x² y). -/")
    L.append("theorem neg_thm4_source :\n    check (MS 3 [y, x, x, y]) (thm4_pre ++ thm4_cert ++ thm4_post) (AK 3)"
             " = false := by\n  decide +kernel\n")
    L.append("end AC")
    with open(out, "w") as f:
        f.write("\n".join(L) + "\n")
    for s in summary:
        print(*s)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
