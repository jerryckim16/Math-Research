/* cascade_verify.c -- independent re-check of one binary-cascade step.
 *
 * Usage: cascade_verify k p l  < reps_at_level_l
 * Reads unit-orbit representatives at level l (residues mod M = l*p, one tuple
 * per line).  For each, enumerates the FULL lift fibre w_i = b_i + j_i*M,
 * j_i in {0,1} (2^k lifts, plain DFS, no branch-and-bound), keeps the lifts with
 * no witness on the (1/N)Z grid, N = 2M (witness: m with (k+1)*d_N(m*w_i) >= N
 * for all i), drops those proper by the gcd clause at level 2l
 * (gcd(2l, w_j : j != i) > 1 for some i), and prints the canonical form of each
 * survivor: lexicographic minimum over units u of Z_N of the sorted tuple of
 * min(u*w_i mod N, N - u*w_i mod N).  Caller sorts -u and compares.
 * Stderr: counts.  Written independently of liftfree.c and small_gates.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 20
#define MAXW 64
static int k, p, l, M, N, W, L2;
static uint64_t good[MAXK][2][MAXW];
static int b[MAXK], cur[MAXK];
static int units[20000], nu;
static unsigned long long nlifts = 0, nwf = 0, ngcd = 0, nout = 0;

static int gcd(int a, int c) { while (c) { int t = a % c; a = c; c = t; } return a < 0 ? -a : a; }

static int cmp_int(const void *x, const void *y) { return *(const int *)x - *(const int *)y; }

static void emit(void) {
    int best[MAXK], t[MAXK], have = 0;
    for (int ui = 0; ui < nu; ui++) {
        long u = units[ui];
        for (int i = 0; i < k; i++) { int r = (int)((u * cur[i]) % N); t[i] = r < N - r ? r : N - r; }
        qsort(t, k, sizeof(int), cmp_int);
        int lt = !have;
        for (int i = 0; have && i < k; i++) if (t[i] != best[i]) { lt = t[i] < best[i]; break; }
        if (lt) { memcpy(best, t, sizeof(int) * k); have = 1; }
    }
    for (int i = 0; i < k; i++) printf(i ? " %d" : "%d", best[i]);
    putchar('\n');
    nout++;
}

static int gcd_clause(void) {
    for (int i = 0; i < k; i++) {
        int g = L2;
        for (int j = 0; j < k && g > 1; j++) if (j != i) g = gcd(g, cur[j]);
        if (g > 1) return 1;
    }
    return 0;
}

static void dfs(int i, const uint64_t *acc) {
    if (i == k) {
        nlifts++;
        for (int x = 0; x < W; x++) if (acc[x]) return;   /* has a witness */
        nwf++;
        if (gcd_clause()) { ngcd++; return; }
        emit();
        return;
    }
    for (int j = 0; j < 2; j++) {
        uint64_t nxt[MAXW];
        for (int x = 0; x < W; x++) nxt[x] = acc[x] & good[i][j][x];
        cur[i] = b[i] + j * M;
        dfs(i + 1, nxt);
    }
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: cascade_verify k p l < reps\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); l = atoi(argv[3]);
    M = l * p; N = 2 * M; L2 = 2 * l; W = (N + 63) / 64;
    if (k > MAXK || W > MAXW) { fprintf(stderr, "too large\n"); return 2; }
    nu = 0; for (int u = 1; u < N; u++) if (gcd(u, N) == 1) units[nu++] = u;
    uint64_t all[MAXW]; memset(all, 0, sizeof all);
    for (int m = 0; m < N; m++) all[m >> 6] |= 1ULL << (m & 63);
    long reps = 0;
    for (;;) {
        int ok = 1;
        for (int i = 0; i < k; i++) { long x; if (scanf("%ld", &x) != 1) { ok = 0; break; } b[i] = (int)(((x % M) + M) % M); }
        if (!ok) break;
        reps++;
        for (int i = 0; i < k; i++) {
            if (b[i] % p == 0) { fprintf(stderr, "input divisible by p\n"); return 3; }
            for (int j = 0; j < 2; j++) {
                long w = b[i] + (long)j * M;
                memset(good[i][j], 0, sizeof(uint64_t) * MAXW);
                for (int m = 0; m < N; m++) {
                    long r = (w * m) % N, d = r < N - r ? r : N - r;
                    if ((long)(k + 1) * d >= N) good[i][j][m >> 6] |= 1ULL << (m & 63);
                }
            }
        }
        dfs(0, all);
    }
    fprintf(stderr, "reps %ld lifts %llu witness_free %llu gcd_proper %llu improper_out %llu\n",
            reps, nlifts, nwf, ngcd, nout);
    return 0;
}
