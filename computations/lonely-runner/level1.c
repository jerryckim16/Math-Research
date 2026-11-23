/* level1.c -- enumerate orbit representatives (1, a_2 <= ... <= a_k),
 * 1 <= a_i <= (p-1)/2, of Z_{p,1}^k and print those with NO witness time
 * t = m/p (0 <= m < p) satisfying ||a_i m / p|| >= 1/(k+1) for all i.
 * Exact integer arithmetic; bitsets over m.  Output: one tuple per line.
 * The caller (sieve.py, level1_improper_c) canonicalises and de-duplicates.
 * Usage: level1 k p            Build: cc -O2 -o level1 level1.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXW 64   /* p < 4096 */
#define MAXK 32

static int k, p, h, W;
static uint64_t *mask;            /* (h+1) * W */
static uint64_t acc[MAXK + 1][MAXW];
static int tup[MAXK + 1];
static unsigned long long leaves = 0, improper = 0;

static void dfs(int depth, int start) {
    /* tup[0..depth-1] fixed; acc[depth] = AND of their masks */
    if (depth == k) {
        leaves++;
        uint64_t any = 0;
        for (int w = 0; w < W; w++) any |= acc[depth][w];
        if (!any) {
            improper++;
            for (int i = 0; i < k; i++) printf(i ? " %d" : "%d", tup[i]);
            putchar('\n');
        }
        return;
    }
    for (int a = start; a <= h; a++) {
        uint64_t *m = mask + (size_t)a * W;
        for (int w = 0; w < W; w++) acc[depth + 1][w] = acc[depth][w] & m[w];
        tup[depth] = a;
        dfs(depth + 1, a);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: level1 k p\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]);
    if (k < 2 || k > MAXK || p < 3 || p >= 64 * MAXW) { fprintf(stderr, "bad args\n"); return 2; }
    h = (p - 1) / 2; W = (p + 63) / 64;
    mask = calloc((size_t)(h + 1) * W, sizeof(uint64_t));
    for (int a = 1; a <= h; a++)
        for (int m = 0; m < p; m++) {
            long r = ((long)a * m) % p;
            long d = r < p - r ? r : p - r;
            if ((long)(k + 1) * d >= p) mask[(size_t)a * W + m / 64] |= 1ULL << (m % 64);
        }
    tup[0] = 1;
    memcpy(acc[1], mask + W, W * sizeof(uint64_t));
    dfs(1, 1);
    fprintf(stderr, "leaves %llu improper %llu\n", leaves, improper);
    return 0;
}
