# Grok a Claude: lote K

Rama `grok/lote-k`, carpeta `inbox/lote-k/`. Fuentes SRC-0945 a SRC-0985 (las de Claude desde SRC-1900 no se tocan). Todo `sin_revisar`. Originales fuera de la rama, con sha256 en `documents_manifest.csv`. Detalle y huecos en `inbox/lote-k/unresolved.md` y `sintesis.md`.

## Qué respondí

1. **TMG27 y TMF27:** no encontré canje, conversión ni rescate entre 2026-04-15 y 2026-06-30 (ni hasta 2026-08-31) en ONCP, en OPC de abril a agosto ni en los resultados de Finanzas. La baja existe (TMF27: 3.906.522 contra 4.391.522 millones, 485.000 exactos al 2026-09-11) pero no hay operación que la explique. No cargué filas en `operaciones.csv`.
2. **BONAR Dual 2036 (INS-C-0357):** cargado en `terminos.csv`, `tasas.csv` y `duales.csv` (seis tramos, USD 640.874.451 exactos con TCI 350,6425576018, `tablas/bonar_dual_2036_*.csv`). Puntos abiertos: emisión 2023-10-20 (ONCP) contra 2023-09-29 (estructura y SIGADE), día de cupón 29 contra 20, si el máximo rige también en el capital, base 30/360 supuesta, y no encontré el texto de la RC 53/2023.
3. **TTD26:** la cadena publicada da 4.624.064 millones, 0,11% sobre los 4.618.994 derivados (`tablas/ttd26_vno_publicado.csv`).
4. **Conversiones con el BCRA:** montos de RC 39, 49 y 51 en `tablas/conversiones_bcra_2026.csv`; RC 53 y 60 solo con topes; no hay SIGADE al 2026-09-30.
5. **Rezago del CER:** `tablas/cer_rezago_verificacion.csv`. Verificados 11 de 17 (saldo SIGADE por CER del día de emisión contra VNO publicado, diferencia relativa menor a 2 por millón). Sin verificar: INS-C-0373, 0379, 0380, 0386, 0387 y 0388. No modifiqué filas de ids existentes.

## Validación

`argfx validate` real sobre main más `lote-k`: 1 error y 2.273 advertencias, iguales a main solo (el error es INS-I-0007 de lote-i). `argfx calendario --corte 2026-06-30` con las filas nuevas genera 22 flujos de INS-C-0357 que no coinciden con SIGADE (diferencia relativa máxima 1,57).

## Para Alejandro

- El lote K no cambia ninguna cifra existente. Lo que falta para cerrar TMF27 y TMG27, los tres CER sin verificar y la RC 53/2023 está en `unresolved.md`.

## Para Claude

- Para los 11 BONCER y LETES CER verificados, `rezago_habiles` = 10, `indice_inicial` = CER del día de emisión e `indice_base` = CER del décimo día hábil anterior, con día hábil igual a día con A 3500 publicado. La tabla trae ambos valores. Esa definición es mía.
- El factor de la rama CER del dual es TCI sobre el CER base de la norma (136,4111244672), porque el motor no aplica rezago en la segunda pata. Si la norma lo define distinto, el factor cambia (alternativas en `unresolved.md`, punto 2, incisos a y f).
- ¿Querés que cargue las filas de `terminos.csv` de los 11 verificados, o las incorporás vos desde la tabla?
