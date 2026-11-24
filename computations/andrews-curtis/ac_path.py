"""Turn a path of canonical states printed by ac_search into an explicit
elementary-move certificate, and check it with ac_check (the checker, not
this script, is what certifies the result).

Usage: python3 ac_path.py SEARCH_OUTPUT START_U/START_V END_U/END_V OUT.json
  START/END are the named presentations (letters x X y Y); the path printed by
  ac_search runs between them in either direction.

Paths from the --undirected searches may use an edge backwards (S <- T: the
graph has the edge T -> S only).  Such a step is written as the forward step
T -> S (found from a representative of T), inverted move by move: mul(i,j,e)
by mul(i,j,-e), conj(i,g) by conj(i,g^-1), invert by invert, and cycle by the
conjugation that undoes it; an orbit bridge joins the current words to the
start of the inverted block.  As before, only ac_check's replay certifies.
"""
import json
import sys

import ac_check as A

L2I = {"x": 1, "X": -1, "y": 2, "Y": -2}


def w(s):
    return tuple(L2I[c] for c in s)


def canon_key(state):
    def cw(u):
        rots = [u[k:] + u[:k] for k in range(len(u))] or [u]
        iu = A.inv(u)
        rots += [iu[k:] + iu[:k] for k in range(len(iu))]
        return min("".join("xXyY"[{1: 0, -1: 1, 2: 2, -2: 3}[a]] for a in r) for r in rots) \
            if u else ""
    return tuple(sorted((cw(state[0]), cw(state[1]))))


def cyc_reduce_moves(state, i):
    mv = []
    while len(state[i]) >= 2 and state[i][0] == -state[i][-1]:
        m = ["conj", i, -state[i][0]]
        state = A.apply(state, m)
        mv.append(m)
    return state, mv


def forward_step_moves(state, target_key):
    """Elementary moves taking `state` (cyclically reduced words) to some state
    whose canonical key is target_key, via one forward product edge."""
    for i in (0, 1):
        j = 1 - i
        for fi in (False, True):          # either orientation of r_i
            for e in (1, -1):
                for ra in range(max(len(state[i]), 1)):
                    for rb in range(max(len(state[j]), 1)):
                        mv = []
                        s = state
                        if fi:
                            mv.append(["invert", i]); s = A.apply(s, mv[-1])
                        if ra:
                            mv.append(["cycle", i, ra]); s = A.apply(s, mv[-1])
                        if e == -1:
                            mv.append(["invert", j]); s = A.apply(s, mv[-1])
                        if rb:
                            mv.append(["cycle", j, rb]); s = A.apply(s, mv[-1])
                        mv.append(["mul", i, j, 1]); s = A.apply(s, mv[-1])
                        s, m2 = cyc_reduce_moves(s, i)
                        mv += m2
                        if canon_key(s) == target_key:
                            return mv, s
    return None, None


def inverse_moves(state, moves):
    """Moves undoing `moves` (which start at `state`), in AC move language."""
    blocks = []                                # blocks[k] undoes moves[k]
    for mv in moves:
        if mv[0] == "invert":
            blocks.append([["invert", mv[1]]])
        elif mv[0] == "mul":
            blocks.append([["mul", mv[1], mv[2], -mv[3]]])
        elif mv[0] == "conj":
            blocks.append([["conj", mv[1], -mv[2]]])
        elif mv[0] == "cycle":                 # r = uv -> vu; undo: conjugate by u
            r = state[mv[1]]
            u = r[: mv[2] % len(r)] if r else ()
            blocks.append(A.conj_word_moves(mv[1], u))
        else:
            raise ValueError(mv)
        state = A.apply(state, mv)
    return [m for b in reversed(blocks) for m in b]


def step_moves(state, target_key):
    """Moves from `state` to a state with key target_key along one edge used
    forwards, or else backwards; returns (moves, new_state, direction)."""
    mv, s = forward_step_moves(state, target_key)
    if mv is not None:
        return mv, s, "fwd"
    trep = tuple(w(t) for t in target_key)      # a representative of the target
    mv, s = forward_step_moves(trep, canon_key(state))
    if mv is None:
        return None, None, None
    br = A.bridge(state, s)                      # state -> s (same orbit)
    assert br is not None
    back = br + inverse_moves(trep, mv)
    s2 = A.replay(state, back)[0]
    assert s2 == trep, "backward step did not return to the target"
    return back, s2, "back"


def main(out_path, start, end, json_out):
    lines = open(out_path).read().split("\n")
    p = lines[lines.index("PATH") + 1: lines.index("END")]
    keys = [canon_key(tuple(w(t) for t in l.split("|"))) for l in p]
    S = tuple(w(t) for t in start.split("/"))
    E = tuple(w(t) for t in end.split("/"))
    if keys[0] != canon_key(S):
        keys.reverse()
    assert keys[0] == canon_key(S), "path does not start at START"
    assert keys[-1] == canon_key(E), "path does not end at END"
    state = S
    moves = []
    nback = 0
    for k in keys[1:]:
        mv, state, d = step_moves(state, k)
        assert mv is not None, f"no single edge to {k}"
        nback += d == "back"
        moves += mv
    print(f"path: {len(keys) - 1} edges, {nback} used backwards")
    br = A.bridge(state, E)
    assert br is not None
    moves += br
    cert = {"generators": 2, "claim": "AC_equivalence",
            "initial": [list(x) for x in S], "target": [list(x) for x in E],
            "reached": [list(x) for x in A.replay(S, moves)[0]], "moves": moves}
    ok, info = A.check_cert(cert)
    info.pop("full_chain", None)
    print("OK" if ok else "FAIL", info)
    with open(json_out, "w") as f:
        json.dump(cert, f)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
