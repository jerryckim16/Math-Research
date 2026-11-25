/* shift_gap.c -- lower bound for the shifted-Dirichlet gap gamma(k,c).
 *
 * For y in Z_c^k put lambda(y) = max_{r in Z_c, r != 0} sup_t min_i || i t + y_i r / c ||.
 * y is TRIVIAL if y_i = j*i (mod c) for some j (then lambda(y) = 1/(k+1)).
 * lambda(y + j*(1..k)) = lambda(y), so we enumerate y with y_1 = 0, y != 0.
 * For each such y we evaluate min_i ||i t + y_i r/c|| EXACTLY at the rational
 * times t = m/G, 0 <= m < G (integers: numerator (i*m*c + y_i*r*G) mod (c*G)),
 * which gives a valid LOWER bound lb(y) <= lambda(y).  Output: the minimum over
 * nontrivial y of lb(y), as a fraction num/(c*G), and the worst y.
 * Second output (the one used in notes/lonely-runner/structure.md, Lemma R):
 * for each nontrivial y, the longest circular run of consecutive grid times
 * m/G (r over 1..c-1) with ALL ||i t + y_i r/c|| >= 1/(k+1), i.e.
 * (k+1)*d >= c*G; a run of n points spans a closed good interval of length
 * >= (n-1)/G.  Printed: min over nontrivial y of (n-1), so that
 * L_lb = minrun/G is a lower bound for the longest good interval of every y.
 * Usage: shift_gap k c G
 */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: shift_gap k c G\n"); return 2; }
    int k = atoi(argv[1]), c = atoi(argv[2]); long G = atol(argv[3]), D = c * G;
    int y[64] = {0};
    long total = 1; for (int i = 1; i < k; i++) total *= c;   /* y_1 = 0 fixed */
    long worst = D, nworst = 0; int wy[64];
    long minrun = G; int ry[64];
    char *good = malloc(G);
    for (long code = 1; code < total; code++) {
        long x = code; for (int i = 1; i < k; i++) { y[i] = x % c; x /= c; }
        long best = 0, bestrun = 0;
        for (int r = 1; r < c; r++) {
            for (long m = 0; m < G; m++) {
                long mn = D;
                for (int i = 0; i < k; i++) {
                    long v = ((long)(i + 1) * m * c + (long)y[i] * r * G) % D;
                    long d = v < D - v ? v : D - v;
                    if (d < mn) mn = d;
                }
                if (mn > best) best = mn;
                good[m] = (long)(k + 1) * mn >= D;
            }
            long run = 0, maxrun = 0, start = -1;
            for (long m = 0; m < G; m++) if (!good[m]) { start = m; break; }
            if (start < 0) maxrun = G;
            else for (long q = 1; q <= G; q++) { long m = (start + q) % G; if (good[m]) { run++; if (run > maxrun) maxrun = run; } else run = 0; }
            if (maxrun > bestrun) bestrun = maxrun;
        }
        if (bestrun - 1 < minrun) { minrun = bestrun - 1; for (int i = 0; i < k; i++) ry[i] = y[i]; }
        if (best < worst) { worst = best; nworst = 0; for (int i = 0; i < k; i++) wy[i] = y[i]; }
        if (best == worst) nworst++;
    }
    printf("k=%d c=%d G=%ld nontrivial_y=%ld  min lb(y) = %ld/%ld = %.6f  (1/(k+1) = %.6f)  #worst=%ld  worst y =",
           k, c, G, total - 1, worst, D, (double)worst / D, 1.0 / (k + 1), nworst);
    for (int i = 0; i < k; i++) printf(" %d", wy[i]);
    printf("\nmin over nontrivial y of the longest good run: (n-1) = %ld grid steps, L_lb = %ld/%ld = 1/%.2f; worst y =", minrun, minrun, G, minrun > 0 ? (double)G / minrun : 0.0);
    for (int i = 0; i < k; i++) printf(" %d", ry[i]);
    printf("\n");
    return 0;
}
