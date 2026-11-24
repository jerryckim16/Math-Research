import Lake
open Lake DSL

package oaicheck where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from "../mathlib"

lean_lib OAI where
  globs := #[.submodules `OAI]

lean_lib Check where
