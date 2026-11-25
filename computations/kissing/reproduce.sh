#!/usr/bin/env bash
# Reproduce the exact pairwise checks of the 2026 kissing-number lower bounds
# (Yang et al., arXiv:2609.35051v1 "Qiushi Engine"; Q. Lin, arXiv:2611.03682v1;
# A. Kravatskiy's repository records in 25-39D; 11D 604, arXiv:2606.10402v2;
# 12D 841, arXiv:2606.18984v2). See problems/kissing-numbers.md.
#
# Needs: gcc with OpenMP, python3 with numpy, network access to github.com
# release assets, raw.githubusercontent.com and zenodo.org. About 1.5 h wall
# on 4 cores, plus about 1.5-2 h for section 7c (Kravatskiy 34-39D); peak RAM
# < 1 GB (25D/27D field checks: < 2 GB; 39D build and class mode: < 3 GB).
# Usage: reproduce.sh [WORKDIR] [--with-43] [--with-40-43] [--with-45] [--with-45-full]
#   (downloads and logs go to WORKDIR)
# --with-43 adds the Qiushi 43D export (2,553,792 points; about 75 min more).
# --with-40-43 adds Kravatskiy's 40-43D records (section 7d; about 6.5 h more).
# --with-45 adds the 45D build, its negative controls and two calibration parts
#   (section 7e; about 1.2 h); --with-45-full runs all 16 parts (about 6.1 h of C).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)}
with43=""
with4043=0
with45=0
for a in "${@:2}"; do
  case "$a" in --with-43) with43=--with-43 ;; --with-40-43) with4043=1 ;; --with-45) with45=1 ;;
    --with-45-full) with45=2 ;; *) echo "unknown option $a"; exit 2 ;; esac
done
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

# 7c. Kravatskiy 34-39D, rebuilt from their edit chains with our own code; integer
#     rows by kiss_check.c and kiss_check_np.py, 34D heads and 37D sqrt2 rows by
#     kiss_check_field.py, 36D (K12^3, lattice basis) by the partner (Gram) mode,
#     39D by the class mode (class_table.py)
python3 -I "$here/fetch_kravatskiy.py" "$K" --with-34-39
python3 -I "$here/build_kravatskiy34.py" "$K" "$K/krav34"      # asserts the final sha256 4b605a02...
python3 -I "$here/build_kravatskiy35.py" "$K" "$K/krav35.i8"
python3 -I "$here/build_kravatskiy36.py" "$K" "$K/krav36"
python3 -I "$here/build_kravatskiy37.py" "$K" "$K/krav37"
python3 -I "$here/build_kravatskiy38.py" "$K" "$K/krav38.i8"
python3 -I "$here/build_kravatskiy39.py" "$K" "$K/krav39"      # about 3 min
python3 -I "$here/class_table.py" "$K/krav39_classes.json" "$K/krav39_table.txt"
for d in 34 35 37 38; do
  "$CHK" "$K/krav$d.i8" "$d" | tee "$K/check$d.txt" | grep -E "^rows|^pairs|class_pair|contacts|RESULT"
  python3 "$here/kiss_check_np.py" "$K/krav$d.i8" "$d" | grep -E "contacts|RESULT"
done
"$CHK" "$K/krav36_x.i8" 36 --partner "$K/krav36_xg.i8" | tee "$K/check36.txt" | grep -E "^pairs|class_pair|contacts|RESULT"
python3 "$here/kiss_check_np.py" "$K/krav36_x.i8" 36 --partner "$K/krav36_xg.i8" | grep -E "contacts|RESULT"
"$CHK" "$K/krav39_body.i8" 36 "$K/krav39_labels.u8" "$K/krav39_table.txt" | tee "$K/check39.txt" \
  | grep -E "^rows|^pairs|contacts|max_excess|RESULT"
python3 "$here/kiss_check_np.py" "$K/krav39_body.i8" 36 --classes "$K/krav39_labels.u8" "$K/krav39_table.txt" \
  | grep -E "contacts|max_excess|RESULT"
"$CHK" "$K/krav39_sparse.i8" 39 | grep -E "^pairs|contacts|RESULT"   # sparse rows alone, norm mode
for m in float interval; do
  python3 "$here/kiss_check_field.py" "$K/krav34.i8" "$K/krav34_field.json" --mode $m | grep -E "pairs_checked|contacts|RESULT"
  python3 "$here/kiss_check_field.py" "$K/krav37.i8" "$K/krav37_field.json" --mode $m | grep -E "pairs_checked|contacts|RESULT"
done
# negative controls (wrong parent, wrong chain stage or order, wrong layout): each must FAIL
# (KISS_STOP_AT_FIRST=1: the C checker stops at the first violation)
export KISS_STOP_AT_FIRST=1
neg() {  # neg NAME FILE d [field.json]
  if "$CHK" "$2" "$3" > "$work/neg/$1.txt"; then
    if [ -z "${4:-}" ] || python3 "$here/kiss_check_field.py" "$2" "$4" --mode float >> "$work/neg/$1.txt"; then
      echo "NEGATIVE CONTROL $1 WAS ACCEPTED"; exit 1
    fi
  fi
  grep -E "^violations|RESULT" "$work/neg/$1.txt" | head -2
}
for v in unswitched oldroots; do
  python3 -I "$here/build_kravatskiy34.py" "$K" "$work/neg/k34_$v" --variant $v
  neg "k34_$v" "$work/neg/k34_$v.i8" 34 "$work/neg/k34_${v}_field.json"
done
for v in unswitched oldparity; do
  python3 -I "$here/build_kravatskiy35.py" "$K" "$work/neg/k35_$v.i8" --variant $v; neg "k35_$v" "$work/neg/k35_$v.i8" 35
done
for v in keepflat geometry; do
  python3 -I "$here/build_kravatskiy37.py" "$K" "$work/neg/k37_$v" --variant $v; neg "k37_$v" "$work/neg/k37_$v.i8" 37
done
for v in unswitched halfswitch; do
  python3 -I "$here/build_kravatskiy38.py" "$K" "$work/neg/k38_$v.i8" --variant $v; neg "k38_$v" "$work/neg/k38_$v.i8" 38
done
for v in noflip identity unswitched; do
  python3 -I "$here/build_kravatskiy39.py" "$K" "$work/neg/k39_$v" --variant $v
  python3 -I "$here/class_table.py" "$work/neg/k39_${v}_classes.json" "$work/neg/k39_$v.tab"
  if "$CHK" "$work/neg/k39_${v}_body.i8" 36 "$work/neg/k39_${v}_labels.u8" "$work/neg/k39_$v.tab" > "$work/neg/k39_$v.txt"; then
    echo "NEGATIVE CONTROL k39_$v WAS ACCEPTED"; exit 1
  fi
done
for v in noremove stale phase; do
  python3 -I "$here/build_kravatskiy36.py" "$K" "$work/neg/k36_$v" --variant $v
  if "$CHK" "$work/neg/k36_${v}_x.i8" 36 --partner "$work/neg/k36_${v}_xg.i8" > "$work/neg/k36_$v.txt"; then
    echo "NEGATIVE CONTROL k36_$v WAS ACCEPTED"; exit 1
  fi
done
unset KISS_STOP_AT_FIRST

# 7d. Kravatskiy 40-43D (affine lattice shells with rational heads), rebuilt with our own
#     shell enumerator (enum_affine.c) and checked over all pairs by kiss_check.c in
#     partner mode (40D) or class + partner mode (41-43D, table from the builder).
#     Only with --with-40-43: about 1.7 h of C on 4 cores (40D 11 min, 41D 22 min,
#     42D 21 min, 43D 44 min), numpy 48 min for 40D, 73 min for 41D and about 2.4 h
#     for 42D, builds about 25 min; peak RAM < 2 GB (C), about 3 GB (numpy, 41D/42D).
if [ "$with4043" = 1 ]; then
  gcc -O3 -march=native -fopenmp -Wall "$here/enum_affine.c" -o "$work/bin/enum_affine" -lm
  python3 -I "$here/fetch_kravatskiy.py" "$K" --with-40-43
  B4043="$here/build_kravatskiy4043.py"
  for d in 40 41 42 43; do
    python3 -I "$B4043" "$K" $d "$K/krav$d" "$work/bin/enum_affine" --work "$K/enum$d"   # asserts every population
  done
  "$CHK" "$K/krav40_x.i8" 40 --partner "$K/krav40_xg.i8" | tee "$K/check40.txt" | grep -E "^pairs|class_pair|contacts|RESULT"
  for k in 0 1; do  # second implementation for 40D (about 24 min per half)
    python3 "$here/kiss_check_np.py" "$K/krav40_x.i8" 40 --partner "$K/krav40_xg.i8" --part $k 2 | grep -E "^part|contacts|RESULT"
  done
  for k in 0 1 2 3 4; do  # second implementation for 41D: five tile parts (about 15 min each), which cover every pair once
    python3 "$here/kiss_check_np.py" "$K/krav41_x.i8" 40 --classes "$K/krav41.lab" "$K/krav41.tab" \
      --partner "$K/krav41_xg.i8" --part $k 5 | tee "$K/np41_p$k.txt" | grep -E "^part|contacts|max_excess|RESULT"
  done
  for k in 0 1 2 3 4 5 6 7; do  # second implementation for 42D: eight tile parts (about 18 min each), which cover every pair once
    python3 "$here/kiss_check_np.py" "$K/krav42_x.i8" 40 --classes "$K/krav42.lab" "$K/krav42.tab" \
      --partner "$K/krav42_xg.i8" --part $k 8 | tee "$K/np42_p$k.txt" | grep -E "^part|contacts|max_excess|RESULT"
  done
  for d in 41 42 43; do
    for k in 0 1 2 3; do  # four parts (each under 25 min); together they cover every pair once
      "$CHK" "$K/krav${d}_x.i8" 40 "$K/krav$d.lab" "$K/krav$d.tab" --partner "$K/krav${d}_xg.i8" --part $k 4 \
        | tee "$K/check${d}_p$k.txt" | grep -E "pairs_in_part|contacts|max_excess|RESULT"
    done
  done
  # negative controls: each must FAIL (wrong centre, wrong parent lattice, heads in the wrong order or sign or scale)
  export KISS_STOP_AT_FIRST=1
  python3 -I "$B4043" "$K" 40 "$work/neg/k40_negcore" "$work/bin/enum_affine" --variant negcore
  if "$CHK" "$work/neg/k40_negcore_x.i8" 40 --partner "$work/neg/k40_negcore_xg.i8" > "$work/neg/k40_negcore.txt"; then
    echo "NEGATIVE CONTROL k40_negcore WAS ACCEPTED"; exit 1
  fi
  if python3 -I "$B4043" "$K" 43 "$work/neg/k43_p48q" "$work/bin/enum_affine" --variant p48q > "$work/neg/k43_p48q.txt" 2>&1; then
    echo "NEGATIVE CONTROL k43_p48q WAS ACCEPTED"; exit 1
  fi
  for s in 41:shift 42:shift 43:shift 43:purenegate 43:tinyscale; do
    d=${s%%:*}; v=${s##*:}
    python3 -I "$B4043" --retable "$K/krav$d" $v "$work/neg/k${d}_$v"
    if "$CHK" "$K/krav${d}_x.i8" 40 "$K/krav$d.lab" "$work/neg/k${d}_$v.tab" --partner "$K/krav${d}_xg.i8" \
        > "$work/neg/k${d}_$v.txt"; then echo "NEGATIVE CONTROL k${d}_$v WAS ACCEPTED"; exit 1; fi
  done
  unset KISS_STOP_AT_FIRST
fi

# 7e. Kravatskiy 45D (7,655,056 points; 2,187 affine-shell families with rational heads
#     over 3^8 class residues, plus 16 pure heads; 2,203 classes), rebuilt with our own
#     shell enumerator. Only with --with-45: build (about 10 min on 4 cores, 18 min
#     alongside other jobs), head-order and head-scale negative controls (early exit),
#     and parts 0 and 1 of the 16-part C check (about 23 min each) as a calibration.
#     --with-45-full runs all 16 parts (about 6.1 h of C); a part with a log is skipped.
if [ "$with45" -ge 1 ]; then
  [ -x "$work/bin/enum_affine" ] || gcc -O3 -march=native -fopenmp -Wall "$here/enum_affine.c" -o "$work/bin/enum_affine" -lm
  python3 -I "$here/fetch_kravatskiy.py" "$K" --with-45
  B45="$here/build_kravatskiy45.py"
  [ -f "$K/krav45_meta.json" ] || python3 -I "$B45" "$K" "$K/krav45" "$work/bin/enum_affine" --work "$K/enum45" --jobs 4  # asserts every weight
  export KISS_STOP_AT_FIRST=1
  for v in shift headscale; do
    python3 -I "$B45" --retable "$K/krav45" $v "$work/neg/k45_$v"
    if "$CHK" "$K/krav45_x.i8" 40 "$K/krav45.lab" "$work/neg/k45_$v.tab" --partner "$K/krav45_xg.i8" \
        > "$work/neg/k45_$v.txt"; then echo "NEGATIVE CONTROL k45_$v WAS ACCEPTED"; exit 1; fi
  done
  unset KISS_STOP_AT_FIRST
  parts="0 1"; [ "$with45" = 2 ] && parts=$(seq 0 15)
  for k in $parts; do  # 16 parts (each under 25 min); together they cover every pair once
    log="$K/check45_p$k.txt"
    grep -q "^RESULT" "$log" 2>/dev/null && { grep -E "pairs_in_part|contacts|max_excess|RESULT" "$log"; continue; }
    "$CHK" "$K/krav45_x.i8" 40 "$K/krav45.lab" "$K/krav45.tab" --partner "$K/krav45_xg.i8" --part $k 16 \
      > "$log.tmp" && mv "$log.tmp" "$log"
    grep -E "pairs_in_part|contacts|max_excess|RESULT" "$log"
  done
fi

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
