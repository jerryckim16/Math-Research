/*
 * kiss_check.c -- exact pairwise check of a kissing configuration.
 *
 * Input: a raw file of n rows x d columns of signed int8 integers (row-major,
 * no header). Each row a is a nonzero integer direction in R^d.
 *
 * The rows form a kissing configuration (pairwise angles >= 60 degrees) iff
 * for every pair i < j, with p = a_i.a_j, A = |a_i|^2, B = |a_j|^2:
 *
 *        p <= 0   or   4 p^2 <= A B.
 *
 * Equivalently p <= T(A,B) where T(A,B) = isqrt(floor(A*B/4)) (p integer).
 * A repeated row (or a positive multiple) has 4p^2 = 4AB > AB, so the check
 * also certifies that the rows are pairwise distinct directions.
 *
 * Arithmetic: dot products are accumulated in int16. This is exact when
 * every squared norm is <= 32767: each partial sum satisfies
 * |sum_{k<=m} a_k b_k| <= sum_k |a_k||b_k| <= |a||b| <= max(A,B) (Cauchy-
 * Schwarz), so no partial sum overflows. The program checks this
 * precondition and aborts if it fails.
 *
 * Output: n, d, the norm classes, number of violating pairs, the maximum
 * of p - T over all pairs (<= 0 iff the check passes), the number of
 * contact pairs (4p^2 = AB exactly, i.e. angle exactly 60 degrees), and for
 * each class pair the maximum inner product p observed.
 *
 * Class mode (optional, used for points that are not small integer rows):
 *   kiss_check FILE.i8 d LABELS.u8 TABLE.txt
 * LABELS.u8 holds one class label per row, uint8 (file size n) or uint16
 * little-endian (file size 2n, for more than 256 classes); TABLE.txt holds
 * "k" (1 <= k <= MAXTAB; the class arrays are allocated for k, so 45D's
 * 2,203 classes fit) and
 * then k*k lines "a b T C". Pair (i, j) then passes iff a_i.a_j <= T[l_i][l_j],
 * and counts as a contact iff a_i.a_j == C[l_i][l_j]. The table is computed
 * exactly elsewhere (class_table.py) from an exact decomposition of the true
 * inner product as an increasing function of the row dot product; this
 * program only evaluates the row dot products (exactly, as above).
 *
 * Partner (Gram) mode (optional, for points given in a lattice basis):
 *   kiss_check FILE.i8 d --partner PARTNER.i8
 * PARTNER holds b_j = a_j G for a symmetric positive definite integer Gram
 * matrix G (written by the builder, which checks the symmetry). The inner
 * product of points i, j is then a_i . b_j = a_i G a_j^T, and the squared
 * norm of point i is a_i . b_i. Every partial sum is bounded by
 * |a_i| |b_j| (Euclidean norms of the stored rows), which the program checks
 * is <= 32767, so int16 accumulation stays exact.
 *
 * Class and partner modes combine: kiss_check FILE d LABELS TABLE --partner P
 * (used when class bodies are given in a lattice basis).
 *
 * Part mode (optional, to split long runs): --part K M checks only the
 * column blocks blk with blk % M == K. Block blk covers exactly the pairs
 * (i, j) with i < j and j in [blk*JB, (blk+1)*JB), so the M parts together
 * cover every pair exactly once; each part prints its own pair count.
 *
 * Output of the per class-pair maxima: one line per class pair observed when
 * there are at most MAXNORM classes (as before); with more classes (45D:
 * 2.4M class pairs) only the pairs whose maximum reaches or exceeds the
 * threshold are listed, with a count of the pairs omitted.
 *
 * Environment KISS_STOP_AT_FIRST=1 (for negative controls only): stop soon
 * after the first violation; the counts printed are then partial and the
 * result is FAIL with a genuine violating pair.
 *
 * Build: gcc -O3 -march=native -fopenmp kiss_check.c -o kiss_check
 * Usage: kiss_check FILE.i8 d [LABELS TABLE] [--partner PARTNER.i8] [--part K M]
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MAXNORM 1024  /* norm classes (norm mode); also the old class-mode limit */
#define MAXTAB 8192   /* class mode: table classes (memory ~ 7 * MAXTAB^2 * 2 bytes) */
#define JB 2048

static int64_t isqrt64(int64_t x) {
    if (x < 0) return -1;
    int64_t r = 0;
    while ((r + 1) * (r + 1) <= x) r++; /* values here are small */
    return r;
}

int main(int argc, char **argv) {
    const char *labfn = NULL, *tabfn = NULL, *partfn = NULL;
    int64_t partk = 0, partm = 1;
    int ai = 3;
    if (argc < 3) goto usage;
    if (ai + 1 < argc && strncmp(argv[ai], "--", 2) != 0) { labfn = argv[ai]; tabfn = argv[ai + 1]; ai += 2; }
    while (ai < argc) {
        if (strcmp(argv[ai], "--partner") == 0 && ai + 1 < argc) { partfn = argv[ai + 1]; ai += 2; }
        else if (strcmp(argv[ai], "--part") == 0 && ai + 2 < argc) { partk = atoll(argv[ai + 1]); partm = atoll(argv[ai + 2]); ai += 3; }
        else goto usage;
    }
    if (partm < 1 || partk < 0 || partk >= partm) goto usage;
    if (0) {
      usage:
        fprintf(stderr, "usage: %s FILE.i8 d [LABELS TABLE] [--partner PARTNER.i8] [--part K M]\n", argv[0]); return 2;
    }
    int partnermode = partfn != NULL;
    int classmode = labfn != NULL;  /* body rows may be zero there */
    /* class arrays: K x K, K = MAXNORM, or the table's k when larger */
    int K = MAXNORM, tabk = 0;
    if (classmode) {
        FILE *ft = fopen(tabfn, "r");
        if (!ft || fscanf(ft, "%d", &tabk) != 1 || tabk < 1 || tabk > MAXTAB) { fprintf(stderr, "bad table\n"); return 2; }
        fclose(ft);
        if (tabk > K) K = tabk;
    }
#define IX(a, b) ((size_t)(a) * K + (b))
    const char *fn = argv[1];
    int d = atoi(argv[2]);
    if (d <= 0 || d > 4096) { fprintf(stderr, "bad d\n"); return 2; }
    FILE *f = fopen(fn, "rb");
    if (!f) { perror(fn); return 2; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (sz % d) { fprintf(stderr, "file size %ld not a multiple of d=%d\n", sz, d); return 2; }
    int64_t n = sz / d;
    int8_t *raw = malloc(sz);
    if (fread(raw, 1, sz, f) != (size_t)sz) { fprintf(stderr, "read error\n"); return 2; }
    fclose(f);
    int8_t *praw = raw;
    if (partnermode) {
        FILE *fp = fopen(partfn, "rb");
        if (!fp) { perror(partfn); return 2; }
        praw = malloc(sz);
        if (fread(praw, 1, sz, fp) != (size_t)sz || fgetc(fp) != EOF) { fprintf(stderr, "partner file size differs\n"); return 2; }
        fclose(fp);
        int64_t ma = 0, mb = 0;
        for (int64_t i = 0; i < n; i++) {
            int64_t sa = 0, sb = 0;
            for (int k = 0; k < d; k++) { sa += (int64_t)raw[i * d + k] * raw[i * d + k]; sb += (int64_t)praw[i * d + k] * praw[i * d + k]; }
            if (sa > ma) ma = sa;
            if (sb > mb) mb = sb;
        }
        if (ma * mb > (int64_t)32767 * 32767) { fprintf(stderr, "partner mode: |a||b| may exceed 32767\n"); return 2; }
    }

    /* norms and classes */
    int32_t *nrm = malloc(n * sizeof(int32_t));
    int ncls = 0;
    int32_t *clsnorm = malloc(sizeof(int32_t) * K); int64_t *clscount = malloc(sizeof(int64_t) * K);
    uint16_t *cls = malloc(n * sizeof(uint16_t));
    int32_t maxnorm = 0;
    for (int64_t i = 0; i < n; i++) {
        int32_t s = 0;
        for (int k = 0; k < d; k++) s += (int32_t)raw[i * d + k] * praw[i * d + k];
        nrm[i] = s;
        if (s <= 0 && !(classmode && s == 0)) { fprintf(stderr, "row %lld has squared norm %d <= 0\n", (long long)i, s); return 1; }
        if (s > maxnorm) maxnorm = s;
        int c;
        for (c = 0; c < ncls; c++) if (clsnorm[c] == s) break;
        if (c == ncls) {
            if (ncls == MAXNORM) { fprintf(stderr, "too many norm classes\n"); return 2; }
            clsnorm[ncls] = s; clscount[ncls] = 0; ncls++;
        }
        cls[i] = (uint16_t)c; clscount[c]++;
    }
    if (!partnermode && maxnorm > 32767) { fprintf(stderr, "max squared norm %d > 32767: int16 path not exact\n", maxnorm); return 2; }

    /* thresholds T[c1][c2] and contact values */
    int16_t *T = calloc((size_t)K * K, sizeof(int16_t)), *C = calloc((size_t)K * K, sizeof(int16_t));
    if (!T || !C) { fprintf(stderr, "out of memory\n"); return 2; }
    for (int a = 0; a < ncls; a++) for (int b = 0; b < ncls; b++) {
        int64_t AB = (int64_t)clsnorm[a] * clsnorm[b];
        int64_t t = isqrt64(AB / 4);
        T[IX(a, b)] = (int16_t)t;
        C[IX(a, b)] = (4 * t * t == AB) ? (int16_t)t : (int16_t)32767; /* 32767 never reached */
    }
    if (classmode) {
        if (maxnorm >= 32767) { fprintf(stderr, "class mode needs max squared norm < 32767\n"); return 2; }
        FILE *fl = fopen(labfn, "rb");
        if (!fl) { fprintf(stderr, "bad labels file\n"); return 2; }
        fseek(fl, 0, SEEK_END); long lsz = ftell(fl); fseek(fl, 0, SEEK_SET);
        if (lsz == n) {
            uint8_t *l8 = malloc(n);
            if (fread(l8, 1, n, fl) != (size_t)n) { fprintf(stderr, "bad labels file\n"); return 2; }
            for (int64_t i = 0; i < n; i++) cls[i] = l8[i];
            free(l8);
        } else if (lsz == 2 * n) {
            uint8_t *l8 = malloc(2 * n);
            if (fread(l8, 1, 2 * n, fl) != (size_t)(2 * n)) { fprintf(stderr, "bad labels file\n"); return 2; }
            for (int64_t i = 0; i < n; i++) cls[i] = (uint16_t)(l8[2 * i] | (l8[2 * i + 1] << 8));
            free(l8);
        } else { fprintf(stderr, "labels file size is neither n nor 2n\n"); return 2; }
        fclose(fl);
        FILE *ft = fopen(tabfn, "r");
        if (!ft || fscanf(ft, "%d", &ncls) != 1 || ncls != tabk) { fprintf(stderr, "bad table\n"); return 2; }
        uint8_t *seen = calloc((size_t)K * K, 1);
        if (!seen) { fprintf(stderr, "out of memory\n"); return 2; }
        for (int64_t e = 0; e < (int64_t)ncls * ncls; e++) {
            int a, b; long tv, cv;
            if (fscanf(ft, "%d %d %ld %ld", &a, &b, &tv, &cv) != 4 || a < 0 || b < 0 || a >= ncls || b >= ncls || seen[IX(a, b)]
                || tv < -32768 || tv > 32767 || cv < -32768 || cv > 32767) { fprintf(stderr, "bad table entry\n"); return 2; }
            seen[IX(a, b)] = 1; T[IX(a, b)] = (int16_t)tv; C[IX(a, b)] = (int16_t)cv;
        }
        fclose(ft);
        free(seen);
        for (int c = 0; c < ncls; c++) { clsnorm[c] = c; clscount[c] = 0; }
        for (int64_t i = 0; i < n; i++) {
            if (cls[i] >= ncls) { fprintf(stderr, "label out of range\n"); return 2; }
            clscount[cls[i]]++;
        }
    }

    /* column-major int16 copy */
    int16_t *bt = aligned_alloc(64, ((size_t)d * n * 2 + 63) / 64 * 64);
    for (int64_t i = 0; i < n; i++) for (int k = 0; k < d; k++) bt[(size_t)k * n + i] = praw[i * d + k];
    /* per-class threshold rows are built per column block (below):
       TT[c][t] = T[c][cls[j0 + t]], CC[c][t] = C[c][cls[j0 + t]] */

    int64_t nblk = (n + JB - 1) / JB;
    int64_t viol = 0, contacts = 0;
    int32_t maxexcess = -32768;
    int16_t *maxp = malloc(sizeof(int16_t) * (size_t)K * K);
    if (!maxp) { fprintf(stderr, "out of memory\n"); return 2; }
    for (size_t e = 0; e < (size_t)K * K; e++) maxp[e] = -32768;
    int64_t partpairs = 0;
    for (int64_t blk = partk; blk < nblk; blk += partm) {
        int64_t j0 = blk * JB, j1 = j0 + JB; if (j1 > n) j1 = n;
        partpairs += (j0 + j1 - 1) * (j1 - j0) / 2;  /* sum of j over the block */
    }
    int64_t first_i = -1, first_j = -1;
    const char *sf = getenv("KISS_STOP_AT_FIRST");
    int stopfirst = sf && strcmp(sf, "1") == 0;
    volatile int found = 0;

    #pragma omp parallel
    {
        int16_t acc[JB] __attribute__((aligned(64)));
        int64_t lviol = 0, lcont = 0; int32_t lmax = -32768;
        int16_t *lmaxp = malloc(sizeof(int16_t) * (size_t)K * K);
        int16_t *TT = malloc(sizeof(int16_t) * (size_t)ncls * JB), *CC = malloc(sizeof(int16_t) * (size_t)ncls * JB);
        if (!lmaxp || !TT || !CC) { fprintf(stderr, "out of memory\n"); exit(2); }
        for (size_t e = 0; e < (size_t)K * K; e++) lmaxp[e] = -32768;
        int64_t lfi = -1, lfj = -1;
        #pragma omp for schedule(dynamic, 1)
        for (int64_t blk = nblk - 1; blk >= 0; blk--) {
            if (stopfirst && found) continue;
            if (blk % partm != partk) continue;
            int64_t j0 = blk * JB, j1 = j0 + JB; if (j1 > n) j1 = n;
            for (int c = 0; c < ncls; c++) for (int64_t j = j0; j < j1; j++) {
                TT[(size_t)c * JB + (j - j0)] = T[IX(c, cls[j])];
                CC[(size_t)c * JB + (j - j0)] = C[IX(c, cls[j])];
            }
            for (int64_t i = 0; i < j1 - 1; i++) {
                int64_t js = (i + 1 > j0) ? i + 1 : j0;
                int len = (int)(j1 - js);
                if (len <= 0) continue;
                memset(acc, 0, sizeof(int16_t) * len);
                const int8_t *ai = raw + i * d;
                for (int k = 0; k < d; k++) {
                    int16_t x = ai[k];
                    if (!x) continue;
                    const int16_t *b = bt + (size_t)k * n + js;
                    for (int t = 0; t < len; t++) acc[t] += x * b[t];
                }
                int ci = cls[i];
                const int16_t *tt = TT + (size_t)ci * JB + (js - j0), *cc = CC + (size_t)ci * JB + (js - j0);
                int32_t bmax = -32768; int64_t bv = 0, bc = 0;
                for (int t = 0; t < len; t++) {
                    int32_t e = (int32_t)acc[t] - tt[t];
                    bmax = e > bmax ? e : bmax;
                    bv += (e > 0);
                    bc += (acc[t] == cc[t]);
                }
                if (bmax > lmax) lmax = bmax;
                lviol += bv; lcont += bc;
                if (bv && stopfirst) found = 1;
                if (bv && lfi < 0) {
                    for (int t = 0; t < len; t++) if ((int32_t)acc[t] - tt[t] > 0) { lfi = i; lfj = js + t; break; }
                }
                /* per class-pair maxima (scalar, cheap relative to the dot products) */
                for (int t = 0; t < len; t++) {
                    int cj = cls[js + t];
                    if (acc[t] > lmaxp[IX(ci, cj)]) lmaxp[IX(ci, cj)] = acc[t];
                }
            }
        }
        #pragma omp critical
        {
            viol += lviol; contacts += lcont;
            if (lmax > maxexcess) maxexcess = lmax;
            for (int a = 0; a < ncls; a++) for (int b = 0; b < ncls; b++) if (lmaxp[IX(a, b)] > maxp[IX(a, b)]) maxp[IX(a, b)] = lmaxp[IX(a, b)];
            if (lfi >= 0 && (first_i < 0 || lfi < first_i)) { first_i = lfi; first_j = lfj; }
        }
        free(lmaxp); free(TT); free(CC);
    }

    printf("file %s\nrows %lld\ncolumns %d\n%s %d\n", fn, (long long)n, d, classmode ? "label_classes" : "norm_classes", ncls);
    for (int c = 0; c < ncls; c++) printf("  %s %d count %lld\n", classmode ? "label" : "squared_norm", clsnorm[c], (long long)clscount[c]);
    printf("pairs %lld\n", (long long)(n * (n - 1) / 2));
    if (partm > 1) printf("part %lld of %lld: pairs_in_part %lld\n", (long long)partk, (long long)partm, (long long)partpairs);
    int64_t omitted = 0;
    for (int a = 0; a < ncls; a++) for (int b = a; b < ncls; b++) {
        int16_t m = maxp[IX(a, b)] > maxp[IX(b, a)] ? maxp[IX(a, b)] : maxp[IX(b, a)];
        if (m == -32768) continue;
        if (ncls > MAXNORM && m < T[IX(a, b)]) { omitted++; continue; }
        printf("  class_pair %d,%d max_inner_product %d threshold %d\n", clsnorm[a], clsnorm[b], m, T[IX(a, b)]);
    }
    if (ncls > MAXNORM) printf("class_pairs_below_threshold_omitted %lld\n", (long long)omitted);
    printf("contacts_60deg %lld\n", (long long)contacts);
    printf("max_excess %d\nviolations %lld\n", maxexcess, (long long)viol);
    if (viol) printf("first_violation %lld %lld\n", (long long)first_i, (long long)first_j);
    if (stopfirst) printf("stopped_at_first_violation %s (counts partial)\n", found ? "yes" : "no");
    printf("RESULT %s\n", viol == 0 ? "PASS" : "FAIL");
    return viol == 0 ? 0 : 1;
}
