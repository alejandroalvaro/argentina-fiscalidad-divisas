# Manifiestos

Los manifiestos conectan Git con R2. Cada fila apunta a un objeto inmutable por su SHA-256, de modo que un commit fija exactamente qué fuentes usaba el proyecto en ese momento.

## `objects.csv`

Lo genera `argfx ingest`. Una fila por hash; si el mismo archivo se ingiere dos veces, la fila no se duplica.

| Columna | Contenido |
|---|---|
| `sha256` | Hash del contenido, identidad del objeto |
| `size_bytes` | Tamaño en bytes |
| `object_key` | Clave en R2: `objects/sha256/ab/cd/<sha256>` |
| `media_type` | Tipo MIME deducido de la extensión; vacío si no se conoce |
| `original_filename` | Nombre del archivo al momento de la ingesta |
| `source_id` | Vínculo con `sources.csv` de Grok; vacío si todavía no hay |
| `ingested_at` | Fecha y hora UTC de la ingesta (ISO 8601) |

Un campo vacío significa "desconocido", nunca cero.
