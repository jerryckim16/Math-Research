import AC.Certs
/-! Negative control: the Theorem 4 chain with its last move's sign flipped,
claimed to reach AK(3).  `build.sh` requires this file to FAIL. -/
namespace AC
open L
theorem bad : check (MS 3 [Y, x, x, Y])
    (thm4_pre ++ [
    .cycle .r0 6, .mul .r1 false, .conj .r0 Y, .mul .r1 true, .cycle .r1 2, .conj .r0 x,
    .mul .r0 false, .cycle .r0 4, .invert .r1, .cycle .r1 4, .mul .r1 true, .conj .r1 X,
    .mul .r1 false] ++ thm4_post) (AK 3) = true := by
  decide +kernel
end AC
