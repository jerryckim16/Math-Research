/* dwsolve.c -- dense-window solver for the Lonely Runner Conjecture.
 *
 * Statement DW(m): every set V of at most m positive integers in [1,2m]
 * has a real t with ||v t|| >= 1/(m+1) for all v in V.
 * (Sets of size < m are subsets of m-sets, and adding speeds can only
 * lower min_v ||v t||, so it suffices to treat |V| = m.)
 *
 * Method (exact integer arithmetic throughout).
 *  For a rational time t = a/q (gcd(a,q)=1) the bad set is
 *      B(a/q) = { x in [1,H] : K*min(xa mod q, q - xa mod q) < q },
 *  with H = 2m and K = m+1 by default.  t is a witness for V iff V and
 *  B(t) are disjoint.  So V has no witness among a family of times iff V
 *  is a transversal (hitting set) of their bad sets.
 *
 *  We search, depth first, for hitting sets T with |T| <= m of the current
 *  family F (initially all a/q with 2 <= q <= Q, 1 <= a <= q/2, reduced to
 *  inclusion-minimal sets).  Branching: pick an unhit set S of F with the
 *  fewest non-forbidden elements, branch on its non-forbidden elements in
 *  increasing order, forbidding each element in the later siblings.
 *  Completeness: if V (|V| <= m) hits every set of F, then following, at
 *  each node, the first branch element that lies in V reaches a leaf whose
 *  T is contained in V; such a leaf is reported (or, in complete mode, is
 *  examined as below and the search continues there).
 *
 *  Complete mode: for each hitting set T found we run a complete witness
 *  test on T (left-endpoint search: a witness exists iff one of the times
 *  (k + 1/K)/x, x in T, 0 <= k < x, is a witness; proof in
 *  ../lonely.py).  If T has a witness t then T misses B(t); B(t) is
 *  appended to F and the search continues at the same node (T now has an
 *  unhit set).  If T has no witness, T is a counterexample (printed; the
 *  search stops).  If the search ends with no counterexample, then no set
 *  of size <= m hits every member of F, and every member of F is a genuine
 *  bad set, so DW(m) holds.  (A set V of size <= m with no witness would
 *  hit every member of F at every stage, so the search would reach a leaf
 *  T contained in V; T has no witness either, since V has none and T is a
 *  subset... see the note below.)
 *
 *  Note on subsets: if T is a subset of V and V has no witness, T may still
 *  have one.  That is harmless: then B(t) is added, V still hits B(t)
 *  (V has no witness), and the search continues below the same node, where
 *  V again contains the path.  Since the family only grows and the tree
 *  below each node is finite for a fixed family, and each added set is new
 *  (it is missed by the current T, which hits all older sets), the search
 *  terminates; at termination a witness-free V would have produced a leaf
 *  T contained in V that is a hitting set of the final family, a
 *  contradiction unless T itself was reported as a counterexample.
 *
 * Usage:
 *   dwsolve m Q                 complete mode (decides DW(m))
 *   dwsolve m Q fixed [cap=C]   only the family with denominators <= Q;
 *                               prints up to C hitting sets of size <= m.
 *   options: k=K  threshold 1/K instead of 1/(m+1) (negative controls)
 *            top=H  window [1,H] instead of [1,2m]   (H <= 128)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
static int M, H, K;
static u128 *fam;
static int nfam, capfam;
static long long nodes, added, ntrans, capprint = 20;
static int fixedmode, stop;
static long long maxden_added;

static int popc(u128 x) { return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64)); }
static int ctz128(u128 x) {
  uint64_t lo = (uint64_t)x;
  if (lo) return __builtin_ctzll(lo);
  return 64 + __builtin_ctzll((uint64_t)(x >> 64));
}
static long long gcdll(long long a, long long b) {
  while (b) { long long t = a % b; a = b; b = t; }
  return a < 0 ? -a : a;
}
/* bit (x-1) represents speed x in [1,H] */
static u128 badset(long long a, long long q) {
  u128 B = 0;
  for (int x = 1; x <= H; x++) {
    long long r = ((long long)x * a) % q, d = r < q - r ? r : q - r;
    if ((long long)K * d < q) B |= ((u128)1) << (x - 1);
  }
  return B;
}
static void addset(u128 B) {
  if (nfam == capfam) { capfam = capfam ? 2 * capfam : 1024; fam = realloc(fam, capfam * sizeof(u128)); }
  fam[nfam++] = B;
}
static void printset(const char *tag, u128 T) {
  printf("%s size %d:", tag, popc(T));
  for (int x = 1; x <= H; x++) if ((T >> (x - 1)) & 1) printf(" %d", x);
  printf("\n");
}
/* complete witness test; returns 1 and the witness a/q (reduced) if one exists */
static int witness(u128 T, long long *wa, long long *wq) {
  int xs[128], n = 0;
  for (int x = 1; x <= H; x++) if ((T >> (x - 1)) & 1) xs[n++] = x;
  if (n == 0) { *wa = 1; *wq = 2; return 1; }
  for (int i = 0; i < n; i++) {
    long long x = xs[i], b = (long long)K * x;
    for (long long k = 0; k < x; k++) {
      long long a = k * K + 1; /* t = a/b = (k + 1/K)/x */
      int ok = 1;
      for (int j = 0; j < n; j++) {
        long long r = ((long long)xs[j] * a) % b, d = r < b - r ? r : b - r;
        if ((long long)K * d < b) { ok = 0; break; }
      }
      if (ok) { long long g = gcdll(a, b); *wa = a / g; *wq = b / g; return 1; }
    }
  }
  return 0;
}
static void dfs(u128 T, u128 forb, int k) {
  nodes++;
  if (stop) return;
  for (;;) {
    int best = -1, bc = 1 << 30;
    for (int i = 0; i < nfam; i++) {
      if (fam[i] & T) continue;
      int c = popc(fam[i] & ~forb);
      if (c < bc) { bc = c; best = i; if (c <= 1) break; }
    }
    if (best < 0) {
      ntrans++;
      if (fixedmode) { if (ntrans <= capprint) printset("TRANSVERSAL", T); return; }
      long long a, q;
      if (witness(T, &a, &q)) {
        u128 B = badset(a, q);
        if (B & T) { fprintf(stderr, "internal error\n"); exit(2); }
        addset(B); added++;
        if (q > maxden_added) maxden_added = q;
        continue;
      }
      printset("COUNTEREXAMPLE", T);
      stop = 1;
      return;
    }
    if (k == M) return;
    u128 S = fam[best] & ~forb, f = forb;
    while (S) {
      int b = ctz128(S);
      u128 bit = ((u128)1) << b;
      S &= ~bit;
      dfs(T | bit, f, k + 1);
      if (stop) return;
      f |= bit;
    }
    return;
  }
}
int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: dwsolve m Q [fixed] [cap=C] [k=K] [top=H]\n"); return 1; }
  M = atoi(argv[1]);
  int Q = atoi(argv[2]);
  H = 2 * M; K = M + 1;
  for (int i = 3; i < argc; i++) {
    if (!strcmp(argv[i], "fixed")) fixedmode = 1;
    else if (!strncmp(argv[i], "k=", 2)) K = atoi(argv[i] + 2);
    else if (!strncmp(argv[i], "top=", 4)) H = atoi(argv[i] + 4);
    else if (!strncmp(argv[i], "cap=", 4)) capprint = atoll(argv[i] + 4);
    else { fprintf(stderr, "bad option %s\n", argv[i]); return 1; }
  }
  if (H > 128 || H < 1) { fprintf(stderr, "H out of range\n"); return 1; }
  for (long long q = 2; q <= Q; q++)
    for (long long a = 1; 2 * a <= q; a++)
      if (gcdll(a, q) == 1) addset(badset(a, q));
  int n0 = nfam, nk = 0;
  u128 *keep = malloc((nfam + 1) * sizeof(u128));
  for (int i = 0; i < nfam; i++) {
    int red = 0;
    for (int j = 0; j < nfam && !red; j++) {
      if (j == i) continue;
      if ((fam[j] & fam[i]) == fam[j] && (fam[j] != fam[i] || j < i)) red = 1;
    }
    if (!red) keep[nk++] = fam[i];
  }
  free(fam); fam = keep; nfam = nk; capfam = nk + 1;
  for (int i = 1; i < nfam; i++) {
    u128 x = fam[i]; int j = i - 1;
    while (j >= 0 && popc(fam[j]) > popc(x)) { fam[j + 1] = fam[j]; j--; }
    fam[j + 1] = x;
  }
  dfs(0, 0, 0);
  printf("m=%d H=%d K=%d Q=%d mode=%s initial_sets=%d minimal=%d nodes=%lld transversals=%lld added=%lld maxden_added=%lld result=%s\n",
         M, H, K, Q, fixedmode ? "fixed" : "complete", n0, nk, nodes, ntrans, added, maxden_added,
         fixedmode ? (ntrans ? "TRANSVERSALS_EXIST" : "NO_TRANSVERSAL") : (stop ? "COUNTEREXAMPLE" : "DW_HOLDS"));
  return 0;
}
