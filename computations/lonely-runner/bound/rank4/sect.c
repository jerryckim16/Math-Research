/* Complete ternary-section census for one greedy support profile of odd
 * relation rank R (R = 3 or 4, compile with -DR=4), general n.
 *
 * Our own implementation of the method of Allikvere, "Sixteen lonely runners"
 * (Zenodo 10.5281/zenodo.23304361), App. B / Sec. "rank-four classification".
 * None of his code is used.
 *
 * Setting.  O = span of the odd ternary relations of a counterexample v to
 * LRC(n), dim O = R; H = R x n matrix of a greedy odd basis (row supports
 * s_1 <= ... <= s_R).  Up to column sign the columns of H form a multiset of
 * the (3^R-1)/2 projective nonzero ternary types plus zero columns, so H is a
 * multiplicity vector m over the types with row supports exactly s and
 * sum m <= n.  We enumerate ALL such m.  For each m with present type set P:
 *
 *   section  T(O) = { lambda in Q^R \ 0 (mod sign) : lambda.c in {-1,0,1}
 *                     for every c in P },  support(lambda) = sum_{c in P,
 *                     lambda.c != 0} m_c.
 *   Every section element is lambda = M^{-1} x for an invertible M of R
 *   present types and x ternary, so it lies in the finite global candidate
 *   set Lam (all M^{-1}x over all R-subsets of types); we build Lam once
 *   and filter it along the DFS (a type c, once present, removes every
 *   lambda with lambda.c not ternary).  rank P < R  <=>  some surviving
 *   lambda has support 0 (then the rows are dependent: skip).
 *
 *   tests:  no line of support <= REJ (support 1: v_l = 0; support 2:
 *           v_i = v_j, impossible for distinct speeds);
 *           signed Riesz S_O(delta) > delta, where
 *           S_O = sum_odd w(s) - sum_even w(s), w(s) = (delta+s)/2^(s-1);
 *           with A = sum +-2^(n-s), B = sum +-s 2^(n-s):
 *           S_O - delta = [delta (A - 2^(n-1)) + B] / 2^(n-1), affine in
 *           delta; the section is EXCLUDED iff this is < 0 at both rational
 *           endpoints delta_lo = PLO/QD, delta_hi = PHI/QD of an enclosure;
 *           greedy: the greedy support sequence of the odd lines (increasing
 *           support, independent) equals s.
 *   admitted sections: exact saturated Gram g = det(H H^T) / idx^2, idx =
 *           gcd of the R x R minors of the present types.
 *
 *   pruning (rigorous): lines only disappear and supports only grow along
 *           the DFS; odd lines of a greedy-valid section have support
 *           >= s_1.  So S_O <= sum over current candidates of
 *           w(odd ceiling of max(s_1, partial support)); if that upper bound
 *           minus delta is < 0 at both endpoints, prune.
 *
 * Usage: sect n PLO PHI QD REJ s_1 ... s_R [shard nshard]
 * Output: summary lines; one "ADM" line per admitted multiplicity vector.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifndef R
#define R 4
#endif
#define MAXT 121
#define MAXL 200000
#ifndef PRUNE_MAX
#define PRUNE_MAX 48
#endif

typedef long long ll;
typedef __int128 i128;

static int NT;                 /* number of projective types */
static int T[MAXT][R];
static int nn, REJ, prof[R];
static ll PLO, PHI, QD;

/* candidate lambdas: y/D, y integral, D > 0 */
static int NL;
static int LY[MAXL][R], LD[MAXL];
static uint64_t Ltern[MAXL][2], Lnz[MAXL][2];

static int gcdi(int a, int b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { int t = a % b; a = b; b = t; } return a; }
static ll gcdl(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }

static int bit(const uint64_t *m, int k) { return (m[k >> 6] >> (k & 63)) & 1; }
static void setbit(uint64_t *m, int k) { m[k >> 6] |= 1ULL << (k & 63); }

static void make_types(void) {
    int t[R];
    int tot = 1;
    for (int i = 0; i < R; i++) tot *= 3;
    NT = 0;
    for (int code = 0; code < tot; code++) {
        int c = code, first = 0;
        for (int i = 0; i < R; i++) { t[i] = c % 3 - 1; c /= 3; }
        /* lexicographic order on (t_0..t_{R-1}) with digit 0 most significant:
           rebuild in that order below; here accept canonical (first nonzero > 0) */
        for (int i = 0; i < R; i++) if (t[i]) { first = t[i]; break; }
        if (first <= 0) continue;
        memcpy(T[NT++], t, sizeof t);
    }
    /* sort lexicographically for a reproducible order */
    for (int i = 0; i < NT; i++)
        for (int j = i + 1; j < NT; j++)
            if (memcmp(T[j], T[i], sizeof T[i]) < 0) {
                int tmp[R]; memcpy(tmp, T[i], sizeof tmp); memcpy(T[i], T[j], sizeof tmp); memcpy(T[j], tmp, sizeof tmp);
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

/* adjugate via cofactors: adj[i][j] = (-1)^(i+j) minor(j,i) */
static void adjR(ll M[R][R], ll adj[R][R]) {
    for (int i = 0; i < R; i++)
        for (int j = 0; j < R; j++) {
            ll S[R][R]; /* build (R-1)x(R-1) minor deleting row j col i, padded */
            int ri = 0;
            ll m[R][R];
            for (int a = 0; a < R; a++) {
                if (a == j) continue;
                int ci = 0;
                for (int b = 0; b < R; b++) { if (b == i) continue; m[ri][ci++] = M[a][b]; }
                ri++;
            }
            /* determinant of (R-1)x(R-1) block m by expansion via Bareiss on padded matrix */
            memset(S, 0, sizeof S);
            for (int a = 0; a < R - 1; a++) for (int b = 0; b < R - 1; b++) S[a][b] = m[a][b];
            S[R - 1][R - 1] = 1;
            ll d = detR(S);
            adj[i][j] = ((i + j) & 1) ? -d : d;
        }
}

/* hash set for lambdas */
#define HS (1 << 21)
static int htab[HS];
static unsigned hkey(const int *y, int D) {
    unsigned h = 2166136261u;
    for (int i = 0; i < R; i++) { h ^= (unsigned)(y[i] + 64); h *= 16777619u; }
    h ^= (unsigned)D; h *= 16777619u;
    return h & (HS - 1);
}
static void add_lambda(int *y, int D) {
    int g = D;
    for (int i = 0; i < R; i++) g = gcdi(g, y[i]);
    if (g == 0) return;
    for (int i = 0; i < R; i++) y[i] /= g;
    D /= g;
    if (D < 0) { D = -D; for (int i = 0; i < R; i++) y[i] = -y[i]; }
    int f = 0;
    for (int i = 0; i < R; i++) if (y[i]) { f = y[i]; break; }
    if (f == 0) return;
    if (f < 0) for (int i = 0; i < R; i++) y[i] = -y[i];
    unsigned h = hkey(y, D);
    while (htab[h]) {
        int id = htab[h] - 1;
        if (LD[id] == D && memcmp(LY[id], y, sizeof(int) * R) == 0) return;
        h = (h + 1) & (HS - 1);
    }
    if (NL >= MAXL) { fprintf(stderr, "MAXL\n"); exit(2); }
    memcpy(LY[NL], y, sizeof(int) * R); LD[NL] = D;
    NL++;
    htab[h] = NL;
}

static void make_lambdas(void) {
    int idx[R];
    for (int i = 0; i < R; i++) idx[i] = i;
    int tot = 1; for (int i = 0; i < R; i++) tot *= 3;
    while (1) {
        ll M[R][R], adj[R][R];
        for (int a = 0; a < R; a++) for (int b = 0; b < R; b++) M[a][b] = T[idx[a]][b];
        ll D = detR(M);
        if (D) {
            adjR(M, adj);          /* M adj = D I ; lambda with M lambda = x is adj x / D */
            for (int code = 0; code < tot; code++) {
                int x[R], c = code, nz = 0;
                for (int i = 0; i < R; i++) { x[i] = c % 3 - 1; c /= 3; nz |= x[i]; }
                if (!nz) continue;
                int y[R];
                for (int i = 0; i < R; i++) { ll s = 0; for (int j = 0; j < R; j++) s += adj[i][j] * x[j]; y[i] = (int)s; }
                add_lambda(y, (int)D);
            }
        }
        int k = R - 1;
        while (k >= 0 && idx[k] == NT - R + k) k--;
        if (k < 0) break;
        idx[k]++;
        for (int j = k + 1; j < R; j++) idx[j] = idx[j - 1] + 1;
    }
    for (int l = 0; l < NL; l++) {
        Ltern[l][0] = Ltern[l][1] = Lnz[l][0] = Lnz[l][1] = 0;
        for (int k = 0; k < NT; k++) {
            int s = 0;
            for (int i = 0; i < R; i++) s += LY[l][i] * T[k][i];
            if (s == 0 || s == LD[l] || s == -LD[l]) setbit(Ltern[l], k);
            if (s != 0) setbit(Lnz[l], k);
        }
    }
}

/* ------------------------------------------------------------ DFS state */
static int m[MAXT];
static int *cand[MAXT + 1];      /* candidate lambda ids at depth k */
static int *csup[MAXT + 1];      /* partial supports */
static int ccount[MAXT + 1];
static ll pow2[64];
static ll leaves, n_rank_def, n_short, n_riesz_fail, n_greedy_fail, n_adm, n_pruned;
static ll shard = 0, nshard = 1, prefix_ord = 0;
#define SHARD_DEPTH 4

static int GREEDY = 1, PRUNE = 1, have_max = 0;
static i128 best_flo, bestA, bestB;
static int oddceil(int s) { return (s & 1) ? s : s + 1; }

/* f(delta) numerator at endpoint p/QD for sum of terms sign*(delta+s)/2^(s-1) minus delta:
   value * 2^(n-1) * QD = p*(A - 2^(n-1)) + QD*B */
static int excluded_AB(i128 A, i128 B) {
    i128 base = pow2[nn - 1];
    i128 flo = (i128)PLO * (A - base) + (i128)QD * B;
    i128 fhi = (i128)PHI * (A - base) + (i128)QD * B;
    return flo < 0 && fhi < 0;
}

/* rank of a set of integer vectors (as rationals) - incremental: keep echelon basis */
static int rank_add(ll basis[R][R], int *nb, const int *y) {
    ll v[R];
    for (int i = 0; i < R; i++) v[i] = y[i];
    for (int b = 0; b < *nb; b++) {
        int p = 0; while (basis[b][p] == 0) p++;
        if (v[p]) {
            ll a = basis[b][p], c = v[p];
            ll g = 0;
            for (int i = 0; i < R; i++) { v[i] = v[i] * a - basis[b][i] * c; g = gcdl(g, v[i]); }
            if (g > 1) for (int i = 0; i < R; i++) v[i] /= g;
        }
    }
    int nz = 0; for (int i = 0; i < R; i++) if (v[i]) nz = 1;
    if (!nz) return 0;
    /* insert keeping pivots sorted */
    int p = 0; while (v[p] == 0) p++;
    int pos = *nb;
    for (int b = 0; b < *nb; b++) { int q = 0; while (basis[b][q] == 0) q++; if (q > p) { pos = b; break; } }
    for (int b = *nb; b > pos; b--) memcpy(basis[b], basis[b - 1], sizeof basis[0]);
    memcpy(basis[pos], v, sizeof v);
    (*nb)++;
    return 1;
}

static int present[MAXT], np;

static void leaf(void) {
    int K = NT;
    int c = ccount[K];
    leaves++;
    i128 A = 0, B = 0;
    {   /* rank of the present types */
        ll bs[R][R]; int nb0 = 0;
        for (int k = 0; k < NT; k++) if (m[k]) rank_add(bs, &nb0, T[k]);
        if (nb0 < R) { n_rank_def++; return; }
    }
    for (int i = 0; i < c; i++) if (csup[K][i] == 0) { fprintf(stderr, "support-0 line in full-rank leaf\n"); exit(5); }
    for (int i = 0; i < c; i++) if (csup[K][i] <= REJ) { n_short++; return; }
    for (int i = 0; i < c; i++) {
        int s = csup[K][i];
        ll w = pow2[nn - s];
        if (s & 1) { A += w; B += (i128)s * w; } else { A -= w; B -= (i128)s * w; }
    }
    /* track the maximum of S_O - delta over short-line-free sections (no greedy) */
    {
        i128 base = pow2[nn - 1];
        i128 flo = (i128)PLO * (A - base) + (i128)QD * B;
        if (!have_max || flo > best_flo) { have_max = 1; best_flo = flo; bestA = A; bestB = B; }
    }
    if (excluded_AB(A, B)) { n_riesz_fail++; return; }
    /* greedy check: odd lines by increasing support */
    int ord[MAXL > 4096 ? 4096 : MAXL]; int no = 0;
    for (int i = 0; i < c && no < 4096; i++) if (csup[K][i] & 1) ord[no++] = i;
    if (no >= 4096) { fprintf(stderr, "too many odd lines\n"); exit(3); }
    for (int i = 1; i < no; i++) { int x = ord[i], j = i - 1; while (j >= 0 && csup[K][ord[j]] > csup[K][x]) { ord[j + 1] = ord[j]; j--; } ord[j + 1] = x; }
    ll basis[R][R]; int nb = 0; int gs[R];
    for (int i = 0; i < no && nb < R; i++) {
        int id = cand[K][ord[i]];
        int sup = csup[K][ord[i]];
        int before = nb;
        rank_add(basis, &nb, LY[id]);
        if (nb > before) gs[before] = sup;
    }
    int ok = (nb == R) || !GREEDY;
    for (int i = 0; ok && GREEDY && i < R; i++) if (gs[i] != prof[i]) ok = 0;
    if (!ok) { n_greedy_fail++; return; }
    /* Gram and saturation index */
    ll G[R][R]; memset(G, 0, sizeof G);
    np = 0; int a = 0;
    for (int k = 0; k < NT; k++) if (m[k]) {
        present[np++] = k; a += m[k];
        for (int i = 0; i < R; i++) for (int j = 0; j < R; j++) G[i][j] += (ll)m[k] * T[k][i] * T[k][j];
    }
    ll gram = detR(G);
    ll idx = 0;
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
    /* S_O(delta) * 2^(n-1) = delta*A + B */
    printf("ADM a=%d g=%lld idx=%lld raw=%lld lines=%d A=%lld B=%lld m=", a, g, idx, gram, c, (ll)A, (ll)B);
    for (int k = 0; k < NT; k++) printf("%d%c", m[k], k + 1 < NT ? ',' : '\n');
}

static int need[R];            /* remaining row deficits */
static int lastnz[R];          /* last type index with a nonzero entry in row i */
static int *buf[MAXT + 2], *sbuf[MAXT + 2], *bbuf[MAXT + 2], *zbuf[MAXT + 2];

/* list at depth k: ids cand[k], supports csup[k][i] + cv[k]*cz[k][i] */
static int *cz[MAXT + 2], cv[MAXT + 2];

static int prune_ub2(int k) {
    i128 A = 0, B = 0;
    int c = ccount[k], v = cv[k], *bs = csup[k], *zf = cz[k];
    for (int i = 0; i < c; i++) {
        int s = bs[i] + v * zf[i];
        if (s < prof[0]) s = prof[0];
        s = oddceil(s);
        if (s > nn) continue;
        A += pow2[nn - s];
        B += (i128)s * pow2[nn - s];
    }
    return excluded_AB(A, B);
}

static int *leafsup;

static void dfs(int k, int rem) {
    if (k == SHARD_DEPTH) {
        ll o = prefix_ord++;
        if (o % nshard != shard) return;
    }
    if (k == NT) {
        for (int i = 0; i < R; i++) if (need[i]) return;
        int c = ccount[k], v = cv[k], *bs = csup[k], *zf = cz[k];
        for (int i = 0; i < c; i++) leafsup[i] = bs[i] + v * zf[i];
        csup[k] = leafsup;
        leaf();
        csup[k] = bs;
        return;
    }
    int mx = 0;
    for (int i = 0; i < R; i++) if (need[i] > mx) mx = need[i];
    if (mx > rem) return;
    for (int i = 0; i < R; i++) if (need[i] && k > lastnz[i]) return;
    if (PRUNE && GREEDY && ccount[k] <= PRUNE_MAX && prune_ub2(k)) { n_pruned++; return; }
    /* m_k = 0 */
    m[k] = 0;
    cand[k + 1] = cand[k]; csup[k + 1] = csup[k]; cz[k + 1] = cz[k]; cv[k + 1] = cv[k]; ccount[k + 1] = ccount[k];
    dfs(k + 1, rem);
    /* m_k >= 1 */
    int cap = rem;
    for (int i = 0; i < R; i++) if (T[k][i] && need[i] < cap) cap = need[i];
    if (cap < 1) return;
    int c = ccount[k], *src = cand[k], *ssrc = csup[k], *zsrc = cz[k], pv = cv[k];
    int *dst = buf[k + 1], *bs = bbuf[k + 1], *zf = zbuf[k + 1], nc_n = 0;
    for (int i = 0; i < c; i++) {
        int id = src[i];
        if (bit(Ltern[id], k)) { dst[nc_n] = id; bs[nc_n] = ssrc[i] + pv * zsrc[i]; zf[nc_n] = bit(Lnz[id], k); nc_n++; }
    }
    cand[k + 1] = dst; csup[k + 1] = bs; cz[k + 1] = zf; ccount[k + 1] = nc_n;
    for (int v = 1; v <= cap; v++) {
        m[k] = v;
        for (int i = 0; i < R; i++) if (T[k][i]) need[i] -= v;
        cand[k + 1] = dst; csup[k + 1] = bs; cz[k + 1] = zf; cv[k + 1] = v; ccount[k + 1] = nc_n;
        dfs(k + 1, rem - v);
        for (int i = 0; i < R; i++) if (T[k][i]) need[i] += v;
    }
    m[k] = 0;
}

int main(int argc, char **argv) {
    if (argc < 6 + R) { fprintf(stderr, "usage: sect n PLO PHI QD REJ s1..sR [shard nshard]\n"); return 1; }
    nn = atoi(argv[1]); PLO = atoll(argv[2]); PHI = atoll(argv[3]); QD = atoll(argv[4]); REJ = atoi(argv[5]);
    for (int i = 0; i < R; i++) prof[i] = atoi(argv[6 + i]);
    if (argc >= 8 + R) { shard = atoll(argv[6 + R]); nshard = atoll(argv[7 + R]); }
    if (getenv("NOGREEDY")) GREEDY = 0;
    if (getenv("NOPRUNE")) PRUNE = 0;
    pow2[0] = 1; for (int i = 1; i < 64; i++) pow2[i] = pow2[i - 1] * 2;
    make_types();
    make_lambdas();
    fprintf(stderr, "R=%d types=%d lambdas=%d\n", R, NT, NL);
    int *all = (int *)malloc(sizeof(int) * NL);
    for (int i = 0; i < NL; i++) all[i] = i;
    for (int d = 0; d <= NT + 1; d++) {
        buf[d] = (int *)malloc(sizeof(int) * NL); sbuf[d] = (int *)malloc(sizeof(int) * NL);
        bbuf[d] = (int *)malloc(sizeof(int) * NL); zbuf[d] = (int *)malloc(sizeof(int) * NL);
    }
    cand[0] = all; csup[0] = (int *)calloc(NL, sizeof(int)); cz[0] = (int *)calloc(NL, sizeof(int)); cv[0] = 0; ccount[0] = NL;
    leafsup = (int *)malloc(sizeof(int) * NL);
    for (int i = 0; i < R; i++) { need[i] = prof[i]; lastnz[i] = -1; for (int k = 0; k < NT; k++) if (T[k][i]) lastnz[i] = k; }
    printf("TYPES");
    for (int k = 0; k < NT; k++) { printf(" "); for (int i = 0; i < R; i++) printf("%d%s", T[k][i], i + 1 < R ? "," : ""); }
    printf("\n");
    dfs(0, nn);
    printf("SUMMARY n=%d prof=", nn);
    for (int i = 0; i < R; i++) printf("%d%s", prof[i], i + 1 < R ? "," : "");
    printf(" shard=%lld/%lld leaves=%lld rankdef=%lld short=%lld riesz_fail=%lld greedy_fail=%lld admitted=%lld pruned=%lld\n",
           shard, nshard, leaves, n_rank_def, n_short, n_riesz_fail, n_greedy_fail, n_adm, n_pruned);
    if (have_max) printf("MAXS A=%lld B=%lld (S_O*2^(n-1) = delta*A + B, max at delta_lo over short-free full-rank leaves) greedy=%d prune=%d\n", (ll)bestA, (ll)bestB, GREEDY, PRUNE);
    return 0;
}
