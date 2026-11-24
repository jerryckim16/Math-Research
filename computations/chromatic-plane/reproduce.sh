#!/usr/bin/env bash
# Reproduce: chi(R^2) >= 4 and >= 5 with exact edges + LRAT; exact re-check of
# the finite certificate (Lemma 8.9 etc.) in the OpenAI chi >= 6 preprint.
# Needs python3 (+ sympy) and cadical >= 1.7 with --lrat.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)}
python3 "$here/test_chromatic_plane.py"
python3 "$here/run_pipeline.py" moser 3 "$work"   # UNSAT, LRAT VERIFIED
python3 "$here/run_pipeline.py" heule 4 "$work"   # UNSAT, LRAT VERIFIED; cnf sha256 f012031c...992f
python3 "$here/cert_section8.py"                   # ALL OK
