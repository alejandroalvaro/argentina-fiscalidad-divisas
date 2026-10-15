# Grok a Claude Code: lote I3 (términos de los cinco instrumentos y conversiones con el BCRA)

Rama `grok/lote-i3` (sale de main 910e0c1). Todo `sin_revisar`. Sin PDF ni html en la rama; los originales retenidos (RC 28, 32 y 35, y los JSON de CER y Com. A 3500 del 25-05 al 12-06) están en la caja en `/workspace/lote_I3/`, con sha256 en `sources.csv` (SRC-0909 a SRC-0913) y filas `original` en el manifiesto, para que los subas a R2.

## Qué trae `inbox/lote-i3/`

- `contratos/terminos.csv` (6 filas): INS-C-0408 (TXMD9) e INS-C-0409 (TXMD8) como CER cupón cero con `indice_inicial` 779,88639312623 (CER del 2026-05-29, décimo día hábil anterior a la emisión del 2026-06-12, calendario con Com. A 3500); INS-C-0629 (D31L6, emisión 2026-05-29, RC 28 art. 2) e INS-C-0630 (D31G6, emisión 2026-06-12, RC 32 art. 1) como letras dólar linked cupón cero pagaderas en pesos; INS-C-0446 (RC 35 art. 1) flotante a la tasa de reservas del BCRA con `tope_indice` `SOFR_TERM_1A` y `tope_margen` -0,0028487; INS-I-0010 (letra intransferible de 15-09-2031, RC 54 y 57), que el lote I dejaba sin identificador. Los `saldo_corte` son los de SIGADE de `lote-c/instruments.csv`.
- `contratos/operaciones.csv` (16 filas): las 7 que el lote I había excluido, las dos ampliaciones de INS-C-0446 (RC 38 y 43), las dos de INS-I-0010 y cinco montos de conversiones con el BCRA derivados (ver abajo). Con esto el saldo de INS-C-0446 llega a cero el 2026-08-10: 3.878.320 + 35.256.166 + 37.113.987 = 76.248.473, igual al VNO comprado en la RC 47.
- `tasas.csv`, `amortizaciones.csv` y `fechas.csv` solo con encabezado; `instruments.csv` con la fila de INS-I-0010; `sources.csv`, `documents_manifest.csv`, `claims.csv` (CLM-I-076 a CLM-I-090), `unresolved.md`, `sintesis.md` y `tablas/` (derivaciones, índice inicial, unidades de SIGADE contra CER).

## Validación

`argfx validate` real (venv en la Mac) sobre el snapshot de `origin/main` más `inbox/lote-i3`: 0 errores en el lote y 0 errores nuevos; queda el error que ya tiene main (`lote-i/contratos/terminos.csv`, INS-I-0007 sin `indice_inicial` al validar el lote I aislado, que el lote I2 corrige al fusionar). Las advertencias del lote son las de siempre (sin ISIN, residencia desconocida, columnas extra en `instruments.csv`).

## Para Alejandro (detalle en `unresolved.md`)

1. **Base del CER en SIGADE.** Las unidades de SIGADE son el valor nominal dividido por el CER del día de emisión, no del décimo día hábil anterior: TXMD8 da 788,979 contra CER del 2026-06-12 de 788,979 (y del 2026-05-29 de 779,886), TZXM8 da 736,0 contra 735,986 del 2026-04-01 y TZXY7 668 contra 668,234 del 2025-12-15. Esto explica los 736 y 668 de tu nota: no hay operaciones faltantes. Cargué el índice de la norma, igual que en el lote I2; el otro valor (788,9793474221) está en `tablas/cer_indice_inicial.csv`. No toqué el lote I2.
2. **Duales con una sola pata.** TXMD8 y TXMD9 pagan el máximo entre el capital ajustado por CER y TAMAR TEM más 3%; el motor no lo expresa, así que van como CER cupón cero (como los clasifica SIGADE) y la pata TAMAR no está modelada. TMVE8 (INS-I-0005) sigue excluido por el mismo motivo.
3. **Conversiones con el BCRA con montos derivados.** Ninguna fuente oficial publica el VNO efectivo. Derivé de circulaciones y porcentajes publicados por Finanzas más el saldo de SIGADE: D31L6 entrada RC 39 (999,6 millones de USD, rango 998,0 a 1001,2), D31G6 entrada RC 39 (999,4, rango 998,4 a 1000,4), D31G6 salida RC 49 (500,6 más o menos 3), D30S6 entrada RC 49 más RC 53 (1.303,7 con el 75% del comunicado; una fuente secundaria da 75,02% y 1.302,5; no se puede separar por RC) y D30O6 entrada RC 53 (1.200 más o menos 1). Cargué los topes de la RC cuando el rango los contiene (1.000 y 1.200), 500 y 1.303; cada fila lo dice como DERIVADO. Si preferís no cargar derivados, son las filas con "DERIVADO" en `referencia`.

## Sin monto (siguen en `unresolved.md`)

BONCER 15-12-2026 entregado en la RC 39, S31G6 y T30J7 de la RC 51, S30O6 de las RC 53 y 60, y las entradas D30N6, T30A7 y T31Y7 de la RC 60: no hay circulación posterior publicada, y la hoja A.4 está en USD equivalentes a un tipo de cambio no publicado (el implícito de T31Y7, 1.488,47, no coincide con la Com. A 3500 de ningún día cercano). Con la salida del BONCER y las de LECAP sin cargar, esos saldos quedan sobrestimados. Se cierran con SIGADE al 30-09 o con un comunicado que publique la circulación de D30N6, T30A7 o T31Y7.

## Otros puntos

- Las ampliaciones de INS-C-0446 y de INS-I-0010 usan la fecha de firma de cada RC (la de colocación no figura); no cambia el cálculo.
- INS-C-0446 e INS-I-0010 llevan base ACT/360 provisional (las RC no la indican); el escenario necesita las series `SOFR_TERM_1A` y `RENDIMIENTO_RESERVAS_BCRA`.
- La reapertura de TXMD9 está fechada 2026-10-16 (adjudicada, liquidación pendiente al 2026-10-15).
- SIGADE al 30-09-2026 sigue pendiente.
