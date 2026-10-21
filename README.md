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
inbox/         entregas de Grok, sólo en sus ramas (ver docs/FLUJO_GROK.md)
mensajes/      mensajes entre Claude Code y Grok
docs/          protocolo de investigación y documentación técnica
```

## Fases

- [x] Fase 0: repositorio, almacenamiento R2, caché DuckDB, tests offline
- [x] Fase 1: ingesta y validación de los lotes de Grok
- [x] Fase 2: motor contractual de flujos de deuda
- [x] Fase 3: reconciliación con series oficiales
- [x] Fase 4: simulación de los regímenes
- [ ] Fase 5: manuscrito reproducible (tercer borrador en `informe/`)

## Seguridad

Las credenciales viven sólo en `.env` local o en secretos de CI. El token de R2 tiene permiso de lectura y escritura sobre este bucket y nada más. Ningún documento con licencia restrictiva se publica antes de revisar sus derechos.

## Datos públicos

Los documentos originales oficiales (1.074 de 1.214) se pueden bajar de https://datos.8kgm.com.br, cuya portada los lista con buscador, con la misma clave que en el bucket privado: `objects/sha256/<aa>/<bb>/<huella>`. La tabla `manifests/publicacion.csv` da, para cada original, la fuente, la URL de origen, la huella sha256 y la dirección pública. Los 140 documentos de terceros (prensa, trabajos académicos, cámaras privadas, copias en sitios de terceros) no se reproducen; la tabla da su URL y su huella. `argfx publicar` regenera la tabla y, con `--copiar`, sube al bucket público los originales oficiales que falten y la portada `index.html`, con un token propio de ese bucket (`R2_PUBLIC_ACCESS_KEY_ID`, `R2_PUBLIC_SECRET_ACCESS_KEY`, `R2_PUBLIC_BASE_URL`).

## Licencias

Código: MIT (`LICENSE`). Textos, documentación y tablas propias: CC BY 4.0 (`LICENSE-CONTENIDO.md`). Los documentos originales son de sus emisores.
