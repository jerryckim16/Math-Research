/* liftfree.c -- all witness-free lifts of one level-one tuple to level c.
 *
 * Usage: liftfree k M c        (tuples b_1..b_k, residues mod M, one per
 *        line on stdin; M = l*p is the current level's modulus)
 * N = c*M.  Lifts: w_i = b_i + j_i*M, 0 <= j_i < c (c^k tuples, the full
 * lift fibre as in arXiv:2604.23906).
 * w is WITNESS-FREE if no m in [0,N) has (k+1)*d_N(m*w_i) >= N for all i.
 * (The gcd alternative of properness is NOT applied here; the caller does it.)
 * Branch and bound over coordinates: acc = good times left; a branch is cut
 * when the remaining coordinates, each removing at most max_j |acc \ good(w)|
 * times, cannot empty acc.  Cut branches contain no witness-free lift.
 * Output: "idx w_1 .. w_k" per witness-free lift (idx = 0-based input line);
 * total node count to stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 24
#define MAXC 64
#define MAXW 256   /* N < 16384 */
typedef struct { uint64_t w[MAXW]; } bs;
static int k, p, c, N, W;  /* p here is the base modulus M */
static long idx = 0;
static int b[MAXK];
static bs good[MAXK][MAXC];
static int cur[MAXK];
static unsigned long long nodes = 0, found = 0;

static int popc(const bs *a) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i]); return s; }
static int popandnot(const bs *a, const bs *g) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i] & ~g->w[i]); return s; }

static void dfs(int i, const bs *acc) {
    nodes++;
    int n = popc(acc);
    if (n == 0) {   /* every completion is witness-free */
        if (i == k) { found++; printf("%ld", idx); for (int t = 0; t < k; t++) printf(" %d", cur[t]); putchar('\n'); return; }
    }
    if (i == k) return;
    if (n > 0) {
        long cap = 0;
        for (int t = i; t < k; t++) {
            int best = 0;
            for (int j = 0; j < c; j++) { int r = popandnot(acc, &good[t][j]); if (r > best) best = r; }
            cap += best;
        }
        if (cap < n) return;
    }
    for (int j = 0; j < c; j++) {
        bs nxt; for (int x = 0; x < W; x++) nxt.w[x] = acc->w[x] & good[i][j].w[x];
        cur[i] = b[i] + j * p;
        dfs(i + 1, &nxt);
    }
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: liftfree k M c  < tuples\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); c = atoi(argv[3]);
    if (k > MAXK || c > MAXC || k < 1) { fprintf(stderr, "bad args\n"); return 2; }
    N = c * p; W = (N + 63) / 64;
    if (W > MAXW) { fprintf(stderr, "N too large\n"); return 2; }
    bs all; memset(&all, 0, sizeof all);
    for (int m = 0; m < N; m++) all.w[m >> 6] |= 1ULL << (m & 63);
    for (;;) {
        for (int i = 0; i < k; i++) {
            long x;
            if (scanf("%ld", &x) != 1) { fprintf(stderr, "nodes %llu witness_free %llu inputs %ld\n", nodes, found, idx); return 0; }
            b[i] = (int)(((x % p) + p) % p);
        }
        for (int i = 0; i < k; i++)
            for (int j = 0; j < c; j++) {
                long w = b[i] + (long)j * p;
                memset(&good[i][j], 0, sizeof(bs));
                for (int m = 0; m < N; m++) {
                    long r = (w * m) % N, d = r < N - r ? r : N - r;
                    if ((long)(k + 1) * d >= N) good[i][j].w[m >> 6] |= 1ULL << (m & 63);
                }
            }
        dfs(0, &all);
        idx++;
    }
}
