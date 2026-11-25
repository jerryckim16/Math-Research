/* gate15.c -- binary cascade and kill for k-speed gates with k+1 a power of
 * two (k = 15: the kill level 16 = 2^4 is reached by the binary cascade
 * itself).  Written for the LRC(15) pilot (notes/lonely-runner/gates.md);
 * the lift enumeration is the branch and bound of gatecheck.c / liftfree.c.
 *
 * Definitions (arXiv:2604.23906, Def. 2.1): N = l p, w in Z_N^k with p not
 * dividing any w_i is IMPROPER iff no t in (1/N)Z has (k+1) d_N(t w_i) >= N
 * for all i, AND no i has gcd(l, w_j : j != i) > 1.
 *
 * Usage: gate15 k p LMAX      stdin: level-one rows (k residues mod p)
 *   For each row r: check that r is witness-free at level 1 (else the row is
 *   reported as BADROW: it is not in I(k,p,1)); S_1 = {r};
 *   S_{2l} = improper lifts (w_i + j_i l p, j_i in {0,1}) of S_l,
 *   for l = 1, 2, ..., LMAX/2 (stop when empty).  At each level l >= 4 the
 *   members of S_l are tested with the shift lemma (Lemma S, gates.md) for
 *   every d | l, d >= 4: with E = {i : d does not divide w_i}, g_i =
 *   gcd(w_i, d), b_i = g_i * ceil(2d / ((k+1) g_i)), the member is SHIFT-KILLED
 *   if sum_{i in E} b_i < d.  (Then every integer u == w mod N is lonely,
 *   given LRC(k - |E|).)
 *   Prints per row: "idx n2 n4 n8 n16 n32 f4 f8 f16 f32" where n_l = |S_l|
 *   (0 beyond the last level computed) and f_l = members of S_l NOT
 *   shift-killed (-1 when l > LMAX).
 *   Env G15_DUMP=1: also print "SURV l w_1..w_k" for every unkilled member at
 *   the last level (diagnostics; first 50 per row).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAXK 16
static int k, p;
typedef uint64_t word;
typedef struct { int N, W; word *g; } level_t;
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
static int shift_killed(const int *w, int l) {
    for (int d = 4; d <= l; d *= 2) {
        if (l % d) continue;
        long s = 0;
        for (int i = 0; i < k; i++) {
            if (w[i] % d == 0) continue;
            int g = gcdi(w[i], d);
            long num = 2L * d, den = (long)(k + 1) * g;
            s += (long)g * ((num + den - 1) / den);
        }
        if (s < d) return 1;
    }
    return 0;
}
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
#define MAXS 4000000
static int *Sa, *Sb; static long na, nb; static int curl;
static int push_improper(const int *w) {
    if (gcd_clause(w, curl)) return 0;
    if (nb >= MAXS) { fprintf(stderr, "cascade overflow\n"); exit(1); }
    memcpy(Sb + nb * k, w, k * sizeof(int)); nb++; return 0;
}
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: gate15 k p LMAX\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); int lmax = atoi(argv[3]);
    if (k > MAXK || lmax < 2 || lmax > 32 || (lmax & (lmax - 1))) return 2;
    int nlev = __builtin_ctz(lmax);
    int dump = getenv("G15_DUMP") ? atoi(getenv("G15_DUMP")) : 0;
    level_t L[6]; for (int e = 0; e <= nlev; e++) L[e] = mk((1 << e) * p);
    Sa = malloc(sizeof(int) * (size_t)MAXS * k); Sb = malloc(sizeof(int) * (size_t)MAXS * k);
    char line[4096]; long idx = 0, bad = 0;
    while (fgets(line, sizeof line, stdin)) {
        int v[MAXK], n = 0; char *s = line, *e;
        for (;;) { long x = strtol(s, &e, 10); if (e == s) break; if (n < MAXK) v[n++] = (int)(((x % p) + p) % p); s = e; }
        if (n == 0) continue;
        if (n != k) { fprintf(stderr, "bad row\n"); return 1; }
        /* level-one witness test */
        { int W = L[0].W; word acc[1024]; int any = 1;
          for (int x = 0; x < W; x++) acc[x] = ~0ULL;
          if (L[0].N % 64) acc[W - 1] = (1ULL << (L[0].N % 64)) - 1;
          for (int i = 0; i < k && any; i++) { if (v[i] == 0) { any = 1; break; } const word *g = L[0].g + (size_t)v[i] * W; any = 0; for (int x = 0; x < W; x++) { acc[x] &= g[x]; any |= acc[x] != 0; } }
          if (any) { bad++; printf("BADROW %ld\n", idx); idx++; continue; } }
        memcpy(Sa, v, k * sizeof(int)); na = 1;
        long cnt[6] = {0}, fail[6]; for (int i = 0; i < 6; i++) fail[i] = -1;
        for (int ex = 1; ex <= nlev; ex++) {
            nb = 0; curl = 1 << ex;
            if (na > 0) for (long r = 0; r < na; r++) run_lifts(Sa + r * k, (1 << (ex - 1)) * p, 2, &L[ex], push_improper);
            cnt[ex] = nb;
            if (ex >= 2) {
                long f = 0, shown = 0;
                for (long r = 0; r < nb; r++) if (!shift_killed(Sb + r * k, curl)) {
                    f++;
                    if (dump && ex == nlev && shown < 50) { shown++; printf("SURV %d", curl); for (int i = 0; i < k; i++) printf(" %d", Sb[r * k + i]); printf("\n"); }
                }
                fail[ex] = f;
            }
            int *t = Sa; Sa = Sb; Sb = t; na = nb;
        }
        printf("%ld %ld %ld %ld %ld %ld %ld %ld %ld %ld\n", idx, cnt[1], cnt[2], cnt[3], cnt[4], cnt[5], fail[2], fail[3], fail[4], fail[5]);
        fflush(stdout);
        idx++;
    }
    fprintf(stderr, "rows %ld badrows %ld\n", idx, bad);
    return 0;
}
