/*
 * matchcrit.c -- the matching criterion of general-n-explicit.md, Lemma C.
 *
 * For n >= 1 and n+1 <= M <= 2n let A = floor(M/2) and let G(n,M) be the
 * bipartite graph with left side [1,A], right side [n+2, 2n+2] and edges
 *   (a) s -- t  when gcd(s,t) = 1 and M < s+t <= 2n+2;
 *   (b) s -- 2s when s >= 2, 3s > M and 2s >= n+2.
 * Lemma C: if G(n,M) has a matching that saturates [1,A], then every set of
 * n distinct positive integers with maximum M is lonely.  Lemma C' (monotone):
 * a saturating matching for M gives one for every M' in [n+1, M].
 *
 * Exact integer arithmetic throughout.  Matching: Hopcroft-Karp.
 *
 * Usage:
 *   matchcrit scan N1 N2           for n = N1..N2 print "n Mstar fstar",
 *                                  Mstar = largest M <= 2n with a saturating
 *                                  matching (found by descending from 2n),
 *                                  fstar = 2n - Mstar.  Mstar = 0 if none.
 *   matchcrit test n M             print "n M OK" or "n M FAIL deficit=d"
 *   matchcrit cert n M             print the matching, one line "s t" per s
 *   matchcrit fixed F N1 N2        for n = N1..N2 test M = 2n - F, print
 *                                  failures and a summary line
 *   matchcrit alpha P Q N1 N2      for n = N1..N2 test M = floor(P n / Q)
 *                                  (only if that is >= n+1), print failures
 *                                  and a final summary line
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }

/* graph storage (CSR) */
static long *adjstart, *adj;
static long nleft, nright;          /* left vertices 1..nleft, right 0..nright-1 */
static long *matchL, *matchR, *dist, *queue, *itp;

static int build(long n, long M) {
    long A = M / 2, R0 = n + 2;
    nleft = A; nright = n + 1;      /* right vertex t <-> index t - R0 */
    long cap = 16, cnt = 0;
    free(adjstart); free(adj);
    adjstart = malloc(sizeof(long) * (A + 2));
    adj = malloc(sizeof(long) * cap);
    for (long s = 1; s <= A; s++) {
        adjstart[s] = cnt;
        long lo = M + 1 - s; if (lo < R0) lo = R0;
        long hi = 2 * n + 2 - s;
        for (long t = hi; t >= lo; t--) {   /* larger t first */
            if (gcdl(s, t) == 1) {
                if (cnt == cap) { cap *= 2; adj = realloc(adj, sizeof(long) * cap); }
                adj[cnt++] = t - R0;
            }
        }
        if (s >= 2 && 3 * s > M && 2 * s >= R0 && !(2 * s >= lo && 2 * s <= hi && gcdl(s, 2 * s) == 1)) {
            if (cnt == cap) { cap *= 2; adj = realloc(adj, sizeof(long) * cap); }
            adj[cnt++] = 2 * s - R0;
        }
    }
    adjstart[A + 1] = cnt;
    return 0;
}

#define INF 0x3fffffffffffffffL

static int bfs(void) {
    long qh = 0, qt = 0; int found = 0;
    for (long u = 1; u <= nleft; u++) {
        if (matchL[u] < 0) { dist[u] = 0; queue[qt++] = u; } else dist[u] = INF;
    }
    while (qh < qt) {
        long u = queue[qh++];
        for (long e = adjstart[u]; e < adjstart[u + 1]; e++) {
            long v = adj[e], w = matchR[v];
            if (w < 0) found = 1;
            else if (dist[w] == INF) { dist[w] = dist[u] + 1; queue[qt++] = w; }
        }
    }
    return found;
}

/* iterative DFS along the layered graph */
static long *stk;
static int dfs(long root) {
    long sp = 0; stk[sp++] = root;
    while (sp > 0) {
        long u = stk[sp - 1];
        if (itp[u] >= adjstart[u + 1]) { dist[u] = INF; sp--; continue; }
        long v = adj[itp[u]], w = matchR[v];
        if (w < 0) {
            /* augment along the stack */
            for (long i = sp - 1; i >= 0; i--) {
                long uu = stk[i], vv = adj[itp[uu]];
                long prev = matchL[uu];
                matchL[uu] = vv; matchR[vv] = uu;
                (void)prev;
            }
            return 1;
        }
        if (dist[w] == dist[u] + 1) { stk[sp++] = w; continue; }
        itp[u]++;
    }
    return 0;
}

/* returns size of a maximum matching */
static long hk(void) {
    matchL = realloc(matchL, sizeof(long) * (nleft + 2));
    matchR = realloc(matchR, sizeof(long) * (nright + 2));
    dist = realloc(dist, sizeof(long) * (nleft + 2));
    queue = realloc(queue, sizeof(long) * (nleft + 2));
    itp = realloc(itp, sizeof(long) * (nleft + 2));
    stk = realloc(stk, sizeof(long) * (nleft + 2));
    for (long u = 0; u <= nleft; u++) matchL[u] = -1;
    for (long v = 0; v <= nright; v++) matchR[v] = -1;
    long size = 0;
    /* greedy start */
    for (long u = 1; u <= nleft; u++)
        for (long e = adjstart[u]; e < adjstart[u + 1]; e++)
            if (matchR[adj[e]] < 0) { matchR[adj[e]] = u; matchL[u] = adj[e]; size++; break; }
    while (bfs()) {
        for (long u = 1; u <= nleft; u++) itp[u] = adjstart[u];
        for (long u = 1; u <= nleft; u++)
            if (matchL[u] < 0 && dfs(u)) size++;
    }
    return size;
}

static long test(long n, long M) {   /* returns deficit (0 = saturating matching) */
    build(n, M);
    return nleft - hk();
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: see header\n"); return 2; }
    if (!strcmp(argv[1], "scan") && argc == 4) {
        long a = atol(argv[2]), b = atol(argv[3]);
        for (long n = a; n <= b; n++) {
            long Ms = 0;
            for (long M = 2 * n; M >= n + 1; M--) if (test(n, M) == 0) { Ms = M; break; }
            printf("%ld %ld %ld\n", n, Ms, Ms ? 2 * n - Ms : -1);
            fflush(stdout);
        }
        return 0;
    }
    if (!strcmp(argv[1], "test") && argc == 4) {
        long n = atol(argv[2]), M = atol(argv[3]);
        if (M < n + 1 || M > 2 * n) { fprintf(stderr, "need n+1 <= M <= 2n\n"); return 2; }
        long d = test(n, M);
        if (d == 0) printf("%ld %ld OK\n", n, M); else printf("%ld %ld FAIL deficit=%ld\n", n, M, d);
        return 0;
    }
    if (!strcmp(argv[1], "cert") && argc == 4) {
        long n = atol(argv[2]), M = atol(argv[3]);
        if (M < n + 1 || M > 2 * n) { fprintf(stderr, "need n+1 <= M <= 2n\n"); return 2; }
        long d = test(n, M);
        printf("# n=%ld M=%ld deficit=%ld\n", n, M, d);
        for (long s = 1; s <= nleft; s++) printf("%ld %ld\n", s, matchL[s] < 0 ? -1 : matchL[s] + n + 2);
        return 0;
    }
    if (!strcmp(argv[1], "alpha") && argc == 6) {
        long P = atol(argv[2]), Q = atol(argv[3]), a = atol(argv[4]), b = atol(argv[5]);
        long fails = 0, tested = 0;
        for (long n = a; n <= b; n++) {
            long M = (P * n) / Q;
            if (M > 2 * n) M = 2 * n;
            if (M < n + 1) continue;
            tested++;
            long d = test(n, M);
            if (d) { fails++; printf("FAIL n=%ld M=%ld deficit=%ld\n", n, M, d); fflush(stdout); }
        }
        printf("SUMMARY P=%ld Q=%ld n=%ld..%ld tested=%ld fails=%ld\n", P, Q, a, b, tested, fails);
        return 0;
    }
    if (!strcmp(argv[1], "fixed") && argc == 5) {
        long F = atol(argv[2]), a = atol(argv[3]), b = atol(argv[4]);
        long fails = 0, tested = 0;
        for (long n = a; n <= b; n++) {
            long M = 2 * n - F;
            if (M < n + 1) continue;
            tested++;
            long d = test(n, M);
            if (d) { fails++; printf("FAIL n=%ld M=%ld deficit=%ld\n", n, M, d); fflush(stdout); }
        }
        printf("SUMMARY F=%ld n=%ld..%ld tested=%ld fails=%ld\n", F, a, b, tested, fails);
        return 0;
    }
    fprintf(stderr, "bad arguments\n");
    return 2;
}
