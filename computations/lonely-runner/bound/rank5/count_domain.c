/* Exact size of the rank-R multiplicity-vector domain (feasibility count).
 *
 * For a greedy profile s = (s_1..s_R), count the multiplicity vectors m over
 * the (3^R - 1)/2 projective nonzero ternary types with row supports exactly
 * s (row i: sum of m_c over types c with c_i != 0) and sum m <= n.
 * Types are grouped by support pattern P (nonempty subset of rows); a pattern
 * with |P| = j holds 2^(j-1) types, and k columns of pattern P can be spread
 * over its types in C(k + 2^(j-1) - 1, 2^(j-1) - 1) ways.  DP over patterns
 * with state (partial row supports, total).  Counts in unsigned __int128.
 *
 * Usage: count_domain n R  < profiles   (one profile per line, R integers)
 * Output: one line per profile with its count, then the total.
 * Validation: R = 4, n = 17 over the 49 surviving profiles must give
 * 135,937,974 (bound-rank4.md, section 4).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
static int R, N;

static void print128(u128 x) {
    char b[64]; int i = 63; b[i] = 0;
    if (!x) { printf("0"); return; }
    while (x) { b[--i] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", b + i);
}

static u128 binom(int a, int b) {
    if (b < 0 || b > a) return 0;
    u128 r = 1;
    for (int i = 1; i <= b; i++) r = r * (a - b + i) / i;
    return r;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: count_domain n R < profiles\n"); return 1; }
    N = atoi(argv[1]); R = atoi(argv[2]);
    int s[8];
    u128 total = 0;
    while (1) {
        int ok = 1;
        for (int i = 0; i < R; i++) if (scanf("%d", &s[i]) != 1) { ok = 0; break; }
        if (!ok) break;
        /* state index: r_0..r_{R-1} (0..s_i), tot (0..N) */
        long dims[9], size = 1;
        for (int i = 0; i < R; i++) { dims[i] = s[i] + 1; size *= dims[i]; }
        dims[R] = N + 1; size *= dims[R];
        u128 *cur = calloc(size, sizeof(u128)), *nxt = calloc(size, sizeof(u128));
        cur[0] = 1;
        for (int P = 1; P < (1 << R); P++) {
            int j = __builtin_popcount(P), t = 1 << (j - 1);
            memset(nxt, 0, size * sizeof(u128));
            for (long idx = 0; idx < size; idx++) {
                if (!cur[idx]) continue;
                long x = idx; int r[9];
                for (int i = 0; i <= R; i++) { r[i] = x % dims[i]; x /= dims[i]; }
                for (int k = 0;; k++) {
                    int rr[9]; int bad = 0;
                    for (int i = 0; i < R; i++) { rr[i] = r[i] + ((P >> i) & 1) * k; if (rr[i] > s[i]) bad = 1; }
                    rr[R] = r[R] + k; if (rr[R] > N) bad = 1;
                    if (bad) break;
                    long ni = 0, mul = 1;
                    for (int i = 0; i <= R; i++) { ni += rr[i] * mul; mul *= dims[i]; }
                    nxt[ni] += cur[idx] * binom(k + t - 1, t - 1);
                }
            }
            u128 *tmp = cur; cur = nxt; nxt = tmp;
        }
        u128 cnt = 0;
        for (int tot = 0; tot <= N; tot++) {
            long ni = 0, mul = 1;
            for (int i = 0; i < R; i++) { ni += s[i] * mul; mul *= dims[i]; }
            ni += tot * mul;
            cnt += cur[ni];
        }
        for (int i = 0; i < R; i++) printf("%d%c", s[i], i + 1 < R ? ',' : ' ');
        print128(cnt); printf("\n");
        total += cnt;
        free(cur); free(nxt);
    }
    printf("TOTAL "); print128(total); printf("\n");
    return 0;
}
