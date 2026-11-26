"""Tests for the gate251 pipeline (run: python3 -m pytest test_gate251.py; about 2 min).

The full pipeline (covergen | expand | xcascq | xcascq, per-shard checks and
the cascade_verify re-check) is run end to end on small gates; the production
code paths are the same, only k and p differ.
"""
import json
import os
import subprocess

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
LR = os.path.dirname(HERE)


@pytest.fixture(scope="module")
def bins(tmp_path_factory):
    d = tmp_path_factory.mktemp("g251bin")
    out = {}
    for name, src, extra in [("xcasc", os.path.join(LR, "midp17", "xcasc.c"), []),
                             ("xcascq", os.path.join(HERE, "xcascq.c"), []),
                             ("xcascq_nong", os.path.join(HERE, "xcascq.c"), ["-DNO_NG"]),
                             ("expand", os.path.join(HERE, "expand.c"), [])]:
        subprocess.run(["gcc", "-O2"] + extra + ["-o", str(d / name), src], check=True)
        out[name] = str(d / name)
    return out


def gate(tmp_path, k, p, nsh, depth):
    env = dict(os.environ, K=str(k), NSH=str(nsh), DEPTH=str(depth), JOBS="2")
    subprocess.run(["bash", os.path.join(HERE, "run_gate251.sh"), str(tmp_path), str(p)], env=env,
                   capture_output=True, text=True, check=True)
    D = tmp_path / f"p{p}"
    recs = [json.load(open(D / f"shard_{i}.json")) for i in range(nsh) if (D / f"shard_{i}.json").exists()]
    finished = [l.split()[0] for l in open(D / "times.txt")] if (D / "times.txt").exists() else []
    failed = open(D / "failed.txt").read() if (D / "failed.txt").exists() else ""
    return recs, finished, failed


def hist(recs):
    h = {}
    for r in recs:
        for a, n in r["closed_hist"].items():
            h[a] = h.get(a, 0) + n
    return h


def test_small_gate_closes_and_is_shard_invariant(tmp_path):
    """(k, p) = (8, 67): every shard passes every check, every base closes,
    and the totals do not depend on the sharding (4 depth-2 shards against 3
    depth-4 shards)."""
    a, fa, xa = gate(tmp_path / "a", 8, 67, 4, 2)
    b, fb, xb = gate(tmp_path / "b", 8, 67, 3, 4)
    assert not xa and not xb and len(fa) == 4 and len(fb) == 3
    assert all(r["ok"] for r in a + b)
    assert sum(r["bases"] for r in a) == sum(r["bases"] for r in b) > 0
    assert sum(r["minimal_covers"] for r in a) == sum(r["minimal_covers"] for r in b)
    assert hist(a) == hist(b)
    assert sum(r["recheck"]["per_base"] for r in a) > 0     # cascade_verify really ran


def test_negative_control_nonclosing_prime(tmp_path):
    """(7, 43): some bases do not close by level 36 (the tight orbit (1..7)
    among them), so the gate must be reported as failed."""
    recs, fin, failed = gate(tmp_path, 7, 43, 2, 2)
    assert failed and len(fin) < 2
    assert "verify_failed" in failed or "check_failed" in failed


def test_xcascq_normal_mode_identical_to_xcasc(bins, tmp_path):
    bases = "\n".join(open(os.path.join(HERE, "data", "p251_level9_bases.txt")).read().split("\n")[:8]) + "\n"
    strip = lambda t: [l.split('"sec"')[0] for l in t.splitlines()]
    for chain in ("2", "3,3,2,2"):
        a = subprocess.run([bins["xcasc"], "17", "251", chain], input=bases, capture_output=True, text=True, check=True).stdout
        b = subprocess.run([bins["xcascq"], "17", "251", chain], input=bases, capture_output=True, text=True, check=True).stdout
        assert strip(a) == strip(b) and a


def test_negative_control_lemma_s_off(bins):
    """At p = 251 the bases that close at level 9 need Lemma S: with it they
    close at 9, without it (-DNO_NG) none closes by 36."""
    bases = open(os.path.join(HERE, "data", "p251_level9_bases.txt")).read()
    env = dict(os.environ, XC_QUIET="1")
    on = subprocess.run([bins["xcascq"], "17", "251", "3,3,2,2"], input=bases, capture_output=True, text=True, env=env, check=True)
    off = subprocess.run([bins["xcascq_nong"], "17", "251", "3,3,2,2"], input=bases, capture_output=True, text=True, env=env, check=True)
    n = len([l for l in bases.splitlines() if l.strip()])
    assert f"XCSUM bases {n} open 0 " in on.stderr and f"hist 9:{n}" in on.stderr
    assert f"XCSUM bases {n} open {n} " in off.stderr


def test_expand_count_and_truncated_line(bins):
    from math import comb
    covers = "1 2 3\n1 5\n"
    out = subprocess.run([bins["expand"], "5", "11"], input=covers, capture_output=True, text=True, check=True)
    h = 5
    assert len(out.stdout.splitlines()) == comb(h + 5 - 1 - 3, 5 - 3) + comb(h + 5 - 1 - 2, 5 - 2)
    assert all(l.split() == sorted(l.split(), key=int) for l in out.stdout.splitlines())
    bad = subprocess.run([bins["expand"], "5", "11"], input="1 2 3\n1 5", capture_output=True, text=True)
    assert bad.returncode == 1                                  # a truncated last line is rejected
