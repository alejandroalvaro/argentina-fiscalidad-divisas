# Argentina: fiscalidad en divisas y restricción externa

Infraestructura reproducible para una investigación académica sobre la percepción de derechos de exportación en divisas y su efecto sobre la liquidez externa del Tesoro argentino. Brasil entra como referencia comparativa acotada.

El diseño de la investigación está en [`docs/protocolo/`](docs/protocolo/). Conviene empezar por el [protocolo de investigación](docs/protocolo/RESEARCH_PROTOCOL.md) y el [protocolo de auditoría](docs/protocolo/AUDIT_PROTOCOL.md).

## Dónde vive cada cosa

| Lugar | Contenido |
|---|---|
| GitHub (este repositorio) | Código, Markdown, tests y manifiestos CSV pequeños. Objetivo: menos de 1 GB. |
| R2, bucket `argentina-fx-research` (privado) | Documentos originales, Parquet y snapshots, guardados bajo su SHA-256. |
| `data/` local | Caché DuckDB y copias verificadas. Se puede borrar y regenerar. |

Los documentos originales son inmutables. Cada archivo se guarda en `objects/sha256/ab/cd/<sha256>` y se registra en [`manifests/objects.csv`](manifests/), que sí entra en Git. Así cada versión del repositorio apunta a un conjunto exacto de fuentes.

## Puesta en marcha

Hace falta Python 3.11 o superior y [uv](https://docs.astral.sh/uv/).

```bash
make install            # crea .venv e instala dependencias
cp .env.example .env    # completar con el token S3 de R2
make config             # muestra la configuración, sin secretos
make storage-check      # escribe, lista, lee y borra un objeto de prueba
make check              # ruff + pytest
```

Los tests funcionan sin red y sin credenciales: usan un almacén local y un S3 simulado.

## Comandos

```bash
uv run argfx ingest prospecto.pdf --source-id SRC-0001   # guarda por hash y registra en el manifiesto
uv run argfx fetch <sha256> destino.pdf                   # descarga y verifica el hash
```

Si el archivo ya existe en R2, `ingest` no lo vuelve a subir ni duplica la fila del manifiesto.

## Estructura

```
src/argfx/     código (configuración, hashing, almacenamiento, manifiestos, DuckDB, CLI)
tests/         pruebas offline
schemas/       esquemas de los lotes de Grok (fase 1)
scripts/       tareas puntuales que todavía no forman parte del CLI
manifests/     manifiestos versionados que apuntan a objetos en R2
docs/          protocolo de investigación y documentación técnica
```

## Fases

- [x] Fase 0: repositorio, almacenamiento R2, caché DuckDB, tests offline
- [ ] Fase 1: ingesta y validación de los lotes de Grok
- [ ] Fase 2: motor contractual de flujos de deuda
- [ ] Fase 3: reconciliación con series oficiales
- [ ] Fase 4: simulación de los tres regímenes
- [ ] Fase 5: manuscrito reproducible

## Seguridad

Las credenciales viven sólo en `.env` local o en secretos de CI. El token de R2 tiene permiso de lectura y escritura sobre este bucket y nada más. Ningún documento con licencia restrictiva se publica antes de revisar sus derechos.
