import OAI.Geometry.PlaneColoring.Five

/-! Independent statement check, written for this re-check (not from openai/math).
The statement below is typed out from scratch: no OAI definition is used in it. -/

namespace CNPRecheck

theorem plane_not_five_colourable :
    ¬ ∃ c : ℂ → Fin 5, ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y :=
  OAI.EuclideanFiveColor.no_proper_five_coloring

end CNPRecheck

#print axioms CNPRecheck.plane_not_five_colourable
#print axioms OAI.EuclideanFiveColor.no_proper_five_coloring
