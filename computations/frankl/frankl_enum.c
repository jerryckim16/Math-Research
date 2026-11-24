/*
 * Exhaustive check of Frankl's union-closed sets conjecture on universe [n],
 * n <= 6, with exact labeled counts.
 *
 * Objects: union-closed families F of subsets of [n] = {0..n-1} with the empty
 * set in F.  (Enough: if F is union-closed and F != {}, {{}} then F u {{}} is
 * union-closed, and an element in half of F u {{}} is in half of F.)  These are
 * exactly the complements of Moore families on [n]; their labeled numbers are
 * 2, 7, 61, 2480, 1385552, 75973751474 for n = 1..6 (Brinkmann-Deklerck,
 * arXiv:1701.03751, Table 2; Colomb-Irlande-Raynaud).
 *
 * Decomposition on the last element k = n-1:
 *   F0 = {A in F : k notin A},  F1 = {A \ {k} : k in A in F}.
 * F is union-closed with {} in F  <=>  F0 union-closed with {} in F0,
 * F1 union-closed (possibly empty) and a u B in F1 for a in F0, B in F1.
 * Frequencies: f_j(F) = f_j(F0) + f_j(F1) for j < k, f_k(F) = |F1|.
 *
 * Symmetry: S_k acts on [k]; the property "F satisfies Frankl" and all counts
 * are invariant, so we enumerate F0 only up to S_k (canonical = numerically
 * smallest image of the family bitmask) and weight by the orbit size.
 *
 * F1 enumeration: depth-first over subsets s of [k] in DECREASING numeric
 * order.  The chosen part P (subsets > s) is always closed, because s|t >= s.
 * Including s is allowed iff {s|T : T in P} and {s|a : a in F0} \ {s} lie in P.
 * Each admissible F1 is produced exactly once.
 *
 * Usage: frankl_enum n [part nparts]
 * Output: one line of totals (summable over parts).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;

static int k;          /* size of the base universe [k], k = n-1 */
static int NS;         /* 2^k subsets */
static u64 MASKJ[8];   /* MASKJ[j]: family-mask of subsets containing j */
static u64 FULL;

/* {s | T : T in M} as a family mask */
static inline u64 join_set(int s, u64 M) {
    for (int j = 0; j < k; j++)
        if (s >> j & 1) {
            u64 with = M & MASKJ[j], without = M & ~MASKJ[j];
            M = with | (without << (1u << j));
        }
    return M;
}

/* ------------------------------------------------------------ F0 = context */
static u64 F0;
static int f0size, f0freq[8];
static u64 up0[64];    /* {s | a : a in F0} minus s */

/* accumulators (weighted) */
static u64 w_cur;
static unsigned __int128 tot, totfull, tight, fail;
static u64 leaves_unweighted;

static void leaf(u64 F1) {
    int s1 = __builtin_popcountll(F1);
    int size = f0size + s1;
    leaves_unweighted++;
    tot += w_cur;
    /* universe = [n] iff F1 nonempty (k used) and every j<k used */
    int full = (s1 > 0);
    int best = s1;               /* frequency of element k */
    for (int j = 0; j < k; j++) {
        int f = f0freq[j] + __builtin_popcountll(F1 & MASKJ[j]);
        if (f == 0) full = 0;
        if (f > best) best = f;
    }
    if (full) totfull += w_cur;
    if (size >= 2) {             /* F != {{}} */
        if (2 * best < size) {
            fail += w_cur;
            fprintf(stderr, "COUNTEREXAMPLE F0=%llx F1=%llx\n",
                    (unsigned long long)F0, (unsigned long long)F1);
        } else if (2 * best == size) tight += w_cur;
    }
}

static void dfs(int s, u64 P) {
    if (s < 0) { leaf(P); return; }
    /* exclude s */
    dfs(s - 1, P);
    /* include s */
    u64 need = join_set(s, P) | up0[s];
    need &= ~(1ULL << s);
    if ((need & ~P) == 0) dfs(s - 1, P | (1ULL << s));
}

/* --------------------------------------------- enumerate families on [k] */
/* union-closed families on [k] containing {} via the same dfs with F0={{}} */
static u64 *fam; static size_t nfam, capfam;
static void collect(int s, u64 P) {
    if (s < 0) {
        if (P & 1ULL) {          /* contains the empty set (subset 0) */
            if (nfam == capfam) { capfam = capfam ? 2 * capfam : 1024; fam = realloc(fam, capfam * sizeof(u64)); }
            fam[nfam++] = P;
        }
        return;
    }
    collect(s - 1, P);
    u64 need = join_set(s, P) & ~(1ULL << s);
    if ((need & ~P) == 0) collect(s - 1, P | (1ULL << s));
}

static int nperm; static unsigned char perms[720][64];
static void gen_perms(void) {
    int p[8]; for (int i = 0; i < k; i++) p[i] = i;
    /* Heap-free: iterate all permutations lexicographically */
    nperm = 0;
    for (;;) {
        for (int s = 0; s < NS; s++) {
            int t = 0;
            for (int j = 0; j < k; j++) if (s >> j & 1) t |= 1 << p[j];
            perms[nperm][s] = (unsigned char)t;
        }
        nperm++;
        int i = k - 2; while (i >= 0 && p[i] > p[i + 1]) i--;
        if (i < 0) break;
        int j = k - 1; while (p[j] < p[i]) j--;
        int tmp = p[i]; p[i] = p[j]; p[j] = tmp;
        for (int a = i + 1, b = k - 1; a < b; a++, b--) { tmp = p[a]; p[a] = p[b]; p[b] = tmp; }
    }
}
static u64 apply_perm(int pi, u64 M) {
    u64 R = 0;
    while (M) { int s = __builtin_ctzll(M); M &= M - 1; R |= 1ULL << perms[pi][s]; }
    return R;
}

static void print128(const char *name, unsigned __int128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    if (v == 0) buf[--i] = '0';
    while (v) { buf[--i] = '0' + (int)(v % 10); v /= 10; }
    printf(" %s=%s", name, buf + i);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s n [part nparts]\n", argv[0]); return 1; }
    int n = atoi(argv[1]);
    int part = argc > 3 ? atoi(argv[2]) : 0, nparts = argc > 3 ? atoi(argv[3]) : 1;
    if (n < 1 || n > 7) { fprintf(stderr, "n out of range\n"); return 1; }
    k = n - 1; NS = 1 << k;
    FULL = (NS == 64) ? ~0ULL : ((1ULL << NS) - 1);
    for (int j = 0; j < k; j++) { MASKJ[j] = 0; for (int s = 0; s < NS; s++) if (s >> j & 1) MASKJ[j] |= 1ULL << s; }

    /* all labeled families on [k] containing {} */
    collect(NS - 1, 0);
    gen_perms();
    long long fact = 1; for (int i = 2; i <= k; i++) fact *= i;
    if (fact != nperm) { fprintf(stderr, "perm bug\n"); return 1; }

    /* canonical representatives with orbit sizes */
    size_t nrep = 0; unsigned long long orbitsum = 0;
    u64 *rep = malloc(nfam * sizeof(u64)); u64 *wt = malloc(nfam * sizeof(u64));
    for (size_t i = 0; i < nfam; i++) {
        u64 M = fam[i]; int canon = 1, stab = 0;
        for (int p = 0; p < nperm; p++) {
            u64 R = apply_perm(p, M);
            if (R < M) { canon = 0; break; }
            if (R == M) stab++;
        }
        if (canon) { rep[nrep] = M; wt[nrep] = (u64)(nperm / stab); orbitsum += wt[nrep]; nrep++; }
    }
    fprintf(stderr, "n=%d: base [k=%d]: %zu labeled families, %zu classes, orbit-sum %llu\n",
            n, k, nfam, nrep, orbitsum);

    for (size_t r = 0; r < nrep; r++) {
        if ((int)(r % nparts) != part) continue;
        F0 = rep[r]; w_cur = wt[r];
        f0size = __builtin_popcountll(F0);
        for (int j = 0; j < k; j++) f0freq[j] = __builtin_popcountll(F0 & MASKJ[j]);
        for (int s = 0; s < NS; s++) up0[s] = join_set(s, F0) & ~(1ULL << s);
        dfs(NS - 1, 0);
    }
    printf("n=%d part=%d/%d base_labeled=%zu base_classes=%zu leaves=%llu",
           n, part, nparts, nfam, nrep, (unsigned long long)leaves_unweighted);
    print128("labeled_total", tot);
    print128("labeled_fulluniverse", totfull);
    print128("tight", tight);
    print128("counterexamples", fail);
    printf("\n");
    return fail ? 2 : 0;
}
