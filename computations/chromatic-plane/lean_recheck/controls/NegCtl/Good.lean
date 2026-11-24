import Lean
open Lean Meta
-- Positive control: the same mechanism with the kernel check ON and a well-typed value.
run_meta do
  let decl := Declaration.thmDecl
    { name := `NegCtl.good, levelParams := [], type := mkConst ``True, value := mkConst ``True.intro }
  addDecl decl
theorem NegCtl.uses_good : True := NegCtl.good
