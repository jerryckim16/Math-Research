/* Complete ternary-section census for one greedy support profile of odd
 * relation rank R (compile with -DR=5; R = 3, 4 for validation), general n,
 * with an optional cap AMAX on the support a = sum m.
 *
 * Same method, tests and output format as ../rank4/sect.c (read its header
 * for the setting: sections T(O), the no-short-line test, signed Riesz,
 * greedy consistency, saturated Gram), and the same row-sign symmetry
 * quotient and rigorous Riesz pruning.  The one change is how section
 * candidates are produced: instead of a global list of M^{-1} x over all
 * R-subsets of the (3^R-1)/2 types (2*10^8 subsets at R = 5), the candidates
 * are generated at the DFS node where the present types first reach rank R:
 * if c_1..c_R are the first R present types that increase the rank (rows of
 * an invertible M), every section element lambda satisfies M lambda = x with
 * x ternary, so the section is contained in the (3^R-1)/2 vectors
 * lambda = adj(M) x / det M (mod sign).  These are filtered by every present
 * type and carried down the DFS as before.  Before rank R is reached no
 * candidate list exists and no Riesz pruning is done (the domain there is
 * small because a <= AMAX).
 *
 * Usage: sectn n PLO PHI QD REJ AMAX s_1 ... s_R [shard nshard]
 * Env:   NOPRUNE, NOSYM, NOGREEDY as in sect.c.
 * Output: TYPES line, ADM lines (same fields as sect.c), SUMMARY, ORBITSUM, MAXS.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifndef R
#define R 5
#endif
#define MAXT 121
#define MAXC 122                 /* candidates per node: (3^R - 1)/2 <= 121 */
#ifndef PRUNE_MAX
#define PRUNE_MAX 121
#endif

typedef long long ll;
typedef __int128 i128;

static int NT;
static int T[MAXT][R];
static int nn, REJ, AMAX, prof[R];
static ll PLO, PHI, QD;

static ll gcdl(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

#define NG (1 << (R - 1))
static int img[NG][MAXT];
static int blk_end[MAXT + 1];
static int SYM = 1, GREEDY = 1, PRUNE = 1;
static int pattern(const int *t) { int p = 0; for (int i = 0; i < R; i++) if (t[i]) p |= 1 << i; return p; }

static void make_types(void) {
    int t[R], tot = 1;
    for (int i = 0; i < R; i++) tot *= 3;
    NT = 0;
    for (int code = 0; code < tot; code++) {
        int c = code, first = 0;
        for (int i = 0; i < R; i++) { t[i] = c % 3 - 1; c /= 3; }
        for (int i = 0; i < R; i++) if (t[i]) { first = t[i]; break; }
        if (first <= 0) continue;
        memcpy(T[NT++], t, sizeof t);
    }
    /* lexicographic, then stable by pattern: identical order to sect.c */
    for (int i = 0; i < NT; i++)
        for (int j = i + 1; j < NT; j++)
            if (memcmp(T[j], T[i], sizeof T[i]) < 0) { int tmp[R]; memcpy(tmp, T[i], sizeof tmp); memcpy(T[i], T[j], sizeof tmp); memcpy(T[j], tmp, sizeof tmp); }
    for (int i = 0; i < NT; i++)
        for (int j = i + 1; j < NT; j++)
            if (pattern(T[j]) < pattern(T[i]) || (pattern(T[j]) == pattern(T[i]) && memcmp(T[j], T[i], sizeof T[i]) < 0)) {
                int tmp[R]; memcpy(tmp, T[i], sizeof tmp); memcpy(T[i], T[j], sizeof tmp); memcpy(T[j], tmp, sizeof tmp);
            }
    for (int k = 0; k <= NT; k++) blk_end[k] = (k == 0) || k == NT || pattern(T[k]) != pattern(T[k - 1]);
    for (int g = 0; g < NG; g++)
        for (int k = 0; k < NT; k++) {
            int u[R], f = 0;
            for (int i = 0; i < R; i++) u[i] = ((i > 0 && ((g >> (i - 1)) & 1)) ? -1 : 1) * T[k][i];
            for (int i = 0; i < R; i++) if (u[i]) { f = u[i]; break; }
            if (f < 0) for (int i = 0; i < R; i++) u[i] = -u[i];
            int found = -1;
            for (int q = 0; q < NT; q++) if (memcmp(T[q], u, sizeof u) == 0) found = q;
            if (found < 0 || pattern(T[found]) != pattern(T[k])) { fprintf(stderr, "img error\n"); exit(6); }
            img[g][k] = found;
        }
}

static ll detR(ll M[R][R]) {          /* Bareiss, exact */
    ll A[R][R]; memcpy(A, M, sizeof A);
    ll prev = 1; int sign = 1;
    for (int k = 0; k < R - 1; k++) {
        int p = k;
        while (p < R && A[p][k] == 0) p++;
        if (p == R) return 0;
        if (p != k) { for (int j = 0; j < R; j++) { ll t = A[k][j]; A[k][j] = A[p][j]; A[p][j] = t; } sign = -sign; }
        for (int i = k + 1; i < R; i++)
            for (int j = k + 1; j < R; j++)
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) / prev;
        prev = A[k][k];
    }
    return sign * A[R - 1][R - 1];
}

static void adjR(ll M[R][R], ll adj[R][R]) {
    for (int i = 0; i < R; i++)
        for (int j = 0; j < R; j++) {
            ll S[R][R]; memset(S, 0, sizeof S);
            int ri = 0;
            for (int a = 0; a < R; a++) {
                if (a == j) continue;
                int ci = 0;
                for (int b = 0; b < R; b++) { if (b == i) continue; S[ri][ci++] = M[a][b]; }
                ri++;
            }
            S[R - 1][R - 1] = 1;
            ll d = detR(S);
            adj[i][j] = ((i + j) & 1) ? -d : d;
        }
}

/* incremental echelon rank */
typedef struct { ll b[R][R]; int nb; } Ech;
static int ech_add(Ech *e, const int *y) {
    ll v[R];
    for (int i = 0; i < R; i++) v[i] = y[i];
    for (int b = 0; b < e->nb; b++) {
        int p = 0; while (e->b[b][p] == 0) p++;
        if (v[p]) {
            ll a = e->b[b][p], c = v[p], g = 0;
            for (int i = 0; i < R; i++) { v[i] = v[i] * a - e->b[b][i] * c; g = gcdl(g, v[i]); }
            if (g > 1) for (int i = 0; i < R; i++) v[i] /= g;
        }
    }
    int nz = 0; for (int i = 0; i < R; i++) if (v[i]) nz = 1;
    if (!nz) return 0;
    int p = 0; while (v[p] == 0) p++;
    int pos = e->nb;
    for (int b = 0; b < e->nb; b++) { int q = 0; while (e->b[b][q] == 0) q++; if (q > p) { pos = b; break; } }
    for (int b = e->nb; b > pos; b--) memcpy(e->b[b], e->b[b - 1], sizeof e->b[0]);
    memcpy(e->b[pos], v, sizeof v);
    e->nb++;
    return 1;
}

/* candidate: lambda = y / D, normalised (gcd 1, D > 0, first nonzero y > 0) */
typedef struct { int y[R]; int D; int sup; } Cand;

static int m[MAXT];
static Cand cbuf[MAXT + 2][MAXC];              /* storage for lists created at depth k */
static Cand *cl[MAXT + 2];                     /* list in force at depth k (shared when m_k = 0) */
static int ccount[MAXT + 2], have[MAXT + 2];   /* have[k]: candidate list exists at depth k */
typedef struct { Ech e; int bt[R]; } RS;       /* echelon state + types that raised the rank */
static RS rsbuf[MAXT + 2];
static RS *rs[MAXT + 2];
static ll pow2[64];
static ll leaves, n_rank_def, n_short, n_riesz_fail, n_greedy_fail, n_adm, n_pruned, n_gen;
static ll shard = 0, nshard = 1, prefix_ord = 0;
#define SHARD_DEPTH 4
static int cur_orbit = 1; static ll orbit_leaves = 0;
static int have_max = 0; static i128 best_flo, bestA, bestB;
static int oddceil(int s) { return (s & 1) ? s : s + 1; }
static int need[R], lastnz[R];

static int excluded_AB(i128 A, i128 B) {
    i128 base = pow2[nn - 1];
    i128 flo = (i128)PLO * (A - base) + (i128)QD * B;
    i128 fhi = (i128)PHI * (A - base) + (i128)QD * B;
    return flo < 0 && fhi < 0;
}

static void normalise(int *y, int *D) {
    ll g = *D;
    for (int i = 0; i < R; i++) g = gcdl(g, y[i]);
    for (int i = 0; i < R; i++) y[i] /= (int)g;
    *D /= (int)g;
    if (*D < 0) { *D = -*D; for (int i = 0; i < R; i++) y[i] = -y[i]; }
    int f = 0;
    for (int i = 0; i < R; i++) if (y[i]) { f = y[i]; break; }
    if (f < 0) for (int i = 0; i < R; i++) y[i] = -y[i];
}

/* generate the candidate list at depth k+1 from the R basis types, filtered by
   all present types 0..k (multiplicities m[]) */
static void generate(int kd) {
    ll M[R][R], adj[R][R];
    for (int a = 0; a < R; a++) for (int b = 0; b < R; b++) M[a][b] = T[rs[kd]->bt[a]][b];
    ll D = detR(M);
    if (!D) { fprintf(stderr, "singular basis\n"); exit(7); }
    adjR(M, adj);
    int tot = 1; for (int i = 0; i < R; i++) tot *= 3;
    int nc = 0;
    for (int code = 0; code < tot; code++) {
        int x[R], c = code, first = 0;
        for (int i = 0; i < R; i++) { x[i] = c % 3 - 1; c /= 3; }
        for (int i = 0; i < R; i++) if (x[i]) { first = x[i]; break; }
        if (first <= 0) continue;                 /* one of each +-x pair */
        int y[R]; int Dn = (int)D;
        for (int i = 0; i < R; i++) { ll s = 0; for (int j = 0; j < R; j++) s += adj[i][j] * x[j]; y[i] = (int)s; }
        normalise(y, &Dn);
        int ok = 1, sup = 0;
        for (int t = 0; t < kd && ok; t++) if (m[t]) {
            int s = 0;
            for (int i = 0; i < R; i++) s += y[i] * T[t][i];
            if (s != 0 && s != Dn && s != -Dn) ok = 0;
            else if (s) sup += m[t];
        }
        if (!ok) continue;
        Cand *cd = &cbuf[kd][nc++];
        memcpy(cd->y, y, sizeof y); cd->D = Dn; cd->sup = sup;
    }
    cl[kd] = cbuf[kd]; ccount[kd] = nc; have[kd] = 1; n_gen++;
}

static int prune_ub(int k) {
    i128 A = 0, B = 0;
    for (int i = 0; i < ccount[k]; i++) {
        int s = cl[k][i].sup;
        if (s < prof[0]) s = prof[0];
        s = oddceil(s);
        if (s > nn) continue;
        A += pow2[nn - s];
        B += (i128)s * pow2[nn - s];
    }
    return excluded_AB(A, B);
}

static int present[MAXT], np;

static void leaf(int K) {
    leaves++; orbit_leaves += cur_orbit;
    if (!have[K]) { n_rank_def++; return; }
    int c = ccount[K];
    Cand *L = cl[K];
    for (int i = 0; i < c; i++) if (L[i].sup == 0) { fprintf(stderr, "support-0 line in full-rank leaf\n"); exit(5); }
    for (int i = 0; i < c; i++) if (L[i].sup <= REJ) { n_short++; return; }
    i128 A = 0, B = 0;
    for (int i = 0; i < c; i++) {
        int s = L[i].sup; ll w = pow2[nn - s];
        if (s & 1) { A += w; B += (i128)s * w; } else { A -= w; B -= (i128)s * w; }
    }
    {
        i128 base = pow2[nn - 1];
        i128 flo = (i128)PLO * (A - base) + (i128)QD * B;
        if (!have_max || flo > best_flo) { have_max = 1; best_flo = flo; bestA = A; bestB = B; }
    }
    if (excluded_AB(A, B)) { n_riesz_fail++; return; }
    int ord[MAXC]; int no = 0;
    for (int i = 0; i < c; i++) if (L[i].sup & 1) ord[no++] = i;
    for (int i = 1; i < no; i++) { int x = ord[i], j = i - 1; while (j >= 0 && L[ord[j]].sup > L[x].sup) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = x; }
    Ech e; e.nb = 0; int gs[R];
    for (int i = 0; i < no && e.nb < R; i++) {
        int before = e.nb;
        ech_add(&e, L[ord[i]].y);
        if (e.nb > before) gs[before] = L[ord[i]].sup;
    }
    int ok = (e.nb == R) || !GREEDY;
    for (int i = 0; ok && GREEDY && i < R; i++) if (gs[i] != prof[i]) ok = 0;
    if (!ok) { n_greedy_fail++; return; }
    ll G[R][R]; memset(G, 0, sizeof G);
    np = 0; int a = 0;
    for (int k = 0; k < NT; k++) if (m[k]) {
        present[np++] = k; a += m[k];
        for (int i = 0; i < R; i++) for (int j = 0; j < R; j++) G[i][j] += (ll)m[k] * T[k][i] * T[k][j];
    }
    ll gram = detR(G), idx = 0;
    int id[R]; for (int i = 0; i < R; i++) id[i] = i;
    if (np >= R) while (1) {
        ll M[R][R];
        for (int i = 0; i < R; i++) for (int j = 0; j < R; j++) M[i][j] = T[present[id[i]]][j];
        idx = gcdl(idx, detR(M));
        int kk = R - 1;
        while (kk >= 0 && id[kk] == np - R + kk) kk--;
        if (kk < 0) break;
        id[kk]++;
        for (int j = kk + 1; j < R; j++) id[j] = id[j - 1] + 1;
    }
    if (idx == 0 || gram % (idx * idx)) { fprintf(stderr, "index error\n"); exit(4); }
    ll g = gram / (idx * idx);
    n_adm++;
    printf("ADM a=%d g=%lld idx=%lld raw=%lld lines=%d A=%lld B=%lld orb=%d m=", a, g, idx, gram, c, (ll)A, (ll)B, cur_orbit);
    for (int k = 0; k < NT; k++) printf("%d%c", m[k], k + 1 < NT ? ',' : '\n');
}

static void dfs(int k, int rem, unsigned tied) {
    if (SYM && blk_end[k] && k > 0) {
        int b0 = k - 1;
        while (b0 > 0 && !blk_end[b0]) b0--;
        unsigned nt = tied;
        for (int g = 1; g < NG; g++) if ((tied >> g) & 1) {
            for (int q = b0; q < k; q++) {
                int gm = m[img[g][q]];
                if (gm < m[q]) return;
                if (gm > m[q]) { nt &= ~(1u << g); break; }
            }
        }
        tied = nt;
    }
    if (k == SHARD_DEPTH) {
        ll o = prefix_ord++;
        if (o % nshard != shard) return;
    }
    if (k == NT) {
        for (int i = 0; i < R; i++) if (need[i]) return;
        cur_orbit = SYM ? NG / (1 + __builtin_popcount(tied)) : 1;
        leaf(k);
        return;
    }
    int mx = 0;
    for (int i = 0; i < R; i++) if (need[i] > mx) mx = need[i];
    if (mx > rem) return;
    for (int i = 0; i < R; i++) if (need[i] && k > lastnz[i]) return;
    if (PRUNE && GREEDY && have[k] && ccount[k] <= PRUNE_MAX && prune_ub(k)) { n_pruned++; return; }
    /* m_k = 0: pass state down unchanged (shared pointers) */
    m[k] = 0;
    have[k + 1] = have[k]; ccount[k + 1] = ccount[k]; cl[k + 1] = cl[k]; rs[k + 1] = rs[k];
    dfs(k + 1, rem, tied);
    /* m_k >= 1 */
    int cap = rem;
    for (int i = 0; i < R; i++) if (T[k][i] && need[i] < cap) cap = need[i];
    if (cap < 1) return;
    /* the filtered list and the rank state do not depend on v >= 1, except supports */
    int had = have[k], nc = 0, gen = 0;
    RS *rnew = rs[k];
    static int sflag[MAXT + 2][MAXC];
    if (!had) {
        rsbuf[k + 1] = *rs[k];
        int nb0 = rsbuf[k + 1].e.nb;
        if (ech_add(&rsbuf[k + 1].e, T[k])) { rsbuf[k + 1].bt[nb0] = k; rnew = &rsbuf[k + 1]; }
        gen = (rnew->e.nb == R);
    } else {
        for (int i = 0; i < ccount[k]; i++) {
            Cand *cd = &cl[k][i];
            int sum = 0;
            for (int j = 0; j < R; j++) sum += cd->y[j] * T[k][j];
            if (sum != 0 && sum != cd->D && sum != -cd->D) continue;
            cbuf[k + 1][nc] = *cd; sflag[k + 1][nc] = (sum != 0); cbuf[k + 1][nc].sup += (sum != 0); nc++;
        }
    }
    for (int v = 1; v <= cap; v++) {
        m[k] = v;
        for (int i = 0; i < R; i++) if (T[k][i]) need[i] -= v;
        rs[k + 1] = rnew;
        if (!had) {
            if (gen) generate(k + 1);
            else { have[k + 1] = 0; ccount[k + 1] = 0; cl[k + 1] = NULL; }
        } else {
            if (v > 1) for (int i = 0; i < nc; i++) cbuf[k + 1][i].sup += sflag[k + 1][i];
            cl[k + 1] = cbuf[k + 1]; ccount[k + 1] = nc; have[k + 1] = 1;
        }
        dfs(k + 1, rem - v, tied);
        for (int i = 0; i < R; i++) if (T[k][i]) need[i] += v;
    }
    m[k] = 0;
}

int main(int argc, char **argv) {
    if (argc < 7 + R) { fprintf(stderr, "usage: sectn n PLO PHI QD REJ AMAX s1..sR [shard nshard]\n"); return 1; }
    nn = atoi(argv[1]); PLO = atoll(argv[2]); PHI = atoll(argv[3]); QD = atoll(argv[4]); REJ = atoi(argv[5]); AMAX = atoi(argv[6]);
    for (int i = 0; i < R; i++) prof[i] = atoi(argv[7 + i]);
    if (argc >= 9 + R) { shard = atoll(argv[7 + R]); nshard = atoll(argv[8 + R]); }
    if (getenv("NOGREEDY")) GREEDY = 0;
    if (getenv("NOPRUNE")) PRUNE = 0;
    if (getenv("NOSYM")) SYM = 0;
    pow2[0] = 1; for (int i = 1; i < 64; i++) pow2[i] = pow2[i - 1] * 2;
    make_types();
    fprintf(stderr, "R=%d types=%d AMAX=%d\n", R, NT, AMAX);
    for (int i = 0; i < R; i++) { need[i] = prof[i]; lastnz[i] = -1; for (int k = 0; k < NT; k++) if (T[k][i]) lastnz[i] = k; }
    printf("TYPES");
    for (int k = 0; k < NT; k++) { printf(" "); for (int i = 0; i < R; i++) printf("%d%s", T[k][i], i + 1 < R ? "," : ""); }
    printf("\n");
    rsbuf[0].e.nb = 0; rs[0] = &rsbuf[0]; have[0] = 0; ccount[0] = 0; cl[0] = NULL;
    int amax = AMAX < nn ? AMAX : nn;
    dfs(0, amax, SYM ? ((1u << NG) - 2) : 0);
    printf("SUMMARY n=%d prof=", nn);
    for (int i = 0; i < R; i++) printf("%d%s", prof[i], i + 1 < R ? "," : "");
    printf(" shard=%lld/%lld leaves=%lld rankdef=%lld short=%lld riesz_fail=%lld greedy_fail=%lld admitted=%lld pruned=%lld\n",
           shard, nshard, leaves, n_rank_def, n_short, n_riesz_fail, n_greedy_fail, n_adm, n_pruned);
    printf("ORBITSUM leaves_weighted=%lld sym=%d amax=%d generated=%lld\n", orbit_leaves, SYM, amax, n_gen);
    if (have_max) printf("MAXS A=%lld B=%lld (S_O*2^(n-1) = delta*A + B, max at delta_lo over short-free full-rank leaves) greedy=%d prune=%d\n", (ll)bestA, (ll)bestB, GREEDY, PRUNE);
    return 0;
}
