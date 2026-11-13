"""Render the Markdown reports to styled, print-ready PDFs.

How: Markdown -> HTML (python-markdown) -> PDF (headless Google Chrome's
built-in "print to PDF"). No LaTeX needed.

Usage (from the 05-typology-reports folder):
    .venv/bin/python tools/build_pdfs.py                # all reports in this folder
    .venv/bin/python tools/build_pdfs.py path/to/x.md   # specific files -> next to each file

Front matter (optional, at the top of a .md file):
    ---
    title: "..."
    subtitle: "..."
    date: "..."
    ---
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]

CSS = """
@page { size: A4; margin: 16mm 16mm 16mm 16mm; }
@page landscape { size: A4 landscape; margin: 9mm 10mm; }
:root { --ink:#14213d; --muted:#5c677d; --accent:#b5432b; --rule:#d9dee7; --band:#f3f5f9; }
* { box-sizing: border-box; }
body { font-family: "Source Serif 4", Georgia, "Times New Roman", serif; color: var(--ink);
       font-size: 10.4pt; line-height: 1.45; margin: 0; background: #fff; }
.masthead { border-bottom: 3px solid var(--accent); padding-bottom: 8px; margin-bottom: 14px; }
.kicker { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; text-transform: uppercase;
          letter-spacing: .12em; font-size: 7.8pt; color: var(--accent); font-weight: 700; }
h1.title { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 19pt;
           line-height: 1.15; margin: 4px 0 2px; }
.subtitle { color: var(--muted); font-size: 11pt; margin: 0; }
.date { font-family: -apple-system, Helvetica, Arial, sans-serif; color: var(--muted); font-size: 8.5pt; margin-top: 4px; }
h2 { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13pt; margin: 18px 0 6px;
     padding-bottom: 3px; border-bottom: 1px solid var(--rule); break-after: avoid; }
h3 { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11pt; margin: 12px 0 4px; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 18px; margin: 4px 0 8px; }
li { margin: 2px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 8.9pt; line-height: 1.35;
        font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; break-inside: auto; }
th { background: var(--ink); color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; }
td { border-bottom: 1px solid var(--rule); padding: 5px 6px; vertical-align: top; }
tr:nth-child(even) td { background: var(--band); }
tr { break-inside: avoid; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 8.6pt; background: var(--band); padding: 0 3px; border-radius: 3px; }
pre { background: var(--band); border-left: 3px solid var(--accent); padding: 8px 10px; font-size: 7.9pt;
      line-height: 1.3; overflow: hidden; white-space: pre; break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { margin: 8px 0; padding: 6px 12px; border-left: 3px solid var(--accent); background: #fbf3f1; font-size: 9.6pt; }
a { color: #1d4ed8; text-decoration: none; word-break: break-all; }
h2#sources + p, h2#sources ~ p { font-size: 8.4pt; line-height: 1.38; }
.footer-note { margin-top: 14px; font-size: 7.8pt; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 6px; }
/* tighter layout for the 2-3 page findings memo */
@page memo { size: A4; margin: 13mm 14mm; }
body.memo { page: memo; font-size: 9.4pt; line-height: 1.38; }
body.memo h2 { font-size: 11.5pt; margin: 12px 0 4px; }
body.memo h3 { font-size: 10pt; margin: 9px 0 3px; }
body.memo table { font-size: 8.2pt; margin: 5px 0 8px; }
body.memo td, body.memo th { padding: 3px 5px; }
body.memo p { margin: 5px 0; }
/* compact one-page layout for the cheat sheet */
body.compact { font-size: 8.2pt; line-height: 1.3; }
body.compact { page: landscape; }
body.compact .masthead { margin-bottom: 6px; padding-bottom: 4px; }
body.compact h1.title { font-size: 14pt; }
body.compact h3 { font-size: 9pt; margin: 6px 0 2px; }
body.compact table { font-size: 7.4pt; margin: 4px 0 6px; }
body.compact td, body.compact th { padding: 3px 4px; }
body.compact ul, body.compact ol { margin: 2px 0 4px; }
body.compact li { margin: 0; }
body.compact .cols { column-count: 2; column-gap: 18px; }
"""


def chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    sys.exit("Google Chrome/Chromium not found - install it or edit CHROME_CANDIDATES.")


def split_front_matter(text: str):
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def linkify(html_text: str) -> str:
    # Turn bare URLs in the Sources list into clickable links.
    return re.sub(r'(?<!["=>])(https?://[^\s<;)]+)', r'<a href="\1">\1</a>', html_text)


def render(md_path: Path, out_pdf: Path, kicker: str) -> None:
    meta, body = split_front_matter(md_path.read_text(encoding="utf-8"))
    compact = "cheat" in md_path.stem
    memo = "MEMO" in md_path.stem.upper()
    # Each "[n] source" line on its own line (markdown would otherwise join them).
    body = re.sub(r"^(\[\d+\] .*)$", r"\1  ", body, flags=re.M)
    body_html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    body_html = linkify(body_html)
    if compact:  # put the two trailing sections side by side to fit one page
        body_html = body_html.replace("<h3", '<div class="cols"><h3', 1) + "</div>"
    head = (f'<div class="masthead"><div class="kicker">{html.escape(kicker)}</div>'
            f'<h1 class="title">{html.escape(meta.get("title", md_path.stem))}</h1>'
            + (f'<p class="subtitle">{html.escape(meta["subtitle"])}</p>' if meta.get("subtitle") else "")
            + (f'<div class="date">{html.escape(meta["date"])}</div>' if meta.get("date") else "")
            + "</div>")
    doc = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(meta.get('title', ''))}</title>"
           f"<style>{CSS}</style></head><body class='{'compact' if compact else ('memo' if memo else '')}'>{head}{body_html}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc)
        tmp = f.name
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", f"file://{tmp}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Path(tmp).unlink(missing_ok=True)
    print(f"  {out_pdf.relative_to(out_pdf.parents[1])}")


def main():
    args = [Path(a).resolve() for a in sys.argv[1:]]
    if args:
        for p in args:
            render(p, p.with_suffix(".pdf"), "Financial crime analysis · public sources")
        return
    for p in sorted(ROOT.glob("0[1-4]_*.md")):
        render(p, ROOT / "pdf" / (p.stem + ".pdf"), "Sanctions evasion typology series")


if __name__ == "__main__":
    main()
