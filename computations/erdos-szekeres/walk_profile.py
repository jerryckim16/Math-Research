"""Per-depth Knuth estimates and per-walk hardness ratios for nested static-split probes.

Usage: python3 walk_profile.py static33_s11_*.jsonl static33_s12_*.jsonl

Files are cube_sample.py outputs (--order static --nested ...). Walks are
identified by (file tag "sNN", path index): the same seed and index give the
same walk at every depth. Knuth totals mix caps; any timed-out cube makes the
total a LOWER bound (marked ">="). r(d1->d2) = (t(d1)/t(d2))^(1/(d2-d1)) is
the per-decision hardness ratio along one walk (">=" if t(d1) timed out).
"""
import glob
import json
import random
import re
import sys

YR = 31557600


def main():
    recs = []
    for f in sys.argv[1:]:
        m = re.search(r"_s(\d+)_", f)
        tag = int(m.group(1)) if m else 0
        for line in open(f):
            r = json.loads(line)
            r["seed"] = tag
            recs.append(r)
    by = {}
    for r in recs:
        by.setdefault(r["depth"], []).append(r)
    for d in sorted(by):
        rs = by[d]
        c = [r["weight"] * r["time"] for r in rs]
        to = sum(r["status"] == "TIMEOUT" for r in rs)
        est = sum(c) / len(c)
        rng = random.Random(0)
        boots = sorted(sum(rng.choice(c) for _ in c) / len(c) for _ in range(2000))
        lb = ">=" if to else ""
        print(f"depth {d}: n={len(rs)} timeouts={to} Knuth total {lb}{est / YR:.3g} CPU-yr "
              f"[bootstrap 5-95%: {lb}{boots[100] / YR:.3g} .. {lb}{boots[1899] / YR:.3g}]; "
              f"largest probe {max(c) / sum(c):.0%}")
    walks = {}
    for r in recs:
        walks.setdefault((r["seed"], r["path"]), {})[r["depth"]] = r
    for k, w in sorted(walks.items()):
        ds = sorted(w)
        line = f"walk s{k[0]}p{k[1]}: " + "; ".join(
            f"d{d} {'>=' if w[d]['status'] == 'TIMEOUT' else ''}{w[d]['time']:.1f}s (w=2^{w[d]['weight'].bit_length() - 1})"
            for d in ds)
        for a, b in zip(ds, ds[1:]):
            if w[b]["status"] == "UNSAT":
                line += f" | r({a}->{b}) {'>=' if w[a]['status'] == 'TIMEOUT' else ''}{(w[a]['time'] / w[b]['time']) ** (1 / (b - a)):.2f}"
        print(line)


if __name__ == "__main__":
    main()
