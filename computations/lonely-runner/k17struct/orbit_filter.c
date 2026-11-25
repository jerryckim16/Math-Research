/* orbit_filter.c -- gcd clause + unit-orbit canonical form for tuples mod N = l*p.
 *
 * Usage: orbit_filter k p l [idx] [ng]  < tuples   (k residues mod N per line;
 *        'idx': input lines are liftfree.c's "idx w_1..w_k" format;
 *        'ng': also drop tuples settled by the weighted-shift lemma NG for some
 *        divisor d >= 2 of l: E = {i : d does not divide w_i}, g_i = gcd(w_i, d),
 *        drop if 1 <= |E| < k and sum_{i in E} g_i*ceil(2d/((k+1) g_i)) < d.
 *        (notes/lonely-runner/structure.md, Lemma NG = Allikvere's weighted shift;
 *        valid through the gate criterion (ii), given LRC(m), m < k.)
 * Drops tuples proper by the gcd clause at level l (gcd(l, w_j : j != i) > 1 for
 * some i) and prints the canonical form of the rest: the lexicographic minimum
 * over units u of Z_N of the sorted tuple min(u w_i mod N, N - u w_i mod N).
 * Same definitions as cascade_verify.c and small_gates.py.  Pipe into sort -u.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXK 24
static int k, p, l, N, nu, units[40000];
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int cmpi(const void *x, const void *y) { return *(const int *)x - *(const int *)y; }
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: orbit_filter k p l [idx]\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); l = atoi(argv[3]); N = l * p;
    int idx = 0, ng = 0;
    for (int a = 4; a < argc; a++) { if (!strcmp(argv[a], "idx")) idx = 1; if (!strcmp(argv[a], "ng")) ng = 1; }
    int divs[64], nd = 0; for (int d = 2; d <= l; d++) if (l % d == 0) divs[nd++] = d;
    long nng = 0;
    for (int u = 1; u < N; u++) if (gcd(u, N) == 1) units[nu++] = u;
    long nin = 0, ngcd = 0, nout = 0; int w[MAXK], t[MAXK], best[MAXK];
    for (;;) {
        long x;
        if (idx && scanf("%ld", &x) != 1) break;
        int ok = 1;
        for (int i = 0; i < k; i++) { if (scanf("%ld", &x) != 1) { ok = 0; break; } w[i] = (int)(((x % N) + N) % N); }
        if (!ok) break;
        nin++;
        int g1 = 0;
        for (int i = 0; i < k && !g1; i++) { int g = l; for (int j = 0; j < k && g > 1; j++) if (j != i) g = gcd(g, w[j]); if (g > 1) g1 = 1; }
        if (g1) { ngcd++; continue; }
        if (ng) {
            int hit = 0;
            for (int a = 0; a < nd && !hit; a++) {
                int d = divs[a], e = 0; long cost = 0;
                for (int i = 0; i < k; i++) if (w[i] % d) { int g = gcd(w[i], d); e++; cost += (long)g * ((2L * d + (long)(k + 1) * g - 1) / ((long)(k + 1) * g)); }
                if (e >= 1 && e < k && cost < d) hit = 1;
            }
            if (hit) { nng++; continue; }
        }
        int have = 0;
        for (int a = 0; a < nu; a++) {
            long u = units[a];
            for (int i = 0; i < k; i++) { int r = (int)((u * w[i]) % N); t[i] = r < N - r ? r : N - r; }
            qsort(t, k, sizeof(int), cmpi);
            int lt = !have;
            for (int i = 0; have && i < k; i++) if (t[i] != best[i]) { lt = t[i] < best[i]; break; }
            if (lt) { memcpy(best, t, sizeof(int) * k); have = 1; }
        }
        for (int i = 0; i < k; i++) printf(i ? " %d" : "%d", best[i]);
        putchar('\n'); nout++;
    }
    fprintf(stderr, "in %ld gcd_proper %ld ng_settled %ld out %ld\n", nin, ngcd, nng, nout);
    return 0;
}
