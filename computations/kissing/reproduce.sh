#!/usr/bin/env bash
# Reproduce the exact pairwise checks of the 2026 kissing-number lower bounds
# (Yang et al., arXiv:2609.35051v1 "Qiushi Engine"; Q. Lin, arXiv:2611.03682v1;
# A. Kravatskiy's repository records in 25-33D; 11D 604, arXiv:2606.10402v2;
# 12D 841, arXiv:2606.18984v2). See problems/kissing-numbers.md.
#
# Needs: gcc with OpenMP, python3 with numpy, network access to github.com
# release assets, raw.githubusercontent.com and zenodo.org. About 1.5 h wall
# on 4 cores; peak RAM < 1 GB (25D/27D field checks: < 2 GB).
# Usage: reproduce.sh [WORKDIR] [--with-43]   (downloads and logs go to WORKDIR)
# --with-43 adds the Qiushi 43D export (2,553,792 points; about 75 min more).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)}
with43=${2:-}
mkdir -p "$work"/bin "$work"/known "$work"/qiushi "$work"/lin "$work"/linbuild "$work"/neg "$work"/q2527 \
  "$work"/krav "$work"/small
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
python3 -I "$here/fetch_qiushi.py" "$work/qiushi" $with43 --with-25-27
for d in 32 33 34 35 36 37 39; do
  "$CHK" "$work/qiushi/qiushi$d.i8" "$d" | tee "$work/qiushi/check$d.txt" | grep -E "^rows|class_pair|contacts|RESULT"
done
python3 "$here/check_mixed.py" "$work/qiushi/qiushi38.i64" 52 --tail-copy 24,14,38 \
  --write-small "$work/qiushi/qiushi38_small.i8" | tee "$work/qiushi/mixed38.txt"
"$CHK" "$work/qiushi/qiushi38_small.i8" 52 | tee "$work/qiushi/check38_small.txt" | grep -E "^rows|class_pair|contacts|RESULT"

if [ "$with43" = "--with-43" ]; then
  python3 "$here/span_check.py" "$work/qiushi/qiushi43.i8" 48   # rank over Q = 43
  "$CHK" "$work/qiushi/qiushi43.i8" 48 | tee "$work/qiushi/check43.txt" | grep -E "^rows|class_pair|contacts|RESULT"
fi

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
# 6. Qiushi 25D and 27D, rebuilt from the repository data (coordinates in
#    Q(sqrt2, sqrt3)): integer bulk rows by kiss_check.c and kiss_check_np.py,
#    all pairs involving the other rows by kiss_check_field.py in both modes
python3 -I "$here/build_qiushi2527.py" "$work/qiushi/src2527" "$work/q2527"
for d in 25 27; do
  "$CHK" "$work/q2527/qiushi${d}_bulk.i8" "$d" | tee "$work/q2527/bulk$d.txt" | grep -E "^rows|contacts|RESULT"
  python3 "$here/kiss_check_np.py" "$work/q2527/qiushi${d}_bulk.i8" "$d" | grep -E "contacts|RESULT"
  for m in float interval; do
    python3 "$here/kiss_check_field.py" "$work/q2527/qiushi${d}_bulk.i8" "$work/q2527/qiushi${d}_field.json" \
      --mode $m | tee "$work/q2527/field${d}_$m.txt" | grep -E "pairs_checked|contacts|RESULT"
  done
done
# negative controls: each must FAIL
for v in q25_extra q25_norepair q27_owner q27_label; do
  python3 -I "$here/build_qiushi2527.py" "$work/qiushi/src2527" "$work/neg" --variant $v
  if python3 "$here/kiss_check_field.py" "$work/neg/${v}_bulk.i8" "$work/neg/${v}_field.json" --mode float \
      > "$work/neg/$v.txt"; then
    echo "NEGATIVE CONTROL $v WAS ACCEPTED"; exit 1
  else
    grep -E "violations|RESULT" "$work/neg/$v.txt"
  fi
done
# 7. Kravatskiy's 25-31D configurations (repository alexlegeartis/KissingNumbers
#    @ 907f9b1f, sha256-pinned): five coordinate files, 25D rebuilt from its
#    witness, 29D from parent + trade; integer pairs by kiss_check.c and
#    kiss_check_np.py, pairs with irrational rows by kiss_check_field.py
python3 -I "$here/fetch_kravatskiy.py" "$work/krav"
K="$work/krav"
for x in 26:201188 27:209884 28:223528 30:248506 31:251524; do
  python3 -I "$here/load_kravatskiy.py" "$K/krav${x%%:*}_${x##*:}.npz" "$K/krav${x%%:*}" "${x##*:}" "${x%%:*}"
done
python3 -I "$here/build_kravatskiy29.py" "$K/krav29_parent_232154.npz" "$K/krav29_trade.npz" "$K/krav29.i8"
python3 -I "$here/build_kravatskiy25.py" "$K/krav25_certificate25.json" "$K/krav25"
mv "$K/krav25_bulk.i8" "$K/krav25.i8"
for d in 25 26 27 28 29 30 31; do
  "$CHK" "$K/krav$d.i8" "$d" | tee "$K/check$d.txt" | grep -E "^rows|^pairs|contacts|RESULT"
  [ "$d" = 25 ] || python3 "$here/kiss_check_np.py" "$K/krav$d.i8" "$d" | grep -E "contacts|RESULT"
done
for d in 25 26; do
  for m in float interval; do
    python3 "$here/kiss_check_field.py" "$K/krav$d.i8" "$K/krav${d}_field.json" --mode $m \
      | tee "$K/field${d}_$m.txt" | grep -E "pairs_checked|contacts|RESULT"
  done
done
# negative controls: each must FAIL
for d in 27 31; do
  for m in dup merge; do
    python3 "$here/perturb.py" "$K/krav$d.i8" "$d" "$m" "$work/neg/k${d}_$m.i8"
    if "$CHK" "$work/neg/k${d}_$m.i8" "$d" > "$work/neg/k${d}_$m.txt"; then
      echo "NEGATIVE CONTROL k$d $m WAS ACCEPTED"; exit 1
    fi
  done
done
for v in dupfield conjfield; do
  python3 -I "$here/load_kravatskiy.py" "$K/krav26_201188.npz" "$work/neg/k26_$v" 201188 26 --variant $v
  if python3 "$here/kiss_check_field.py" "$work/neg/k26_$v.i8" "$work/neg/k26_${v}_field.json" --mode float \
      > "$work/neg/k26_$v.txt"; then echo "NEGATIVE CONTROL k26 $v WAS ACCEPTED"; exit 1; fi
done
for v in keepowner dupsmall; do
  python3 -I "$here/build_kravatskiy25.py" "$K/krav25_certificate25.json" "$work/neg/k25_$v" --variant $v
  if python3 "$here/kiss_check_field.py" "$work/neg/k25_${v}_bulk.i8" "$work/neg/k25_${v}_field.json" --mode float \
      > "$work/neg/k25_$v.txt"; then echo "NEGATIVE CONTROL k25 $v WAS ACCEPTED"; exit 1; fi
done

# 7b. Kravatskiy 32D and 33D, rebuilt from his compact witnesses
python3 -I "$here/build_kravatskiy32.py" "$K/krav32_certificate.json" "$K/krav32.i8"
python3 -I "$here/build_kravatskiy33.py" "$K/krav33_witness.npz" "$K/krav33.i8"
for d in 32 33; do
  "$CHK" "$K/krav$d.i8" "$d" | tee "$K/check$d.txt" | grep -E "^rows|^pairs|contacts|RESULT"
  python3 "$here/kiss_check_np.py" "$K/krav$d.i8" "$d" | grep -E "contacts|RESULT"
done
# negative controls: the mirrored support reading of the 33D witness, and a
# duplicated row in 32D, must FAIL
python3 -I "$here/build_kravatskiy33.py" "$K/krav33_witness.npz" "$work/neg/k33_msb.i8" --support-order msb
if "$CHK" "$work/neg/k33_msb.i8" 33 > "$work/neg/k33_msb.txt"; then echo "NEGATIVE CONTROL k33 msb WAS ACCEPTED"; exit 1; fi
python3 "$here/perturb.py" "$K/krav32.i8" 32 dup "$work/neg/k32_dup.i8"
if "$CHK" "$work/neg/k32_dup.i8" 32 > "$work/neg/k32_dup.txt"; then echo "NEGATIVE CONTROL k32 dup WAS ACCEPTED"; exit 1; fi
# relation to Lin's 32D/33D (bookkeeping; L32, L33 from section 4)
for d in 32 33; do
  python3 -I "$here/compare_rows.py" "$K/krav$d.i8" "LIN$d:$L32:$L33" "$d" --mirror-lin-octads
done

# 8. 11D: 604 points from the EinsteinArena appendix (arXiv:2606.10402v2), our build
python3 -I "$here/build_einstein11.py" "$work/small/e11"
"$CHK" "$work/small/e11.i8" 11 | grep -E "^pairs|contacts|RESULT"
for m in float interval; do
  python3 "$here/kiss_check_field.py" "$work/small/e11.i8" "$work/small/e11_field.json" --mode $m \
    | grep -E "pairs_checked|contacts|RESULT"
done
# (its negative variants are run by test_kissing.py, section 1 above)

# 9. 12D: the published 841 decimal coordinates (arXiv:2606.18984v2), read exactly
python3 -I "$here/fetch_small.py" "$work/small"
python3 -I "$here/check_decimal.py" "$work/small/tay12_841.txt" 12
for c in "dup 0 0" "merge 413 756" "nudge 413 756"; do
  # shellcheck disable=SC2086
  if python3 -I "$here/check_decimal.py" "$work/small/tay12_841.txt" 12 --control $c > "$work/neg/t12.txt"; then
    echo "NEGATIVE CONTROL 12D $c WAS ACCEPTED"; exit 1
  fi
done
# 10. 19D: Ho's published 11,948 points (arXiv:2603.10425v3); sign rows rescaled
python3 -I "$here/load_ho19.py" "$work/small/ho19_11948.txt" "$work/small/ho19.i8"
"$CHK" "$work/small/ho19.i8" 19 | grep -E "^pairs|class_pair|contacts|RESULT"
python3 "$here/kiss_check_np.py" "$work/small/ho19.i8" 19 | grep -E "contacts|RESULT"
for m in dup merge; do
  python3 "$here/perturb.py" "$work/small/ho19.i8" 19 "$m" "$work/neg/h19_$m.i8"
  if "$CHK" "$work/neg/h19_$m.i8" 19 > "$work/neg/h19_$m.txt"; then echo "NEGATIVE CONTROL h19 $m WAS ACCEPTED"; exit 1; fi
done
echo "ALL DONE"
