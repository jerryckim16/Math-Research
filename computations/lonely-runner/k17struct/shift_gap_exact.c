/* shift_gap_exact.c -- EXACT value of the shifted-Dirichlet gap Lambda(k,c).
 *
 * Setting (notes/lonely-runner/structure.md, Lemma R; notes/lonely-runner/k17-structure.md).
 * For y in Z_c^k and r in Z_c put
 *     G(y,r) = { t in R/Z : || i t + y_i r / c || >= 1/(k+1)  for all i = 1..k }.
 * G(y,r) is closed: the complement of the open "bad" arcs
 *     B(i,n) = ( (n - y_i r/c - 1/(k+1)) / i , (n - y_i r/c + 1/(k+1)) / i ),  n in Z.
 * len(y,r) = length of the longest closed arc contained in G(y,r) (0 if G is a point set,
 * -1 if G is empty).  Lambda(k,c) = min over NONTRIVIAL y of max_{r != 0} len(y,r),
 * where y is trivial iff y = j(1..k) mod c.
 *
 * Exactness.  Every endpoint has denominator dividing c(k+1)i, so all endpoints are
 * integers in units of 1/D, D = c(k+1) lcm(1..k).  The good set is kept as a sorted list
 * of disjoint closed integer intervals [a,b] (a <= b) and each coordinate subtracts its
 * open arcs exactly.  No floating point is used.
 *
 * Reductions (proved in the note):
 *  - y -> y + j(1..k) translates G(y,r) by -jr/c, so y_1 = 0 (then trivial <=> y = 0);
 *  - with y_1 = 0 the coordinate i = 1 leaves G inside [D/(k+1), D - D/(k+1)]: no wrap.
 *  - r ranges over 1..c-1 (all of them; no symmetry is used, so the output also checks
 *    G(y,c-r) = -G(y,r) numerically by agreement of the per-r minima).
 * Enumeration: DFS over y_2..y_k in Z_c, incremental subtraction, c^(k-1)-1 leaves.
 *
 * Usage: shift_gap_exact k c [r]      (r: only that shift; default all r = 1..c-1)
 * Output: per r, min over nontrivial y of len(y,r) with an argmin; then Lambda with argmin,
 * the number of y attaining it, and a histogram of 1/(max_r len) in coarse bins.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXK 24
#define MAXI 2048
typedef long long ll;
static int k, c, ronly = 0;
static ll D, L;
static ll iv[MAXK + 1][MAXI][2];
static int niv[MAXK + 1];
static int y[MAXK + 1];
static ll minLam = -2; static int argLam[MAXK + 1]; static ll nLam = 0;
static ll minR[64]; static int argR[64][MAXK + 1];
static ll leaves = 0;
static ll hist[8];  /* bins of D/len: <300, <600, <900, <1200, <1800, <2400, >=2400, empty/point */

static ll gcdl(ll a, ll b) { while (b) { ll t = a % b; a = b; b = t; } return a; }
static ll floordiv(ll a, ll b) { ll q = a / b; if ((a % b) && ((a < 0) != (b < 0))) q--; return q; }

/* subtract coordinate i (speed i) with shift numerator s = y_i * r mod c from level i-1 */
static void subtract(int i, int s) {
    int out = 0;
    ll unit = L / i;                    /* D/(c(k+1)i) */
    /* arc n: ( (n c(k+1) - s(k+1) - c) * unit , (n c(k+1) - s(k+1) + c) * unit ) */
    for (int a = 0; a < niv[i - 1]; a++) {
        ll lo = iv[i - 1][a][0], hi = iv[i - 1][a][1];
        /* arcs that can meet [lo,hi]: centre (n c(k+1) - s(k+1)) unit within radius c*unit */
        ll step = (ll)c * (k + 1) * unit;
        ll base = -(ll)s * (k + 1) * unit;
        ll n0 = floordiv(lo - base - c * unit, step);
        ll cur = lo;
        int alive = 1;
        for (ll n = n0; alive; n++) {
            ll blo = base + n * step - c * unit, bhi = base + n * step + c * unit;  /* open */
            if (blo >= hi) break;          /* arc entirely right of [cur,hi] (open: blo>=hi ok) */
            if (bhi <= cur) continue;      /* arc entirely left */
            /* arc meets: keep [cur, blo] if blo >= cur */
            if (blo >= cur) {
                if (out >= MAXI) { fprintf(stderr, "MAXI\n"); exit(3); }
                iv[i][out][0] = cur; iv[i][out][1] = blo; out++;
            }
            if (bhi > hi) { alive = 0; break; }
            cur = bhi;
        }
        if (alive) {
            if (out >= MAXI) { fprintf(stderr, "MAXI\n"); exit(3); }
            iv[i][out][0] = cur; iv[i][out][1] = hi; out++;
        }
    }
    niv[i] = out;
}

static ll maxlen(int i) {
    ll m = -1;
    for (int a = 0; a < niv[i]; a++) { ll d = iv[i][a][1] - iv[i][a][0]; if (d > m) m = d; }
    return m;
}

/* per-r DFS state: we run the whole DFS once per r, storing len(y,r) per leaf index */
static ll *leafval;   /* max over r so far, indexed by code */
static int rcur;

static void dfs(int i, ll code) {
    if (i > k) {
        if (code == 0) return;   /* trivial y */
        ll m = maxlen(k);
        leaves++;
        if (minR[rcur] == -2 || m < minR[rcur]) { minR[rcur] = m; memcpy(argR[rcur], y, sizeof y); }
        if (m > leafval[code]) leafval[code] = m;
        return;
    }
    for (int v = 0; v < c; v++) {
        y[i] = v;
        subtract(i, (v * rcur) % c);
        dfs(i + 1, code * c + v);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: shift_gap_exact k c [r]\n"); return 2; }
    k = atoi(argv[1]); c = atoi(argv[2]); if (argc > 3) ronly = atoi(argv[3]);
    L = 1; for (int i = 2; i <= k; i++) L = L / gcdl(L, i) * i;
    D = (ll)c * (k + 1) * L;
    ll total = 1; for (int i = 2; i <= k; i++) total *= c;
    leafval = malloc(sizeof(ll) * total);
    for (ll q = 0; q < total; q++) leafval[q] = -2;
    /* level 1: speed 1, y_1 = 0: good set [D/(k+1), D - D/(k+1)] */
    niv[0] = 0;
    y[1] = 0;
    for (int r = 1; r < c; r++) {
        if (ronly && r != ronly) continue;
        rcur = r; minR[r] = -2;
        niv[1] = 1; iv[1][0][0] = D / (k + 1); iv[1][0][1] = D - D / (k + 1);
        dfs(2, 0);
        printf("k=%d c=%d r=%d D=%lld: min over nontrivial y of len(y,r) = %lld/%lld = 1/%.4f ; argmin y =",
               k, c, r, D, minR[r], D, minR[r] > 0 ? (double)D / minR[r] : 0.0);
        for (int t = 1; t <= k; t++) printf(" %d", argR[r][t]);
        printf("\n");
    }
    for (ll q = 1; q < total; q++) {
        ll m = leafval[q];
        if (minLam == -2 || m < minLam) { minLam = m; nLam = 0; ll x = q; for (int t = k; t >= 2; t--) { argLam[t] = x % c; x /= c; } argLam[1] = 0; }
        if (m == minLam) nLam++;
        double inv = m > 0 ? (double)D / m : 1e18;
        int b = m <= 0 ? 7 : inv < 300 ? 0 : inv < 600 ? 1 : inv < 900 ? 2 : inv < 1200 ? 3 : inv < 1800 ? 4 : inv < 2400 ? 5 : 6;
        hist[b]++;
    }
    ll g = gcdl(minLam > 0 ? minLam : 1, D);
    printf("Lambda(%d,%d) = %lld/%lld = %lld/%lld = 1/%.4f  (nontrivial y with y_1=0: %lld; attained by %lld; leaves visited %lld)\nargmin y =",
           k, c, minLam, D, minLam / g, D / g, minLam > 0 ? (double)D / minLam : 0.0, total - 1, nLam, leaves);
    for (int t = 1; t <= k; t++) printf(" %d", argLam[t]);
    printf("\nhistogram of 1/max_r len(y,r): <300 %lld | <600 %lld | <900 %lld | <1200 %lld | <1800 %lld | <2400 %lld | >=2400 %lld | len<=0 %lld\n",
           hist[0], hist[1], hist[2], hist[3], hist[4], hist[5], hist[6], hist[7]);
    return 0;
}
