"""Validation tests for the rank-5 census code (run: python3 -m pytest test_rank5.py).
About 2 minutes; compiles the C programs into a temporary directory."""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
RANK4 = os.path.join(os.path.dirname(HERE), "rank4")
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, RANK4)
from relrank_n import delta_bounds, survivors  # noqa: E402
from run_census import endpoints, QD  # noqa: E402


@pytest.fixture(scope="module")
def bins(tmp_path_factory):
    d = tmp_path_factory.mktemp("r5bin")
    out = {}
    for name, src, r in [("sect4", os.path.join(RANK4, "sect.c"), 4), ("sectn4", "sectn.c", 4), ("sectj4", "sectj.c", 4),
                         ("sectn5", "sectn.c", 5), ("sectj5", "sectj.c", 5), ("count", "count_domain.c", None)]:
        path = str(d / name)
        cmd = ["gcc", "-O2", "-o", path, src if os.path.isabs(src) else os.path.join(HERE, src)]
        if r:
            cmd.insert(2, f"-DR={r}")
        subprocess.run(cmd, check=True)
        out[name] = path
    return out


def run(binary, n, args, env=None):
    lo, hi = endpoints(n)
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run([binary, str(n), str(lo.numerator), str(hi.numerator), str(QD), "2"] + [str(a) for a in args],
                          capture_output=True, text=True, check=True, env=e).stdout


def lines(text, drop=("ORBITSUM",)):
    return [l for l in text.splitlines() if not l.startswith(drop)]


def test_domain_count_reproduces_rank4_total(bins):
    profs = "\n".join(" ".join(map(str, s)) for s in survivors(17, 4, delta_bounds(17))) + "\n"
    out = subprocess.run([bins["count"], "17", "4"], input=profs, capture_output=True, text=True, check=True).stdout
    assert out.strip().splitlines()[-1] == "TOTAL 135937974"     # bound-rank4.md, section 4


@pytest.mark.parametrize("prof", [(3, 3, 3, 3), (3, 3, 5, 5)])
def test_new_enumerators_byte_identical_to_sect_at_rank4(bins, prof):
    ref = run(bins["sect4"], 17, prof, {"NOPRUNE": "1"})
    for b in ("sectn4", "sectj4"):
        new = run(bins[b], 17, (17,) + prof, {"NOPRUNE": "1"})
        assert lines(new) == lines(ref), b
    # with pruning: identical admitted records
    adm = [l for l in run(bins["sect4"], 17, prof).splitlines() if l.startswith("ADM")]
    for b in ("sectn4", "sectj4"):
        assert [l for l in run(bins[b], 17, (17,) + prof).splitlines() if l.startswith("ADM")] == adm


def test_rank5_leaf_count_equals_domain_and_sectj_equals_sectn(bins):
    prof = (3, 3, 3, 3, 3)
    out_n = run(bins["sectn5"], 17, (6,) + prof)
    out_j = run(bins["sectj5"], 17, (6,) + prof)
    assert [l for l in out_n.splitlines() if l.startswith("ADM")] == [l for l in out_j.splitlines() if l.startswith("ADM")]
    w = int([l for l in out_n.splitlines() if l.startswith("ORBITSUM")][0].split("leaves_weighted=")[1].split()[0])
    dp = subprocess.run([bins["count"], "6", "5"], input="3 3 3 3 3\n", capture_output=True, text=True, check=True).stdout
    assert w == int(dp.splitlines()[0].split()[1]) == 2914728
    # NOSYM: raw leaf count equals the domain too
    raw = run(bins["sectj5"], 17, (6,) + prof, {"NOSYM": "1", "NOPRUNE": "1"})
    leaves = int([l for l in raw.splitlines() if l.startswith("SUMMARY")][0].split("leaves=")[1].split()[0])
    assert leaves == 2914728


def test_negative_control_delta_matters(bins):
    """Using the smaller n = 15 delta enclosure at n = 17 must change the
    admitted set of a rank-5 profile (the Riesz test is load-bearing)."""
    prof = (3, 3, 3, 3, 5)
    good = run(bins["sectj5"], 17, (7,) + prof)
    lo, hi = endpoints(15)
    bad = subprocess.run([bins["sectj5"], "17", str(lo.numerator), str(hi.numerator), str(QD), "2", "7"] + [str(x) for x in prof],
                         capture_output=True, text=True, check=True).stdout
    na = lambda t: sum(1 for l in t.splitlines() if l.startswith("ADM"))
    assert na(bad) != na(good)
