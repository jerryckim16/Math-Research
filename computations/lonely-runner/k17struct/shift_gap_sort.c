/* shift_gap_sort.c -- independent second computation of Lambda(k,c) (see shift_gap_exact.c).
 *
 * Different algorithm from shift_gap_exact.c: for each y (y_1 = 0, y != 0) and each r,
 * list ALL open bad arcs of G(y,r) as exact integers on the circle R/DZ,
 * D = c(k+1)lcm(1..k), sort them by left end (qsort) and sweep; the longest closed good
 * arc is the largest (next left end) - (current reach) that is >= 0.
 * The arc of speed 1 (y_1 = 0) is (-D/(k+1), D/(k+1)); it is split as (-D/(k+1), D/(k+1))
 * and (D - D/(k+1), D + D/(k+1)), and every other arc (length <= D/(k+1)) is placed with
 * its left end reduced into [0, D); its right end is then < D + D/(k+1), inside the
 * second speed-1 piece, so no good arc is lost or invented at the seam.
 *
 * Usage: shift_gap_sort k c            full enumeration, prints Lambda and all argmins
 *        shift_gap_sort k c eval       reads y_1..y_k per line, prints len(y,r) for r=1..c-1
 * Lengths are printed as integers in units of 1/D (-1 = empty good set).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static int k, c; static ll D, L;
typedef struct { ll lo, hi; } arc;
static arc A[4096];
static int cmparc(const void *a, const void *b) { ll x = ((const arc *)a)->lo, y = ((const arc *)b)->lo; return x < y ? -1 : x > y; }
static ll gcdl(ll a, ll b) { while (b) { ll t = a % b; a = b; b = t; } return a; }
static ll md(ll a, ll m) { a %= m; return a < 0 ? a + m : a; }

static ll len_of(const int *y, int r) {
    int na = 0;
    ll R1 = D / (k + 1);
    A[na].lo = -R1; A[na].hi = R1; na++;
    A[na].lo = D - R1; A[na].hi = D + R1; na++;
    for (int i = 2; i <= k; i++) {
        int s = (y[i] * r) % c;
        /* centre (n - s/c)/i, radius 1/((k+1)i), times D */
        ll rad = D / ((ll)(k + 1) * i);
        for (int n = 0; n < i; n++) {
            /* centre numerator: D*(n*c - s)/(c*i) -- exact since c*i | D */
            ll cen = (D / ((ll)c * i)) * ((ll)n * c - s);
            ll lo = md(cen - rad, D);
            A[na].lo = lo; A[na].hi = lo + 2 * rad; na++;
        }
    }
    qsort(A, na, sizeof(arc), cmparc);
    ll reach = A[0].hi, best = -1;   /* A[0] = (-R1,R1) */
    for (int a = 1; a < na; a++) {
        if (A[a].lo >= reach && A[a].lo - reach > best) best = A[a].lo - reach;
        if (A[a].hi > reach) reach = A[a].hi;
    }
    return best;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 2; }
    k = atoi(argv[1]); c = atoi(argv[2]);
    L = 1; for (int i = 2; i <= k; i++) L = L / gcdl(L, i) * i;
    D = (ll)c * (k + 1) * L;
    int y[64];
    if (argc > 3 && !strcmp(argv[3], "eval")) {
        for (;;) {
            int ok = 1;
            for (int i = 1; i <= k; i++) if (scanf("%d", &y[i]) != 1) { ok = 0; break; }
            if (!ok) break;
            for (int r = 1; r < c; r++) printf(r > 1 ? " %lld" : "%lld", len_of(y, r));
            printf("\n");
        }
        return 0;
    }
    ll total = 1; for (int i = 2; i <= k; i++) total *= c;
    ll minv = -2, nmin = 0;
    y[1] = 0;
    for (ll code = 1; code < total; code++) {
        ll x = code; for (int i = k; i >= 2; i--) { y[i] = x % c; x /= c; }
        ll m = -1;
        for (int r = 1; r < c; r++) { ll v = len_of(y, r); if (v > m) m = v; }
        if (minv == -2 || m < minv) { minv = m; nmin = 0; }
        if (m == minv) {
            nmin++;
            printf("argmin candidate (value %lld):", m); for (int i = 1; i <= k; i++) printf(" %d", y[i]); printf("\n");
        }
    }
    ll g = gcdl(minv, D);
    printf("SORT k=%d c=%d D=%lld Lambda = %lld/%lld = %lld/%lld = 1/%.4f attained by %lld (last printed block)\n",
           k, c, D, minv, D, minv / g, D / g, (double)D / minv, nmin);
    return 0;
}
