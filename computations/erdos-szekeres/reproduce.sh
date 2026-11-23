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
