/* sample1.c -- exact uniform sampling of level-one improper multisets I(k,p,1).
 *
 * Fix k and a prime p > k+1, h = (p-1)/2.  Folded classes and folded times are
 * 1..h; class v covers time a iff (k+1)*d_p(a v) < p (as in covergen.c).  A
 * k-multiset of classes is improper at level one iff its SUPPORT covers every
 * time.  Write A_j for the number of j-subsets of {1..h} that cover.  A k-multiset
 * with support S of size j corresponds to a composition of k into j positive
 * parts, so
 *        #I(k,p,1) (as multisets) = sum_j C(k-1, j-1) A_j .
 *
 * Modes:
 *   sample1 k p count T SEED        for j = 1..k: draw T uniform j-subsets,
 *                                   print j, hits, A_j estimate, rel. std. error,
 *                                   and the weight C(k-1,j-1) A_j.  Env JMIN:
 *                                   skip j < JMIN (use JMIN = tau_k(p)).
 *   sample1 k p sample n SEED W_1 .. W_k
 *                                   draw n multisets: j with probability
 *                                   proportional to W_j (pass the weights from
 *                                   'count'), then a uniform covering j-set by
 *                                   rejection, then a uniform composition of k
 *                                   into j parts.  Output: k classes, sorted.
 *   sample1 k p check               read multisets on stdin, print 1/0 (covers).
 * Given exact weights W_j the output is exactly uniform on multisets; with
 * estimated weights the mixture over j inherits the estimates' error.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define MAXH 512
#define MAXK 24
#define WW 8
static int k, p, h, nw;
static uint64_t cov[MAXH + 1][WW], full[WW];
static uint64_t rs;
static inline uint64_t rnd(void) { /* splitmix64 */
    uint64_t z = (rs += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static inline int rndb(int n) { return (int)(((unsigned __int128)rnd() * (unsigned)n) >> 64); }
static int perm[MAXH];
/* uniform j-subset of 1..h into s[0..j-1] (partial Fisher-Yates on perm) */
static void subset(int j, int *s) {
    for (int i = 0; i < j; i++) { int r = i + rndb(h - i); int t = perm[i]; perm[i] = perm[r]; perm[r] = t; s[i] = perm[i]; }
}
static int covers(int j, const int *s) {
    uint64_t acc[WW] = {0};
    for (int i = 0; i < j; i++) for (int w = 0; w < nw; w++) acc[w] |= cov[s[i]][w];
    for (int w = 0; w < nw; w++) if (acc[w] != full[w]) return 0;
    return 1;
}
static double lchoose(int n, int r) { return lgamma(n + 1.0) - lgamma(r + 1.0) - lgamma(n - r + 1.0); }
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: sample1 k p count T SEED | sample1 k p sample n SEED W_1..W_k | sample1 k p check\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2; nw = (h + 63) / 64;
    if (h > MAXH || k > MAXK || nw > WW) { fprintf(stderr, "too large\n"); return 2; }
    for (int v = 1; v <= h; v++) {
        memset(cov[v], 0, sizeof cov[v]);
        for (int a = 1; a <= h; a++) { long r = (long)a * v % p; long d = r < p - r ? r : p - r; if ((k + 1) * d < p) cov[v][(a - 1) >> 6] |= 1ULL << ((a - 1) & 63); }
    }
    memset(full, 0, sizeof full);
    for (int a = 1; a <= h; a++) full[(a - 1) >> 6] |= 1ULL << ((a - 1) & 63);
    for (int i = 0; i < h; i++) perm[i] = i + 1;
    int s[MAXK];
    if (!strcmp(argv[3], "check")) {
        long x; int n = 0;
        while (scanf("%ld", &x) == 1) {
            long r = ((x % p) + p) % p; s[n++] = (int)(r <= h ? r : p - r);
            if (n == k) { printf("%d\n", s[0] > 0 && covers(k, s)); n = 0; }
        }
        return 0;
    }
    if (argc < 6) return 2;
    rs = strtoull(argv[5], 0, 10) * 0x2545F4914F6CDD1DULL + (uint64_t)p;
    if (!strcmp(argv[3], "count")) {
        long T = atol(argv[4]);
        double tot = 0, var = 0;
        printf("# k %d p %d h %d T %ld : j hits A_j_est rel_se weight=C(k-1,j-1)*A_j\n", k, p, h, T);
        int jmin = getenv("JMIN") ? atoi(getenv("JMIN")) : 1;
        for (int j = 1; j <= k && j <= h; j++) {
            long hits = 0;
            if (j < jmin) { printf("%d skipped\n", j); continue; }
            for (long t = 0; t < T; t++) { subset(j, s); hits += covers(j, s); }
            double f = (double)hits / T, A = exp(lchoose(h, j)) * f;
            double se = hits ? sqrt(f * (1 - f) / T) / f : 0;
            double wgt = exp(lchoose(k - 1, j - 1)) * A;
            tot += wgt; var += (se * wgt) * (se * wgt);
            printf("%d %ld %.6e %.4f %.6e\n", j, hits, A, se, wgt);
            fflush(stdout);
        }
        printf("# total_multisets %.6e rel_se %.4f orbits_approx(total/h) %.6e\n", tot, tot > 0 ? sqrt(var) / tot : 0, tot / h);
        return 0;
    }
    if (!strcmp(argv[3], "sample")) {
        long n = atol(argv[4]);
        if (argc < 6 + k) { fprintf(stderr, "need k weights\n"); return 2; }
        double Wt[MAXK + 1], tot = 0;
        for (int j = 1; j <= k; j++) { Wt[j] = atof(argv[5 + j]); tot += Wt[j]; }
        long tries = 0;
        for (long t = 0; t < n; t++) {
            double u = (double)(rnd() >> 11) / 9007199254740992.0 * tot; int j = 1;
            while (j < k && (u >= Wt[j] || Wt[j] == 0)) { u -= Wt[j]; j++; }
            do { subset(j, s); tries++; } while (!covers(j, s));
            /* uniform composition of k into j positive parts: (j-1)-subset of 1..k-1 */
            int cut[MAXK], pool[MAXK];
            for (int i = 0; i < k - 1; i++) pool[i] = i + 1;
            for (int i = 0; i < j - 1; i++) { int r = i + rndb(k - 1 - i); int x = pool[i]; pool[i] = pool[r]; pool[r] = x; cut[i] = pool[i]; }
            qsort(cut, j - 1, sizeof(int), cmpi);
            int out[MAXK], no = 0, prev = 0;
            for (int i = 0; i < j; i++) { int nxt = i < j - 1 ? cut[i] : k; for (int q = prev; q < nxt; q++) out[no++] = s[i]; prev = nxt; }
            qsort(out, k, sizeof(int), cmpi);
            for (int i = 0; i < k; i++) printf(i ? " %d" : "%d", out[i]);
            printf("\n");
        }
        fprintf(stderr, "samples %ld subset_draws %ld\n", n, tries);
        return 0;
    }
    return 2;
}
