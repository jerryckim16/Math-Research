#!/usr/bin/env bash
# Independent check of Carreras, arXiv:2607.23611v1 (Andrews-Curtis, length-14 frontier).
# Needs python3 and g++.  Usage: reproduce.sh [WORKDIR]; AC_HEAVY=1 adds the cap-26/27 exhaustions.
set -eu   # no pipefail: the engines exit 1 on "EXHAUSTED", which is an expected result
here=$(cd "$(dirname "$0")" && pwd)
W=${1:-$(mktemp -d)}; mkdir -p "$W"
python3 "$here/test_ac.py"                            # all tests passed
python3 "$here/ac_check.py" --theorems "$here/certs"  # ALL OK (author certificates, our checker)
# Lean-verified replay (needs lean v4.34.1 on PATH; skipped otherwise): ALL LEAN CHECKS OK, ~6 s
if command -v lean >/dev/null; then "$here/lean/build.sh" "$W/lean"; else echo "lean not found: Lean check skipped"; fi
g++ -O2 -std=c++17 -o "$W/ac_search" "$here/ac_search.cpp"
AK3=xxxYYYY/xyxYXY; P3=XyyyxYYYY/Xyxxy; P4=XyyyxYYYY/XYxxY      # MS(3, y x^2 y), MS(3, y^-1 x^2 y^-1)
P1=XyyxYYY/XXXYxxy; P2=XyyxYYY/XXXYxxY                          # MS(2, x^-2y^-1x^2y^{+-1})
# our own rediscovery of Theorems 3 and 4 (then expanded to elementary moves and checked)
for p in "$P3" "$P4"; do
  "$W/ac_search" 19 --junction "$p" + $AK3 | tail -1    # EXHAUSTED: bottleneck >= 19
  "$W/ac_search" 20 --junction "$p" + $AK3 > "$W/path.out"; grep MEET "$W/path.out"   # MEET at 19
  python3 "$here/ac_path.py" "$W/path.out" "$p" $AK3 "$W/cert.json"                  # OK
done
# Directed reading (the GS graph is directed): one source expanded, the other a passive target.
g++ -O2 -std=c++17 -o "$W/ac_compact" "$here/ac_search_compact.cpp"
for p in "$P3" "$P4"; do for d in "$p --passive $AK3" "$AK3 --passive $p"; do
  "$W/ac_compact" 19 --maxstates 2000000 $d | tail -1                # EXHAUSTED: no directed path below 19
  "$W/ac_compact" 20 --maxstates 2000000 $d | grep MEET              # MEET at level 19: directed path, bottleneck 19
done; done
# Theorem 6 sublevel counts at exclusive cap 25: expect 1532732 135892 168304, no meeting (~90 s, 0.4 GB)
"$W/ac_search" 25 --junction $AK3 + $P1 + $P2 | tail -2
if [ "${AC_HEAVY:-0}" = 1 ]; then
  "$W/ac_search" 26 --junction $AK3 + $P1 + $P2 | tail -2   # 6,212,968 states (5431780 356836 424352), no meeting; 5.5 min
  "$W/ac_search" 27 --junction $AK3 + $P1 + $P2 | tail -2   # 13,504,944 states (10118636 851836 2534472), no meeting; 14 min, 3.0 GB
  "$W/ac_compact" 28 --maxstates 95000000 $AK3 + $P1 + $P2 | tail -2  # 47,544,780 states (36700896 2323596 8520288), no meeting; 18 min, 1.7 GB
  "$W/ac_compact" 29 --maxstates 190000000 $AK3 + $P1 + $P2 | tail -2 # 88,628,824 states (68481208 5374816 14772800), no meeting; 34 min, 3.1 GB
  g++ -O2 -std=c++17 -pthread -o "$W/ac_par" "$here/ac_search_par.cpp"
  "$W/ac_par" 27 --slots 40000000 $AK3 + $P1 + $P2 | tail -1        # 13,504,944 states (10118636 851836 2534472), no meeting; 93 s
  "$W/ac_par" 30 --slots 600000000 $AK3 + $P1 + $P2 | tail -4       # levels 26-28 give the cap-27/28/29 totals; then
  # 351,388,696 states (284176652 17796820 49415224), no meeting; 54 min wall on 4 threads, 4.7 GB
fi
