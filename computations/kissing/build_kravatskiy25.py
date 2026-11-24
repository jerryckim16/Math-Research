"""Rebuild A. Kravatskiy's 197,586-point configuration in R^25 from his
published witness `certificate25.json` (repository alexlegeartis/KissingNumbers
@ 907f9b1f, package verifications/improved/dim25-critical-cluster), with our
own code and our own Leech shell (known.leech_min_scaled). The witness is
untrusted data: we only parse its JSON. The point formulas below follow the
package's PROOF.md, Section 2, and the conventions of its checker
(source/verify_general.py, read but not run). Any misreading of those
conventions makes the rebuilt set fail our checks (owners missing from our
shell, wrong norms or count, or violations). It cannot make an invalid set
pass, because the check is of the rebuilt points themselves.

Witness contents and the points they define (all coordinates scaled so that
every point has squared norm 32):
  classes[k] = {shift v (24 ints, v.v = 48), owners [u, ...]}: for each owner
    u, both u and u + v must be shell vectors with u.v = -24. They are deleted
    from the shell and replaced by 3 points on the circle
        x(theta) = ((2u + v)/2 + cos(theta) v/2,  2 sqrt3 sin(theta)).
    The phases: cos, sin of the three base phases are, over the denominator 6,
        j = 0: (6, 0); j = 1: (-2 sqrt3, 2 sqrt6); j = 2: (-2 sqrt3, -2 sqrt6),
    except class 0, j = 0: (3 sqrt2 + sqrt3, 3 - sqrt6). Each base phase is then
    rotated by the angle delta with tan(delta/2) = p/q, p the next entry of
    rotation_half_tangent_numerators and q = rotation_half_tangent_denominator:
    cos delta = (q^2 - p^2)/(q^2 + p^2), sin delta = 2pq/(q^2 + p^2).
  small[i] = {numerator (25 ints), denominator}: a rational point.
  local_owners, new_owners: further shell vectors deleted.
Total = 196,560 - |deleted| + 3 * #owners + #small, asserted = 197,586.

Output (formats of kiss_check.c and kiss_check_field.py):
  OUT_bulk.i8      the retained shell vectors (int8, 25 columns, last = 0)
  OUT_field.json   circle and rational points as [C0, C1, C2, C3], integer
                   vectors with x = C0 + C1 sqrt2 + C2 sqrt3 + C3 sqrt6 up to a
                   positive factor (the common denominator is dropped)

Negative controls (--variant, each must FAIL; the count assertion is skipped):
  keepowner  do not delete the first owner u of class 0 (its circle passes
             at angle < 60 degrees from u for phases with cos(theta) < 1/3)
  dupsmall   append a second copy of the first rational point

Usage: python3 -I build_kravatskiy25.py certificate25.json OUTPREFIX [--variant V]
"""
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import known  # noqa: E402

SHA = "5270afec106a2336179fd8c1d21fd5b9e30da100a8d4f1e6ec4ca3ec8b161299"
D = 25


def mul(x, y):
    """Product in Q(sqrt2, sqrt3) on coefficient 4-tuples (1, r2, r3, r6)."""
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + 2 * b * f + 3 * c * g + 6 * d * h,
            a * f + b * e + 3 * (c * h + d * g),
            a * g + c * e + 2 * (b * h + d * f),
            a * h + d * e + b * g + c * f)


def build(cert_path, variant=None):
    raw = open(cert_path, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "certificate sha256 mismatch"
    cert = json.loads(raw)
    shell = known.leech_min_scaled()
    shell_set = set(shell)
    q = int(cert["rotation_half_tangent_denominator"])
    ps = [int(p) for p in cert["rotation_half_tangent_numerators"]]
    assert q > 0
    field = []
    deleted = set()
    i = 0
    n_owners = 0
    for k, cl in enumerate(cert["classes"]):
        v = [int(t) for t in cl["shift"]]
        assert len(v) == 24 and sum(t * t for t in v) == 48
        for row in cl["owners"]:
            u = [int(t) for t in row]
            other = [a + b for a, b in zip(u, v)]
            assert tuple(u) in shell_set and tuple(other) in shell_set, "owner not in our shell"
            assert sum(a * b for a, b in zip(u, v)) == -24
            deleted.add(tuple(u))
            deleted.add(tuple(other))
            n_owners += 1
            centre2 = [2 * a + b for a, b in zip(u, v)]          # 2 * centre
            for j in range(3):
                if k == 0 and j == 0:
                    co, si = (0, 3, 1, 0), (3, 0, 0, -1)
                elif j == 0:
                    co, si = (6, 0, 0, 0), (0, 0, 0, 0)
                else:
                    co, si = (0, 0, -2, 0), (0, 0, 0, 2 if j == 1 else -2)
                # check cos^2 + sin^2 = 1 for the base phase (denominator 36)
                s2 = [a + b for a, b in zip(mul(co, co), mul(si, si))]
                assert s2 == [36, 0, 0, 0]
                p = ps[i]
                i += 1
                rc, rs, rd = q * q - p * p, 2 * q * p, q * q + p * p
                co, si = (tuple(rc * a - rs * b for a, b in zip(co, si)),
                          tuple(rs * a + rc * b for a, b in zip(co, si)))
                # cos = co/(6 rd), sin = si/(6 rd). Point times 12 rd:
                #   first 24: 6 rd (2u + v) + co * v;  last: 4 sqrt3 * si
                C = [[0] * D for _ in range(4)]
                for t in range(24):
                    C[0][t] = 6 * rd * centre2[t]
                    for b in range(4):
                        C[b][t] += co[b] * v[t]
                s3 = mul((0, 0, 4, 0), si)                         # 4 sqrt3 * si
                for b in range(4):
                    C[b][24] = s3[b]
                field.append(C)
    assert i == len(ps), "rotation count mismatch"
    n_small = 0
    for x in cert["small"]:
        num = [int(t) for t in x["numerator"]]
        den = int(x["denominator"])
        assert len(num) == D and den > 0
        field.append([num, [0] * D, [0] * D, [0] * D])
        n_small += 1
    for name in ("local_owners", "new_owners"):
        for row in cert.get(name, []):
            u = tuple(int(t) for t in row)
            assert u in shell_set, "deleted vector not in our shell"
            deleted.add(u)
    if variant == "keepowner":
        deleted.discard(tuple(int(t) for t in cert["classes"][0]["owners"][0]))
    elif variant == "dupsmall":
        field.append(field[3 * n_owners])
    elif variant is not None:
        raise SystemExit("unknown variant")
    bulk = [r for r in shell if r not in deleted]
    total = len(bulk) + len(field)
    print(f"shell 196560, deleted {len(deleted)}, retained {len(bulk)}; "
          f"circles {n_owners} -> {3 * n_owners} points; rational {n_small}; total {total}")
    assert variant or int(cert["points"]) == total == 197586
    return bulk, field


def main(cert_path, prefix, variant=None):
    bulk, field = build(cert_path, variant)
    B = np.zeros((len(bulk), D), dtype=np.int8)
    B[:, :24] = np.array(bulk, dtype=np.int8)
    B.tofile(prefix + "_bulk.i8")
    with open(prefix + "_field.json", "w") as f:
        json.dump({"d": D, "rows": field}, f)
    print(f"-> {prefix}_bulk.i8 ({len(bulk)} rows), {prefix}_field.json ({len(field)} rows)")


if __name__ == "__main__":
    v = sys.argv[sys.argv.index("--variant") + 1] if "--variant" in sys.argv else None
    main(sys.argv[1], sys.argv[2], v)
