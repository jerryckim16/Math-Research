/* mcmc1.c -- uniform sampling and counting of level-one improper multisets
 * I(k,p,1) by Metropolis chains and a ladder of nested constraints.
 *
 * Fix k and a prime p > k+1, h = (p-1)/2; class v covers time a iff
 * (k+1) d_p(a v) < p.  A k-multiset is improper at level one iff its support
 * covers all h folded times.
 *
 * Chain.  State: an ordered k-tuple x.  Proposal: choose one position (prob
 * 1/2) or two distinct positions (prob 1/2) uniformly, and replace each by a
 * uniform class in 1..h.  The proposal is symmetric on ordered tuples.  The
 * target on ordered tuples is pi(x) proportional to prod_c n_c(x)! (n_c =
 * multiplicity of class c) restricted to the constraint set, i.e. the uniform
 * distribution on MULTISETS (each multiset has k!/prod n_c! orderings).
 * Metropolis acceptance: min(1, pi(y)/pi(x)) if y satisfies the constraint.
 *
 * Ladder.  Times are added in a fixed random order, STEP at a time, giving
 * constraint sets E_0 (no constraint) > E_1 > ... > E_S = I(k,p,1), where E_s
 * requires the support to cover the first s*STEP times.  #E_0 = C(h+k-1, k).
 * At stage s the chain samples E_s and estimates r_s = #E_{s+1}/#E_s as the
 * fraction of samples in E_{s+1}; #I = #E_0 prod r_s.  The last stage's samples
 * are (approximately) uniform on I(k,p,1).
 *
 * Usage: mcmc1 k p SEED NSAMP THIN [FINAL_N FINAL_THIN]
 *   NSAMP samples per stage, THIN chain steps between samples (burn-in = 20 THIN).
 *   If FINAL_N > 0, after the ladder print FINAL_N samples of I(k,p,1) (sorted
 *   multisets, one per line, prefixed by "M"), FINAL_THIN steps apart.
 * Stderr / stdout '#' lines: per-stage ratios, the estimate of #I (multisets) and
 * the delta-method relative error from the binomial errors of the r_s (chain
 * autocorrelation is not included; compare independent seeds).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#define MAXH 512
#define MAXK 24
#define MAXM 64
static int k, p, h;
static int ncov[MAXH + 1], covl[MAXH + 1][MAXM];   /* times covered by class v */
static int inT[MAXH + 1];                           /* 1 if time a is constrained */
static int cnt[MAXH + 1];                           /* # positions covering time a */
static int x[MAXK], mult[MAXH + 1];
static uint64_t rs;
static inline uint64_t rnd(void) {
    uint64_t z = (rs += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static inline int rndb(int n) { return (int)(((unsigned __int128)rnd() * (unsigned)n) >> 64); }
static inline double rndu(void) { return (double)(rnd() >> 11) / 9007199254740992.0; }
static double lchoose(int n, int r) { return lgamma(n + 1.0) - lgamma(r + 1.0) - lgamma(n - r + 1.0); }

static void addc(int v, int s) { for (int q = 0; q < ncov[v]; q++) cnt[covl[v][q]] += s; }
static int ok_removed(int v) { for (int q = 0; q < ncov[v]; q++) { int a = covl[v][q]; if (inT[a] && cnt[a] == 0) return 0; } return 1; }
static long acc = 0, tried = 0;
static void step(void) {
    tried++;
    int two = rnd() & 1;
    int i = rndb(k), j = i, b = 1 + rndb(h), b2 = 0;
    if (two) { j = rndb(k - 1); if (j >= i) j++; b2 = 1 + rndb(h); }
    int a = x[i], a2 = two ? x[j] : 0;
    /* Metropolis ratio prod n! (y) / prod n! (x) */
    double r;
    if (!two) {
        if (b == a) return;
        r = (double)(mult[b] + 1) / mult[a];
    } else {
        /* apply to multiplicities temporarily */
        double lr = 0;
        lr -= log((double)mult[a]); mult[a]--;
        lr -= log((double)mult[a2]); mult[a2]--;
        lr += log((double)(mult[b] + 1)); mult[b]++;
        lr += log((double)(mult[b2] + 1)); mult[b2]++;
        mult[b2]--; mult[b]--; mult[a2]++; mult[a]++;
        r = exp(lr);
    }
    if (r < 1 && rndu() >= r) return;
    /* constraint check */
    addc(a, -1); if (two) addc(a2, -1);
    addc(b, +1); if (two) addc(b2, +1);
    int ok = ok_removed(a) && (!two || ok_removed(a2));
    if (!ok) { addc(b, -1); if (two) addc(b2, -1); addc(a, +1); if (two) addc(a2, +1); return; }
    x[i] = b; mult[a]--; mult[b]++;
    if (two) { x[j] = b2; mult[a2]--; mult[b2]++; }
    acc++;
}
static int cmpi(const void *u, const void *v) { return *(const int *)u - *(const int *)v; }

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: mcmc1 k p SEED NSAMP THIN [FINAL_N FINAL_THIN]\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2;
    rs = strtoull(argv[3], 0, 10) * 0x2545F4914F6CDD1DULL + (uint64_t)p * 104729;
    long NS = atol(argv[4]), THIN = atol(argv[5]);
    long FN = argc > 6 ? atol(argv[6]) : 0, FT = argc > 7 ? atol(argv[7]) : THIN;
    int STEP = getenv("STEP") ? atoi(getenv("STEP")) : 3;
    for (int v = 1; v <= h; v++) {
        ncov[v] = 0;
        for (int a = 1; a <= h; a++) { long r = (long)a * v % p; long d = r < p - r ? r : p - r; if ((k + 1) * d < p) covl[v][ncov[v]++] = a; }
    }
    int order[MAXH]; for (int a = 0; a < h; a++) order[a] = a + 1;
    for (int a = h - 1; a > 0; a--) { int r = rndb(a + 1); int t = order[a]; order[a] = order[r]; order[r] = t; }
    memset(inT, 0, sizeof inT); memset(cnt, 0, sizeof cnt); memset(mult, 0, sizeof mult);
    for (int i = 0; i < k; i++) { x[i] = 1 + rndb(h); mult[x[i]]++; addc(x[i], +1); }
    double logcount = lchoose(h + k - 1, k), relvar = 0;
    printf("# k %d p %d h %d seed %s NSAMP %ld THIN %ld STEP %d\n", k, p, h, argv[3], NS, THIN, STEP);
    int ntimes = 0;
    while (ntimes < h) {
        int next = ntimes + STEP < h ? ntimes + STEP : h;
        for (long t = 0; t < 20 * THIN; t++) step();
        long hit = 0; int saved[MAXK]; int have = 0;
        for (long s = 0; s < NS; s++) {
            for (long t = 0; t < THIN; t++) step();
            int all = 1;
            for (int q = ntimes; q < next && all; q++) if (cnt[order[q]] == 0) all = 0;
            if (all) { hit++; if (!have || rndb(4) == 0) { memcpy(saved, x, sizeof(int) * k); have = 1; } }
        }
        if (hit == 0) { printf("# stage %d: no hits, abort\n", ntimes); return 1; }
        double r = (double)hit / NS;
        logcount += log(r); relvar += (1 - r) / (r * NS);
        printf("# times %d->%d ratio %.5f acc %.4f\n", ntimes, next, r, (double)acc / tried);
        /* move to a state in E_{s+1} and tighten the constraint */
        memset(cnt, 0, sizeof cnt); memset(mult, 0, sizeof mult);
        for (int i = 0; i < k; i++) { x[i] = saved[i]; mult[x[i]]++; addc(x[i], +1); }
        for (int q = ntimes; q < next; q++) inT[order[q]] = 1;
        ntimes = next;
    }
    printf("# est_multisets %.6e rel_err_binomial %.4f orbits_approx %.6e\n", exp(logcount), sqrt(relvar), exp(logcount) / h);
    fflush(stdout);
    for (long t = 0; t < 20 * FT; t++) step();
    for (long s = 0; s < FN; s++) {
        for (long t = 0; t < FT; t++) step();
        int y[MAXK]; memcpy(y, x, sizeof(int) * k); qsort(y, k, sizeof(int), cmpi);
        printf("M"); for (int i = 0; i < k; i++) printf(" %d", y[i]); printf("\n");
    }
    return 0;
}
