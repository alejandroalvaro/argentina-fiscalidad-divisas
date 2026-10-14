# Esquemas

Aquí van los esquemas de los lotes que entrega Grok (`sources.csv`, `claims.csv`, `documents_manifest.csv` e instrumentos candidatos). Se definen en la fase 1 como modelos Pydantic en `src/argfx/` y se exportan a JSON Schema en esta carpeta, para que Grok y cualquier revisor puedan validar un lote sin instalar el proyecto.

Las columnas mínimas están en [`docs/protocolo/GROK_TASKS.md`](../docs/protocolo/GROK_TASKS.md).
