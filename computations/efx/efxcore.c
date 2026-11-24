/*
 * efxcore.c -- exact EFX(0) existence checker for additive valuations.
 *
 * Definition checked (zero-tolerant "EFX_0", the form in the problem file):
 *   allocation X = (X_1..X_n) partitions all m goods; it is EFX iff for all
 *   i != j and every g in X_j:  v_i(X_i) >= v_i(X_j) - v_i(g).
 * Equivalently v_i(X_i) >= r_i(X_j) where r_i(B) = v_i(B) - min_{g in B} v_i(g)
 * for nonempty B (no constraint for empty B).
 *
 * Method: enumerate unordered set partitions of the goods into at most n
 * blocks (restricted growth strings), pad with empty blocks, and for each
 * partition decide whether some bijection agents -> blocks is EFX.  Agent i
 * can take block k iff v_i(B_k) >= max_{k' != k} r_i(B_{k'}).  Every complete
 * allocation arises from exactly one padded partition, so this is exhaustive.
 * All EFX decisions use exact 64-bit integer arithmetic (values must satisfy
 * m * max value < 2^62).  The double "score" is a heuristic only.
 *
 * Build: gcc -O3 -march=native -shared -fPIC -o libefx.so efxcore.c
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#define MAXN 6
#define MAXM 16
#define NEG_INF INT64_MIN

typedef struct {
    int n, m, mode;
    int64_t *val;   /* val[i*(1<<m)+S] */
    int64_t *thr;   /* r_i(S); NEG_INF for S empty */
    int64_t tot[MAXN];
    int nperm;
    int perm[720][MAXN];
    uint32_t blocks[MAXN];
    int nblocks;
    /* outputs */
    int found;
    long long count;          /* ordered EFX allocations */
    long long count_part;     /* padded partitions admitting an EFX matching */
    double best;              /* max over allocations of min_i normalised slack */
    uint32_t best_blocks[MAXN];
    int best_perm[MAXN];
    int have_best;
    long long leaves;
} ctx_t;

static void gen_perms(ctx_t *c) {
    int n = c->n, a[MAXN], i;
    for (i = 0; i < n; i++) a[i] = i;
    c->nperm = 0;
    /* Heap-free lexicographic generation */
    for (;;) {
        memcpy(c->perm[c->nperm++], a, sizeof(int) * n);
        int k = n - 2;
        while (k >= 0 && a[k] > a[k + 1]) k--;
        if (k < 0) break;
        int l = n - 1;
        while (a[l] < a[k]) l--;
        int t = a[k]; a[k] = a[l]; a[l] = t;
        for (i = k + 1, l = n - 1; i < l; i++, l--) { t = a[i]; a[i] = a[l]; a[l] = t; }
    }
}

static int fact(int e) { int f = 1; while (e > 1) f *= e--; return f; }

/* returns 1 to request early stop */
static int leaf(ctx_t *c) {
    int n = c->n, m = c->m, i, k;
    size_t W = (size_t)1 << m;
    int64_t diff[MAXN][MAXN];
    c->leaves++;
    for (i = 0; i < n; i++) {
        const int64_t *vi = c->val + i * W, *ti = c->thr + i * W;
        int64_t t1 = NEG_INF, t2 = NEG_INF; int a1 = -1;
        for (k = 0; k < n; k++) {
            int64_t t = ti[c->blocks[k]];
            if (t > t1) { t2 = t1; t1 = t; a1 = k; } else if (t > t2) t2 = t;
        }
        for (k = 0; k < n; k++) {
            int64_t other = (k == a1) ? t2 : t1;
            int64_t own = vi[c->blocks[k]];
            diff[i][k] = (other == NEG_INF) ? INT64_MAX / 4 : own - other;
        }
    }
    if (c->mode == 0) {
        for (int p = 0; p < c->nperm; p++) {
            const int *pp = c->perm[p];
            for (i = 0; i < n; i++) if (diff[i][pp[i]] < 0) break;
            if (i == n) {
                c->found = 1;
                memcpy(c->best_blocks, c->blocks, sizeof(c->blocks));
                memcpy(c->best_perm, pp, sizeof(int) * n);
                c->have_best = 1;
                return 1;
            }
        }
        return 0;
    }
    if (c->mode == 2 && c->have_best) {
        /* score-only mode: skip partitions that cannot beat the current best */
        double ub = DBL_MAX;
        for (i = 0; i < n; i++) {
            double mx = -DBL_MAX;
            for (k = 0; k < n; k++) {
                double s = diff[i][k] >= INT64_MAX / 8 ? 1e9
                         : (c->tot[i] > 0 ? (double)diff[i][k] / (double)c->tot[i] : 1e9);
                if (s > mx) mx = s;
            }
            if (mx < ub) ub = mx;
        }
        if (ub <= c->best) return 0;
    }
    /* full mode: count and bottleneck score */
    int empties = 0;
    for (k = 0; k < n; k++) if (c->blocks[k] == 0) empties++;
    long long cnt = 0;
    double sl[MAXN][MAXN];
    for (i = 0; i < n; i++) for (k = 0; k < n; k++) {
        if (diff[i][k] >= INT64_MAX / 8) sl[i][k] = 1e9;
        else sl[i][k] = c->tot[i] > 0 ? (double)diff[i][k] / (double)c->tot[i] : 1e9;
    }
    for (int p = 0; p < c->nperm; p++) {
        const int *pp = c->perm[p];
        double mn = DBL_MAX; int ok = 1;
        for (i = 0; i < n; i++) {
            if (diff[i][pp[i]] < 0) ok = 0;
            if (sl[i][pp[i]] < mn) mn = sl[i][pp[i]];
        }
        if (ok) cnt++;
        if (!c->have_best || mn > c->best) {
            c->best = mn; c->have_best = 1;
            memcpy(c->best_blocks, c->blocks, sizeof(c->blocks));
            memcpy(c->best_perm, pp, sizeof(int) * n);
        }
    }
    if (cnt) { c->found = 1; c->count_part++; c->count += cnt / fact(empties); }
    return 0;
}

static int rec(ctx_t *c, int g) {
    if (g == c->m) return leaf(c);
    uint32_t bit = 1u << g;
    for (int k = 0; k < c->nblocks; k++) {
        c->blocks[k] |= bit;
        int r = rec(c, g + 1);
        c->blocks[k] &= ~bit;
        if (r) return 1;
    }
    if (c->nblocks < c->n) {
        c->blocks[c->nblocks++] = bit;
        int r = rec(c, g + 1);
        c->blocks[--c->nblocks] = 0;
        if (r) return 1;
    }
    return 0;
}

/*
 * efx_eval
 *   n, m     : agents (<= 6), goods (<= 16)
 *   v        : n*m nonnegative integers, row-major (agent i, good g)
 *   mode     : 0 = stop at first EFX allocation; 1 = enumerate everything;
 *              2 = score only (branch-and-bound; count is then a lower bound)
 *   witness  : out, length m: agent index owning each good (valid if ret==1,
 *              or in mode 1 the allocation maximising the min normalised slack)
 *   score    : out (mode 1): max over allocations of min_i slack_i / total_i;
 *              EFX exists iff score >= 0 (up to float rounding; use the
 *              return value for the exact answer)
 *   count    : out (mode 1): number of EFX allocations (ordered, complete)
 * returns 1 if an EFX allocation exists (exact), 0 if not, -1 on bad input.
 */
int efx_eval(int n, int m, const int64_t *v, int mode, int *witness,
             double *score, long long *count) {
    if (n < 1 || n > MAXN || m < 0 || m > MAXM) return -1;
    ctx_t *c = calloc(1, sizeof(ctx_t));
    size_t W = (size_t)1 << m;
    c->n = n; c->m = m; c->mode = mode;
    c->val = malloc(sizeof(int64_t) * W * n);
    c->thr = malloc(sizeof(int64_t) * W * n);
    for (int i = 0; i < n; i++) {
        int64_t *vi = c->val + i * W, *ti = c->thr + i * W;
        vi[0] = 0; ti[0] = NEG_INF;
        int64_t tot = 0;
        for (int g = 0; g < m; g++) { if (v[i * m + g] < 0) { free(c->val); free(c->thr); free(c); return -1; } tot += v[i * m + g]; }
        c->tot[i] = tot;
        /* minval via lowest bit recursion */
        int64_t *mn = malloc(sizeof(int64_t) * W);
        mn[0] = INT64_MAX;
        for (size_t S = 1; S < W; S++) {
            int g = __builtin_ctzll(S);
            size_t R = S & (S - 1);
            vi[S] = vi[R] + v[i * m + g];
            int64_t x = v[i * m + g];
            mn[S] = mn[R] < x ? mn[R] : x;
            ti[S] = vi[S] - mn[S];
        }
        free(mn);
    }
    gen_perms(c);
    c->blocks[0] = 0; c->nblocks = 0;
    if (m == 0) { /* single empty allocation, trivially EFX */
        if (witness) {}
        if (score) *score = 1e9;
        if (count) *count = 1;
        free(c->val); free(c->thr); free(c); return 1;
    }
    if (mode == 2 && witness && witness[0] >= 0) {
        /* seed the branch-and-bound with the caller's allocation */
        uint32_t own[MAXN] = {0};
        int okseed = 1;
        for (int g = 0; g < m; g++) {
            if (witness[g] < 0 || witness[g] >= n) { okseed = 0; break; }
            own[witness[g]] |= 1u << g;
        }
        if (okseed) {
            double mn = DBL_MAX;
            for (int i = 0; i < n; i++) {
                int64_t other = NEG_INF;
                for (int j = 0; j < n; j++) if (j != i) {
                    int64_t t = c->thr[i * W + own[j]];
                    if (t > other) other = t;
                }
                double s = (other == NEG_INF || c->tot[i] == 0) ? 1e9
                         : (double)(c->val[i * W + own[i]] - other) / (double)c->tot[i];
                if (s < mn) mn = s;
            }
            /* strictly below, so the enumeration re-finds an allocation at least this good */
            c->best = mn - 1e-12; c->have_best = 1;
            memcpy(c->best_blocks, own, sizeof(own));
            for (int i = 0; i < n; i++) c->best_perm[i] = i;
        }
    }
    rec(c, 0);
    if (witness && c->have_best) {
        for (int i = 0; i < n; i++) {
            uint32_t B = c->best_blocks[c->best_perm[i]];
            for (int g = 0; g < m; g++) if (B >> g & 1) witness[g] = i;
        }
    }
    if (score) *score = c->best;
    if (count) *count = c->count;
    int ret = c->found;
    free(c->val); free(c->thr); free(c);
    return ret;
}
