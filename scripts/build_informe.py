"""Assemble the report: informe/*.md + docs/GLOSARIO.md -> data/informe/informe.html.

Needs pandoc. The Sankey pages from `argfx flujos` must sit next to the output, since
the chapters embed them with `<iframe src="flujos_....html">`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
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


def build(src: Path, glossary: Path, out: Path, date: str) -> Path:
    parts = [p.read_text(encoding="utf-8") for p in chapters(src)]
    parts.append(glossary.read_text(encoding="utf-8"))
    body = "\n\n".join(parts)
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
            "--metadata=title:La deuda en dos monedas",
            "--metadata=subtitle:Pesos y dólares de la deuda pública argentina, 2023-2026",
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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=ROOT / "informe")
    ap.add_argument("--glosario", type=Path, default=ROOT / "docs" / "GLOSARIO.md")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "informe" / "informe.html")
    ap.add_argument("--fecha", default="17-10-2026")
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    print(build(a.src, a.glosario, a.out, a.fecha))


if __name__ == "__main__":
    main()
