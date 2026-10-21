"""Which stored originals can be republished, and the copy into the public bucket.

Official documents (governments, central banks, official international bodies, official
statistics and gazettes) are republished as stored. Press, private associations, academic
papers and third-party copies of official texts stay private: the public table gives their
URL and SHA-256 so a reader can check a copy they fetch themselves.
"""

from __future__ import annotations

import csv
import tempfile
from collections.abc import Iterable
from html import escape
from pathlib import Path

from argfx.storage import ObjectStore

# Lowercase fragments of the `issuer` field that mark a source as not republishable.
# Checked before anything else, so a third-party copy of an official text stays private.
THIRD_PARTY = (
    "infobae", "bloomberg", "ámbito", "el cronista", "perfil", "el destape",
    "clarín", "bae negocios", "rio times", "extra catamarca", "letra p", "eldiarioar",
    "chequeado", "tiempo de san juan", "parte de pesca", "bichos de campo", "el litoral",
    "punto federal", "urgente24", "newsdigitales", "poder360", "el argentino diario",
    "adeba", "cafci", "cámara argentina", "cámara de industria", "mercados argentina",
    "consultora", "bolsa de comercio", "nber", "levy economics", "white rose",
    "aaep", "mehrling", "unu-wider", "warren mosler", "leyes.co", "justia", "legisweb",
    "aiddata", "ifswf", "facultad de ciencias económicas", "compendio", "sin fuente",
)  # fmt: skip
# Issuers that start with these words are third parties; matched only at the start because
# "la nación" also ends many official names (Presidencia de la Nación).
THIRD_PARTY_PREFIX = ("la nación", "ciara-cec")

FIELDS = [
    "source_id", "sha256", "object_key", "media_type", "issuer", "url", "publicar", "motivo",
    "url_publica",
]  # fmt: skip


def classify(issuer: str) -> tuple[bool, str]:
    low = issuer.strip().lower()
    if not low:
        return False, "sin emisor registrado"
    if low.split(" ")[0] == "tn" or low.startswith(THIRD_PARTY_PREFIX):
        return False, "fuente de terceros"
    for frag in THIRD_PARTY:
        if frag in low:
            return False, "fuente de terceros"
    return True, "documento oficial"


def read_sources(inbox: Path) -> dict[str, dict[str, str]]:
    """First registration of each source_id across every sources.csv under the inbox."""
    out: dict[str, dict[str, str]] = {}
    for path in sorted(inbox.glob("**/sources.csv")):
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                out.setdefault(row["source_id"].strip(), row)
    return out


def build_table(
    objects_csv: Path, inbox: Path, base_url: str | None = None
) -> list[dict[str, str]]:
    sources = read_sources(inbox)
    rows: list[dict[str, str]] = []
    with objects_csv.open(encoding="utf-8") as f:
        for obj in csv.DictReader(f):
            src = sources.get(obj["source_id"], {})
            issuer = (src.get("issuer") or "").strip()
            ok, why = classify(issuer)
            public_url = f"{base_url.rstrip('/')}/{obj['object_key']}" if ok and base_url else ""
            rows.append({
                "source_id": obj["source_id"], "sha256": obj["sha256"],
                "object_key": obj["object_key"], "media_type": obj["media_type"],
                "issuer": issuer, "url": (src.get("url") or "").strip(),
                "publicar": "si" if ok else "no", "motivo": why,
                "url_publica": public_url,
            })  # fmt: skip
    return rows


def write_table(rows: Iterable[dict[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def copy_public(rows: Iterable[dict[str, str]], src: ObjectStore, dst: ObjectStore) -> int:
    """Copy each republishable object missing from `dst`; returns how many were copied."""
    copied = 0
    with tempfile.TemporaryDirectory() as tmp:
        for row in rows:
            if row["publicar"] != "si" or dst.exists(row["object_key"]):
                continue
            local = Path(tmp) / row["sha256"]
            src.download(row["object_key"], local)
            dst.upload(local, row["object_key"], row["media_type"] or None)
            local.unlink()
            copied += 1
    return copied


INDEX_KEY = "index.html"
REPO = "https://github.com/alejandroalvaro/argentina-fiscalidad-divisas"
REPORT = "https://8kgm.com.br/blog/deuda-en-dos-monedas"


def build_index(rows: Iterable[dict[str, str]], titles: dict[str, str]) -> str:
    """The landing page of the public bucket: one row per republished original.

    R2 serves no listing at the root, so this page is uploaded as `index.html` and the domain
    sends `/` to it. Third-party sources are left out, as in the bucket itself.
    """
    public = sorted(
        (r for r in rows if r["publicar"] == "si"), key=lambda r: (r["issuer"], r["source_id"])
    )
    body = "\n".join(
        "<tr>"
        f"<td class=id>{escape(r['source_id'])}</td>"
        f"<td>{escape(r['issuer'])}</td>"
        f"<td><a href=\"{escape(r['object_key'])}\">"
        f"{escape(titles.get(r['source_id'], '').strip() or r['object_key'].rsplit('/', 1)[-1])}"
        "</a></td>"
        + (f"<td><a href=\"{escape(r['url'])}\" rel=noopener>origen</a></td>" if r["url"]
           else "<td></td>")
        + f"<td class=h title=\"{escape(r['sha256'])}\">{escape(r['sha256'][:12])}</td>"
        "</tr>"
        for r in public
    )  # fmt: skip
    return INDEX_TEMPLATE.format(
        n=f"{len(public):,}".replace(",", "."), rows=body, fonts=FONTS, repo=REPO, report=REPORT
    )


FONTS = (
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600"
    "&family=DM+Sans:opsz,wght@9..40,400;9..40,500&family=IBM+Plex+Mono&display=swap"
)
INDEX_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Originales oficiales</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<style>
:root {{ --navy-dark: #0D1520; --navy-mid: #243556; --amber: #C4A46C; --amber-dim: #9E8555;
  --cream: #EDE6DA; --cream-dim: #B5A898; --heading: #F5F0E8; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--navy-dark); color: var(--cream);
  font: 400 .95rem/1.7 'DM Sans', system-ui, sans-serif; }}
nav {{ position: sticky; top: 0; z-index: 2; background: rgba(51,31,24,.95);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); }}
nav div, main, footer div {{ max-width: 1100px; margin: 0 auto; padding-left: 16px;
  padding-right: 16px; }}
nav div {{ display: flex; align-items: center; justify-content: space-between;
  padding-top: 12px; padding-bottom: 12px; }}
nav img {{ height: 28px; display: block; }}
nav a.blog {{ font-size: .85rem; color: var(--cream-dim); text-decoration: none; }}
nav a.blog:hover {{ color: var(--cream); }}
main {{ padding-top: 48px; padding-bottom: 64px; }}
.eyebrow {{ font: .75rem 'IBM Plex Mono', Consolas, monospace; letter-spacing: .1em;
  text-transform: uppercase; color: var(--amber); margin: 0 0 12px; }}
h1 {{ font: 600 2.4rem/1.15 'Fraunces', Georgia, serif; color: var(--heading);
  margin: 0 0 20px; }}
p {{ max-width: 760px; margin: 0 0 14px; }}
a {{ color: var(--amber); text-underline-offset: 3px; }}
a:hover {{ color: var(--amber-dim); }}
.lang {{ color: var(--cream-dim); font-size: .82rem; }}
input {{ width: 100%; max-width: 420px; margin: 28px 0 16px; padding: 10px 14px; font: inherit;
  color: var(--cream); background: rgba(255,255,255,.03); border: 1px solid var(--navy-mid);
  border-radius: 8px; }}
input:focus {{ outline: none; border-color: var(--amber); }}
.wrap {{ overflow-x: auto; border-top: 2px solid var(--amber); }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; vertical-align: top; padding: 9px 12px 9px 0;
  border-bottom: 1px solid var(--navy-mid); }}
td:nth-child(3) {{ overflow-wrap: anywhere; }}
td:nth-child(4) {{ white-space: nowrap; }}
th {{ font: .7rem 'IBM Plex Mono', Consolas, monospace; letter-spacing: .1em;
  text-transform: uppercase; color: var(--cream-dim); }}
td:nth-child(2) {{ color: var(--cream-dim); }}
.id, .h {{ font: .75rem 'IBM Plex Mono', Consolas, monospace; white-space: nowrap; }}
.id {{ color: var(--amber); }}
.h {{ color: var(--cream-dim); }}
footer {{ border-top: 1px solid var(--navy-mid); padding: 40px 0 56px; color: var(--cream-dim);
  font-size: .85rem; }}
footer img {{ height: 24px; display: block; margin-bottom: 12px; }}
@media (max-width: 640px) {{
  h1 {{ font-size: 1.9rem; }}
  td:nth-child(2), th:nth-child(2), td:nth-child(5), th:nth-child(5) {{ display: none; }}
}}
</style>
</head>
<body>
<nav><div>
<a href="https://8kgm.com.br/"><img src="https://8kgm.com.br/logos/8kgm-logo.svg" alt="8KGM"></a>
<a class=blog href="{report}">Informe</a>
</div></nav>
<main>
<p class=eyebrow>datos.8kgm.com.br</p>
<h1>Originales oficiales</h1>
<p>Copia de los {n} documentos oficiales que usa el informe
<a href="{report}">«La deuda en dos monedas»</a>. Cada archivo está guardado tal como se bajó,
bajo su huella SHA-256, de modo que cualquiera puede comprobar que es el mismo que publicó el
emisor.</p>
<p>Los documentos de terceros (prensa, trabajos académicos, cámaras privadas) quedan afuera.
La tabla <a href="{repo}/blob/main/manifests/publicacion.csv">publicacion.csv</a> da la dirección
de origen y la huella de todos, y el código que reproduce los cálculos está en
<a href="{repo}">el repositorio</a>.</p>
<p class=lang>PT: cópia dos documentos oficiais citados no relatório, guardados sob o hash SHA-256
de cada um. EN: copies of the official documents cited in the report, stored under their SHA-256
hash.</p>
<input id=q type=search placeholder="Buscar por emisor, título o código" aria-label="Buscar">
<div class=wrap>
<table>
<thead><tr><th>Fuente</th><th>Emisor</th><th>Documento</th><th>Origen</th><th>SHA-256</th></tr></thead>
<tbody id=t>
{rows}
</tbody>
</table>
</div>
</main>
<footer><div>
<img src="https://8kgm.com.br/logos/8kgm-logo-amber.svg" alt="8KGM">
datos.8kgm.com.br · Grupo 8
</div></footer>
<script>
const q = document.getElementById('q'), rows = [...document.querySelectorAll('#t tr')];
q.addEventListener('input', () => {{
  const s = q.value.trim().toLowerCase();
  for (const r of rows) r.hidden = s && !r.textContent.toLowerCase().includes(s);
}});
</script>
</body>
</html>
"""
