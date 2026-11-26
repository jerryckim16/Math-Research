/* cover_canon.c -- unit-orbit canonical form of each minimal cover (any length).
 *
 * Canonical form of a set S of folded classes: the lexicographically least
 * sorted tuple (fold(a s))_{s in S} over units a in 1..(p-1)/2, where
 * fold(x) = min(x mod p, p - x mod p); shorter tuples are padded by length
 * first (the length is an orbit invariant).  Same definition as
 * gate251/orbit_check.py (Python); used for the orderly-rule check at the
 * larger small primes, where the Python version is too slow.
 *
 * Usage: cover_canon p < covers > canonical_forms   (one per input line, in order)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc != 2) { fprintf(stderr, "usage: cover_canon p < covers\n"); return 2; }
    int p = atoi(argv[1]), h = (p - 1) / 2;
    char line[8192];
    int S[64], T[64], best[64];
    unsigned long long n = 0;
    while (fgets(line, sizeof line, stdin)) {
        size_t L = strlen(line);
        if (!L || line[L - 1] != '\n') { fprintf(stderr, "truncated line\n"); return 1; }
        int m = 0; char *s = line, *e;
        for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (m < 64) S[m++] = (int)x; s = e; }
        if (!m) continue;
        int have = 0;
        for (int a = 1; a <= h; a++) {
            for (int i = 0; i < m; i++) { long r = (long)a * S[i] % p; T[i] = (int)(r < p - r ? r : p - r); }
            qsort(T, m, sizeof(int), cmpi);
            if (!have || memcmp(T, best, m * sizeof(int)) < 0) {
                int lt = !have;
                if (!lt) for (int i = 0; i < m; i++) { if (T[i] != best[i]) { lt = T[i] < best[i]; break; } }
                if (lt) { memcpy(best, T, m * sizeof(int)); have = 1; }
            }
        }
        for (int i = 0; i < m; i++) printf(i ? " %d" : "%d", best[i]);
        putchar('\n');
        n++;
    }
    fprintf(stderr, "cover_canon: %llu covers\n", n);
    return 0;
}
