/* cascade_verify.c -- independent re-check of one cascade step, any lift factor c.
 * (k17struct version: generalises structure/cascade_verify.c from c = 2 to any c, adds NG.)
 *
 * Usage: cascade_verify k p l c [ng]  < reps_at_level_l
 * Reads unit-orbit representatives at level l (residues mod M = l*p, one tuple per line).
 * For each, enumerates the lift fibre w_i = b_i + j_i*M, j_i in {0..c-1} (c^k lifts) by DFS,
 * keeps the lifts with no witness on the (1/N)Z grid, N = c*M (witness: m with
 * (k+1)*d_N(m*w_i) >= N for all i), drops those proper by the gcd clause at level L = c*l
 * (gcd(L, w_j : j != i) > 1 for some i), with 'ng' also those settled by Lemma NG at some
 * divisor d >= 2 of L, and prints the canonical form of each survivor: the lexicographic
 * minimum over units u of Z_N of the sorted tuple of min(u*w_i mod N, N - u*w_i mod N).
 * Caller sorts -u and compares with the main pipeline (liftfree.c | orbit_filter.c).
 *
 * Pruning (different from liftfree.c's counting bound, and simpler): a branch at depth i is
 * cut iff some still-possible witness time m is good for EVERY choice j of EVERY remaining
 * coordinate t >= i; such an m survives to every leaf, so no leaf below is witness-free.
 * Coordinates are processed in REVERSE input order (liftfree.c uses input order).
 * Stderr: counts.  Written independently of liftfree.c, orbit_filter.c and small_gates.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 24
#define MAXC 8
#define MAXW 128          /* N <= 8192 */
static int k, p, l, c, M, N, W, LL, ng;
static uint64_t good[MAXK][MAXC][MAXW];
static uint64_t always[MAXK + 1][MAXW];   /* always[i] = AND over t >= i, j of good[t][j] */
static int b[MAXK], cur[MAXK], ord[MAXK];
static int units[10000], nu, divs[64], nd;
static unsigned long long nodes = 0, nwf = 0, ngcd = 0, nng = 0, nout = 0;

static int gcd(int a, int e) { while (e) { int t = a % e; a = e; e = t; } return a < 0 ? -a : a; }
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
        int g = LL;
        for (int j = 0; j < k && g > 1; j++) if (j != i) g = gcd(g, cur[j]);
        if (g > 1) return 1;
    }
    return 0;
}

/* Lemma NG: some divisor d >= 2 of LL with E = {i : d does not divide w_i}, 1 <= |E| < k and
 * sum_{i in E} g_i * ceil(2d / ((k+1) g_i)) < d, g_i = gcd(w_i, d). */
static int ng_settled(void) {
    for (int a = 0; a < nd; a++) {
        int d = divs[a], e = 0; long cost = 0;
        for (int i = 0; i < k; i++) {
            if (cur[i] % d == 0) continue;
            e++;
            int g = gcd(cur[i], d);
            long q = 0; while (q * (k + 1) * g < 2L * d) q++;      /* q = ceil(2d/((k+1)g)) */
            cost += (long)g * q;
        }
        if (e >= 1 && e < k && cost < d) return 1;
    }
    return 0;
}

static void dfs(int depth, const uint64_t *acc) {
    nodes++;
    if (depth == k) {
        for (int x = 0; x < W; x++) if (acc[x]) return;   /* has a witness */
        nwf++;
        if (gcd_clause()) { ngcd++; return; }
        if (ng && ng_settled()) { nng++; return; }
        emit();
        return;
    }
    for (int x = 0; x < W; x++) if (acc[x] & always[depth][x]) return;   /* sound cut */
    int i = ord[depth];
    for (int j = 0; j < c; j++) {
        uint64_t nxt[MAXW];
        for (int x = 0; x < W; x++) nxt[x] = acc[x] & good[i][j][x];
        cur[i] = b[i] + j * M;
        dfs(depth + 1, nxt);
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: cascade_verify k p l c [ng] < reps\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); l = atoi(argv[3]); c = atoi(argv[4]);
    ng = argc > 5 && !strcmp(argv[5], "ng");
    M = l * p; N = c * M; LL = c * l; W = (N + 63) / 64;
    if (k > MAXK || c > MAXC || W > MAXW) { fprintf(stderr, "too large\n"); return 2; }
    nu = 0; for (int u = 1; u < N; u++) if (gcd(u, N) == 1) units[nu++] = u;
    nd = 0; for (int d = 2; d <= LL; d++) if (LL % d == 0) divs[nd++] = d;
    for (int i = 0; i < k; i++) ord[i] = k - 1 - i;
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
            for (int j = 0; j < c; j++) {
                long w = b[i] + (long)j * M;
                memset(good[i][j], 0, sizeof(uint64_t) * MAXW);
                for (int m = 0; m < N; m++) {
                    long r = (w * m) % N, d = r < N - r ? r : N - r;
                    if ((long)(k + 1) * d >= N) good[i][j][m >> 6] |= 1ULL << (m & 63);
                }
            }
        }
        /* always[depth] over coordinates ord[depth..k-1] */
        for (int x = 0; x < W; x++) always[k][x] = all[x];
        for (int dd = k - 1; dd >= 0; dd--)
            for (int x = 0; x < W; x++) {
                uint64_t a = always[dd + 1][x];
                for (int j = 0; j < c; j++) a &= good[ord[dd]][j][x];
                always[dd][x] = a;
            }
        dfs(0, all);
    }
    fprintf(stderr, "reps %ld nodes %llu witness_free %llu gcd_proper %llu ng_settled %llu improper_out %llu\n",
            reps, nodes, nwf, ngcd, nng, nout);
    return 0;
}
