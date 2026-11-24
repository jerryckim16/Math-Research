-- Control: a sorry-proved theorem is kernel-correct (sorryAx is an axiom), so leanchecker passes;
-- this is why the `#print axioms` check is needed in addition.
theorem NegCtl.sorried : (1 : Nat) = 2 := by sorry
