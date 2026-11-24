#!/usr/bin/env bash
# Build and kernel-check the Lean development with plain `lean` (core only, no Mathlib).
# Usage: build.sh [OUTDIR]    needs `lean` (v4.34.1) on PATH, python3 for the generator.
# Memory is capped with lean -M (MB) so a runaway kernel evaluation fails instead of swapping.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-$here/.lake/build/lib/lean}; mkdir -p "$OUT/AC"
lean --version
python3 "$here/gen_lean.py" "$here/AC/Certs.lean.new" > /dev/null
cmp -s "$here/AC/Certs.lean.new" "$here/AC/Certs.lean" && rm "$here/AC/Certs.lean.new" \
  || { echo "AC/Certs.lean is out of date with gen_lean.py (see AC/Certs.lean.new)"; exit 1; }
export LEAN_PATH="$OUT"
MEM=${AC_LEAN_MEM_MB:-3000}
for m in Defs Checker Certs Audit; do
  t0=$(date +%s.%N)
  lean -j 1 -M "$MEM" -o "$OUT/AC/$m.olean" -i "$OUT/AC/$m.ilean" "$here/AC/$m.lean"
  printf 'built AC/%s.lean in %.1f s\n' "$m" "$(echo "$(date +%s.%N) - $t0" | bc)"
done
# Re-check the compiled modules with the standalone kernel checker.
for m in AC.Defs AC.Checker AC.Certs AC.Audit; do leanchecker "$m"; done
echo "leanchecker OK"
[ "${AC_LEAN_FRESH:-0}" = 1 ] && leanchecker --fresh AC.Audit && echo "leanchecker --fresh OK"
# Negative control: a corrupted certificate claimed `= true` must NOT elaborate.
if lean -j 1 -M "$MEM" "$here/test/BadCert.lean" > "$OUT/badcert.log" 2>&1; then
  echo "NEGATIVE CONTROL FAILED: test/BadCert.lean elaborated"; exit 1
else
  grep -q "decide" "$OUT/badcert.log" && echo "negative control OK: test/BadCert.lean rejected"
fi
echo "ALL LEAN CHECKS OK"
