# Math Research

A workspace for attacking problems in mathematics — open conjectures, competition-style problems, and anything in between — with proofs checked as rigorously as possible.

## Layout

| Folder | What goes there |
| --- | --- |
| `problems/` | One file per problem: statement, status, approaches tried, results |
| `lean/` | Lean 4 formalizations of verified results |
| `computations/` | Scripts and data supporting numerical or exhaustive checks |
| `notes/` | Literature notes, sketches, and failed routes worth remembering |

## Working rules

1. **State the claim exactly** before trying to prove it.
2. **Label evidence honestly**: *proved*, *Lean-verified*, *computationally checked up to N*, *heuristic*, or *conjectured*. A bounded computation is never a proof.
3. **Keep failed routes.** Write down why an approach broke so it isn't retried blindly.
4. **Cite sources** for any external theorem used, with its exact hypotheses.

## Adding a problem

Copy `problems/TEMPLATE.md` to `problems/<short-name>.md` and fill it in.

## Status

| Problem | Status |
| --- | --- |
| _none yet_ | |
