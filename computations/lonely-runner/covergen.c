/* covergen.c -- level-one improper family via minimal covers.
 *
 * Fix k and a prime p; h = (p-1)/2.  Folded speed classes and folded time
 * classes are both 1..h.  Class v COVERS time a iff (k+1)*d_p(a*v) < p,
 * where d_p(x) = min(x mod p, p - x mod p); i.e. the speed fails the witness
 * inequality at t = a/p.  (t = 0 is never a witness and is not a time class.)
 * A k-multiset of classes is in I(k,p,1) iff its support covers all h times.
 *
 * Every such multiset M contains a MINIMAL cover C (every class of C covers
 * some time no other class of C covers) with |C| <= k, and M = C + (k-|C|)
 * arbitrary classes.  Multiplying by a unit maps covers to covers, so every
 * orbit has a representative in which some class of C is 1.  This program
 * prints every minimal cover C with 1 in C and |C| <= k, exactly once:
 *
 *   DFS(L, U = uncovered times, A = allowed classes):
 *     U empty -> print L if minimal.  |L| = k -> stop.
 *     gain bound: if (k-|L|) * max_{c in A} |cov(c) & U| < |U| -> stop.
 *     pick a in U with fewest allowed coverers c_1 < ... < c_m;
 *     branch i: add c_i, and remove c_1..c_{i-1} from A ("exclusion").
 *
 * Uniqueness/completeness: for a minimal cover C containing 1, at each node
 * on its path the chosen time a is covered by some class of C; follow the
 * branch of the first candidate lying in C (the excluded earlier ones are
 * not in C).  The leaf reached is a cover contained in C, hence equals C by
 * minimality.  The gain bound only cuts nodes with no cover below them.
 *
 * Usage: covergen k p [maxtop]   (maxtop: only explore the first maxtop
 * branches of the root, for timing samples; prints node counts to stderr)
 *        covergen k p -1 PROBES SEED NODECAP
 *   Cost estimation mode: Knuth's random-probe estimator of the size of
 *   the search tree (unbiased for the node count), plus a timed DFS capped
 *   at NODECAP nodes to measure nodes/second.  Nothing is printed to stdout
 *   in this mode.
 * Output: one cover per line, classes separated by spaces.
 * Sharding: with environment LRC_NSHARDS=m and LRC_SHARD=r, only root
 * branches with index = r (mod m) are explored (each skipped branch still
 * excludes its class for later siblings, exactly as in the unsharded run),
 * so the union over r = 0..m-1 is the unsharded output.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* Compile-time width (step 15): with -DWFIX=n the bitsets have exactly n
 * 64-bit words and W is the constant n, so struct copies move n words instead
 * of 32 and the word loops unroll.  Requires (p-1)/2 + 1 <= 64 n, and n words
 * must be enough (checked at start-up); the default build is unchanged. */
#ifdef WFIX
#define MAXW WFIX
#else
#define MAXW 32            /* h < 2048 */
#endif
#define MAXK 24
typedef struct { uint64_t w[MAXW]; } bs;

#ifdef WFIX
static int k, p, h;
#define W WFIX
#else
static int k, p, h, W;
#endif
static bs cov[2048];
static unsigned long long nodes = 0, leaves = 0, printed = 0;
static int L[MAXK + 1], nL;
static long maxtop = -1;
static long shard = 0, nshards = 1;   /* env LRC_SHARD / LRC_NSHARDS: split root branches */
/* LRC_SHARD_DEPTH=2 (step 15): split at depth 1 instead of the root.  Every
 * shard walks depths 0 and 1 identically (all root branches are explored), and
 * the children of depth-1 nodes are dealt out by a global counter in that
 * common order; skipped children still exclude their class for later
 * siblings.  Leaves at depth <= 1 are printed by shard 0 only.  The union over
 * shards is the unsharded output (tested); the finer jobs balance better. */
static int sharddepth = 1;
static unsigned long long d1count = 0;   /* LRC_SHARD_DEPTH=D >= 2: global count of the nodes at depth D-1 (D >= 3 added for gate251) */
static int shard_passed = 0;            /* the current path went through the depth-(D-1) shard filter */
static unsigned long long nodecap = 0;
static int quiet = 0;
static unsigned long long rng = 88172645463325252ULL;
static inline unsigned long long xs(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static inline int popc(const bs *a) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i]); return s; }
static inline int popand(const bs *a, const bs *b) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i] & b->w[i]); return s; }
static inline int isempty(const bs *a) { for (int i = 0; i < W; i++) if (a->w[i]) return 0; return 1; }
static inline int has(const bs *a, int x) { return (a->w[x >> 6] >> (x & 63)) & 1; }
static inline void clr(bs *a, int x) { a->w[x >> 6] &= ~(1ULL << (x & 63)); }

static int minimal(void) {
    for (int i = 0; i < nL; i++) {
        bs priv = cov[L[i]];
        for (int j = 0; j < nL; j++) if (j != i)
            for (int w = 0; w < W; w++) priv.w[w] &= ~cov[L[j]].w[w];
        if (isempty(&priv)) return 0;
    }
    return 1;
}

/* Private-time pruning (Allikvere, arXiv:2609.02604v2, Lemma 4.1), enabled
 * with LRC_PRUNE=1.  Every class covers exactly m = floor((p-1)/(k+1)) of the
 * n = (p-1)/2 folded times, so in a cover by s classes at least 2n - s*m
 * times are covered exactly once, and some class has
 * q_s = ceil(max(0, 2n - s*m)/s) private times.  Units preserve private
 * times, so every orbit of minimal covers has a representative containing
 * class 1 with priv(1) >= q_|C|.  We keep only those (leaf filter), and since
 * priv(1) only shrinks as classes are added and q_s is non-increasing in s,
 * a node with priv(1) < q_k has no such leaf below it (cut). */
static int prune = 0, qk = 0, mcov = 0;
static int qs(int s) { long t = 2L * h - (long)s * mcov; if (t <= 0) return 0; return (int)((t + s - 1) / s); }
static bs others;   /* union of cov of chosen classes other than class 1 */
/* LRC_PRUNE=2 adds the max-private normalisation (Allikvere §4.1, "each orbit
 * has a representative with enough times covered by just one speed"; the
 * locked-time rule is Lemma M of the munim notes): scale so that class 1 has
 * the MOST private times in C (any class attaining the maximum).  Leaf filter:
 * priv(1) >= priv(v) for every v in C.  Cut: a private time of a chosen class v
 * that no still-allowed class covers stays private to v in every completion,
 * while priv(1) can only shrink; so if |locked(v)| > priv(1) no leaf below
 * passes the filter. */
static int priv1(const bs *O) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(cov[1].w[i] & ~O->w[i]); return s; }

/* Irredundance-aware cuts, enabled with LRC_IRR (a bitmask, step 7): bit 1
 * enables (i)+(ii), bit 2 enables (iii); LRC_IRR=2 is the recommended setting
 * (measured: (iii) gives nearly all the node saving, (i)+(ii) cost more
 * time per node than they save).  All of them remove
 * only nodes/classes that cannot lead to a MINIMAL cover, so the printed set
 * of minimal covers is exactly the same as without them (tested):
 *  (i)  if some chosen class has no private time w.r.t. the other chosen
 *       classes, no minimal cover lies below (adding classes only shrinks
 *       private sets), so the node is cut;
 *  (ii) an allowed class c with P_v subset of cov(c) for some chosen v (P_v =
 *       v's private times) would make v redundant in every cover containing
 *       c below this node, so c is removed from the allowed set of the subtree;
 *  (iii) gain bound: the `left` largest gains |cov(c) & U| over allowed c
 *       must sum to at least |U| (the plain bound uses left * max gain).
 * irr_cuts returns 0 to cut; otherwise *Aout is the reduced allowed set. */
static int irr = 0, maxcov = 0;   /* maxcov = max |cov(c)| (gains are <= it) */
/* Two-branch search (Allikvere, arXiv:2609.02604v2 Sec. 4.1), enabled with
 * LRC_TWOBRANCH=1 (step 11).  The minimal covers C with 1 in C, |C| <= k are
 * split by size and searched in two trees:
 *   branch 1: |C| = k exactly.  Depth limit k; leaves with |L| < k are not
 *     printed; extra cut |U| >= k - |L|: each class of C not yet chosen has a
 *     private time (C is minimal), that time is not covered by L, and private
 *     times of distinct classes are distinct.
 *   branch 2: |C| <= k-1.  Depth limit k-1, so the gain bound and the
 *     private-time node cut use k-1: with LRC_PRUNE the cut is q_{k-1} >= q_k.
 * Every cut removes only nodes with no admissible leaf below, so the union of
 * the two outputs is exactly the single-tree output (tested). */
static int kmax = 0, exactk = 0;
/* Child ordering and child-gain cutoff, enabled with LRC_ORDER=1 (step 12;
 * the rules are those described in the change log of Allikvere's generator,
 * basegen_v66_lf.cpp v6.3, reimplemented here from that description).
 *  - The children of the chosen time a (allowed classes covering a) are tried
 *    in order of DEScending gain |cov(c) & U|, ties by ascending c, instead of
 *    ascending c.  Exclusion of earlier siblings is unchanged, and the
 *    completeness/uniqueness argument in the header holds for any fixed child
 *    order, so the printed set of minimal covers is unchanged (tested).
 *  - Cutoff: after child c the other (left-1) classes cover at most bsum =
 *    the sum of the (left-1) largest gains over the allowed classes (gains only
 *    shrink below the node), so c is dead if g_c + bsum < |U|; the siblings
 *    after it have g <= g_c and are dead too, so the loop stops. */
static int order = 0;
/* LRC_IRR bit 4 (step 12): incremental redundancy cut.  State per depth d:
 * cv2[d] = times covered at least twice by L, pv[d][j] = private times of the
 * j-th chosen class.  Adding class c: newly2 = cov(c) & covered & ~cv2;
 * every earlier private set loses newly2; if one becomes empty that class has
 * no private time in any completion (private sets only shrink), so no minimal
 * cover lies below and the child is skipped (its class is still excluded for
 * later siblings).  Same cut as bit 1 part (i), at O(|L|) instead of O(|L|^2)
 * mask work per child, and applied before the child node is created. */
static bs cv2[MAXK + 2], pv[MAXK + 2][MAXK + 1];
static void irr4_init(void) { memset(&cv2[1], 0, sizeof(bs)); pv[1][0] = cov[1]; }
/* returns 1 if child c (added at depth d = |L|, uncovered set U) passes */
static int irr4_add(int d, int c, const bs *U) {
    bs n2; int ok = 1;
    for (int w = 0; w < W; w++) { n2.w[w] = cov[c].w[w] & ~U->w[w] & ~cv2[d].w[w]; cv2[d + 1].w[w] = cv2[d].w[w] | n2.w[w]; pv[d + 1][d].w[w] = cov[c].w[w] & U->w[w]; }
    for (int j = 0; j < d; j++) {
        uint64_t any = 0;
        for (int w = 0; w < W; w++) { pv[d + 1][j].w[w] = pv[d][j].w[w] & ~n2.w[w]; any |= pv[d + 1][j].w[w]; }
        if (!any) ok = 0;
    }
    return ok;
}
static int irr_cuts(const bs *U, const bs *A, bs *Aout) {
    *Aout = *A;
    if (nL >= 2 && (irr & 1)) {
        bs P[MAXK + 1];
        for (int i = 0; i < nL; i++) {
            P[i] = cov[L[i]];
            for (int j = 0; j < nL; j++) if (j != i)
                for (int w = 0; w < W; w++) P[i].w[w] &= ~cov[L[j]].w[w];
            if (isempty(&P[i])) return 0;
        }
        /* classes c with P_i subset of cov(c): c covers every a in P_i, and the
         * coverers of time a are exactly cov[a] (d_p(av) is symmetric in a, v) */
        for (int i = 0; i < nL; i++) {
            bs F; int first = 1, any = 1;
            for (int w = 0; w < W && any; w++) {
                uint64_t x = P[i].w[w];
                while (x) {
                    int a = w * 64 + __builtin_ctzll(x); x &= x - 1;
                    if (first) { F = cov[a]; first = 0; }
                    else { any = 0; for (int u = 0; u < W; u++) { F.w[u] &= cov[a].w[u]; if (F.w[u]) any = 1; } }
                    if (!any) break;
                }
            }
            if (!first && any) for (int u = 0; u < W; u++) Aout->w[u] &= ~F.w[u];
        }
    }
    if ((irr & 2) && !isempty(U)) {
        int hist[2049]; int mx = 0;
        memset(hist, 0, (maxcov + 1) * sizeof(int));
        for (int c = 1; c <= h; c++) if (has(Aout, c)) { int g = popand(&cov[c], U); hist[g]++; if (g > mx) mx = g; }
        long need = popc(U), got = 0; int left = kmax - nL;
        for (int g = mx; g > 0 && left > 0; g--) {
            int take = hist[g] < left ? hist[g] : left;
            got += (long)take * g; left -= take;
        }
        if (got < need) return 0;
    }
    return 1;
}

/* Orderly-root rule (LRC_ORDERLY=1, step 16; Toner, "Seventeen lonely
 * runners, assuming sixteen", Zenodo 10.5281/zenodo.23552885, Appendix B,
 * Lemma B.1, reimplemented from the paper's text; his code was not run).
 * At the root the branching time and its candidate list R = (r_0, r_1, ...)
 * (in the child order used) are fixed.  For a cover S containing 1 let
 * rho(S) = least i with r_i in S; the DFS finds S in the subtree of r_rho(S).
 * S is canonical iff the pair (rho(S), sorted(S)) is lexicographically least
 * among the pairs of s^-1 S (folded), s in S.  Each unit orbit of minimal
 * covers has exactly one canonical member, and one member per orbit suffices
 * for the multiset expansion (u maps C + extras to u C + u extras).
 * Cut: at a node in the subtree of r_rho with selection T, if s^-1 T contains
 * some r_i with i < rho (s in T), every completion S has rho(s^-1 S) <= i <
 * rho(S), so S is not canonical.  The class-1 private-time quota is not
 * invariant under rescaling, so LRC_ORDERLY requires LRC_PRUNE=0. */
static int orderly = 0, rho = -1;
static int ridx[2048], invt[2048];
static unsigned short *quot;   /* quot[a*(h+1)+b] = fold(a * b^-1), built when LRC_ORDERLY is set */
static inline int fold(long x) { x %= p; if (x < 0) x += p; return x < p - x ? (int)x : (int)(p - x); }
static void orderly_root(const int *R, int nr) {
    for (int c = 0; c <= h; c++) ridx[c] = 1 << 30;
    for (int i = 0; i < nr; i++) ridx[R[i]] = i;
}
/* may class c join L[0..nL-1] in the subtree of r_rho? */
static int orderly_ok(int c) {
    for (int i = 0; i < nL; i++) {
        int t = L[i];
        if (ridx[quot[c * (h + 1) + t]] < rho) return 0;
        if (ridx[quot[t * (h + 1) + c]] < rho) return 0;
    }
    return 1;
}
static int orderly_canonical(void) {
    int S[MAXK + 1], T[MAXK + 1], n = nL, rs = 1 << 30;
    for (int i = 0; i < n; i++) { S[i] = L[i]; if (ridx[S[i]] < rs) rs = ridx[S[i]]; }
    for (int i = 1; i < n; i++) { int x = S[i], j = i - 1; while (j >= 0 && S[j] > x) { S[j + 1] = S[j]; j--; } S[j + 1] = x; }
    for (int a = 0; a < n; a++) {
        int s0 = L[a], rt = 1 << 30;
        for (int i = 0; i < n; i++) { T[i] = quot[L[i] * (h + 1) + s0]; if (ridx[T[i]] < rt) rt = ridx[T[i]]; }
        if (rt > rs) continue;
        if (rt < rs) return 0;
        for (int i = 1; i < n; i++) { int x = T[i], j = i - 1; while (j >= 0 && T[j] > x) { T[j + 1] = T[j]; j--; } T[j + 1] = x; }
        for (int i = 0; i < n; i++) { if (T[i] < S[i]) return 0; if (T[i] > S[i]) break; }
    }
    return 1;
}

/* Leaf processing for L[0..nL-1] covering every time (others = union of
 * cov over L[1..]): the normalisation filters, then minimality, then print. */
static void leaf(void) {
        if (nshards > 1 && sharddepth >= 2 && !shard_passed && shard != 0) return;   /* leaves above the cut (incl. LRC_FINISH leaves) only in shard 0 */
        leaves++;
        if (exactk && nL != kmax) return;
        if (orderly && !orderly_canonical()) return;
        if (prune && priv1(&others) < qs(nL)) return;
        if (prune >= 2) {
            int p1 = priv1(&others);
            for (int i = 1; i < nL; i++) {
                int c = 0;
                for (int w = 0; w < W; w++) {
                    uint64_t x = cov[L[i]].w[w];
                    for (int j = 0; j < nL; j++) if (j != i) x &= ~cov[L[j]].w[w];
                    c += __builtin_popcountll(x);
                }
                if (c > p1) return;
            }
        }
        if (minimal()) {
            printed++;
            if (!quiet) {
                for (int i = 0; i < nL; i++) printf(i ? " %d" : "%d", L[i]);
                putchar('\n');
            }
        }
}

/* Exact two-slot finish (LRC_FINISH=1, step 15; rule from the change log of
 * Allikvere's generator, v6.2, reimplemented).  At a node with two classes
 * left, after the first child c1 (uncovered set U1 = U minus cov(c1), allowed
 * set A1), a second class c2 completes the cover iff c2 is in A1 and covers
 * every time of U1, i.e. c2 lies in the intersection of the coverer sets
 * cov[t] (t in U1; coverers of t are cov[t] by symmetry).  Those c2 are
 * enumerated directly and passed to leaf(); every cut the generic child node
 * would apply removes only nodes with no admissible leaf, and leaf() applies
 * all leaf filters, so the printed set is unchanged (tested). */
static int finish = 0;
static void finish2(const bs *U1, const bs *A1) {
    nodes++;
    bs comp = *A1;
    uint64_t any = 1;
    for (int w = 0; w < W && any; w++) {
        uint64_t x = U1->w[w];
        while (x) {
            int t = w * 64 + __builtin_ctzll(x); x &= x - 1;
            any = 0;
            for (int u = 0; u < W; u++) { comp.w[u] &= cov[t].w[u]; any |= comp.w[u]; }
            if (!any) break;
        }
    }
    if (!any) return;
    for (int w = 0; w < W; w++) {
        uint64_t x = comp.w[w];
        while (x) {
            int c2 = w * 64 + __builtin_ctzll(x); x &= x - 1;
            bs saveO = others;
            for (int u = 0; u < W; u++) others.w[u] |= cov[c2].w[u];
            L[nL++] = c2;
            nodes++;
            leaf();
            nL--;
            others = saveO;
        }
    }
}

static void dfs(const bs *U, const bs *A, int depth) {
    nodes++;
    if (nodecap && nodes >= nodecap) return;
    if (isempty(U)) { leaf(); return; }
    if (nL == kmax) return;
    if (exactk && popc(U) < kmax - nL) return;
    static bs Airr[MAXK + 2];
    /* with LRC_ORDER the gains are computed once per node (below) and feed the
     * sharper gain bound, the cutoff and the child order, so irr_cuts runs
     * only its bit-1 part here */
    int irr_here = order ? (irr & ~2) : irr;
    if (irr_here) { int sv = irr; irr = irr_here; int ok = irr_cuts(U, A, &Airr[nL]); irr = sv; if (!ok) return; A = &Airr[nL]; }
    int need = popc(U), left = kmax - nL, maxg = 0;
    static unsigned short G[2048];
    long bsum = 0;
    if (order) {
        int gh[2049]; memset(gh, 0, (maxcov + 1) * sizeof(int));
        for (int w = 0; w < W; w++) {
            uint64_t x = A->w[w];
            while (x) { int c = w * 64 + __builtin_ctzll(x); x &= x - 1; int g = popand(&cov[c], U); G[c] = (unsigned short)g; gh[g]++; }
        }
        long got = 0; int lft = left;
        for (int g = maxcov; g > 0 && lft > 0; g--) { int t = gh[g] < lft ? gh[g] : lft; got += (long)t * g; lft -= t; }
        if (got < need) return;               /* sharper gain bound (LRC_IRR bit 2) */
        lft = left - 1;                        /* bsum = sum of the (left-1) largest gains */
        for (int g = maxcov; g > 0 && lft > 0; g--) { int t = gh[g] < lft ? gh[g] : lft; bsum += (long)t * g; lft -= t; }
    }
    /* gain bound (implied by the sharper bound when irr & 2 or order) */
    if (!(irr & 2) && !order) {
        for (int c = 1; c <= h; c++) if (has(A, c)) { int g = popand(&cov[c], U); if (g > maxg) maxg = g; }
        if ((long)left * maxg < need) return;
    }
    if (prune >= 2 && nL > 1) {
        bs reach; memset(&reach, 0, sizeof reach);
        for (int c = 1; c <= h; c++) if (has(A, c)) for (int w = 0; w < W; w++) reach.w[w] |= cov[c].w[w];
        int p1 = priv1(&others), maxlocked = 0;
        for (int i = 1; i < nL; i++) {
            int c = 0;
            for (int w = 0; w < W; w++) {
                uint64_t x = cov[L[i]].w[w] & ~reach.w[w];
                for (int j = 0; j < nL; j++) if (j != i) x &= ~cov[L[j]].w[w];
                c += __builtin_popcountll(x);
            }
            if (c > p1) return;
            if (c > maxlocked) maxlocked = c;
        }
        /* forbid classes that would leave class 1 with fewer private times
         * than some class's locked times (forbidding only adds locked times) */
        if (maxlocked > 0) {
            static bs Aloc[MAXK + 2];
            Aloc[nL] = *A;
            bs P1; for (int w = 0; w < W; w++) P1.w[w] = cov[1].w[w] & ~others.w[w];
            for (int c = 1; c <= h; c++) if (has(A, c)) {
                if (p1 - popand(&P1, &cov[c]) < maxlocked) clr(&Aloc[nL], c);
            }
            A = &Aloc[nL];
            /* re-check the gain bound with the smaller allowed set */
            maxg = 0;
            for (int c = 1; c <= h; c++) if (has(A, c)) { int g = popand(&cov[c], U); if (g > maxg) maxg = g; }
            if ((long)left * maxg < need) return;
        }
    }
    /* most constrained uncovered time (times are bit positions 1..h) */
    int besta = -1, bestm = 1 << 30;
    for (int a = 1; a <= h; a++) if (has(U, a)) {
        int m = popand(&cov[a], A);   /* coverers of a = cov[a] by symmetry */
        if (m < bestm) { bestm = m; besta = a; if (m <= 1) break; }
    }
    if (bestm == 0) return;
    bs A2 = *A;
    long branch = 0;
    int ch[2048], nch = 0, chg[2048];
    for (int w = 0; w < W; w++) {
        uint64_t x = cov[besta].w[w] & A->w[w];
        while (x) { ch[nch++] = w * 64 + __builtin_ctzll(x); x &= x - 1; }
    }
    if (order) {
        for (int i = 0; i < nch; i++) chg[i] = G[ch[i]];
        for (int i = 1; i < nch; i++) {   /* insertion sort: gain desc, class asc */
            int c = ch[i], g = chg[i], j = i - 1;
            while (j >= 0 && (chg[j] < g || (chg[j] == g && ch[j] > c))) { ch[j + 1] = ch[j]; chg[j + 1] = chg[j]; j--; }
            ch[j + 1] = c; chg[j + 1] = g;
        }
    }
    if (orderly && depth == 0) orderly_root(ch, nch);
    for (int ci = 0; ci < nch; ci++) {
        int c = ch[ci];
        if (order && chg[ci] + bsum < need) break;
        if (depth == 0 && maxtop >= 0 && branch >= maxtop) break;
        branch++;
        clr(&A2, c);                  /* excluded for later siblings and below */
        if (nshards > 1 && sharddepth == 1 && depth == 0 && (branch - 1) % nshards != shard) continue;
        if (nshards > 1 && sharddepth >= 2 && depth == sharddepth - 1 && (long)(d1count++ % nshards) != shard) continue;
        bs saveO = others;
        for (int w = 0; w < W; w++) others.w[w] |= cov[c].w[w];
        if (prune && priv1(&others) < qk) { others = saveO; continue; }
        if ((irr & 4) && !irr4_add(nL, c, U)) { others = saveO; continue; }
        if (orderly) { if (depth == 0) rho = ci; if (!orderly_ok(c)) { others = saveO; continue; } }
        bs U2; for (int w = 0; w < W; w++) U2.w[w] = U->w[w] & ~cov[c].w[w];
        L[nL++] = c;
        int sp_save = shard_passed;
        if (nshards > 1 && sharddepth >= 2 && depth == sharddepth - 1) shard_passed = 1;
        if (finish && left == 2 && !isempty(&U2)) finish2(&U2, &A2);
        else dfs(&U2, &A2, depth + 1);
        shard_passed = sp_save;
        nL--;
        others = saveO;
    }
}

/* One random root-to-leaf probe; returns the Knuth estimate of the number
 * of nodes (sum over depths of the product of branching factors). */
static double probe(bs U, bs A) {
    double est = 1.0, mult = 1.0;
    nL = 1;
    bs O; memset(&O, 0, sizeof O);
    for (;;) {
        if (isempty(&U) || nL == kmax) return est;
        if (exactk && popc(&U) < kmax - nL) return est;
        if (irr) { bs A3; if (!irr_cuts(&U, &A, &A3)) return est; A = A3; }
        int need = popc(&U), left = kmax - nL, maxg = 0;
        for (int c = 1; c <= h; c++) if (has(&A, c)) { int g = popand(&cov[c], &U); if (g > maxg) maxg = g; }
        if ((long)left * maxg < need) return est;
        int besta = -1, bestm = 1 << 30;
        for (int a = 1; a <= h; a++) if (has(&U, a)) {
            int m = popand(&cov[a], &A);
            if (m < bestm) { bestm = m; besta = a; if (m <= 1) break; }
        }
        if (bestm == 0) return est;
        /* children = candidates not removed by the private-time node cut (a
         * skipped candidate still excludes its class for later siblings) */
        int cand[2048], nc = 0, kept[2048], nk = 0;
        int oc[2048], og[2048], no = 0; long bsum = 0;
        for (int c = 1; c <= h; c++) if (has(&cov[besta], c) && has(&A, c)) { oc[no] = c; og[no++] = popand(&cov[c], &U); }
        if (order) {
            int gh[2049]; memset(gh, 0, (maxcov + 1) * sizeof(int));
            for (int c = 1; c <= h; c++) if (has(&A, c)) gh[popand(&cov[c], &U)]++;
            int lft = left - 1;
            for (int g = maxcov; g > 0 && lft > 0; g--) { int t = gh[g] < lft ? gh[g] : lft; bsum += (long)t * g; lft -= t; }
            for (int i = 1; i < no; i++) {
                int c = oc[i], g = og[i], j = i - 1;
                while (j >= 0 && (og[j] < g || (og[j] == g && oc[j] > c))) { oc[j + 1] = oc[j]; og[j + 1] = og[j]; j--; }
                oc[j + 1] = c; og[j + 1] = g;
            }
        }
        if (orderly && nL == 1) orderly_root(oc, no);
        for (int oi = 0; oi < no; oi++) {
            int c = oc[oi];
            if (order && og[oi] + bsum < need) break;
            if (orderly) { int sv = rho; if (nL == 1) rho = oi; int ok = orderly_ok(c); if (nL == 1) rho = sv; if (!ok) { cand[nc++] = c; continue; } }
            if (prune) { bs O2; for (int w = 0; w < W; w++) O2.w[w] = O.w[w] | cov[c].w[w]; if (priv1(&O2) < qk) { cand[nc++] = c; continue; } }
            if ((irr & 4) && !irr4_add(nL, c, &U)) { cand[nc++] = c; continue; }
            kept[nk++] = nc; cand[nc++] = c;
        }
        if (nk == 0) return est;
        int i = kept[(int)(xs() % (unsigned long long)nk)];
        if (orderly && nL == 1) rho = i;
        if (irr & 4) irr4_add(nL, cand[i], &U);   /* recompute the chosen child's state */
        for (int j = 0; j <= i; j++) clr(&A, cand[j]);
        for (int w = 0; w < W; w++) { U.w[w] &= ~cov[cand[i]].w[w]; O.w[w] |= cov[cand[i]].w[w]; }
        L[nL++] = cand[i];
        mult *= nk;
        est += mult;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: covergen k p [maxtop]\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]);
    if (argc > 3) maxtop = atol(argv[3]);
    if (getenv("LRC_PRUNE")) prune = atoi(getenv("LRC_PRUNE"));
    if (getenv("LRC_IRR")) irr = atoi(getenv("LRC_IRR"));
    if (getenv("LRC_ORDER")) order = atoi(getenv("LRC_ORDER"));
    if (getenv("LRC_FINISH")) finish = atoi(getenv("LRC_FINISH"));
    if (getenv("LRC_ORDERLY")) orderly = atoi(getenv("LRC_ORDERLY"));
    if (orderly && prune) { fprintf(stderr, "LRC_ORDERLY requires LRC_PRUNE=0 (the class-1 quota is not unit-invariant)\n"); return 2; }
    int twob = getenv("LRC_TWOBRANCH") ? atoi(getenv("LRC_TWOBRANCH")) : 0;
    if (getenv("LRC_SHARD_DEPTH")) sharddepth = atoi(getenv("LRC_SHARD_DEPTH"));
    if (getenv("LRC_NSHARDS")) { nshards = atol(getenv("LRC_NSHARDS")); shard = getenv("LRC_SHARD") ? atol(getenv("LRC_SHARD")) : 0; }
    long probes = 0;
    if (argc > 6) { probes = atol(argv[4]); rng ^= (unsigned long long)atol(argv[5]) * 2654435761ULL; nodecap = strtoull(argv[6], 0, 10); maxtop = -1; quiet = 1; }
    h = (p - 1) / 2;
#ifdef WFIX
    if ((h + 1 + 63) / 64 != WFIX) { fprintf(stderr, "this build needs (p-1)/2+1 in (%d,%d] (WFIX=%d)\n", 64 * (WFIX - 1), 64 * WFIX, WFIX); return 2; }
#else
    W = (h + 1 + 63) / 64;
#endif
    if (k < 2 || k > MAXK || p < 5 || h + 1 > 64 * MAXW) { fprintf(stderr, "bad args\n"); return 2; }
    for (int v = 1; v <= h; v++)
        for (int a = 1; a <= h; a++) {
            long r = ((long)a * v) % p, d = r < p - r ? r : p - r;
            if ((long)(k + 1) * d < p) cov[v].w[a >> 6] |= 1ULL << (a & 63);
        }
    for (int v = 1; v <= h; v++) { long r = 1, b = v, e = p - 2; while (e) { if (e & 1) r = r * b % p; b = b * b % p; e >>= 1; } invt[v] = (int)r; }
    if (orderly) {
        quot = malloc(sizeof(unsigned short) * (size_t)(h + 1) * (h + 1));
        for (int a = 1; a <= h; a++) for (int b = 1; b <= h; b++) quot[a * (h + 1) + b] = (unsigned short)fold((long)a * invt[b]);
    }
    mcov = (p - 1) / (k + 1);
    for (int v = 1; v <= h; v++) { int c = popc(&cov[v]); if (c > maxcov) maxcov = c; }
    qk = qs(k);
    kmax = k;
    memset(&others, 0, sizeof others);
    bs U, A; memset(&U, 0, sizeof U); memset(&A, 0, sizeof A);
    for (int a = 1; a <= h; a++) { U.w[a >> 6] |= 1ULL << (a & 63); A.w[a >> 6] |= 1ULL << (a & 63); }
    for (int w = 0; w < W; w++) U.w[w] &= ~cov[1].w[w];
    clr(&A, 1);
    L[0] = 1; nL = 1;
    irr4_init();
    if (probes > 0) {
        int nb = twob ? 2 : 1;
        for (int b = 1; b <= nb; b++) {
            if (twob) { exactk = (b == 1); kmax = b == 1 ? k : k - 1; qk = qs(kmax); }
            double sum = 0, sum2 = 0;
            for (long r = 0; r < probes; r++) { double e = probe(U, A); sum += e; sum2 += e * e; }
            double mean = sum / probes, var = sum2 / probes - mean * mean;
            fprintf(stderr, "knuth_estimate_nodes %.6e stderr %.3e probes %ld branch %d prune %d irr %d\n", mean, var > 0 ? sqrt(var / probes) : 0.0, probes, twob ? b : 0, prune, irr);
        }
        if (twob) { exactk = 1; kmax = k; qk = qs(k); }
        nL = 1;
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        dfs(&U, &A, 0);
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double secs = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
        fprintf(stderr, "capped_dfs nodes %llu secs %.3f nodes_per_sec %.3e\n", nodes, secs, nodes / secs);
        return 0;
    }
    if (twob) {
        unsigned long long n1, c1;
        exactk = 1; kmax = k; qk = qs(k);
        dfs(&U, &A, 0);
        n1 = nodes; c1 = printed;
        fprintf(stderr, "branch 1 (|C| = %d): nodes %llu minimal_covers %llu q %d\n", k, n1, c1, qk);
        exactk = 0; kmax = k - 1; qk = qs(k - 1); nL = 1; memset(&others, 0, sizeof others);
        dfs(&U, &A, 0);
        fprintf(stderr, "branch 2 (|C| <= %d): nodes %llu minimal_covers %llu q %d\n", k - 1, nodes - n1, printed - c1, qk);
    } else dfs(&U, &A, 0);
    fprintf(stderr, "nodes %llu leaves %llu minimal_covers %llu prune %d q_k %d m %d irr %d twobranch %d order %d\n", nodes, leaves, printed, prune, qs(k), mcov, irr, twob, order);
    return 0;
}
