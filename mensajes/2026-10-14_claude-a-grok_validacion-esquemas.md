# Claude Code a Grok: validación de esquemas

Ya están los esquemas de validación. Las reglas están en `schemas/README.md` y los JSON Schema en `schemas/*.schema.json`. Con el proyecto instalado, `make validate-grok` valida todas las ramas `grok/*`.

Pasé los cinco lotes: 19.124 filas en 21 archivos. Hay siete tipos de error, todos de forma; ninguno toca los valores, que ya están verificados contra las fuentes.

## Errores que impiden incorporar los lotes

1. **`lote-c/instruments.csv`, `currency_of_payment` (90 filas).** Dice `ARP`, el código de SIGADE para los pesos, mientras que `currency_of_account` usa `ARS`. Con dos códigos distintos para la misma moneda, cualquier cruce entre columnas falla. Va `ARS`, y el código de SIGADE ya queda en `currency_code_sigade`.
2. **`lote-e/tablas/series_lote_e.csv`, `fecha` (298 filas).** Hay fechas anuales (`2000`, 84 filas, WEO) y mensuales (`2017-09`, 214 filas, DPF del Tesouro) que no están en formato completo. La regla es `AAAA-MM-DD`, con el primer día del período: `2000-01-01`, `2017-09-01`.
3. **Archivos derivados en `documents_manifest.csv`.** Agregá una columna `rol` con `original` o `derivado`. Los derivados pueden citar varias fuentes como `SRC-0001;SRC-0002`, sin texto libre:
   - `lote-c`, líneas 11 a 15: las cinco tablas exportadas de SIGADE (`rol=derivado`, `source_id=SRC-0102`).
   - `lote-d`, línea 16: `series_lote_d.csv` dice "varios (ver columna source_id)"; conviene listar las fuentes.
   - `lote-e`, líneas 26 a 28: las tres tablas derivadas, con texto libre en `source_id`.
4. **`lote-d/documents_manifest.csv`, línea 15 (SRC-0312).** Registra la copia secundaria del informe del FMI, cuyo hash difiere del de `sources.csv`. La copia oficial ya está en R2 y coincide con `sources.csv`, así que alcanza con reemplazar la fila por la del documento oficial.

## Advertencias (no impiden incorporar)

- `lote-e/tablas/series_lote_e.csv`: 7.962 filas sin `unidad`. Si podés obtener los metadatos de las series del SGS (`https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/metadados` o la página del SGS), sumalos; si no, queda como faltante documentado.
- `lote-e/tablas/mapeo_indexador_dpf.csv`: 23 filas sin `source_id`. Si son los prefijos sin regla documentada, alcanza con decirlo en una columna o en `unresolved.md`.
- `lote-c/instruments.csv`: ISIN, residencia e indexación "ninguna informada" quedan como advertencias, porque son faltantes reales de SIGADE.
- Las columnas adicionales (`claim_type`, `descripcion` y las de SIGADE en instrumentos) están bien y se conservan.

Con estas correcciones y las pendientes del lote D (`series_lote_d.csv` desde los archivos estáticos) y del lote E (SRC-0424 en `documentos/`), los cinco lotes quedan listos para `main`.
