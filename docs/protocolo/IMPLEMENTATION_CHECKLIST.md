# Tareas del investigador — puesta en marcha

## Accesos (no compartir secretos en chats)
- [ ] Crear repositorio privado `argentina-fiscalidad-divisas` en GitHub, sin datos grandes.
- [ ] Dar a Claude Code acceso de lectura/escritura al repositorio; permisos mínimos.
- [ ] Crear bucket privado `argentina-fx-research` en Cloudflare R2 Standard.
- [ ] Crear token S3 compatible restringido al bucket; guardar en gestor de secretos o `.env` local excluido de Git.
- [ ] Elegir máquina de ejecución y carpeta local para caché DuckDB/Parquet.
- [ ] Configurar segundo respaldo independiente de R2, con prueba de restauración.
- [ ] Crear proyecto Grok y cargar `GROK_TASKS.md` y `RESEARCH_PROTOCOL.md`.
- [ ] Crear proyecto Claude Code y cargar `CLAUDE_CODE_TASKS.md`, `AUDIT_PROTOCOL.md` y protocolo de investigación.
- [ ] Verificar que los agentes pueden intercambiar CSV/JSONL y manifiestos; no concederles acceso innecesario a credenciales.

## Primera aceptación
- [ ] Un documento fuente descargado con hash, metadatos y respaldo.
- [ ] Un título con calendario calculado y verificado manualmente.
- [ ] Un lote Grok validado por esquema sin correcciones manuales silenciosas.
- [ ] Primera conciliación contra un agregado oficial, con discrepancias visibles.
- [ ] Una corrida de prueba de los tres escenarios con identidades SFC consistentes.

## Reglas de almacenamiento
GitHub: código, Markdown, pequeños CSV de manifiesto y tests; objetivo operativo <1 GB de repositorio. R2: PDF, fuentes, Parquet y snapshots. Local: caché DuckDB regenerable. No usar Git LFS por defecto. Datos y documentos originales privados hasta revisión de derechos de publicación.
