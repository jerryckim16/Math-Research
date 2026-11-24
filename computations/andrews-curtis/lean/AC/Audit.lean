import AC.Certs

/-!
# Main statements, explicit words, and axiom audit

The theorems below restate the results with the presentations written out
letter by letter (x, X = x⁻¹, y, Y = y⁻¹), and check by `rfl` that the
named definitions in `AC/Defs.lean` (MS n w, AK n, johnsonP1) produce
exactly these words.
-/

namespace AC
open L

/-! ## The named presentations, as explicit words -/

-- P1 = MS(2, x⁻²y⁻¹x²y)
example : MS 2 [X, X, Y, x, x, y] = ([X, y, y, x, Y, Y, Y], [X, X, X, Y, x, x, y]) := rfl
-- P2 = MS(2, x⁻²y⁻¹x²y⁻¹)
example : MS 2 [X, X, Y, x, x, Y] = ([X, y, y, x, Y, Y, Y], [X, X, X, Y, x, x, Y]) := rfl
-- P3 = MS(3, yx²y), P4 = MS(3, y⁻¹x²y⁻¹)
example : MS 3 [y, x, x, y] = ([X, y, y, y, x, Y, Y, Y, Y], [X, y, x, x, y]) := rfl
example : MS 3 [Y, x, x, Y] = ([X, y, y, y, x, Y, Y, Y, Y], [X, Y, x, x, Y]) := rfl
-- P5 = MS(2, yx²yx⁻²), P6 = MS(2, yx²y⁻¹x⁻²)
example : MS 2 [y, x, x, y, X, X] = ([X, y, y, x, Y, Y, Y], [X, y, x, x, y, X, X]) := rfl
example : MS 2 [y, x, x, Y, X, X] = ([X, y, y, x, Y, Y, Y], [X, y, x, x, Y, X, X]) := rfl
-- AK(3) = ⟨x, y | x³ = y⁴, xyx = yxy⟩, AK(2)
example : AK 3 = ([x, x, x, Y, Y, Y, Y], [x, y, x, Y, X, Y]) := rfl
example : AK 2 = ([x, x, Y, Y, Y], [x, y, x, Y, X, Y]) := rfl
-- Johnson: ⟨x, y | x⁻¹y²x = y³, y⁻¹x²y = x³⟩
example : johnsonP1 = ([X, y, y, x, Y, Y, Y], [Y, x, x, y, X, X, X]) := rfl

/-! ## Main theorems, in explicit words -/

/-- Carreras Thm 1: P1 ~AC P6 (P1 in Johnson's form and in MS form). -/
theorem carreras_thm1 :
    ACEquiv ([X, y, y, x, Y, Y, Y], [Y, x, x, y, X, X, X])
            ([X, y, y, x, Y, Y, Y], [X, y, x, x, Y, X, X]) := thm1

theorem carreras_thm1_MS :
    ACEquiv ([X, y, y, x, Y, Y, Y], [X, X, X, Y, x, x, y])
            ([X, y, y, x, Y, Y, Y], [X, y, x, x, Y, X, X]) := p1_ms.trans thm1

/-- Carreras Thm 2: P5 ~AC P2. -/
theorem carreras_thm2 :
    ACEquiv ([X, y, y, x, Y, Y, Y], [X, y, x, x, y, X, X])
            ([X, y, y, x, Y, Y, Y], [X, X, X, Y, x, x, Y]) := thm2

/-- Carreras Thm 3: P3 ~AC AK(3). -/
theorem carreras_thm3 :
    ACEquiv ([X, y, y, y, x, Y, Y, Y, Y], [X, y, x, x, y])
            ([x, x, x, Y, Y, Y, Y], [x, y, x, Y, X, Y]) := thm3

/-- Carreras Thm 4: P4 ~AC AK(3). -/
theorem carreras_thm4 :
    ACEquiv ([X, y, y, y, x, Y, Y, Y, Y], [X, Y, x, x, Y])
            ([x, x, x, Y, Y, Y, Y], [x, y, x, Y, X, Y]) := thm4

/-- AK(2) is AC-trivial. -/
theorem ak2_trivial :
    ACEquiv ([x, x, Y, Y, Y], [x, y, x, Y, X, Y]) ([x], [y]) := ak2

end AC

/-! ## Axiom audit (expected: no `sorryAx`, no `Lean.ofReduceBool`) -/
#print axioms AC.check_sound
#print axioms AC.carreras_thm1
#print axioms AC.carreras_thm1_MS
#print axioms AC.carreras_thm2
#print axioms AC.carreras_thm3
#print axioms AC.carreras_thm4
#print axioms AC.ak2_trivial
#print axioms AC.thm3b
#print axioms AC.ours_thm3
#print axioms AC.ours_thm4
#print axioms AC.neg_thm4_move5
