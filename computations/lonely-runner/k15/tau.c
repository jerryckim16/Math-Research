/* tau.c -- tau_k(p): the least number of folded speed classes that cover
 * every folded time class, for the k-speed cover relation of covergen.c:
 *   class v covers time a (1 <= a, v <= h = (p-1)/2) iff (k+1)*d_p(a v) < p.
 * A k-multiset lies in I(k,p,1) iff its support covers all h times.
 *
 * Why it matters (see notes/lonely-runner/gates.md): if tau_k(p) <= k-2 then
 * J(k,p) is non-empty (C-coordinates lifted to multiples of l, two free
 * coordinates equal to 1 defeat the gcd clause at every level l), so the gate
 * can only be used with a near-gcd lemma; tau_k(p) >= k-1 is necessary for
 * "J(k,p) = empty".
 *
 * Method: exhaustive DFS for a cover containing class 1 with at most s
 * classes (units map covers to covers, so a least cover can be scaled to
 * contain 1).  Branch on the uncovered time with fewest allowed coverers;
 * children in descending gain; earlier siblings excluded (complete for
 * covers containing 1: follow the first candidate lying in a given cover C,
 * the leaf is a cover inside C).  Cut: the (s-|L|) largest gains over the
 * allowed classes must sum to at least |U|.  Both rules remove only nodes
 * with no cover of size <= s below them.
 *
 * Extra cuts (env TAU_CUTS=1, default on; TAU_CUTS=0 for validation): a
 * least cover is MINIMAL, so it suffices to find minimal covers.
 *  (q) Lemma 4.1 of arXiv:2609.02604v2 (transcribed in the problem file,
 *      Approach 8): a cover by s' classes has a class with at least
 *      q_{s'} = ceil(max(0, 2h - s' m)/s') private times (m = floor((p-1)/(k+1))
 *      times per class); scaling that class to 1 keeps the cover minimal and
 *      its size.  q_{s'} >= q_lim for s' <= lim, and class 1's private set only
 *      shrinks as classes are added, so a node with priv(1) < q_lim is cut.
 *      (Normalising class 1 this way is compatible with the exclusion
 *      argument: we look for ONE minimal cover C containing 1 with
 *      priv_C(1) >= q_|C|, and every node on its path has priv(1) >= priv_C(1).)
 *  (r) along the path to a minimal C every chosen class keeps a private time
 *      (its private set w.r.t. a subset of C contains its private set w.r.t.
 *      C), so a node where some chosen class has no private time is cut.
 *
 * Usage: [TAU_FROM=s0] tau k p smax   (with TAU_FROM, only limits s0..smax
 *        are searched: a cover found then proves tau <= its size, but tau
 *        itself is only reported exactly when s0 = 1)  prints "k p h m tau T nodes N" where T is the least
 *        cover size if <= smax, else ">smax" (then no cover of size <= smax
 *        exists), and the cover found.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define MAXW 32
typedef struct { uint64_t w[MAXW]; } bs;
static int k, p, h, W, smax, maxcov;
static bs cov[2048];
static unsigned long long nodes;
static int L[64], nL, found[64], nfound = 0;
static inline int popand(const bs *a, const bs *b) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i] & b->w[i]); return s; }
static inline int popc(const bs *a) { int s = 0; for (int i = 0; i < W; i++) s += __builtin_popcountll(a->w[i]); return s; }
static inline int has(const bs *a, int x) { return (a->w[x >> 6] >> (x & 63)) & 1; }
static inline void clr(bs *a, int x) { a->w[x >> 6] &= ~(1ULL << (x & 63)); }
static int lim, cuts = 1, mcov, qlim;
static int qs(int s) { long t = 2L * h - (long)s * mcov; if (t <= 0) return 0; return (int)((t + s - 1) / s); }
/* cut (q) and (r): returns 1 if the node must be cut */
static int privcut(void) {
    for (int i = 0; i < nL; i++) {
        int c = 0;
        for (int w = 0; w < W; w++) {
            uint64_t x = cov[L[i]].w[w];
            for (int j = 0; j < nL; j++) if (j != i) x &= ~cov[L[j]].w[w];
            c += __builtin_popcountll(x);
        }
        if (c == 0) return 1;
        if (i == 0 && c < qlim) return 1;
    }
    return 0;
}
static int dfs(const bs *U, const bs *A) {
    nodes++;
    if (cuts && privcut()) return 0;
    int need = popc(U);
    if (need == 0) { nfound = nL; memcpy(found, L, nL * sizeof(int)); return 1; }
    int left = lim - nL;
    if (left <= 0) return 0;
    static int G[2048]; int gh[2049]; memset(gh, 0, sizeof(int) * (maxcov + 1));
    for (int c = 1; c <= h; c++) if (has(A, c)) { G[c] = popand(&cov[c], U); gh[G[c]]++; }
    long got = 0; int t = left;
    for (int g = maxcov; g > 0 && t > 0; g--) { int x = gh[g] < t ? gh[g] : t; got += (long)x * g; t -= x; }
    if (got < need) return 0;
    long bsum = 0; t = left - 1;
    for (int g = maxcov; g > 0 && t > 0; g--) { int x = gh[g] < t ? gh[g] : t; bsum += (long)x * g; t -= x; }
    int besta = -1, bestm = 1 << 30;
    for (int a = 1; a <= h; a++) if (has(U, a)) { int m = popand(&cov[a], A); if (m < bestm) { bestm = m; besta = a; } }
    if (bestm == 0) return 0;
    int ch[2048], cg[2048], n = 0;
    for (int c = 1; c <= h; c++) if (has(&cov[besta], c) && has(A, c)) { ch[n] = c; cg[n] = G[c]; n++; }
    for (int i = 1; i < n; i++) { int c = ch[i], g = cg[i], j = i - 1; while (j >= 0 && cg[j] < g) { ch[j+1] = ch[j]; cg[j+1] = cg[j]; j--; } ch[j+1] = c; cg[j+1] = g; }
    bs A2 = *A;
    for (int i = 0; i < n; i++) {
        if (cg[i] + bsum < need) break;      /* later siblings have smaller gain */
        int c = ch[i]; clr(&A2, c);
        bs U2; for (int w = 0; w < W; w++) U2.w[w] = U->w[w] & ~cov[c].w[w];
        L[nL++] = c;
        int r = dfs(&U2, &A2);
        nL--;
        if (r) return 1;
    }
    return 0;
}
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: tau k p smax\n"); return 2; }
    k = atoi(argv[1]); p = atoi(argv[2]); smax = atoi(argv[3]);
    h = (p - 1) / 2; W = (h + 1 + 63) / 64;
    if (h + 1 > 64 * MAXW || smax > 60) return 2;
    for (int v = 1; v <= h; v++) for (int a = 1; a <= h; a++) {
        long r = ((long)a * v) % p, d = r < p - r ? r : p - r;
        if ((long)(k + 1) * d < p) cov[v].w[a >> 6] |= 1ULL << (a & 63);
    }
    for (int v = 1; v <= h; v++) { int c = popc(&cov[v]); if (c > maxcov) maxcov = c; }
    bs U, A; memset(&U, 0, sizeof U); memset(&A, 0, sizeof A);
    for (int a = 1; a <= h; a++) { U.w[a >> 6] |= 1ULL << (a & 63); A.w[a >> 6] |= 1ULL << (a & 63); }
    for (int w = 0; w < W; w++) U.w[w] &= ~cov[1].w[w];
    clr(&A, 1);
    if (getenv("TAU_CUTS")) cuts = atoi(getenv("TAU_CUTS"));
    mcov = (p - 1) / (k + 1);
    int tau = -1;
    int from = getenv("TAU_FROM") ? atoi(getenv("TAU_FROM")) : 1;   /* screening: search only sizes >= from */
    for (lim = from; lim <= smax; lim++) { qlim = qs(lim); L[0] = 1; nL = 1; if (dfs(&U, &A)) { tau = lim; break; } }
    if (tau > 0) { printf("k %d p %d h %d m %d tau %d nodes %llu cover", k, p, h, (p - 1) / (k + 1), tau, nodes); for (int i = 0; i < nfound; i++) printf(" %d", found[i]); printf("\n"); }
    else printf("k %d p %d h %d m %d tau >%d nodes %llu\n", k, p, h, (p - 1) / (k + 1), smax, nodes);
    return 0;
}
