import Lean
open Lean Elab Command Meta
-- Negative control: add an ILL-TYPED theorem `NegCtl.bad : False := True.intro`
-- with the kernel check switched off (environment hacking). leanchecker must reject this module.
run_meta do
  let decl := Declaration.thmDecl
    { name := `NegCtl.bad, levelParams := [], type := mkConst ``False, value := mkConst ``True.intro }
  withOptions (fun o => debug.skipKernelTC.set o true) (addDecl decl)
theorem NegCtl.uses_bad : False := NegCtl.bad
