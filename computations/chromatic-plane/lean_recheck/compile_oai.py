"""Compile the OAI Lean files against the locally built Mathlib, in dependency
order, with up to 4 parallel `lean` processes. Usage: compile_oai.py OAICHECK_DIR MATHLIB_DIR"""
import os, re, subprocess, sys, time
root, mathlib = map(os.path.abspath, sys.argv[1:3])
out = os.path.join(root, "build")
mods = {}
for d, _, fs in os.walk(os.path.join(root, "OAI")):
    for f in fs:
        if f.endswith(".lean"):
            p = os.path.join(d, f)
            m = os.path.relpath(p, root)[:-5].replace("/", ".")
            mods[m] = [i for i in re.findall(r"^import\s+([\w.]+)", open(p).read(), re.M) if i.startswith("OAI.")]
env = dict(os.environ)
lp = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=mathlib, capture_output=True, text=True).stdout.strip()
env["LEAN_PATH"] = lp + ":" + out
done, running, failed = set(), {}, []
t0 = time.time()
def start(m):
    src = os.path.join(root, m.replace(".", "/") + ".lean")
    ol = os.path.join(out, m.replace(".", "/") + ".olean")
    os.makedirs(os.path.dirname(ol), exist_ok=True)
    log = open(os.path.join(out, m + ".log"), "w")
    return subprocess.Popen(["lean", "-R", root, "-o", ol, src], cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT), time.time()
pending = set(mods)
while pending or running:
    for m in sorted(pending):
        if len(running) >= 4: break
        if all(d in done for d in mods[m]) and not any(d in failed for d in mods[m]):
            running[m] = start(m); pending.discard(m)
    time.sleep(1)
    for m, (p, ts) in list(running.items()):
        if p.poll() is not None:
            del running[m]
            if p.returncode == 0:
                done.add(m); print(f"OK   {m} {time.time()-ts:.0f}s", flush=True)
            else:
                failed.append(m); print(f"FAIL {m} rc={p.returncode}", flush=True)
    if failed and not running:
        break
    if not running and pending and not any(all(d in done for d in mods[m]) for m in pending):
        break
print(f"done {len(done)}/{len(mods)} failed {failed} wall {time.time()-t0:.0f}s", flush=True)
