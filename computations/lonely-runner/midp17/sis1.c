/* sis1.c -- Knuth / sequential-importance estimator of the level-one improper
 * set I(k,p,1) (as multisets), with importance-weighted sample leaves.
 *
 * Tree: non-decreasing sequences x_1 <= ... <= x_k of folded classes in 1..h,
 * so every k-multiset is exactly one leaf.  A multiset is improper at level one
 * iff its support covers every folded time (class v covers a iff
 * (k+1) d_p(a v) < p).  A node (prefix ending at x, uncovered times U, r slots
 * left) is cut only if no completion covers:
 *   (i)  some a in U has no coverer >= x, or
 *   (ii) r * max_{c >= x} |cov(c) & U| < |U|.
 * If U is empty every completion covers: the node contributes C(h-x+r, r)
 * leaves and one of them is drawn uniformly.
 * A probe walks from the root choosing a child uniformly; its weight is the
 * product of the numbers of children (times the completion count).  The mean
 * weight is an unbiased estimate of #I(k,p,1); the leaf, with its weight, is an
 * importance sample of the uniform distribution on I(k,p,1).
 *
 * Usage: sis1 k p PROBES SEED     prints "logw x_1 .. x_k" for each probe that
 *                                 reached a leaf ("-inf" probes are omitted),
 *                                 and on stderr the estimate of #multisets, its
 *                                 relative standard error and the effective
 *                                 sample size (sum w)^2 / sum w^2.
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
static uint64_t cov[MAXH + 2][WW], low[MAXH + 2][WW];
static uint64_t rs;
static inline uint64_t rnd(void) {
    uint64_t z = (rs += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static inline int rndb(int n) { return (int)(((unsigned __int128)rnd() * (unsigned)n) >> 64); }
static int popw(const uint64_t *a) { int s = 0; for (int w = 0; w < nw; w++) s += __builtin_popcountll(a[w]); return s; }
static int isz(const uint64_t *a) { for (int w = 0; w < nw; w++) if (a[w]) return 0; return 1; }
static double lchoose(int n, int r) { return lgamma(n + 1.0) - lgamma(r + 1.0) - lgamma(n - r + 1.0); }

/* node feasibility for prefix ending at x with uncovered U and r slots left */
static int feasible(int x, const uint64_t *U, int r) {
    if (isz(U)) return 1;
    if (r == 0) return 0;
    for (int w = 0; w < nw; w++) if (U[w] & low[x][w]) return 0;
    int n = popw(U), best = 0;
    for (int c = x; c <= h; c++) {
        int g = 0; for (int w = 0; w < nw; w++) g += __builtin_popcountll(cov[c][w] & U[w]);
        if (g > best) { best = g; if ((long)r * best >= n) return 1; }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: sis1 k p PROBES SEED\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2; nw = (h + 63) / 64;
    long probes = atol(argv[3]);
    rs = strtoull(argv[4], 0, 10) * 0x2545F4914F6CDD1DULL + (uint64_t)p * 7919;
    int maxcov[MAXH + 1];
    for (int a = 1; a <= h; a++) maxcov[a] = 0;
    for (int v = 1; v <= h; v++) {
        memset(cov[v], 0, sizeof cov[v]);
        for (int a = 1; a <= h; a++) { long r = (long)a * v % p; long d = r < p - r ? r : p - r; if ((k + 1) * d < p) { cov[v][(a - 1) >> 6] |= 1ULL << ((a - 1) & 63); if (v > maxcov[a]) maxcov[a] = v; } }
    }
    for (int x = 1; x <= h + 1; x++) { memset(low[x], 0, sizeof low[x]); for (int a = 1; a <= h; a++) if (maxcov[a] < x) low[x][(a - 1) >> 6] |= 1ULL << ((a - 1) & 63); }
    double sw = 0, sw2 = 0; long nleaf = 0;
    /* use log weights relative to a reference to avoid overflow */
    double ref = NAN;
    double *lw = malloc(sizeof(double) * probes);
    for (long t = 0; t < probes; t++) {
        uint64_t U[WW]; memset(U, 0, sizeof U);
        for (int a = 1; a <= h; a++) U[(a - 1) >> 6] |= 1ULL << ((a - 1) & 63);
        int x = 1, seq[MAXK], n = 0; double logw = 0; int dead = 0;
        while (n < k) {
            if (isz(U)) { /* uniform completion: multiset of size k-n from [x,h] */
                int r = k - n; logw += lchoose(h - x + r, r);
                /* stars and bars: choose r positions among h-x+r */
                int tot = h - x + r, need = r, pos = 0, val = x;
                for (int q = 0; q < tot && need > 0; q++) {
                    /* select q with probability need/(tot-q) */
                    if (rndb(tot - q) < need) { seq[n++] = val; need--; } else val++;
                    pos++;
                }
                break;
            }
            int ch[MAXH + 1], nc = 0, r = k - n - 1;
            for (int c = x; c <= h; c++) {
                uint64_t V[WW]; for (int w = 0; w < nw; w++) V[w] = U[w] & ~cov[c][w];
                if (feasible(c, V, r)) ch[nc++] = c;
            }
            if (nc == 0) { dead = 1; break; }
            int c = ch[rndb(nc)]; logw += log((double)nc);
            for (int w = 0; w < nw; w++) U[w] &= ~cov[c][w];
            seq[n++] = c; x = c;
        }
        if (dead || !isz(U)) { lw[t] = -INFINITY; continue; }
        lw[t] = logw; nleaf++;
        if (isnan(ref)) ref = logw;
        printf("%.6f", logw); for (int i = 0; i < k; i++) printf(" %d", seq[i]); printf("\n");
    }
    for (long t = 0; t < probes; t++) if (isfinite(lw[t])) { double w = exp(lw[t] - ref); sw += w; sw2 += w * w; }
    double mean = sw / probes, m2 = sw2 / probes, var = (m2 - mean * mean) / probes;
    fprintf(stderr, "k %d p %d probes %ld leaves %ld est_multisets %.6e rel_se %.4f ess %.1f orbits_approx %.6e\n",
            k, p, probes, nleaf, mean * exp(ref), sqrt(var > 0 ? var : 0) / mean, sw * sw / sw2, mean * exp(ref) / h);
    return 0;
}
