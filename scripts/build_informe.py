"""Assemble the report: informe/*.md + docs/GLOSARIO.md -> data/informe/informe.html, and with
--docx also informe.docx.

Needs pandoc. The Sankey pages from `argfx flujos` and the charts from `argfx graficos` must sit
next to the output, since the chapters embed them with `<iframe src="....html">`. For Word, each
embedded page is captured as an image with headless Chrome.

The first time a glossary acronym appears in the text it links to its entry.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSS = """
:root { --ink:#20293A; --paper:#FFF7EB; --gold:#E1B53E; --muted:#8B8580; --rule:#e6dccb;
  --font-display:'Fraunces',Georgia,serif; --font-body:'DM Sans',system-ui,sans-serif;
  --font-mono:'IBM Plex Mono',Consolas,monospace; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ink:#FFF7EB; --paper:#1A1A1A; --muted:#C4B8A8; --rule:#3d2a20; } }
:root[data-theme="dark"] { --ink:#FFF7EB; --paper:#1A1A1A; --muted:#C4B8A8; --rule:#3d2a20; }
html { background:var(--paper); }
body { background:var(--paper); color:var(--ink); font-family:var(--font-body); font-size:15px;
  line-height:1.7; max-width:820px; margin:0 auto; padding:24px 16px 80px; }
h1,h2,h3 { font-family:var(--font-display); font-weight:600; line-height:1.2; }
h1 { font-size:2.1rem; margin-top:3rem; border-top:2px solid var(--gold); padding-top:1rem; }
h2 { font-size:1.45rem; margin-top:2.2rem; } h3 { font-size:1.15rem; }
header.title-block h1 { border:none; margin-top:1rem; font-size:2.5rem; }
.subtitle { font-family:var(--font-display); font-style:italic; font-weight:300; }
table { border-collapse:collapse; width:100%; font-size:13.5px; margin:1rem 0; display:block;
  overflow-x:auto; }
th,td { border-bottom:1px solid var(--rule); padding:5px 8px; text-align:left; vertical-align:top; }
th { font-weight:600; }
code { font-family:var(--font-mono); font-size:12.5px; }
blockquote { border-left:3px solid var(--gold); margin:1rem 0; padding:.2rem 1rem;
  color:var(--muted); }
iframe.sankey { width:100%; height:560px; border:1px solid var(--rule); border-radius:8px;
  background:#fff; }
iframe.grafico { width:100%; height:500px; border:1px solid var(--rule); border-radius:8px;
  background:#fff; }
a.glosario { color:inherit; text-decoration:underline dotted; text-underline-offset:3px; }
div.destacado { border:1px solid var(--gold); border-left:4px solid var(--gold); border-radius:8px;
  padding:.4rem 1.1rem; margin:1.2rem 0 1.6rem; background:rgba(225,181,62,.08); }
div.destacado p:first-child { font-family:var(--font-display); font-size:1.15rem;
  line-height:1.35; }
div.destacado p:last-child { color:var(--muted); font-size:13.5px; }
nav#TOC { font-size:13.5px; border:1px solid var(--rule); border-radius:8px; padding:8px 16px; }
nav#TOC ul { padding-left:18px; } a { color:#4E80EE; }
footer { margin-top:4rem; color:var(--muted); font-size:12px; }
"""

FONTS = (
    "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;"
    "0,9..144,600;1,9..144,300&family=DM+Sans:opsz,wght@9..40,400;9..40,600"
    "&family=IBM+Plex+Mono&display=swap"
)


def chapters(src: Path) -> list[Path]:
    return sorted(p for p in src.glob("*.md") if re.match(r"\d\d_", p.name))


IFRAME = re.compile(
    r'<iframe class="(sankey|grafico)" src="([^"]+)\.html" title="([^"]+)"></iframe>'
)
ENTRY = re.compile(r"^\*\*(.+?)\.\*\*", re.M)
ACRONYM = re.compile(r"\b[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9]+\b")
SKIP_TERMS = {"SRC", "USD", "DE", "Y"}


def slug(text: str) -> str:
    plain = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode().lower()
    return "g-" + re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


def glossary_with_anchors(glossary: str) -> tuple[str, dict[str, str]]:
    """Give each entry an anchor and map every acronym in its title to it."""
    terms: dict[str, str] = {}

    def anchor(m: re.Match[str]) -> str:
        title = m.group(1)
        sid = slug(title)
        for term in ACRONYM.findall(title):
            if term not in SKIP_TERMS:
                terms.setdefault(term, sid)
        return f"[**{title}.**]{{#{sid}}}"

    return ENTRY.sub(anchor, glossary), terms


def link_first_uses(body: str, terms: dict[str, str]) -> str:
    """Link the first use of each acronym in running text: not in headings, tables, captions,
    embedded pages or code."""
    pending = dict(terms)
    out = []
    for line in body.splitlines():
        if not pending or line.startswith(("#", "|", "<", "*Fuente", "*Gráfico", "*Diagrama",
                                           "*Cuadro", "    ", "```", ">")):  # fmt: skip
            out.append(line)
            continue

        def repl(m: re.Match[str], line: str = line) -> str:
            term = m.group(0)
            before = line[: m.start()]
            # Inside a code span or an existing link target: leave it.
            if before.count("`") % 2 or before.endswith(("[", "(#", "/")) or term not in pending:
                return term
            return f"[{term}](#{pending.pop(term)}){{.glosario}}"

        out.append(ACRONYM.sub(repl, line))
    return "\n".join(out)


TITLE = "La deuda en dos monedas"
SUBTITLE = "Pesos y dólares de la deuda pública argentina, 2023-2026"


def assemble(src: Path, glossary: Path) -> str:
    gloss, terms = glossary_with_anchors(glossary.read_text(encoding="utf-8"))
    parts = [p.read_text(encoding="utf-8") for p in chapters(src)]
    return link_first_uses("\n\n".join(parts), terms) + "\n\n" + gloss


def build(src: Path, glossary: Path, out: Path, date: str) -> Path:
    body = assemble(src, glossary)
    head = (
        f"<link rel='stylesheet' href='{FONTS}'>\n<style>{CSS}</style>\n"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
    )
    header = out.parent / "_head.html"
    header.write_text(head, encoding="utf-8")
    after = out.parent / "_after.html"
    after.write_text(
        f"<footer>Borrador del {date}. Generado con scripts/build_informe.py desde "
        "informe/*.md y docs/GLOSARIO.md.</footer>",
        encoding="utf-8",
    )
    subprocess.run(
        [
            "pandoc",
            "--from=markdown",
            "--to=html5",
            "--standalone",
            "--toc",
            "--toc-depth=1",
            f"--metadata=title:{TITLE}",
            f"--metadata=subtitle:{SUBTITLE}",
            f"--metadata=date:Borrador del {date}",
            "--metadata=lang:es",
            f"--include-in-header={header}",
            f"--include-after-body={after}",
            "-o",
            str(out),
        ],
        input=body,
        text=True,
        check=True,
    )
    header.unlink()
    after.unlink()
    return out


CHROME = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
)
WINDOW = {"sankey": "1400,760", "grafico": "900,500"}


def capture(page: Path, kind: str, png: Path) -> None:
    """Screenshot an embedded page with headless Chrome, at twice the resolution."""
    chrome = next((c for c in CHROME if Path(c).exists() or shutil.which(c)), None)
    if chrome is None:
        raise SystemExit("hace falta Google Chrome o Chromium para pasar los gráficos a imagen")
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", "--virtual-time-budget=8000",
         f"--window-size={WINDOW[kind]}", f"--screenshot={png}", page.resolve().as_uri()],
        check=True, capture_output=True,
    )  # fmt: skip
    if not png.is_file():
        raise SystemExit(f"no se pudo capturar {page}")


def build_docx(src: Path, glossary: Path, out: Path, date: str) -> Path:
    """The same text in Word, with every embedded page as an image."""
    pages = out.parent
    with tempfile.TemporaryDirectory() as tmp:

        def image(m: re.Match[str]) -> str:
            kind, name, _ = m.groups()
            png = Path(tmp) / f"{name}.png"
            capture(pages / f"{name}.html", kind, png)
            return f"![]({png}){{width=100%}}"

        body = IFRAME.sub(image, assemble(src, glossary))
        if "<iframe" in body:
            raise SystemExit("quedó un iframe sin convertir")
        subprocess.run(
            ["pandoc", "--from=markdown", "--to=docx", "--toc", "--toc-depth=1",
             f"--metadata=title:{TITLE}", f"--metadata=subtitle:{SUBTITLE}",
             f"--metadata=date:Borrador del {date}", "--metadata=lang:es-AR", "-o", str(out)],
            input=body, text=True, check=True,
        )  # fmt: skip
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=ROOT / "informe")
    ap.add_argument("--glosario", type=Path, default=ROOT / "docs" / "GLOSARIO.md")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "informe" / "informe.html")
    ap.add_argument("--fecha", default="18-10-2026")
    ap.add_argument("--docx", action="store_true", help="also write informe.docx next to it")
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    print(build(a.src, a.glosario, a.out, a.fecha))
    if a.docx:
        print(build_docx(a.src, a.glosario, a.out.with_suffix(".docx"), a.fecha))


if __name__ == "__main__":
    main()
