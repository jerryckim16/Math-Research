// Multi-source minimax ("bottleneck") search for AC connections between
// two-generator balanced presentations.  Written independently here.
//
// States: unordered pairs {u, v} of cyclically reduced words, each word taken
// up to rotation and inversion (canonical form = lexicographically least
// rotation of w or w^-1; pair sorted).  Every symmetry used is AC-realizable.
// Edge: replace u by cyclic_reduce(rot(u) * rot(v)^e), e = +-1, for every
// rotation of u and of v (and symmetrically for v).  Each edge is a short
// sequence of elementary AC moves (two conjugations/rotations, one
// multiplication, conjugations to cyclically reduce), so every path found
// expands to an AC-move certificate; expansion and the final check are done
// by ac_path.py / ac_check.py, NOT trusted from this program.
// Optional restriction --junction: only products whose junction cancels
// (last letter of rot(u) inverse to first letter of rot(v)^e).
//
// The search settles states in nondecreasing bottleneck (max total length on
// the path), never entering a state of total length >= cap.  It stops when
// two different sources' regions meet and prints the joining path (as the
// sequence of canonical states, one per line: "u_letters | v_letters").
//
// Usage: ac_search CAP [--junction] [--maxstates N] SRC1 SRC2 ... [+ SRC ...]
//   each SRC is "w1/w2" with letters x X y Y (X = x^-1).  A lone "+" starts a
//   new source group; only meetings between different GROUPS stop the search
//   (default: every source is its own group).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

static inline char invc(char c) { return c ^ 32; }  // x<->X, y<->Y
static string inv(const string& w) {
    string r(w.rbegin(), w.rend());
    for (auto& c : r) c = invc(c);
    return r;
}
static string freered(const string& w) {
    string o;
    for (char c : w) {
        if (!o.empty() && o.back() == invc(c)) o.pop_back(); else o.push_back(c);
    }
    return o;
}
static string cycred(string w) {
    w = freered(w);
    size_t i = 0, j = w.size();
    while (j - i >= 2 && w[i] == invc(w[j - 1])) { i++; j--; }
    return w.substr(i, j - i);
}
static string minrot(const string& w) {  // least rotation (simple O(n^2), n small)
    size_t n = w.size();
    if (n == 0) return w;
    string d = w + w, best = w;
    for (size_t k = 1; k < n; k++) {
        if (d.compare(k, n, best) < 0) best = d.substr(k, n);
    }
    return best;
}
static string canonword(const string& w) {
    string a = minrot(w), b = minrot(inv(w));
    return a < b ? a : b;
}
static string key(const string& u, const string& v) {
    string a = canonword(u), b = canonword(v);
    if (b < a) swap(a, b);
    return a + "|" + b;
}
struct Node { int src; int bott; string parent; };

int main(int argc, char** argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 2; }
    int cap = atoi(argv[1]);
    bool junction = false;
    long maxstates = 50000000;
    vector<pair<string, string>> srcs;
    vector<int> group;
    int g = 0;
    bool grouped = false;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "+")) { g++; grouped = true; continue; }
        if (!strcmp(argv[i], "--junction")) { junction = true; continue; }
        if (!strcmp(argv[i], "--maxstates")) { maxstates = atol(argv[++i]); continue; }
        string s = argv[i];
        size_t p = s.find('/');
        srcs.push_back({cycred(s.substr(0, p)), cycred(s.substr(p + 1))});
        group.push_back(g);
    }
    if (!grouped) for (size_t i = 0; i < group.size(); i++) group[i] = i;
    unordered_map<string, Node> seen;
    seen.reserve(1 << 20);
    vector<vector<string>> bucket(cap + 1);
    for (size_t i = 0; i < srcs.size(); i++) {
        string k = key(srcs[i].first, srcs[i].second);
        int L = srcs[i].first.size() + srcs[i].second.size();
        if (seen.count(k)) { printf("sources %zu coincide with an earlier one\n", i); return 0; }
        seen[k] = Node{(int)i, L, ""};
        bucket[L].push_back(k);
    }
    long settled = 0;
    vector<long> per_src(srcs.size(), 0);
    for (int level = 0; level < cap; level++) {
        // states in bucket[level] have bottleneck == level; expand them (may add to same level)
        for (size_t qi = 0; qi < bucket[level].size(); qi++) {
            string k = bucket[level][qi];
            Node nd = seen[k];
            settled++;
            per_src[nd.src]++;
            if (settled % 1000000 == 0) {
                fprintf(stderr, "settled %ld level %d seen %zu\n", settled, level, seen.size());
            }
            if ((long)seen.size() > maxstates) { printf("BUDGET exhausted at level %d, settled %ld\n", level, settled); return 3; }
            size_t bar = k.find('|');
            string w[2] = {k.substr(0, bar), k.substr(bar + 1)};
            for (int i = 0; i < 2; i++) {
                const string& a = w[i];
                const string& b0 = w[1 - i];
                for (int e = 0; e < 2; e++) {
                    string b = e ? inv(b0) : b0;
                    size_t na = a.size(), nb = b.size();
                    for (size_t ra = 0; ra < max(na, (size_t)1); ra++) {
                        string A = na ? a.substr(ra) + a.substr(0, ra) : a;
                        for (size_t rb = 0; rb < max(nb, (size_t)1); rb++) {
                            string B = nb ? b.substr(rb) + b.substr(0, rb) : b;
                            if (junction && !(na && nb && A.back() == invc(B.front()))) continue;
                            string nw = cycred(A + B);
                            int L = nw.size() + b0.size();
                            if (L >= cap) continue;
                            string k2 = key(nw, b0);
                            auto it = seen.find(k2);
                            int nb2 = max(level, L);
                            if (it == seen.end()) {
                                seen[k2] = Node{nd.src, nb2, k};
                                bucket[nb2].push_back(k2);
                            } else if (group[it->second.src] != group[nd.src]) {
                                // meeting: print both half-paths
                                printf("MEET at bottleneck %d (sources %d,%d) after %ld settled, %zu seen\n",
                                       max(nb2, it->second.bott), nd.src, it->second.src, settled, seen.size());
                                vector<string> p1, p2;
                                for (string c = k; !c.empty(); c = seen[c].parent) p1.push_back(c);
                                for (string c = k2; !c.empty(); c = seen[c].parent) p2.push_back(c);
                                reverse(p1.begin(), p1.end());
                                printf("PATH\n");
                                for (auto& s : p1) printf("%s\n", s.c_str());
                                for (auto& s : p2) printf("%s\n", s.c_str());
                                printf("END\n");
                                return 0;
                            }
                        }
                    }
                }
            }
        }
        printf("level %d done: settled %ld, seen %zu, per source:", level, settled, seen.size());
        for (auto c : per_src) printf(" %ld", c);
        printf("\n");
        fflush(stdout);
        bucket[level].clear();
        bucket[level].shrink_to_fit();
    }
    printf("EXHAUSTED below cap %d: settled %ld, no meeting\n", cap, settled);
    return 1;
}
