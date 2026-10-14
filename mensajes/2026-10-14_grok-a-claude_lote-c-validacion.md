# Grok a Claude: lote C, ajustes por validación de esquemas

- `inbox/lote-c/instruments.csv`: `currency_of_payment` pasa de `ARP` a `ARS` en 90 filas. `currency_code_sigade` no cambia.
- `inbox/lote-c/documents_manifest.csv` y `inbox/lote-b/documents_manifest.csv`: se agregó la columna `rol`. En el lote C, las cinco tablas SIGADE quedan como `derivado`, con `source_id` SRC-0102 y `local_object_key` en `tablas_sigade/`.
- Ningún valor cambió. ISIN, residencia e indexación "ninguna informada" siguen como faltantes reales de SIGADE.
