/* gatecheck.c -- independent re-computation of the per-row cascade and the
 * per-orbit level-15 kill for LRC(14) gate certificates (Allikvere,
 * arXiv:2609.02604v2, Section 4), using only the definitions:
 *
 *   w in Z_{p,l}^k is improper iff no t in (1/(lp))Z has (k+1) d_N(t w_i) >= N
 *   for all i (N = lp)  AND  no i has gcd(l, w_j : j != i) > 1.
 *
 * Usage:
 *   gatecheck cascade k p     stdin: level-one rows (k residues mod p)
 *     For each row r: S_1 = {r}; S_{2l} = improper lifts (w_i + j_i*lp,
 *     j_i in {0,1}) of S_l, for l = 1,2,4,8,16 (stop when empty).
 *     Prints "idx n2 n4 n8 n16 n32" (|S_l|, with multiplicity per row).
 *   gatecheck kill k p        stdin: level-one orbit representatives
 *     For each r: W3 / W5 = witness-free lifts of r to level 3 / 5 (no gcd
 *     clause), CRT-combine W3 x W5 to level-15 lifts (Lemma 4.4 there: any
 *     witness-free level-15 lift reduces to witness-free lifts at 3 and 5),
 *     test the level-15 grid, then the gcd clause (l = 15), then the
 *     few-exception shift Lemma 3.12 for d in {3, 5}:
 *       e = #{i : d does not divide w_i}, m_d = ceil(2d/(k+1)); it applies
 *       when 2 <= e and e*m_d < d.
 *     Prints "idx wf3 wf5 crt wf15 improper_after_gcd improper_after_neargcd".
 *   gatecheck hexrows k p n   stdin: certificate row files (hex, 2 or 4 hex
 *     digits per class, n classes per line).  Tests every row for a level-1
 *     witness t = m/p with (k+1) d_p(m v_i) >= p for all i (the threshold
 *     uses k even when n = k-1, as for km1 covers).  Prints
 *     "rows R with_witness X" and up to 20 offending rows.
 * Branch and bound as in liftfree.c (cuts only branches with no
 * witness-free completion).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 16
static int k, p;
typedef uint64_t word;

typedef struct { int N, W; word *g; } level_t;   /* g[w*W ..] = good times of speed w mod N */
static level_t mk(int N) {
    level_t L; L.N = N; L.W = (N + 63) / 64;
    L.g = calloc((size_t)N * L.W, sizeof(word));
    for (int w = 0; w < N; w++)
        for (int m = 0; m < N; m++) {
            long r = ((long)w * m) % N, d = r < N - r ? r : N - r;
            if ((long)(k + 1) * d >= N) L.g[(size_t)w * L.W + m / 64] |= 1ULL << (m % 64);
        }
    return L;
}
static int gcdi(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a < 0 ? -a : a; }
static int gcd_clause(const int *w, int l) {
    if (l == 1) return 0;
    for (int i = 0; i < k; i++) { int g = l; for (int j = 0; j < k; j++) if (j != i) g = gcdi(g, w[j]); if (g > 1) return 1; }
    return 0;
}
/* enumerate witness-free lifts of base (mod M) by factor c into level L (N = cM) */
static int cur[MAXK], base[MAXK], cfac, Mmod;
static level_t *LV;
static int (*sink)(const int *w);
static word accbuf[MAXK + 1][1024];
static int popc(const word *a, int W) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a[i]); return s; }
static void enumlifts(int i) {
    int W = LV->W; const word *acc = accbuf[i];
    int n = popc(acc, W);
    if (i == k) { if (n == 0) sink(cur); return; }
    if (n > 0) {
        long cap = 0;
        for (int t = i; t < k; t++) {
            int best = 0;
            for (int j = 0; j < cfac; j++) {
                const word *g = LV->g + (size_t)(base[t] + j * Mmod) * W; int r = 0;
                for (int x = 0; x < W; x++) r += __builtin_popcountll(acc[x] & ~g[x]);
                if (r > best) best = r;
            }
            cap += best;
        }
        if (cap < n) return;
    }
    for (int j = 0; j < cfac; j++) {
        int w = base[i] + j * Mmod;
        const word *g = LV->g + (size_t)w * W;
        for (int x = 0; x < W; x++) accbuf[i + 1][x] = acc[x] & g[x];
        cur[i] = w; enumlifts(i + 1);
    }
}
static void run_lifts(const int *b, int M, int c, level_t *L, int (*f)(const int *)) {
    memcpy(base, b, k * sizeof(int)); Mmod = M; cfac = c; LV = L; sink = f;
    for (int x = 0; x < L->W; x++) accbuf[0][x] = ~0ULL;
    if (L->N % 64) accbuf[0][L->W - 1] = (1ULL << (L->N % 64)) - 1;
    enumlifts(0);
}
/* ---- cascade ---- */
#define MAXS 2000000
static int *Sa, *Sb; static long na, nb; static int curl;
static int push_improper(const int *w) {
    if (gcd_clause(w, curl)) return 0;
    if (nb >= MAXS) { fprintf(stderr, "cascade overflow\n"); exit(1); }
    memcpy(Sb + nb * k, w, k * sizeof(int)); nb++; return 0;
}
/* ---- kill ---- */
#define MAXW 200000
static int W3[MAXW][MAXK], W5[MAXW][MAXK]; static long n3, n5;
static int add3(const int *w) { if (n3 >= MAXW) { fprintf(stderr, "W3 overflow\n"); exit(1); } memcpy(W3[n3++], w, k * sizeof(int)); return 0; }
static int add5(const int *w) { if (n5 >= MAXW) { fprintf(stderr, "W5 overflow\n"); exit(1); } memcpy(W5[n5++], w, k * sizeof(int)); return 0; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: gatecheck cascade|kill k p | hexrows k p n\n"); return 2; }
    if (!strcmp(argv[1], "hexrows")) {
        if (argc != 5) return 2;
        k = atoi(argv[2]); p = atoi(argv[3]); int n = atoi(argv[4]);
        level_t L = mk(p); int W = L.W; word acc[1024];
        char line[4096]; unsigned long long rows = 0, bad = 0;
        while (fgets(line, sizeof line, stdin)) {
            int len = (int)strcspn(line, "\r\n"); if (len == 0) continue;
            int wdt = len / n;
            if (wdt * n != len || (wdt != 2 && wdt != 4)) { fprintf(stderr, "bad hex row length %d\n", len); return 1; }
            int v[64];
            for (int i = 0; i < n; i++) { char b[5]; memcpy(b, line + i * wdt, wdt); b[wdt] = 0; v[i] = (int)strtol(b, 0, 16) % p; }
            for (int x = 0; x < W; x++) acc[x] = ~0ULL;
            if (L.N % 64) acc[W - 1] = (1ULL << (L.N % 64)) - 1;
            int any = 1;
            for (int i = 0; i < n && any; i++) { const word *g = L.g + (size_t)v[i] * W; any = 0; for (int x = 0; x < W; x++) { acc[x] &= g[x]; any |= acc[x] != 0; } }
            rows++;
            if (any) { bad++; if (bad <= 20) { printf("WITNESS"); for (int i = 0; i < n; i++) printf(" %d", v[i]); printf("\n"); } }
        }
        printf("rows %llu with_witness %llu\n", rows, bad);
        return 0;
    }
    int mode_kill = !strcmp(argv[1], "kill");
    k = atoi(argv[2]); p = atoi(argv[3]);
    if (k > MAXK) return 2;
    char line[4096]; long idx = 0;
    if (!mode_kill) {
        level_t L[6]; for (int e = 1; e <= 5; e++) L[e] = mk((1 << e) * p);
        Sa = malloc(sizeof(int) * (size_t)MAXS * k); Sb = malloc(sizeof(int) * (size_t)MAXS * k);
        while (fgets(line, sizeof line, stdin)) {
            int v[MAXK], n = 0; char *s = line, *e;
            for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (n < MAXK) v[n++] = (int)(((x % p) + p) % p); s = e; }
            if (n == 0) continue;
            if (n != k) { fprintf(stderr, "bad row\n"); return 1; }
            memcpy(Sa, v, k * sizeof(int)); na = 1;
            long counts[6] = {0};
            for (int ex = 1; ex <= 5 && na > 0; ex++) {
                nb = 0; curl = 1 << ex;
                for (long r = 0; r < na; r++) run_lifts(Sa + r * k, (1 << (ex - 1)) * p, 2, &L[ex], push_improper);
                counts[ex] = nb;
                int *t = Sa; Sa = Sb; Sb = t; na = nb;
            }
            printf("%ld %ld %ld %ld %ld %ld\n", idx, counts[1], counts[2], counts[3], counts[4], counts[5]);
            idx++;
        }
        return 0;
    }
    level_t L3 = mk(3 * p), L5 = mk(5 * p), L15 = mk(15 * p);
    while (fgets(line, sizeof line, stdin)) {
        int v[MAXK], n = 0; char *s = line, *e;
        for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (n < MAXK) v[n++] = (int)(((x % p) + p) % p); s = e; }
        if (n == 0) continue;
        if (n != k) { fprintf(stderr, "bad row\n"); return 1; }
        n3 = n5 = 0;
        run_lifts(v, p, 3, &L3, add3);
        run_lifts(v, p, 5, &L5, add5);
        long crt = 0, wf15 = 0, ig = 0, in = 0;
        int W = L15.W; word acc[1024];
        for (long a = 0; a < n3; a++) for (long b = 0; b < n5; b++) {
            int w[MAXK];
            for (int i = 0; i < k; i++) {
                int x = -1;
                for (int j = 0; j < 5; j++) { int y = W3[a][i] + 3 * p * j; if ((y - W5[b][i]) % (5 * p) == 0) { x = y; break; } }
                if (x < 0) { fprintf(stderr, "CRT failure\n"); return 1; }
                w[i] = x;
            }
            crt++;
            for (int x = 0; x < W; x++) acc[x] = ~0ULL;
            if (L15.N % 64) acc[W - 1] = (1ULL << (L15.N % 64)) - 1;
            int any = 0;
            for (int i = 0; i < k; i++) { const word *g = L15.g + (size_t)w[i] * W; any = 0; for (int x = 0; x < W; x++) { acc[x] &= g[x]; any |= acc[x] != 0; } if (!any) break; }
            if (any) continue;          /* has a witness on the level-15 grid */
            wf15++;
            if (gcd_clause(w, 15)) continue;
            ig++;
            int ok = 0;
            for (int d = 3; d <= 5; d += 2) {
                int ecount = 0; for (int i = 0; i < k; i++) if (w[i] % d) ecount++;
                int md = (2 * d + k) / (k + 1);   /* ceil(2d/(k+1)) */
                if (ecount >= 2 && ecount * md < d) ok = 1;
            }
            if (!ok) in++;
        }
        printf("%ld %ld %ld %ld %ld %ld %ld\n", idx, n3, n5, crt, wf15, ig, in);
        idx++;
    }
    return 0;
}
