#!/usr/bin/env bash
# Reproduce the exact pairwise checks of the 2026 kissing-number lower bounds
# in dimensions 32-39 (Yang et al., arXiv:2609.35051v1 "Qiushi Engine";
# Q. Lin, arXiv:2611.03682v1). See problems/kissing-numbers.md.
#
# Needs: gcc with OpenMP, python3 with numpy, network access to github.com
# release assets and zenodo.org. About 25 min wall on 4 cores; peak RAM < 1 GB.
# Usage: reproduce.sh [WORKDIR]   (downloads and logs go to WORKDIR)
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)}
mkdir -p "$work"/bin "$work"/known "$work"/qiushi "$work"/lin "$work"/linbuild "$work"/neg
gcc -O3 -march=native -fopenmp -Wall "$here/kiss_check.c" -o "$work/bin/kiss_check"
CHK="$work/bin/kiss_check"

# 1. unit tests: known cases, negative controls, three-way cross-check
python3 "$here/test_kissing.py" "$work/bin"

# 2. known configurations (expected contacts: 96, 240, 6720, 452088000)
for c in D4:4 D5:5 E8:8 Leech:24; do
  python3 "$here/known.py" "${c%%:*}" "$work/known/${c%%:*}.i8"
  "$CHK" "$work/known/${c%%:*}.i8" "${c##*:}" | grep -E "^rows|contacts|RESULT"
done
python3 "$here/kiss_check_np.py" "$work/known/Leech.i8" 24 | grep -E "contacts|RESULT"

# 3. Qiushi Engine exports, dims 32-39 (sha256-pinned)
python3 -I "$here/fetch_qiushi.py" "$work/qiushi"
for d in 32 33 34 35 36 37 39; do
  "$CHK" "$work/qiushi/qiushi$d.i8" "$d" | tee "$work/qiushi/check$d.txt" | grep -E "^rows|class_pair|contacts|RESULT"
done
python3 "$here/check_mixed.py" "$work/qiushi/qiushi38.i64" 52 --tail-copy 24,14,38 \
  --write-small "$work/qiushi/qiushi38_small.i8" | tee "$work/qiushi/mixed38.txt"
"$CHK" "$work/qiushi/qiushi38_small.i8" 52 | tee "$work/qiushi/check38_small.txt" | grep -E "^rows|class_pair|contacts|RESULT"

# 4. Lin's configurations, rebuilt from his certificates with our own builder
read -r L32 L33 < <(python3 -I "$here/fetch_lin.py" "$work/lin" | awk '/-> /{print $NF}' | tr '\n' ' ')
python3 -I "$here/build_lin.py" "$L32" "$L33" "$work/qiushi" "$work/linbuild"
for d in 32 33 34 35 37 39; do
  "$CHK" "$work/linbuild/lin$d.i8" "$d" | tee "$work/linbuild/check$d.txt" | grep -E "^rows|class_pair|contacts|RESULT"
done
python3 "$here/check_mixed.py" "$work/linbuild/lin38.i64" 52 --tail-copy 24,14,38 \
  --write-small "$work/linbuild/lin38_small.i8" | tee "$work/linbuild/mixed38.txt"
"$CHK" "$work/linbuild/lin38_small.i8" 52 | tee "$work/linbuild/check38_small.txt" | grep -E "^rows|class_pair|contacts|RESULT"

# 5. negative controls on real data: each must FAIL
for m in dup merge; do
  python3 "$here/perturb.py" "$work/qiushi/qiushi32.i8" 32 "$m" "$work/neg/q32_$m.i8"
  if "$CHK" "$work/neg/q32_$m.i8" 32 > "$work/neg/q32_$m.txt"; then
    echo "NEGATIVE CONTROL $m WAS ACCEPTED"; exit 1
  else
    grep -E "violations|RESULT" "$work/neg/q32_$m.txt"
  fi
done
echo "ALL DONE"
