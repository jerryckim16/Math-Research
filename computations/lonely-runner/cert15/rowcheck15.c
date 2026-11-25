/* rowcheck15.c -- level-one checks of stored certificate rows for LRC(k)
 * gate certificates (written for Allikvere's LRC(15) archives, Zenodo
 * 10.5281/zenodo.23304361), from the covering formulation of Def. 2.1 at
 * level l = 1 (arXiv:2604.23906; restated as eq. (cover) of the LRC(15)
 * manuscript):
 *
 *   folded time classes a = 1..h, h = (p-1)/2; a folded speed class v covers
 *   time a iff (k+1) d_p(a v) < p, d_p(x) = distance of x mod p to 0.
 *   A multiset of classes is witness-free at level 1 (lies in I(k,p,1))
 *   iff it covers every folded time (t = 0 is never a witness; t = a/p and
 *   t = (p-a)/p give the same distances).
 *
 * Usage: rowcheck15 k p n      stdin: hex rows, n classes per line, 2 or 4
 *                              hex digits per class (as in the archives)
 * Per row: value range 1..h; classes distinct; class 1 present; COVER
 * (witness-free at level 1, threshold k+1 even when n < k); IRREDUNDANT
 * (every class covers some time no other class of the row covers).
 * Prints one summary line
 *   rows R bad_format F out_of_range O not_distinct D no_class1 C
 *   not_cover X redundant Y
 * and the first 20 offending rows ("BAD <what> v_1 .. v_n").
 * This is a second, independent implementation of the level-one test of
 * gatecheck.c hexrows (which tests every t = m/p directly).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: rowcheck15 k p n\n"); return 2; }
    int k = atoi(argv[1]), p = atoi(argv[2]), n = atoi(argv[3]);
    int h = (p - 1) / 2;
    if (n < 1 || n > 64 || h < 1 || h > 4096) return 2;
    /* cov[v][a] = 1 iff class v covers time a */
    unsigned char *cov = calloc((size_t)(h + 1) * (h + 1), 1);
    for (int v = 1; v <= h; v++)
        for (int a = 1; a <= h; a++) {
            long r = ((long)a * v) % p, d = r < p - r ? r : p - r;
            cov[(size_t)v * (h + 1) + a] = (long)(k + 1) * d < p;
        }
    int *cnt = malloc(sizeof(int) * (h + 1));
    char line[4096];
    unsigned long long rows = 0, fmt = 0, oor = 0, nd = 0, nc1 = 0, ncov = 0, red = 0, shown = 0;
    while (fgets(line, sizeof line, stdin)) {
        int len = (int)strcspn(line, "\r\n");
        if (len == 0) continue;
        rows++;
        int w = len / n, v[64], ok = 1;
        if (w * n != len || (w != 2 && w != 4)) { fmt++; continue; }
        for (int i = 0; i < n; i++) {
            char b[5]; memcpy(b, line + i * w, w); b[w] = 0;
            char *e; v[i] = (int)strtol(b, &e, 16);
            if (*e) { fmt++; ok = 0; break; }
        }
        if (!ok) continue;
        const char *what = 0;
        int range_ok = 1;
        for (int i = 0; i < n; i++) if (v[i] < 1 || v[i] > h) range_ok = 0;
        if (!range_ok) { oor++; what = "out_of_range"; }
        else {
            int dist = 1, has1 = 0;
            for (int i = 0; i < n; i++) { if (v[i] == 1) has1 = 1; for (int j = 0; j < i; j++) if (v[i] == v[j]) dist = 0; }
            if (!dist) { nd++; what = "not_distinct"; }
            if (!has1) { nc1++; if (!what) what = "no_class1"; }
            memset(cnt, 0, sizeof(int) * (h + 1));
            for (int i = 0; i < n; i++) for (int a = 1; a <= h; a++) cnt[a] += cov[(size_t)v[i] * (h + 1) + a];
            int cover = 1;
            for (int a = 1; a <= h; a++) if (!cnt[a]) { cover = 0; break; }
            if (!cover) { ncov++; if (!what) what = "not_cover"; }
            int irr = 1;
            for (int i = 0; i < n && irr; i++) {
                int priv = 0;
                for (int a = 1; a <= h && !priv; a++) if (cov[(size_t)v[i] * (h + 1) + a] && cnt[a] == 1) priv = 1;
                if (!priv) irr = 0;
            }
            if (!irr) { red++; if (!what) what = "redundant"; }
        }
        if (what && shown < 20) { shown++; printf("BAD %s", what); for (int i = 0; i < n; i++) printf(" %d", v[i]); printf("\n"); }
    }
    printf("rows %llu bad_format %llu out_of_range %llu not_distinct %llu no_class1 %llu not_cover %llu redundant %llu\n",
           rows, fmt, oor, nd, nc1, ncov, red);
    return 0;
}
