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

static void dfs(const bs *U, const bs *A, int depth) {
    nodes++;
    if (nodecap && nodes >= nodecap) return;
    if (isempty(U)) {
        leaves++;
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
        return;
    }
    if (nL == k) return;
    int need = popc(U), left = k - nL, maxg = 0;
    /* gain bound */
    for (int c = 1; c <= h; c++) if (has(A, c)) { int g = popand(&cov[c], U); if (g > maxg) maxg = g; }
    if ((long)left * maxg < need) return;
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
    for (int c = 1; c <= h; c++) if (has(&cov[besta], c) && has(A, c)) {
        if (depth == 0 && maxtop >= 0 && branch >= maxtop) break;
        branch++;
        clr(&A2, c);                  /* excluded for later siblings and below */
        if (depth == 0 && nshards > 1 && (branch - 1) % nshards != shard) continue;
        bs saveO = others;
        for (int w = 0; w < W; w++) others.w[w] |= cov[c].w[w];
        if (prune && priv1(&others) < qk) { others = saveO; continue; }
        bs U2; for (int w = 0; w < W; w++) U2.w[w] = U->w[w] & ~cov[c].w[w];
        L[nL++] = c;
        dfs(&U2, &A2, depth + 1);
        nL--;
        others = saveO;
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
    if (getenv("LRC_PRUNE")) prune = atoi(getenv("LRC_PRUNE"));
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
    mcov = (p - 1) / (k + 1);
    qk = qs(k);
    memset(&others, 0, sizeof others);
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
    fprintf(stderr, "nodes %llu leaves %llu minimal_covers %llu prune %d q_k %d m %d\n", nodes, leaves, printed, prune, qk, mcov);
    return 0;
}
