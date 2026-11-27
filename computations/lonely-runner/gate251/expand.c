/* expand.c -- stream every level-one base containing a minimal cover.
 *
 * Input (stdin): one minimal cover per line (c <= k distinct folded classes,
 * as printed by covergen.c).  Output (stdout): every k-multiset b with
 * supp(b) containing the cover, i.e. the cover plus a multiset of k - c extra
 * classes from 1..(p-1)/2, sorted, one per line.  Each such b covers every
 * time, so b is a level-one base; and every base contains a minimal cover,
 * so expanding one cover per unit orbit (covergen with LRC_ORDERLY=1)
 * reaches every base orbit at least once (a unit u maps C + extras to
 * uC + u extras).  No deduplication: a base containing several minimal-cover
 * orbits is produced several times, which costs time but not soundness.
 * Within one cover the extensions are distinct multisets.
 *
 * Usage: expand k p < covers > bases
 * Env:   EX_SAMPLE=path, EX_EVERY=n (default 100): also write every n-th base
 *        (bases n, 2n, ...) to path, for the independent re-check.
 * stderr: "EXPAND covers N bases M sampled S bad 0" (bad = malformed, too-long
 *        or truncated lines; any bad line makes the exit status 1), then
 *        "COVERSIZES c:n ..." (covers by number of classes).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXK 32
static int k, p, h, C[MAXK], nC, ext[MAXK];
static unsigned long long nbase = 0, nsamp = 0, every = 100, bysize[MAXK + 1];
static FILE *samp = NULL;

static void emit(void) {
    int v[MAXK], i = 0, j = 0, n = 0;
    int ne = k - nC;
    while (i < nC || j < ne) {                 /* merge two sorted lists */
        if (j >= ne || (i < nC && C[i] <= ext[j])) v[n++] = C[i++];
        else v[n++] = ext[j++];
    }
    for (int t = 0; t < k; t++) printf(t ? " %d" : "%d", v[t]);
    putchar('\n');
    nbase++;
    if (samp && nbase % every == 0) { for (int t = 0; t < k; t++) fprintf(samp, t ? " %d" : "%d", v[t]); fputc('\n', samp); nsamp++; }
}

static void rec(int pos, int start) {
    if (pos == k - nC) { emit(); return; }
    for (int a = start; a <= h; a++) { ext[pos] = a; rec(pos + 1, a); }
}

static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: expand k p < covers\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2;
    if (getenv("EX_EVERY")) every = strtoull(getenv("EX_EVERY"), 0, 10);
    if (getenv("EX_SAMPLE")) { samp = fopen(getenv("EX_SAMPLE"), "w"); if (!samp) { fprintf(stderr, "cannot open EX_SAMPLE\n"); return 2; } }
    char line[8192];
    unsigned long long ncov = 0, bad = 0;
    while (fgets(line, sizeof line, stdin)) {
        size_t L = strlen(line);
        if (L == 0 || line[L - 1] != '\n') { bad++; continue; }   /* truncated last line */
        nC = 0; char *s = line, *e;
        for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (nC < MAXK) C[nC] = (int)x; nC++; s = e; }
        if (nC == 0) continue;
        if (nC > k) { bad++; continue; }
        int okr = 1;
        for (int i = 0; i < nC; i++) if (C[i] < 1 || C[i] > h) okr = 0;
        if (!okr) { bad++; continue; }
        qsort(C, nC, sizeof(int), cmpi);
        ncov++; bysize[nC]++;
        rec(0, 1);
    }
    if (samp) fclose(samp);
    fprintf(stderr, "EXPAND covers %llu bases %llu sampled %llu bad %llu\n", ncov, nbase, nsamp, bad);
    fprintf(stderr, "COVERSIZES");
    for (int c = 1; c <= k; c++) if (bysize[c]) fprintf(stderr, " %d:%llu", c, bysize[c]);
    fprintf(stderr, "\n");
    return bad ? 1 : 0;
}
