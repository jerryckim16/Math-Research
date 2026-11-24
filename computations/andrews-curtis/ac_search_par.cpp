// Key-only, multi-threaded version of ac_search_compact.cpp (same graph, same
// multi-source "meeting" criterion), for exclusive caps >= 30.
//
// Graph (identical to ac_search.cpp --junction): vertices are unordered pairs
// of cyclically reduced words, each up to rotation and inversion; an edge
// replaces u by cyclic_reduce(rot(u) * rot(v)^e) when the junction cancels.
// The graph is DIRECTED (an edge whose product cancels all of v^e has no
// reverse edge), so, as in ac_search*, a MEET means a state reachable forward
// from sources of two different groups.
//
// Storage: one 64-bit table entry per state, no parent pointers, no queue.
//   bits  0..55  key: the canonical pair (k1 <= k2 as in ac_search_compact)
//                written in mixed radix (first letter base 4, later letters
//                base 3 = "not the inverse of the previous letter"), times 512,
//                plus a code for the two lengths (never 0);
//   bits 56..60  level (bottleneck at which the state is settled);
//   bits 61..62  group of the source that reached it first;
//   bit  63      settled.
// Levels are processed in increasing order.  At level L every thread scans its
// share of the table for unsettled level-L entries (claiming each with a CAS
// on the settled bit) and keeps a local stack for level-L states it inserts
// itself, so the set settled at each level is exactly the one of the
// sequential engines; per-level counts are printed for comparison.
// A meeting is reported with the two states and their groups only (no path):
// recover a path with ac_search_compact (--passive) if it ever happens.
//
// Usage: ac_search_par CAP [--slots N] [--threads T] SRC ... [+ SRC ...] [--passive SRC ...]
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <thread>
#include <vector>
#include <algorithm>
using namespace std;

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
// --- exactly the canonical form of ac_search_compact.cpp ---
static uint64_t pack(const uint8_t* a, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 2) | a[i];
    v <<= 2 * (29 - n);
    return (v << 6) | (uint64_t)n;
}
static uint64_t canon(const W& w) {
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
// --- compact 56-bit key ---
static const uint64_t KEYMASK = (1ULL << 56) - 1;
static uint64_t encode(uint64_t c1, uint64_t c2) {  // c1 <= c2 packed canonical words
    W a, b; unpack(c1, a); unpack(c2, b);
    uint64_t v = 0;
    for (const W* w : {&a, &b})
        for (int i = 0; i < w->n; i++) {
            int c = w->a[i];
            if (i == 0) v = v * 4 + c;
            else { int p = w->a[i - 1] ^ 2; v = v * 3 + (c - (c > p ? 1 : 0)); }
        }
    int s = a.n + b.n;
    uint64_t lc = (uint64_t)(s * (s + 1) / 2 + a.n);  // 1..464 for s <= 29
    return v * 512 + lc;
}
static void decode(uint64_t key, W& a, W& b) {
    int lc = key % 512; uint64_t v = key / 512;
    int s = 0; while ((s + 1) * (s + 2) / 2 <= lc) s++;
    a.n = lc - s * (s + 1) / 2; b.n = s - a.n;
    for (W* w : {&b, &a})  // undo in reverse order
        for (int i = w->n - 1; i >= 0; i--) {
            if (i == 0) { w->a[0] = v % 4; v /= 4; }
            else { w->a[i] = v % 3; v /= 3; }
        }
    for (W* w : {&a, &b})
        for (int i = 1; i < w->n; i++) { int p = w->a[i - 1] ^ 2; if (w->a[i] >= p) w->a[i]++; }
}

static atomic<uint64_t>* table;
static uint64_t nslots;
static atomic<long> nstates{0};
static long maxstates;
static atomic<int> stop{0};  // 1 = meet, 2 = budget
static uint64_t meetA, meetB; static int meetGA, meetGB, meetLevel;

static inline uint64_t slot_of(uint64_t key) {
    uint64_t h = key * 0x9E3779B97F4A7C15ULL; h ^= h >> 29; h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 32;
    return (uint64_t)(((__uint128_t)h * nslots) >> 64);
}
// insert; returns slot, sets isnew; existing entry value in old
static uint64_t insert(uint64_t entry, bool& isnew, uint64_t& old) {
    uint64_t key = entry & KEYMASK;
    uint64_t i = slot_of(key);
    for (;;) {
        uint64_t cur = table[i].load(memory_order_acquire);
        if (cur == 0) {
            if (table[i].compare_exchange_strong(cur, entry, memory_order_acq_rel)) { isnew = true; return i; }
        }
        if ((cur & KEYMASK) == key) { isnew = false; old = cur; return i; }
        if (++i == nslots) i = 0;
    }
}
static inline uint64_t mk(uint64_t key, int level, int group) {
    return key | ((uint64_t)level << 56) | ((uint64_t)group << 61);
}

static vector<int> grp_of;  // group per source index; entries store group directly
static int CAP;

struct Local { long settled[4] = {0, 0, 0, 0}; vector<uint32_t> stack; };

static void expand(uint64_t entry, int level, Local& L) {
    int grp = (entry >> 61) & 3;
    W w[2]; decode(entry & KEYMASK, w[0], w[1]);
    L.settled[grp]++;
    for (int i = 0; i < 2; i++) {
        const W& a = w[i]; const W& b0 = w[1 - i];
        for (int e = 0; e < 2; e++) {
            W b = b0;
            if (e) for (int t = 0; t < b0.n; t++) b.a[t] = b0.a[b0.n - 1 - t] ^ 2;
            int na = a.n, nb = b.n;
            if (!na || !nb) continue;
            for (int ra = 0; ra < na; ra++) {
                uint8_t lastA = a.a[(ra + na - 1) % na];
                for (int rb = 0; rb < nb; rb++) {
                    if (b.a[rb] != (lastA ^ 2)) continue;
                    W nw; nw.n = na + nb;
                    for (int t = 0; t < na; t++) nw.a[t] = a.a[(ra + t) % na];
                    for (int t = 0; t < nb; t++) nw.a[na + t] = b.a[(rb + t) % nb];
                    cycred(nw);
                    int Ln = nw.n + b0.n;
                    if (Ln >= CAP || nw.n > 29) continue;
                    uint64_t k1 = canon(nw), k2 = canon(b0);
                    if (k2 < k1) swap(k1, k2);
                    uint64_t key = encode(k1, k2);
                    int nl = max(level, Ln);
                    bool isnew; uint64_t old;
                    uint64_t s = insert(mk(key, nl, grp), isnew, old);
                    if (isnew) {
                        long c = ++nstates;
                        if (c >= maxstates) { int z = 0; stop.compare_exchange_strong(z, 2); }
                        if (nl == level) L.stack.push_back((uint32_t)s);
                    } else if ((int)((old >> 61) & 3) != grp) {
                        int z = 0;
                        if (stop.compare_exchange_strong(z, 1)) {
                            meetA = entry & KEYMASK; meetGA = grp; meetB = old & KEYMASK;
                            meetGB = (old >> 61) & 3; meetLevel = level;
                        }
                    }
                }
            }
        }
    }
}
// claim an unsettled entry at slot s of the given level
static bool claim(uint64_t s, int level, uint64_t& entry) {
    uint64_t cur = table[s].load(memory_order_acquire);
    for (;;) {
        if (cur == 0 || (cur >> 63) || (int)((cur >> 56) & 31) != level) return false;
        if (table[s].compare_exchange_weak(cur, cur | (1ULL << 63), memory_order_acq_rel)) { entry = cur; return true; }
    }
}
static string wstr(const W& w) { string s; for (int i = 0; i < w.n; i++) s += LET[w.a[i]]; return s; }

int main(int argc, char** argv) {
    CAP = atoi(argv[1]);
    nslots = 400000000ULL; int T = 4;
    vector<pair<W, W>> srcs; vector<int> group; vector<bool> passive; int g = 0; bool pas = false;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "+")) { g++; continue; }
        if (!strcmp(argv[i], "--passive")) { pas = true; g++; continue; }
        if (!strcmp(argv[i], "--slots")) { nslots = atoll(argv[++i]); continue; }
        if (!strcmp(argv[i], "--threads")) { T = atoi(argv[++i]); continue; }
        if (!strcmp(argv[i], "--junction")) continue;
        string s = argv[i]; size_t p = s.find('/');
        W u, v; u.n = v.n = 0;
        for (char c : s.substr(0, p)) u.a[u.n++] = code(c);
        for (char c : s.substr(p + 1)) v.a[v.n++] = code(c);
        cycred(u); cycred(v);
        srcs.push_back({u, v}); group.push_back(g); passive.push_back(pas);
        if (pas) g++;
    }
    if (g > 3) { printf("at most 4 groups\n"); return 2; }
    maxstates = (long)(nslots * 0.9);
    table = new atomic<uint64_t>[nslots];
    for (uint64_t i = 0; i < nslots; i++) table[i].store(0, memory_order_relaxed);
    for (size_t i = 0; i < srcs.size(); i++) {
        uint64_t a = canon(srcs[i].first), b = canon(srcs[i].second);
        if (b < a) swap(a, b);
        int lev = srcs[i].first.n + srcs[i].second.n;
        bool isnew; uint64_t old;
        uint64_t e = mk(encode(a, b), lev, group[i]) | (passive[i] ? (1ULL << 63) : 0);
        insert(e, isnew, old);
        if (!isnew) { printf("source %zu coincides with an earlier one\n", i); return 0; }
        nstates++;
        // sanity: decode(encode) round trip
        W x, y; decode(e & KEYMASK, x, y); W p, q; unpack(a, p); unpack(b, q);
        if (wstr(x) != wstr(p) || wstr(y) != wstr(q)) { printf("encode/decode mismatch\n"); return 2; }
    }
    long tot[4] = {0, 0, 0, 0};
    for (int level = 0; level < CAP && !stop; level++) {
        vector<thread> th; vector<Local> loc(T);
        for (int t = 0; t < T; t++) th.emplace_back([&, t] {
            Local& L = loc[t];
            uint64_t lo = nslots * t / T, hi = nslots * (t + 1) / T;
            for (uint64_t s = lo; s < hi && !stop; s++) {
                uint64_t e;
                if (claim(s, level, e)) expand(e, level, L);
                while (!L.stack.empty() && !stop) {
                    uint32_t q = L.stack.back(); L.stack.pop_back();
                    if (claim(q, level, e)) expand(e, level, L);
                }
            }
        });
        for (auto& x : th) x.join();
        // leftover: entries of this level inserted behind every scanner (each was
        // pushed on its inserter's stack and drained, so none should remain)
        long left = 0;
        for (uint64_t s = 0; s < nslots && !stop; s++) { uint64_t e; if (claim(s, level, e)) { left++; expand(e, level, loc[0]); while (!loc[0].stack.empty()) { uint32_t q = loc[0].stack.back(); loc[0].stack.pop_back(); if (claim(q, level, e)) expand(e, level, loc[0]); } } }
        for (auto& L : loc) for (int k = 0; k < 4; k++) tot[k] += L.settled[k];
        long settled = tot[0] + tot[1] + tot[2] + tot[3];
        if (stop == 2) { printf("BUDGET exhausted at level %d, %ld states\n", level, nstates.load()); return 3; }
        if (stop == 1) break;
        printf("level %d done: settled %ld, seen %ld, per group: %ld %ld %ld %ld%s\n", level, settled,
               nstates.load(), tot[0], tot[1], tot[2], tot[3], left ? " (rescan used)" : "");
        fflush(stdout);
    }
    if (stop == 1) {
        W a, b, c, d; decode(meetA, a, b); decode(meetB, c, d);
        printf("MEET at level %d (groups %d,%d): expanding %s|%s hit %s|%s\n", meetLevel, meetGA, meetGB,
               wstr(a).c_str(), wstr(b).c_str(), wstr(c).c_str(), wstr(d).c_str());
        return 0;
    }
    long settled = tot[0] + tot[1] + tot[2] + tot[3];
    printf("EXHAUSTED below cap %d: settled %ld, no meeting\n", CAP, settled);
    return 1;
}
