/* xcasc.c -- extended cascade for one level-one base at a time (any k, any chain).
 *
 * Usage: xcasc k p CHAIN [CAP] [DUMP_LEVEL]   < bases (k folded classes per line)
 *   CHAIN: lift factors separated by commas, e.g. 2,3,3,2 (levels 2, 6, 18, 36).
 *   CAP:   abort a base when a retained set exceeds CAP orbits (default 2000000).
 *   DUMP_LEVEL: if given, print every retained tuple at that level as
 *               "S <baseidx> <level> w_1 .. w_k" (residues mod level*p).
 *
 * Definitions (notes/lonely-runner/midprimes17.md, section 2; same as
 * smallp/xcascade.py and k17struct/cascade_verify.c):
 *   A lift w of the level-l tuple to level L = c*l is w_i + j_i*l*p, 0 <= j_i < c.
 *   It is DISCARDED (extended-proper) if
 *     (a) it has a witness on the grid (1/(Lp))Z: some m in [0, Lp) with
 *         (k+1) d_{Lp}(m w_i) >= Lp for all i; or
 *     (b) the gcd clause holds: gcd(L, w_j : j != i) > 1 for some i; or
 *     (c) Lemma S / NG holds for some divisor d >= 2 of L:
 *         E = {i : d does not divide w_i}, g_i = gcd(w_i, d),
 *         |E| >= 2 and sum_{i in E} g_i * ceil(2d / ((k+1) g_i)) < d.
 *   The retained set at level L is the set of undiscarded lifts of the retained
 *   set at level l, up to the symmetries below.  Each discard reason persists to
 *   lifts, so an empty retained set at level L proves that every lift of the base
 *   to level L is extended-proper (Lemma 2.2(ii) at level L for this base).
 *
 * Representation and symmetry.  The base b is sorted, b_i in [1, (p-1)/2].
 * A level-l tuple is stored by e = w mod l (w = b mod p, by CRT).  Two tuples are
 * identified if they differ by a unit v of Z_l (i.e. the unit of Z_{lp} that is
 * 1 mod p and v mod l) and a permutation of coordinates with equal b_i.  Both
 * preserve (a)-(c) and commute with lifting.  Canonical form: lexicographic
 * minimum over v of (v e mod l), sorted inside each block of equal b_i.
 * Inside the DFS, coordinates that are equal (same b_i, same e_i) are lifted
 * with non-decreasing digits j_i, which loses nothing after canonicalisation.
 *
 * Pruning (sound): a branch is cut when some time m is good for every digit of
 * every remaining coordinate (it survives to every leaf, so every leaf has a
 * witness), or when the counting bound of liftfree.c fails.
 * Output: one JSON line per base: levels, retained orbits, DFS nodes, and the
 * level at which the retained set became empty (or null).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MAXK 24
#define MAXC 8
#define MAXSTEP 12
typedef unsigned char u8;

static int k, p, h, nchain, chain[MAXSTEP];
static long CAP = 2000000;
static unsigned long long NODECAP = ~0ULL;   /* env XC_NODECAP: per-step DFS node cap (then reported as capped) */
static int dumplevel = -1;
static int gcdi(int a, int b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { int t = a % b; a = b; b = t; } return a; }

/* ---------- hash set of k-byte keys ---------- */
typedef struct { u8 *keys; u8 *used; size_t cap, cnt; } hset;
static void hs_init(hset *s, size_t cap) { s->cap = cap; s->cnt = 0; s->keys = malloc(cap * k); s->used = calloc(cap, 1); }
static void hs_free(hset *s) { free(s->keys); free(s->used); }
static uint64_t hh(const u8 *t) { uint64_t x = 1469598103934665603ULL; for (int i = 0; i < k; i++) { x ^= t[i]; x *= 1099511628211ULL; } return x ^ (x >> 29); }
static int hs_add(hset *s, const u8 *t);
static void hs_grow(hset *s) {
    hset n; hs_init(&n, s->cap * 2);
    for (size_t i = 0; i < s->cap; i++) if (s->used[i]) hs_add(&n, s->keys + i * k);
    hs_free(s); *s = n;
}
static int hs_add(hset *s, const u8 *t) {
    if (2 * (s->cnt + 1) > s->cap) hs_grow(s);
    size_t i = hh(t) & (s->cap - 1);
    while (s->used[i]) { if (!memcmp(s->keys + i * k, t, k)) return 0; i = (i + 1) & (s->cap - 1); }
    s->used[i] = 1; memcpy(s->keys + i * k, t, k); s->cnt++; return 1;
}

/* ---------- per-level tables ---------- */
static int L, M, N, Wd;               /* new level L, old modulus M = l p, new modulus N = L p */
static uint64_t *G;                    /* G[x*Wd ..]: good-time bitset of residue x mod N */
static int units[4096], nu, divs[64], nd;
static int base[MAXK], blk[MAXK];      /* blk[i] = start index of i's block of equal b */
static int curw[MAXK], ce[MAXK], c;    /* parent tuple mod M; digits */
static int same[MAXK];                 /* same[i] = 1 if coordinate i equals i-1 in parent */
static uint64_t *alw;                  /* suffix AND of goods, (k+1) x Wd */
static uint64_t *accs;                 /* acc per depth, (k+1) x Wd */
static unsigned long long nodes, leaves, ngcd, nng, nwit;
static hset *out;

static void build_level(int lnew, int mold) {
    L = lnew; M = mold; N = L * p; Wd = (N + 63) / 64;
    free(G); G = calloc((size_t)N * Wd, 8);
    for (int x = 0; x < N; x++) {
        uint64_t *g = G + (size_t)x * Wd;
        for (int m = 1; m < N; m++) { long r = (long)m * x % N; long d = r < N - r ? r : N - r; if ((long)(k + 1) * d >= N) g[m >> 6] |= 1ULL << (m & 63); }
    }
    nu = 0; for (int v = 1; v <= L; v++) if (gcdi(v, L) == 1) units[nu++] = v % L;
    nd = 0; for (int d = 2; d <= L; d++) if (L % d == 0) divs[nd++] = d;
    free(alw); free(accs); alw = malloc((size_t)(k + 1) * Wd * 8); accs = malloc((size_t)(k + 1) * Wd * 8);
}

static int discard_e(const int *e) {   /* e = w mod L; returns 1 if gcd clause or Lemma S at some d | L */
    for (int i = 0; i < k; i++) { int g = L; for (int j = 0; j < k && g > 1; j++) if (j != i) g = gcdi(g, e[j]); if (g > 1) { ngcd++; return 1; } }
    for (int a = 0; a < nd; a++) {
        int d = divs[a], ne = 0; long cost = 0;
#ifndef BROKEN_NG
        for (int i = 0; i < k; i++) if (e[i] % d) { int g = gcdi(e[i], d); ne++; cost += (long)g * ((2L * d + (long)(k + 1) * g - 1) / ((long)(k + 1) * g)); }
#else   /* negative control for the tests: floor instead of ceiling (unsound) */
        for (int i = 0; i < k; i++) if (e[i] % d) { int g = gcdi(e[i], d); ne++; cost += (long)g * ((2L * d) / ((long)(k + 1) * g)); }
#endif
        if (ne >= 2 && cost < d) { nng++; return 1; }
    }
    return 0;
}
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
static void canon_e(const int *e, u8 *best) {
    int t[MAXK]; int have = 0;
    for (int a = 0; a < nu; a++) {
        int v = units[a];
        for (int i = 0; i < k; i++) t[i] = (int)((long)v * e[i] % L);
        for (int i = 0; i < k;) { int j = i; while (j < k && blk[j] == blk[i]) j++; qsort(t + i, j - i, sizeof(int), cmpi); i = j; }
        int lt = !have;
        for (int i = 0; have && i < k; i++) if (t[i] != best[i]) { lt = t[i] < best[i]; break; }
        if (lt) { for (int i = 0; i < k; i++) best[i] = (u8)t[i]; have = 1; }
    }
}
static void leaf(void) {
    int e[MAXK];
    leaves++;
    for (int i = 0; i < k; i++) e[i] = (int)(((long)curw[i] + (long)ce[i] * M) % L);
    if (discard_e(e)) return;
    u8 key[MAXK]; canon_e(e, key);
    hs_add(out, key);
}
static inline int popc(const uint64_t *a) { int s = 0; for (int i = 0; i < Wd; i++) s += __builtin_popcountll(a[i]); return s; }
static void dfs(int i) {
    nodes++;
    uint64_t *acc = accs + (size_t)i * Wd;
    int empty = 1, hitalw = 0;
    for (int x = 0; x < Wd; x++) { if (acc[x]) empty = 0; if (acc[x] & alw[(size_t)i * Wd + x]) hitalw = 1; }
    if (i == k) { if (empty) leaf(); else nwit++; return; }
    if (hitalw) return;
    if (!empty && k - i >= 2) {   /* counting bound */
        int n = popc(acc); long capb = 0;
        for (int t = i; t < k && capb < n; t++) {
            int best = 0;
            for (int j = 0; j < c; j++) {
                const uint64_t *g = G + (size_t)(((long)curw[t] + (long)j * M) % N) * Wd; int r = 0;
                for (int x = 0; x < Wd; x++) r += __builtin_popcountll(acc[x] & ~g[x]);
                if (r > best) best = r;
            }
            capb += best;
        }
        if (capb < n) return;
    }
    int j0 = (same[i] && i > 0) ? ce[i - 1] : 0;
    for (int j = j0; j < c; j++) {
        ce[i] = j;
        const uint64_t *g = G + (size_t)(((long)curw[i] + (long)j * M) % N) * Wd;
        uint64_t *nx = accs + (size_t)(i + 1) * Wd;
        for (int x = 0; x < Wd; x++) nx[x] = acc[x] & g[x];
        dfs(i + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: xcasc k p CHAIN [CAP] [DUMP_LEVEL] < bases\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); h = (p - 1) / 2;
    nchain = 0; for (char *s = argv[3]; *s;) { chain[nchain++] = (int)strtol(s, &s, 10); if (*s == ',') s++; }
    if (argc > 4) CAP = atol(argv[4]);
    if (argc > 5) dumplevel = atoi(argv[5]);
    if (getenv("XC_NODECAP")) NODECAP = strtoull(getenv("XC_NODECAP"), 0, 10);
    int lev[MAXSTEP + 1]; lev[0] = 1; for (int s = 0; s < nchain; s++) lev[s + 1] = lev[s] * chain[s];
    if (lev[nchain] > 255) { fprintf(stderr, "final level must be <= 255\n"); return 2; }
    /* precompute per-level tables lazily: one table set per step, rebuilt per base (cheap relative) is too slow,
       so keep all levels' G tables */
    uint64_t *Gs[MAXSTEP]; int Ws[MAXSTEP];
    int unitss[MAXSTEP][256], nus[MAXSTEP], divss[MAXSTEP][64], nds[MAXSTEP];
    for (int s = 0; s < nchain; s++) {
        G = NULL; alw = NULL; accs = NULL;
        build_level(lev[s + 1], lev[s] * p);
        Gs[s] = G; Ws[s] = Wd; nus[s] = nu; nds[s] = nd;
        memcpy(unitss[s], units, sizeof(int) * nu); memcpy(divss[s], divs, sizeof(int) * nd);
        free(alw); free(accs);
    }
    G = NULL;
    char line[4096]; long bidx = 0;
    while (fgets(line, sizeof line, stdin)) {
        int n = 0; char *s = line, *e2;
        for (;;) { long x = strtol(s, &e2, 10); if (e2 == s) break; if (n < MAXK) { long r = ((x % p) + p) % p; base[n++] = (int)(r <= h ? r : p - r); } s = e2; }
        if (n == 0) continue;
        if (n != k) { fprintf(stderr, "bad row\n"); return 1; }
        qsort(base, k, sizeof(int), cmpi);
        for (int i = 0; i < k; i++) blk[i] = (i > 0 && base[i] == base[i - 1]) ? blk[i - 1] : i;
        /* level-one witness check */
        int lvl1wit = 0;
        for (int m = 1; m < p && !lvl1wit; m++) { int ok = 1; for (int i = 0; i < k && ok; i++) { long r = (long)m * base[i] % p; long d = r < p - r ? r : p - r; if ((k + 1) * d < p) ok = 0; } if (ok) lvl1wit = 1; }
        clock_t t0 = clock();
        /* retained set at level 1: the single tuple e = () (all zero mod 1) */
        hset cur; hs_init(&cur, 16); { u8 z[MAXK] = {0}; hs_add(&cur, z); }
        int l = 1; int emptyat = -1, capped = 0, laststep = nchain - 1;
        long counts[MAXSTEP]; unsigned long long nds_[MAXSTEP];
        int done = 0;
        for (int st = 0; st < nchain && !done; st++) {
            c = chain[st];
            G = Gs[st]; Wd = Ws[st]; L = lev[st + 1]; M = l * p; N = L * p; nu = nus[st]; nd = nds[st];
            memcpy(units, unitss[st], sizeof(int) * nu); memcpy(divs, divss[st], sizeof(int) * nd);
            alw = malloc((size_t)(k + 1) * Wd * 8); accs = malloc((size_t)(k + 1) * Wd * 8);
            hset nxt; hs_init(&nxt, 1024); out = &nxt; int capflag = 0;
            nodes = 0;
            int pinv = 0; for (int x = 0; x < l; x++) if ((long)p * x % l == 1 % l) { pinv = x; break; }
            for (size_t q = 0; q < cur.cap; q++) {
                if (!cur.used[q]) continue;
                const u8 *ep = cur.keys + q * k;
                for (int i = 0; i < k; i++) {   /* CRT: w = b mod p, w = e mod l */
                    long t = ((long)ep[i] - base[i]) % l; if (t < 0) t += l;
                    curw[i] = (int)(base[i] + (long)p * ((t * pinv) % l));
                    same[i] = (i > 0 && blk[i] == blk[i - 1] && ep[i] == ep[i - 1]);
                }
                /* suffix AND of goods */
                uint64_t *a = alw + (size_t)k * Wd; for (int x = 0; x < Wd; x++) a[x] = ~0ULL;
                for (int i = k - 1; i >= 0; i--) {
                    uint64_t *ai = alw + (size_t)i * Wd, *an = alw + (size_t)(i + 1) * Wd;
                    for (int x = 0; x < Wd; x++) ai[x] = an[x];
                    for (int j = 0; j < c; j++) { const uint64_t *g = G + (size_t)(((long)curw[i] + (long)j * M) % N) * Wd; for (int x = 0; x < Wd; x++) ai[x] &= g[x]; }
                }
                uint64_t *a0 = accs; for (int x = 0; x < Wd; x++) a0[x] = 0;
                for (int m = 0; m < N; m++) a0[m >> 6] |= 1ULL << (m & 63);
                dfs(0);
                if ((long)nxt.cnt > CAP || nodes > NODECAP) { capflag = 1; break; }
            }
            free(alw); free(accs);
            l = L;
            counts[st] = (long)nxt.cnt; nds_[st] = nodes;
            if (dumplevel == L) {
                int pinv2 = 0; for (int x = 0; x < l; x++) if ((long)p * x % l == 1 % l) { pinv2 = x; break; }
                for (size_t q = 0; q < nxt.cap; q++) if (nxt.used[q]) {
                    printf("S %ld %d", bidx, L);
                    for (int i = 0; i < k; i++) { long t = ((long)nxt.keys[q * k + i] - base[i]) % l; if (t < 0) t += l; printf(" %ld", base[i] + (long)p * ((t * pinv2) % l)); }
                    printf("\n");
                }
            }
            hs_free(&cur); cur = nxt;
            if (capflag) { capped = 1; done = 1; }
            if (nxt.cnt == 0 && !capflag) { emptyat = L; done = 1; }
            if (done) { laststep = st; for (int z = st + 1; z < MAXSTEP; z++) counts[z] = -1; }
        }
        hs_free(&cur);
        double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("{\"idx\": %ld, \"base\": [", bidx);
        for (int i = 0; i < k; i++) printf(i ? ", %d" : "%d", base[i]);
        printf("], \"lvl1_witness\": %d, \"trace\": [", lvl1wit);
        int lv = 1, first = 1;
        for (int st = 0; st < nchain; st++) { lv *= chain[st]; if (counts[st] < 0) break; printf("%s[%d, %ld, %llu]", first ? "" : ", ", lv, counts[st], nds_[st]); first = 0; if (counts[st] == 0 || (capped && st == laststep)) break; }
        printf("], \"empty_at\": ");
        if (emptyat > 0) printf("%d", emptyat); else printf("null");
        printf(", \"capped\": %d, \"sec\": %.4f}\n", capped, secs);
        fflush(stdout);
        bidx++;
    }
    return 0;
}
