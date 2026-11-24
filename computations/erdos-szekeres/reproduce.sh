#!/usr/bin/env bash
# Reproduce ES(6) = 17 end to end. Needs: python3, cadical (>= 1.7, --lrat support).
# Expected: 16-point set has no convex hexagon; N=17 formula UNSAT; LRAT proof VERIFIED.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)}
python3 "$here/construct.py" 6 7
python3 "$here/test_encoding.py"
python3 "$here/encode.py" 17 6 "$work/es_17_6.cnf"
sha256sum "$work/es_17_6.cnf"   # expected 587ae401ca32f7817d55d1039e879f816f3c87cd67234d49017667b9a0902ad2
cadical -q --lrat=true --binary=false "$work/es_17_6.cnf" "$work/es_17_6.lrat" || [ $? -eq 20 ]
python3 "$here/lrat_check.py" "$work/es_17_6.cnf" "$work/es_17_6.lrat"
# Optional second certificate through the compact cup/cap encoding (COMPACT=1 ./reproduce.sh).
if [ "${COMPACT:-0}" = 1 ]; then
  python3 "$here/encode_compact.py" 17 6 "$work/es_17_6_compact.cnf"
  sha256sum "$work/es_17_6_compact.cnf"   # expected 682629f22be36068a4fd9c9da8ff05c4e72daf3424c0a764b39f5cea252e81e3
  cadical -q --lrat=true --binary=false "$work/es_17_6_compact.cnf" "$work/es_17_6_compact.lrat" || [ $? -eq 20 ]
  python3 "$here/lrat_check.py" "$work/es_17_6_compact.cnf" "$work/es_17_6_compact.lrat"
fi
# Optional third certificate: compact encoding + reflection lex-leader (Approach 5), tuned CaDiCaL (REFLECT=1 ./reproduce.sh).
if [ "${REFLECT:-0}" = 1 ]; then
  python3 "$here/encode_compact.py" 17 6 "$work/es_17_6_rs.cnf" --reflect short
  sha256sum "$work/es_17_6_rs.cnf"   # expected e81aee682d2cca525797e654c286b1788640cfea634e306879692006fd5a2dba
  cadical -q --sat --reducetarget=10 --forcephase --phase=1 --lrat=true --binary=false "$work/es_17_6_rs.cnf" "$work/es_17_6_rs.lrat" || [ $? -eq 20 ]
  python3 "$here/lrat_check.py" "$work/es_17_6_rs.cnf" "$work/es_17_6_rs.lrat"
fi
