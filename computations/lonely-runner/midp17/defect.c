/* defect.c -- free-coordinate patterns of retained tuples (Corollary TN' and Lemma TD of
 * notes/lonely-runner/midprimes17.md, section 4.3).  Exact finite enumeration.
 *
 * Fix k (threshold 1/(k+1)), a level l and f >= 2.  For a multiset e = {e_1..e_f} of
 * nonzero residues mod l (the residues of the coordinates NOT divisible by l):
 *   (R)  gcd(l, e_j : j != j0) = 1 for every j0;
 *   (N)  for every divisor d >= 2 of l with E_d = {j : d does not divide e_j} nonempty,
 *        sum_{j in E_d} g_j ceil(2d / ((k+1) g_j)) >= d,  g_j = gcd(e_j, d);
 *   (B)  there are real phases phi_j with  union_j B_j = Z_l, where
 *        B_j = { s in Z_l : || phi_j + s e_j / l || < 1/(k+1) }.
 * A retained level-l tuple (witness-free, gcd clause false, Lemma S false at every d | l)
 * has its non-multiples of l satisfying (R) and (N); if its multiples of l do not cover
 * every level-one time, they also satisfy (B) (take phi_j = a b_j / p for an uncovered a).
 * (B) is decided exactly: B_j(phi) is the preimage of the subgroup points
 * (g_j/l)Z in an open arc of length 2/(k+1); a largest such set is the preimage of a run of
 * r_j = ceil(2l/((k+1) g_j)) consecutive points (any start), and enlarging a B_j only helps,
 * so (B) holds iff some choice of run starts covers Z_l (DFS on the least uncovered s).
 * Usage: defect k l fmax     prints, for f = 2..fmax: #multisets, #(R)(N), #(R)(N)(B).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int k, l, f;
static int e[16], g[16], q[16], r[16], uinv[16];
static int gcdi(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int divs[64], nd;
static long long cnt_all, cnt_rn, cnt_b;
static int covered[512], used[16];

static int RN(void) {
    for (int j0 = 0; j0 < f; j0++) { int x = l; for (int j = 0; j < f; j++) if (j != j0) x = gcdi(x, e[j]); if (x != 1) return 0; }
    for (int a = 0; a < nd; a++) {
        int d = divs[a], ne = 0; long s = 0;
        for (int j = 0; j < f; j++) if (e[j] % d) { int gg = gcdi(e[j], d); ne++; s += (long)gg * ((2L * d + (long)(k + 1) * gg - 1) / ((long)(k + 1) * gg)); }
        if (ne > 0 && s < d) return 0;
    }
    return 1;
}
/* B_j(t0) = { s : (s * u_j) mod q_j in [t0, t0 + r_j) cyclically }, q_j = l/g_j, u_j = e_j/g_j */
static int inB(int j, int t0, int s) { int t = (int)(((long)s * (e[j] / g[j])) % q[j]); int d = (t - t0) % q[j]; if (d < 0) d += q[j]; return d < r[j]; }
static int dfs(void) {
    int s0 = -1;
    for (int s = 0; s < l; s++) if (!covered[s]) { s0 = s; break; }
    if (s0 < 0) return 1;
    for (int j = 0; j < f; j++) {
        if (used[j]) continue;
        if (j > 0 && !used[j - 1] && e[j] == e[j - 1]) continue;   /* equal coordinates: use the first unused */
        int t = (int)(((long)s0 * (e[j] / g[j])) % q[j]);
        for (int back = 0; back < r[j] && back < q[j]; back++) {   /* runs containing t */
            int t0 = ((t - back) % q[j] + q[j]) % q[j];
            int add[512], na = 0;
            for (int s = 0; s < l; s++) if (!covered[s] && inB(j, t0, s)) { covered[s] = 1; add[na++] = s; }
            used[j] = 1;
            int ok = dfs();
            used[j] = 0;
            for (int i = 0; i < na; i++) covered[add[i]] = 0;
            if (ok) return 1;
        }
    }
    return 0;
}
static void rec(int pos, int start) {
    if (pos == f) {
        cnt_all++;
        if (!RN()) return;
        cnt_rn++;
        for (int j = 0; j < f; j++) { g[j] = gcdi(e[j], l); q[j] = l / g[j]; r[j] = (2 * l + (k + 1) * g[j] - 1) / ((k + 1) * g[j]); }
        memset(covered, 0, sizeof covered); memset(used, 0, sizeof used);
        if (dfs()) cnt_b++;
        return;
    }
    for (int x = start; x < l; x++) { e[pos] = x; rec(pos + 1, x); }
}
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: defect k l fmax\n"); return 2; }
    k = atoi(argv[1]); l = atoi(argv[2]); int fmax = atoi(argv[3]);
    nd = 0; for (int d = 2; d <= l; d++) if (l % d == 0) divs[nd++] = d;
    (void)uinv;
    for (f = 2; f <= fmax; f++) {
        cnt_all = cnt_rn = cnt_b = 0;
        rec(0, 1);
        printf("k %d l %d f %d multisets %lld RN %lld RNB %lld\n", k, l, f, cnt_all, cnt_rn, cnt_b);
        fflush(stdout);
    }
    return 0;
}
