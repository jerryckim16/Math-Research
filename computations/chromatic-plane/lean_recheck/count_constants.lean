import Lean
open Lean
-- Count the constants stored in each given .olean (the set leanchecker replays per module).
unsafe def main (args : List String) : IO Unit := do
  let mut total := 0
  let mut thms := 0
  for f in args do
    let (md, r) ← readModuleData f
    total := total + md.constNames.size
    thms := thms + (md.constants.filter (fun c => c matches .thmInfo _)).size
    IO.println s!"{md.constNames.size} {f}"
    let _ := r  -- region deliberately not freed: `r.free` segfaulted under `lean --run`
  IO.println s!"TOTAL constants {total} theorems {thms} modules {args.length}"
