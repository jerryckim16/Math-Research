import Lean
open Lean
unsafe def main (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  for a in args do
    Lean.withImportModules #[{module := a.toName}] {} fun env => do
      IO.println s!"{a}: {env.constants.map₁.size} constants, {env.header.moduleNames.size} modules"
