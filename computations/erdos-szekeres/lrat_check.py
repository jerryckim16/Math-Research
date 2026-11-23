"""Minimal independent LRAT checker (RUP steps with hints; deletions).

Usage: python3 lrat_check.py formula.cnf proof.lrat

Accepts the textual LRAT emitted by `cadical --lrat=true --binary=false`.
Every added clause must follow by unit propagation using exactly the listed
hint clauses in order. RAT steps (negative hints) are rejected, since CaDiCaL
does not emit them. The proof is valid iff the empty clause is derived.
"""
import sys


def read_cnf(path):
    clauses, cur = [], []
    with open(path) as f:
        for line in f:
            if line.startswith(("c", "p")):
                continue
            for tok in line.split():
                v = int(tok)
                if v == 0:
                    clauses.append(cur); cur = []
                else:
                    cur.append(v)
    return clauses


def check(cnf_path, proof_path):
    db = {i + 1: c for i, c in enumerate(read_cnf(cnf_path))}
    last_id = len(db)
    steps = 0
    with open(proof_path) as f:
        for lineno, line in enumerate(f, 1):
            toks = line.split()
            if not toks or toks[0] == "c":
                continue
            cid = int(toks[0])
            if toks[1] == "d":
                for t in toks[2:]:
                    t = int(t)
                    if t == 0:
                        break
                    db.pop(t, None)
                continue
            nums = list(map(int, toks[1:]))
            z = nums.index(0)
            lemma, hints = nums[:z], nums[z + 1:-1]
            if nums[-1] != 0:
                raise ValueError(f"line {lineno}: malformed")
            if cid <= last_id:
                raise ValueError(f"line {lineno}: non-increasing clause id")
            # assignment: literal -> True; start from negation of lemma
            assign = set(-l for l in lemma)
            conflict = False
            for h in hints:
                if h < 0:
                    raise ValueError(f"line {lineno}: RAT hint not supported")
                c = db.get(h)
                if c is None:
                    raise ValueError(f"line {lineno}: hint {h} not in database")
                unassigned = None
                n_un = 0
                sat = False
                for l in c:
                    if l in assign:
                        sat = True; break
                    if -l not in assign:
                        n_un += 1; unassigned = l
                        if n_un > 1:
                            break
                if sat or n_un > 1:
                    raise ValueError(f"line {lineno}: hint {h} is not unit/conflicting")
                if n_un == 0:
                    conflict = True; break
                assign.add(unassigned)
            if not conflict:
                raise ValueError(f"line {lineno}: hints do not yield a conflict")
            db[cid] = lemma
            last_id = cid
            steps += 1
            if not lemma:
                return steps
    raise ValueError("proof ends without deriving the empty clause")


if __name__ == "__main__":
    n = check(sys.argv[1], sys.argv[2])
    print(f"s VERIFIED ({n} lemmas checked; empty clause derived)")
