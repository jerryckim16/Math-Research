#!/usr/bin/env bash
# Re-check OpenAI's Lean proof of "no proper 5-colouring of the plane"
# (openai/math@adc7f12, lean/OAI/Geometry/PlaneColoring/Five.lean) from source,
# without the Mathlib cache. Usage: lean_recheck.sh WORKDIR   (needs ~6+ CPU-hours, ~6 GB disk)
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
W=${1:?workdir}; mkdir -p "$W"; cd "$W"
PIN=adc7f1241b42e322a6451854ab7e4b4c146bf78a
MATHLIB=d13f23b723b8a846827a245b89c10fc7d3f11612
# 1. toolchain v4.34.1 from the GitHub release (elan's own download path was refused here)
if [ ! -x lean-4.34.1-linux/bin/lean ]; then
  curl -sSL -o lean.tar.zst https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst
  python3 -c "import zstandard,tarfile,sys
with open('lean.tar.zst','rb') as f:
  tarfile.open(fileobj=zstandard.ZstdDecompressor().stream_reader(f),mode='r|').extractall('.',filter='tar')"
  rm lean.tar.zst
fi
elan toolchain link leanprover/lean4:v4.34.1 "$PWD/lean-4.34.1-linux"
# 2. Mathlib at the pinned revision, built from source
if [ ! -d mathlib ]; then
  mkdir mathlib && (cd mathlib && git init -q && git remote add origin https://github.com/leanprover-community/mathlib4.git \
    && git fetch -q --depth 1 origin $MATHLIB && git checkout -q FETCH_HEAD)
fi
(cd mathlib && lake build Mathlib)
# 3. the 70 OAI modules (fetched by following imports from Five.lean), plus our statement check
mkdir -p oaicheck && cd oaicheck
cp "$here/Check.lean" .
B=https://raw.githubusercontent.com/openai/math/$PIN/lean
queue=(OAI.Geometry.PlaneColoring.Five); declare -A seen
while [ ${#queue[@]} -gt 0 ]; do
  m=${queue[0]}; queue=("${queue[@]:1}"); [ -n "${seen[$m]:-}" ] && continue; seen[$m]=1
  p=${m//./\/}.lean; mkdir -p "$(dirname "$p")"; curl -sSf -o "$p" "$B/$p"
  for i in $(grep -E '^import OAI\.' "$p" | awk '{print $2}'); do queue+=("$i"); done
done
find OAI -name "*.lean" | LC_ALL=C sort | xargs cat | sha256sum   # expect 171452cc...a14e4b (70 files)
# compile in dependency order with plain `lean -o` against the Mathlib build (4 parallel jobs)
python3 "$here/compile_oai.py" . ../mathlib          # expect: done 70/70 failed []
LEAN_PATH=$(cd ../mathlib && lake env printenv LEAN_PATH):$PWD/build lean Check.lean
# expect: 'CNPRecheck.plane_not_five_colourable' depends on axioms: [propext, Classical.choice, Quot.sound]
# 4. kernel replay of the compiled .olean files (leanchecker): see kernel_replay.sh "$W"
#    (70/70 OAI modules in default mode; --fresh replay of all 787,391 constants: exit 0, 41 min)
