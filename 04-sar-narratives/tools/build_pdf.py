"""Render the SAR case files and the guide to PDF: markdown → styled HTML → headless Chrome.

    ../03-transaction-monitoring/.venv/bin/python tools/build_pdf.py
Requires the `markdown` package and Google Chrome (macOS path below, or set CHROME env var).
"""
import os
import subprocess
import tempfile
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parents[1]
PDF = HERE / "pdf"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
DOCS = [("HOW_TO_WRITE_A_SAR_NARRATIVE.md", "00_How_to_Write_a_SAR_Narrative"),
        ("cases/SAR-01_structuring.md", "SAR-01_Structuring"),
        ("cases/SAR-02_mule_network.md", "SAR-02_Mule_Network"),
        ("cases/SAR-03_tbml_gulf_freezone.md", "SAR-03_TBML_Gulf_FreeZone")]

CSS = """
@page { size: Letter; margin: 16mm 15mm 18mm 15mm; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; font-size: 10pt; line-height: 1.45; color: #1b1b1b; }
h1 { font-size: 17pt; color: #0d2c54; border-bottom: 2px solid #0d2c54; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 12.5pt; color: #0d2c54; margin-top: 18px; border-bottom: 1px solid #d5dbe3; padding-bottom: 2px; }
h3 { font-size: 11pt; color: #0d2c54; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 8.6pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #0d2c54; color: #fff; text-align: left; padding: 4px 6px; }
td { border-bottom: 1px solid #e3e7ec; padding: 3px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #f6f8fa; }
blockquote { margin: 10px 0; padding: 10px 14px; background: #f3f6fa; border-left: 4px solid #0d2c54; font-family: Georgia, 'Times New Roman', serif; font-size: 10pt; }
blockquote:first-of-type { background: #fff4e5; border-left-color: #c77700; font-family: inherit; font-size: 9pt; }
code { background: #eef1f4; padding: 0 3px; border-radius: 3px; font-size: 9pt; }
.banner { position: running(header); }
.foot { margin-top: 24px; font-size: 8pt; color: #777; border-top: 1px solid #ddd; padding-top: 4px; }
"""


def to_html(md_text: str, title: str) -> str:
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head>"
            f"<body>{body}<div class='foot'>FICTIONAL / SYNTHETIC training material, not a real SAR filing. "
            f"Meridian Harbor Bank is fictional.</div></body></html>")


def print_pdf(html: str, out: Path):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", f"file://{tmp}"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(tmp)


def main():
    PDF.mkdir(exist_ok=True)
    parts = []
    for src, name in DOCS:
        text = (HERE / src).read_text()
        # relative links to CSVs don't work inside a PDF; keep the text, drop nothing
        print_pdf(to_html(text, name), PDF / f"{name}.pdf")
        parts.append(text)
        print("wrote", PDF / f"{name}.pdf")
    combined = "\n\n<div style='page-break-before: always'></div>\n\n".join(parts)
    print_pdf(to_html(combined, "SAR Narratives Portfolio"), PDF / "SAR_Narratives_Portfolio.pdf")
    print("wrote", PDF / "SAR_Narratives_Portfolio.pdf")


if __name__ == "__main__":
    main()
