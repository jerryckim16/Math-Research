"""Build the progress website from the repository contents.

Usage: python3 site/build.py [output_dir]   (default: _site)

Reads problems/*.md, notes/*.md, README.md and the git history, and writes a
static site. The GitHub Actions workflow .github/workflows/pages.yml runs it on
every push to main and publishes the result with GitHub Pages.
"""
import datetime as dt
import html
import os
import re
import subprocess
import sys
from pathlib import Path

import json
import shutil

import markdown
from markdown.extensions.toc import slugify as _slugify

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_site")
REPO = os.environ.get("GITHUB_REPOSITORY", "jerryckim16/Math-Research")
REPO_URL = f"https://github.com/{REPO}"
BRANCH = "main"


def git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def last_updated(path):
    out = git("log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT)))
    return out.strip() or "uncommitted"


def history(n=30):
    out = git("log", f"-{n}", "--no-merges", "--format=%H%x1f%cs%x1f%s")
    rows = []
    for line in out.splitlines():
        sha, date, subject = line.split("\x1f")
        files = git("show", "--name-only", "--format=", sha).split()
        rows.append((sha, date, subject, files))
    return rows


def meta(text):
    def field(name):
        m = re.search(rf"^\*\*{name}:\*\*\s*(.+)$", text, re.M)
        return m.group(1).strip() if m else ""
    title = re.search(r"^#\s+(.+)$", text, re.M)
    return {
        "title": title.group(1).strip() if title else "Untitled",
        "area": field("Area"),
        "status": field("Status"),
        "started": field("Started"),
        "proofatlas": field("ProofAtlas"),
    }


def section(text, heading):
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def status_class(status):
    s = status.lower()
    for key in ("solved", "abandoned", "progress", "open"):
        if key in s:
            return key
    return "open"


def fix_links(text, depth):
    """Point .md links at generated pages and other repo paths at GitHub."""
    up = "../" * depth

    def repl(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"[a-z]+://|#|mailto:", target):
            return m.group(0)
        clean = target.lstrip("./")
        for prefix in ("problems/", "notes/"):
            if clean.startswith(prefix) and clean.endswith(".md"):
                return f"[{label}]({up}{clean[:-3]}.html)"
        if clean.endswith(".md") and "/" not in clean and depth == 1:
            return f"[{label}]({clean[:-3]}.html)"
        return f"[{label}]({REPO_URL}/blob/{BRANCH}/{clean})"

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, text)


MATH_RE = re.compile(r"(\$\$.+?\$\$|\\\[.+?\\\]|\\\(.+?\\\)|(?<![\\$\w])\$(?=\S)[^$\n]+?(?<=\S)\$(?![\w$]))", re.S)
CODE_RE = re.compile(r"(```.*?```|`[^`\n]+`)", re.S)


def protect_math(text):
    """Replace LaTeX math spans by placeholders so Markdown does not mangle them
    (underscores, asterisks, backslashes). Code spans are left untouched."""
    stash = []

    def keep(m):
        stash.append(m.group(0))
        return f"MATHPH{len(stash) - 1}ZZ"

    parts = CODE_RE.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = MATH_RE.sub(keep, parts[i])
        for line in parts[i].splitlines():
            if re.search(r"(?<!\\)\$", line):   # a $ that is not part of a recognised math span
                STRAY.append(line.strip()[:120])
    return "".join(parts), stash


class KaTeX:
    """Renders LaTeX to HTML at build time with KaTeX (site/katex_render.js, via
    node and site/node_modules; `npm ci --prefix site` installs it). Readers then
    get finished math: no raw $...$ while a script loads, and nothing breaks if a
    CDN is blocked. Without node or KaTeX the build falls back to rendering in the
    browser with KaTeX's auto-render script."""
    DIST = ROOT / "site" / "node_modules" / "katex" / "dist"

    def __init__(self):
        self.proc, self.cache, self.errors = None, {}, []
        if self.DIST.is_dir() and shutil.which("node"):
            self.proc = subprocess.Popen(["node", str(ROOT / "site" / "katex_render.js")], cwd=ROOT / "site",
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
        else:
            print("warning: node or site/node_modules/katex missing; math will be rendered in the browser", file=sys.stderr)

    def render(self, src):
        for left, right, display in (("$$", "$$", True), ("\\[", "\\]", True), ("\\(", "\\)", False), ("$", "$", False)):
            if src.startswith(left) and src.endswith(right) and len(src) >= len(left) + len(right):
                tex = src[len(left):len(src) - len(right)]
                break
        key = (tex, display)
        if key not in self.cache:
            self.proc.stdin.write(json.dumps({"tex": tex, "display": display}) + "\n")
            self.proc.stdin.flush()
            res = json.loads(self.proc.stdout.readline())
            if res["error"]:
                self.errors.append(f"{src[:80]!r}: {res['error']}")
            self.cache[key] = res["html"]
        return self.cache[key]


KATEX = None
STRAY = []   # lines with a lone "$" (e.g. "$x$s": math touching a letter is not recognised); fix the source


def restore_math(html_text, stash):
    if KATEX and KATEX.proc:
        return re.sub(r"MATHPH(\d+)ZZ", lambda m: KATEX.render(stash[int(m.group(1))]), html_text)
    return re.sub(r"MATHPH(\d+)ZZ", lambda m: html.escape(stash[int(m.group(1))], quote=False), html_text)


TEX_WORDS = {r"\tau": "τ", r"\le": "≤", r"\ge": "≥", r"\leq": "≤", r"\geq": "≥", r"\times": "×", r"\cdot": "·"}


def tex_to_text(s):
    """Plain-text version of a title for <title>, where math cannot be rendered."""
    def plain(m):
        tex = m.group(1)
        tex = re.sub(r"\\(?:mathrm|mathbf|text|operatorname)\{([^}]*)\}", r"\1", tex)
        for k, v in TEX_WORDS.items():
            tex = re.sub(re.escape(k) + r"(?![A-Za-z])", v, tex)
        return re.sub(r"[{}]|\\,", "", tex).replace("_", "")
    return re.sub(r"\$([^$]+)\$", plain, s)


def widen_list_indent(text):
    """The sources nest lists with 2-space indents; Python-Markdown needs 4.
    Double the leading spaces of every indented line that belongs to a list
    (list items and their continuation lines), outside fenced code."""
    out, in_fence, in_list, fence_ind = [], False, False, 0
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            # fenced_code only recognises fences at column 0: dedent fences
            # nested in list items (they then render as a block after the item)
            if not in_fence:
                fence_ind = len(line) - len(line.lstrip(" "))
                if out and out[-1].strip():
                    out.append("")
            in_fence = not in_fence
            out.append(line[fence_ind:] if line[:fence_ind].strip() == "" else line)
            if not in_fence:
                out.append("")
            continue
        if in_fence:
            out.append(line[fence_ind:] if line[:fence_ind].strip() == "" else line)
            continue
        stripped = line.lstrip(" ")
        ind = len(line) - len(stripped)
        if re.match(r"([-*+]|\d+[.)])\s", stripped):
            # Python-Markdown needs a blank line between a paragraph and a list
            if ind == 0 and not in_list and out and out[-1].strip() and not out[-1].lstrip().startswith("|"):
                out.append("")
            in_list = True
        elif not stripped:
            pass
        elif ind == 0:
            in_list = False
        out.append(" " * (2 * ind) + stripped if in_list and ind else line)
    return "\n".join(out)


def slug(value, separator):
    """Heading anchors from the words only (math placeholders dropped)."""
    return _slugify(re.sub(r"MATHPH\d+ZZ", "", value), separator)


def render_md(text, depth):
    # keep the "**Field:** value" header lines on separate lines
    text = re.sub(r"^(\*\*(?:Area|Status|Started|ProofAtlas):\*\*.*)$", r"\1  ", text, flags=re.M)
    text, stash = protect_math(text)
    text = fix_links(widen_list_indent(text), depth)
    out = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "toc"],
                            extension_configs={"toc": {"slugify": slug}})
    return restore_math(out, stash)


CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1f;--muted:#6b6b70;--card:#fff;--line:#e4e2dc;--accent:#3b5bdb;
--open:#868e96;--progress:#e67700;--solved:#2b8a3e;--abandoned:#c92a2a;--code:#f1efe9}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#ececef;--muted:#9a9aa2;--card:#1d1d21;
--line:#2e2e34;--accent:#8ea2ff;--code:#26262c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
.wrap{max-width:920px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line);padding:18px 0}
header .wrap{display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
header a.brand{font-weight:700;font-size:18px;color:var(--fg);text-decoration:none}
header nav a{color:var(--muted);margin-right:14px;text-decoration:none;font-size:15px}
header nav a:hover{color:var(--accent)}
main{padding:28px 0 60px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px}
h2{font-size:21px;margin:36px 0 12px}
h3{font-size:17px}
a{color:var(--accent)}
.lede{color:var(--muted);margin:0 0 24px;max-width:680px}
.cards{display:grid;gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.card h3{margin:0 0 6px;font-size:18px}
.card h3 a{color:var(--fg);text-decoration:none}
.card h3 a:hover{color:var(--accent)}
.meta{color:var(--muted);font-size:14px;display:flex;flex-wrap:wrap;gap:4px 14px}
.badge{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.02em;padding:2px 8px;border-radius:99px;color:#fff;white-space:nowrap}
.badge.open{background:var(--open)}.badge.progress{background:var(--progress)}
.badge.solved{background:var(--solved)}.badge.abandoned{background:var(--abandoned)}
.next{margin:10px 0 0;font-size:14.5px}
.next b{font-weight:600}
table{border-collapse:collapse;width:100%;font-size:14.5px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{font-weight:600;white-space:nowrap}
.katex{font-size:1.1em}
code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:.9em}
pre{background:var(--code);padding:12px;border-radius:8px;overflow-x:auto}
pre code{padding:0}
.activity{list-style:none;padding:0;margin:0}
.activity li{display:grid;grid-template-columns:96px 1fr;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14.5px}
.activity .date{color:var(--muted);font-variant-numeric:tabular-nums}
.activity .tags{color:var(--muted);font-size:13px}
.doc{max-width:760px}
footer{color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding:18px 0}
"""


def page(title, body, depth=0, desc="Live progress on open math problems"):
    up = "../" * depth
    built = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(tex_to_text(title))}</title>
<meta name="description" content="{html.escape(desc)}">
<style>{CSS}</style>
{math_head(up)}
</head>
<body><header><div class="wrap"><a class="brand" href="{up}index.html">Math Research</a>
<nav><a href="{up}index.html#problems">Problems</a><a href="{up}index.html#activity">Activity</a><a href="{up}notes/ai-feasible-open-problems.html">Shortlist</a><a href="{REPO_URL}">GitHub</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">Built {built} from <a href="{REPO_URL}">{REPO}</a>. Evidence labels follow the repository's working rules: a bounded computation is never a proof.</div></footer>
</body></html>"""


def math_head(up):
    if KATEX and KATEX.proc:   # math already rendered: only KaTeX's stylesheet and fonts, served with the site
        return f'<link rel="stylesheet" href="{up}katex/katex.min.css">'
    return """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\\\[',right:'\\\\]',display:true},{left:'\\\\(',right:'\\\\)',display:false},{left:'$',right:'$',display:false}],ignoredTags:['script','noscript','style','textarea','pre','code'],throwOnError:false})"></script>"""


def first_bullet(text):
    m = re.search(r"^\s*-\s+(.+)$", text, re.M)
    return m.group(1).strip().rstrip(":") if m else ""


def inline(text):
    text, stash = protect_math(text)
    return restore_math(markdown.markdown(text), stash).removeprefix("<p>").removesuffix("</p>")


def build():
    global KATEX
    KATEX = KaTeX()
    OUT.mkdir(parents=True, exist_ok=True)
    if KATEX.proc:
        shutil.copytree(KaTeX.DIST / "fonts", OUT / "katex" / "fonts", dirs_exist_ok=True)
        shutil.copy(KaTeX.DIST / "katex.min.css", OUT / "katex" / "katex.min.css")
    (OUT / "problems").mkdir(exist_ok=True)
    (OUT / "notes").mkdir(exist_ok=True)
    (OUT / ".nojekyll").write_text("")

    problems = []
    for p in sorted((ROOT / "problems").glob("*.md")):
        if p.name == "TEMPLATE.md":
            continue
        text = p.read_text()
        m = meta(text)
        m.update(slug=p.stem, updated=last_updated(p), next=first_bullet(section(text, "Next steps")))
        problems.append(m)
        body = f'<div class="doc">{render_md(text, 1)}<p class="meta">Last updated {m["updated"]} · ' \
               f'<a href="{REPO_URL}/blob/{BRANCH}/problems/{p.name}">source</a> · ' \
               f'<a href="{REPO_URL}/commits/{BRANCH}/problems/{p.name}">history</a></p></div>'
        (OUT / "problems" / f"{p.stem}.html").write_text(page(m["title"], body, depth=1))

    for n in sorted((ROOT / "notes").rglob("*.md")):
        rel = n.relative_to(ROOT / "notes")
        depth = len(rel.parts)
        text = n.read_text()
        title = meta(text)["title"]
        body = f'<div class="doc">{render_md(text, depth)}<p class="meta">Last updated {last_updated(n)} · ' \
               f'<a href="{REPO_URL}/blob/{BRANCH}/notes/{rel.as_posix()}">source</a></p></div>'
        dest = OUT / "notes" / rel.with_suffix(".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(title, body, depth=depth))

    problems.sort(key=lambda m: m["updated"], reverse=True)
    cards = []
    for m in problems:
        meta_bits = [f'<span class="badge {status_class(m["status"])}">{html.escape(m["status"].split("(")[0].strip() or "open")}</span>']
        for label in ("area", "started", "proofatlas"):
            if m[label]:
                meta_bits.append(f'<span>{label.capitalize() if label != "proofatlas" else "ProofAtlas"}: {inline(m[label])}</span>')
        meta_bits.append(f'<span>Updated {m["updated"]}</span>')
        detail = ""
        if "(" in m["status"]:
            detail += f'<p class="next">{inline(m["status"][m["status"].index("(") + 1:].rstrip(")"))}</p>'
        if m["next"]:
            detail += f'<p class="next"><b>Next:</b> {inline(m["next"])}</p>'
        cards.append(f'<div class="card"><h3><a href="problems/{m["slug"]}.html">{html.escape(m["title"])}</a></h3>'
                     f'<div class="meta">{"".join(meta_bits)}</div>{detail}</div>')
    if not cards:
        cards.append('<div class="card">No problems yet.</div>')

    items = []
    for sha, date, subject, files in history():
        touched = sorted({f.split("/")[0] + ("/" + f.split("/")[1].removesuffix(".md") if f.startswith(("problems/", "notes/")) and "/" in f else "")
                          for f in files})
        items.append(f'<li><span class="date">{date}</span><span><a href="{REPO_URL}/commit/{sha}">{html.escape(subject)}</a>'
                     f'<br><span class="tags">{html.escape(", ".join(touched[:6]))}</span></span></li>')

    body = f"""<h1>Open problems, attacked in the open</h1>
<p class="lede">An AI-assisted research log. Each problem page states the exact claim, what has been tried, what failed,
and how strong the evidence is for each result: proved, Lean-verified, certificate-checked, computed up to N, or heuristic.
New work lands here automatically as it is merged.</p>
<h2 id="problems">Problems</h2><div class="cards">{''.join(cards)}</div>
<h2 id="activity">Recent activity</h2><ul class="activity">{''.join(items) or '<li>No commits yet.</li>'}</ul>"""
    (OUT / "index.html").write_text(page("Math Research progress", body))
    print(f"built {len(problems)} problem pages into {OUT}")
    for line in STRAY:
        print("  warning: unrendered $ in:", line, file=sys.stderr)
    if KATEX.proc:
        KATEX.proc.stdin.close()
        KATEX.proc.wait()
        print(f"math rendered at build time: {len(KATEX.cache)} distinct expressions, {len(KATEX.errors)} errors")
        for e in KATEX.errors:
            print("  KaTeX error:", e, file=sys.stderr)


if __name__ == "__main__":
    build()
