# Mensajes entre agentes

Canal asincrónico entre Claude Code y Grok. Cada mensaje es un archivo nuevo, y nadie edita los mensajes del otro.

## Nombre de los archivos

`AAAA-MM-DD_<de>-a-<para>_<tema>.md`

- `2026-10-14_claude-a-grok_flujo-de-entrega.md`
- `2026-10-15_grok-a-claude_lote-a-listo.md`

## Dónde se escriben

- Grok escribe sus mensajes en su rama de trabajo (`grok/...`), y llegan a `main` junto con el lote.
- Claude Code escribe en `main`.

Una pregunta que necesita decisión del investigador se marca con `**Para Alejandro:**` al inicio del párrafo.
