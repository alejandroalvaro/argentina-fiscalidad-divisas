# Lote U: síntesis (sin_revisar)

Todo queda `sin_revisar`. Fuentes nuevas SRC-1212 a SRC-1221 (sigue la secuencia del lote T, que terminó en SRC-1211; el bloque SRC-1900 a 1906 del lote J no se toca). Se usa también SRC-1160 (balance mensual del BCRA, lote R) como control.

## 1. Depósitos del Tesoro en el BCRA en dólares

**No existe una serie publicada en USD.** El catálogo de la API del BCRA (1610 variables, SRC-1215) solo tiene los depósitos del gobierno en el BCRA en millones de pesos: 1264 (total), 1265 (en pesos) y 1266 (en moneda extranjera, valuada en pesos) (CLM-U-001 y CLM-U-002). El Informe Monetario Mensual no trae el saldo en dólares de la cuenta del Tesoro: la fila "depósitos del sector público no financiero en dólares" del cuadro de agregados (USD 2,5 mil millones en septiembre de 2026) es otra cosa, depósitos del sector público en el sistema financiero (CLM-U-014). Los informes del programa con el FMI no se pudieron leer: el sitio del FMI devuelve 403 desde la caja y desde la Mac (ver unresolved.md).

**Serie calculada (cálculo propio sobre datos oficiales).** Saldo en moneda extranjera de la variable 1266 (millones de pesos) dividido por el tipo de cambio de valuación contable (variable 84) del mismo día (CLM-U-003 y CLM-U-004). La variable 5 (mayorista de referencia) es idéntica a la 84 en los 692 días en que están las dos; solo el 2026-10-13 usa la 5.

Controles:
- Contra el balance mensual del BCRA (SRC-1160): en los 33 fines de mes de 2024-01 a 2026-09 el saldo en pesos coincide con diferencia máxima de 0,499 millones de pesos (CLM-U-012).
- Contra tres cifras en USD de la prensa (el cálculo da 2.760,4 el 2026-09-10 contra 2.762 publicado; 1.409,5 el 2026-09-25 contra 1.409; 1.176,7 el 2026-10-05 contra 1.177): coinciden dentro de USD 2 millones (CLM-U-013 a 016, `tablas/control_contra_cifras_de_prensa.csv`). Las notas son de terceros y no son fuente de la serie.

Saldo al último día hábil de cada mes, millones de USD (`tablas/depositos_tesoro_bcra_moneda_extranjera_usd_fin_de_mes_2024-01_a_2026-10.csv`; el diario está en `..._usd_diario_2024-01-02_a_2026-10-13.csv`):

| mes | millones de USD |
|---|---|
| 2024-01 | 2.767,5 |
| 2024-02 | 1.764,9 |
| 2024-03 | 1.033,9 |
| 2024-04 | 1.083,9 |
| 2024-05 | 428,0 |
| 2024-06 | 1.033,9 |
| 2024-07 | 1.242,8 |
| 2024-08 | 835,4 |
| 2024-09 | 1.587,0 |
| 2024-10 | 1.276,0 |
| 2024-11 | 3.560,3 |
| 2024-12 | 5.994,7 |
| 2025-01 | 3.186,1 |
| 2025-02 | 2.759,7 |
| 2025-03 | 1.951,5 |
| 2025-04 | 15.447,9 |
| 2025-05 | 3.067,5 |
| 2025-06 | 4.679,8 |
| 2025-07 | 2.707,9 |
| 2025-08 | 1.685,7 |
| 2025-09 | 2.327,4 |
| 2025-10 | 91,9 |
| 2025-11 | 212,6 |
| 2025-12 | 1.969,9 |
| 2026-01 | 526,2 |
| 2026-02 | 532,8 |
| 2026-03 | 485,3 |
| 2026-04 | 1.365,1 |
| 2026-05 | 3.057,9 |
| 2026-06 | 3.919,7 |
| 2026-07 | 3.605,6 |
| 2026-08 | 2.779,1 |
| 2026-09 | 1.124,5 |
| 2026-10 | 1.229,8 |

Hitos (CLM-U-005 a 011): fin de 2024 USD 5.994,7 millones; máximo de los fines de mes en abril de 2025 (USD 15.447,9 millones); mínimo en octubre de 2025 (USD 91,9 millones); fin de 2025 USD 1.969,9 millones; fin de junio de 2026 USD 3.919,7 millones; fin de septiembre de 2026 USD 1.124,5 millones; último dato diario (2026-10-13) USD 1.229,8 millones. El mes de 2026-10 está incompleto.

**Para D-001 (reservas netas, definición del FMI):** esta serie es la que habría que mostrar como activo del Tesoro y pasivo del BCRA, y no se resta de las reservas netas del TMU. Ojo con el supuesto: el BCRA no dice en qué monedas está el saldo en moneda extranjera; la división por el tipo de cambio del dólar lo trata todo como USD.

## 2. Revisión al 2026-10-15 (21:41 hora de Brasilia)

Sin cambios respecto de los lotes S y T (`tablas/revision_sigade_finanzas_rc60_lote_u.csv`, CLM-U-017 a 019): la planilla de Finanzas del III trimestre 2026 y SIGADE al 2026-09-30 no están publicados (las páginas de Finanzas y de la ONCP son idénticas byte a byte), y no hay montos ejecutados de la RC 60/2026. El monitor de la OPC llega a la RC 59/2026.
