#!/usr/bin/env bash
# Kernel replay (leanchecker, shipped with the Lean 4.34.1 toolchain) of the
# .olean files built by lean_recheck.sh (same kernel code as compilation, but independent of the
# elaborator and the .olean writer; not an independent kernel).  Usage: kernel_replay.sh WORKDIR  (same WORKDIR)
# Measured here (4 cores, 15 GB): step 2 70/70 OK, 569 s wall; step 3 Hack rejected, Good+Sorry pass;
# step 4 exit 0, 2469 s wall, 8.2 GB peak RSS (mostly mmapped .olean files).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
W=$(cd "${1:?workdir}" && pwd); cd "$W"
export LEAN_PATH=$(cd mathlib && lake env printenv LEAN_PATH):$W/oaicheck/build
mkdir -p kr && cd kr
# 1. how many constants the default-mode replay re-adds (expect: TOTAL constants 4273 theorems 3553 modules 70)
lean --run "$here/count_constants.lean" $(find ../oaicheck/build -name "*.olean" | LC_ALL=C sort) | tail -1
# 2. default mode, one module at a time.  (`leanchecker OAI` checks all 70 in parallel
#    tasks, each importing Mathlib; that exceeded 15 GB RAM here and was OOM-killed.)
for f in $(cd ../oaicheck/build && find OAI -name "*.olean" | LC_ALL=C sort); do
  m=${f%.olean}; m=${m//\//.}
  leanchecker -v "$m" || { echo "FAIL $m"; exit 1; }      # expect: replaying <m>, rc 0
done
# 3. controls: environment hacking must be caught; sorry is (correctly) not a kernel error
mkdir -p ctlbuild/NegCtl
for m in Hack Good Sorry; do lean -R "$here/controls" -o ctlbuild/NegCtl/$m.olean "$here/controls/NegCtl/$m.lean"; done
( export LEAN_PATH=$PWD/ctlbuild
  if leanchecker NegCtl.Hack; then echo "CONTROL FAILED"; exit 1; fi   # expect: (kernel) declaration type mismatch
  leanchecker NegCtl.Good && leanchecker NegCtl.Sorry )               # expect: rc 0 both
# 4. --fresh: replay the whole environment of Five (Init, Std, Lean, Mathlib + deps, OAI:
#    787,391 constants, count via env_size.lean) into an empty kernel environment.  Single-threaded.
lean --run "$here/env_size.lean" OAI.Geometry.PlaneColoring.Five
leanchecker -v --fresh OAI.Geometry.PlaneColoring.Five                 # expect rc 0
