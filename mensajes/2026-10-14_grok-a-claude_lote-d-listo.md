# Grok a Claude Code: lote D listo

El lote D (series externas) está en `inbox/lote-d/`: 13 fuentes, 11 afirmaciones y dos tablas derivadas en `tablas/`.

- SRC-0312 es una copia secundaria del Country Report 26/105 del FMI. La URL oficial devolvió 403 desde mi entorno; conviene bajar la oficial y comparar el hash.
- Las URL de datos.gob.ar y de la API del BCRA devuelven datos vivos, así que el hash cambiará en cada descarga. `series_lote_d.csv` congela lo que bajé el 14/10/2026.

**Para Alejandro:** el TMU del FMI no descuenta los depósitos en divisas del Tesoro al calcular las reservas netas. Conviene decidir qué definición de reservas netas usará el paper antes de la fase 3.
