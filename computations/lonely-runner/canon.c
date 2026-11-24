/* canon.c -- unit-orbit canonical forms of level-one k-multisets, deduplicated.
 *
 * Canonical form of v in (Z_p \ 0)^k: the lexicographically least sorted
 * tuple (min(a v_i mod p, p - a v_i mod p))_i over units a in 1..p-1
 * (a and -a give the same folded tuple, so a in 1..(p-1)/2 suffices).
 * This is the same as sieve.Level(k,p,1).canon.
 *
 * Usage: canon k p rows     stdin: k residues per line
 *        canon k p each     same input; prints the canonical form of every
 *                           input line, in order (no deduplication)
 *        canon k p expand   stdin: one cover per line (1..k classes); every
 *                           k-multiset C + (k-|C|) classes from 1..(p-1)/2
 *                           is formed (as in sieve.level1_improper_covers)
 * Output: the distinct canonical tuples (unsorted); counts on stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 24
static int k, p, h;
static uint64_t ninput = 0, nrows = 0;
/* open-addressing hash set of canonical tuples (bytes, k <= 24, classes < 256*256) */
static uint16_t *tab; static uint8_t *used; static size_t cap = 1 << 22, cnt = 0;

static uint64_t hsh(const uint16_t *t) { uint64_t x = 1469598103934665603ULL; for (int i = 0; i < k; i++) { x ^= t[i]; x *= 1099511628211ULL; } return x; }
static void grow(void);
static void insert(const uint16_t *t) {
    if (2 * (cnt + 1) > cap) grow();
    size_t i = hsh(t) & (cap - 1);
    while (used[i]) { if (!memcmp(tab + i * k, t, k * sizeof(uint16_t))) return; i = (i + 1) & (cap - 1); }
    used[i] = 1; memcpy(tab + i * k, t, k * sizeof(uint16_t)); cnt++;
}
static void grow(void) {
    size_t oc = cap; uint16_t *ot = tab; uint8_t *ou = used;
    cap *= 2; tab = calloc(cap * k, sizeof(uint16_t)); used = calloc(cap, 1); cnt = 0;
    for (size_t i = 0; i < oc; i++) if (ou[i]) insert(ot + i * k);
    free(ot); free(ou);
}
static int cmpu16(const void *a, const void *b) { return (int)*(const uint16_t *)a - (int)*(const uint16_t *)b; }
static int mode_each = 0;
static void canon_insert(const int *v) {
    uint16_t best[MAXK], cur[MAXK]; int have = 0;
    for (int a = 1; a <= h; a++) {
        for (int i = 0; i < k; i++) { long r = ((long)a * v[i]) % p; cur[i] = (uint16_t)(r < p - r ? r : p - r); }
        qsort(cur, k, sizeof(uint16_t), cmpu16);
        if (!have || memcmp(cur, best, k * sizeof(uint16_t)) < 0) {
            /* lexicographic on values: compare elementwise */
            int less = !have;
            if (have) for (int i = 0; i < k; i++) { if (cur[i] != best[i]) { less = cur[i] < best[i]; break; } }
            if (less) { memcpy(best, cur, sizeof cur); have = 1; }
        }
    }
    nrows++;
    if (mode_each) { for (int j = 0; j < k; j++) printf(j ? " %d" : "%d", best[j]); putchar('\n'); return; }
    insert(best);
}
static int ext[MAXK], C[MAXK], nC;
static void expand(int pos, int start, int need) {
    if (need == 0) { int v[MAXK]; for (int i = 0; i < nC; i++) v[i] = C[i]; for (int i = 0; i < pos; i++) v[nC + i] = ext[i]; canon_insert(v); return; }
    for (int a = start; a <= h; a++) { ext[pos] = a; expand(pos + 1, a, need - 1); }
}
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: canon k p rows|expand\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2;
    int mode_expand = !strcmp(argv[3], "expand");
    mode_each = !strcmp(argv[3], "each");
    tab = calloc(cap * k, sizeof(uint16_t)); used = calloc(cap, 1);
    char line[4096];
    while (fgets(line, sizeof line, stdin)) {
        int v[MAXK], n = 0; char *s = line, *e;
        for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (n < MAXK) v[n++] = (int)(((x % p) + p) % p); s = e; }
        if (n == 0) continue;
        ninput++;
        if (mode_expand) { if (n > k) { fprintf(stderr, "cover too long\n"); return 1; } nC = n; memcpy(C, v, n * sizeof(int)); expand(0, 1, k - n); }
        else { if (n != k) { fprintf(stderr, "row length %d != k\n", n); return 1; } canon_insert(v); }
    }
    if (!mode_each) for (size_t i = 0; i < cap; i++) if (used[i]) { for (int j = 0; j < k; j++) printf(j ? " %d" : "%d", tab[i * k + j]); putchar('\n'); }
    fprintf(stderr, "inputs %llu rows %llu distinct_orbits %zu\n", (unsigned long long)ninput, (unsigned long long)nrows, cnt);
    return 0;
}
