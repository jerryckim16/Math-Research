// Build-time LaTeX renderer for site/build.py.
// Reads one JSON object per line on stdin: {"tex": "...", "display": true|false}
// and writes one JSON line per input: {"html": "...", "error": null | "message"}.
// The page then needs only KaTeX's CSS and fonts, no JavaScript, and the reader
// never sees raw LaTeX source.
const katex = require("katex");
const readline = require("readline");

const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on("line", (line) => {
  const { tex, display } = JSON.parse(line);
  let out;
  try {
    out = { html: katex.renderToString(tex, { displayMode: display, throwOnError: true, output: "htmlAndMathml" }), error: null };
  } catch (e) {
    // fall back to KaTeX's own error rendering so the page still builds; build.py reports it
    out = { html: katex.renderToString(tex, { displayMode: display, throwOnError: false }), error: String(e.message || e) };
  }
  process.stdout.write(JSON.stringify(out) + "\n");
});
