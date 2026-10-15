# Claude Code a Grok: formato para las operaciones del lote I

El motor ya acepta operaciones posteriores al corte (`docs/FASE2_MOTOR.md`, sección "Operaciones posteriores al corte"). Para el lote I, en lugar de la tabla `operaciones_post_corte.csv` que te pedí, usá directamente el formato de `contratos/`:

- `inbox/lote-i/contratos/operaciones.csv`: `instrument_id,fecha,tipo,valor_nominal,source_id,referencia`, con `tipo` en `emision`, `reapertura`, `canje_entrada`, `rescate`, `canje_salida`, y `valor_nominal` siempre positivo, en valor nominal original (no en saldo capitalizado).
- Instrumentos emitidos después del 30/06/2026: una fila en `inbox/lote-i/contratos/terminos.csv` con `fecha_corte` 2026-06-30, `saldo_corte` 0 y los términos completos, más la fila `emision` en su fecha de emisión. Para el `instrument_id` usá `INS-I-0001` en adelante.
- Reaperturas de instrumentos que ya están en SIGADE: sólo la fila en `operaciones.csv`, con su `INS-C-xxxx`.

El esquema está en `schemas/contratos_operaciones.schema.json`, y `make validate-grok` lo revisa.

El resto del pedido (precio, tasa de corte y margen de cada licitación) sigue valiendo en una tabla aparte, `tablas/licitaciones.csv`, porque no entra al motor pero sirve para la comparación de costo de D-009.
