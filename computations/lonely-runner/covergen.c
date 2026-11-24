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

#define MAXW 32            /* h < 2048 */
#define MAXK 24
typedef struct { uint64_t w[MAXW]; } bs;

static int k, p, h, W;
static bs cov[2048];
static unsigned long long nodes = 0, leaves = 0, printed = 0;
static int L[MAXK + 1], nL;
static long maxtop = -1;
static long shard = 0, nshards = 1;   /* env LRC_SHARD / LRC_NSHARDS: split root branches */
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

static void dfs(const bs *U, const bs *A, int depth) {
    nodes++;
    if (nodecap && nodes >= nodecap) return;
    if (isempty(U)) {
        leaves++;
        if (minimal()) {
            printed++;
            if (!quiet) {
                for (int i = 0; i < nL; i++) printf(i ? " %d" : "%d", L[i]);
                putchar('\n');
            }
        }
        return;
    }
    if (nL == k) return;
    int need = popc(U), left = k - nL, maxg = 0;
    /* gain bound */
    for (int c = 1; c <= h; c++) if (has(A, c)) { int g = popand(&cov[c], U); if (g > maxg) maxg = g; }
    if ((long)left * maxg < need) return;
    /* most constrained uncovered time (times are bit positions 1..h) */
    int besta = -1, bestm = 1 << 30;
    for (int a = 1; a <= h; a++) if (has(U, a)) {
        int m = popand(&cov[a], A);   /* coverers of a = cov[a] by symmetry */
        if (m < bestm) { bestm = m; besta = a; if (m <= 1) break; }
    }
    if (bestm == 0) return;
    bs A2 = *A;
    long branch = 0;
    for (int c = 1; c <= h; c++) if (has(&cov[besta], c) && has(A, c)) {
        if (depth == 0 && maxtop >= 0 && branch >= maxtop) break;
        branch++;
        clr(&A2, c);                  /* excluded for later siblings and below */
        if (depth == 0 && nshards > 1 && (branch - 1) % nshards != shard) continue;
        bs U2; for (int w = 0; w < W; w++) U2.w[w] = U->w[w] & ~cov[c].w[w];
        L[nL++] = c;
        dfs(&U2, &A2, depth + 1);
        nL--;
    }
}

/* One random root-to-leaf probe; returns the Knuth estimate of the number
 * of nodes (sum over depths of the product of branching factors). */
static double probe(bs U, bs A) {
    double est = 1.0, mult = 1.0;
    nL = 1;
    for (;;) {
        if (isempty(&U) || nL == k) return est;
        int need = popc(&U), left = k - nL, maxg = 0;
        for (int c = 1; c <= h; c++) if (has(&A, c)) { int g = popand(&cov[c], &U); if (g > maxg) maxg = g; }
        if ((long)left * maxg < need) return est;
        int besta = -1, bestm = 1 << 30;
        for (int a = 1; a <= h; a++) if (has(&U, a)) {
            int m = popand(&cov[a], &A);
            if (m < bestm) { bestm = m; besta = a; if (m <= 1) break; }
        }
        if (bestm == 0) return est;
        int cand[2048], nc = 0;
        for (int c = 1; c <= h; c++) if (has(&cov[besta], c) && has(&A, c)) cand[nc++] = c;
        int i = (int)(xs() % (unsigned long long)nc);
        for (int j = 0; j <= i; j++) clr(&A, cand[j]);
        for (int w = 0; w < W; w++) U.w[w] &= ~cov[cand[i]].w[w];
        L[nL++] = cand[i];
        mult *= nc;
        est += mult;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: covergen k p [maxtop]\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]);
    if (argc > 3) maxtop = atol(argv[3]);
    if (getenv("LRC_NSHARDS")) { nshards = atol(getenv("LRC_NSHARDS")); shard = getenv("LRC_SHARD") ? atol(getenv("LRC_SHARD")) : 0; }
    long probes = 0;
    if (argc > 6) { probes = atol(argv[4]); rng ^= (unsigned long long)atol(argv[5]) * 2654435761ULL; nodecap = strtoull(argv[6], 0, 10); maxtop = -1; quiet = 1; }
    h = (p - 1) / 2; W = (h + 1 + 63) / 64;
    if (k < 2 || k > MAXK || p < 5 || h + 1 > 64 * MAXW) { fprintf(stderr, "bad args\n"); return 2; }
    for (int v = 1; v <= h; v++)
        for (int a = 1; a <= h; a++) {
            long r = ((long)a * v) % p, d = r < p - r ? r : p - r;
            if ((long)(k + 1) * d < p) cov[v].w[a >> 6] |= 1ULL << (a & 63);
        }
    bs U, A; memset(&U, 0, sizeof U); memset(&A, 0, sizeof A);
    for (int a = 1; a <= h; a++) { U.w[a >> 6] |= 1ULL << (a & 63); A.w[a >> 6] |= 1ULL << (a & 63); }
    for (int w = 0; w < W; w++) U.w[w] &= ~cov[1].w[w];
    clr(&A, 1);
    L[0] = 1; nL = 1;
    if (probes > 0) {
        double sum = 0, sum2 = 0;
        for (long r = 0; r < probes; r++) { double e = probe(U, A); sum += e; sum2 += e * e; }
        double mean = sum / probes, var = sum2 / probes - mean * mean;
        fprintf(stderr, "knuth_estimate_nodes %.6e stderr %.3e probes %ld\n", mean, var > 0 ? sqrt(var / probes) : 0.0, probes);
        nL = 1;
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        dfs(&U, &A, 0);
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double secs = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
        fprintf(stderr, "capped_dfs nodes %llu secs %.3f nodes_per_sec %.3e\n", nodes, secs, nodes / secs);
        return 0;
    }
    dfs(&U, &A, 0);
    fprintf(stderr, "nodes %llu leaves %llu minimal_covers %llu\n", nodes, leaves, printed);
    return 0;
}
