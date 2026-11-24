// Memory-lean version of ac_search.cpp (same graph, same search order), for
// caps >= 28.  States are packed into two 64-bit words (2 bits per letter,
// first letter in the high bits, length in the low 6 bits), stored once in an
// append-only array; an open-addressing table of 32-bit indices finds them.
// About 30 bytes per state instead of about 220.
//
// Graph (identical to ac_search.cpp with --junction): vertices are unordered
// pairs of cyclically reduced words, each up to rotation and inversion; an edge
// replaces u by cyclic_reduce(rot(u) * rot(v)^e) when the junction cancels.
// Output format is the same as ac_search (PATH ... END of "u|v" lines), so
// ac_path.py can expand and ac_check.py can check any path it prints.
//
// Usage: ac_search_compact CAP [--maxstates N] SRC ... [+ SRC ...] [--passive SRC ...]
//   A passive source is put in the table (reaching it from another group is a
//   MEET) but is never expanded.  "P1 --passive AK3 P2" thus explores only the
//   forward sublevel set of P1 and reports whether it contains AK3 or P2.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

// letters: X=0 Y=1 x=2 y=3 (ASCII order X<Y<x<y); inverse = c ^ 2
static const char LET[4] = {'X', 'Y', 'x', 'y'};
static int code(char c) { return c == 'X' ? 0 : c == 'Y' ? 1 : c == 'x' ? 2 : 3; }
struct W { int n; uint8_t a[64]; };

static void freered(W& w) {
    int o = 0;
    for (int i = 0; i < w.n; i++) {
        if (o && w.a[o - 1] == (w.a[i] ^ 2)) o--; else w.a[o++] = w.a[i];
    }
    w.n = o;
}
static void cycred(W& w) {
    freered(w);
    int i = 0, j = w.n;
    while (j - i >= 2 && w.a[i] == (w.a[j - 1] ^ 2)) { i++; j--; }
    if (i) memmove(w.a, w.a + i, j - i);
    w.n = j - i;
}
static uint64_t pack(const uint8_t* a, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 2) | a[i];
    v <<= 2 * (29 - n);
    return (v << 6) | (uint64_t)n;  // 58 bits of letters + 6 bits length
}
static uint64_t canon(const W& w) {  // least rotation of w or w^-1 (n <= 29)
    int n = w.n;
    if (n == 0) return 0;
    uint8_t d[128];
    uint64_t best = ~0ULL;
    for (int f = 0; f < 2; f++) {
        for (int i = 0; i < n; i++) d[i] = f ? (w.a[n - 1 - i] ^ 2) : w.a[i];
        for (int i = 0; i < n; i++) d[n + i] = d[i];
        for (int k = 0; k < n; k++) { uint64_t v = pack(d + k, n); if (v < best) best = v; }
    }
    return best;
}
static void unpack(uint64_t v, W& w) {
    w.n = v & 63;
    uint64_t bits = v >> 6;
    for (int i = 0; i < w.n; i++) w.a[i] = (bits >> (2 * (28 - i))) & 3;
}
static string str(uint64_t v) { W w; unpack(v, w); string s; for (int i = 0; i < w.n; i++) s += LET[w.a[i]]; return s; }

struct E { uint64_t k1, k2; uint32_t parent; uint8_t src; } __attribute__((packed));
static vector<E> ent;
static vector<uint32_t> table;  // 0 = empty, else index+1
static uint64_t mask;
static inline uint64_t hsh(uint64_t a, uint64_t b) {
    uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
    return h ^ (h >> 29);
}
static int64_t find(uint64_t a, uint64_t b, uint64_t& slot) {
    uint64_t i = hsh(a, b) & mask;
    while (table[i]) {
        const E& e = ent[table[i] - 1];
        if (e.k1 == a && e.k2 == b) { slot = i; return table[i] - 1; }
        i = (i + 1) & mask;
    }
    slot = i;
    return -1;
}

int main(int argc, char** argv) {
    int cap = atoi(argv[1]);
    long maxstates = 100000000;
    vector<pair<W, W>> srcs; vector<int> group; vector<bool> passive; int g = 0; bool grouped = false, pas = false;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "+")) { g++; grouped = true; continue; }
        if (!strcmp(argv[i], "--passive")) { pas = true; continue; }
        if (!strcmp(argv[i], "--maxstates")) { maxstates = atol(argv[++i]); continue; }
        if (!strcmp(argv[i], "--junction")) continue;  // always on
        string s = argv[i]; size_t p = s.find('/');
        W u, v; u.n = v.n = 0;
        for (char c : s.substr(0, p)) u.a[u.n++] = code(c);
        for (char c : s.substr(p + 1)) v.a[v.n++] = code(c);
        cycred(u); cycred(v);
        srcs.push_back({u, v}); group.push_back(g); passive.push_back(pas);
    }
    if (!grouped) for (size_t i = 0; i < group.size(); i++) group[i] = i;
    for (size_t i = 0; i < group.size(); i++) if (passive[i]) group[i] = 1000 + i;  // own group each
    uint64_t tsz = 1; while (tsz < (uint64_t)(maxstates * 1.4)) tsz <<= 1;
    table.assign(tsz, 0); mask = tsz - 1;
    ent.reserve(maxstates + 1024);
    vector<vector<uint32_t>> bucket(cap + 1);
    for (size_t i = 0; i < srcs.size(); i++) {
        uint64_t a = canon(srcs[i].first), b = canon(srcs[i].second);
        if (b < a) swap(a, b);
        uint64_t slot;
        if (find(a, b, slot) >= 0) { printf("sources %zu coincide with an earlier one\n", i); return 0; }
        ent.push_back(E{a, b, 0xFFFFFFFFu, (uint8_t)i});
        table[slot] = ent.size();
        if (!passive[i]) bucket[srcs[i].first.n + srcs[i].second.n].push_back(ent.size() - 1);
    }
    long settled = 0;
    vector<long> per(srcs.size(), 0);
    for (int level = 0; level < cap; level++) {
        for (size_t qi = 0; qi < bucket[level].size(); qi++) {
            uint32_t id = bucket[level][qi];
            E cur = ent[id];
            settled++; per[cur.src]++;
            if (settled % 5000000 == 0) { fprintf(stderr, "settled %ld level %d seen %zu\n", settled, level, ent.size()); }
            W w[2]; unpack(cur.k1, w[0]); unpack(cur.k2, w[1]);
            for (int i = 0; i < 2; i++) {
                const W& a = w[i]; const W& b0 = w[1 - i];
                for (int e = 0; e < 2; e++) {
                    W b = b0;
                    if (e) for (int t = 0; t < b0.n; t++) b.a[t] = b0.a[b0.n - 1 - t] ^ 2;
                    int na = a.n, nb = b.n;
                    if (!na || !nb) continue;
                    if (na + nb > 60) continue;
                    for (int ra = 0; ra < na; ra++) {
                        uint8_t lastA = a.a[(ra + na - 1) % na];
                        for (int rb = 0; rb < nb; rb++) {
                            if (b.a[rb] != (lastA ^ 2)) continue;  // cancelling junction
                            W nw; nw.n = na + nb;
                            for (int t = 0; t < na; t++) nw.a[t] = a.a[(ra + t) % na];
                            for (int t = 0; t < nb; t++) nw.a[na + t] = b.a[(rb + t) % nb];
                            cycred(nw);
                            int L = nw.n + b0.n;
                            if (L >= cap || nw.n > 29) continue;
                            uint64_t k1 = canon(nw), k2 = canon(b0);
                            if (k2 < k1) swap(k1, k2);
                            uint64_t slot;
                            int64_t f = find(k1, k2, slot);
                            if (f < 0) {
                                if ((long)ent.size() >= maxstates) { printf("BUDGET exhausted at level %d, settled %ld, seen %zu\n", level, settled, ent.size()); return 3; }
                                ent.push_back(E{k1, k2, id, cur.src});
                                table[slot] = ent.size();
                                bucket[max(level, L)].push_back(ent.size() - 1);
                            } else if (group[ent[f].src] != group[cur.src]) {
                                printf("MEET at level %d (sources %d,%d) after %ld settled, %zu seen\n", level, cur.src, ent[f].src, settled, ent.size());
                                vector<uint32_t> p1, p2;
                                for (uint32_t c = id; c != 0xFFFFFFFFu; c = ent[c].parent) p1.push_back(c);
                                for (uint32_t c = (uint32_t)f; c != 0xFFFFFFFFu; c = ent[c].parent) p2.push_back(c);
                                reverse(p1.begin(), p1.end());
                                printf("PATH\n");
                                for (auto c : p1) printf("%s|%s\n", str(ent[c].k1).c_str(), str(ent[c].k2).c_str());
                                for (auto c : p2) printf("%s|%s\n", str(ent[c].k1).c_str(), str(ent[c].k2).c_str());
                                printf("END\n");
                                return 0;
                            }
                        }
                    }
                }
            }
        }
        printf("level %d done: settled %ld, seen %zu, per source:", level, settled, ent.size());
        for (auto c : per) printf(" %ld", c);
        printf("\n"); fflush(stdout);
        vector<uint32_t>().swap(bucket[level]);
    }
    printf("EXHAUSTED below cap %d: settled %ld, no meeting\n", cap, settled);
    return 1;
}
