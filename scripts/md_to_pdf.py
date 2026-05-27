"""Converte arquivo Markdown em PDF usando Edge headless.

Uso:
    python scripts/md_to_pdf.py <arquivo.md> [arquivo.pdf]
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from html import escape

import markdown

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm; }
body {
    font-family: 'Segoe UI', 'Calibri', 'Helvetica', sans-serif;
    font-size: 11.5pt;
    line-height: 1.55;
    color: #1a1a1a;
    max-width: none;
}
h1 {
    color: #6b1a1a;
    border-bottom: 3px solid #6b1a1a;
    padding-bottom: 6px;
    margin-top: 0;
    page-break-after: avoid;
}
h2 {
    color: #6b1a1a;
    margin-top: 26px;
    page-break-after: avoid;
}
h3 {
    color: #444;
    margin-top: 20px;
    page-break-after: avoid;
}
h4 { color: #555; margin-top: 16px; }
p { text-align: justify; }
code {
    background: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 10pt;
    font-family: 'Consolas', 'Courier New', monospace;
}
pre {
    background: #f4f4f4;
    border-left: 3px solid #6b1a1a;
    padding: 10px 12px;
    overflow-x: auto;
    page-break-inside: avoid;
}
pre code { background: none; padding: 0; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 14px 0;
    page-break-inside: avoid;
    font-size: 10.5pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 7px 10px;
    text-align: left;
    vertical-align: top;
}
th { background: #f4ece8; color: #6b1a1a; font-weight: 600; }
blockquote {
    border-left: 4px solid #c2a878;
    padding: 8px 14px;
    color: #555;
    background: #faf6f0;
    margin: 12px 0;
}
ul, ol { padding-left: 22px; }
li { margin: 3px 0; }
a { color: #6b1a1a; text-decoration: none; }
.cover {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 16px;
    border-bottom: 2px solid #6b1a1a;
}
.cover h1 { border: none; padding: 0; }
.cover .subtitle { color: #888; margin-top: 6px; font-size: 12pt; }
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def find_edge() -> str:
    candidates = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    raise SystemExit("Edge/Chrome nao encontrado. Instale um deles ou ajuste o caminho.")


def md_to_html(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    title = md_path.stem
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()

    body_html = markdown.markdown(
        text,
        extensions=["extra", "tables", "fenced_code", "sane_lists", "toc"],
    )
    return HTML_TEMPLATE.format(title=escape(title), css=CSS, body=body_html)


def html_to_pdf(html: str, pdf_path: Path) -> None:
    edge = find_edge()
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        html_path = Path(f.name)

    try:
        pdf_path = pdf_path.resolve()
        cmd = [
            edge,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            raise SystemExit(f"Falha ao gerar PDF em {pdf_path}")
    finally:
        try:
            html_path.unlink()
        except OSError:
            pass


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    md_path = Path(sys.argv[1]).resolve()
    if not md_path.exists():
        raise SystemExit(f"Arquivo nao encontrado: {md_path}")
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else md_path.with_suffix(".pdf")

    print(f"[md_to_pdf] {md_path} -> {pdf_path}")
    html = md_to_html(md_path)
    html_to_pdf(html, pdf_path)
    size_kb = pdf_path.stat().st_size / 1024
    print(f"[md_to_pdf] OK ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
