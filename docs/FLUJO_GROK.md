# Flujo de entrega Grok → GitHub → R2

Grok tiene acceso sólo a GitHub. Claude Code es quien sube los documentos a R2, valida los lotes y los incorpora a `main`.

## Qué hace Grok

1. Trabaja en una rama propia por lote, por ejemplo `grok/lote-a`, y nunca empuja a `main`.
2. Deja todo dentro de `inbox/<lote>/`, por ejemplo `inbox/lote-a/`:
   - `sources.csv`, `claims.csv`, `documents_manifest.csv`, `unresolved.md` y la síntesis, tal como pide [`GROK_TASKS.md`](protocolo/GROK_TASKS.md).
   - La columna `url` de `sources.csv` apunta al documento en la fuente oficial. La columna `sha256` puede quedar vacía, porque la calcula Claude Code al descargar.
3. Sólo cuando un documento no se puede descargar por URL (requiere login, captcha o ya no está publicado), Grok sube el archivo a `inbox/<lote>/documentos/` y lo menciona en `unresolved.md`.
4. Avisa que el lote está listo abriendo un pull request de la rama contra `main`.

## Qué hace Claude Code

1. Descarga cada documento desde su `url`, calcula el SHA-256 y lo sube a R2 bajo `objects/sha256/...`. Si la fuente oficial ya no lo ofrece, usa la copia de `inbox/<lote>/documentos/`.
2. Registra cada objeto en `manifests/objects.csv` con su `source_id`, y completa `sha256` y `local_object_key` en `sources.csv`.
3. Valida los CSV contra los esquemas. Los errores quedan anotados en el lote, sin corrección silenciosa.
4. Incorpora a `main` sólo texto y CSV, en un único commit (squash), sin los binarios. Después borra la rama, de modo que los PDF no quedan en la historia de `main`.

## Por qué así

- El repositorio se mantiene por debajo de 1 GB y sin Git LFS.
- Bajar el documento desde la fuente oficial, en lugar de confiar en una copia, da una procedencia verificable y una fecha de acceso real.
- Grok no necesita credenciales de R2.
