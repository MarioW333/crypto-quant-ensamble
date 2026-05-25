"""Build REPORT.pdf from REPORT.md (text + tables + figures).

Requirements (build-time only, not needed to run the notebook):
    pip install markdown xhtml2pdf
Run from anywhere:
    python report/build_pdf.py
"""
import os, matplotlib
import markdown
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')

# Register a Unicode font so symbols (★ → σ ≈ ≤ × −) render correctly
pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(FONT_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Oblique', os.path.join(FONT_DIR, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold',
                              italic='DejaVu-Oblique', boldItalic='DejaVu-Bold')

CSS = """
@page { size: A4 portrait; margin: 1.8cm 1.7cm; }
body { font-family: DejaVu; font-size: 9.5pt; line-height: 1.45; color: #1b1b1b; }
h1 { font-family: DejaVu; font-size: 19pt; color: #111; margin: 0 0 2pt 0; }
h2 { font-family: DejaVu; font-size: 13.5pt; color: #14365c; margin: 16pt 0 4pt 0;
     border-bottom: 1pt solid #14365c; padding-bottom: 2pt; }
h3 { font-family: DejaVu; font-size: 11pt; color: #14365c; margin: 11pt 0 3pt 0; }
p, li { font-size: 9.5pt; }
em { color: #444; }
code { font-family: Courier; font-size: 8.5pt; background-color: #f3f3f3; }
hr { border: none; border-top: 0.5pt solid #ccc; margin: 8pt 0; }
table { -pdf-keep-with-next: true; border-collapse: collapse; width: 100%;
        margin: 6pt 0; font-size: 8.3pt; }
th { background-color: #14365c; color: #fff; border: 0.5pt solid #14365c;
     padding: 3pt 5pt; font-weight: bold; }
td { border: 0.5pt solid #bbb; padding: 3pt 5pt; }
"""

def link_callback(uri, rel):
    # Resolve relative paths (figures/*.png) against the report/ directory
    if uri.startswith(('http://', 'https://')):
        return uri
    path = os.path.join(HERE, uri)
    return path if os.path.exists(path) else uri

def main():
    md_text = open(os.path.join(HERE, 'REPORT.md'), encoding='utf-8').read()
    body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'sane_lists'])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    out = os.path.join(HERE, 'REPORT.pdf')
    with open(out, 'wb') as f:
        result = pisa.CreatePDF(html, dest=f, link_callback=link_callback, encoding='utf-8')
    if result.err:
        raise SystemExit(f'PDF build had {result.err} error(s)')
    print('Built', out, f'({os.path.getsize(out)/1e6:.2f} MB)')

if __name__ == '__main__':
    main()
