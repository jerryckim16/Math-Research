/*
 * enum_affine.c -- enumerate an affine lattice shell (our own Fincke-Pohst).
 *
 * Input (text): "d n", then the d x d symmetric positive definite integer
 * Gram matrix G, then d residues c_k in {0,1,2}. Output: every integer
 * vector x with x == c (mod 3) componentwise and x^T G x == n exactly,
 * written as int8 rows (row-major, d bytes per row) in lexicographic order
 * of (x_{d-1}, ..., x_0) as enumerated; the count goes to stdout.
 *
 * Method: G = R^T R (Cholesky, double precision). For a vector x,
 *   x^T G x = sum_i q_ii (x_i + sum_{j>i} q_ij x_j)^2,  q_ii = R_ii^2, q_ij = R_ij / R_ii.
 * Coordinates are chosen from i = d-1 down to 0 inside the interval allowed
 * by the remaining budget, stepping through the residue class mod 3. The
 * budget is n + 1e-6, so floating rounding (relative ~1e-13 here) cannot
 * prune a vector of norm n; every leaf's norm is then recomputed exactly in
 * int64 and kept only if it equals n. A pruning error could only lose
 * vectors (never add a wrong one); the builders compare the counts with the
 * published populations, and the pairwise check is of the rows written.
 *
 * Build: gcc -O3 -march=native -fopenmp enum_affine.c -o enum_affine -lm
 * Usage: enum_affine INPUT.txt OUT.i8
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MAXD 64
static int d;
static long n;
static long G[MAXD][MAXD];
static int res[MAXD];
static double q[MAXD][MAXD];

typedef struct { int8_t *buf; size_t len, cap; long leaves; } Out;

static void emit(Out *o, const int *x) {
    if (o->len + d > o->cap) { o->cap = o->cap ? 2 * o->cap : 1 << 20; o->buf = realloc(o->buf, o->cap); }
    for (int k = 0; k < d; k++) o->buf[o->len++] = (int8_t)x[k];
}

static long exact_norm(const int *x) {
    long s = 0;
    for (int i = 0; i < d; i++) { long t = 0; for (int j = 0; j < d; j++) t += G[i][j] * x[j]; s += t * x[i]; }
    return s;
}

/* first value >= lo with v == r (mod 3) */
static long first_ge(double lo, int r) {
    long v = (long)ceil(lo);
    long m = ((v - r) % 3 + 3) % 3;
    return m ? v + (3 - m) : v;
}

static void rec(int i, double budget, int *x, Out *o) {
    double c = 0;
    for (int j = i + 1; j < d; j++) c -= q[i][j] * x[j];
    double w = sqrt(budget / q[i][i]);
    for (long v = first_ge(c - w - 1e-9, res[i]); v <= c + w + 1e-9; v += 3) {
        double t = v - c, rem = budget - q[i][i] * t * t;
        if (rem < 0) continue;
        if (v < -127 || v > 127) { fprintf(stderr, "entry out of int8 range\n"); exit(3); }
        x[i] = (int)v;
        if (i == 0) {
            o->leaves++;
            if (exact_norm(x) == n) emit(o, x);
        } else rec(i - 1, rem, x, o);
    }
    x[i] = 0;
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s INPUT.txt OUT.i8\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f || fscanf(f, "%d %ld", &d, &n) != 2 || d < 2 || d > MAXD || n <= 0) { fprintf(stderr, "bad header\n"); return 2; }
    for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) if (fscanf(f, "%ld", &G[i][j]) != 1) { fprintf(stderr, "bad gram\n"); return 2; }
    for (int i = 0; i < d; i++) if (fscanf(f, "%d", &res[i]) != 1 || res[i] < 0 || res[i] > 2) { fprintf(stderr, "bad residue\n"); return 2; }
    fclose(f);
    for (int i = 0; i < d; i++) for (int j = 0; j < d; j++) if (G[i][j] != G[j][i]) { fprintf(stderr, "gram not symmetric\n"); return 2; }
    /* Cholesky G = R^T R */
    double R[MAXD][MAXD]; memset(R, 0, sizeof R);
    for (int i = 0; i < d; i++) {
        double s = (double)G[i][i];
        for (int k = 0; k < i; k++) s -= R[k][i] * R[k][i];
        if (s <= 0) { fprintf(stderr, "gram not positive definite\n"); return 2; }
        R[i][i] = sqrt(s);
        for (int j = i + 1; j < d; j++) {
            double t = (double)G[i][j];
            for (int k = 0; k < i; k++) t -= R[k][i] * R[k][j];
            R[i][j] = t / R[i][i];
        }
    }
    for (int i = 0; i < d; i++) { q[i][i] = R[i][i] * R[i][i]; for (int j = i + 1; j < d; j++) q[i][j] = R[i][j] / R[i][i]; }

    /* prefixes: the top two coordinates (x_{d-1}, x_{d-2}) */
    double B = (double)n + 1e-6;
    int np = 0; static int pre[100000][2]; static double prem[100000];
    {
        int i = d - 1; double w = sqrt(B / q[i][i]);
        for (long v = first_ge(-w - 1e-9, res[i]); v <= w + 1e-9; v += 3) {
            double r1 = B - q[i][i] * v * v; if (r1 < 0) continue;
            double c = -q[i - 1][i] * v, w2 = sqrt(r1 / q[i - 1][i - 1]);
            for (long u = first_ge(c - w2 - 1e-9, res[i - 1]); u <= c + w2 + 1e-9; u += 3) {
                double r2 = r1 - q[i - 1][i - 1] * (u - c) * (u - c); if (r2 < 0) continue;
                if (np == 100000) { fprintf(stderr, "too many prefixes\n"); return 2; }
                pre[np][0] = (int)v; pre[np][1] = (int)u; prem[np] = r2; np++;
            }
        }
    }
    Out *outs = calloc(np, sizeof(Out));
    #pragma omp parallel for schedule(dynamic, 1)
    for (int p = 0; p < np; p++) {
        int x[MAXD]; memset(x, 0, sizeof x);
        x[d - 1] = pre[p][0]; x[d - 2] = pre[p][1];
        if (d == 2) { outs[p].leaves++; if (exact_norm(x) == n) emit(&outs[p], x); }
        else rec(d - 3, prem[p], x, &outs[p]);
    }
    FILE *fo = fopen(argv[2], "wb");
    long cnt = 0, leaves = 0;
    for (int p = 0; p < np; p++) { fwrite(outs[p].buf, 1, outs[p].len, fo); cnt += outs[p].len / d; leaves += outs[p].leaves; free(outs[p].buf); }
    fclose(fo);
    printf("%ld %ld\n", cnt, leaves);
    return 0;
}
